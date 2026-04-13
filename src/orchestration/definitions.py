from dagster import Definitions, asset, AssetExecutionContext
import subprocess
import os

@asset(group_name="ingestion")
def airbyte_sync():
    """Trigger Airbyte Sync (Placeholder for E2E logic)"""
    # In a real scenario, use dagster-airbyte resource
    return "Airbyte sync complete"

@asset(deps=[airbyte_sync], group_name="processing")
def spark_kafka_to_postgres(context: AssetExecutionContext):
    """Run PySpark job to consume Kafka data into Postgres"""
    spark_script = "/opt/dagster/app/../spark/kafka_to_postgres.py"
    # Note: This is an example of trigger logic. 
    # In production, use SparkSubmitOperator or a dedicated Spark resource.
    context.log.info(f"Triggering Spark job: {spark_script}")
    # Logic to run spark-submit would go here
    return "Spark processing complete"

@asset(deps=[spark_kafka_to_postgres], group_name="transformation")
def dbt_run(context: AssetExecutionContext):
    """Run dbt transformations"""
    dbt_dir = "/opt/dagster/app/../dbt"
    context.log.info(f"Running dbt from: {dbt_dir}")
    # Logic to run 'dbt run' would go here
    return "dbt transformation complete"

defs = Definitions(
    assets=[airbyte_sync, spark_kafka_to_postgres, dbt_run],
)
