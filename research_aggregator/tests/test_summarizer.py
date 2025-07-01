import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.summarizer import summarize_texts

def test_summarizer():
    print("Testing summarizer...")
    print("-" * 50)
    
    # Test texts
    test_texts = [
        "Artificial Intelligence (AI) is transforming industries across the globe. Recent developments in machine learning have enabled computers to perform tasks that previously required human intelligence.",
        "The healthcare sector is seeing significant improvements through AI applications. From disease diagnosis to drug discovery, AI is helping medical professionals make better decisions.",
        "Ethical considerations in AI development are becoming increasingly important. As AI systems become more powerful, questions about bias, privacy, and accountability need to be addressed."
    ]
    
    print("Input texts:")
    for i, text in enumerate(test_texts, 1):
        print(f"\nText {i}:")
        print("-" * 30)
        print(text)
    
    print("\nGenerating summary...")
    summary = summarize_texts(test_texts)
    
    print("\nSummary:")
    print("-" * 50)
    print(summary)

if __name__ == "__main__":
    test_summarizer() 