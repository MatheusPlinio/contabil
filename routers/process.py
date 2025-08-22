from fastapi import APIRouter
from services.process_pdfs import process_pdfs

router = APIRouter()


@router.get("/process-pdf")
def process_pdf_route():
    files = process_pdfs()
    return {"status": "success", "total": len(files), "files": files}
