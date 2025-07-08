import streamlit as st
import os
import pandas as pd
import json
from collections import defaultdict

from utils.file_handler import handle_file
from parsers.pdf_parser import extract_text_from_pdf
from parsers.text_parser import extract_fields_from_text
from parsers.gemini_generic_parser import extract_generic_financial_info
from parsers.gemini_paystub_parser import extract_fields_with_gemini as extract_paystub_fields
from parsers.gemini_tax_return_parser import extract_fields_with_gemini as extract_tax_fields
from parsers.gemini_bank_parser import extract_fields_with_gemini as extract_bank_fields
from utils.document_type_detector import detect_document_type
from utils.coaching_report_generator import generate_coaching_report
from utils.chatbot_handler import chat_with_gemini
from utils.financial_health_analyzer import analyze_financial_health

# --- Helper to flatten nested profiles ---
def flatten_full_profile(full_profile_dict):
    flat_profile = {}
    for doc_type, docs in full_profile_dict.items():
        for idx, doc in enumerate(docs):
            for key, value in doc.items():
                flat_key = f"{doc_type}_{idx+1}_{key}"
                flat_profile[flat_key] = value
    return flat_profile

# --- Set up page ---
st.set_page_config(page_title="AI Financial Advisor", page_icon="💸", layout="wide")

st.title("💸 AI Financial Advisor")
st.caption("Analyze your financial documents and get personalized advice!")

st.sidebar.header("📂 Upload Your Financial Documents")
uploaded_files = st.sidebar.file_uploader(
    "Choose one or more documents",
    type=["csv", "pdf", "txt"],
    accept_multiple_files=True,
    help="Supported formats: PDF, CSV, TXT"
)

st.sidebar.markdown("---")
st.sidebar.info("After uploading, you can generate a financial report, chat with AI, and analyze your financial health.")

# --- Initialize ---
file_summaries = []
full_profile = defaultdict(list)
all_extracted_fields = {}

# --- File Processing ---
if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = handle_file(uploaded_file)

        if uploaded_file.type in ["text/plain", "text/csv"]:
            content = uploaded_file.read().decode("utf-8")
            extracted_text = content
        elif uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(save_path)
        else:
            st.warning(f"⚠️ Unsupported file type: {uploaded_file.name}")
            continue

        doc_type = detect_document_type(extracted_text)

        file_summaries.append({
            "File Name": uploaded_file.name,
            "Document Type": doc_type
        })

        fields = {}
        if doc_type == "Pay Stub":
            fields = extract_paystub_fields(save_path)
        elif doc_type == "Tax Return" or doc_type == "Income Statement":
            fields = extract_tax_fields(save_path)
        elif doc_type == "Bank Statement":
            fields = extract_bank_fields(save_path)
        else:
            doc_type = "General Document"
            fields = extract_generic_financial_info(save_path)

        if isinstance(fields, dict):
            full_profile[doc_type].append(fields)
            all_extracted_fields[uploaded_file.name] = {"type": doc_type, "fields": fields}
        else:
            st.warning(f"⚠️ Could not extract fields for {uploaded_file.name}")

