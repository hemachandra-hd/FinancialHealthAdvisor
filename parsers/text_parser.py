import re

# parsers/text_parser.py

# parsers/text_parser.py

def extract_fields_from_text(text):
    """Safely extract key financial fields from plain text."""
    fields = {
        "Employee Name": None,
        "Employer": None,
        "Pay Date": None,
        "Gross Pay": None,
        "Federal Tax": None,
        "State Tax": None,
        "Other Deductions": None,
        "Net Pay": None
    }

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if ":" in line:  # Check if colon exists before splitting
            key_part, value_part = line.split(":", 1)  # Split only once safely
            key = key_part.strip()
            value = value_part.strip()

            if "Employee Name" in key:
                fields["Employee Name"] = value
            elif "Employer" in key:
                fields["Employer"] = value
            elif "Pay Date" in key:
                fields["Pay Date"] = value
            elif "Gross Pay" in key:
                fields["Gross Pay"] = value
            elif "Federal Tax" in key:
                fields["Federal Tax"] = value
            elif "State Tax" in key:
                fields["State Tax"] = value
            elif "Other Deductions" in key:
                fields["Other Deductions"] = value
            elif "Net Pay" in key:
                fields["Net Pay"] = value

    return fields
