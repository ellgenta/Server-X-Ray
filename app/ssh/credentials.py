from dataclasses import dataclass

@dataclass
class ServerCredentials:
    host: str
    username: str
    key_path: str
    port: int = 22