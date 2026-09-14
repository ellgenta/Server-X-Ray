from ssh.credentials import ServerCredentials
from ssh.connection import SSHConnectionError, SSHExecutionError, SFTPSessionError
from ssh.collector import CollectorError, ScriptExecutionError
from parser.parser import ParserException
from services.snapshot_service import SnapshotService
from getpass import getpass

def get_credentials():
    print("Input host IP-address:", end=" ")
    _host = input()
    print("Input username:", end=" ")
    _username = input()
    _password = getpass(prompt="Input password: ", echo_char="*")

    return ServerCredentials(_host, _username, _password)

service = None

try:
    credentials = get_credentials()

    service = SnapshotService()

    service.start_service(credentials)

    test_snapshot = service.get_snapshot()

    test_snapshot = service.get_snapshot()

except SSHConnectionError as er:
    print(f"Connection failed: {er}")
except SSHExecutionError as er:
    print(f"Command execution failed: {er}")
except SFTPSessionError as er:
    print(f"SFTP-session error: {er}")
except CollectorError as er:
    print(f"Collector error: {er}")
except ParserException as er:
    print(f"Parser error: {er}")
except ScriptExecutionError as er:
    print(f"Script execution error: {er}")
finally:
    if service:
        service.stop_service()
