import streamlit as st

def setup_page():
    st.set_page_config(page_title="Invoice OCR with LLaMA 4", layout="wide")
    st.title("🧾 Smarter Invoice Parsing Powered by Llama 4 🦙")

def select_input_method():
    return st.radio("Select input method: 📸", 
                   ["Upload Image 📤", "Image URL 🌐"])

def show_extraction_button():
    return st.button("Extract Invoice Data")

def display_results(invoice_data):
    st.success("✅ Data extracted successfully!")
    st.json(invoice_data.dict())

def display_error(message):
    st.error(f"❌ {message}")
