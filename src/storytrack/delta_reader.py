from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def load_data(file, path="tmp/gpx_points"):
    # Initialize SparkSession
    builder = (
        SparkSession.builder.appName("GPX Processing with Pandas UDF")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    # Read from delta and filter for a specific run
    df_read = spark.read.format("delta").load(path)
    df_filtered = df_read.filter(df_read.run_id == file)

    # Need to convert from spark to pandas before stopping the Spark session
    pandas_df = df_filtered.toPandas()
    spark.stop()

    return pandas_df
