import fnmatch
import os
import zipfile


class Compress:

    def __init__(self, configuration, helper,debug=True):
        self.config = configuration.default('compress')
        self.helper = helper
        self.debug = debug

        self.name = 'compress'

    def compress(self):
        if os.path.isdir(self.config["compress_location"]):
            files = os.listdir(self.config["compress_location"])
            file_list = self.getfile_list(files)
            if len(file_list) >= 1:
                zip_name = self.zip_file_name()
                _zip_created = self.zip_create_files(zip_name, self.config["compress_location"], file_list)
                if _zip_created and (self.config[self.name]['remove_compressed'] == "True"):
                    self.remove_old_files(file_list)
                return zip_name + ' zipped'
            else:
                return self.name + ':no new files found to zip'
        else:
            problem = 'configured compress_location {0} not found'.format(self.config["compress_location"])
            self.log(problem)
            return problem

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
            os.remove(self.config["compress_location"] + '/' + file)

    def search_pattern(self):
        pattern = str(self.config['identify']) + '*' + self.config_output['file_extension']
        return pattern

    def zip_create_files(self, zip_name, folder_name, file_list):
        _zip = zipfile.ZipFile(zip_name, "w")
        _rz = zip_name.rfind('/')
        for file_name in file_list:
            file_path = folder_name + '/' + file_name
            _zip.write(file_path, arcname=file_name, compress_type=zipfile.ZIP_DEFLATED)
            self.log('added ' + file_path + ' to ' + zip_name)
        _zip.close()
        return True

    def zip_file_name(self):
        now_str = self.helper.now_str()
        file_name = self.config["compress_location"] + '/' + now_str + ".zip"
        return file_name
