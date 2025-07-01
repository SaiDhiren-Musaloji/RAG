from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from newspaper import Article
import nltk
from transformers import pipeline

# Download required NLTK data
nltk.download('punkt')

app = FastAPI(title="Research Aggregator API")

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class URLInput(BaseModel):
    url: str

class ReportResponse(BaseModel):
    title: str
    summary: str
    key_points: List[str]
    full_text: str

@app.post("/analyze", response_model=ReportResponse)
async def analyze_article(url_input: URLInput):
    try:
        # Scrape the article
        article = Article(url_input.url)
        article.download()
        article.parse()
        article.nlp()  # This will extract keywords, summary, etc.

        # Generate a more detailed summary using BART
        summary = summarizer(article.text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

        return ReportResponse(
            title=article.title,
            summary=summary,
            key_points=article.keywords,
            full_text=article.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Research Aggregator API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 