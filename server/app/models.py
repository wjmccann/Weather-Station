from app import db

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(64))
    month = db.Column(db.String(64))
    day = db.Column(db.String(64))
    maxtemp = db.Column(db.Float)
    mintemp = db.Column(db.Float)
    avetemp = db.Column(db.Float)
    rain = db.Column(db.Float)

    def __repr__(self):
        return self.year + "-" + self.month + "-" + self.day
