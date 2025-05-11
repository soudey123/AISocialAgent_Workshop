import os
import openai


class ContentStrategistAgent:

    def __init__(self, model="gpt-4o"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    def run(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{
                "role":
                "system",
                "content":
                "Analyze and reframe prompts into structured content briefs."
            }, {
                "role": "user",
                "content": prompt
            }],
        )
        return response.choices[0].message.content.strip()
