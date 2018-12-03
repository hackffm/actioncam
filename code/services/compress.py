import datetime
import fnmatch
import os
import zipfile


class Compress:

    def __init__(self, configuration, helper):
        self.config = configuration.config
        self.helper = helper

        self.default = self.config['default']
        self.config_output = self.config[self.default['output']]
        self.name = 'compress'

    def compress(self):
        files = os.listdir(self.config_output['file_location'])
        file_list = self.getfile_list(files)
        if len(file_list) >= 1:
            zipName = self.zip_file_name()
            _zip_created = self.zip_create_files(zipName, self.config_output['file_location'], file_list)
            if _zip_created and (self.config[self.name]['remove_compressed'] == "True"):
                self.removeOldFiles(file_list)
            return zipName + ' ziped'
        else:
            return self.name + ':no new files found to zip'

    def getfile_list(self, folder):
        files = []
        for filename in folder:
            if fnmatch.fnmatch(filename, self.getSearchPattern()):
                self.log('add ' + str(filename) + ' to files')
                files.append(str(filename))
        return files

    def getSearchPattern(self):
        pattern = str(self.default['identify']) + '*' + self.config_output['file_extension']
        return pattern

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def removeOldFiles(self, file_list):
        for file in file_list:
            self.log('remove ' + str(file))
            os.remove(self.config_output['file_location'] + '/' + file)

    def zip_create_files(self, zipname, folder_name, file_list):
        zip = zipfile.ZipFile(zipname, "w")

        for filename in file_list:
            self.log('add ' + folder_name + '/' + filename + ' to ' + zipname)
            zip.write(folder_name + '/' + filename, arcname=filename, compress_type=zipfile.ZIP_DEFLATED)

        zip.close()
        return True

    def zip_file_name(self):
        now_str = self.helper.now_str()
        fName = self.config_output['file_location'] + '/' + now_str + ".zip"
        return fName
