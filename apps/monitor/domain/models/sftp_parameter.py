class SftpParameter:
    def __init__(self, host, port, user_name, password, private_key_file_path, local_file_path, target_path, directory_name):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password
        self.private_key_file_path = private_key_file_path
        self.local_file_path = local_file_path
        self.target_path = target_path
        self.directory_name = directory_name
