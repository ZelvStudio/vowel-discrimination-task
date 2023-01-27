from flask import Flask
from data import Experiment
import peewee

EXPERIMENT = 'experiment.yaml'
experiment = Experiment(EXPERIMENT)

DATABASE = 'instance/test_P5_D4_RT_003_cam.db'
db = peewee.SqliteDatabase(DATABASE)

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

