import streamlit as st
from pyspark.sql import SparkSession
from llm import generate_summary

spark = (
    SparkSession.builder
    .appName("NewsPulseDashboard")
    .getOrCreate()
)

st.title("News Pulse Live Dashboard")

# ----------------------------
# Source chart
# ----------------------------

src_df = spark.sql("""
SELECT * FROM by_source
""").toPandas()

st.subheader("Headlines by Source")
st.bar_chart(src_df.set_index("source"))

# ----------------------------
# Window chart
# ----------------------------

window_df = spark.sql("""
SELECT window.start as time, count
FROM by_window
ORDER BY time
""").toPandas()

st.subheader("Headline Volume Over Time")
st.line_chart(window_df.set_index("time"))

# ----------------------------
# Top words
# ----------------------------

words_df = spark.sql("""
SELECT * FROM top_words
LIMIT 10
""").toPandas()

st.subheader("Top Keywords")
st.table(words_df)

# ----------------------------
# LLM Summary
# ----------------------------

keywords = words_df["word"].tolist()

summary = generate_summary(keywords)

st.subheader("AI News Summary")
st.write(summary)