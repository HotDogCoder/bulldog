from django.db import connections

class MonitorRouter:
    """
    A router to control all database operations on models in the
    monitoreo application.
    """
    app_name = 'monitor'

    def db_for_read(self, model, **hints):
        """
        Attempts to read monitoreo models go to monitoreo database.
        """
        if model._meta.app_label == self.app_name:
            return 'monitor_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write monitoreo models go to monitoreo database.
        """
        if model._meta.app_label == self.app_name:
            return 'monitor_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the monitoreo app is involved.
        """
        if obj1._meta.app_label == self.app_name or \
           obj2._meta.app_label == self.app_name:
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the monitoreo app only appears in the monitoreo database.
        """
        if app_label == self.app_name:
            return db == 'monitor_db'
        return None
