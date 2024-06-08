import socket
import requests
import justext
from fastapi import APIRouter, Request, HTTPException
from src.clients.fastapi.schemas import TaskInput, TaskOutput
import src.clients.clients_utils.other_utils as utils
from src.clients.clients_utils.http_server_handler import HTTPServer
import src.clients.clients_utils.port_scanner as port_scanner
import src.clients.clients_utils.pid_processes as pid_processes
import src.clients.clients_utils.cli_linux_client as cli_linux_client
import src.clients.clients_utils.registry_handler as registry_handler

router = APIRouter(prefix="/api/tasks")
land_page = APIRouter()


@land_page.get("/")
def welcome():
    """returns friendly welcome message"""
    return {"message": F"Welcome to tasks handler"}


@router.post("/resolve_ip", response_model=TaskOutput)
async def resolve_ip(task_data: TaskInput) -> TaskOutput:
    """
    resolve the ip address of a given domain name.
    :param task_data: domain name.
    :return: resolved ip address.
    """
    params = task_data.task_parameters
    url = params.get('domain')
    if url:
        s = socket.gethostbyname(url)
    else:
        raise HTTPException(status_code=404, detail=F"no Domain was given")
    output = TaskOutput(return_value=s, **vars(task_data))
    return output


@router.post("/perform_http_request", response_model=TaskOutput)
async def perform_http_request(task_data: TaskInput) -> TaskOutput:
    """
    perform a request of a given method
    :param task_data: Server's Domain/IP, server's port, request method (e.g. GET), requested path.
    :return: body returned from the request.
    """
    params = task_data.task_parameters
    domain = params.get('domain')
    method = params.get('method')
    port = params.get('port')
    path = params.get('path')
    uri = F"{domain}:{port}{path}"
    try:
        s = getattr(requests, method)(uri).content
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"invalid params, {e}")
    paragraphs = justext.justext(s, justext.get_stoplist("English"))
    s = ' '.join([p.text for p in paragraphs])
    output = TaskOutput(return_value=s, **vars(task_data))
    return output


@router.post("/start_http_server", response_model=TaskOutput)
async def start_http_server(task_data: TaskInput, request: Request) -> TaskOutput:
    """
    start an http server and get the ip of the requester.
    :param task_data: Server's page uri, port, Data to return when accessing the page, requester of this call.
    :param request: The requester of this resource
    :return: requester of this call and the returned data from the requested page.
    """
    params = task_data.task_parameters
    page_uri = params.get('page_uri')
    port = params.get('port')
    uri = F"{page_uri}:{port}"
    with HTTPServer(port=port, url=page_uri):
        try:
            requests.get(uri)
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=404, detail=F"get request failed: {e}")
    client_ip = request.client.host
    output = TaskOutput(return_value=client_ip, **vars(task_data))
    return output


@router.post("/port_scan", response_model=TaskOutput)
async def port_scan(task_data: TaskInput) -> TaskOutput:
    """
    Scan open ports of a given domain or an IP
    :param task_data: domain or an IP
    :return: all open ports within a given port range.
    """
    params = utils.dict_to_obj(task_data.task_parameters)
    try:
        resp = list(port_scanner.get_open_ports(**vars(params)))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"failed to scan open port with the given domain/ip. "
                                                    f"parameters are: {task_data.task_parameters}, {e}")
    output = TaskOutput(return_value=resp, **vars(task_data))
    return output


@router.post("/process_tree", response_model=TaskOutput)
async def process_tree(task_data: TaskInput) -> TaskOutput:
    """
    Getting subprocesses of a given PID from a docker Ubuntu container.
    :param task_data: PID parameter of which to extract all its subprocesses
    :return: a list of pid-s (embedded within a TaskOutput - BaseModel object)
    """
    is_docker_installed = pid_processes.is_docker_installed()
    pid = task_data.task_parameters.get('pid')
    if is_docker_installed:
        resp = pid_processes.get_processes(pid)
        output = TaskOutput(return_value=resp, **vars(task_data))
        return output
    else:
        raise HTTPException(status_code=404, detail=f"No docker engine - can't create nor connect")


@router.post("/process_tree_cli", response_model=TaskOutput)
async def process_tree(task_data: TaskInput) -> TaskOutput:
    """
    another option of getting PID-s, by connecting remotely to server's - PID-s
    It supposed to be failed, since no username/password are supplied.
    :param task_data: PID parameter of which to extract all its subprocesses.
    :return: a list of pid-s (embedded within a TaskOutput - BaseModel object)
    """
    params = task_data.task_parameters
    try:
        linux_client = cli_linux_client.LinuxCliClient('<some ip>', '<password>')
    except socket.error as e:
        raise HTTPException(status_code=404, detail=f"linux client failed to connect the server: {e}")
    resp = linux_client.invoke_linux_cmd(params.get('pid'))
    output = TaskOutput(return_value=resp, **vars(task_data))
    return output


@router.post("/registry", response_model=TaskOutput)
async def registry(task_data: TaskInput) -> TaskOutput:
    """
    read, update or delete windows' key
    :param task_data: action(GET, SET, DELETE), registry key (sub_key) and value to be edited with (when updating).
    :return: Success/Fail status
    """
    actions = {"GET": "read_key", "SET": "update_key", "DELETE": "delete_key"}
    params = task_data.task_parameters
    action_param = params.get('action')
    action = actions.get(action_param)
    key = params.get('key')
    value = params.get('value')
    if not all([action, key]):
        raise HTTPException(status_code=404, detail=f"empty parameters given")
    handler = registry_handler.RegistryHandler()
    resp = getattr(handler, action)(key, value)
    output = TaskOutput(return_value=resp, **vars(task_data))
    return output

