import traceback
import datetime
import re
import pytz

from core.util.path.path_helper import PathHelper


class TraceHelper:
    def __init__(self, prefix="log"):
        self.prefix = prefix
        self.message = ""
        self.trace = ""
        self.image = ""
        self.log_lines = []
        tz = pytz.timezone('America/Bogota')
        self.now = datetime.datetime.now(tz).strftime('%Y%m%d%H%M%S')
        self.path_helper = PathHelper()
        self.path = f'{self.path_helper.get_project_root_path()}/storage/logs'
        self.folder_path = self.path_helper.create_directory(self.path)

    @staticmethod
    def get_trace_str(e):
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        return traceback_str

    @staticmethod
    def xml_escape(chars, data_dict):
        return chars.encode('ascii', 'xmlcharrefreplace').decode()

    def log_open(self):
        # Get current date and time
        with open(f'{self.folder_path}/{self.prefix}_{self.now}.html',
                  'a', encoding='utf-8') as file:
            # self.log_lines.append(text)
            file.write(f'<html>\n')
            file.write(f'<body>\n')

    def log_close(self):
        # Get current date and time
        with open(f'{self.folder_path}/{self.prefix}_{self.now}.html',
                  'a', encoding='utf-8') as file:
            # self.log_lines.append(text)
            file.write(f'</body>\n')
            file.write(f'</html>\n')

    def log(self, text="", type="TEXT", width=200):
        # Get current date and time
        with open(f'{self.folder_path}/{self.prefix}_{self.now}.html',
                  'a', encoding='utf-8') as file:
            # self.log_lines.append(text)
            if type == "TEXT":
                file.write(f'<p>{text}</p><br/>\n')
            elif type == "STYLE_IMG":
                pattern = r"url\((.*?)\)"

                result = re.search(pattern, text)

                if result:
                    url = result.group(1)
                    file.write(f'<img width="{width}" src={url} /><br/>\n')
                else:
                    file.write(f'<p>NO CONTIENE IMAGEN</p><br/>\n')
            elif type == "URL_IMG":
                
                file.write(f'<img width="{width}" src={url} /><br/>\n')
                