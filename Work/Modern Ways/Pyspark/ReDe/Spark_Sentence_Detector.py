from pyspark.ml import PipelineModel
from sparknlp.annotator import *
from sparknlp.base import *
import sparknlp
from pyspark.ml import Pipeline
import pandas as pd
pd.set_option("display.max_colwidth", 0)

from pyspark.sql import SparkSession

builder = SparkSession.builder\
        .appName("Spark NLP Licensed")\
        .master("local[*]")\
        .config("spark.driver.memory", "124G")\
        .config("spark.driver.maxResultSize", "2048GB")\
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
        .config("spark.kryoserializer.buffer.max", "2000M")\
        .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:3.3.2")

spark = builder.getOrCreate()

df = spark.read.text('tr6.txt').toDF('text')

df.rdd.getNumPartitions()

df = df.repartition(200)

documenter = DocumentAssembler()\
    .setInputCol("text")\
    .setOutputCol("document")
    
sentencerDL = SentenceDetectorDLModel\
    .pretrained("sentence_detector_dl", "xx") \
    .setInputCols(["document"]) \
    .setOutputCol("sentences")

model = PipelineModel(stages=[documenter, sentencerDL])

result = model.transform(df)

pd_res = result.select("sentences.result").toPandas()

pd_res.to_csv("Spark_Sentence_Tokenize6.csv", index=False)