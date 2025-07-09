from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Vacancies:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 5
        # Các locator cho các phần tử trên trang Vacancies
        self.menu_recruitment = (By.XPATH, "//span[text()='Recruitment']")
        self.tab_vacancies = (By.XPATH, "//a[text()='Vacancies']")
        self.button_add = (By.XPATH, "//button[contains(., 'Add')]")
        self.title_add_vacancy = (By.XPATH, "//h6[text()='Add Vacancy']")
        self.button_save = (
            By.XPATH,
            "//button[@type='submit' and contains(., 'Save')]",
        )

        #
        self.input_vacancy_name = (
            By.XPATH,
            "//label[text()='Vacancy Name']/following::input[1]",
        )
        self.dropdown_job_title = (
            By.XPATH,
            "//label[text()='Job Title']/following::div[contains(@class,'oxd-select')]",
        )
        self.input_description = (
            By.XPATH,
            "//label[text()='Description']/following::textarea[1]",
        )
        self.input_hiring_manager = (
            By.XPATH,
            "//label[text()='Hiring Manager']/following::input[1]",
        )
        self.input_number_of_position = (
            By.XPATH,
            "//label[text()='Number of Positions']/following::input[1]",
        )
        self.checkbox_active = (
            By.XPATH,
            "//label[text()='Active']/following::input[1]",
        )
        self.checkbox_publish = (
            By.XPATH,
            "//label[text()='Publish in RSS Feed and Web Page']/following::input[1]",
        )
        self.title_edit_vacancy = (By.XPATH, "//h6[text()='Edit Vacancy']")
        self.button_cancel = (By.XPATH, "//button[contains(., 'Cancel')]")
        self.title_vacancies = (By.XPATH, "//h5[text()='Vacancies']")

        self.filter_job_title = (
            By.XPATH,
            "//label[text()='Job Title']/following::div[contains(@class,'oxd-select-wrapper')][1]",
        )
        self.filter_hiring_manager = (
            By.XPATH,
            "//label[text()='Hiring Manager']/following::input[1]",
        )
        self.button_search = (By.XPATH, "//button[normalize-space()='Search']")

        self.search_result_rows = (
            By.XPATH,
            "//div[@role='row' and .//div[text()='Automation Tester']]",
        )

        self.result_rows = (By.XPATH, "//div[@role='row' and position()>1]")

        self.user_profile_menu = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
        self.logout_item = (By.XPATH, "//a[text()='Logout']")

    def go_to(self):
        # Bấm vào menu Recruitment
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.menu_recruitment)
        ).click()

        # Bấm vào tab Vacancies
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.tab_vacancies)
        ).click()

    def click_add(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.button_add)
        ).click()

    def is_add_vacancy_displayed(self):
        return (
            WebDriverWait(self.driver, 10)
            .until(EC.visibility_of_element_located(self.title_add_vacancy))
            .is_displayed()
        )

    def select_job_title(self, job_title):
        from time import sleep

        # Click dropdown
        job_title_dropdown = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.XPATH, "//div[@class='oxd-select-text-input']")
        )
        job_title_dropdown.click()
        sleep(5)
        # Chờ option render và click chọn
        select_job_title = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(
                By.XPATH, f"//div[@role='listbox']//span[text()='{job_title}']"
            )
        )
        select_job_title.click()

    def get_current_user_name(self):
        user_name_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[@class='oxd-userdropdown-name']")
            )
        )
        return user_name_element.text.strip()

    def fill_hiring_manager(self):
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver import ActionChains
        from time import sleep

        # 1️⃣ Lấy current_user_name từ profile
        current_user_name = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[@class='oxd-userdropdown-name']")
                )
            )
            .text.strip()
        )
        print(f"[INFO] Current user name: {current_user_name}")

        # 2️⃣ Gõ 1 phần tên vào field Hiring Manager để trigger recommend
        manager_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.input_hiring_manager)
        )
        manager_input.clear()
        manager_input.send_keys(current_user_name[:3])  # Gõ vài ký tự đầu
        sleep(10)

        # 3️⃣ Dùng ActionChains để move, select recommend
        actions = ActionChains(self.driver)
        actions.move_to_element(manager_input)  # Di chuột tới field
        actions.click()  # Click để focus
        actions.send_keys(Keys.ARROW_DOWN)  # Chọn dòng recommend đầu tiên
        actions.send_keys(Keys.ENTER)  # Confirm chọn
        actions.perform()

        print(f"[INFO] Đã chọn Hiring Manager: {current_user_name}")

    def set_active_checkbox(self, active):
        wait = WebDriverWait(self.driver, self.timeout)

        # 1️⃣ Tìm wrapper chứa label "Active"
        wrapper_xpath = "//p[text()='Active']/following-sibling::div[@class='oxd-switch-wrapper']//span[contains(@class,'oxd-switch-input')]"
        checkbox_span = wait.until(
            EC.element_to_be_clickable((By.XPATH, wrapper_xpath))
        )

        # 2️⃣ Kiểm tra trạng thái hiện tại
        is_checked = "oxd-switch-input--active" in checkbox_span.get_attribute("class")

        # 3️⃣ Click nếu trạng thái chưa đúng
        if is_checked != active:
            checkbox_span.click()
            print(f"[INFO] Đã set checkbox Active = {active}")

    def set_publish_checkbox(self, publish):
        wait = WebDriverWait(self.driver, self.timeout)

        # 1️⃣ Tìm wrapper chứa label "Publish in RSS Feed and Web Page"
        wrapper_xpath = "//p[text()='Publish in RSS Feed and Web Page']/following-sibling::div[@class='oxd-switch-wrapper']//span[contains(@class,'oxd-switch-input')]"
        checkbox_span = wait.until(
            EC.element_to_be_clickable((By.XPATH, wrapper_xpath))
        )

        # 2️⃣ Kiểm tra trạng thái hiện tại
        is_checked = "oxd-switch-input--active" in checkbox_span.get_attribute("class")

        # 3️⃣ Click nếu trạng thái chưa đúng
        if is_checked != publish:
            checkbox_span.click()
            print(f"[INFO] Đã set checkbox Publish = {publish}")

    def fill_add_vacancy_form(
        self,
        vacancy_name,
        job_title,
        description,
        number_of_position,
        active=True,
        publish_rss_webpage=False,
    ):
        # 1️⃣ Điền Vacancy Name
        vacancy_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.input_vacancy_name)
        )
        vacancy_input.clear()
        vacancy_input.send_keys(vacancy_name)

        # 2️⃣ Chọn Job Title
        self.select_job_title(job_title)

        # 3️⃣ Điền Description
        desc_input = self.driver.find_element(*self.input_description)
        desc_input.clear()
        desc_input.send_keys(description)

        # 4️⃣ Điền Hiring Manager
        self.fill_hiring_manager()

        # 5️⃣ Điền Number of Positions
        pos_input = self.driver.find_element(*self.input_number_of_position)
        pos_input.clear()
        pos_input.send_keys(number_of_position)

        # 6️⃣ Set checkbox Active
        self.set_active_checkbox(active)

        # 7️⃣ Set checkbox Publish
        self.set_publish_checkbox(publish_rss_webpage)

    def click_save(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.button_save)
        ).click()

    def is_edit_vacancy_displayed(self):
        return (
            WebDriverWait(self.driver, 10)
            .until(EC.visibility_of_element_located(self.title_edit_vacancy))
            .is_displayed()
        )

    def click_cancel(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.button_cancel)
        ).click()

    def is_vacancy_page_displayed_again(self):
        return (
            WebDriverWait(self.driver, 10)
            .until(EC.visibility_of_element_located(self.title_vacancies))
            .is_displayed()
        )

    # def search_vacancy(self, job_title):
    #     wait = WebDriverWait(self.driver, self.timeout)

    #     # 🔥 Lấy current user name từ profile
    #     current_user_name = wait.until(
    #         EC.visibility_of_element_located(
    #             (By.XPATH, "//p[@class='oxd-userdropdown-name']")
    #         )
    #     ).text.strip()

    #     # 👉 Log để debug
    #     print(f"[INFO] Current user name (Hiring Manager): {current_user_name}")

    #     # 1️⃣ Mở dropdown Job Title
    #     job_title_dropdown = wait.until(
    #         EC.element_to_be_clickable(
    #             (
    #                 By.XPATH,
    #                 "//label[text()='Job Title']/following-sibling::div//div[contains(@class,'oxd-select-text-input')]",
    #             )
    #         )
    #     )
    #     job_title_dropdown.click()

    #     # 2️⃣ Chọn Job Title
    #     option_xpath = f"//div[@role='listbox']//span[text()='{job_title}']"
    #     option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
    #     option.click()

    #     # 3️⃣ Gõ vào Hiring Manager
    #     manager_input = wait.until(
    #         EC.visibility_of_element_located(
    #             (By.XPATH, "//input[@placeholder='Type for hints...']")
    #         )
    #     )
    #     manager_input.clear()
    #     manager_input.send_keys(current_user_name)

    #     # 4️⃣ Chọn dòng suggest bằng ActionChains
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(manager_input)
    #     actions.send_keys(Keys.ARROW_DOWN)
    #     actions.send_keys(Keys.ENTER)
    #     actions.perform()

    #     # 5️⃣ Click Search
    #     search_button = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    #     )
    #     search_button.click()
    #     print(
    #         f"[INFO] Search với Job Title: {job_title}, Hiring Manager: {current_user_name}"
    #     )

    #     WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable(self.filter_job_title)
    #     ).click()

    #     # Chọn Job Title
    #     self.driver.find_element(
    #         By.XPATH, f"//div[@role='option']/span[text()='{job_title}']"
    #     ).click()

    #     # Nhập Hiring Manager
    #     self.driver.find_element(*self.filter_hiring_manager).send_keys(hiring_manager)

    #     # Bấm Search
    #     self.driver.find_element(*self.button_search).click()

    def has_search_result(self):
        rows = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.search_result_rows)
        )
        return len(rows) >= 1

    def verify_search_results(self, expected_data: dict):
        rows = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.result_rows)
        )
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//div[@role='cell']")
            assert expected_data["vacancy_name"] in columns[1].text
            assert expected_data["job_title"] == columns[2].text
            assert expected_data["hiring_manager"] == columns[3].text
            assert expected_data["positions"] == columns[4].text
            assert expected_data["status"] == columns[5].text

    def logout(self):
        # Mở menu profile
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.user_profile_menu)
        ).click()

        # Click vào Logout
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.logout_item)
        ).click()
