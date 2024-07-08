from abc import ABC, abstractmethod

from apps.monitor.domain.models.alira import Alira


class AliraRepositoryInterface(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def set_seo_parameters_per_page(self, alira: Alira):
        return alira

    @abstractmethod
    def set_seo_redirection(self, alira: Alira):
        return alira

    @abstractmethod
    def get_layouts(self, alira: Alira):
        return alira

    @abstractmethod
    def set_page_url(self, alira: Alira):
        return alira