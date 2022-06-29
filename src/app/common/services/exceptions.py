from typing import Optional
from app.common.services import messages, codes


class ServiceException(Exception):

    default_message = messages.MSG_000
    code = codes.CODE_000

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[dict] = None
    ):
        self.message = message or self.default_message
        self.details = {'code': self.code}
        if details is not None:
            self.details.update(details)
        super().__init__(message)

    def as_dict(self):
        return {
            'message': self.message,
            'details': self.details
        }


class ServiceConnectionError(ServiceException):

    default_message = messages.MSG_001
    code = codes.CODE_001


class ServiceBadRequest(ServiceException):

    default_message = messages.MSG_002
    code = codes.CODE_002


class ServiceInvalidResponse(ServiceException):

    default_message = messages.MSG_003
    code = codes.CODE_003
