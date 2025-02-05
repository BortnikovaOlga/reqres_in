from http import HTTPStatus

import pytest
import requests

from model.user import UserData, UsersDataPage


@pytest.mark.usefixtures("app_url")
class TestUsers:
    path = "/api/users"

    @pytest.mark.smoke
    def test_get_all_users(self, db_users):
        """Получить всех пользователей. Проверки :
         - КО 200 ОК,
         - количество пользователей в ответе совпадает с числом пользователей в массиве,
         - поле total содержит то же число. """
        response = requests.get(f"{self.app_url}{self.path}")
        assert response.status_code == HTTPStatus.OK
        page_data = UsersDataPage.model_validate(response.json())
        total_db = len(db_users)
        total_items = len(page_data.items)
        assert total_items == total_db, f"В теле ответа ожидалось {total_db} записей"
        assert page_data.total == total_items

    @pytest.mark.parametrize("page, size",
                             [
                                 pytest.param(2, 5, marks=pytest.mark.smoke),
                                 (3, 5), (4, 5),
                                 (2, 6), (1, 12),
                                 (1, 20), (2, 20)
                             ])
    def test_get_users_pagination(self, page, size):
        """Получить пользователей постранично. Проверки :
        - КО 200 ОК,
        - в ответе поля page, size содержат числа из параметров запроса
        - количество пользователей по формуле, в зависимости от получаемой страницы"""
        params = {"page": page, "size": size}
        response = requests.get(f"{self.app_url}{self.path}", params=params)
        assert response.status_code == HTTPStatus.OK
        data = UsersDataPage.model_validate(response.json())
        assert data.page == page
        assert data.size == size
        assert len(data.items) == (size if size * page <= data.total else
                                   (data.total % size if size * (page - 1) < data.total
                                    else 0))

    @pytest.fixture
    def get_users_data_page(self, request):
        """фикстура, вернет данные страницы заданой первым параметром из параметризации."""
        page_1, page_2, size = request.param
        params = {"page": page_1, "size": size}
        response = requests.get(f"{self.app_url}{self.path}", params=params)
        assert response.status_code == HTTPStatus.OK
        data_1 = UsersDataPage.model_validate(response.json())
        return data_1, page_2, size

    @pytest.mark.parametrize("get_users_data_page", [(2, 3, 4), (1, 2, 8)], indirect=True)
    def test_get_users_with_diff(self, get_users_data_page):
        """Получить пользователей c двух разных страниц. Проверки :
        - КО 200 ОК,
        - ид пользователей с разных страниц - разные множества."""
        data_1, page_2, size = get_users_data_page
        params = {"page": page_2, "size": size}
        response = requests.get(f"{self.app_url}{self.path}", params=params)
        assert response.status_code == HTTPStatus.OK
        data_2 = UsersDataPage.model_validate(response.json())
        assert set([user.id for user in data_1.items]) != set([user.id for user in data_2.items])

    @pytest.mark.parametrize("size", [5, 12, 20])
    def test_check_pages_count(self, size):
        """Получить данные страниц без указания page. Проверки :
        - КО 200 ОК,
        - вернулась страница 1.
        - количество страниц проверка по формуле, зависит от size.
        """
        response = requests.get(f"{self.app_url}{self.path}", params={"size": size})
        assert response.status_code == HTTPStatus.OK
        data = UsersDataPage.model_validate(response.json())
        assert data.pages == (data.total // size + 1 if data.total % size else data.total // size)

    @pytest.mark.parametrize("user_id", [1, 5, 12])
    def test_get_user_by_id(self, user_id, db_users):
        """Получить пользователя по ид. Проверки :
        - КО 200 ОК,
        - данные пользователя из ответа совпадают с данными пользователя в 'БД' "
        """
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
