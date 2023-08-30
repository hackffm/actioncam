import json

import helper_test

from configuration import Configuration
from helper import Helper

debug = True
configuration = Configuration(name='actioncam', path=helper_test.config_path(), debug=debug)
config = configuration.config
helper = Helper(config)


def test_helper_infos():
    print('test_infos')
    infos = helper.infos_self()
    for info in infos:
        print(info)
    assert len(infos) > 1, 'test_infos failed finding infos'


def test_helper_loghome():
    print("test_helper_loghome")
    log_good = helper.log_home("actioncam")
    print("actioncam log home is " + log_good)
    log_bad = helper.log_home("DOESNOTEXIST")
    print("all other log home is also " + log_bad)
    assert log_good == log_bad, "Failed getting valid Loghome for unknown section"


def test_helper_log_ad_text():
    print("test_helper_log_ad_text")
    helper.log_add_text('coroutine', 'ws modus updated Error:Test')


def test_helper_dict_copy():
    print("test_helper_dict_copy")
    t_dict = {'actioncam': 'pause', 'camera': 'pause', 'idle': 0}
    t_new = {}
    helper.dict_copy(t_dict, t_new)
    if debug:
        print(json.dumps(t_new, indent=4))
    assert t_dict == t_new


def test_helper_dict_is_different():
    print("test_helper_dict_is_different")
    current_modus = {}
    new_modus = {'actioncam': 'pause', 'camera': 'pause', 'idle': 0}
    changed_modus = {'actioncam': 'stop', 'camera': 'pause', 'idle': 0}
    assert helper.is_different_modus(current_modus, new_modus) is True, "test_helper_dict_is_different failed comparing"
    assert helper.is_different_modus(current_modus, changed_modus) is True, "test_helper_dict_is_different failed comparing"
    assert helper.is_different_modus(new_modus, new_modus) is False, "test_helper_dict_is_different failed comparing"


if __name__ == '__main__':
    test_helper_infos()
    test_helper_loghome()
    test_helper_log_ad_text()
    test_helper_dict_copy()
    test_helper_dict_is_different()
