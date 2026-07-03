# 🎓 Deep Learning Material: Understanding PromQL — Prometheus Query Language

**Source:** [256-understanding-promql-prometheus-query-language.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt?EntityRepresentationId=dab3d73d-cfc7-4d8b-a423-e778ce97824e) (video caption) + [256.PromQL+Intro.xlsx](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D\&file=256.PromQL%2BIntro.xlsx\&action=default\&mobileredirect=true\&EntityRepresentationId=8b51e5b9-9205-4217-bed9-b13eabf53e09) (reference spreadsheet) — Video lecture covering PromQL fundamentals: data types (instant vector, range vector, scalar, string), arithmetic/comparison/logical operators, time offset, rate and aggregation functions, vector matching, label operations, and common infrastructure monitoring patterns — all executed live against a Prometheus server with node exporter and a Python Flask application. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What PromQL Is and Where It Fits

Prometheus is a monitoring system that scrapes metrics from targets at regular intervals (every 15 seconds by default) and stores them as time-series data. Those metrics accumulate, but they are useless until you can **query** them. PromQL (Prometheus Query Language) is the language you use to retrieve, filter, transform, and compute over this stored time-series data. You write PromQL queries in the Prometheus web UI's query box (on port 9090), and later — more importantly — in Grafana dashboards to build visual panels. The video emphasizes repeatedly that PromQL will "make more sense when we go into Grafana." For now, the goal is to understand the query mechanics by executing them directly in the Prometheus console. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

The monitoring setup consists of: a **Prometheus server** (port 9090), targets including a **web server** running both **node exporter** (which exposes system-level metrics like CPU, memory, disk, network) and a **Python Flask application** (which exposes HTTP-level metrics like request counts). The Prometheus configuration defines **jobs** — logical groups of targets. Each job can contain one or multiple targets. In this setup, there are three jobs, each with a single target. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## 1.2 The Four Data Types in PromQL

Every PromQL expression evaluates to one of four data types. Understanding these types is essential because they determine what operations you can perform and what functions accept them.

### Instant Vector

An **instant vector** is the most common data type. It is a set of time series, each with a **single sample** at the current moment (or at a specified point in time). When you type the metric name `up` and execute it, Prometheus returns one value per target: `1` if the target is up, `0` if it's down. Each result includes **labels** — key-value pairs that identify which target the value belongs to (e.g., `app="prometheus"`, `app="web01-appstat"`). The label values can be strings (shown in double quotes), and the metric values are integers or floats. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

### Range Vector

A **range vector** is a set of time series where each series contains **multiple samples over a time window**. You create a range vector by appending a duration in square brackets to a metric: `up[5m]` returns all samples of the `up` metric from the last 5 minutes. Since Prometheus scrapes every 15 seconds, a 5-minute window contains approximately 20 data points per target. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

The duration syntax uses: `m` for minutes, `h` for hours, `d` for days, `s` for seconds, `ms` for milliseconds. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

Range vectors are not directly human-readable in the console — they show long lists of timestamp-value pairs. But they are essential as **inputs to functions** like `rate()`, `increase()`, and `avg_over_time()`. You rarely display a range vector directly; you pass it into a function that computes something meaningful from it. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

The timestamps in the output are in **Unix format** — the number of seconds since January 1, 1970. The video acknowledges this looks "slightly weird" but explains that it helps store data in a proper structure. Grafana converts these timestamps into human-readable dates automatically. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### Scalar

A **scalar** is a single numeric value with no labels. The function `count(up)` returns the number of time series matching the `up` metric — which is 3 (one per target). But it still returns this as an instant vector with empty labels `{}`. To get a **pure scalar** (just the number, no labels at all), you wrap it in the `scalar()` function: `scalar(count(up))` returns simply `3`. The difference between an instant vector with one element and a scalar matters in certain PromQL operations and in Grafana panel configurations. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

### String

A **string** is a literal text value. It is rarely used in practice — the video mentions it briefly as a data type that exists, primarily useful in console mode for label testing. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

***

## 1.3 Arithmetic Operators

PromQL supports standard arithmetic operations between metrics: addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), modulo (`%`), and power (`^`). These operate on instant vectors element-wise, matching time series by their labels. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

