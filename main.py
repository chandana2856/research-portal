from fastapi import FastAPI, UploadFile, File
import pdfplumber
import io
from extractor import extract_financials

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    df = extract_financials(text)

    output = io.StringIO()
    df.to_csv(output, index=False)

    return {
        "filename": "financial_output.csv",
        "data": output.getvalue()
    }
