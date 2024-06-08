import inspect
import logging
import socket
from typing import Generator


def get_open_ports(domain_or_ip: str = None, from_port: str = '1', to_port: str = '65535') \
        -> Generator[str, str, int] | None:
    """
    search for open port in a server
    :param domain_or_ip:  domain or ip
    :param from_port: port number for start searching
    :param to_port: port's upper boundary
    :return: port number if it is opened
    """
    logging.info(F"called by: {inspect.stack()[1][3]}")
    from_port, to_port = map(int, [from_port, to_port])
    try:
        socket.inet_aton(domain_or_ip)  # Convert an IPv4 address to 32-bit packed binary format
        ip = domain_or_ip
    except socket.error:
        ip = socket.gethostbyname(domain_or_ip)  # translate a host name to IPv4 address format
    logging.info(F"in in {inspect.currentframe().f_code.co_name}: searching in {ip} for open ports within the range of"
                 F" {from_port}-{to_port}")
    for port in range(from_port, to_port):  # check for all ports in a given range
        try:
            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a new socket
            serv.bind((ip, port))  # bind socket with address
        except socket.error:
            yield F"[OPEN] Port open : {port}"  # yield the open port number
        serv.close()  # close connection


if __name__ == '__main__':
    print(list(get_open_ports(domain_or_ip='127.0.0.1', from_port='1', to_port='65535')))
