from app.accounts.services import UserService


class LastSeenUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated():
            UserService.set_last_seen_now(request.user)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
