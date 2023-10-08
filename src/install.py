#!/usr/bin/env python3

"""
    Copyright (C) 2023  Juliandev02

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses>
"""

import os
import urllib.request
import requests
import subprocess
from sys import exit
import shutil

from colorama import Fore
from halo import Halo
import time

import sqlite3 as sql
from sqlite3 import *

from urllib.error import HTTPError
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError
from yaml.scanner import ScannerError

from init import *
from src.functions import delete_last_line, lock
from src.plugin_daemon import PluginDaemon, is_plugin_enabled
from src.force_no_sandbox import *
from src.package_manager import *

import yaml
from yaml import SafeLoader


# Try to connect to the locally saved main package database
try:
    db = sql.connect(Files.package_database)
    c  = db.cursor()

# If the Database doesn't exists/no entries, return a error
except OperationalError:
    pass

if is_plugin_enabled("sandbox"):
    PluginDaemon.import_plugin("sandbox")


# Check if user config path exists
if not os.path.exists(Directories.user_config):
    os.mkdir(Directories.user_config)
    user_config = {
        "sandbox": {
            "bootstrap_location": f"{home_dir}/.local/share/spkg/sandbox/",
            "handler": "bwrap"
        }
    }
    
    with open(Files.user_config, 'w') as file:
        yaml.dump(user_config, file)


class Sandbox:
    bootstrap_location = user_config['sandbox']['bootstrap_location']
    sandbox_handler = user_config['sandbox']['handler']

