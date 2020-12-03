try:
    from .local import *
except ModuleNotFoundError:
    from cappa.utils import msg
    raise Exception(msg.SYS__01)
