import os
import sqlite3
import sys

def db_path():
    home = os.getenv('HOME')
    path_data = home + '/actioncam/data/actioncam.db'
    return path_data

def db_exists(path_db):
    if not os.path.exists(path_db):
        return False
    return True

dp = db_path()
if not db_exists(dp):
    print('can not find db ' + dp)
    sys.exit(1)

conn = sqlite3.connect(dp)
print('successfully connected to ' + dp)

conn.execute("INSERT INTO RECORDING (ID,NAME,DATE) \
        VALUES (1, '20190828225930', 20190828 )");
conn.commit()
print('successfully inserted intorecording')
