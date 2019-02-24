import json

from app import db


class Config(db.Model):
    __tablename__ = "global_config"
    __bind_key__ = "config"

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    name = db.Column(db.String(36), nullable=False, unique=True)
    value = db.Column(db.TEXT)

    def __init__(self, key, value):
        self.name = key
        self.value = json.dumps(value, separators=(",", ":"), ensure_ascii=True)

    @classmethod
    def get_value(cls, key, default=None):
        obj = cls.query.filter_by(name=key).first()

        if obj:
            return json.loads(obj.value, ensure_ascii=True)

        return default

    def __str__(self):
        return "%s=%r" % (self.name, self.value)
