import pytest
from http import HTTPStatus
from app.model.auth import LoginResponse


class TestLogin:

    @pytest.mark.smoke
    def test_auth_with_valid_data(self, envs, login_api):
        """Авторизация с валидным логином и паролем."""
        response = login_api.login(
            json={
                "email": envs.test_username,
                "password": envs.test_password
            })
        assert response.status_code == HTTPStatus.OK
        body = LoginResponse.model_validate(response.json())
        assert body.token

    @pytest.mark.parametrize("password", ["", " ", "cityslick"])
    def test_auth_with_invalid_password(self, password, envs, login_api):
        """Авторизация с невалидным паролем."""
        response = login_api.login(
            json={
                "email": envs.test_username,
                "password": password
            })
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize("login", ["", " ", "eve.holt"])
    def test_auth_with_invalid_login(self, login, login_api):
        """Авторизация с невалидным логином."""
        response = login_api.login(json={"email": login, "password": "password"})
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize("auth_data", [{"email": "", "password": ""}, {"email": " ", "password": " "}])
    def test_auth_with_invalid_login_password(self, auth_data, login_api):
        """Авторизация с пустыми логином/паролем."""
        response = login_api.login(json=auth_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize("auth_data", [{"email": "1@1.ru"}, {"password": "password"}])
    def test_auth_with_invalid_data(self, auth_data, login_api):
        """Авторизация с невалидной структурой запроса - отсутствует логин или пароль."""
        response = login_api.login(json=auth_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
