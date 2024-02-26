from flask import render_template, url_for, request, redirect, session, abort
from functools import wraps

from config import app, experiment, CONTACT
from models import Participant, Trial, create_tables
from peewee import DoesNotExist

@app.cli.command('initdb')
def initdb_command():
    try:
        create_tables()
        print('Initialized the database.')
    except FileExistsError as error:
        print(error)

def registration_required(func):
    """
        decorator to check if the participant is registered and if she already
        completed the test
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check the Participant is valid
        if not "id" in session:
            return redirect('/')

        try:
            if Participant.is_completed(session):
                return redirect('/end')
        except DoesNotExist as e:
            session.clear()
            return redirect('/')

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
        return redirect('/conditioning')
    else:
        return render_template('start.html')


@app.route("/conditioning", methods=['POST', 'GET'])
@registration_required
def conditioning():
    if request.method == 'POST':
        return redirect('/trial/1')
    else:
        permutation = session["permutation"]
        trial_index, sound_file, truth, assist, vowels = experiment[permutation[0]]
        vowels = [(vowel, url_for("static", filename=f)) for vowel, f in vowels]
        return render_template('conditioning.html',
                               vowels=vowels,
                               )


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
    vowels = [(vowel, url_for("static", filename=f)) for vowel, f in vowels]

    trial = Trial.select()\
                 .where(Trial.index==trial_index,
                        Trial.participant==session["id"])
    trial_already_done = trial.exists()
    if request.method == 'POST':
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        listen_count = request.form['listen_count']
        listens = request.form['listens']
        if trial_already_done:
            Trial.update(answer1=answer1,
                         answer2=answer2,
                         listen_count=listen_count,
                         listens=listens,
                         )\
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
                         assist=assist,
                         listen_count=listen_count,
                         listens=listens,
                         )
        next = n+1
        if next == len(permutation) + 1:
            Participant.complete(session)
            return redirect('/end')
        else:
            return redirect(f'/trial/{next}')
    else:
        checked1 = trial.get().answer1 if trial_already_done else None
        checked2 = trial.get().answer2 if trial_already_done else None
        listen_count = trial.get().listen_count if trial_already_done else 0
        listens = trial.get().listens + ' RELOAD' if trial_already_done else ''
        return render_template('trial.html',
                               vowels=vowels,
                               sound_file=sound_file,
                               n=n,
                               length=len(permutation),
                               checked1=checked1,
                               checked2=checked2,
                               listen_count=listen_count,
                               listens=listens,
                               )

@app.route("/trial/<int:n>/back", methods=['POST', 'GET'])
def previous_trial(n):
    return redirect(f'/trial/{n-1}')

@app.route("/end")
def end():
    return render_template('end.html', contact=CONTACT, participant_id=session["id"])
