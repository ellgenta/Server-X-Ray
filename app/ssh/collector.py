from ssh.connection import ServerConnection
from pathlib import Path
import uuid

class CollectorError(Exception):
    pass

class ScriptExecutionError(Exception):
    pass

class Collector:
    def __init__(self, ssh_server: ServerConnection):
        self.ssh_server = ssh_server
        self.collector_hash = str(uuid.uuid4())
        self.scripts_path = Path(__file__).parent.parent / "scripts"
        self.parent_name = f"/tmp/collector-{self.collector_hash}" 

    def build_workspace(self):
        subdir_names = [
            f"{self.parent_name}/scripts",
            f"{self.parent_name}/stats/perf",
            f"{self.parent_name}/stats/logs"
        ]

        _, stderr = self.ssh_server.execute_command(f"mkdir {self.parent_name}")
        if stderr:
            raise CollectorError(stderr)

        for subdir in subdir_names:
            _, stderr = self.ssh_server.execute_command(f"mkdir -p {subdir}")
            if stderr:
                raise CollectorError(stderr)

    def clear_workspace(self):
        self.ssh_server.execute_command(self.parent_name)