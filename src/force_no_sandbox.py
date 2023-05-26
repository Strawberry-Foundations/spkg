import sqlite3 as sql
import platform

from sqlite3 import *
from sys import exit
from defs import *

# from plugin_daemon import *
# from src.pkg_install import * 
# from src.pkg_remove import * 
# from src.pkg_download import *

arch = platform.machine()

if arch == "x86_64":
    arch = "amd64"
elif arch == "x86":
    arch = "i386"
elif arch == "aarch64":
    arch = "arm64"
    

# Try to connect to the locally saved package database
try:
    db = sql.connect(package_database)
    c = db.cursor()

# If the Database doesn't exists/no entries, return a error
except OperationalError as e:
    print(e)
    exit()

def force_no_sandbox(pkg_name):
    c.execute("SELECT arch FROM packages where name = ?", (pkg_name,))
    
    try:
        result = c.fetchone()[0]
        
    except TypeError as e:
        print(e)
        exit()
    
    if result == "all":
        try:
            c.execute("SELECT ForceNoSandbox FROM packages where name = ?", (pkg_name,))
            for row in c:
                return row[0]

        except OperationalError as e:
            print(e)
            exit()
        
    else:
        try:
            c.execute("SELECT ForceNoSandbox FROM packages where name = ? AND arch = ?", (pkg_name, arch))
            for row in c:
                return row[0]

        except OperationalError as e:
            print(e)
            exit()