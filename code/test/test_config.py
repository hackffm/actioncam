import test_helper

from config import Configuration

configuration = Configuration(config_path=test_helper.config_path())
config = configuration.config

_input = config['camera']['input']
_input = config['input'][_input]
print(_input)
print(config['default'])
