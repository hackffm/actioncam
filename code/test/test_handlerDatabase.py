import helper_test

import requests

from config import Configuration
from database import Database
from helper import Helper


configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
database = Database(configuration, helper)
database.db_path = config['default']['folder_data'] + '/test.db'
db_url = 'http://localhost:8081/database'
headers = {'content-type': 'application/json','Accept-Charset': 'UTF-8'}


def log(text):
    print(text)
    helper.log_add_text('test', text)


def query_compressed():
    log('query_compressed')
    try:
        data = '{"query": {"compressed": "None"}}'
        response = requests.get(db_url, headers=headers, data=data)
        return response.text
    except Exception as e:
        return e


def query_report():
    log('query_report')
    try:
        data = '{"query": {"report": "None"}}'
        headers = {'content-type': 'application/json','Accept-Charset': 'UTF-8'}
        response = requests.get(config['database']['url'], headers=headers, data=data)
        return response.text
    except Exception as e:
        return e


print(query_compressed())
print(query_report())