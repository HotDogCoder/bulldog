import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from apps.peru.domain.models.mtc_model import MtcModel
from apps.peru.domain.models.sunat_model import SunatModel
from apps.peru.presentation.controllers.mtc_controller import MtcController
from apps.peru.presentation.controllers.sunat_controller import SunatController

class SunatTokenView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):

        request_data = self.request.data

        sunat_model = SunatModel()
        sunat_model.ruc = request_data.get('ruc', '')
        sunat_model.user = request_data.get('user', '')
        sunat_model.password = request_data.get('password', '')

        SC = SunatController()
        response = SC.get_token(sunat_model)
        json_data = json.dumps(vars(response))
        return HttpResponse(json_data, content_type='application/json')
    
class CallaoTokenView(APIView):
    ## permission_classes = [HasAPIKey]

    def post(self, request):

        request_data = self.request.data

        mtc_model = MtcModel()
        mtc_model.registration_number = request_data.get('registration_number', '')

        MC = MtcController()
        response = MC.get_callao_car_tickets(mtc_model)
        json_data = json.dumps(vars(response))
        return HttpResponse(json_data, content_type='application/json')
    
class LimaTokenView(APIView):
    ## permission_classes = [HasAPIKey]

    def post(self, request):

        request_data = self.request.data

        mtc_model = MtcModel()
        mtc_model.registration_number = request_data.get('registration_number', '')
        mtc_model.site_key = request_data.get('site_key', '')

        MC = MtcController()
        response = MC.get_lima_car_tickets(mtc_model)
        json_data = json.dumps(vars(response))
        return HttpResponse(json_data, content_type='application/json')