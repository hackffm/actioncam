import sqlite3


class Database:

    def __init__(self, configuration, helper):
        self.configuration = configuration
        self.config = configuration.config
        self.helper = helper

        self.default = self.config['default']
        self.db_path = self.config['default']['folder_data'] + '/' + self.config['default']['db_name']

        self.conn = ''

    def db_check(self):
        if self.helper.folder_create_once(self.config['default']['folder_data']):
            self.db_create()
        else:
            return self.config['error'] + ' creating database ' + self.db_path
        return 'db ok'

    def db_create(self):
        self.conn = sqlite3.connect(self.db_path)
        print("successfully connected database " + self.db_path)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS compress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name           TEXT    NOT NULL,
                        date           TEXT    NOT NULL
                        );''')
        print("successfully created table compress")

        self.conn.execute('''CREATE TABLE IF NOT EXISTS recording (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        identifier     TEXT    NOT NULL,
                        mode           TEXT    NOT NULL,
                        name           TEXT    NOT NULL,
                        type           TEXT    NOT NULL,
                        date           TEXT    NOT NULL
                        );''')
        print("successfully created table recording")

        # connection tables
        self.conn.execute('''CREATE TABLE IF NOT EXISTS  compress2recording (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        id_compress    INT     NOT NULL,
                        id_recording   INT     NOT NULL,
                        FOREIGN KEY (id_compress) REFERENCES compress (id),
                        FOREIGN KEY (id_recording) REFERENCES recording (id)
                        );''')
        print("successfully created table compress2recording")

        self.conn.commit()
        self.conn.close()

    def db_path(self):
        home = os.getenv('HOME')
        path_data = home + '/actioncam/data/actioncam.db'
        return path_data

    # -- compress ------------------------------------------------------------------------
    def add_compressed(self, compressed):
        _date = self.helper.now_str()
        self.conn.execute("INSERT INTO compress (name,date) \
                VALUES ('" + str(compressed) + "', '" + _date + "');")
        self.conn.commit()
        print('successfully added recording ' + str(compressed))

    def add_recording(self, recording):
        r1 = recording.split('.')
        r = r1[0].split('_')
        r.append(r1[1])
        _date = self.helper.now_str()
        self.conn.execute("INSERT INTO recording (identifier,mode,name,type,date) \
                VALUES ('" + r[0] + "', '" + str(r[1]) + "', '" + str(r[2]) + "', '" + str(
            r[3]) + "', '" + _date + "');")
        self.conn.commit()
        print('successfully added recording ' + str(r))
        _name = r[2]
        return _name

    def add_compressed2recording(self, compressed, recording):
        self.conn = sqlite3.connect(self.db_path)
        self.add_compressed(compressed)
        name = self.add_recording(recording)
        self.conn.execute("insert into compress2recording ( id_compress, id_recording) SELECT \
            (select id as id_compress from compress where name = '" + compressed + "'), \
            (select id as id_recording from recording where name = " + name + ")")
        self.conn.commit()
        print('successfully added compress2recording')
        return 'added'
