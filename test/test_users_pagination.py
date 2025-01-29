from http import HTTPStatus

import pytest
import requests

from app.model.user import UserData


@pytest.mark.usefixtures("app_url", "insert_users")
class TestUsersPagination:
    path = "/api/users"

    @pytest.mark.parametrize("page, size",
                             [
                                 pytest.param(2, 5, marks=pytest.mark.smoke),
                                 (3, 5), (4, 5),
                                 (2, 6), (1, 12),
                                 (1, 20), (2, 20)
                             ])
    def test_get_users_pagination(self, page, size):
        """Получить пользователей постранично."""
        params = {"page": page, "size": size}
        response = requests.get(f"{self.app_url}{self.path}", params=params)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body["page"] == page
        assert body["size"] == size
        total = body["total"]
        assert len(body["items"]) == (
            size if page * size <= total else (total % size if total > size * (page - 1) else 0))
        for user in body["items"]:
            UserData.model_validate(user)

    @pytest.mark.parametrize("page_1, page_2, size", [(1, 3, 4)])
    def test_get_users_with_diff(self, page_1, page_2, size):
        """Получить пользователей c двух разных страниц."""
        params = {"page": page_1, "size": size}
        response = requests.get(f"{self.app_url}{self.path}", params=params)
        assert response.status_code == HTTPStatus.OK
        body_1 = response.json()
        params = {"page": page_2, "size": size}
        response = requests.get(f"{self.app_url}{self.path}", params=params)
        assert response.status_code == HTTPStatus.OK
        body_2 = response.json()
        assert body_1 != body_2
