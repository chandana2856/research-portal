from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pdfplumber
import io
import pandas as pd
import uuid
from services.financial_extractor import extract_financials

app = FastAPI(title="Research Portal")

@app.post("/execute")
async def execute(file: UploadFile = File(...)):
    try:
        print("Received file:", file.filename)

        contents = await file.read()
        pdf_file = io.BytesIO(contents)

        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            print(f"PDF has {len(pdf.pages)} pages")
            for i, page in enumerate(pdf.pages):
                if i >= 50:  # limit pages to prevent hanging
                    break
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        print("Finished extracting text from PDF")

        df = extract_financials(text)
        print("Financials extracted, creating CSV")

        # Save CSV to BytesIO for streaming
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)

        print("Returning CSV file")
        return StreamingResponse(
            stream,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=income_statement.csv"}
        )

    except Exception as e:
        print("Error during execution:", e)
        raise HTTPException(status_code=500, detail=str(e))
