# Grafana Panels and Dashboards — Building Real Monitoring Visualizations

**Source:** Video caption file — *"Building Grafana Panels and Dashboards"*, with supplementary panel query reference sheet [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt), [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is a Grafana Panel and Why It Exists

A Grafana **panel** is the fundamental visualization unit — a single chart, gauge, stat counter, or bar chart that displays the result of one or more Prometheus queries. Everything you see on a Grafana dashboard is made of panels. Each panel asks a specific question ("What is the CPU utilization right now?", "How many HTTP requests are hitting the server per second?") and displays the answer visually using time series data from Prometheus. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

Panels exist because raw Prometheus metrics — numbers scraped every 15 seconds and stored in a time series database — are useless for human decision-making in their raw form. A panel transforms those numbers into a visual representation that reveals trends, anomalies, and thresholds at a glance. The entire purpose of Grafana is to be the **visualization layer** on top of Prometheus's data storage layer. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## 1.2 — Dashboard Organization: Folders, Dashboards, Rows, Panels

Grafana has a four-level organizational hierarchy that maps to how real monitoring environments are structured: [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

**Folder** → A top-level container that groups related dashboards. The video uses a folder called `Titan monitoring`. In real environments, folders might represent teams, projects, or environments.

**Dashboard** → A collection of panels. The video creates a dashboard called `Titan prod` inside the `Titan monitoring` folder — this dashboard is for "all the production systems."

**Row** → A collapsible section within a dashboard that groups related panels. The video uses two rows: `application` (for HTTP/request-level panels) and `system` (for CPU, memory, disk panels). Rows create visual and logical separation within a single dashboard.

**Panel** → The individual visualization — one query (or multiple queries), one chart. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

This hierarchy — folder → dashboard → row → panel — mirrors how monitoring is structured in real organizations: you group by project/team, then by environment (prod/staging), then by monitoring category (system vs. application), then by individual metric. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## 1.3 — Visualization Types: Choosing the Right Display

Different metrics demand different visual representations. The video covers four visualization types, each suited to a specific kind of data: [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt), [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

**Time Series** — The most common visualization in DevOps monitoring. Displays metric values as lines over time (X-axis = time, Y-axis = value). Used for anything that changes continuously: CPU utilization, request rate, load average, disk read rate. The video states: "Most of the monitoring panels you will see related to our software, DevOps application, you will see mostly time series." [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

**Gauge** — Displays a single current value on a speedometer-like dial. Best for metrics that represent a percentage or a value within a known range. The video uses it for available memory percentage — the gauge immediately shows whether memory is in a safe zone, warning zone, or danger zone. Gauges are especially powerful when combined with **thresholds** (see Theory 1.7). [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

**Stat** — Displays a single number prominently. Used for values where the number itself is the message: total request count, service up/down status (1 or 0). The reference sheet shows `up{job="webserver-appstat"}` displayed as a Stat — the value is either 1 (up) or 0 (down). [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

**Bar Chart** — Displays values as horizontal or vertical bars. Used for comparing discrete categories. The reference sheet uses it for "Requests by Endpoint (Last 5m)" — comparing how many requests each endpoint received. [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

***

## 1.4 — The Query: Prometheus Metric Queries in Grafana

Every panel is driven by one or more **Prometheus queries** (PromQL). The query is what connects the panel to actual data. In Grafana's panel editor, you have two modes for writing queries: **Builder** (a GUI form) and **Code** (raw PromQL text). The video explicitly instructs: "You might have selected here Builder. Instead of that, select Code and paste your query here." The Code mode gives you full control over the query syntax. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

The queries themselves use Prometheus metrics and functions. Understanding the key query patterns used in the video is essential:

### `irate()` for CPU Utilization

```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

This is the standard CPU utilization query. `node_cpu_seconds_total{mode="idle"}` measures how much time the CPU spends idle. `irate(...[5m])` calculates the per-second rate of change over a 5-minute window. Multiplying by 100 converts to percentage. Subtracting from 100 inverts the result: instead of "how much is idle" you get "how much is busy." The `avg by (instance)` averages across all CPU cores for each instance. [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

### `rate()` for Request Rate

```promql
rate(http_requests_total{job="webserver-appstat"}[1m])
```

`http_requests_total` is a counter (it only goes up). `rate(...[1m])` calculates the per-second rate of increase over a 1-minute window — converting a raw counter into "requests per second." This is the standard way to visualize throughput for any counter metric. [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

### Division for Average Duration

```promql
rate(http_request_duration_seconds_sum{job="webserver-appstat"}[1m]) / rate(http_request_duration_seconds_count{job="webserver-appstat"}[1m])
```

This calculates average request duration by dividing the total accumulated duration by the total count of requests. Both are counters, so `rate()` is applied to both before dividing. This pattern — `rate(sum) / rate(count)` — is the standard PromQL pattern for computing averages from summary or histogram metrics. [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

### `increase()` for Totals Over a Window

```promql
increase(http_requests_total{job="webserver-appstat"}[5m])
```

`increase()` returns the total increase in a counter over the specified time window. Unlike `rate()` which gives per-second values, `increase()` gives the absolute count over the window. Used in the bar chart to show "total requests per endpoint in the last 5 minutes." [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

### `offset` for Time Comparison

```promql
rate(http_requests_total{job="webserver-appstat", endpoint="/"}[1m] offset 5m)
```

The `offset` keyword shifts the query backward in time. This query returns the request rate from **5 minutes ago**. By running the same query with and without `offset` as two separate queries in the same panel, you can visually compare current performance against historical performance — seeing both lines on the same graph. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt), [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

***

## 1.5 — Legends: Labeling What You See

When a panel displays multiple lines (multiple instances, multiple endpoints), you need to know which line represents what. **Legends** are the labels displayed alongside each line in the graph. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

By default, Grafana uses `Auto` legends which show all Prometheus labels — often producing long, unreadable strings. The video switches to **Custom** legends and uses Prometheus label variables inside double curly braces: [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

```
{{instance}} - CPU Usage
{{endpoint}} - {{app}}
```

`{{instance}}` is replaced at runtime with the value of the `instance` label from the Prometheus metric (e.g., the IP address and port). `{{endpoint}}` is replaced with the endpoint value (`/` or `/payment`). `{{app}}` is replaced with the app label value. Any text outside the curly braces is treated as a literal string — so `- CPU Usage` just appears as-is. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

This is a **template substitution** pattern: you mix literal text with dynamic label values to create readable, informative legends.

***

## 1.6 — Multiple Queries in a Single Panel

A panel is not limited to one query. You can add **multiple queries** (labeled A, B, C, D, etc.) and all results appear on the same graph. The video demonstrates this with the `offset` comparison: Query A shows the current request rate, Query B shows the request rate from 5 minutes ago, and both lines appear together for visual comparison. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

The video notes this is not only for offset comparisons: "You can use it for other — one query you can have for slash, the other one can have for slash payment. So you can have query A, B, C, D in one graph." Any combination of queries can be layered in a single panel. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

You can also **hide/show** individual queries using the eye icon next to each query. This lets you temporarily isolate one line to understand it before showing all lines together. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## 1.7 — Thresholds: Color-Coded Health Zones

Thresholds transform a gauge (or other visualization) from a plain number into a **health indicator** by assigning colors to value ranges. The video demonstrates this with the available memory percentage gauge: [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

* Below 20% → **Dark Red** (extremely dangerous — system nearly out of memory)
* 20% to 50% → **Red/Warning**
* 50% to 70% → **Orange** (caution)
* Above 70% → **Green** (healthy — plenty of memory available) [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

With thresholds set, the gauge color changes automatically as the value moves between zones. A quick glance at the gauge color tells you the health state without reading the actual number. This is the visual equivalent of alert levels — green means safe, red means act immediately. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

The video notes that setting thresholds well takes practice: "This takes me some time to set this." The exact threshold values depend on the specific metric and the system's capacity — there's no universal "right" threshold for memory or CPU. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## 1.8 — Dynamic Variables: Interactive Dashboard Filtering

This is the most powerful dashboard feature covered in the lecture. A **dynamic variable** is a dropdown selector on the dashboard that lets you filter which data panels display — without editing the panel queries manually. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

The variable is defined at the **dashboard level** (Settings → Variables → Add Variable). You give it a name (e.g., `endpoint`), a label (e.g., `Endpoint`), and a **query** that generates its possible values dynamically from Prometheus. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

The query used in the video:

```promql
label_values(http_requests_total, endpoint)
```

`label_values()` is a special Grafana function (not PromQL) that returns all unique values of a specific label from a metric. For `http_requests_total` with the label `endpoint`, it returns `["/", "/payment"]` — the two endpoints being monitored. These become the dropdown options. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

Once the variable exists, panels use it in their queries with the `$variable_name` syntax:

```promql
sum by (endpoint) (http_requests_total{job="webserver-appstat", endpoint=~"$endpoint"})
```

The `$endpoint` is replaced at runtime with whatever value is selected in the dropdown. When you select `/`, only root endpoint data shows. When you select `/payment`, only payment data shows. The `=~` operator enables regex matching, which supports multi-select. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

The variable is **dynamic** because its values come from a query that runs at dashboard load time. If new endpoints are added to the application, they automatically appear in the dropdown without any dashboard configuration changes. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

🔍 **Deep Dive:**
Dynamic variables transform a static dashboard into an interactive exploration tool. Instead of creating separate panels for each endpoint (or each server, or each region), you create one panel with a variable filter and let the user select what to view. This scales dramatically better — one panel with a variable serves the same purpose as N panels for N endpoints. In real production dashboards, you'll commonly see variables for `instance`, `job`, `namespace`, `pod`, `region`, and other dimensions. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## 1.9 — Panel Configuration Options

The video touches on several panel customization options: [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

**Graph Styles** — In the Time Series visualization, you can change line styles: smooth lines, stepped lines, or default. This is aesthetic but can affect readability for certain metrics.

**Transparent Background** — A checkbox that removes the panel's background color, making it blend into the dashboard. Used on the memory gauge.

**Standard Options → Unit** — You can set the unit of measurement for the displayed values. The video searches for "percentage 0-100" to format the memory gauge correctly. This ensures values display with the right suffix (%, MB, req/s, etc.). [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## 1.10 — Label Consistency: The Foundation of Correct Queries

The video opens with a critical warning: "Make sure you have the right label names. Compare and check from your Prometheus what name you have given. Make sure you have that label." [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

Every query in the reference sheet uses labels like `job="webserver-system"`, `job="webserver-appstat"`, `job="node"`. These labels were defined in the Prometheus configuration (`prometheus.yml`) when targets were set up. If your label names don't match the queries, the queries return empty results — no errors, just no data. This is the most common source of "empty panel" problems. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a complete Grafana monitoring dashboard with multiple panels organized into rows, covering system health metrics (CPU, memory) and application metrics (HTTP request rate, latency), including a multi-query comparison panel and a dynamic variable-filtered panel. The final outcome: a `Titan prod` dashboard inside the `Titan monitoring` folder, with `system` and `application` rows containing interactive, threshold-colored panels driven by Prometheus queries. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Pre-Requisite Check: Ensure Load Scripts Are Running

**What we are doing:** Verifying that the background scripts generating test traffic are active on the web server.

**Why:** The panels we're building query HTTP request metrics. If no requests are being made, the panels show no data.

**Verification command (on the web server node via SSH):**

```bash
ps -ef | grep load.sh
```

**Expected output:** You should see the `load.sh` process running in the background. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

**If NOT running (e.g., after a reboot):**

```bash
nohup ./load.sh &
```

**Breakdown:**

* `nohup` — prevents the script from stopping when you close the SSH session.
* `./load.sh` — the script path (located where it was copied from the GitHub repository).
* `&` — runs the process in the background. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

**Important:** "Wait for a minimum ten minutes before you continue" — the script needs time to generate enough metric data points for meaningful graphs.

**Also verify on the Prometheus server:** Two scripts should be running — one for the root endpoint (`/`) and one for the payment endpoint (`/payment`). These scripts access the web server URLs to generate HTTP traffic. They can be run from any machine that can reach the web server — Prometheus server, Grafana server, or anywhere else. Just ensure the script contains the correct web server IP address. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Panel 1: CPU Utilization (%) — Time Series

**What we are doing:** Creating the first system health panel showing CPU usage over time.

### Step 1: Add Visualization

Navigate to: Dashboards → `Titan monitoring` folder → `Titan prod` dashboard → **Add Visualization**. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 2: Configure the Query

1. **Data Source:** Confirm `Prometheus` is selected.
2. **Query mode:** Click **Code** (not Builder) to enter raw PromQL.
3. **Paste the query:**

```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

4. Click **Run Query**.
5. **Time range:** Change from "Last 6 hours" to **Last 5 minutes** using the dropdown for a more readable view. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 3: Configure the Legend

Go to **Options → Legend → Custom** and enter:

```
{{instance}} - CPU Usage
```

This displays the instance's IP:port followed by "- CPU Usage" as the line label. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 4: Set Panel Title

Title: `CPU Utilization (%)` [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 5: Save and Organize

1. Click **Save Dashboard** → Save.
2. Go back to the dashboard.
3. Enter **Edit mode** (required for drag-and-drop — "if you're not in the edit, you cannot drag and drop").
4. Drag the panel into the **system** row.
5. Save dashboard again. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Panel 2: Available Memory (%) — Gauge with Thresholds

**What we are doing:** Creating a gauge panel showing available memory as a percentage with color-coded health zones.

### Step 1: Add Visualization and Set Query

1. Click **Add Visualization**.
2. Select **Code** mode, paste the percentage query:

```promql
(node_memory_MemAvailable_bytes{job="webserver-system"} / node_memory_MemTotal_bytes{job="webserver-system"}) * 100
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

3. Run Query.

### Step 2: Change Visualization Type

Switch from **Time Series** to **Gauge**. The display changes to a speedometer-style dial. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 3: Configure Legend

Options → Legend → Custom: `{{app}} - Mem Available` [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 4: Set Unit

In **Standard Options**, search for `percent (0-100)` and select it. The gauge now correctly displays values as percentages. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 5: Configure Thresholds

Scroll to the **Thresholds** section. Add color zones:

| Value Range                                                                                                                                                                                                      | Color    | Meaning             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------- |
| Base (0-20%)                                                                                                                                                                                                     | Dark Red | Extremely dangerous |
| 20%                                                                                                                                                                                                              | Red      | Critical            |
| 50%                                                                                                                                                                                                              | Orange   | Warning             |
| 70%                                                                                                                                                                                                              | Green    | Healthy             |
|  [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt) |          |                     |

**How to set:** Click "Add threshold", enter the value, click the color swatch to choose the color. The gauge dynamically changes color based on the current value.

### Step 6: Optional — Enable Transparent Background

Check **Transparent Background** for a cleaner look. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 7: Set Title, Save, Organize

Title: `Available Memory (%)`. Save dashboard. Drag into the **system** row. Resize panels by dragging their edges to fit side by side. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Panel 3: HTTP Request Rate — Time Series (Application Row)

**What we are doing:** Creating an application-level panel showing HTTP requests per second, separated by endpoint.

### Step 1: Add Visualization with Query

```promql
rate(http_requests_total{job="webserver-appstat"}[1m])
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

Run Query. You should see lines for both endpoints (`/` and `/payment`). [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 2: Configure Legend

Options → Legend → Custom:

```
{{endpoint}} - {{app}}
```

This shows which endpoint each line represents (e.g., `/ - webserver-appstat`). [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 3: Set Title, Save, Organize

Title: `HTTP Request Rate (req/sec)`. Save. Drag into the **application** row. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Panel 4: Endpoint Request Comparison (Current vs. 5 Minutes Ago) — Multi-Query

**What we are doing:** Creating a panel with two queries in the same graph — current request rate and the rate from 5 minutes ago — to enable visual comparison.

### Step 1: Add Visualization with Query A (Current)

```promql
rate(http_requests_total{job="webserver-appstat", endpoint="/"}[1m])
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

Run Query.

### Step 2: Add Query B (5 Minutes Ago)

Click **Add Query** (creates Query B).

```promql
rate(http_requests_total{job="webserver-appstat", endpoint="/"}[1m] offset 5m)
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

Run Query. Both lines appear on the same graph. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 3: Configure Legends for Clarity

**Query A** → Options → Legend → Custom:

```
{{endpoint}} - {{app}} - current
```

**Query B** → Options → Legend → Custom:

```
{{endpoint}} - {{app}} - 5 minutes older
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 4: Use Hide/Show to Verify

Click the **eye icon** next to a query to temporarily hide its line. This helps you identify which line is which before setting final legends. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 5: Set Title, Save, Organize

Title: `Endpoint Request - Now and Older`. Save. Drag into **application** row. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Panel 5: Dynamic Variable Panel — Interactive Filtering

**What we are doing:** Creating a dashboard-level variable that enables a dropdown selector for endpoints, then building a panel that responds to the selection.

### Step 1: Create the Variable

1. From the dashboard, click **Settings** (gear icon).
2. Go to **Variables → Add Variable**.
3. Configure:
   * **Name:** `endpoint`
   * **Label:** `Endpoint` (display label in the dropdown)
   * **Type:** Query
   * **Data Source:** Prometheus
   * **Query:**

```promql
label_values(http_requests_total, endpoint)
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

4. Scroll down — you should see the preview values (`/` and `/payment`).
5. Click **Run Query** to verify.
6. **Save Dashboard**. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 2: Create the Panel Using the Variable

Add Visualization. Paste the variable-filtered query:

```promql
sum by (endpoint) (http_requests_total{job="webserver-appstat", endpoint=~"$endpoint"})
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

**Breakdown:**

* `endpoint=~"$endpoint"` — the `=~` operator does regex matching. `$endpoint` is replaced with the dashboard variable's current value at runtime.
* `sum by (endpoint)` — aggregates the total by endpoint.

Run Query. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 3: Test the Dropdown

At the top of the dashboard, the `Endpoint` dropdown should now appear. Select `/` — only root endpoint data shows. Select `/payment` — only payment data shows. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

### Step 4: Set Title, Save, Organize

Title: `Dynamic Variable Panel` (for learning; in production, use a descriptive name like "HTTP Total Request Count by Endpoint"). Save. Drag into **application** row. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

⚠️ **Expert Note:**
Dynamic variables are the key to building dashboards that scale. In production, you'll commonly create variables for `instance`, `job`, `namespace`, `pod`, `environment`, etc. One dashboard with 3-4 variables can serve hundreds of different views, eliminating the need for separate dashboards per server/service/environment. [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Grafana Panels and Dashboards
PURPOSE:  Transform Prometheus metrics into visual monitoring panels
CONTEXT:  Hands-on lecture after Prometheus setup + Node Exporter + App metrics
OUTPUT:   Titan prod dashboard with system + application rows, 5+ panels
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Dashboard Organization Hierarchy

```
Folder: Titan monitoring
  └── Dashboard: Titan prod
        ├── Row: system
        │     ├── Panel: CPU Utilization (%)         [Time Series]
        │     └── Panel: Available Memory (%)        [Gauge + Thresholds]
        └── Row: application
              ├── Panel: HTTP Request Rate (req/sec)  [Time Series]
              ├── Panel: Endpoint Request Now & Older [Time Series, 2 queries]
              └── Panel: Dynamic Variable Panel       [Time Series, $variable]
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Panel Creation Flow

```
Add Visualization
  │
  ├── Select Data Source: Prometheus
  ├── Switch to Code mode (not Builder)
  ├── Paste PromQL query → Run Query
  ├── Choose Visualization Type (time series / gauge / stat / bar)
  ├── Configure Legend (Custom: {{label}} - text)
  ├── Set Thresholds (if gauge)
  ├── Set Unit (if applicable)
  ├── Set Panel Title
  │
  ▼
Save Dashboard → Enter Edit Mode → Drag panel into correct Row → Save
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Visualization Type Selection

```
DATA PATTERN                    VIZ TYPE        EXAMPLE
──────────────                  ────────        ───────
Continuous value over time      Time Series     CPU %, request rate
Single current value (ranged)   Gauge           Memory available %
Single prominent number         Stat            Up/Down status, total count
Category comparison             Bar Chart       Requests per endpoint
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt), [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

***

## Key PromQL Patterns (Query Reference)

```
PATTERN                         USE CASE                    EXAMPLE
───────                         ────────                    ───────
rate(counter[window])           Per-second rate of counter  rate(http_requests_total[1m])
irate(counter[window])          Instant rate (spiky data)   irate(node_cpu_seconds_total[5m])
increase(counter[window])       Total increase in window    increase(http_requests_total[5m])
100 - (idle_rate * 100)         CPU utilization (invert)    100 - (avg(irate(cpu_idle[5m]))*100)
rate(sum) / rate(count)         Average from summary        rate(duration_sum[1m])/rate(duration_count[1m])
metric offset Xm               Time-shifted comparison     rate(metric[1m] offset 5m)
label_values(metric, label)     Dynamic variable values     label_values(http_requests_total, endpoint)
metric{label=~"$var"}           Variable-filtered query     http_requests_total{endpoint=~"$endpoint"}
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true), [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Panel Query Reference (Complete)

```
PANEL                    VIZ        QUERY (simplified)
─────                    ───        ─────
CPU Utilization          TimeSeries 100 - (avg(irate(cpu_idle[5m])) * 100)
Memory Available (MB)    Gauge      mem_available_bytes / 1024^2
Memory Available (%)     Gauge      mem_available / mem_total * 100
Load Average (1m)        TimeSeries node_load1
Root Disk Usage (%)      TimeSeries (1 - avail/size) * 100
Disk Read Rate           TimeSeries rate(disk_reads_completed[2m])
HTTP Request Rate        TimeSeries rate(http_requests_total[1m])
Total Requests           Stat       sum by (endpoint)(http_requests_total)
Avg Request Duration     TimeSeries rate(duration_sum[1m]) / rate(duration_count[1m])
Requests by Endpoint     BarChart   increase(http_requests_total[5m])
Service Status           Stat       up{job="webserver-appstat"}
Dynamic Variable         TimeSeries sum by (endpoint)(requests{endpoint=~"$endpoint"})
Current vs Offset        TimeSeries Query A: rate(...[1m]) / Query B: rate(...[1m] offset 5m)
```

 [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

***

## Legend Template Syntax

```
SYNTAX:  {{label_name}} - literal text

EXAMPLES:
  {{instance}} - CPU Usage      → "10.0.0.5:9100 - CPU Usage"
  {{endpoint}} - {{app}}        → "/ - webserver-appstat"
  {{endpoint}} - current        → "/ - current"
  {{endpoint}} - 5 min older    → "/ - 5 min older"

SET VIA: Options → Legend → Custom
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Threshold Configuration (Gauge)

```
Available Memory (%):

  0%  ─────── 20% ─────── 50% ─────── 70% ─────── 100%
  │  DARK RED  │   RED    │  ORANGE   │   GREEN    │
  │ (critical) │(warning) │ (caution) │ (healthy)  │

SET VIA: Panel editor → Thresholds → Add threshold → Set value + color
EFFECT: Gauge color changes automatically as value crosses thresholds
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Multi-Query Panel (Offset Comparison)

```
Query A: rate(http_requests_total{endpoint="/"}[1m])           → CURRENT
Query B: rate(http_requests_total{endpoint="/"}[1m] offset 5m) → 5 MIN AGO

BOTH on same graph → visual comparison of current vs. historical
Legend A: "/ - current"
Legend B: "/ - 5 minutes older"

GENERALIZED:
  offset 1h  → 1 hour ago
  offset 1d  → 1 day ago
  Can add Query C, D for more comparisons or different endpoints
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Dynamic Variable Architecture

```
DEFINITION (Dashboard Settings → Variables):
  Name:   endpoint
  Label:  Endpoint
  Type:   Query
  Source: Prometheus
  Query:  label_values(http_requests_total, endpoint)
  Values: ["/", "/payment"]  ← generated dynamically at load time

USAGE (in Panel Query):
  http_requests_total{endpoint=~"$endpoint"}
  $endpoint → replaced with dropdown selection at runtime

RESULT:
  Dashboard shows dropdown → user selects endpoint → panel filters automatically

SCALING BENEFIT:
  1 panel + 1 variable = replaces N separate panels (one per endpoint)
  New endpoints auto-appear in dropdown (no dashboard changes needed)
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Drag-and-Drop Rule

```
EDIT MODE:    Can drag panels between rows ✅
VIEW MODE:    Cannot drag panels ❌

WORKFLOW: Enter edit mode → drag panel to correct row → save → exit edit mode
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Label Consistency Warning

```
QUERY USES:        job="webserver-system", job="webserver-appstat"
THESE MUST MATCH:  Labels defined in prometheus.yml scrape config

SYMPTOM IF WRONG:  Panel shows no data (no error, just empty)
FIX:               Check Prometheus targets → verify label names → update queries
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Pre-Requisite Check

```
BEFORE CREATING PANELS:
  1. Verify load.sh is running on web server:
       ps -ef | grep load.sh
  2. If not running (after reboot):
       nohup ./load.sh &
  3. Verify traffic scripts running on Prometheus server:
       ps -ef | grep script_name
  4. If not running:
       nohup ./script_path &
  5. Wait 10 minutes for metrics to accumulate
```

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt)

***

## Reusable Engineering Patterns

| Pattern                            | Manifestation                                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Hierarchical Organization**      | Folder → Dashboard → Row → Panel = mirrors team/env/category/metric                            |
| **Query-Driven Visualization**     | Every panel is defined by its PromQL query — change query, change panel                        |
| **Visualization-to-Data Matching** | Time series for trends, Gauge for ranges, Stat for single values, Bar for comparison           |
| **Template Variables for Scaling** | One panel + `$variable` dropdown replaces N static panels                                      |
| **Threshold-Based Health Coding**  | Color zones on gauges = instant visual health assessment without reading numbers               |
| **Offset for Time Comparison**     | Same query + `offset` = current vs. historical on one graph                                    |
| **Multi-Query Composition**        | Queries A, B, C, D in one panel = layered analysis in single view                              |
| **Label-Driven Filtering**         | Prometheus labels (`job`, `endpoint`, `instance`) are the filtering vocabulary for all queries |
| **Dynamic Value Generation**       | `label_values()` generates dropdown options from live data — auto-updates as system changes    |

 [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt), [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

***

## One-Line System Reconstruction

> **Grafana panels are PromQL-driven visualizations (time series/gauge/stat/bar) organized in folders → dashboards → rows, configured via Code mode queries with custom `{{label}}` legends, enhanced with gauge thresholds for color-coded health zones, multi-query panels for offset-based time comparison (Query A current vs. Query B with `offset 5m`), and dashboard-level dynamic variables (`label_values()` → `$variable` in queries) that create interactive dropdown filtering — all dependent on matching Prometheus label names exactly.** [\[260-buildi...dashboards \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/260-building-grafana-panels-and-dashboards.txt), [\[260.Grafan...ueries (1) \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B9115E70C-C93F-475A-9085-199FD406B423%7D&file=260.GrafanaPanelQueries%20%281%29.xlsx&action=default&mobileredirect=true)

***

This completes the full reconstruction of the Building Grafana Panels and Dashboards lecture. It connects directly to the Prometheus and monitoring introduction lectures — the metrics being queried were set up in those sessions, and the panels built here are the visual layer that makes those metrics operationally useful. The next lecture covers Grafana notifications/alerting. Let me know if you'd like any section expanded or adjusted! 🚀
