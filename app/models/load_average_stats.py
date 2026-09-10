from datetime import datetime
from dataclasses import dataclass

@dataclass
class LoadAverageStats:
    timestamp: datetime
    last_1: float
    last_5: float
    last_15: float