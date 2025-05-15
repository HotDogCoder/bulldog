from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as Wait
from twocaptcha import TwoCaptcha

class MtcHelper:
    def __init__(self, driver, mtc_model=None):
        self.driver = driver
        self.mtc_model = mtc_model

    def get_callao_car_tickets(self):
        self.driver.maximize_window()
        self.driver.get(self.mtc_model.url)

        captcha_element = self.driver.find_element(By.XPATH, '//*[@alt="captcha"]')
        captcha_element.get_attribute('src')

        solver = TwoCaptcha('f37d1c71dd4c02bb257a19698fb329b1')

        captcha_base64 = captcha_element.get_attribute('src').split(',')[1]

        try:
            result = solver.normal(captcha_base64)
            captcha_text = result['code']
            print("CAPTCHA solved:", captcha_text)
        except Exception as e:
            print("Error solving CAPTCHA:", e)
            self.driver.quit()
            exit()

        self.mtc_model.captcha_text = captcha_text

        input_captcha = self.driver.find_element(By.ID, 'captcha')
        input_captcha.send_keys(captcha_text)

        input_registration_number = self.driver.find_element(By.ID, 'valor_busqueda')
        input_registration_number.send_keys(self.mtc_model.registration_number)
        
        search_button = self.driver.find_element(By.ID, 'idBuscar')  
        search_button.click()

        table = Wait(self.driver, 10).until(
            ec.presence_of_element_located((By.ID, 'dataTable'))
        )
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            if len(columns) > 0:
                ticket = {
                    'ticket_code': columns[2].text,
                    'ticket_number': columns[3].text,
                    'ticket_date': columns[4].text,
                    'ticket_amount': columns[5].text,
                    'ticket_quote_number': columns[6].text
                }

                pdf_button = row.find_element(By.TAG_NAME, 'i')
                pdf_button.click()
                
                miModal = Wait(self.driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'miModal'))
                )
                embed = Wait(miModal, 10).until(
                    ec.presence_of_element_located((By.TAG_NAME, 'embed'))
                )
                sleep(2)
                ticket['pdf_url'] = embed.get_attribute('src')
                # close the modal btn-close
                close_button = miModal.find_element(By.CLASS_NAME, 'btn-close')
                close_button.click()

                self.mtc_model.tickets.append(ticket)

    def get_lima_car_tickets(self):
        self.driver.maximize_window()
        self.driver.get(self.mtc_model.url)
        # solver = TwoCaptcha('f37d1c71dd4c02bb257a19698fb329b1')

        a_tags = self.driver.find_elements(By.TAG_NAME, 'a')
        for a_tag in a_tags:
            if str.lower(a_tag.text) == 'consultas de papeletas.':
                # remove _blank from href
                href = a_tag.get_attribute('href')
                self.mtc_model.url = href
                # click on the link
                a_tag.click()
                # self.driver.get(self.mtc_model.url)
                break

        # sleep(4)

        # switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        # frameset id frameSetPrincipal
        # self.driver.switch_to.frame('frameSetPrincipal')
        # iframe id fraRightFrame
        self.driver.switch_to.frame('fraRightFrame')

        search_type_select = Wait(self.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'tipoBusquedaPapeletas'))
        )
        search_type_select.click()
        search_type_select.find_element(By.XPATH, "//option[@value='busqPlaca']").click()

        # wait for input field to be present must have placeholder 'Ingrese Placa'
        input_registration_number = Wait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@placeholder='Ingrese Placa']"))
        )
        input_registration_number.send_keys(self.mtc_model.registration_number)

        # solve captcha using data-sitekey 
        solver = TwoCaptcha('f37d1c71dd4c02bb257a19698fb329b1')
        
        try:
            result = solver.recaptcha(
                sitekey=self.mtc_model.site_key,
                url=self.mtc_model.url,
                version='v2',
                # proxy={'id': 'proxy_id', 'data': 'proxy_data'}
            )
            captcha_text = result['code']
            print("CAPTCHA solved:", captcha_text)
            self.mtc_model.captcha_text = captcha_text
            # textarea id g-recaptcha-response
            
        except Exception as e:
            print("Error solving CAPTCHA:", e)
            self.driver.quit()
            exit()

        # execute script to set the value of g-recaptcha-response
        self.driver.execute_script(
            "document.getElementById('g-recaptcha-response').innerHTML = arguments[0];", 
            captcha_text
        )

        # input type submit value 'Buscar'
        search_button = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Buscar']")
        search_button.click()

        # wait for the table to be present
        table = Wait(self.driver, 10).until(
            ec.presence_of_element_located((By.TAG_NAME, 'table'))
        )

        # get the tbody
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        # the first row is the header get the indexs of the columns that does not have the class HiddenCol
        columns = tbody.find_elements(By.TAG_NAME, 'tr')[0].find_elements(By.TAG_NAME, 'td')
        column_indices = [
            index for index, col in enumerate(columns) 
            if 'HiddenCol' not in col.get_attribute('class')
        ]
        
        # get the rows
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        # iterate over the rows from the second row
        for row in rows[1:]:
            columns = row.find_elements(By.TAG_NAME, 'td')
            if len(columns) > 0:
                ticket = {
                    'ticket_regulation': columns[2].text,
                    'ticket_code': columns[3].text,
                    'ticket_number': columns[4].text,
                    'ticket_date': columns[5].text,
                    'ticket_amount': columns[6].text,
                    'ticket_cost': columns[7].text,
                    'ticket_discount': columns[8].text,
                    'ticket_debt': columns[9].text,
                    'ticket_status': columns[10].text,
                    'ticket_license': columns[12].text,
                    'ticket_document_type': columns[13].text,
                    'ticket_document_number': columns[14].text,
                }

                # pdf button
                pdf_button = row.find_element(By.TAG_NAME, 'a')
                pdf_button.click()

                sleep(2)
                # switch to the new tab
                self.driver.switch_to.window(self.driver.window_handles[2])
                
                image_tag = Wait(self.driver, 10).until(
                    ec.presence_of_element_located((By.ID, 'imgPapel'))
                )
                ticket['image_url'] = image_tag.get_attribute('src')

                self.mtc_model.tickets.append(ticket)

                # return to the tab 0
                self.driver.switch_to.window(self.driver.window_handles[1])
        