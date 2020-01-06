import helper_test

from config import Configuration
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
_db_name = 'test.db'
config['database']['name'] = _db_name


def test_report_all():
    items = helper.report_all()
    print(type(items))
    print(items)


test_report_all()