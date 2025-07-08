import os
import fitz  # PyMuPDF
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load .env
load_dotenv()

def extract_fields_with_gemini(pdf_path):
    # ✅ Extract raw text from PDF
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])

    # ✅ Gemini setup
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set. Please check environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    prompt = f"""
You are a financial assistant. The following is raw text extracted from a personal or business bank statement.

Please extract the following information and return it as a valid JSON object (no markdown or explanation).

Required Fields:
- Bank Name
- Account Holder Name
- Account Number (masked if needed, e.g., ****1234)
- Account Type (Checking, Savings, Business, etc.)
- Statement Period Start Date
- Statement Period End Date
- Opening Balance
- Closing Balance

Transactions (list of):
- Date
- Description
- Amount
- Type ("debit" or "credit")

Instructions:
- Format amounts with decimals (e.g., 1250.50)
- Use ISO format for dates (YYYY-MM-DD)
- For transaction type, infer based on labels like “Withdrawal”, “Deposit”, “Credit”, “Debit”, etc.
- Return `null` for any missing field
- Respond only with a valid JSON object

Raw Bank Statement Text:
\"\"\"
{text}
\"\"\"
"""

    response = model.generate_content(prompt)

    # ✅ Clean Gemini response
    cleaned = response.text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(json)?|```$", "", cleaned, flags=re.IGNORECASE).strip()

    cleaned = cleaned.replace("−", "-")
    cleaned = re.sub(r"\$?(\d{1,3})\s(\d{3})\s(\d{2})", r"\1\2.\3", cleaned)
    cleaned = re.sub(r"\$?(\d{1,3})\s(\d{2})", r"\1.\2", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("❌ JSON parsing failed. Raw cleaned response:\n")
        print(cleaned)
        return None