class InstallManager:
    """ 
        **** INSTALL FUNCTION ****
        This function installs packages, depending on various plugins, e.g. if the sandbox is enabled or not. 
    """
    class Installer:
        def __init__(self, package_name):
            self.package_name = package_name
            
        # Fetch url
        def fetch_url(self, url):
            try:
                request = urllib.request.Request(
                    url,
                    data = None,
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                )
                
                return urllib.request.urlopen(request)
                
            except Exception as e:
                print("")
                delete_last_line()
                # print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(f"{RED + Colors.BOLD}[×]{RESET} {Fore.RESET + Colors.RESET}{Colors.BOLD}{StringLoader('Get')}: {url}")
                print(StringLoader("HttpError"))
                exit()
                
        
        # Return file size from a given url response
        def file_size(self, response, type: FileSizes):
            file_size_bytes = int(response.headers.get('Content-Length', 0))
            
            if type == FileSizes.Megabytes:
                return file_size_bytes / (1024 * 1024)
            
            elif type == FileSizes.Kilobytes:
                return file_size_bytes / 1024
            

        # Save a file 
        def file_saving(self, input, output, file_extension: str = "", warn_force_no_sandbox: bool = True):
            # Check if the sandbox plugin is enabled
            if is_plugin_enabled("sandbox"):
                
                # If the package needs to be installed natively, continue the installation without the sandbox plugin
                if force_no_sandbox(self.package_name):
                    # Alternative Warn message
                    if warn_force_no_sandbox:
                        print(f"\n{StringLoader('ForceNoSandbox')}")
                        time.sleep(3)
                    
                    # Save local and not in the sandbox
                    with open(f"{output}.{file_extension}", 'wb') as file:
                        file.write(input.read())
                
                # If package can be installed in sandbox, save file to sandbox 
                else:
                    with open(f"{Sandbox.bootstrap_location}{output}.{file_extension}", 'wb') as file:
                        file.write(input.read())
            
            # If sandbox is not enabled save locally
            else:
                with open(f"{output}.{file_extension}", 'wb') as file:
                        file.write(input.read())
                        
        # return a file location      
        def file(self, input):
            if is_plugin_enabled("sandbox"):
                if force_no_sandbox(self.package_name):
                    return input

                else:
                    return Sandbox.bootstrap_location + input
            
            else:
                return input
        
        

        def get_package_manager(self):
            try:
                output = subprocess.check_output(["which", "apt"]).decode("utf-8")
                if "apt" in output:
                    return PackageManagers.Apt
            except subprocess.CalledProcessError:
                pass
            
            try:
                output = subprocess.check_output(["which", "apk"]).decode("utf-8")
                if "apk" in output:
                    return PackageManagers.Apk
            except subprocess.CalledProcessError:
                pass
            
            try:
                output = subprocess.check_output(["which", "dnf"]).decode("utf-8")
                if "dnf" in output:
                    return PackageManagers.Dnf
            except subprocess.CalledProcessError:
                pass
            
            return False
    
        def cleanup(self):
            shutil.rmtree(config["build_directory"])
            os.remove("/tmp/specfile.yml")
            
            for package_file in os.listdir("/tmp/"):
                if package_file.startswith('package'):
                    file = os.path.join("/tmp/", package_file)
                    os.remove(file)
        
        
        def install(self, args):
            # Create and start the spinner for searching the database
            spinner = Halo(text=f"{StringLoader('SearchingDatabaseForPackage')}",
                            spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                            text_color="white",
                            color="green")
                
            spinner.start()
            
            c.execute("SELECT arch FROM packages where name = ?", (self.package_name,))
            
            try:
                result = c.fetchone()[0]
                lock(type=Procedure.Install)
                
            except TypeError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader('PackageNotFound'))
                exit()
            
            except PermissionError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(f"{Fore.CYAN + Colors.BOLD}{Files.lockfile}: {Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsLockfile'))
                exit()
            
            try:
                if result == "all":
                    c.execute("SELECT name, version, url, filename, specfile FROM packages where name = ?", (self.package_name,))

                else:
                    c.execute("SELECT name, version, url, filename, specfile FROM packages where name = ? AND arch = ?", (self.package_name, arch))
                    
            except OperationalError:
                    print(StringLoader("PackageDatabaseNotSynced"))
                    exit()
            
            try:     
                for row in c:
                    class Package:
                        Name        = row[0]
                        Version     = row[1]
                        Url         = row[2]
                        Filename    = row[3]
                        Specfile    = row[4]
                    
                    headers = requests.head(Package.Url)
                    file_size = round(self.file_size(response=headers, type=FileSizes.Megabytes), 2)
                    
                    spinner.stop()
                    print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingDatabaseForPackage')}")
                    
                    if not "-y" in args:
                        try:
                            cont_package_install = input(f"{StringLoader('ContinuePackageInstallation', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")

                        except KeyboardInterrupt as e:
                            print(f"\n{RESET}{StringLoader('Abort')}")
                            exit()

                        if not cont_package_install.lower() in ["y", "j", "yes", "ja"]:
                            print(RESET + StringLoader("Abort"))
                            exit()
                    else:
                        print(f"{StringLoader('ContinuePackageInstallationCompact', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")
                        
                    download_time_start = time.time()
                    
                    spinner = Halo(
                        text=f"{StringLoader('GettingSpecfile')}",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    specfile = self.fetch_url(Package.Specfile)
                    self.file_saving(input=specfile, output="/tmp/specfile", file_extension="yml", warn_force_no_sandbox=False)
                    
                    spinner.stop()
                    
                    print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET}{StringLoader('GettingSpecfile')}")

                    spinner = Halo(
                        text=f"{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    with open("/tmp/specfile.yml") as file:
                        package = yaml.load(file, Loader=SafeLoader)
                    
                    file = self.fetch_url(Package.Url)
                    self.file_saving(input=file, output=f"/tmp/package", file_extension=package["Flags"]["ArchiveType"], warn_force_no_sandbox=True)
                    
                    spinner.stop()
                    
                    print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET}{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})")

                    download_time_end = time.time()
                    
                    print(f"{StringLoader('FinishedDownloading')} {Fore.CYAN + Colors.BOLD}{Package.Filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
                    
                    time.sleep(.4)
                    
                    install_time_start = time.time()

                    spinner = Halo(
                        text=f"{StringLoader('ParsingSpecfile')}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    SpecName        = package["Name"]
                    SpecVersion     = package["Version"]
                    SpecArch        = package["Architecture"]
                    SpecDeps        = package["Dependencies"]
                    SpecFlags       = package["Flags"]
                    
                    class Commands:
                        Install        = package["Install"]["Commands"]
                        Remove         = package["Remove"]["Commands"]
                        Upgrade        = package["Upgrade"]["Commands"]
                        try: Compile   = package["Compile"]["Commands"]
                        except: pass
                    
                    spinner.stop()
                    
                    print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('SuccessParsingSpecfile')}")
                    
                    time.sleep(.1)
                    
                    dep_start_time = time.time()

                    spinner = Halo(
                        text=f"{StringLoader('DeterminateDependencies')} {Colors.BOLD}({get_package_manager()}){Colors.RESET}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    package_manager = get_package_manager()
                    
                    match package_manager:
                        case PackageManagers.Apt:
                            apt_install(SpecDeps["Apt"].split(" "), print_output=False)
                            deps = SpecDeps["Apt"]
                            
                        case PackageManagers.Apk:
                            apk_install(SpecDeps["Apk"].split(" "), print_output=False)
                            deps = SpecDeps["Apk"]
                            
                        case PackageManagers.Dnf:
                            dnf_install(SpecDeps["Dnf"].split(" "), print_output=False)
                            deps = SpecDeps["Dnf"]
                        
                        case PackageManagers.Pip:
                            pip_install(SpecDeps["Pip"].split(" "), print_output=False)
                            deps = SpecDeps["Pip"]
                        
                        case _:
                            exit()
                
                    spinner.stop() 

                    dep_end_time = time.time()
                    
                    print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('SuccessDeterminateDependencies', argument_1=round(dep_end_time - dep_start_time, 2))} {Colors.BOLD}({get_package_manager()}){Colors.RESET}")
                    print(f"{Fore.GREEN + Colors.BOLD}↳   {Fore.RESET + Colors.RESET}{Colors.ITALIC}{deps}{Colors.RESET}")
                                        
                    spinner = Halo(
                        text=f"{StringLoader('DeterminatePipDependencies')}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    try:
                        SpecDeps["Pip"].split(" ")
                        spinner.stop()
                    
                        dep_start_time = time.time()

                        spinner = Halo(
                        text=f"{StringLoader('NeedPipDependencies')}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                        spinner.start()
                        
                        pip_install(SpecDeps["Pip"].split(" "), print_output=False)
                        
                        spinner.stop()

                        dep_end_time = time.time()

                        print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('SuccessPipDeterminateDependencies', argument_1=round(dep_end_time - dep_start_time, 2))}")
                        print(f"{Fore.GREEN + Colors.BOLD}↳   {Fore.RESET + Colors.RESET}{Colors.ITALIC}{SpecDeps['Pip']}{Colors.RESET}")
                        
                    except:
                            spinner.stop()
                            print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('NoNeedPipDependencies')} {Colors.BOLD}{Colors.RESET}")
                    
                    spinner = Halo(
                        text=f"{StringLoader('ExtractArchive')}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    file_extension = SpecFlags["ArchiveType"]
                    
                    match file_extension:
                        case "tar": 
                            import tarfile
                            
                            with tarfile.open(f"/tmp/package.{file_extension}", 'r') as tar:
                                tar.extractall(path=config["build_directory"])
                                
                        case "tar.gz" | "gz": 
                            import tarfile
                            
                            with tarfile.open(f"/tmp/package.{file_extension}", 'r:gz') as tar:
                                tar.extractall(path=config["build_directory"])
                                
                        case _:
                            fe_unsupported = True
                            spinner.stop()
                            print("")
                            delete_last_line()
                            print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('ExtractArchive')}")
                            print(StringLoader('ExtractError'))
                            self.cleanup()
                            exit()
                    
                    time.sleep(4)               
                    spinner.stop()
                    
                    print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('SuccessExtractArchive')}")
                    
                    
                    spinner = Halo(
                    text=f"{StringLoader('PrepareCompile')}",
                    spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                    text_color="white",
                    color="green")
                
                    spinner.start()

                    try:
                        requires_compile = SpecFlags["RequiresCompile"]
                        if not requires_compile:
                            spinner.stop()
                            print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('NoCompileNeed')} {Colors.BOLD}{Colors.RESET}")

                        else:
                            print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Compile')} {Colors.BOLD}{Colors.RESET}")
                            os.chdir(config["build_directory"])
                            compile_command = Commands.Compile
                            
                            try:
                                for command in compile_command:
                                    subprocess.run(command, shell=True, check=True, text=True)

                            except Exception as e: 
                                print(StringLoader('InstallationError', argument_1=e))
                                self.cleanup()
                                exit()

                    except:
                        spinner.stop()
                        print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('NoCompileNeed')} {Colors.BOLD}{Colors.RESET}")
                    

                    spinner = Halo(
                    text=f"{StringLoader('PrepareInstall')}",
                    spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                    text_color="white",
                    color="green")
                
                    spinner.start()
                    
                    install_command = Commands.Install
                    
                    spinner.stop()
                    print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('PrepareInstall')} {Colors.BOLD}{Colors.RESET}")
                    
                    print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Install')} {Colors.BOLD}{Colors.RESET}")

                    try:
                        try:
                            os.chdir(f"{config['build_directory']}{package['Install']['WorkDir']}")
                        except: 
                            pass
                        
                        shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            
                        for command in install_command:
                            # subprocess.run(command, shell=True, check=True, text=True)
                            # os.system(command)
                            shell.stdin.write(command + '\n')
                            shell.stdin.flush()
                        
                        # Lies die Ausgabe der Shell (könnte stdout und stderr sein)
                        output, errors = shell.communicate()

                        # Gib die Ausgabe aus
                        print("Ausgabe:")
                        print(output)

                        # Gib Fehler aus, falls vorhanden
                        print("Fehler:")
                        print(errors)

                        # Beende die Shell
                        shell.terminate()

                    except Exception as e: 
                        print(StringLoader('InstallationError', argument_1=e))
                        self.cleanup()
                        exit()

                    install_time_end = time.time()
                    
                    if not "-k" in args or "--keep" in args:
                        self.cleanup()
                        
                    print(StringLoader('SuccessInstall', argument_1=self.package_name, argument_2=round(install_time_end - install_time_start, 2)))
                    
            except NameError as e:
                print(StringLoader('PackageNotFound'))
                self.cleanup()
                exit()

            except PermissionError:
                print("")   
                delete_last_line()
                print(f"{Fore.CYAN + Colors.BOLD}/tmp/: {Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsLockfile'))
                self.cleanup()
                exit()
            
            except ScannerError:
                spinner.stop()
                delete_last_line()
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('GettingSpecfile')}")
                print(StringLoader("ParsingError"))
                self.cleanup()
                exit()
                
            except (HTTPError, ConnectionError, NewConnectionError, MaxRetryError) as e:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader("HttpError"))
                self.cleanup()
                exit()
                               
            
