import os
import openai


class TwitterAgent:

    def __init__(self, model="gpt-4o"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    def run(self, brief):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "You write concise Twitter posts (max 280)."
            }, {
                "role": "user",
                "content": f"Create a tweet from this brief: {brief}"
            }],
        )
        return response.choices[0].message.content.strip()
