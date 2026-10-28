---
layout: simple
title: "pandas vs Polars vs Dask"
permalink: /pattern/pandas-polars-dask
---

# pandas vs Polars vs Dask — In-Depth Comparison (2025)

**Versions:** pandas 3.0 · Polars 2.1 · Dask 2025.4

Choosing between the three is not about which is "best" — it is about matching the tool to the data size, machine scope, and ecosystem constraints of your problem.

---

## Quick Decision Matrix

```
Data size     Machine scope    Pandas compat needed?    → Pick
──────────────────────────────────────────────────────────────
< 1 GB        single           yes                      pandas 3.0
1–50 GB       single           no                       Polars (lazy + streaming)
1–50 GB       single           yes                      Dask (local threads)
> 50 GB       single           no                       Polars streaming / DuckDB
> 50 GB       cluster          either                   Dask distributed
Any size      single           SQL-first                DuckDB
GPU workload  single/cluster   either                   RAPIDS cuDF / dask-cudf
```

---

## 1. Architecture & Execution Model

| | pandas | Polars | Dask |
|---|---|---|---|
| **Execution** | Eager only | Eager (`DataFrame`) + Lazy (`LazyFrame`) | Lazy only (`.compute()` triggers) |
| **Parallelism** | Single-threaded (GIL-bound) | Multi-threaded (Rust work-stealing pool) | Multi-threaded local or distributed cluster |
| **Query optimizer** | None | Full IR optimizer (predicate pushdown, join reordering, CSE, cardinality-aware) | dask-expr: projection + predicate pushdown, task fusion — no cost-based |
| **Streaming / OOC** | No | Yes — chunked streaming engine, spills to disk at 80% RAM | Partition-based; each partition must fit in RAM |
| **Distributed** | No | Experimental `RemoteEngine` (Polars 2.0) | Yes — `dask.distributed` with scheduler + workers |
| **Core language** | Python + NumPy (C extensions) | Rust (SIMD-optimized) | Python orchestration + pandas per partition |

**Mental model:**

```
pandas:  [data in RAM] → execute now → result

Polars:  [build expression tree]
           → optimizer rewrites (predicate pushdown, join reorder, CSE)
           → execute (in-memory or streaming chunks)

Dask:    [build task DAG]
           → dask-expr rewrites (projection/predicate pushdown, task fusion)
           → scheduler executes DAG on workers
```

The key architectural difference: Polars' optimizer is a **relational query planner** (like a SQL engine). Dask's optimizer works at the task-graph level — shallower, no cost-based decisions.

---

## 2. Memory Model

### pandas 3.0
- NumPy arrays per column; Python objects for mixed/string types (28+ bytes each)
- **Copy-on-Write is now default** — views share a buffer; copy only on first write. Eliminates `SettingWithCopyWarning`
- `str` dtype backed by PyArrow if installed, otherwise NumPy `object`
- `dtype_backend="pyarrow"` opts into fully Arrow-backed columns
- Hard limit: **entire DataFrame must fit in RAM**

### Polars
- **Native Apache Arrow** columnar format throughout — no NumPy
- `Series` are `ChunkedArray`; `rechunk()` called automatically when contiguity is needed
- **Zero-copy interop** with PyArrow, DuckDB, Arrow-backed pandas via C Data Interface
- **No row index** — intentional; eliminates alignment bugs and index memory overhead
- **OOC spilling default since Polars 2.0:** at 80% RAM usage, data spills to disk. Polars 2.1 added compression and prefetching for spilled chunks

### Dask
- Each partition is a **pandas DataFrame** — inherits all pandas memory characteristics
- No global in-memory data structure; data lives across worker processes/threads
- **128 MB per partition** is the conventional target
  - Too small → scheduler overhead dominates
  - Too large → OOM risk
- Spilling to disk requires `dask.distributed` with memory limits configured on workers

---

## 3. Performance Benchmarks

### TPC-H PDS-H (AWS c7a.24xlarge — 96 vCPUs / 192 GB RAM, 22 queries)

| | SF-10 (~10 GB) | SF-100 (~100 GB) |
|---|---|---|
| **Polars streaming** | **3.89 s** | **23.94 s** |
| Polars in-memory | 9.68 s | 152.27 s |
| DuckDB | ~3 s | ~19.5 s |
| **Dask** | 46.02 s | 548.52 s |
| **pandas** | 365.71 s | OOM |

