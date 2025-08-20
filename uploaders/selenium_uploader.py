import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumUploader:

    def __init__(self, download_dir="./pdfs", max_retries=5, retry_delay=5):
        self.download_dir = download_dir
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Inicializa driver
        self.driver = webdriver.Chrome(options=options)

    def upload_file(self, filepath: str) -> str:
        """
        Faz upload de um PDF específico.
        Retorna a URL ou texto retornado pelo site.
        """
        attempt = 0
        filename = os.path.basename(filepath)

        while attempt < self.max_retries:
            attempt += 1
            try:
                print(f"⬆️ Tentativa {attempt} de upload: {filename}")

                self.driver.get("https://0x0.st") 

                # Espera pelo input de upload
                upload_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "file"))
                )
                upload_input.send_keys(os.path.abspath(filepath))

                # Espera pelo resultado (geralmente um <pre>)
                result = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "pre"))
                )

                url = result.text.strip()
                if url.startswith("https://"):
                    os.remove(filepath)
                    print(f"✅ Upload concluído: {url}")
                    return url
                else:
                    print(f"⚠️ Tentativa {attempt} falhou, resposta: {url}")

            except Exception as e:
                print(f"⚠️ Tentativa {attempt} deu erro: {e}")

            time.sleep(self.retry_delay)

        raise Exception(
            f"❌ Falha no upload de {filename} após {self.max_retries} tentativas")

    def upload_all_pdfs(self):
        """
        Loop contínuo enviando todos os PDFs do diretório.
        Para quando não houver mais PDFs.
        """
        while True:
            pdfs = [f for f in os.listdir(
                self.download_dir) if f.endswith(".pdf")]
            if not pdfs:
                print("🚀 Nenhum PDF restante, finalizando upload_all_pdfs.")
                break

            for pdf in pdfs:
                path = os.path.join(self.download_dir, pdf)
                try:
                    self.upload_file(path)
                except Exception as e:
                    print(f"❌ Falha ao enviar {pdf}: {e}")

        self.driver.quit()
        print("🟢 Selenium driver finalizado.")
