from rest_framework import serializers

from apps.monitor.models import ReportType


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ['description', 'url', 'created_at']