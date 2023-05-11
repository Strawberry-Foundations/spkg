#!/usr/bin/env python3

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
from plugin_daemon import plugin_daemon, check_plugin_enabled_silent, check_plugin_enabled_ret
from .force_no_sandbox import *
from defs import *

language = spkg_cfg_data['language']

if not language == "de" and not language == "en":
    print(f"{Fore.RED}You have either a corrupted or unconfigured config file! Please check the language settings!")

if language == "de":
    PackageNotFound = f"{Fore.RED + Colors.BOLD}[E]{Fore.RESET} Paket wurde nicht gefunden{Colors.RESET}"
    FinishedDownloading = f"Download abgeschlossen für"
    StrGet = "Holen"
    UnknownError = f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unbekannter Fehler{Colors.RESET}"
    Canceled = f"{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Prozess wurde abgebrochen!{Colors.RESET}"
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Die Paketdatenbank wurde noch nicht synchronisiert. Führe {Fore.CYAN}spkg sync{Fore.RESET} aus, um die Datenbank zu synchronisieren{Colors.RESET}"
    SearchingDatabaseForPackage = f"{Colors.BOLD}Durchsuche Datenbank nach Paket ...{Colors.RESET}"
    ContinePackageInstallation1 = f"{Colors.RESET}Das Paket {Fore.CYAN + Colors.BOLD}"
    ContinePackageInstallation2 = f"{Colors.RESET} wird nun heruntergeladen. \nDafür müssen "
    ContinePackageInstallation3 = f"{Colors.RESET} heruntergeladen werden. Fortfahren? [J/N]{Fore.RESET}{Colors.RESET}"
    Abort = "Abbruch ... "
    ExecutingSetup = f"Setup Script wird ausgeführt... Bitte warten"
    InstallingToSandboxEnv = f"{Fore.CYAN + Colors.BOLD}[!]{Fore.RESET} Paket wird in der Sandbox installiert."
    ForceNoSandbox = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} Warnung: Paket kann nicht in der Sandbox installiert werden: Es ist Host-only.{Colors.RESET}"


elif language == "en":
    PackageNotFound = f"{Fore.RED  + Colors.BOLD}[E]{Fore.RESET} Package not found{Colors.RESET}"
    FinishedDownloading = f"Finished downloading"
    StrGet = "Get"
    UnknownError = f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unknown Error{Colors.RESET}"
    Canceled = f"{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Process canceled!{Colors.RESET}"
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The package database has not been synchronized yet. Run {Fore.CYAN}spkg sync{Fore.RESET} to synchronize the database{Colors.RESET}"
    SearchingDatabaseForPackage = f"{Colors.BOLD}Searching through the database ...{Colors.RESET}"
    ContinePackageInstallation1 = f"{Colors.RESET}The package {Fore.CYAN + Colors.BOLD}"
    ContinePackageInstallation2 = f"{Colors.RESET} will now be downloaded. \nThis requires "
    ContinePackageInstallation3 = f"{Colors.RESET} to be downloaded. Continue? [Y/N]{Fore.RESET}{Colors.RESET}"
    Abort = "Aborting ..."
    ExecutingSetup = f"Executing Setup Script... Please wait"
    InstallingToSandboxEnv = f"{Fore.CYAN + Colors.BOLD}[!]{Fore.RESET} Package will be installed to the sandbox."
    ForceNoSandbox = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} Warning: Package cannot be installed in the sandbox: It is host-only.{Colors.RESET}"

if check_plugin_enabled_ret("sandbox") == True:
    plugin_daemon.import_plugin("sandbox")
else:
    pass


