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
import time
import json
import sqlite3 as sql
import urllib.request
import platform
import requests
import subprocess

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore
from halo import Halo
from sys import exit
from .plugin_daemon import plugin_daemon, check_plugin_enabled_silent, check_plugin_enabled_ret
from defs import *
from .force_no_sandbox import *

if check_plugin_enabled_ret("sandbox") == True:
    plugin_daemon.import_plugin("sandbox")
else:
    pass

language = spkg_cfg_data['language']


if not language in ["de", "en"]:
    print(f"{Fore.RED}You have either a corrupted or unconfigured config file! Please check the language settings!")

if language == "de":
    PackageNotFound = f"{Fore.RED + Colors.BOLD}[E]{Fore.RESET} Paket wurde nicht gefunden{Colors.RESET}"
    FinishedDownloading = f"Download abgeschlossen für"
    StrGet = "Holen"
    UnknownError = f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unbekannter Fehler{Colors.RESET}"
    Canceled = f"{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Prozess wurde abgebrochen!{Colors.RESET}"
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Die Paketdatenbank wurde noch nicht synchronisiert. Führe {Fore.CYAN}spkg sync{Fore.RESET} aus, um die Datenbank zu synchronisieren{Colors.RESET}"
    SearchingDatabaseForPackage = f"{Colors.BOLD}Durchsuche Datenbank nach Paket ...{Colors.RESET}"
    ContinePackageInstallation1 = f"{Colors.RESET}Das Setup Script für {Fore.CYAN + Colors.BOLD}"
    ContinePackageInstallation2 = f"{Colors.RESET} wird nun heruntergeladen. Fortfahren? [J/N]{Fore.RESET}{Colors.RESET}"
    Abort = "Abbruch ... "
    ExecutingSetup = f"Setup Script wird ausgeführt... Bitte warten"
    InstallingToSandboxEnv = f"{Fore.CYAN + Colors.BOLD}[!]{Fore.RESET} Paket wird in der Sandbox installiert."
    WorldDatabaseNotBuilded = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Die lokale World Datenbank wurde noch nicht aufgebaut. Ist deine spkg Installation korrupt? (Versuche {Fore.CYAN + Colors.BOLD}spkg build world{Fore.RESET} auszuführen){Colors.RESET + Fore.RESET}"
    PackageNotInstalled = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} Paket ist nicht installiert, es gibt nichts zu entfernen.{Colors.RESET}"
    SearchingWorldForPackage = f"{Colors.BOLD}Durchsuche lokale World Datenbak nach installierten Paket ...{Colors.RESET}"


elif language == "en":
    PackageNotFound = f"{Fore.RED  + Colors.BOLD}[E]{Fore.RESET} Package not found{Colors.RESET}"
    FinishedDownloading = f"Finished downloading"
    StrGet = "Get"
    UnknownError = f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unknown Error{Colors.RESET}"
    Canceled = f"{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Process canceled!{Colors.RESET}"
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The package database has not been synchronized yet. Run {Fore.CYAN}spkg sync{Fore.RESET} to synchronize the database{Colors.RESET}"
    SearchingDatabaseForPackage = f"{Colors.BOLD}Searching through the database ...{Colors.RESET}"
    ContinePackageInstallation1 = f"{Colors.RESET}The setup script for {Fore.CYAN + Colors.BOLD}"
    ContinePackageInstallation2 = f"{Colors.RESET} will now be downloaded. Continue? [Y/N]{Fore.RESET}{Colors.RESET}"
    Abort = "Aborting ..."
    ExecutingSetup = f"Executing Setup Script... Please wait"
    InstallingToSandboxEnv = f"{Fore.CYAN + Colors.BOLD}[!]{Fore.RESET} Package will be installed to the sandbox."
    WorldDatabaseNotBuilded = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The local world database has not been built yet. Is your spkg installation corrupt? (Try running {Fore.CYAN + Colors.BOLD}spkg build world{Fore.RESET}){Colors.RESET + Fore.RESET}"
    PackageNotInstalled = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} Package is not installed, there is nothing to uninstall.{Colors.RESET}"
    SearchingWorldForPackage = f"{Colors.BOLD}Searching through the local world database for the installed package ...{Colors.RESET}"
    

try:
    db = sql.connect(package_database)
    c = db.cursor()

except OperationalError:
    print(PackageDatabaseNotSynced)
    exit()

try:
    db_world = sql.connect(world_database)
    c_world = db_world.cursor()

except OperationalError:
    print(WorldDatabaseNotBuilded)
    exit()

with open(user_sandbox_config, "r") as f:
    user_sandbox_cfg = json.load(f)
    
bootstrap_location = user_sandbox_cfg['bootstrap_location']
sandbox_handler = user_sandbox_cfg['sandbox_handler']

