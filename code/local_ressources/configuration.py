# -*- coding: utf-8 -*-
import collections
import json
import os


class Configuration:

    def __init__(self, name, path='../config.json', debug=False):
        self.name = name
        self.config_path = path
        self.debug = debug

        self.config = self.load(path)
        self.copy_default_to_all_sections()

    def load(self, config_path):
        if self.debug:
            print('load config from', config_path)
        if os.path.exists(config_path):
            with open(config_path) as json_data:
                j_config = json.load(json_data)
            if self.name in j_config:
                j_config = j_config[self.name]
            else:
                print(self.name + ' not found in ' + config_path)
                return {}
            j_config = self.dict_replace_values(j_config, self.replacements())
            self.config_path = config_path
            return j_config
        else:
            print('config file %s not found' % config_path)
            return {}

    def save(self):
        data = self.config
        deletions = []
        if "DEFAULT" in self.config:
            _default = self.config['DEFAULT']
            for k_c , v_c in self.config.items():
                if k_c != "DEFAULT" and k_c != "debug":
                    for kk_c, vv_c in self.config[k_c].items():
                        for k_d, v_d in _default.items():
                            if kk_c == k_d and self.config[k_c][kk_c] == v_d:
                                deletions.append([k_c,kk_c])
        for deletion in deletions:
            del data[deletion[0]][deletion[1]]
        return self.save_json(data)
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
                if isinstance(v, list):
                    _v = []
                    for value in v:
                        value = value.replace(r, replace[r])
                        _v.append(value)
                    obj[k] = _v
                if isinstance(v, dict):
                    self.dict_replace_values(v, replace, indent + indent)
        return obj

    def path_home(self):
        _path = os.getenv('USERPROFILE')
        if _path == '' or _path is None:
            _path = os.getenv('HOME')
        _path = str(_path)
        _path = _path.replace('\\', '/')
        if self.debug:
            print("Home Path is " + _path)
        return _path

    def replacements(self):
        _homepath = self.path_home()
        key_value_pairs = {"PATHHOME": _homepath}
        return key_value_pairs

    def save_json(self, data):
        data = collections.OrderedDict(sorted(data.items()))
        data = { self.name : data }
        data = json.dumps(data, indent=4)
        with open(self.config_path, 'w') as outfile:
            outfile.write(data)
        if self.debug:
            print('new config saved in', self.config_path)
        return
