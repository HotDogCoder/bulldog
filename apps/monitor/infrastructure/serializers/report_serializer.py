from rest_framework import serializers

from apps.monitor.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['name', 'code', 'description', 'created_at']

