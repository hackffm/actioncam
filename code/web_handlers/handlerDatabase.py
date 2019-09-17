import tornado.web
import json


class HandlerDatabase(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.config = self.configuration.config
        self.helper = helper
        self.name = 'HandlerDatabase'

    def get(self):
        self.log('get called')
        self.write('not implemented')

    def post(self, *args):
        execute = tornado.escape.json_decode(self.request.body)
        _result = self.sql_execute(execute)
        self.write(_result)
        self.finish()

    # ----------------------------------------------------------
    def log(self, text):
        self.helper.log_add_text(self.name, self.name + ':' + text)

    def sql_execute(self, sql_command):
        print('sql was ' + str(sql_command))
        return 'executed'