from typing import Optional
import requests
from app.common.services import exceptions


class RequestMixin:

    @classmethod
    def _perform_request(
        cls,
        url: str,
        data: dict,
        method: str = 'post',
        timeout: Optional[int] = None
    ) -> requests.Response:

        try:
            request_kwargs = {
                'url': url,
                'json': data
            }
            if timeout:
                request_kwargs['timeout'] = timeout

            if method == 'post':
                response = requests.post(**request_kwargs)
            elif method == 'get':
                response = requests.get(**request_kwargs)
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
