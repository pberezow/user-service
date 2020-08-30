import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping


class DBManager:
    def __init__(self, connection):
        self.connection = connection
        self.engine = sqlalchemy.create_engine(self.connection)
        self._db_session = scoping.scoped_session(
            orm.sessionmaker(
                bind=self.engine,
                autocommit=True
            )
        )

    @property
    def session(self):
        return self._db_session()

    def setup(self):
        pass
