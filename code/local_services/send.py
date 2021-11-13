import fnmatch
import os
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

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def send(self):
        results = []
        for target in self.config["targets"]:
            if target == "mail":
                _path_compressed = self.configuration.config['compress']['compress_location']
                files = os.listdir(_path_compressed)
                zips = self.zips_in_folder(files)
                zips = self.zips_not_send(zips)
                if self.debug:
                    self.log("Debug: {} Files found {} Files to be send".format(str(len(files)), str(len(zips))))
                for zip_name in zips:
                    zippath = _path_compressed + '/' + zip_name
                    if self.debug:
                        self.log("Debug: send by mail" + zippath)
                    if self.send_to_mail(zippath):
                        self.data_save(self.helper.now_str() + ";mail;" + zip_name)
        return results

    def send_to_mail(self, zippath):
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

            self.log('sending ' + zippath + ' as mail attachment to ' + address_to)
            if self.helper.is_online(config_mail['server'], config_mail['server_port']):
                server = smtplib.SMTP(config_mail['server'], config_mail['server_port'])
                server.starttls()
                server.login(address_from, str(config_mail['server_password']))
                text = msg.as_string()
                server.sendmail(address_from, address_to, text)
                server.quit()
                return True
            else:
                self.log('Error:' + str(config_mail['server']) + ':' + str(config_mail['server_port']) + ' is offline')
                return False
        except Exception as e:
            self.log('send_zip_by_mail failed with ' + str(e))
            return False

    def zips_not_send(self, ziplist):
        q_sended = self.data_load()
        if len(q_sended) > 0:
            for zipname in q_sended:
                zipname = zipname.split(";")[2].replace("\n","")
                if zipname in ziplist:
                    ziplist.remove(zipname)
            return ziplist
        else:
            return ziplist

    def zips_in_folder(self, folder_name):
        zip_files = []
        for file_name in folder_name:
            if fnmatch.fnmatch(file_name, '*.zip'):
                zip_files.append(file_name)
        return zip_files