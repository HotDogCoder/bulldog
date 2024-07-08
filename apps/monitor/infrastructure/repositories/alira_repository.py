from apps.monitor.application.repositories_interfaces.alira_repository_interface import AliraRepositoryInterface
from apps.monitor.domain.models.alira import Alira
from core.config import constants


class AliraRepository(AliraRepositoryInterface):

    def __init__(self):
        super().__init__()

    def set_seo_parameters_per_page(self, alira: Alira):

        url = constants.API_UPLOAD_SCREENSHOT
        multiple_files = []

        return alira

    def set_seo_redirection(self, alira: Alira):
        return alira

    def get_layouts(self, alira: Alira):
        return alira

    def set_page_url(self, alira: Alira):
        return alira