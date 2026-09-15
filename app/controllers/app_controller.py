from services.snapshot_service import SnapshotService
from ssh.credentials import ServerCredentials

class ControllerError(Exception):
    pass

class AppController:
    MAX_HISTORY = 100 
    MAX_LOGS = 50

    def __init__(self):
        self.is_connected = False
        self.service = SnapshotService()
        self.ram_stats_history = []
        self.swap_stats = None
        self.load_average_stats = None
        self.disk_stats = None
        self.proc_list = None
        self.auth_logs = []
        self.sys_logs = []
        self.kern_logs = []

    def connect(self, credentials: ServerCredentials):
        if self.is_connected:
            return
        
        self.service.start_service(credentials)
        self.is_connected = True

    def _update_logs(self, old_logs, new_logs):
        logs = old_logs + new_logs

        if len(logs) > self.MAX_LOGS:
            return logs[-self.MAX_LOGS:]

        return logs

    def _update_ram_stats(self, stats_history, cur_stats):
        stats_history.append(cur_stats)

        if len(stats_history) > self.MAX_HISTORY:
            return stats_history[1:]

        return stats_history

    def update(self):
        if not self.is_connected:
            raise ControllerError("There is no connection with the remote server!")

        snapshot = self.service.get_snapshot()

        self.ram_stats_history = self._update_ram_stats(self.ram_stats_history, snapshot.ram_stats)
        self.swap_stats = snapshot.swap_stats
        self.load_average_stats = snapshot.load_average_stats
        self.disk_stats = snapshot.disk_stats
        self.proc_list = snapshot.proc_list
        self.auth_logs = self._update_logs(self.auth_logs, snapshot.auth_logs)
        self.sys_logs = self._update_logs(self.sys_logs, snapshot.sys_logs)
        self.kern_logs = self._update_logs(self.kern_logs, snapshot.kern_logs)

    def reset(self):
        self.ram_stats_history = []
        self.swap_stats = None
        self.load_average_stats = None
        self.disk_stats = None
        self.proc_list = None
        self.auth_logs = []
        self.sys_logs = []
        self.kern_logs = []

    def disconnect(self):
        self.reset()
        self.service.save_session()
        self.service.stop_service()

        self.is_connected = False