# Installation von spkg
Die Installation von spkg erfolgt über verschiedene Wege. Bevor du spkg installierst, kontrolliere ob dein System unterstützt ist. Das kannst du [hier](https://github.com/Salware-Foundations/spkg#linux-support) tun. 

# 1. Über den offiziellen Binary-Installer
Wir bieten einen einfachen Installer für spkg. So brauchst du (eigentlich) nur einen Befehl auszuführen, eine Eingabe tätigen und spkg wird für dich Installiert. 
→ [Link zum Download](https://sources.juliandev02.ga/bin/spkg-installer-ubuntu-amd64)
→ [Source Code](https://raw.githubusercontent.com/Salware-Foundations/spkg/main/spkg-installer.py)

Die einzige Vorraussetzung ist, das du `sudo` installiert haben musst. Außerdem solltest du in deinem Nutzerverzeichnis einen `.config` Ordner und einen `.local` Ordner besitzen. 
Wenn diese Vorraussetzungen erfüllt sind, führe den Installer aus! Wenn du keine Berechtigung dafür besitzt, musst du dir vorher diese geben. Führe dazu `chmod a+x spkg-installer*` aus.
Falls es Probleme beim Installieren gibt, kannst du gerne ein [Issue eröffnen](https://github.com/Salware-Foundations/spkg/issues/new/choose) oder mir auf Discord schreiben (`$ Juliandev02#6046`)

# 2. Über den Python-Code-Installer
Falls unsere fertige Binary bei dir nicht gehen sollte, kannst du auch einfach den Installer separat ausführen. Lade dazu einfach den [Source Code](https://raw.githubusercontent.com/Salware-Foundations/spkg/main/spkg-installer.py) herunter, oder klone [unser Repository](https://github.com/Salware-Foundations/spkg). Dafür brauchst du aber folgende Abhängigkeiten: `colorama halo requests urllib3`.
Führe diesen Installer einfach gewohnt wie jede andere Python Datei aus.
Falls es auch hier Probleme beim Installieren gibt, kannst du gerne ein [Issue eröffnen](https://github.com/Salware-Foundations/spkg/issues/new/choose) oder mir auf Discord schreiben (`$ Juliandev02#6046`)

# 3. Manuell
Falls beide Methoden nicht gehen sollten, oder du ein bisschen experimentieren willst, kannst du auch spkg per Hand installieren. Das ist allerdings etwas komplizierter und wird **nicht** empfohlen. 

1. Du benötigst folgende Abhängigkeiten: `python3 python3-dev python3-pip python3-sql python3-urllib3 sudo`
2. Klone [unser Repository](https://github.com/Salware-Foundations/spkg) oder lade den [aktuellsten Release](https://github.com/Salware-Foundations/spkg/releases/latest) von spkg herunter. 
3. Kopiere alle Source-Dateien nach `/usr/share/spkg/` → `sudo cp -r  /your/spkg/source/folder/  /usr/share/spkg/`
4. (Optional) Entferne die unnötigen Dateien `sudo rm -rf  build data resources setup_scripts package.db spkg-installer.py`
5. Verschiebe spkg.py zu spkg `sudo mv /usr/share/spkg/spkg.py /usr/share/spkg/spkg`
6. Kennzeichne die Python-Datei als ausführbar `sudo chmod a+x  /usr/share/spkg/spkg`
7. Erstelle einen dynamischen Link, damit spkg immer ausgeführt werden kann `sudo ln -s  /usr/share/spkg/spkg  /usr/bin/spkg`
8. Synchronisere die Datenbank und baue die World Datenbank neu `sudo spkg build  world && sudo spkg sync`

Das wars! 