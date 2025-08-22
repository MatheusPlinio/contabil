import os
import requests


class PDFDownloader:
    def download(self, url: str, save_dir="downloads") -> str:
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.basename(url.split("?")[0])
        filepath = os.path.join(save_dir, filename)

        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"⬇️ PDF baixado: {filepath}")
        return filepath
