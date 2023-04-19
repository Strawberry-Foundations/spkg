import os
import sys
import time
import json
import sqlite3 as sql
import urllib.request
import platform

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore, Back, Style
from halo import Halo
from sys import exit
import requests
import subprocess
from api import * 

# Language Config
spkg_config = "/etc/spkg/config.json"
with open(spkg_config, "r") as f:
    spkg_cfg = json.load(f)

language = spkg_cfg['language']

if not language == "de" and not language == "en":
    exit()

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
    """

# PluginHandler Main Class
class PluginHandler:
    def setup():
        print("")
        
