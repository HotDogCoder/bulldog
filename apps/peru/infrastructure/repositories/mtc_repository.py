from apps.peru.application.repositories_interfaces.mtc_repository_interface import MtcRepositoryInterface
from apps.peru.domain.models.mtc_model import MtcModel

class MtcRepository(MtcRepositoryInterface):
    def __init__(self):
        super().__init__()

    def get_callao_car_tickets(self, mtc_model: MtcModel):
        return mtc_model
