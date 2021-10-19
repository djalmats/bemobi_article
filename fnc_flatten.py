from pyspark.sql import functions as F
from pyspark.sql import types as T

def flatten(schema, prefix=None):
    for field in schema.fields:
        if prefix is None:
            colName = field.name
        else:
            colName = prefix + "." + field.name
        if isinstance(field.dataType,T.StructType):
            yield from flatten(field.dataType, colName)
        else:
            yield F.col(colName).alias(colName.lower().split('.')[1]).cast('string')
            
df = spark.read.json('path')
df = df.select(list(flatten(df.schema)))
