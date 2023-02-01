from flask import render_template, url_for, request, redirect, session, abort
from functools import wraps

from config import app, experiment
from models import Participant, Trial


def registration_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check the Participant is valid
        if not "id" in session:
            return redirect('/')
        elif Participant.is_completed(session):
            return redirect('/fin')
        return func(*args, **kwargs)
    return wrapper


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        native = request.form['french-native']
        consent = request.form['consent']
        participant_trials = experiment.randomize()
        participant = Participant.create(gender=gender, age=age, native=native, consent=consent, trial_permutation=participant_trials)
        session["id"] = participant.id
        session["permutation"] = participant_trials
        return redirect('/start')
    else:
        return render_template('index.html')

@app.route("/start", methods=['POST', 'GET'])
@registration_required
def start():
    if request.method == 'POST':
        return redirect('/trial/1')
    else:
        return render_template('start.html')

@app.route("/trial/<int:n>", methods=['POST', 'GET'])
@registration_required
def trial(n):
    # check the url is valid
    if n < 0 or n >= len(experiment):
        abort(404)

    # i is the index used for indexing (starts at 0)
    i = n-1

    permutation = session["permutation"]
    trial_index, sound_file, truth, assist, vowels = experiment[permutation[i]]
    sound_file = url_for("static", filename=sound_file)
    if request.method == 'POST':
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        trial_aready_done = Trial.select()\
                                 .where(Trial.index==trial_index,
                                        Trial.participant==session["id"])\
                                 .exists()
        if trial_aready_done:
            Trial.update(answer1=answer1,
                         anwer2=answer2)\
                 .where(Trial.index==trial_index,
                        Trial.participant==session["id"])\
                 .execute()
        else:
            Trial.create(index=trial_index,
                         participant=session["id"],
                         file=sound_file,
                         truth=truth,
                         answer1=answer1,
                         answer2=answer2,
                         assist=assist)
        next = n+1
        if next == len(permutation):
            Participant.complete(session)
            return redirect('/fin')
        else:
            return redirect(f'/trial/{next}')
    else:
        return render_template('trial.html', vowels=vowels, sound_file=sound_file, n=n, length=len(permutation))

@app.route("/fin")
def fin():
    return render_template('fin.html')
