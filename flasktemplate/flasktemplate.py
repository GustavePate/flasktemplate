import os
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import logging.config

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
# create the application instance :)
# here for availability in other packages
app = Flask(__name__)


from flask import json
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flasktemplate.services.ExempleResource import ExempleResource
from flasktemplate.utils.db import Db

logger = logging.getLogger(__name__)

##########################
# Application configuration
##########################

app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

# conf from env var
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

##########################
# Logger conf
##########################

# Flaskr_settings peut contenir le path vers un fichier de conf qui surachargera la conf déclaréé

log_conf_path = os.path.join(app.root_path, "./conf/logging.json")
# read log configuration
if os.path.exists(log_conf_path):
    with open(log_conf_path, 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

#
# file_handler = RotatingFileHandler('./logs/foo.log', maxBytes=10000, backupCount=1)
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(Formatter(
#     '%(asctime)s %(levelname)s: %(message)s '
#     '[in %(pathname)s:%(lineno)d]'
# ))
#
# logger.addHandler(file_handler)
logger.info("!!!!!!!!!!!!!!!")
logger.info("!!! started !!!")
logger.info("!!!!!!!!!!!!!!!")


##########################
# Swagger conf
##########################


api = Api(app, api_version='0.0', api_spec_url='/api/swagger')
api.add_resource(ExempleResource, '/api/users/<int:user_id>')
# api.add_resource(SwaggerResource, '/api/swagger/')

SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:5000/api/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Super Test application override"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def handle404(ctx):
    logger.error('404')
    return "404"


app.register_error_handler(404, handle404)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    db = Db()
    db.init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = Db()
    ldb = db.get_db()
    cur = ldb.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = Db()
    ldb = db.get_db()
    ldb.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    ldb.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(url_for('show_entries'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/rest/user/<username>', methods=['GET', 'PUT'])
def show_user_profile(username):
    # show the user profile for that user
    if request.method == 'GET':
        return json.jsonify({'user': '%s' % username})
    else:
        return 'put'
