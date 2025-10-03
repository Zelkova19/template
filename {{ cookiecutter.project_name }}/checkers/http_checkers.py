import json
from contextlib import contextmanager
from typing import Generator

import allure
import requests


@contextmanager
def check_status_code_http(
    exception: type[Exception] = None,
    expected_status_code: requests.codes = requests.codes.OK,
    expected_message: str = "",
) -> Generator:
    with allure.step("Проверка ответа"):
        try:
            yield
            if expected_status_code != requests.codes.OK:
                raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
            if expected_message:
                raise AssertionError(f'Должно быть получено сообщение "{expected_message}", но запрос прошел успешно')
        except exception as e:
            assert e.status == expected_status_code
            assert json.loads(e.body)["title"] == expected_message
