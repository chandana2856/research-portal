from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pdfplumber
import io
import pandas as pd
import uuid
from services.financial_extractor import extract_financials

app = FastAPI(title="Research Portal")

@app.get("/")
def root():
    return {"status": "Running"}

@app.post("/execute")
async def execute(file: UploadFile = File(...)):
    # read uploaded file into memory
    contents = await file.read()
    pdf_file = io.BytesIO(contents)

    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= 50:  # limit to first 50 pages
                break
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    df = extract_financials(text)

    output_path = f"output_{uuid.uuid4()}.csv"
    df.to_csv(output_path, index=False)

    return FileResponse(
        path=output_path,
        filename="income_statement.csv",
        media_type="text/csv"
    )
