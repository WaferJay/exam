import json

from app import db


class ConfigItem(db.Model):
    __tablename__ = "global_config"
    __bind_key__ = "config"

    separators = (",", ":")
    json_dump_kwargs = {
        'separators': (',', ':'),
        'ensure_ascii': True
    }

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    name = db.Column(db.String(36), nullable=False, unique=True)
    _value = db.Column('value', db.TEXT, nullable=True)

    @property
    def value(self):
        return json.loads(self._value) if self._value else self._value

    @value.setter
    def value(self, value):
        self._value = json.dumps(value, **self.json_dump_kwargs)

    def __init__(self, key: str, value=None):
        self.name = key
        self.value = value

    def __str__(self):
        return "%s=%r" % (self.name, self.value)