""" 
    **** REMOVE FUNCTION ****
    This function removes packages, depending on various plugins, e.g. if the sandbox is enabled or not. 
"""
def remove(name):      
    # Create and start the spinner for searching the database  
    spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
                             'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    spinner_db_search.start()
    
    # Try selecting name, fetch_url, file_name, setup_script from the database
    try:
        c.execute("SELECT name, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

    except OperationalError:
                print(PackageDatabaseNotSynced)
                exit()
    
    # For-loop the results           
    for row in c:
        setup_script = row[3]
        
        # stop the spinner
        spinner_db_search.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
        
        
        # ask if you want to continue the package removing process
        try:
            continue_pkg_removing = input(f"{ContinePackageInstallation1}{name}{Colors.RESET}{ContinePackageInstallation2} ")

        # If you press ^C, it prints out a error message
        except KeyboardInterrupt as e:
            print(f"\n{Canceled}")
            exit()

        # Check if you want to continue the installation
        if continue_pkg_removing.lower() == "j":
            continue

        elif continue_pkg_removing.lower() == "y":
            continue
        
        elif continue_pkg_removing.lower() == "":
            continue
        
        # If you press any other key, it prints out an error message
        else:
            print(Abort)
            exit()

    try:
        # Start the setup spinner
        spinner_setup = Halo(text=f"{StrGet}: {setup_script}", spinner={'interval': 150, 'frames': [
                       '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
        spinner_setup.start()

        # request the setup url 
        setup_request = urllib.request.Request(
            setup_script,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )

        pkgbuild_file = urllib.request.urlopen(setup_request)


        # If the package needs to be "installed" natively, continue the installation without the sandbox plugin
        if force_no_sandbox(name) == 1:
                with open("/tmp/PKGBUILD", 'wb') as file_setup:
                    file_setup.write(pkgbuild_file.read())
        
        # Else check if the sandbox plugin is enabled
        else:
            if check_plugin_enabled_silent("sandbox") == True:
                with open(f"{bootstrap_location}/tmp/PKGBUILD", 'wb') as file_setup:
                    file_setup.write(pkgbuild_file.read())
                    
            # If not, save the PKGBUILD file natively
            else:
                with open("/tmp/PKGBUILD", 'wb') as file_setup:
                    file_setup.write(pkgbuild_file.read())

        # Stop the Setup Spinner
        spinner_setup.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[|] {Fore.RESET}{StrGet}: {setup_script}{Colors.RESET}")
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")
        
        
        # Execute the PKGBUILD File natively if the package needs to be "installed" natively
        if force_no_sandbox(name) == 1:
            subprocess.run(['sudo', 'chmod', '+x', '/tmp/PKGBUILD'])
            subprocess.run(['sudo', 'bash', '/tmp/PKGBUILD', '--remove'])
        
        # Else check if the sandbox plugin is enabled
        else:
            if check_plugin_enabled_silent("sandbox") == True:
                os.system(f"sudo chroot {bootstrap_location} bash /tmp/PKGBUILD --remove")
                
            # If not, run the PKGBUILD file natively
            else:
                subprocess.run(['sudo', 'chmod', '+x', '/tmp/PKGBUILD'])
                subprocess.run(['sudo', 'bash', '/tmp/PKGBUILD', '--remove'])
                
    # Catch HTTPError, NameError and KeyboardInterrupt errors
    except HTTPError as e:
        print(UnknownError)
        print(e)

    except NameError as e:
        print(f"\n{PackageNotFound}")
        exit()

    except KeyboardInterrupt as e:
        print(f"\n{Canceled}")
        exit()


# Sandbox Remove
def sandbox_remove(name):        
    spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
                             'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    spinner_db_search.start()
    
    try:
        c.execute("SELECT name, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

    except OperationalError:
                print(PackageDatabaseNotSynced)
                exit()
                
    for row in c:
        setup_script = row[3]

        spinner_db_search.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
        
        
        try:
            continue_pkg_installation = input(f"{ContinePackageInstallation1}{name}{Colors.RESET}{ContinePackageInstallation2} ")

        except KeyboardInterrupt as e:
            print(f"\n{Canceled}")
            exit()

        if continue_pkg_installation.lower() == "j":
            continue

        elif continue_pkg_installation.lower() == "y":
            continue

        else:
            print(Abort)
            exit()
        
    try:
        req = urllib.request.Request(
            setup_script,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )

        f = urllib.request.urlopen(req)

        spinner_setup = Halo(text=f"{StrGet}: {setup_script}", spinner={'interval': 150, 'frames': [
                       '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
        spinner_setup.start()

        setup_req = urllib.request.Request(
            setup_script,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )

        f_setup = urllib.request.urlopen(setup_req)

        with open(f"{bootstrap_location}/tmp/{row[0]}.setup", 'wb') as file_setup:
            file_setup.write(f_setup.read())

        spinner_setup.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET}{StrGet}: {setup_script}{Colors.RESET}")
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

        os.system(f"sudo chroot {bootstrap_location} bash /tmp/{row[0]}.setup --remove")

    except HTTPError as e:
        print(UnknownError)
        print(e)

    except NameError as e:
        print(f"\n{PackageNotFound}")
        exit()

    except KeyboardInterrupt as e:
        print(f"\n{Canceled}")
        exit()