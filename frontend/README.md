# L2 Assignment – Research Tool Implementation

## Overview
This project implements a minimal internal research portal where AI is used as a **specific research tool**, not a chatbot.

The implemented tool extracts **income statement data** from uploaded financial documents and outputs a **structured, analyst-ready CSV file**.

---

## Implemented Research Tool
### Option A: Financial Statement Extraction to Excel/CSV

**Input**
- Annual report or financial statement (PDF, text-based)

**Output**
- CSV file containing normalized income-statement line items
- Supports multiple financial years
- Missing or ambiguous data is explicitly flagged

---

## System Flow
1. Researcher uploads a financial document
2. System ingests and extracts raw text from the PDF
3. Income-statement line items are detected and normalized
4. Numeric values are extracted deterministically (no hallucination)
5. Output is generated as an Excel-compatible CSV

---

## Key Design Decisions

- **Hybrid extraction approach**: rule-based parsing with normalization
- **No hallucinated numbers**: values are extracted only if present in the document
- **Line-item normalization**: handles variations such as “Sales” vs “Revenue”
- **Multi-year support**: all detected years are extracted
- **Analyst transparency**: missing values are left blank and flagged

---

## Technology Stack
- Backend: FastAPI (Python)
- PDF Parsing: pdfplumber
- Data Processing: pandas
- Frontend: Minimal HTML + JavaScript
- Hosting: Render (Free Tier)

---

## Limitations
- Supports text-based PDFs only (no OCR)
- File size limited by free hosting tier
- Cold-start latency on free deployment

---

## How to Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
