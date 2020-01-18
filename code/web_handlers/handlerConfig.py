import tornado.web
import json


class HandlerConfig(tornado.web.RequestHandler):
    def initialize(self, configuration):
        self.configuration = configuration
        self.config = self.configuration.config

    def get(self):
        config = self.configuration.config
        self.write(json.dumps(config))

    def post(self, *args):
        _config = tornado.escape.json_decode(self.request.body)
        if type(_config) == dict:
            self.assign_config(_config)
            self.configuration.save()
            self.write(json.dumps({'status': 'ok'}))
        else:
            self.write(json.dumps({'status': 'failed'}))
        self.finish()

    def assign_config(self, _config):
        self.config['default']['identify'] = _config['default']['identify']
        self.config['default']['mode'] = _config['default']['mode']
        self.config["default"]["recording_location"] = _config["default"]["recording_location"]
        self.config["camera"]["input"] = _config["camera"]["input"]
        _output = self.config['default']['output']
        self.config[_output]['file_length'] = int(_config[_output]['file_length'])
        self.config['mail']['address_from'] = _config['mail']['address_from']
        self.config['mail']['address_to'] = _config['mail']['address_to']
        self.config['mail']['server'] = _config['mail']['server']
        self.config['mail']['server_password'] = _config['mail']['server_password']
        self.config['mail']['server_port'] = int(_config['mail']['server_port'])
        self.config['webserver']['server_port'] = int(_config['webserver']['server_port'])