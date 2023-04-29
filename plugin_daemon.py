#!/usr/bin/env python3

import json

from sqlite3 import *
from colorama import Fore
from sys import exit
import importlib
import sqlite3 as sql

class Colors:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

enabled_plugins_cfg = "/etc/spkg/enabled_plugins.json"
package_database = "/etc/spkg/package.db"
spkg_config = "/etc/spkg/config.json"

with open(enabled_plugins_cfg, "r") as f:
    data = json.load(f)

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
    UserConfigNotExists = f"{Fore.RED + Colors.BOLD}Error:{Fore.RESET + Colors.RESET} Deine Nutzerkonfiguration existiert nicht."
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} Die Paketdatenbank wurde noch nicht synchronisiert. Führe {Fore.CYAN}spkg sync{Fore.RESET} aus, um die Datenbank zu synchronisieren{Colors.RESET}"
    PluginMarketplace = "Advanced Source Package Managment - Plugin Marketplace"

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
    UserConfigNotExists = f"{Fore.RED + Colors.BOLD}Error:{Fore.RESET + Colors.RESET} Your user configuration doesn't exist."
    PackageDatabaseNotSynced = f"{Fore.RED + Colors.BOLD}[!]{Fore.RESET} The package database has not been synchronized yet. Run {Fore.CYAN}spkg sync{Fore.RESET} to synchronize the database{Colors.RESET}"
    

# Try to connect to the locally saved package database
try:
    db = sql.connect(package_database)
    c = db.cursor()

# If the Database doesn't exists/no entries, return a error
except OperationalError:
    print(PackageDatabaseNotSynced)
    exit()

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
        return True
    else:
        return False


def check_plugin_enabled_ret(plugin):
    plugin_data = data[plugin]
    if plugin_data == True:
        return Enabled
    else:
        return Disabled


class plugin_management:
    def list_plugins():
        print(f"{Colors.BOLD + Colors.UNDERLINE}{PluginManagement} -> {InstalledPlugins}\n")
        try:
            for entry in data:
                plugin_daemon.import_plugin(entry)
                
                print(f"{Fore.GREEN + Colors.BOLD + Colors.UNDERLINE}{module.Spec.Name} ({entry}){Fore.RESET + Colors.RESET}")
                print(f"{Fore.CYAN + Colors.BOLD}{Description}:{Fore.RESET + Colors.RESET} {module.Spec.Desc}")
                print(f"{Fore.CYAN + Colors.BOLD}{Condition}:{Fore.RESET + Colors.RESET} {check_plugin_enabled_ret(entry)}")
                print(f"{Fore.CYAN + Colors.BOLD}{Version}:{Fore.RESET + Colors.RESET} {module.Spec.Version}")
                print(f"{Fore.CYAN + Colors.BOLD}{Commands}:{Fore.RESET + Colors.RESET} {module.Spec.Commands}")
        except FileNotFoundError:
            print(UserConfigNotExists)
    
    def exec(cmd):
        try:
            plugin_handler = module.PluginHandler
            getattr(plugin_handler, cmd)()
            
        except AttributeError as Err:
            print(ErrorOccured)
            print(f"{Fore.RED + Colors.BOLD}{ErrCode} 043:{Fore.RESET + Colors.BOLD} {Err}")
    
    
    def marketplace():
        print(f"{Colors.BOLD + Colors.UNDERLINE + Fore.CYAN}{PluginMarketplace}\n")
        try:
                c.execute("SELECT * FROM plugins")
                for row in c:
                    print(f"{Colors.BOLD} * --------- {row[0]} --------- * {Colors.RESET} ")
                    print(f"   -> {Fore.GREEN + Colors.BOLD}Version: {Fore.RESET + Colors.RESET}{row[1]}           ")
                    print(f"   -> {Fore.GREEN + Colors.BOLD}Author: {Fore.RESET + Colors.RESET}{row[5]}           ")
                    print(f"   -> {Fore.GREEN + Colors.BOLD}Author: {Fore.RESET + Colors.RESET}{row[4]}           ")
                    print()
                exit()

        except OperationalError:
            print(PackageDatabaseNotSynced)