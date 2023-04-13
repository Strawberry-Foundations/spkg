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

class fakeroot:
    def setup():
        print("")