import falcon
from sqlalchemy.engine.url import URL
from user_service.db import DBManager
from user_service.resources import ExampleResource


class UserApplication(falcon.API):
    def __init__(self, config, middleware=None, router=None, independent_middleware=True):
        super().__init__(middleware=middleware, router=router, independent_middleware=independent_middleware)

        self.config = config

        self._setup_db()
        self._setup_services()
        self._setup_routes()

    def _setup_db(self):
        connection = URL(**self.config['db'])
        self.db_manager = DBManager(connection)
        self.db_manager.setup()
        print(self.db_manager)

    def _setup_services(self):
        pass

    def _setup_routes(self):
        self.add_route('/example', ExampleResource())
