import allure

from api.base_api import BaseApi


class ScooterApi(BaseApi):
    @allure.step('Создать курьера')
    def create_courier(self, payload):
        return self.request('POST', '/courier', json=payload)

    @allure.step('Выполнить вход курьера')
    def login_courier(self, payload):
        return self.request('POST', '/courier/login', json=payload)

    @allure.step('Удалить курьера {courier_id}')
    def delete_courier(self, courier_id=None):
        courier_path = '' if courier_id is None else courier_id
        return self.request('DELETE', f'/courier/{courier_path}')

    @allure.step('Создать заказ')
    def create_order(self, payload):
        return self.request('POST', '/orders', json=payload)

    @allure.step('Получить список заказов')
    def list_orders(self, **params):
        return self.request('GET', '/orders', params=params)

    @allure.step('Получить заказ по номеру {track}')
    def get_order(self, track=None):
        params = {} if track is None else {'t': track}
        return self.request('GET', '/orders/track', params=params)

    @allure.step('Отменить заказ {track}')
    def cancel_order(self, track):
        return self.request('PUT', '/orders/cancel', params={'track': track})

    @allure.step('Принять заказ {order_id} курьером {courier_id}')
    def accept_order(self, order_id=None, courier_id=None):
        order_path = '' if order_id is None else order_id
        params = {} if courier_id is None else {'courierId': courier_id}
        return self.request('PUT', f'/orders/accept/{order_path}', params=params)

    @allure.step('Завершить заказ {order_id}')
    def finish_order(self, order_id):
        return self.request('PUT', f'/orders/finish/{order_id}')
