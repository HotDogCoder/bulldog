from apps.peru.application.services_interfaces.sunat_service_interface import SunatServiceInterface
from apps.peru.helpers.sunat_helper import SunatHelper
from apps.peru.infrastructure.repositories.sunat_repository import SunatRepository
from apps.peru.domain.models.sunat_model import SunatModel
from core.util.path.path_helper import PathHelper

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display
import os
from datetime import datetime

class SunatService(SunatServiceInterface):
    def __init__(self):
        super().__init__()
        self.sunat_repository = SunatRepository()

    def post(self, sunat_model: SunatModel):
        return self.sunat_repository.post(sunat_model)
    def get_token(self, sunat_model: SunatModel):

        try:
            driver = None
            # url = screenshot.url
            if sunat_model.driver == 'Chrome':
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
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--ignore-certificate-errors')
                
                chrome_service = Service(sunat_model.chrome_driver_path)
                # driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
                # display = Display(visible=0, size=(1920, 1080))
                # display.start()
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            elif sunat_model.driver == 'Firefox':
                driver = webdriver.Firefox(
                    executable_path="/usr/bin/geckodriver"
                )
            elif sunat_model.driver == 'Safari':
                driver = webdriver.Safari()
            elif sunat_model.driver == 'Edge':
                driver = webdriver.Edge()

            sunat_helper = SunatHelper(driver, sunat_model=sunat_model)
            # # resize diver maximaze
            driver.maximize_window()
            sunat_helper.login_sunat()

            path_helper = PathHelper()
            
            driver.close()
            print('-------------------- finished -----------------------')

        except (UnicodeDecodeError, StopIteration) as e:

            print('error: ', e)


        return self.sunat_repository.get_token(sunat_model)
