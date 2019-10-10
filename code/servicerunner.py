import time

from local_services import Compress
from local_services import Send


class Servicerunner:

    def __init__(self, l_lock, configuration, helper, m_modus):
        self.configuration = configuration
        self.config = self.configuration.config
        self.helper = helper
        self.m_modus = m_modus

        self.compress = Compress(configuration, helper)
        self.current_modus = self.configuration.default_mode()
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
        self.helper.log_add_text('servicerunner', text)

    def reset(self, info, _modus):
        if len(info) >= 1:
            self.log(info)
        if 'actioncam' in _modus:
            self.current_modus = _modus
        else:
            self.current_modus = self.configuration.default_mode()
        self.log('current modus ' + str(self.current_modus))
        return 0

    def run(self):
        self.log('Start servicerunner')
        # prepare running loop
        idle = 0
        idle_time = self.config['servicerunner']['idle_time']
        new_modus = {}
        _running = True

        # main loop
        while _running:
            try:
                new_modus = self.helper.dict_copy(self.m_modus, new_modus)
                if self.helper.is_different_modus(self.current_modus, new_modus):
                    self.current_modus = new_modus
                    self.current_modus['idle'] = idle
                    self.log('current modus ' + str(self.current_modus))
                else:
                    pass
            except Exception as e:
                # sometimes empty errors here
                pass

            # run services if idle
            if self.current_modus['actioncam'] == self.config['mode']['compress'] and self.is_idle():
                compressed = self.compress.compress()
                idle = self.reset(compressed)
            if self.current_modus['actioncam'] == self.config['mode']['mail_zips'] and self.is_idle():
                if self.send_failed == 0:
                    sended = self.send.send_mail()
                    if sended == 'send_mail:no new zip files':
                        sended = ''
                        idle = self.reset(sended, self.current_modus)
                    if sended == 'send_mail:failed':
                        self.send_failed = 10
                else:
                    self.send_failed -= 1

            # all other services must be idle when camera is recording
            if self.current_modus['camera'].startswith('record'):
                idle = 0

            # maintenance
            if self.is_idle():
                idle += 1
                self.current_modus['idle'] = idle
            if idle >= idle_time and self.is_idle():
                if self.config['compress'] == "True":
                    self.current_modus['actioncam'] = self.config['mode']['compress']
                    self.log('compress start')
                else:
                    with self.lock:
                        idle = self.reset('[servicerunner]compress disabled', self.current_modus)
            time.sleep(0.01)
            # end of servicerunner loop

        self.log('End')
        return
