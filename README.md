# AI Social Media Content Generator (Legacy OpenAI SDK v0.27.0)

This version pins the OpenAI SDK to v0.27.0 to keep using `openai.ChatCompletion.create()` without TypeIs conflicts.

## Setup

1. In Replit shell:
   ```bash
   pip install openai==0.27.0 --break-system-packages
   pip install -r requirements.txt --break-system-packages
   ```

2. Create `.env` from `.env.example`

3. Click **Run**

## Local

```bash
pip install openai==0.27.0
pip install -r requirements.txt
streamlit run app.py
```
