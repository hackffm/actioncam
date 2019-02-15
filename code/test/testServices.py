import os.path as path
import sys


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
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from config import Configuration
    from helper import Helper
    from services import Compress
    from services import Send

    configuration = Configuration()
    helper = Helper(configuration)

    #print(configuration.default_mode())
    #print(configuration.output_folder())
    print(configuration.previewpattern())
    #testCompress(configuration, helper)
    #testSend(configuration, helper)
