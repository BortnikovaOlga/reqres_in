from requests import Response

from client.http_client import HttpClient


class LoginApi:
    url: str = "login"

    def __init__(self, base_url: str):
        self.client = HttpClient(f"{base_url}/{self.url}")

    def login(self, **kwargs) -> Response:
        return self.client.post(**kwargs)