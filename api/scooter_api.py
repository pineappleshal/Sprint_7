from api.base_api import BaseApi


class ScooterApi(BaseApi):
    def create_courier(self, payload):
        return self.request('POST', '/courier', json=payload)

    def login_courier(self, payload):
        return self.request('POST', '/courier/login', json=payload)

    def delete_courier(self, courier_id=None):
        courier_path = '' if courier_id is None else courier_id
        return self.request('DELETE', f'/courier/{courier_path}')

    def create_order(self, payload):
        return self.request('POST', '/orders', json=payload)

    def list_orders(self, **params):
        return self.request('GET', '/orders', params=params)

    def get_order(self, track=None):
        params = {} if track is None else {'t': track}
        return self.request('GET', '/orders/track', params=params)

    def cancel_order(self, track):
        return self.request('PUT', '/orders/cancel', params={'track': track})

    def accept_order(self, order_id=None, courier_id=None):
        order_path = '' if order_id is None else order_id
        params = {} if courier_id is None else {'courierId': courier_id}
        return self.request('PUT', f'/orders/accept/{order_path}', params=params)

    def finish_order(self, order_id):
        return self.request('PUT', f'/orders/finish/{order_id}')
