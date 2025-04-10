import json
import base64
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from typing import List, Optional
from pydantic import BaseModel, Field
from groq import Groq


# ---------------------------
# Data Models
# ---------------------------

class LineItem(BaseModel):
    description: Optional[str] = Field(
        None, description="A brief description of the product or service provided."
    )
    quantity: Optional[float] = Field(
        None, description="The number of units of the product or service."
    )
    unit_price: Optional[float] = Field(
        None, description="The price per unit of the product or service."
    )
    total_price: Optional[float] = Field(
        None, description="The total price for the line item, calculated as quantity × unit price."
    )


class InvoiceData(BaseModel):
    invoice_number: Optional[str] = Field(
        None, description="The unique identifier or reference number of the invoice."
    )
    invoice_date: Optional[str] = Field(
        None, description="The date when the invoice was issued."
    )
    due_date: Optional[str] = Field(
        None, description="The payment due date."
    )
    billing_address: Optional[str] = Field(
        None, description="The address of the customer who is being billed."
    )
    shipping_address: Optional[str] = Field(
        None, description="The address where the goods/services are to be delivered."
    )
    vendor_name: Optional[str] = Field(
        None, description="The name of the company or individual issuing the invoice."
    )
    customer_name: Optional[str] = Field(
        None, description="The name of the person or organization being billed."
    )
    line_items: Optional[List[LineItem]] = Field(
        None, description="A list of items described in the invoice."
    )
    subtotal: Optional[float] = Field(
        None, description="The sum of all line item totals before taxes or additional fees."
    )
    tax: Optional[float] = Field(
        None, description="The tax amount applied to the subtotal."
    )
    total_amount: Optional[float] = Field(
        None, description="The final total to be paid including subtotal and taxes."
    )
    currency: Optional[str] = Field(
        None, description="The currency in which the invoice is issued (e.g., USD, EUR)."
    )


# -----------------------------------
# LLaMA Client Wrapper using Groq Api
# -----------------------------------

class GroqClient:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
    
    def extract_invoice_data(self, prompt, image_content, model="meta-llama/llama-4-scout-17b-16e-instruct"):
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                image_content
            ]
        }]
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.4,
            max_completion_tokens=1024,
            stream=False,
            response_format={"type": "json_object"},
        )
        
        return json.loads(response.choices[0].message.content)


# ---------------------------
# Image Handling Utilities
# ---------------------------

def process_image_upload(uploaded_file):
    if not uploaded_file:
        return None, None
    image_bytes = uploaded_file.read()
    suffix = uploaded_file.name.split(".")[-1].lower()
    mime_type = "image/jpeg" if suffix in ("jpg", "jpeg") else "image/png"
    return image_bytes, mime_type

def process_image_url(image_url):
    if not image_url:
        return None
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        raise ValueError(f"Error loading image from URL: {str(e)}")

def display_image_preview(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        st.image(image)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")


# ---------------------------
# Streamlit UI Functions
# ---------------------------

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
