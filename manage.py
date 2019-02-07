import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import Customer, Order


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def shell_make_context():
    return dict(app=app, db=db, Customer=Customer, Order=Order)


manager.add_command('shell', Shell(make_context=shell_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
