import os
import requests

# Simple link discovery using NewsAPI
API_KEY = os.getenv("NEWSAPI_KEY")
ENDPOINT = "https://newsapi.org/v2/everything"


def discover_links(topic, max_links=3):
    """
    Fetches top news articles for a given topic using NewsAPI.
    Returns a list of dicts containing 'title', 'url', and 'urlToImage'.
    """
    if not API_KEY:
        raise ValueError("Missing NEWSAPI_KEY in environment variables.")
    params = {
        "q": topic,
        "apiKey": API_KEY,
        "pageSize": max_links,
        "sortBy": "relevancy",
    }
    resp = requests.get(ENDPOINT, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json().get("articles", [])
    articles = []
    for a in data:
        articles.append({
            "title": a.get("title") or a.get("url"),
            "url": a.get("url"),
            "urlToImage": a.get("urlToImage"),
        })
    return articles
