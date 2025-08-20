from utils.date_utils import get_prev_month
from downloaders.pdf_collector import PDFCollector
from downloaders.pdf_downloader import PDFDownloader
from uploaders.request_uploader import RequestUploader  # <- novo uploader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.binary_location = "/usr/bin/chromium"  # ajuste se necessário
    return webdriver.Chrome(options=chrome_options)


def main():
    prev_month, year, prev_month_name = get_prev_month()
    driver = setup_driver()

    collector = PDFCollector(driver)
    downloader = PDFDownloader()
    uploader = RequestUploader(
        download_dir="downloads")  # <- usando requests

    try:
        # Coleta URLs dos PDFs
        pdf_urls = collector.collect(year, prev_month_name)
        print(f"🔍 Total de PDFs coletados: {len(pdf_urls)}")

        # Baixa os PDFs para o diretório do uploader
        for url in pdf_urls:
            downloader.download(url, save_dir=uploader.download_dir)

        # Faz upload de todos PDFs presentes na pasta via requests
        uploaded_files = uploader.upload_all_pdfs()

        # Mostra resumo
        print("\n📋 RESUMO DOS UPLOADS:")
        for info in uploaded_files:
            print(f"📄 {info['original']} → {info['url']}")

        print("✅ Todos os PDFs processados com sucesso.")

    finally:
        driver.quit()
        print("🟢 Selenium driver finalizado.")


if __name__ == "__main__":
    main()
