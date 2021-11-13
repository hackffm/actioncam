import time

from local_services import Compress
from local_services import Send


class Servicerunner:

    def __init__(self, l_lock, configuration, default_mode, helper, m_modus):
        self.configuration = configuration
        self.config = self.configuration.config
        self.helper = helper
        self.m_modus = m_modus

        self.compress = Compress(configuration, helper)
        self.current_modus = default_mode
        self.lock = l_lock
        self.name = 'servicerunner'
        self.send = Send(configuration, helper)
        self.send_failed = 0
        self.run()

    def is_idle(self):
        if (self.current_modus['camera'] == self.config['camera']['mode']['pause'] or
           self.current_modus['camera'] == self.config['camera']['mode']['stop']):
            return True
        else:
            return False

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def reset(self, info, _modus):
        if len(info) >= 1:
            self.log(info)
        if 'actioncam' in _modus:
            self.current_modus = _modus
        else:
            self.current_modus = self.configuration.default_mode()
        self.current_modus['idle'] = 0
        self.log('current modus ' + str(self.current_modus))
        return 0

    def run(self):
        idle = 0
        idle_time = self.config[self.name]['idle_time']
        new_modus = {}
        _running = True

        # main loop
        self.log('Start main loop')
        while _running:
            try:
                time.sleep(0.01)
                new_modus = self.helper.dict_copy(self.m_modus, new_modus)
                if self.helper.is_different_modus(self.current_modus, new_modus):
                    self.current_modus = new_modus
                    self.current_modus['idle'] = idle
                    self.log('current modus ' + str(self.current_modus))
                else:
                    pass
            except Exception as e:
                self.log('Error:' + str(e))

            # here we have a decision what can be done during idle time
            if self.is_idle():
                idle += 1
                self.current_modus['idle'] = idle
            if idle >= idle_time and self.is_idle():
                self.log('do work when the rest is idle')
                #
                if self.config['compress']['active'] == "True":
                    self.current_modus['actioncam'] = self.config['mode']['compress']
                    compressed = self.compress.compress()
                    self.log(compressed)
                #
                if self.config['send']['active'] == 'True':
                    self.current_modus['actioncam'] = self.config['mode']['mail_zips']
                    sended = self.send.send_mail()
                    self.log('sended mails ' + str(sended))
                #
                idle = self.reset('give others a chance', self.current_modus)
        # end of main loop

        self.log('End')
        return
