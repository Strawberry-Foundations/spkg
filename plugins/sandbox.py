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
from init import *
from halo import Halo

# Language Strings
match lang:
    case "de_DE":
        Description = "spkg-sandbox installiert Pakete in einer isolierten Umgebung."
    case "en_US":
        Description = "spkg-sandbox installs packages in a isolated environment."

# Spec Class for more Details about the Plugin
class Spec:
    Name = "spkg-sandbox"
    Desc = Description
    Version = "2.0.0"
    Commands = f"""
    -> setup
    -> reconfigure
    -> remove
    -> delete (alias of remove)
    -> enter
    """
    

# Get user name
if os.environ.get('SUDO_USER'):
    user_name = os.environ['SUDO_USER']
    
else:
    user_name = os.environ['USER']

# Check if user config path exists
if not os.path.exists(Directories.user_config):
    os.mkdir(Directories.user_config)
    user_config = {
        "sandbox": {
            "bootstrap_location": f"{home_dir}/.local/share/spkg/sandbox/",
            "handler": "bwrap"
        }
    }
    
    with open(Files.user_config, 'w') as file:
        yaml.dump(user_config, file)
    
# Check if config file exists
if not os.path.exists(Files.user_config):
    print(f"{Fore.YELLOW + Colors.BOLD}Warning:{Fore.RESET + RESET} Your user configuration doesn't exist.")

# Basic Variables
try:
    bootstrap_location = user_config['sandbox']['bootstrap_location']
    dist = "jammy"
    sandbox_handler = user_config['sandbox']['handler']
    
except TypeError or FileNotFoundError: 
    pass


