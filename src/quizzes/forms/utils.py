
class Response:

    """ statuses:
        success:
            200 ok
        warnings:
            300 failed tests
        errors:
            400 debug error
            401 invalid form data
            402 not authorized
            403 solution checked, change not allowed
            404 operation not allowed
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
