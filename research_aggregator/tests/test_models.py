import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

def list_models():
    try:
        # Try to get available models
        models = genai.list_models()
        print("Available models:")
        for model in models:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {str(e)}")

if __name__ == "__main__":
    list_models() 