from models.snapshot_data import SnapshotData
from parser.parser import Parser

class SnapshotService:
    def __init__(self):
        self.collector = None
        self.parser = Parser()