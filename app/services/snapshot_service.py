import shutil
from pathlib import Path
from models.snapshot_data import SnapshotData
from parser.parser import Parser
from ssh.connection import ServerConnection
from ssh.credentials import ServerCredentials
from ssh.collector import Collector

class SnapshotService:
    def __init__(self):
        self.collector = None
        self.parser = Parser()
        self.snapshot_id = 1

    def start_service(self, credentials: ServerCredentials):        
        client = ServerConnection(credentials)
    
        client.set_connection()
    
        client.open_sftp_session()

        self.collector = Collector(client)
        
        self.collector.build_workspace()
    
        self.collector.inject_scripts()

    def get_snapshot(self):
        self.collector.collect_data(self.snapshot_id)
        
        self.collector.retrieve_data(self.snapshot_id)

        root_path = Path(__file__).parent.parent.parent

        src_path =  root_path / f"data/tmp/record_{self.snapshot_id}.zip"
        dst_path =  root_path / "data/current"

        shutil.unpack_archive(src_path, dst_path)

        dst_path = dst_path / f"record_{self.snapshot_id}"

        self.snapshot_id += 1

        return SnapshotData(
            ram_stats=self.parser.parse_ram_stats(dst_path / "perf/ram_stats.txt"),
            swap_stats=self.parser.parse_swap_stats(dst_path / "perf/swap_stats.txt"),
            load_average_stats=self.parser.parse_load_average_stats(dst_path / "perf/la_stats.txt"),
            file_system_stats=None,
            auth_logs=self.parser.parse_logs(dst_path / "logs/authlog.txt"),
            sys_logs=self.parser.parse_logs(dst_path / "logs/syslog.txt"),
            kern_logs=self.parser.parse_logs(dst_path / "logs/kernlog.txt")
        )

    def stop_service(self):
        if self.collector:
            self.collector.clear_workspace()
            self.collector.close()