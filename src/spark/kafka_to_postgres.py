from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
import os

# --- Configuration ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKERS", "kafka:29092")
KAFKA_TOPIC = "raw_stream"
POSTGRES_URL = "jdbc:postgresql://postgres:5432/dwh_prod"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
CHECKPOINT_LOCATION = "/tmp/spark_checkpoints/kafka_to_postgres"

# --- Schema Definition ---
# Designing a generic schema for sales/events
schema = StructType([
    StructField("id", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("amount", DoubleType(), True),
    StructField("status", StringType(), True),
    StructField("timestamp", TimestampType(), True)
])

def main():
    spark = SparkSession.builder \
        .appName("KafkaToPostgres") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.6.0") \
        .getOrCreate()

    # 1. Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()

    # 2. Parse JSON payload
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # 3. Write to PostgreSQL
    def write_to_postgres(batch_df, batch_id):
        batch_df.write \
            .format("jdbc") \
            .option("url", POSTGRES_URL) \
            .option("dbtable", "public.landing_events") \
            .option("user", POSTGRES_USER) \
            .option("password", POSTGRES_PASSWORD) \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()

    query = parsed_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .option("checkpointLocation", CHECKPOINT_LOCATION) \
        .trigger(availableNow=True) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
