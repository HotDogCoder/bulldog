from abc import ABC, abstractmethod
from apps.peru.domain.models.mtc_model import MtcModel

class MtcRepositoryInterface(ABC):
    def __init__(self):
        super().__init__()


    @abstractmethod
    def get_callao_car_tickets(self, mtc_model: MtcModel):
        return mtc_model
