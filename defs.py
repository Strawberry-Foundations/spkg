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
version = "1.5.0"

# Database Variables
world_database = "/etc/spkg/world.db"
package_database = "/etc/spkg/package.db"

# Url's
world_database_url = "https://sources.juliandev02.ga/packages/world_base.db"

# Config File Variables
spkg_repositories = "/etc/spkg/repositories.json"
enabled_plugins_cfg = "/etc/spkg/enabled_plugins.json"
spkg_config = "/etc/spkg/config.json"

# Environ Variables
home_dir = os.getenv("HOME")
arch = platform.machine()

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
with open(enabled_plugins_cfg, "r") as f:
    global enabled_plugins_cfg_data
    enabled_plugins_cfg_data = json.load(f)