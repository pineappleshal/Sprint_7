import allure
import pytest

from data import ACCOUNT_NOT_FOUND, LOGIN_MISSING_DATA, make_courier


@allure.feature('Логин курьера')
class TestLoginCourier:
    @allure.title('Успешный вход возвращает id курьера')
    def test_login_returns_courier_id(self, api, registered_courier):
        credentials = {key: registered_courier[key] for key in ('login', 'password')}
        response = api.login_courier(credentials)
        assert response.status_code == 200, response.text
        assert type(response.json().get('id')) is int
        assert response.json()['id'] > 0

    @allure.title('Вход без обязательного поля {field} возвращает ошибку')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_login_without_required_field_returns_bad_request(self, api, registered_courier, field):
        credentials = {key: registered_courier[key] for key in ('login', 'password') if key != field}
        response = api.login_courier(credentials)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == LOGIN_MISSING_DATA

    @allure.title('Вход с пустым полем {field} возвращает ошибку')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_login_with_empty_field_returns_bad_request(self, api, registered_courier, field):
        credentials = {key: registered_courier[key] for key in ('login', 'password')}
        credentials[field] = ''
        response = api.login_courier(credentials)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == LOGIN_MISSING_DATA

    @allure.title('Вход с неправильным полем {field} возвращает ошибку')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_login_with_wrong_credentials_returns_not_found(self, api, registered_courier, field):
        credentials = {key: registered_courier[key] for key in ('login', 'password')}
        credentials[field] = make_courier()[field]
        response = api.login_courier(credentials)
        assert response.status_code == 404, response.text
        assert response.json()['message'] == ACCOUNT_NOT_FOUND

    @allure.title('Несуществующий курьер не может войти')
    def test_login_nonexistent_courier_returns_not_found(self, api):
        payload = make_courier()
        response = api.login_courier({key: payload[key] for key in ('login', 'password')})
        assert response.status_code == 404, response.text
        assert response.json()['message'] == ACCOUNT_NOT_FOUND
