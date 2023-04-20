"""
Sandbox System for spkg - Made by Juliandev02
"""

import json
from sqlite3 import *
from colorama import Fore
from halo import Halo
from sys import exit
import os
import platform

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
dist = "jammy"

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'


with open('/etc/os-release') as f:
    os_info = dict(line.strip().split('=') for line in f if '=' in line)

# Language Strings
if language == "de":
    Description = "spkg-sandbox installiert Pakete in einer isolierten Umgebung."

elif language == "en":
    Description = "spkg-sandbox installs packages in a isolated environment."

# Spec Class for more Details about the Plugin
class Spec:
    Name = "spkg-sandbox"
    Desc = Description
    Version = "0.2.1"
    Commands = f"""
    -> setup
    -> config
    -> remove
    -> enter
    """

# PluginHandler Main Class
class PluginHandler:
    def setup():
        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Detecting Operating System")
        print(f"{Fore.GREEN + BOLD}[!]{Fore.RESET + RESET} Detected {os_info['NAME']}")
        
        if not os.path.exists("/usr/sbin/debootstrap"):
            print(f"{Fore.RED + BOLD}Error:{Fore.RESET + RESET} spkg-sandbox cannot be executed on your system. Missing dependency 'debootstrap'")
            exit()
        
        if os_info['ID'] == "debian" and os_info['VERSION_ID'] == '"10"':
            print(f"{Fore.YELLOW + BOLD}Warning:{Fore.RESET + RESET} Your version of debootstrap is outdated and doesn't support to build Ubuntu 22.04 Jammy Jellyfish.")
            print(f"         Using Focal Fossa (Ubuntu 20.04) build script instead ...")
            dist = "focal"
            
        elif os_info['ID'] == "debian" and os_info['VERSION_ID'] == '"11"':
            print(f"{Fore.YELLOW + BOLD}Warning:{Fore.RESET + RESET} Your version of debootstrap is outdated and doesn't support to build Ubuntu 22.04 Jammy Jellyfish.")
            print(f"         Using Focal Fossa (Ubuntu 20.04) build script instead ...")
            dist = "focal"
        
        elif os_info['ID'] == "ubuntu" and os_info['VERSION_ID'] == '"20.04"':
            print(f"{Fore.YELLOW + BOLD}Warning:{Fore.RESET + RESET} Your version of ubuntu is outdated and the sandbox cannot continue to work with Ubuntu 22.04 Jammy Jellyfish")
            print(f"         Using Focal Fossa (Ubuntu 20.04) build script instead ...")
            dist = "focal"
        
        else:
            print(f"{Fore.YELLOW + BOLD}Warning:{Fore.RESET + RESET} Your Linux distrobution has not yet been tested by the spkg developers. It is possible that spkg-sandbox does not work. Please open a GitHub issue if something is not working. ")
            
        print(f"{Fore.YELLOW+ BOLD}[!]{Fore.RESET + RESET} Sandbox Setup will now start")
        
        try: 
            ans = input("Do you want to continue? [Y/N]? ")
            
        except KeyboardInterrupt: 
            print("\nAborting ...")
            exit()
        
        if ans != "y" and ans != "Y" and ans != "j" and ans != "J": 
            print("Aborting ...")
            exit()
            
        print(f"{Fore.YELLOW+ BOLD}[!]{Fore.RESET + RESET} Checking system architecture")
        arch = platform.machine()
        
        if arch == "x86_64":
            arch = "amd64"
            repo = "http://archive.ubuntu.com/ubuntu"
            
        elif arch == "x86":
            arch = "i386"
            repo = "http://archive.ubuntu.com/ubuntu"
            
        elif arch == "aarch64":
            arch = "arm64"
            repo="http://ports.ubuntu.com/ubuntu-ports"
        
        else:
            print(f"{Fore.RED + BOLD}Error:{Fore.RESET + RESET} spkg-sandbox cannot be executed on your system. Your architecture is currently not supported.")
            exit()
            
        if os.path.exists(bootstrap_location):
            os.system(f"sudo rm -rf {bootstrap_location}")
            
            
        
    def config():
        print("config")
        
    def remove():
        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET}Removing sandbox ... This can take some time.")
        os.system(f"sudo rm -rf {bootstrap_location}")
        exit()
        
    def enter():
        os.system(f'sudo chroot {bootstrap_location}')