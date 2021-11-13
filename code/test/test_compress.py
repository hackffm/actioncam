import helper_test

from configuration import Configuration
from local_services import Compress
from helper import Helper

configuration = Configuration('actioncam', path=helper_test.config_path())
helper = Helper(configuration.config)
helper.state_set_start()
debug = True
compress = Compress(configuration, helper, debug)


def test_compress_folder_does_not_exist(configuration, helper):
    print('test_compress_folder_does_not_exist')
    compress.config["compress_location"] = "DoesNotExist"
    compressed = compress.compress()
    assert 'not found' in compressed, "test_compress_folder_does_not_exist failed"


def test_compress(configuration, helper):
    print('test_compress')
    file_test = configuration.config["DEFAULT"]["recording_location"] + "/" + configuration.config["DEFAULT"]["identify"] + "_20211113" + "." + configuration.config["DEFAULT"]["output"]
    helper.file_touch(file_test)
    compressed = compress.compress()
    assert 'zip' in compressed, "test_compress failed as no zip found in reply"
    helper.file_delete(file_test)
    compressed = compress.get_compressed()
    print('Report')
    for cmp in compressed:
        print(cmp)
    assert len(compressed) >= 1, "test_compress failed as not compressed found"


if __name__ == '__main__':
    test_compress(configuration, helper)
    test_compress_folder_does_not_exist(configuration, helper)
