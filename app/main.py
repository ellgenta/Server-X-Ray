from ssh.credentials import ServerCredentials
from ssh.connection import ServerConnection

client = None

try:
    credentials = ServerCredentials()

    client = ServerConnection(credentials)

    client.set_connection()

    output, er = client.execute_command("pwd")

    print(output)
finally:
    if client:
        client.close_connection()