try:
    from .local import *
except ModuleNotFoundError:
    from src.utils import msg
    raise Exception(msg.SYS__01)
