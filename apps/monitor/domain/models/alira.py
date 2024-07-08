from apps.monitor.features.alira.alira_helper import AliraHelper


class Alira:

    def __init__(self, url, image_name_prefix, driver, alira_helper: AliraHelper):
        self.url = url
        self.image_name_prefix = image_name_prefix
        self.driver = driver
        self.image_list = []
        self.data_list = []
        self.alira_helper = alira_helper