The video demonstrates subtraction to calculate **used memory**: `node_memory_MemTotal_bytes - node_memory_MemFree_bytes`. The `node_memory_MemTotal_bytes` metric gives total memory in bytes, `node_memory_MemFree_bytes` gives free memory in bytes. Subtracting gives the used portion. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

Division and multiplication are used together for **percentage calculations**: `(node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100` gives disk free percentage. Divide available by total to get a ratio (0 to 1), multiply by 100 to convert to percentage. This pattern — `(part / whole) * 100` — is reused across CPU, memory, and disk metrics. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

***

## 1.4 Comparison Operators

Comparison operators **filter** time series based on their values. They do not return `true`/`false` — they return only the series that match the condition, dropping everything else.

* `up == 1` — returns only targets that are up.
* `up == 0` — returns only targets that are down (if any).
* `node_load1 > 2` — returns only instances with load average above 2.
* `up != 0` — returns all targets that are not down (equivalent to `up == 1` in this context).

The full set: `==`, `!=`, `>`, `<`, `>=`, `<=`. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

The video demonstrates that `node_load1 > 3` may return nothing initially because the load fluctuates. A script running on the web server pushes load up and down, so the query result changes depending on when you execute it. This is a live demonstration that metric values are **dynamic** — the same query can return different results seconds apart. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## 1.5 Logical and Set Operators

Logical operators combine multiple conditions:

