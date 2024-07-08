from apps.monitor.application.services.server_request_service import ServerRequestService
from apps.monitor.domain.models.server_request import ServerRequest
from apps.monitor.domain.models.server_request_filter import ServerRequestFilter
from apps.monitor.domain.models.sftp_parameter import SftpParameter


class ServerRequestController:

    def __init__(self):
        self.server_request_service = ServerRequestService()

    def insert_server_request(self, server_request: ServerRequest):
        return self.server_request_service.insert_server_request(server_request)

    def select_server_request(self, server_request_filter: ServerRequestFilter):
        pass

    def get_server_request_files_data(self, server_request_filter: ServerRequestFilter):
        return self.server_request_service.get_server_request_files_data(server_request_filter)

    def upload_file_into_external_folder(self, sftp_parameter: SftpParameter):
        return self.server_request_service.upload_file_into_external_folder(sftp_parameter)