# Check if user config path exists
if not os.path.exists(f"{home_dir}/.config/spkg"):
    os.mkdir(f"{home_dir}/.config/spkg")
    os.system(f"rm -rf {home_dir}/.config/spkg")
    os.mkdir(f"{home_dir}/.config/spkg")
    os.system(f"touch {user_sandbox_config}")
    os.system("sh -c 'echo {} >> " + user_sandbox_config + "'")
    
    with open(user_sandbox_config, "r") as f:
        data = json.load(f)
    
    data["bootstrap_location"] = f"{home_dir}/.local/spkg/sandbox/"
    data["sandbox_handler"] = "chroot"
    
    with open(user_sandbox_config, 'w') as f:
        json.dump(data, f)

bootstrap_location = user_sandbox_cfg_data['bootstrap_location']
sandbox_handler = user_sandbox_cfg_data['sandbox_handler']

if arch == "x86_64":
    arch = "amd64"

elif arch == "x86":
    arch = "i386"

elif arch == "aarch64":
    arch = "arm64"


class Package:
    # Install
    def install(name):
        # Create and start the spinner for searching the database
        spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
                                'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
        spinner_db_search.start()

        # Select architecture of package where package name
        c.execute("SELECT arch FROM packages where name = ?", (name,))

        # fetch the results
        try:
            result = c.fetchone()[0]

        except TypeError:
            print(PackageNotFound)
            exit()

        # If the package_architecture is all, try to find the corresponding package
        if result == "all":
            try:
                c.execute(
                    "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

            except OperationalError:
                print(PackageDatabaseNotSynced)
                exit()
                
        # If not, try to find the corresponding package depending on the available architecture
        else:
            try:
                c.execute(
                    "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ? AND arch = ?", (name, arch))

            except OperationalError:
                print(PackageDatabaseNotSynced)
                exit()

        # For-loop the results
        for row in c:
            package_url = row[1]
            filename = row[2]
            pkgbuild_url = row[3]

            # get the response of the package header
            response = requests.head(package_url)
            
            # fetch the size of the package and convert it to mbytes 
            file_size_bytes = int(response.headers.get('Content-Length', 0))
            file_size_mb = file_size_bytes / (1024 * 1024)

            # stop the spinner
            spinner_db_search.stop()
            print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
            
            # ask if you want to continue the installation
            try:
                continue_pkg_installation = input(
                    f"{ContinePackageInstallation1}{filename}{Colors.RESET}{ContinePackageInstallation2}{round(file_size_mb, 2)} MB{ContinePackageInstallation3} ")

            # If you press ^C, it prints out a error message
            except KeyboardInterrupt as e:
                print(f"\n{Canceled}")
                exit()

            # Check if you want to continue the installation
            if continue_pkg_installation.lower() == "j":
                continue

            elif continue_pkg_installation.lower() == "y":
                continue
            
            elif continue_pkg_installation.lower() == "":
                continue
            
            # If you press any other key, it prints out an error message
            else:
                print(Abort)
                exit()
                
        # Try to request the package url 
        try:
            package_request = urllib.request.Request(
                package_url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
            )

            package_file = urllib.request.urlopen(package_request)
            
            # Start the download timer
            download_time_start = time.time()

            # Start download spinner
            spinner_package = Halo(text=f"{StrGet}: {package_url}", spinner={'interval': 150, 'frames': [
                        '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
            spinner_package.start()
            
            # Check if the sandbox plugin is enabled
            if check_plugin_enabled_silent("sandbox") == True:
                
                # If the package needs to be installed natively, continue the installation without the sandbox plugin
                if force_no_sandbox(name) == 1:
                    print()
                    print(ForceNoSandbox)
                    time.sleep(5)
                    with open(f"/tmp/{filename}", 'wb') as file:
                        file.write(package_file.read())
                
                # If not just continue with the sandbox plugin   
                else:
                    with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
                        file.write(package_file.read())
            
            # (M) Else 
            else:
                # (A) (M) Check if the sandbox plugin is enabled
                if check_plugin_enabled_silent("sandbox") == True:
                    with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
                        file.write(package_file.read())

                # If not, save the package natively
                else:
                    with open(f"/tmp/{filename}", 'wb') as file:
                        file.write(package_file.read())

            # Stop the download timer
            download_time_end = time.time()
            
            # Stop download spinner
            spinner_package.stop()
            
            # Print download finished message
            print(f"\n{FinishedDownloading} {Fore.LIGHTCYAN_EX + Colors.BOLD}{filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")

            # Start the setup spinner
            spinner_setup = Halo(text=f"{ExecutingSetup}: {package_url}", spinner={'interval': 150, 'frames': [
                '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
            spinner_setup.start()
            
            # request the setup url 
            setup_request = urllib.request.Request(
                pkgbuild_url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
            )

            pkgbuild_file = urllib.request.urlopen(setup_request)

            # If the package needs to be installed natively, continue the installation without the sandbox plugin
            if force_no_sandbox(name) == 1:
                    with open(f"/tmp/{row[0]}.setup", 'wb') as file_setup:
                        file_setup.write(pkgbuild_file.read())
            
            # Else check if the sandbox plugin is enabled
            else:
                if check_plugin_enabled_silent("sandbox") == True:
                    with open(f"{bootstrap_location}/tmp/{row[0]}.setup", 'wb') as file_setup:
                        file_setup.write(pkgbuild_file.read())
                        
                # If not, save the PKGBUILD file natively
                else:
                    with open(f"/tmp/{row[0]}.setup", 'wb') as file_setup:
                        file_setup.write(pkgbuild_file.read())

            # Stop the Setup Spinner
            spinner_setup.stop()
            print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

            # Execute the PKGBUILD File natively if the package needs to be installed natively
            if force_no_sandbox(name) == 1:
                subprocess.run(['sudo', 'chmod', '+x', f'/tmp/{row[0]}.setup'])
                subprocess.run(['sudo', 'bash', f'/tmp/{row[0]}.setup'])
            
            # Else check if the sandbox plugin is enabled
            else:
                if check_plugin_enabled_silent("sandbox") == True:
                    os.system(f"sudo chroot {bootstrap_location} bash /tmp/{row[0]}.setup")
                    
                # If not, run the PKGBUILD file natively
                else:
                    subprocess.run(['sudo', 'chmod', '+x', f'/tmp/{row[0]}.setup'])
                    subprocess.run(['sudo', 'bash', f'/tmp/{row[0]}.setup'])

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


# Upgrade
def upgrade(name):
    spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
                             'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    spinner_db_search.start()

    c.execute("SELECT arch FROM packages where name = ?", (name,))

    try:
        result = c.fetchone()[0]

    except TypeError:
        print(f"\n{PackageNotFound}")
        exit()

    if result == "all":
        try:
            c.execute(
                "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()

    else:
        try:
            c.execute(
                "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ? AND arch = ?", (name, arch))

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()

    for row in c:
        url = row[1]
        filename = row[2]
        setup_script = row[3]

        response = requests.head(url)
        file_size_bytes = int(response.headers.get('Content-Length', 0))
        file_size_mb = file_size_bytes / (1024 * 1024)

        spinner_db_search.stop()
        print(
            f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
        try:
            continue_pkg_installation = input(
                f"{ContinePackageInstallation1}{filename}{Colors.RESET}{ContinePackageInstallation2}{round(file_size_mb, 2)} MB{ContinePackageInstallation3} ")

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
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )

        f = urllib.request.urlopen(req)

        download_time_start = time.time()

        spinner = Halo(text=f"{StrGet}: {url}", spinner={'interval': 150, 'frames': [
                       '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
        spinner.start()
        
        if check_plugin_enabled_silent("sandbox") == True:
            if force_no_sandbox(name) == 1:
                print()
                print(ForceNoSandbox)
                time.sleep(5)
                with open(f"/tmp/{filename}", 'wb') as file:
                    file.write(f.read())
                    
            else:
                with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
                    file.write(f.read())
        else:
            if check_plugin_enabled_silent("sandbox") == True:
                with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
                    file.write(f.read())

            else:
                with open(f"/tmp/{filename}", 'wb') as file:
                    file.write(f.read())

        download_time_end = time.time()
        print(f"\n{FinishedDownloading} {Fore.LIGHTCYAN_EX + Colors.BOLD}{filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")

        spinner_setup = Halo(text=f"{ExecutingSetup}: {url}", spinner={'interval': 150, 'frames': [
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
        
        if force_no_sandbox(name) == 1:
                with open(f"/tmp/{row[0]}.setup", 'wb') as file_setup:
                    file_setup.write(f_setup.read())
                    
        else:
            if check_plugin_enabled_silent("sandbox") == True:
                with open(f"{bootstrap_location}/tmp/{row[0]}.setup", 'wb') as file_setup:
                    file_setup.write(f_setup.read())

            else:
                with open(f"/tmp/{row[0]}.setup", 'wb') as file_setup:
                    file_setup.write(f_setup.read())

        spinner_setup.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

        spinner.stop()

        if force_no_sandbox(name) == 1:
            subprocess.run(['sudo', 'chmod', '+x', f'/tmp/{row[0]}.setup'])
            subprocess.run(['sudo', 'bash', f'/tmp/{row[0]}.setup', '--upgrade'])
            
        else:
            if check_plugin_enabled_silent("sandbox") == True:
                os.system(f"sudo chroot {bootstrap_location} bash /tmp/{row[0]}.setup --upgrade")

            else:
                subprocess.run(['sudo', 'chmod', '+x', f'/tmp/{row[0]}.setup'])
                subprocess.run(['sudo', 'bash', f'/tmp/{row[0]}.setup', '--upgrade'])

    except HTTPError as e:
        print(UnknownError)
        print(e)

    except NameError as e:
        print(f"\n{PackageNotFound}")
        exit()

    except KeyboardInterrupt as e:
        print(f"\n{Canceled}")
        exit()
        

# Sandbox Install
def sandbox_install(name):
    if force_no_sandbox(name) == 1:
            print(ForceNoSandbox)
            print(Abort)
            exit()
            
    print(InstallingToSandboxEnv)
    spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
                             'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    spinner_db_search.start()

    c.execute("SELECT arch FROM packages where name = ?", (name,))

    try:
        result = c.fetchone()[0]

    except TypeError:
        print(PackageNotFound)
        exit()

    if result == "all":
        try:
            c.execute(
                "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ?", (name,))

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()

    else:
        try:
            c.execute(
                "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ? AND arch = ?", (name, arch))

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()

    for row in c:
        url = row[1]
        filename = row[2]
        setup_script = row[3]

        response = requests.head(url)
        file_size_bytes = int(response.headers.get('Content-Length', 0))
        file_size_mb = file_size_bytes / (1024 * 1024)

        spinner_db_search.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
        try:
            continue_pkg_installation = input(
                f"{ContinePackageInstallation1}{filename}{Colors.RESET}{ContinePackageInstallation2}{round(file_size_mb, 2)} MB{ContinePackageInstallation3} ")

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
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )

        f = urllib.request.urlopen(req)

        download_time_start = time.time()

        spinner = Halo(text=f"{StrGet}: {url}", spinner={'interval': 150, 'frames': [
                       '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
        spinner.start()
        
        with open(f"{bootstrap_location}/tmp/{filename}", 'wb') as file:
            file.write(f.read())
            
        download_time_end = time.time()
        print(f"\n{FinishedDownloading} {Fore.LIGHTCYAN_EX + Colors.BOLD}{filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")

        spinner_setup = Halo(text=f"{ExecutingSetup}: {url}", spinner={'interval': 150, 'frames': [
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
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

        spinner.stop()

        os.system(f"sudo chroot {bootstrap_location} bash /tmp/{row[0]}.setup")

    except HTTPError as e:
        print(UnknownError)
        print(e)

    except NameError as e:
        print(f"\n{PackageNotFound}")
        exit()

    except KeyboardInterrupt as e:
        print(f"\n{Canceled}")
        exit()