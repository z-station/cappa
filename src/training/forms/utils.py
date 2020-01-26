
class Response:

    """ statuses:
        200 ok
        201 failed tests
        202 debug error
        203 invalid form data
        204 not authorized
     """

    def __init__(self, status, msg, output=None, error=None, tests_result=None):
        self.status = status
        self.msg = msg
        if output:
            self.output = output
        if error:
            self.error = error
        if tests_result:
            self.tests_result = tests_result
