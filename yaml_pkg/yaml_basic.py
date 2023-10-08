import yaml
from yaml import SafeLoader

import subprocess
import os

with open("./test.yml") as file:
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

os.system(package["Install"]["Commands"])