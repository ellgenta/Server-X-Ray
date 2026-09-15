from datetime import datetime
from dataclasses import dataclass

@dataclass
class ProcessEntry:
    user: str
    pid: int
    cpu_load: float
    mem_load: float
    status: str
    time: datetime
    command: str 