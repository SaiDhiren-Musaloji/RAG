from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import nltk
from nltk.tokenize import sent_tokenize
from typing import List, Dict
import torch
import logging
from collections import Counter
import spacy
from sentence_transformers import SentenceTransformer
import numpy as np
from gensim import corpora, models
import os
import json
from sklearn.neighbors import NearestNeighbors

class NLPProcessor:
    def __init__(self):
        self.setup_logging()
        self.setup_models()
        self.setup_vector_store()
        self.nlp = spacy.load("en_core_web_sm")

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_models(self):
        """Initialize the necessary NLP models."""
        try:
            # Using smaller models for better performance on CPU
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU
            )
            
            # Using sentence transformers for semantic search
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # For named entity recognition
            self.ner = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                device=-1
            )
            
            # For sentiment analysis
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1
            )
            
        except Exception as e:
            self.logger.error(f"Error setting up models: {str(e)}")
            raise

    def setup_vector_store(self):
        """Setup NearestNeighbors for semantic search."""
        self.vector_dimension = 384  # Dimension for all-MiniLM-L6-v2
        self.embeddings = []
        self.texts = []
        self.nn_model = None

    def chunk_text(self, text: str, max_length: int = 1024) -> List[str]:
        """Split text into chunks that can be processed by the model."""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length > max_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Generate a summary of the input text."""
        try:
            chunks = self.chunk_text(text)
            summaries = []

            for chunk in chunks:
                summary = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                summaries.append(summary[0]['summary_text'])

            return " ".join(summaries)
        except Exception as e:
            self.logger.error(f"Error in summarization: {str(e)}")
            return ""

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract named entities from the text."""
        try:
            doc = self.nlp(text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            return entities
        except Exception as e:
            self.logger.error(f"Error in entity extraction: {str(e)}")
            return []

    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze the sentiment of the text."""
        try:
            result = self.sentiment_analyzer(text)[0]
            return {
                'label': result['label'],
                'score': result['score']
            }
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            return {'label': 'NEUTRAL', 'score': 0.0}

    def extract_key_phrases(self, text: str, num_phrases: int = 5) -> List[str]:
        """Extract key phrases from the text."""
        try:
            doc = self.nlp(text)
            # Get noun chunks and named entities
            phrases = [chunk.text for chunk in doc.noun_chunks]
            phrases.extend([ent.text for ent in doc.ents])
            
            # Count frequency
            phrase_freq = Counter(phrases)
            
            # Return most common phrases
            return [phrase for phrase, _ in phrase_freq.most_common(num_phrases)]
        except Exception as e:
            self.logger.error(f"Error in key phrase extraction: {str(e)}")
            return []

    def extract_topics(self, texts: List[str], num_topics: int = 5) -> List[Dict]:
        """Extract topics using LDA."""
        try:
            # Prepare texts
            texts = [text.split() for text in texts]
            
            # Create dictionary
            dictionary = corpora.Dictionary(texts)
            
            # Create corpus
            corpus = [dictionary.doc2bow(text) for text in texts]
            
            # Train LDA model
            lda_model = models.LdaModel(
                corpus,
                num_topics=num_topics,
                id2word=dictionary
            )
            
            # Extract topics
            topics = []
            for topic_id in range(num_topics):
                topic_words = lda_model.show_topic(topic_id)
                topics.append({
                    'topic_id': topic_id,
                    'words': [word for word, _ in topic_words]
                })
            
            return topics
        except Exception as e:
            self.logger.error(f"Error in topic extraction: {str(e)}")
            return []

    def add_to_vector_store(self, text: str):
        """Add text to vector store for semantic search."""
        try:
            # Get text embedding
            embedding = self.sentence_model.encode([text])[0]
            
            # Add to embeddings and texts
            self.embeddings.append(embedding)
            self.texts.append(text)
            
            # Re-fit the NearestNeighbors model whenever new data is added
            if len(self.embeddings) > 0:
                self.nn_model = NearestNeighbors(n_neighbors=min(5, len(self.embeddings)), metric='cosine')
                self.nn_model.fit(np.array(self.embeddings))
        except Exception as e:
            self.logger.error(f"Error adding to vector store: {str(e)}")

    def semantic_search(self, query: str, k: int = 5) -> List[str]:
        """Perform semantic search in vector store."""
        try:
            if not self.nn_model or len(self.embeddings) == 0:
                return []
            
            # Get query embedding
            query_embedding = self.sentence_model.encode([query])[0]
            
            # Search using NearestNeighbors
            distances, indices = self.nn_model.kneighbors(np.array([query_embedding]))
            
            # Return matching texts
            return [self.texts[i] for i in indices[0]]
        except Exception as e:
            self.logger.error(f"Error in semantic search: {str(e)}")
            return []

    def process_article(self, article_data: Dict) -> Dict:
        """Process a single article with all NLP tasks."""
        try:
            text = article_data['text']
            
            # Add to vector store
            self.add_to_vector_store(text)
            
            return {
                'summary': self.summarize_text(text),
                'entities': self.extract_entities(text),
                'sentiment': self.analyze_sentiment(text),
                'key_phrases': self.extract_key_phrases(text),
                'original_data': article_data
            }
        except Exception as e:
            self.logger.error(f"Error processing article: {str(e)}")
            return {}

    def combine_summaries(self, processed_articles: List[Dict]) -> Dict:
        """Combine multiple article summaries into a comprehensive analysis."""
        try:
            all_text = " ".join([article['summary'] for article in processed_articles])
            
            # Extract topics from all articles
            topics = self.extract_topics([article['summary'] for article in processed_articles])
            
            return {
                'comprehensive_summary': self.summarize_text(all_text, max_length=300, min_length=100),
                'common_entities': self.extract_entities(all_text),
                'overall_sentiment': self.analyze_sentiment(all_text),
                'key_themes': self.extract_key_phrases(all_text, num_phrases=10),
                'topics': topics,
                'source_count': len(processed_articles)
            }
        except Exception as e:
            self.logger.error(f"Error combining summaries: {str(e)}")
            return {} 