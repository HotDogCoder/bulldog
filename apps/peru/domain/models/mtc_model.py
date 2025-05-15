class MtcModel:
    def __init__(self):
        self.id = None
        ## selenium webdriver params
        self.url = ""
        self.driver = None
        self.chrome_driver_path = ""
        self.captcha_text = ""
        self.site_key = ""

        self.ruc = ""
        self.ruc_type = ""
        self.ruc_status = ""
        self.ruc_date = None
        self.ruc_expiration_date = None
        self.ruc_renewal_date = None
        self.registration_number = ""
        self.registration_date = None
        self.registration_type = ""
        self.registration_status = ""
        self.tickets = []
        self.license_plate = ""
        self.license_plate_type = ""
        self.license_plate_status = ""
        self.license_plate_date = None
        self.license_plate_expiration_date = None
        self.license_plate_renewal_date = None
        self.license_plate_renewal_status = ""
        self.license_plate_renewal_type = ""
        self.license_plate_renewal_expiration_date = None
        pass


