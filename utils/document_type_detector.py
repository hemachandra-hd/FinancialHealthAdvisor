# utils/document_type_detector.py

def detect_document_type(text):
    """Detect the type of financial document based on keywords in the extracted text."""

    text_lower = text.lower()  # For easier matching

    if "form 16a" in text_lower or "income-tax act" in text_lower or "certificate under section 203" in text_lower:
        return "Tax Certificate"

    if "w2" in text_lower or "1099" in text_lower or "social security wages" in text_lower:
        return "Income Statement"

    if "pay date" in text_lower or "gross pay" in text_lower or "net pay" in text_lower or "earnings statement" in text_lower:
        return "Pay Stub"

    if "form 1040" in text_lower or "adjusted gross income" in text_lower or "filing status" in text_lower:
        return "Tax Return"

    if "account number" in text_lower or "withdrawals" in text_lower or "deposits" in text_lower or "ending balance" in text_lower:
        return "Bank Statement"

    if "mortgage" in text_lower or "loan number" in text_lower or "college debt" in text_lower:
        return "Debt Document"

    if "retirement account" in text_lower or "401(k)" in text_lower or "ira" in text_lower or "investments" in text_lower:
        return "Retirement or Investment Document"

    if "insurance policy" in text_lower or "life insurance" in text_lower:
        return "Insurance Document"

    if "monthly budget" in text_lower or "typical expenses" in text_lower:
        return "Monthly Budget"

    if "emergency savings" in text_lower or "nest egg" in text_lower:
        return "Emergency Plan"

    if "personal goals" in text_lower or "buying a home" in text_lower or "retirement goals" in text_lower:
        return "Personal Goals"

    if "tax return" in text_lower or "federal taxes paid" in text_lower or "state taxes paid" in text_lower:
        return "Federal or State Tax Return"

    return "Unknown"
