class Singleton(object):

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.__init__(instance, *args, **kwargs)
        return instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = cls.__internal_new__(*args, **kwargs)

        return cls._instance

    def __init__(self, *args, **kwargs):
        pass