# --- Display Tabs ---
if uploaded_files:
    tab1, tab2, tab3, tab4 = st.tabs(["📂 Uploaded Summary", "📄 Coaching Report", "💬 Financial Chatbot", "📊 Financial Health"])

    with tab1:
        st.subheader("🗂️ Uploaded File Summary")
        st.dataframe(pd.DataFrame(file_summaries))

        for file_name, content in all_extracted_fields.items():
            doc_type = content["type"]
            fields = content["fields"]

            with st.expander(f"📄 Extracted Fields: {file_name}", expanded=False):
                st.markdown(f"**🗂 Document Type:** {doc_type}")

                if doc_type == "Pay Stub":
                    keys = ["Employee Name", "Company", "Employee ID", "Department", "Period Beginning", "Period Ending", "Pay Date", "Gross Pay", "Net Pay", "Federal Income Tax", "State Income Tax", "Social Security", "Medicare", "Rate", "Hours Worked"]
                    for key in keys:
                        st.write(f"**{key}:** {fields.get(key, 'Not found')}")

                elif doc_type == "Bank Statement":
                    keys = ["Bank Name", "Account Holder Name", "Account Number", "Account Type", "Statement Period Start Date", "Statement Period End Date", "Opening Balance", "Closing Balance"]
                    for key in keys:
                        st.write(f"**{key}:** {fields.get(key, 'Not found')}")
                    if "Transactions" in fields and isinstance(fields["Transactions"], list):
                        st.write("**Transactions:**")
                        df = pd.DataFrame(fields["Transactions"])
                        st.dataframe(df)

                elif doc_type == "Tax Return" or doc_type == "Income Statement":
                    keys = ["Taxpayer Name", "Spouse Name", "Last 4 of Taxpayer SSN", "Last 4 of Spouse SSN", "Filing Status", "Wages, Salaries, Tips", "Taxable Interest", "Ordinary Dividends", "Total Income", "Adjusted Gross Income", "Standard Deduction", "Taxable Income", "Total Tax", "Federal Income Tax Withheld", "Estimated Tax Payments", "Amount You Owe", "Refund", "Bank Routing Number", "Bank Account Number"]
                    for key in keys:
                        st.write(f"**{key}:** {fields.get(key, 'Not found')}")

                else:
                    for key, value in fields.items():
                        st.write(f"**{key}:** {value if value else 'Not found'}")

    with tab2:
        st.subheader("📄 Generate Financial Coaching Report")
        if st.button("📄 Generate Coaching Report"):
            if full_profile:
                flat_profile = flatten_full_profile(full_profile)
                coaching_report = generate_coaching_report(flat_profile)
                st.text_area("📝 Financial Coaching Report", coaching_report, height=400)

                st.download_button(
                    label="⬇️ Download Coaching Report (TXT)",
                    data=coaching_report.encode('utf-8'),
                    file_name="financial_coaching_report.txt",
                    mime="text/plain"
                )
            else:
                st.warning("⚠️ No sufficient data to generate a coaching report.")

    with tab3:
        st.subheader("💬 Financial Chatbot")

        # Optional UI style
        st.markdown("""
            <style>
            .stChatMessage.user {
                background-color: #e1f5fe;
                border-radius: 10px;
                padding: 8px;
                margin-bottom: 10px;
            }
            .stChatMessage.bot {
                background-color: #f1f8e9;
                border-radius: 10px;
                padding: 8px;
                margin-bottom: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        user_question = st.chat_input("Ask your financial question...")

        if user_question and full_profile:
            flat_profile = flatten_full_profile(full_profile)
            bot_response = chat_with_gemini(user_question, flat_profile)
            st.session_state.chat_history.append(("user", user_question))
            st.session_state.chat_history.append(("bot", bot_response))

        for role, message in st.session_state.chat_history:
            with st.chat_message(role):
                if role == "user":
                    st.markdown(f"**{message}**", unsafe_allow_html=True)
                else:
                    st.markdown(message, unsafe_allow_html=True)


    with tab4:
        st.subheader("📊 Analyze Financial Health")

        if st.button("📊 Analyze My Financial Health"):
            if full_profile:
                flat_profile = flatten_full_profile(full_profile)
                #st.markdown("### 🧪 Debug: Flattened Profile Keys")
                #st.json(flat_profile)  # 👈 SHOW what's actually being passed
                health_report = analyze_financial_health(flat_profile)

                st.success(f"✅ Your Financial Health Score: **{health_report['Final Score']} / 100**")
                for insight in health_report["Insights"]:
                    st.write(insight)

                st.download_button(
                    label="⬇️ Download Financial Health Report (TXT)",
                    data="\n".join(health_report["Insights"]).encode('utf-8'),
                    file_name="financial_health_report.txt",
                    mime="text/plain"
                )
            else:
                st.warning("⚠️ No sufficient data to analyze financial health.")
