import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchChat:
    def __init__(self):
        """Initialize the chat with Google's Generative AI model."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')
        self.chat = self.model.start_chat(history=[])
        
    def send_message(self, message: str) -> str:
        """
        Send a message to the chat and get the response.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The model's response
        """
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
            
    def get_history(self) -> list:
        """
        Get the chat history.
        
        Returns:
            list: List of messages in the chat history
        """
        return self.chat.history 