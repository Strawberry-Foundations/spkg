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

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore
from halo import Halo
from sys import exit
import subprocess


class Colors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


version = "1.2.0"

db = sql.connect("/tmp/spkg_installer.db")
c = db.cursor()

repo = "http://main.tuxifan.net:49171/packages/package.db"
filename = "/tmp/spkg_installer.db"

print(f"{Colors.BOLD + Colors.UNDERLINE}Welcome to spkg-installer v{version}{Colors.RESET}")
print(f"The spkg-installer will install the desired version of the Advanced Source Package Management (spkg) on your system.\n")

try:
    req = urllib.request.Request(
        repo,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    )

    f = urllib.request.urlopen(req)

    download_time_start = time.time()

    spinner = Halo(text=f"Fetching main database ({repo})...", spinner={
        'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    spinner.start()

    with open(filename, 'wb') as file:
        file.write(f.read())

    download_time_end = time.time()

    print(f"{Colors.BOLD}\nDatabase was fetched.{Colors.RESET}\n")

except HTTPError as e:
    print(
        f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unknown Error{Colors.RESET}")
    print(e)

spkg_py = "spkg"
spkg_git = "spkg-git"

c.execute("SELECT name FROM packages where name = ?", (spkg_py,))
if c.fetchall():
    c.execute(
        "SELECT name, version, branch, fetch_url, setup_script FROM packages where name = ?", (spkg_py,))
    for row in c:
        spkg_py_ver = row[1]
        spkg_py_branch = row[2]
        spkg_py_url = row[3]
        spkg_py_setup = row[4]

c.execute("SELECT name FROM packages where name = ?", (spkg_git,))
if c.fetchall():
    c.execute(
        "SELECT name, version, branch, fetch_url, setup_script FROM packages where name = ?", (spkg_git,))
    for row in c:
        spkg_git_ver = row[1]
        spkg_git_branch = row[2]
        spkg_git_url = row[3]
        spkg_git_setup = row[4]

print(f"{Colors.BOLD + Colors.UNDERLINE}Please select the version of spkg you want to install:{Colors.RESET}")
print(
    f"{Colors.BOLD + Fore.CYAN}[i]{Fore.RESET} You don't know which version is the right one for you? Get help with '?' or 'help'.\nType 'exit' or 'q' to exit")
print(f"{Colors.BOLD} -> 1. {Fore.BLUE}spkg-py ({spkg_py_ver}) {Fore.CYAN}@ {spkg_py_branch}{Fore.RESET}{Colors.RESET}")
print(f"{Colors.BOLD} -> 2. {Fore.BLUE}spkg-git ({spkg_git_ver}) {Fore.CYAN}@ {spkg_git_branch}{Fore.RESET}{Colors.RESET}")

spinner.stop()
while 1:
    try:
        install_version_input = input(": ")

    except KeyboardInterrupt as e:
        print(
            f"\n{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Canceled installation of spkg.{Colors.RESET}")
        exit()

    if install_version_input == "?" or install_version_input == "help":
        print(f"\n{Fore.BLUE + Colors.UNDERLINE + Colors.BOLD}spkg-py")
        print(f"The official version of spkg, which is extensively tested. Runs faster and more\nreliable than the spkg-bin version. Requires the Python interpreter")

        print(f"\n{Fore.BLUE + Colors.UNDERLINE + Colors.BOLD}spkg-bin")
        print(f"A compiled version of spkg. Runs on any system, even without Python interpreter.\nRuns a bit slower, and more unreliable. THIS PACKAGE IS NO LONGER AVAILABLE!!!!")

        print(f"\n{Fore.BLUE + Colors.UNDERLINE + Colors.BOLD}spkg-git")
        print(f"The Git version of spkg. This uses the codebase from GitHub (https://github.com/Juliandev02/spkg).\nUses the latest source code. May run unstable. Mostly untested. Requires the Python interpreter")

    if install_version_input == "exit" or install_version_input == "q":
        print(
            f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Canceled installation of spkg.{Colors.RESET}")
        exit()

    if install_version_input == "spkg-py" or install_version_input == "1":
        time.sleep(1)
        print(f"{Colors.BOLD}Preparing installation of spkg-py ...{Colors.RESET}")

        try:
            req = urllib.request.Request(
                spkg_py_url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
            )

            req_setup = urllib.request.Request(
                spkg_py_setup,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
            )

            f = urllib.request.urlopen(req)

            download_time_start = time.time()

            spinner = Halo(text=f"Get: {spkg_py_url}", spinner={'interval': 150, 'frames': [
                '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
            spinner.start()

            with open("/tmp/spkg_py.tar", 'wb') as file:
                file.write(f.read())

            spinner.stop()
            print(
                f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.BOLD}Get: {spkg_py_url}")

            f_setup = urllib.request.urlopen(req_setup)

            spinner2 = Halo(text=f"Get: {spkg_py_setup}", spinner={'interval': 150, 'frames': [
                '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
            spinner2.start()

            with open("/tmp/PKGBUILD", 'wb') as file_setup:
                file_setup.write(f_setup.read())

            spinner.stop()
            print(
                f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.BOLD}Get: {spkg_py_setup}")

            download_time_end = time.time()
            print(
                f"Finished downloading sources for {Fore.LIGHTCYAN_EX + Colors.BOLD}spkg-py{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
            
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



    if install_version_input == "spkg-git" or install_version_input == "2":
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
            
            
    else:
        print(f"{Fore.RED + Colors.BOLD}Unknown Input")

subprocess.run(['sudo', 'rm', '-r', '/tmp/target*'])
subprocess.run(['sudo', 'rm', '-r' ,'/tmp/PKGBUILD'])

exit()


# 1, 2, 3 and unknown Warning Error when you selecting the package
# check if /usr/bin/spkg exists, if not Installation is not completed
