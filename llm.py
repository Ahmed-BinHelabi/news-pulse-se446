import requests
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_summary(words):

    keywords = ", ".join(words[:15])

    fallback = f"Trending topics include: {keywords}"

    if not OPENAI_API_KEY:
        return fallback

    try:
        prompt = f"""
        Summarize these news keywords in ONE paragraph under 80 words.
        Mention at least 3 storylines.

        Keywords:
        {keywords}
        """

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 120
            }
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception:
        return fallback