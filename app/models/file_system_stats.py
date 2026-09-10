from datetime import datetime
from dataclasses import dataclass

@dataclass
class FileSystemStats:
    timestamp: datetime
    units: str
    fs_name: str
    size: int
    used: int
    available: int
    mount: str
    usage_percent: float