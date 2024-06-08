import logging
import pytest
from src.cfg.cfg_global import settings
from importlib.resources import contents
from conftest import cfg_get_data
from src.clients.clients_utils.run_concurrency import run_concurrency
from src.clients.fastapi.tasks_base import app


@pytest.mark.parametrize('test_name', contents(settings.cfg_tests_dir))
def test_perform_tasks(api_client: app, test_name: str) -> None:
    cfg_data = cfg_get_data(test_name)
    task_data = cfg_data['task_data']
    expected_data = cfg_data['return_data']
    api_path = cfg_data['api_path']
    response = api_client.post(api_path, json=task_data)
    res = response.json()
    logging.info(F"response from api-client: {res}")
    assert response.status_code == expected_data['status_code'], \
        F"Expected status code: {expected_data['status_code']}, actual: {response.status_code}"
    if expected_data['validate_resp_val']:
        assert res.get('return_value') == expected_data[
            'return_value'], F"wrong response val: {res['return_value']}, expected: {expected_data['return_value']}"


def test_run_parallel(api_client: object) -> None:
    tests_data = []
    tests_expected_data = []
    for test_name in contents(settings.cfg_tests_dir):
        cfg_data = cfg_get_data(test_name)
        task_data = cfg_data['task_data']
        api_path = cfg_data['api_path']
        expected_data = cfg_data['return_data']
        tests_data.append((api_path, task_data))
        tests_expected_data.append(expected_data)
    res = list(run_concurrency(api_client, tests_data))
    for i in range(len(res)):
        http_resp = res[i]
        expected = tests_expected_data[i]
        json_res = http_resp.json()
        assert http_resp.status_code == expected['status_code'], (F"{res[i].request.url}: Expected status code: "
                                                                  F"{expected['status_code']},"
                                                                  F" actual: {http_resp.status_code},"
                                                                  F"json_data: {json_res}")

