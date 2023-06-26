import sqlite3
import csv

connection = sqlite3.connect("valutes.db")
cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS valutes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        crb_date TEXT,
        value_id TEXT,
        num_code TEXT,
        char_code TEXT,
        nominal TEXT,
        name TEXT,
        value REAL
    )
""")


with open("valutes.csv", newline="", encoding="cp1251") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("""
            INSERT INTO valutes (date, crb_date, value_id, num_code, char_code, nominal, name, value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Date"],
            row["crb_date"],
            row["Value ID"],
            row["NumCode"],
            row["CharCode"],
            row["Nominal"],
            row["Name"],
            row["Value"]
        ))


connection.commit()