from app.common.services.exceptions import ServiceException
from app.common.services import messages, codes


class ServiceConnectionError(ServiceException):

    default_message = messages.MSG_001
    code = codes.CODE_001


class ServiceBadRequest(ServiceException):

    default_message = messages.MSG_002
    code = codes.CODE_002


class ServiceInvalidResponse(ServiceException):

    default_message = messages.MSG_003
    code = codes.CODE_003
