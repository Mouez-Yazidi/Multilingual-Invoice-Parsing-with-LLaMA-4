import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional
import base64
from groq import Groq
import json
from PIL import Image
import tempfile
import logging
# -----------------------------
# Define the Pydantic models
# -----------------------------
class LineItem(BaseModel):
    description: Optional[str] = Field(None)
    quantity: Optional[float] = Field(None)
    unit_price: Optional[float] = Field(None)
    total_price: Optional[float] = Field(None)

class InvoiceData(BaseModel):
    invoice_number: Optional[str] = Field(None)
    invoice_date: Optional[str] = Field(None)
    due_date: Optional[str] = Field(None)
    billing_address: Optional[str] = Field(None)
    shipping_address: Optional[str] = Field(None)
    vendor_name: Optional[str] = Field(None)
    customer_name: Optional[str] = Field(None)
    line_items: Optional[List[LineItem]] = Field(None)
    subtotal: Optional[float] = Field(None)
    tax: Optional[float] = Field(None)
    total_amount: Optional[float] = Field(None)
    currency: Optional[str] = Field(None)

# -----------------------------
# Function to encode image
# -----------------------------
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Invoice OCR with LLaMA 4", layout="wide")
st.title("🧾 OCR Invoice Parser using LLaMA 4 (Groq)")

uploaded_file = st.file_uploader("Upload an invoice image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Layout with columns
    col1, col2 = st.columns([1, 2])

    # Left column: Show image
    with col1:
        st.subheader("Invoice Image")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice")

    # Right column: Process and show extracted fields
    with col2:
        st.subheader("Extracted Invoice Fields")
        if st.button("Extract Invoice Data"):
            with st.spinner("Extracting data using LLaMA 4..."):
                suffix = uploaded_file.name.split(".")[-1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as temp_file:
                    temp_file.write(uploaded_file.read())
                    file_path = temp_file.name
                logging.info(f'**************{file_path}')
                base64_image = encode_image(file_path)
                
                # Ensure the API key is loaded securely from Streamlit secrets
                groq_api_key = st.secrets["GROQ_API_KEY"]
                client = Groq(api_key=groq_api_key)

                prompt = f"""
                You are an intelligent OCR extraction agent capable of understanding and processing documents in multiple languages.
                Given an image of an invoice, extract all relevant information in structured JSON format.
                The JSON object must use the schema: {json.dumps(InvoiceData.model_json_schema(), indent=2)}
                If any field cannot be found in the invoice, return it as null. Focus on clarity and accuracy, and ignore irrelevant text such as watermarks, headers, or decorative elements. Return the final result strictly in JSON format.
                """

                try:
                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ],
                        temperature=0.4,
                        max_completion_tokens=1024,
                        stream=False,
                        response_format={"type": "json_object"},
                    )

                    data = json.loads(response.choices[0].message.content)
                    invoice = InvoiceData(**data)

                    st.success("✅ Data extracted successfully!")
                    st.json(invoice.dict())

                except Exception as e:
                    st.error(f"❌ Failed to parse invoice: {str(e)}")
