import datetime
import fnmatch
import os
import zipfile


class Compress:

    def __init__(self, configuration, helper,debug=True):
        self.config = configuration.config
        self.helper = helper
        self.debug = debug

        self.default = self.config['default']
        self.config_output = self.config[self.default['output']]
        self.name = 'compress'

    def compress(self):
        files = os.listdir(self.config_output['file_location'])
        file_list = self.getfile_list(files)
        if len(file_list) >= 1:
            zip_name = self.zip_file_name()
            _zip_created = self.zip_create_files(zip_name, self.config_output['file_location'], file_list)
            if _zip_created and (self.config[self.name]['remove_compressed'] == "True"):
                self.remove_old_files(file_list)
            self.helper.data_append(self.name, zip_name)
            return zip_name + ' ziped'
        else:
            return self.name + ':no new files found to zip'

    def getfile_list(self, folder):
        files = []
        for filename in folder:
            if fnmatch.fnmatch(filename, self.search_pattern()):
                self.log('add ' + str(filename) + ' to files')
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

    def zip_create_files(self, zipname, folder_name, file_list):
        _zip = zipfile.ZipFile(zipname, "w")

        for filename in file_list:
            self.log('add ' + folder_name + '/' + filename + ' to ' + zipname)
            _zip.write(folder_name + '/' + filename, arcname=filename, compress_type=zipfile.ZIP_DEFLATED)

        _zip.close()
        return True

    def zip_file_name(self):
        now_str = self.helper.now_str()
        file_name = self.config_output['file_location'] + '/' + now_str + ".zip"
        return file_name
