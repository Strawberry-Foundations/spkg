"""
Sandbox System for spkg - Made by Juliandev02
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
        debug = False

        if len(argv) > 4 and argv[4] == "--debug" or len(argv) > 4 and argv[4] == "--verbose" or len(argv) > 4 and argv[4] == "-v" or len(argv) > 4 and argv[4] == "--v":
            debug = True
            print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Enabling Verbose Mode")

        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Detecting Operating System")
        print(f"{Fore.GREEN + BOLD}[!]{Fore.RESET + RESET} Detected Distrobution {os_info['NAME']}")
        print(f"{Fore.GREEN + BOLD}[!]{Fore.RESET + RESET} Detected Version {os_info['VERSION_ID']}")

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
            
        elif os_info['ID'] == "Ubuntu" and os_info['VERSION_ID'] == '"22.04"':
            dist = "jammy"

        elif os_info['ID'] == "Ubuntu" and os_info['VERSION_ID'] == '"20.04"':
            print(f"{Fore.YELLOW + BOLD}Warning:{Fore.RESET + RESET} Your version of ubuntu is outdated and the sandbox cannot continue to work with Ubuntu 22.04 Jammy Jellyfish")
            print(f"         Using Focal Fossa (Ubuntu 20.04) build script instead ...")
            dist = "focal"
            
        else:
            print(f"{Fore.YELLOW + BOLD}Warning:{Fore.RESET + RESET} Your Linux distrobution has not yet been tested by the spkg developers. It is possible that spkg-sandbox does not work. Please open a GitHub issue if something is not working. ")
            dist = "jammy"

        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Sandbox Setup will now start")

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
            repo = "http://archive.ubuntu.com/ubuntu"

        elif arch == "x86":
            arch = "i386"
            repo = "http://archive.ubuntu.com/ubuntu"

        elif arch == "aarch64":
            arch = "arm64"
            repo = "http://ports.ubuntu.com/ubuntu-ports"

        else:
            print(f"{Fore.RED + BOLD}Error:{Fore.RESET + RESET} spkg-sandbox cannot be executed on your system. Your architecture is currently not supported.")
            exit()

        if os.path.exists(bootstrap_location):
            print(f"{Fore.YELLOW + BOLD}Warning:{Fore.RESET + RESET} You have already a installation of spkg-sandbox. Reinstalling spkg-sandbox ...")
            os.system(f"sudo rm -rf {bootstrap_location}")

        start_time = time.time()


        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Bootstrapping your spkg-sandbox ... This could take some time depending on your drive speed and internet speed")
        print(f"{Fore.CYAN + BOLD}[i]{Fore.RESET + RESET} Installing to {bootstrap_location}")
        os.mkdir(bootstrap_location)

        if debug == True:
            os.system(f"sudo debootstrap --arch={arch} --variant=minbase --include=wget,ca-certificates,busybox-static {dist} {bootstrap_location} {repo}")

        else:
            subprocess.run(["sudo", "debootstrap", f"--arch={arch}", "--variant=minbase", "--include=wget,ca-certificates,busybox-static",
                           f"{dist}", f"{bootstrap_location}", f"{repo}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Updating your sandbox ...")
        if debug == True:
            os.system(f"sudo chroot {bootstrap_location} apt clean all")
            os.system(f"sudo chroot {bootstrap_location} apt autoclean")
            os.system(f"sudo chroot {bootstrap_location} apt update")

        else:
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "clean", "all"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "autpclean"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "update"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Modifying /etc/apt/sources.list ({bootstrap_location}) for the best program compability")
        os.system(f"sudo rm {bootstrap_location}/etc/apt/sources.list")

        if arch == "amd64" or arch == "i386":
            os.system(
                f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist} main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-backports main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-proposed main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-security main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-updates main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")

        elif arch == "arm64":
            os.system(
                f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist} main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-backports main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-proposed main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-security main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
            os.system(
                f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-updates main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'")
        
        else:
            print(f"{Fore.RED + BOLD}Error:{Fore.RESET + RESET} That shouldn't happend. Please open an issue on GitHub.")
            exit()


        print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Installing some base packages ... ")
        if debug == True:
            os.system(f"sudo chroot {bootstrap_location} apt update")
            os.system(f"sudo chroot {bootstrap_location} apt install -y python3 python3-dev python3-pip")
            
            print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Upgrading your sandbox ... ")
            os.system(f"sudo chroot {bootstrap_location} apt upgrade -y")
            os.system(f"sudo chroot {bootstrap_location} apt clean all")
            
            print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Cleaning your sandbox ... ")
            os.system(f"sudo chroot {bootstrap_location} apt autoclean")
            os.system(f"sudo chroot {bootstrap_location} apt autoremove -y")
            
        else:
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "update"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "install", "-y", "python3", "python3-dev", "python3-pip"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Upgrading your sandbox ... ")
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "upgrade", "-y"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "clean", "all"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print(f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Upgrading your sandbox ... ")
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "autoclean"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["sudo", "chroot", f"{bootstrap_location}", "apt", "autoremove"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        end_time = time.time()

        print(
            f"{Fore.GREEN + BOLD}[!]{Fore.RESET + RESET} Finished sandbox setup in {round(end_time - start_time, 2)} s")

    def config():
        print("config")

    def remove():
        print(
            f"{Fore.YELLOW + BOLD}[!]{Fore.RESET + RESET} Removing sandbox ... This can take some time.")
        os.system(f"sudo rm -rf {bootstrap_location}")
        exit()

    def enter():
        os.system(f'sudo chroot {bootstrap_location}')
