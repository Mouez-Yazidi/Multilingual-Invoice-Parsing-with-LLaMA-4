import json
from groq import Groq

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
