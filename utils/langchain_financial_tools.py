# utils/langchain_financial_tools.py

from langchain.tools import tool

@tool
def calculate_emergency_fund(input: str) -> str:
    """Calculate total emergency fund needed based on monthly expenses and duration."""
    try:
        parts = {k.strip(): float(v.strip()) for k, v in [pair.split('=') for pair in input.split(',')]}
        expenses = parts.get('monthly_expenses', 0)
        months = parts.get('months', 6)
        total = round(expenses * months, 2)
        return f"""```To build a {months}-month emergency fund with monthly expenses of ${expenses:.2f}, you should save a total of ${total:.2f}.```"""
    except Exception as e:
        return f"```❌ Error: Unable to calculate emergency fund. Details: {str(e)}```"

@tool
def savings_goal_monthly(input: str) -> str:
    """Calculate monthly savings needed to meet a financial goal in a given time."""
    try:
        parts = {k.strip(): float(v.strip()) for k, v in [pair.split('=') for pair in input.split(',')]}
        goal = parts.get('goal_amount', 0)
        months = parts.get('months', 1)
        if months <= 0:
            return "```❌ Error: Number of months must be greater than zero.```"
        monthly = round(goal / months, 2)
        return f"""```To reach a goal of ${goal:.2f} in {months} months, you should save ${monthly:.2f} per month.```"""
    except Exception as e:
        return f"```❌ Error: Unable to calculate savings goal. Details: {str(e)}```"

@tool
def debt_payoff_monthly(input: str) -> str:
    """Estimate monthly payment to pay off a loan based on interest rate and term."""
    try:
        parts = {k.strip(): float(v.strip()) for k, v in [pair.split('=') for pair in input.split(',')]}
        debt = parts.get('total_debt', 0)
        rate = parts.get('annual_interest_rate', 0) / 12 / 100
        months = parts.get('months', 1)
        if months <= 0:
            return "```❌ Error: Number of months must be greater than zero.```"
        if rate == 0:
            payment = round(debt / months, 2)
        else:
            payment = round(debt * rate * ((1 + rate) ** months) / (((1 + rate) ** months) - 1), 2)
        return f"""```To pay off a debt of ${debt:.2f} over {months} months at an annual interest rate of {parts.get('annual_interest_rate', 0):.2f}%, your monthly payment would be approximately ${payment:.2f}.```"""
    except Exception as e:
        return f"```❌ Error: Unable to calculate debt payoff. Details: {str(e)}```"

@tool
def estimate_retirement_savings(input: str) -> str:
    """Estimate total retirement savings based on age, contributions, and rate of return."""
    try:
        parts = {k.strip(): float(v.strip()) for k, v in [pair.split('=') for pair in input.split(',')]}
        age = parts.get('age', 0)
        retirement_age = parts.get('retirement_age', 65)
        savings = parts.get('current_savings', 0)
        contribution = parts.get('monthly_contribution', 0)
        rate = parts.get('annual_return_rate', 0) / 12 / 100
        months = max(0, (retirement_age - age) * 12)
        future_value = savings * ((1 + rate) ** months)
        if rate == 0:
            future_value += contribution * months
        else:
            future_value += contribution * (((1 + rate) ** months - 1) / rate)
        return f"""```If you contribute ${contribution:.2f} monthly starting at age {int(age)} with ${savings:.2f} saved now, and earn {parts.get('annual_return_rate', 0):.2f}% annually, you will have approximately ${future_value:.2f} by age {int(retirement_age)}.```"""
    except Exception as e:
        return f"```❌ Error: Unable to estimate retirement savings. Details: {str(e)}```"

@tool
def calculate_credit_utilization(input: str) -> str:
    """Calculate credit utilization percentage based on credit used and total limit."""
    try:
        parts = {k.strip(): float(v.strip()) for k, v in [pair.split('=') for pair in input.split(',')]}
        used = parts.get('credit_used', 0)
        limit = parts.get('credit_limit', 1)
        if limit <= 0:
            return "```❌ Error: Credit limit must be greater than zero.```"
        percent = round((used / limit) * 100, 2)
        return f"""```Your credit utilization is {percent:.2f}% (based on ${used:.2f} used out of ${limit:.2f} limit).```"""
    except Exception as e:
        return f"```❌ Error: Unable to calculate credit utilization. Details: {str(e)}```"

@tool
def monthly_budget_percentage(input: str) -> str:
    """Calculate the percentage of income spent on a specific budget category."""
    try:
        parts = {k.strip(): float(v.strip()) for k, v in [pair.split('=') for pair in input.split(',')]}
        amount = parts.get('category_amount', 0)
        income = parts.get('total_income', 1)
        if income <= 0:
            return "```❌ Error: Total income must be greater than zero.```"
        percent = round((amount / income) * 100, 2)
        return f"""```You're spending {percent:.2f}% of your income (${income:.2f}) on this category (${amount:.2f}).```"""
    except Exception as e:
        return f"```❌ Error: Unable to calculate budget percentage. Details: {str(e)}```"
