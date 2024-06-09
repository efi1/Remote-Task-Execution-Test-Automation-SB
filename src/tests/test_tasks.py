import logging
import pytest
from src.cfg.cfg_global import settings
from importlib.resources import files
from conftest import cfg_get_data
from src.clients.clients_utils.run_concurrency import run_concurrency
from src.clients.fastapi.tasks_base import app


@pytest.mark.parametrize('test_name', [resource.name for resource in files(settings.cfg_tests_dir).iterdir()])
def test_perform_tasks(api_client: app, test_name: str) -> None:
    """
    Testing various task using the files in src.cfg.cfg_tests as input (parameterized test)
    :param api_client: the FastAPI client
    :param test_name: test name as taken from src.cfg.cfg_tests folder
    :return:
    """
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


def test_run_parallel(api_client: app) -> None:
    """
    Run the same tests as in 'test_perform_tasks' above, but concurrently.
    :param api_client: api_client: the FastAPI client
    :return: test name
    """
    tests_data = []
    tests_expected_data = {}
    for resource in files(settings.cfg_tests_dir).iterdir():
        cfg_name = resource.name
        cfg_data = cfg_get_data(cfg_name)
        task_data = cfg_data['task_data']
        api_path = cfg_data['api_path']
        expected_data = cfg_data['return_data']
        tests_data.append((api_path, task_data, cfg_name))
        tests_expected_data[cfg_name] = expected_data
    res = list(run_concurrency(api_client, tests_data))
    for elem in res:
        cfg_name = list(elem)[0]
        http_resp = elem[cfg_name]
        expected = tests_expected_data.get(cfg_name)
        json_res = http_resp.json()
        assert http_resp.status_code == expected['status_code'], (F"{http_resp.request.url}: Expected status code: "
                                                                  F"{expected['status_code']},"
                                                                  F" actual: {http_resp.status_code},"
                                                                  F"json_data: {json_res}")
