import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO shoes (title, image, price) VALUES (?, ?,?)", ("Prada", "https://images.app.goo.gl/MRbUpGPGnk3ya83D9", "ksh10000"))
cursor.execute("INSERT INTO shoes (title,image, price) VALUES (?, ?, ?)", ('Toughees', "https://images.app.goo.gl/QXpuchEErRWKg4So7", "Ksh2500"))

connection.commit()

connection.close()