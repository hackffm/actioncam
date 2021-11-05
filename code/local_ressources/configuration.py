# -*- coding: utf-8 -*-
import json
import os
import sys


class Configuration:

    def __init__(self, name, path='../config.json'):
        self.config_name = name
        self.config = self.load(path)
        pass

    def load(self, config_path):
        print('load config from', config_path)
        if os.path.exists(config_path):
            with open(config_path) as json_data:
                j_config = json.load(json_data)
            if self.config_name in j_config:
                j_config = j_config[self.config_name]
            else:
                print(self.config_name + ' not found in ' + config_path)
                return {}
            j_config = self.dict_replace_values(j_config, self.replacements())
            return j_config
        else:
            print('config file %s not found' % config_path)
            return {}

    def save(self):
        data = {'actioncam': self.config}
        data = json.dumps(data, indent=4)
        with open(self.config_path, 'w') as outfile:
            outfile.write(data)
        print('new config saved in', self.config_path)
        return

    # -- config ------------------------------------------------------------------
    def default(self, section):
        default = self.config["default"]
        if section in self.config:
             for key in self.config[section]:
                 default.update(self.config[section])
        return default

    def default_mode(self):
        _mode = {"actioncam": self.config['default']['mode'],
                 "camera": self.config['camera']['mode']['pause'],
                 "idle": 0}
        return _mode

    def output(self):
        output = self.config['default']['output']
        output = self.config[output]
        return output

    def recording_folder(self):
        output = self.config['default']['recording_location']

        if output != '':
            if not os.path.exists(output):
                print('create ' + output)
                os.makedirs(output)

            return output
        else:
            print('Error: no recording_location folder set in defaults')
            sys.exit()

    def previewpattern(self):
        default = self.config['default']
        pattern = str(default['identify']) + '_*' + self.config['preview']['file_extension']
        return pattern

    def valid_camera_mode(self, new_mode):
        if new_mode in self.config['camera']['mode']:
            return True
        return False

    # -- Helper ------------------------------------------------------------------
    def dict_replace_values(self, obj, replace, indent='    '):
        for r in list(replace.keys()):
            for k, v in obj.items():
                if isinstance(v, str):
                    if r in v:
                        v = v.replace(r, replace[r])
                        obj[k] = v
                    # print(indent + k + " : " + v)
                if isinstance(v, list):
                    _v = []
                    for value in v:
                        value = value.replace(r, replace[r])
                        _v.append(value)
                    obj[k] = _v
                if isinstance(v, dict):
                    # print(indent + k)
                    self.dict_replace_values(v, replace, indent + indent)
        return obj
    
    def path_home(self):
        _path = os.getenv('USERPROFILE')
        if _path == '' or _path == None:
            _path = os.getenv('HOME')
        _path = str(_path)
        _path = _path.replace('\\', '/')
        return _path

    def replacements(self):
        _homepath = self.path_home()
        key_value_pairs = {"PATHHOME":_homepath}
        return key_value_pairs
