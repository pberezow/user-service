import psycopg2
from typing import Optional, Dict, Any
from copy import deepcopy


class DBManager:
    class DBConnectionError(Exception):
        pass

    def __init__(self, db_config: Optional[Dict[str, Any]] = None, init_db: bool = False,
                 init_script: Optional[str] = None):
        if db_config is None:
            raise self.DBConnectionError()

        self._config = None
        if db_config:
            self._config = db_config
            self.connection = self.prepare_uri(**db_config)

        if init_db:
            self._db_connection = None
            self.init_db(init_script=init_script)

        try:
            self._db_connection = self._connect()
        except psycopg2.Error:
            raise self.DBConnectionError()

    def _connect(self, autocommit: bool = False):
        conn = psycopg2.connect(dsn=self.connection)
        if autocommit:
            conn.set_session(autocommit=True)
        return conn

    def _connect_root(self):
        connection_cfg = dict(**self._config)
        connection_cfg['dbname'] = ''
        dsn = self.prepare_uri(**connection_cfg)
        conn = psycopg2.connect(dsn=dsn)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        return conn

    def _create_db(self, db_name: str) -> bool:
        if not self._config:
            return False

        # close old connection and connect to db
        if self._db_connection:
            self._db_connection.close()
        con = self._connect_root()

        # create database
        with con.cursor() as cur:
            try:
                cur.execute(f'CREATE DATABASE {db_name};')
            except psycopg2.Error as err:
                raise self.DBConnectionError() from err

        # connect manager to created db
        con.close()
        self._config['dbname'] = db_name
        self.connection = self.prepare_uri(**self._config)
        try:
            self._db_connection = self._connect()
        except psycopg2.Error as err:
            raise self.DBConnectionError() from err
        return True

    def _drop_db(self, db_name: Optional[str] = None) -> bool:
        if db_name is None:
            try:
                db_name = self._config['dbname']
            except KeyError:
                return False

        # close old connection and connect to db
        if self._db_connection:
            self._db_connection.close()
        con = self._connect_root()

        # drop database
        with con.cursor() as cur:
            try:
                cur.execute(f'DROP DATABASE {db_name};')
            except psycopg2.Error as err:
                raise self.DBConnectionError() from err

        # restore previous connection (if selected database was dropped, then DBConnectionError will be raised!)
        con.close()
        self.connection = self.prepare_uri(**self._config)
        try:
            self._db_connection = self._connect()
        except psycopg2.Error as err:
            raise self.DBConnectionError() from err
        return True

    def session(self):
        if self._db_connection.closed:
            self._db_connection = self._connect()
        return self._db_connection.cursor()

    def commit(self):
        self._db_connection.commit()

    def rollback(self):
        self._db_connection.rollback()

    def init_db(self, init_script: Optional[str] = None) -> bool:
        try:
            self._drop_db(self._config['dbname'])
        except self.DBConnectionError:
            pass
        except KeyError:
            # has to be initialized with config object
            return False
        # will raise self.DBConnectionError if failed
        self._create_db(self._config['dbname'])

        if init_script is not None:
            self.create_tables(init_script)

        return True

    def setup(self):
        pass

    def create_tables(self, init_script: str):
        with open(init_script, 'r') as file:
            script = file.read()

        lines = script.split('\n')
        lines = [line for line in lines if not line.startswith('--') and line != '']
        queries = filter(lambda q: q != '', '\n'.join(lines).split(';'))
        with self.session() as cur:
            for query in queries:
                try:
                    cur.execute(query)
                except psycopg2.Error as err:
                    self.rollback()
                    raise err
            self.commit()

    @staticmethod
    def prepare_uri(host: str, port: int, dbname: str, username: str = '', password: str = '',
                    engine: str = 'postgresql', **kwargs) -> str:
        connection_str = f'{engine}://{username}' + (f':{password}' if password else '') + ('@' if username else '') \
                         + f'{host}:{port}/{dbname}'
        return connection_str
