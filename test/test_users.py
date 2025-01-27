from http import HTTPStatus

import pytest
import requests

from model.user import UserData


@pytest.mark.usefixtures("app_url")
class TestUsers:
    path = "/api/users"

    @pytest.mark.smoke
    def test_get_all_users(self, db_users):
        """Получить всех пользователей."""
        response = requests.get(f"{self.app_url}{self.path}")
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        total = len(db_users)
        assert len(body["items"]) == total, f"В теле ответа ожидалось {total} количество записей"
        assert body["total"] == total

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

    @pytest.mark.parametrize("user_id", [1, 5, 12])
    def test_get_user_by_id(self, user_id, db_users):
        """Получить пользователя по ид."""
        response = requests.get(f"{self.app_url}{self.path}/{user_id}")
        assert response.status_code == HTTPStatus.OK
        body = UserData.model_validate(response.json())
        assert body == UserData(**db_users[user_id]), "В теле ответа ожидались другие данные"

    @pytest.mark.parametrize("user_id", [-10, 0, 100])
    def test_get_user_by_not_exist_id(self, user_id):
        """Получить пользователя с несуществующим ид."""
        response = requests.get(f"{self.app_url}{self.path}/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", ["one"])
    def test_get_user_by_invalid_id(self, user_id):
        """Запрос пользователя с невалидным ид."""
        response = requests.get(f"{self.app_url}{self.path}/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