**Speedup ratios at SF-10:**
- Polars streaming is **~12× faster than Dask**
- Polars streaming is **~94× faster than pandas**
- Dask is **~8× faster than pandas** (parallelism across partitions)

### Why the gaps exist

```
pandas → Polars (~94×):
  Single-threaded + NumPy  vs  SIMD + 96-core work-stealing.
  On a 96-core machine, theoretical max is ~96× — benchmark shows ~94×
  (I/O bottleneck dominates at streaming level).

Dask → Polars (~12×):
  Python task scheduling overhead (~1–5 ms per task).
  Each partition runs single-threaded pandas internally.
  At SF-10: scheduling overhead dominates, not the compute itself.

pandas → Dask (~8×):
  Dask wins by parallelising across partitions.
  But each partition still runs single-threaded pandas — no SIMD.
```

---

## 4. API Comparison

### Filter

```python
# pandas
df[df["age"] > 30]
df.query("age > 30")

# Polars eager
df.filter(pl.col("age") > 30)

# Polars lazy — pushed into file scan by optimizer
lf.filter(pl.col("age") > 30)

# Dask (lazy, mirrors pandas)
ddf[ddf["age"] > 30]
```

### GroupBy + Aggregation

```python
# pandas
df.groupby("dept").agg(mean_sal=("salary", "mean"), max_sal=("salary", "max"))

# Polars — expressions are first-class, composable, type-safe
df.group_by("dept").agg([
    pl.col("salary").mean().alias("mean_sal"),
    pl.col("salary").max().alias("max_sal"),
])

# Dask (lazy, pandas-like)
ddf.groupby("dept")["salary"].mean().compute()
```

### Join

```python
# pandas
pd.merge(left, right, on="id", how="left")

# Polars — also has join_where() for non-equi joins
left.join(right, on="id", how="left")

# Dask — large-large joins trigger a full shuffle (expensive)
dd.merge(left_ddf, right_ddf, on="id", how="left")
```

### Apply / UDF

```python
# pandas — row-wise, slow (Python loop)
df.apply(lambda row: f(row["a"], row["b"]), axis=1)

# Polars — avoid map_elements; use native expressions instead
# BAD (breaks SIMD/parallelism):
df.with_columns(
    pl.struct(["a","b"]).map_elements(lambda r: r["a"] + r["b"], return_dtype=pl.Int64)
)
# GOOD (native expression — optimizer can parallelize):
df.with_columns((pl.col("a") + pl.col("b")).alias("c"))

# Dask — map_partitions applies any pandas function across partitions
ddf.map_partitions(lambda df: df.assign(c=df["a"] + df["b"]))
```

### Window Functions

```python
# pandas
df["rank"] = df.groupby("dept")["salary"].rank(method="dense")

# Polars — .over() is cleaner; no groupby object needed
df.with_columns(
    pl.col("salary").rank("dense").over("dept").alias("rank")
)

# Dask — not directly supported; requires map_partitions + careful partitioning
```

---

## 5. Lazy Evaluation Deep-Dive

### Polars `LazyFrame` — relational query planner

```python
lf = pl.scan_csv("data.csv")       # no I/O yet

result = (
    lf
    .filter(pl.col("age") > 30)    # pushed into scan: only matching rows read
    .select(["name","age","dept","salary"])  # only these columns read from disk
    .group_by("dept")
    .agg(pl.col("salary").mean())
    .sort("salary", descending=True)
)

print(result.explain())            # print the optimized logical plan
result.collect()                   # execution starts here (in-memory)
result.collect(streaming=True)     # chunked execution if data > memory budget
```

**Optimizer passes (applied in order):**

| Pass | What it does |
|---|---|
| Predicate pushdown | Moves `filter` to scan time — CSV/Parquet only reads matching rows |
| Projection pushdown | Only reads columns that are referenced downstream |
| Join reordering | Cost-based swap of join sides using cardinality estimates (Polars 2.0+) |
| Common subexpression elimination (CSE) | Deduplicates repeated sub-expressions in the plan |
| Streaming plan selection | Auto-switches to chunked execution if memory budget would be exceeded |

### Dask task graph — task-level DAG

```python
ddf = dd.read_csv("data-*.csv")          # lazy; one graph node per file glob match
result = ddf[ddf["age"] > 30].groupby("dept")["salary"].mean()

result.visualize()                        # render the DAG as a PNG (requires graphviz)
result.compute()                          # scheduler executes the full DAG
```