#     """ 
#         **** SANDBOX INSTALL FUNCTION ****
#         This function installs the package to the sandbox environment, without checking if the sandbox is enabled or not. 
#         INFO: You need to have the sandbox INSTALLED.
#     """
#     def sandbox_install(name):
#         # Check if package needs to be installed natively, if true, cancel the installation
#         if force_no_sandbox(name) == 1:
#                 print(ForceNoSandbox)
#                 print(Abort)
#                 exit()
        
#         # Print an information that the package will be installed to the sandbox environment
#         print(InstallingToSandboxEnv)
        
#         # Start the spinner for the package database search
#         spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
#                                 'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
#         spinner_db_search.start()

#         # Select architecture of package where package name
#         c.execute("SELECT arch FROM packages where name = ?", (name,))

#         # fetch the results
#         try:
#             result = c.fetchone()[0]

#         except TypeError:
#             print(PackageNotFound)
#             exit()
        
#         # If the package_architecture is all, try to find the corresponding package
#         if result == "all":
#             try:
#                 c.execute(
#                     "SELECT name, version, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

#             except OperationalError:
#                 print(PackageDatabaseNotSynced)
#                 exit()
                
#         # If not, try to find the corresponding package depending on the available architecture
#         else:
#             try:
#                 c.execute(
#                     "SELECT name, version, fetch_url, file_name, setup_script FROM packages where name = ? AND arch = ?", (name, arch))

