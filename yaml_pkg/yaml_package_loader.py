import yaml
from yaml import SafeLoader

with open("./package.yml") as file:
    package = yaml.load(file, Loader=SafeLoader)
    
print(f'''
      Name: {package["Name"]}
      Version: {package["Version"]}
      Architecture: {package["Architecture"]}
      Dependencies: {package["Dependencies"]}
      ''')