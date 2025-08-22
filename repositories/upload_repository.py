from database.config import sessionmaker, engine
from models.upload import Upload
from datetime import datetime
import re


class UploadRepository:
    def save(self, filename: str, url: str) -> Upload:
        SessionLocal = sessionmaker(
            bind=engine, autoflush=False, autocommit=False)
        match = re.search(r"dom_(\d{8})_", filename)
        date = None
        if match:
            try:
                date = datetime.strptime(match.group(1), "%Y%m%d")
            except ValueError:
                pass
        with SessionLocal() as session:
            upload = Upload(filename=filename, url=url, date=date)
            session.add(upload)
            session.commit()
            session.refresh(upload)
            return upload
