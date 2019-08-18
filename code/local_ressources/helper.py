import datetime
import fnmatch
import json
import netifaces
import os
import socket
import pandas as pd


class Helper:

    def __init__(self, configuration):
        self.configuration = configuration
        self.config = configuration.config

        self.default = self.config['default']
        self.config_mode = self.config['mode']

        _config_output = self.default['output']
        self.config_output = self.config[_config_output]

        self.state = self.state_start()

    #-- data store--------------------------------------------------------
    def data_home(self,name):
        _config = self.config[name]
        if 'folder_data' in _config:
            return _config['folder_data']
        else:
            return self.config['actioncam']['folder_data']

    def data_append(self, name, what):
        datafolder =  self.data_home(name)
        if self.folder_create_once(datafolder):
            data_store_path = datafolder + '/' + name + '.csv'
            text = self.now_str() + '; ' + str(what)
            with open(data_store_path, 'a') as outfile:
                outfile.write(text + '\n')
        else:
            return self.config['error'] + ' creating store for ' + name

    # < data store--------------------------------------------------------
    def datetime_diff_from_string(self, dt_old):
        dt_now = self.now()
        delta = dt_now - self.datetime_from_string(dt_old)
        delta_seconds = delta.total_seconds()
        return delta_seconds

    def datetime_from_string(self, text):
        return datetime.datetime.strptime(text, self.config_output['file_format_time'])

    def folder_create_once(self, folder_path):
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            return True
        except IOError as e:
            print(e)
            return False

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
        infos.append('port ' + str(self.config['webserver']['server_port']))
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
        if self.folder_create_once(log_home_path):
                return log_home_path
        else:
            return self.config['error'] + ' creating folder for ' + name

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

    def preview_file_number(self):
        previews = self.preview_files()
        return len(previews)

    def preview_files(self):
        output_folder = self.config_output['file_location']
        prev_ext = self.config['preview']['file_extension']
        if output_folder != '':
            pattern = self.configuration.previewpattern()
            if pattern != '':
                files = self.folder_files(output_folder, pattern)
                p_files = []
                for file in files:
                    _date = file.split('_')[2].replace(prev_ext, '')
                    pf = {"name": str(file.replace(prev_ext, '')),
                          "date": _date,
                          "filename": file}
                    p_files.append(pf)
                p_files = sorted(p_files, key=lambda k: k['date'])
                return p_files
            else:
                print('failed get search pattern')
        else:
            print('failed creating preview')

    # -- state --------------------------------------------------
    def state_start(self):
        state = {}
        state['start_dt'] = self.now_str()
        state['start_previews'] = str(self.preview_file_number())
        return state

    def state_updated(self):
        state = self.state_load()
        start_dt = state['start_dt']
        dt_diff = str(self.datetime_diff_from_string(start_dt))
        infos = []
        infos.append('started:' + start_dt)
        infos.append('Now: ' + str(self.now()))
        infos.append('seconds running: ' + dt_diff)
        prev_old = state['start_previews']
        prev_new = self.preview_files()
        infos.append('Previews:' + str(len(prev_new)))
        infos.append('Previews this time:' + str(len(prev_new) - int(prev_old)))
        return infos

    # -- state helper
    def state_load(self):
        with open(self.state_path()) as json_data:
            j_state = json.load(json_data)
        return j_state

    def state_path(self):
        return self.config['actioncam']['folder_data'] + '/state.json'

    def state_save(self):
        data = json.dumps(self.state, indent=4)
        with open(self.state_path(), 'w') as outfile:
            outfile.write(data)
        return

    # -- statics ------------------------------------------------
    @staticmethod
    def copy_modus(source_modus, dest_modus):
        for k, v in source_modus.items():
            dest_modus[k] = v
        return dest_modus

    @staticmethod
    def dict_same_structure(one, two):
        if len(one) != len(two):
            return False
        for item in one:
            if item not in two:
                return False
        return True

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
