from app.common.services.exceptions import ServiceException
from app.common.services import messages, codes


class CourseNotFoundException(ServiceException):

    default_message = messages.MSG_010
    code = codes.CODE_010


class GroupStatisticPermissionError(ServiceException):

    default_message = messages.MSG_009
    code = codes.CODE_009
