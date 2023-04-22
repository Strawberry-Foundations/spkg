"""
Docker integration for spkg - Made by Juliandev02
"""

import json
from sqlite3 import *
from colorama import Fore
from sys import exit, argv
import os
import platform
import time
import subprocess

# Define Home Directory
home_dir = os.getenv("HOME")

# Use User Home even if spkg was executed with sudo
if os.environ.get('SUDO_USER'):
    home_dir = os.path.expanduser(f"~{os.environ['SUDO_USER']}")
else:
    home_dir = os.path.expanduser("~")

# Language Config
spkg_config = "/etc/spkg/config.json"
with open(spkg_config, "r") as f:
    spkg_cfg = json.load(f)

language = spkg_cfg['language']

if not language == "de" and not language == "en":
    exit()

# Basic Variables
bootstrap_location = f"{home_dir}/.local/spkg/sandbox/"
image = "ubuntu:latest"

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'


with open('/etc/os-release') as f:
    os_info = dict(line.strip().split('=') for line in f if '=' in line)

# Language Strings
if language == "de":
    Description = "Die Docker Integration für spkg installiert Pakete in einem Docker Container, abgesichert vom Hauptsystem."

elif language == "en":
    Description = "The Docker integration for spkg installs packages in a Docker container, secured from the main system."

# Spec Class for more Details about the Plugin
class Spec:
    Name = "Docker Containers"
    Desc = Description
    Version = "0.1.0"
    Commands = f"""
    -> setup
    -> config
    -> remove
    -> enter
    """

# PluginHandler Main Class
class PluginHandler:
    def setup():
        debug = False

        if len(argv) > 4 and argv[4] == "--debug" or len(argv) > 4 and argv[4] == "--verbose" or len(argv) > 4 and argv[4] == "-v" or len(argv) > 4 and argv[4] == "--v":
            debug = True
            print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Enabling Verbose Mode")


    def config():
        print("config")

    def remove():
        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Removing container ... This can take some time.")
        os.system(f'')
        exit()

    def enter():
        os.system(f'')
