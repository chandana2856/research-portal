import re
import pandas as pd

LINE_ITEM_MAP = {
    "revenue": ["revenue", "total revenue", "sales"],
    "operating expenses": ["operating expenses", "operating costs"],
    "net income": ["net income", "profit"]
}

def extract_financials(text: str):
    data = {
        "Revenue": {"2021": None, "2022": None, "2023": None},
        "Operating Expenses": {"2021": None, "2022": None, "2023": None},
        "Net Income": {"2021": None, "2022": None, "2023": None},
    }

    currency = "USD"

    for line in text.split("\n"):
        clean = line.lower()

        for item, aliases in LINE_ITEM_MAP.items():
            if any(a in clean for a in aliases):
                numbers = re.findall(r"\d{2,}", line)
                if len(numbers) >= 3:
                    data[item.title()]["2021"] = numbers[0]
                    data[item.title()]["2022"] = numbers[1]
                    data[item.title()]["2023"] = numbers[2]

    rows = []
    for item, years in data.items():
        confidence = "HIGH" if all(years.values()) else "MISSING"
        rows.append([
            item,
            years["2021"],
            years["2022"],
            years["2023"],
            currency,
            confidence
        ])

    df = pd.DataFrame(rows, columns=[
        "Line Item", "2021", "2022", "2023", "Currency", "Confidence"
    ])

    return df
