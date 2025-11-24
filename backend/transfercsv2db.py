import csv
#import mariadb
import pymysql

from datetime import datetime

aktuelles_datum = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Verbindung zur MariaDB-Datenbank herstellen
conn = pymysql.connect(
    user="dbuser",
    password="dbuser",
    host="localhost",
    port=3306,
    database="mrsdb",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()

# Pfad zur CSV-Datei
csv_datei = 'metadata.csv'

# Konstante Werte für dbfeld3 und dbfeld4
user_id = '34ff85e5-c387-ce30-84d1-b19a2f642cd9'
language = 'german'

# CSV Datei öffnen und Zeilen einlesen
with open(csv_datei, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='|')
    for row in csv_reader:
        if len(row) >= 2:
            feld1 = row[0]     # audio_id
            feld2 = row[1]     # prompt
            # INSERT-Befehl mit den konstanten und CSV-Werten
            sql = """
            INSERT INTO audiomodel (audio_id, prompt, language, user_id, created_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (feld1, feld2, language, user_id, aktuelles_datum))

# Änderungen speichern und Verbindung schließen
conn.commit()
cursor.close()
conn.close()

