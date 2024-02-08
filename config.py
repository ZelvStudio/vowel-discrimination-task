from flask import Flask
from data import Experiment
import os
import peewee
import sass

EXPERIMENT_NAME = 'P5_D4_RT_003_cam_short'

CONTACT = 'gael.le-godais@univ-grenoble-alpes.fr'

DATABASE = 'P5_D4_RT_003_cam_short.db'

SECRET_KEY = '3urg0459'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = SECRET_KEY
# session.permanent = True

EXPERIMENT = os.path.join(app.root_path, 'experiments/', f'{EXPERIMENT_NAME}.yaml')
experiment = Experiment(EXPERIMENT)

DATABASE = os.path.join(app.root_path, 'instance', DATABASE)
db = peewee.SqliteDatabase(DATABASE)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response


# compile scss files into css folder
scss_dir = os.path.join(app.root_path, 'static/scss')
css_dir = os.path.join(app.root_path, 'static/css')
sass.compile(dirname=(scss_dir, css_dir), output_style='compressed')
