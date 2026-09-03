from ssh.credentials import ServerCredentials
import paramiko

class SSHConnectionError(Exception):
    pass

class SSHExecutionError(Exception):
    pass

class SFTPSessionError(Exception):
    pass

class ServerConnection:
    def __init__(self, credentials: ServerCredentials):
        self.credentials = credentials
        self.client = paramiko.SSHClient()
        self.sftp_server = None

        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

    def set_connection(self):
        try:
            self.client.connect(
                hostname=self.credentials.host,
                username=self.credentials.username,
                port=self.credentials.port,
                password=self.credentials.password
            )
        except paramiko.SSHException as er:
            raise SSHConnectionError(er)
        except OSError as er:
            raise SSHConnectionError(er.strerror)

    def execute_command(self, command_name: str):
        try:
            _in, _out, _er = self.client.exec_command(command_name)

            return (_out.read().decode(), _er.read().decode())
        except paramiko.SSHException as er:
            raise SSHExecutionError(er)

    def close_connection(self):
        self.client.close()

    def open_sftp_session(self):
        try:
            self.sftp_server = self.client.open_sftp()
        except paramiko.SSHException as er:
            raise SFTPSessionError(er)

    def close_sftp_session(self):
        if self.sftp_server:
            self.sftp_server.close()
        self.sftp_server = None