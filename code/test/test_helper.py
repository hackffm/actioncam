import helper_test

from configuration import Configuration
from helper import Helper

configuration = Configuration(name='actioncam', path=helper_test.config_path())
config = configuration.config
helper = Helper(config)


def test_infos():
    print('test_infos')
    infos = helper.infos_self()
    for info in infos:
        print(info)
    assert len(infos) > 1, 'test_infos failed finding infos'


if __name__ == '__main__':
    test_infos()