import allure
import pytest

from data import ACCEPT_COURIER_NOT_FOUND, ACCEPT_ORDER_NOT_FOUND, SEARCH_MISSING_DATA


@pytest.mark.extra
@allure.feature('Принятие заказа')
class TestAcceptOrder:
    @allure.title('Курьер принимает существующий заказ')
    def test_accept_order_returns_ok(self, api, courier_id, created_order):
        response = api.accept_order(created_order['id'], courier_id)
        assert response.status_code == 200, response.text
        assert response.json() == {'ok': True}

    @allure.title('Принятие заказа без id курьера возвращает ошибку')
    def test_accept_order_without_courier_returns_bad_request(self, api, created_order):
        response = api.accept_order(order_id=created_order['id'])
        assert response.status_code == 400, response.text
        assert response.json()['message'] == SEARCH_MISSING_DATA

    @allure.title('Несуществующий курьер не может принять заказ')
    def test_accept_order_with_nonexistent_courier_returns_not_found(self, api, deleted_courier_id, created_order):
        response = api.accept_order(created_order['id'], deleted_courier_id)
        assert response.status_code == 404, response.text
        assert response.json()['message'] == ACCEPT_COURIER_NOT_FOUND

    @allure.title('Принятие заказа без id заказа возвращает ошибку')
    def test_accept_order_without_order_id_returns_bad_request(self, api, courier_id):
        response = api.accept_order(courier_id=courier_id)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == SEARCH_MISSING_DATA

    @allure.title('Несуществующий заказ нельзя принять')
    def test_accept_nonexistent_order_returns_not_found(self, api, courier_id):
        response = api.accept_order(order_id=-1, courier_id=courier_id)
        assert response.status_code == 404, response.text
        assert response.json()['message'] == ACCEPT_ORDER_NOT_FOUND
