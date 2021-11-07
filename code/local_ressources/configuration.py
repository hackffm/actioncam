# -*- coding: utf-8 -*-
import json
import os


def path_home():
    _path = os.getenv('USERPROFILE')
    if _path == '' or _path is None:
        _path = os.getenv('HOME')
    _path = str(_path)
    _path = _path.replace('\\', '/')
    return _path


def replacements():
    _homepath = path_home()
    key_value_pairs = {"PATHHOME":_homepath}
    return key_value_pairs


class Configuration:

    def __init__(self, name, path='../config.json'):
        self.config_name = name
        self.config = self.load(path)
        self.copy_default_to_all_sections()

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
            j_config = self.dict_replace_values(j_config, replacements())
            return j_config
        else:
            print('config file %s not found' % config_path)
            return {}

    def save(self):
        data = {self.config_name : self.config}
        data = json.dumps(data, indent=4)
        with open(self.config_path, 'w') as outfile:
            outfile.write(data)
        print('new config saved in', self.config_path)
        return

    # -- Helper ------------------------------------------------------------------
    def copy_default_to_all_sections(self):
        if 'DEFAULT' in self.config:
            _DEFAULT = self.config['DEFAULT']
            for k_c, v_c in self.config.items():
                if k_c not in ('DEFAULT','debug'):
                    for k_d, v_d in _DEFAULT.items():
                        if k_d not in self.config[k_c]:
                            self.config[k_c][k_d] = v_d
        else:
            return

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
