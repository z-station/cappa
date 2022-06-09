from app.common.services.exceptions import ServiceException
from app.common.services import (
    codes,
    messages
)


class InvalidScoreValue(ServiceException):

    default_message = messages.MSG_007
    code = codes.CODE_007


class ScoreRequired(ServiceException):

    default_message = messages.MSG_008
    code = codes.CODE_008


class ReviewUnAvailable(ServiceException):

    default_message = messages.MSG_011
    code = codes.CODE_011


class SolutionsLimit(ServiceException):

    default_message = messages.MSG_012
    code = codes.CODE_012