`dask-expr` (default since 2024) adds an expression tree *above* the task graph enabling:
- Projection and predicate pushdown for Parquet
- Adjacent-map task fusion

**What it does NOT do:** join reordering, cardinality estimation, cost-based planning.

Since Dask 2025.4.0, graph optimization runs **on the distributed scheduler** for multi-collection queries, reducing client-side serialization overhead.

---

## 6. Dask Schedulers

### Local schedulers

| Scheduler | Best for |
|---|---|
| `synchronous` | Debugging — serial execution, full Python stack traces |
| `threads` (default for DataFrame) | I/O-heavy work; NumPy/pandas release the GIL in C extensions |
| `processes` | CPU-heavy pure Python; bypasses GIL via separate processes |

```python
import dask

dask.config.set(scheduler='synchronous')  # debug: serial, clear errors
dask.config.set(scheduler='threads')      # default for DataFrames
dask.config.set(scheduler='processes')    # process pool, bypasses GIL
```

### `dask.distributed` — cluster scheduler

```python
from dask.distributed import Client

client = Client()                          # local cluster (spawns worker processes)
client = Client("scheduler-host:8786")    # connect to a remote cluster

result.compute()   # automatically routes to the distributed scheduler
```

**Architecture:**
- **Scheduler process:** single coordinator; tracks task graph, worker state, future dependencies
- **Worker processes:** execute tasks, cache intermediates in local memory
- **Dashboard:** live Bokeh UI at `:8787` — task stream, memory pressure, network bandwidth
- **Adaptive scaling:** integrates with Kubernetes, YARN, SLURM via `client.adapt(minimum=2, maximum=100)`

**Local threaded vs distributed:** use local threads for data that fits on one machine. Switch to distributed when: (1) data exceeds single-machine RAM, (2) fault tolerance is required, or (3) scaling to a cluster.

---

## 7. Interoperability

All three libraries now share **Apache Arrow** as a common memory format. When both sides use Arrow-backed storage, conversions are **zero-copy** (no data duplication).

```python
# pandas → Polars (zero-copy if pandas uses Arrow backend)
pl_df = pl.from_pandas(pd_df)
pl_df = pl.from_pandas(pd_df, use_pyarrow_extension_array=True)   # zero-copy

# Polars → pandas
pd_df = pl_df.to_pandas(use_pyarrow_extension_array=True)          # zero-copy

# pandas ↔ Dask
ddf = dd.from_pandas(pd_df, npartitions=4)
pd_df = ddf.compute()

# Any ↔ Arrow (zero-copy)
arrow_table = pl_df.to_arrow()
pl_df = pl.from_arrow(arrow_table)

# pandas 3.0 ↔ Arrow (new PyCapsule interface — no pyarrow import needed)
df = pd.DataFrame.from_arrow(arrow_table)

# DuckDB ↔ Polars (zero-copy, no intermediate copy)
import duckdb
result = duckdb.sql("SELECT * FROM pl_df WHERE age > 30").pl()   # returns Polars df
result = duckdb.sql("SELECT * FROM pd_df WHERE age > 30").df()   # returns pandas df
```

### Polars → Dask (no direct path yet)

```python
# Go through Arrow → pandas → Dask
arrow_table = pl_df.to_arrow()
pd_df = arrow_table.to_pandas(types_mapper=pd.ArrowDtype)   # Arrow-backed pandas
ddf = dd.from_pandas(pd_df, npartitions=4)
```

---

## 8. Key Limitations

### pandas
| Limitation | Notes |
|---|---|
| Single-threaded | No parallelism even with Arrow backend |
| Must fit in RAM | No streaming, no spill |
| `apply()` is slow | Python-level row iteration; no SIMD possible |
| Index complexity | Largely solved by CoW default in 3.0, but multi-index still tricky |

### Polars
| Limitation | Notes |
|---|---|
| No distributed compute | `RemoteEngine` is experimental — not production-ready |
| No row index | Intentional; requires mindset shift from pandas |
| `map_elements` breaks the engine | Python UDFs disable SIMD and parallelism; prefer native expressions |
| Smaller ecosystem | Less sklearn / statsmodels / plotly native integration |
| Faster release cadence | More breaking changes between versions than pandas |

