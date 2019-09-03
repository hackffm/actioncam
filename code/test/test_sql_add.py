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


def add_compressed(compressed):
    _date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    conn.execute("INSERT INTO compress (name,date) \
            VALUES ('" + str(compressed) + "', '" + _date + "');")
    conn.commit()
    print('successfully added recording ' + str(compressed))


def add_recording(recording):
    r1 = recording.split('.')
    r = r1[0].split('_')
    r.append(r1[1])
    _date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    conn.execute("INSERT INTO recording (identifier,mode,name,type,date) \
            VALUES ('" + r[0] + "', '" + str(r[1]) + "', '" + str(r[2]) + "', '" + str(r[3]) + "', '" + _date + "');")
    conn.commit()
    print('successfully added recording ' + str(r))
    _name = r[2]
    return _name


def add_compressed2recording(compressed, recording):
    add_compressed(compressed)
    name = add_recording(recording)
    conn.execute("insert into compress2recording ( id_compress, id_recording) SELECT \
        (select id as id_compress from compress where name = '" + compressed + "'), \
        (select id as id_recording from recording where name = " + name + ")")
    conn.commit()
    print('successfully added compress2recording')


dp = db_path()
if not db_exists(dp):
    print('can not find db ' + dp)
    sys.exit(1)

conn = sqlite3.connect(dp)
print('successfully connected to ' + dp)

add_compressed2recording('20190818172955.zip', '1_record_20190818144842.jpeg')


