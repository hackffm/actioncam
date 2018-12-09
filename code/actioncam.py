import os
import threading
import sys

from multiprocessing import Process, Queue, Lock
from multiprocessing import Manager

from services import Camera
from utils import Configuration
from utils import Helper
from services import HumanInterface
from webserver import WebServer
from servicerunner import Servicerunner

l_lock = Lock()
q_message = Queue()
m_modus = ''
name = 'actioncam'

configuration = Configuration()
helper = Helper(configuration)
logHome = helper.log_home(name)
running = True


def handle_message(msg):
    if msg.startswith('do:'):
        msg = msg[3:]
        if msg == 'shutdown':
            log(msg)
            return False
        if msg == 'start':
            log(msg)
            return True
    elif msg.startswith('camera_mode:'):
        new_modus = msg[12:]
        if new_modus in configuration.config['camera']['mode']:
            m_modus['camera'] = new_modus
            log('camera_mode ' + str(new_modus))
        return True
    else:
        log(msg)
        return True


def log(text):
    helper.log_add_text('actioncam', text)


if __name__ == '__main__':
    handle_message('do:start')
    if logHome == configuration.config['error']:
        print('Error:can not create default log files')
        log('can not create default log files')
        sys.exit()
        
    try:
        with Manager() as manager:
            m_modus = manager.dict()
            m_video = manager.dict()

            helper.copy_modus(configuration.default_mode(), m_modus)
            # start processes
            p1 = Process(target=Servicerunner, args=(l_lock, configuration, helper, q_message, m_modus))
            p2 = Process(target=WebServer, args=(l_lock, configuration, helper, q_message, m_modus, m_video))
            p3 = Process(target=Camera, args=(configuration, helper, m_modus, m_video))
            p1.daemon = True
            p2.daemon = True
            p3.daemon = True
            p1.start()
            p2.start()
            p3.start()

            '''
            add hid hardware if on raspberry
            current_dir = os.path.dirname(__file__)
            utils_path = './utils/'
            thread_hi = threading.Thread(target=HumanInterface, args=(utils_path,))
            thread_hi.setDaemon(True)
            thread_hi.start()
            '''

            # startup info to console
            infos = helper.infos_self()
            print(name, 'running')
            for info in infos:
                print(info)
            print('PID Servicerunner', p1.pid)
            print('PID Webserver', p2.pid)
            print('PID Camera', p3.pid)


            # main loop
            while running:
                message = ''
                try:
                    message = q_message.get()
                except Exception as e:
                    log('error in Main loop ' + str(e))
                if message != '':
                    running = handle_message(message)
                # helper.loop()
            # exit
            handle_message('actioncam terminating')
            sys.exit()
    except KeyboardInterrupt:
        log('ending with keyboard interrupt')
        p1.terminate()
        p2.terminate()
        p3.terminate()
        sys.exit()
    except Exception as e:
        log('error in actioncam __main__ ' + str(e))
