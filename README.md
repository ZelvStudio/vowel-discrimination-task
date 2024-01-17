# 👂 Vowel discrimination task

## ⚙️ Installation
#### Requirements

This has been developped with `python3.10`, it does not work with older versions of Python 3. If necessary, install it from your package manager as well as `pip` for Python 3.

#### Clone git repo

```
git clone git@github.com:gaheldev/vowel-discrimination-task.git
cd vowel-discrimination-task
```

#### Set up virtualenv (optional)

We use virtualenv to create an environment with controlled python package versions. 


```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

`source venv/bin/activate` should be run in any terminal tab you open before working on the project. Run `deactivate` to deactivate the virtualenv.

#### Install required python packages

```
pip install -r requirements.txt
```

Should be ready to go!

## 🏃 Running
#### Create database

```
python -m flask initdb
```

#### Run local server in debug mode
Start the server in debug mode by running 

```
python -m flask --app app --debug run
```

Open [localhost:5000](http://localhost:5000) in your favorite browser to access the website.

#### Inspect database
Check out [peewee's documentation](http://docs.peewee-orm.com/en/latest/peewee/querying.html) about making queries to the database.

```python
from config import app, db, experiment
from models import *
participants = [p for p in Participant.select().dicts()] # get all participants
trials = [p for p in Trial.select().dicts()] # get all trials
```

#### Deploy
As of 03/02/2023, we recommend using pythonanywhere.com which has a free tier and is easy to use.

## 🔧 Make your own experiment
The recommended workflow is to create a new branch per experiment. Commits to the main branch should benefit to all experiments, i.e. mainly bug fixes. 
Experiments branches should not be merged into main (in general). If you need to include in your branch some changes from main, just rebase your branch on main:
```
git rebase main
```

#### Create a new development branch (required)
```
git branch <your-branch-name>
git checkout <your-branch-name>
```
Now you can edit anything without messing up with the main branch. 

#### Add your data (required)
Create a folder `static/data/<your-experiment>/` and copy the sound files of your trials in it.

#### Create an experiment config file (required)
Create a copy of `experiments/test.yaml` into `experiments/<your-experiment>.yaml` and edit it.
The file should be self explanatory.

#### Edit config.py (required)
Open config.py and edit the configuration variables in all caps:

```python
EXPERIMENT_NAME = '<your-experiment>'
CONTACT = '<your-mail-adress>'
DATABASE = '<your-experiment-database.db>'
SECRET_KEY = '<a-random-sequence-of-characters>'
```

#### Edit the application (optional)
The project follows a typical flask structure: 
- the application logic is found in `app.py`
- the database models are found in `models.py`
- the app configuration is found in `config.py`
- the data loader of the experiment is found in `data.py`
- the html views are in `templates/`
- the css styling is in `static/scss/` and `static/css/`
- the databases are in `instance`

<details><summary>Deleting the database (required if you updated the data models)</summary>
<p>

Either delete your database file in `instance/` or run a `python` interpreter:
```
from models import *
delete_tables()
```

Then recreate the database.

</p>
</details>


