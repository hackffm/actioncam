import fnmatch
import os
import requests
import zipfile


class Compress:

    def __init__(self, configuration, helper,debug=True):
        self.config = configuration.config
        self.helper = helper
        self.debug = debug

        self.default = self.config['default']
        self.config_output = self.config[self.default['output']]
        self.db_web = 'http://localhost:8081/database'
        self.failed = 'failed'
        self.name = 'compress'

    def compress(self):
        files = os.listdir(self.config_output['file_location'])
        file_list = self.getfile_list(files)
        file_list = self.not_compressed(file_list)
        if file_list == self.failed:
            return self.failed
        if len(file_list) >= 1:
            zip_name = self.zip_file_name()
            _zip_created = self.zip_create_files(zip_name, self.config_output['file_location'], file_list)
            if _zip_created and (self.config[self.name]['remove_compressed'] == "True"):
                self.remove_old_files(file_list)
            return zip_name + ' zipped'
        else:
            return self.name + ':no new files found to zip'

    def db_query_compressed(self):
        self.log('db query compressed')
        result = []
        try:
            headers = {
                'content-type': 'application/json',
                'Accept-Charset': 'UTF-8'
            }
            data = '{"query": {"compressed": "None"}}'
            response = requests.get(self.db_web, headers=headers, data=data)
            _t = response.text
            _t = _t.replace(' ', '')
            _t = _t.replace('[','')
            _t = _t.replace(']', '')
            _t = _t.replace('"', '')
            _t = _t.replace("'", "")
            result = _t.split(',')
        except Exception as e:
            self.log(str(e))
        return result

    def db_add_compressed(self, compress):
        self.log('db add compressed ' + compress)
        response = []
        try:
            headers = {
                'content-type': 'application/json',
                'Accept-Charset': 'UTF-8'
            }
            data = '{"add": {"compressed": "' + compress + '"}}'
            response = requests.post(self.db_web, headers=headers, data=data)
        except Exception as e:
            self.log(str(e))
            return self.failed
        return response.text

    def db_add_compressed2recording(self, compress, recording):
        self.log('db add compressed2recording ' + compress + ',' + recording)
        response = []
        try:
            headers = {
                'content-type': 'application/json',
                'Accept-Charset': 'UTF-8'
            }
            data = '{"add": {"compressed2recording": ["' + compress + '","' + recording +'"]}}'
            response = requests.post(self.db_web, headers=headers, data=data)
        except Exception as e:
            self.log(str(e))
            return self.failed
        return response.text

    def not_compressed(self, all_files):
        _compressed = self.db_query_compressed()
        for c in _compressed:
            for af in all_files:
                if c in af:
                    all_files.remove(af)
        return all_files

    def getfile_list(self, folder):
        files = []
        for filename in folder:
            if fnmatch.fnmatch(filename, self.search_pattern()):
                files.append(str(filename))
        return files

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def remove_old_files(self, file_list):
        for file in file_list:
            self.log('remove ' + str(file))
            os.remove(self.config_output['file_location'] + '/' + file)

    def search_pattern(self):
        pattern = str(self.default['identify']) + '*' + self.config_output['file_extension']
        return pattern

    def zip_create_files(self, zip_name, folder_name, file_list):
        _zip = zipfile.ZipFile(zip_name, "w")
        _rz = zip_name.rfind('/')
        db_result = self.db_add_compressed(zip_name[_rz+1:])
        if self.failed == db_result:
            self.log('db_add_compressed failed with ' + str(db_result))
        for file_name in file_list:
            file_path = folder_name + '/' + file_name
            _zip.write(file_path, arcname=file_name, compress_type=zipfile.ZIP_DEFLATED)
            self.log('added ' + file_path + ' to ' + zip_name)
            db_result = self.db_add_compressed2recording(zip_name[_rz+1:], file_name)
            if self.failed == db_result:
                _zip.close()
                return False
        _zip.close()
        return True

    def zip_file_name(self):
        now_str = self.helper.now_str()
        file_name = self.config_output['file_location'] + '/' + now_str + ".zip"
        return file_name
