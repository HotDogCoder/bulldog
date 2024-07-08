from apps.peru.application.repositories_interfaces.sunat_repository_interface import SunatRepositoryInterface
from apps.peru.domain.models.sunat_model import SunatModel

class SunatRepository(SunatRepositoryInterface):
    def __init__(self):
        super().__init__()

    def post(self, sunat_model: SunatModel):
        return sunat_model
    def get_token(self, sunat_model: SunatModel):
        return sunat_model
