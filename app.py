from flask import render_template, url_for, request, redirect, session

from .config import app
from .models import Participant, Trial


# If test is already completed, the participant is redirected to the end page
def check_completed(func):
    def wrapper():
        if Participant.is_completed(session):
            return redirect('/fin')
        else:
            return func()
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        consent = request.form['consent']
        participant = Participant.create(gender=gender, age=age, consent=consent)
        session["id"] = participant.id
        return redirect('/trial')
    else:
        return render_template('index.html')

@app.route("/trial", methods=['POST', 'GET'])
@check_completed
def trial():
    vowels = ['a','e','i','o','u','é','è','ou','an','on','in']
    truth = 'a'
    sound_file = url_for("static", filename=f'data/{truth}.wav')
    if request.method == 'POST':
        answer = request.form['answer']
        Trial.create(participant=session["id"],truth=truth,answer=answer)
        Participant.complete(session)
        return redirect('/fin')
    else:
        return render_template('trial.html', vowels=vowels, sound_file=sound_file)

@app.route("/fin")
def fin():
    return render_template('fin.html')
