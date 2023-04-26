import sqlite3
connection = sqlite3.connect('chattopiadb.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE chat(chatID INTEGER PRIMARY KEY, chat TEXT, user INTEGER)')
