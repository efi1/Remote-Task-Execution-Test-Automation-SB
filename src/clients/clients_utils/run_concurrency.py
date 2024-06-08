import inspect
from queue import Queue
from threading import Thread
import logging


def run_concurrency(api_client, tests_data):
    """
    run api requests in parallel using thread.
    :param api_client: FastAPI client.
    :param tests_data: data required for the test execution.
    :return: execution results of the entire tests.
    """
    que = Queue()
    threads_list = list()
    logging.info(F"called by: {inspect.stack()[1][3]}")
    logging.info(F"in {inspect.currentframe().f_code.co_name}")
    for path, json_data, test_name in tests_data:
        t = Thread(target=lambda q, arg1, arg2, arg3: q.put({arg3: api_client.post(url=arg1, json=arg2)}),
                   args=(que, path, json_data, test_name), name=test_name)
        logging.info(F"starting thread: {t}")
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

    while not que.empty():
        result = que.get()
        yield result
