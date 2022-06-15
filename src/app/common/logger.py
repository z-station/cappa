import sys
import logging
from logging import StreamHandler, Formatter
from django.conf import settings


def get_logger():

    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.ERROR)
    handler = StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)
    handler.setFormatter(
        Formatter(fmt="[%(levelname)s] %(module)s.py:%(lineno)s %(message)s")
    )
    return logger
