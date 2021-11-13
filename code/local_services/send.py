import fnmatch
import os
import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Send:

    def __init__(self, configuration, helper, debug):
        self.name = 'send'
        self.helper = helper
        self.debug = debug

        self.configuration = configuration
        self.config = configuration.config[self.name]
        self.data_csv = self.config["folder_data"] + '/' + self.name + ".csv"

    def data_load(self):
        if os.path.exists(self.data_csv):
            with open(self.data_csv, 'r') as infile:
                data_loaded = infile.readlines()
            return data_loaded
        else:
            self.log("No Data saved so far")
            return []

    def data_save(self, text):
        if '\n' not in text:
            text = text + '\n'
        with open(self.data_csv, 'a+') as outfile:
            outfile.write(text)

    def files_not_in_data(self, fileslist):
        data_send = self.data_load()
        if len(data_send) > 0:
            for ds in data_send:
                ds = ds.split(";")[2].replace("\n", "")
                if ds in fileslist:
                    fileslist.remove(ds)
            return fileslist
        else:
            return fileslist

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def mail_zip(self, zippath):
        config_mail = self.configuration.config['mail']
        try:
            address_from = config_mail['address_from']
            address_to = config_mail['address_to']
            msg = MIMEMultipart()
            msg['From'] = address_from
            msg['To'] = address_to
            msg['Subject'] = config_mail['subject']
            body = 'see attachment'
            msg.attach(MIMEText(body, 'plain'))

            attachment = open(zippath, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=  %s' % os.path.basename(zippath))
            msg.attach(part)

            self.log('Mail:' + zippath + ' as attachment to ' + address_to)
            if self.helper.is_online(config_mail['server'], config_mail['server_port']):
                server = smtplib.SMTP(config_mail['server'], config_mail['server_port'])
                server.starttls()
                server.login(address_from, str(config_mail['server_password']))
                text = msg.as_string()
                server.sendmail(address_from, address_to, text)
                server.quit()
                return True
            else:
                self.log('Mail:Error:' + str(config_mail['server']) + ':' + str(config_mail['server_port']) + ' is offline')
                return False
        except Exception as e:
            self.log('Mail:Error:' + str(e))
            return False

    def send(self):
        results = []
        for target in self.config["targets"]:
            if target == "mail":
                self.send_to_mail()
            if target == "upload":
                self.send_to_upload()
        return results

    def send_to_mail(self):
        files = os.listdir(self.configuration.config['compress']['compress_location'])
        files = self.valid_file_in_list(files, '*.zip')
        zips = self.files_not_in_data(files)
        if self.debug:
            self.log("Debug: {} Files found {} Files to be send".format(str(len(files)), str(len(zips))))
        for zip_name in zips:
            zippath = self.configuration.config['compress']['compress_location'] + '/' + zip_name
            if self.debug:
                self.log("Debug: send by mail" + zippath)
            if self.mail_zip(zippath):
                self.data_save(self.helper.now_str() + ";mail;" + zip_name)
        return

    def send_to_upload(self):
        files = os.listdir(self.config["recording_location"])
        files = self.valid_file_in_list(files, '*.avi')
        files_upload = self.files_not_in_data(files)
        if self.debug:
            self.log("Debug: {} Files found {} Files to be Uploaded".format(str(len(files)), str(len(files_upload))))
        for file in files_upload:
            _path_file = self.config["recording_location"] + "/" + file
            if self.upload_file(_path_file):
                self.data_save(self.helper.now_str() + ";upload;" + file)
        return

    def upload_file(self, path_file):
        config_upload = self.configuration.config["upload"]
        self.log("Upload:" + os.path.basename(path_file) + " to " + config_upload["url"])
        return True

    def valid_file_in_list(self, files, file_type):
        files_valid = []
        for file_name in files:
            if fnmatch.fnmatch(file_name, file_type):
                files_valid.append(file_name)
        return files_valid