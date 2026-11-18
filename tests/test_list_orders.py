import allure


@allure.feature('Список заказов')
class TestListOrders:
    @allure.title('Ответ содержит список заказов и сведения о пагинации')
    def test_list_orders_returns_order_list(self, api, order_factory, order_payload):
        created = order_factory(order_payload)
        assert created.status_code == 201, created.text
        response = api.list_orders(limit=10, page=0)
        assert response.status_code == 200, response.text
        body = response.json()
        assert isinstance(body.get('orders'), list)
        assert 0 < len(body['orders']) <= 10
        assert all(isinstance(order, dict) and 'id' in order for order in body['orders'])
        assert body['pageInfo']['page'] == 0
        assert body['pageInfo']['limit'] == 10
