import os
from time import sleep

import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

from apps.monitor.application.services_interfaces.alira_service_interface import AliraServiceInterface
from apps.monitor.domain.models.alira import Alira
from apps.monitor.features.alira.alira_helper import AliraHelper
from apps.monitor.infrastructure.repositories.alira_repository import AliraRepository
from core.util.debug.trace_helper import TraceHelper


class AliraService(AliraServiceInterface):

    def __init__(self):
        super().__init__()
        self.alira_repository = AliraRepository()

    def set_seo_parameters_per_page(self, alira: Alira):

        try:
            driver = None

            if alira.driver == 'Chrome':
                driver = webdriver.Chrome()
            elif alira.driver == 'Firefox':
                driver = webdriver.Firefox()
            elif alira.driver == 'Safari':
                driver = webdriver.Safari()
            elif alira.driver == 'Edge':
                driver = webdriver.Edge()

            tz = pytz.timezone('America/Bogota')
            directory_name = datetime.now(tz).strftime('%Y%m%d%H%M%S')

            alira_helper = AliraHelper(driver, page=0)
            alira_helper.login(alira.url, "rterrones", "P@ssw0rd123.")
            excel_path = os.getcwd() + f"/resources/templates/seo/2022/12/KWR.xlsx"
            alira_helper.get_kwr(excel_path)

            """ CASINO ONLINE """
            """first get our url base or references /casino-online /apuestas-deportivas"""
            alira_helper.get_sheet_url_reference(1, 4, [
                        f"https://www.casinoatlnaticcity.com",
                        f"https://demo-acp.calimaco.com",
                    ])

            references_1 = list(set(filter(lambda x: x != "/" and x != "", alira_helper.sheets[1].data)))

            alira_helper.access_to_pages_tab()

            for reference in references_1:
                alira_helper.get_sheet_target_urls(
                    1, 4, 5,
                    [
                        f"https://www.casinoatlnaticcity.com",
                        f"https://demo-acp.calimaco.com",
                    ])
                alira_helper.url = reference
                alira_helper.target_urls = []
                for index, url in enumerate(alira_helper.sheets[1].data):
                    url.title = alira_helper.get_sheet_row_data(1, [26], url.id)
                    url.description = alira_helper.get_sheet_row_data(1, [28], url.id)
                    url.keywords = alira_helper.get_sheet_row_data(1, [
                        7, 9, 11, 13, 15, 17, 19, 21, 23
                    ], url.id)

                    # url.flag = True
                    alira_helper.target_urls.append(url)
                alira_helper.page = 1
                alira_helper.iterate_main_datatable()
                while alira_helper.page < alira_helper.table_page_total:
                    alira_helper.iterate_main_datatable()
            """ """

            """" APUESTAS DEPORTIVAS """
            alira_helper.get_sheet_url_reference(2, 2, [
                f"https://www.casinoatlnaticcity.com",
                f"https://demo-acp.calimaco.com",
            ])
            references_2 = list(set(filter(lambda x: x != "/" and x != "", alira_helper.sheets[2].data)))


            # alira_helper.access_to_pages_tab()

            for reference in references_2:
                alira_helper.get_sheet_target_urls(
                    2,
                    2,
                    3,
                    [
                        f"https://www.casinoatlnaticcity.com",
                        f"https://demo-acp.calimaco.com",
                    ])
                alira_helper.url = reference
                alira_helper.target_urls = []
                for index, url in enumerate(alira_helper.sheets[2].data):
                    url.title = alira_helper.get_sheet_row_data(2, [28], url.id)
                    url.description = alira_helper.get_sheet_row_data(2, [30], url.id)
                    url.keywords = alira_helper.get_sheet_row_data(2, [
                        9, 11, 13, 15, 17, 19, 21, 23, 25
                    ], url.id)
                    # url.flag = True
                    alira_helper.target_urls.append(url)
                alira_helper.page = 1
                alira_helper.iterate_main_datatable(save=False)
                while alira_helper.page < alira_helper.table_page_total:
                    alira_helper.iterate_main_datatable(save=False)

            alira.alira_helper = alira_helper
            driver.close()
            print('-------------------- finished -----------------------')

        except (UnicodeDecodeError, StopIteration) as e:

            print('error: ', e)

        return self.alira_repository.set_seo_parameters_per_page(alira)

    def set_seo_redirection(self, alira: Alira):

        try:
            driver = None

            if alira.driver == 'Chrome':
                driver = webdriver.Chrome()
            elif alira.driver == 'Firefox':
                driver = webdriver.Firefox()
            elif alira.driver == 'Safari':
                driver = webdriver.Safari()
            elif alira.driver == 'Edge':
                driver = webdriver.Edge()

            tz = pytz.timezone('America/Bogota')
            directory_name = datetime.now(tz).strftime('%Y%m%d%H%M%S')

            alira_helper = AliraHelper(driver, page=0)
            alira_helper.login(alira.url, "rterrones", "P@ssw0rd123.")
            excel_path = os.getcwd() + f"/resources/templates/seo/2022/12/KWR.xlsx"
            alira_helper.get_kwr(excel_path)

            alira_helper.access_to_redirections()

            """ CASINO ONLINE """
            """first get our url base or references /casino-online /apuestas-deportivas"""
            alira_helper.get_sheet_url_reference(1, 4, [
                f"https://www.casinoatlnaticcity.com",
                f"https://demo-acp.calimaco.com",
            ])

            references_1 = list(set(filter(lambda x: x != "/" and x != "", alira_helper.sheets[1].data)))

            alira_helper.access_to_pages_tab()

            for reference in references_1:
                alira_helper.get_sheet_target_urls(
                    1, 4, 5,
                    [
                        f"https://www.casinoatlnaticcity.com",
                        f"https://demo-acp.calimaco.com",
                    ])
                alira_helper.url = reference
                alira_helper.target_urls = []
                for index, url in enumerate(alira_helper.sheets[1].data):
                    url.title = alira_helper.get_sheet_row_data(1, [26], url.id)
                    url.description = alira_helper.get_sheet_row_data(1, [28], url.id)
                    url.keywords = alira_helper.get_sheet_row_data(1, [
                        7, 9, 11, 13, 15, 17, 19, 21, 23
                    ], url.id)

                    # url.flag = True
                    alira_helper.target_urls.append(url)
                alira_helper.page = 1
                alira_helper.iterate_redirections_datatable_edit()
                while alira_helper.page < alira_helper.table_page_total:
                    alira_helper.iterate_redirections_datatable_edit()
            """ """

            alira_helper.iterate_redirections_datatable_save()

            driver.close()

        except (UnicodeDecodeError, StopIteration, Exception) as e:
            trace_helper = TraceHelper()

            print(f"Error on alira service: {trace_helper.get_trace_str(e)}")
        return self.alira_repository.set_seo_redirection(alira)

    def get_layouts(self, alira: Alira):
        pass

    def set_page_url(self, alira: Alira):
        return alira