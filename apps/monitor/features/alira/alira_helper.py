import math
from datetime import datetime
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as Wait

from core.domain.models.url import Url
from core.util.debug.trace_helper import TraceHelper
from core.util.excel.excel_helper import ExcelHelper
from core.util.excel.sheet import Sheet


class AliraHelper:

    def __init__(self, driver, url="", page=0, reload=False, layouts=[], target_urls=[], table_page_total=0):
        self.driver = driver
        self.url = url
        self.page = page
        self.reload = reload
        self.layouts = layouts
        self.target_urls = target_urls
        self.table_page_total = table_page_total
        self.sheets = []
        self.trace_helper = TraceHelper()

    def login(self, url, username="rterrones", password="P@ssw0rd123."):
        self.driver.maximize_window()
        self.driver.get(url)

        target_user = self.driver.find_element(By.ID, "alias")
        target_password = self.driver.find_element(By.ID, "password")
        target_submit = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-success.btn-block")

        target_user.send_keys("rterrones")
        target_password.send_keys("P@ssw0rd123.")
        target_submit.click()

        sleep(15)

    def access_to_redirections(self):
        if self.reload is True:
            print("reload enabled")
            # self.driver.get(self.url)
            # sleep(15)

        targets_menu = self.driver.find_elements(By.CSS_SELECTOR, ".has-submenu")
        print(f'------- menu list : {len(targets_menu)} ----------')

        target_menu = None

        try:
            for target in targets_menu:
                targets_menu_span = target.find_element(By.CSS_SELECTOR, ".text-uppercase")
                targets_menu_a = target.find_element(By.CSS_SELECTOR, "a")
                text = targets_menu_span.text.strip()
                print(f'-------------------- text : {text} -----------------------')

                if text == "SITIO WEB":
                    if target_menu is None:
                        target_menu = target
                    targets_menu_a.click()
                    sleep(5)
                    print("uwu")
                    raise StopIteration

        except (Exception, NoSuchElementException, StopIteration) as e:
            print(f"Error : {e}")

        target_menu_submenu_items = target_menu.find_elements(By.CSS_SELECTOR, "li")
        print(f'---------- sub menu items : {len(target_menu_submenu_items)} ------------')
        # target_menu_submenu_cms = None

        try:
            for submenu_target in target_menu_submenu_items:
                # target_menu_submenu_cms = target
                targets_menu_a = submenu_target.find_element(By.CSS_SELECTOR, "a")
                text = targets_menu_a.text.strip()
                print(f'-------------------- text : {text} -----------------------')

                if text == "Configuración":
                    targets_menu_a.click()
                    print("Configuración link clicked")
                    sleep(1)

                    ul = submenu_target.find_element(By.CSS_SELECTOR, "ul")
                    arr = ul.find_elements(By.CSS_SELECTOR, "a")
                    for a in arr:
                        text = a.text.strip()
                        if text == "Redirección":
                            a.click()
                            print("Configuración link clicked")
                            sleep(10)

                    raise StopIteration

        except (Exception, NoSuchElementException, StopIteration) as e:
            print(f"Error : {e}")

    def redirections_new(self, target_url: Url, save=False):
        if target_url.url != "/" \
                and target_url.url.strip() != ""\
                and target_url.new_url != "/"\
                and target_url.new_url.strip() != "":
            btn_new = self.driver.find_element(By.ID, "newRedirection")
            btn_new.click()
            sleep(4)
            print(f"add redirection to : {target_url.url}")
            """
            ----------- ADD ROW DATA ----------------
            """
            input_from_redirection = self.driver.find_element(By.ID, "from_redirection")
            input_to_redirection = self.driver.find_element(By.ID, "to_redirection")
            input_type_redirection = self.driver.find_element(By.ID, "type_redirection")
            input_comment_redirection = self.driver.find_element(By.ID, "comment_redirection")
            """
            """
            now = datetime.now()

            input_comment_redirection.clear()
            input_comment_redirection.send_keys(f'Creado por el bot de alira, fecha :'
                                                f'{now.strftime("%d/%m/%Y %H:%M")},'
                                                f' Url Origen : '
                                                f'{target_url.url}'
                                                f' Url Destino : '
                                                f'{target_url.new_url}')
            input_from_redirection.clear()
            input_from_redirection.send_keys(target_url.url)
            input_to_redirection.clear()
            input_to_redirection.send_keys(target_url.new_url)
            sleep(1)

            input_type_redirection.send_keys(target_url.redirection_type)
            sleep(1)
            """
            ------------------------
            """
            self.driver.implicitly_wait(5)
            # self.driver.execute_script("PageEditor.onGoToList(true)")
            if save is True:
                save_button = self.driver.find_element(By.ID, "saveRedirection")
                save_button.click()
                sleep(5)
                # self.driver.execute_script("PageEditor.onGoToList(true)")

            self.driver.execute_script('$("#newRedirectionModal").modal("hide")')

            sleep(2)

            # target_url_index = self.target_urls.index(target_url)
            self.target_urls[target_url.id].flag = False
            # target_url.flag = False
            print(f"{target_url.url} was set it {self.target_urls[target_url.id].flag}")

    def iterate_redirections_datatable_edit(self, save=False):

        table_target = Wait(self.driver, timeout=30).until(
            ec.visibility_of_element_located((By.ID, "allRedirections_wrapper")))
        # table_target.click()
        table_input = table_target.find_elements(By.CSS_SELECTOR, "input")[0]
        table_input.clear()
        table_input.send_keys(self.url)
        table_input.send_keys(Keys.RETURN)

        sleep(2)

        table_paginator = self.driver.find_element(By.CSS_SELECTOR, ".dataTables_paginate.paging_simple_numbers")
        table_paginator_options = table_paginator.find_elements(By.CSS_SELECTOR, "li")
        # table_paginator_next = driver.find_element(By.ID, "allPagesEditor_next")
        table_paginator_options_len = len(table_paginator_options) - 2

        current_window = self.driver.current_window_handle

        if table_paginator_options_len > 0:
            self.table_page_total = int(table_paginator_options[table_paginator_options_len].text.strip())

            print(f"-------- total pages: {self.table_page_total} ----------")
            try:
                # for index in range(self.table_page_total):
                if self.page > 1:
                    for thing in range(self.page - 1):
                        table_paginator_next_container = Wait(self.driver, timeout=20).until(
                            ec.visibility_of_element_located((By.ID, "allPagesEditor_next")))
                        table_paginator_next = table_paginator_next_container.find_element(By.CSS_SELECTOR, "a")
                        table_paginator_next.click()
                        sleep(2)

                print(f"--------- page : {self.page} ----------")

                table_target = Wait(self.driver, timeout=20).until(
                    ec.visibility_of_element_located((By.ID, "allRedirections_wrapper")))

                # sleep(4)

                table_target_tr_list = table_target.find_elements(By.CSS_SELECTOR, "tbody tr")

                try:
                    flag = False
                    for tr in table_target_tr_list:
                        tds = tr.find_elements(By.CSS_SELECTOR, "td")
                        target_urls = list(filter(lambda x: x.flag is True, self.target_urls))

                        if len(target_urls) == 0:
                            self.page = self.table_page_total
                            raise StopIteration

                        for target_url in target_urls:
                            target_url_str = target_url.url.strip()
                            td_str = ""
                            try:
                                td_str = tds[1].text
                                td_str = td_str.strip()
                            except Exception as e:
                                print(f"Error : {self.trace_helper.get_trace_str(e)}")
                            if target_url_str == td_str and target_url.flag is True:
                                print(f"there is a match with some url : {target_url.url}")
                                flag = True
                                sleep(1)
                                print("searching for link")
                                new_tab_links = tr.find_elements(By.CSS_SELECTOR, "a")
                                if len(new_tab_links) > 0 and len(new_tab_links) != 3:
                                    print(f"links founded : {len(new_tab_links)}")
                                    new_tab_links[0].click()
                                elif len(new_tab_links) == 3:
                                    print(f"3 links founded : {len(new_tab_links)}")
                                    new_tab_links[1].click()
                                print("loading page link")
                                sleep(5)
                                """
                                ----------- ADD ROW DATA
                                """
                                input_to_redirection = self.driver.find_element(By.ID, "to_redirection")
                                input_type_redirection = self.driver.find_element(By.ID, "type_redirection")
                                input_comment_redirection = self.driver.find_element(By.ID, "comment_redirection")
                                """
                                table_input.send_keys(self.url)
                                table_input.send_keys(Keys.RETURN)
                                """
                                now = datetime.now()

                                if target_url.new_url != "":
                                    input_comment_redirection.clear()
                                    input_comment_redirection\
                                        .send_keys(f'Modificado por el bot de alira, fecha :'
                                                   f' {now.strftime("%d/%m/%Y %H:%M")},'
                                                   f' Anterior valor: '
                                                   f"{input_to_redirection.get_attribute('value')}")

                                    input_to_redirection.clear()
                                    input_to_redirection.send_keys(target_url.new_url)
                                    sleep(1)

                                input_type_redirection.clear()
                                input_type_redirection.send_keys(target_url.redirection_type)
                                sleep(1)
                                """
                                ------------------------
                                """
                                # self.driver.execute_script("PageEditor.onGoToList(true)")
                                if save is True:
                                    save_button = self.driver.find_element(By.ID, "saveRedirection")
                                    save_button.click()
                                    sleep(5)

                                self.driver.execute_script('$("#editConstantsModal").modal("hide")')

                                sleep(2)
                                # target_url_index = self.target_urls.index(target_url)
                                self.target_urls[target_url.id].flag = False
                                # target_url.flag = False
                                print(f"{target_url.url} was set it {self.target_urls[target_url.id].flag}")
                                print(target_urls)

                    if flag is False:
                        self.page = self.page + 1

                except (Exception, NoSuchElementException, StopIteration) as e:
                    print(f"Error : {self.trace_helper.get_trace_str(e)}")

                if self.page == self.table_page_total:

                    raise StopIteration

            except (NoSuchElementException, StopIteration) as e:
                print(f"Error : {self.trace_helper.get_trace_str(e)}")
        else:
            table_input.clear()
            self.page = self.table_page_total
            print("--------- no results -------------")

    def iterate_redirections_datatable_save(self):

        try:
            target_urls = filter(lambda x: x.flag is True and x.url.strip() != "" and x.url != "/", self.target_urls)
            target_urls = filter(lambda x: x.new_url.strip() != "" and x.new_url != "/", target_urls)
            target_urls = list(
                target_urls
            )

            if len(target_urls) == 0:
                self.page = self.table_page_total
                raise StopIteration

            for target_url in target_urls:
                self.redirections_new(target_url=target_url)

            target_urls = list(filter(lambda x: x.flag is True, self.target_urls))
            print(target_urls)

        except (NoSuchElementException, StopIteration) as e:
            print(f"Error : {self.trace_helper.get_trace_str(e)}")

    def access_to_pages_tab(self):
        if self.reload is True:
            print("reload enabled")
            # self.driver.get(self.url)
            # sleep(15)

        targets_menu = self.driver.find_elements(By.CSS_SELECTOR, ".has-submenu")
        print(f'------- menu list : {len(targets_menu)} ----------')

        target_menu = None

        try:
            for target in targets_menu:
                targets_menu_span = target.find_element(By.CSS_SELECTOR, ".text-uppercase")
                targets_menu_a = target.find_element(By.CSS_SELECTOR, "a")
                text = targets_menu_span.text.strip()
                print(f'-------------------- text : {text} -----------------------')

                if text == "SITIO WEB":
                    if target_menu is None:
                        target_menu = target
                    targets_menu_a.click()
                    sleep(5)
                    print("uwu")
                    raise StopIteration

        except (Exception, NoSuchElementException, StopIteration) as e:
            print(f"Error : {e}")

        target_menu_submenu_items = target_menu.find_elements(By.CSS_SELECTOR, "li")
        print(f'---------- sub menu items : {len(target_menu_submenu_items)} ------------')
        # target_menu_submenu_cms = None

        try:
            for submenu_target in target_menu_submenu_items:
                # target_menu_submenu_cms = target
                targets_menu_a = submenu_target.find_element(By.CSS_SELECTOR, "a")
                text = targets_menu_a.text.strip()
                print(f'-------------------- text : {text} -----------------------')

                if text == "CMS":
                    targets_menu_a.click()
                    sleep(15)
                    print("cms link clicked")
                    raise StopIteration

        except (Exception, NoSuchElementException, StopIteration) as e:
            print(f"Error : {e}")

    def iterate_main_datatable(self, save=True):

        table_target = Wait(self.driver, timeout=30).until(
            ec.visibility_of_element_located((By.ID, "allPagesEditor")))
        # table_target.click()
        table_input = table_target.find_elements(By.CSS_SELECTOR, "input")[2]
        table_input.clear()
        table_input.send_keys(self.url)
        table_input.send_keys(Keys.RETURN)

        sleep(2)

        table_paginator = self.driver.find_element(By.CSS_SELECTOR, ".dataTables_paginate.paging_simple_numbers")
        table_paginator_options = table_paginator.find_elements(By.CSS_SELECTOR, "li")
        # table_paginator_next = driver.find_element(By.ID, "allPagesEditor_next")
        table_paginator_options_len = len(table_paginator_options) - 2

        current_window = self.driver.current_window_handle

        if table_paginator_options_len > 0:
            self.table_page_total = int(table_paginator_options[table_paginator_options_len].text.strip())

            print(f"-------- total pages: {self.table_page_total} ----------")
            try:
                # for index in range(self.table_page_total):
                if self.page > 1:
                    for thing in range(self.page - 1):
                        table_paginator_next_container = Wait(self.driver, timeout=20).until(
                            ec.visibility_of_element_located((By.ID, "allPagesEditor_next")))
                        table_paginator_next = table_paginator_next_container.find_element(By.CSS_SELECTOR, "a")
                        table_paginator_next.click()
                        sleep(2)

                print(f"--------- page : {self.page} ----------")

                table_target = Wait(self.driver, timeout=20).until(
                    ec.visibility_of_element_located((By.ID, "allPagesEditor")))

                sleep(4)

                table_target_tr_list = table_target.find_elements(By.CSS_SELECTOR, "tbody tr")

                try:
                    flag = False
                    for tr in table_target_tr_list:
                        tds = tr.find_elements(By.CSS_SELECTOR, "td")
                        target_urls = list(filter(lambda x: x.flag is True, self.target_urls))

                        if len(target_urls) == 0:
                            self.page = self.table_page_total
                            raise StopIteration

                        for target_url in target_urls:
                            target_url_str = target_url.url.strip()
                            td_str = ""
                            try:
                                td_str = tds[3].text
                                td_str = td_str.strip()
                            except Exception as e:
                                print(f"Error : {self.trace_helper.get_trace_str(e)}")
                            if target_url_str == td_str and target_url.flag is True:
                                print(f"there is a match with some url : {target_url.url}")
                                flag = True
                                print("searching for popup menu button")
                                new_tab_buttons = tr.find_elements(By.CSS_SELECTOR, "button")
                                new_tab_buttons[1].click()
                                sleep(1)
                                print("searching for link")
                                new_tab_links = tr.find_elements(By.CSS_SELECTOR, "a")
                                new_tab_links[1].click()
                                print("loading page link")
                                sleep(5)

                                target_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                                for target_button in target_buttons:
                                    data_id = target_button.get_attribute("data-id")

                                    if data_id == "pageLayout":
                                        title = target_button.get_attribute("title")
                                        self.layouts.append(title)

                                """
                                ----------- ADD ROW DATA
                                """
                                input_new_url = self.driver.find_element(By.ID, "pageUrl_es-ES")
                                input_title = self.driver.find_element(By.ID, "pageTitle_es-ES")
                                input_description = self.driver.find_element(By.ID, "pageDescription_es-ES")
                                input_keywords = self.driver.find_element(By.ID, "pageKeys_es-ES")
                                """
                                table_input.send_keys(self.url)
                                table_input.send_keys(Keys.RETURN)
                                """
                                if target_url.new_url != "":
                                    #input_new_url.send_keys(target_url.new_url)
                                    sleep(1)
                                if target_url.title != "":
                                    input_title.send_keys(target_url.title)
                                    sleep(1)
                                if target_url.description != "":
                                    input_description.send_keys(target_url.description)
                                    sleep(1)
                                if target_url.keywords != "":
                                    input_keywords.send_keys(target_url.keywords)
                                    sleep(1)
                                """
                                ------------------------
                                """
                                self.driver.implicitly_wait(5)
                                #self.driver.execute_script("PageEditor.onGoToList(true)")
                                if save is True:
                                    self.driver.execute_script("PageEditor.onSave()")
                                    sleep(5)
                                    self.driver.execute_script("PageEditor.onGoToList(true)")
                                else:
                                    self.driver.execute_script("PageEditor.onGoToList(true)")
                                # cancel_page_button = self.driver.find_element(By.ID, "cancelPage")
                                # cancel_page_button.click()
                                sleep(5)
                                self.target_urls[target_url.id].flag = True
                                print(f"{target_url.url} was set it {self.target_urls[target_url.id].flag}")
                                print(target_urls)

                    if flag is False:
                        self.page = self.page + 1

                except (Exception, NoSuchElementException, StopIteration) as e:
                    print(f"Error : {self.trace_helper.get_trace_str(e)}")

                if self.page == self.table_page_total:
                    raise StopIteration

            except (NoSuchElementException, StopIteration) as e:
                print(f"Error : {self.trace_helper.get_trace_str(e)}")
        else:
            table_input.clear()
            self.page = self.table_page_total
            print("--------- no results -------------")

    def get_kwr(self, excel_path):

        sheets = [
            Sheet("Categorías", 0, [
                "N1 Actual",
                "Propuesta",
                "URL actual",
                "URL propuesta",
                "Acción SEO prioritarias",
                "KW 1",
                "SV 1",
                "KW 2",
                "SV 2",
                "KW 3",
                "SV 3",
                "KW 4",
                "SV 4",
                "KW 5",
                "SV 5",
                "KW 6",
                "SV 6",
                "KW 7",
                "SV 7",
                "KW 8",
                "SV 8",
                "KW 9",
                "SV 9",
                "H1",
                "Meta Title",
                "Len 1",
                "Meta Descripción",
                "Len 2",
                "Publicados metadatos",
                "Canonical"
            ]),
            Sheet("Casino online", 0, [
                "Subcategoría actual 1",
                "Subcategoría propuesta - N2",
                "Subcategoría actual 2",
                "Subcategoría propuesta - N3",
                "URL actual",
                "URL propuesta",
                "Acción SEO prioritarias",
                "KW 1",
                "SV 1",
                "KW 2",
                "SV 2",
                "KW 3",
                "SV 3",
                "KW 4",
                "SV 4",
                "KW 5",
                "SV 5",
                "KW 6",
                "SV 6",
                "KW 7",
                "SV 7",
                "KW 8",
                "SV 8",
                "KW 9",
                "SV 9",
                "H1",
                "Nuevo Meta Title",
                "Len 1",
                "Nueva  Meta Descripción",
                "Len 2",
                "Canonical",
            ]),
            Sheet("Apuestas deportivas", 0, [
                "Subcategoría actual",
                "Subcategoría propuesta - N2",
                "URL actual",
                "URL propuesta",
                "Acción SEO prioritarias",
                "KW 1",
                "SV 1",
                "KW 2",
                "SV 2",
                "KW 3",
                "SV 3",
                "KW 4",
                "SV 4",
                "KW 5",
                "SV 5",
                "KW 6",
                "SV 6",
                "KW 7",
                "SV 7",
                "KW 8",
                "SV 8",
                "KW 9",
                "SV 9",
                "KW 10",
                "SV 10",
                "KW 11",
                "SV 11",
                "H1",
                "Nuevo Meta Title",
                "Len 1",
                "Nueva Meta Descripción",
                "Len 2",
                "Canonical"
            ]),
            Sheet("Footer casino online", 0, [
                "SECCION",
                "NOMBRE",
                "URL",
                "INDEX"
            ]),
            Sheet("Footer apuestas deportivas", 0, [
                "SECCION",
                "NOMBRE",
                "URL",
                "INDEX"
            ])
        ]

        sheet_names = [sheets[i].name for i in range(len(sheets))]
        excel_helper = ExcelHelper(path=excel_path, sheet_name=sheet_names)
        for sheet in sheets:
            if len(sheet.columns) > 0:
                number_of_rows = excel_helper.df[sheet.name].shape[0]
                print(f"------ number_of_rows : {number_of_rows} -------")
                for time in range(number_of_rows):
                    print(f"reading {sheet.name} row {time + 1}, column {sheet.columns}")
                    row = excel_helper.get_row(sheet.name, time)
                    row_data = excel_helper.get_row_values(row, sheet.columns)
                    sheet.rows.append(row_data)
                self.sheets.append(sheet)

    def get_sheet_data_list(self, index, field_index, prefix=[]):
        for row in self.sheets[index].rows:
            if row[field_index]['value'] != "" and row[field_index]['value'] != "-":
                data_raw = row[field_index]['value']
                if len(prefix) > 0:
                    for p in prefix:
                        data_raw = data_raw.replace(p, "")
                self.sheets[index].data.append(data_raw)
        self.sheets[index].data = list(set(self.sheets[index].data))

    def get_sheet_row_data(self, index, field_indexes=[], row_index=0, prefix=[], action="concat"):
        result = []
        for field_index in field_indexes:
            if self.sheets[index].rows[row_index][field_index]['value'] != "" \
                    and self.sheets[index].rows[row_index][field_index]['value'] != "-":
                data_raw = self.sheets[index].rows[row_index][field_index]['value']
                if len(prefix) > 0 and type(data_raw) == str:
                    for p in prefix:
                        if prefix != "":
                            data_raw = data_raw.replace(p, "")
                    result.append(data_raw)
                elif type(data_raw) == float:
                    if math.isnan(self.sheets[index].rows[row_index][field_index]['value']) is False:
                        result.append(data_raw)
            else:
                print("concat message: " + self.sheets[index].rows[row_index][field_index]['value'])
        if action == "concat":
            fr = []
            for r in result:
                if type(r) != str:
                    r = str(r)
                fr.append(r)
            return ",".join(fr)
        else:
            return ""

    def get_sheet_url_reference(self, index, url_index, prefix=[]):
        self.sheets[index].data = []
        for row_index, row in enumerate(self.sheets[index].rows):
            # url = Url(row_index)
            if row[url_index]['value'] != "" and row[url_index]['value'] != "-":
                data_raw = row[url_index]['value']
                if type(data_raw) == str:
                    if len(prefix) > 0:
                        for thing in prefix:
                            if thing in data_raw:
                                data_raw = data_raw.replace(thing, "")
                                # data_raw = "/" + data_raw.split("/")[0]
                    else:
                        data_raw = data_raw.split("/")
                        print(f"url : {data_raw}")
                        data_raw = data_raw\
                            .replace(f'{data_raw[0]} + "/" + {data_raw[1]} + "/" + {data_raw[2]}', "")
                else:
                    data_raw = "/"

                # url.url = data_raw

                self.sheets[index].data.append(data_raw)

    def get_sheet_target_urls(self, index, url_index, new_url_index, prefix=[]):
        self.sheets[index].data = []
        for row_index, row in enumerate(self.sheets[index].rows):
            url = Url(row_index)
            if row[url_index]['value'] != "" and row[url_index]['value'] != "-":
                data_raw = row[url_index]['value']
                if type(data_raw) == str:
                    if len(prefix) > 0:
                        for thing in prefix:
                            if prefix != "":
                                data_raw = data_raw.replace(thing, "")
                            else:
                                data_raw = data_raw.split("/")
                                print(f"url : {data_raw}")
                                data_raw = data_raw\
                                    .replace(f'{data_raw[0]} + "/" + {data_raw[1]} + "/" + {data_raw[2]}', "")
                else:
                    data_raw = "/"

                url.url = data_raw

            if row[new_url_index]['value'] != "" and row[new_url_index]['value'] != "-":
                new_data_raw = row[new_url_index]['value']
                if type(new_data_raw) == str:
                    if len(prefix) > 0:
                        for thing in prefix:
                            if prefix != "":
                                new_data_raw = new_data_raw.replace(thing, "")
                            else:
                                new_data_raw = new_data_raw.split("/")
                                print(f"url : {new_data_raw}")
                                new_data_raw = new_data_raw \
                                    .replace(f'{new_data_raw[0]} + "/" + {new_data_raw[1]} + "/" + {new_data_raw[2]}', "")
                else:
                    new_data_raw = "/"

                url.new_url = new_data_raw

            self.sheets[index].data.append(url)
