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
    print(f"{Fore.RED}You have either a corrupted or unconfigured config file! Please check the language settings!")

# Basic Variables
bootstrap_location = f"{home_dir}/.local/spkg/sandbox/"
image = "juliandev02/spkg-debian:bookworm"

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
        # debug = False

        # if len(argv) > 4 and argv[4] == "--debug" or len(argv) > 4 and argv[4] == "--verbose" or len(argv) > 4 and argv[4] == "-v" or len(argv) > 4 and argv[4] == "--v":
        #     debug = True
        #     print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Enabling Verbose Mode")
        
        if not os.path.exists("/usr/bin/docker"):
            print(f"{Fore.RED + BOLD}Error:{Fore.RESET + RESET} spkg-docker cannot be executed on your system. Please install docker and try again  ")
            exit()
        
        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Container Setup will now start")

        try:
            ans = input("Do you want to continue? [Y/N]? ")

        except KeyboardInterrupt:
            print("\nAborting ...")
            exit()
            
        
        if ans != "y" and ans != "Y" and ans != "j" and ans != "J":
            print("Aborting ...")
            exit()
            
        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Checking system architecture")
        arch = platform.machine()

        if arch == "x86_64":
            arch = "amd64"

        # elif arch == "x86":
        #     arch = "i386"

        # elif arch == "aarch64":
        #     arch = "arm64"

        else:
            print(f"{Fore.RED + BOLD}Error:{Fore.RESET + RESET} spkg-docker cannot be executed on your system. Your architecture is currently not supported.")
            exit()
        
        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Pulling Docker Image... This could take some time depending on your internet speed")
        os.system(f"docker pull {image}")
        
            
         
            
    def config():
        print("config")

    def remove():
        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Removing container ... This can take some time.")
        os.system(f'')
        exit()

    def enter():
        os.system(f'')
