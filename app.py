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

# Sidebar for input
with st.sidebar:
    st.title("🎯 Content Prompt")
    prompt = st.text_area("What's your idea?", key="prompt", height=150)
    st.markdown("**Choose Platforms**")
    linkedin_chk = st.checkbox("LinkedIn")
    twitter_chk = st.checkbox("Twitter")
    instagram_chk = st.checkbox("Instagram")
    facebook_chk = st.checkbox("Facebook")
    generate = st.button("✨ Generate Content")

# Main area title
st.markdown("<h1 style='text-align: center;'>📣 AI Social Media Content Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Create tailored posts for different platforms using AI agents</p>", unsafe_allow_html=True)

# Determine selected platforms
selected = []
for name, chk in [("LinkedIn", linkedin_chk), ("Twitter", twitter_chk),
                  ("Instagram", instagram_chk), ("Facebook", facebook_chk)]:
    if chk:
        selected.append(name)

# Generate and display content
if generate:
    if prompt and selected:
        with st.spinner("🧠 Generating brief..."):
            strategist = ContentStrategistAgent()
            brief = strategist.run(prompt)

        for platform in selected:
            with st.spinner(f"✍️ Creating content for {platform}..."):
                agent_map = {
                    "LinkedIn": LinkedInAgent(),
                    "Twitter": TwitterAgent(),
                    "Instagram": InstagramAgent(),
                    "Facebook": FacebookAgent()
                }
                agent = agent_map[platform]
                post = agent.run(brief)

                # Display in colored box with readable text color
                st.markdown(f"### 🎯 {platform}")
                st.markdown(
                    f"<div style='background-color:#e0f7fa; color:#000000; padding:15px; border-radius:8px; line-height:1.5;'>{post}</div>",
                    unsafe_allow_html=True
                )

                # Log to Airtable
                if log_to_airtable(prompt, platform, post):
                    st.caption(f"✅ Logged to Airtable ({platform})")
                else:
                    st.caption(f"⚠️ Airtable log failed ({platform})")

        # Celebrate with balloons and confetti
        st.balloons()
        components.html(
            "<script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>"
            "<script>confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 }});</script>",
            height=0,
        )
    else:
        st.warning("Enter an idea and select at least one platform.")