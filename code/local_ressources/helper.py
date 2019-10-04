import datetime
import fnmatch
import json
import netifaces
import os
import socket
import requests


class Helper:

    def __init__(self, configuration):
        self.configuration = configuration
        self.config = configuration.config

        self.default = self.config['default']
        self.config_mode = self.config['mode']

        _config_output = self.default['output']
        self.config_output = self.config[_config_output]

        self.state = self.state_default()

    def datetime_diff_from_string(self, dt_string):
        dt_now = self.datetime_from_string(self.now())
        dt_old = self.datetime_from_string(dt_string)
        delta = dt_now - dt_old
        delta_seconds = delta.total_seconds()
        return delta_seconds

    def datetime_from_string(self, text):
        dt = ''
        try:
            dt = datetime.datetime.strptime(text, self.config_output['file_format_time'])
        except ValueError:
            dt = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            self.log_add_text('actioncam', 'Error' + str(e))
        return dt

    def file_exists(self, path_file):
        if not os.path.isfile(path_file):
            return False
        return True

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

    def is_online(self, REMOTE_SERVER, PORT):
        try:
            host = socket.gethostbyname(REMOTE_SERVER)
            s = socket.create_connection((host, PORT), 2)
            return True
        except:
            return False

    def log_add_text(self, name, text):
        l_home = self.log_home(name)
        text = self.now_str() + ': ' + text
        with open(l_home, 'a') as outfile:
            outfile.write(text + '\n')

    def log_home(self, name):
        _config = self.default
        _log_location = _config['log_location']
        _log_file = _config['log_file']
        if name in self.config:
            _config = self.config[name]
        if 'log_location' in _config:
            _log_location = _config['log_location']
        if 'log_file' in _config:
            _log_file = _config['log_file']
        log_home_path = _log_location + '/' + _log_file
        self.folder_create_once(_log_location)
        return log_home_path

    def not_local(self, ip):
        if ip != '127.0.0.1':
            return True
        return False

    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def now_str(self):
        return datetime.datetime.now().strftime(self.config_output['file_format_time'])

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
    def state_default(self):
        state = {}
        state['date_start'] = self.now()
        state['mode'] = self.config['default']['mode']
        state['previews_start'] = str(self.preview_file_number())
        return state

    def state_updated(self):
        state = self.state_load()
        date_start = str(state['date_start'])
        #dt_diff =  self.datetime_delta_to_string(date_start)
        dt_diff = str(self.datetime_diff_from_string(date_start))
        dt_diff = float(dt_diff)
        if dt_diff > 60.0:
            dt_diff = dt_diff / 60.0
            dt_diff = str("{:.2f}".format(dt_diff))
            dt_diff = dt_diff + " min"
        else:
            dt_diff = str(dt_diff)
        infos = []
        infos.append('started:' + date_start)
        infos.append('Now: ' + str(self.now()))
        infos.append('seconds running: ' + dt_diff)
        prev_old = state['previews_start']
        prev_new = self.preview_files()
        infos.append('Previews:' + str(len(prev_new)))
        infos.append('Previews this time:' + str(len(prev_new) - int(prev_old)))
        self.log_add_text('helper', 'stated updated:' + str(infos))
        return infos

    def state_load(self):
        try:
            data = '{"query": {"state": "None"}}'
            response = requests.get(self.config['database']['url'], headers=self.config['database']['headers'], data=data)
            _t = response.text
            _j = json.loads(_t)
            return _j
        except Exception as e:
            self.log_add_text('helper', str(e))

    def state_save(self):
        try:
            data = '{"put": {"state":' + str(json.dumps(self.state)) + '}}'
            response = requests.put(self.config['database']['url'], self.config['database']['headers'], data=data)
            self.log_add_text('helper', str(response.text))
            self.log_add_text('helper', 'saved state ' + str(self.state))
            return
        except Exception as e:
            self.log_add_text('helper', str(e))

    def state_set_start(self):
        self.state['date_start'] = self.now_str()
        self.state_save()

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
