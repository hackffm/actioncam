import tornado.web
import json

from tornado.escape import json_encode


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
        if type(_result) == list:
            result = {"result": _result}
            self.write(result)
        self.write(str(_result))

    def post(self, *args):
        try:
            db_command = tornado.escape.json_decode(self.request.body)
            _result = self.database_insert(db_command)
            self.write(str(_result))
        except Exception as e:
            self.log(str(e))
            self.write('failed')
        self.finish()

    def put(self, *args):
        try:
            db_command = tornado.escape.json_decode(self.request.body)
            _result = self.database_update(db_command)
            self.write(str(_result))
        except Exception as e:
            self.log(str(e))
            self.write('failed')
        self.finish()

    # ----------------------------------------------------------
    def log(self, text):
        self.helper.log_add_text('handlerDatabase', str(text))

    def database_insert(self, db_command):
        self.log('insert:' + str(db_command))
        result = self.executed
        if 'add' in db_command:
            _command = db_command['add']
            if 'compressed' in _command:
                result = self.database.add_compressed(_command['compressed'])
            if 'compressed2recording' in _command:
                _cr = _command['compressed2recording']
                result = self.database.add_compressed2recording(_cr['compressed'], _cr['recording'])
            if 'preview' in _command:
                _preview = _command['preview']
                result = self.database.add_preview(_preview['name'], _preview['recording'])
            if 'recording' in _command:
                result = self.database.add_recording(_command['recording'])
            if 'send' in _command:
                _send = _command['send']
                _compress = _send['compressed']
                _size = _send['size']
                _receiver = _send['receiver']
                _date = _send['date']
                result = self.database.add_send(_compress, _size, _receiver, _date)
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
            if 'report' in _command:
                result = self.database.query_report()
                result = json.dumps(result)
            if 'state' in _command:
                result = self.database.query_state()
                result = json.dumps(result)
            if 'send' in _command:
                result = self.database.query_send()
                result = json.dumps(result)
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
