import tornado.web
import json


class HandlerConfig(tornado.web.RequestHandler):
    def initialize(self, configuration):
        self.configuration = configuration
        self.config = self.configuration.config
        self.name = self.configuration.name

    def get(self):
        self.write(json.dumps(self.config))

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
        if self.name in _config:
            self.config[self.name]['identify'] = _config[self.name]['identify']
        self.config["DEFAULT"]['mode'] = _config["DEFAULT"]['mode']
        self.config["DEFAULT"]["recording_location"] = _config["DEFAULT"]["recording_location"]
        self.config["camera"]["input"] = _config["camera"]["input"]
        _output = self.config["DEFAULT"]['output']
        self.config[_output]['file_length'] = int(_config[_output]['file_length'])
        self.config['webserver']['server_port'] = int(_config['webserver']['server_port'])