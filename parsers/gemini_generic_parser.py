
import os
import fitz  # PyMuPDF
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load environment variables
load_dotenv()

def extract_generic_financial_info(file_path):
    # ✅ Determine file type from extension
    _, ext = os.path.splitext(file_path)
    #print(f"📄 File extension detected: {ext}")  # Debug print

    # ✅ Extract text depending on file type
    if ext.lower() == ".pdf":
        try:
            doc = fitz.open(file_path)
            text = "\n".join([page.get_text() for page in doc])
        except Exception as e:
            raise RuntimeError(f"PDF parsing failed: {e}")
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            raise RuntimeError(f"Text file reading failed: {e}")

    # ✅ Gemini setup
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set. Please check environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # ✅ Gemini Prompt
    prompt = f"""
You are a financial assistant.

The following is raw text from a general financial document, which may include narrative statements, summaries, letters, or advisory notes.

Your task is to extract any meaningful **financial information** as a structured JSON object.

Extract (if present):
- Income sources and amounts
- Expenses or spending categories
- Loans, debts, or liabilities
- Savings or investment mentions
- Tax-related notes
- Goals, budgets, retirement plans
- Any other named financial fields

Return only a valid JSON response. Do not include markdown, headers, or comments. Use null where data is missing.

Raw Document Text:
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
