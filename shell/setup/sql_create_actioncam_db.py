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
print ("database successfully creates as" + db)

conn.execute('''CREATE TABLE COMPRESS (
                ID INT PRIMARY KEY     NOT NULL,
                NAME           TEXT    NOT NULL,
                DATE           TEXT    NOT NULL
                );''')
print ("table compress created successfully")

conn.execute('''CREATE TABLE RECORDING (
                ID INT PRIMARY KEY     NOT NULL,
                NAME           TEXT    NOT NULL,
                DATE           TEXT    NOT NULL
                );''')
print ("table recording created successfully")

#connection tables
conn.execute('''CREATE TABLE COMPRESS2RECORDING (
                ID INT PRIMARY KEY     NOT NULL,
                ID_COMPRESS    INT     NOT NULL,
                ID_RECORDING   INT     NOT NULL
                );''')
print ("table compress2recording created successfully")

conn.close()
