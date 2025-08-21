from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PDFCollector:
    def __init__(self, driver):
        self.driver = driver

    def collect(self, year: int, month_name: str) -> list[str]:
        self.driver.get("https://www.natal.rn.gov.br/dom")

        # Seleciona ano e mês
        Select(self.driver.find_element(By.NAME, "ano")
               ).select_by_visible_text(str(year))
        Select(self.driver.find_element(By.NAME, "mes")
               ).select_by_visible_text(month_name)

        # Clica no botão para filtrar
        self.driver.find_element(
            By.CSS_SELECTOR, "button[data-attach-loading]").click()

        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@id='example']//tbody//tr")))

        pdf_urls = set()

        while True:
            # Captura os links dos PDFs na página atual
            rows = self.driver.find_elements(
                By.XPATH, "//table[@id='example']//tbody//tr")
            for row in rows:
                links = row.find_elements(By.TAG_NAME, "a")
                for link_elem in links:
                    href = link_elem.get_attribute("href")
                    if href and href.lower().endswith(".pdf"):
                        pdf_urls.add(href)

            # Paginação por números
            page_items = self.driver.find_elements(
                By.XPATH, "//div[@id='example_paginate']//li")
            active_item = self.driver.find_element(
                By.XPATH, "//div[@id='example_paginate']//li[contains(@class,'active')]")
            active_index = page_items.index(active_item)

            # Se houver próxima página
            if active_index + 1 < len(page_items):
                next_page_link = page_items[active_index +
                                            1].find_element(By.TAG_NAME, "a")
                next_page_link.click()
                time.sleep(2)
                wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//table[@id='example']//tbody//tr")))
            else:
                break

        return list(pdf_urls)
