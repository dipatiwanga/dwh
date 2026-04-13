#!/bin/bash

# Define constants
KAFKA_CONTAINER="dwh_kafka"
TOPICS=("raw_stream" "users_events" "orders_stream")

# Function to create topic
create_topic() {
  local topic_name=$1
  echo "Creating topic: $topic_name..."
  docker exec $KAFKA_CONTAINER kafka-topics --create --topic "$topic_name" --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1 --if-not-exists
}

# Iterate and create
for topic in "${TOPICS[@]}"; do
  create_topic "$topic"
done

echo "Kafka topics setup complete."
