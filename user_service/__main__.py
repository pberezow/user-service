from gunicorn.app.base import BaseApplication

from user_service.settings import Settings, settings_dict
from user_service.app import UserApplication


def get_app():
    # config = Settings(**settings_dict)
    config = settings_dict
    return UserApplication(config=config)


class GunicornApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or dict()
        super().__init__()

    def load(self):
        return self.application

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)


if __name__ == '__main__':
    print('Starting...')
    app = get_app()
    gunicorn_app = GunicornApplication(app, options=app.config['gunicorn'])
    gunicorn_app.run()
