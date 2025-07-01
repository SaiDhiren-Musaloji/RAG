import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.research_agent import run_research_agent

def test_pipeline():
    print("Testing complete research pipeline...")
    print("-" * 50)
    
    # Test query
    query = "impact of artificial intelligence on healthcare"
    print(f"Research query: {query}")
    
    print("\nRunning research pipeline...")
    result = run_research_agent(query, max_results=3)
    
    print("\nFinal Report:")
    print("-" * 50)
    print(result)

if __name__ == "__main__":
    test_pipeline() 