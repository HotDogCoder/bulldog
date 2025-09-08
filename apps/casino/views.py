from django.shortcuts import render
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from apps.casino.domain.models.zera_model import ZeraModel
from apps.casino.presentation.controllers.zera_controller import ZeraController
# Create your views here.


class ZeraUsersView(APIView):
    # permission_classes = [HasAPIKey]

    def post(self, request):

        request_data = self.request.data

        zera_model = ZeraModel()
        zera_model.page = request_data.get('page', 0)
        zera_model.username = request_data.get('username', '')
        zera_model.password = request_data.get('password', '')
        zera_model.language = request_data.get('language', 'en')
        zera_model.from_year = request_data.get('from_year', '')
        zera_model.from_month = request_data.get('from_month', '')
        zera_model.to_year = request_data.get('to_year', '')
        zera_model.to_month = request_data.get('to_month', '')
        zera_model.url = request_data.get('url', 'https://ag.casinozera.com/index.php')
        zera_model.target_user = request_data.get('target_user', '')

        MC = ZeraController()
        response = MC.get_users(zera_model)
        json_data = json.dumps(vars(response))
        return HttpResponse(json_data, content_type='application/json')