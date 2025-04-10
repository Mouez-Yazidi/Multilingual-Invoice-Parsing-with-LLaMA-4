# multilingual Invoice Parsing with LLaMA 4, OCR, and Python
Combining OCR for text extraction with LLMs for accurate, efficient document structuring.

## 🔍 Project Overview

This project demonstrates how **Meta's LLaMA 4** is revolutionizing **OCR and document parsing** with its advanced **multimodal** and **multilingual** capabilities. By utilizing **LLaMA 4**, we explore its ability to **extract structured data** from real-world invoices, validate the results using **Pydantic**, and build an intuitive **Streamlit app** for user interaction. 

The model excels in parsing invoices in multiple languages, including **English**, **French**, and **Arabic**, ensuring **accurate** and **reliable** outputs. This project showcases **LLaMA 4** as a powerful tool for **intelligent document processing**, paving the way for smarter, **AI-driven automation** in various industries.

# 🎯 Key Features
- **Automated Invoice Parsing with LLaMA 4**: Leverage LLaMA 4’s advanced multimodal capabilities to automate and enhance the invoice parsing process, extracting structured data efficiently.

- **Structured Data Validation with Pydantic**: Use Pydantic’s BaseModel to refine, validate, and ensure the output from LLaMA 4 is clean, structured, and reliable for further processing.

- **Multilingual OCR Parsing**: Unlock LLaMA 4’s versatility by parsing invoices in multiple languages, including **English**, **French**, and **Arabic**, demonstrating its robust multilingual understanding.

- **Interactive Streamlit App**: Build an intuitive, interactive Streamlit app for invoice parsing and deploy it to the cloud, providing a seamless user experience for document processing.

# 🚀 Getting Started
### Prerequisites
* Python 3.11 or above 🐍
* Groq API for inference, which is currently available for free in its beta version with rate limits. You can obtain your API key here after creating an account: [Groq API](https://medium.com/r/?url=https%3A%2F%2Fconsole.groq.com%2Fkeys).

# 💻 Local Deployment
### 1. Clone the Repository
```bash
git clone https://github.com/Mouez-Yazidi/Multilingual-Invoice-Parsing-with-LLaMA-4.git
cd Multilingual-Invoice-Parsing-with-LLaMA-4
```
### 2. Add Environment Variables
* Create a `.env` file and add the following variables according to the credentials you obtained from the required platforms:

    ```plaintext
    GROQ_API_KEY=
    ```
    
### 3. Install Dependencies
Navigate to the local directory and install the necessary dependencies:
```bash
pip install -r requirements.txt
```

### 4. Running the App Locally
To run the app locally, execute the following command:

```bash
streamlit run app.py --environment local
```
You should now be able to access the app at http://localhost:8501 🌐.

### 🐳 Optional: Running with Docker
If you prefer running the app in a Docker container, follow these steps:
1. Make sure you have Docker installed 🐋.
2. Build the Docker image:
```bash
docker build -t InvoiceParsing -f Dockerfile  ..
```
3. Run the container:
```bash
docker run -p 8501:8501 InvoiceParsing streamlit run app.py --environment local
```
# ☁️ Streamlit Cloud Deployment
### 1. Prepare Your Repository
Ensure that your code is pushed to a GitHub repository 📂.

### 2. Link with Streamlit Cloud
* Visit Streamlit Cloud and sign in.
* Connect your GitHub repository 🔗.
* Choose your repository and branch.

### 3. Environment Variables
* Go to the "Advanced settings" section of your app.
* In the "Secrets" section, input any sensitive information, such as API keys or other credentials.
* Make sure to add this variables according to the credentials you obtained from the required platforms.
```csharp
GROQ_API_KEY=""
```
Streamlit Cloud will:
* Install dependencies from cloud/requirements.txt 📦

🎉 You’re all set! Your app will now be live on Streamlit Cloud!
