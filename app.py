from flask import render_template, url_for, request, redirect, session, abort
from functools import wraps

from config import app, experiment, CONTACT
from models import Participant, Trial


def registration_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check the Participant is valid
        if not "id" in session:
            return redirect('/')
        elif Participant.is_completed(session):
            return redirect('/end')
        return func(*args, **kwargs)
    return wrapper


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        native = request.form['french-native']
        consent = request.form['consent']
        name = request.form['name']
        participant_trials = experiment.randomize()
        participant = Participant.create(gender=gender, 
                                         age=age,
                                         native=native,
                                         consent=consent,
                                         name=name,
                                         trial_permutation=participant_trials)
        session["id"] = participant.id
        session["permutation"] = participant_trials
        return redirect('/start')
    else:
        return render_template('index.html', contact=CONTACT)

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
    if n < 1 or n > len(experiment):
        abort(404)

    # i is the index used for indexing (starts at 0)
    i = n-1

    permutation = session["permutation"]
    trial_index, sound_file, truth, assist, vowels = experiment[permutation[i]]
    sound_file = url_for("static", filename=sound_file)

    trial = Trial.select()\
                 .where(Trial.index==trial_index,
                        Trial.participant==session["id"])
    trial_already_done = trial.exists()
    if request.method == 'POST':
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        if trial_already_done:
            Trial.update(answer1=answer1,
                         answer2=answer2)\
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
        if next == len(permutation) + 1:
            Participant.complete(session)
            return redirect('/end')
        else:
            return redirect(f'/trial/{next}')
    else:
        checked1 = trial.get().answer1 if trial_already_done else None
        checked2 = trial.get().answer2 if trial_already_done else None
        return render_template('trial.html',
                               vowels=vowels,
                               sound_file=sound_file,
                               n=n,
                               length=len(permutation),
                               checked1=checked1,
                               checked2=checked2,
                               )

@app.route("/end")
def end():
    return render_template('end.html', contact=CONTACT, participant_id=session["id"])
