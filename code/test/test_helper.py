import os
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(file_dir)
dir_lr = os.path.join(parent_dir, 'local_ressources')
sys.path.append(dir_lr)


def config_path():
    home = os.getenv('HOME')
    c_path = home + '/actioncam/config.json'
    if not os.path.exists(c_path):
        print('failed to find config file in ' + c_path)
        print('see in ../shell/setup for an example')
        sys.exit(1)
    return c_path
