#!/usr/bin/env python3

import os
import sys
import time
import json
import sqlite3 as sql
import urllib.request

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore, Back, Style
from halo import Halo
import requests
import subprocess

version = "1.1.2"


class Colors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


with open("/etc/spkg/config.json", "r") as f:
    data = json.load(f)

language = data['language']

if not language == "de" and not language == "en":
    print(f"{Fore.RED}You have either a corrupted or unconfigured config file! Please check the language settings!")

if language == "de":
    NoArgument = f"{Fore.RED + Colors.BOLD}[E]{Fore.RESET} Kein Argument angegeben!{Colors.RESET}"
    PackageNotFound = f"{Fore.RED + Colors.BOLD}[E]{Fore.RESET} Paket wurde nicht gefunden{Colors.RESET}"
    PackageInformationTitle = f"{Colors.BOLD + Colors.UNDERLINE}Information über das Paket"
    FinishedDownloading = f"Download abgeschlossen für"
    StrGet = "Holen"
    UnknownError = f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unbekannter Fehler{Colors.RESET}"
    StrArchitecture = "Architektur"
    SyncingPackageDatabase = f"Synchronisieren von"
    SuccessSyncingPackageDatabase = f"{Colors.BOLD}Die Paketdatenbank wurde synchronisiert. Führe {Fore.CYAN}spkg update{Fore.RESET} aus, um nach Paketupdates zu suchen.{Colors.RESET}"
    Canceled = f"{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Prozess wurde abgebrochen!{Colors.RESET}"
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Die Paketdatenbank wurde noch nicht synchronisiert. Führe {Fore.CYAN}spkg sync{Fore.RESET} aus, um die Datenbank zu synchronisieren{Colors.RESET}"
    SearchingDatabaseForPackage = f"{Colors.BOLD}Durchsuche Datenbank nach Paket ...{Colors.RESET}"
    ContinePackageInstallation1 = f"{Colors.RESET}Das Paket {Fore.CYAN + Colors.BOLD}"
    ContinePackageInstallation2 = f"{Colors.RESET} wird nun heruntergeladen. \nDafür müssen "
    ContinePackageInstallation3 = f"{Colors.RESET} heruntergeladen werden. Fortfahren? [J/N]{Fore.RESET}{Colors.RESET}"
    Abort = "Abbruch ... "
    ExecutingSetup = f"Setup Script wird ausgeführt... Bitte warten"
    MissingPermissons = f"{Colors.BOLD}Fehlende Berechtigung{Colors.RESET}"
    MissingPermissonsPackageDatabaseUpdate = f"{Fore.RED + Colors.BOLD}Die Paketdatenbank konnte nicht aktualisiert werden. (Wird spkg als Root ausgeführt?){Colors.RESET}"


elif language == "en":
    NoArgument = f"{Fore.RED + Colors.BOLD}[E]{Fore.RESET} No Argument passed!{Colors.RESET}"
    PackageNotFound = f"{Fore.RED  + Colors.BOLD}[E]{Fore.RESET} Package not found{Colors.RESET}"
    PackageInformationTitle = f"{Colors.BOLD + Colors.UNDERLINE}Information about the package"
    FinishedDownloading = f"Finished downloading"
    StrGet = "Get"
    UnknownError = f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unknown Error{Colors.RESET}"
    StrArchitecture = "Architecture"
    SyncingPackageDatabase = f"Synchronize from"
    SuccessSyncingPackageDatabase = f"{Colors.BOLD}The package database has been synchronized. Run {Fore.CYAN}spkg update{Fore.RESET} to check for package updates.{Colors.RESET}"
    Canceled = f"{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Process canceled!{Colors.RESET}"
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The package database has not been synchronized yet. Run {Fore.CYAN}spkg sync{Fore.RESET} to synchronize the database{Colors.RESET}"
    SearchingDatabaseForPackage = f"{Colors.BOLD}Searching trough the database ...{Colors.RESET}"
    ContinePackageInstallation1 = f"{Colors.RESET}The package {Fore.CYAN + Colors.BOLD}"
    ContinePackageInstallation2 = f"{Colors.RESET} will now be downloaded. \nThis requires "
    ContinePackageInstallation3 = f"{Colors.RESET} to be downloaded. Continue? [Y/N]{Fore.RESET}{Colors.RESET}"
    Abort = "Aborting ..."
    ExecutingSetup = f"Executing Setup Script... Please wait"
    MissingPermissons = f"{Colors.BOLD}Missing Permissons{Colors.RESET}"
    MissingPermissonsPackageDatabaseUpdate = f"{Fore.RED + Colors.BOLD}The package database could not be updated. (Is spkg running as root?){Colors.RESET}"


