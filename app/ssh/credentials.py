from dataclasses import dataclass

@dataclass
class ServerCredentials:
    host: str
    username: str
    password: str
    port: int = 22