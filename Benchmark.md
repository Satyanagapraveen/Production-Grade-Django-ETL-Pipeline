# ETL Pipeline Benchmark Results

## 1. Memory Usage Analysis
* **Naive Approach Peak Memory:** 492.0 MiB
* **Optimized Approach (iterator, batch=1000) Peak Memory:** ~5.0 MiB

**Analysis:**
The naive approach attempted to load all 500,000 JSON documents into Python memory simultaneously via the default QuerySet evaluation. This consumed nearly 500 MiB of RAM just for data serialization, which would trigger Out-Of-Memory (OOM) kills on standard restricted containers. The optimized approach utilizes `iterator(chunk_size=1000)`, which acts as a server-side cursor. This keeps the application's memory footprint incredibly low and completely flat, regardless of how large the PostgreSQL table grows, because only 1,000 objects exist in RAM at any given millisecond.

## 2. Execution Time vs. Batch Size
| Batch Size | Total Migration Time (seconds) | Throughput (records/sec) |
|------------|--------------------------------|--------------------------|
| 100        | 113.99                         | 4386.43                  |
| 500        | 71.85                          | 6958.58                  |
| 1000       | 57.41                          | 8708.84                  |
| 5000       | 77.72                          | 6433.66                  |

**Analysis:**
The data demonstrates a clear U-curve for database transaction efficiency. A batch size of 100 is network-bound; the pipeline spends too much time waiting for PostgreSQL acknowledgments. A batch size of 5000 is CPU-bound; the time saved on network trips is lost while Python constructs a massive multi-megabyte SQL `INSERT` string and PostgreSQL parses it. The batch size of 1000 provides the optimal balance, maximizing our throughput to over 8,700 records per second.

## 3. Database Query Count (per 1000 Records)
* **Naive `.create()` Loop:** 3,000 queries
* **Optimized `bulk_create()`:** 4 queries

**Analysis:**
If we processed 1,000 legacy records using a standard `.save()` loop, we would trigger exactly 1,000 `INSERT` queries for Orders, 1,000 `INSERT` queries for OrderLines, and 1,000 `UPDATE` queries for the migrated flags. That equals 3,000 individual network round-trips to the database. By utilizing `bulk_create()`, we consolidated this into exactly 4 queries: 1 `INSERT` for all Orders, 1 `SELECT` to fetch the new primary keys, 1 `INSERT` for all OrderLines, and 1 `UPDATE` for the flags. This 99.8% reduction in query volume is the primary driver of the pipeline's speed.