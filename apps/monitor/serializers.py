from rest_framework import serializers
from .models import VmwareMachine

class VmwareMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VmwareMachine
        fields = '__all__'