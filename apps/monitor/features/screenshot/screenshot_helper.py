import math
import os
from datetime import datetime
from time import sleep

import pytz
from selenium.webdriver.common.by import By

from apps.monitor.domain.models.screenshot import Screenshot
from apps.monitor.models import ReportScreenshot, ReportType
from core.util.path.path_helper import PathHelper


class ScreenshotHelper:

    def __init__(self):
        pass

    @staticmethod
    def scroll_and_take_screenshot(screenshot: Screenshot, report_type, driver, target_iterations=None, zoom=None):
        my_trash = []
        tz = pytz.timezone('America/Bogota')
        directory_name = datetime.now(tz).strftime('%Y%m%d%H%M%S')
        driver.maximize_window()
        driver.get(report_type.url)
        sleep(10)

        targets = driver.find_elements(By.CSS_SELECTOR, ".react-grid-item")

        target = driver.find_element(By.CSS_SELECTOR, '.react-grid-layout')
        target_height = target.get_attribute('style')
        target_arr = target_height.split(' ')
        target_string = target_arr[1]
        target_string = target_string.strip()
        target_string = target_string.replace('}', '')
        target_string = target_string.replace("'", '')
        target_string = target_string.replace("px", '')
        target_string = target_string.replace(";", '')
        target_height_value = int(target_string)

        print(f'----------- number of chars : {len(targets)} ----------------')

        if zoom is not None:
            driver.execute_script(f"document.body.style.zoom='{zoom}%'")
            sleep(15)

        size = driver.get_window_size()
        scroll_height = driver.execute_script(
            f"var scroll_targets = document.querySelectorAll('.scrollbar-view');"
            f"return scroll_targets[1].scrollHeight;"
        )
        client_height = driver.execute_script("return document.documentElement.clientHeight")

        target_height_clear = client_height + 10

        trash = (scroll_height - client_height) % client_height
        if target_iterations is None:
            target_iterations = math.floor((scroll_height - client_height) / client_height)

        print(f"----------- screen height :{client_height} ----------------")
        print(f"----------- scroll tag height : {target_string} ----------------")

        sleep(5)

        print(f"----------- scroll tag iterations : {target_iterations} ----------------")

        path_helper = PathHelper()
        current_directory = path_helper.get_project_root_path()

        driver.save_screenshot(
            f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
            f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_0_{directory_name}.png")

        my_trash.append(

            ReportScreenshot(
                path=f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                     f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_0_{directory_name}.png",
                report_id=screenshot.report.id,
                report_type_id=report_type.id
            )
        )
        screenshot.image_list.append(
            f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
            f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_0_{directory_name}.png")

        sleep(5)

        if trash == 0 and target_iterations > 1:
            for x in range(target_iterations - 1):
                driver.execute_script(f"var scroll_targets = document.querySelectorAll('.scrollbar-view');"
                                      f"var scroll_target = scroll_targets[1];"
                                      f"scroll_target.scrollTo(0, {target_height_clear * (x + 1)});")

                sleep(10)

                driver.implicitly_wait(100)

                driver.save_screenshot(
                    f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                    f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{x + 1}_{directory_name}.png")

                my_trash.append(
                    ReportScreenshot(
                        path=f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                             f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{x + 1}_{directory_name}.png",
                        report_id=screenshot.report.id,
                        report_type_id=report_type.id
                    )
                )
                screenshot.image_list.append(
                    f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                    f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{x + 1}_{directory_name}.png")

        if trash > 0 and target_iterations > 1:

            for x in range(target_iterations - 1):
                driver.execute_script(f"var scroll_targets = document.querySelectorAll('.scrollbar-view');"
                                      f"var scroll_target = scroll_targets[1];"
                                      f"scroll_target.scrollTo(0, {target_height_clear * (x + 1)});")

                sleep(10)

                driver.implicitly_wait(100)

                driver.save_screenshot(
                    f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                    f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{x + 1}_{directory_name}.png")
                my_trash.append(
                    ReportScreenshot(
                        path=f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                             f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{x + 1}_{directory_name}.png",
                        report_id=screenshot.report.id,
                        report_type_id=report_type.id
                    )
                )
                screenshot.image_list.append(
                    f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                    f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{x + 1}_{directory_name}.png")

            if trash > 0.15:
                driver.execute_script(f"var scroll_targets = document.querySelectorAll('.scrollbar-view');"
                                      f"var scroll_target = scroll_targets[1];"
                                      f"scroll_target.scrollTo(0, {target_height_clear * (target_iterations + trash)});")

                sleep(10)

                driver.implicitly_wait(100)

                driver.save_screenshot(
                    f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                    f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{target_iterations}_{directory_name}.png")
                my_trash.append(
                    ReportScreenshot(
                        path=f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                             f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{target_iterations}_{directory_name}.png",
                        report_id=screenshot.report.id,
                        report_type_id=report_type.id
                    )
                )
                screenshot.image_list.append(
                    f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                    f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_{target_iterations}_{directory_name}.png")

        report_type.screenshots = my_trash
        screenshot.trash.append(report_type)

    @staticmethod
    def scroll_and_take_screenshot_monitoreo(screenshot: Screenshot, report_type: ReportType, driver,
                                             target_iterations=None, zoom=None):
        my_trash = []
        tz = pytz.timezone('America/Bogota')
        directory_name = datetime.now(tz).strftime('%Y%m%d%H%M%S')

        driver.maximize_window()
        driver.get(report_type.url)
        sleep(10)
        if zoom is not None:
            driver.execute_script(f"document.body.style.zoom='{zoom}%'")

        scroll_pause_time = 5
        sleep(scroll_pause_time)

        target = driver.find_element(By.CSS_SELECTOR, 'html')

        size = driver.get_window_size()
        target_height_clear = size.get('height') - 163 - 30 - 64 - 130
        target_height_value = driver.execute_script("return document.querySelector('html').scrollHeight")
        target_iterations = math.floor(target_height_value / target_height_clear)

        print(f"----------- screen height :{size.get('height')} ----------------")
        print(f"----------- scroll tag height : {target_height_value} ----------------")
        print(f"----------- scroll tag iterations : {target_iterations} ----------------")

        path_helper = PathHelper()
        current_directory = path_helper.get_project_root_path()

        driver.save_screenshot(
            f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
            f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_0_{directory_name}.png")
        
        my_trash.append(
            ReportScreenshot.custom_objects.create(
                path=f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
                     f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_0_{directory_name}.png",
                report_id=screenshot.report.id,
                report_type_id=report_type.id
            )
        )
        
        screenshot.image_list.append(
            f"{current_directory}/storage/screenshots/{screenshot.image_name_prefix}"
            f"{datetime.now().strftime('%y%m%d')}_{report_type.id}_0_{directory_name}.png")
        
        report_type.screenshots = my_trash
        screenshot.trash.append(report_type)