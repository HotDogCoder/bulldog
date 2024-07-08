from .main_request import MainRequest


class ServerRequest(MainRequest):

    def __init__(self, method, request_type, os, port, url):
        super().__init__(method, request_type)
        self._error = None
        self.os = os
        self.port = port
        self.url = url
        self.__secret = "some secret"

    def set_error(self, error):
        self._error = error

    def get_error(self):
        if hasattr(self, "_error"):
            return self._error
        else:
            return "no error"

    def getMethod(self):
        return self.method

    # class methods
    @classmethod
    def get_request_types(cls):
        return cls.REQUEST_TYPES

    # static methods
    __server_request_list = None

    @staticmethod
    def get_server_request_list():
        if ServerRequest.__server_request_list is None:
            ServerRequest.__server_request_list = []
        return ServerRequest.__server_request_list
