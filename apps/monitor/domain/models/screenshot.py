from apps.monitor.models import Report


class Screenshot:

    def __init__(self, url, image_name_prefix, driver, report: Report = None, id=0, to=None):
        self.url = url
        self.image_name_prefix = image_name_prefix
        self.driver = driver
        self.image_list = []
        self.report = report
        self.report_types = []
        self.trash = []
        self.paths = []
        self.id = id
        self.to = to

