import streamlit as st
import openai
import os
import json
from datetime import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AISocialPros Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize directories
ARTICLES_DIR = Path("articles")
ARTICLES_DIR.mkdir(exist_ok=True)
LOG_FILE = "generation_log.json"

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    st.error("⚠️ OpenAI API key not found! Please set OPENAI_API_KEY in your .env file.")
    st.stop()

# Initialize session state
if 'generated_articles' not in st.session_state:
    st.session_state.generated_articles = []

def load_log():
    """Load the generation log"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_log(entry):
    """Save entry to generation log"""
    log = load_log()
    log.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def fetch_article_content(url):
    """Fetch content from URL (simplified version)"""
    try:
        response = requests.get(url, timeout=10)
        # This is a simplified version - in production you'd want proper HTML parsing
        return response.text[:2000]  # Limit content length
    except:
        return f"Could not fetch content from {url}"

def generate_article(topic, example_articles, openai_api_key):
    """Generate article using OpenAI API"""
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Prepare the prompt
        examples_text = "\n\n".join([f"Example {i+1}:\n{content}" for i, content in enumerate(example_articles)])
        
        prompt = f"""
        Create a marketing article on the topic: "{topic}"
        
        Please write in a similar style to these examples:
        {examples_text}
        
        The article should be:
        - Engaging and professional
        - Well-structured with clear sections
        - Include practical insights
        - Be around 500-800 words
        - Follow the writing style and tone of the provided examples
        """
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are an expert marketing content writer. Write articles in plain text format only. Do not use HTML tags, markdown formatting, or any markup language. Return clean, readable text with proper line breaks and spacing."},
                {"role": "user", "content": prompt}
            ],
            # max_tokens=3000,
            # temperature=0.8
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating article: {str(e)}"

def save_article(title, content):
    """Save article to file and return filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"article_{timestamp}.txt"
    filepath = ARTICLES_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Title: {title}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n\n")
        f.write(content)
    
    return filename

def get_archived_articles():
    """Get list of archived articles"""
    articles = []
    if ARTICLES_DIR.exists():
        for file in sorted(ARTICLES_DIR.glob("*.txt"), reverse=True):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    title = lines[0].replace("Title: ", "").strip() if lines else "Untitled"
                    date = lines[1].replace("Generated: ", "").strip() if len(lines) > 1 else "Unknown date"
                    articles.append({
                        'title': title,
                        'date': date,
                        'filename': file.name,
                        'filepath': str(file)
                    })
            except:
                continue
    return articles

# Main UI
st.title("🚀 AISocialPros Studio")
st.markdown("Generate compelling marketing articles with AI assistance!")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Hello at AISocialPros Studio!",
    "🔗 Example Articles",
    "✨ Result",
    "📚 Archive"
])

with tab1:
    st.header("Welcome to AISocialPros Studio!")
    st.markdown("""
    Generate high-quality marketing articles tailored to your style using AI.
    
    **How it works:**
    1. Provide a topic for your new article
    2. Share up to 3 links to existing articles as style examples
    3. Get your AI-generated article
    4. Access all your articles in the archive
    """)
    
    # Topic input
    st.subheader("📋 Article Topic")
    topic = st.text_area(
        "Enter the topic for your new article:",
        placeholder="e.g., 'Email marketing strategies for small businesses'",
        height=100
    )
    
    if topic:
        st.session_state.topic = topic
        st.success(f"Topic set: {topic}")

with tab2:
    st.header("📎 Example Articles")
    st.markdown("Provide up to 3 links to existing articles that will be used as style examples.")
    
    example_urls = []
    
    for i in range(3):
        url = st.text_input(f"Example Article {i+1} URL:", key=f"url_{i}")
        if url:
            example_urls.append(url)
    
    if example_urls:
        st.session_state.example_urls = example_urls
        st.success(f"Added {len(example_urls)} example article(s)")
        
        # Preview fetched content
        with st.expander("Preview fetched content"):
            for i, url in enumerate(example_urls):
                st.write(f"**Example {i+1}:** {url}")
                with st.spinner(f"Fetching content from example {i+1}..."):
                    content = fetch_article_content(url)
                    st.text_area(f"Content preview {i+1}:", content[:500] + "...", height=100, disabled=True)

with tab3:
    st.header("✨ Generated Article")
    
    if st.button("🎯 Generate Article", type="primary", use_container_width=True):
        # Check requirements
        if not hasattr(st.session_state, 'topic'):
            st.error("Please provide a topic in the first tab.")
        elif not hasattr(st.session_state, 'example_urls') or len(st.session_state.example_urls) == 0:
            st.error("Please provide at least one example article URL in the second tab.")
        else:
            with st.spinner("Generating your article... This may take a few moments."):
                # Fetch example articles
                example_articles = []
                for url in st.session_state.example_urls:
                    content = fetch_article_content(url)
                    example_articles.append(content)
                
                # Generate article
                article = generate_article(
                    st.session_state.topic,
                    example_articles,
                    OPENAI_API_KEY
                )
                
                if article and not article.startswith("Error"):
                    # Save article
                    filename = save_article(st.session_state.topic, article)
                    
                    # Log generation
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'topic': st.session_state.topic,
                        'example_urls': st.session_state.example_urls,
                        'filename': filename
                    }
                    save_log(log_entry)
                    
                    st.success("Article generated successfully!")
                    st.session_state.last_generated_article = article
                    st.session_state.last_filename = filename
                else:
                    st.error(article)
    
    # Display last generated article
    if hasattr(st.session_state, 'last_generated_article'):
        st.subheader("📄 Your Generated Article")
        st.markdown(st.session_state.last_generated_article)
        
        # Download button
        if hasattr(st.session_state, 'last_filename'):
            with open(ARTICLES_DIR / st.session_state.last_filename, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="💾 Download Article",
                    data=f.read(),
                    file_name=st.session_state.last_filename,
                    mime="text/plain"
                )

with tab4:
    st.header("📚 Article Archive")
    st.markdown("All your previously generated articles, newest first.")
    
    articles = get_archived_articles()
    
    if articles:
        for article in articles:
            with st.expander(f"📄 {article['title']} - {article['date']}"):
                try:
                    with open(article['filepath'], 'r', encoding='utf-8') as f:
                        content = f.read()
                        st.text_area("Content:", content, height=300, disabled=True)
                        
                        # Download button for each article
                        st.download_button(
                            label="💾 Download",
                            data=content,
                            file_name=article['filename'],
                            mime="text/plain",
                            key=f"download_{article['filename']}"
                        )
                except Exception as e:
                    st.error(f"Error loading article: {str(e)}")
    else:
        st.info("No articles generated yet. Create your first article using the tabs above!")

# Footer
st.markdown("---")
st.markdown("*Powered by OpenAI GPT and Streamlit*")
