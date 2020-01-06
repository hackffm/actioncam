import helper_test

from config import Configuration
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)

_input = config['camera']['input']
_input = config['input'][_input]
print(_input)
print(config['default'])

print(helper.log_home('ServLocalhost'))
print(helper.log_home('camera'))
print(config['database']['headers'])
