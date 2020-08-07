from .db import db


class Scraping(db.Document):
    link = db.URLField(required=True, unique=True)
    image = db.URLField(required=True, unique=True)
    contador = db.FloatField()


class Fase(db.Document):
    fazer = db.DateTimeField()

