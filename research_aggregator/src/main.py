from scraper import WebScraper
from nlp_processor import NLPProcessor
import logging
from typing import Dict, List
import json
from datetime import datetime
import os
import asyncio
from pathlib import Path
import pandas as pd
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResearchAggregator:
    def __init__(self):
        self.setup_logging()
        self.scraper = WebScraper()
        self.nlp_processor = NLPProcessor()
        self.setup_output_directory()
        self.setup_memory()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_output_directory(self):
        """Create output directory if it doesn't exist."""
        self.output_dir = Path("data/research_outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def setup_memory(self):
        """Initialize memory components."""
        self.query_history = []
        self.topic_memory = defaultdict(list)
        self.source_effectiveness = defaultdict(lambda: {'success': 0, 'total': 0})
        self.vectorizer = TfidfVectorizer()
        self.query_vectors = None
        self.query_texts = []

    def save_results(self, results: Dict, query: str):
        """Save research results to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"research_{timestamp}.json"
        
        output = {
            'query': query,
            'timestamp': timestamp,
            'results': results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to {filename}")
        return filename

    def format_output(self, combined_analysis: Dict, processed_articles: List[Dict]) -> Dict:
        """Format the final output in a readable structure."""
        return {
            'comprehensive_analysis': combined_analysis,
            'source_articles': [
                {
                    'title': article['original_data']['title'],
                    'url': article['original_data']['url'],
                    'summary': article['summary'],
                    'key_phrases': article['key_phrases'],
                    'sentiment': article['sentiment']
                }
                for article in processed_articles
            ],
            'metadata': {
                'total_sources': len(processed_articles),
                'generation_timestamp': datetime.now().isoformat()
            }
        }

    def update_memory(self, query: str, results: Dict):
        """Update memory with new research results."""
        # Update query history
        self.query_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'result_count': len(results.get('source_articles', []))
        })
        
        # Update topic memory
        if results.get('comprehensive_analysis'):
            self.topic_memory[query].append({
                'summary': results['comprehensive_analysis'].get('comprehensive_summary', ''),
                'themes': results['comprehensive_analysis'].get('key_themes', []),
                'topics': results['comprehensive_analysis'].get('topics', []),
                'timestamp': datetime.now().isoformat()
            })
        
        # Update source effectiveness
        for article in results.get('source_articles', []):
            domain = self.extract_domain(article['url'])
            self.source_effectiveness[domain]['total'] += 1
            if article.get('summary'):
                self.source_effectiveness[domain]['success'] += 1
        
        # Update query vectors for similarity search
        self.update_query_vectors(query)

    def extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        from urllib.parse import urlparse
        return urlparse(url).netloc

    def update_query_vectors(self, query: str):
        """Update TF-IDF vectors for query similarity search."""
        self.query_texts.append(query)
        if len(self.query_texts) > 1:
            self.query_vectors = self.vectorizer.fit_transform(self.query_texts)

    def find_similar_queries(self, query: str, threshold: float = 0.3) -> List[str]:
        """Find similar previous queries."""
        if not self.query_vectors or len(self.query_texts) < 2:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.query_vectors)[0]
        similar_indices = np.where(similarities > threshold)[0]
        
        return [self.query_texts[i] for i in similar_indices]

    def get_effective_sources(self, query: str) -> List[str]:
        """Get most effective sources based on historical performance."""
        if not self.source_effectiveness:
            return self.scraper.get_relevant_sources(query)
        
        # Calculate success rate for each source
        source_scores = {
            domain: stats['success'] / stats['total']
            for domain, stats in self.source_effectiveness.items()
            if stats['total'] > 0
        }
        
        # Sort sources by success rate
        sorted_sources = sorted(source_scores.items(), key=lambda x: x[1], reverse=True)
        return [source for source, _ in sorted_sources[:5]]

    async def research_topic(self, query: str, num_sources: int = 5) -> Dict:
        """Main method to research a topic."""
        try:
            self.logger.info(f"Starting research on topic: {query}")
            
            # Check for similar previous queries
            similar_queries = self.find_similar_queries(query)
            if similar_queries:
                self.logger.info(f"Found similar previous queries: {similar_queries}")
            
            # Get effective sources based on history
            effective_sources = self.get_effective_sources(query)
            self.logger.info(f"Using effective sources: {effective_sources}")
            
            # Step 1: Scrape relevant sources
            self.logger.info("Scraping sources...")
            articles = await self.scraper.scrape_multiple_sources(query, num_sources)
            
            if not articles:
                self.logger.warning("No articles found for the query")
                return {}
            
            # Step 2: Process each article
            self.logger.info("Processing articles...")
            processed_articles = [
                self.nlp_processor.process_article(article)
                for article in articles
            ]
            
            # Step 3: Combine and analyze all summaries
            self.logger.info("Combining and analyzing summaries...")
            combined_analysis = self.nlp_processor.combine_summaries(processed_articles)
            
            # Step 4: Format the final output
            final_output = self.format_output(combined_analysis, processed_articles)
            
            # Step 5: Update memory
            self.update_memory(query, final_output)
            
            # Step 6: Save results
            self.save_results(final_output, query)
            
            return final_output
            
        except Exception as e:
            self.logger.error(f"Error in research process: {str(e)}")
            return {}

    def get_research_history(self) -> Dict:
        """Get the research history and insights."""
        return {
            'query_history': self.query_history,
            'topic_memory': dict(self.topic_memory),
            'source_effectiveness': dict(self.source_effectiveness),
            'total_queries': len(self.query_history)
        }

async def main():
    # Example usage
    aggregator = ResearchAggregator()
    
    # Get query from user
    query = input("Enter your research query: ")
    
    # Perform research
    results = await aggregator.research_topic(query)
    
    # Print results
    if results:
        print("\nResearch Results:")
        print("=" * 50)
        print(f"\nComprehensive Summary:")
        print(results['comprehensive_analysis']['comprehensive_summary'])
        
        print("\nKey Themes:")
        for theme in results['comprehensive_analysis']['key_themes']:
            print(f"- {theme}")
        
        print("\nTopics:")
        for topic in results['comprehensive_analysis']['topics']:
            print(f"\nTopic {topic['topic_id']}:")
            print(", ".join(topic['words']))
        
        print("\nSources Analyzed:")
        for article in results['source_articles']:
            print(f"\nTitle: {article['title']}")
            print(f"URL: {article['url']}")
            print(f"Summary: {article['summary'][:200]}...")
    else:
        print("No results found for the query.")

if __name__ == "__main__":
    asyncio.run(main()) 