from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as Wait

class SunatHelper:
    def __init__(self, driver, sunat_model=None):
        self.driver = driver
        self.sunat_model = sunat_model

    def get_session_storage_item(self, key, origin):
        """Retrieve an item from session storage of a specific origin."""
        script = f"""
        var storage = null;
        if (window.location.origin === '{origin}') {{
            storage = window.sessionStorage.getItem('{key}');
        }}
        return storage;
        """

        script = f"""
        var storage = null;
        
        storage = window.sessionStorage.getItem('{key}');
        
        return storage;
        """
        return self.driver.execute_script(script)

    def login_sunat(self):
        self.driver.maximize_window()
        self.driver.get(self.sunat_model.url)

        """
        <form role="form">
            <div class="form-group text-center">
                <div class="btn-group btn-group-sm" role="group">
                    <div class="btn-group" role="group">
                        <button type="button" class="btn active btnPor" id="btnPorRuc" style="margin-right: 3px;">RUC</button>
                    </div>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btnPor" id="btnPorDni" style="margin-left: 3px;">DNI</button>
                    </div>
                </div>
            </div>
            <div class="form-group" id="divFilaDni" style="display: none;">
                <input type="text" placeholder="DNI" id="txtDni" class="form-control" maxlength="8" value="">
            </div>

            <div class="form-group" id="divFilaRuc">
                <input type="text" placeholder="RUC" id="txtRuc" class="form-control" maxlength="11" value="">
            </div>
            <div class="form-group" id="divFilaUsuario">
                <input type="text" placeholder="Usuario" id="txtUsuario" class="form-control" maxlength="8" onblur="this.value=this.value.toUpperCase()" onchange="this.value=this.value.toUpperCase()" value="">
            </div>
            <div class="form-group" id="divFilaConstrasena">
                <input type="password" placeholder="Contraseña" id="txtContrasena" class="form-control" maxlength="12" onkeypress="return onPressEnter(this,event)" value="">
            </div>
            <div class="form-group">
                <div id="divFails" class="text-centro"></div>
            </div>
            <div class="text-center">
                <label id="lblRecuerdame" style="color: #808080">Recuérdame,
                    para entrar más fácil &nbsp;</label> <label class="switch"> <input type="checkbox" id="chkRecuerdame"> <span class="slider round"></span>
                </label>
            </div>

            <div class="text-center">
                        <!--<small><a id="aLinkOlvidaste" href="https://ww1.sunat.gob.pe/ol-ti-itmantpregrespsec/MantPregResp.htm" target='_blank'>�Olvidaste tu usuario o contrase�a?</a></small>-->
                        <small><span class="nivel1">¿Te olvidaste tu usuario o clave?</span></small>
                        <!-- fin de incorporado-->
            </div>
            <div id="divMensajeError" class="form-group text-center hidden">
                <div class="alert alert-danger text-left" role="alert">
                    <span class="glyphicon glyphicon-remove-sign" aria-hidden="true"></span> <span id="spanMensajeError"></span>
                </div>
            </div>
            <div class="text-center">
                <button id="btnAceptar" class="btn btn-sm btn-primary" type="button">Iniciar sesión</button>
            </div>
        </form>
        """

        # time_select = Wait(self.driver, timeout=20).until(
        #             ec.element_to_be_clickable((By.ID, "appointments_consulate_appointment_time")))

        ruc_input = self.driver.find_element(By.ID, "txtRuc")
        ruc_input.send_keys(self.sunat_model.ruc)

        user_input = self.driver.find_element(By.ID, "txtUsuario")
        user_input.send_keys(self.sunat_model.user)

        password_input = self.driver.find_element(By.ID, "txtContrasena")
        password_input.send_keys(self.sunat_model.password)
        
        btn_submit = self.driver.find_element(By.ID, "btnAceptar")
        btn_submit.click()

        sleep(3)

        # divOpcionServicio2
        option_btn = Wait(self.driver, timeout=30).until(
                    ec.element_to_be_clickable((By.ID, "divOpcionServicio2")))
        option_btn.click()

        sleep(1)

        ul_menu_li = self.driver.find_elements(By.CLASS_NAME, "nivel1")
        for li in ul_menu_li:
            text = li.text.strip()
            print(text)
            if text == "Guía de Remisión Electrónica":
                li.click()
                level_2 = self.driver.find_elements(By.CLASS_NAME, "nivel2")
                for _li in level_2:
                    sleep(1)
                    _text_tag = _li.find_element(By.CLASS_NAME, "spanNivelDescripcion")
                    _text = _text_tag.text.strip()
                    print(f"level 2: {_text}")
                    if _text == "Guía de Remisión Electrónica":
                        _li.click()
                        level_3 = self.driver.find_elements(By.CLASS_NAME, "nivel3")
                        for __li in level_3:
                            sleep(1)
                            __text_tag = __li.find_element(By.CLASS_NAME, "spanNivelDescripcion")
                            __text = __text_tag.text.strip()
                            print(f"level 3: {__text}")
                            if __text == "Consulta de GRE":
                                __li.click()
                                level_4 = self.driver.find_elements(By.CLASS_NAME, "nivel4")
                                for ___li in level_4:
                                    sleep(1)
                                    ___text_tag = ___li.find_element(By.CLASS_NAME, "spanNivelDescripcion")
                                    ___text = ___text_tag.text.strip()
                                    print(f"level 4: {___text}")
                                    if ___text == "Consulta de GRE":
                                        ___li.click()
                                        break

        # Retrieve the sessionStorage item
        # sunat_token = None
        # while sunat_token is None:
        #     sunat_token = self.driver.execute_script("let s = sessionStorage.getItem('SUNAT.token'); s;")
        # # sunat_token = self.driver.execute_script("var s = sessionStorage.getItem('SUNAT.token'); return s;")

        # Retrieve an item from session storage
        # wait = Wait(self.driver, 10)
        # wait.until(lambda driver: driver.execute_script("return window.sessionStorage.length > 0;"))

        # driver execute_script( "return Object.entries(sessionStorage);" )},

        # item_value = None
        # while item_value is None:
        #     item_key = "SUNAT.token"  # Replace with the key of the session storage item you want to retrieve
        #     script = f"return window.sessionStorage.getItem('{item_key}');"
        #     item_value = self.driver.execute_script(script)

        # Define the origin you are interested in
        origin = "https://e-factura.sunat.gob.pe"
        # disable alerts

        disable_alerts_script = """
        window.alert = function() {};
        window.confirm = function() { return true; };
        window.prompt = function() { return null; };
        window.addEventListener('beforeunload', function(event) {
            event.stopImmediatePropagation();
        });
        """
        self.driver.execute_script(disable_alerts_script)

        # Switch to the iframe
        iframe = self.driver.find_element(By.ID, "iframeApplication")
        self.driver.switch_to.frame(iframe)

        # Retrieve an item from session storage for the specified origin
        item_key = "SUNAT.token"  # Replace with the key of the session storage item you want to retrieve
        item_value = self.get_session_storage_item(item_key, origin)
        # Assign the retrieved token to your model or use it as needed
        self.sunat_model.sunat_token = item_value
    

