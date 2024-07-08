import os
from datetime import datetime

import numpy as np
import pysftp
import pytz

from apps.monitor.application.repositories_interfaces.server_request_repository_interface import \
    ServerRequestRepositoryInterface
from apps.monitor.domain.models.server_request import ServerRequest
from apps.monitor.domain.models.server_request_filter import ServerRequestFilter
from apps.monitor.domain.models.sftp_parameter import SftpParameter
from core.config import constants


class ServerRequestRepository(ServerRequestRepositoryInterface):
    def __init__(self):
        super().__init__()

    def insert_server_request(self, server_request: ServerRequest):
        return server_request

    def select_server_request(self, server_request_filter: ServerRequestFilter):
        pass

    def get_server_request_files_data(self, server_request_filter: ServerRequestFilter):
        current_directory = os.getcwd()
        print(current_directory)

        return
        raw_line = []
        matriz_line = []
        with open(current_directory + '/py_app/u_ex210816.log', encoding='utf8') as f:
            for line in f:
                str_line = line.strip()
                str_line_array = str_line.split(' ')
                # print(str_line_array)
                raw_line.append(line.strip())
                matriz_line.append([str for str in str_line_array])

        num_raw_line = np.array(raw_line)
        num_matriz_line = np.array(matriz_line)
        # print(raw_line)
        return num_matriz_line

    def upload_file_into_external_folder(self, sftp_parameter: SftpParameter):
        with pysftp.Connection(
                host=sftp_parameter.host,
                username=sftp_parameter.user_name,
                password=sftp_parameter.password,
                port=sftp_parameter.port
        ) as sftp:
            print("sftp connection success")
            sftp.cwd(sftp_parameter.target_path)
            fnames = sftp.listdir()
            shared_directory_list = os.listdir(f'{constants.SHARED_FOLDER}')
            tz = pytz.timezone('America/Bogota')
            time = datetime.now(tz).strftime('%H%M')
            print(f'file in sftp server will have {time} in the name')
            # if sftp_parameter.directory_name in shared_directory_list:
            # print('old file list: ', fnames)
            if sftp_parameter.directory_name in fnames:
                print('directory maybe exists')
                if not sftp.isdir('test'):
                    print('warning there is some file with the same name of the target folder')
                    print('creating directory anyway')
                    sftp.rename(sftp_parameter.directory_name, f"{sftp_parameter.directory_name}_backup")
                    sftp.mkdir(sftp_parameter.directory_name)
                else:
                    print('directory exist the file will be created or replaced there')
            else:
                sftp.mkdir(sftp_parameter.directory_name)
                print(f'{sftp_parameter.directory_name} folder was created')

            directories_files_inside = sftp.listdir(sftp_parameter.directory_name)
            directories_inside = [dir for dir in directories_files_inside if sftp.isdir(f'{sftp_parameter.directory_name}/{dir}')]
            print('there is this directories inside: ', directories_inside)
            sftp.cwd(sftp_parameter.directory_name)
            print('creating new one for this cut ......')
            count = len(directories_inside) + 1
            sftp.mkdir(f'{sftp_parameter.directory_name}_{count}')
            print(f'{sftp_parameter.directory_name}_{count} created')

            try:
                shared_directory_file_list = [file for file in shared_directory_list if
                                              os.path.isfile(f'{constants.SHARED_FOLDER}\{file}') and f'_{sftp_parameter.directory_name}_' in file]
                for shared_directory_file in shared_directory_file_list:
                    if not os.path.isdir(f'{constants.SHARED_FOLDER}\{shared_directory_file}'):
                        print(f'coping {constants.SHARED_FOLDER}\{shared_directory_file}')
                        accepted_extensions = ['txt']
                        file_name_arr = shared_directory_file.split('.')
                        extension = file_name_arr[-1]
                        if extension in accepted_extensions:
                            sftp.put(
                                f'{constants.SHARED_FOLDER}\{shared_directory_file}',
                                preserve_mtime=True,
                                remotepath=f"/{sftp_parameter.target_path}/{sftp_parameter.directory_name}/{sftp_parameter.directory_name}_{count}/{file_name_arr[0]}_{time}.{extension}"
                            )
            except FileNotFoundError as e:
                print('check if your local file exists :')
                print(e)
            else:
                fnames = sftp.listdir()
                print('new file list :', fnames)

            # else:
                # print(f'{sftp_parameter.directory_name} do not exist in shared folder')

        print('----------------------------------------------------------------')
        return False
