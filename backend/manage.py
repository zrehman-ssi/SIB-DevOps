import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import blueprint
from sqlalchemy_utils import create_database, database_exists

from app.main import create_app, db
from app.main.model import user

app = create_app(os.getenv('SIB_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run(port=5000):
    app.run(port=port)

@manager.command
def create_db():
    url = app.config['SQLALCHEMY_DATABASE_URI']
    if not database_exists(url):
        create_database(url)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()