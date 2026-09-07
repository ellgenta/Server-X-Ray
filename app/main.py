from ssh.credentials import ServerCredentials
from ssh.connection import ServerConnection, SSHConnectionError, SSHExecutionError, SFTPSessionError
from ssh.collector import Collector, CollectorError, ScriptExecutionError
from getpass import getpass

def get_credentials():
    print("Input host IP-address:", end=" ")
    _host = input()
    print("Input username:", end=" ")
    _username = input()
    _password = getpass(prompt="Input password: ", echo_char="*")

    return ServerCredentials(_host, _username, _password)

client = None
collector = None

try:
    credentials = get_credentials()

    client = ServerConnection(credentials)

    client.set_connection()

    client.open_sftp_session()

    # output, er = client.execute_command("ls -la")

    collector = Collector(client)

    collector.build_workspace()

    collector.inject_scripts()

    collector.collect_data()

except SSHConnectionError as er:
    print(f"Connection failed: {er}")
except SSHExecutionError as er:
    print(f"Command execution failed: {er}")
except SFTPSessionError as er:
    print(f"SFTP-session error: {er}")
except CollectorError as er:
    print(f"Collector error: {er}")
finally:
    if collector:
        collector.clear_workspace()
    if client:
        client.close_sftp_session()
        client.close_connection()
