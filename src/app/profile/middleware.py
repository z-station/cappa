from django.utils import timezone
from django.core.cache import cache
from django.conf import settings


class LastSeenUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated():
            last_seen_dict = cache.get('users__last_seen') or {}
            last_seen_dict[request.user.id] = {
                'full_name': request.user.get_full_name(),
                'last_seen': timezone.now().timestamp()
            }
            cache.set(
                key='users__last_seen',
                value=last_seen_dict,
                timeout=settings.LAST_SEEN_CACHE_TIMEOUT
            )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
