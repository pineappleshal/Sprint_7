import allure
import pytest

from api.scooter_api import ScooterApi
from data import make_courier, make_order


@pytest.fixture
def api():
    client = ScooterApi()
    yield client
    client.close()


@pytest.fixture
def courier_payload(api):
    payload = make_courier()
    yield payload
    with allure.step('Удалить созданного в тесте курьера'):
        response = api.login_courier({key: payload[key] for key in ('login', 'password')})
        if response.status_code == 200:
            deleted = api.delete_courier(response.json()['id'])
            assert deleted.status_code == 200, deleted.text
            assert deleted.json() == {'ok': True}
        else:
            assert response.status_code == 404, response.text


@pytest.fixture
def registered_courier(api, courier_payload):
    with allure.step('Создать уникального курьера для теста'):
        response = api.create_courier(courier_payload)
        assert response.status_code == 201, response.text
        assert response.json() == {'ok': True}
    return courier_payload


@pytest.fixture
def courier_id(api, registered_courier):
    with allure.step('Получить id созданного курьера'):
        response = api.login_courier({key: registered_courier[key] for key in ('login', 'password')})
        assert response.status_code == 200, response.text
        value = response.json()['id']
        assert type(value) is int and value > 0
        return value


@pytest.fixture
def deleted_courier_id(api, courier_id):
    with allure.step('Удалить тестового курьера для проверки несуществующего id'):
        response = api.delete_courier(courier_id)
        assert response.status_code == 200, response.text
        assert response.json() == {'ok': True}
    return courier_id


@pytest.fixture
def order_payload():
    return make_order()


@pytest.fixture
def order_factory(api):
    tracks = []

    def create(payload):
        response = api.create_order(payload)
        if response.status_code == 201:
            track = response.json().get('track')
            if type(track) is int:
                tracks.append(track)
        return response

    yield create
    with allure.step('Отменить или завершить заказы, созданные тестом'):
        errors = []
        for track in tracks:
            response = api.cancel_order(track)
            if response.status_code == 409:
                order = api.get_order(track)
                if order.status_code != 200:
                    errors.append(f'{track}: не удалось получить заказ: {order.status_code} {order.text}')
                    continue
                response = api.finish_order(order.json()['order']['id'])
            if response.status_code != 200 or response.json() != {'ok': True}:
                errors.append(f'{track}: {response.status_code} {response.text}')
        assert not errors, '\n'.join(errors)


@pytest.fixture
def created_order(api, order_factory, order_payload):
    with allure.step('Создать заказ и получить его id'):
        response = order_factory(order_payload)
        assert response.status_code == 201, response.text
        track = response.json()['track']
        details = api.get_order(track)
        assert details.status_code == 200, details.text
        order = details.json()['order']
        assert order['track'] == track
        assert type(order['id']) is int and order['id'] > 0
        return order
