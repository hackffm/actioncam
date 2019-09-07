import helper_test

from config import Configuration
from database import Database
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
database = Database(configuration, helper)

print(database.db_check())
print(database.add_compressed2recording('20190818172955.zip', '1_record_20190818144842.jpeg'))
#print(database.add_recording('1_record_20190818144842.jpeg'))