# PluginHandler Main Class
class Commands:
    def setup():
        debug = False
        
        # Sandbox Handler checking, first if sandbox handler is chroot
        if sandbox_handler == "chroot":
            sandbox_enter_cmd = f"sudo chroot {bootstrap_location}"
        
        # If sandbox handler is bwrap
        elif sandbox_handler == "bwrap":
            sandbox_enter_cmd = f"sudo bwrap --bind {bootstrap_location} / --dev /dev --bind /sys /sys --bind /proc /proc --bind /tmp /tmp"

        # If the value is not valid, print error
        else:
            print(f"{Fore.RED + Colors.BOLD}E:{Colors.RESET} Unknown sandbox handler '{sandbox_handler}'. Check your config")

        # check if sandbox setup is executed in debug mode
        # if len(argv) > 4 and argv[4] == "--debug" or len(argv) > 4 and argv[4] == "--verbose" or len(argv) > 4 and argv[4] == "-v" or len(argv) > 4 and argv[4] == "--v":
        if "--debug" in argv or "--verbose" in argv:
            debug = True
            print(f"{Fore.YELLOW + Colors.BOLD} ! {Fore.RESET + RESET} Enabling Verbose Mode")

        # Check Operating System
        spinner = Halo(text=f"Detecting Operating System",
                            spinner={'interval': 500, 'frames': ['.  ', '.. ', '...', ' ..', '  .', '   ']},
                            text_color="white",
                            color="green")
                
        spinner.start()
        
        # Open the /etc/os-release file
        with open('/etc/os-release') as f:
            os_info = dict(line.strip().split('=') for line in f if '=' in line)
            
        os_distro = os_info['NAME']
        os_version = os_info['VERSION_ID']
        
        spinner.stop()
        print(f"{Fore.GREEN + Colors.BOLD} ✓ {Fore.RESET + RESET} Detected Distrobution {os_distro}")
        print(f"{Fore.GREEN + Colors.BOLD} ✓ {Fore.RESET + RESET} Detected Version {os_version}")

        # check dependency debootstrap
        if not os.path.exists("/usr/sbin/debootstrap"):
            print(f"{Fore.RED + Colors.BOLD}Error:{Fore.RESET + RESET} spkg-sandbox cannot be executed on your system. Missing dependency 'debootstrap'")
            exit()
        
        # check dependency bubblewrap
        if sandbox_handler == "bwrap" and not os.path.exists("/usr/bin/bwrap"):
            print(f"{Fore.RED + Colors.BOLD}Error:{Fore.RESET + RESET} spkg-sandbox cannot be executed on your system. Missing dependency 'bwrap' (bubblewrap)")
            exit()

        os_string = os_info['ID'] + " " + os_info['VERSION_ID'].replace('"', "")
        
        match os_string:
            case "debian 10":
                print(f"{Fore.YELLOW + Colors.BOLD}W:{Fore.RESET + RESET} Your version of debootstrap is outdated and doesn't support to build Ubuntu 22.04 Jammy Jellyfish.")
                print(f"   Using Focal Fossa (Ubuntu 20.04) build script instead ...")
                dist = "focal"
                
            case "debian 11":
                print(f"{Fore.YELLOW + Colors.BOLD}W:{Fore.RESET + RESET} Your version of debootstrap is outdated and doesn't support to build Ubuntu 22.04 Jammy Jellyfish.")
                print(f"   Using Focal Fossa (Ubuntu 20.04) build script instead ...")
                dist = "focal"
            
            case "debian 12":
                print(f"{Fore.GREEN + Colors.BOLD} ✓ {Fore.RESET + RESET} Your operating system is fully supported")
                dist = "jammy"

            case "Ubuntu 22.04":
                print(f"{Fore.GREEN + Colors.BOLD} ✓ {Fore.RESET + RESET} Your operating system is fully supported")
                dist = "jammy"
                
            case "Ubuntu 20.04":
                print(f"{Fore.YELLOW + Colors.BOLD}W:{Fore.RESET + RESET} Your version of Ubuntu is outdated and the sandbox cannot continue to work with Ubuntu 22.04 Jammy Jellyfish")
                print(f"   Using Focal Fossa (Ubuntu 20.04) build script instead ...")
                dist = "focal"

            case _:
                print(f"{Fore.YELLOW + Colors.BOLD}W:{Fore.RESET + RESET} Your Linux distrobution has not yet been tested by the spkg developers. It is possible that spkg-sandbox does not work. Please open a GitHub issue if something is not working.")
                dist = "jammy"
        
        # Ask to continue the setup
        try:
            ans = input(f"{Fore.YELLOW + Colors.BOLD} ! {Fore.RESET + RESET} Sandbox Setup will now start. {Colors.RESET}Do you want to continue? [Y/N] {GREEN}")

        except KeyboardInterrupt:
            print(RESET + "\nAborting ...")
            exit()

        if ans != "y" and ans != "Y" and ans != "j" and ans != "J":
            print(RESET + "Aborting ...")
            exit()

        # Check system architecture
        spinner = Halo(text=f"Checking system architecture",
                            spinner={'interval': 500, 'frames': ['.  ', '.. ', '...', ' ..', '  .', '   ']},
                            text_color="white",
                            color="green")
                
        spinner.start()
        arch = platform.machine()

        match arch:
            case "x86_64":
                arch = "amd64"
                repo = "http://archive.ubuntu.com/ubuntu"

            case "x86":
                arch = "i386"
                repo = "http://archive.ubuntu.com/ubuntu"

            case "aarch64":
                arch = "arm64"
                repo = "http://ports.ubuntu.com/ubuntu-ports"
            
            case _:
                spinner.stop()
                print(f"{RED + Colors.BOLD} × {RESET} Checking system architecture")
                print(f"{Fore.RED + Colors.BOLD} E:{Fore.RESET + RESET} spkg-sandbox cannot be executed on your system. Your architecture is currently not supported. ({arch})")
                exit()
                
        spinner.stop()
        print(f"{GREEN + Colors.BOLD} ✓ {RESET} Checking system architecture ({arch})")
        
        # check if user-local spkg directory exists
        if not os.path.exists(f"{home_dir}/.local/spkg"):
            os.mkdir(f"{home_dir}/.local/spkg")

        # if the sandbox is already existend, ask to reinstall
        if os.path.exists(bootstrap_location):
            try:
                cont_sandbox_setup = input(f"{Fore.YELLOW + Colors.BOLD} ! {Fore.RESET + RESET} You have already a installation of spkg-sandbox. {Colors.RESET}Do you want to continue? [Y/N] {GREEN}")

            # If you press ^C, it prints out a error message
            except KeyboardInterrupt as e:
                print(f"\n{Fore.RED + Colors.BOLD} × {Fore.RESET} Process canceled!{RESET}")
                exit()

            # Check if you want to continue the sandbox setup
            if cont_sandbox_setup.lower() in ["j", "y"]:
                os.system(f"sudo rm -rf {bootstrap_location}")
            
            # If you press any other key, it prints out an error message
            else:
                print(RESET + "Aborting ...")
                exit()
            
        start_time = time.time()
        
        # try to create the sandbox location
        try:
            os.mkdir(bootstrap_location)
            print(f"{GREEN + Colors.BOLD} ✓ {RESET} Creating bootstrap directory ({bootstrap_location})")
            
        except:
            print(f"{RED + Colors.BOLD} × {RESET} Creating bootstrap directory ({bootstrap_location})")
            print(f"{Fore.RED + Colors.BOLD} E:{Fore.RESET + RESET} Couldn't create {bootstrap_location} (Maybe try to run spkg as root)")
            exit()

        # bootstrap
        try:        
            # boostrap the sandbox
            if debug == True:
                print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Bootstrapping your sandbox... {Colors.ITALIC}This could take some time depending on your drive and internet speed{Colors.RESET}")
                print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Installing to {bootstrap_location}")
                
                subprocess.run(["sudo", "debootstrap", f"--arch={arch}", "--variant=minbase", "--include=wget,ca-certificates,busybox-static",
                            f"{dist}", f"{bootstrap_location}", f"{repo}"])

                print(f"{GREEN + Colors.BOLD} ✓ {RESET} Bootstrapping was successfully")

            else:
                print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Installing to {bootstrap_location}")
                
                spinner = Halo(text=f"Bootstrapping your sandbox... {Colors.ITALIC}This could take some time depending on your drive and internet speed{Colors.RESET}",
                            spinner={'interval': 500, 'frames': ['.  ', '.. ', '...', ' ..', '  .', '   ']},
                            text_color="white",
                            color="green")
                
                spinner.start()
                
                subprocess.run(["sudo", "debootstrap", f"--arch={arch}", "--variant=minbase", "--include=wget,ca-certificates,busybox-static",
                            f"{dist}", f"{bootstrap_location}", f"{repo}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                spinner.stop()
                print(f"{GREEN + Colors.BOLD} ✓ {RESET} Bootstrapping was successfully")
            
        except Exception as e:
            print(f"{RED + Colors.BOLD} × {RESET} Bootstrapping your sandbox...")
            print(f"{Fore.RED + Colors.BOLD} E:{Fore.RESET + RESET} Couldn't bootstrap your sandbox: {e}")
            

        # Update the sandbox
        
        
        clean_cmd = sandbox_enter_cmd.split() + ["apt", "clean", "all"] 
        autoclean_cmd = sandbox_enter_cmd.split() + ["apt", "autoclean"]
        autoremove_cmd = sandbox_enter_cmd.split() + ["apt", "autoremove", "-y"]
        
        update_cmd = sandbox_enter_cmd.split() + ["apt", "update"]
        upgrade_cmd = sandbox_enter_cmd.split() + ["apt", "autoclean"]
        
        base_pkg_cmd = sandbox_enter_cmd.split() + ["apt", "install", "-y", "python3", "python3-dev", "python3-pip"] 
        
        
        if debug == True:
            print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Updating your sandbox ...")
            
            subprocess.run(clean_cmd, check=True)
            subprocess.run(autoclean_cmd, check=True)
            subprocess.run(update_cmd, check=True)

        else:
            spinner = Halo(text=f"Updating your sandbox ...",
                            spinner={'interval': 500, 'frames': ['.  ', '.. ', '...', ' ..', '  .', '   ']},
                            text_color="white",
                            color="green")
                
            spinner.start()
            
            subprocess.run(clean_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(autoclean_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(update_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Modify sandbox for the best program compability
        print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Modifying /etc/apt/sources.list for the best program compability")
        os.system(f"sudo rm {bootstrap_location}/etc/apt/sources.list")
        try:
            if arch == "amd64" or arch == "i386":
                commands = [
                    f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist} main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-backports main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-proposed main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-security main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://archive.ubuntu.com/ubuntu {dist}-updates main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'"
                ]

                # Befehle ausführen
                for cmd in commands:
                    subprocess.run(cmd, shell=True)

            elif arch == "arm64":
                commands = [
                    f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist} main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-backports main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-proposed main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-security main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'",
                    f"sudo sh -c 'echo deb http://ports.ubuntu.com/ubuntu-ports {dist}-updates main restricted universe multiverse >> {bootstrap_location}/etc/apt/sources.list'"
                ]

                # Befehle ausführen
                for cmd in commands:
                    subprocess.run(cmd, shell=True)
            
            else:
                print(f"{Fore.RED + Colors.BOLD} E:{Colors.RESET} That shouldn't happend. Please open an issue on GitHub.")
                exit()
                
        except Exception as e:
            print(f"{RED + Colors.BOLD} × {RESET} Modifying /etc/apt/sources.list for the best program compability")
            print(f"{Fore.RED + Colors.BOLD} E:{Fore.RESET + RESET} Couldn't modify sources.list: {e}")
            
        try:
            # install some base packages that are required 
            if debug == True:
                print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Installing some base packages ... ")
                subprocess.run(update_cmd, check=True)
                subprocess.run(base_pkg_cmd, check=True)
                
                print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Upgrading your sandbox ... ")
                subprocess.run(upgrade_cmd, check=True)
                subprocess.run(clean_cmd, check=True)
                
                print(f"{Fore.CYAN + Colors.BOLD} ! {Fore.RESET + RESET} Cleaning your sandbox ... ")
                subprocess.run(autoclean_cmd, check=True)
                subprocess.run(autoremove_cmd, check=True)
                
            else:
                spinner = Halo(text=f"Installing some base packages ... ",
                                spinner={'interval': 500, 'frames': ['.  ', '.. ', '...', ' ..', '  .', '   ']},
                                text_color="white",
                                color="green")
                    
                spinner.start()
                subprocess.run(update_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(base_pkg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                spinner.stop()
                print(f"{GREEN + Colors.BOLD} ✓ {RESET} Base packages has been installed")

                spinner = Halo(text=f"Upgrading your sandbox ... ",
                                spinner={'interval': 500, 'frames': ['.  ', '.. ', '...', ' ..', '  .', '   ']},
                                text_color="white",
                                color="green")
                    
                spinner.start()
                subprocess.run(upgrade_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(clean_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                spinner.stop()
                print(f"{GREEN + Colors.BOLD} ✓ {RESET} Sandbox has been upgraded")

                spinner = Halo(text=f"Cleaning your sandbox ...",
                                spinner={'interval': 500, 'frames': ['.  ', '.. ', '...', ' ..', '  .', '   ']},
                                text_color="white",
                                color="green")
                    
                spinner.start()
                subprocess.run(autoclean_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(autoremove_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                spinner.stop()
                print(f"{GREEN + Colors.BOLD} ✓ {RESET} Sandbox has been cleaned")
                
        except Exception as e:
            print(f"{RED + Colors.BOLD} × {RESET} Installing some base packages, Upgrading your sandbox, Cleaning your sandbox")
            print(f"{Fore.RED + Colors.BOLD} E:{Fore.RESET + RESET} Couldn't either install base packages, upgrade sandbox or clean sandbox: {e}")
            
        end_time = time.time()

        print(f"{GREEN + Colors.BOLD} ✓ {RESET} Finished sandbox setup in {round(end_time - start_time, 2)} s")


    def reconfigure():
        # Check if you're want to reconfigure as root
        if os.geteuid() == 0:
                print(f"{Fore.YELLOW + Colors.BOLD}That shouldn't happen. Don't generate your config as root!{Fore.RESET + RESET}")
        else:
            pass
        
        # Regenerate spkg sandbox config
        print(f"{Fore.YELLOW + Colors.BOLD}>>>{Fore.RESET + RESET} Regenerating config ...")
        os.system(f"rm -rf {home_dir}/.config/spkg")
        os.mkdir(f"{home_dir}/.config/spkg")
        user_sandbox_config = f"{home_dir}/.config/spkg/sandbox.json"
        os.system(f"touch {user_sandbox_config}")
        os.system("sh -c 'echo {} >> " + user_sandbox_config + "'")
        with open(user_sandbox_config, "r") as f:
            data = json.load(f)
        
        data["bootstrap_location"] = f"{home_dir}/.local/spkg/sandbox/"
        data["sandbox_handler"] = "chroot"
        
        # dump new config
        with open(user_sandbox_config, 'w') as f:
            json.dump(data, f)
    
    # Remove spkg sandbox
    def remove():
        try:
            cont_sandbox_remove = input(f"{Fore.BLUE + Colors.BOLD}Info:{Fore.RESET + RESET} This will completly remove the spkg-sandbox. Note that this does not remove the packages from the world database.\nDo you want to continue? [Y/N] ")

        # If you press ^C, it prints out a error message
        except KeyboardInterrupt as e:
            print(f"\n{Fore.RED + Colors.BOLD}[!!!]{Fore.RESET} Process canceled!{RESET}")
            exit()

        # Check if you want to continue the sandbox setup
        if cont_sandbox_remove.lower() == "j":
            print(f"{Fore.YELLOW + Colors.BOLD}>>>{Fore.RESET + RESET} Removing sandbox ... This can take some time.")
            os.system(f"sudo rm -rf {bootstrap_location}")
            exit()

        elif cont_sandbox_remove.lower() == "y":
            print(f"{Fore.YELLOW + Colors.BOLD}>>>{Fore.RESET + RESET} Removing sandbox ... This can take some time.")
            os.system(f"sudo rm -rf {bootstrap_location}")
            exit()
        
        # If you press any other key, it prints out an error message
        else:
            print("Aborting ...")
            exit()
        
    
    # alias for remove
    def delete():
        PluginHandler.delete()

    # Enter the sandbox depending on the configured sandbox handler
    def enter():
        if not os.path.exists(bootstrap_location):
            print(f"{Fore.RED + Colors.BOLD}Error:{Fore.RESET + RESET} Your sandbox has not been set up yet. Please set up the sandbox before you can enter the sandbox!")
            exit()
            
        if sandbox_handler == "chroot":
            sandbox_enter_cmd = f"sudo chroot {bootstrap_location}"
        
        elif sandbox_handler == "bwrap":
            sandbox_enter_cmd = f"sudo bwrap --bind {bootstrap_location} / --dev /dev --bind /sys /sys --bind /proc /proc --bind /tmp /tmp /bin/bash"
        
        else:
            print(f"{Fore.RED + Colors.BOLD}Error:{Fore.RESET + RESET} Unknown Config for sandbox_handler. Check your config")
        
        os.system(f'{sandbox_enter_cmd}')