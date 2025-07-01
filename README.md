# Research Aggregator

An AI-powered research paper aggregator that uses Google's Gemini API to analyze, summarize, and provide insights from research papers.

## 🚀 Features

- **AI-Powered Analysis**: Uses Google Gemini 1.5 Flash for intelligent paper analysis
- **Smart Summarization**: Generates comprehensive summaries of research papers
- **Interactive Chat**: Chat with your research papers using natural language
- **Web Scraping**: Automatically extracts content from research paper URLs
- **Free Tier**: Uses Google's free tier models (no cost for basic usage)

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd research-aggregator
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
   cp .env.example .env
   
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

### Running the Application

```bash
# Activate your virtual environment
source venv/bin/activate

# Run the main application
python research_aggregator/main.py
```

### Using the Chat Interface

```python
from research_aggregator.agent.chat import ChatAgent

# Initialize the chat agent
chat_agent = ChatAgent()

# Start a conversation
response = chat_agent.chat("What are the latest trends in AI research?")
print(response)
```

### Summarizing Papers

```python
from research_aggregator.agent.summarizer import summarize_paper

# Summarize a research paper
summary = summarize_paper("path/to/paper.pdf")
print(summary)
```

## 📁 Project Structure

```
research-aggregator/
├── research_aggregator/
│   ├── agent/
│   │   ├── chat.py          # Chat interface with AI
│   │   ├── summarizer.py    # Paper summarization
│   │   ├── analyzer.py      # Paper analysis
│   │   └── web_scraper.py   # Web content extraction
│   ├── src/                 # Core application logic
│   ├── tests/               # Test files
│   └── data/                # Data storage
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
3. Check the [Google AI Studio documentation](https://ai.google.dev/docs)
4. Open an issue in this repository

## 🔄 Updates

- **Model**: Currently using `models/gemini-1.5-flash` (free tier)
- **API**: Google Gemini API
- **Last Updated**: June 2024 