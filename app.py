import streamlit as st
from dotenv import load_dotenv
import os
import openai
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import streamlit.components.v1 as components

from social_agents.content_strategist import ContentStrategistAgent
from social_agents.linkedin_agent import LinkedInAgent
from social_agents.twitter_agent import TwitterAgent
from social_agents.instagram_agent import InstagramAgent
from social_agents.facebook_agent import FacebookAgent
from airtable_logger import log_to_airtable

# Health endpoint
def run_health_server():
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
    HTTPServer(('0.0.0.0', 5000), HealthHandler).serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# Load environment and API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit configuration
st.set_page_config(page_title="AI Social Media Content Generator", layout="wide")

# Initialize session state
if 'generated_posts' not in st.session_state:
    st.session_state.generated_posts = {}
if 'log_results' not in st.session_state:
    st.session_state.log_results = {}
if 'generated' not in st.session_state:
    st.session_state.generated = False

# Sidebar for input
with st.sidebar:
    st.title("🎯 Content Prompt")
    st.text_area("What's your idea?", key="user_prompt", height=150)
    st.markdown("**Choose Platforms**")
    linkedin_chk = st.checkbox("LinkedIn")
    twitter_chk = st.checkbox("Twitter")
    instagram_chk = st.checkbox("Instagram")
    facebook_chk = st.checkbox("Facebook")
    generate = st.button("✨ Generate Content")

# Main area title
st.markdown("<h1 style='text-align: center;'>📣 AI Social Media Content Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Create tailored posts for different platforms using AI agents</p>", unsafe_allow_html=True)

# Read prompt from session
prompt = st.session_state.get("user_prompt", "")

# Show prompt if generated
if st.session_state.generated:
    st.markdown(f"**Your prompt:** {prompt}")

# Determine selected platforms
selected = [name for name, chk in [
    ("LinkedIn", linkedin_chk),
    ("Twitter", twitter_chk),
    ("Instagram", instagram_chk),
    ("Facebook", facebook_chk),
] if chk]

# Generate and store content
if generate:
    if prompt and selected:
        st.session_state.generated = True
        st.session_state.generated_posts.clear()
        st.session_state.log_results.clear()
        with st.spinner("🧠 Generating brief..."):
            strategist = ContentStrategistAgent()
            brief = strategist.run(prompt)
        for platform in selected:
            with st.spinner(f"✍️ Creating content for {platform}..."):
                agent = {
                    "LinkedIn": LinkedInAgent(),
                    "Twitter": TwitterAgent(),
                    "Instagram": InstagramAgent(),
                    "Facebook": FacebookAgent()
                }[platform]
                post = agent.run(brief)
                st.session_state.generated_posts[platform] = post
                success = log_to_airtable(prompt, platform, post)
                st.session_state.log_results[platform] = success
    else:
        st.warning("Enter an idea and select at least one platform.")

# Display generated posts and log status
if st.session_state.generated:
    for platform, post in st.session_state.generated_posts.items():
        st.markdown(f"### 🎯 {platform}")
        # Content box
        st.markdown(
            f"<div style='background-color:#e0f7fa; color:#000000; padding:15px; border-radius:8px; line-height:1.5;'>{post}</div>",
            unsafe_allow_html=True
        )
        # Airtable log status
        success = st.session_state.log_results.get(platform, False)
        if success:
            st.markdown(f"<p style='color: #28a745;'>✅ Logged to Airtable ({platform})</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: #e5534b;'>⚠️ Failed to log {platform} content to Airtable</p>", unsafe_allow_html=True)
    # Celebrate
    st.balloons()
    components.html(
        "<script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>"
        "<script>confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 }});</script>",
        height=0,
    )
