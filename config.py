from flask import Flask
from data import Experiment
import peewee
import sass

EXPERIMENT = 'experiments/experiment.yaml'
experiment = Experiment(EXPERIMENT)

CONTACT = 'gael.le-godais@univ-grenoble-alpes.fr'

DATABASE = 'instance/test_P5_D4_RT_003_cam.db'
db = peewee.SqliteDatabase(DATABASE)

# compile scss files into css folder
sass.compile(dirname=('static/scss', 'static/css'), output_style='compressed')

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "3urg0459"
# session.permanent = True

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

