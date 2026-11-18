from api.base_api import BaseApi


class ScooterApi(BaseApi):
    def create_courier(self, payload):
        return self.request('POST', '/courier', json=payload)

    def login_courier(self, payload):
        return self.request('POST', '/courier/login', json=payload)

    def delete_courier(self, courier_id):
        return self.request('DELETE', f'/courier/{courier_id}')

    def create_order(self, payload):
        return self.request('POST', '/orders', json=payload)

    def list_orders(self, **params):
        return self.request('GET', '/orders', params=params)

    def get_order(self, track):
        return self.request('GET', '/orders/track', params={'t': track})

    def cancel_order(self, track):
        return self.request('PUT', '/orders/cancel', params={'track': track})
