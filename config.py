from flask import Flask
from data import Experiment
import os
import peewee
import sass

EXPERIMENT = 'experiments/experiment.yaml'

CONTACT = 'gael.le-godais@univ-grenoble-alpes.fr'

DATABASE = 'instance/test_P5_D4_RT_003_cam.db'

SECRET_KEY = '3urg0459'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = SECRET_KEY
# session.permanent = True

EXPERIMENT = os.path.join(app.root_path, EXPERIMENT)
experiment = Experiment(EXPERIMENT)

DATABASE = os.path.join(app.root_path, DATABASE)
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
