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
from src.plugin import PluginDaemon, is_plugin_enabled
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


# Try to connect to the world database
try:
    wdb = sql.connect(Files.world_database)
    wc  = wdb.cursor()

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

class RemoveManager:
    """ 
        **** REMOVE FUNCTION ****
        This function removes packages, depending on various plugins, e.g. if the sandbox is enabled or not. 
    """
    class Remove:
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
        
        
        # get package manager
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

        
        # Clean temporary files
        def cleanup(self):
            try:
                shutil.rmtree(config["build_directory"])
                os.remove("/tmp/specfile.yml")
                
                for package_file in os.listdir("/tmp/"):
                    if package_file.startswith('package'):
                        file = os.path.join("/tmp/", package_file)
                        os.remove(file)
            except:
                pass
        
        
        # World database insertion
        def remove_world(self):
            try:
                c.execute("SELECT name, version, branch FROM packages where name = ?", (self.package_name,))
                for row in c:
                    name = row[0]
                    version = row[1]
                    branch = row[2]

            except OperationalError:
                print(StringLoader("PackageDatabaseNotSynced"))
                exit()
                
            try:
                wc.execute("DELETE FROM world WHERE name = ? AND version = ? AND branch = ?", (name, version, branch))
                wdb.commit()
                
            except OperationalError:
                print(StringLoader("WorldDatabaseNotBuilded"))
                exit()
            
            except PermissionError:
                print(f"{Fore.CYAN + Colors.BOLD}{Files.world_database}{Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsWorldDatabaseInsert'))
                exit()
        
        """
            MAIN REMOVE FUNCTION
        """
        def remove(self, args):
            # Create and start the spinner for searching the database
            spinner = Halo(text=f"{StringLoader('SearchingDatabaseForPackage')}",
                            spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                            text_color="white",
                            color="green")
                
            spinner.start()
            
            # Search for the architecture
            c.execute("SELECT arch FROM packages where name = ?", (self.package_name,))
            
            # fetch the result and try to lock the lockfile
            try:
                result = c.fetchone()[0]
                lock(type=Procedure.Remove)
            
            # Error Handling for TypeError
            except TypeError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader('PackageNotFound'))
                exit()
            
            # Error Handling for PermissionError
            except PermissionError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(f"{Fore.CYAN + Colors.BOLD}{Files.lockfile}: {Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsLockfile'))
                exit()
            
            # fetch name, version, url from the package database
            try:
                if result == "all":
                    c.execute("SELECT name, version, url, filename, specfile FROM packages where name = ?", (self.package_name,))

                else:
                    c.execute("SELECT name, version, url, filename, specfile FROM packages where name = ? AND arch = ?", (self.package_name, arch))
                    
            except OperationalError:
                    print(StringLoader("PackageDatabaseNotSynced"))
                    exit()
            
            # fetch the results
            try:     
                for row in c:
                    class Package:
                        Name        = row[0]
                        Version     = row[1]
                        Url         = row[2]
                        Filename    = row[3]
                        Specfile    = row[4]
                    
                    # request the package headers and get the file size
                    headers = requests.head(Package.Url)
                    file_size = round(self.file_size(response=headers, type=FileSizes.Megabytes), 2)
                    
                    spinner.stop()
                    print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingDatabaseForPackage')}")
                    
                    # ask if you want to continue the package installation (only if you dont have passed -y flag)
                    if not "-y" in args:
                        try:
                            cont_package_install = input(f"{StringLoader('ContinuePackageUninstallation', argument_1=self.package_name)}{Colors.RESET}{GREEN}")

                        except KeyboardInterrupt as e:
                            print(f"\n{RESET}{StringLoader('Abort')}")
                            exit()

                        if not cont_package_install.lower() in ["y", "j", "yes", "ja"]:
                            print(RESET + StringLoader("Abort"))
                            exit()
                    else:
                        print(f"{StringLoader('ContinuePackageUninstallationCompact', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")
                        
                    download_time_start = time.time()
                    
                    spinner = Halo(
                        text=f"{StringLoader('GettingSpecfile')}",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    # fetch specfile and save it
                    specfile = self.fetch_url(Package.Specfile)
                    self.file_saving(input=specfile, output="/tmp/specfile", file_extension="yml", warn_force_no_sandbox=False)
                    
                    spinner.stop()
                    
                    print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET}{StringLoader('GettingSpecfile')}")
                    
                    # oprn specfile and get the file extension for saving the package archive
                    with open("/tmp/specfile.yml") as file:
                        package = yaml.load(file, Loader=SafeLoader)
                    
                    try:
                        require_archive = package["Flags"]["RequiresArchiveForUninstall"]
                    except:
                        require_archive = False
                    
                    if require_archive:
                        print(StringLoader('RequiresArchiveForUninstall'))
                        spinner = Halo(
                        text=f"{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                        spinner.start()
                        # get package archive
                        file = self.fetch_url(Package.Url)
                        self.file_saving(input=file, output=f"/tmp/package", file_extension=package["Flags"]["ArchiveType"], warn_force_no_sandbox=True)
                        
                        spinner.stop()
                        
                        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET}{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})")

                        download_time_end = time.time()
                        
                        print(f"{StringLoader('FinishedDownloading')} {Fore.CYAN + Colors.BOLD}{Package.Filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
                        
                        time.sleep(.4)
                        
                    remove_time_start = time.time()

                    spinner = Halo(
                        text=f"{StringLoader('ParsingSpecfile')}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    # Start parsing specfile
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
                    
                    # get package manager
                    package_manager = get_package_manager()
                    
                    _apt_update = False
                    
                    if "-au" in  args or "--aptupdate" in args:
                        _apt_update = True
                        
                    apt_support = apk_support = dnf_support = pip_support = True
                    
                    # case-switch for package managers
                    match package_manager:
                        case PackageManagers.Apt:
                            try:
                                deps = SpecDeps["Apt"]
                            except Exception as e: 
                                print("APT UNSUPPORTED")
                                apt_support = False
                            
                        case PackageManagers.Apk:
                            try:
                                deps = SpecDeps["Apk"]
                            except: 
                                print("APK UNSUPPORTED")
                                apk_support = False
                            
                        case PackageManagers.Dnf:
                            try:
                                deps = SpecDeps["Dnf"]
                            except: 
                                print("DNF UNSUPPORTED")
                                dnf_support = False
                        
                        case PackageManagers.Pip:
                            try:
                                deps = SpecDeps["Pip"]
                            except: 
                                print("PIP UNSUPPORTED")
                                pip_support = False
                        
                        case _:
                            pass
                    
                    # if no package manager is supported, (for whatever reason, shouldnt happen) exit
                    if (apt_support and apk_support and dnf_support and pip_support) == False:
                        exit()
                
                    print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('RemoveDependenciesForYourself')} {Colors.BOLD}{Colors.RESET}")
                    print(f"{Fore.GREEN + Colors.BOLD}↳   {Fore.RESET + Colors.RESET}{Colors.ITALIC}{deps}{Colors.RESET}")

                    if require_archive:
                        spinner = Halo(
                            text=f"{StringLoader('ExtractArchive')}",
                            spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                            text_color="white",
                            color="green")
                        
                        spinner.start()
                        
                        # get file extension of archive
                        file_extension = SpecFlags["ArchiveType"]
                        
                        # case-switch for file extensions
                        match file_extension:
                            case "tar": 
                                import tarfile
                                
                                with tarfile.open(f"/tmp/package.{file_extension}", 'r') as tar:
                                    tar.extractall(path=config["build_directory"])
                                    
                            case "tar.gz" | "gz": 
                                import tarfile
                                
                                with tarfile.open(f"/tmp/package.{file_extension}", 'r:gz') as tar:
                                    tar.extractall(path=config["build_directory"])
                                
                            # if file extension is unsupported exit    
                            case _:
                                fe_unsupported = True
                                spinner.stop()
                                print("")
                                delete_last_line()
                                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('ExtractArchive')}")
                                print(StringLoader('ExtractError'))
                                self.cleanup()
                                exit()
                        
                        spinner.stop()
                        
                        print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('SuccessExtractArchive')}")
                    

                    # prepare remove
                    remove_command = Commands.Remove
                    
                    
                    print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Remove')} {Colors.BOLD}{Colors.RESET}")

                    try:
                        # try to change to the (maybe) passed workdir
                        try:
                            os.chdir(f"{config['build_directory']}{package['Install']['WorkDir']}")
                        except: 
                            pass
                        
                        # if -o flag has passed, print output
                        if "-o" in args or "--output" in args:
                            shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            
                        else:
                            shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        
                        # execute commands
                        for command in remove_command:
                            if "-o" in args or "--output" in args:
                                print(f"{MAGENTA + Colors.BOLD}@{Colors.RESET + CYAN}{command}{RESET}")
                                
                            shell.stdin.write(command + '\n')
                            shell.stdin.flush()
                            
                        output, errors = shell.communicate()

                        # print errors, if occured
                        if not errors.rstrip() == "":
                            print(StringLoader("EncounteredErrors"))
                            print(errors)
                            print(StringLoader('UninstallationError', argument_1=e))
                            self.cleanup()
                            exit()

                        shell.terminate()

                    except Exception as e: 
                        print(StringLoader('UninstallationError', argument_1=e))
                        self.cleanup()
                        exit()

                    remove_time_end = time.time()
                    
                    # if -k flag hasnt passed, clean temporary files
                    if not "-k" in args or "--keep" in args:
                        self.cleanup()
                        
                    print(StringLoader('SuccessRemove', argument_1=self.package_name, argument_2=round(remove_time_end - remove_time_start, 2)))
            
            # Error Handling for NameError
            except NameError as e:
                print(StringLoader('PackageNotFound'))
                self.cleanup()
                exit()
            
            # Error Handling for PermissionError
            except PermissionError:
                print("")   
                delete_last_line()
                print(f"{Fore.CYAN + Colors.BOLD}/tmp/: {Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsLockfile'))
                self.cleanup()
                exit()
            
            # Error Handling for ScannerError
            except ScannerError:
                spinner.stop()
                delete_last_line()
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('GettingSpecfile')}")
                print(StringLoader("ParsingError"))
                self.cleanup()
                exit()
            
            # Error Handling for some internet errors 
            except (HTTPError, ConnectionError, NewConnectionError, MaxRetryError) as e:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader("HttpError"))
                self.cleanup()
                exit()
        
        
        
        
        """ 
            **** SANDBOX INSTALL FUNCTION ****
            This function installs the package to the sandbox environment, without checking if the sandbox is enabled or not. 
            INFO: You need to have the sandbox INSTALLED.
        """
        def install_sandbox(self, args):
            # Create and start the spinner for searching the database
            spinner = Halo(text=f"{StringLoader('SearchingDatabaseForPackage')}",
                            spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                            text_color="white",
                            color="green")
                
            spinner.start()
            
            # Search for the architecture
            c.execute("SELECT arch FROM packages where name = ?", (self.package_name,))
            
            # fetch the result and try to lock the lockfile
            try:
                result = c.fetchone()[0]
                lock(type=Procedure.Install)
            
            # Error Handling for TypeError
            except TypeError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader('PackageNotFound'))
                exit()
            
            # Error Handling for PermissionError
            except PermissionError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(f"{Fore.CYAN + Colors.BOLD}{Files.lockfile}: {Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsLockfile'))
                exit()
            
            # fetch name, version, url from the package database
            try:
                if result == "all":
                    c.execute("SELECT name, version, url, filename, specfile FROM packages where name = ?", (self.package_name,))

                else:
                    c.execute("SELECT name, version, url, filename, specfile FROM packages where name = ? AND arch = ?", (self.package_name, arch))
                    
            except OperationalError:
                    print(StringLoader("PackageDatabaseNotSynced"))
                    exit()
            
            # fetch the results
            try:     
                for row in c:
                    class Package:
                        Name        = row[0]
                        Version     = row[1]
                        Url         = row[2]
                        Filename    = row[3]
                        Specfile    = row[4]
                    
                    # request the package headers and get the file size
                    headers = requests.head(Package.Url)
                    file_size = round(self.file_size(response=headers, type=FileSizes.Megabytes), 2)
                    
                    spinner.stop()
                    print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingDatabaseForPackage')}")
                    
                    # ask if you want to continue the package installation (only if you dont have passed -y flag)
                    if not "-y" in args:
                        try:
                            cont_package_install = input(f"{StringLoader('ContinuePackageUninstallation', argument_1=self.package_name)}{Colors.RESET}{GREEN}")

                        except KeyboardInterrupt as e:
                            print(f"\n{RESET}{StringLoader('Abort')}")
                            exit()

                        if not cont_package_install.lower() in ["y", "j", "yes", "ja"]:
                            print(RESET + StringLoader("Abort"))
                            exit()
                    else:
                        print(f"{StringLoader('ContinuePackageUninstallationCompact', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")
                        
                    download_time_start = time.time()
                    
                    spinner = Halo(
                        text=f"{StringLoader('GettingSpecfile')}",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    # fetch specfile and save it
                    specfile = self.fetch_url(Package.Specfile)
                    self.file_saving(input=specfile, output="/tmp/specfile", file_extension="yml", warn_force_no_sandbox=False)
                    
                    spinner.stop()
                    
                    print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET}{StringLoader('GettingSpecfile')}")
                    
                    # oprn specfile and get the file extension for saving the package archive
                    with open("/tmp/specfile.yml") as file:
                        package = yaml.load(file, Loader=SafeLoader)
                    
                    try:
                        require_archive = package["Flags"]["RequiresArchiveForUninstall"]
                    except:
                        require_archive = False
                    
                    if require_archive:
                        print(StringLoader('RequiresArchiveForUninstall'))
                        spinner = Halo(
                        text=f"{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                        spinner.start()
                        # get package archive
                        file = self.fetch_url(Package.Url)
                        self.file_saving(input=file, output=f"/tmp/package", file_extension=package["Flags"]["ArchiveType"], warn_force_no_sandbox=True)
                        
                        spinner.stop()
                        
                        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET}{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})")

                        download_time_end = time.time()
                        
                        print(f"{StringLoader('FinishedDownloading')} {Fore.CYAN + Colors.BOLD}{Package.Filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
                        
                        time.sleep(.4)
                        
                    remove_time_start = time.time()

                    spinner = Halo(
                        text=f"{StringLoader('ParsingSpecfile')}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    # Start parsing specfile
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
                    
                    # get package manager
                    package_manager = get_package_manager()
                    
                    _apt_update = False
                    
                    if "-au" in  args or "--aptupdate" in args:
                        _apt_update = True
                        
                    apt_support = apk_support = dnf_support = pip_support = True
                    
                    # case-switch for package managers
                    match package_manager:
                        case PackageManagers.Apt:
                            try:
                                deps = SpecDeps["Apt"]
                            except Exception as e: 
                                print("APT UNSUPPORTED")
                                apt_support = False
                            
                        case PackageManagers.Apk:
                            try:
                                deps = SpecDeps["Apk"]
                            except: 
                                print("APK UNSUPPORTED")
                                apk_support = False
                            
                        case PackageManagers.Dnf:
                            try:
                                deps = SpecDeps["Dnf"]
                            except: 
                                print("DNF UNSUPPORTED")
                                dnf_support = False
                        
                        case PackageManagers.Pip:
                            try:
                                deps = SpecDeps["Pip"]
                            except: 
                                print("PIP UNSUPPORTED")
                                pip_support = False
                        
                        case _:
                            pass
                    
                    # if no package manager is supported, (for whatever reason, shouldnt happen) exit
                    if (apt_support and apk_support and dnf_support and pip_support) == False:
                        exit()
                
                    print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('RemoveDependenciesForYourself')} {Colors.BOLD}{Colors.RESET}")
                    print(f"{Fore.GREEN + Colors.BOLD}↳   {Fore.RESET + Colors.RESET}{Colors.ITALIC}{deps}{Colors.RESET}")

                    if require_archive:
                        spinner = Halo(
                            text=f"{StringLoader('ExtractArchive')}",
                            spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                            text_color="white",
                            color="green")
                        
                        spinner.start()
                        
                        # get file extension of archive
                        file_extension = SpecFlags["ArchiveType"]
                        
                        # case-switch for file extensions
                        match file_extension:
                            case "tar": 
                                import tarfile
                                
                                with tarfile.open(f"/tmp/package.{file_extension}", 'r') as tar:
                                    tar.extractall(path=config["build_directory"])
                                    
                            case "tar.gz" | "gz": 
                                import tarfile
                                
                                with tarfile.open(f"/tmp/package.{file_extension}", 'r:gz') as tar:
                                    tar.extractall(path=config["build_directory"])
                                
                            # if file extension is unsupported exit    
                            case _:
                                fe_unsupported = True
                                spinner.stop()
                                print("")
                                delete_last_line()
                                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('ExtractArchive')}")
                                print(StringLoader('ExtractError'))
                                self.cleanup()
                                exit()
                        
                        spinner.stop()
                        
                        print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('SuccessExtractArchive')}")
                    

                    # prepare remove
                    remove_command = Commands.Remove
                    
                    
                    print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Remove')} {Colors.BOLD}{Colors.RESET}")

                    try:
                        # try to change to the (maybe) passed workdir
                        try:
                            os.chdir(f"{config['build_directory']}{package['Install']['WorkDir']}")
                        except: 
                            pass
                        
                        # if -o flag has passed, print output
                        if "-o" in args or "--output" in args:
                            shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            
                        else:
                            shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        
                        # execute commands
                        for command in remove_command:
                            if "-o" in args or "--output" in args:
                                print(f"{MAGENTA + Colors.BOLD}@{Colors.RESET + CYAN}{command}{RESET}")
                                
                            shell.stdin.write(command + '\n')
                            shell.stdin.flush()
                            
                        output, errors = shell.communicate()

                        # print errors, if occured
                        if not errors.rstrip() == "":
                            print(StringLoader("EncounteredErrors"))
                            print(errors)
                            print(StringLoader('UninstallationError', argument_1=e))
                            self.cleanup()
                            exit()

                        shell.terminate()

                    except Exception as e: 
                        print(StringLoader('UninstallationError', argument_1=e))
                        self.cleanup()
                        exit()

                    remove_time_end = time.time()
                    
                    # if -k flag hasnt passed, clean temporary files
                    if not "-k" in args or "--keep" in args:
                        self.cleanup()
                        
                    print(StringLoader('SuccessRemove', argument_1=self.package_name, argument_2=round(remove_time_end - remove_time_start, 2)))
            
            # Error Handling for NameError
            except NameError as e:
                print(StringLoader('PackageNotFound'))
                self.cleanup()
                exit()
            
            # Error Handling for PermissionError
            except PermissionError:
                print("")   
                delete_last_line()
                print(f"{Fore.CYAN + Colors.BOLD}/tmp/: {Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsLockfile'))
                self.cleanup()
                exit()
            
            # Error Handling for ScannerError
            except ScannerError:
                spinner.stop()
                delete_last_line()
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('GettingSpecfile')}")
                print(StringLoader("ParsingError"))
                self.cleanup()
                exit()
            
            # Error Handling for some internet errors 
            except (HTTPError, ConnectionError, NewConnectionError, MaxRetryError) as e:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader("HttpError"))
                self.cleanup()
                exit()