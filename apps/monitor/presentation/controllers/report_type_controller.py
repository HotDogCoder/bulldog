from apps.monitor.application.services.report_type_service import ReportTypeService
from apps.monitor.domain.models.report_type_model import ReportTypeModel
class ReportTypeController:
    def __init__(self):
        super().__init__()
        self.report_type_service = ReportTypeService()

    def get_report_type(self, report_type_model: ReportTypeModel):
        return self.report_type_service.get_report_type(report_type_model)
