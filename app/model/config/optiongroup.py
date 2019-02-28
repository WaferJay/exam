from app.model.config import Config


class OptionMeta(type):

    def __new__(mcs, cls_name, parent: tuple, attr: dict):
        for key in attr.keys():

            if isinstance(attr[key], Option):
                attr[key].name = key

        cls = type.__new__(mcs, cls_name, parent, attr)
        cls.instance = cls()
        return cls


class Option(object):

    name = None

    def __init__(self, name=None, allow_create=True, ignore_not_exists=True):
        self.name = name
        self.allow_create = allow_create
        self.ignore_not_exists = ignore_not_exists

    def __get__(self, instance, owner):
        return Config.get(self.name)

    def __set__(self, instance, value):
        return Config.set(self.name, value, self.allow_create)

    def __delete__(self, instance):
        Config.delete(self.name, self.ignore_not_exists)


class OptionGroup(object, metaclass=OptionMeta):
    pass

