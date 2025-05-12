from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as Wait

class MtcHelper:
    def __init__(self, driver, mtc_model=None):
        self.driver = driver
        self.mtc_model = mtc_model

    def get_callao_car_tickets(self):
        self.driver.maximize_window()
        self.driver.get(self.mtc_model.url)

        sleep(10)


