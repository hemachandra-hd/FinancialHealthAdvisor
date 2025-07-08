# utils/chatbot_handler.py
# utils/chatbot_handler.py

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory

from utils.langchain_financial_tools import (
    calculate_emergency_fund,
    savings_goal_monthly,
    debt_payoff_monthly,
    estimate_retirement_savings,
    calculate_credit_utilization,
    monthly_budget_percentage,
)

# ✅ Load .env variables
load_dotenv()

# 🧠 Gemini-powered LangChain agent for financial coaching
def chat_with_gemini(user_question, parsed_data_summary):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not set in environment variables")

        # Gemini chat model via LangChain
        llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0, google_api_key=api_key)

        tools = [
            calculate_emergency_fund,
            savings_goal_monthly,
            debt_payoff_monthly,
            estimate_retirement_savings,
            calculate_credit_utilization,
            monthly_budget_percentage,
        ]
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            handle_parsing_errors=True,
        )

        # Profile context injection
        context = "Here is the user's financial profile:\n"
        for key, value in parsed_data_summary.items():
            context += f"- {key}: {value}\n"

        full_prompt = f"""
        {context}
        You have access to previous messages via chat history. Use the chat history to understand the user’s current and previous queries and respond in context.
        Now respond to the user's question:

        {user_question}

        Please format all numbers with commas, clearly label amounts (e.g., $300 per month), and avoid collapsing phrases. Use proper punctuation and spacing.
        """

        response = agent.run(full_prompt)
        return response

    except Exception as e:
        return f"⚠️ Sorry, I encountered an error while processing: {str(e)}"
