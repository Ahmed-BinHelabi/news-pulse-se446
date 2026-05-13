import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="News Pulse", layout="wide")
st.title("📰 News Pulse — Live")

def load_agg():
    if os.path.exists("aggregations.json"):
        try:
            with open("aggregations.json") as f:
                return json.load(f)
        except:
            return {}
    return {}

agg = load_agg()
by_src = agg.get("by_source", {})
by_win = agg.get("by_window", {})
top_w = agg.get("top_words", {})

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 By Source")
    if by_src:
        df = pd.DataFrame(list(by_src.items()), columns=["source", "count"])
        st.bar_chart(df.set_index("source"))
    else:
        st.info("Loading...")

with col2:
    st.subheader("📈 By Hour")
    if by_win:
        df = pd.DataFrame(list(by_win.items()), columns=["hour", "count"])
        st.line_chart(df.set_index("hour"))
    else:
        st.info("Loading...")

st.subheader("🔤 Top Keywords")
if top_w:
    df = pd.DataFrame(list(top_w.items()), columns=["word", "count"])
    st.dataframe(df.head(10))
else:
    st.info("Loading...")

st.divider()
st.subheader("✨ AI Summary")

def get_summary(top_w):
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or not top_w:
        return None
    
    keywords_str = ", ".join([w[0] for w in sorted(top_w.items(), key=lambda x: x[1], reverse=True)[:15]])
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            messages=[{"role": "user", "content": f"News keywords: {keywords_str}\n\nWrite ONE paragraph (max 80 words) on main topics. Must mention 3+ storylines. Factual and concise."}]
        )
        return msg.content[0].text
    except:
        return f"Keywords: {keywords_str}"

if top_w:
    summary = get_summary(top_w)
    if summary:
        st.markdown(summary)
else:
    st.info("Waiting for keywords...")

st.button("🔄 Refresh")