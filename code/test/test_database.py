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

recording1 = '1_record_motion_20190219204447.avi'
recording2 = '1_record_video_20190219204453.avi'
recording3 = '1_record_motion_20190000000000.avi'
preview1 = '1_20190219204447_.jpeg'
preview2 = '1_20190219204453_.jpeg'
compressed = '20190818172955.zip'


def in_list_member_0(list_check, item):
    if isinstance(list_check, list):
        if str(list_check[0]) in item:
            return True
    return False


# preparation
helper_test.file_delete(_db_path)
database = Database(configuration, helper)
# expect a double entry for tis in logfile
assert database.db_check() == 'db ok', 'failed initial db creation'

# recordings
assert database.add_recording(recording1) == 1, 'Failed adding recording1'
assert database.add_recording(recording1) == 'exists', 'Failed adding recording1'
assert database.add_recording(recording2) == 2, 'Failed adding recording2'
assert database.query_recording_id(recording1) == 1, 'Failed query recording1'
assert database.query_recording_id(recording3) == 'failed', 'Failed handling missing recordings'
assert database.add_recording(recording3) == 3, 'Failed adding recording3'
print('added recordings')

# compress
assert database.add_compressed(compressed) == 1, 'Failed adding compress'
assert database.add_compressed2recording(compressed, recording1) == 'executed', 'Failed adding compressed2recording'
assert database.add_compressed2recording(compressed, recording1) == 'failed', 'adding again recording to compressed2recording should not be q_reportowed'
assert database.add_compressed2recording(compressed, recording2) == 'executed', 'Failed adding compressed2recording'
assert in_list_member_0(database.query_compressed2recording(compressed), recording1) == True, 'Failed finding compressed with recording1'
assert database.query_compressed2recording(recording1) == compressed, 'Failed to find recording in compressed'
print('finding compressed ' + str(database.query_compressed()))

# state
q_state = database.query_state()
assert q_state['mode'] == config['mode']['stop'], 'failed verifying state'
q_state['mode'] = config['mode']['record_motion']
assert database.update_state(q_state) == 'executed', 'failed updating state'
print('state ' + str(q_state))

# send
assert database.add_send(compressed, '5000', 'test@test.com', str(helper.now())) == 'executed', 'Failed adding send'
send = database.query_send()
print('found send compressed files \n' + str(send))

# final report
print('--Final report--')
q_report = database.query_report()
for a in q_report:
    _pn = a[0]
    if _pn == None:
        _pn = 'missing'
    _ri = a[1]
    _rm = a[2]
    _rn = a[3]
    _rt = a[4]
    _cn = a[5]
    _cd = a[6]
    _sd = a[7]
    if _cn == None:
        print("No preview for recording {}_{}_{}.{}".format(_ri, _rm, _rn, _rt))
    else:
        print("Preview {} for recording {}_{}_{}.{} was compressed in {} on {} and send at date {}".format(
            _pn, _ri, _rm, _rn, _rt, _cn, _cd, _sd))
