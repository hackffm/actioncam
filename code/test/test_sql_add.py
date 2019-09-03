import datetime
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


def add_recording(recording):
    r1 = recording.split('.')
    r = r1[0].split('_')
    r.append(r1[1])
    _date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    conn.execute("INSERT INTO RECORDING (IDENTIFIER,MODE,NAME,TYPE,DATE) \
            VALUES ('" + r[0] + "', '" + str(r[1]) + "', '" + str(r[2]) + "', '" + str(r[3]) + "', '" + _date + "');")
    conn.commit()

    print('successfully added recording ' + str(r))


dp = db_path()
if not db_exists(dp):
    print('can not find db ' + dp)
    sys.exit(1)

conn = sqlite3.connect(dp)
print('successfully connected to ' + dp)

recorded = '1_record_20190818144842.jpeg'
add_recording(recorded)

