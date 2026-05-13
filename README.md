# News Pulse — Big Data Challenge SE446

Real-time news aggregation pipeline: RSS feeds → Python ingester → Streaming aggregation → Streamlit dashboard.

## System Architecture

**Three-Process Pipeline:**
1. **Ingester** (`ingester.py`) - Pulls from 4 RSS feeds every 60s, writes JSON-lines to `data/incoming/`
2. **Streaming Job** (`streaming_job.py`) - Processes batches, aggregates by source/hour/keywords
3. **Dashboard** (`app.py`) - Streamlit dashboard showing live charts + AI summary

## Dashboard Features

- 📊 **Bar Chart**: Headlines by source (BBC, Reuters, CNN, TechCrunch)
- 📈 **Line Chart**: Volume trends by hour
- 🔤 **Keywords Table**: Top 10 keywords with counts
- ✨ **AI Summary**: LLM-generated insight from keywords

## Files

- `ingester.py` - RSS feed puller (feedparser, 4 sources)
- `streaming_job.py` - File watcher + aggregations (Python, no Spark)
- `app.py` - Streamlit dashboard
- `reflection.txt` - Scaling analysis (max 100 words)
- `aggregations.json` - In-memory state (by_source, by_window, top_words)

## Running

**Terminal 1 - Ingester:**
```bash
python ingester.py
```

**Terminal 2 - Streaming Job:**
```bash
python streaming_job.py
```

**Terminal 3 - Dashboard:**
```bash
$env:ANTHROPIC_API_KEY = "sk-ant-..."
streamlit run app.py
```

Open browser: `http://localhost:8501`

## Key Decisions

- **Python-based streaming** instead of Spark (faster development, no Windows Hadoop issues)
- **Defensive API calls** - falls back to keyword display if LLM fails
- **File-based state** (aggregations.json) - simple, observable, debuggable

## Reflection

See `reflection.txt` for scaling analysis (identifies LLM as bottleneck at 1000× volume).

---

**Team:** Zakariya Ba Alawi  ---  Ahmed Bin Halabi | **Date:** May 13, 2026 | **University:** Alfaisal SE446