import helper_test

from config import Configuration
from database import Database
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
database = Database(configuration, helper)
database.db_path = config['default']['folder_data'] + '/test.db'

recording1 = '1_record_20190919100000.jpeg'
recording2 = '1_record_20190818144842.jpeg'
recording3 = '1_recording_nono_.jpeg'
compressed = '20190818172955.zip'

def in_list_member_0(list_check, item):
    if isinstance(list_check, list):
        if str(list_check[0]) in item:
            return True
    return False

helper_test.file_delete(database.db_path)
assert database.db_check() == 'db ok', 'failed initial db creation'

assert database.add_recording(recording1) == 1, 'Failed adding recording1'
assert database.add_recording(recording1) == 'exists', 'Failed adding recording1'
assert database.add_recording(recording2) == 2, 'Failed adding recording2'

assert database.query_recording_id(recording1) == 1, 'Failed query recording1'
assert database.query_recording_id(recording3) == 'failed', 'Failed handling missing recordings'

assert database.add_compressed(compressed) == 1, 'Failed adding compress'
assert database.add_compressed2recording(compressed, recording1) == 'added', ' Failed adding compressed2recording'
assert database.add_compressed2recording(compressed, recording1) == 'failed', ' adding again recording to compressed2recording should not be allowed'
assert database.add_compressed2recording(compressed, recording2) == 'added', ' Failed adding compressed2recording'
assert in_list_member_0(database.query_compressed2recording(compressed), recording1) == True, 'Failed finding compressed with recording1'
assert database.query_compressed2recording(recording1) == compressed, 'Failed to find recording in compressed'
