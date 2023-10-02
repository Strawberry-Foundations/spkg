#!/usr/bin/env python3

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

import time
import sqlite3 as sql
import urllib.request
import requests

from sqlite3 import *
from urllib.error import HTTPError
from colorama import Fore
from halo import Halo
from sys import exit
from init import *
from src.functions import delete_last_line


# Try to connect to the locally saved main package database
try:
    db = sql.connect(Files.package_database)
    c  = db.cursor()

# If the Database doesn't exists/no entries, return a error
except OperationalError:
    pass

class FileSizes:
    Kilobytes = 0
    Megabytes = 1
    

class DownloadManager:
    class Downloader:
        def __init__(self, package_name):
            self.package_name = package_name
            
        
        def fetch_url(self, url):
            try:
                request = urllib.request.Request(
                    url,
                    data = None,
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                )
                
                return urllib.request.urlopen(request)
                
            except:
                print(StringLoader("HttpError"))
                exit()
                
                
        def file_size(self, response, type: FileSizes):
            file_size_bytes = int(response.headers.get('Content-Length', 0))
            
            if type == FileSizes.Megabytes:
                return file_size_bytes / (1024 * 1024)
            
            elif type == FileSizes.Kilobytes:
                return file_size_bytes / 1024
                
            
        def download(self):
            spinner = Halo(text=f"{StringLoader('SearchingDatabaseForPackage')}",
                           spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                           text_color="white",
                           color="green")
            
            spinner.start()
            time.sleep(.1)
            
            c.execute("SELECT arch FROM packages where name = ?", (self.package_name,))
            
            try:
                result = c.fetchone()[0]
                
            except TypeError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader('PackageNotFound'))
                exit()

            if result == "all":
                try:
                    c.execute("SELECT name, fetch_url, file_name FROM packages where name = ?", (self.package_name,))
                
                except OperationalError:
                    print(StringLoader("PackageDatabaseNotSynced"))
                    exit()

            else:
                try:
                    c.execute("SELECT name, fetch_url, file_name FROM packages where name = ? AND arch = ?", (self.package_name, arch))
                    
                except OperationalError:
                    print(StringLoader("PackageDatabaseNotSynced"))
                    exit()

            try:
                for row in c:
                    url = row[1]
                    filename = row[2]
                    
                    headers = requests.head(url)
                    file_size = round(self.file_size(response=headers, type=FileSizes.Megabytes), 2)
                    
                file = self.fetch_url(url)
                
                spinner.stop()
                print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{StringLoader('SearchingDatabaseForPackage')}")
                
                try:
                    cont_package_download = input(f"{StringLoader('ContinuePackageDownload', argument_1=filename)}{Colors.RESET}{GREEN}")

                except KeyboardInterrupt as e:
                    print(f"\n{RESET}{StringLoader('Abort')}")
                    exit()

                if not cont_package_download.lower() in ["y", "j", "yes", "ja"]:
                    print(RESET + StringLoader("Abort"))
                    exit()

                download_time_start = time.time()

                spinner = Halo(
                    text=f"{StringLoader('Get')}: {url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})",
                    spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                    text_color="white",
                    color="green")
                
                spinner.start()

                with open(filename, 'wb') as download_archive:
                    download_archive.write(file.read())

                download_time_end = time.time()
                spinner.stop()
                print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{Colors.BOLD}{StringLoader('Get')}: {url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})")
                print(f"{StringLoader('FinishedDownloading')} {Fore.CYAN + Colors.BOLD}{filename}{Colors.RESET} in {round(download_time_end - download_time_start, 2)} s{Colors.RESET}")
                

            except NameError as e:
                print(StringLoader('PackageNotFound'))
                exit()
                
            except Exception as e:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader("HttpError"))
                exit()
        
        
        def compact_download(self, noarch=False):            
            c.execute("SELECT arch FROM packages where name = ?", (self.package_name,))
            
            try:
                result = c.fetchone()[0]
                
            except TypeError:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader('PackageNotFound'))
                exit()

            if noarch == False:
                if result == "all":
                    try:
                        c.execute("SELECT name, fetch_url, file_name FROM packages where name = ?", (self.package_name,))
                    
                    except OperationalError:
                        print(StringLoader("PackageDatabaseNotSynced"))
                        exit()

                else:
                    try:
                        c.execute("SELECT name, fetch_url, file_name FROM packages where name = ? AND arch = ?", (self.package_name, arch))
                        
                    except OperationalError:
                        print(StringLoader("PackageDatabaseNotSynced"))
                        exit()
                        
            elif noarch == True:
                try:
                    c.execute("SELECT name, fetch_url, file_name FROM packages where name = ?", (self.package_name))
                        
                except OperationalError:
                    print(StringLoader("PackageDatabaseNotSynced"))
                    exit()
                    
            else:
                exit()

            try:
                for row in c:
                    url = row[1]
                    
                    filename = row[2]
                    
                    try:
                        headers = requests.head(url)
                        file_size = round(self.file_size(response=headers, type=FileSizes.Megabytes), 2)
                        
                        file = self.fetch_url(url)
                    
                        spinner = Halo(
                            text=f"{StringLoader('Get')}: {url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})",
                            spinner={'interval': 200, 'frames': ['[-]', '[\\]', '[|]', '[/]']},
                            text_color="white",
                            color="green")
                        
                        spinner.start()

                        with open(filename, 'wb') as download_archive:
                            download_archive.write(file.read())

                        print()
                        spinner.stop()
                        delete_last_line()
                        print(f"{Fore.GREEN + Colors.BOLD}[✓] {Fore.RESET + Colors.RESET}{Colors.BOLD}{StringLoader('Get')}: {url} ({GREEN + Colors.BOLD}{file_size} MB{Colors.RESET})")
                    
                    except:
                        print(f"{RED + Colors.BOLD}[×]{RESET} {Fore.RESET + Colors.RESET}{Colors.BOLD}{StringLoader('Get')}: {url}")
                        print(f"{RED + Colors.BOLD} ↳ {RESET} {StringLoader('UnsuccessPackageDownload', argument_1=self.package_name)}")

            except NameError as e:
                print(e)
                print(StringLoader('PackageNotFound'))
                exit()
                
            except HTTPError as e:
                print("")
                delete_last_line()
                print(f"{RED + Colors.BOLD}[×]{RESET} {StringLoader('SearchingDatabaseForPackage')}")
                print(StringLoader("HttpError"))
                exit()
            
            
    # def download_compact_noarch(name): 
    #     try:
    #         c.execute("SELECT name, fetch_url, file_name FROM packages where name = ?", (name,))
        
    #     except OperationalError:
    #         print(PackageDatabaseNotSynced)
    #         exit()
        
    #     download_time_start = time.time()
        
    #     for row in c:
    #         url = row[1]
    #         filename = row[2]
            
    #         response = requests.head(url)
    #         file_size_bytes = int(response.headers.get('Content-Length', 0))
    #         file_size_mb = file_size_bytes / (1024 * 1024)

    #     try:
    #         req = urllib.request.Request(
    #             url,
    #             data=None,
    #             headers={
    #                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    #             }
    #         )

    #         f = urllib.request.urlopen(req)

    #         spinner = Halo(text=f"{StrGet}: {url} ({round(file_size_mb, 2)} MB)", spinner={'interval': 200, 'frames': [
    #                        '[-]', '[\\]', '[|]', '[/]']}, text_color="white", color="green")
    #         spinner.start()

    #         with open(filename, 'wb') as file:
    #             file.write(f.read())

    #         print()
            
    #         spinner.stop()

    #     except HTTPError as e:
    #         print(Str[lang]["HttpError"])
    #         exit()

    #     except NameError as e:
    #         print(PackageNotFound)
    #         exit()