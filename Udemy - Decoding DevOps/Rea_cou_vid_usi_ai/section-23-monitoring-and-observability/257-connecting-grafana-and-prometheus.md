# 🎓 Deep Learning Material: Connecting Grafana and Prometheus

**Source:** [257-connecting-grafana-and-prometheus.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt?EntityRepresentationId=2854948c-5498-4aed-aeb1-18e1bb091ba4) — Video lecture covering Grafana's role as a visualization layer, connecting Grafana to Prometheus as a data source, security group requirements between Grafana and Prometheus EC2 instances, the Explore interface for running PromQL queries, builder vs code query modes, multiple query panels, and verification of the end-to-end data pipeline. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why Grafana Exists — The Visualization Problem

In the previous lecture, PromQL queries were executed directly in the Prometheus web UI. The results were functional but not readable — raw numbers, Unix timestamps, lists of label-value pairs. Prometheus was never designed for visual presentation. It was designed to **collect and store** metrics in a structured format. Reading those metrics in a way that enables operational decisions — spotting trends, identifying anomalies, comparing baselines — requires a dedicated **visualization tool**. That tool is Grafana. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

Grafana reads the structured metric data that Prometheus stores and presents it as **dashboards** — collections of visual panels (graphs, bar charts, gauges, tables) that can be customized for any monitoring use case. In production environments, NOC (Network Operations Center) and SOC (Security Operations Center) teams who monitor infrastructure 24/7 typically have Grafana dashboards displayed on their screens continuously. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

Beyond visualization, Grafana also provides **alert notifications** — the ability to trigger alerts based on metric conditions and send them to communication channels like Slack, email, or PagerDuty. The video foreshadows this: Slack will be connected as a "contact point" for notifications in the next lecture. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## 1.2 Grafana's Data Source Architecture — Not Just Prometheus

