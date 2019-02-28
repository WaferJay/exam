
def singleton_instance(*args, **kwargs):

    if not kwargs and len(args) == 1:
        return args[0]()

    def _wrapper(cls):
        instance = cls(*args, **kwargs)
        cls.singleton_instance = instance
        return instance

    return _wrapper
