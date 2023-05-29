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
import sys
import time
import json
import sqlite3 as sql
import urllib.request
import platform
import subprocess

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore
from halo import Halo
from sys import exit

# Base Variables
version = "1.6.0-rc5"
date = "20230529"
release_type = "rc"
alpha = False
hbp = False
dev_local = False

if release_type in ["rc", "beta", "alpha"]:
    version = version + f" ({date})"
    
else: 
    version = version

# Environ Variables
home_dir = os.getenv("HOME")
arch = platform.machine()

# environ SUDO_USER is set, get the home from the executed user
if os.environ.get('SUDO_USER'):
    home_dir = os.path.expanduser(f"~{os.environ['SUDO_USER']}")
else:
    home_dir = os.path.expanduser("~")

# Database Variables and Config File Variabless
if dev_local == False:
    spkg_data_dir = "/etc/spkg/"
    mirror_dir = "/var/lib/spkg/mirrors/"
    
    world_database = "/var/lib/spkg/world.db"
    package_database = "/var/lib/spkg/mirrors/main.db"
    
    spkg_repositories = "/etc/spkg/repositories.json"
    enabled_plugins_config = "/etc/spkg/enabled_plugins.json"
    spkg_config = "/etc/spkg/config.json"
    user_sandbox_config = f"{home_dir}/.config/spkg/sandbox.json"
    
else:
    spkg_data_dir = "./data/etc/spkg/"
    mirror_dir = "./data/var/lib/spkg/mirrors/"
    
    world_database = "./data/var/lib/spkg/world.db"
    package_database = "./data/var/lib/spkg/mirrors/main.db"
    
    spkg_repositories = "./data/etc/spkg/repositories.json"
    enabled_plugins_config = "./data/etc/spkg/enabled_plugins.json"
    spkg_config = "./data/etc/spkg/config.json"
    user_sandbox_config = f"{home_dir}/.config/spkg/sandbox.json"

# Url's
world_database_url = "https://sources.juliandev02.ga/archive/world_base.db"


# Color Variables
class Colors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Open spkg config file
with open(spkg_config, "r") as f:
    global spkg_cfg_data
    spkg_cfg_data = json.load(f)
    
# Open plugin config file
with open(enabled_plugins_config, "r") as f:
    global enabled_plugins_cfg_data
    enabled_plugins_cfg_data = json.load(f)

# Open user sandbox config file    
with open(user_sandbox_config, "r") as f:
    global user_sandbox_cfg_data
    user_sandbox_cfg_data = json.load(f)

# Open spkg repo config file
with open(spkg_repositories, "r") as f:
    global spkg_repo_data
    spkg_repo_data = json.load(f)

# Check if alpha or hbp is enabled
if alpha == True and hbp == True:
    a_info_msg = f"\n{Fore.YELLOW + Colors.BOLD}WARNING:{Fore.RESET + Colors.RESET} This is an Alpha Release and this program is in a highly development state!\n"
    
elif alpha == True:
    a_info_msg = f"\n{Fore.YELLOW + Colors.BOLD}WARNING:{Fore.RESET + Colors.RESET} This is an Alpha Release!\n"
    
elif hbp == True:
    a_info_msg = f"\n{Fore.YELLOW + Colors.BOLD}WARNING:{Fore.RESET + Colors.RESET} This program is in a highly development state!\n"
    
else:
    a_info_msg = "\n"
    
# Language-specific Variables
local_lang = spkg_cfg_data['language']
    
if not local_lang == "de" and not local_lang == "en":
    print(f"{Fore.RED}You have either a corrupted or unconfigured config file! Please check the language settings!")

if local_lang == "de":
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Die Paketdatenbank wurde noch nicht synchronisiert. Führe {Fore.CYAN}spkg sync{Fore.RESET} aus, um die Datenbank zu synchronisieren{Colors.RESET}"
    HttpError = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Ein HTTP-Fehler ist aufgetreten. Die angeforderte Datei konnte nicht angefordert werden. (Ist der Repository-Server offline?){Colors.RESET}"

elif local_lang == "en":
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The package database has not been synchronized yet. Run {Fore.CYAN}spkg sync{Fore.RESET} to synchronize the database{Colors.RESET}"
    HttpError = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} An HTTP error has occurred. The requested file could not be requested. (Is the repository server offline?){Colors.RESET}"

if dev_local == False:
    # Connect to the Package Database
    try:
        db = sql.connect(package_database)
        c = db.cursor()

    except OperationalError:
        print(PackageDatabaseNotSynced)
        exit()
else:
    try:
        db = sql.connect(package_database)
        c = db.cursor()

    except OperationalError:
        print(PackageDatabaseNotSynced)
        exit()