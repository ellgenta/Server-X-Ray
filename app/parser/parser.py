from models.file_system_stats import FileSystemStats
from models.load_average_stats import LoadAverageStats
from models.ram_stats import RAMStats
from models.swap_stats import SwapStats
from models.log_entry import LogEntry
from models.proc_entry import ProcessEntry
from datetime import datetime

class ParserException(Exception):
    pass

class Parser:
    WARNING_TRIGGERS = ["warning","retry","deprecated"]
    
    ERROR_TRIGGERS = ["failed","failure","exception","error",
        "denied","not found","corrupted","refused","kill"
    ]

    CRITICAL_TRIGGERS = ["panic","out of memory",
        "segfault"
    ]

    def parse_key_value_pairs(self, file_path: str):
        try:
            parsed_data = dict()
            with open(file_path, encoding="utf-8") as file:
                for line in file:
                    key, value = line.strip().split("=", 1)
                    parsed_data[key] = value
            return parsed_data
        except OSError as er:
            raise ParserException(f"An error occured while working with {file_path}: {er}")
        except Exception as er:
            raise ParserException(f"An error occured while parsing {file_path}: {er}")

    def parse_ram_stats(self, file_path: str):
        parsed_data = self.parse_key_value_pairs(file_path)

        _usage_percent = round(int(parsed_data["used"]) / int(parsed_data["total"]) * 100)

        return RAMStats(
            timestamp=datetime.now(),
            units="MB",
            total=int(parsed_data["total"]),
            used=int(parsed_data["used"]),
            free=int(parsed_data["free"]),
            shared=int(parsed_data["shared"]),
            cache=int(parsed_data["buff/cache"]),
            available=int(parsed_data["available"]),
            usage_percent=_usage_percent
        )

    def parse_swap_stats(self, file_path: str):
        parsed_data = self.parse_key_value_pairs(file_path)
        
        _usage_percent = round(int(parsed_data["used"]) / int(parsed_data["total"]) * 100)

        return SwapStats(
            timestamp=datetime.now(),
            units="MB",
            total=int(parsed_data["total"]),
            used=int(parsed_data["used"]),
            free=int(parsed_data["free"]),
            usage_percent=_usage_percent
        )

    def parse_load_average_stats(self, file_path: str):
        parsed_data = self.parse_key_value_pairs(file_path)

        return LoadAverageStats(
            timestamp=datetime.now(),
            last_1=float(parsed_data["last_1"]),
            last_5=float(parsed_data["last_5"]),
            last_15=float(parsed_data["last_15"])
        )

    def parse_file_system_stats(self, file_path: str):
        parsed_data = self.parse_key_value_pairs(file_path)

        _usage_percent = round(int(parsed_data["used"].removesuffix("MB")) / int(parsed_data["size"].removesuffix("MB")) * 100)

        return FileSystemStats(
            timestamp=datetime.now(),
            units="MB",
            fs_name=parsed_data["fs_name"],
            size=int(parsed_data["size"].removesuffix("MB")),
            used=int(parsed_data["used"].removesuffix("MB")),
            available=int(parsed_data["available"].removesuffix("MB")),
            mount=parsed_data["mount"],
            usage_percent=_usage_percent
        )

    def parse_proc_list(self, file_path: str):
        try:
            entries = list()
            with open(file_path, encoding="utf-8") as file:
                for line in file:
                    entry = line.strip().split(maxsplit=6)
                    if len(entry) != 7:
                        continue
                    try:
                        entry_timestamp = datetime.strptime(entry[5], "%H:%M")
                    except ValueError:
                        continue
                    entries.append(
                        ProcessEntry(
                            user=entry[0],
                            pid=int(entry[1]),
                            cpu_load=float(entry[2]),
                            mem_load=float(entry[3]),
                            status=entry[4],
                            time=entry_timestamp,
                            command=entry[6]
                        )
                    )
            return entries
        except OSError as er:
            raise ParserException(f"An error occured while working with {file_path}: {er}")
        except Exception as er:
            raise ParserException(f"An error occured while parsing {file_path}: {er}")

    def has_any_trigger(self, message: str, triggers: list[str]):
        return any(tr in message for tr in triggers)

    def get_log_level(self, message: str):
        message = message.lower()

        if self.has_any_trigger(message, self.CRITICAL_TRIGGERS):
            return "CRITICAL"
        if self.has_any_trigger(message, self.ERROR_TRIGGERS):
            return "ERROR"
        if self.has_any_trigger(message, self.WARNING_TRIGGERS):
            return "WARNING"

        return "INFO"

    def parse_logs(self, file_path: str):
        try:
            entries = list()
            with open(file_path, encoding="utf-8") as file:
                for line in file:
                    entry = line.strip().split(maxsplit=2)
                    if len(entry) != 3:
                        continue
                    try:
                        entry_timestamp = datetime.strptime(entry[0], "%Y-%m-%dT%H:%M:%S.%f%z")
                    except ValueError:
                        continue
                    entry_level = self.get_log_level(entry[2])
                    entries.append(
                        LogEntry(
                            timestamp=entry_timestamp,
                            user=entry[1],
                            message=entry[2],
                            level=entry_level
                        )
                    )
                return entries
        except OSError as er:
            raise ParserException(f"An error occured while working with {file_path}: {er}")
        except Exception as er:
            raise ParserException(f"An error occured while parsing {file_path}: {er}")