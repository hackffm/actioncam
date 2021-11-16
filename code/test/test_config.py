import json

import helper_test

from configuration import Configuration
from helper import Helper

debug = True
configuration = Configuration('actioncam', path=helper_test.config_path(), debug=debug)
config_actioncam = configuration.config["actioncam"]
helper = Helper(configuration.config)
helper.state_set_start()


def test_config_default():
    print("test_config_default")
    assert configuration.config['DEFAULT'] != "", "Failed checkingd Default"
    print(json.dumps(configuration.config['DEFAULT'], indent=4, sort_keys=True))


def test_config_save():
    print("test_config_save")
    _temp_path = configuration.path_home() + "/temp"
    configuration.config_path = _temp_path + "/test.json"
    assert "test" in configuration.config_path, "Failed setting config test path"
    configuration.save()


def test_config_update():
    print("test_config_update")
    config_actioncam["identify"] = "test"
    assert config_actioncam["identify"] == "test", "Fail setting identify"


if __name__ == '__main__':
    test_config_default()
    test_config_update()
    test_config_save()
