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
print ("successfully create database " + db)

conn.execute('''CREATE TABLE COMPRESS (
                ID INT PRIMARY KEY     NOT NULL,
                NAME           TEXT    NOT NULL,
                DATE           TEXT    NOT NULL
                );''')
print ("successfully created table COMPRESS")

conn.execute('''CREATE TABLE RECORDING (
                IDENTIFIER     TEXT    NOT NULL,
                MODE           TEXT    NOT NULL,
                NAME           TEXT    NOT NULL,
                TYPE           TEXT    NOT NULL,
                DATE           TEXT    NOT NULL
                );''')
print ("successfully created table RECORDJNG")

#connection tables
conn.execute('''CREATE TABLE COMPRESS2RECORDING (
                ID INT PRIMARY KEY     NOT NULL,
                ID_COMPRESS    INT     NOT NULL,
                ID_RECORDING   INT     NOT NULL
                );''')
print ("successfully created table COMPRESS2RECORDING")

conn.close()
