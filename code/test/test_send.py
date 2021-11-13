import json

import helper_test

from configuration import Configuration
from local_services import Send
from helper import Helper

configuration = Configuration('actioncam', path=helper_test.config_path())
helper = Helper(configuration.config)
helper.state_set_start()
debug = True
send = Send(configuration, helper, debug)

def test_send_config():
    print("test_send_config")
    print(json.dumps(send.config, indent=4, sort_keys=True))
    targets = send.config["targets"]
    assert isinstance(targets, list), "Targets is not a List"


def test_send_data_load():
    print("test_data_load")
    q_sended = send.data_load()
    print("\t" + str(len(q_sended)) + " sended Files")


def test_send_send():
    print("test_send_send")
    with open(send.config["folder_data"] + "/mail.json") as json_data:
        j_config = json.load(json_data)
    send.configuration.config["mail"] = j_config
    config_mail = send.configuration.config['mail']
    print(json.dumps(config_mail, indent=4, sort_keys=True))
    send.send()


if __name__ == '__main__':
    test_send_config()
    test_send_data_load()
    test_send_send()
