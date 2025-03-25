from requests import Session, Response
from client.request_logger import request_logger


class BaseSession(Session):

    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    @request_logger
    def request(self, method, path=None, **kwargs) -> Response:
        url = self.base_url
        if path:
            url += path
        response = super().request(method, url, **kwargs)
        return response