#             except OperationalError:
#                 print(PackageDatabaseNotSynced)
#                 exit()

#         # For-loop the results
#         for row in c:
#             package_name = row[0]
#             package_version = row[1]
#             package_url = row[2]
#             filename = row[3]
#             pkgbuild_url = row[4]    

#             # get the response of the package header
#             response = requests.head(package_url)
            
#             # fetch the size of the package and convert it to mbytes 
#             file_size_bytes = int(response.headers.get('Content-Length', 0))
#             file_size_mb = file_size_bytes / (1024 * 1024)

#             # stop the spinner
#             spinner_db_search.stop()
#             print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
            
#             # ask if you want to continue the installation
#             try:
#                 continue_pkg_installation = input(
#                     f"{ContinePackageInstallation1}{package_name} ({package_version}){Colors.RESET}{ContinePackageInstallation2}{round(file_size_mb, 2)} MB{ContinePackageInstallation3} ")

#             # If you press ^C, it prints out a error message
#             except KeyboardInterrupt as e:
#                 print(f"\n{Canceled}")
#                 exit()

#             # Check if you want to continue the installation
#             if continue_pkg_installation.lower() == "j":
#                 continue

#             elif continue_pkg_installation.lower() == "y":
#                 continue
            
#             elif continue_pkg_installation.lower() == "":
#                 continue
            
