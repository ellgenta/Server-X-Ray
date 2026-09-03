from ssh.credentials import ServerCredentials
from ssh.connection import ServerConnection, SSHConnectionError, SSHExecutionError
from getpass import getpass

def get_credentials():
    print("Input host IP-address:", end=" ")
    _host = input()
    print("Input username:", end=" ")
    _username = input()
    _password = getpass(prompt="Input password: ", echo_char="*")

    return ServerCredentials(_host, _username, _password)

client = None

try:
    credentials = get_credentials()

    client = ServerConnection(credentials)

    client.set_connection()

    output, er = client.execute_command("ll")

    print(output)
except SSHConnectionError as er:
    print(f"Connection failed: {er}")
except SSHExecutionError as er:
    print(f"Command execution failed: {er}")
finally:
    if client:
        client.close_connection()