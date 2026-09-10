from datetime import datetime
from dataclasses import dataclass

@dataclass
class RAMStats:
    timestamp: datetime
    units: str
    free: int
    shared: int
    cache: int
    available: int
    usage_percent: float