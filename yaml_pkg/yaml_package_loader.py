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
    try:
        if print_output:
            subprocess.run(["sudo", "apt", "update"], check=True) 
            subprocess.run(["sudo", "apt", "install", package], check=True)
        else:
            subprocess.run(["sudo", "apt", "update"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
            subprocess.run(["sudo", "apt", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

def apk_install(package, print_output=False):
    try:
        if print_output:
            subprocess.run(["sudo", "apk", "add", package], check=True)
        else:
            subprocess.run(["sudo", "apk", "add", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

def dnf_install(package, print_output=False):
    try:
        if print_output:
            subprocess.run(["sudo", "dnf", "install", package], check=True)
        else:
            subprocess.run(["sudo", "dnf", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

def pip_install(package, print_output=False):
    try:
        if print_output:
            subprocess.run(["pip", "install", package], check=True)
        else:
            subprocess.run(["pip", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

        try:
            if print_output:
                subprocess.run(["pip", "install", package, "--break-system-packages"], check=True)
            else:
                subprocess.run(["pip", "install", package, "--break-system-packages"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
        except subprocess.CalledProcessError as e:
            print(f"Error while installing {package}: {e}")
            pip_install(package)


with open("./package.yml") as file:
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

class Commands:
    Install        = package["Install"]["Commands"]
    Remove         = package["Remove"]["Commands"]
    Upgrade        = package["Upgrade"]["Commands"]

package_manager = get_package_manager()

match package_manager:
    case PackageManagers.Apt:
        apt_install(SpecDeps["Apt"], print_output=True)