from apps.monitor.application.services.log_reader_service import LogReaderService
from apps.monitor.domain.models.log_reader import LogReader


class LogReaderController:

    def __init__(self):
        self.log_reader_service = LogReaderService()

    def read_log_file_directories(self, log_reader: LogReader):
        return self.log_reader_service.read_log_file_directories(log_reader)

# pytest