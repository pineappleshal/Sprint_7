import allure
import pytest

from data import ORDER_NOT_FOUND, SEARCH_MISSING_DATA


@pytest.mark.extra
@allure.feature('Получение заказа по номеру')
class TestGetOrder:
    @allure.title('Получение созданного заказа по трек-номеру')
    def test_get_order_returns_order(self, api, order_factory, order_payload):
        created = order_factory(order_payload)
        assert created.status_code == 201, created.text
        track = created.json()['track']
        response = api.get_order(track)
        assert response.status_code == 200, response.text
        order = response.json().get('order')
        assert isinstance(order, dict)
        assert order['track'] == track
        assert type(order['id']) is int and order['id'] > 0
        assert order['firstName'] == order_payload['firstName']
        assert order['lastName'] == order_payload['lastName']
        assert order['address'] == order_payload['address']
        assert order['comment'] == order_payload['comment']

    @allure.title('Получение заказа без номера возвращает ошибку')
    def test_get_order_without_track_returns_bad_request(self, api):
        response = api.get_order()
        assert response.status_code == 400, response.text
        assert response.json()['message'] == SEARCH_MISSING_DATA

    @allure.title('Получение несуществующего заказа возвращает ошибку')
    def test_get_nonexistent_order_returns_not_found(self, api):
        response = api.get_order(track=2_147_483_647)
        assert response.status_code == 404, response.text
        assert response.json()['message'] == ORDER_NOT_FOUND
