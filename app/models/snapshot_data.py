from .file_system_stats import FileSystemStats
from .load_average_stats import LoadAverageStats
from .ram_stats import RAMStats
from .swap_stats import SwapStats
from .log_entry import LogEntry
from dataclasses import dataclass

@dataclass
class SnapshotData:
    ram_stats: RAMStats
    swap_stats: SwapStats
    load_average_stats: LoadAverageStats
    file_system_stats: FileSystemStats
    auth_logs: list[LogEntry]
    sys_logs: list[LogEntry]
    kern_logs: list[LogEntry]