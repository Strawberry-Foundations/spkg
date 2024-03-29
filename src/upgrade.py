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
    c = db.cursor()

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

class UpgradeManager:
    """ 
        **** UPGRADE FUNCTION ****
        This function upgrades packages, depending on various plugins, e.g. if the sandbox is enabled or not. 
    """
    class Upgrade:
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
        def insert_world(self):
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
                wc.execute("INSERT INTO world (name, version, branch) VALUES (?, ?, ?)", (name, version, branch))
                wdb.commit()                
            except OperationalError:
                print(StringLoader("WorldDatabaseNotBuilded"))
                exit()
            
            except PermissionError:
                print(f"{Fore.CYAN + Colors.BOLD}{Files.world_database}{Fore.RESET}{StringLoader('MissingPermissions')}")
                print(StringLoader('MissingPermissionsWorldDatabaseInsert'))
                exit()

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
            MAIN UPGRADE FUNCTION
        """
        def upgrade(self, args):
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
                lock(type=Procedure.Upgrade)
            
            # Error Handling for TypeError
            except TypeError as e:
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
                            cont_package_install = input(f"{StringLoader('ContinuePackageUpdate', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")

                        except KeyboardInterrupt as e:
                            print(f"\n{RESET}{StringLoader('Abort')}")
                            exit()

                        if not cont_package_install.lower() in ["y", "j", "yes", "ja"]:
                            print(RESET + StringLoader("Abort"))
                            exit()
                    else:
                        print(f"{StringLoader('ContinuePackageUpdateCompact', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")
                        
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

                    spinner = Halo(
                        text=f"{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    # oprn specfile and get the file extension for saving the package archive
                    with open("/tmp/specfile.yml") as file:
                        package = yaml.load(file, Loader=SafeLoader)
                    
                    # get package archive
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
                    
                    dep_start_time = time.time()

                    # determinate dependencies
                    spinner = Halo(
                        text=f"{StringLoader('DeterminateDependencies')} {Colors.BOLD}({get_package_manager()}){Colors.RESET}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
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
                                apt_install(SpecDeps["Apt"].split(" "), print_output=False, update=_apt_update)
                                deps = SpecDeps["Apt"]
                            except Exception as e: 
                                print("APT UNSUPPORTED")
                                apt_support = False
                            
                        case PackageManagers.Apk:
                            try:
                                apk_install(SpecDeps["Apk"].split(" "), print_output=False)
                                deps = SpecDeps["Apk"]
                            except: 
                                print("APK UNSUPPORTED")
                                apk_support = False
                            
                        case PackageManagers.Dnf:
                            try:
                                dnf_install(SpecDeps["Dnf"].split(" "), print_output=False)
                                deps = SpecDeps["Dnf"]
                            except: 
                                print("DNF UNSUPPORTED")
                                dnf_support = False
                        
                        case PackageManagers.Pip:
                            try:
                                pip_install(SpecDeps["Pip"].split(" "), print_output=False)
                                deps = SpecDeps["Pip"]
                            except: 
                                print("PIP UNSUPPORTED")
                                pip_support = False
                        
                        case _:
                            pass
                    
                    # if no package manager is supported, (for whatever reason, shouldnt happen) exit
                    if (apt_support and apk_support and dnf_support and pip_support) == False:
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
                    
                    # Search for pip dependencies
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
                        
                        # install pip dependencies
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
                    
                    
                    spinner = Halo(
                    text=f"{StringLoader('PrepareCompile')}",
                    spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                    text_color="white",
                    color="green")
                
                    spinner.start()

                    # Check if package has to be compiled before installing
                    try:
                        requires_compile = SpecFlags["RequiresCompile"]
                        if not requires_compile:
                            spinner.stop()
                            print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('NoCompileNeed')} {Colors.BOLD}{Colors.RESET}")

                        else:
                            print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Compile')} {Colors.BOLD}{Colors.RESET}")
                            os.chdir(config["build_directory"])
                            compile_command = Commands.Compile
                            
                            # try to change to the (maybe) passed workdir
                            try:
                                try:
                                    os.chdir(f"{config['build_directory']}{package['Compile']['WorkDir']}")
                                except: 
                                    pass
                                
                                # if -o flag has passed, print output
                                if "-o" in args or "--output" in args:
                                    shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                    
                                else:
                                    shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                
                                # execute commands
                                for command in compile_command:
                                    if "-o" in args or "--output" in args:
                                        print(f"{MAGENTA + Colors.BOLD}@{Colors.RESET + CYAN}{command}{RESET}")
                                        
                                    shell.stdin.write(command + '\n')
                                    shell.stdin.flush()
                                    
                                output, errors = shell.communicate()

                                # print errors, if occured
                                if not errors.rstrip() == "":
                                    print(StringLoader("EncounteredErrors"))
                                    print(errors)

                                shell.terminate()

                            except Exception as e: 
                                print(StringLoader('InstallationError', argument_1=e))
                                self.cleanup()
                                exit()

                    except:
                        spinner.stop()
                        print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('NoCompileNeed')} {Colors.BOLD}{Colors.RESET}")
                    

                    spinner = Halo(
                    text=f"{StringLoader('PrepareUpdate')}",
                    spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                    text_color="white",
                    color="green")
                
                    spinner.start()
                    
                    # prepare install
                    update_command = Commands.Upgrade
                    
                    spinner.stop()
                    print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('PrepareUpdate')} {Colors.BOLD}{Colors.RESET}")
                    
                    print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Update')} {Colors.BOLD}{Colors.RESET}")

                    try:
                        os.chdir(config["build_directory"])
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
                        for command in update_command:
                            if "-o" in args or "--output" in args:
                                print(f"{MAGENTA + Colors.BOLD}@{Colors.RESET + CYAN}{command}{RESET}")
                                
                            shell.stdin.write(command + '\n')
                            shell.stdin.flush()
                            
                        output, errors = shell.communicate()

                        # print errors, if occured
                        if not errors.rstrip() == "":
                            print(StringLoader("EncounteredErrors"))
                            print(errors)
                            print(StringLoader('UpdateError', argument_1=e))
                            self.cleanup()
                            exit()

                        shell.terminate()

                    except Exception as e: 
                        print(StringLoader('UpdateError', argument_1=e))
                        self.cleanup()
                        exit()

                    install_time_end = time.time()
                    
                    # if -k flag hasnt passed, clean temporary files
                    if not "-k" in args or "--keep" in args:
                        self.cleanup()
                        
                    print(StringLoader('SuccessUpdate', argument_1=self.package_name, argument_2=round(install_time_end - install_time_start, 2)))
            
            # Error Handling for NameError
            # except NameError as e:
            #     print(e)
            #     print(StringLoader('PackageNotFound'))
            #     self.cleanup()
            #     exit()
            
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
                lock(type=Procedure.Upgrade)
            
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
                            cont_package_install = input(f"{StringLoader('ContinuePackageUpdate', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")

                        except KeyboardInterrupt as e:
                            print(f"\n{RESET}{StringLoader('Abort')}")
                            exit()

                        if not cont_package_install.lower() in ["y", "j", "yes", "ja"]:
                            print(RESET + StringLoader("Abort"))
                            exit()
                    else:
                        print(f"{StringLoader('ContinuePackageUpdateCompact', argument_1=Package.Filename, argument_2=file_size)}{Colors.RESET}{GREEN}")
                        
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

                    spinner = Halo(
                        text=f"{StringLoader('Get')}: {Package.Url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    # oprn specfile and get the file extension for saving the package archive
                    with open("/tmp/specfile.yml") as file:
                        package = yaml.load(file, Loader=SafeLoader)
                    
                    # get package archive
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
                    
                    dep_start_time = time.time()

                    # determinate dependencies
                    spinner = Halo(
                        text=f"{StringLoader('DeterminateDependencies')} {Colors.BOLD}({get_package_manager()}){Colors.RESET}",
                        spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
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
                                apt_install(SpecDeps["Apt"].split(" "), print_output=False, update=_apt_update)
                                deps = SpecDeps["Apt"]
                            except Exception as e: 
                                print("APT UNSUPPORTED")
                                apt_support = False
                            
                        case PackageManagers.Apk:
                            try:
                                apk_install(SpecDeps["Apk"].split(" "), print_output=False)
                                deps = SpecDeps["Apk"]
                            except: 
                                print("APK UNSUPPORTED")
                                apk_support = False
                            
                        case PackageManagers.Dnf:
                            try:
                                dnf_install(SpecDeps["Dnf"].split(" "), print_output=False)
                                deps = SpecDeps["Dnf"]
                            except: 
                                print("DNF UNSUPPORTED")
                                dnf_support = False
                        
                        case PackageManagers.Pip:
                            try:
                                pip_install(SpecDeps["Pip"].split(" "), print_output=False)
                                deps = SpecDeps["Pip"]
                            except: 
                                print("PIP UNSUPPORTED")
                                pip_support = False
                        
                        case _:
                            pass
                    
                    # if no package manager is supported, (for whatever reason, shouldnt happen) exit
                    if (apt_support and apk_support and dnf_support and pip_support) == False:
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
                    
                    # Search for pip dependencies
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
                        
                        # install pip dependencies
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
                    
                    
                    spinner = Halo(
                    text=f"{StringLoader('PrepareCompile')}",
                    spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                    text_color="white",
                    color="green")
                
                    spinner.start()

                    # Check if package has to be compiled before installing
                    try:
                        requires_compile = SpecFlags["RequiresCompile"]
                        if not requires_compile:
                            spinner.stop()
                            print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('NoCompileNeed')} {Colors.BOLD}{Colors.RESET}")

                        else:
                            print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Compile')} {Colors.BOLD}{Colors.RESET}")
                            os.chdir(config["build_directory"])
                            compile_command = Commands.Compile
                            
                            # try to change to the (maybe) passed workdir
                            try:
                                try:
                                    os.chdir(f"{config['build_directory']}{package['Compile']['WorkDir']}")
                                except: 
                                    pass
                                
                                # if -o flag has passed, print output
                                if "-o" in args or "--output" in args:
                                    shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                    
                                else:
                                    shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                
                                # execute commands
                                for command in compile_command:
                                    if "-o" in args or "--output" in args:
                                        print(f"{MAGENTA + Colors.BOLD}@{Colors.RESET + CYAN}{command}{RESET}")
                                        
                                    shell.stdin.write(command + '\n')
                                    shell.stdin.flush()
                                    
                                output, errors = shell.communicate()

                                # print errors, if occured
                                if not errors.rstrip() == "":
                                    print(StringLoader("EncounteredErrors"))
                                    print(errors)

                                shell.terminate()

                            except Exception as e: 
                                print(StringLoader('InstallationError', argument_1=e))
                                self.cleanup()
                                exit()

                    except:
                        spinner.stop()
                        print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('NoCompileNeed')} {Colors.BOLD}{Colors.RESET}")
                    

                    spinner = Halo(
                    text=f"{StringLoader('PrepareUpdate')}",
                    spinner={'interval': 500, 'frames': ['.  ', '.. ', '...']},
                    text_color="white",
                    color="green")
                
                    spinner.start()
                    
                    # prepare install
                    update_command = Commands.Upgrade
                    
                    spinner.stop()
                    print(f"{Fore.GREEN + Colors.BOLD}✓   {Fore.RESET}{StringLoader('PrepareUpdate')} {Colors.BOLD}{Colors.RESET}")
                    
                    print(f"{Fore.BLUE + Colors.BOLD}!   {Fore.RESET}{StringLoader('Update')} {Colors.BOLD}{Colors.RESET}")

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
                        for command in update_command:
                            if "-o" in args or "--output" in args:
                                print(f"{MAGENTA + Colors.BOLD}@{Colors.RESET + CYAN}{command}{RESET}")
                                
                            shell.stdin.write(command + '\n')
                            shell.stdin.flush()
                            
                        output, errors = shell.communicate()

                        # print errors, if occured
                        if not errors.rstrip() == "":
                            print(StringLoader("EncounteredErrors"))
                            print(errors)
                            print(StringLoader('UpdateError', argument_1=e))
                            self.cleanup()
                            exit()

                        shell.terminate()

                    except Exception as e: 
                        print(StringLoader('UpdateError', argument_1=e))
                        self.cleanup()
                        exit()

                    install_time_end = time.time()
                    
                    # if -k flag hasnt passed, clean temporary files
                    if not "-k" in args or "--keep" in args:
                        self.cleanup()
                        
                    print(StringLoader('SuccessUpdate', argument_1=self.package_name, argument_2=round(install_time_end - install_time_start, 2)))
            
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