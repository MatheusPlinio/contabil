import os
import requests
from utils.file_utils import remove_file
from repositories.upload_repository import UploadRepository


class RequestUploader:
    def __init__(self, download_dir="./pdfs"):
        self.download_dir = download_dir
        self.uploader = UploadRepository()

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": "curl/8.5.0",
            "Accept": "*/*"
        })
        return session

    def upload_file(self, filepath: str) -> str | None:
        filename = os.path.basename(filepath)

        try:
            print(f"⬆️ Enviando: {filename}")
            session = self._create_session()

            with open(filepath, "rb") as f:
                response = session.post(
                    "https://0x0.st",
                    files={"file": (filename, f, "application/pdf")},
                    timeout=90,
                    allow_redirects=True
                )

            print(f"📊 Status: {response.status_code}")

            if response.status_code == 200:
                url = response.text.strip()
                print(f"📋 Resposta: '{url}'")

                if url and not url.endswith('/aaa') and 'error' not in url.lower():
                    if url.startswith('http') or '0x0.st' in url:
                        self.uploader.save(filename, url)
                        remove_file(filepath)
                        print(f"✅ Upload concluído: {url}")
                        return url
                print(f"⚠️ Resposta inválida: '{url}'")

            elif response.status_code == 403:
                print("🚫 Erro 403 (Forbidden) - bloqueio no servidor")
            elif response.status_code == 413:
                print("📦 Erro 413 (Arquivo muito grande)")
            elif response.status_code == 429:
                print("🐌 Erro 429 (Rate limit) - muitas requisições")
            else:
                print(
                    f"❌ Erro inesperado {response.status_code}: {response.text[:200]}")

        except requests.exceptions.Timeout:
            print("⏰ Timeout na requisição")
        except requests.exceptions.ConnectionError:
            print("🌐 Erro de conexão")
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")

        return None

    def upload_all_pdfs(self) -> list[dict]:
        uploaded = []

        while True:
            pdfs = [f for f in os.listdir(
                self.download_dir) if f.endswith(".pdf")]
            if not pdfs:
                print("🚀 Nenhum PDF restante, finalizando upload_all_pdfs.")
                break

            print(f"📁 Encontrados {len(pdfs)} PDFs para processar")

            for i, pdf in enumerate(pdfs, 1):
                path = os.path.join(self.download_dir, pdf)
                print(f"\n📤 Processando arquivo {i}/{len(pdfs)}: {pdf}")

                if not os.path.exists(path):
                    print(f"⚠️ Arquivo {pdf} não existe mais, pulando...")
                    continue

                url = self.upload_file(path)
                if url:
                    uploaded.append({'original': pdf, 'url': url})
                else:
                    remove_file(path)

        print(
            f"🟢 Uploads concluídos: {len(uploaded)} PDFs enviados com sucesso.")
        return uploaded
