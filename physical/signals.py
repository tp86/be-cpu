class _SignalMeta(type):
    def __repr__(cls):
        return cls.repr
    __str__ = __repr__

    def __bool__(cls):
        return cls.value


class _Signal(metaclass=_SignalMeta):
    pass


class H(_Signal):
    repr = '\u0393'
    value = True


class L(_Signal):
    repr = 'L'
    value = False
    flip = H


H.flip = L
