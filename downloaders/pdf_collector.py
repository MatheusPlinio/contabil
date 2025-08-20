from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PDFCollector:
    def __init__(self, driver):
        self.driver = driver

    def collect(self, year: int, month_name: str):
        self.driver.get("https://www.natal.rn.gov.br/dom")

        Select(self.driver.find_element(By.NAME, "ano")
               ).select_by_visible_text(str(year))
        Select(self.driver.find_element(By.NAME, "mes")
               ).select_by_visible_text(month_name)

        self.driver.find_element(
            By.CSS_SELECTOR, "button[data-attach-loading]").click()

        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@id='example']//tbody//tr")))

        pdf_urls = set()

        while True:
            rows = self.driver.find_elements(
                By.XPATH, "//table[@id='example']//tbody//tr")
            for row in rows:
                link = row.find_element(By.TAG_NAME, "a").get_attribute("href")
                pdf_urls.add(link)

            page_numbers = self.driver.find_elements(
                By.XPATH, "//div[@id='example_paginate']//li[not(contains(@class,'previous') or contains(@class,'next'))]")
            current_page = self.driver.find_element(
                By.XPATH, "//div[@id='example_paginate']//li[contains(@class,'active')]")
            current_index = page_numbers.index(current_page)

            if current_index + 1 < len(page_numbers):
                page_numbers[current_index + 1].click()
                time.sleep(3)
                wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//table[@id='example']//tbody//tr")))
            else:
                break

        return list(pdf_urls)
