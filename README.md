# Vowel discrimination task

## Installation
#### Requirements

This has been developped with `python3.10`, it should work with older versions of Python 3 too. If necessary, install it from your package manager as well as `pip` for Python 3.

#### Clone git repo

```
git clone git@github.com:ZelvStudio/vowel-discrimination-task.git
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

## Running
#### Create database

```
python -m flask initdb
```

#### Run local server in debug mode
Start the server in debug mode by running 

```flask --app app --debug run```

Open [localhost:5000](http://localhost:5000) in your favorite browser to access the website.

<details><summary>Troubleshooting</summary>
<p>

> ModuleNotFoundError: No module named 'config'

Try running ```python -m flask --app app --debug run``` instead
</p>
</details>
