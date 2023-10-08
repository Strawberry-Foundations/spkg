import subprocess
from init import PackageManagers

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

# Apt (Deb-based) install function
def apt_install(package, print_output=False, update=False):
    command = ["apt", "install", "-y"] + package
    command_update = ["apt", "update"]
    
    try:
        if print_output:
            if update:
                subprocess.run(command_update, check=True) 
            subprocess.run(command, check=True)
        else:
            if update:
                subprocess.run(command_update, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

# Apk (alpine-based) install function
def apk_install(package, print_output=False):
    command = ["apk", "add"] + package
    
    try:
        if print_output:
            subprocess.run(command, check=True)
        else:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

# Dnf (Fedora-based) install function
def dnf_install(package, print_output=False):
    command = ["dnf", "install", "-y"] + package
    
    try:
        if print_output:
            subprocess.run(command, check=True)
        else:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

def pip_install(package, print_output=False):
    command = ["pip", "install"] + package
    command_break_system_packages = ["pip", "install"] + package + ["--break-system-packages"]
    
    try:
        if print_output:
            subprocess.run(command_break_system_packages, check=True)
        else:
            subprocess.run(command_break_system_packages, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")