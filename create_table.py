from multiprocessing import connection
import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username UNIQUE text,password text)"
cursor.execute(create_table)

connection.commit()
connection.close()
