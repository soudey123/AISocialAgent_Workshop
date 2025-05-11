import os
import openai

class FacebookAgent:
    def __init__(self, model="gpt-4o"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    def run(self, brief):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"system","content":"You write Facebook posts."},
                      {"role":"user","content":f"Create a Facebook post from this brief: {brief}"}],
        )
        return response.choices[0].message.content.strip()
