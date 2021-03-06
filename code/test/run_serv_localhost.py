import helper_test

import sys

from multiprocessing import Process

from config import Configuration
from helper import Helper
from database import Database
from serv_localhost import ServLocalhost


configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)

database = Database(configuration, helper)
database.db_path = config['default']['folder_data'] + '/test.db'

name = 'run_serv_localhost'


def log(text):
    helper.log_add_text(name, text)


if __name__ == '__main__':
    p1 = Process(target=ServLocalhost, args=(configuration, database, helper))
    try:
        p1.daemon = True
        p1.start()
        print('start ' + name)
        log('start ' + name)
        p1.join()
    except KeyboardInterrupt:
        log('ending with keyboard interrupt')
        p1.terminate()
        sys.exit()
    except Exception as e:
        log('error in ' + name + ' __main__ ' + str(e))
