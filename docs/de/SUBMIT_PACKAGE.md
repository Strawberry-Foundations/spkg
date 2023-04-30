# Pakete einreichen
Das einreichen von Paketen erfreut uns immer wieder, da so unser Repository immer weiter wächst! Es erfordert aber, das du mindestens einen GitHub Account oder ein Discord Account besitzt. 

spkg ist so aufgebaut, das es sogenannte "Setup Scripts" herunterlädt und diese dann ausführt. Diese Scripts können inviduell aufgebaut sein. Allerdings müssen diese bestimmte Richtlinien befolgen. Diese sind:
1. Du musst bestätigen das das Setup Script keine bösen Dinge macht, keine Viren installiert, nix zerstört oder unerlaubtes Datensammeln macht. 
2. Temporäre Dateien müssen nach /tmp heruntergeladen werden und extrahiert werden. Falls dann irgendwas nicht gelöscht werden kann oder das Script fehlerhaft ist, werden die temporären Dateien nach einem Neustart des Systemes gelöscht.
3. Es muss eine Upgrade Funktion geben, was Nutzern die Möglichkeit bietet, ein Programm zu updaten, ohne das Nutzerdaten oder anderes verloren gehen. Falls das Programm keine Nutzerdaten speichert, ist dies nicht benötigt. Allerdings sollte vor dem Upgrade die vorherige Installation des Programmes bereinigt werden damit keine Duplikate entstehen. 
4. Es muss mindestens den apt Paketmanager unterstützen. Weitere Paketmanager sind optional, es ist gerne gesehen wenn immer mehr Paketmanager unterstützt werden. 
5. Du musst akzeptieren, das wir dein Script nach unseren Bedürfnissen anpassen dürfen

### Jetzt aber ans arbeiten. Wie kann ich ein Paket einreichen? 
Schreibe zuerst ein Setup Script was das Paket installiert. Nimm dir gerne ein Beispiel an andere Setup Scripts, wie z.B. [cpufetch](https://github.com/Salware-Foundations/spkg/blob/main/setup_scripts/cpufetch.setup) oder [spkg-git](https://github.com/Salware-Foundations/spkg/blob/main/setup_scripts/spkg_git.setup). 
Üblicherweise lädt spkg die Source Dateien direkt herunter. Also muss das herunterladen der Sources nicht über den Setup Script erfolgen. Ein Eintrag in der Paketdatenbank sieht so aus: ![package.db in DB Browser for SQLite](https://cdn.discordapp.com/attachments/880513737948270642/1102303575566192702/image.png)
Das Paket wird dann mit den Namen was in file_name drinnen steht nach /tmp/ heruntergeladen. Das Setup Script muss das Archiv dort entpacken, und dort rein cd'en. 
Anschließend müssen die benötigten Abhänigkeiten installiert werden. Dann werden die nötigen Befehle ausgeführt, um das Programm zu installieren. Das ist je nach Programm inviduell. Wenn das Programm installiert ist, müssen die temporären Dateien gelöscht werden. 

Wenn das alles getan ist kannst du mir entweder auf Discord schreiben (`$ Juliandev02#6046`) und mir die nötigen Dateien & Informationen geben, oder du kannst Vorzugsweise ein Pull Request auf GitHub öffnen. Es ist wahrscheinlicher das wir ein Pull Request annehmen als über Discord. 

Noch fragen? [Eröffne ein Issue](https://github.com/Salware-Foundations/spkg/issues/new/choose) oder schreib mir auf Discord (`$ Juliandev02#6046`).