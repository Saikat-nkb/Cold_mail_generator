import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import time
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def load_css():
    st.markdown("""
        <style>
        /* Reset default streamlit background */
        .stApp {
            background: transparent;
        }
        
        /* Main background with gradient */
        .main {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            padding: 2em;
            border-radius: 10px;
            margin: -1em -1em 2em -1em;
        }
        
        /* Gradient animation */
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Card styles */
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            color: white;
        }
        
        /* Title styles */
        .title {
            text-align: center;
            color: white;
            font-size: 3.5em;  /* Increased from 2.5em to 3.5em */
            margin-bottom: 30px;
            font-weight: bold;
        }
        
        /* Input container */
        .input-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        /* Output container */
        .output-container {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            min-height: 300px;  /* Added minimum height */
            white-space: pre-line;  /* Preserve line breaks */
        }
        
        /* Email text styling */
        .output-container pre {
            white-space: pre-line;  /* Preserve line breaks */
            font-family: inherit;   /* Use regular font instead of monospace */
            margin: 0;
            padding: 0;
            overflow-wrap: break-word;  /* Handle long lines */
        }
        
        /* Custom button */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 5px;
            transition: all 0.3s ease;
            height: 61px;  /* Match the height of the URL input */
            margin-top: 25px;  /* Align with the URL input */
        }
        
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }

        /* URL input styling */
        .stTextInput div[data-baseweb="input"] {
            margin-top: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

def create_streamlit_app(llm, portfolio, clean_text):
    load_css()
    
    # Main container with gradient background
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="title">📧 Cold Mail Generator</h1>', unsafe_allow_html=True)
    
    # Welcome card
    st.markdown("""
        <div class="card">
            <h2>Welcome to XYZ COMPANY's Cold Mail Generator!</h2>
            <p>Generate personalized cold emails based on job postings with just a few clicks.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section with adjusted columns ratio
    with st.container():
        col1, col2 = st.columns([4, 1])  # Adjusted ratio from [3, 1] to [4, 1]
        
        with col1:
            url_input = st.text_input(
                "Enter a Job Posting URL:",
                placeholder="e.g., https://careers.company.com/job-posting",
                help="Paste the complete URL of the job posting you want to analyze",
                label_visibility="collapsed"  # Hide the label to improve alignment
            )
        
        with col2:
            submit_button = st.button("Generate Email", type="primary", use_container_width=True)

    if submit_button and url_input:
        try:
            # Progress tracking
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with progress_placeholder.container():
                progress_bar = st.progress(0)
            
            # Load and process
            for i, status in enumerate([
                "Loading job posting...",
                "Analyzing content...",
                "Extracting job details...",
                "Generating email..."
            ], 1):
                status_placeholder.markdown(f'<div class="card">{status}</div>', unsafe_allow_html=True)
                progress_bar.progress(i * 25)
                time.sleep(0.5)
                
                if i == 1:
                    loader = WebBaseLoader([url_input])
                    data = loader.load()
                    if not data:
                        st.error("Could not load content from the provided URL")
                        return
                    content = data[0].page_content
                    cleaned_content = clean_text(content)
                elif i == 2:
                    portfolio.load_portfolio()
                elif i == 3:
                    jobs = llm.extract_jobs(cleaned_content)
                    if not isinstance(jobs, list):
                        jobs = [jobs]
                elif i == 4:
                    for idx, job in enumerate(jobs, 1):
                        skills = job.get('skills', [])
                        if isinstance(skills, list):
                            skills = ', '.join(skills)
                        links = portfolio.query_links(skills)
                        email = llm.write_mail(job, links)
                        
                        st.markdown(f"""
                            <div class="output-container">
                                <h3>Generated Email {idx}</h3>
                                <pre>{email}</pre>
                            </div>
                        """, unsafe_allow_html=True)
            
            # Clear progress indicators
            progress_placeholder.empty()
            status_placeholder.empty()
            
        except Exception as e:
            st.error(f"An Error Occurred: {str(e)}")
    elif submit_button:
        st.warning("Please enter a URL first")
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="Cold Email Generator",
        page_icon="📧",
        initial_sidebar_state="collapsed",
        menu_items=None
    )
    
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)