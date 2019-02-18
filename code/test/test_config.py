import os
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(file_dir)
utils_dir = os.path.join(parent_dir, 'utils')
sys.path.append(utils_dir)

from config import Configuration


def config_path():
    home = os.getenv('HOME')
    c_path = home + '/actioncam/config.json'
    if not os.path.exists(c_path):
        print('failed to find config file in ' + c_path)
        print('see in ../shell/setup for an example')
        sys.exit(1)
    return c_path

configuration = Configuration(config_path=config_path())
config = configuration.config
_input = config['camera']['input']
_input = config['input'][_input]
print(_input)