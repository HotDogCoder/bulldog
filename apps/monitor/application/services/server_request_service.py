from apps.monitor.application.services_interfaces.server_request_service_interface import \
    ServerRequestServiceInterface
from apps.monitor.domain.models.server_request import ServerRequest
from apps.monitor.domain.models.server_request_filter import ServerRequestFilter
from apps.monitor.domain.models.sftp_parameter import SftpParameter
from apps.monitor.infrastructure.repositories.server_request_repository import ServerRequestRepository


class ServerRequestService(ServerRequestServiceInterface):
    def __init__(self):
        super().__init__()
        self.server_request_repository = ServerRequestRepository()

    def insert_server_request(self, server_request: ServerRequest):
        return self.server_request_repository.insert_server_request(server_request)

    def select_server_request(self, server_request_filter: ServerRequestFilter):
        return self.server_request_repository.get_server_request_files_data(server_request_filter)

    def get_server_request_files_data(self, server_request_filter: ServerRequestFilter):
        return self.server_request_repository.get_server_request_files_data(server_request_filter)

    def upload_file_into_external_folder(self, sftp_parameter: SftpParameter):
        return self.server_request_repository.upload_file_into_external_folder(sftp_parameter)

