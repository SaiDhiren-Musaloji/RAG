# Research Aggregator - RAG Model

A sophisticated **Retrieval-Augmented Generation (RAG)** system that leverages Google's Gemini API to provide accurate, context-aware responses by training on proper research data before performing any analysis tasks.

## 🚀 Features

- **RAG Architecture**: Retrieval-Augmented Generation for context-aware responses
- **Data Training Pipeline**: Proper data preprocessing and training before task execution
- **Intelligent Retrieval**: Smart document retrieval and context building
- **AI-Powered Analysis**: Uses Google Gemini 1.5 Flash for intelligent paper analysis
- **Smart Summarization**: Generates comprehensive summaries based on trained data
- **Interactive Chat**: Context-aware conversations using retrieved information
- **Web Scraping**: Automatically extracts and processes content for training
- **Free Tier**: Uses Google's free tier models (no cost for basic usage)

## 🔬 How RAG Works

This system implements a **Retrieval-Augmented Generation** approach:

1. **Data Ingestion**: Collects and processes research papers, documents, and web content
2. **Training Phase**: Properly trains the model on the collected data
3. **Retrieval**: When queried, retrieves relevant context from trained data
4. **Generation**: Generates responses based on retrieved context + AI capabilities
5. **Validation**: Ensures responses are grounded in the trained data

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)
- Research papers or documents for training

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SaiDhiren-Musaloji/RAG.git
   cd RAG
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   **IMPORTANT**: Never commit your actual API key to version control!
   
   Create a `.env` file in the root directory:
   ```bash
   # Copy the example file
   cp research_aggregator/.env.example .env
   
   # Edit the .env file and add your actual API key
   nano .env
   ```
   
   Your `.env` file should look like this:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## 🔑 Getting Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in your `.env` file

**Note**: The free tier includes:
- Gemini 1.5 Flash (what we're using)
- Gemini 2.0 Flash
- Other free models

## 🚀 Usage

### Training Your RAG Model

```python
from research_aggregator.agent.research_agent import ResearchAgent

# Initialize the research agent
agent = ResearchAgent()

# Train on your research data
agent.train_on_documents([
    "path/to/paper1.pdf",
    "path/to/paper2.pdf",
    "https://arxiv.org/abs/your-paper"
])

# The model is now trained and ready for queries
```

### Running the Application

```bash
# Activate your virtual environment
source venv/bin/activate

# Run the main application
python research_aggregator/main.py
```

### Using the RAG Chat Interface

```python
from research_aggregator.agent.chat import ChatAgent

# Initialize the chat agent (uses trained data)
chat_agent = ChatAgent()

# Ask questions based on trained data
response = chat_agent.chat("What are the key findings in the papers I trained on?")
print(response)
```

### Summarizing Papers with Context

```python
from research_aggregator.agent.summarizer import summarize_paper

# Summarize a research paper using trained context
summary = summarize_paper("path/to/paper.pdf")
print(summary)
```

## 📁 Project Structure

```
RAG/
├── research_aggregator/
│   ├── agent/
│   │   ├── chat.py          # RAG chat interface
│   │   ├── summarizer.py    # Context-aware summarization
│   │   ├── analyzer.py      # Data analysis with training
│   │   ├── research_agent.py # Main RAG training agent
│   │   └── web_scraper.py   # Data collection for training
│   ├── src/                 # Core RAG logic
│   ├── tests/               # Test files
│   └── data/                # Training data storage
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔒 Security

- **Never commit your `.env` file** - it's already in `.gitignore`
- **Never share your API keys** publicly
- **Use environment variables** for all sensitive data
- **Rotate your API keys** regularly

## 🧪 Testing

```bash
# Run tests
python -m pytest research_aggregator/tests/

# Run specific test
python research_aggregator/tests/test_models.py
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

If you encounter any issues:
1. Check that your API key is correctly set in the `.env` file
2. Ensure you're using the free tier models
3. Verify your training data is properly formatted
4. Check the [Google AI Studio documentation](https://ai.google.dev/docs)
5. Open an issue in this repository

## 🔄 Updates

- **Model**: Currently using `models/gemini-1.5-flash` (free tier)
- **Architecture**: RAG (Retrieval-Augmented Generation)
- **API**: Google Gemini API
- **Last Updated**: June 2024 