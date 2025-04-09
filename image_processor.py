import base64
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

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
        st.image(image, use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")
