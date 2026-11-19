import allure
import pytest

from data import CREATE_MISSING_DATA, DUPLICATE_LOGIN


@allure.feature('Создание курьера')
class TestCreateCourier:
    @allure.title('Курьер создаётся со всеми обязательными полями')
    def test_create_courier_returns_created_and_ok(self, api, courier_payload):
        response = api.create_courier(courier_payload)
        assert response.status_code == 201, response.text
        assert response.json() == {'ok': True}

    @allure.title('Двух одинаковых курьеров создать нельзя')
    def test_create_duplicate_courier_returns_conflict(self, api, registered_courier):
        response = api.create_courier(registered_courier)
        assert response.status_code == 409, response.text
        assert response.json()['message'].startswith(DUPLICATE_LOGIN)

    @allure.title('Занятый логин нельзя использовать с другим именем и паролем')
    def test_create_courier_with_existing_login_returns_conflict(self, api, registered_courier):
        payload = {**registered_courier, 'password': 'another_password', 'firstName': 'Анна'}
        response = api.create_courier(payload)
        assert response.status_code == 409, response.text
        assert response.json()['message'].startswith(DUPLICATE_LOGIN)

    @allure.title('Создание без обязательного поля {field} возвращает ошибку')
    @pytest.mark.parametrize('field', ['login', 'password', 'firstName'])
    def test_create_courier_without_required_field_returns_bad_request(self, api, courier_payload, field):
        payload = courier_payload.copy()
        payload.pop(field)
        response = api.create_courier(payload)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == CREATE_MISSING_DATA

    @allure.title('Создание с пустым полем {field} возвращает ошибку')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_create_courier_with_empty_credentials_returns_bad_request(self, api, courier_payload, field):
        response = api.create_courier({**courier_payload, field: ''})
        assert response.status_code == 400, response.text
        assert response.json()['message'] == CREATE_MISSING_DATA
