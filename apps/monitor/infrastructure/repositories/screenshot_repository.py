from datetime import datetime
from time import sleep

import json
import requests
from apps.monitor.application.repositories_interfaces.screenshot_repository_interface import \
    ScreenshotRepositoryInterface
from apps.monitor.domain.models.screenshot import Screenshot
from apps.monitor.models import ReportType
from apps.monitor.models import Report, ReportScreenshot
from core.config import constants
from core.util.debug.trace_helper import TraceHelper

class ScreenshotRepository(ScreenshotRepositoryInterface):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all_report_types():
        # report_types = session.query(ReportTypesTable).all()
        # session.close()
        # report_type = ReportTypeModel()
        report_types = ReportType.custom_objects.all()

        return report_types

    @staticmethod
    def get_report_types(id=0):
        # report_types = session.query(ReportTypesTable).all()
        # session.close()
        # report_type = ReportTypeModel()
        if id == 0:
            report_types = ReportType.custom_objects.all()
        elif id > 0:
            report_types = ReportType.custom_objects.filter(id=id)
        return report_types

    @staticmethod
    def add_report(name, code, description):
        report = Report.custom_objects.create(name = name, code = code, description = description, created_at = datetime.now())
        report.save()
        
        return report

    @staticmethod
    def add_report_screenshot(name, path, report_id, report_type_id):
        report_screenshot = ReportScreenshot.custom_objects.create(name = name,path = path,report_id = report_id,
                                             report_type_id = report_type_id,created_at = datetime.now())
        report_screenshot.save()

        return report_screenshot

    def upload_screeshots(self, report_screenshot):
        url = constants.API_UPLOAD_SCREENSHOT
        multiple_files = []

        filename = report_screenshot.path.split('/').pop()
        multiple_files.append(
            ('multi-files', (filename, open(report_screenshot.path, 'rb'), 'image/png'))
        )
        r = requests.post(url, files=multiple_files)
        output = json.loads(r.content)
        paths = output['paths']
        report_screenshot.path = paths[0]

        report_screenshot = self.add_report_screenshot(
            name=f"screenshot_{report_screenshot.report_id}_{report_screenshot.report_type_id}",
            path=report_screenshot.path,
            report_id=report_screenshot.report_id,
            report_type_id=report_screenshot.report_type_id
        )

        return report_screenshot

    def take_screenshot_of_servers_status_1(self, screenshot: Screenshot):
        # report_type = ReportType(base=self.base.declarative_base)
        paths = []
        for index, report_type in enumerate(screenshot.trash):
            for report_screenshot in report_type.screenshots:
                new_report_screenshot = self.upload_screeshots(report_screenshot)
                paths.append(new_report_screenshot.path)

        # paths = []

        current_datetime = datetime.now()

        for file in paths:

            url = constants.API_WHATSAPP_WEB
            body = {
                'message': '',
                'number': screenshot.to,
                'photo': f'{constants.API_WHATSAPP_WEB_BOT}/{file}'
            }
            r = requests.post(url, json=body)
            print(f'send whatsapp: {r.content}')
            sleep(5)

        screenshot.paths = paths
        # session.close()
        return screenshot

    def test_atlantic_city_casino_and_sports(self, screenshot: Screenshot):
        pass
