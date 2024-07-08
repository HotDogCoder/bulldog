from apps.monitor.application.services.alira_service import AliraService
from apps.monitor.domain.models.alira import Alira


class AliraController:

    def __init__(self):
        self.alira_service = AliraService()

    def set_seo_parameters_per_page(self, alira: Alira):
        return self.alira_service.set_seo_parameters_per_page(alira)

    def set_seo_redirection(self, alira: Alira):
        return self.alira_service.set_seo_redirection(alira)
