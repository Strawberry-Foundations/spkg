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

import time
import sqlite3 as sql
import urllib.request
import os
import yaml
from yaml import SafeLoader
import shutil

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore
from halo import Halo
from sys import exit
import subprocess
import tarfile

    
class Functions:
    def get_package_manager():
        try:
            output = subprocess.check_output(["which", "apt"]).decode("utf-8")
            if "apt" in output:
                return "apt"
        except subprocess.CalledProcessError:
            pass
        
        try:
            output = subprocess.check_output(["which", "apk"]).decode("utf-8")
            if "apk" in output:
                return "apk"
        except subprocess.CalledProcessError:
            pass
        
        try:
            output = subprocess.check_output(["which", "dnf"]).decode("utf-8")
            if "dnf" in output:
                return "dnf"
        except subprocess.CalledProcessError:
            pass
        
        return False
    
    # Apt (Deb-based) install function
    def apt_install(package):
        command = ["apt", "install", "-y"] + package
        try: subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e: print(f"Error while installing {package}: {e}")

    # Apk (Alpine-based) install function
    def apk_install(package):
        command = ["apk", "add"] + package
        try: subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e: print(f"Error while installing {package}: {e}")

    # Dnf (Fedora-based) install function
    def dnf_install(package):
        command = ["dnf", "install", "-y"] + package
        try: subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e: print(f"Error while installing {package}: {e}")
    
    # Dnf (Fedora-based) install function
    def pip_install(package):
        command = ["pip", "install"] + package + ["--break-system-packages"]
        try: subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e: print(f"Error while installing {package}: {e}")
    
    # Clean temporary files
    def cleanup(self):
        try:
            shutil.rmtree("/tmp/_spkg_installer.build/")
            os.remove("/tmp/specfile.yml")
            os.remove("/tmp/spkg_installer.db")
            
            for package_file in os.listdir("/tmp/"):
                if package_file.startswith('spkg'):
                    file = os.path.join("/tmp/", package_file)
                    os.remove(file)
        except:
            pass

class Colors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    GRAY = "\033[90m"
    ITALIC = "\033[3m"

version = "1.3.0"

db = sql.connect("/tmp/spkg_installer.db")
c = db.cursor()

repo = "http://sources.strawberryfoundations.xyz:49171/packages/package.db"
filename = "/tmp/spkg_installer.db"

print(f"{Colors.BOLD + Colors.UNDERLINE}Welcome to spkg-installer v{version}{Colors.RESET}")
print(f"The spkg-installer will install the desired version of the Advanced Source Package Management (spkg) on your system.\n")

try:
    request = urllib.request.Request(
        repo,
        data=None,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    )

    database = urllib.request.urlopen(request)

    download_time_start = time.time()

    spinner = Halo(
            text=f"Fetching main database ({repo})...",
            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
            text_color="white",
            color="green"
            )
    
    spinner.start()
    
    try:
        with open(filename, 'wb') as file:
            file.write(database.read())
            
    except PermissionError:
        spinner.stop()
        print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} Fetching main database ({repo})...{Colors.RESET}")
        print(f"{Fore.CYAN + Colors.BOLD}/tmp/: {Fore.RESET}{Colors.RESET}Missing permissions")
        print(f"{Fore.RED + Colors.BOLD}No access to /tmp - the temporary package database could not be saved.\nIs spkg running as root? If yes, then look into /tmp, and delete the spkg_installer.db if present.")
        exit()
        

    download_time_end = time.time()
    spinner.stop()
    print(f"{Fore.GREEN + Colors.BOLD} ✓  {Fore.RESET}Database was fetched")

except HTTPError as e:
    print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} Unknown Error{Colors.RESET}")
    print(e)

db = sql.connect("/tmp/spkg_installer.db")
c = db.cursor()

# Fetch base spkg package information
c.execute("SELECT name FROM packages where name = ?", ("spkg",))
if c.fetchall():
    c.execute("SELECT version, branch FROM packages where name = ?", ("spkg",))
    for row in c:
        _spkg_py_ver = row[0]
        _spkg_py_branch = row[1]

# Fetch base spkg-git package information
c.execute("SELECT name FROM packages where name = ?", ("spkg-git",))
if c.fetchall():
    c.execute("SELECT version, branch FROM packages where name = ?", ("spkg-git",))
    for row in c:
        _spkg_git_ver = row[0]
        _spkg_git_branch = row[1]

