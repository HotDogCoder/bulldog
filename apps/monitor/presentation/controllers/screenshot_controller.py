from apps.monitor.application.services.screenshot_service import ScreenshotService
from apps.monitor.domain.models.screenshot import Screenshot


class ScreenshotController:

    def __init__(self):
        self.screenshot_service = ScreenshotService()

    def take_screenshot_of_servers_status_1(self, screenshot: Screenshot):
        return self.screenshot_service.take_screenshot_of_servers_status_1(screenshot)

    def test_atlantic_city_casino_and_sports(self, screenshot: Screenshot):
        return self.screenshot_service.test_atlantic_city_casino_and_sports(screenshot)