The most important architectural concept is that Grafana is **data-source agnostic**. It is not a Prometheus-specific tool. When you add a data source in Grafana, you choose from a large list of supported backends: Prometheus, InfluxDB, Loki (for logs), Elasticsearch, Jaeger, Tempo, Zipkin (for distributed tracing), SQL databases, cloud monitoring services like **AWS CloudWatch** and **Azure Monitor**, and even **Grafana Cloud** (a managed SaaS offering where you pay a subscription instead of hosting your own Grafana). [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

This means the dashboarding skills you build with Prometheus transfer directly to any other data source. The panel types, visualization options, alerting rules, and dashboard organization are all the same — only the query language changes based on the backend. For Prometheus, the query language is PromQL. For CloudWatch, it would be CloudWatch query syntax. For SQL databases, it would be SQL. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

When you have **multiple Prometheus servers** (common in large organizations where different teams or environments have separate Prometheus instances), you can add each as a separate data source in Grafana and name them distinctively. Panels on a dashboard can pull data from different data sources, enabling a single dashboard to aggregate views across multiple monitoring backends. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## 1.3 The Connection Model — Grafana to Prometheus

Grafana connects to Prometheus over **HTTP**. The connection URL follows the format: `http://<prometheus-ip>:<port>`. In this setup, both Grafana and Prometheus run on separate EC2 instances within the **same network** (same VPC). Because they share a network, the connection uses the **private IP** of the Prometheus server, not the public IP. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

The instructor explicitly explains why: when you stop and restart EC2 instances (to save costs during learning), the **public IP changes** but the **private IP stays the same**. If you configure the data source with the public IP, the connection breaks every time the instance restarts. Using the private IP ensures the connection remains stable across power cycles. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

Prometheus in this setup listens on port **9090** (the video references port 1990, which appears to be a custom port configured in this specific course setup). The key point is: whatever port Prometheus listens on, that port must be open in the Prometheus instance's **security group** to allow traffic from the Grafana instance. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## 1.4 Security Group Chain — Grafana to Prometheus

The network access between Grafana and Prometheus is controlled by AWS security groups. The Prometheus security group must have an **inbound rule** allowing traffic on the Prometheus port (1990 in this setup) **from the Grafana security group**. This is the secure approach — it restricts access to only the Grafana instance. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

The instructor provides a troubleshooting fallback: if you're having connection issues and suspect the security group, temporarily create a rule allowing the Prometheus port from **anywhere** (`0.0.0.0/0`). If that works, the issue was the security group reference. Fix it properly and remove the open rule. But the production-correct configuration is: Prometheus port allowed only from Grafana's security group. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

The video also notes that if you return after a day or more, your **local IP** may have changed. Since the Grafana security group allows port 3000 from "My IP," you need to **update that rule** with your current IP before accessing Grafana's web UI. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## 1.5 Authentication on Prometheus — Current vs Production

In this learning setup, Prometheus has **no authentication** — anyone who can reach the URL gets access. When configuring the data source in Grafana, the authentication section is left as "no authentication." [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

The instructor explicitly notes this would not be the case in real production environments. In production, Prometheus would have authentication — either **basic authentication** (username/password) or **OAuth token-based** authentication. Grafana's data source configuration supports all these methods. You select the authentication type and provide credentials accordingly. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## 1.6 The Explore Interface — Query Testing Before Dashboard Building

After connecting the data source, Grafana provides an **Explore** interface — a sandbox for running PromQL queries and seeing results before committing them to dashboard panels. You access it by clicking on the data source and selecting "Explore." [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

The Explore interface has two query modes:

**Builder mode** — A visual, dropdown-based interface where you select the metric name from a dropdown, then select label filters (e.g., label: `endpoint`, value: `payment`). Grafana constructs the PromQL query for you. This is helpful for discovering available metrics and labels without memorizing exact names. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**Code mode** — A text input where you write raw PromQL queries directly. The instructor says "usually we use code, that's much better" — because it gives full control over the query, supports complex expressions, and matches how queries are written in documentation and shared between teams. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

You can switch between the two modes. If you build a query using the builder, clicking **"Explain"** shows you the actual PromQL code that was generated. You can then copy that code into the code editor, modify it, and run it. This is a useful learning bridge — use the builder to discover, then switch to code for precision. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## 1.7 Multiple Queries and Panel Visualization

The Explore interface supports **multiple queries** on the same view. Each query is labeled (A, B, C, etc.) and its results are overlaid on the same graph. The video demonstrates: query A runs `http_requests_total` for the root endpoint (`/`), and query B runs `http_requests_total{endpoint="/payment"}`. Both lines appear on the same graph — the green line for `/` and the yellow line for `/payment`. The legend shows which line belongs to which query, including all labels. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

This multi-query capability is how you build **comparative panels** — overlaying different metrics or the same metric with different filters to see relationships, correlations, or divergences. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

The visualization can be switched between multiple formats directly in the Explore view: **lines** (default time-series graph), **bars**, **points**, **stacked lines**, **stacked bars**. These are just the Explore options — when building actual dashboard panels, the customization options are far more extensive. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## 1.8 Panels — The Building Blocks of Dashboards

The video introduces the term **panel** — each individual visualization widget on a Grafana dashboard. A panel contains one or more PromQL queries, a visualization type (graph, bar, gauge, stat, table, etc.), and extensive customization options. Dashboards are composed of multiple panels arranged to give a comprehensive view of the system. The video states: "We're going to build these kind of panels" — setting up the expectation that upcoming lectures will focus on panel and dashboard creation. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are connecting Grafana to the Prometheus server as a data source and verifying the connection by running PromQL queries through Grafana's Explore interface. The final outcome: Grafana can read all metrics stored in Prometheus, display them as graphs, and serve as the platform for building monitoring dashboards in subsequent lectures. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## Step 1: Power On the Grafana EC2 Instance

Navigate to the **AWS EC2 console**. Find the Grafana instance and start it (if it was stopped). [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**If returning after a break:** Your public IP may have changed. Update the Grafana security group's inbound rule for port 3000 — change the source from the old IP to your current IP ("My IP"). Save the rules. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

Wait a few minutes after powering on for the instance and Grafana service to fully initialize. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## Step 2: Log Into Grafana

Open a browser and navigate to:

```
http://<grafana-public-ip>:3000
```

| Field    | Value                                       |
| -------- | ------------------------------------------- |
| Username | `admin`                                     |
| Password | The password you reset during initial setup |

 [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

If you've forgotten the password, you would need to reset it via the Grafana CLI on the instance.

***

## Step 3: Add Prometheus as a Data Source

**3a. Navigate to data source configuration:**

Click **Connections** (left sidebar) → **Data Sources** → **Add Data Source**. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**3b. Select Prometheus:**

From the list of available data sources, select **Prometheus**. You'll see many other options (InfluxDB, Loki, Elasticsearch, CloudWatch, etc.) — select Prometheus specifically. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**3c. Configure the connection:**

| Setting        | Value                                 | Reasoning                                                                                              |
| -------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Name           | (default or custom)                   | Custom name is useful when you have multiple Prometheus servers                                        |
| Connection URL | `http://<prometheus-private-ip>:1990` | Use **private IP** — public IP changes on restart. Port 1990 is where Prometheus listens in this setup |
| Authentication | No authentication                     | This learning setup has no auth. Production would use basic auth or OAuth                              |

 [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**Where to find the Prometheus private IP:** Go to the EC2 console → find the Prometheus instance → copy its **private IPv4 address**.

⚠️ Do NOT use the public IP. It changes every time the instance is stopped and restarted. The private IP is stable within the VPC. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**3d. Scroll down and click "Save & Test":**

**Expected result:** A green success message: *"Successfully queried Prometheus API."* [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**If you get an error, troubleshoot in this order:**

1. **Check the URL:** Is the IP correct? Is the port correct? Is it `http://` not `https://`?
2. **Check the Prometheus security group:** Does it have an inbound rule allowing port 1990 from the Grafana security group?
3. **Quick fix (temporary):** Add an inbound rule to the Prometheus security group: port 1990 from `0.0.0.0/0` (anywhere). If this works, the issue is the security group reference — fix the proper rule and remove the open one.
4. **Is Prometheus running?** SSH into the Prometheus instance and verify the service is active.

 [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**Connection to larger flow:** Once saved, this data source is permanently available in Grafana. Every dashboard panel will reference this Prometheus data source when running PromQL queries.

***

## Step 4: Verify the Connection via Explore

**4a. Navigate to Explore:**

After the successful test, click on **Data Sources** again. You should see the Prometheus data source listed. Click on it and select **Explore**. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

Confirm that "Prometheus" is selected as the data source in the dropdown at the top.

**4b. Run a query using Builder mode:**

The interface shows a query labeled "A" with two mode tabs: **Builder** and **Code**.

In Builder mode:

* Select the metric: `http_requests_total`
* Click "Select label" → choose `endpoint`
* Select the value: `payment`
* Click **Run Query** [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**Expected result:** A graph line showing the `http_requests_total` counter for the `/payment` endpoint over time.

**4c. Switch to Code mode and see the generated query:**

Click **Explain** — Grafana displays the actual PromQL query it built. Copy this query. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

Switch to the **Code** tab. The query is already populated. You can now edit it directly as raw PromQL. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

***

## Step 5: Run Multiple Queries on the Same Graph

**5a. Modify query A:**

In Code mode, remove the `{endpoint="/payment"}` filter so query A becomes:

```promql
http_requests_total
```

Run the query. This shows all endpoints. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**5b. Add query B:**

Click **"Add query"** (or the `+` button). A new query row labeled "B" appears. Switch it to Code mode. Enter:

```promql
http_requests_total{endpoint="/payment"}
```

Click **Run Query**. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**Expected result:** Two lines on the graph — one for each query. The legend at the bottom shows which color corresponds to which query/endpoint, along with all associated labels. [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

**5c. Explore visualization options:**

The graph defaults to **lines**. Try switching to:

* **Bars** — bar chart format
* **Points** — discrete data points
* **Stacked lines** — lines stacked on top of each other
* **Stacked bars** — bars stacked

 [\[257-connec...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/257-connecting-grafana-and-prometheus.txt)

These are preview options in Explore. Dashboard panels offer even more customization.

**Connection to larger flow:** This confirms the complete data pipeline works: Flask app → metrics endpoint → Prometheus scrape → Prometheus storage → Grafana query → visual output. The next steps are: connecting Slack for alert notifications, then building actual dashboard panels.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture — End-to-End Data Flow

```
[ Flask App ]  →  /metrics endpoint
[ Node Exporter ] → /metrics endpoint
        │
        │  scraped every 15s
        ▼
[ Prometheus Server :1990 ]  ← stores time-series data (TSDB)
        │
        │  HTTP (private IP, port 1990)
        │  Security: Prometheus SG allows 1990 from Grafana SG
        ▼
[ Grafana Server :3000 ]     ← queries Prometheus via PromQL
        │                       visualizes as dashboards/panels
        │                       sends alert notifications
        ▼
[ User Browser :3000 ]       ← views dashboards
                               Security: Grafana SG allows 3000 from My IP
```

***

## Connection Configuration

```
Grafana → Connections → Data Sources → Add → Prometheus

URL:    http://<prometheus-PRIVATE-ip>:1990
Auth:   None (learning) | Basic/OAuth (production)
Test:   "Save & Test" → "Successfully queried Prometheus API"

⚠️ PRIVATE IP — not public (public changes on restart)
⚠️ Port must be open in Prometheus SG from Grafana SG
```

***

## Security Group Chain

```
Your IP ──[3000]──→ Grafana SG ──→ Grafana instance
Grafana SG ──[1990]──→ Prometheus SG ──→ Prometheus instance

Troubleshooting: If connection fails:
  1. Check URL (IP, port, http://)
  2. Check Prometheus SG inbound rule
  3. Temporary fix: allow 1990 from 0.0.0.0/0 → test → fix properly

IP change after break: Update Grafana SG → port 3000 → My IP
```

***

## Explore Interface — Two Modes

```
Builder Mode:
  Dropdown → select metric → select label → select value
  Good for: discovery, learning available metrics
  Click "Explain" → see generated PromQL

Code Mode:
  Raw PromQL text input
  Good for: precision, complex queries, production use
  "Usually we use code, that's much better"

Multiple queries: A, B, C... → overlaid on same graph
```

***

## Grafana Data Source Flexibility

```
Prometheus  ← this course
InfluxDB
Loki (logs)
Elasticsearch
Jaeger / Tempo / Zipkin (tracing)
AWS CloudWatch
Azure Monitor
SQL databases
Grafana Cloud (SaaS)

Same dashboard skills → different query languages per backend
Multiple data sources → panels can pull from different backends
```

***

## Visualization Options (Explore)

```
Lines → default time-series graph
Bars → bar chart
Points → discrete data points
Stacked Lines → cumulative overlay
Stacked Bars → cumulative bars

Dashboard panels: far more options (gauges, stats, tables, heatmaps, etc.)
```

***

## Panel Concept

```
Panel = single visualization widget on a dashboard
  Contains: 1+ PromQL queries + visualization type + customization
Dashboard = collection of panels
  Used by: NOC/SOC teams for 24/7 monitoring
```

***

## Operational Sequence

```
1. Power on Grafana EC2
2. Update Grafana SG if IP changed (port 3000 from My IP)
3. Wait for boot → access http://<public-ip>:3000
4. Login: admin / <your-password>
5. Connections → Data Sources → Add → Prometheus
6. URL: http://<prometheus-private-ip>:1990
7. Auth: None
8. Save & Test → "Successfully queried"
9. Data Sources → click Prometheus → Explore
10. Builder: select metric + labels → Run Query → see graph
11. Code: write raw PromQL → Run Query
12. Add query B → overlay multiple series
```

***

## Connection Troubleshooting Decision Tree

```
"Save & Test" fails?
  ├── Check URL format: http://<private-ip>:<port>
  ├── Check IP: is it private, not public?
  ├── Check port: matches Prometheus config?
  ├── Check Prometheus SG:
  │     └── Inbound: port 1990 from Grafana SG?
  │           └── Quick test: try 1990 from 0.0.0.0/0
  └── Check Prometheus service: is it running?
```

***

## Private IP vs Public IP Rule

```
PRIVATE IP:  stable across stop/start cycles → USE for service-to-service connections
PUBLIC IP:   changes on every stop/start → USE only for browser access from outside

Grafana → Prometheus: PRIVATE IP (both in same VPC)
You → Grafana: PUBLIC IP (from internet)
```

***

## Key Engineering Patterns

| Pattern                               | Manifestation                                                                                              |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Visualization as separate concern** | Prometheus stores; Grafana displays — separation of storage and presentation                               |
| **Data-source abstraction**           | Grafana decouples from any specific backend — same dashboard framework, any data source                    |
| **Private IP for internal comms**     | Service-to-service connections use stable private IPs within VPC — public IPs are for external access only |
| **Security group chaining**           | Each hop in the architecture has its own SG rule — Grafana SG → Prometheus SG                              |
| **Builder → Code progression**        | Discover with visual builder, operate with raw code — learning bridge pattern                              |
| **Multi-query overlay**               | Multiple queries on one panel for comparison — the basis of operational dashboards                         |

***

## Project Continuity

```
BEFORE: PromQL fundamentals — data types, operators, functions (executed in Prometheus UI)
THIS:   Grafana connected to Prometheus — Explore interface verified — multi-query tested
NEXT:   Connect Slack as notification contact point → then build dashboard panels
```

***

This completes the full reconstruction. **Theory** explains Grafana's role as a data-source-agnostic visualization layer and the connection architecture. **Practical** walks through every click and configuration with troubleshooting paths. The **Compression Map** gives you the architecture diagram, security group chain, and operational sequence for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
