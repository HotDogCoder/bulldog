from django.db import models

class ReportTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('monitor_db')

class ReportManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('monitor_db')

class ReportScreenshotManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('monitor_db')