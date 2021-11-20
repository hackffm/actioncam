import os
import sys
import time

from multiprocessing import Process, Queue, Lock
from multiprocessing import Manager

from local_ressources import Camera
from local_ressources import Configuration
from local_ressources import Helper
from servicerunner import Servicerunner
from webserver import WebServer

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
            print('shutdown actioncam')
            return False
        if msg == 'start':
            log(msg)
            return True
    elif msg.startswith('camera_mode:'):
        new_modus = msg[12:]
        if new_modus in configuration.config["camera"]["modes"]:
            with l_lock:
                m_modus['camera'] = new_modus
            log('camera_mode ' + str(new_modus))
        return True
    else:
        log(msg)
        return True


def log(text):
    helper.log_add_text('actioncam', text)


if __name__ == '__main__':
    configuration = Configuration(name=name, path=config_path())
    config = configuration.config
    helper = Helper(config)
    log_location = config[name]['log_location']

    debug = config['debug']
    print('debug is ' + str(debug))
    default_mode = {"actioncam": config['DEFAULT']['mode'],
                     "camera": config['camera']['modes']['pause'],
                     "idle": 0}
    running = True

    # start
    handle_message('do:start')

    try:
        with Manager() as manager:
            m_modus = manager.dict()
            m_video = manager.dict()

            helper.dict_copy(default_mode, m_modus)
            p2 = Process(target=Servicerunner, args=(l_lock, configuration, default_mode, helper, m_modus))
            p3 = Process(target=WebServer, args=(l_lock, configuration, helper, q_message, m_modus, m_video))
            p4 = Process(target=Camera, args=(l_lock, configuration, default_mode, helper, m_modus, m_video))
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
            print('PID Servicerunner', p2.pid)
            print('PID Webserver', p3.pid)
            print('PID Camera', p4.pid)

            # main loop
            while running:
                message = ''
                try:
                    message = q_message.get()
                    if debug:
                        print("actioncam:message:" + message)
                    if message != '':
                        running = handle_message(message)
                    if m_modus['actioncam'] == 'do:shutdown':
                        log('shutdown')
                except Exception as e:
                    log('error in Main loop ' + str(e))
            # exit
            sys.exit()
    except KeyboardInterrupt:
        log('ending with keyboard interrupt')
        p2.terminate()
        p3.terminate()
        p4.terminate()
        sys.exit()
    except Exception as e:
        log('error in actioncam __main__ ' + str(e))
        print('error in actioncam __main__ ' + str(e))
