import allure
import pytest

from data import COURIER_NOT_FOUND, DELETE_MISSING_ID


@pytest.mark.extra
@allure.feature('Удаление курьера')
class TestDeleteCourier:
    @allure.title('Удаление существующего курьера возвращает ok')
    def test_delete_courier_returns_ok(self, api, courier_id):
        response = api.delete_courier(courier_id)
        assert response.status_code == 200, response.text
        assert response.json() == {'ok': True}

    @allure.title('Удаление курьера без id возвращает ошибку')
    def test_delete_courier_without_id_returns_bad_request(self, api):
        response = api.delete_courier()
        assert response.status_code == 400, response.text
        assert response.json()['message'] == DELETE_MISSING_ID

    @allure.title('Удаление несуществующего курьера возвращает ошибку')
    def test_delete_nonexistent_courier_returns_not_found(self, api, deleted_courier_id):
        response = api.delete_courier(deleted_courier_id)
        assert response.status_code == 404, response.text
        assert response.json()['message'].rstrip('.') == COURIER_NOT_FOUND
