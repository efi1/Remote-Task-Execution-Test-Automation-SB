import inspect
import subprocess
import docker
import logging
from docker.models.containers import Container

CREATE_CMD = 'docker run --name ubuntu_testing -it --rm -d "efiradware/ubuntu-test-updated:latest"'
SEARCH_PID_CMD = 'pstree -p'
RUN_PROCESSES = 'bash run_processes.sh &'

client = docker.from_env()


def get_pids(s):
    res = []
    digits = []
    for i in range(len(s)):
        if s[i].isdigit():
            digits.append(s[i])
            continue
        if digits:
            res.append(''.join(digits))
            digits.clear()
    return res


def is_docker_installed() -> bool:
    res = subprocess.run('docker ps', capture_output=True)
    if len(res.stderr) > 0:
        return False
    return True


def get_processes(pid) -> list:
    def get_container(containers: list, c_id: str) -> Container:
        for c in containers:
            if c.id == c_id:
                return c

    logging.info(F"called by: {inspect.stack()[1][3]}")
    logging.info(F"in {inspect.currentframe().f_code.co_name}")
    logging.info('creating docker container')
    res_creation = subprocess.run(CREATE_CMD, capture_output=True)  # create docker container
    assert len(res_creation.stderr) == 0, F"failed to create container: {res_creation.stderr}"
    container_id = res_creation.stdout.decode('utf-8').strip()  # get container id
    logging.info(F"container: {container_id} created")
    l_containers = client.containers.list()
    container = get_container(l_containers, container_id)  # get container object
    assert container, 'no container available'
    try:
        logging.info(F"connect to container's bash")
        container.exec_run(cmd=['/bin/bash', '-c', RUN_PROCESSES])  # connect into container bash
        logging.info(F"in bash executing command: '{SEARCH_PID_CMD} {pid}'")
        res = container.exec_run(cmd=['/bin/bash', '-c', F"{SEARCH_PID_CMD} {pid}"])  # execute bash command
        processes = get_pids(res.output.decode('utf-8'))
    except Exception as e:
        logging.info(F'failed running scripts in container: {e}')
        container.stop()  # remove container
        raise
    logging.info('remove container')
    container.stop()
    return processes


if __name__ == '__main__':
    is_docker_installed = is_docker_installed()
    result = get_processes(1)
    print(result)
