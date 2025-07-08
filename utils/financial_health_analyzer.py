# utils/financial_health_analyzer.py
# utils/financial_health_analyzer.py

import numpy as np

def analyze_financial_health(parsed_data: dict) -> dict:
    """Analyze financial data and generate a health report and score."""

    insights = []
    score_components = []

    # --- Extract Best-Matching Values Across Namespaced Keys ---
    def find_value(field_name):
        for key, val in parsed_data.items():
            if key.lower().endswith(field_name.lower()) and val not in [None, ""]:
                try:
                    return float(str(val).replace("$", "").replace(",", "").strip())
                except:
                    continue
        return None

    income = find_value("Gross Pay")
    net_income = find_value("Net Pay")
    fit = find_value("Federal Income Tax")
    sit = find_value("State Income Tax")
    ss = find_value("Social Security")
    medicare = find_value("Medicare")

    expenses = None
    savings_balance = None
    savings_rate = None
    months_covered = None

    # Estimate total deductions
    deductions = 0
    for val in [fit, sit, ss, medicare]:
        if val is not None:
            deductions += abs(val)

    if net_income and deductions:
        expenses = deductions

    # ---------------------
    # Generate Insights
    # ---------------------

    # Income
    if income:
        insights.append(f"💵 **Estimated Monthly Gross Income:** ${income:,.2f}")
        score_components.append(20)
    else:
        insights.append("💵 **Income information missing**.")
        score_components.append(10)

    # Expenses & Savings Rate
    if expenses:
        if income:
            savings_rate = max(0, (income - expenses) / income)
            insights.append(f"💸 **Estimated Savings Rate:** {savings_rate*100:.1f}%")
            if savings_rate >= 0.20:
                score_components.append(20)
            elif savings_rate >= 0.10:
                score_components.append(15)
            else:
                score_components.append(5)
        else:
            insights.append("💸 **Expenses found, but can't compute savings rate without income**.")
            score_components.append(10)
    else:
        insights.append("💸 **Expenses information missing**.")
        score_components.append(10)

    # Emergency fund (if applicable — to be extended later)
    insights.append("🛡️ **Emergency fund status unclear.**")
    score_components.append(10)

    # Debt
    insights.append("💳 **Debt-to-Income Ratio:** _Not available_ (Upload debt documents to enable this).")
    score_components.append(10)

    # Final Score
    final_score = np.clip(sum(score_components), 0, 100)

    return {
        "Insights": insights,
        "Final Score": final_score,
        "Summary Data": {
            "Income": income,
            "Net Income": net_income,
            "Expenses": expenses,
            "Deductions": deductions,
            "Savings Rate": savings_rate,
            "Emergency Fund Coverage": months_covered
        }
    }

