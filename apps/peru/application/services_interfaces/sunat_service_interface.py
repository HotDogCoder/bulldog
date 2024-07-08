from abc import ABC, abstractmethod
from apps.peru.domain.models.sunat_model import SunatModel

class SunatServiceInterface(ABC):
    def __init__(self):
        super().__init__()


    @abstractmethod
    def post(self, sunat_model: SunatModel):
        return sunat_model
    @abstractmethod
    def get_token(self, sunat_model: SunatModel):
        return sunat_model
