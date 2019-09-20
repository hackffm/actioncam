import helper_test

import requests

from config import Configuration
from helper import Helper


configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)


def log(text):
    helper.log_add_text('test', text)


def query_compressed():
    log('query_compressed')
    response = []
    try:
        headers = {
            'content-type': 'application/json',
            'Accept-Charset': 'UTF-8'
        }
        data = '{"query": {"compressed": "None"}}'
        response = requests.get('http://localhost:8081/database', headers=headers, data=data)
    except Exception as e:
        log(str(e))
    return response.text


print(query_compressed())
