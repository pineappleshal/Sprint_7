import allure
import pytest
import requests

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
        if response.status_code == 404:
            return
        response.raise_for_status()
        api.delete_courier(response.json()['id']).raise_for_status()


@pytest.fixture
def registered_courier(api, courier_payload):
    with allure.step('Создать уникального курьера для теста'):
        response = api.create_courier(courier_payload)
        response.raise_for_status()
    return courier_payload


@pytest.fixture
def courier_id(api, registered_courier):
    with allure.step('Получить id созданного курьера'):
        response = api.login_courier({key: registered_courier[key] for key in ('login', 'password')})
        response.raise_for_status()
        return response.json()['id']


@pytest.fixture
def deleted_courier_id(api, courier_id):
    with allure.step('Удалить тестового курьера для проверки несуществующего id'):
        response = api.delete_courier(courier_id)
        response.raise_for_status()
    return courier_id


@pytest.fixture
def order_payload():
    return make_order()


@pytest.fixture
def order_factory(api):
    tracks = []

    def create(payload):
        response = api.create_order(payload)
        if response.ok:
            track = response.json().get('track')
            if track is not None:
                tracks.append(track)
        return response

    yield create
    with allure.step('Отменить или завершить заказы, созданные тестом'):
        errors = []
        for track in tracks:
            try:
                response = api.cancel_order(track)
                if response.status_code == 409:
                    order = api.get_order(track)
                    order.raise_for_status()
                    response = api.finish_order(order.json()['order']['id'])
                response.raise_for_status()
            except (requests.RequestException, KeyError, ValueError) as error:
                errors.append(f'{track}: {error}')
        if errors:
            raise RuntimeError('Не удалось очистить тестовые заказы:\n' + '\n'.join(errors))


@pytest.fixture
def created_order_track(order_factory, order_payload):
    with allure.step('Создать заказ для теста'):
        response = order_factory(order_payload)
        response.raise_for_status()
        return response.json()['track']


@pytest.fixture
def created_order(api, created_order_track):
    with allure.step('Получить данные подготовленного заказа'):
        response = api.get_order(created_order_track)
        response.raise_for_status()
        return response.json()['order']
