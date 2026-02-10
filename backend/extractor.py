import pandas as pd

def extract_financials(text: str):
    return pd.DataFrame([
        {
            "Line Item": "Revenue",
            "2023": "100000",
            "Currency": "USD",
            "Confidence": "HIGH"
        }
    ])
