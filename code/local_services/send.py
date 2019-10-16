import fnmatch
import os
import requests
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Send:

    def __init__(self, configuration, helper):
        self.config = configuration.config
        self.default = self.config['default']

        self.config_mail = self.config['mail']
        self.config_mode = self.config['mode']
        self.failed = self.config['failed']
        self.helper = helper
        self.mode = self.default['mode']
        self.name = 'send'

        _config_output = self.default['output']
        self.config_output = self.config[_config_output]

    def db_add_send(self, compress, size, date):
        self.log('db add send ' + compress + ',' + date)
        response = []
        try:
            data = '{"add": { "send": {"compressed": "' + compress + '", "size": "' + size
            data = data + '", "mail": "' + self.config_mail['address_to'] + '", "date": "' + str(date) + '" }}}'
            response = requests.post(self.config['database']['url'], headers=self.config['database']['headers'], data=data)
        except Exception as e:
            self.log('db_add_send:' + str(e))
            return self.failed
        return response.text

    def db_query_send(self):
        self.log('db query send')
        result = []
        try:
            data = '{"query": {"send": "None"}}'
            response = requests.get(self.config['database']['url'], headers=self.config['database']['headers'], data=data)
            _t = response.text
            _t = _t.replace(' ', '')
            _t = _t.replace('[', '')
            _t = _t.replace(']', '')
            _t = _t.replace('"', '')
            _t = _t.replace("'", "")
            result = _t.split(',')
        except Exception as e:
            self.log('db_query_send:' + str(e))
            return self.failed
        return result

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def zips_not_send(self, ziplist):
        q_sended = self.db_query_send()
        if q_sended != self.failed:
            for zipname in q_sended:
                if zipname in ziplist:
                    ziplist.remove(zipname)
            return ziplist
        else:
            return self.failed

    def zips_in_folder(self, folder_name):
        zip_files = []
        for file_name in folder_name:
            if fnmatch.fnmatch(file_name, '*.zip'):
                zip_files.append(file_name)
        return zip_files

    def send_zip_by_mail(self, zippath):
        msg = MIMEMultipart()
        try:
            address_from = self.config_mail['address_from']
            address_to = self.config_mail['address_to']
            msg['From'] = address_from
            msg['To'] = address_to
            msg['Subject'] = self.config_mail['subject']
            body = 'see attachment'
            msg.attach(MIMEText(body, 'plain'))

            attachment = open(zippath, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=  %s' % os.path.basename(zippath))
            msg.attach(part)

            self.log('sending ' + zippath + ' as mail attachment to ' + address_from)
            if self.helper.is_online(self.config_mail['server'], self.config_mail['server_port']):
                server = smtplib.SMTP(self.config_mail['server'], self.config_mail['server_port'])
                server.starttls()
                server.login(address_from, str(self.config_mail['server_password']))
                text = msg.as_string()
                server.sendmail(address_from, address_to, text)
                server.quit()
                return True
            else:
                self.log('mail server ' + str(self.config_mail['server']) + ':' + str(self.config_mail['server_port'])
                         + ' is offline')
                return False
        except Exception as e:
            self.log('send_zip_by_mail failed with ' + str(e))
            return False

    def send_zips(self, zips):
        self.log('send_zips')
        for zip_name in zips:
            zippath = self.config_output['file_location'] + '/' + zip_name
            if self.send_zip_by_mail(zippath):
                zipsize = os.path.getsize(zippath) / 1024
                now_str = self.helper.now_str()
                self.db_add_send(self, str(zip_name), str(zipsize), str(now_str))
            else:
                self.log('failed to sending ' + zippath)
                return self.failed
        return 'done'

    def send_mail(self):
        files = os.listdir(self.config_output['file_location'])
        zips = self.zips_in_folder(files)
        zips = self.zips_not_send(zips)
        if len(zips) >= 1 and zips != self.failed:
            result = self.send_zips(zips)
            return 'send_mail:' + result
        else:
            return 'send_mail:no new zip files'
