import random
from http import HTTPStatus
from app.model.user import UserCreate


class TestDeleteUser:
    path = "/api/users"

    def test_delete_user_by_id(self, insert_users, db_service, users_api):
        """Удалить пользователя по ид. (ид рандомное из вставленных в БД)
        Проверки :
        - КО 200 ОК,
        - в БД нет записи с ид удаленнного пользователя.
       """
        user = random.choice(insert_users)
        response = users_api.delete(user.id)
        assert response.status_code == HTTPStatus.OK
        assert db_service.get_user(user.id) is None

    def test_post_delete_get_user(self, users_api):
        """
        1. Создание пользователя, проверка КО 200 ОК
        2. Удаление пользователя, проверка КО 200 ОК
        3. Поиск по ид, КО 404
        """
        user_create = UserCreate.random()
        response = users_api.post(json=user_create.model_dump())
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        id = body["id"]

        response = users_api.delete(id)
        assert response.status_code == HTTPStatus.OK

        response = users_api.get_by_id(id)
        assert response.status_code == HTTPStatus.NOT_FOUND
