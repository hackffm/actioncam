import os
import sys


file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(file_dir)
utils_dir = os.path.join(parent_dir, 'utils')
services_dir = os.path.join(parent_dir, 'services')
sys.path.append(utils_dir)
sys.path.append(services_dir)
sys.path.append(parent_dir)


def config_path():
    home = os.getenv('HOME')
    c_path = home + '/actioncam/config.json'
    if not os.path.exists(c_path):
        print('failed to find config file in ' + c_path)
        print('see in ../shell/setup for an example')
        sys.exit(1)
    return c_path


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
    from config import Configuration
    from helper import Helper
    from services import Compress
    from services import Send

    configuration = Configuration(config_path=config_path())
    helper = Helper(configuration)

    #print(configuration.default_mode())
    #print(configuration.output_folder())
    #print(configuration.previewpattern())
    #test_compress(configuration, helper)
    test_send(configuration, helper)
