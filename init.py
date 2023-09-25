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
import sqlite3 as sql
import platform

from sqlite3 import *
from colorama import Fore
from sys import exit
import yaml
from yaml import SafeLoader
from src.colors import *

# Base Variables
version         = "2.0a1+u1"
date            = "20230925"
release_type    = "alpha"
alpha           = True
dev_local       = True
langs           = ["de_DE", "en_US"]

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


if dev_local == False:
    class Directories:
        spkg_config         = "/etc/spkg/"
        user_config         = f"{home_dir}/.config/spkg/"
        data                = "/var/lib/spkg/"
        mirror              = data + "mirrors/"
        
else:
    class Directories:
        spkg_config         = "./data/etc/spkg/"
        user_config         = f"./data/userconfig/spkg/"
        data                = "./data/var/lib/spkg/"
        mirror              = data + "mirrors/"
        
class Files:        
    world_database      = Directories.data + "world.db"
    package_database    = Directories.mirror + "main.db"
    
    spkg_config         = Directories.spkg_config + "config.yml"
    user_sandbox_config = Directories.user_config + "sandbox.yml"
    lang_strings        = Directories.spkg_config + "lang.yml"

# Color Variables
class Colors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Open Configuration
with open(Files.spkg_config) as file:
    config = yaml.load(file, Loader=SafeLoader)
    
# Open user sandbox config file    
with open(Files.user_sandbox_config, "r") as file:
    user_sandbox_config = yaml.load(file, Loader=SafeLoader)
    
# Open language strings
with open(Files.lang_strings, encoding="utf-8") as lang_strings:
    Str = yaml.load(lang_strings, Loader=SafeLoader)

if alpha == True:
    a_info_msg = f"\n{YELLOW + Colors.BOLD}WARNING:{RESET + Colors.RESET} This is an Alpha Release!\n"
else:
    a_info_msg = "\n"
    
# Variables
lang            = config["language"]
world_db_url    = config["main_url"] + "archive/world_base.db"


# check if language is available
if lang not in langs:
    print(f"{RED + Colors.BOLD}Error loading language: Selected language is not available.{RESET}")
    print(f"{YELLOW + Colors.BOLD}Falling back to en_US\n{RESET}")
    time.sleep(1)
    lang = "en_US"
    

def StringLoader(string, argument=""):
    string = Str[lang][string]
    string = string.replace("#red", RED)
    string = string \
            .replace("#red", RED) \
            .replace("#green", GREEN) \
            .replace("#yellow", YELLOW) \
            .replace("#blue", BLUE) \
            .replace("#magenta", MAGENTA) \
            .replace("#cyan", CYAN) \
            .replace("#white", WHITE) \
            .replace("#reset", RESET) \
            .replace("#bold", Colors.BOLD) \
            .replace("#underline", Colors.UNDERLINE) \
            .replace("%s", argument)
    return string

try:
    db = sql.connect(Files.package_database)
    c = db.cursor()

except OperationalError:
    print(f"{RED + Colors.BOLD}[!]{RESET}{Str[lang]['PackageDatabaseNotSynced']}{RESET}")
    exit()  