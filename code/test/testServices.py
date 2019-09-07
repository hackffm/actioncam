import helper_test

from config import Configuration
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
config = configuration.config
helper = Helper(configuration)


def test_compress(configuration, helper):
    compress = Compress(configuration, helper)
    compressed = compress.compress()
    print('compressed ' + compressed)


def test_send(configuration, helper):
    send = Send(configuration, helper)
    sended = send.send_mail()
    print('sended ' + sended)
    return


if __name__ == '__main__' and __package__ is None:
    #from local_services import Compress
    #from local_services import Send

    #print(configuration.default_mode())
    #print(configuration.output_folder())
    #print(configuration.previewpattern())
    print(helper.log_home('compress'))
    #test_compress(configuration, helper)
    #test_send(configuration, helper)
