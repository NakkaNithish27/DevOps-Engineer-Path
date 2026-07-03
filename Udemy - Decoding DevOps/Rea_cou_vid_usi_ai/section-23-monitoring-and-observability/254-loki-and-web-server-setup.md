# 🎓 Deep Learning Material: Loki and Web Server Setup — Log Aggregation Server, Application Node with Alloy Agent, and the Complete Monitoring Stack Wiring

**Source:** Video lecture on Loki and web application server setup (from [254-loki-and-web-server-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt?EntityRepresentationId=98678690-fc12-4009-803b-755327983053) caption file) [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Video Context:** This lecture completes the monitoring stack infrastructure by setting up two final EC2 instances: **(1)** a **Loki server** (log aggregation, analogous to Prometheus for metrics) and **(2)** a **web application server** running a Titan Flask app, Node Exporter, Alloy agent, and background scripts that generate fake load and logs. Grafana and Prometheus were set up in previous lectures. After this lecture, all four components of the monitoring stack exist: **Grafana** (visualization), **Prometheus** (metrics collection), **Loki** (log aggregation), and **Alloy** (agent on the application server that pushes logs to Loki and exposes metrics for Prometheus to scrape). The instructor carefully distinguishes what's part of the monitoring stack vs. what's just generating test data.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Loki: The Log Aggregation Server

Loki is a **log aggregation system** — it collects, stores, and indexes log data from multiple sources so you can query and visualize logs in Grafana. Its role in the monitoring stack is analogous to Prometheus, but for a different data type: **Prometheus handles metrics** (numeric time-series data like CPU usage), while **Loki handles logs** (text-based event records like application errors, access logs, info messages). [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

The instructor frames Loki's setup as *"similar to Prometheus"* — both follow the same installation pattern: download a binary from GitHub, extract it, create a system user, set up a configuration file, create a systemd service file, and start the service. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

Loki runs on **port 3100** by default. Other services (specifically the Alloy agent on application servers) **push logs** to Loki on this port. This is an important architectural distinction: Prometheus **pulls** (scrapes) metrics from targets, while Loki **receives** (is pushed to) logs from agents. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

The Loki setup script sets several paths: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

* **Binary:** `/usr/local/bin/loki`
* **Configuration:** `/etc/loki/config.yml`
* **Data storage:** `/var/lib/loki` (with subdirectories `chunks` and `rules`)
* **System user/group:** `loki:loki` (dedicated service account)

The configuration file is mentioned but the instructor explicitly defers detailed explanation: *"You don't need to understand anything for now\... When we do log aggregation in detail, we'll take a look at this configuration."* [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

After starting Loki, you can verify it's running with a readiness check that returns `"ready"`. There's also a metrics endpoint for Loki itself (Loki exposes its own metrics, which Prometheus could scrape). [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

> 🔍 **Deep Dive**
>
> Loki's readiness takes time — the instructor observes it takes more than 120 seconds: *"it still says Ingestor is not ready... It takes more than 120s. Maybe you can set it for 180s."* The setup script has a built-in wait, but the actual readiness time varies. The "Ingestor not ready" message indicates Loki's internal write component (the ingestor) hasn't finished initializing. Running the readiness check again after a brief wait confirms it becomes ready. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

## 1.2 — The Web Application Server: Three Layers of Purpose

The web server (web01) is the **most complex setup** in the monitoring stack because it serves three distinct purposes: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

### Layer 1: The Application (Titan Flask App) — Generates Real-Looking Data

The instructor built a Python Flask web application called "Titan" using a template from **2play.com** (a website template provider). This application serves web pages on **port 5000** and exposes its own **application-level metrics** at `/metrics` (HTTP request counts, response times, etc.). [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

The instructor repeatedly emphasizes that this application is **not part of the monitoring stack** — it exists solely to generate realistic metrics and logs for monitoring: *"Please do not worry. Most of the things are just relevant to generating metrics and logs. Only node exporter and alloy is the thing that will be relevant to the monitoring stack."* [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

The application has two pages: the main Titan page and a `/payment` page. It runs as a systemd service (not just a Python process) because, as the instructor states: *"we run everything as a service because we are DevOps, we should manage everything as a service."* [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

### Layer 2: Load and Log Generation Scripts — Fake Data for Monitoring

Two background scripts run to generate data: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**`load.sh`** — A while-true loop that repeatedly runs the `stress` command with random durations and random numbers of CPU workers. This creates **CPU spikes that go up and down** — producing realistic-looking metric graphs. The randomness is intentional: *"So we see the proper graph that we can use it as a metric."* [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**`generate_multi_logs.sh`** — Creates log files in `/var/log/titan/` with three files: `app1.log`, `app2.log`, `app3.log`. These contain fake access, error, and info log entries. The instructor notes this was created with GitHub Copilot: *"I have created this script by using GitHub Copilot. Of course I made many changes, but the ultimate aim was to have some log files which we can fetch and display on Grafana."* [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Important operational note:** These scripts are **not managed as services** — they run in the background. When the instance is stopped, they die and must be manually restarted: *"when we power off this, these scripts are going to be dead. They're not going to come up when we power on again."* [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

### Layer 3: Monitoring Agents (Node Exporter + Alloy) — The Actual Stack Components

**Node Exporter** — The same Prometheus agent seen in previous lectures. It's a binary that exposes **system metrics** (CPU, memory, disk) on **port 9100** at `/metrics`. Prometheus scrapes this endpoint. The installation follows the identical pattern: download binary from Prometheus downloads, extract, create user/group (`prometheus:prometheus`), create systemd service, start. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Alloy** — A more versatile agent that can both **expose metrics** (like Node Exporter) AND **push logs to Loki**. It's installed from a repository (`apt install alloy`) rather than downloading a binary — a simpler installation method. Alloy runs on **port 12345** by default and has a web UI for checking the health of its log and metric pipelines. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

## 1.3 — Alloy Configuration: The Wiring Between Components

Alloy's configuration file (`/etc/alloy/config.alloy`) is the **critical wiring point** that connects the application server to both Prometheus and Loki. The configuration contains IP addresses that must be manually set: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Prometheus endpoint** — Where Alloy pushes metrics: `http://<prometheus-private-ip>:19090` (the instructor uses private IPs, not public, because the servers are in the same VPC). [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Local metrics source** — The Titan Flask app exposes metrics at `localhost:5000/metrics`. Alloy scrapes these locally and forwards them to Prometheus. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Loki endpoint** — Where Alloy pushes logs: `http://<loki-private-ip>:3100`. Alloy reads log files from the filesystem (like `/var/log/titan/`) and pushes them to Loki. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

The instructor also mentions a default behavior that must be changed for remote access: Alloy's web UI listens on `localhost` only by default. To access it from a browser, you must add `--server.http.listen-addr=0.0.0.0:12345` to `/etc/default/alloy` and restart the service. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

## 1.4 — Push vs. Pull: Two Data Flow Directions in the Stack

The monitoring stack uses **both** data flow patterns: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Pull (scraping):** Prometheus actively reaches out to targets (Node Exporter on port 9100, Titan app on port 5000) and pulls metrics at regular intervals. This requires the target to have ports open toward Prometheus.

**Push:** Alloy actively sends logs **to** Loki on port 3100. The application server initiates the connection. This requires Loki to have port 3100 open to receive incoming data.

The instructor clarifies this for the security group rules: *"Loki we don't need to do anything because Loki we are going to push the logs to Loki right on port 3100. We push it to Loki so we don't need to add anything over here \[on the web server's SG]."* [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

## 1.5 — Security Group Architecture: Who Talks to Whom

The security group rules reveal the complete communication architecture: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Loki SG:**

* Port 22 from My IP (SSH)
* Port 3100 from anywhere (temporarily; should be restricted to web server and Grafana)

**Web SG:**

* Port 22 from My IP (SSH)
* Port 5000 from My IP (view app in browser) + from Prometheus SG (scraping app metrics)
* Port 9100 from My IP (view node exporter in browser) + from Prometheus SG (scraping system metrics)

**Not needed on Web SG:** Port 3100 — because the web server **pushes** to Loki, it doesn't need to receive connections from Loki. The web server is the client in the Alloy → Loki connection. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

> ⚠️ **Expert Note**
>
> The instructor explicitly flags the "3100 from anywhere" rule on Loki as non-production: *"Definitely not production use case. We are going to change that later."* In production, Loki's port 3100 should only be accessible from specific application server security groups and Grafana's security group. The temporary "anywhere" rule exists only because the web server hasn't been created yet when Loki is being set up. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

## 1.6 — The Recurring Binary Setup Pattern

The instructor notes that Loki's setup is *"similar to Prometheus"* — and indeed, Node Exporter follows the same pattern too. This is a **recurring infrastructure pattern** across the entire monitoring stack: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

1. Define version and download URL as variables
2. Create directories (config, data, binary location)
3. Download the archive (wget from GitHub releases)
4. Extract (unzip/tar)
5. Move binary to `/usr/local/bin/`
6. Set executable permissions
7. Create dedicated system user and group
8. Set directory ownership
9. Create configuration file
10. Create systemd service file (with ExecStart pointing to binary + config)
11. Open firewall port (UFW)
12. `systemctl daemon-reload`, `enable`, `start`

Prometheus, Loki, and Node Exporter all follow this exact sequence. The only differences are: the binary name, the port, the config file content, and the user/group name. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

## 1.7 — IP Address Management: Private IPs and the Restart Problem

The instructor uses **private IPs** for inter-server communication (Alloy → Prometheus, Alloy → Loki). Private IPs stay stable as long as the instance exists (even across stop/start cycles in the same VPC). [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

However, **public IPs change** when instances are stopped and started. The instructor warns: *"when you power on these instances, its public IP will change. And also your public IP might also change. So later you need to update the security group."* Security group rules referencing "My IP" for SSH will need updating when your ISP assigns you a new IP. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are setting up two EC2 instances: **(1)** a **Loki server** for log aggregation and **(2)** a **web application server** running a Flask app, Node Exporter, Alloy agent, and background load/log generators. The final outcome: a complete monitoring stack where Prometheus scrapes metrics from the web server, Alloy pushes logs from the web server to Loki, and Grafana (set up previously) can visualize both metrics and logs. After this lecture, all four stack components are operational.

***

## Part A: Loki Server Setup

### Step 1: Launch the Loki EC2 Instance

1. AWS Console → **Launch Instance** [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)
2. Name: `Loki Server`
3. OS: **Ubuntu**
4. Instance type: **t2.micro**
5. Key pair: same as other instances
6. **Security Group** — create new: `loki-sg`
   * Port 22 from **My IP** (SSH)
   * Port 3100 from **Anywhere** (temporary — will restrict later) [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)
7. **Launch Instance**

**Why port 3100 from anywhere:** The web server (which will push logs to Loki) doesn't exist yet, so we can't reference its security group. This will be tightened later. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

### Step 2: SSH In and Run the Setup Script

```bash
ssh -i <key-path> ubuntu@<loki-public-ip>
sudo -i
```

**Download the setup script from GitHub:**

1. Go to the project repository → **monitoring branch** → locate the Loki setup script [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)
2. Click **Raw** → copy the URL

```bash
wget <raw-script-url>
chmod +x <script-name>.sh
./<script-name>.sh
```

<cite>turn19search13</cite>

**What the script does internally (in order):**

1. Sets variables (version, URLs, paths)
2. Creates directories (`/etc/loki`, `/var/lib/loki/chunks`, `/var/lib/loki/rules`)
3. Installs `unzip`
4. Downloads and extracts Loki binary → moves to `/usr/local/bin/loki`
5. Sets executable permissions
6. Creates `loki` user and group
7. Sets ownership on data and config directories
8. Writes `/etc/loki/config.yml`
9. Creates systemd service file
10. Opens firewall port 3100 (`ufw allow 3100`)
11. `systemctl daemon-reload`, `enable`, `start loki`
12. Waits \~120s for readiness check [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

### Step 3: Verify Loki Is Running

The script includes a readiness check, but it may complete before Loki is actually ready. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**If the script says "Ingestor is not ready":** Wait 30-60 more seconds and run the readiness check command again manually. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Expected result:** Output shows `"ready"` [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Verify version:**

```bash
loki --version
```

 [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Stop the instance** after confirming Loki is set up (to save costs):
EC2 → select Loki instance → Instance State → **Stop Instance** [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

## Part B: Web Application Server Setup

### Step 4: Launch the Web Server EC2 Instance

1. AWS Console → **Launch Instance** [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)
2. Name: `web01`
3. OS: **Ubuntu 24**
4. Instance type: **t2.micro**
5. Key pair: same
6. **Security Group** — create new: `web-sg`

| Port | Source        | Purpose                           |
| ---- | ------------- | --------------------------------- |
| 22   | My IP         | SSH                               |
| 5000 | My IP         | View Titan app in browser         |
| 5000 | Prometheus SG | Prometheus scrapes app metrics    |
| 9100 | My IP         | View Node Exporter in browser     |
| 9100 | Prometheus SG | Prometheus scrapes system metrics |

 [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**NOT needed:** Port 3100 — the web server pushes TO Loki; it doesn't receive from Loki. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

7. **Launch Instance**

***

### Step 5: SSH In and Download the Setup Script

```bash
ssh -i <key-path> ubuntu@<web01-public-ip>
sudo -i
```

```bash
wget <raw-url-of-web-node-setup.sh>
chmod +x web-node-setup.sh
```

 [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

### Step 6: Edit IP Addresses in the Script BEFORE Running

**This is critical — you must update two IP addresses before execution.** [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

```bash
vim web-node-setup.sh
```

**Find the Alloy configuration section** and update: [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

1. **Prometheus IP** — Replace the placeholder `PROMETHEUS_IP` with the **private IP** of the Prometheus instance
   * Find it: EC2 Console → select Prometheus instance → copy Private IP
   * Format in script: `http://<prometheus-private-ip>:19090` [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

2. **Loki IP** — Replace the placeholder `LOKI_IP` with the **private IP** of the Loki instance
   * Find it: EC2 Console → select Loki instance → copy Private IP
   * Format in script: `http://<loki-private-ip>:3100` <cite>turn19search13</cite>

**Use private IPs, not public IPs** — all servers are in the same VPC. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Double-check the syntax** — incorrect IP or missing port will break Alloy's connectivity.

Save and quit (`:wq`).

***

### Step 7: Run the Setup Script

```bash
./web-node-setup.sh
```

**Takes several minutes.** The script installs: Node Exporter, Python/Flask, the Titan app, Alloy, load scripts, and log generation scripts. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

### Step 8: Verify Everything Is Running

**Titan Flask App (port 5000):**

* Browser → `http://<web01-public-ip>:5000` → Titan web page loads
* Browser → `http://<web01-public-ip>:5000/payment` → Payment page loads
* Browser → `http://<web01-public-ip>:5000/metrics` → Application metrics (HTTP-related) [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Node Exporter (port 9100):**

* Browser → `http://<web01-public-ip>:9100/metrics` → System metrics (CPU, disk, memory) [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Load generation script:**

```bash
ps -ef | grep load.sh
```

Should show the script running in background. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Verify CPU load:**

```bash
top
```

CPU utilization should spike up and down (50% average, fluctuating). Press `q` to quit. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Log generation:**

```bash
ls /var/log/titan/
```

Should show: `app1.log`, `app2.log`, `app3.log` [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

The Titan Flask app also generates its own logs: `access.log`, `error.log`, `info.log` [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

### Step 9: Stop the Instance

```bash
exit  # from root
exit  # from SSH
```

EC2 Console → select web01 → Instance State → **Stop Instance** [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

**Remember:** Public IPs will change on restart. Security group rules with "My IP" may need updating. Background scripts (load.sh, generate\_multi\_logs.sh) will need to be restarted manually. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Complete Monitoring Stack (After This Lecture)

```
GRAFANA (visualization)          PROMETHEUS (metrics)
  │  Port: 3000                    │  Port: 19090
  │  Queries Prometheus + Loki     │  SCRAPES targets:
  │                                │    ├── web01:9100 (Node Exporter = system metrics)
  │                                │    └── web01:5000/metrics (Titan app = app metrics)
  │                                │
  ├── Queries ─────────────────────┘
  │
  └── Queries ─────────────────────┐
                                   │
LOKI (log aggregation)            WEB01 (application server)
  │  Port: 3100                    │  Components:
  │  RECEIVES logs                 │    ├── Titan Flask App (port 5000)
  │  ◄──── pushed by Alloy        │    ├── Node Exporter (port 9100)
  │                                │    ├── Alloy agent (port 12345)
  │                                │    │     ├── pushes logs → Loki:3100
  │                                │    │     └── pushes app metrics → Prometheus:19090
  │                                │    ├── load.sh (background, generates CPU stress)
  │                                │    └── generate_multi_logs.sh (background, generates logs)
```

***

## 🔷 Data Flow Directions

```
PULL (scraping):
  Prometheus ──scrapes──► Node Exporter (port 9100)
  Prometheus ──scrapes──► Titan App (port 5000/metrics)

PUSH:
  Alloy ──pushes logs──► Loki (port 3100)
  Alloy ──pushes metrics──► Prometheus (port 19090)

QUERY:
  Grafana ──queries──► Prometheus (metrics)
  Grafana ──queries──► Loki (logs)
```

***

## 🔷 Loki Setup (Compressed)

```
Binary: /usr/local/bin/loki
Config: /etc/loki/config.yml
Data:   /var/lib/loki/ (chunks/, rules/)
User:   loki:loki
Port:   3100
Service: systemctl start loki

Readiness: takes >120s (ingestor initialization)
Verify: readiness endpoint → "ready"
        loki --version

Setup pattern: IDENTICAL to Prometheus
  download → extract → binary → user → config → systemd → firewall → start
```

***

## 🔷 Web Server Components Map

```
WEB01 INSTANCE:

MONITORING STACK COMPONENTS (relevant):
  ├── Node Exporter     → port 9100 → system metrics → scraped by Prometheus
  └── Alloy             → port 12345 → pushes logs to Loki, metrics to Prometheus
       Config: /etc/alloy/config.alloy
       IPs to set: Prometheus private IP, Loki private IP

APPLICATION (test data generators, NOT monitoring stack):
  ├── Titan Flask App   → port 5000 → web pages + app metrics at /metrics
  ├── load.sh           → background → stress command → CPU spikes
  └── generate_multi_logs.sh → background → /var/log/titan/app{1,2,3}.log

"Only node exporter and alloy is the thing relevant to the monitoring stack."
```

***

## 🔷 Alloy Configuration (Critical IPs)

```
/etc/alloy/config.alloy

MUST SET BEFORE RUNNING:
  Prometheus: http://<prometheus-PRIVATE-ip>:19090
  Loki:       http://<loki-PRIVATE-ip>:3100

LOCAL (no change needed):
  Titan app metrics: localhost:5000/metrics
  Node exporter:     localhost:9100/metrics

WEB UI ACCESS:
  Default: listens on localhost only
  Fix: /etc/default/alloy → add --server.http.listen-addr=0.0.0.0:12345
  Then: systemctl restart alloy
```

***

## 🔷 Security Groups (Complete Wiring)

```
LOKI-SG:
  22   ← My IP (SSH)
  3100 ← Anywhere (TEMP → later restrict to web-sg + grafana-sg)

WEB-SG:
  22   ← My IP (SSH)
  5000 ← My IP + Prometheus-SG (app + scraping)
  9100 ← My IP + Prometheus-SG (node exporter + scraping)
  
  NOT NEEDED: 3100 (web PUSHES to Loki, doesn't receive)

PROMETHEUS-SG: (from previous lectures)
  22    ← My IP
  19090 ← Grafana-SG + web-SG (receives metrics)

GRAFANA-SG: (from previous lectures)
  22   ← My IP
  3000 ← My IP (dashboard access)
```

***

## 🔷 Recurring Binary Setup Pattern (Used 3x in Stack)

```
1. Variables (version, URL, paths)
2. mkdir config + data dirs
3. wget binary archive from GitHub
4. Extract (unzip/tar)
5. mv binary → /usr/local/bin/<name>
6. chmod +x
7. Create user:group (no login shell)
8. chown data + config dirs
9. Write config file
10. Write systemd service file (ExecStart = binary + config)
11. ufw allow <port>
12. systemctl daemon-reload && enable && start

Applied to: Prometheus, Loki, Node Exporter
Exception: Alloy uses apt install (repository-based)
```

***

## 🔷 Metrics Types on Web Server

```
PORT 5000/metrics → APPLICATION metrics (Titan Flask)
  → HTTP request counts, response times, status codes
  → Generated by the Flask app itself

PORT 9100/metrics → SYSTEM metrics (Node Exporter)
  → CPU, memory, disk, network, filesystem
  → Generated by Node Exporter reading /proc, /sys
  
Both scraped by Prometheus, but they measure DIFFERENT things.
```

***

## 🔷 Operational Warnings

```
SCRIPTS NOT MANAGED AS SERVICES:
  load.sh + generate_multi_logs.sh → die on instance stop
  Must restart manually after power-on

PUBLIC IPS CHANGE ON RESTART:
  → Update "My IP" rules in security groups
  → Public IPs of instances change too

PRIVATE IPS STABLE:
  → Alloy config uses private IPs (correct)
  → No update needed on restart for inter-service communication

EDIT SCRIPT BEFORE RUNNING:
  → Must replace Prometheus IP and Loki IP placeholders
  → Use PRIVATE IPs, not public
  → Verify syntax (http://ip:port format)
```

***

## 🔷 Log File Structure on Web Server

```
/var/log/titan/
  ├── app1.log    ← generated by generate_multi_logs.sh
  ├── app2.log    ← generated by generate_multi_logs.sh
  ├── app3.log    ← generated by generate_multi_logs.sh
  ├── access.log  ← generated by Titan Flask app
  ├── error.log   ← generated by Titan Flask app
  └── info.log    ← generated by Titan Flask app

Alloy reads these files → pushes to Loki → queryable in Grafana
```

***

## 🔷 The "Everything as a Service" Principle

```
"We are DevOps, we should manage everything as a service."

Titan Flask app → systemd service (systemctl start titan)
Node Exporter   → systemd service (systemctl start node)
Alloy           → systemd service (systemctl start alloy)
Loki            → systemd service (systemctl start loki)
Prometheus      → systemd service (from previous lecture)

WHY: services auto-start on boot, can be monitored,
     can be stopped/restarted cleanly, have logs in journalctl

EXCEPTION: load.sh + generate_multi_logs.sh → NOT services
           → instructor acknowledges this gap
           → "we have to run them again later"
```

This distinction — what's managed as a service and what isn't — determines what survives a reboot and what requires manual intervention. In production, everything should be a service or managed by an orchestrator. [\[254-loki-a...rver-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/254-loki-and-web-server-setup.txt)
