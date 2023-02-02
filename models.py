import peewee as pw
from datetime import datetime
from config import db
import os

def create_tables():
    if os.path.isfile(db.database):
        raise FileExistsError(f'Database {db.database} already exists')
    with db:
        db.create_tables([Participant,Trial])

def delete_tables():
    database_path = db.database
    if not os.path.isfile(database_path):
        print(f"{database_path} doesn't exist")
        return

    database_name = os.path.basename(database_path)
    answer = input(f"Do you really want to delete {database_name}? All data will be lost (y/[n])? ")
    match answer.lower():
        case 'y':
            os.remove(database_path)
            if not os.path.isfile(database_path):
                print(f"{database_name} has been deleted")
            else:
                print(f"Failed to delete {database_name}")
        case _:
            print("No changes were made")



class BaseModel(pw.Model):
    class Meta:
        database = db

GENDER = ( 
          "undefined",
          "female",
          "male",
          )

class GenderField(pw.CharField):
    def db_value(self,value):
        if not value in GENDER:
            raise TypeError("Wrong value, constrained to {GENDER}")
        return super().adapt(value)

class PermutationField(pw.TextField):
    def db_value(self,integer_list):
        string_list =  " ".join([str(n) for n in integer_list])
        return super().adapt(string_list)

    def python_value(self,string_list):
        return [int(n) for n in string_list.split()]

class Participant(BaseModel):
    id = pw.AutoField(primary_key=True)
    gender = GenderField(default="undefined")
    age = pw.IntegerField(default=0)
    native = pw.BooleanField(default=False)
    consent = pw.BooleanField(default=False)
    name = pw.CharField(default="")
    date_created = pw.DateTimeField(default=datetime.now)
    completed = pw.BooleanField(default=False)
    trial_permutation = PermutationField()

    @classmethod
    def is_completed(cls,session):
        return cls.get(cls.id==session["id"]).completed

    @classmethod
    def complete(cls,session):
        query = cls.update(completed=True).where(cls.id==session["id"])
        query.execute()

    def __repr__(self):
        return f'<Participant {self.id}: "{self.name}"> trial_permutation={self.trial_permutation}, gender={self.gender}, age={self.age}, native={self.native}, consent={self.consent}, date={self.date_created}, completed={self.completed}'


class Trial(BaseModel):
    participant = pw.ForeignKeyField(Participant, backref='trials')
    index = pw.IntegerField()
    file = pw.CharField()
    truth = pw.CharField()
    assist = pw.FloatField()
    answer1 = pw.CharField()
    answer2 = pw.CharField()

    def __repr__(self):
        return f'<Trial {self.index}> participant={self.participant}, truth={self.truth}, assist={self.assist}, answer1={self.answer1}, answer2={self.answer2}\n file={self.file}'
