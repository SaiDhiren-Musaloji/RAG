from analyzer import ResearchAnalyzer

def test_model():
    print("Initializing ResearchAnalyzer...")
    analyzer = ResearchAnalyzer()
    
    # Test query and sample article
    test_query = "What are the key features of artificial intelligence?"
    test_articles = [
        """
        Artificial Intelligence (AI) has become a transformative technology in recent years. 
        Key features include machine learning, which allows systems to learn from data, 
        natural language processing for understanding human language, and computer vision 
        for interpreting visual information. AI systems can now perform tasks that typically 
        require human intelligence, such as recognizing speech, making decisions, and solving 
        complex problems. The field continues to evolve rapidly, with new applications 
        emerging in healthcare, finance, and autonomous systems.
        """
    ]
    
    print("\nTesting model with sample query and article...")
    try:
        result = analyzer.filter_and_analyze(test_query, test_articles)
        print("\nAnalysis Result:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError during test: {str(e)}")

if __name__ == "__main__":
    test_model() 