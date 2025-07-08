# parsers/bank_statement_parser.py

# parsers/bank_statement_parser.py

import pandas as pd
import re
from utils.gemini_extractor import extract_fields_with_gemini

def regex_parse_bank_statement(text):
    """Try simple regex-based line parsing for basic CSV-like bank statements."""
    lines = text.split('\n')
    transactions = []

    # Try to detect header
    header_detected = False
    for line in lines:
        if re.search(r'Date.*Description.*Amount.*Balance', line, re.IGNORECASE):
            header_detected = True
            continue
        if header_detected:
            # Assume following lines are transactions
            parts = [part.strip() for part in line.split(',')]
            if len(parts) >= 4:
                transactions.append({
                    "Date": parts[0],
                    "Description": parts[1],
                    "Amount": parts[2],
                    "Balance": parts[3]
                })

    return pd.DataFrame(transactions)

def smart_parse_bank_statement(text):
    """Smart parser: Try regex first, fallback to Gemini if too messy."""
    df = regex_parse_bank_statement(text)
    
    # If very few transactions found, fallback to Gemini
    if df.empty or len(df) < 3:
        # Future enhancement: Send text to Gemini to extract structured transaction table
        return None

    return df
