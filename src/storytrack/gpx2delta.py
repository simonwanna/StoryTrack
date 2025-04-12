import os

import gpxpy
import pandas as pd
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql import types as T


# Output schema for each GPX point record.
point_schema = T.StructType(
    [
        T.StructField("run_id", T.StringType(), True),
        T.StructField("latitude", T.DoubleType(), True),
        T.StructField("longitude", T.DoubleType(), True),
        T.StructField("elevation", T.DoubleType(), True),
        T.StructField("time", T.TimestampType(), True),
        T.StructField("speed", T.DoubleType(), True)
    ]
)


def parse_gpx_pd(pdf_iter):
    for pdf in pdf_iter:
        all_records = []
        for run_id, path in zip(pdf["run_id"], pdf["path"]):
            with open(path, "r") as f:
                gpx_file = gpxpy.parse(f)
            for track in gpx_file.tracks:
                for segment in track.segments:
                    for i, point in enumerate(segment.points):
                        speed = point.speed
                        if speed is None and i > 0:
                            speed = segment.points[i - 1].speed_between(point)

                        # convert from m/s to km/h;
                        if speed is not None:
                            speed = speed * 3.6
                        else:
                            speed = 0.0
                        
                        all_records.append(
                            {
                                "run_id": run_id,
                                "latitude": point.latitude,
                                "longitude": point.longitude,
                                "elevation": point.elevation,
                                "time": point.time,
                                "speed": speed
                            }
                        )
        yield pd.DataFrame(all_records)


if __name__ == '__main__':
    # SparkSession with Delta support
    builder = (
        SparkSession.builder.appName("GPX Processing with Pandas UDF")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    gpx_files = os.listdir("gpx_files")
    file_paths = []
    for f in gpx_files:
        if f.endswith(".gpx"):
            file_paths.append((f.split(".")[0], os.path.join("gpx_files", f)))
    
    # if you want only specific files
    # file_paths = [
    #     ("run_04_07_24", "gpx_files/run_04_07_24.gpx"),
    #     ("run_21_06_24", "gpx_files/run_21_06_24.gpx")
    # ]

    df_paths = spark.createDataFrame(file_paths, ["run_id", "path"])
    print(df_paths.show(truncate=False))

    # Parallelise the GPX parsing row-wise
    df_points = df_paths.mapInPandas(parse_gpx_pd, schema=point_schema)

    # Save to delta
    df_points.write.format("delta").mode("overwrite").save("tmp/gpx_points")

    print("\033[92m" + "GPX points written to Delta table." + "\033[0m")    
    spark.stop()