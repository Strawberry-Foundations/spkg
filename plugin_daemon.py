#!/usr/bin/env python3

import os
import sys
import time
import json
import sqlite3 as sql
import urllib.request
import platform
import requests
import subprocess

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore, Back, Style
from halo import Halo
from sys import exit
import importlib



class Colors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

enabled_plugins_cfg = "./data/etc/spkg/enabled_plugins.json"
with open(enabled_plugins_cfg, "r") as f:
    data = json.load(f)

spkg_config = "/etc/spkg/config.json"
with open(spkg_config, "r") as f:
    spkg_cfg = json.load(f)

language = spkg_cfg['language']

if not language == "de" and not language == "en":
    exit()

if language == "de":
    PluginManagement = "Plugin Verwaltung"
    InstalledPlugins = "Installierte Plugins"
    Enabled = "\033[32mAktiviert\033[0m"
    Disabled = "\033[31mDeaktiviert\033[0m"
    ErrorPlugin = "\033[38;5;52m\033[1mFehler\033[0m"
    Condition = "Zustand"
    Description = "Beschreibung"
    Version = "Version"
    Commands = "Befehle"
    ErrorOccured = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Ein Fehler ist aufgetreten. Überprüfe deine Eingabe. Wenn dies nicht weiterhilft, öffne ein Issue auf GitHub{Colors.RESET}"
    ErrCode = "Fehlercode"

elif language == "en":
    PluginManagement = "Plugin Management"
    InstalledPlugins = "Installed Plugins"
    Enabled = "\033[32mActivated\033[0m"
    Disabled = "\033[31mDeactivated\033[0m"
    ErrorPlugin = "\033[38;5;52m\033[1mError\033[0m"
    Condition = "Condition"
    Description = "Description"
    Version = "Version"
    Commands = "Commands"
    ErrorOccured = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} An error has occurred. Check your input. If this does not help, open an issue on GitHub{Colors.RESET}"
    ErrCode = "Errorcode"


class plugin_daemon:
    def import_plugin(plugin_name):
        check_plugin_enabled_silent(plugin_name)
        global module
        module_name = "plugins." + plugin_name
        module = importlib.import_module(module_name)
        return module

    def setup():
        module.PluginHandler.setup()


def check_plugin_enabled_silent(plugin):
    plugin_data = data[plugin]
    if plugin_data == True:
        pass
    else:
        pass


def check_plugin_enabled_ret(plugin):
    plugin_data = data[plugin]
    if plugin_data == True:
        return Enabled
    else:
        return Disabled


class plugin_management:
    def list_plugins():
        print(f"{Colors.BOLD + Colors.UNDERLINE}{PluginManagement} -> {InstalledPlugins}\n")
        
        for entry in data:
            plugin_daemon.import_plugin(entry)
            
            print(f"{Fore.GREEN + Colors.BOLD + Colors.UNDERLINE}{module.Spec.Name} ({entry}){Fore.RESET + Colors.RESET}")
            print(f"{Fore.CYAN + Colors.BOLD}{Description}:{Fore.RESET + Colors.RESET} {module.Spec.Desc}")
            print(f"{Fore.CYAN + Colors.BOLD}{Condition}:{Fore.RESET + Colors.RESET} {check_plugin_enabled_ret(entry)}")
            print(f"{Fore.CYAN + Colors.BOLD}{Version}:{Fore.RESET + Colors.RESET} {module.Spec.Version}")
            print(f"{Fore.CYAN + Colors.BOLD}{Commands}:{Fore.RESET + Colors.RESET} {module.Spec.Commands}")
    
    def exec(cmd):
        try:
            plugin_handler = module.PluginHandler
            getattr(plugin_handler, cmd)()
        except AttributeError as Err:
            print(ErrorOccured)
            print(f"{Fore.RED + Colors.BOLD}{ErrCode} 043:{Fore.RESET + Colors.BOLD} {Err}")