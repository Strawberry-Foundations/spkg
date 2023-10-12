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
from sys import exit, argv

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

argv_len = len(sys.argv)

# Try to connect to the locally saved main package database
try:
    db = sql.connect(Files.package_database)
    c  = db.cursor()

# If the Database doesn't exists/no entries, return a error
except OperationalError:
    print(StringLoader("PackageDatabaseNotSynced"))
    

# Try to connect to the world database
try:
    wdb = sql.connect(Files.world_database)
    wc  = wdb.cursor()

# If the Database doesn't exists/no entries, return a error
except OperationalError:
    print(StringLoader("WorldDatabaseNotBuilded"))


# Check if user config path exists
if not os.path.exists(NativeDirectories.user_config):
    print(StringLoader("UserConfigNotExists2"))
    os.mkdir(NativeDirectories.user_config)


# * --- Build Function --- *
if argv_len > 1 and argv[1] == "build":
    # case switch
    match argv_len > 2 and argv[2]:
        case "world":
            pass
            # Ask if you really want to rebuilt the world database
            ays_input = input(StringLoader("AskRegenWorld") + Colors.BOLD + GREEN)
            
            # Case Statement for input
            match ays_input.lower():
                # If yes, rebuilt the world database
                case "yes" | "ja":
                    spinner = Halo(
                        text=f"{StringLoader('BuildingWorldDatabase')}",
                        spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                        text_color="white",
                        color="green")
                    
                    spinner.start()
                    
                    wdb.close()
                    
                    try:
                        Tools.regen_world()
                        spinner.stop()
                    
                    # Error handling for permission errors 
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
                    
        case _:
            if argv_len >= 3:
                print(StringLoader("UnknownOperation"), argv[2])
            else:
                print(StringLoader("NoArgument"))
            exit()


# * --- Package Info Function --- *
elif argv_len > 1 and argv[1] == "info":
    if not argv_len > 2:
        print(StringLoader("NoArgument"))
        exit()  
        
    package_name = argv[2]
        
    c.execute("SELECT arch FROM packages where name = ?", (package_name,))
    
    try:
        result = c.fetchone()[0]
        
    except TypeError:
        print(StringLoader("PackageNotFound"))
        exit()
    
    if result == "all":
        try:
            arch = "all"
            c.execute("SELECT name FROM packages where name = ? AND arch = ? ", (package_name, arch))

        except OperationalError:
            print(StringLoader("PackageDatabaseNotSynced"))
            exit()
            
    else:
        try:
            c.execute("SELECT name FROM packages where name = ? AND arch = ? ", (package_name, arch))

        except OperationalError:
            print(StringLoader("PackageDatabaseNotSynced"))
            exit()
        
        c.execute("SELECT name FROM packages where name = ? AND arch = ?", (package_name, arch))
    
    if c.fetchall():
        c.execute("SELECT name, version, branch, arch, url, specfile FROM packages where name = ? AND arch = ?", (package_name, arch))
        
        for row in c:
            print(f"{Colors.BOLD + Colors.UNDERLINE}{StringLoader('PackageInformationTitle', color_reset_end=False)} {row[0]} ({row[1]}){Colors.RESET}")
            print(f"{StringLoader('Name')}:", row[0])
            print(f"{StringLoader('Version')}:", row[1])
            print(f"{StringLoader('Branch')}:", row[2])
            print(f"{StringLoader('Architecture')}:", row[3])
            print(f"{StringLoader('PackageUrl')}:", row[4])
            print(f"{StringLoader('PkgbuildUrl')}:", row[5])
            exit()

    else:
        print(StringLoader("PackageNotFound"))

    exit()


