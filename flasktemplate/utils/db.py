from flask import Flask, current_app, g
import sqlite3
import logging

logger = logging.getLogger(__name__)


class Db():

    app = None

    def __init__(self):
        app = Flask(__name__)
        with app.app_context():
            self.app = current_app

    def init_db(self):
        logger.info('init db here')
        db = self.get_db()
        with self.app.open_resource('sql/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    def connect_db(self):
        """Connects to the specific database."""
        logger.info("connect to: %s", self.app.config['DATABASE'])
        rv = sqlite3.connect(self.app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = self.connect_db()
        return g.sqlite_db
