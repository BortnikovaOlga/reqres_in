from requests import Response

from client.http_client import HttpClient


class UsersApi:
    url: str = "users"

    def __init__(self, base_url: str):
        self.client = HttpClient(f"{base_url}/{self.url}")

    def get_all(self) -> Response:
        return self.client.get(url="/all")

    def get_paginated(self, page=None, size=None) -> Response:
        params = {}
        if page:
            params["page"] = page
        if size:
            params["size"] = size
        return self.client.get(params=params)

    def get_by_id(self, user_id: int) -> Response:
        return self.client.get(url=f"/{user_id}")

    def post(self, **kwargs) -> Response:
        return self.client.post(**kwargs)

    def patch(self, user_id: int, **kwargs) -> Response:
        return self.client.patch(url=f"/{user_id}", **kwargs)

    def delete(self, user_id: int, **kwargs) -> Response:
        return self.client.delete(url=f"/{user_id}", **kwargs)
