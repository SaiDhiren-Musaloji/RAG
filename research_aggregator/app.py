import streamlit as st
from agent.web_scraper import search_and_scrape
from agent.chat import ResearchChat
from agent.analyzer import ResearchAnalyzer

st.set_page_config(page_title="AI Research Agent", layout="wide")

st.title("AI Research Agent 🤖")

# Initialize session state for chat and analyzer
if "chat" not in st.session_state:
    st.session_state.chat = ResearchChat()
if "analyzer" not in st.session_state:
    st.session_state.analyzer = ResearchAnalyzer()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for research query
with st.sidebar:
    st.header("Research Query")
    query = st.text_input("Enter your research topic:")
    max_results = st.slider("Maximum number of sources", 1, 10, 5)
    
    if st.button("Start Research"):
        with st.spinner("Gathering information and generating report..."):
            # Get articles
            articles = search_and_scrape(query, max_results)
            
            # Store raw articles in session state for debugging
            st.session_state.raw_articles = articles
            
            if articles and not articles[0].startswith("Error"):
                # Generate comprehensive analysis report
                analysis_report = st.session_state.analyzer.filter_and_analyze(query, articles)
                
                # Store in session state
                st.session_state.research_summary = analysis_report # Renaming for consistency, though it's now a report
                st.session_state.messages.append({"role": "assistant", "content": f"I've completed the research on '{query}'. Here's the detailed analysis report:\n\n{analysis_report}"})
            else:
                st.error(articles[0] if articles else "No results found or an error occurred during scraping.")

# Main chat interface
st.header("Chat with Research Assistant")

# Display raw scraped articles for debugging
if "raw_articles" in st.session_state and st.session_state.raw_articles:
    st.subheader("Raw Scraped Content (for debugging):")
    for i, article_content in enumerate(st.session_state.raw_articles):
        st.write(f"--- Article {i+1} ---")
        st.code(article_content, language="text")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a follow-up question about the research"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response}) 