import json
import os
import time
from collections import defaultdict
from datetime import datetime
import re

by_source_data = defaultdict(int)
by_window_data = defaultdict(int)
top_words_data = defaultdict(int)

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "am", "be", "been",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "as", "it",
    "that", "this", "these", "those", "was", "were", "be", "has", "have",
    "had", "do", "does", "did", "will", "would", "should", "could", "may",
    "might", "can", "about", "into", "through", "during", "before", "after",
    "above", "below", "up", "down", "out", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "each", "every", "both", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "just", "s", "t", "can", "now", "said", "says", "say"
}

processed_files = set()

def process_batch(file_path):
    global by_source_data, by_window_data, top_words_data
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                source = record.get("source", "")
                title = record.get("title", "").lower()
                ts_str = record.get("ts", "")
                by_source_data[source] += 1
                if ts_str:
                    ts = datetime.fromisoformat(ts_str)
                    hour_key = ts.strftime("%Y-%m-%d %H:00:00")
                    by_window_data[hour_key] += 1
                words = re.findall(r'\b[a-z]+\b', title)
                for word in words:
                    if len(word) > 2 and word not in STOP_WORDS:
                        top_words_data[word] += 1
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed {file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to process {file_path}: {e}")

def save_aggregations():
    global by_source_data, by_window_data, top_words_data
    agg = {
        "by_source": dict(by_source_data),
        "by_window": dict(by_window_data),
        "top_words": dict(sorted(top_words_data.items(), key=lambda x: x[1], reverse=True)[:10])
    }
    with open("aggregations.json", 'w') as f:
        json.dump(agg, f)

def watch_and_process():
    global processed_files
    incoming_dir = "data/incoming"
    print("[STREAMING] Watching data/incoming/")
    print("[STREAMING] Query 1: by_source aggregating")
    print("[STREAMING] Query 2: by_window aggregating")
    print("[STREAMING] Query 3: top_words aggregating")
    print("[STREAMING] All queries active. Waiting for data...")
    last_save = time.time()
    while True:
        try:
            if os.path.exists(incoming_dir):
                files = sorted([f for f in os.listdir(incoming_dir) if f.endswith('.json')])
                for file in files:
                    file_path = os.path.join(incoming_dir, file)
                    if file not in processed_files:
                        process_batch(file_path)
                        processed_files.add(file)
            if time.time() - last_save > 5:
                save_aggregations()
                last_save = time.time()
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[STOP] Streaming stopped.")
            save_aggregations()
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(5)

if __name__ == "__main__":
    watch_and_process()