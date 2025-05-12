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


# Start health-check server
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

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit config
st.set_page_config(page_title="AI Social Media Content Generator",
                   layout="wide")

# Initialize session state
st.session_state.setdefault('generated_posts', {})
st.session_state.setdefault('log_results', {})
st.session_state.setdefault('generated', False)

# Sidebar
with st.sidebar:
    st.title("🎯 Content Prompt")
    st.text_area("What's your idea?", key="user_prompt", height=150)
    st.markdown("**Choose Platforms**")
    linkedin_chk = st.checkbox("LinkedIn")
    twitter_chk = st.checkbox("Twitter")
    instagram_chk = st.checkbox("Instagram")
    facebook_chk = st.checkbox("Facebook")
    generate_btn = st.button("✨ Generate Content")

# Header
st.markdown(
    "<h1 style='text-align:center;'>📣 AI Social Media Content Generator</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Create tailored posts for different platforms</p>",
    unsafe_allow_html=True)

prompt = st.session_state.get("user_prompt", "")

# On Generate
if generate_btn:
    if prompt:
        st.session_state.generated = True
        st.session_state.generated_posts.clear()
        st.session_state.log_results.clear()

        # Get brief + discovered resources
        with st.spinner("🧠 Generating content..."):
            strategist = ContentStrategistAgent()
            brief, articles = strategist.run(prompt)

        # Generate platform posts
        for platform, chk in [("LinkedIn", linkedin_chk),
                              ("Twitter", twitter_chk),
                              ("Instagram", instagram_chk),
                              ("Facebook", facebook_chk)]:
            if chk:
                agent = {
                    "LinkedIn": LinkedInAgent(),
                    "Twitter": TwitterAgent(),
                    "Instagram": InstagramAgent(),
                    "Facebook": FacebookAgent()
                }[platform]
                post = agent.run(brief)
                st.markdown(f"## {platform}")
                st.markdown(
                    f"<div style='background-color:#e0f7fa;color:#000;padding:15px;"
                    f"border-radius:8px;'>{post}</div>",
                    unsafe_allow_html=True)
                success = log_to_airtable(prompt, platform, post)
                st.caption(
                    "✅ Logged to Airtable" if success else "⚠️ Failed to log")

        # Celebrate
        st.balloons()
        components.html(
            "<script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>"
            "<script>confetti({particleCount:100,spread:70,origin:{y:0.6}});</script>",
            height=0,
        )
    else:
        st.warning("Please enter a prompt.")

# If already generated, nothing further
