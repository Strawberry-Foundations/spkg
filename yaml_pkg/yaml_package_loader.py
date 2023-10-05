import yaml
from yaml import SafeLoader

import subprocess

class PackageManagers:
    Apt = "apt"
    Apk = "apk"
    Dnf = "dnf"

def get_package_manager():
    try:
        output = subprocess.check_output(["which", "apt"]).decode("utf-8")
        if "apt" in output:
            return PackageManagers.Apt
    except subprocess.CalledProcessError:
        pass
    
    try:
        output = subprocess.check_output(["which", "apk"]).decode("utf-8")
        if "apk" in output:
            return PackageManagers.Apk
    except subprocess.CalledProcessError:
        pass
    
    try:
        output = subprocess.check_output(["which", "dnf"]).decode("utf-8")
        if "dnf" in output:
            return PackageManagers.Dnf
    except subprocess.CalledProcessError:
        pass
    
    return False

def apt_install(package, print_output=False):
    command = ["sudo", "apt", "install"] + package
    try:
        if print_output:
            # subprocess.run(["sudo", "apt", "update"], check=True) 
            subprocess.run(command, check=True)
        else:
            subprocess.run(["sudo", "apt", "update"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
            subprocess.run(["sudo", "apt", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print()
        print(f"Error while installing {package}: {e}")


with open("./spkg.yml") as file:
    package = yaml.load(file, Loader=SafeLoader)
    
print(f'''
      Name: {package["Name"]}
      Version: {package["Version"]}
      Architecture: {package["Architecture"]}
      Dependencies: {package["Dependencies"]}
      ''')

SpecName        = package["Name"]
SpecVersion     = package["Version"]
SpecArch        = package["Architecture"]
SpecDeps        = package["Dependencies"]
SpecFlags       = package["Flags"]

AptDeps         = SpecDeps["Apt"].split(" ")
print(AptDeps)

class Commands:
    Install        = package["Install"]["Commands"]
    Remove         = package["Remove"]["Commands"]
    Upgrade        = package["Upgrade"]["Commands"]

package_manager = get_package_manager()

match package_manager:
    case PackageManagers.Apt:
        apt_install(AptDeps, print_output=True)