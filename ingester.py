import os
import json
import time
from datetime import datetime
import feedparser

INCOMING = "data/incoming"
os.makedirs(INCOMING, exist_ok=True)

FEEDS = {
    "BBC": "http://feeds.bbc.co.uk/news/rss.xml",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "TechCrunch": "http://feeds.techcrunch.com/feed/"
}

def pull_once(tick):
    rows = []
    
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            
            if feed.bozo:
                print(f"[WARNING] {source} feed parse issue, continuing...")
            
            for entry in feed.entries[:10]:
                record = {
                    "source": source,
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "ts": datetime.utcnow().isoformat()
                }
                rows.append(record)
        
        except Exception as e:
            print(f"[ERROR] Failed to fetch {source}: {e}")
            continue
    
    path = os.path.join(INCOMING, f"batch_{tick}.json")
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Wrote {len(rows)} records to {path}")

if __name__ == "__main__":
    tick = 0
    while True:
        try:
            pull_once(tick)
            tick += 1
            time.sleep(60)
        except KeyboardInterrupt:
            print("\n[STOP] Ingester stopped.")
            break
        except Exception as e:
            print(f"[FATAL] {e}, retrying in 5s...")
            time.sleep(5)