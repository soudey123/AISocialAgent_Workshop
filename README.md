# AI Social Media Content Generator – README
A Streamlit app that uses OpenAI agents to transform a single prompt into platform-optimized social media posts (LinkedIn, Twitter, Instagram, Facebook). Fully deployable on Replit or run locally.
---
## ✨ Features
- **Multi-Platform Generation**: Create posts for 4 networks from one idea.  
- **OpenAI-Powered Agents**: Custom strategist and platform agents for focused tone.  
- **Airtable Logging**: Optional integration to store all outputs.  
- **Health Check**: Built-in HTTP endpoint for uptime monitoring.  
- **Visual Flair**: Colored output boxes, balloons, and confetti effects.
---
## 🚀 Quick Start on Replit
1. **Fork or clone** this repository on GitHub:  
   ```
   https://github.com/soudey123/AISocialAgent_Workshop
   ```
2. **Log in** to [Replit](https://replit.com) and click **Create** → **Import from GitHub**.  
3. **Enter** your repo URL and **Import**.  
4. In the Replit **Shell**, run:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
5. Click the **Secrets** icon and add your environment variables (see **Environment** below).  
6. Hit **Run** to launch the app.
---
## 🖥️ Local Development
1. **Clone** the repo:
   ```bash
   git clone https://github.com/soudey123/AISocialAgent_Workshop.git
   cd ai-social-agent
   ```
2. **(Optional)** Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. **Install** dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Create** a `.env` file based on `.env.example`.  
5. **Run** the app:
   ```bash
   streamlit run app.py
   ```
---
## 📁 Project Structure
```
ai-social-agent/
├── app.py
├── requirements.txt
├── .env.example
├── link_discovery.py
├── social_agents/
│   ├── content_strategist.py
│   ├── linkedin_agent.py
│   ├── twitter_agent.py
│   ├── instagram_agent.py
│   └── facebook_agent.py
├── airtable_logger.py
└── README.md
```
---
## 🔧 Environment Variables
Use the `.env` file or Replit Secrets to define:
```dotenv
OPENAI_API_KEY=sk-...
AIRTABLE_PAT=pat...
AIRTABLE_BASE_ID=app...
AIRTABLE_TABLE_NAME=SocialMediaPosts
NEWSAPI_KEY=...  # If using link discovery feature
```
- **OPENAI_API_KEY**: Your OpenAI credential.  
- **AIRTABLE_* variables**: For logging (optional).
- **NEWSAPI_KEY**: For link discovery (optional).
---
## 🧩 Dependencies
Update your `requirements.txt` to avoid dependency conflicts:
```
openai==0.27.0
streamlit>=1.20.0
python-dotenv
pyairtable
requests
```
---
## 🎨 UI/UX Notes
- **Sidebar**: Enter prompt, select platforms, click **Generate**.  
- **Main Panel**: Displays each platform's post in a colored box.  
- **Celebrations**: Balloons + confetti on generation.  
- **Health Check**: GET `/` returns `OK`.
---
## 📦 Airtable Setup (Optional)
1. Create a base with a table named **SocialMediaPosts**.  
2. Add columns:
   - **Prompt** (Long text)  
   - **Platform** (Single line)  
   - **Generated Content** (Long text)  
3. Ensure your PAT has write access.
---
## 🐞 Troubleshooting
- **Dependency conflicts**: If you encounter protobuf conflicts between opentelemetry and streamlit, use the requirements.txt provided above with `crewai<0.119.0` and `streamlit==1.34.0`.
- **Installation issues on Replit**: Use `--break-system-packages` when installing via pip.
- **Airtable 422/403**: Verify table schema and PAT permissions.  
- **Port in use**: Health check server runs on port 5000; ensure it's free.
- **Empty links/images**: If using NewsAPI integration, verify your API key and limits.
---

Happy building! 🎉
