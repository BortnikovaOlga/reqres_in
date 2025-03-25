from http import HTTPStatus

import pytest

from app.model.user import UsersDataPage


@pytest.mark.usefixtures("insert_users")
class TestUsersPagination:
    path = "/api/users"

    @pytest.mark.parametrize("page, size",
                             [
                                 pytest.param(2, 5, marks=pytest.mark.smoke),
                                 (3, 5), (4, 5),
                                 (2, 6), (1, 12),
                                 (1, 20), (2, 20)
                             ])
    def test_get_users_pagination(self, page, size, users_api):
        """Получить пользователей постранично. Проверки :
        - КО 200 ОК,
        - в ответе поля page, size содержат числа из параметров запроса
        - количество пользователей по формуле, в зависимости от получаемой страницы"""

        response = users_api.get_paginated(page, size)

        assert response.status_code == HTTPStatus.OK
        data = UsersDataPage.model_validate(response.json())
        assert data.page == page
        assert data.size == size
        assert len(data.items) == (size if size * page <= data.total else
                                   (data.total % size if size * (page - 1) < data.total
                                    else 0))

    @pytest.mark.parametrize("size", [5, 12, 50])
    def test_check_pages_count(self, size, users_api):
        """Получить данные страницы 1 без указания page. Проверки :
        - КО 200 ОК,
        - вернулась страница 1.
        - количество страниц - проверка по формуле, зависит от size.
        """
        response = users_api.get_paginated(size=size)

        assert response.status_code == HTTPStatus.OK
        data = UsersDataPage.model_validate(response.json())
        assert data.page == 1
        assert data.pages == (data.total // size + 1 if data.total % size else data.total // size)

    @pytest.fixture
    def get_users_data_page(self, request, users_api):
        """фикстура, вернет данные страницы заданой первым параметром из параметризации."""
        page_1, page_2, size = request.param
        response = users_api.get_paginated(page_1, size)

        assert response.status_code == HTTPStatus.OK
        data_1 = UsersDataPage.model_validate(response.json())
        return data_1, page_2, size

    @pytest.mark.parametrize("get_users_data_page", [(2, 3, 4), (1, 2, 8)], indirect=True)
    def test_get_users_with_diff(self, get_users_data_page, users_api):
        """Получить пользователей c двух разных страниц. Проверки :
        - КО 200 ОК,
        - множества ид пользователей с разных страниц - разные множества."""
        data_1, page_2, size = get_users_data_page
        response = users_api.get_paginated(page_2, size)

        assert response.status_code == HTTPStatus.OK
        data_2 = UsersDataPage.model_validate(response.json())
        assert set([user.id for user in data_1.items]) != set([user.id for user in data_2.items])
