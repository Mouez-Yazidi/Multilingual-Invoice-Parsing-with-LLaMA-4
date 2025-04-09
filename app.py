import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional
import base64
from groq import Groq
import json
from PIL import Image
from io import BytesIO
# -----------------------------
# Define the Pydantic models
# -----------------------------
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


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Invoice OCR with LLaMA 4", layout="wide")
st.title("🧾 Smarter Invoice Parsing Powered by Llama 4 🦙")

# Image source selection
input_method = st.radio(
    "Select input method: 📸", 
    ["Upload Image 📤", "Image URL 🌐"]
)

image_source = None
image_url = None
image_bytes = None
mime_type = "image/jpeg"

if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload an invoice image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image_bytes = uploaded_file.read()
        suffix = uploaded_file.name.split(".")[-1].lower()
        if suffix == "png":
            mime_type = "image/png"
        elif suffix in ("jpg", "jpeg"):
            mime_type = "image/jpeg"

elif input_method == "Image URL":
    image_url = st.text_input("Enter image URL:")
    if image_url:
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_bytes = response.content  # For display only
        except Exception as e:
            st.error(f"Error loading image from URL: {str(e)}")

if image_bytes:
    # Layout with columns
    col1, col2 = st.columns([1, 2])

    # Left column: Show image
    with col1:
        st.subheader("Invoice Image")
        try:
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption="Uploaded Invoice" if input_method == "Upload Image" else "Image from URL")
        except Exception as e:
            st.error(f"Error displaying image: {str(e)}")

    # Right column: Process and show extracted fields
    with col2:
        st.subheader("Extracted Invoice Fields")
        if st.button("Extract Invoice Data"):
            with st.spinner("Extracting data using LLaMA 4..."):
                try:
                    # Ensure the API key is loaded securely from Streamlit secrets
                    groq_api_key = st.secrets["GROQ_API_KEY"]
                    client = Groq(api_key=groq_api_key)

                    prompt = f"""
                    You are an intelligent OCR extraction agent capable of understanding and processing documents in multiple languages.
                    Given an image of an invoice, extract all relevant information in structured JSON format.
                    The JSON object must use the schema: {json.dumps(InvoiceData.model_json_schema(), indent=2)}
                    If any field cannot be found in the invoice, return it as null. Focus on clarity and accuracy, and ignore irrelevant text such as watermarks, headers, or decorative elements. Return the final result strictly in JSON format.
                    """

                    # Prepare the image content based on input method
                    if input_method == "Upload Image":
                        base64_image = base64.b64encode(image_bytes).decode("utf-8")
                        image_content = {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    else:  # Image URL case
                        image_content = {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }

                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    image_content
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
                except Exception as e:
                    st.error(f"❌ Failed to parse invoice: {str(e)}")
