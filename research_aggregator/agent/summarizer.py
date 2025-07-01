import google.generativeai as genai
import os
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

load_dotenv()

class RateLimitException(Exception):
    """Custom exception for rate limit errors."""
    pass

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(RateLimitException)
)
def summarize_texts(texts: list[str]) -> str:
    """
    Summarizes a list of texts using the gemma-3-27b-it model.
    
    Args:
        texts (list[str]): A list of text documents to summarize.
        
    Returns:
        str: A comprehensive summary of all texts.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY not found in environment variables"
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    combined_text = "\n\n".join(texts)
    
    prompt = f"""
    You are an AI research assistant. Your task is to provide a comprehensive and well-structured research report based on the provided texts. 
    The report should include an executive summary, a detailed introduction, a breakdown of key findings, ethical considerations (if applicable), limitations and future research directions, and a conclusion. 
    Ensure that the report is coherent, informative, and free of redundancies. Provide citations in the text using numerical references (e.g., [1], [2]) corresponding to the order of the source texts provided. 
    When citing, refer to the source text number. If a piece of information comes from more than one source, cite all applicable sources. 
    Do not make up any information or add any external knowledge beyond what is provided in the texts. If a section cannot be generated based on the provided text, state 'N/A' or 'Not applicable'.

    Here are the texts:

    {combined_text}

    Comprehensive Research Report:
    """
    
    try:
        response = model.generate_content(prompt)
        if "quota_metric" in response.text and "rate-limits" in response.text:
            raise RateLimitException(response.text)
        return response.text
    except RateLimitException as e:
        print(f"Rate limit exceeded, retrying... {e}")
        raise # Re-raise to trigger tenacity retry
    except Exception as e:
        return f"Error generating summary: {str(e)}" 