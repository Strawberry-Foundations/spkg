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

"""
Repository Manager for spkg - Made by Juliandev02
"""

import json
from sqlite3 import *
from colorama import Fore
from sys import exit, argv
import os
import platform
import time
import subprocess

# Language Config
spkg_config = "/etc/spkg/config.json"
with open(spkg_config, "r") as f:
    spkg_cfg = json.load(f)

language = spkg_cfg['language']

if not language == "de" and not language == "en":
    print(f"{Fore.RED}You have either a corrupted or unconfigured config file! Please check the language settings!")

# Basic Variables
spkg_repositories = "/etc/spkg/repositories.json"
repomgr_list = "/etc/spkg/available_repositories.json"

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'


# Language Strings
if language == "de":
    Description = "Das Repo Manager Plugin für spkg ermöglicht es dir einfach Repositories zu verwalten, auszuwählen, hinzuzufügen und anderes!"
    MissingPermissonsPluginConfig = f"{Fore.RED + BOLD}Die Repository-Konfiguration konnte nicht bearbeitet werden. (Wird spkg als Root ausgeführt?){RESET}"
    MissingPermissons = f"{Fore.RESET + RESET}: Fehlende Berechtigung"
    WarningRegeneratingConfig = f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Warnung! Dies löscht deine Aktuelle Repositorie-Liste! Möchtest du wirklich fortfahren? [J/N] "
    RegeneratingConfig = f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Die Repositorie-Konfiguration wird neu generiert ..."
    Abort = "Abbruch ... "
    Canceled = f"{Fore.RED + BOLD}[!!!]{Fore.RESET} Prozess wurde abgebrochen!{RESET}"

elif language == "en":
    Description = "The Repo Manager plugin for spkg allows you to easily manage, select, add repositories and more!"
    MissingPermissonsPluginConfig = f"{Fore.RED + BOLD}The repository configuration could not be edited. (Is spkg running as root?){RESET}"
    MissingPermissons = f"{Fore.RESET + RESET}Missing Permissons"
    RegeneratingConfig = f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} The repository configuration is regenerated ..."
    WarningRegeneratingConfig = f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Warning! This will delete your current Repository list! Do you really want to continue? [Y/N] "
    Abort = "Aborting ... "
    Canceled = f"{Fore.RED + BOLD}[!!!]{Fore.RESET} Process canceled!{RESET}"


# Spec Class for more Details about the Plugin
class Spec:
    Name = "Repository Manager"
    Desc = Description
    Version = "1.0.0"
    Commands = f"""
    -> list
    -> reconfigure
    -> add
    -> delete
    """

# PluginHandler Main Class
class PluginHandler:
    def list():
        with open(repomgr_list, "r") as f:
            data = json.load(f)
        
        for key, value in data.items():
            print(f"{Fore.GREEN + BOLD}{key}:{Fore.CYAN} {value}")
        exit()
        
        
    def current():
        with open(spkg_repositories, "r") as f:
            data = json.load(f)
        
        for key, value in data.items():
            print(f"{Fore.GREEN + BOLD}{key} -->{Fore.CYAN} {value}")
        exit()
        
        
    def active():
        PluginHandler.current()


    def reconfigure():
        if not os.geteuid() == 0:
                print(f"{Fore.CYAN + BOLD}{repomgr_list}{Fore.RESET}{MissingPermissons}")
                print(MissingPermissonsPluginConfig)
                exit()
        else:
            pass
        
        try:
            continue_pkg_installation = input(WarningRegeneratingConfig)

        except KeyboardInterrupt as e:
            print(f"\n{Canceled}")
            exit()

        if continue_pkg_installation.lower() == "j":
            pass

        elif continue_pkg_installation.lower() == "y":
            pass

        else:
            print(Abort)
            exit()
            
        print(RegeneratingConfig)
        os.system(f"rm -f {repomgr_list}")
        os.system(f"touch {repomgr_list}")
        os.system("sh -c 'echo {} >> " + repomgr_list + "'")
        with open(repomgr_list, "r") as f:
            data = json.load(f)
        
        data["main"] = f"https://sources.juliandev02.ga/packages"
        
        with open(repomgr_list, 'w') as f:
            json.dump(data, f)