def help_en():
    print(f"{Colors.UNDERLINE + Colors.BOLD}Advanced Source Package Managment (spkg) {version}{Colors.RESET}\n")
    print(
        f"{Fore.CYAN + Colors.BOLD}Usage:{Fore.RESET} spkg {Fore.GREEN}[command]{Fore.RED} <argument>\n")
    print(f"spkg is a package manager that downloads the source code from the \nofficial sources, and then compiles it specifically for your device.")
    print(f"The goal of spkg is to get the latest versions of programs easily and \nwithout much experience, even under distros that do not offer the latest version.")
    print(f"By compiling the package, the program is optimized for your device and can run faster.")
    print(f"So spkg offers you a high security, so you don't have to worry about viruses in packages.\n")
    print(f"{Colors.UNDERLINE + Colors.BOLD}Commands:{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}info:{Fore.RESET} Gives you information about a specific package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}download:{Fore.RESET} Downloads a specific package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}install:{Fore.RESET} Installs the specified package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}sync:{Fore.RESET} Syncronizes the package database{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}update:{Fore.RESET} Checks if an update is available for an installed package{Colors.RESET} (not available yet)")
    print(f"{Colors.BOLD} -> {Fore.BLUE}upgrade:{Fore.RESET} Updates all available package updates{Colors.RESET} (not available yet)")
    print(f"\n{Colors.BOLD}Copyright Juliandev02 2023 (C) - Made with <3")


def help_de():
    print(f"{Colors.UNDERLINE + Colors.BOLD}Advanced Source Package Managment (spkg) {version}{Colors.RESET}\n")
    print(
        f"{Fore.CYAN + Colors.BOLD}Aufruf:{Fore.RESET} spkg {Fore.GREEN}[Befehl]{Fore.RED} <Argument>\n")
    print(f"spkg ist ein Paketmanager, der den Quellcode von den \noffiziellen Quellen herunterlädt, und diesen dann spezifisch für dein Gerät kompiliert.")
    print(f"Das Ziel von spkg ist, einfach und auch ohne viel Erfahrungen die neusten Versionen \nvon Programmen zu erhalten, auch unter Distrobutionen die nicht die neuste Version anbieten.")
    print(f"Durch das kompilieren des Paketes ist das Programm für dein Gerät optimiert und kann schneller laufen.")
    print(f"So bietet dir spkg eine hohe Sicherheit, sodass du dir keine Sorgen um Viren in Paketen machen musst.\n")
    print(f"{Colors.UNDERLINE + Colors.BOLD}Befehle:{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}info:{Fore.RESET} Gibt dir Informationen über ein bestimmtes Paket aus{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}download:{Fore.RESET} Downloads a specific package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}install:{Fore.RESET} Installiert das angegebene Paket{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}sync:{Fore.RESET} Syncronisiert die Paketdatenbank{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}update:{Fore.RESET} Überprüft, ob ein Update für die installierten Pakete verfügbar ist{Colors.RESET} (Noch nicht verfügbar)")
    print(f"{Colors.BOLD} -> {Fore.BLUE}upgrade:{Fore.RESET} Aktualisiert alle verfügbaren Paketupdates{Colors.RESET} (Noch nicht verfügbar)")
    print(f"\n{Colors.BOLD}Copyright Juliandev02 2023 (C) - Made with <3")


