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
    with allure.step('Отменить заказы, созданные тестом'):
        errors = []
        for track in tracks:
            response = api.cancel_order(track)
            if response.status_code != 200 or response.json() != {'ok': True}:
                errors.append(f'{track}: {response.status_code} {response.text}')
        assert not errors, '\n'.join(errors)