# * --- List Function --- *
elif argv_len > 1 and argv[1] == "list":
    # case switch
    match argv_len > 2 and argv[2]:
        # if argument is --installed
        case "--installed":
            # Select * from the world database
            try:
                wc.execute("SELECT * FROM world ORDER BY name GLOB '[A-Za-z]*' DESC, name")
                
                # Print the entries 
                for row in wc:
                    print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{RESET}/{row[3]}")
                    
                exit()

            except OperationalError:
                print(StringLoader("WorldDatabaseNotBuilded"))
        
        # if argument is --arch
        case "--arch":
            try:
                arch_a = argv[3]
                c.execute("SELECT * FROM packages where arch = ? ORDER BY name GLOB '[A-Za-z]*' DESC, name", (arch_a, ))
                
                for row in c:
                    print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{Fore.RESET}/{row[3]}")
                    
                exit()

            except OperationalError:
                print(StringLoader("PackageDatabaseNotSynced"))
            
            except IndexError:
                print(StringLoader("NoArgument"))
                exit()
                
        # If not, print just all packages
        case _:
            try:
                c.execute("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
                
                for row in c:
                    print(f"{Fore.GREEN + Colors.BOLD}{row[0]} {Fore.RESET + Colors.RESET}({row[1]}) @ {Fore.CYAN}{row[2]}{Fore.RESET}/{row[3]}")
                    
                exit()

            except OperationalError:
                print(StringLoader("PackageDatabaseNotSynced"))
                
            
            
# * --- Download Function --- *
elif argv_len > 1 and argv[1] == "download":
    if not argv_len > 2:
        print(StringLoader("NoArgument"))
        exit()
        
    package_name = argv[2]
        
    # Check if the passed package is all or --all
    if package_name in ["all", "--all"]:
        spinner = Halo(text=f"{StringLoader('SearchingDatabaseForPackage')}",
                       spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                       text_color="white",
                       color="green")
        
        spinner.start()
        time.sleep(.1)
        
        download_time_start = time.time()
        
        spinner.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingDatabaseForPackage')}")
        
        try:
            c.execute("SELECT name from packages")
        
        except OperationalError as e:
            print(PackageDatabaseNotSynced)
            exit()
            
        for row in c:
            packages = row[0]
            package = DownloadManager.Downloader(packages)
            package.compact_download(noarch=True)
        
        download_time_end = time.time()
        print(DownloadManager.Downloader.get_package_download_list())
        DownloadManager.Downloader.success_unsuccess_counter()
        print(f"{StringLoader('FinishedDownloadingCompact')} {Fore.LIGHTCYAN_EX + Colors.BOLD}{Colors.RESET}in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
        exit()
        
    elif argv_len > 3:
        spinner = Halo(text=f"{StringLoader('SearchingDatabaseForPackage')}",
                       spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                       text_color="white",
                       color="green")
        
        spinner.start()
        time.sleep(.1)
        
        download_time_start = time.time()
        
        spinner.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingDatabaseForPackage')}")
        
        for package_name in argv[2:]:
            package = DownloadManager.Downloader(package_name)
            package.compact_download()
        
        
        packages = ', '.join(sys.argv[2:])
        download_time_end = time.time()
        
        print(f"{StringLoader('FinishedDownloading')} {Fore.CYAN + Colors.BOLD}{packages} {Colors.RESET}in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
        exit()
        
    else:
        package = DownloadManager.Downloader(package_name)
        package.download()
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
                spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                text_color="white",
                color="green")
            
            spinner.start()
            
            try:
                request = urllib.request.Request(
                    repo,
                    data = None,
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
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
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SyncingPackageDatabase', color_reset_end=False)} {CYAN}{url}{RESET} ({name})")
                print(f"{RED + Colors.BOLD} ↳ {RESET} {StringLoader('HttpError')}")
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
        print(f"{StringLoader('SuccessSyncingPackageDatabase', argument_1=required_time)}{Colors.RESET}")
        exit()
        
    else:
        print(f"{StringLoader('SuccessSyncingPackageDatabase', argument_1=required_time)}{Colors.RESET}")
        exit()



# * --- Install Function --- *
elif argv_len > 1 and argv[1] == "install":
    if not argv_len > 2:
        print(StringLoader("NoArgument"))
        exit()
    
    package_name = argv[2]
    
    # Fetch world database and check if package is already installed
    try:
        wc.execute("SELECT name from world where name = ?", (package_name,))

    except OperationalError as e:
        print(StringLoader("WorldDatabaseNotBuilded"))
        exit()

    if wc.fetchall():
        print(StringLoader("PackageAlreadyInstalled"))
        exit()
        
    if argv_len > 2 and "--sandbox" in argv or "-s" in argv:
        package_name = " ".join(argv[1:])
        package_name = package_name.replace("--sandbox", "").replace("-s", "").replace("install", "").replace(" ", "")
        
        if package_name == "":
            print(StringLoader("NoArgument"))
            exit()
        
        # Fetch world database and check if package is already installed
        try:
            wc.execute("SELECT name from world where name = ?", (package_name,))

        except OperationalError as e:
            print(StringLoader("WorldDatabaseNotBuilded"))
            exit()

        if wc.fetchall():
            print(StringLoader("PackageAlreadyInstalled"))
            exit()
        
        package = InstallManager.Installer(package_name)
        package.install_sandbox(args=argv)
        package.insert_world()
        exit()
    
    elif argv_len > 2 and "--docker" in argv:
        package_name = " ".join(argv[1:])
        package_name = package_name.replace("--docker", "").replace("install", "").replace(" ", "")
        
        if package_name == "":
            print(StringLoader("NoArgument"))
            exit()
        
        # Fetch world database and check if package is already installed
        try:
            wc.execute("SELECT name from world where name = ?", (package_name,))

        except OperationalError as e:
            print(StringLoader("WorldDatabaseNotBuilded"))
            exit()

        if wc.fetchall():
            print(StringLoader("PackageAlreadyInstalled"))
            exit()
        
        package = InstallManager.Installer(package_name)
        package.install_sandbox(args=argv)
        package.insert_world()
        exit()
        
    else:
        package = InstallManager.Installer(package_name)
        package.install(args=argv)
        package.insert_world()
        exit()



# * --- Remove Function --- *
elif argv_len > 1 and argv[1] == "remove":
    if not argv_len > 2:
        print(StringLoader("NoArgument"))
        exit()
    
    package_name = argv[2]
    
    spinner = Halo(text=f"{StringLoader('SearchingWorldForPackage')}",
                   spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                   text_color="white",
                   color="green")
    
    spinner.start()
    
    # Fetch world database and check if package is already installed
    try:
        wc.execute("SELECT name from world where name = ?", (package_name,))

    except OperationalError as e:
        print(StringLoader("WorldDatabaseNotBuilded"))
        exit()

    if not wc.fetchall():
        spinner.stop()
        print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingWorldForPackage')}")
        print(StringLoader("PackageNotInstalledRemove"))
        exit()
        
    if argv_len > 2 and "--sandbox" in argv or "-s" in argv:
        package_name = " ".join(argv[1:])
        package_name = package_name.replace("--sandbox", "").replace("-s", "").replace("install", "").replace(" ", "")
        
        if package_name == "":
            print(StringLoader("NoArgument"))
            exit()
        
        # Fetch world database and check if package is already installed
        try:
            wc.execute("SELECT name from world where name = ?", (package_name,))

        except OperationalError as e:
            print(StringLoader("WorldDatabaseNotBuilded"))
            exit()

        if not wc.fetchall():
            spinner.stop()
            print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingWorldForPackage')}")
            print(StringLoader("PackageNotInstalledRemove"))
            exit()
        
        spinner.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingWorldForPackage')}")
        
        package = RemoveManager.Remove(package_name)
        package.remove(args="argv")
        package.remove_world()
        exit()
    
    elif argv_len > 2 and "--docker" in argv:
        package_name = " ".join(argv[1:])
        package_name = package_name.replace("--docker", "").replace("install", "").replace(" ", "")
        
        if package_name == "":
            print(StringLoader("NoArgument"))
            exit()
        
        # Fetch world database and check if package is already installed
        try:
            wc.execute("SELECT name from world where name = ?", (package_name,))

        except OperationalError as e:
            print(StringLoader("WorldDatabaseNotBuilded"))
            exit()

        if not wc.fetchall():
            spinner.stop()
            print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingWorldForPackage')}")
            print(StringLoader("PackageNotInstalledRemove"))
            exit()
        
        spinner.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingWorldForPackage')}")
        
        package = RemoveManager.Remove(package_name)
        package.remove(args="argv")
        package.remove_world()
        exit()
        
    else:        
        spinner.stop()
        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingWorldForPackage')}")
        
        package = RemoveManager.Remove(package_name)
        package.remove(args="")
        package.remove_world()
        exit()


# * --- Reinstall Function --- *
elif argv_len > 1 and argv[1] == "reinstall":
    if not argv_len > 2:
        print(StringLoader("NoArgument"))
        exit()
    
    package_name = argv[2]
    
    # Fetch world database and check if package is already installed
    try:
        wc.execute("SELECT name from world where name = ?", (package_name,))

    except OperationalError as e:
        print(StringLoader("WorldDatabaseNotBuilded"))
        exit()
        
    if argv_len > 2 and "--sandbox" in argv or "-s" in argv:
        package_name = " ".join(argv[1:])
        package_name = package_name.replace("--sandbox", "").replace("-s", "").replace("install", "").replace(" ", "")
        
        if package_name == "":
            print(StringLoader("NoArgument"))
            exit()
        
        # Fetch world database and check if package is already installed
        try:
            wc.execute("SELECT name from world where name = ?", (package_name,))

        except OperationalError as e:
            print(StringLoader("WorldDatabaseNotBuilded"))
            exit()
        
        package = InstallManager.Installer(package_name)
        package.install_sandbox(args=argv)
        package.remove_world()
        package.insert_world()
        exit()
    
    elif argv_len > 2 and "--docker" in argv:
        package_name = " ".join(argv[1:])
        package_name = package_name.replace("--docker", "").replace("install", "").replace(" ", "")
        
        if package_name == "":
            print(StringLoader("NoArgument"))
            exit()
        
        # Fetch world database and check if package is already installed
        try:
            wc.execute("SELECT name from world where name = ?", (package_name,))

        except OperationalError as e:
            print(StringLoader("WorldDatabaseNotBuilded"))
            exit()
        
        package = InstallManager.Installer(package_name)
        package.install_sandbox(args=argv)
        package.remove_world()
        package.insert_world()
        exit()
        
    else:
        package = InstallManager.Installer(package_name)
        package.install(args=argv)
        package.remove_world()
        package.insert_world()
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
    # if language == "en_US":
    #     help_en()
    # elif language == "de_DE":
    #     help_de()        
    print(StringLoader("Help", argument_1=a_info_msg))

db.close()