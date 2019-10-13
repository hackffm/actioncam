import os
import sys
import time

from multiprocessing import Process, Queue, Lock
from multiprocessing import Manager

from local_services import Camera
from local_ressources import Configuration
from local_ressources import Database
from local_ressources import Helper
from webserver import WebServer
from servicerunner import Servicerunner
from serv_localhost import ServLocalhost

l_lock = Lock()
q_message = Queue()
m_modus = ''
name = 'actioncam'


def config_path():
    home = os.getenv('HOME')
    c_path = home + '/actioncam/config.json'
    if not os.path.exists(c_path):
        print('failed to find config file in ' + c_path)
        print('see in ../shell/setup for an example')
        sys.exit(1)
    return c_path


def handle_message(msg):
    if msg.startswith('do:'):
        msg = msg[3:]
        if msg == 'shutdown':
            helper.state_save()
            log(msg)
            time.sleep(1.0)
            return False
        if msg == 'start':
            log(msg)
            return True
    elif msg.startswith('camera_mode:'):
        new_modus = msg[12:]
        if configuration.valid_camera_mode(new_modus):
            m_modus['camera'] = new_modus
            log('camera_mode ' + str(new_modus))
        return True
    else:
        log(msg)
        return True


def log(text):
    helper.log_add_text('actioncam', text)


if __name__ == '__main__':
    configuration = Configuration(config_path=config_path())
    helper = Helper(configuration)

    database = Database(configuration, helper)
    logHome = helper.log_home(name)

    running = True
    # start
    handle_message('do:start')
    if logHome == configuration.config['error']:
        print('Error:can not create default log files')
        print('check you config.json')
        sys.exit()

    try:
        with Manager() as manager:
            m_modus = manager.dict()
            m_video = manager.dict()

            helper.dict_copy(configuration.default_mode(), m_modus)
            # start processes
            print('launch DB')
            log('launch DB')
            p1 = Process(target=ServLocalhost, args=(configuration, database, helper))
            p1.daemon = True
            p1.start()
            time.sleep(1.0)
            p2 = Process(target=Servicerunner, args=(l_lock, configuration, helper, m_modus))
            p3 = Process(target=WebServer, args=(l_lock, configuration, helper, q_message, m_modus, m_video))
            p4 = Process(target=Camera, args=(configuration, helper, m_modus, m_video))
            p2.daemon = True
            p3.daemon = True
            p4.daemon = True
            p2.start()
            p3.start()
            p4.start()

            # startup info to console
            helper.state_set_start()
            infos = helper.infos_self()
            print(name, 'running')
            for info in infos:
                print(info)
            print('webserver will listen at port ' + str(configuration.config['webserver']['server_port']))
            print('PID Servicerunner', p1.pid)
            print('PID Webserver', p2.pid)
            print('PID Camera', p3.pid)
            print('PID ServLocalhost', p4.pid)

            # main loop
            while running:
                message = ''
                try:
                    message = q_message.get()
                except Exception as e:
                    log('error in Main loop ' + str(e))
                if message != '':
                    running = handle_message(message)
                if m_modus['actioncam'] == 'do:shutdown':
                    log('shutdown')
            # exit
            sys.exit()
    except KeyboardInterrupt:
        log('ending with keyboard interrupt')
        p1.terminate()
        p2.terminate()
        p3.terminate()
        p4.terminate()
        sys.exit()
    except Exception as e:
        log('error in actioncam __main__ ' + str(e))
