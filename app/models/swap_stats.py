from datetime import datetime
from dataclasses import dataclass

@dataclass
class SwapStats:
    timestamp: datetime
    units: str
    total: int
    used: int
    free: int
    usage_percent: int