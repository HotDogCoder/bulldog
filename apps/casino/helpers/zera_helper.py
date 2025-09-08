from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import csv
import os

class ZeraHelper:
    def __init__(self, driver, zera_model=None):
        self.driver = driver
        self.zera_model = zera_model


    def login_zera(self):
        """This method should contain the logic to log in to the Zera platform."""
        # Implement the login logic here
        self.driver.get(self.zera_model.url)
        # Additional login steps would go here
        self.driver.find_element("name", "login").send_keys(self.zera_model.username)
        self.driver.find_element("name", "password").send_keys(self.zera_model.password)
        
        # get the login button and click it this is a button with the text Entrar or Enter
        if self.zera_model.language == 'es':
            self.driver.find_element("xpath", "//button[contains(text(), 'Entrar')]").click()
        elif self.zera_model.language == 'en':
            self.driver.find_element("xpath", "//button[contains(text(), 'Enter')]").click()


    def set_filter_form_parameters(self, start_date=None, end_date=None):
        """Fill filters, click Mostrar/Show, and wait for the new table."""

        wait = Wait(self.driver, 30)

        # --- fill the From date ---
        if start_date:
            from_field = wait.until(ec.element_to_be_clickable((By.ID, "from-date")))
            from_field.clear()
            from_field.send_keys(start_date.strftime("%d-%m-%Y"))

        # --- fill the To date (optional) ---
        if end_date:
            to_field = wait.until(ec.element_to_be_clickable((By.ID, "to-date")))
            to_field.clear()
            to_field.send_keys(end_date.strftime("%d-%m-%Y"))

        # --- click the search button ---
        button_text = "Mostrar" if self.zera_model.language == "es" else "Show"
        search_btn = wait.until(
            ec.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
        )
        search_btn.click()

        # --- wait for the old table to go stale, then for the new one to appear ---
        wait.until(ec.staleness_of(search_btn))                                   # old DOM gone
        wait.until(ec.presence_of_element_located((By.ID, "users-table")))  
        
        sleep(1)      # new table ready

    def get_offset(self):
        # form-control select-number select-offset
        """Get the current offset value from the dropdown."""
        wait = Wait(self.driver, 30)
        offset_dropdown = wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, ".form-control.select-number.select-offset"))
        )
        # get len of options
        options = offset_dropdown.find_elements(By.TAG_NAME, "option")
        return len(options)

    def export_excel(self):
        
        offsets = self.get_offset()  # Ensure the table is loaded and we have the offset
        init = 1
        if self.zera_model.page > 0:
            init = self.zera_model.page
        for i in range(init, offsets + 1):
            # if i > 0:
            # Click the offset dropdown and select the option
            new_url = f"{self.zera_model.url}?act=admin&area=users&cashier=all&id=1319162&offset={i}"
            self.driver.get(new_url)
            
            sleep(2)  # wait for the page to load
            # Click the export button
            wait = Wait(self.driver, 30)
            export_button = wait.until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, ".xls-icon.right-icon"))
            )
            export_button.click()

        sleep(2)  # wait for the download to complete

    def extract_table_data(self):
        """Return a list of dicts for the rows that have real data."""
        wait = Wait(self.driver, 30)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#users-table tbody tr")))

        rows = self.driver.find_elements(By.CSS_SELECTOR, "#users-table tbody tr")

        for row in rows:
            cells = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]

            if not cells or not cells[0] or cells[0] == "No matching records found":
                continue

            self.zera_model.users.append({
                "id":            cells[0],
                "username":      cells[1],
                "currency_iso":  cells[2],
                "data":          cells[3],
                "balance":       cells[4],
                "credit":        cells[5],
                "debit":         cells[6],
                "gains":         cells[7],
                "rtp":           cells[8],
                "jackpots":      cells[9],
                "bonifications": cells[10],
                "users": []
            })

        for index, user in enumerate(self.zera_model.users):
            # self.driver.get(f"{self.zera_model.url}?act=admin&area=users&id={user['id']}")
            # sleep(2)  # wait for the page to load
            # self.get_users_from_user(index)
            if self.zera_model.target_user.lower() in user['username'].lower():
                self.driver.get(f"{self.zera_model.url}?act=admin&area=users&id={user['id']}")
                sleep(2)  # wait for the page to load
                self.export_excel()
    
    def get_users_from_user(self, index):
        """Return a list of dicts for the rows that have real data."""
        wait = Wait(self.driver, 30)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#users-table tbody tr")))

        rows = self.driver.find_elements(By.CSS_SELECTOR, "#users-table tbody tr")

        for row in rows:
            cells = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]

            if len(cells) == 10:
                # skip rows that don't have enough cells (e.g., empty rows)
                if not cells or not cells[0] or cells[0] == "No matching records found":
                    continue

                self.zera_model.users[index]['users'].append({
                    "id":            cells[0],
                    "username":      cells[1],
                    "email":         cells[2],
                    "name":          cells[3],
                    "balance":       cells[4],
                    "data":          cells[5],
                    "credit":        cells[6],
                    "debit":         cells[7],
                    "gains":         cells[8],
                    "game":         cells[9]
                })

            elif len(cells) == 9:
                # skip rows that don't have enough cells (e.g., empty rows)
                if not cells or not cells[0] or cells[0] == "No matching records found":
                    continue

                self.zera_model.users[index]['users'].append({
                    "id":            cells[0],
                    "username":      cells[1],
                    "name":          cells[2],
                    "balance":       cells[3],
                    "data":          cells[4],
                    "credit":        cells[5],
                    "debit":         cells[6],
                    "gains":         cells[7],
                    "game":         cells[8]
                })

            elif len(cells) == 11:
                # skip empty or “No matching…” placeholder rows
                if not cells or not cells[0] or cells[0] == "No matching records found":
                    continue

                self.zera_model.users[index]['users'].append({
                    "id":            cells[0],
                    "username":      cells[1],
                    "currency_iso":  cells[2],
                    "data":          cells[3],
                    "balance":       cells[4],
                    "credit":        cells[5],
                    "debit":         cells[6],
                    "gains":         cells[7],
                    "rtp":           cells[8],
                    "jackpots":      cells[9],
                    "bonifications": cells[10],
                })



    def save_nested_users_to_csv(self, output_dir="user_csvs"):
        """Create one CSV per user with their nested users (children), sanitized and |-delimited."""
        os.makedirs(output_dir, exist_ok=True)

        for user in self.zera_model.users:
            user_id = user["id"]
            nested_users = user.get("users", [])
            if not nested_users:
                continue

            # All potential keys + new balance breakdown fields
            all_keys = [
                "id", "username", "email", "name", "currency_iso", "data", "balance",
                "credit", "debit", "gains", "rtp", "jackpots", "bonifications", "game",
                "wagered", "wager", "chargeable", "total"
            ]

            def parse_balance_fields(balance_str):
                """Extract subfields from balance if formatted with multiple lines."""
                fields = {
                    "wagered": "0",
                    "wager": "0",
                    "chargeable": "0",
                    "total": "0"
                }

                if not isinstance(balance_str, str):
                    return balance_str, fields

                lines = balance_str.split('\n')

                if len(lines) < 2:
                    return balance_str.strip(), fields  # No extra info, leave as-is, fill with 0s

                # Parse each line like "Wagered: 1,340.00/10,000.00"
                for line in lines:
                    if ':' in line:
                        key, val = line.split(':', 1)
                        key = key.strip().lower()
                        val = val.strip()
                        if key in fields:
                            fields[key] = val

                # Remove newlines from balance field (keep full string flattened)
                flat_balance = ' '.join(line.strip() for line in lines)
                return flat_balance, fields

            normalized_users = []
            for nu in nested_users:
                cleaned = {}
                for key in all_keys:
                    cleaned[key] = ""

                for k, v in nu.items():
                    cleaned[k] = v.strip() if isinstance(v, str) else v

                # Parse balance into flat string + subfields
                cleaned["balance"], subfields = parse_balance_fields(cleaned.get("balance", ""))
                cleaned.update(subfields)

                normalized_users.append(cleaned)

            file_path = os.path.join(output_dir, f"user_{user_id}.csv")

            with open(file_path, mode="w", newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=all_keys, delimiter='|')
                writer.writeheader()
                for row in normalized_users:
                    writer.writerow(row)
