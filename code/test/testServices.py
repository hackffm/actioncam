import sys

import helper_test

from config import Configuration
from helper import Helper
from servicerunner import Servicerunner

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)
helper.state_set_start()


def log(text):
    helper.log_add_text('test', text)


def test_compress(configuration, helper):
    compress = Compress(configuration, helper)
    compressed = compress.compress()
    print('test_compress: ' + str(compressed))


def test_send(configuration, helper):
    send = Send(configuration, helper)
    sended = send.send_mail()
    print('sended ' + sended)
    return


def test_servicerunner(configuration, helper):
    log('start test_servicerunner')
    from multiprocessing import Process, Lock
    from multiprocessing import Manager
    l_lock = Lock()
    try:
        with Manager() as manager:
            m_modus = manager.dict()
            p1 = Process(target=Servicerunner, args=(l_lock, configuration, helper, m_modus))
            p1.daemon = True
            p1.start()
    except KeyboardInterrupt:
        log('ending with keyboard interrupt')
        p1.terminate()
        sys.exit()
    except Exception as e:
        log('error in test __main__ ' + str(e))


def test_state():
    print(helper.state_updated())
    print('report all')
    report = helper.report_all()
    print(report)
    for r in report:
        print(r)
    print(helper.report_number_recorded())


if __name__ == '__main__' and __package__ is None:
    from local_services import Compress
    from local_services import Send

    print(configuration.default_mode())
    print(configuration.output_folder())
    print(configuration.previewpattern())
    test_compress(configuration, helper)
    test_send(configuration, helper)
    test_state()
    test_servicerunner(configuration, helper)