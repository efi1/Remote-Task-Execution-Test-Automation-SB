import re
import logging
import paramiko
import time


class LinuxCliClient(object):
    def __init__(self, ip, user_name='root', password=None, timeout=30, logger=None, stdout=False,
                 prompt_char='#', conn_timeout=None):
        """
        connect via ssh and run linux command
        :param ip: ip for ssh connection
        :param user_name: user
        :param password: password
        :param timeout: timeout for connection establishment
        :param logger: logger
        :param stdout - should the invoke_linux_cmd function return the linux shell command output:
        """
        self.ip = ip
        self.user_name = user_name
        self.password = password
        self.timeout = timeout
        self.conn_timeout = conn_timeout
        self.logger = logger
        self.stdout = stdout
        self.prompt_char = prompt_char
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, 22, self.user_name, self.password, timeout=self.conn_timeout)
        transport = self.ssh.get_transport()
        self.session = transport.open_session()
        self.session.get_pty()
        self.session.invoke_shell()
        self.session_buffer = []
        self.last_cmd_buffer = []
        self._login()

    def __del__(self):
        self.ssh.close()

    def _login(self):
        if not self.is_string_in_cmd_output('', self.prompt_char):
            raise Exception('Something is wrong with Linux CLI login, see session buffer : %s' %
                            self.session_buffer)

    def is_string_in_session_buffer(self, expected_string_in_output):
        return len([line for line in self.session_buffer if expected_string_in_output in line ]) != 0

    def is_string_in_cmd_output(self, cmd, expected_string_in_output):
        self.invoke_linux_cmd(cmd)
        return len([line for line in self.last_cmd_buffer if expected_string_in_output in line]) != 0

    def invoke_linux_cmd(self, cmd: str = 'pstree -p', *args, prompt_char=None):
        cmd = F"{cmd} {args[0]}" if args else cmd

        def _is_prompt_back():
            if not lines:
                raise Exception('Buffer is empty for command - %s. session buffer - %s' % (cmd, self.session_buffer))
            prompt_string = (re.compile(r'\x1b[^m]*m|\x0F')).sub('', lines[-1])
            return prompt_string.endswith( F"{prompt_char} " if prompt_char else F"{self.prompt_char} " )

        start_time = time.time()
        self.session.send(F"{cmd}\n")
        self.last_cmd_buffer = []
        while time.time() - start_time < self.timeout:
            time.sleep(1)
            if self.session.recv_ready():
                lines = self.session.recv(9999).decode('utf-8').splitlines()
                self.session_buffer.extend(lines)
                self.last_cmd_buffer.extend(lines)
                if _is_prompt_back():
                    if self.logger:
                        logging.debug('BUFFER : {}'.format(self.last_cmd_buffer))
                    return self.last_cmd_buffer if self.stdout else None
        raise Exception('Could not get prompt back after waiting for %s seconds. session buffer %s' %
                        (str(time.time() - start_time), self.session_buffer))


if __name__ == '__main__':
    linux_client = LinuxCliClient('127.0.0.1')
