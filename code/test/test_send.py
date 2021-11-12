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
    print('test_send_config')
    targets = send.config["targets"]
    assert isinstance(targets, list), "Targets is not a List"


def test_send_data():
    print("test_data_load")
    q_sended = send.data_load()
    print(str(len(q_sended)) + " sended Files")


if __name__ == '__main__':
    test_send_config()
    test_send_data()
