import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.web_scraper import search_and_scrape

def test_scraper():
    print("Testing web scraper...")
    print("-" * 50)
    
    # Test query
    query = "latest developments in artificial intelligence"
    print(f"Searching for: {query}")
    
    # Get results
    results = search_and_scrape(query, max_results=3)
    
    # Print results
    print("\nResults:")
    print("-" * 50)
    if isinstance(results, list):
        for i, content in enumerate(results, 1):
            print(f"\nArticle {i}:")
            print("-" * 30)
            print(f"Length: {len(content)} characters")
            print(f"Preview: {content[:200]}...")
    else:
        print(f"Error: {results}")

if __name__ == "__main__":
    test_scraper() 