# Print message
print(f"\n{Colors.BOLD + Colors.UNDERLINE}Please select the version of spkg you want to install:{Colors.RESET}")
print(f"{Colors.BOLD + Fore.CYAN}[i]{Fore.RESET} You don't know which version is the right one for you? Get help with '?' or 'help'.\nType 'exit' or 'q' to exit")
print(f"{Colors.BOLD} -> 1. {Fore.BLUE}spkg ({_spkg_py_ver}) {Fore.CYAN}@ {_spkg_py_branch}{Fore.RESET}{Colors.RESET}")
print(f"{Colors.BOLD} -> 2. {Fore.BLUE}spkg-git ({_spkg_git_ver}) {Fore.CYAN}@ {_spkg_git_branch}{Fore.RESET}{Colors.RESET}")

# Input loop
while True:
    try:
        user_input = input(": ")

    except KeyboardInterrupt as e:
        print(f"\n{Fore.RED + Colors.BOLD} × {Fore.RESET} Canceled installation of spkg.{Colors.RESET}")
        exit()
    match user_input:
        case "?" | "help":
            print(f"\n{Fore.BLUE + Colors.UNDERLINE + Colors.BOLD}spkg")
            print(f"The official version of spkg, which is extensively tested. Runs more stable and \nreliable than the spkg-git version. Requires the Python interpreter")

            print(f"\n{Fore.BLUE + Colors.UNDERLINE + Colors.BOLD}spkg-git")
            print(f"The Git version of spkg. This uses the codebase from GitHub (https://github.com/Strawberry-Foundations/spkg).\nUses the latest source code. May run unstable. Mostly untested. Requires the Python interpreter")
            
        case "exit" | "q":
            print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} Canceled installation of spkg.{Colors.RESET}")
            exit()
        
        case "spkg" | "1":
            # Fetch base spkg package information
            c.execute("SELECT name FROM packages where name = ?", ("spkg",))
            if c.fetchall():
                c.execute("SELECT name, version, branch, url, specfile FROM packages where name = ?", ("spkg",))
                for row in c:
                    ver = row[1]
                    branch = row[2]
                    url = row[3]
                    specfile = row[4]
                    
            print(f"{Colors.BOLD}Preparing installation of spkg ...{Colors.RESET}")

            try:
                request_archive = urllib.request.Request(
                    url,
                    data=None,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                    }
                )

                request_specfile = urllib.request.Request(
                    specfile,
                    data=None,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                    }
                )

                download_time_start = time.time()

                spinner = Halo(
                            text=f"Get: {Fore.CYAN}{url}{Fore.RESET}",
                            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
                            text_color="white",
                            color="green"
                            )
                
                spinner.start()
                
                package_archive = urllib.request.urlopen(request_archive)
                
                try:
                    with open(f"/tmp/spkg-{ver}.tar", 'wb') as file:
                        file.write(package_archive.read())
                        
                except PermissionError:
                    spinner.stop()
                    print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} Get: {Fore.CYAN}{url}{Fore.RESET}")
                    print(f"{Fore.CYAN + Colors.BOLD}/tmp/: {Fore.RESET}{Colors.RESET}Missing permissions")
                    print(f"{Fore.RED + Colors.BOLD}No access to /tmp - the temporary package archive could not be saved.\nIs spkg running as root? If yes, then look into /tmp, and delete the /tmp/spkg-{ver}.tar if present.")
                    exit()

                spinner.stop()
                print(f"{Fore.GREEN + Colors.BOLD} ✓  {Colors.BOLD + Fore.RESET}Get: {Fore.CYAN}{url}{Fore.RESET}")


                spinner = Halo(
                            text=f"Get: {Fore.CYAN}{specfile}{Fore.RESET}",
                            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
                            text_color="white",
                            color="green"
                            )
                
                spinner.start()
                
                package_specfile = urllib.request.urlopen(request_specfile)

                with open("/tmp/specfile.yml", 'wb') as file:
                    file.write(package_specfile.read())

                spinner.stop()
                print(f"{Fore.GREEN + Colors.BOLD} ✓  {Colors.BOLD + Fore.RESET}Get: {Fore.CYAN}{specfile}{Fore.RESET}")


                download_time_end = time.time()
                print(f"{Fore.GREEN + Colors.BOLD} ↳  {Colors.RESET}Finished downloading sources for {Fore.CYAN + Colors.BOLD}spkg ({ver}){Colors.RESET} in {Fore.GREEN + Colors.BOLD}{round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
                
                
                spinner = Halo(
                            text=f"The package configuration is read in",
                            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
                            text_color="white",
                            color="green"
                            )
                
                spinner.start()
                
                # Open specfile and get package configurations
                with open("/tmp/specfile.yml") as file:
                    package = yaml.load(file, Loader=SafeLoader)
                        
                # Start parsing specfile
                spec_name   = package["Name"]
                spec_ver    = package["Version"]
                spec_arch   = package["Architecture"]
                spec_deps   = package["Dependencies"]
                spec_flags  = package["Flags"]
                spec_cmd    = package["Install"]["Commands"]
                
                spinner.stop()
                
                print(f"{Fore.GREEN + Colors.BOLD} ✓  {Fore.RESET}The package configuration was read in")
                
                dep_start_time = time.time()

                # determinate dependencies
                spinner = Halo(
                            text=f"Dependencies are determined and installed {Colors.BOLD}({Functions.get_package_manager()}){Colors.RESET}",
                            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
                            text_color="white",
                            color="green"
                            )
                
                spinner.start()
                
                # get package manager
                package_manager = Functions.get_package_manager()
                
                # case-switch for package managers
                match package_manager:
                    case "apt":
                        try:
                            Functions.apt_install(spec_deps["Apt"].split(" "))
                            deps = spec_deps["Apt"]
                            
                        except Exception as e: 
                            print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} An error occured while installing the dependencies for spkg.{Colors.RESET}")
                        
                    case "apk":
                        try:
                            Functions.apk_install(spec_deps["Apk"].split(" "), print_output=False)
                            deps = spec_deps["Apk"]
                        except: 
                            print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} An error occured while installing the dependencies for spkg.{Colors.RESET}")
                        
                    case "dnf":
                        try:
                            Functions.dnf_install(spec_deps["Dnf"].split(" "), print_output=False)
                            deps = spec_deps["Dnf"]
                        except: 
                            print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} An error occured while installing the dependencies for spkg.{Colors.RESET}")
            
                spinner.stop() 

                dep_end_time = time.time()
                
                print(f"{Fore.GREEN + Colors.BOLD} ✓  {Fore.RESET}Dependencies were installed (in %s s) {Colors.BOLD}({Functions.get_package_manager()}){Colors.RESET}" % round(dep_end_time - dep_start_time, 2))
                print(f"{Fore.GREEN + Colors.BOLD} ↳  {Fore.RESET + Colors.RESET}{Colors.ITALIC}{deps}{Colors.RESET}")
                                    
                spinner = Halo(
                            text=f"Pip dependencies will be installed...",
                            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
                            text_color="white",
                            color="green"
                            )
                
                spinner.start()
                
                # Search for pip dependencies
                try:
                    spec_deps["Pip"].split(" ")                
                    dep_start_time = time.time()
                    
                    # install pip dependencies
                    Functions.pip_install(spec_deps["Pip"].split(" "))
                    
                    dep_end_time = time.time()

                    spinner.stop()
                    print(f"{Fore.GREEN + Colors.BOLD} ✓  {Fore.RESET}Pip dependencies were installed (in %s s)" % round(dep_end_time - dep_start_time, 2))
                    print(f"{Fore.GREEN + Colors.BOLD} ↳  {Fore.RESET + Colors.RESET}{Colors.ITALIC}{spec_deps['Pip']}{Colors.RESET}")
                    
                except:
                    spinner.stop()
                    print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} An error occured while installing the pip dependencies for spkg.{Colors.RESET}")
                
                spinner = Halo(
                            text=f"Unpacking package archive...",
                            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
                            text_color="white",
                            color="green"
                            )
                    
                spinner.start()
                            
                with tarfile.open(f"/tmp/spkg-{ver}.tar", 'r') as tar:
                    tar.extractall(path="/tmp/_spkg_installer.build/")
                
                spinner.stop()
                print(f"{Fore.GREEN + Colors.BOLD} ✓  {Fore.RESET}Package archive has been unpacked")
                
                spinner = Halo(
                            text=f"Installing spkg...",
                            spinner={'interval': 150, 'frames': [' - ', ' \\ ', ' | ', ' / ']},
                            text_color="white",
                            color="green"
                            )
                    
                spinner.start()
                
                try:
                    try:
                        os.chdir(f"/tmp/_spkg_installer.build/")
                    except Exception as e: 
                        print(f"{Fore.RED + Colors.BOLD} × {Fore.RESET} Couldn't change directory to /tmp/_spkg_installer.build/{Colors.RESET}")
                        exit()
                    
                    shell = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    # execute commands
                    for command in spec_cmd:
                        shell.stdin.write(command + '\n')
                        shell.stdin.flush()
                        
                    output, errors = shell.communicate()

                    # print errors, if occured
                    if not errors.rstrip() == "":
                        print(f"{Fore.RED}{Colors.BOLD}   Errors encountered:{Colors.RESET}")
                        print(errors)

                    shell.terminate()

                except Exception as e: 
                    print(f"{Fore.RED}{Colors.BOLD} E:{Fore.RESET} spkg could not be installed (%s){Colors.RESET}")
                    Functions.cleanup()
                    exit()
                
                
                if os.path.exists('/usr/bin/spkg'):
                    print(f"{Colors.BOLD + Fore.GREEN}Congratulations! The Advanced Source Package Management has been successfully installed on your system!{Colors.BOLD + Fore.GREEN}")
                else: 
                    print(f"{Colors.BOLD + Fore.RED}Error occured while installing spkg. Try asking a developer.{Colors.RESET + Fore.RESET}")
                    exit()
                
                exit()
            
            except HTTPError as e:
                print(f"{Fore.RED + Colors.BOLD}E:{Fore.RESET} Unknown Error{Colors.RESET}")
                print(e)

            except NameError as e:
                print(f"{Fore.RED  + Colors.BOLD}E:{Fore.RESET} Package not found{Colors.RESET}")
            
            except KeyboardInterrupt as e:
                print(f"\n{Fore.RED + Colors.BOLD} × {Fore.RESET} Canceled installation of spkg.{Colors.RESET}")
                exit()

        case "spkg-git" | "2":
            time.sleep(1)
            print(f"{Colors.BOLD}Preparing installation of spkg-git ...{Colors.RESET}")

            try:
                req = urllib.request.Request(
                    spkg_git_url,
                    data=None,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                    }
                )

                req_setup = urllib.request.Request(
                    spkg_git_setup,
                    data=None,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                    }
                )

                f = urllib.request.urlopen(req)

                download_time_start = time.time()

                spinner = Halo(text=f"Get: {spkg_git_url}", spinner={'interval': 150, 'frames': [
                    '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
                spinner.start()

                with open("/tmp/spkg_git.tar.gz", 'wb') as file:
                    file.write(f.read())

                spinner.stop()
                print(
                    f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.BOLD}Get: {spkg_git_url}")

                f_setup = urllib.request.urlopen(req_setup)

                spinner2 = Halo(text=f"Get: {spkg_git_setup}", spinner={'interval': 150, 'frames': [
                    '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
                spinner2.start()

                with open("/tmp/PKGBUILD", 'wb') as file_setup:
                    file_setup.write(f_setup.read())

                spinner.stop()
                print(
                    f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.BOLD}Get: {spkg_git_setup}")

                download_time_end = time.time()
                print(
                    f"Finished downloading sources for {Fore.LIGHTCYAN_EX + Colors.BOLD}spkg-git{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")

                spinner.stop()
                spinner2.stop()
                
                subprocess.run(['sudo', 'chmod', '+x', f'/tmp/PKGBUILD'])
                subprocess.run(['sudo', 'bash', f'/tmp/PKGBUILD', '--install'])
                
                if os.path.exists('/usr/bin/spkg'):
                    print(f"{Colors.BOLD + Fore.GREEN}Congratulations! The Advanced Source Package Management has been successfully installed on your system!{Colors.BOLD + Fore.GREEN}")
                else: 
                    print(f"{Colors.BOLD + Fore.RED}Error occured while installing spkg. Try asking a developer.{Colors.RESET + Fore.RESET}")
                    exit()
                
                exit()

            except HTTPError as e:
                print(
                    f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unknown Error{Colors.RESET}")
                print(e)

            except NameError as e:
                print(
                    f"{Fore.RED  + Colors.BOLD}[E]{Fore.RESET} Package not found{Colors.RESET}")
            
            except KeyboardInterrupt as e:
                print(
                    f"\n{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Canceled installation of spkg.{Colors.RESET}")
                exit()
        case _:
            print(f"{Fore.RED + Colors.BOLD}Unknown Input")

subprocess.run(['sudo', 'rm', '-r', '/tmp/target*'])
subprocess.run(['sudo', 'rm', '-r' ,'/tmp/PKGBUILD'])

exit()


# 1, 2, 3 and unknown Warning Error when you selecting the package
# check if /usr/bin/spkg exists, if not Installation is not completed
