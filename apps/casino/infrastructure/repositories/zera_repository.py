from apps.casino.application.repositories_interfaces.zera_repository_interface import ZeraRepositoryInterface
from apps.casino.domain.models.zera_model import ZeraModel

class ZeraRepository(ZeraRepositoryInterface):
    def __init__(self):
        super().__init__()

    def get_users(self, zera_model: ZeraModel):
        return zera_model
