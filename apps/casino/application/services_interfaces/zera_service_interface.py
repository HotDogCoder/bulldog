from abc import ABC, abstractmethod
from apps.casino.domain.models.zera_model import ZeraModel

class ZeraServiceInterface(ABC):
    def __init__(self):
        super().__init__()


    @abstractmethod
    def get_users(self, zera_model: ZeraModel):
        return zera_model
