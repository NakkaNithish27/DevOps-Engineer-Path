# Monitoring & Observability Tools — Deep Learning Material

**Source:** DevOps course lecture on Monitoring and Observability Tools (caption file: [252-monitoring-and-observability-tools.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt?EntityRepresentationId=76149bda-cb51-4976-a86e-145808e63b54)) [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

The user-provided architecture diagram is also referenced throughout for port/flow accuracy.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Monitoring & Observability Problem Space

Before diving into individual tools, you need to understand what problem this entire stack solves. In any production system — whether it's a single EC2 instance running Apache or a Kubernetes cluster with hundreds of pods — two questions are always critical: **"What is happening right now?"** (metrics) and **"What happened when something broke?"** (logs). Metrics tell you CPU is at 95%. Logs tell you *why* — maybe a specific request pattern triggered a memory leak at 3:47 AM.

These two data types — **metrics** and **logs** — are two of the three "golden pillars" of observability (the third being **traces**, which track a request's journey across services). This lecture focuses primarily on the metrics and logs pillars, and introduces the tool ecosystem that handles collection, storage, visualization, and alerting for both. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

The architecture is not a single monolithic tool. It's a **distributed system of specialized components**, each handling one responsibility. Understanding *why* there are multiple tools — instead of one — is the first conceptual key: each tool is purpose-built for a specific data type and operation, and they integrate through well-defined network ports.

***

## 1.2 — Prometheus: The Metrics Engine

**Prometheus** is an open-source monitoring and alerting toolkit. Its core job is to **collect, store, and query metrics** — numerical measurements of system behavior over time (CPU usage, memory consumption, request counts, error rates, disk I/O, etc.).

**How it works internally:** Prometheus operates on a **pull model** called **scraping**. Target systems expose metrics at HTTP endpoints (e.g., `http://target:9100/metrics`). Prometheus periodically visits these endpoints, reads all the metrics they expose, and stores them. This periodic pull process is called scraping. You configure Prometheus with the list of targets to scrape and the interval at which to scrape them.

**Storage model:** Prometheus stores all scraped data as **time-series data** — each metric is a sequence of timestamped values. This format is specifically designed for charting graphs, bar charts, and other temporal visualizations. You can answer questions like "What was CPU usage at 2 PM?" or "How has memory consumption trended over the last 24 hours?" because every data point carries a timestamp. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

**Querying:** To extract information from Prometheus, you use **PromQL** (Prometheus Query Language) — its own dedicated query language. For example, the metric `up` returns whether a target is reachable (`1` = up, `0` = down). You can filter using labels: `up{app="node1"}` returns the status only for targets labeled `app=node1`. PromQL supports aggregation, rate calculations, histograms, and many other operations that we'll explore in later lectures.

**Prometheus UI:** Prometheus has its own web dashboard, but the video is explicit — it's **"nothing fancy."** The UI is functional for executing PromQL queries and checking target health (which endpoints are being scraped, their state, when the last scrape occurred), but it's not designed for rich visualization. Rich dashboards are Grafana's job.

**Alerting integration:** Prometheus can integrate with Alert Manager to trigger notifications, but the video notes that **Grafana is better** for alert integration and will be used instead for that purpose. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

**Ecosystem fit:** Prometheus is ideal for cloud-native applications, especially Kubernetes. It can monitor pods, containers, nodes, and the cluster itself. But it's equally applicable to traditional infrastructure monitoring on standalone servers.

> 🔍 **Deep Dive**
> The pull/scrape model has an important architectural implication: Prometheus must be able to reach every target's metrics endpoint over the network. This means firewall rules must allow Prometheus to connect *outward* to targets on their metrics ports (e.g., 9100 for Node Exporter, 5000 for application metrics). The target doesn't push to Prometheus — Prometheus comes to the target. This is the opposite of Loki's model (covered below), where the client pushes to the server.

***

## 1.3 — Grafana: The Visualization & Dashboard Layer

**Grafana** is an open-source dashboard and visualization tool. It does **not** collect or store metrics or logs itself. Instead, it connects to **data sources** — like Prometheus (for metrics) and Loki (for logs) — fetches data from them, and presents it in rich, customizable visual panels.

Think of Grafana as the **front end** of the entire monitoring stack. Prometheus and Loki are the backend data stores; Grafana is the user-facing interface where you see graphs, charts, gauges, pie charts, threshold indicators, and all the "fancy" visualization.

**How it works with Prometheus:** Grafana connects to Prometheus and executes PromQL queries to fetch metric data. Based on the query results, it renders panels — graphs of CPU over time, gauges for current disk utilization, bar charts for request rates, etc. Grafana does not have its own query language for metrics; it uses PromQL by proxying queries to Prometheus.

**How it works with Loki:** Similarly, Grafana connects to Loki to query and visualize logs. This integration allows you to see logs and metrics side by side on the same dashboard — correlating a CPU spike with the log entries that occurred at the same time. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

**Customization:** The video emphasizes that Grafana is exceptionally flexible — "I have never seen any such flexible monitoring tool." You get extensive options for dashboard layouts, panel types, color schemes, thresholds, and alerts. Changes can be made through the browser UI or through JSON configuration files.

**Alerting:** Grafana can integrate with Alert Manager and send notifications to Slack, email, PagerDuty, or any webhook-based system. While Prometheus itself can connect to Alert Manager, the recommended approach in this stack is to use **Grafana as the alert integration point**.

**Access:** Grafana is accessed through a web browser on **port 3000** (default, configurable). [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## 1.4 — Loki: The Log Aggregation System

**Loki** is a log aggregation system — it **receives, stores, and indexes logs**. If Prometheus is the database for metrics, Loki is the database for logs.

**Key design difference from Prometheus:** Loki uses a **push model**, not a pull model. Log clients (Promtail or Alloy) running on application servers read log files, structure them, attach labels, and **push** them to Loki. Loki does not go out and fetch logs — it sits and listens for incoming log data on **port 3100** (default). This is architecturally the opposite of Prometheus's scraping behavior.

**Storage model:** Loki stores logs efficiently using **labels**. Labels are key-value tags attached to log streams (e.g., `job="apache"`, `host="web01"`). You use these labels to sort, filter, and find specific log entries. The label-based indexing makes Loki lightweight compared to full-text indexing systems.

**Grafana integration:** Once Loki is added as a data source in Grafana, you can query, visualize, and create alerts on log data — just as you do with Prometheus metrics. This completes the observability picture: metrics from Prometheus + logs from Loki, both visualized in Grafana.

**Target use case:** Like Prometheus, Loki is designed for modern cloud-native applications — containers, Kubernetes, microservices. But it works equally well for traditional server log aggregation. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## 1.5 — Node Exporter: The System Metrics Agent

All the tools above are **servers** — they run as services, listen on ports, and process data. But someone needs to actually **produce** the metrics data that Prometheus scrapes. On the application/infrastructure side, that's the job of **agents**. Node Exporter is the first agent covered.

**Node Exporter** is a lightweight agent that runs on a Linux server (or similar) and **exposes system-level metrics** — CPU utilization, memory usage, disk space, disk I/O, network statistics. It doesn't push these metrics anywhere; it simply makes them available at an HTTP endpoint on **port 9100** (default). Prometheus then scrapes this endpoint periodically.

This is the **infrastructure monitoring** agent. It answers: "How is this server performing at the hardware/OS level?" [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

> 🔍 **Deep Dive**
> Node Exporter is not the only way to expose metrics to Prometheus. Developers can instrument their applications to expose **application-level metrics** (request counts, response times, error rates, queue depths) at custom endpoints. The video mentions that the application being set up will expose its own metrics on port 5000, separate from Node Exporter's system metrics on port 9100. Prometheus can scrape both — it just needs both endpoints configured as targets.

***

## 1.6 — Promtail: The Log Forwarder (Outdated)

**Promtail** is a log forwarder agent — it runs on application servers, reads log files (or standard output), attaches labels to the log entries, and **pushes** them to Loki on port 3100. If Node Exporter is the metrics agent for Prometheus, Promtail is the log agent for Loki.

**Current status:** The video explicitly states that Promtail is **outdated** — its support has been stopped. It's still discussed because many organizations continue to use it, but new deployments should use **Alloy** instead. Promtail is actively phasing out. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## 1.7 — Alloy: The Unified Agent (Replacement)

**Alloy** is the **all-in-one unified agent** from Grafana Labs. It can collect **metrics, logs, traces, and profiles** — replacing both Node Exporter and Promtail with a single agent.

**Current transition state (as described in the video):**

* **Node Exporter** is still widely used in production. It will eventually phase out in favor of Alloy, but that hasn't happened yet.
* **Promtail** is actively phasing out. Alloy is its direct replacement for log forwarding.
* **Long-term vision:** Alloy becomes the single agent for all observability data collection.

Alloy works with both self-hosted Grafana stacks and Grafana Cloud. The video states that the course will use a **self-hosted** setup to understand the full infrastructure, not the cloud-managed version. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## 1.8 — Alert Manager: The Alert Delivery System

**Alert Manager** works with Prometheus to handle alerts. When a metric crosses a defined threshold — CPU above 60-80%, disk getting full, HTTP requests failing at a certain rate — Alert Manager receives the alert from Prometheus and delivers notifications to configured channels: **Slack, email, PagerDuty, or any webhook**.

The video describes it precisely: Alert Manager is an **alert delivery system for Prometheus**. It doesn't decide what's wrong — Prometheus's alerting rules determine that. Alert Manager handles the *routing and delivery* of those alerts to the right people through the right channels. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## 1.9 — Architecture: How Everything Connects

The complete architecture follows a clear separation of concerns with two parallel data pipelines converging at a single visualization layer:

**Metrics Pipeline:**
Application/Server → Node Exporter (exposes metrics on :9100) ← Prometheus (scrapes on :9100, stores time-series data, serves on :9090) ← Grafana (queries via PromQL on :9090, visualizes on :3000)

**Logs Pipeline:**
Application/Server → Promtail/Alloy (reads logs, pushes to :3100) → Loki (receives logs on :3100, stores with labels) ← Grafana (queries on :3100, visualizes on :3000)

**Key architectural observations from the video:**

* Metrics flow uses **pull** (Prometheus scrapes targets). The arrow direction matters: Prometheus initiates the connection to targets.
* Logs flow uses **push** (Promtail/Alloy pushes to Loki). The client initiates the connection to Loki.
* Grafana is the **single visualization entry point** for both pipelines. It connects to both Prometheus (:9090) and Loki (:3100) as data sources.
* All services communicate over **TCP ports**. Knowing the default ports is critical for firewall rules and network security configuration. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

The user-provided architecture diagram confirms the network topology with additional detail:

* **Admin IPs/VPN** access Grafana EC2 on TCP/3000 and Prometheus EC2 on TCP/9090 (for direct dashboard access).
* **Grafana EC2** connects to Prometheus EC2 on TCP/9090 (data source queries).
* **Prometheus EC2** scrapes App EC2 on TCP/9100 (Node Exporter metrics) and connects to Loki EC2 on TCP/3100.
* **Internet/Users** access App EC2 (Apache2) on TCP/80,443 (web traffic).
* **App EC2** runs Promtail, which pushes logs to Loki EC2 on TCP/3100.
* **Grafana EC2** also connects to Loki EC2 on TCP/3100 (log queries).

> ⚠️ **Expert Note**
> The video explicitly calls out that knowing port numbers is a **DevOps engineering responsibility**. When setting up this stack — whether on bare EC2 instances or on Kubernetes — you must configure security groups / firewall rules to allow the correct port-to-port communication. Misconfigured firewalls are the most common reason these tools fail to connect. Every port mentioned is a default that *can* be changed, but the defaults are the industry standard and what you'll encounter in most environments. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a **self-hosted monitoring and observability stack** across multiple EC2 instances. The final outcome: a fully functioning system where system metrics and application metrics are collected by Prometheus, application logs are forwarded to Loki, and everything is visualized through Grafana dashboards — with alerting capability through Alert Manager. The setup in this lecture is conceptual and architectural; the actual installation and configuration happen in the next lectures. This lecture establishes the **port map, tool roles, and communication flows** you need before starting the setup.

***

## Step 1 — Understand the Tool Inventory

Before any setup, you need to know exactly which components you're deploying and on which machines. Based on the architecture:

| Component            | Role                         | Runs On                              | Default Port                             |
| -------------------- | ---------------------------- | ------------------------------------ | ---------------------------------------- |
| **Prometheus**       | Metrics collection & storage | Dedicated EC2 (Prometheus EC2)       | **9090**                                 |
| **Grafana**          | Visualization & dashboards   | Dedicated EC2 (Grafana EC2)          | **3000**                                 |
| **Loki**             | Log aggregation & storage    | Dedicated EC2 (Loki EC2)             | **3100**                                 |
| **Node Exporter**    | System metrics agent         | App EC2 (the monitored server)       | **9100**                                 |
| **Promtail / Alloy** | Log forwarding agent         | App EC2 (the monitored server)       | Pushes to Loki :3100                     |
| **Alert Manager**    | Alert delivery               | Typically co-located with Prometheus | —                                        |
| **Application**      | The thing being monitored    | App EC2 (Apache2)                    | **80/443** (web), **5000** (app metrics) |

 [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

**Key decision from the video:** We are doing a **self-hosted** setup, not using Grafana Cloud. This means we manage every component ourselves — installation, configuration, networking, and security. This gives full understanding of the infrastructure.

***

## Step 2 — Map the Network Communication (Port Planning)

Before provisioning any infrastructure, you must plan the port-based communication between services. This directly translates into **security group / firewall rules** on AWS.

**Connections to configure (derived from the video and the architecture diagram):**

### Grafana EC2 Security Group — Inbound:

| Port     | Source          | Purpose                           |
| -------- | --------------- | --------------------------------- |
| TCP/3000 | Admin IPs / VPN | Admin access to Grafana dashboard |

### Grafana EC2 — Outbound (or target SG inbound):

| Port     | Destination    | Purpose                                |
| -------- | -------------- | -------------------------------------- |
| TCP/9090 | Prometheus EC2 | Grafana queries Prometheus for metrics |
| TCP/3100 | Loki EC2       | Grafana queries Loki for logs          |

### Prometheus EC2 Security Group — Inbound:

| Port     | Source          | Purpose                        |
| -------- | --------------- | ------------------------------ |
| TCP/9090 | Grafana EC2     | Grafana data source connection |
| TCP/9090 | Admin IPs / VPN | Direct Prometheus UI access    |

### Prometheus EC2 — Outbound (or target SG inbound):

| Port     | Destination | Purpose                                  |
| -------- | ----------- | ---------------------------------------- |
| TCP/9100 | App EC2     | Prometheus scrapes Node Exporter metrics |
| TCP/5000 | App EC2     | Prometheus scrapes application metrics   |
| TCP/3100 | Loki EC2    | Prometheus connects to Loki              |

### App EC2 Security Group — Inbound:

| Port        | Source           | Purpose                        |
| ----------- | ---------------- | ------------------------------ |
| TCP/80, 443 | Internet / Users | Web traffic to Apache2         |
| TCP/9100    | Prometheus EC2   | Node Exporter metrics scraping |
| TCP/5000    | Prometheus EC2   | Application metrics scraping   |

### Loki EC2 Security Group — Inbound:

| Port     | Source                   | Purpose                          |
| -------- | ------------------------ | -------------------------------- |
| TCP/3100 | App EC2 (Promtail/Alloy) | Log push from application server |
| TCP/3100 | Grafana EC2              | Grafana queries logs             |
| TCP/3100 | Prometheus EC2           | Prometheus connection            |

 [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

> ⚠️ **Expert Note**
> All ports listed are **defaults that can be changed**. However, in practice, the industry universally uses these defaults. Changing them creates operational confusion for anyone joining the team later. Only change ports if there's a specific conflict or security requirement. When writing automation (Terraform, Ansible) for this stack, parameterize the port numbers as variables so they can be adjusted without rewriting firewall rules.

***

## Step 3 — Understand the Data Flow Direction (Critical for Firewall Design)

This is operationally the most important distinction for setup:

**PULL (Prometheus → Targets):**
Prometheus **initiates** the connection to scrape metrics. This means:

* Prometheus EC2 needs **outbound** access to target ports (9100, 5000).
* Target EC2s need **inbound** rules allowing Prometheus's IP on those ports.

The video explicitly corrects the arrow direction in its own diagram: the arrow should point FROM Prometheus TO the target, because Prometheus goes to the metrics and scrapes them.

**PUSH (Promtail/Alloy → Loki):**
The agent on the app server **initiates** the connection to push logs. This means:

* App EC2 needs **outbound** access to Loki's port (3100).
* Loki EC2 needs an **inbound** rule allowing App EC2's IP on port 3100.

Getting this direction wrong means your firewall rules will block the wrong side of the connection. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## Step 4 — Verify Prometheus Targets and Scraping (Post-Setup Verification)

Once the stack is set up (next lectures), you verify that Prometheus is successfully scraping targets by:

1. Access Prometheus UI at `http://<prometheus-ip>:9090`.
2. Navigate to **Status → Target Health**.
3. Check each endpoint's **state** (should be "UP") and **last scrape** time.
4. Run a basic PromQL query: type `up` in the query box and execute.
   * `1` = target is up and being scraped successfully.
   * `0` = target is down or unreachable.
5. Filter by label: `up{app="node1"}` to check a specific target. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

**Common failure scenario:** If a target shows as DOWN, the most likely cause is a **firewall/security group rule** blocking Prometheus from reaching the target's metrics port. Verify the security group allows inbound from Prometheus EC2 on the correct port.

***

## Step 5 — Verify Grafana Dashboards (Post-Setup Verification)

1. Access Grafana at `http://<grafana-ip>:3000`.
2. Navigate to **Dashboards** → select a project/team dashboard.
3. Verify panels are rendering: graphs (CPU, disk I/O, disk space utilization), gauges, pie charts.
4. Check that both **Prometheus** and **Loki** are configured as data sources (Settings → Data Sources).
5. Verify threshold indicators are working on graphs. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## Step 6 — Decide on Agent Strategy (Promtail vs Alloy)

For new deployments, the video's guidance is clear:

* **For log collection:** Use **Alloy** (Promtail is outdated, support stopped).
* **For system metrics:** **Node Exporter** is still widely used and acceptable. Alloy *can* replace it, but the transition hasn't fully happened in the industry yet.
* **Long-term:** Plan for Alloy as the single unified agent for everything (metrics + logs + traces + profiles). [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

## Step 7 — Download the Architecture Diagram

The video instructs to download the architecture diagram image from the lecture resources. This diagram is the reference for all port numbers and communication flows during setup. Keep it accessible while configuring security groups and service configurations. [\[252-monito...lity-tools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/252-monitoring-and-observability-tools.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## The Two Parallel Pipelines

```
METRICS PIPELINE (PULL model):
  App Server → Node Exporter (:9100) ←─SCRAPE─ Prometheus (:9090) ←─QUERY─ Grafana (:3000)
                App Metrics  (:5000) ←─SCRAPE─┘

LOGS PIPELINE (PUSH model):
  App Server → Promtail/Alloy ──PUSH──→ Loki (:3100) ←─QUERY─ Grafana (:3000)

ALERTING:
  Prometheus → Alert Manager → Slack / Email / PagerDuty / Webhook
  (Grafana preferred as alert integration point over direct Prometheus→AlertManager)
```

***

## Tool → Role → One-Line Identity

```
Prometheus     →  Metrics database     →  "Scrapes, stores, queries time-series metrics"
Grafana        →  Visualization front  →  "Dashboards, graphs, alerts — the UI for everything"
Loki           →  Log database         →  "Receives, stores, indexes logs with labels"
Node Exporter  →  System metrics agent →  "Exposes CPU/mem/disk/net at :9100 for Prometheus"
Promtail       →  Log forwarder        →  "Reads logs, labels them, pushes to Loki" (OUTDATED)
Alloy          →  Unified agent        →  "Replaces Node Exporter + Promtail — one agent for all"
Alert Manager  →  Alert delivery       →  "Routes Prometheus alerts to notification channels"
```

***

## Port Map (Defaults)

```
:3000  →  Grafana        (browser access, admin)
:9090  →  Prometheus     (UI + PromQL queries from Grafana)
:3100  →  Loki           (log ingestion from Promtail/Alloy + queries from Grafana)
:9100  →  Node Exporter  (system metrics scraped by Prometheus)
:5000  →  Application    (app metrics scraped by Prometheus)
:80/443 → Application    (user web traffic — Apache2)
```

***

## Data Flow Direction (Critical for Firewalls)

```
PULL:  Prometheus ──→ Node Exporter (:9100)     Prometheus INITIATES connection
PULL:  Prometheus ──→ App Metrics (:5000)       Prometheus INITIATES connection
PULL:  Grafana    ──→ Prometheus (:9090)        Grafana INITIATES connection
PULL:  Grafana    ──→ Loki (:3100)              Grafana INITIATES connection

PUSH:  Promtail/Alloy ──→ Loki (:3100)          Agent INITIATES connection
```

```
RULE: For PULL → target needs inbound rule allowing source IP on target port
      For PUSH → receiver needs inbound rule allowing sender IP on receiver port
```

***

## Server vs Agent Classification

```
SERVERS (run as services, listen on ports, store data):
  Prometheus  │  Grafana  │  Loki  │  Alert Manager

AGENTS (run on monitored hosts, collect/expose data):
  Node Exporter  │  Promtail (outdated)  │  Alloy (unified replacement)
```

***

## Agent Transition Timeline

```
CURRENT STATE:
  Node Exporter  →  still widely used for system metrics
  Promtail       →  PHASING OUT (support stopped)
  Alloy          →  replacing Promtail NOW, will replace Node Exporter LATER

FUTURE STATE:
  Alloy          →  single agent for metrics + logs + traces + profiles
```

***

## Prometheus Internals (Compressed)

```
Scraping:   visits target HTTP endpoints periodically → reads metrics → stores
Storage:    time-series data (value + timestamp) → enables temporal graphs
Query:      PromQL → up{app="node1"} → 1=up, 0=down
UI:         functional, not fancy → use Grafana for dashboards
Targets:    Status → Target Health → state + last scrape time
```

***

## Grafana Internals (Compressed)

```
Data sources:  Prometheus (:9090) + Loki (:3100) + others
Mechanism:     executes PromQL/LogQL against data sources → renders panels
Panels:        graphs, gauges, pie charts, bar charts, thresholds
Config:        browser UI or JSON files
Alerts:        integrates with Alert Manager → Slack/email/PagerDuty/webhook
Access:        browser → :3000
```

***

## Loki vs Prometheus (Parallel Structure)

```
                  Prometheus              Loki
Data type:        Metrics                 Logs
Model:            PULL (scrape)           PUSH (receive)
Agent:            Node Exporter           Promtail/Alloy
Storage:          Time-series             Label-indexed logs
Query via:        PromQL                  LogQL (implied)
Port:             9090                    3100
Visualized by:    Grafana                 Grafana
```

***

## Architecture Diagram — EC2 Topology (from user image)

```
                    Admin IPs/VPN
                    ├── :3000 ──→ Grafana EC2
                    └── :9090 ──→ Prometheus EC2

Grafana EC2 ──:9090──→ Prometheus EC2
Grafana EC2 ──:3100──→ Loki EC2

Prometheus EC2 ──:9100──→ App EC2 (Node Exporter)
Prometheus EC2 ──:3100──→ Loki EC2

Internet/Users ──:80/443──→ App EC2 (Apache2)

App EC2 (Promtail) ──:3100──→ Loki EC2
```

***

## Reusable Engineering Pattern: Separation of Collection, Storage, and Presentation

```
PATTERN:
  COLLECT (agents: Node Exporter, Promtail, Alloy)
     ↓
  STORE (databases: Prometheus for metrics, Loki for logs)
     ↓
  PRESENT (front end: Grafana)

WHY: Each layer scales independently. Replace an agent without touching storage.
     Add a new data source to Grafana without changing collection.
     Swap Prometheus for a different metrics DB → Grafana still works.

WHERE ELSE: ELK stack (Beats → Elasticsearch → Kibana)
            CloudWatch (Agent → CloudWatch → Console)
            Any observability platform follows this 3-layer pattern
```

***

## Setup Readiness Checklist (Before Next Lecture)

```
☐ Know all 6 components and their roles
☐ Know which are servers vs agents
☐ Know all default ports
☐ Know pull vs push for each data flow
☐ Know security group rules needed per EC2
☐ Know Promtail is outdated → use Alloy
☐ Have architecture diagram downloaded and accessible
☐ Understand: self-hosted setup, not Grafana Cloud
```

***

This completes the full reconstruction. Theory builds the conceptual foundation of each tool and their relationships, Practical maps the operational setup and port planning you'll need before the next lecture's hands-on work, and the Compression Map enables instant recall of the entire stack architecture. Let me know if you'd like AnkiDeck cards from this or if you're ready for the next lecture! 🚀
