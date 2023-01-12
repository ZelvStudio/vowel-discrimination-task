# Installation

    1. python (v3)
    2. pip (v3)
    3. ```pip install virtualenv```
    4. ```git clone git@github.com:ZelvStudio/vowel-discrimination-task.git```
    5. ```cd vowel-discrimination-task```
    6. ```virtualenv venv```
    7. ```source venv/bin/activate```
    8. ```pip install -r requirements.txt```

Should be ready to go!

# Create database

Run ```python``` to open a python shell
Now create the database

```
>>> from models import *
>>> create_tables()
```

# Run local server in debug mode

```flask --app app --debug run```

Open [localhost:5000](http://localhost:5000) in your favorite browser
