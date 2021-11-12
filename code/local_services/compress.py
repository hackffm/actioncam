import fnmatch
import os
import zipfile


class Compress:

    def __init__(self, configuration, helper, debug=False):
        self.name = 'compress'
        self.helper = helper
        self.debug = debug

        self.config = configuration.config[self.name]
        self.data_csv = self.config["folder_data"] + '/' + self.name + ".csv"

    def compress(self):
        check = self.folders_checked()
        if check == 'checked':
            files = os.listdir(self.config["recording_location"])
            file_list = self.get_valid_files(files)
            if len(file_list) >= 1:
                zip_name = self.zip_file_name()
                _zip_created = self.zip_create_files(zip_name, self.config["recording_location"], file_list)
                if _zip_created and (self.config['remove_compressed'] == "True"):
                    self.remove_old_files(file_list)
                return zip_name + ' zipped'
            else:
                return self.name + ':no new files found to zip'
        else:
            return check

    def data_load(self):
        if os.path.exists(self.data_csv):
            with open(self.data_csv, 'r') as infile:
                data_loaded = infile.read()
                return data_loaded
        else:
            return ''

    def data_save(self, text):
        if not '\n' in text:
            text = text + '\n'
        with open(self.data_csv, 'a+') as outfile:
            outfile.write(text)

    def folders_checked(self):
        if os.path.isdir(self.config["recording_location"]):
            if self.debug:
                self.log(self.config["recording_location"] + ' found')
        else:
            problem = 'configured recording_location {0} not found'.format(self.config["recording_location"])
            self.log(problem)
            return problem
        if os.path.isdir(self.config["compress_location"]):
            if self.debug:
                self.log(self.config["compress_location"] + ' found')
        else:
            problem = 'configured recording_location {0} not found'.format(self.config["compress_location"])
            self.log(problem)
            return problem
        return 'checked'

    def get_compressed(self):
        data_saved = self.data_load()
        data_saved = data_saved.split('\n')
        compressed = []
        for ds in data_saved:
            _ds = ds.split(";")
            if len(_ds) == 3:
                compressed.append(_ds)
        return compressed

    def get_valid_files(self, all_files):
        files = []
        data_saved = self.data_load()
        for filename in all_files:
            if filename not in data_saved:
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
        pattern = str(self.config['identify']) + '*' + self.config['output']
        return pattern

    def zip_create_files(self, zip_name, folder_name, file_list):
        _zip = zipfile.ZipFile(zip_name, "w")
        _rz = zip_name.rfind('/')
        for file_name in file_list:
            file_path = folder_name + '/' + file_name
            _zip.write(file_path, arcname=file_name, compress_type=zipfile.ZIP_DEFLATED)
            self.log('added ' + file_path + ' to ' + zip_name)
            self.data_save(self.helper.now_str() + ";" + os.path.basename(file_path) + ";" + os.path.basename(zip_name))
        _zip.close()
        return True

    def zip_file_name(self):
        now_str = self.helper.now_str()
        file_name = self.config["compress_location"] + '/' + now_str + ".zip"
        return file_name
