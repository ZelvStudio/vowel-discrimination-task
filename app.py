from flask import render_template, url_for, request, redirect, session, abort

from config import app, experiment
from models import Participant, Trial


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        consent = request.form['consent']
        participant = Participant.create(gender=gender, age=age, consent=consent)
        session["id"] = participant.id
        return redirect('/trial/0')
    else:
        return render_template('index.html')

@app.route("/trial/<int:n>", methods=['POST', 'GET'])
def trial(n):
    # check the Participant is valid
    if not "id" in session:
        return redirect('/')
    elif Participant.is_completed(session):
        return redirect('/fin')
    # check the url is valid
    if n < 0 or n >= len(experiment):
        abort(404)

    trial_index, sound_file, truth, vowels = experiment[n]
    sound_file = url_for("static", filename=sound_file)
    if request.method == 'POST':
        answer = request.form['answer']
        Trial.create(index=trial_index,participant=session["id"],truth=truth,answer=answer)
        next = n+1
        if next == len(experiment):
            Participant.complete(session)
            return redirect('/fin')
        else:
            return redirect(f'/trial/{next}')
    else:
        return render_template('trial.html', vowels=vowels, sound_file=sound_file, n=n)

@app.route("/fin")
def fin():
    return render_template('fin.html')
