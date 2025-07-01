import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.research_agent import run_research_agent

# Configure the page
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        font-size: 1.2em;
    }
    .stButton>button {
        font-size: 1.2em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🧠 AI Research Agent")
st.markdown("""
This AI-powered research agent helps you gather and analyze information from across the web.
Simply enter your research topic or question, and the agent will:
1. Search for relevant articles
2. Extract and analyze the content
3. Generate a comprehensive research report
""")

# Input section
query = st.text_input(
    "Enter your research topic or question:",
    placeholder="e.g., 'Latest developments in quantum computing' or 'Impact of AI on healthcare'"
)

# Advanced options in an expander
with st.expander("Advanced Options"):
    max_results = st.slider("Maximum number of articles to analyze", 3, 10, 5)

# Generate button
if st.button("Generate Research Report", type="primary") and query:
    with st.spinner("🔍 Researching and analyzing..."):
        try:
            result = run_research_agent(query, max_results=max_results)
            st.markdown("### 📊 Research Report")
            st.markdown(result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("👆 Enter a research topic and click 'Generate Research Report' to begin") 