### Dask
| Limitation | Notes |
|---|---|
| Scheduler overhead | ~1–5 ms per task; thousands of tasks = seconds of overhead |
| No cost-based optimizer | No join reordering, no cardinality estimates |
| Partial pandas coverage | `pivot_table`, some multi-index ops, `swaplevel` not fully supported |
| Large-large joins are expensive | Full shuffle across workers required |
| Debugging is hard | Errors surface at `.compute()` with graph-node stack traces, not user-code lines |
| Slower than pandas on small data | Task overhead dominates below ~10k rows |

---

## 9. Ecosystem Integrations

| | pandas | Polars | Dask |
|---|---|---|---|
| **scikit-learn** | Native | Via `.to_pandas()` | Dask-ML (parallel sklearn) |
| **XGBoost / LightGBM** | Native | Native (XGB 1.7+, LGBM 4.0+) | Native Dask callbacks |
| **PyTorch / TF** | Via numpy | Via numpy (zero-copy Arrow) | Via numpy per partition |
| **SQL** | Via DuckDB | Built-in `SQLContext` + DuckDB | FugueSQL / BlazingSQL |
| **Parquet** | pyarrow / fastparquet | Native (fastest reader) | pyarrow |
| **Delta Lake** | `deltalake` pkg | `deltalake` pkg | `dask-deltatable` |
| **Iceberg** | `read_iceberg()` (pandas 3.0) | Native (Polars 2.0+) | `dask-iceberg` |
| **GPU (RAPIDS)** | cuDF (pandas API on GPU) | Polars → Arrow → cuDF | dask-cudf |
| **Monitoring** | None | `explain()`, `profile()`, `show_graph()` | Bokeh dashboard (:8787), OpenTelemetry |

### SQL support comparison

```python
# Polars built-in SQL (full engine: CTEs, window funcs, subqueries)
ctx = pl.SQLContext({"sales": df})
result = ctx.execute("""
    SELECT dept, AVG(salary) AS avg_sal
    FROM sales
    WHERE age > 30
    GROUP BY dept
    ORDER BY avg_sal DESC
""")

# DuckDB on any of the three (recommended for SQL-heavy work — fastest in class)
import duckdb
duckdb.sql("SELECT dept, AVG(salary) FROM df GROUP BY dept")       # pandas df
duckdb.sql("SELECT dept, AVG(salary) FROM pl_df GROUP BY dept")    # polars df
duckdb.sql("SELECT dept, AVG(salary) FROM parquet_scan('*.parquet') GROUP BY dept")
```

### Streaming / real-time

- **pandas:** No streaming. Use with Kafka via `kafka-python` manually.
- **Polars:** Streaming engine processes files in chunks — not event-driven. Use `collect(streaming=True)` or `scan_*` functions.
- **Dask:** Batch-oriented. For true event streaming use **Bytewax**, **Faust**, or **Kafka + Flink**. `streamz` exists but is not actively maintained.

---

## 10. File Format Support

| Format | pandas | Polars | Dask |
|---|---|---|---|
| Parquet | ✓ (pyarrow/fastparquet) | ✓ native — fastest | ✓ (pyarrow) |
| CSV | ✓ | ✓ multithreaded reader | ✓ glob patterns |
| Arrow IPC / Feather | ✓ | ✓ native | ✓ |
| Delta Lake | `deltalake` pkg | `deltalake` pkg | `dask-deltatable` |
| Apache Iceberg | `read_iceberg()` (pandas 3.0) | ✓ Polars 2.0+, schema evolution | `dask-iceberg` |
| JSON | ✓ | ✓ | ✓ |
| GeoParquet | Via geopandas | Experimental (Polars 2.1) | Via geopandas |

---

## Summary

| | pandas 3.0 | Polars 2.1 | Dask 2025.4 |
|---|---|---|---|
| **Speed** | Baseline | 10–94× faster | 8× faster than pandas |
| **Memory** | Must fit in RAM (CoW helps) | Native Arrow + OOC spill | Partitioned; spill needs distributed |
| **Lazy eval** | No | Yes — full query planner | Yes — task graph + dask-expr |
| **Distributed** | No | Experimental | Production-ready |
| **API familiarity** | Most familiar | Different but clean | pandas-compatible |
| **Ecosystem** | Best | Growing | Good (sklearn, XGBoost) |
| **Best for** | EDA, ML pipelines, small data | Single-machine ETL / analytics | Cluster-scale pandas work |

**The one-line summary:**
- **pandas** when ecosystem compatibility matters more than speed
- **Polars** when speed matters and you are on a single machine
- **Dask** when the data genuinely does not fit on one machine
