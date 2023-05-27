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
        
