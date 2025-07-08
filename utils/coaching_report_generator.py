# utils/coaching_report_generator.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load .env immediately at import
load_dotenv()

def generate_coaching_report(parsed_data_summary):
    # Load API Key inside the function (not at import time)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set. Please check environment variables.")

    genai.configure(api_key=api_key)

    prompt = f"""
    You are a financial advisor.

    Based on the following user's financial information, create a short personalized financial coaching report.

    Be supportive, constructive, and mention:
    - Good things they are doing
    - Potential areas for improvement
    - Suggestions on saving, debt management, credit health, and budgeting.

    User Data:
    {parsed_data_summary}
    """

    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    response = model.generate_content(prompt)

    return response.text.strip()
