import peewee as pw
from datetime import datetime
from config import db

def create_tables():
    with db:
        db.create_tables([Participant,Trial])


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
    consent = pw.BooleanField(default=False)
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
        return f'<Participant {self.id}> trial_permutation={self.trial_permutation}, gender={self.gender}, age={self.age}, consent={self.consent}, date={self.date_created}, completed={self.completed}'


class Trial(BaseModel):
    participant = pw.ForeignKeyField(Participant, backref='trials')
    index = pw.IntegerField()
    truth = pw.CharField()
    answer = pw.CharField()
    assist = pw.FloatField()

    def __repr__(self):
        return f'<Trial {self.index}> participant={self.participant}, truth={self.truth}, answer={self.answer}, assist={self.assist}'
