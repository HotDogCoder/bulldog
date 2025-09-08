from apps.casino.application.services_interfaces.zera_service_interface import ZeraServiceInterface
from apps.casino.helpers.zera_helper import ZeraHelper
from apps.casino.infrastructure.repositories.zera_repository import ZeraRepository
from apps.casino.domain.models.zera_model import ZeraModel
from core.util.path.path_helper import PathHelper

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service

from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import os

class ZeraService(ZeraServiceInterface):
    def __init__(self):
        super().__init__()
        self.zera_repository = ZeraRepository()

    def get_users(self, zera_model: ZeraModel):
        try:
            driver = None
            # url = screenshot.url
            if zera_model.driver == 'Chrome':
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

                # Set the download directory
                # Create download directory
                download_dir = os.path.abspath("downloads/excel_files_zera")
                os.makedirs(download_dir, exist_ok=True)

                prefs = {
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "profile.default_content_setting_values.automatic_downloads": 1,
                    "plugins.always_open_pdf_externally": True
                }
                chrome_options.add_experimental_option("prefs", prefs)

                chrome_service = Service(zera_model.chrome_driver_path)
                driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
                # display = Display(visible=0, size=(1920, 1080))
                # display.start()
                # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            elif zera_model.driver == 'Firefox':
                driver = webdriver.Firefox(
                    executable_path="/usr/bin/geckodriver"
                )
            elif zera_model.driver == 'Safari':
                driver = webdriver.Safari()
            elif zera_model.driver == 'Edge':
                driver = webdriver.Edge()

            zera_helper = ZeraHelper(driver, zera_model=zera_model)
            # # resize diver maximaze
            driver.maximize_window()
            zera_helper.login_zera()

            path_helper = PathHelper()

            # set the trough all the months between the from and to dates
            start_date = datetime.strptime(f"{zera_model.from_year}-{zera_model.from_month}-01", "%Y-%m-%d")
            # Get the last day of the to_month
            end_year = int(zera_model.to_year)
            end_month = int(zera_model.to_month)
            last_day = monthrange(end_year, end_month)[1]
            end_date = datetime.strptime(f"{zera_model.to_year}-{zera_model.to_month}-{last_day}", "%Y-%m-%d")
            current_date = start_date

            # if end_date is after the current date, set it to the current date
            #if end_date > datetime.now():
            #    end_date = datetime.now()

            while current_date < end_date:
                zera_helper.set_filter_form_parameters(start_date=current_date, end_date=current_date + relativedelta(months=1, days=-1))
                zera_helper.extract_table_data()
                current_date += relativedelta(months=1)

            zera_helper.save_nested_users_to_csv()

            driver.close()
            print('-------------------- finished -----------------------')

        except (UnicodeDecodeError, StopIteration) as e:

            print('error: ', e)
        
        return self.zera_repository.get_users(zera_model)
