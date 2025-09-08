from apps.casino.application.services.zera_service import ZeraService
from apps.casino.domain.models.zera_model import ZeraModel

class ZeraController:
    def __init__(self):
        super().__init__()
        self.zera_service = ZeraService()

    def get_users(self, zera_model: ZeraModel):
        # zera_model.url = 'https://ag.casinozera.com/index.php'
        zera_model.driver = 'Chrome'
        zera_model.chrome_driver_path = '/Users/Shared/chromedriver/chromedriver'
        # zera_model.chrome_driver_path = "/var/lib/jenkins/.cache/selenium/chromedriver/linux64/114.0.5735.90/chromedriver"
        # zera_model.chrome_driver_path = "/usr/lib/chromium-browser"
        # zera_model.chrome_driver_path = 'C:\chromedriver'
        return self.zera_service.get_users(zera_model)
