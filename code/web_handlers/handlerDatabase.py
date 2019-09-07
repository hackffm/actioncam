import tornado.web
import json


class HandlerDatabase(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.config = self.configuration.config

    def get(self):
        self.write('not implemented')

    def post(self, *args):
        #_execute = tornado.escape.json_decode(self.request.body)
        _result = self.sql_execute('')
        self.write(_result)
        self.finish()

    def sql_execute(self, sql_command):
        return 'executed'