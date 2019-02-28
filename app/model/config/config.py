from app import db
from app.util import singleton_instance
from .configitem import ConfigItem


@singleton_instance
class Config(object):

    @staticmethod
    def get(key: str, default=None):
        obj = ConfigItem.query.filter_by(name=key).first()

        if obj:
            return obj.value

        return default

    @staticmethod
    def set(key: str, value, allow_create=True):
        obj: ConfigItem = ConfigItem.query.filter_by(name=key).first()
        if not obj:
            if allow_create:
                obj = ConfigItem(key, value)
                db.session.add(obj)
            else:
                raise KeyError(key)
        else:
            obj.value = value

        db.session.commit()

    @staticmethod
    def delete(key, ignore=True):
        option = ConfigItem.query.filter_by(name=key).first()

        if option:
            db.session.delete(option)
            db.session.commit()
        elif not ignore:
            raise KeyError(key)

    def __getitem__(self, item: str):
        return self.get(item)

    def __setitem__(self, key: str, value):
        return self.set(key, value)

    def __getattr__(self, item):
        getter = object.__getattribute__(self, 'get')
        value = getter(item)
        return value

    def __setattr__(self, key: str, value):
        self.set(key, value)

    def __delitem__(self, key):
        option = ConfigItem.query.filter_by(name=key).first()

        if option:
            db.session.delete(option)
            db.session.commit()
        else:
            raise KeyError(key)

    def __delattr__(self, item: str):
        self.delete(item, False)
