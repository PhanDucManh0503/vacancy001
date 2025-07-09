import pytest
import datetime
from base.base_test import BaseTest
from pages.login_page import LoginPage
from pages.vacancy_page import Vacancies
from utils.read_config import ConfigReader


class TestVacancy(BaseTest):
    def test_vacancy_flow(self, driver):
        # Bước 1: Login vào OrangeHRM
        login_page = LoginPage(self.driver)
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())

        # Khởi tạo page Vacancies
        vacancy_page = Vacancies(self.driver)

        # Bước 2: Click menu Recruitment > tab Vacancies
        vacancy_page.go_to()

        # Bước 3: Click "+ Add" button
        vacancy_page.click_add()

        # Bước 4: Verify Add Vacancy page hiển thị
        assert (
            vacancy_page.is_add_vacancy_displayed()
        ), "Add Vacancy page không hiển thị"

        # Bước 5: Điền thông tin Vacancy
        today = datetime.date.today().strftime("%Y-%m-%d")
        vacancy_name = f"Automation Tester For {today}"
        vacancy_page.fill_add_vacancy_form(
            vacancy_name=vacancy_name,
            job_title="API Tester",
            description="Automation Test Is Running",
            number_of_position="1",
            active=False,
            publish_rss_webpage=True,
        )

        # Bước 6: Click Save button
        vacancy_page.click_save()

        # Bước 7: Verify Edit Vacancy page hiển thị
        assert (
            vacancy_page.is_edit_vacancy_displayed()
        ), "Edit Vacancy page không hiển thị"

        # Bước 8: Click Cancel button
        vacancy_page.click_cancel()

        # Bước 9: Verify quay lại trang Vacancies
        assert (
            vacancy_page.is_vacancy_page_displayed_again()
        ), "Không quay lại trang Vacancies"

        # # Bước 10: Chọn Job Title + Hiring Manager và click Search
        # vacancy_page.search_vacancy(
        #     job_title="Automation Tester", hiring_manager=ConfigReader.get_username()
        # )

        # # Bước 11: Verify có ít nhất 1 item tồn tại
        # assert vacancy_page.has_search_result(), "Không có kết quả tìm kiếm"

        # # Bước 12: Verify dữ liệu hiển thị khớp với dữ liệu đã nhập
        # expected_data = {
        #     "vacancy_name": vacancy_name,
        #     "job_title": "Automation Tester",
        #     "hiring_manager": ConfigReader.get_username(),
        #     "positions": "1",
        #     "status": "Inactive",  # Vì Active=False
        # }
        # vacancy_page.verify_search_results(expected_data)

        # # Bước 13: Logout
        # vacancy_page.logout()
