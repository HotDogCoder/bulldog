from abc import ABC, abstractmethod

from apps.monitor.domain.models.log_reader import LogReader


class LogReaderRepositoryInterface(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def read_log_file_directories(self, log_reader: LogReader):
        pass

