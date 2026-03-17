# FinancialHealthAdvisor
AI Powered FinancialHealthAdvisor
Capstone Project Title: AI-Powered Financial Health Advisor This is the customized project similar to Resume coach, but in Financial domain.

The AI-Powered Financial Health Advisor reimagines personal finance management by analyzing financial documents and offering intelligent, personalized guidance using Generative AI. This project empowers individuals to gain deeper insights into their financial health by automatically extracting key data from pay stubs, tax returns, bank statements, and other financial records. Leveraging the power of Large Language Models, the advisor serves as a virtual financial coach—offering tailored recommendations, savings tips, budgeting advice, and credit insights. Through an interactive web application, the system simplifies complex financial decisions, supports long-term planning, and brings accessible financial literacy to everyday users.

Project Overview
This capstone project demonstrates the use of Generative AI to build an interactive, web-based financial health assistant. Users upload documents like pay stubs, bank statements, and tax returns to receive personalized coaching reports and interact with an AI-powered chatbot.

Please see Project Documentation for more details - Project Design

Motivation
Managing personal finances is often complex, especially when important information is scattered across various formats. This application aims to democratize financial insights using LLMs like Gemini, making personal financial coaching more accessible and intelligent.

Architecture Overview
The application consists of the following components:

Streamlit UI hosted on AWS EC2
Document Parsers (paystub, bank, tax) using Gemini API
LangChain Integration for prompt orchestration and chatbot
Gemini 1.5 Pro for coaching and field extraction
Please see Project Documentation for more details - Project Architecture Overview

Technology Stack
Component	Tool
Web UI	Streamlit
LLM	Gemini 1.5 Pro via Google GenAI API
Orchestration	LangChain
Hosting	AWS EC2
Parsing	PyMuPDF, Gemini
Language	Python 3.10+
📁 Folder Structure
HemachandraHD_FinancialHealthAdvisor/
├── streamlit_app.py
├── parsers/
├── utils/
├── sample_outputs/
├── screenshots/
├── requirements.txt
├── user_manual.md
└── HemachandraHD_FinancialHealthAdvisor.ipynb
Prompt Engineering
Prompts were custom-designed for document-specific extraction and financial coaching. LangChain was used to handle:

Multi-step prompts
Output parsing
Chatbot memory and tool use
Example Prompt
You are a financial assistant. Extract the following fields from this pay stub: Gross Pay, Net Pay, FIT, SIT, SS, Med. Return the output in JSON format.
Chatbot Module
LangChain's ConversationalRetrievalChain + tool-calling was used to create an AI financial assistant that can:

Answer follow-up questions
Access extracted financial fields
Recommend financial actions interactively
Sample Output
Example coaching advice includes:

Emergency fund recommendations
Credit utilization warnings
Savings rate insights
These are generated contextually based on uploaded financial data.

Please see Project Documentation for more details - User Manual

How to Run This Project
Run the Streamlit app using the command:

streamlit run streamlit_app.py
Make sure to set your GOOGLE_API_KEY in the .env file.

Please see Project Documentation for more details - Project Design

Deployment Notes
Hosted on AWS EC2 Ubuntu (Free Tier)
Opened port 8501 for Streamlit access
Streamlit auto-launches on VM startup for demo
Screenshots
Added in the project folder

Homepage
Coaching Report
Chatbot
EC2 Terminal
Demo Video
Include a link in the project folder.

✅ Submission Summary
This project meets the following objectives of real-time LLM-assisted financial document processing, personalized coaching, and chatbot-driven guidance. It integrates Gemini, LangChain, and Streamlit on AWS EC2.

Design and implement an AI-powered system that extracts, interprets, and analyzes financial information from user-submitted documents such as pay stubs, bank statements, and tax returns.

Generate a personalized financial coaching report, including insights on income, savings patterns, spending habits, tax liabilities, and suggested next steps.

Develop a Streamlit-based web application that allows users to upload financial documents in PDF, CSV, or plain text formats, view parsed data, and interact with visualizations and summaries.

Integrate a Generative AI chatbot assistant using Gemini API and LangChain to provide conversational financial advice, respond to user queries, and recommend actionable tips.

Ensure modular, scalable architecture using structured parsing, AI output formatting, and LangChain-enhanced prompting to support future extensions (e.g., retirement planning, credit score analysis).

Demonstrate the use of real-world financial documents (anonymized) and show how the system helps users gain clarity on their current financial health and improve their decision-making.
