from .base import *

try:
    from .local import *
except ModuleNotFoundError:
    try:
        from .prod import *
    except ModuleNotFoundError:
        from src.utils import msg
        raise Exception(msg.SYS__01)
