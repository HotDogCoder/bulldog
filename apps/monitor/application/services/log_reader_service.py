import os
import pytz
from datetime import datetime

from apps.monitor.application.services_interfaces.log_reader_service_interface import LogReaderServiceInterface
from apps.monitor.domain.models.log_reader import LogReader
from apps.monitor.infrastructure.repositories.log_reader_repository import LogReaderRepository


class LogReaderService(LogReaderServiceInterface):

    def __init__(self):
        super().__init__()
        self.log_reader_repository = LogReaderRepository()

    def read_log_file_directories(self, log_reader: LogReader):

        try:
            daily_directory_list = os.listdir(f'{log_reader.local_path}')

            tz = pytz.timezone(log_reader.timezone)
            if log_reader.date_string != '':
                inspect_date = datetime.strptime(log_reader.date_string, '%Y-%m-%d').astimezone(tz).strftime('%y%m%d')
            else:
                inspect_date = datetime.now(tz).strftime('%y%m%d')

            # print('Inspect Date: ', log_reader.date_string)
            # print('Timezone: ', log_reader.timezone)
            # print('Local Path: ', log_reader.local_path)
            # if log_reader.read_all:
                # print('--read-all true: reading all the files')

            # print(f'searching for file with {inspect_date} in the name')

            for daily_directory in daily_directory_list:
                daily_directory_file_list = os.listdir(f'{log_reader.local_path}/{daily_directory}')
                if log_reader.read_all is False:
                    daily_directory_file_list = [x for x in daily_directory_file_list if inspect_date in x]

                # print(daily_directory_file_list)
                for daily_directory_file in daily_directory_file_list:
                    log_reader.last_file_readed = f'{log_reader.local_path}/{daily_directory}/{daily_directory_file}'
                    # print('reading', log_reader.last_file_readed)

                    file = open(
                        f'{log_reader.local_path}/{daily_directory}/{daily_directory_file}',
                        mode='r',
                        encoding='utf8',
                        errors='ignore'
                    )

                    for line in file:
                        log_reader.counter = log_reader.counter + 1

                        line_split = line.split(' ')

                        if 'GET' in line_split:
                            log_reader.get_counter = log_reader.get_counter + 1

                        if 'POST' in line_split:
                            log_reader.post_counter = log_reader.post_counter + 1

                        if log_reader.counter == log_reader.limit:
                            log_reader.message = 'Too much lines'
                            raise StopIteration

        except (UnicodeDecodeError, StopIteration) as e:

            print('error in: ', log_reader.last_file_readed)
            print('line: ', log_reader.counter + 1)
            print('error: ', e)
        
        return self.log_reader_repository.read_log_file_directories(log_reader)

