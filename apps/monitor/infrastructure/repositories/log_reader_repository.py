from apps.monitor.application.repositories_interfaces.log_reader_repository_interface import \
    LogReaderRepositoryInterface
from apps.monitor.domain.models.log_reader import LogReader


class LogReaderRepository(LogReaderRepositoryInterface):
    def __init__(self):
        super().__init__()

    def read_log_file_directories(self, log_reader: LogReader):
        return log_reader

