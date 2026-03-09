from pyspark.sql import SparkSession
import plotly.express as px
import os

spark = (
    SparkSession.builder.appName("sample")
    .config("spark.sql.catalogImplementation", "hive")
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("use prod_db")
customer_df = spark.sql(
    "select * from prod_db.customer_outreach_metrics order by avg_order_value desc limit 10"
).toPandas()

# Plot the top 10 exchanges' volumeUSD
fig = px.bar(
    customer_df,
    x="customer_name",
    y="avg_order_value",
    title="Top 10 customers by average order value",
)

# Save as HTML file
fig.write_html("/home/airflow/tpch_analytics/dashboard_plot.html")
print("Plot saved to dashboard_plot.html")
