import peewee as pw
from datetime import datetime
from config import db

def create_tables():
    with db:
        db.create_tables([Participant,Trial])


class BaseModel(pw.Model):
    class Meta:
        database = db


class Participant(BaseModel):
    id = pw.AutoField(primary_key=True)
    gender = pw.IntegerField(default=-1)
    age = pw.IntegerField(default=0)
    consent = pw.BooleanField(default=False)
    date_created = pw.DateTimeField(default=datetime.now)
    completed = pw.BooleanField(default=False)

    @classmethod
    def is_completed(cls,session):
        return cls.get(cls.id==session["id"]).completed

    @classmethod
    def complete(cls,session):
        query = cls.update(completed=True).where(cls.id==session["id"])
        query.execute()

    def __repr__(self):
        return f'<Participant {self.id}> gender={self.gender}, age={self.age}, consent={self.consent}, date={self.date_created}, completed={self.completed}'


class Trial(BaseModel):
    participant = pw.ForeignKeyField(Participant, backref='trials')
    index = pw.IntegerField()
    truth = pw.CharField()
    answer = pw.CharField()

    def __repr__(self):
        return f'<Trial {self.index}> participant={self.participant}, truth={self.truth}, answer={self.answer}'
