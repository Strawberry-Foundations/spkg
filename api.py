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

def plugin(name):
    def wrapper(*args, **kwargs):
        # Hier können Sie Code ausführen, bevor die Funktion aufgerufen wird

        print("test")
    return wrapper