**`and`** — Intersection. Returns series that match **both** conditions. `up == 1 and node_load1 > 2` returns targets that are both up AND have high load. Both conditions must match for the same target. If one condition is true but the other is false for a target, that target is excluded. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`or`** — Union. Returns series that match **either** condition. `up == 0 or node_load1 > 2` returns targets that are either down or have high load (or both). [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`unless`** — Exclusion. Returns series from the left side that do NOT have a matching series on the right side. `up unless node_load1 > 2` returns targets that are up but excludes those with high load. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

***

## 1.6 Vector Matching — `on`, `ignoring`, `group_left`, `group_right`

When you perform operations between two different metrics (which have different label sets), PromQL needs to know **how to match** the series from one side to the other. By default, it matches on **all shared labels**. But sometimes the label sets don't align perfectly.

**`ignoring(label1, label2)`** — Ignore specific labels when matching. The spreadsheet example: `node_cpu_seconds_total{mode="user"} / ignoring(cpu,mode) node_cpu_seconds_total{mode="idle"}` divides user CPU time by idle CPU time, ignoring the `cpu` and `mode` labels during matching. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`on(label)`** — Match **only** on the specified label, ignoring everything else. `node_load1 * on(instance) group_left() up` matches by `instance` label only. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`group_left()` / `group_right()`** — Used for **many-to-one** or **one-to-many** matching. When one side has more series than the other, these modifiers tell PromQL which side is the "many" side and optionally which labels to bring across from the other side. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

🔍 **Deep Dive**
Vector matching is one of the more advanced PromQL concepts. The basic rule: without modifiers, PromQL matches series by identical label sets. When label sets differ between left and right operands, the operation fails silently (returns no results) unless you use `on` or `ignoring` to tell PromQL how to match. `group_left`/`group_right` are needed when the cardinality (number of series) differs between sides — for example, joining a per-CPU metric (many series) with a per-instance metric (one series per instance). [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

***

## 1.7 Time Offset — Looking at Historical Data

The `offset` modifier lets you query metric values from the **past**. By default, every metric query returns the current value. Adding `offset 5m` returns the value from 5 minutes ago. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

`node_memory_MemAvailable_bytes offset 6m` — What was the available memory 6 minutes ago? `up offset 5m` — Was this target up 5 minutes ago? [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

This is useful for comparing current values against historical values — for example, checking if memory is trending down compared to a recent past point. The duration syntax is the same as range vectors: `m`, `h`, `d`, `s`, `ms`. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## 1.8 Functions — Rates, Aggregations, and Predictions

Functions are where PromQL becomes powerful. They transform raw metric data into operationally meaningful information.

### Rate Functions (for Counters)

**`rate(metric[duration])`** — Calculates the **per-second rate of increase** of a counter metric over the specified window. `rate(http_requests_total[5m])` returns requests per second averaged over 5 minutes. This is one of the most commonly used PromQL functions. The video demonstrates it live: after executing the rate query, it shows approximately 3 requests per second for the main endpoint and less for the payment endpoint (because the script generating traffic wasn't working initially). [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`irate(metric[duration])`** — **Instantaneous rate** — calculates rate using only the last two data points in the range. More responsive to spikes than `rate()` (which smooths over the entire window). The spreadsheet notes it as "helpful for network throughput." [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`increase(metric[duration])`** — Returns the **total increase** of a counter over the duration. `increase(http_requests_total[1h])` tells you how many total requests came in during the last hour. Unlike `rate()` which gives per-second, `increase()` gives the absolute count over the window. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`delta(metric[duration])`** — The change in value of a **gauge** metric over the duration. `delta(node_memory_MemFree_bytes[10m])` shows how much free memory changed in the last 10 minutes. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

### Aggregation Operators

**`sum()`** — Adds all values together. `sum(up)` with three targets returns `3`. `sum by (job) (up)` groups by the `job` label — showing how many targets are up per job. The video demonstrates: since each job has only one target, each job shows `1`. But if a job had 10 targets, it would show how many of those 10 are up. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`avg()`** — Average. `avg without (instance) (node_load1)` averages load across all instances (ignoring the `instance` label). [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`count()`** — Counts the number of time series. `count(up)` returns `3`. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`topk(k, metric)`** / **`bottomk(k, metric)`** — Returns the top/bottom K series by value. `topk(3, node_load1)` returns the 3 instances with the highest load. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

Other aggregations: `min()`, `max()`, `stddev()`, `stdvar()`, `count_values()`, `quantile()`. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

### Grouping with `by` and `without`

Aggregations can be grouped: `sum by (job) (up)` groups by the `job` label. `avg without (instance) (node_load1)` aggregates across all instances by removing the `instance` label from the grouping. `by` specifies which labels to keep; `without` specifies which labels to remove. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

### Predictive and Time Functions

**`predict_linear(metric[duration], seconds)`** — Linear regression prediction. `predict_linear(node_filesystem_avail_bytes[1h], 3600)` predicts what disk space will be in 1 hour based on the trend from the last hour. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`time()`** — Returns the current Unix timestamp. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**`histogram_quantile(quantile, metric)`** — Estimates percentile values from histogram metrics. `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` calculates the 95th percentile latency. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

### Time-Range Aggregation Functions

These operate over a range vector to produce an instant vector: `sum_over_time()`, `avg_over_time()`, `min_over_time()`, `max_over_time()`, `count_over_time()`. They aggregate **across time** for each series rather than across series at a single point. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

***

## 1.9 Metrics Sources — Node Exporter vs Application Metrics

The video works with two distinct metrics sources. **Node exporter** generates system-level metrics prefixed with `node_` — memory (`node_memory_MemTotal_bytes`, `node_memory_MemFree_bytes`, `node_memory_MemAvailable_bytes`), CPU (`node_cpu_seconds_total`), disk (`node_filesystem_avail_bytes`, `node_filesystem_size_bytes`), network (`node_network_receive_bytes_total`), and load (`node_load1`). These exist only for the web server target, not for the Prometheus server itself. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

The **Python Flask application** exposes HTTP metrics like `http_requests_total`, which counts total HTTP requests per endpoint. This metric has labels for the endpoint path (e.g., `/`, `/payment`). The video shows the request count growing as a script generates traffic, and demonstrates that the payment endpoint count lagged behind because the traffic script had stopped running and needed to be restarted. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

🔍 **Deep Dive**
The video captures a live debugging moment: the `http_requests_total` for `/payment` was stuck at 1 while `/` was in the thousands. The instructor SSHs into the web server, checks the script process with `ps -f | grep web`, kills it (`kill 2363`), examines the script, tests with `curl` manually (confirming the page responds), then restarts the script. After restarting, the counter starts increasing. The instructor also restarts the main page script to equalize the counts. This demonstrates that metric values depend on **real traffic** — if the traffic generator stops, the counters stop increasing, and `rate()` drops to zero. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## 1.10 The Scrape Interval and Its Effect on Data

Prometheus scrapes metrics every **15 seconds** (the configured scrape interval). This means a 5-minute range vector contains approximately 20 data points (300 seconds / 15 seconds). After making a change (like accessing a web page manually), you must wait **at least 15 seconds** for Prometheus to scrape the new value before it appears in query results. The video demonstrates this directly — after hitting the payment endpoint in the browser, the instructor waits, executes the query multiple times, and only after the scrape interval passes does the new count appear. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## 1.11 Common Monitoring Patterns

The spreadsheet provides five critical infrastructure monitoring patterns that combine the operators and functions covered:

**CPU Usage %:** `100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` — Calculate idle CPU rate, convert to percentage, subtract from 100 to get usage. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**Memory Usage %:** `(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100` — Ratio of available to total, inverted, as percentage. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**Disk Free %:** `(node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100` — Direct ratio as percentage. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**Request Rate:** `rate(http_requests_total[1m])` — Requests per second over the last minute. [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

**Error Rate:** `rate(http_requests_total{status!~"2.."}[5m])` — Rate of non-2xx responses (using regex label matching). [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing

We are executing PromQL queries directly in the Prometheus web UI to understand every data type, operator, and function. The final outcome: hands-on familiarity with PromQL mechanics so that when we build Grafana dashboards in later lectures, the queries are already understood. A downloadable spreadsheet with all queries is provided as a reference. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 1: Access the Prometheus Query Interface

Open a browser and navigate to:

```
http://<prometheus-server-ip>:9090
```

Click on **Status** → check your targets. You should see three targets: Prometheus itself, web server app stat (Flask app), and web server system (node exporter). All should show as "UP." [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

Click on the **Query** tab (or the query input box at the top) to enter PromQL queries.

***

## Step 2: Execute Data Type Queries

### 2a. Instant Vector

```promql
up
```

Click **Execute**. Expected output: three rows, one per target, each showing `1` (up) or `0` (down) with their labels. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 2b. Range Vector

```promql
up[5m]
```

Execute. Expected: each target shows \~20 timestamp-value pairs (one per scrape over 5 minutes). Timestamps are in Unix format. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 2c. Scalar

```promql
scalar(count(up))
```

Execute. Expected: a single number `3` with no labels. Compare with `count(up)` alone — which returns `3` but with empty labels `{}`. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 3: Execute Arithmetic Operator Queries

### 3a. Used Memory (subtraction)

```promql
node_memory_MemTotal_bytes - node_memory_MemFree_bytes
```

Execute. Returns the used memory in bytes for the web server. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 3b. Disk Free Percentage (division + multiplication)

```promql
(node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100
```

Execute. Returns the percentage of free disk space. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 4: Execute Comparison Operator Queries

### 4a. Only Healthy Targets

```promql
up == 1
```

Execute. Returns only targets with value `1`. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 4b. Only Down Targets

```promql
up == 0
```

Execute. Expected: no results (if all targets are up). [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 4c. High Load Instances

```promql
node_load1 > 2
```

Execute. Results may fluctuate — a script on the web server generates variable load. Execute multiple times over several seconds to see results appear and disappear. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 5: Execute Logical Operator Queries

### 5a. AND — Both Conditions Must Match

```promql
up == 1 and node_load1 > 2
```

Returns targets that are both up AND have load > 2. If load is below 2 at the moment, returns nothing. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 5b. OR — Either Condition Matches

```promql
up == 0 or node_load1 > 4
```

Returns targets that are either down or have load > 4. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 6: Execute Offset Queries

### 6a. Current Free Memory

```promql
node_memory_MemAvailable_bytes
```

Execute. Shows current value. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 6b. Free Memory 5 Minutes Ago

```promql
node_memory_MemAvailable_bytes offset 5m
```

Execute. Shows the value from 5 minutes ago — may differ from current. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 7: Execute HTTP Metrics Queries (Flask Application)

### 7a. Total Request Count

```promql
http_requests_total
```

Execute. Shows total requests per endpoint (e.g., `/` and `/payment`). [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 7b. Range of Requests Over 5 Minutes

```promql
http_requests_total[5m]
```

Execute. Shows how the counter grew over time — each scrape captured an increasing count. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 7c. Request Rate (Requests Per Second)

```promql
rate(http_requests_total[5m])
```

Execute. Returns the per-second request rate averaged over 5 minutes. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

⚠️ If the payment endpoint shows a very low or zero rate, the traffic-generating script may have stopped. See Step 8 for troubleshooting. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 8: Troubleshoot the Traffic Script (If Needed)

If `http_requests_total` for `/payment` is not increasing:

**8a. SSH into the web server:**

```bash
ssh -i <key> <user>@<web-server-ip>
```

**8b. Check if the script is running:**

```bash
ps -f | grep web
```

**8c. Kill the stuck process:**

```bash
kill <PID>
```

**8d. Verify the endpoint works manually:**

```bash
curl http://localhost:5000/payment
```

Should return HTML. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

**8e. Restart the script:**

```bash
./web_payment.sh &
```

**8f. Wait at least 15 seconds** for the next Prometheus scrape, then re-execute the query. The counter should start increasing. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 9: Execute Aggregation Queries

### 9a. Sum by Job

```promql
sum by (job) (up)
```

Returns the count of up targets per job group. With one target per job, each shows `1`. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

### 9b. Increase Over Time

```promql
increase(http_requests_total[1h])
```

Returns the total number of new requests in the last hour. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

## Step 10: Download and Work Through the Reference Spreadsheet

Download [256.PromQL+Intro.xlsx](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D\&file=256.PromQL%2BIntro.xlsx\&action=default\&mobileredirect=true\&EntityRepresentationId=8b51e5b9-9205-4217-bed9-b13eabf53e09) from the lecture resources. It contains two sheets:

* **Sheet 1:** Categorized queries with expected outputs — data types, arithmetic, comparison, logical, offset, and functions.
* **Sheet 2:** Comprehensive reference of every PromQL category, type, example, and description.

Execute **every query** from the spreadsheet in the Prometheus UI. Read the description while observing the output. Some results may not make full sense until Grafana is introduced — this is expected. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt), [\[256.PromQL+Intro \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B5B7C6889-BEEC-463F-9007-918DF5A715C6%7D&file=256.PromQL%2BIntro.xlsx&action=default&mobileredirect=true)

⚠️ **Expert Note**
The instructor explicitly says: "Learn by doing it. And not just by watching. By just watching you'll just get confused." Execute every query. Observe the output. Read the description. The understanding builds through repetition and observation, not memorization. For queries you can't construct yourself, use ChatGPT: describe the graph/metric you need, get the query, put it in Prometheus/Grafana, and tinkle until it works. [\[256-unders...y-language \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/256-understanding-promql-prometheus-query-language.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## PromQL Data Type Hierarchy

```
Metric name alone     → Instant Vector (single value per series, current time)
Metric[duration]      → Range Vector   (multiple values per series, over time window)
scalar(expression)    → Scalar          (single number, no labels)
"text"                → String          (literal text, rarely used)

Duration syntax:  m=minutes  h=hours  d=days  s=seconds  ms=milliseconds
```

***

## Operator Categories

```
ARITHMETIC:    +  -  *  /  %  ^        → compute between metrics
COMPARISON:    ==  !=  >  <  >=  <=    → FILTER series by value (not true/false)
LOGICAL:       and  or  unless         → SET operations (intersection/union/exclusion)
VECTOR MATCH:  on()  ignoring()        → control label matching between sides
               group_left()  group_right()  → many-to-one joins
TIME:          offset <duration>       → shift query to past
```

***

## Core Function Map

```
RATE FUNCTIONS (counter → per-second):
  rate(metric[window])      → smoothed per-second rate
  irate(metric[window])     → instant rate (last 2 points, spiky)
  increase(metric[window])  → total increase over window
  delta(metric[window])     → change in gauge over window

AGGREGATION (across series):
  sum()  avg()  min()  max()  count()
  topk(k, metric)  bottomk(k, metric)
  Grouping: sum by (label) (metric)
            avg without (label) (metric)

TIME AGGREGATION (across time, per series):
  sum_over_time()  avg_over_time()  min_over_time()  max_over_time()

PREDICTION:
  predict_linear(metric[window], future_seconds)

HISTOGRAM:
  histogram_quantile(quantile, rate(buckets[window]))
```

***

## Common Monitoring Patterns (Critical)

```
CPU Usage %:
  100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

Memory Usage %:
  (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

Disk Free %:
  (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100

Request Rate:
  rate(http_requests_total[1m])

Error Rate:
  rate(http_requests_total{status!~"2.."}[5m])
```

***

## Metric Sources

```
node_exporter (system metrics):
  node_memory_MemTotal_bytes      → total RAM
  node_memory_MemFree_bytes       → free RAM
  node_memory_MemAvailable_bytes  → available RAM
  node_cpu_seconds_total          → CPU time per mode (idle, user, system)
  node_load1                      → 1-min load average
  node_filesystem_avail_bytes     → disk available
  node_filesystem_size_bytes      → disk total
  node_network_receive_bytes_total → network ingress

Flask app (HTTP metrics):
  http_requests_total             → request counter (labels: endpoint, method, status)
  http_request_duration_seconds   → request latency histogram
```

***

## Architecture

```
[ Prometheus Server :9090 ]
    │
    │ scrapes every 15 seconds
    │
    ├── Job: prometheus     → self-monitoring
    ├── Job: web-app-stat   → Flask app metrics (http_requests_total)
    └── Job: web-system     → node_exporter metrics (node_*)

Query flow:
  User → PromQL query → Prometheus TSDB → instant/range vector → display / Grafana
```

***

## Scrape Interval Effects

```
Scrape interval = 15 seconds
5-minute range  = ~20 data points
After manual action (curl, page visit) → wait ≥15s for metric update
rate() smooths over window → spikes take time to appear
irate() uses last 2 points → responds faster to spikes
```

***

## Instant Vector vs Range Vector Usage

```
Instant vector:
  - Direct display
  - Arithmetic/comparison/logical operations
  - Aggregation functions (sum, avg, count)

Range vector:
  - Input to rate(), irate(), increase(), delta()
  - Input to *_over_time() functions
  - Cannot be displayed directly or used in arithmetic

Rule: most functions that need "over time" require [duration] → range vector
```

***

## Vector Matching Quick Reference

```
Default:           match on ALL shared labels
on(label):         match ONLY on specified label(s)
ignoring(label):   match on all labels EXCEPT specified
group_left():      many-to-one (left side has more series)
group_right():     one-to-many (right side has more series)
```

***

## Aggregation Grouping

```
sum by (job) (up)           → keep only 'job' label, sum within each group
avg without (instance) (m)  → remove 'instance' label, avg across everything else

by    = specify which labels to KEEP
without = specify which labels to REMOVE
```

***

## Debugging Checklist (Metric Not Updating)

```
1. Is the target UP?              → check Status → Targets
2. Is the traffic script running? → ps -f | grep web
3. Is the endpoint responding?    → curl http://localhost:5000/<endpoint>
4. Wait ≥15 seconds              → scrape interval
5. Re-execute query               → check if counter increased
```

***

## Key Engineering Patterns

| Pattern                        | Manifestation                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Counter vs Gauge**           | Counters only go up (use `rate()`, `increase()`); gauges go up/down (use `delta()`, direct value)                        |
| **Range → Function → Instant** | Range vectors are intermediate — always consumed by a function to produce displayable instant vectors                    |
| **Ratio × 100 = Percentage**   | Universal pattern: `(part / total) * 100` for CPU, memory, disk                                                          |
| **Filter-then-aggregate**      | Comparison operators filter series → aggregation functions summarize the filtered set                                    |
| **Label-based grouping**       | `by`/`without` control how aggregation groups series — determines dashboard granularity                                  |
| **Scrape-aware querying**      | All PromQL operates on discrete scraped samples, not continuous data — window sizes and rates depend on scrape frequency |

***

## Learning Strategy (from instructor)

```
NOW:    Execute every query from spreadsheet → observe output → read description
LATER:  Build Grafana panels using these queries → visual context makes everything click
ALWAYS: Use ChatGPT to generate queries for specific requirements → tinkle until correct

"Learn by doing it. Not just by watching."
"PromQL is not over. It just got started."
```

***

## Project Continuity

```
BEFORE: Prometheus setup, node exporter, Flask app, targets configured
THIS:   PromQL fundamentals — data types, operators, functions, patterns
NEXT:   More PromQL throughout monitoring section + Grafana dashboards
```

***

This completes the full reconstruction. **Theory** builds understanding of every PromQL concept from data types through vector matching to common patterns. **Practical** gives you every query to execute and how to troubleshoot when metrics don't update. The **Compression Map** lets you look up any operator, function, or monitoring pattern instantly during future Grafana work. Let me know if you'd like Anki flashcards or any section expanded! 🚀
