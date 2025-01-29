from http import HTTPStatus

import pytest
import requests

from app.model.app_status import AppStatus


@pytest.mark.smoke
@pytest.mark.usefixtures("app_url")
class TestStatus:
    path = "/api/status"

    def test_check_status(self):
        """проверить, что api-сервис отвечает."""
        response = requests.get(f"{self.app_url}{self.path}")
        assert response.status_code == HTTPStatus.OK
        body = AppStatus.model_validate(response.json())
        assert body.database
