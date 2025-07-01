import requests
from newspaper import Article
import time
import os
from dotenv import load_dotenv

load_dotenv()

def search_and_scrape(query, max_results=5):
    """
    Search for articles using serper.dev API and scrape their content
    """
    urls = []
    contents = []
    
    # Get API key from environment
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return ["Error: SERPER_API_KEY not found in environment variables"]
    
    # Search using serper.dev
    try:
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': max_results
        }
        
        response = requests.post(
            'https://google.serper.dev/search',
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            return [f"Error searching: {response.text}"]
            
        data = response.json()
        
        # Extract URLs from organic results
        if 'organic' in data:
            for result in data['organic']:
                if 'link' in result:
                    urls.append(result['link'])
    
    except Exception as e:
        return [f"Error searching: {str(e)}"]

    # Process URLs with delays
    for url in urls:
        try:
            # Add delay between requests
            time.sleep(2)
            
            article = Article(url)
            article.download()
            article.parse()
            
            if article.text.strip():  # Only add non-empty articles
                contents.append(article.text)
        except Exception as e:
            continue
            
    return contents if contents else ["No valid articles found. Try a different query."] 