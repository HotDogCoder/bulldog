from apps.peru.application.services.sunat_service import SunatService
from apps.peru.domain.models.sunat_model import SunatModel

class SunatController:
    def __init__(self):
        super().__init__()
        self.sunat_service = SunatService()

    def post(self, sunat_model: SunatModel):
        return self.sunat_service.post(sunat_model)
    def get_token(self, sunat_model: SunatModel):
        sunat_model.url = 'https://api-seguridad.sunat.gob.pe/v1/clientessol/4f3b88b3-d9d6-402a-b85d-6a0bc857746a/oauth2/loginMenuSol?originalUrl=https://e-menu.sunat.gob.pe/cl-ti-itmenu/AutenticaMenuInternet.htm&state=rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAADdAAEZXhlY3B0AAZwYXJhbXN0AEsqJiomL2NsLXRpLWl0bWVudS9NZW51SW50ZXJuZXQuaHRtJmI2NGQyNmE4YjVhZjA5MTkyM2IyM2I2NDA3YTFjMWRiNDFlNzMzYTZ0AANleGVweA=='
        sunat_model.driver = 'Chrome'
        sunat_model.chrome_driver_path = '/Users/Shared/chromedriver/chromedriver'
        return self.sunat_service.get_token(sunat_model)
