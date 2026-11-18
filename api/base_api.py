import json

import allure
import requests

from config import BASE_URL, REQUEST_TIMEOUT


class BaseApi:
    def __init__(self):
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        url = f'{BASE_URL.rstrip("/")}/{path.lstrip("/")}'
        with allure.step(f'{method} {path}'):
            allure.attach(json.dumps(kwargs, ensure_ascii=False, indent=2),
                          'Параметры запроса', allure.attachment_type.JSON)
            response = self.session.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
            allure.attach(str(response.status_code), 'Код ответа', allure.attachment_type.TEXT)
            allure.attach(response.text, 'Тело ответа', allure.attachment_type.TEXT)
            return response

    def close(self):
        self.session.close()
