from utils.date_utils import get_prev_month
from utils.driver_utils import setup_driver
from services.downloaders.pdf_collector import PDFCollector
from services.downloaders.pdf_downloader import PDFDownloader
from services.uploaders.request_uploader import RequestUploader


def process_pdfs():
    prev_month, year, prev_month_name = get_prev_month()
    driver = setup_driver()

    collector = PDFCollector(driver)
    downloader = PDFDownloader()
    uploader = RequestUploader(download_dir="tmp")

    try:
        pdf_urls = collector.collect(year, prev_month_name)
        for url in pdf_urls:
            downloader.download(url, save_dir=uploader.download_dir)

        return uploader.upload_all_pdfs()
    finally:
        driver.quit()