#             # If you press any other key, it prints out an error message
#             else:
#                 print(Abort)
#                 exit()
                
#         # Try to request the package url 
#         try:
#             package_request = urllib.request.Request(
#                 package_url,
#                 data=None,
#                 headers={
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#                 }
#             )

#             package_file = urllib.request.urlopen(package_request)

#             # Start the download timer
#             download_time_start = time.time()

#             # Start download spinner
#             spinner_package = Halo(text=f"{StrGet}: {Fore.CYAN + Colors.BOLD + package_name + Fore.RESET} ({package_url})", spinner={'interval': 150, 'frames': [
#                         '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
#             spinner_package.start()
            
#             # Write the package archive to the sandbox environment
#             with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
#                 file.write(package_file.read())
            
#             # Stop the download timer
#             download_time_end = time.time()
            
#             # Print download finished message
#             print(f"\n{FinishedDownloading} {Fore.LIGHTCYAN_EX + Colors.BOLD}{filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
            
#             # Stop download spinner
#             spinner_package.stop()
#             spinner_package.stop()
#             spinner_package.stop()
        
#             # Start the setup spinner
#             spinner_setup = Halo(text=f"{ExecutingSetup}: {package_url}", spinner={'interval': 150, 'frames': [
#                 '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
#             spinner_setup.start()

#             # request the setup url 
#             setup_request = urllib.request.Request(
#                 pkgbuild_url,
#                 data=None,
#                 headers={
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#                 }
#             )

#             pkgbuild_file = urllib.request.urlopen(setup_request)

#             # Write the PKBUILD File to the sandbox environment
#             with open(f"{bootstrap_location}/tmp/PKGBUILD", 'wb') as file_setup:
#                 file_setup.write(pkgbuild_file.read())
                
#              # Stop the Setup Spinner
#             spinner_setup.stop()
#             print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

#             # Execute the PKGBUILD File in the sandbox environment
#             os.system(f"sudo chroot {bootstrap_location} bash /tmp/PKGBUILD --install")

#         # Catch HTTPError, NameError and KeyboardInterrupt errors
#         except HTTPError as e:
#             print()
#             print(Str[lang]["HttpError"])
#             exit()

