from datetime import datetime
from dataclasses import dataclass

@dataclass
class LogEntry:
    timestamp: datetime
    user: str
    message: str
    level: str