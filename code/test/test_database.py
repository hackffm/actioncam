import tracemalloc

debug = False
tracemalloc.start()

import helper_test

from config import Configuration
from database import Database
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
_db_name = 'test.db'
config['database']['name'] = _db_name
_db_path = config['default']['folder_data'] + '/' + _db_name

compressed = '20190818172955.zip'
identifier1 = '1'
identifier2 = '2'
mode1 = 'recording'
mode2 = 'motion'
recording1 = '1_record_motion_20190219204447.avi'
recording2 = '1_record_video_20190219204453.avi'
recording3 = '1_record_motion_20190000000000.avi'
path1 = '/user/home/actioncam'
preview1 = '1_20190219204447_.jpeg'
preview2 = '1_20190219204453_.jpeg'


def in_list_member_0(list_check, item):
    print(str(list_check))
    print(item)
    if isinstance(list_check, list):
        if str(list_check[0]) in item:
            return True
    return False


# preparation
helper_test.file_delete(_db_path)
database = Database(configuration, helper)
assert database.db_check() == 'db ok', 'failed initial db creation'

# recordings
assert database.add_recording(identifier1, mode1, path1, preview1, recording1) == 1, 'recording1 addeed with id 1'
assert database.add_recording(identifier1, mode1, path1, preview1, recording1) == 'exists', 'Failed adding recording1'
assert database.add_recording(identifier2, mode2, path1, preview2, recording2) == 2, 'recording2 addeed with id 2'
assert database.query_recording_id(recording1) == 1, 'recording1 found'
assert database.query_recording_id(recording3) == 'failed', 'Failed finding missing recordings'
print('added recordings')

# compress
assert database.add_compressed(compressed) == 1, 'adding compress'
assert database.add_compressed2recording(compressed, recording1) == 'executed', 'Failed adding compressed2recording'
assert database.add_compressed2recording(compressed, recording1) == 'failed', 'adding again recording to compressed2recording should not be q_reportowed'
assert database.add_compressed2recording(compressed, recording2) == 'executed', 'Failed adding compressed2recording'

# send
assert database.add_send(compressed, '5000', 'test@test.com', str(helper.now())) == 'executed', 'Failed adding send'
send = database.query_send()
print('found send compressed files \n' + str(send))

# final report
print('--Final report--')
q_report = database.query_report()
for qr in q_report:
   q = str(qr)
   q = q.replace('(','')
   q = q.replace(')','')
   q = q.split(',')
   _ri = q[0]
   _rn = q[4]
   _cn = q[6]
   _cd = q[7]
   _sd = q[8]
   print("recording {} name {} was compressed in {} on {} and send at date {}".format(_ri, _rn, _cn, _cd, _sd))

if debug == True:
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics("lineno"):
        print(stat)