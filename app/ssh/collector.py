from ssh.connection import ServerConnection, SFTPSessionError
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
        self.scripts_path = Path(__file__).parent.parent.parent / "scripts"
        self.parent_name = f"/tmp/collector-{self.collector_hash}" 

    def build_workspace(self):
        subdir_names = [
            f"{self.parent_name}/scripts",
            f"{self.parent_name}/records",
            f"{self.parent_name}/archives"
        ]

        _, stderr = self.ssh_server.execute_command(f"mkdir {self.parent_name}")
        if stderr:
            raise CollectorError(stderr)

        for subdir in subdir_names:
            _, stderr = self.ssh_server.execute_command(f"mkdir -p {subdir}")
            if stderr:
                raise CollectorError(stderr)

    def clear_workspace(self):
        self.ssh_server.execute_command(f"rm -r {self.parent_name}")

    def inject_scripts(self):
        for sc_path in self.scripts_path.iterdir():
            if sc_path.is_file():
                self.ssh_server.upload(sc_path, f"{self.parent_name}/scripts/{sc_path.name}")

    def collect_data(self, record_id: int):
        scripts_rpath = f"{self.parent_name}/scripts"

        col_scripts, stderr = self.ssh_server.execute_command(f'ls {scripts_rpath} | grep -wo -E "^collect_.*\.sh$"')

        if stderr:
            raise CollectorError(f"An error occured while trying to check for collector tools: {stderr}")

        if not col_scripts:
            raise CollectorError(f"Collector tools are not uploaded at remote")

        _, stderr = self.ssh_server.execute_command(f"mkdir {self.parent_name}/records/record_{record_id}")
        if stderr:
            raise CollectorError(stderr)

        for col_sc_name in col_scripts.strip().split("\n"):
            _, stderr = self.ssh_server.execute_command(f"bash {scripts_rpath}/{col_sc_name} {self.parent_name}/records/record_{record_id}")
            if stderr:
                raise CollectorError(f"Unable to execute script {col_sc_name}: {stderr}")

    def retrieve_data(self, record_id: int):
        scripts_rpath = f"{self.parent_name}/scripts"

        archiver, stderr = self.ssh_server.execute_command(f'ls {scripts_rpath} | grep -wo -E "^get_.*\.sh$"')

        if stderr:
            raise CollectorError(f"An error occured while trying to check for collector tools: {stderr}")

        if not archiver:
            raise CollectorError(f"Archiver tool is not uploaded at remote")
        
        archiver = archiver.strip().split()
        if len(archiver) != 1:
            raise CollectorError(f"There must be exactly one archiver in collector")

        arc_path, stderr = self.ssh_server.execute_command(f"bash {scripts_rpath}/{archiver[0]} {self.parent_name}/records/record_{record_id} {self.parent_name}/archives record_{record_id}")
        if stderr:
            raise CollectorError(f"Unable to execute script {archiver[0]}: {stderr}")

        arc_path = arc_path.strip()

        self.ssh_server.download(arc_path, self.scripts_path.parent / "data" / "tmp" /  Path(arc_path).name)
