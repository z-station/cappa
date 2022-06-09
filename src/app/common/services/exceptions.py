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