#         except NameError as e:
#             print(f"\n{PackageNotFound}")
#             exit()

#         except KeyboardInterrupt as e:
#             print(f"\n{Canceled}")
#             exit()
            
            
            
#     """ 
#         **** UPGRADE FUNCTION ****
#         This function upgrades packages, depending on various plugins, e.g. if the sandbox is enabled or not. 
#     """
#     def upgrade(name):
#         # Create and start the spinner for searching the database
#         spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
#                                 'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
#         spinner_db_search.start()

#         # Select architecture of package where package name
#         c.execute("SELECT arch FROM packages where name = ?", (name,))

#         # fetch the results
#         try:
#             result = c.fetchone()[0]

#         except TypeError:
#             print(PackageNotFound)
#             exit()

#         # If the package_architecture is all, try to find the corresponding package
#         if result == "all":
#             try:
#                 c.execute(
#                     "SELECT name, version, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

#             except OperationalError:
#                 print(PackageDatabaseNotSynced)
#                 exit()
                
#         # If not, try to find the corresponding package depending on the available architecture
#         else:
#             try:
#                 c.execute(
#                     "SELECT name, version, fetch_url, file_name, setup_script FROM packages where name = ? AND arch = ?", (name, arch))

#             except OperationalError:
#                 print(PackageDatabaseNotSynced)
#                 exit()

#         # For-loop the results
#         for row in c:
#             package_name = row[0]
#             package_version = row[1]
#             package_url = row[2]
#             filename = row[3]
#             pkgbuild_url = row[4]    

#             # get the response of the package header
#             response = requests.head(package_url)
            
#             # fetch the size of the package and convert it to mbytes 
#             file_size_bytes = int(response.headers.get('Content-Length', 0))
#             file_size_mb = file_size_bytes / (1024 * 1024)

#             # stop the spinner
#             spinner_db_search.stop()
#             print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
            
#             # ask if you want to continue the installation
#             try:
#                 continue_pkg_installation = input(
#                     f"{ContinePackageInstallation1}{package_name} ({package_version}){Colors.RESET}{ContinePackageInstallation2}{round(file_size_mb, 2)} MB{ContinePackageInstallation3} ")

#             # If you press ^C, it prints out a error message
#             except KeyboardInterrupt as e:
#                 print(f"\n{Canceled}")
#                 exit()

#             # Check if you want to continue the installation
#             if continue_pkg_installation.lower() == "j":
#                 continue

#             elif continue_pkg_installation.lower() == "y":
#                 continue
            
#             elif continue_pkg_installation.lower() == "":
#                 continue
            
#             # If you press any other key, it prints out an error message
#             else:
#                 print(Abort)
#                 exit()
                
#         # Try to request the package url 
#         try:
#             package_request = urllib.request.Request(
#                 package_url,
#                 data=None,
#                 headers={
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#                 }
#             )

#             package_file = urllib.request.urlopen(package_request)
            
#             # Start the download timer
#             download_time_start = time.time()

#             # Start download spinner
#             spinner_package = Halo(text=f"{StrGet}: {Fore.CYAN + Colors.BOLD + package_name + Fore.RESET} ({package_url})", spinner={'interval': 150, 'frames': [
#                         '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
#             spinner_package.start()
            
#             # Check if the sandbox plugin is enabled
#             if check_plugin_enabled_silent("sandbox") == True:
                
#                 # If the package needs to be installed natively, continue the installation without the sandbox plugin
#                 if force_no_sandbox(name) == 1:
#                     print()
#                     print(ForceNoSandbox)
#                     time.sleep(5)
#                     with open(f"/tmp/{filename}", 'wb') as file:
#                         file.write(package_file.read())
                
#                 # If not just continue with the sandbox plugin   
#                 else:
#                     with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
#                         file.write(package_file.read())
            
#             # (M) Else 
#             else:
#                 # (A) (M) Check if the sandbox plugin is enabled
#                 if check_plugin_enabled_silent("sandbox") == True:
#                     with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
#                         file.write(package_file.read())

