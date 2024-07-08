class MainRequest:

    REQUEST_METHODS = ("GET", "POST", "PUT")
    REQUEST_TYPES = ("SERVER", "API", "WEB", "AJAX")

    def __init__(self, method, request_type):
        self.method = method
        if request_type not in MainRequest.REQUEST_TYPES:
            raise ValueError(f"{request_type} is not a valid type")
        else:
            self.type = request_type
        if method not in MainRequest.REQUEST_METHODS:
            raise ValueError(f"{request_type} is not a valid type of request.")
        else:
            self.method = request_type

