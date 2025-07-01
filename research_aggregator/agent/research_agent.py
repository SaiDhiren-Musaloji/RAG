from agent.web_scraper import search_and_scrape
from agent.summarizer import summarize_texts

def run_research_agent(query, max_results=5):
    """
    Run the complete research pipeline:
    1. Search and scrape articles
    2. Summarize the content
    """
    # Step 1: Search and scrape
    scraped_content = search_and_scrape(query, max_results=max_results)
    
    # Step 2: Summarize
    if len(scraped_content) == 1 and scraped_content[0].startswith("Error") or scraped_content[0].startswith("No valid"):
        return scraped_content[0]
        
    summary = summarize_texts(scraped_content)
    return summary 