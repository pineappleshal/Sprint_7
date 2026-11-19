from datetime import date, timedelta
from uuid import uuid4


CREATE_MISSING_DATA = 'Недостаточно данных для создания учетной записи'
LOGIN_MISSING_DATA = 'Недостаточно данных для входа'
ACCOUNT_NOT_FOUND = 'Учетная запись не найдена'
DUPLICATE_LOGIN = 'Этот логин уже используется'
DELETE_MISSING_ID = 'Недостаточно данных для удаления курьера'
COURIER_NOT_FOUND = 'Курьера с таким id нет'
SEARCH_MISSING_DATA = 'Недостаточно данных для поиска'
ACCEPT_COURIER_NOT_FOUND = 'Курьера с таким id не существует'
ACCEPT_ORDER_NOT_FOUND = 'Заказа с таким id не существует'
ORDER_NOT_FOUND = 'Заказ не найден'


def make_courier():
    return {
        'login': f'sprint7_{uuid4().hex}',
        'password': uuid4().hex,
        'firstName': 'Валерия',
    }


def make_order():
    return {
        'firstName': 'Анна',
        'lastName': 'Иванова',
        'address': 'Москва, улица Лесная, дом 10',
        'metroStation': '4',
        'phone': '+79000000001',
        'rentTime': 2,
        'deliveryDate': (date.today() + timedelta(days=2)).isoformat(),
        'comment': f'Учебный заказ {uuid4().hex}',
    }
