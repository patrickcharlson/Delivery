import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models import Customer, Product

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def shell_make_context():
    return dict(app=app, db=db, Product=Product, Customer=Customer)


manager.add_command('shell', Shell(make_context=shell_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
