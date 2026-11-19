import allure
import pytest


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с вариантом цвета: {color}')
    @pytest.mark.parametrize('color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], [], None],
                             ids=['black', 'grey', 'both', 'empty-color-list', 'without-color'])
    def test_create_order_returns_track(self, order_factory, order_payload, color):
        if color is not None:
            order_payload['color'] = color
        response = order_factory(order_payload)
        assert response.status_code == 201, response.text
        assert type(response.json().get('track')) is int
        assert response.json()['track'] > 0
