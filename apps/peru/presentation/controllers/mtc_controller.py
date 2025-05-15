from apps.peru.application.services.mtc_service import MtcService
from apps.peru.domain.models.mtc_model import MtcModel

class MtcController:
    def __init__(self):
        super().__init__()
        self.mtc_service = MtcService()

    def get_callao_car_tickets(self, mtc_model: MtcModel):
        mtc_model.url = 'https://pagopapeletascallao.pe/'
        mtc_model.driver = 'Chrome'
        mtc_model.chrome_driver_path = '/Users/Shared/chromedriver/chromedriver'
        mtc_model.chrome_driver_path = "/var/lib/jenkins/.cache/selenium/chromedriver/linux64/114.0.5735.90/chromedriver"
        mtc_model.chrome_driver_path = "/usr/lib/chromium-browser"
        return self.mtc_service.get_callao_car_tickets(mtc_model)
    
    def get_lima_car_tickets(self, mtc_model: MtcModel):
        mtc_model.url = 'https://www.sat.gob.pe/websitev9/TributosMultas/Papeletas/ConsultasPapeletas'
        mtc_model.driver = 'Chrome'
        mtc_model.chrome_driver_path = '/Users/Shared/chromedriver/chromedriver'
        mtc_model.chrome_driver_path = "/var/lib/jenkins/.cache/selenium/chromedriver/linux64/114.0.5735.90/chromedriver"
        mtc_model.chrome_driver_path = "/usr/lib/chromium-browser"
        return self.mtc_service.get_lima_car_tickets(mtc_model)
