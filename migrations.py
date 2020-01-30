from flask_migrate import Manager, Migrate, MigrateCommand

from server import app, db


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# run: 'python migrations.py db init' to initialize db
# run: 'python migrations.py db migrate' to migrate
# run: 'python migrations.py db upgrade' to apply migrations
