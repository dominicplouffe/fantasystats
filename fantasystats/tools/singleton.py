class Singleton(object):
    @classmethod
    def Instance(cls):
        if not cls.InstanceAvailable():
            cls._INSTANCE = cls()
        return cls._INSTANCE

    @classmethod
    def InstanceAvailable(cls):
        return hasattr(cls, '_INSTANCE')
