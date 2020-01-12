# -*- coding: utf-8 -*-
import json
import os
import sys


class Configuration:

    def __init__(self, config_path='../config.json'):
        self.config_name = 'actioncam'
        self.config = []
        self.load(config_path)

    def load(self, config_path):
        print('load config from', config_path)
        if os.path.exists(config_path):
            with open(config_path) as json_data:
                j_config = json.load(json_data)
            self.config = j_config[self.config_name]
        else:
            print('config file %s not found' % config_path)

    def save(self):
        data = {'actioncam': self.config}
        data = json.dumps(data, indent=4)
        with open(self.config_path, 'w') as outfile:
            outfile.write(data)
        print('new config saved in', self.config_path)
        return

    # -- config ------------------------------------------------------------------
    def default_mode(self):
        _mode = {"actioncam": self.config['default']['mode'],
                 "camera": self.config['camera']['mode']['pause'],
                 "idle": 0}
        return _mode

    def output(self):
        output = self.config['default']['output']
        output = self.config[output]
        return output

    def output_folder(self):
        output = self.config['default']['output']
        output_folder = self.config[output]['file_location']

        if output_folder != '':
            if not os.path.exists(output_folder):
                print('create ' + output_folder)
                os.makedirs(output_folder)

            return output_folder
        else:
            print('Error: no output folder set')
            sys.exit()

    def previewpattern(self):
        default = self.config['default']
        pattern = str(default['identify']) + '_*' + self.config['preview']['file_extension']
        return pattern

    def valid_camera_mode(self, new_mode):
        if new_mode in self.config['camera']['mode']:
            return True
        return False
