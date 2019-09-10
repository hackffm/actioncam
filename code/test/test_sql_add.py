import helper_test

from config import Configuration
from database import Database
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
database = Database(configuration, helper)

#print(database.db_check())
recording1 = '1_record_20190919100000.jpeg'
#recording2 = '1_record_20190818144842.jpeg'
compressed = '20190818172955.zip'
#print('test add recording ' + str(database.add_recording(recording1)))
#print(str(database.query_recording(recording1)))
#print(database.query_recording_name('20190919100000'))
print('test add compress ' + str(database.add_compressed(compressed)))
#print('test add c2r ' + str(database.add_compressed2recording(compressed, recording1)))
#print(database.add_recording('1_record_20190818144842.jpeg'))
'''
        _result = self.add_compressed(compressed)
        if not _result == self.executed:
            return 'failed adding compressed ' + str(_result)

        rd = self.recording_data(recording)
        _result = self.add_recording(rd)
        if not _result == self.executed:
            return _result
        _name = rd[2]
'''