#                 # If not, save the package natively
#                 else:
#                     with open(f"/tmp/{filename}", 'wb') as file:
#                         file.write(package_file.read())

#             # Stop the download timer
#             download_time_end = time.time()
            
#             # Print download finished message
#             print(f"\n{FinishedDownloading} {Fore.LIGHTCYAN_EX + Colors.BOLD}{package_name}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
            
#             # Stop download spinner
#             spinner_package.stop()
#             spinner_package.stop()
#             spinner_package.stop()

#             # Start the setup spinner
#             spinner_setup = Halo(text=f"{ExecutingSetup}...", spinner={'interval': 150, 'frames': [
#                 '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
#             spinner_setup.start()
        
#             # request the setup url 
#             setup_request = urllib.request.Request(
#                 pkgbuild_url,
#                 data=None,
#                 headers={
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#                 }
#             )

#             pkgbuild_file = urllib.request.urlopen(setup_request)

#             # If the package needs to be installed natively, continue the installation without the sandbox plugin
#             if force_no_sandbox(name) == 1:
#                     with open("/tmp/PKGBUILD", 'wb') as file_setup:
#                         file_setup.write(pkgbuild_file.read())
            
#             # Else check if the sandbox plugin is enabled
#             else:
#                 if check_plugin_enabled_silent("sandbox") == True:
#                     with open(f"{bootstrap_location}/tmp/PKGBUILD", 'wb') as file_setup:
#                         file_setup.write(pkgbuild_file.read())
                        
#                 # If not, save the PKGBUILD file natively
#                 else:
#                     with open("/tmp/PKGBUILD", 'wb') as file_setup:
#                         file_setup.write(pkgbuild_file.read())

#             # Stop the Setup Spinner
#             spinner_setup.stop()
#             print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

#             # Execute the PKGBUILD File natively if the package needs to be installed natively
#             if force_no_sandbox(name) == 1:
#                 subprocess.run(['sudo', 'chmod', '+x', '/tmp/PKGBUILD'])
#                 subprocess.run(['sudo', 'bash', '/tmp/PKGBUILD', '--upgrade'])
            
#             # Else check if the sandbox plugin is enabled
#             else:
#                 if check_plugin_enabled_silent("sandbox") == True:
#                     os.system(f"sudo chroot {bootstrap_location} bash /tmp/PKGBUILD --upgrade")
                    
#                 # If not, run the PKGBUILD file natively
#                 else:
#                     subprocess.run(['sudo', 'chmod', '+x', '/tmp/PKGBUILD'])
#                     subprocess.run(['sudo', 'bash', '/tmp/PKGBUILD', '--upgrade'])

#         # Catch HTTPError, NameError and KeyboardInterrupt errors
#         except HTTPError as e:
#             print()
#             print(Str[lang]["HttpError"])
#             exit()

#         except NameError as e:
#             print(f"\n{PackageNotFound}")
#             exit()

#         except KeyboardInterrupt as e:
#             print(f"\n{Canceled}")
#             exit()


# # # Upgrade
# # def upgrade(name):
# #     spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
# #                              'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
# #     spinner_db_search.start()

# #     c.execute("SELECT arch FROM packages where name = ?", (name,))

# #     try:
# #         result = c.fetchone()[0]

# #     except TypeError:
# #         print(f"\n{PackageNotFound}")
# #         exit()

# #     if result == "all":
# #         try:
# #             c.execute(
# #                 "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

# #         except OperationalError:
# #             print(PackageDatabaseNotSynced)
# #             exit()

# #     else:
# #         try:
# #             c.execute(
# #                 "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ? AND arch = ?", (name, arch))

# #         except OperationalError:
# #             print(PackageDatabaseNotSynced)
# #             exit()

# #     for row in c:
# #         url = row[1]
# #         filename = row[2]
# #         setup_script = row[3]

