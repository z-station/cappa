from app.common.services.exceptions import ServiceException
from app.common.services import messages, codes


class TestsNotFound(ServiceException):

    default_message = messages.MSG_004
    code = codes.CODE_004


class OperationNotAllowed(ServiceException):

    default_message = messages.MSG_005
    code = codes.CODE_005


class SolutionIsLocked(ServiceException):

    default_message = messages.MSG_006
    code = codes.CODE_006


class CheckPlagException(ServiceException):

    default_message = messages.MSG_013
    code = codes.CODE_013


class SolutionNotFound(ServiceException):

    default_message = messages.MSG_014
    code = codes.CODE_014


class CheckPlagImpossible(ServiceException):

    default_message = messages.MSG_015
    code = codes.CODE_015


class TestingCheckerNotExist(ServiceException):

    default_message = messages.MSG_016
    code = codes.CODE_016
