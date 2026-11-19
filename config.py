import os


BASE_URL = os.getenv('SCOOTER_BASE_URL', 'https://qa-scooter.education-services.ru/api/v1')
REQUEST_TIMEOUT = (5, 20)
