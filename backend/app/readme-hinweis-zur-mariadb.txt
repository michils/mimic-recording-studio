# HINWEIS: Nachdem die DB im container läuft kann sie noch nicht von localhost aus erreicht werden!!!
# Dazu muss folgender GRANT Befehl abgesetzt werden!
# Beim EInloggen hakt es manchmal mit dem Passwort, welche in der docker-compose.yml vergeben wurde.
# Aber der Mechanismus funktioniert!!! Nicht aufgeben!  Und danach kann auch mit phpMyAdmin problemlos auf die DB zuggriffen werden!


Direkter Zugang zum Datenbank-Client im Container
Wenn du Probleme hast, dich via Root anzumelden, kannst du im Container eine Shell starten und den mariadb-Client ohne Passwortzugang testen:

text
docker exec -it <container-name> sh
mariadb -u root -p

Falls das klappt, ändere mit SQL-Befehlen das Passwort oder berechtige den Root-Zugang via:

text
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'example' WITH GRANT OPTION;
FLUSH PRIVILEGES;

Danach ist der root-Zugang auch remote von anderen Containern erlaubt.
~
