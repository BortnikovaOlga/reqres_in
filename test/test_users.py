import pytest
import requests


class TestUsers:
    url = f"http://127.0.0.1:8080/api/users"

    def test_get_user(self, users):
        """Получить всех пользователей."""
        response = requests.get(self.url)
        assert response.status_code == 200
        body = response.json()
        assert len(body) == len(users), "В теле ответа ожидалось другое количество записей"

    @pytest.mark.parametrize("user_id", [1, 5, 12])
    def test_get_user_by_id(self, user_id, users):
        """Получить пользователя по ид."""
        response = requests.get(f"{self.url}/{user_id}")
        assert response.status_code == 200
        body = response.json()
        assert body == users[user_id], "В теле ответа ожидались другие данные"

    @pytest.mark.parametrize("user_id", [-10, 0, 100])
    def test_get_user_by_not_exist_id(self, user_id):
        """Получить пользователя с несуществующим ид."""
        response = requests.get(f"{self.url}/{user_id}")
        assert response.status_code == 404

    @pytest.mark.parametrize("user_id", ["one"])
    def test_get_user_by_invalid_id(self, user_id):
        """Запрос пользователя с невалидным ид."""
        response = requests.get(f"{self.url}/{user_id}")
        assert response.status_code == 422