import os
import sqlite3


def dir_data():
    home = os.getenv('HOME')
    path_data = home + '/actioncam/data'
    if not os.path.exists(path_data):
        os.makedirs(path_data)
    return path_data


dd = dir_data()
db = dd + '/actioncam.db'
conn = sqlite3.connect(db)
print("successfully create database " + db)

conn.execute('''CREATE TABLE compress (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name           TEXT    NOT NULL,
                date           TEXT    NOT NULL
                );''')
print("successfully created table compress")

conn.execute('''CREATE TABLE recording (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                identifier     TEXT    NOT NULL,
                mode           TEXT    NOT NULL,
                name           TEXT    NOT NULL,
                type           TEXT    NOT NULL,
                date           TEXT    NOT NULL
                );''')
print("successfully created table recording")

# connection tables
conn.execute('''CREATE TABLE compress2recording (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_compress    INT     NOT NULL,
                id_recording   INT     NOT NULL,
                FOREIGN KEY (id_compress) REFERENCES compress (id),
                FOREIGN KEY (id_recording) REFERENCES recording (id)
                );''')
print("successfully created table compress2recording")

conn.close()
