import os
import json
import time
import feedparser
from datetime import datetime

INCOMING = "data/incoming"

os.makedirs(INCOMING, exist_ok=True)

FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
}

def pull_once(tick):
    rows = []

    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:
                rows.append({
                    "source": source,
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "ts": datetime.utcnow().isoformat()
                })

        except Exception as e:
            print(f"Failed feed {source}: {e}")

    path = os.path.join(INCOMING, f"batch_{tick}.json")

    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    print(f"Wrote {len(rows)} records")

if __name__ == "__main__":
    tick = 0

    while True:
        pull_once(tick)
        tick += 1
        time.sleep(60)