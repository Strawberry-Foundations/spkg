import json
from colorama import Fore
from sys import exit

# Language Config
spkg_config = "/etc/spkg/config.json"
with open(spkg_config, "r") as f:
    spkg_cfg = json.load(f)

language = spkg_cfg['language']

if not language == "de" and not language == "en":
    exit()

# Language Strings
if language == "de":
    Description = "Was? Was ist das!"

elif language == "en":
    Description = "What? What is this!"

# Spec Class for more Details about the Plugin
class Spec:
    Name = "Test Plugin"
    Desc = Description
    Version = "1.0"
    Commands = f"""
    -> setup
    -> hello
    """

# PluginHandler Main Class
class PluginHandler:
    def setup():
        print("This is a test plugin for spkg.")
    
    def hello():
        print("Hello World!")
        