# #         response = requests.head(url)
# #         file_size_bytes = int(response.headers.get('Content-Length', 0))
# #         file_size_mb = file_size_bytes / (1024 * 1024)

# #         spinner_db_search.stop()
# #         print(
# #             f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
# #         try:
# #             continue_pkg_installation = input(
# #                 f"{ContinePackageInstallation1}{filename}{Colors.RESET}{ContinePackageInstallation2}{round(file_size_mb, 2)} MB{ContinePackageInstallation3} ")

# #         except KeyboardInterrupt as e:
# #             print(f"\n{Canceled}")
# #             exit()

# #         if continue_pkg_installation.lower() == "j":
# #             continue

# #         elif continue_pkg_installation.lower() == "y":
# #             continue

# #         else:
# #             print(Abort)
# #             exit()

# #     try:
# #         req = urllib.request.Request(
# #             url,
# #             data=None,
# #             headers={
# #                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# #             }
# #         )

# #         f = urllib.request.urlopen(req)

# #         download_time_start = time.time()

# #         spinner = Halo(text=f"{StrGet}: {url}", spinner={'interval': 150, 'frames': [
# #                        '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
# #         spinner.start()
        
# #         if check_plugin_enabled_silent("sandbox") == True:
# #             if force_no_sandbox(name) == 1:
# #                 print()
# #                 print(ForceNoSandbox)
# #                 time.sleep(5)
# #                 with open(f"/tmp/{filename}", 'wb') as file:
# #                     file.write(f.read())
                    
# #             else:
# #                 with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
# #                     file.write(f.read())
# #         else:
# #             if check_plugin_enabled_silent("sandbox") == True:
# #                 with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
# #                     file.write(f.read())

# #             else:
# #                 with open(f"/tmp/{filename}", 'wb') as file:
# #                     file.write(f.read())

# #         download_time_end = time.time()
# #         print(f"\n{FinishedDownloading} {Fore.LIGHTCYAN_EX + Colors.BOLD}{filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")

# #         spinner_setup = Halo(text=f"{ExecutingSetup}: {url}", spinner={'interval': 150, 'frames': [
# #             '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
# #         spinner_setup.start()

# #         setup_req = urllib.request.Request(
# #             setup_script,
# #             data=None,
# #             headers={
# #                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# #             }
# #         )

# #         f_setup = urllib.request.urlopen(setup_req)
        
# #         if force_no_sandbox(name) == 1:
# #                 with open(f"/tmp/{row[0]}.setup", 'wb') as file_setup:
# #                     file_setup.write(f_setup.read())
                    
# #         else:
# #             if check_plugin_enabled_silent("sandbox") == True:
# #                 with open(f"{bootstrap_location}/tmp/{row[0]}.setup", 'wb') as file_setup:
# #                     file_setup.write(f_setup.read())

# #             else:
# #                 with open(f"/tmp/{row[0]}.setup", 'wb') as file_setup:
# #                     file_setup.write(f_setup.read())

# #         spinner_setup.stop()
# #         print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

# #         spinner.stop()

# #         if force_no_sandbox(name) == 1:
# #             subprocess.run(['sudo', 'chmod', '+x', f'/tmp/{row[0]}.setup'])
# #             subprocess.run(['sudo', 'bash', f'/tmp/{row[0]}.setup', '--upgrade'])
            
# #         else:
# #             if check_plugin_enabled_silent("sandbox") == True:
# #                 os.system(f"sudo chroot {bootstrap_location} bash /tmp/{row[0]}.setup --upgrade")

# #             else:
# #                 subprocess.run(['sudo', 'chmod', '+x', f'/tmp/{row[0]}.setup'])
# #                 subprocess.run(['sudo', 'bash', f'/tmp/{row[0]}.setup', '--upgrade'])

# #     except HTTPError as e:
# #             print()
# #             print(HttpError)
# #             exit()

# #     except NameError as e:
# #         print(f"\n{PackageNotFound}")
# #         exit()

# #     except KeyboardInterrupt as e:
# #         print(f"\n{Canceled}")
# #         exit()
        
