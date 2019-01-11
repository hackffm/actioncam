import datetime
import fnmatch
import json
import netifaces
import os
import socket
import pandas as pd


class Helper:

    def __init__(self, configuration):
        self.config = configuration.config

        self.default = self.config['default']
        self.config_mode = self.config['mode']

        _config_output = self.default['output']
        self.config_output = self.config[_config_output]

        self.state = self.state_start()

    def datetime_diff_from_string(self, dt_old):
        dt_now = self.now()
        delta = dt_now - self.datetime_from_string(dt_old)
        delta_seconds = delta.total_seconds()
        return delta_seconds

    def folder_files(self, folder_name, search_pattern):
        _files = os.listdir(folder_name)
        file_list = []
        for filename in _files:
            if fnmatch.fnmatch(filename, search_pattern):
                file_list.append(str(filename))
        return file_list

    def infos_self(self):
        infos = []
        infos.append('hostname ' + str(socket.gethostname()))
        infos.append('PID ' + str(os.getpid()))
        ifaces = self.interfaces_self()
        for iface in ifaces:
            infos.append(iface)
        return infos

    def interfaces_first(self):
        ips = self.interfaces_self()
        # remove ipv6 from results
        for ip in ips:
            if ':' not in ip:
                return ip
        return '127.0.0.1'

    def interfaces_self(self):
        ifaces = []
        for interface in netifaces.interfaces():
            if interface != 'lo':
                if 2 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[2][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
                if 17 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[17][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
                if 18 in netifaces.ifaddresses(interface):
                    _i = netifaces.ifaddresses(interface)
                    _i = _i[18][0]['addr']
                    if self.not_local(_i):
                        ifaces.append(_i)
        return ifaces

    def log_add_text(self, name, text):
        l_home = self.log_home(name)
        text = self.now_str() + ': ' + text
        with open(l_home, 'a') as outfile:
            outfile.write(text + '\n')

    def log_home(self, name):
        _name = self.config[name]
        log_home_path = _name['log_location'] + '/' + _name['log_file']
        try:
            if not os.path.exists(log_home_path):
                with open(log_home_path, 'w') as lf:
                    lf.write(_name['log_header'] + '\n')
            return log_home_path
        except IOError:
            return self.config['error']

    def not_local(self, ip):
        if ip != '127.0.0.1':
            return True
        return False

    def now(self):
        return datetime.datetime.now().replace(microsecond=0)

    def now_str(self):
        return datetime.datetime.now().strftime(self.config_output['file_format_time'])

    def report_csv(self, name):
        _log_home = self.report_home(name)
        _log_name = pd.read_csv(_log_home, sep=',')
        return _log_name

    def report_home(self, name):
        _name = self.config[name]
        log_home = _name['report_location'] + '/' + _name['report_file']
        try:
            if not os.path.exists(log_home):
                with open(log_home, 'w') as lf:
                    lf.write(_name['report_header'] + '/n')
            return log_home
        except IOError:
            return self.config.error

    def report_add(self, name, data):
        df = pd.DataFrame(data, index=[0])
        l_home = self.report_home(name)
        df.to_csv(l_home, mode='a', header=False, index=False)

    def datetime_from_string(self, text):
        return datetime.datetime.strptime(text, self.config_output['file_format_time'])

    # -- state --------------------------------------------------
    def state_start(self):
        state = {}
        state['dt_start'] = self.now_str()
        return state

    def state_load(self):
        with open(self.state_path()) as json_data:
            j_state = json.load(json_data)
        return j_state

    def state_path(self):
        return self.config['actioncam']['log_location'] + '/state.json'

    def state_save(self):
        data = json.dumps(self.state, indent=4)
        with open(self.state_path(), 'w') as outfile:
            outfile.write(data)
        return

    # -- statics ------------------------------------------------
    @staticmethod
    def copy_modus(source_modus, dest_modus):
        for k,v in source_modus.items():
            dest_modus[k] = v
        return dest_modus

    @staticmethod
    def is_different_modus(old, new):
        if old['actioncam'] != new['actioncam']:
            return True
        if old['camera'] != new['camera']:
            return True
        return False

    @staticmethod
    def loop(count=1000000):
        while count >= 0:
            count -= 1
