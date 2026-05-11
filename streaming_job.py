from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("NewsPulse")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("source", StringType(), True),
    StructField("title", StringType(), True),
    StructField("url", StringType(), True),
    StructField("ts", TimestampType(), True)
])

stream = (
    spark.readStream
    .schema(schema)
    .json("data/incoming")
)

# -----------------------------------
# 1. By Source
# -----------------------------------

by_source = (
    stream.groupBy("source")
    .count()
)

q1 = (
    by_source.writeStream
    .outputMode("complete")
    .format("memory")
    .queryName("by_source")
    .start()
)

# -----------------------------------
# 2. By Window
# -----------------------------------

by_window = (
    stream
    .withWatermark("ts", "2 hours")
    .groupBy(F.window("ts", "1 hour"))
    .count()
)

q2 = (
    by_window.writeStream
    .outputMode("complete")
    .format("memory")
    .queryName("by_window")
    .start()
)

# -----------------------------------
# 3. Top Words
# -----------------------------------

words = (
    stream
    .select(
        F.explode(
            F.split(
                F.lower(F.col("title")),
                "\\W+"
            )
        ).alias("word")
    )
)

stop_words = [
    "the", "a", "an", "to", "of", "in",
    "on", "for", "and", "with", "is",
    "at", "by", "from"
]

top_words = (
    words
    .filter(~F.col("word").isin(stop_words))
    .filter(F.length("word") > 3)
    .groupBy("word")
    .count()
    .orderBy(F.desc("count"))
)

q3 = (
    top_words.writeStream
    .outputMode("complete")
    .format("memory")
    .queryName("top_words")
    .start()
)

print("Streaming started...")

spark.streams.awaitAnyTermination()