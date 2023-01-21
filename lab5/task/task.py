from pyspark.sql import SparkSession
import pyspark.sql.functions as func


MONGO_DB = "mongodb://router01:27017/?authSource=admin"
COLLECTION = "london.taxi_rides"


def extract_df(spark):
    df = (
        spark.read.format("mongodb")
        .option(
            "spark.mongodb.read.connection.uri",
            MONGO_DB,
        )
        .option("spark.mongodb.read.database", COLLECTION.split(".")[0])
        .option("spark.mongodb.read.collection", COLLECTION.split(".")[1])
        .load()
    )
    return df


def aggregate(df):
    result = (
        df.groupBy('driver_id')
        .agg(func.avg('client_review.rating').alias('avg_rating'))
        .where(func.col('avg_rating') <= 3.5)
    )
    return result


def main():
    spark = SparkSession.builder.appName("highload-lab5").getOrCreate()

    df = extract_df(spark)
    data = aggregate(df)
    data.show(10)

    spark.stop()


if __name__ == "__main__":
    main()
