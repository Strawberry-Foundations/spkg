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

def apt_install(package):
    try:
        subprocess.run(["sudo", "apt", "update"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
        subprocess.run(["sudo", "apt", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

def apk_install(package):
    try:
        subprocess.run(["sudo", "apk", "add", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

def dnf_install(package):
    try:
        subprocess.run(["sudo", "dnf", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

def pip_install(package):
    try:
        subprocess.run(["pip", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print(f"Error while installing {package}: {e}")

        try:
            subprocess.run(["pip", "install", package, "--break-system-packages"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"Error while installing {package}: {e}")
            pip_install(package)