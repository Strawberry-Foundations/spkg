#!/usr/bin/env python3

"""
    Copyright (C) 2023 Juliandev02

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


from init import *

import os
import sys
import time
import json
import sqlite3 as sql
import urllib.request
import platform
import subprocess

from sqlite3 import *
from urllib.error import HTTPError, URLError
from colorama import Fore
from halo import Halo
from sys import exit

from src.plugin_daemon import *
from src.install import * 
from src.remove import * 
from src.download import *
from src.force_no_sandbox import *
from src.arch import ARCH
from src.db import * 
from src.vars import *
from src.functions import *

# import hardcoded plugin sandbox only if it's enabled
if check_plugin_enabled_ret("sandbox") == True:
    PluginDaemon.import_plugin("sandbox")
else:
    pass

NoArgument = f"{Fore.RED + Colors.BOLD}[E]{Fore.RESET} No Argument passed!{Colors.RESET}"
PackageNotFound = f"{Fore.RED  + Colors.BOLD}[E]{Fore.RESET} Package not found{Colors.RESET}"
PackageInformationTitle = f"{Colors.BOLD + Colors.UNDERLINE}Information about the package"
FinishedDownloading = f"Finished downloading"
FinishedDownloadingCompact = f"Finished downloading"
StrGet = "Get"
UnknownError = f"{Fore.RED + Colors.BOLD}[?]{Fore.RESET} Unknown Error{Colors.RESET}"
StrArchitecture = "Architecture"
SyncingPackageDatabase = f"Synchronize from"
SuccessSyncingPackageDatabase = f"{Colors.BOLD}The package database has been synchronized in %s s. Run {Fore.CYAN}spkg update{Fore.RESET} to check for package updates.{Colors.RESET}"
Canceled = f"{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Process canceled!{Colors.RESET}"
PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The package database has not been synchronized yet. Run {Fore.CYAN}spkg sync{Fore.RESET} to synchronize the database{Colors.RESET}"
SearchingDatabaseForPackage = f"{Colors.BOLD}Searching through the database ...{Colors.RESET}"
ContinePackageInstallation1 = f"{Colors.RESET}The package {Fore.CYAN + Colors.BOLD}"
ContinePackageInstallation2 = f"{Colors.RESET} will now be downloaded. \nThis requires "
ContinePackageInstallation3 = f"{Colors.RESET} to be downloaded. Continue? [Y/N]{Fore.RESET}{Colors.RESET}"
Abort = "Aborting ..."
ExecutingSetup = f"Executing Setup Script... Please wait"
MissingPermissons = f"{Fore.RESET + Colors.RESET}: Missing Permissons"
MissingPermissonsPackageDatabaseUpdate = f"{Fore.RED + Colors.BOLD}The package database could not be updated. (Is spkg running as root?){Colors.RESET}"
SearchingForUpdates = f"Suche nach verfügbaren Updates ..."
WorldDatabaseNotBuilded = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The local world database has not been built yet. Is your spkg installation corrupt? (Try running {Fore.CYAN + Colors.BOLD}spkg build world{Fore.RESET}){Colors.RESET + Fore.RESET}"
PackageAlreadyInstalled = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} Package has already been installed. There is nothing to do.{Colors.RESET}"
PackageNotInstalled = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} Package is not installed, there is nothing to upgrade.{Colors.RESET}"
PackageNotInstalledRemove = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} Package is not installed, there is nothing to uninstall.{Colors.RESET}"
BuildingWorldDatabase = f"{Colors.BOLD}The World database is downloaded and built ... {Colors.RESET}"
SuccessBuildingWorldDatabase = f"{Fore.GREEN + Colors.BOLD}[✓]{Fore.RESET} The World database was successfully built!{Colors.RESET}"
MissingPermissonsWorldDatabaseInsert = f"{Fore.RED + Colors.BOLD}The world database could not be written to. \nThe entry for the newly installed package could therefore not be inserted (Is spkg run as root?).{Colors.RESET}"
MissingPermissonsWorldDatabaseInsertRemove = f"{Fore.RED + Colors.BOLD}The world database could not be written to. \nThe entry for the newly removed package could therefore not be removed (Is spkg run as root?).{Colors.RESET}"
RecommendedRunningAsRoot = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} It is recommended to install packages as root (sudo). Otherwise permission problems could occur{Colors.RESET}"
RecommendedRunningAsRootRemove = f"{Fore.YELLOW + Colors.BOLD}[!]{Fore.RESET} It is recommended to remove packages as root (sudo). Otherwise permission problems could occur{Colors.RESET}"
PluginNotEnabled = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Plugin is not activated.{Colors.RESET}"
PluginIsAlreadyEnabled = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Plugin is already enabled.{Colors.RESET}"
PluginIsAlreadyDisabled = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Plugin is already disabled.{Colors.RESET}"
MissingPermissonsPluginConfig = f"{Fore.RED + Colors.BOLD}The plugin config could not be edited. (Is spkg running as root?){Colors.RESET}"
MissingPermissonsPluginInstallation = f"{Fore.RED + Colors.BOLD}The plugin could not be installed. (Is spkg running as root?){Colors.RESET}"
UnknownOperation = f"{Fore.RED + Colors.BOLD}[E]{Fore.RESET} Invalid Operation: {Colors.RESET}"
MissingPermissonsSpkgConfig = f"{Fore.RED + Colors.BOLD}The spkg config could not be edited. (Is spkg running as root?){Colors.RESET}"
ChangedLanguage = f"{Colors.BOLD}Changed language to {Fore.CYAN}%s{Fore.RESET}{Colors.RESET}"
UnknownLanguage = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Unknown Language.{Colors.RESET}"
UpgradeNotAsRoot = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Do not perform upgrades with root. This could manipulate the installation of the package!{Colors.RESET}"
ReinstallNotAsRoot = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Do not perform reinstallations with root. This could manipulate the installation of the package!{Colors.RESET}"
SearchingWorldForPackage = f"{Colors.BOLD}Searching through the local world database for the installed package ...{Colors.RESET}"
UserConfigNotExists2 = f"{Fore.YELLOW + Colors.BOLD}Warning:{Fore.RESET + Colors.RESET} Your user configuration does not exist. Try to create the configuration folder ..."
    
    
# Help Function for English Language
def help_en():
    print(f"{Colors.UNDERLINE + Colors.BOLD}Advanced Source Package Managment (spkg) {version} {platform.machine()}{Colors.RESET}\n")
    print(f"{Fore.CYAN + Colors.BOLD}Usage:{Fore.RESET} spkg {Fore.GREEN}[command]{Fore.RED} <argument>\n")
    print(f"spkg is a package manager that downloads the source code from the \nofficial sources, and then compiles it specifically for your device.")
    print(f"The goal of spkg is to get the latest versions of programs easily and \nwithout much experience, even under distros that do not offer the latest version.")
    print(f"By compiling the package, the program is optimized for your device and can run faster.")
    print(f"So spkg offers you a high security, so you don't have to worry about viruses in packages.\n")
    print(f"{Colors.UNDERLINE + Colors.BOLD}Commands:{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}install:{Fore.RESET} Installs the specified package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}reinstall:{Fore.RESET} Reinstalls the specified package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}remove:{Fore.RESET} Removes the specified package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}update:{Fore.RESET} Checks if an update is available for an installed package{Colors.RESET} (not available yet)")
    print(f"{Colors.BOLD} -> {Fore.BLUE}upgrade:{Fore.RESET} Updates all available package updates{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}sync:{Fore.RESET} Syncronizes the package database{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}info:{Fore.RESET} Gives you information about a specific package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}list:{Fore.RESET} Lists all available packages{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}download:{Fore.RESET} Downloads a specific package{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}build:{Fore.RESET} Builts various things{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}world:{Fore.RESET} Rebuilds the World database{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}plugins:{Fore.RESET} Plugin manager{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}list:{Fore.RESET} Lists all plugins{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}exec:{Fore.RESET} Executes a command from the plugin{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}enable:{Fore.RESET} Enables a Plugin{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}disable:{Fore.RESET} Disables a Plugin{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}marketplace/market:{Fore.RESET} Plugin Marketplace{Colors.RESET}")
    print(f"{Colors.BOLD}       -> {Fore.BLUE}list:{Fore.RESET} Lists available Plugins{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}get:{Fore.RESET} Installs a Plugin{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}config:{Fore.RESET} Configuration manager{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}language:{Fore.RESET} Configure the language of spkg{Colors.RESET}")
    print(f"\n{Colors.BOLD}Copyright (C) 2023 Juliandev02 - Made with <3")


# Help Function for English German
def help_de():
    print(f"{Colors.UNDERLINE + Colors.BOLD}Advanced Source Package Managment (spkg) {version} {platform.machine()}{Colors.RESET}{a_info_msg}")
    print(f"{Fore.CYAN + Colors.BOLD}Aufruf:{Fore.RESET} spkg {Fore.GREEN}[Befehl]{Fore.RED} <Argument>\n")
    print(f"spkg ist ein Paketmanager, der den Quellcode von den \noffiziellen Quellen herunterlädt, und diesen dann spezifisch für dein Gerät kompiliert.")
    print(f"Das Ziel von spkg ist, einfach und auch ohne viel Erfahrungen die neusten Versionen \nvon Programmen zu erhalten, auch unter Distrobutionen die nicht die neuste Version anbieten.")
    print(f"Durch das kompilieren des Paketes ist das Programm für dein Gerät optimiert und kann schneller laufen.")
    print(f"So bietet dir spkg eine hohe Sicherheit, sodass du dir keine Sorgen um Viren in Paketen machen musst.\n")
    print(f"{Colors.UNDERLINE + Colors.BOLD}Befehle:{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}install:{Fore.RESET} Installiert das angegebene Paket{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}reinstall:{Fore.RESET} Installiert das angegebene Paket neu{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}remove:{Fore.RESET} Entfernt das angegebene Paket neu{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}update:{Fore.RESET} Überprüft, ob ein Update für die installierten Pakete verfügbar ist{Colors.RESET} (Noch nicht verfügbar)")
    print(f"{Colors.BOLD} -> {Fore.BLUE}upgrade:{Fore.RESET} Aktualisiert alle verfügbaren Paketupdates{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}sync:{Fore.RESET} Synchronisiert die Paketdatenbank{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}info:{Fore.RESET} Gibt dir Informationen über ein bestimmtes Paket aus{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}list:{Fore.RESET} Zählt alle verfügbaren Pakete auf{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}download:{Fore.RESET} Lädt ein bestimmtes Paket herunter{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}build:{Fore.RESET} Erstellt verschiedene Dinge{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}world:{Fore.RESET} Baut die World Datenbank neu auf{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}plugins:{Fore.RESET} Plugin Verwaltung{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}list:{Fore.RESET} Zählt alle Plugins auf{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}exec:{Fore.RESET} Führt einen Befehl vom Plugin aus{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}enable:{Fore.RESET} Aktiviert ein Plugin{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}disable:{Fore.RESET} Deaktiviert ein Plugin{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}marketplace/market:{Fore.RESET} Plugin Marketplace{Colors.RESET}")
    print(f"{Colors.BOLD}       -> {Fore.BLUE}list:{Fore.RESET} Zählt verfügbare Plugins auf{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}get:{Fore.RESET} Installiert ein Plugin{Colors.RESET}")
    print(f"{Colors.BOLD} -> {Fore.BLUE}config:{Fore.RESET} Konfigurationsverwaltung{Colors.RESET}")
    print(f"{Colors.BOLD}    -> {Fore.BLUE}language:{Fore.RESET} Konfiguriere die Sprache von spkg{Colors.RESET}")
    print(f"\n{Colors.BOLD}Copyright (C) 2023 Juliandev02 - Made with <3")


# Try to connect to the locally saved main package database
try:
    db = Database(Files.package_database)

# If the Database doesn't exists/no entries, return a error
except OperationalError:
    print(StringLoader("PackageDatabaseNotSynced"))
    print("hier error")
    
# If the world database doesn't exists, return a error
if not os.path.exists(Files.world_database):
    print(StringLoader("WorldDatabaseNotBuilded"))
    exit()

# Try to connect to the world database
try:
    wdb = Database(Files.world_database)

# If the Database doesn't exists/no entries, return a error
except OperationalError:
    print(StringLoader("WorldDatabaseNotBuilded"))
    exit()


# Check if user config path exists
if not os.path.exists(NativeDirectories.user_config):
    print(StringLoader("UserConfigNotExists2"))
    os.mkdir(NativeDirectories.user_config)

# * --- Build Function --- *
if len(sys.argv) > 1 and sys.argv[1] == "build":
    # Check if second argument is world
    if len(sys.argv) > 2 and sys.argv[2] == "world":
        ays_input = input(StringLoader("AskRegenWorld") + Colors.BOLD + GREEN)
        match ays_input.lower():
            case "yes" | "ja":
                spinner = Halo(
                    text=f"{StringLoader('BuildingWorldDatabase')}",
                    spinner={'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                    text_color="white",
                    color="green")
                
                spinner.start()
                
                wdb.close()
                
                try:
                    Tools.regen_world()
                    spinner.stop()
                    
                except PermissionError:
                    spinner.stop() 
                    print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('BuildingWorldDatabase')}")
                    print(f"{Fore.CYAN + Colors.BOLD}{Files.world_database}: {Fore.RESET}{StringLoader('MissingPermissions')}")
                    print(StringLoader("MissingPermissionsWorldDatabase"))
                    exit()

                print(Colors.RESET + StringLoader("SuccessBuildingWorldDatabase"))
                exit()
            
            case _:
                print(Colors.RESET + StringLoader("Abort"))
                exit()
                
    else:
        print(StringLOader("NoArgument"))
        exit()


# * --- Package Info Function --- *
if len(sys.argv) > 1 and sys.argv[1] == "info":
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(StringLoader("NoArgument"))
        exit()
        
    c.execute("SELECT arch FROM packages where name = ?", (pkg_name,))
    
    try:
        result = c.fetchone()[0]
        
    except TypeError:
        print(StringLoader("PackageNotFound"))
        exit()
    
    if result == "all":
        try:
            arch = "all"
            c.execute("SELECT name FROM packages where name = ? AND arch = ? ", (pkg_name, arch))

        except OperationalError:
            print(StringLoader("PackageDatabaseNotSynced"))
            exit()
            
    else:
        try:
            c.execute("SELECT name FROM packages where name = ? AND arch = ? ", (pkg_name, arch))

        except OperationalError:
            print(StringLoader("PackageDatabaseNotSynced"))
            exit()
        
        c.execute("SELECT name FROM packages where name = ? AND arch = ?", (pkg_name, arch))
    
    if c.fetchall():
        c.execute("SELECT name, version, branch, arch, fetch_url, setup_script FROM packages where name = ? AND arch = ?", (pkg_name, arch))
        
        for row in c:
            print(
                f"{Colors.BOLD + Colors.UNDERLINE}{StringLoader('PackageInformationTitle', color_reset_end=False)} {row[0]} ({row[1]})\n{Colors.RESET}")
            print("Name:", row[0])
            print("Version:", row[1])
            print("Branch:", row[2])
            print(f"{StringLoader('Architecture')}:", row[3])
            print("Package URL:", row[4])
            print("PKGBUILD URL:", row[5])
            exit()

    else:
        print(StringLoader("PackageNotFound"))

    db.close()
    exit()


# * --- List Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "list":
    # List installed programms
    if len(sys.argv) > 2 and sys.argv[2] == "--installed":
        # Select * from the world database
        try:
            world_c.execute("SELECT * FROM world ORDER BY name GLOB '[A-Za-z]*' DESC, name")
            
            # Print the entries 
            for row in world_c:
                print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{RESET}/{row[3]}")
            exit()

        except OperationalError:
            print(WorldDatabaseNotBuilded)
        
    # Check if second argument is --arch; List programms that match the architecture from the third argument [all, arm64, amd64, ...]
    else:
        if len(sys.argv) > 2 and sys.argv[2] == "--arch":
            try:
                arch_a = sys.argv[3]
                c.execute("SELECT * FROM packages where arch = ? ORDER BY name GLOB '[A-Za-z]*' DESC, name", (arch_a, ))
                for row in c:
                    print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{Fore.RESET}/{row[3]}")
                exit()

            except OperationalError:
                print(PackageDatabaseNotSynced)
            
            except IndexError:
                print(NoArgument)
                
        # If not, print just all packages
        else:
            try:
                c.execute("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
                for row in c:
                    print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{Fore.RESET}/{row[3]}")
                exit()

            except OperationalError:
                print(PackageDatabaseNotSynced)
              
            # For debugging-purposes only  
            # c.execute("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
            # for row in c:
            #     print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{Fore.RESET}/{row[3]}")
            # exit()
        exit()
    exit()
            
            
# * --- Download Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "download":
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]
    
    else:
        print(NoArgument)
        exit()
        
    # Check if the passed package is all or --all
    if len(sys.argv) > 2 and sys.argv[2] == 'all' or  len(sys.argv) > 2 and sys.argv[2] == '--all':
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
        download_time_start = time.time()
        
        try:
            c.execute("SELECT name from packages")
        
        except OperationalError as e:
            print(PackageDatabaseNotSynced)
            exit()
            
        for row in c:
            pkg_name = row[0]
            download_compact_noarch(pkg_name)
        
        packages = pkg_name
        download_time_end = time.time()
        print(f"{FinishedDownloadingCompact} {Fore.LIGHTCYAN_EX + Colors.BOLD}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
        exit()
        
    if len(sys.argv) > 3:
        print(f"{Fore.GREEN + Colors.BOLD}[/] {Fore.RESET + Colors.RESET}{SearchingDatabaseForPackage}")
        download_time_start = time.time()
        
        for pkg_name in sys.argv[2:]:
            download_compact(pkg_name)
        
        
        packages = ', '.join(sys.argv[2:])
        download_time_end = time.time()
        print(f"{FinishedDownloading}{Fore.LIGHTCYAN_EX + Colors.BOLD}{packages}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
        exit()

    download(pkg_name)
    exit()


# * --- Sync Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "sync":
    start_time          = time.time()
    success_counter     = 0 
    unsuccess_counter   = 0 

    try:
        for name, url in config["repositories"].items():
            repo = url + "/package.db"
            database = Directories.mirror + name + ".db"
            
            spinner = Halo(
                text=f"{StringLoader('SyncingPackageDatabase', color_reset_end=False)} {CYAN}{url}{RESET} ({name})...{Colors.RESET}",
                spinner={'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                text_color="white",
                color="green")
            
            spinner.start()
            
            try:
                request = urllib.request.Request(
                    repo,
                    data = None,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                )
                
                repo_db = urllib.request.urlopen(request)
                
                with open(database, 'wb') as file:
                    file.write(repo_db.read())
                    
                database_size = os.path.getsize(database) / 1024
                    
                spinner.stop()
                print(f"{GREEN + Colors.BOLD}[✓]{RESET} {StringLoader('SyncingPackageDatabase', color_reset_end=False)} {CYAN}{url}{RESET} ({name}) ({database_size} kB){Colors.RESET}")
                success_counter += 1
                
            except PermissionError: 
                print(f"{Fore.CYAN + Colors.BOLD}{Directories.mirror}: {Fore.RESET}{StringLoader('MissingPermissons')}")
                print(StringLoader("MissingPermissonsPackageDatabaseUpdate"))
                exit()
            
            except URLError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SyncingPackageDatabase', color_reset_end=False)} {url} ({name})")
                print(StringLoader("HttpError"))
                unsuccess_counter += 1
                # exit()
                
    except AttributeError: 
        print(StringLoader("NoRepositories"))
        exit()
        
    required_time = round(time.time() - start_time, 2)
    
    if unsuccess_counter >= 1 and success_counter == 0: 
        print(f"{StringLoader('UnsuccessSyncingPackageDatabase')}{Colors.RESET}")
        exit()
        
    elif unsuccess_counter >= 1 and success_counter >= 1: 
        print(f"{StringLoader('AtLeastOneUnsuccessSyncingPackageDatabase')}{Colors.RESET}")
        print(f"{StringLoader('SuccessSyncingPackageDatabase', argument=required_time)}{Colors.RESET}")
        exit()
        
    else:
        print(f"{StringLoader('SuccessSyncingPackageDatabase', argument=required_time)}{Colors.RESET}")
        exit()



# * --- Install Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "install":
    # Check if a package was passed
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(NoArgument)
        exit()

    # Check if you have runned spkg with sudo
    if os.geteuid() == 0:
        None
    else:
        print(RecommendedRunningAsRoot)
    
    # Check if package is already installed
    try:
        world_c.execute("SELECT name from world where name = ?", (pkg_name,))

    except OperationalError as e:
        print(WorldDatabaseNotBuilded)
        exit()

    if world_c.fetchall():
        print(PackageAlreadyInstalled)
        exit()

    else:
        pass
        
        # Check if Package even exists
        try:
            c.execute("SELECT name, version, branch FROM packages where name = ?", (pkg_name,))
            for row in c:
                name = row[0]
                version = row[1]
                branch = row[2]

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()
        
        if len(sys.argv) > 2 and sys.argv[2] == "--sandbox" or sys.argv[2] == "--user":
            if len(sys.argv) > 3:
                pkg_name = sys.argv[3]
                
            Package.sandbox_install(pkg_name)
            
            if os.geteuid() == 0:
                None
                
            else:
                print(f"{Fore.CYAN + Colors.BOLD}{world_database}{Fore.RESET}{MissingPermissons}")
                print(MissingPermissonsWorldDatabaseInsert)
                exit()
                
            try:
                c.execute("SELECT name, version, branch FROM packages where name = ?", (pkg_name,))
                for row in c:
                    name = row[0]
                    version = row[1]
                    branch = row[2]

            except OperationalError:
                print(PackageDatabaseNotSynced)
                exit()
    
            world_c.execute("INSERT INTO world (name, version, branch) VALUES (?, ?, ?)", (name, version, branch))
            world_db.commit()
            world_db.close()
            exit()
            
        elif len(sys.argv) > 2 and sys.argv[2] == "--docker" :
            if len(sys.argv) > 3:
                pkg_name = sys.argv[3]
            print("Currently not working ...")
            exit()
            
        # Install the package
        Package.install(pkg_name)
        
        if os.geteuid() == 0:
                None
        else:
            print(f"{Fore.CYAN + Colors.BOLD}{world_database}{Fore.RESET}{MissingPermissons}")
            print(MissingPermissonsWorldDatabaseInsert)
            exit()
    
        world_c.execute("INSERT INTO world (name, version, branch) VALUES (?, ?, ?)", (name, version, branch))
        world_db.commit()
        world_db.close()
        
        exit()


# * --- Remove Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "remove":
    # Check if you have runned spkg with sudo
    if os.geteuid() == 0:
        None
    else:
        print(RecommendedRunningAsRootRemove)
        
    # Check if a package was passed
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(NoArgument)
        exit()
    
    spinner_world_search = Halo(text=f"{SearchingWorldForPackage}", spinner={
                             'interval': 150, 'frames': ['[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    spinner_world_search.start()
        
        
    # Check if package is already installed
    try:
        world_c.execute("SELECT name from world where name = ?", (pkg_name,))
        spinner_world_search.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[\] {Fore.RESET + Colors.RESET}{SearchingWorldForPackage}")

    except OperationalError as e:
        print(WorldDatabaseNotBuilded)
        exit()

    if not world_c.fetchall():
        print(PackageNotInstalledRemove)
        exit()
        
    else:
        pass
    
        # Check if Package even exists
        try:
            c.execute("SELECT name, version, branch FROM packages where name = ?", (pkg_name,))
            for row in c:
                name = row[0]
                version = row[1]
                branch = row[2]

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()
        
        if len(sys.argv) > 2 and sys.argv[2] == "--sandbox" or sys.argv[2] == "--user":
            if len(sys.argv) > 3:
                pkg_name = sys.argv[3]
            sandbox_remove(pkg_name)
            
            if os.geteuid() == 0:
                None
                
            else:
                print(f"{Fore.CYAN + Colors.BOLD}{world_database}{Fore.RESET}{MissingPermissons}")
                print(MissingPermissonsWorldDatabaseInsertRemove)
                exit()
                
            try:
                c.execute("SELECT name, version, branch FROM packages where name = ?", (pkg_name,))
                for row in c:
                    name = row[0]
                    version = row[1]
                    branch = row[2]

            except OperationalError:
                print(PackageDatabaseNotSynced)
                exit()
        
            world_c.execute("DELETE FROM world WHERE name = ? AND version = ? AND branch = ?", (name, version, branch))
            world_db.commit()
            
            exit()
            
        elif len(sys.argv) > 2 and sys.argv[2] == "--docker" :
            if len(sys.argv) > 3:
                pkg_name = sys.argv[3]
            print("Currently not working ...")
            exit()
            
        # Install the package
        remove(pkg_name)
        
        if os.geteuid() == 0:
                None
        else:
            print(f"{Fore.CYAN + Colors.BOLD}{world_database}{Fore.RESET}{MissingPermissons}")
            print(MissingPermissonsWorldDatabaseInsertRemove)
            exit()
    
        world_c.execute("DELETE FROM world WHERE name = ? AND version = ? AND branch = ?", (name, version, branch))
        world_db.commit()
        world_db.close()
        
        exit()


# * --- Reinstall Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "reinstall":
    # Check if you have runned spkg with sudo
    if os.geteuid() == 0:
        print(ReinstallNotAsRoot)
        time.sleep(3)
        
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(NoArgument)
        exit()
    
    try:
        world_c.execute("SELECT name from world where name = ?", (pkg_name,))
    
    except OperationalError as e:
        print(WorldDatabaseNotBuilded)
        exit()
    
    Package.install(pkg_name)
        
    try:
        c.execute("SELECT name, version FROM packages where name = ?", (pkg_name,))
        for row in c:
            name = row[0]
            version = row[1]

    except OperationalError:
        print(PackageDatabaseNotSynced)
        exit()
    
    exit()


# * --- Upgrade Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "upgrade":
    # Check if you have runned spkg with sudo
    if os.geteuid() == 0:
        print(UpgradeNotAsRoot)
        time.sleep(3)
    
    # Check if a package was passed
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]

    else:
        print(NoArgument)
        exit()
        
    # Check if the passed package is all or --all
    if len(sys.argv) > 2 and sys.argv[2] == 'all' or  len(sys.argv) > 2 and sys.argv[2] == '--all':
        try:
            world_c.execute("SELECT name from world")
        
        except OperationalError as e:
            print(WorldDatabaseNotBuilded)
            exit()
            
        for row in world_c:
            pkg_name = row[0]
            Package.upgrade(pkg_name)
        
        exit()
    
    try:
        world_c.execute("SELECT name from world where name = ?", (pkg_name,))
    
    except OperationalError as e:
        print(WorldDatabaseNotBuilded)
        exit()
    
    Package.upgrade(pkg_name)
        
    try:
        c.execute("SELECT name, version FROM packages where name = ?", (pkg_name,))
        for row in c:
            name = row[0]
            version = row[1]

    except OperationalError:
        print(PackageDatabaseNotSynced)
        exit()
    
    exit()


# * --- Update Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "update":
    # tableCompare = "SELECT name, version FROM world WHERE packages='table' order by name"
    
    # result1 = world_c.execute(tableCompare)
    # result2 = c.execute(tableCompare)
    
    # print("....Comparing Tables")
    # for row1 in result1:
    #     row2 = result2.fetchone()
    #     print(row1)
    #     print(row2)
    #     if row1 is not None and row2 is not None and (row1[0] == row2[0]):
    #         print("........Tables Match:"+ row1[0])
    #     else:
    #         if (row1 is not None and row1[0] is not None):
    #             print("!!!!!!!!PROBLEM "+world_database+" is missing Table:" + row1[0])	
    #         else:		
    #             print("!!!!!!!!PROBLEM "+db+" is missing Table:" + row2[0])	
    #         print("........Fix the problem and restart this comparator")
    #         exit()

    # print("....Done comparing table presence")


    
    # result1 = world_c.fetchall()
    # result2 = c.fetchall()
    
    # for row in result1:
    #     if row not in result2:
    #         print(row)

    #     for row in result2:
    #         if row not in result1:
    #             print(row)
    print("Currently not available")
    exit()


# Check ForceNoSandbox Integer Value (ONLY FOR DEBUGGING)
elif len(sys.argv) > 1 and sys.argv[1] == "force":
    if len(sys.argv) > 2:
        pkg_name = sys.argv[2]
        
    else:
        print("NoArgument")
        exit()
        
    c.execute("SELECT arch FROM packages where name = ?", (pkg_name,))
    
    try:
        result = c.fetchone()[0]
        
    except TypeError:
        print(PackageNotFound)
        exit()
    
    if result == "all":
        try:
            c.execute("SELECT ForceNoSandbox FROM packages where name = ?", (pkg_name,))
            for row in c:
                print(row[0])
                exit()

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()
        
    else:
        try:
            c.execute("SELECT ForceNoSandbox FROM packages where name = ? AND arch = ?", (pkg_name, arch))
            for row in c:
                print(row[0])
                exit()

        except OperationalError:
            print(PackageDatabaseNotSynced)
            exit()
    
    exit()
    
# * --- Plugin Managment --- *
elif len(sys.argv) > 1 and sys.argv[1] == "plugins" or len(sys.argv) > 1 and sys.argv[1] == "plugin":
    if len(sys.argv) > 2 and sys.argv[2] == "list":
        PluginManagement.list_plugins()


    # Plugin Command Execution
    elif len(sys.argv) > 4 and sys.argv[2] == "exec":
        plugin = sys.argv[3]

        if check_plugin_enabled_silent(plugin) == False: 
            print(PluginNotEnabled)
            exit()

        else: 
            PluginDaemon.import_plugin(plugin)
            PluginManagement.exec(sys.argv[4])
            
    
        # Plugin Marketplace
    elif len(sys.argv) > 2 and sys.argv[2] == "market":
        if len(sys.argv) > 3 and sys.argv[3] == "list":
            try:
                c.execute("SELECT * FROM plugins")
                for row in c:
                    print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[5]}{Fore.RESET}")
                exit()

            except OperationalError:
                print(PackageDatabaseNotSynced)
        else:
            PluginManagement.marketplace()
            exit()
            
            
    # Enable a plugin
    elif len(sys.argv) > 3 and sys.argv[2] == "enable":
        plugin = sys.argv[3]
        
        if os.geteuid() == 0:
            None
            
        else:
            print(f"{Fore.CYAN + Colors.BOLD}{enabled_plugins_config}{Fore.RESET}{MissingPermissons}")
            print(MissingPermissonsPluginConfig)
            exit()
        
        
        if check_plugin_enabled_silent(plugin) == True: 
            print(PluginIsAlreadyEnabled)
            exit()

        else: 
            with open(enabled_plugins_config, 'r') as f:
                data = json.load(f)
                
            data[plugin] = True
            
            with open(enabled_plugins_config, 'w') as f:
                json.dump(data, f)


    # Disable a plugin
    elif len(sys.argv) > 3 and sys.argv[2] == "disable":
        plugin = sys.argv[3]
        
        if os.geteuid() == 0:
            None
            
        else:
            print(f"{Fore.CYAN + Colors.BOLD}{enabled_plugins_config}{Fore.RESET}{MissingPermissons}")
            print(MissingPermissonsPluginConfig)
            exit()
        
        
        if check_plugin_enabled_silent(plugin) == False: 
            print(PluginIsAlreadyDisabled)
            exit()

        else: 
            with open(enabled_plugins_config, 'r') as f:
                data = json.load(f)
                
            data[plugin] = False
            
            with open(enabled_plugins_config, 'w') as f:
                json.dump(data, f)
                
        
    # Installs a plugin
    elif len(sys.argv) > 3 and sys.argv[2] == "get":
        plugin = sys.argv[3]
        
        if os.geteuid() == 0:
            None
            
        else:
            print(f"{Fore.CYAN + Colors.BOLD}/usr/share/spkg/plugins/{Fore.RESET}{MissingPermissons}")
            print(MissingPermissonsPluginInstallation)
            exit()
        
        PluginManagement.get(plugin)
            
    # Execution of a plugin-command without 'exec'
    elif len(sys.argv) > 3: 
        plugin = sys.argv[2]

        try: 
            if check_plugin_enabled_silent(plugin) == False: 
                print(PluginNotEnabled)
                exit()
                
        except KeyError:
            print(NoArgument)
            exit()

        else: 
            PluginDaemon.import_plugin(plugin)
            PluginManagement.exec(sys.argv[3])


    # If no Argument was passed, print an error
    else:
        print(NoArgument)
        exit()
        
    exit()
    
    
# * --- Config Function --- *
if len(sys.argv) > 1 and (sys.argv[1] == "config" or sys.argv[1] == "conf"):
    if len(sys.argv) > 3 and (sys.argv[2] == "language" or sys.argv[2] == "lang"):
        try:
            if os.geteuid() == 0:
                None
            else:
                print(f"{Fore.CYAN + Colors.BOLD}{spkg_config}{Fore.RESET}{MissingPermissons}")
                print(MissingPermissonsSpkgConfig)
                exit()
                
            lang = sys.argv[3]
            
            # if not lang == "de" or not lang == "en": 
            #     print(UnknownLanguage)
            #     exit()
            
            with open(spkg_config, "r") as f:
                data = json.load(f)

                data["language"] = lang
                
            with open(spkg_config, 'w') as f:
                json.dump(data, f)
                
            
            if lang == "de": 
                lang = "Deutsch (German)"
            if lang == "en": 
                lang = "English"
                
            print(ChangedLanguage % lang)
                
        except IndexError: 
            print(NoArgument)
        
    # If no Argument was passed, print an error
    else:
        print(NoArgument)
        exit()
        
        
# * --- Help Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "help":
    if language == "en":
        help_en()
    elif language == "de":
        help_de()


# * --- License Function --- *
elif len(sys.argv) > 1 and sys.argv[1] == "license":
    print("""
    Advanced Source Package Managment (spkg) Copyright (C) 2023  Juliandev02
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions
          """)


# Plugin Executor WITHOUT using spkg plugin <...>
elif len(sys.argv) > 2: 
    plugin = sys.argv[1]

    try: 
        if check_plugin_enabled_silent(plugin) == False: 
            print(PluginNotEnabled)
            exit()
            
    except KeyError:
        print(NoArgument)
        exit()

    else: 
        PluginDaemon.import_plugin(plugin)
        PluginManagement.exec(sys.argv[2])


elif len(sys.argv) > 1 and sys.argv[1] != "help":
    print(f"{UnknownOperation}{sys.argv[1]}")
    exit()


else:
    if language == "en_US":
        help_en()
    elif language == "de_DE":
        help_de()        

db.close()