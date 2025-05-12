from apps.peru.application.services_interfaces.mtc_service_interface import MtcServiceInterface
from apps.peru.infrastructure.repositories.mtc_repository import MtcRepository
from apps.peru.domain.models.mtc_model import MtcModel
from apps.peru.helpers.mtc_helper import MtcHelper
from core.util.path.path_helper import PathHelper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

class MtcService(MtcServiceInterface):
    def __init__(self):
        super().__init__()
        self.mtc_repository = MtcRepository()

    def get_callao_car_tickets(self, mtc_model: MtcModel):
        try:
            driver = None
            # url = screenshot.url
            if mtc_model.driver == 'Chrome':
                chrome_options = ChromeOptions()
                # chrome_options.add_argument('--no-sandbox')
                # chrome_options.add_argument('--disable-dev-shm-usage')
                # chrome_options.add_argument('--headless')
                # chrome_options.add_argument('--disable-gpu')
                # chrome_options.add_argument("--start-maximized")
                # chrome_options.add_argument("--window-size=1920,1080")
                # chrome_options.add_argument('--ignore-certificate-errors')
                # chrome_options.add_argument('--allow-running-insecure-content')

                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--proxy-server='direct://'")
                chrome_options.add_argument("--proxy-bypass-list=*")
                chrome_options.add_argument("--start-maximized")
                # chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--ignore-certificate-errors')
                
                chrome_service = Service(mtc_model.chrome_driver_path)
                # driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
                # display = Display(visible=0, size=(1920, 1080))
                # display.start()
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            elif mtc_model.driver == 'Firefox':
                driver = webdriver.Firefox(
                    executable_path="/usr/bin/geckodriver"
                )
            elif mtc_model.driver == 'Safari':
                driver = webdriver.Safari()
            elif mtc_model.driver == 'Edge':
                driver = webdriver.Edge()

            mtc_helper = MtcHelper(driver, mtc_model=mtc_model)
            # # resize diver maximaze
            driver.maximize_window()
            mtc_helper.get_callao_car_tickets()

            path_helper = PathHelper()
            
            driver.close()
            print('-------------------- finished -----------------------')

        except (UnicodeDecodeError, StopIteration) as e:

            print('error: ', e)


        return self.mtc_repository.get_token(mtc_model)

