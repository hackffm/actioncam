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

        self.config = configuration.config[self.name]
        self.data_csv = self.config["folder_data"] + '/' + self.name + ".csv"

    def data_load(self):
        if os.path.exists(self.data_csv):
            with open(self.data_csv, 'r') as infile:
                data_loaded = infile.read()
                return data_loaded
        else:
            return []

    def data_save(self, text):
        if '\n' not in text:
            text = text + '\n'
        with open(self.data_csv, 'a+') as outfile:
            outfile.write(text)

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def zips_not_send(self, ziplist):
        q_sended = self.data_load()
        if len(q_sended) > 0:
            for zipname in q_sended:
                if zipname.split(";")[1] in ziplist:
                    ziplist.remove(zipname)
            return ziplist
        else:
            return []

    def zips_in_folder(self, folder_name):
        zip_files = []
        for file_name in folder_name:
            if fnmatch.fnmatch(file_name, '*.zip'):
                zip_files.append(file_name)
        return zip_files

    def send_zip_by_mail(self, zippath):
        msg = MIMEMultipart()
        config_mail = self.config['mail']
        try:
            address_from = config_mail['address_from']
            address_to = config_mail['address_to']
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

            self.log('sending ' + zippath + ' as mail attachment to ' + address_from)
            if self.helper.is_online(config_mail['server'], config_mail['server_port']):
                server = smtplib.SMTP(config_mail['server'], config_mail['server_port'])
                server.starttls()
                server.login(address_from, str(config_mail['server_password']))
                text = msg.as_string()
                server.sendmail(address_from, address_to, text)
                server.quit()
                return True
            else:
                self.log('mail server ' + str(config_mail['server']) + ':' +
                         str(config_mail['server_port']) + ' is offline')
                return False
        except Exception as e:
            self.log('send_zip_by_mail failed with ' + str(e))
            return False

    def send_zips(self, zips):
        self.log('send_zips')
        for zip_name in zips:
            zippath = self.config['folder_data'] + '/' + zip_name
            if self.send_zip_by_mail(zippath):
                zipsize = os.path.getsize(zippath) / 1024
                self.data_save(self.helper.now_str() + ";" + os.path.basename(zippath) + ";" + zipsize)
            else:
                self.log('failed to sending ' + zippath)
        return 'done'

    def send_mail(self):
        files = os.listdir(self.config['recording_location'])
        zips = self.zips_in_folder(files)
        zips = self.zips_not_send(zips)
        if len(zips) >= 1:
            result = self.send_zips(zips)
            return 'send_mail:' + result
        else:
            return 'send_mail:no new zip files'
