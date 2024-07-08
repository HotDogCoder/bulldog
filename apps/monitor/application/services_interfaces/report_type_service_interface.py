from abc import ABC, abstractmethod
from apps.monitor.domain.models.report_type_model import ReportTypeModel
class ReportTypeServiceInterface(ABC):
    def __init__(self):
        super().__init__()


    @abstractmethod
    def get_report_type(self, report_type_model: ReportTypeModel):
        return report_type_model
