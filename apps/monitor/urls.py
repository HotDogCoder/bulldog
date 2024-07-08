from django.urls import path
from .views import *


urlpatterns = [
    path('screenshot', StartMonitoreo.as_view()),
    path('report-type', ReportTypeView.as_view()),
    # path('getvmwarereport', GetVmwareReport.as_view()),
    # path('profile/<account>', DetailUserProfileView.as_view()),
]