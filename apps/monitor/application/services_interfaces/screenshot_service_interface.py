from abc import ABC, abstractmethod

from apps.monitor.domain.models.screenshot import Screenshot


class ScreenshotServiceInterface(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def take_screenshot_of_servers_status_1(self, screenshot: Screenshot):
        return screenshot

    @abstractmethod
    def test_atlantic_city_casino_and_sports(self, screenshot: Screenshot):
        return screenshot


