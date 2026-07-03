# 🎓 Deep Learning Material: PromQL Queries for Grafana Dashboard Panels

**Source:** [259-promql-for-grafana-dashboards.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt?EntityRepresentationId=f6846a2d-4c3e-435a-9ddd-eede4baeee82) (video caption) + [259.GrafanaPanelQueries.xlsx](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D\&file=259.GrafanaPanelQueries.xlsx\&action=default\&mobileredirect=true\&EntityRepresentationId=73de00df-84d0-4c98-9427-179d1ab99038) (panel reference spreadsheet) — Video lecture covering Grafana dashboard organization (folders, dashboards, rows), step-by-step decoding of PromQL queries for dashboard panels, label filtering, unit conversion (bytes to MB/GB), CPU utilization query construction, metric types (counter vs gauge), and preparing a complete set of panel queries for system health, storage, traffic, performance, and service availability monitoring. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt), [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Grafana Dashboard Organization — The Hierarchy

Before writing any queries, the video establishes how Grafana organizes monitoring content. The hierarchy is: **Folders → Dashboards → Rows → Panels**. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

A **folder** represents a project or a logical grouping. In an organization, you might have one Grafana instance serving multiple projects, so folders prevent them from mixing. The video creates a folder called "Titan Monitoring." [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

Inside a folder, **dashboards** represent environments. A single project will have multiple environments — dev, QA, staging, production. Each environment gets its own dashboard. The video creates a dashboard called "Titan Prod." The instructor notes that naming conventions may change depending on whether you have one Grafana per project or one for the entire organization — but proper organization is essential regardless. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

Inside a dashboard, **rows** segregate different types of monitoring. The video creates two rows: "System" (for CPU, memory, disk metrics) and "Application" (for HTTP request metrics, business KPIs). The instructor references the introduction lecture where different kinds of monitoring were discussed — system monitoring, application monitoring, business KPI monitoring. Rows keep these visually separated within the same dashboard. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

Inside rows, **panels** are the actual visual widgets — time series graphs, gauges, stat displays, bar charts. Each panel is powered by one or more PromQL queries. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

⚠️ **Expert Note**
The instructor emphasizes: "Every time you make changes to a dashboard, you need to click Save Dashboard. If you move on without doing that, it will not be saved." This is demonstrated live when the instructor almost forgets to save after adding rows — Grafana alerts about unsaved changes. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## 1.2 The Relationship Between Queries and Panels

The core message of this lecture: the **query is the essence of the panel**. A panel is just a visualization container. What makes it useful is the PromQL query that feeds it data. The instructor states: "This is the main essence of the panels. Based on this information, only the panels will show the data." Understanding how to construct, decode, and modify PromQL queries is therefore more important than knowing the Grafana UI mechanics. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

The spreadsheet provides a complete reference mapping each panel to its query. Each row specifies: the **category** (System Health, Storage, Traffic, Performance, Service Availability), the **panel title** (what the user sees), the **display name/legend** (how series are labeled in the visualization — using `{{instance}}` or `{{endpoint}}` template variables to dynamically show the label value), the **visualization type** (time series, gauge, stat, bar chart), and the **PromQL query or queries** that power it. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

***

## 1.3 Label Filtering — Selecting Specific Data from Metrics

Prometheus metrics return data for **all** matching targets. In a production environment with thousands of nodes, a raw metric like `node_memory_MemTotal_bytes` would return thousands of results. To narrow down to specific targets, you use **label filtering** with curly braces `{}` appended to the metric name. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

The syntax is: `metric_name{label="value"}`. For example, `node_memory_MemTotal_bytes{job="webserver-system"}` returns memory data only for targets belonging to the job named `webserver-system`. The `job` label comes from the Prometheus configuration file — it is the job name you defined when setting up scrape targets. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

The instructor emphasizes a critical operational point: the **job name in your PromQL queries must exactly match the job name in your Prometheus configuration**. The spreadsheet provides queries with specific job names, but your Prometheus setup may use different names. Before copy-pasting queries, check your actual job names by running `up` in the Prometheus query interface — it shows all targets with their labels, including the `job` label. Replace the job names in the spreadsheet accordingly. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

You can run queries directly in the Grafana query editor without switching to Prometheus — Grafana connects to Prometheus as a data source and provides the same query execution capability. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## 1.4 Unit Conversion — Bytes to Human-Readable Format

Many system metrics (memory, disk) report values in **bytes**. Raw byte values like `1028694016` are not human-readable. The video demonstrates the conversion chain step by step: [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

* Divide by `1024` → kilobytes (KB)
* Divide by `1024` again → megabytes (MB)
* Divide by `1024` again → gigabytes (GB)

Instead of writing `/ 1024 / 1024`, you can use the **power operator**: `/ 1024^2` for MB, `/ 1024^3` for GB. The caret symbol `^` is the exponentiation operator in PromQL (typed with Shift+6). [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

The video demonstrates this with `node_memory_MemAvailable_bytes{job="webserver-system"} / 1024^2`, which converts available memory from bytes to megabytes. Since the lab uses t2.micro instances with very little RAM, MB is more appropriate than GB (which would show small decimal values like 0.9). [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

The spreadsheet uses this pattern for the "Available Memory (MB)" panel: `(node_memory_MemAvailable_bytes{job="webserver-system"} / 1024^2)`. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

***

## 1.5 CPU Utilization Query — The Complete Deconstruction

The CPU utilization query is the most complex query deconstructed in the video, and the instructor walks through it layer by layer. The final query is:

```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

 [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Layer 1 — The raw metric:** `node_cpu_seconds_total` is a **counter** metric (it only increases). It records the total number of seconds the CPU has spent in each mode — idle, user, system, nice, steal, etc. Each mode is a separate time series, identified by the `mode` label. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Layer 2 — Filter to idle:** `node_cpu_seconds_total{mode="idle"}` selects only the idle mode. Idle represents the time the CPU was doing nothing. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Layer 3 — Add a range:** `node_cpu_seconds_total{mode="idle"}[5m]` converts it to a range vector covering the last 5 minutes. This is needed as input for the rate function. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Layer 4 — Calculate the rate of change:** `irate(node_cpu_seconds_total{mode="idle"}[5m])` calculates the instantaneous rate of change — how fast the idle counter is increasing per second. This gives a value between 0 and 1 (representing the fraction of time the CPU was idle). [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Layer 5 — Convert to percentage:** Multiply by 100 to get idle percentage. If the result is 0.96, multiplying by 100 gives 96% — meaning the CPU was idle 96% of the time. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Layer 6 — Invert to get usage:** `100 - (...)` subtracts the idle percentage from 100 to get the **usage** percentage. If idle is 96%, usage is 4%. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Layer 7 — Aggregate across instances:** `avg by (instance)` averages the result grouped by the `instance` label. With a single instance, this has no visible effect. With multiple instances, it produces one line per instance on the graph, each showing its own CPU usage. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

🔍 **Deep Dive**
The instructor mentions that `node_cpu_seconds_total` is a **counter** type metric — it always increases. This is why you must use `rate()` or `irate()` to get useful information from it. A counter's raw value (total seconds spent idle since boot) is meaningless for current utilization; what matters is the rate at which it's changing now. The spreadsheet uses `irate` (instantaneous rate) rather than `rate` (smoothed average) — `irate` is more responsive to recent spikes and drops, making the graph more reflective of real-time CPU behavior. The video also notes that the load script running on the web node causes values to fluctuate, which is visible because of the 5-minute averaging window. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## 1.6 Metric Types: Counter vs Gauge

The video briefly introduces the distinction between **counter** and **gauge** metric types when examining `node_cpu_seconds_total`. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

A **counter** only increases (1, 2, 3, 4...) — it represents cumulative totals like total requests served, total CPU seconds consumed. You never read a counter's raw value directly; you use `rate()`, `irate()`, or `increase()` to extract the rate of change. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

A **gauge** goes up and down — it represents current state values like available memory, current temperature, current load average. You can read a gauge's raw value directly. The instructor says: "We'll take a look at gauge later in memory while we create panels in Grafana." [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## 1.7 The Complete Panel Query Reference

The spreadsheet provides the full set of queries organized by monitoring category. Each query is designed to power a specific Grafana panel visualization. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

### System Health Panels

**CPU Utilization (%) — Time Series:** Uses the inverted idle irate pattern (detailed in §1.5). [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Available Memory (MB) — Gauge:** `node_memory_MemAvailable_bytes{job="webserver-system"} / 1024^2`. Converts bytes to megabytes. Uses gauge visualization because it represents a current-state value. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Available Memory (%) — Gauge:** `(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100`. The ratio pattern from the previous PromQL lecture — part divided by whole, times 100. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Load Average (1m) — Time Series:** `node_load1{job="webserver-system"}`. A direct gauge metric — no rate function needed. Shows the 1-minute load average over time. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

### Storage & Disk Activity Panels

**Root Filesystem Usage (%) — Time Series:** `(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100`. Filters to the root mountpoint `/`, computes the ratio of available to total, subtracts from 1 to get usage (not free), multiplies by 100. This is the same inversion pattern used for CPU. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Disk Read Rate (ops/sec) — Time Series:** `rate(node_disk_reads_completed_total[2m])`. Counter metric → rate function → per-second read operations. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

### Traffic & Requests Panels

**HTTP Request Rate (req/sec) — Time Series:** `rate(http_requests_total{job="webserver-appstat"}[1m])`. Request counter → rate → requests per second per endpoint. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Total Requests by Endpoint — Stat:** `sum by (endpoint) (http_requests_total{job="webserver-appstat"})`. Aggregates total requests grouped by endpoint label. Uses stat visualization (single number display). [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

### Performance & Latency Panels

**Average Request Duration (s) — Time Series:** `rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])`. This divides the rate of total duration by the rate of request count — giving average duration per request. Two separate metrics are used: `_sum` (total seconds spent) and `_count` (total number of requests). [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Requests by Endpoint (Last 5m) — Bar Chart:** `increase(http_requests_total{job="webserver-appstat"}[5m])`. Shows absolute increase over 5 minutes as a bar chart — useful for comparing endpoint traffic volumes. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

### Service Availability Panel

**Service Status (Up/Down) — Stat:** `up{job="webserver-appstat"}`. Simple 1/0 value displayed as a stat widget. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

### Advanced Panels

**Dynamic Variable Panel:** `sum by (endpoint) (http_requests_total{job="webserver-appstat", endpoint=~"$endpoint"})`. Uses the `$endpoint` Grafana template variable — allowing users to select which endpoint to view from a dropdown. The `=~` operator is regex matching. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**Offset Comparison (Two Queries):** Query A: `rate(http_requests_total{endpoint="/"}[1m])`. Query B: `rate(http_requests_total{endpoint="/"}[1m] offset 5m)`. Shows current request rate vs. the rate 5 minutes ago on the same panel — useful for spotting trends. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

***

## 1.8 Legend Templates — `{{label_name}}`

In the spreadsheet's "Display Name (Legend)" column, entries like `{{instance}} - CPU Usage` or `{{endpoint}} - Rate` use Grafana's **legend template syntax**. The double curly braces dynamically insert the value of the specified label from the query result. If the query returns data for instance `web01:9090`, the legend reads `web01:9090 - CPU Usage`. This makes multi-series panels self-labeling without hardcoding names. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are preparing all the PromQL queries that will power Grafana dashboard panels, organizing the Grafana dashboard structure (folder → dashboard → rows), and testing each query to ensure it returns correct data before building visual panels. The final outcome: a fully organized dashboard skeleton with tested queries ready for panel creation in the next lecture. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## Step 1: Create the Grafana Folder Structure

**1a. Open Grafana** in your browser. Click on **Dashboards** in the left sidebar. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**1b. Create a folder:**

Click the dropdown arrow next to the Dashboards header → **Create New Folder**. Name it after your project — e.g., `Titan Monitoring`. Click **Create**. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**1c. Create a dashboard inside the folder:**

Navigate back to Dashboards → click the `Titan Monitoring` folder → click **Create Dashboard**. Click the **Settings** (gear icon) at the top. Give it a name — e.g., `Titan Prod`. Verify the folder shows `Titan Monitoring`. Click **Save Dashboard**. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

⚠️ Always click **Save Dashboard** after any change. Grafana does not auto-save. If you navigate away without saving, changes are lost. Grafana will alert you about unsaved changes, but don't rely on it. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## Step 2: Create Rows for Metric Categories

Inside the `Titan Prod` dashboard:

**2a. Add the System row:**

Click **Add** (dropdown) → **Row**. A row appears. Click the small **gear icon** on the row → rename it to `System`. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**2b. Add the Application row:**

Click **Add** → **Row** again. Rename to `Application`. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**2c. Save the dashboard.** [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Connection to larger flow:** System panels (CPU, memory, disk, load) will be added under the System row. HTTP/request panels will go under the Application row. This mirrors how operations teams mentally separate infrastructure health from application behavior.

***

## Step 3: Identify Your Job Names

Before using any query from the spreadsheet, verify your actual Prometheus job names.

**3a.** In the Grafana query editor (or in Prometheus at `:9090`), execute:

```promql
up
```

**3b.** Check the `job` label for each target in the results. Note the exact names — e.g., `webserver-appstat`, `webserver-system`, `prometheus`. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**3c.** In the downloaded spreadsheet ([259.GrafanaPanelQueries.xlsx](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D\&file=259.GrafanaPanelQueries.xlsx\&action=default\&mobileredirect=true\&EntityRepresentationId=73de00df-84d0-4c98-9427-179d1ab99038)), replace every `job="..."` value with your actual job names. If you skip this, queries will return empty results because the label filter won't match. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## Step 4: Test the Memory Query (Step-by-Step Decoding)

This demonstrates the decoding workflow. Apply the same approach to every query in the spreadsheet.

**4a. Start with the raw metric:**

```promql
node_memory_MemTotal_bytes
```

Execute. Returns total memory in bytes for all node exporter targets. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**4b. Filter by job label:**

```promql
node_memory_MemTotal_bytes{job="webserver-system"}
```

Execute. Returns only the web server's total memory. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**4c. Convert to KB (divide by 1024):**

```promql
node_memory_MemTotal_bytes{job="webserver-system"} / 1024
```

Execute. Value is now in kilobytes. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**4d. Convert to MB (divide by 1024 again):**

```promql
node_memory_MemTotal_bytes{job="webserver-system"} / 1024 / 1024
```

Or equivalently using the power operator:

```promql
node_memory_MemTotal_bytes{job="webserver-system"} / 1024^2
```

Execute. Value is now in megabytes — human-readable for a t2.micro instance. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**4e. For GB, use power of 3:**

```promql
node_memory_MemTotal_bytes{job="webserver-system"} / 1024^3
```

Returns small decimal values for t2.micro — MB is more appropriate here. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Connection to larger flow:** This decoding workflow (raw → filter → transform → verify) applies to every query. Always start with the raw metric, layer on filters, then add transformations.

***

## Step 5: Test the CPU Utilization Query (Layer-by-Layer)

**5a. Raw metric — all CPU modes:**

```promql
node_cpu_seconds_total
```

Execute. Returns many series — one per CPU mode (idle, user, system, nice, steal, etc.). [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**5b. Filter to idle mode:**

```promql
node_cpu_seconds_total{mode="idle"}
```

Execute. Returns only the idle time counter. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**5c. Add range for rate calculation:**

```promql
node_cpu_seconds_total{mode="idle"}[5m]
```

Execute. Returns a range vector — multiple timestamped values. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**5d. Calculate instantaneous rate:**

```promql
irate(node_cpu_seconds_total{mode="idle"}[5m])
```

Execute. Returns the rate of change (fraction of time spent idle, between 0 and 1). [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**5e. Convert to percentage:**

```promql
irate(node_cpu_seconds_total{mode="idle"}[5m]) * 100
```

Execute. Shows idle percentage (e.g., \~96%). [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**5f. Invert to get usage:**

```promql
100 - (irate(node_cpu_seconds_total{mode="idle"}[5m]) * 100)
```

Execute. Shows CPU usage percentage (e.g., \~4%). [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**5g. Add instance grouping (full query):**

```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

Execute. Same result with one instance. With multiple instances, produces one value per instance. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

⚠️ **Common mistake:** Mismatched parentheses. The query editor highlights matching opening/closing parentheses when you place your cursor — use this to verify. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

**Why values fluctuate:** A load-generating script runs on the web node, pushing CPU usage up and down. The 5-minute window averages this, but you'll still see changes between executions. [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## Step 6: Test All Remaining Queries from the Spreadsheet

Execute every query from the spreadsheet one by one in the Grafana query editor or Prometheus UI. For each:

1. Run the raw metric first to see what it returns.
2. Add label filters to narrow down.
3. Add functions/transformations.
4. Verify the output makes sense.

**Key queries to test:** [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

| Panel                | Query                                                                 | What to Verify                                     |
| -------------------- | --------------------------------------------------------------------- | -------------------------------------------------- |
| Available Memory (%) | `(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100` | Returns 0-100 percentage                           |
| Load Average         | `node_load1{job="webserver-system"}`                                  | Direct gauge — fluctuates with load script         |
| Root Disk Usage (%)  | `(1 - (avail/size)) * 100` for mountpoint `/`                         | Returns disk usage, not free space                 |
| HTTP Request Rate    | `rate(http_requests_total{job="webserver-appstat"}[1m])`              | Returns per-second rate per endpoint               |
| Total Requests       | `sum by (endpoint) (http_requests_total)`                             | Absolute counter values grouped by endpoint        |
| Avg Request Duration | `rate(_sum[1m]) / rate(_count[1m])`                                   | Returns seconds per request                        |
| Requests Bar Chart   | `increase(http_requests_total[5m])`                                   | Total increase, not rate — good for bar comparison |
| Service Status       | `up{job="webserver-appstat"}`                                         | Returns 1 (up) or 0 (down)                         |

If any query returns no data, check: (1) Is the job name correct? (2) Is the target up? (3) Is the metric name spelled correctly? [\[259-promql...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/259-promql-for-grafana-dashboards.txt)

***

## Step 7: Understand the Advanced Queries

**7a. Dynamic Variable Query:**

```promql
sum by (endpoint) (http_requests_total{job="webserver-appstat", endpoint=~"$endpoint"})
```

The `$endpoint` is a Grafana **dashboard variable** — it creates a dropdown in the dashboard UI where users select an endpoint. The `=~` operator is regex matching, allowing the variable to filter results dynamically. This will be configured when creating the actual panel. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

**7b. Offset Comparison (Two Queries in One Panel):**

Query A: `rate(http_requests_total{endpoint="/"}[1m])`
Query B: `rate(http_requests_total{endpoint="/"}[1m] offset 5m)`

These are placed in the **same panel** as Query A and Query B. The panel shows two lines — current rate vs. rate 5 minutes ago — enabling visual trend comparison. [\[259.Grafan...nelQueries \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B123955D4-1DD8-445F-83AE-EDBFD7815AB7%7D&file=259.GrafanaPanelQueries.xlsx&action=default&mobileredirect=true)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Grafana Organization Hierarchy

```
Folder (project)
  └── Dashboard (environment: prod, dev, QA)
        ├── Row: System          → CPU, Memory, Disk, Load panels
        └── Row: Application     → HTTP rate, latency, status panels

⚠️ Save Dashboard after EVERY change — no auto-save
```

***

## Query-to-Panel Mapping (Complete Reference)

```
SYSTEM HEALTH:
┌─────────────────────────┬─────────────────┬──────────────────────────────────────────────────────────┐
│ Panel                   │ Viz Type        │ Query                                                    │
├─────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────┤
│ CPU Utilization (%)     │ Time series     │ 100-(avg by(instance)(irate(cpu{idle}[5m]))*100)         │
│ Available Memory (MB)   │ Gauge           │ node_memory_MemAvailable / 1024^2                        │
│ Available Memory (%)    │ Gauge           │ (MemAvailable / MemTotal) * 100                          │
│ Load Average (1m)       │ Time series     │ node_load1                                               │
├─────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────┤
│ Root Disk Usage (%)     │ Time series     │ (1 - (avail{mp="/"} / size{mp="/"})) * 100               │
│ Disk Read Rate          │ Time series     │ rate(disk_reads_completed_total[2m])                      │
├─────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────┤
│ HTTP Request Rate       │ Time series     │ rate(http_requests_total[1m])                             │
│ Total Requests          │ Stat            │ sum by (endpoint) (http_requests_total)                   │
├─────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────┤
│ Avg Request Duration    │ Time series     │ rate(duration_sum[1m]) / rate(duration_count[1m])         │
│ Requests by Endpoint    │ Bar chart       │ increase(http_requests_total[5m])                         │
├─────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────┤
│ Service Status          │ Stat            │ up{job="webserver-appstat"}                               │
└─────────────────────────┴─────────────────┴──────────────────────────────────────────────────────────┘
```

***

## CPU Query Deconstruction (Layer Stack)

```
Layer 7:  100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
Layer 6:  100 - (...)                              ← invert: idle% → usage%
Layer 5:  (...) * 100                              ← fraction → percentage
Layer 4:  irate(...[5m])                           ← rate of change per second
Layer 3:  node_cpu_seconds_total{mode="idle"}[5m]  ← range vector (5min window)
Layer 2:  node_cpu_seconds_total{mode="idle"}      ← filter to idle mode only
Layer 1:  node_cpu_seconds_total                   ← raw counter (all CPU modes)
Layer 0:  avg by (instance)                        ← group per instance (multi-node)
```

***

## Unit Conversion Pattern

```
bytes → KB:  / 1024      (or / 1024^1)
bytes → MB:  / 1024^2
bytes → GB:  / 1024^3

^ = caret = Shift+6 = exponentiation operator in PromQL
```

***

## Label Filtering Syntax

```
metric{label="value"}              ← exact match
metric{label=~"regex"}             ← regex match (used with $variables)
metric{label!="value"}             ← not equal
metric{label!~"regex"}             ← negative regex

Job name MUST match Prometheus config exactly
Verify with: up → check job labels in output
```

***

## Counter vs Gauge — Query Pattern Rule

```
COUNTER (only increases):
  → MUST use rate() / irate() / increase()
  → Raw value = meaningless cumulative total
  Examples: node_cpu_seconds_total, http_requests_total, disk_reads_completed_total

GAUGE (goes up and down):
  → Use raw value directly (or delta() for change)
  → Represents current state
  Examples: node_memory_MemAvailable_bytes, node_load1, up
```

***

## Three Reusable Query Patterns

```
PERCENTAGE (part/whole):
  (part / whole) * 100              ← free/available %
  (1 - (part / whole)) * 100       ← usage % (inverted)

RATE (counter → per-second):
  rate(counter[window])             ← smoothed rate
  irate(counter[window])           ← instant rate (spiky)

AVERAGE DURATION (sum/count):
  rate(duration_sum[window]) / rate(duration_count[window])
  ← total time / total requests = avg time per request
```

***

## Inversion Pattern (Critical)

```
Idle → Usage:     100 - idle%
Free → Used:      1 - (free/total)   then * 100
Available → Used: (1 - (avail/total)) * 100

Same pattern for CPU, Disk, Memory usage calculations
```

***

## Legend Template Syntax

```
{{instance}}    → inserts instance label value (e.g., web01:9100)
{{endpoint}}    → inserts endpoint label value (e.g., /)
{{device}}      → inserts device label value (e.g., sda)
{{app}}         → inserts app label value

Format: {{label_name}} - Static Text
Result: web01:9100 - CPU Usage
```

***

## Advanced Panel Patterns

```
DYNAMIC VARIABLE:
  Query: ...{endpoint=~"$endpoint"}
  $endpoint = Grafana dashboard variable → dropdown selector
  =~ = regex match (required for variable interpolation)

OFFSET COMPARISON (two queries, one panel):
  Query A: rate(metric[1m])                 ← current
  Query B: rate(metric[1m] offset 5m)       ← 5 min ago
  → two lines on same graph → visual trend
```

***

## Visualization Type Selection

```
Time series  → values over time (CPU%, load, request rate, disk usage)
Gauge        → current single value with thresholds (memory available)
Stat         → single number display (total requests, up/down status)
Bar chart    → comparison across categories (requests per endpoint)
```

***

## Query Debugging Checklist

```
Empty results?
  1. Job name matches Prometheus config?     → run 'up' to verify
  2. Metric name spelled correctly?          → check exact name in Prometheus
  3. Target is UP?                           → check Status → Targets
  4. Label values correct?                   → case-sensitive, exact match
  5. Parentheses balanced?                   → editor highlights matches
```

***

## Query Decoding Workflow (Reusable)

```
1. Start with raw metric name alone        → see what it returns
2. Add label filter {job="..."}            → narrow to target
3. Add range [5m] if needed                → for rate/increase functions
4. Wrap in function (rate/irate/increase)  → transform counter to rate
5. Apply arithmetic (* 100, / 1024^2)      → unit conversion
6. Apply inversion (100 - ...)             → usage instead of free
7. Add aggregation (avg by / sum by)       → group for multi-instance

Each layer: execute → verify → add next layer
Never build the full query blindly
```

***

## Key Engineering Patterns

| Pattern                              | Manifestation                                                                       |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| **Folder → Dashboard → Row → Panel** | Hierarchical organization mirrors project → environment → category → metric         |
| **Query is the essence**             | Panel is just a container; the PromQL query determines all data                     |
| **Decode layer by layer**            | Build complex queries from raw metric outward, testing each addition                |
| **Label = filter**                   | Curly brace filtering selects specific targets from thousands                       |
| **Counter → rate → percentage**      | Universal pattern for any cumulative metric → human-readable display                |
| **Inversion pattern**                | `100 - idle` / `1 - free/total` — same logic for CPU, disk, memory                  |
| **Job name alignment**               | Query labels must exactly match Prometheus scrape config — verify before copy-paste |

***

## Project Continuity

```
BEFORE: PromQL fundamentals — data types, operators, functions (lecture 256)
THIS:   Organized dashboard + decoded all panel queries + tested in Prometheus/Grafana
NEXT:   Create actual Grafana panels using these queries (visual panels)
```

***

This completes the full reconstruction. **Theory** explains the dashboard hierarchy, label filtering, unit conversion, and CPU query deconstruction. **Practical** walks through every decoding step and testing workflow. The **Compression Map** gives you the complete panel-query reference table, the layer-by-layer CPU deconstruction, and reusable patterns for instant recall during Grafana panel creation. Let me know if you'd like Anki flashcards or any section expanded! 🚀
