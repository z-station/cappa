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

