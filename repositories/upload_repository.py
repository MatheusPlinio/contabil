from database.config import sessionmaker, engine
from models.upload import Upload


class UploadRepository:
    def save(self, filename: str, url: str) -> Upload:
        SessionLocal = sessionmaker(
            bind=engine, autoflush=False, autocommit=False)
        with SessionLocal() as session:
            upload = Upload(filename=filename, url=url)
            session.add(upload)
            session.commit()
            session.refresh(upload)
            return upload