db = sql.connect("/etc/spkg/package.db")
c = db.cursor()


# * --- Package Info Function --- *
if len(sys.argv) > 1 and sys.argv[1] == "info":
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(NoArgument)
        exit()
    try:
        c.execute("SELECT name FROM packages where name = ?", (pkg_name,))

    except OperationalError:
        print(PackageDatabaseNotSynced)
        exit()

    if c.fetchall():
        c.execute(
            "SELECT name, version, branch, arch, fetch_url, setup_script FROM packages where name = ?", (pkg_name,))
        for row in c:
            print(
                f"{Colors.BOLD + Colors.UNDERLINE}{PackageInformationTitle} {row[0]} ({row[1]})\n{Colors.RESET}")
            print("Name:", row[0])
            print("Version:", row[1])
            print("Branch:", row[2])
            print(f"{StrArchitecture}:", row[3])
            print("Download URL:", row[4])
            print("Setup URL:", row[5])

    else:
        print(PackageNotFound)

    db.close()


# * --- Download Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "download":
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(NoArgument)
        exit()

    try:
        c.execute(
            "SELECT name, fetch_url, file_name FROM packages where name = ?", (pkg_name,))

    except OperationalError:
        print(PackageDatabaseNotSynced)
        exit()

    for row in c:
        url = row[1]
        filename = row[2]

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

        with open(filename, 'wb') as file:
            file.write(f.read())

        download_time_end = time.time()
        print(f"\n{FinishedDownloading} {Fore.LIGHTCYAN_EX + Colors.BOLD}{filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")

    except HTTPError as e:
        print(UnknownError)
        print(e)

    except NameError as e:
        print(PackageNotFound)


# * --- Sync Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "sync":
    with open("/etc/spkg/repositories.json", "r") as f:
        data = json.load(f)
        
    

    repo = f"{data['main']}/package.db"
    filename = "/etc/spkg/package.db"
    
    if os.geteuid() == 0:
        None
    else:
        print(f"{Fore.CYAN}{filename}{Fore.RESET + Colors.BOLD}: {MissingPermissons}")
        print(MissingPermissonsPackageDatabaseUpdate)
        exit()

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

        spinner = Halo(text=f"{SyncingPackageDatabase} {data['main']} ...", spinner={
                       'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
        spinner.start()

        with open(filename, 'wb') as file:
            file.write(f.read())

        download_time_end = time.time()
        print(f"\n{SuccessSyncingPackageDatabase}{Colors.RESET}")

    except HTTPError as e:
        print(UnknownError)
        print(e)


# * --- List Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "list":
    try:
        c.execute("SELECT * FROM packages")
        for row in c:
            print(
                f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{Fore.RESET}")

    except OperationalError:
        print(PackageDatabaseNotSynced)


# * --- Install Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "install":
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(NoArgument)
        exit()

    spinner_db_search = Halo(text=f"{SearchingDatabaseForPackage}", spinner={
                             'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    spinner_db_search.start()

    try:
        c.execute(
            "SELECT name, fetch_url, file_name, setup_script FROM packages where name = ?", (pkg_name,))

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

        with open(f"/tmp/{row[0]}.setup", 'wb') as file_setup:
            file_setup.write(f_setup.read())

        spinner_setup.stop()
        print(
            f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{ExecutingSetup}")

        spinner.stop()
        subprocess.run(['sudo', 'chmod', '+x', f'/tmp/{row[0]}.setup'])
        subprocess.run(['sudo', 'bash', f'/tmp/{row[0]}.setup'])

    except HTTPError as e:
        print(UnknownError)
        print(e)

    except NameError as e:
        print(f"\n{PackageNotFound}")

    except KeyboardInterrupt as e:
        print(f"\n{Canceled}")


# * --- Help Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "help":
    if language == "en":
        help_en()
    elif language == "de":
        help_de()

else:
    if language == "en":
        help_en()
    elif language == "de":
        help_de()


db.close()
