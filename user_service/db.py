import psycopg2


class DBManager:
    def __init__(self, connection: str):
        self.connection = connection
        self._db_connection = self._connect()

    def _connect(self, autocommit: bool = False):
        conn = psycopg2.connect(dsn=self.connection)
        if autocommit:
            conn.set_session(autocommit=True)
        return conn

    def session(self):
        if self._db_connection.closed:
            self._db_connection = self._connect()
        return self._db_connection.cursor()

    def commit(self):
        self._db_connection.commit()

    def rollback(self):
        self._db_connection.rollback()

    def setup(self):
        pass

    @staticmethod
    def prepare_uri(host: str, port: int, dbname: str, username: str = '', password: str = '',
                    engine: str = 'postgresql', **kwargs) -> str:
        connection_str = f'{engine}://{username}' + (f':{password}' if password else '') + ('@' if username else '') \
                         + f'{host}:{port}/{dbname}'
        return connection_str
