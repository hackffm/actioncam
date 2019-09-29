import helper_test

from config import Configuration
from database import Database
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
database = Database(configuration, helper)
database.db_path = config['default']['folder_data'] + '/test.db'

recording1 = '1_motion_20190219204447.avi'
recording2 = '1_motion_20190219204453.avi'
recording3 = '1_recording_nono_.jpeg'
compressed = '20190818172955.zip'


def in_list_member_0(list_check, item):
    if isinstance(list_check, list):
        if str(list_check[0]) in item:
            return True
    return False


# preparation
helper_test.file_delete(database.db_path)
assert database.db_check() == 'db ok', 'failed initial db creation'


# store recordings and compressed
assert database.add_recording(recording1) == 1, 'Failed adding recording1'
assert database.add_recording(recording1) == 'exists', 'Failed adding recording1'
assert database.add_recording(recording2) == 2, 'Failed adding recording2'

assert database.query_recording_id(recording1) == 1, 'Failed query recording1'
assert database.query_recording_id(recording3) == 'failed', 'Failed handling missing recordings'

assert database.add_compressed(compressed) == 1, 'Failed adding compress'
assert database.add_compressed2recording(compressed, recording1) == 'executed', ' Failed adding compressed2recording'
assert database.add_compressed2recording(compressed, recording1) == 'failed', ' adding again recording to compressed2recording should not be allowed'
assert database.add_compressed2recording(compressed, recording2) == 'executed', ' Failed adding compressed2recording'
assert in_list_member_0(database.query_compressed2recording(compressed), recording1) == True, 'Failed finding compressed with recording1'
assert database.query_compressed2recording(recording1) == compressed, 'Failed to find recording in compressed'
print('finding compressed ' + str(database.query_compressed()))


# store state
state_default = helper.state_default()
state_test = database.query_state()
assert state_default['mode'] == state_test['mode'], 'Failed state check'
state_test['mode'] = 'running'
updated = database.update_state(state_test)
assert updated == 'executed', 'Failed updating state'
print('State is now \n' + str(state_test))

# store send
assert database.add_send(compressed, '5000', 'test@test.com', str(helper.now())) == 'executed', 'Failed adding send'
send = database.query_send()
print('found send compressed files \n' + str(send))
