import requests
from app.common.services import exceptions


class RequestMixin:

    @classmethod
    def _perform_request(
        cls,
        url: str,
        data: dict,
        method: str = 'post'
    ) -> requests.Response:

        try:
            if method == 'post':
                response = requests.post(url=url, json=data)
            elif method == 'get':
                response = requests.get(url=url, params=data)
        except Exception as e:
            raise exceptions.ServiceConnectionError(
                details={
                    'error': str(e)
                }
            )
        else:
            if not response.ok:
                raise exceptions.ServiceBadRequest(
                    details={
                        'code': response.status_code,
                        'error': response.json()
                    }
                )
        return response
