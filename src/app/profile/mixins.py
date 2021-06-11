from urllib import parse


class NextPathMixin:

    HOME_PATH = '/'

    def _get_next_path(self, request) -> str:
        next_path = request.GET.get('next')
        if next_path is None:
            next_path = parse.urlparse(
                request.META.get('HTTP_REFERER', self.HOME_PATH)
            ).path
        return next_path
