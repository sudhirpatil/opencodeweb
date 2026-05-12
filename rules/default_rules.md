# PySpark Code Review Rules

## Rule 1: Avoid .collect() on Large DataFrames
Never use `.collect()` on DataFrames that may be large. It pulls all data to the driver and causes OOM errors.
Instead use `.show(n)`, `.take(n)`, `.first()`, or aggregate first then collect.

## Rule 2: Broadcast Small DataFrames in Joins
When joining a large DataFrame with a small one (under ~100MB), wrap the small one with `broadcast()`.
Example: `df_large.join(broadcast(df_small), "key")` instead of `df_large.join(df_small, "key")`.

## Rule 3: Avoid Python UDFs When Possible
Native Python UDFs serialize data row-by-row through the Python interpreter, killing performance.
Prefer Spark SQL built-in functions (`pyspark.sql.functions`). If a UDF is unavoidable, use Pandas UDFs (`@pandas_udf`) which are vectorized.

## Rule 4: Filter Early (Predicate Pushdown)
Apply `.filter()` or `.where()` as early as possible in the pipeline, especially on partition columns (`date`, `region`, `country`). This enables partition pruning and reduces shuffle.

## Rule 5: Explicit Schema Definition
Avoid schema inference (`inferSchema=True`) on large datasets — it requires a full scan.
Define schemas explicitly using `StructType` and `StructField`.

## Rule 6: Avoid repartition() When coalesce() Suffices
`repartition(n)` causes a full shuffle. If you only need to reduce partition count, use `coalesce(n)` which avoids unnecessary data movement.

## Rule 7: Cache Only When Data Is Reused
Calling `.cache()` or `.persist()` on a DataFrame that is only used once wastes memory.
Only cache DataFrames that are accessed multiple times in the same job.

## Rule 8: Use spark.sql.shuffle.partitions Appropriately
The default shuffle partition count is 200. For small datasets this causes tiny partitions and overhead; for large datasets it may cause spill. Set `spark.conf.set("spark.sql.shuffle.partitions", n)` based on data volume.
