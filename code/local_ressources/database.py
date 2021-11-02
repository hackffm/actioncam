import sqlite3


class Database:

    def __init__(self, configuration, helper, debug=False):
        self.configuration = configuration
        self.config = configuration.config
        self.helper = helper
        self.debug = configuration.config['debug']

        self.default = self.config['default']
        self.db_path = self.config['default']['folder_data'] + '/' + self.config['database']['name']
        self.executed = 'executed'
        self.exists = 'exists'
        self.failed = 'failed'
        self.name = 'database'

        self.db_check()

    # -- main ------------------------------------------------------------
    def db_check(self):
        self.log('check DB ' + self.db_path)
        if self.helper.folder_create_once(self.config['default']['folder_data']):
            self.db_create()
        else:
            return self.config['error'] + ' creating database ' + self.db_path
        return 'db ok'

    def db_execute(self, sql_text):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute(sql_text)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            self.log('SQL Error in')
            self.log(sql_text)
            self.log('is')
            self.log(e)
            conn.close()
            return e
        return self.executed

    def db_query(self, sql_text):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(sql_text)
            rows = cur.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            self.log(e)
            conn.close()
            return self.failed

    def int_from_id(self, _id):
        if len(_id) > 0:
            _id = _id[0][0]
            return _id
        else:
            return self.failed

    def log(self, text):
        self.helper.log_add_text(self.name, str(text))
    # -- create -----------------------------------------------------------------

    def db_create(self):
        _sql_text = ('''CREATE TABLE IF NOT EXISTS compress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name           TEXT    NOT NULL UNIQUE,
                        date           TEXT    NOT NULL
                        );''')
        self.db_execute(_sql_text)
        self.log("checked table compress")

        _sql_text = ('''CREATE TABLE IF NOT EXISTS recording (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        identifier     TEXT    NOT NULL,
                        mode           TEXT    NOT NULL,
                        path           TEXT    NOT NULL,
                        preview        TEXT    NOT NULL UNIQUE,
                        recording      TEXT    NOT NULL UNIQUE,
                        date           TEXT    NOT NULL
                        );''')
        self.db_execute(_sql_text)
        self.log("checked table recording")

        _sql_text = ('''CREATE TABLE IF NOT EXISTS send (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        id_compress    INT     NOT NULL,
                        size           TEXT    NOT NULL,
                        receiver       TEXT    NOT NULL,
                        date           TEXT    NOT NULL
                        );''')
        self.db_execute(_sql_text)
        self.log("checked table send")

        _sql_text = ('''CREATE TABLE IF NOT EXISTS state (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        state          TEXT    NOT NULL UNIQUE ,
                        value          TEXT    NOT NULL
                        );''')
        self.db_execute(_sql_text)
        self.log("checked table state")

        # connection tables
        _sql_text = ('''CREATE TABLE IF NOT EXISTS  compress2recording (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        id_compress    INT     NOT NULL,
                        id_recording   INT     NOT NULL UNIQUE,
                        date           TEXT    NOT NULL,
                        FOREIGN KEY (id_compress) REFERENCES compress (id),
                        FOREIGN KEY (id_recording) REFERENCES recording (id)
                        );''')
        self.db_execute(_sql_text)
        self.log("checked table compress2recording")

    # -- compress ------------------------------------------------------------------------

    def add_compressed(self, compressed):
        _date = self.helper.now_str()
        _sql_text = ("INSERT INTO compress (name,date) VALUES ('" + compressed + "', '" + _date + "');")
        _result = self.db_execute(_sql_text)
        if _result == self.executed:
            self.log('successfully added compressed ' + str(compressed))
        else:
            return _result
        _sql_text = ("select id from compress where name like '" + compressed + "'")
        _id = self.db_query(_sql_text)
        return self.int_from_id(_id)

    def add_compressed2recording(self, compressed, recording):
        id_c = self.query_compressed_id(compressed)
        if type(id_c) != int or id_c < 1:
            return self.failed
        id_r = self.query_recording_id(recording)
        if type(id_r) != int or id_r < 1:
            return self.failed
        _sql_text = ("insert into compress2recording ( id_compress, id_recording, date) VALUES ('")
        _sql_text = _sql_text + str(id_c) + "','"
        _sql_text = _sql_text + str(id_r) + "','"
        _sql_text = _sql_text + self.helper.now_str() + "')"
        _result = self.db_execute(_sql_text)
        if _result == self.executed:
            self.log('successfully added add_compressed2recording ' + str(compressed) + " " + str(recording))
        else:
            self.log('failed adding with add_compressed2recording ' + str(compressed) + " " + str(recording))
            self.log(str(_result))
            return self.failed
        return self.executed

    def add_recording(self, identifier, mode, path, preview, recording):
        _id = self.query_recording_id(recording)
        if _id != self.failed:
            return self.exists
        _date = self.helper.now_str()
        _sql_text = ("INSERT INTO recording (identifier, mode, path, preview, recording, date) \
                VALUES ('" + str(identifier) + "', '" + str(mode) + "', '" + str(path) + "', '" + str(preview) + "', '" + str(recording) + "', '" + _date + "');")
        _result = self.db_execute(_sql_text)
        if _result == self.executed:
            self.log('successfully added recording ' + str(recording))
        else:
            return _result
        _sql_text = ("select id from recording where recording like " + "'" + recording + "'")
        if self.debug:
            print(_sql_text)
        _id = self.db_query(_sql_text)
        return self.int_from_id(_id)

    def recording_name(self, rd):
        return rd[2]

    def add_send(self, compress_name, size, receiver, date):
        id_compressed = self.query_compressed_id(compress_name)
        if id_compressed != self.failed:
            _sql_text = ("INSERT INTO send (id_compress, size, receiver, date) VALUES (")
            _sql_text = _sql_text + str(id_compressed) + ", '" + str(size) + "', '" + str(receiver) + "', '" + str(date) + "');"
            _result = self.db_execute(_sql_text)
            return _result
        else:
            self.log('failed to find compressed id of ' + compress_name)
            return self.failed

    # -- query -----------------------------------------------------------------------------------------------
    def query_compressed_id(self, compressed):
        _sql_text = ("select id from compress where name like '" + compressed + "'")
        _id = self.db_query(_sql_text)
        return self.int_from_id(_id)

    def query_recording_id(self, recording):
        self.log('query recording id :' + str(recording))
        _sql_text = ("select id from recording where recording like '" + recording + "'")
        if self.debug:
            print(_sql_text)
        _id = self.db_query(_sql_text)
        return self.int_from_id(_id)

    def query_report(self):
            _sql_text = "select "
            _sql_text = _sql_text + "recording.identifier as id,"
            _sql_text = _sql_text + "recording.mode,"
            _sql_text = _sql_text + "recording.preview,"
            _sql_text = _sql_text + "recording.path,"
            _sql_text = _sql_text + "recording.recording,"
            _sql_text = _sql_text + "recording.date as recorded,"
            _sql_text = _sql_text + "compress.name as compressed,"
            _sql_text = _sql_text + "compress.date,"
            _sql_text = _sql_text + "send.date as send from recording "
            _sql_text = _sql_text + "left join compress2recording on recording.id= compress2recording.id_recording "
            _sql_text = _sql_text + "left join compress on compress.id= compress2recording.id_compress "
            _sql_text = _sql_text + "left join send on compress.id= send.id_compress"
            result = self.db_query(_sql_text)
            return result

    def query_send(self):
        self.log('query state')
        result = []
        _sql_text = ('''select compress.name from compress
                        inner join send on send.id_compress = compress.id
                        order by send.date''')
        _send = self.db_query(_sql_text)
        for s in _send:
            result.append(str(s[0]))
        return result