import sqlite3


class Database:

    def __init__(self, configuration, helper, debug=False):
        self.configuration = configuration
        self.config = configuration.config
        self.helper = helper
        self.debug = True

        self.default = self.config['default']
        self.db_path = self.config['default']['folder_data'] + '/' + self.config['default']['db_name']
        self.executed = 'executed'
        self.failed = 'failed'
        self.name = 'database'

    # -- main ------------------------------------------------------------
    def db_check(self):
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

    def db_count_name(self, table, name):
        _sql_text = ("select count(id) from " + table +" where name like '" + name + "'")
        _count = self.db_query(_sql_text)
        _count = self.int_from_id(_count)
        return _count

    def int_from_id(self, _id):
        if len(_id) > 0:
            _id = _id[0][0]
            return _id
        else:
            return 'failed'

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
        self.log("successfully created table compress")

        _sql_text = ('''CREATE TABLE IF NOT EXISTS recording (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        identifier     TEXT    NOT NULL,
                        mode           TEXT    NOT NULL,
                        name           TEXT    NOT NULL UNIQUE,
                        type           TEXT    NOT NULL,
                        date           TEXT    NOT NULL
                        );''')
        self.db_execute(_sql_text)
        self.log("successfully created table recording")

        # connection tables
        _sql_text = ('''CREATE TABLE IF NOT EXISTS  compress2recording (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        id_compress    INT     NOT NULL,
                        id_recording   INT     NOT NULL,
                        FOREIGN KEY (id_compress) REFERENCES compress (id),
                        FOREIGN KEY (id_recording) REFERENCES recording (id)
                        );''')
        self.db_execute(_sql_text)
        self.log("successfully created table compress2recording")

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

    def add_recording(self, recording):
        recording_fields = self.recording_data(recording)
        r = recording_fields
        _sql_text = ("INSERT INTO recording (identifier,mode,name,type,date) \
                VALUES ('" + r[0] + "', '" + str(r[1]) + "', '" + str(r[2]) + "', '" + str(r[3]) + "', '" + str(r[4]) + "');")
        _result = self.db_execute(_sql_text)
        if _result == self.executed:
            self.log('successfully added recording ' + str(r))
        else:
            return _result
        _name = self.recording_name(recording_fields)
        _sql_text = ("select id from recording where name like " + _name)
        _id = self.db_query(_sql_text)
        return self.int_from_id(_id)

    def recording_data(self, recording):
        r1 = recording.split('.')
        r = r1[0].split('_')
        r.append(r1[1])
        r.append(self.helper.now_str())
        return r

    def recording_name(self, rd):
        return rd[2]

    def add_compressed2recording(self, compressed, recording):
        _name = self.recording_name(self.recording_data(recording))
        _sql_text = ("insert into compress2recording ( id_compress, id_recording) SELECT \
            (select id as id_compress from compress where name = '" + compressed + "'), \
            (select id as id_recording from recording where name = " + _name + ")")
        _result = self.db_execute(_sql_text)
        if _result == self.executed:
            self.log('successfully added add_compressed2recording ' + str(compressed) + " " + str(recording))
        else:
            return _result
        return 'added'

    def query_compressed(self, compressed):
        _sql_text = ("select id from compress where name like " + compressed)
        _id = self.db_query(_sql_text)
        return _id

    def query_recording_id(self, recording):
        recording_fields = self.recording_data(recording)
        r = recording_fields
        _name = self.recording_name(r)
        _sql_text = ("select id from recording where name like '" + _name + "'")
        _id = self.db_query(_sql_text)
        return self.int_from_id(_id)
