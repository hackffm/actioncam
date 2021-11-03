import helper_test

from config import Configuration
from local_services import Compress
from helper import Helper

configuration = Configuration(config_path=helper_test.config_path())
helper = Helper(configuration)
helper.state_set_start()


def log(text):
    helper.log_add_text('test', text)


def test_compress_folder_does_not_exist(configuration, helper):
    print('test_compress_folder_does_not_exist')
    compress = Compress(configuration, helper)
    compress.config["compress_location"] = "DoesNotExist"
    compressed = compress.compress()
    print('compressed:'+ compressed)
    assert 'not found' in compressed, "test_compress_folder_does_not_exist failed"


def test_compress(configuration, helper):
    print('test_compress')
    compress = Compress(configuration, helper)
    compressed = compress.compress()
    print('compressed:' + compressed)
    assert 'zip' in compressed, "test_compress failed"


if __name__ == '__main__':
    test_compress_folder_does_not_exist(configuration, helper)
    test_compress(configuration, helper)
