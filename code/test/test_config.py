import json

import helper_test

from configuration import Configuration

configuration = Configuration(name='actioncam', path=helper_test.config_path())
config = configuration.config

print('debug is ' + str(type(config['debug'])))
print('debug is ' + str(config['debug']))

print("etting recording_location from default")
assert config['camera']['recording_location'] == config['DEFAULT']['recording_location'], \
    "Failed setting recording_location from default"
print("setting log_header individually")
assert config['camera']['log_header'] != config['DEFAULT']['log_header'], \
    "Failed setting log_header individually"

print(json.dumps(config, indent=4, sort_keys=True))