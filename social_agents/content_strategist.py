import os
import openai
from link_discovery import discover_links


class ContentStrategistAgent:

    def __init__(self, model: str = "gpt-4o"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    def extract_topic(self, prompt: str, max_words: int = 5) -> str:
        """
        Extracts a concise topic from the user's prompt.
        """
        words = prompt.strip().split()
        # Use at most max_words words for the search query
        return " ".join(words[:max_words])

    def run(self, prompt: str):
        """
        Generates a strategy brief that includes auto-discovered links & images.
        Uses only the key topic words for news discovery, not the full prompt.
        """
        # Step 1: Extract a concise topic for link discovery
        topic = self.extract_topic(prompt)

        # Step 2: Discover related articles based on the extracted topic
        try:
            articles = discover_links(topic)
        except Exception:
            articles = []

        # Build a simple brief string including resource URLs
        brief = prompt
        for a in articles:
            title = a.get("title", "")
            url = a.get("url", "")
            if url:
                brief += f"\n\nResource: {title} – {url}"

        # Step 3: Call the LLM with the enriched prompt
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role":
                    "system",
                    "content":
                    "You are a helpful content strategist. You will generate a brief for a social media post based on the user's input. You will also include relevant resources."
                },
                {
                    "role": "user",
                    "content": brief
                },
            ],
        )
        return response.choices[0].message.content.strip(), articles
