import json
from time import sleep
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from apps.monitor.domain.models.report_type_model import ReportTypeModel
from apps.monitor.domain.models.screenshot import Screenshot
from apps.monitor.models import VmwareMachine
from apps.monitor.presentation.controllers.report_type_controller import ReportTypeController

from apps.monitor.presentation.controllers.screenshot_controller import ScreenshotController

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
# Create your views here.
import ssl
# from pyVim.connect import SmartConnect, Disconnect
# from pyVmomi import vim, vmodl
# import paramiko

from apps.monitor.serializers import VmwareMachineSerializer

# class GetVmwareReport(APIView):
#     def post(self, request, format=None):
#         request_data = self.request.data

#         # Información de conexión al servidor VMware
#         hostname = request_data['hostname'] # '10.0.10.107'
#         username = request_data['username'] # 'pe280\jporras'
#         password = request_data['password'] # 'Z@bb1.2022'

#         # Desactivar la verificación del certificado SSL
#         context = ssl._create_unverified_context()

#         # Conexión al servidor VMware
#         si = SmartConnect(host=hostname, user=username, pwd=password, sslContext=context)

#         # Obtiene el objeto rootFolder
#         content = si.RetrieveContent()
#         root_folder = content.rootFolder

#         # Obtiene todas las máquinas virtuales en el servidor
#         vm_view = content.viewManager.CreateContainerView(
#             container=root_folder,
#             type=[vim.VirtualMachine],
#             recursive=True
#         )

#         vms = vm_view.view
#         vm_view.Destroy()

#         result_data = []
#         # Imprime el nombre de todas las máquinas virtuales
#         for index, vm in enumerate(vms):
            
#             new_data = VmwareMachine()
#             # print("---------------------------------")
#             # Imprime el nombre de la máquina virtual
#             # print(f'{index}. Nombre: {vm.name}')
#             new_data.name = f"{index}. {vm.name}"
#             # Obtener el objeto de la configuración de la VM
#             config = vm.config
            
#             # with open(f'vm/{vm.name}.json','a', encoding='utf-8') as file:
#             #    file.write(f'{config}\n')

#             new_data.annotation = config.annotation

#             for nic in vm.guest.net:
#                 if nic.network != None:
#                     if nic.ipConfig != None:
#                         for ip in nic.ipConfig.ipAddress:
#                             if ip.state == "preferred":
#                                 new_data.ip = ip.ipAddress
                    
#             # Obtener el objeto padre de la máquina virtual
#             parent_obj_1 = vm.parent
#             parent_obj_2 = vm.parent.parent
#             parent_obj_3 = vm.parent.parent.parent
#             parent_obj_4 = vm.parent.parent.parent.parent

#             # print(f'dato 1: {type(parent_obj_1)}:{parent_obj_1.name}')
#             # print(f'dato 2: {type(parent_obj_2)}:{parent_obj_2.name}')
#             # print(f'dato 3: {type(parent_obj_3)}:{parent_obj_3.name}')
#             # print(f'dato 4: {type(parent_obj_4)}')

#             new_data.data_1 = parent_obj_1.name
#             new_data.data_2 = parent_obj_2.name
#             new_data.data_3 = parent_obj_3.name
#             new_data.data_4 = type(parent_obj_4)

#             # Obtiene el estado de encendido
#             if vm.summary.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
#                 new_data.status = "Encendida"
#                 # print('Estado: Encendida')
#             else:
#                 new_data.status = "Apagada"
#                 # print('Estado: Apagada')

#             # Obtiene la cantidad de memoria RAM
#             mem_size = vm.summary.config.memorySizeMB
#             # print(f'Memoria RAM: {mem_size} MB')
#             new_data.ram = mem_size/1024
#             # Obtiene la cantidad de procesadores
#             cpu_count = vm.summary.config.numCpu
#             # print(f'Procesadores: {cpu_count}')
#             new_data.processors = cpu_count
#             # print(f'Sockets: {config.hardware.numCoresPerSocket}')
#             new_data.sockets = config.hardware.numCoresPerSocket
#             # Obtiene el tamaño del disco duro
#             disk_size = vm.summary.storage.committed / (1024*1024)
#             # print(f'Disco Duro: {disk_size:.2f} GB')
#             new_data.disk = disk_size
#             # Obtiene el idioma del sistema operativo
#             guest_id = vm.config.guestId
#             guest_full_name = vm.config.guestFullName
#             # print(f'Sistema Operativo: {guest_full_name} ({guest_id})')
#             new_data.os = f"{guest_full_name} ({guest_id})"

#             # get guest information
#             guest_info = vm.guest
#             with open(f'vm/{vm.name}.json','a', encoding='utf-8') as file:
#                file.write(f'{vars(vm.config)}\n')

#             # Create an SSH client and connect to the virtual machine
#             ssh = paramiko.SSHClient()
#             ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             ssh.connect(new_data.ip, username=username, password=password)

#             # Run a command on the virtual machine
#             stdin, stdout, stderr = ssh.exec_command('ls -la')

#             # Print the output of the command
#             print(stdout.read().decode('utf-8'))

#             # Close the SSH connection
#             ssh.close()

#             result_data.append(new_data)
#         # Desconexión del servidor VMware
#         Disconnect(si)

#         json_data = json.dumps({
#             'result_data': VmwareMachineSerializer(result_data, many=True).data,
#             'request_data': request_data
#         })
        
#         return HttpResponse(json_data, content_type='application/json')


class StartMonitoreo(APIView):
    def post(self, request, format=None):
        driver = 'Chrome'
        image_name_prefix = 'screenshot_'

        request_data = self.request.data

        screenshot = Screenshot(
            url="https://demo-acp.calimaco.com/",
            image_name_prefix=image_name_prefix,
            driver=driver,
            id=request_data['id'],
            to=request_data['to']
        )

        SC = ScreenshotController()
        SS = SC.take_screenshot_of_servers_status_1(screenshot=screenshot)

        print('------------- termino -----------------')
        print(SS.image_list)

        json_data = json.dumps({
            'image_paths': SS.paths,
            'request_data': request_data
        })
        
        return HttpResponse(json_data, content_type='application/json')

class ReportTypeView(APIView):
    def post(self, request, format=None):
        request_data = self.request.data

        report_type_model = ReportTypeModel()

        RC = ReportTypeController()
        RC = RC.get_report_type(report_type_model=report_type_model)

        json_data = json.dumps(vars(RC))
        return HttpResponse(json_data, content_type='application/json')

    def get(self, request, format=None):
        # text = request.GET.get('text', '')
        # if not text:
        #     return HttpResponseBadRequest("Missing 'text' parameter")

        report_type_model = ReportTypeModel()

        RC = ReportTypeController()
        RC = RC.get_report_type(report_type_model=report_type_model)

        json_data = json.dumps(vars(RC))
        return HttpResponse(json_data, content_type='application/json')
