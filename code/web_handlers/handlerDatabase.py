import tornado.web
import json


class HandlerDatabase(tornado.web.RequestHandler):
    def initialize(self, configuration, database, helper):
        self.configuration = configuration
        self.config = self.configuration.config
        self.database = database
        self.executed = 'executed'
        self.helper = helper
        self.name = 'HandlerDatabase'

    def get(self):
        query = self.get_arguments('query')
        query = str(query)
        self.log(query)
        self.write('done')

    def post(self, *args):
        try:
            db_command = tornado.escape.json_decode(self.request.body)
            _result = self.database_insert(db_command)
            self.write(_result)
        except Exception as e:
            self.log(str(e))
            self.write('failed')
        self.finish()

    # ----------------------------------------------------------
    def log(self, text):
        self.helper.log_add_text(self.name, self.name + ':' + text)

    def database_insert(self, db_command):
        self.log('insert:' + str(db_command))
        result = self.executed
        if 'add' in db_command:
            _command = db_command['add']
            if 'recording' in _command:
                result = self.database.add_recording(_command['recording'])
            if 'compressed' in _command:
                result = self.database.add_compressed(_command['compressed'])
        return str(result)

    def database_query(self, db_command):
        self.log('query:' + str(db_command))
        result = self.executed
        if 'query'in db_command:
            _command = db_command['query']
            if 'recording' in _command:
                result = self.database.query_recording_id(str(_command['recording']))
            if 'compressed' in _command:
                result = self.database.query_recording_id(str(_command['compressed']))
        return result
