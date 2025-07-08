import os
import fitz  # PyMuPDF
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load environment variables
load_dotenv()

def extract_fields_with_gemini(pdf_path):
    # Step 1: Extract raw text from PDF
    doc = fitz.open(pdf_path)
    raw_text = "\n".join([page.get_text() for page in doc])

    # Step 2: Setup Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set. Please check environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # Step 3: Gemini Prompt
    prompt = f"""
You are a financial assistant helping extract structured data from U.S. tax return documents.

The raw text provided comes from one or more tax forms such as:
- IRS Form 1040, W-2, 1099, 8879, 8889, 8867
- State tax forms such as Georgia Form 500

The document may include multiple forms and pages. Your task is to extract the information **exactly as labeled**, and return it as a valid JSON object. Use `null` where data is not found.

Important instructions:
- The **Taxpayer Name** is the **first name listed** on the return.
- The **Spouse Name** (if applicable) will usually appear **second** or under the filing status section.
- The **Refund** value must only be taken from a line explicitly labeled “Refund”.
- The **Amount You Owe** must only be taken from a line labeled “Amount You Owe”.
- The **Bank Routing Number** and **Bank Account Number** should only be included if a refund is present.
- The **Last 4 of SSN** should be extracted from the line labeled “SSN” or “Taxpayer Identification Number”.
- The **Filing Status** should be extracted from the line labeled “Filing Status”.
- The **Wages, Salaries, Tips** should be extracted from the line labeled “Wages, Salaries, Tips”.
- The **Taxable Interest** should be extracted from the line labeled “Taxable Interest”.
- The **Ordinary Dividends** should be extracted from the line labeled “Ordinary Dividends”.
- The **Total Income** should be extracted from the line labeled “Total Income”.
- The **Adjusted Gross Income** should be extracted from the line labeled “Adjusted Gross Income”.
- The **Standard Deduction** should be extracted from the line labeled “Standard Deduction”.
- Adjusted gross income, Total tax, Federal income tax withheld, Refund and Amount you owe information are available in the form 8899 under Part I section.
- There are two types of refund: one is the refund from the IRS and the other is the refund from the state. The refund from the IRS is usually labeled as "Refund" and the refund from the state is usually labeled as "State Refund".
- Total refund is the sum of the refund from the IRS and the refund from the state.
- Only one of "Refund" or "Amount You Owe" will usually have a value — do not infer or guess the other.
- Use numeric formatting for money (e.g., 1234.56).
- Use negative values (e.g., -250.00) for any field that represents a tax owed.
- Mask sensitive values (e.g., SSNs, bank numbers) where needed.
- Respond **only** with valid JSON (no markdown, headers, or commentary).

Required fields:
- Taxpayer Name
- Spouse Name (if applicable)
- Last 4 of Taxpayer SSN
- Last 4 of Spouse SSN (if applicable)
- Filing Status
- Wages, Salaries, Tips
- Taxable Interest
- Ordinary Dividends
- Total Income
- Adjusted Gross Income
- Standard Deduction
- Taxable Income
- Total Tax
- Federal Income Tax Withheld
- Estimated Tax Payments
- Amount You Owe
- Refund
- Bank Routing Number (if refund exists)
- Bank Account Number (partially masked if refund exists)

Raw Tax Return Text:
\"\"\"
{raw_text}
\"\"\"
"""

    response = model.generate_content(prompt)

    # Step 4: Clean & Parse
    cleaned = response.text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(json)?|```$", "", cleaned, flags=re.IGNORECASE).strip()

    cleaned = cleaned.replace("−", "-")  # Unicode minus
    cleaned = re.sub(r"\$?(\d{1,3})\s(\d{3})\s(\d{2})", r"\1\2.\3", cleaned)
    cleaned = re.sub(r"\$?(\d{1,3})\s(\d{2})", r"\1.\2", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("❌ JSON parsing failed. Raw cleaned response below:\n")
        print(cleaned)
        return None
