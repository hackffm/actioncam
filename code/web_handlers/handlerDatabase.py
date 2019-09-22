import tornado.web
import json


class HandlerDatabase(tornado.web.RequestHandler):
    def initialize(self, configuration, database, helper, name='HandlerDatabase'):
        self.configuration = configuration
        self.config = self.configuration.config
        self.database = database
        self.executed = 'executed'
        self.helper = helper
        self.name = name

    def get(self):
        _query = tornado.escape.json_decode(self.request.body)
        _result = self.database_query(_query)
        self.write(json.dumps(_result))

    def post(self, *args):
        try:
            db_command = tornado.escape.json_decode(self.request.body)
            _result = self.database_insert(db_command)
            self.write(_result)
        except Exception as e:
            self.log(str(e))
            self.write('failed')
        self.finish()

    def put(self, *args):
        try:
            db_command = tornado.escape.json_decode(self.request.body)
            _result = self.database_update(db_command)
            self.write(_result)
        except Exception as e:
            self.log(str(e))
            self.write('failed')
        self.finish()

    # ----------------------------------------------------------
    def log(self, text):
        self.helper.log_add_text('handlerDatabase', 'handlerDatabase' + ':' + text)

    def database_insert(self, db_command):
        self.log('insert:' + str(db_command))
        result = self.executed
        if 'add' in db_command:
            _command = db_command['add']
            if 'recording' in _command:
                result = self.database.add_recording(_command['recording'])
            if 'compressed' in _command:
                result = self.database.add_compressed(_command['compressed'])
            if 'compressed2recording' in _command:
                result = self.database.add_compressed2recording(_command['compressed2recording'][0], _command['compressed2recording'][1])
        return result

    def database_query(self, db_command):
        self.log('query:' + str(db_command))
        result = self.executed
        if 'query'in db_command:
            _command = db_command['query']
            # keep the order !
            if 'recording_id' in _command:
                result = self.database.query_recording_id(str(_command['recording']))
            if 'compressed_id' in _command:
                result = self.database.query_compressed_id(str(_command['compressed']))
            if 'compressed2recording' == _command:
                result = self.database.query_compressed2recording(str(_command['compressed2recording']))
            if 'compressed' in _command:
                result = self.database.query_compressed()
            if 'state' in _command:
                result = self.database.query_state()
        return result

    def database_update(self, db_command):
        self.log('update:' + str(db_command))
        result = self.executed
        if 'update' in db_command:
            _command = db_command['update']
            if 'state' in _command:
                print(_command['state'])
                result = self.database.update_state(_command['state'])
        return result
