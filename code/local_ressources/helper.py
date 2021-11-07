import datetime
import fnmatch
import json
import netifaces
import os
import socket


class Helper:

    def __init__(self, config):
        self.config = config

        self.default = self.config['DEFAULT']
        self.config_mode = self.config['mode']
        self.state_file = self.default["folder_data"] + "/" + self.default["state_file"]

        _config_output = self.default['output']
        self.config_output = self.config[_config_output]

        self.headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
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
            self.log_add_text('actioncam', 'Error[Helper]' + str(e))
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
            self.log_add_text('actioncam', 'Error[Helper]' + str(e))
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
        if name not in self.config:
            name = self.config['DEFAULT']['name']
        l_home = self.log_home(name)
        text = self.now_str() + ': ' + name + ':' + str(text)
        with open(l_home, 'a') as outfile:
            outfile.write(text + '\n')

    def log_home(self, name):
        if name not in self.config:
            name = self.config['DEFAULT']['name']
        log_home_path = self.config[name]['log_location'] + '/' + self.config[name]['log_file']
        self.folder_create_once(self.config[name]['log_location'] )
        return log_home_path

    def not_local(self, ip):
        if ip != '127.0.0.1':
            return True
        return False

    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def now_str(self):
        return datetime.datetime.now().strftime(self.config_output['file_format_time'])

    # -- state --------------------------------------------------
    def state_default(self):
        state = {}
        state['date_start'] = self.now()
        state['mode'] = self.config['DEFAULT']['mode']
        state['previews_start'] = 0
        return state

    def state_updated(self):
        try:
            state = self.state_load()
            date_start = str(state['date_start'])
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
            self.log_add_text('helper', 'state_updated:' + str(infos))
            return infos
        except Exception as e:
            self.log_add_text('helper', 'state_updated:' +str(e))
            return []

    def state_load(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file) as json_data:
                    j_state = json.load(json_data)
                self.state = j_state
            else:
                self.log_add_text('helper','stata_load:error:can not find ' + self.state_file)
        except Exception as e:
            self.log_add_text('helper', str(e))
        return self.state

    def state_save(self):
        try:
            data = json.dumps(self.state, indent=4)
            with open(self.state_file, 'w') as outfile:
                outfile.write(data)
            return self.state
        except Exception as e:
            self.log_add_text('helper', 'state_save:error:' + str(e))

    def state_set_start(self):
        self.state['date_start'] = str(self.now())
        self.state_save()

    # -- statics ------------------------------------------------
    def dict_copy(self, source_modus, dest_modus):
        if not isinstance(source_modus,dict):
            try:
                source_modus = dict(source_modus)
            except Exception as e:
                self.log_add_text('helper', str(e))
                return {}
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
    def is_online(_host, _port):
        try:
            host = socket.gethostbyname(_host)
            s = socket.create_connection((host, _port), 2)
            return True
        except:
            return False

    @staticmethod
    def loop(count=1000000):
        while count >= 0:
            count -= 1
