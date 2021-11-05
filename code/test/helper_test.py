import os
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.dirname(file_dir)
project_dir = os.path.dirname(code_dir)
ressources_dir = os.path.join(code_dir, 'local_ressources')
sys.path.append(ressources_dir)
sys.path.append(code_dir)


def config_path():
    home = os.getenv('HOME')
    c_path = project_dir + '/shell/setup/config.json'
    if not os.path.exists(c_path):
        print('failed to find config file in ' + c_path)
        print('see in ../shell/setup for an example')
        sys.exit(1)
    return c_path


def file_delete(file_name):
    if os.path.exists(file_name):
        print('remove ' + file_name)
        os.remove(file_name)
