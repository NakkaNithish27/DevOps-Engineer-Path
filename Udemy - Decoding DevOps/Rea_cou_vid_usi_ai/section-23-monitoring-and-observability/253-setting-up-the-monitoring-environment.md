# 🧠 Setting Up the Monitoring Environment — Prometheus, Grafana & Service Architecture on AWS

**Source:** *253. Setting Up the Monitoring Environment* — Monitoring & Observability Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Monitoring Stack — What We Are Building and Why

The goal of this lecture is to build a complete **monitoring and observability environment** composed of four EC2 instances, each running a distinct component:

1. **Grafana** — The visualization and dashboarding layer. It queries data from Prometheus and Loki and presents it as graphs, alerts, and dashboards.
2. **Prometheus** — The metrics collection engine. It **scrapes** (pulls) metrics from target systems at regular intervals and stores them in its own time-series database.
3. **Application Server** — A Python Flask application that generates **metrics and logs**. It runs exporters (Node Exporter, Alloy) that expose system and application data for Prometheus and Loki to collect.
4. **Loki** — The log aggregation system (set up in a later lecture).

These four components form a standard modern observability stack: applications and systems **expose** data → collection engines **gather** that data → visualization tools **present** it for humans. Understanding this architecture is foundational to monitoring in any production environment.

***

## 1.2 Binary vs. Service — The Critical Operational Distinction

All the tools in this stack — Prometheus, Grafana, Loki, Alloy, Node Exporter — are distributed as **binaries**. You can download the binary for your operating system, run it directly from the command line, and it works. But the instructor immediately flags this: *"That is not the right way to run in real time."*

Running a binary directly from the terminal has severe operational limitations: it stops when you close the terminal or log out, it doesn't restart automatically after a crash or reboot, and it can't be managed centrally. In production, these tools must run as **systemd services** — background processes managed by Linux's `systemctl` command. A service starts automatically on boot, restarts on failure, can be started/stopped/enabled/disabled through standardized commands, and its status can be queried programmatically.

The instructor draws a direct parallel: *"Similarly as we set up Tomcat service"* in earlier lectures. The pattern is identical regardless of what software you're running — download the binary, create a systemd service file, configure it, and manage it through `systemctl`. This is a **universal Linux service management pattern**.

> 🔍 **Deep Dive:** The distinction between "runs as a binary" and "runs as a service" is the difference between a **foreground process** and a **managed daemon**. A foreground process is tied to the terminal session that started it. A systemd-managed service is a daemon — it runs in the background, has a lifecycle managed by the init system, logs to the journal, and participates in the system's boot/shutdown sequence. Every production deployment of every server-side tool follows this pattern.

***

## 1.3 Grafana — Installation Model: Debian Package

Grafana follows a simpler installation path than Prometheus. It's distributed as a **Debian package** (`.deb` file) for Ubuntu systems. Debian packages are pre-built installation bundles that include the binary, configuration files, and the systemd service file — everything needed. When you install with `dpkg -i`, the package manager places files in the correct locations and registers the service automatically. After installation, you simply `enable` and `start` the Grafana service.

Grafana listens on **port 3000** by default. The default login credentials are **admin/admin**, and on first login, it prompts you to change the password.

The setup script's structure reveals a clean automation pattern: define variables (version, download URL, file name) → update the system → install dependencies → download the package → install with `dpkg -i` → enable and start the service. This is a repeatable, scriptable pattern.

***

## 1.4 Prometheus — Installation Model: Binary + Manual Service Setup

Prometheus follows a more involved installation path than Grafana. It's distributed as a **tarball** (`.tar.gz` archive) containing raw binaries and a default configuration file — but **no systemd service file**. You must create the service infrastructure yourself. The instructor explicitly connects this: *"It will be similar as we set up the Tomcat service. Download the binary, extract, set up the systemctl file, and then run it through systemctl command."*

### The Prometheus File System Layout

The setup script establishes a specific directory structure, and understanding where each component lives is essential:

| Path                                     | Purpose                                                                                       |
| ---------------------------------------- | --------------------------------------------------------------------------------------------- |
| `/usr/local/bin/`                        | Prometheus binaries (`prometheus`, `promtool`)                                                |
| `/etc/prometheus/`                       | Configuration directory (stores `prometheus.yml` and sub-dirs: `rules`, `rules.d`, `file_sd`) |
| `/var/lib/prometheus/`                   | Data directory (where Prometheus stores its time-series database)                             |
| `/etc/systemd/system/prometheus.service` | The systemd service file                                                                      |

### The Tarball Contents

When you download and extract the Prometheus tarball, the extracted folder contains:

* **`prometheus`** — The main binary
* **`promtool`** — A utility tool for checking configuration and rules
* **`prometheus.yml`** — The default configuration file

The binaries get moved to `/usr/local/bin/` (the standard location for locally installed binaries on Linux). The configuration file gets moved to `/etc/prometheus/` (the standard location for service configuration).

### User and Group Creation

The script creates a dedicated **`prometheus` user and group**. This is a security best practice — the Prometheus process runs under its own restricted user, not as root. The data directory (`/var/lib/prometheus/`) and configuration directory (`/etc/prometheus/`) are given ownership to this user/group with appropriate permissions (775 — full access for user and group, read+execute for others).

### The Systemd Service File

The most important part of the setup: the systemd service file at `/etc/systemd/system/prometheus.service`. This file tells systemd **how to run Prometheus**. The critical section is `ExecStart`, which defines the command systemd executes when you run `systemctl start prometheus`:

```
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --web.listen-address=:9090 \
  --web.enable-remote-write-receiver
```

**Flag breakdown:**

* `--config.file` — Points to the configuration file location
* `--storage.tsdb.path` — Points to the data storage directory
* `--web.listen-address=:9090` — Prometheus listens on **port 9090** (changeable here if needed)
* `--web.enable-remote-write-receiver` — Enables receiving metrics via **remote write** (push model). The instructor specifically highlights this: *"From the beginning I'm saying that Prometheus is going to scrape the metrics, but from Alloy, you can also send the metrics to Prometheus. If you want that to happen, you need to enable this option."*

After creating the service file: `systemctl daemon-reload` (reload systemd to recognize the new service file) → `systemctl enable prometheus` (start on boot) → `systemctl start prometheus` (start now).

> 🔍 **Deep Dive — Pull vs. Push Model:** Prometheus's native model is **pull-based** (scraping) — it reaches out to targets and collects metrics from their `/metrics` endpoints. But the `--web.enable-remote-write-receiver` flag enables a **push-based** path — external agents like Alloy can push metrics into Prometheus. This dual capability is architecturally significant: scraping works when Prometheus can reach the targets, but push is needed when targets are behind firewalls or when you want agents to control when data is sent. The flag must be explicitly enabled; it's not on by default.

***

## 1.5 The prometheus.yml Configuration File — Scrape Targets

The `prometheus.yml` file (from the tarball, moved to `/etc/prometheus/`) is the central configuration that defines **what Prometheus monitors**. By default, it contains a configuration to scrape **Prometheus itself** — Prometheus monitors its own metrics as a baseline. The instructor shows this in the Prometheus UI: under Status → Target Health, you can see it scraping `localhost:9090/metrics`.

The `/metrics` endpoint is a standard HTTP endpoint that exposes metrics in Prometheus's text format. When you access `<prometheus-ip>:9090/metrics` in a browser, you see raw metrics data — key-value pairs with labels that Prometheus collects and stores. In later lectures, this file will be edited to add other scrape targets (Node Exporter on the application server, etc.).

***

## 1.6 Prometheus Download Ecosystem

The instructor navigates to the Prometheus download page to show the broader ecosystem. Beyond Prometheus itself, the download page offers:

* **Alert Manager** — Handles alerting based on Prometheus rules
* **Node Exporter** — Exposes Linux system metrics (CPU, memory, disk, network) — will be set up on the application server
* **Blackbox Exporter** — Probes endpoints (HTTP, HTTPS, DNS, TCP, ICMP)
* **MySQL Exporter** — Exposes MySQL database metrics
* **Memcache Exporter, Graphite Exporter, Console Exporter** — Various specialized exporters

The instructor highlights Node Exporter specifically: *"This is the one we will be setting up on our web server."* The exporter pattern is central to Prometheus's architecture — exporters are lightweight agents that run on target machines, collect metrics specific to their domain, and expose them on HTTP endpoints for Prometheus to scrape.

Packages are available for **Linux (amd64)**, **Windows**, and **Darwin (macOS)**. The lecture uses Linux amd64.

***

## 1.7 Security Group Architecture — Port-Based Access Control

Each server gets its own **security group** with intentional, minimal port access. The instructor emphasizes naming security groups meaningfully because *"we will need to add this security group information in Prometheus."*

**Grafana Security Group:**

* Port 22 (SSH) from my IP — for administration
* Port 3000 from my IP — for browser access to the Grafana UI

**Prometheus Security Group:**

* Port 22 (SSH) from my IP — for administration
* Port 9090 from my IP — for browser access to the Prometheus UI
* Port 9090 from **Grafana Security Group** — so Grafana can query Prometheus for data

The third rule is architecturally critical: it establishes the **data flow path** between Grafana and Prometheus at the network level. Grafana needs to run PromQL queries against Prometheus's API on port 9090. By referencing the Grafana security group as the source (rather than a specific IP), the rule automatically applies to any instance in that security group — a scalable, maintainable approach.

> ⚠️ **Expert Note:** The instructor uses a single SSH key for all instances: *"This is definitely not production style. You should have different login keys."* In production, each server or server role should have its own key pair for security isolation — compromise of one key shouldn't grant access to the entire stack.

***

## 1.8 Setup Sequence — Learning vs. Production

The instructor establishes the setup order: Grafana → Prometheus → Application Server → Loki. But he immediately clarifies: *"In real time, the sequence does not matter."* In production, applications and systems exist first (generating metrics and logs), and the monitoring stack is set up afterward to observe them. The lecture's sequence is optimized for **learning** — setting up visualization first so you can verify each subsequent component as it's added.

***

## 1.9 Ephemeral Public IPs — Operational Awareness

The instructor warns about a critical AWS behavior: *"When you power on, you use its new IP because this IP will be gone. You'll get a new public IP."* EC2 instances with default networking get a new public IP every time they're stopped and started. Any SSH commands, browser bookmarks, or security group rules referencing the old IP will break.

This is mentioned when the instructor suggests shutting down instances between lectures to save costs. The operational implication: always check the new public IP after starting an instance.

***

## 1.10 The `--no-pager` Flag — Scripting-Friendly Output

The instructor encounters a minor operational issue: `systemctl status prometheus` pauses the output and waits for user input (pager behavior). Adding `--no-pager` makes the command print all output and return to the prompt immediately. This is essential for **scripts** — if a setup script includes `systemctl status` without `--no-pager`, the script hangs waiting for a keypress that never comes.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are setting up the first two servers of a monitoring stack on AWS EC2: a **Grafana server** (visualization) and a **Prometheus server** (metrics collection). Both will run as systemd services on Ubuntu instances, configured via bash scripts from a GitHub repository. By the end, both UIs will be accessible in the browser, and Prometheus will be scraping its own metrics.

**Final outcome:** Grafana accessible on `<ip>:3000` with login working, Prometheus accessible on `<ip>:9090` showing itself as a healthy scrape target. Application server and Loki follow in subsequent lectures.

***

## Step 1: Access the Setup Scripts on GitHub

Navigate to: **github.com/hkhcoder/vprofile-project** → switch to the **monitoring** branch.

This branch contains bash scripts for setting up each component:

* `grafana-setup.sh` — Grafana installation
* `prometheus-setup.sh` — Prometheus installation
* (Others for later lectures)

**Click on each script to review its contents before running.** Understanding what a script does before executing it is essential operational practice.

***

## Step 2: Launch the Grafana EC2 Instance

In the **AWS EC2 Console** (the instructor uses **North California** region) → **Launch Instance**:

| Field              | Value                                                                |
| ------------------ | -------------------------------------------------------------------- |
| **Name**           | `Grafana-Server`                                                     |
| **AMI**            | Ubuntu 24 (free tier)                                                |
| **Instance type**  | `t2.micro`                                                           |
| **Key pair**       | Create new: `monit-stack-key`, PEM format → download the `.pem` file |
| **Security group** | Create new: `Grafana-SG`                                             |

**Security group rules for Grafana-SG:**

| Type       | Port | Source | Purpose                      |
| ---------- | ---- | ------ | ---------------------------- |
| SSH        | 22   | My IP  | Administration access        |
| Custom TCP | 3000 | My IP  | Browser access to Grafana UI |

Click **Launch Instance**.

***

## Step 3: Install Grafana via Script

SSH into the Grafana instance:

```bash
ssh -i downloads/monit-stack-key.pem ubuntu@<grafana-public-ip>
```

**Command breakdown:**

* `-i downloads/monit-stack-key.pem` — path to the private key downloaded in Step 2
* `ubuntu` — default SSH user for Ubuntu AMIs
* `@<grafana-public-ip>` — the instance's public IP from the EC2 console

Switch to root:

```bash
sudo -i
```

Download the setup script from GitHub. Go to `grafana-setup.sh` on GitHub → click **Raw** → copy the URL. Then:

```bash
wget <raw-github-url-of-grafana-setup.sh>
chmod +x grafana-setup.sh
./grafana-setup.sh
```

**Command breakdown:**

* `wget <url>` — downloads the script file
* `chmod +x grafana-setup.sh` — grants execute permission
* `./grafana-setup.sh` — runs the script

**What the script does internally:** Sets version variables → `apt update` + `apt upgrade` → installs dependencies → downloads the Grafana `.deb` package → installs with `dpkg -i` → enables and starts the Grafana service via `systemctl`.

***

## Step 4: Verify Grafana

Open a browser and navigate to:

```
http://<grafana-public-ip>:3000
```

**Expected:** The Grafana login page loads (may take a moment initially).

**Default credentials:** Username: `admin`, Password: `admin`

After login, Grafana prompts for a **password reset**. Set a new password and remember it.

**Verification complete:** Grafana is running as a service, accessible on port 3000.

**Cost saving:** The instructor shuts down the instance after verification: *"You can shut it down for now."* ⚠️ Remember: when you power it back on, the **public IP will change** — you must use the new IP for SSH and browser access.

***

## Step 5: Launch the Prometheus EC2 Instance

Back in the EC2 Console → **Launch Instance**:

| Field              | Value                       |
| ------------------ | --------------------------- |
| **Name**           | `Prometheus-Server`         |
| **AMI**            | Ubuntu 24                   |
| **Instance type**  | `t2.micro`                  |
| **Key pair**       | Same `monit-stack-key`      |
| **Security group** | Create new: `Prometheus-SG` |

**Security group rules for Prometheus-SG:**

| Type       | Port | Source         | Purpose                            |
| ---------- | ---- | -------------- | ---------------------------------- |
| SSH        | 22   | My IP          | Administration                     |
| Custom TCP | 9090 | My IP          | Browser access to Prometheus UI    |
| Custom TCP | 9090 | **Grafana-SG** | Allows Grafana to query Prometheus |

The third rule is critical — search for your Grafana security group by name and select it. Add a description like *"Allows Grafana to run query"* or *"Allows Grafana."*

Click **Launch Instance**.

***

## Step 6: Install Prometheus via Script

SSH into the Prometheus instance:

```bash
ssh -i downloads/monit-stack-key.pem ubuntu@<prometheus-public-ip>
```

Switch to root:

```bash
sudo -i
```

Download and run the setup script:

```bash
wget <raw-github-url-of-prometheus-setup.sh>
chmod +x prometheus-setup.sh
./prometheus-setup.sh
```

**What the script does internally:**

1. Sets hostname to `prometheus`
2. Creates directories: `/etc/prometheus/` (config), `/var/lib/prometheus/` (data), subdirectories (`rules`, `rules.d`, `file_sd`)
3. Downloads the Prometheus tarball → extracts it
4. Creates `prometheus` user and group
5. Moves binaries (`prometheus`, `promtool`) to `/usr/local/bin/`
6. Moves `prometheus.yml` to `/etc/prometheus/`
7. Creates the systemd service file at `/etc/systemd/system/prometheus.service`
8. Sets ownership and permissions on config and data directories
9. Runs `systemctl daemon-reload` → `enable` → `start`
10. Checks status

**If the status output pauses (pager behavior):** Press `q` to quit. To avoid this in scripts, use:

```bash
systemctl status prometheus --no-pager
```

The `--no-pager` flag prints output and returns immediately — essential for non-interactive script execution.

**Verify Prometheus is running:**

```bash
systemctl status prometheus --no-pager
```

Expected: `Active: active (running)`.

***

## Step 7: Verify Prometheus in Browser

Open a browser:

```
http://<prometheus-public-ip>:9090
```

**Expected:** The Prometheus web UI loads.

**Verify scrape target:** Navigate to **Status → Target Health**. You should see Prometheus scraping **itself** at `localhost:9090/metrics` with status **UP**.

**View raw metrics:** Navigate to `http://<prometheus-public-ip>:9090/metrics` in the browser. This displays the raw metrics text that Prometheus collects from its own `/metrics` endpoint — key-value pairs in Prometheus exposition format.

**Verification complete:** Prometheus is running as a service, scraping its own metrics, and accessible on port 9090.

**Cost saving:** Shut down the instance if not continuing immediately. Remember the public IP will change on restart.

***

## Step 8: Explore the Prometheus Tarball Contents (Optional Exploration)

On any EC2 instance, download and extract the Prometheus tarball to examine its contents:

```bash
wget <prometheus-tarball-download-url>
tar xvfz prometheus-<version>.linux-amd64.tar.gz
cd prometheus-<version>.linux-amd64/
ls
```

**Contents:**

* `prometheus` — the main binary
* `promtool` — configuration checking utility
* `prometheus.yml` — default configuration file
* Other files (LICENSE, NOTICE, console templates)

This helps you understand what the setup script is working with — the tarball is the raw material, and the script transforms it into a properly installed, service-managed deployment.

> ⚠️ **Expert Note:** You can verify the Prometheus version after installation:
>
> ```bash
> prometheus --version
> ```
>
> This confirms the binary was correctly placed in `/usr/local/bin/` and is executable.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Monitoring Stack Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   Monitoring Environment                      │
│                   (4 EC2 instances, Ubuntu 24, t2.micro)      │
│                                                              │
│  ┌─────────────┐     queries :9090      ┌──────────────────┐ │
│  │   GRAFANA    │ ──────────────────────→│   PROMETHEUS     │ │
│  │   :3000      │                        │   :9090          │ │
│  │  (visualize) │                        │  (scrape metrics)│ │
│  └─────────────┘                        └────────┬─────────┘ │
│                                                   │ scrapes   │
│                                                   ▼           │
│  ┌─────────────┐                        ┌──────────────────┐ │
│  │    LOKI      │ ◄──── logs ───────────│  APP SERVER      │ │
│  │  (logs)      │                        │  (Flask + Node   │ │
│  │  [later]     │                        │   Exporter +     │ │
│  └─────────────┘                        │   Alloy)         │ │
│                                          └──────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

***

## Two Installation Models

```
MODEL 1: DEBIAN PACKAGE (Grafana)
  .deb file → dpkg -i → service file INCLUDED → systemctl enable/start
  SIMPLE: package handles everything

MODEL 2: BINARY + MANUAL SERVICE (Prometheus)
  .tar.gz → extract → move binaries to /usr/local/bin/
  → create user/group → create directories
  → create systemd service file manually
  → systemctl daemon-reload → enable → start
  COMPLEX: you build the service infrastructure yourself

SAME PATTERN AS: Tomcat service setup (earlier lectures)
```

***

## Prometheus File System Layout

```
/usr/local/bin/
  ├── prometheus          ← main binary
  └── promtool            ← config check utility

/etc/prometheus/
  ├── prometheus.yml      ← scrape configuration
  ├── rules/              ← alerting rules
  ├── rules.d/            ← additional rules
  └── file_sd/            ← file-based service discovery

/var/lib/prometheus/      ← time-series data storage

/etc/systemd/system/
  └── prometheus.service  ← systemd service file
```

***

## Prometheus Service File — ExecStart Flags

```
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml    ← config path
  --storage.tsdb.path=/var/lib/prometheus          ← data path
  --web.listen-address=:9090                       ← listen port
  --web.enable-remote-write-receiver               ← enable PUSH (from Alloy)

DEFAULT: Prometheus PULLS (scrapes)
WITH FLAG: also accepts PUSH (remote write)
```

***

## Security Group Architecture

```
Grafana-SG:
  22   ← My IP (SSH)
  3000 ← My IP (browser → Grafana UI)

Prometheus-SG:
  22   ← My IP (SSH)
  9090 ← My IP (browser → Prometheus UI)
  9090 ← Grafana-SG (Grafana queries Prometheus)
         ↑ security group reference, not IP — scalable

KEY: meaningful SG names matter (referenced cross-service)
```

***

## Setup Script Pattern (Both Services)

```
1. Define variables (version, URLs, paths)
2. apt update / upgrade
3. Install dependencies
4. Download package/tarball
5. Install (dpkg -i) OR extract + manual setup
6. [Binary model only]: create user/group, create dirs, set permissions
7. [Binary model only]: create systemd service file
8. systemctl daemon-reload (if new service file)
9. systemctl enable <service>
10. systemctl start <service>
11. Verify: systemctl status <service> --no-pager
```

***

## Operational Execution Sequence (This Lecture)

```
GRAFANA:
  1. Launch EC2 (Ubuntu 24, t2.micro, Grafana-SG: 22+3000)
  2. SSH → sudo -i
  3. wget script → chmod +x → run
  4. Verify: browser → <ip>:3000 → admin/admin → reset password

PROMETHEUS:
  1. Launch EC2 (Ubuntu 24, t2.micro, Prometheus-SG: 22+9090+9090-from-Grafana-SG)
  2. SSH → sudo -i
  3. wget script → chmod +x → run
  4. Verify: browser → <ip>:9090 → Status → Target Health → self-scrape UP
  5. Verify: <ip>:9090/metrics → raw metrics visible
```

***

## Prometheus Download Ecosystem

```
prometheus.io/download:
  Prometheus          ← metrics server (this lecture)
  Alert Manager       ← alerting
  Node Exporter       ← Linux system metrics (next lecture, on app server)
  Blackbox Exporter   ← endpoint probing
  MySQL Exporter      ← MySQL metrics
  Memcache Exporter   ← Memcache metrics
  + many more

Platforms: linux-amd64, windows, darwin(macOS)
```

***

## Key Operational Warnings

```
⚠️ Public IP changes on stop/start    → always check new IP after power-on
⚠️ Single SSH key for all instances   → NOT production-style; use separate keys
⚠️ systemctl status hangs in scripts  → add --no-pager flag
⚠️ Default Grafana password admin     → MUST change on first login; remember it
⚠️ Setup sequence ≠ production order  → in production, apps exist first, then monitoring
```

***

## Reusable Engineering Pattern: Binary-to-Service Transformation

```
PATTERN:
  Tool distributed as BINARY (download + run)
  Production requires SERVICE (managed daemon)

TRANSFORMATION STEPS:
  1. Create dedicated USER + GROUP (security isolation)
  2. Create DIRECTORY structure (config, data, binary locations)
  3. Move binary to STANDARD location (/usr/local/bin/)
  4. Move config to STANDARD location (/etc/<service>/)
  5. Create SYSTEMD SERVICE FILE (/etc/systemd/system/<service>.service)
     → ExecStart defines binary path + flags
  6. Set OWNERSHIP + PERMISSIONS on dirs
  7. systemctl daemon-reload → enable → start

WHERE ELSE THIS APPLIES:
  • Tomcat (already seen in this course)
  • Jenkins
  • Consul / Vault
  • Any binary-distributed tool on Linux
  • Node Exporter, Alert Manager, Loki (upcoming lectures)

ALTERNATIVE (simpler):
  Tool distributed as DEB/RPM PACKAGE → package handles steps 1-6
  (Grafana follows this simpler path)
```

***

## Prometheus Self-Monitoring Verification

```
Browser → <ip>:9090
  → Status → Target Health → localhost:9090/metrics → UP ✅

Browser → <ip>:9090/metrics
  → raw metrics in Prometheus exposition format ✅

MEANING: Prometheus scrapes itself by default as a baseline target
```

***

## Failure Signature Index

```
Grafana page won't load on :3000        → SG missing port 3000 rule, or service not started
Prometheus page won't load on :9090     → SG missing port 9090 rule, or service not started
SSH connection refused                  → wrong IP (changed after restart) or port 22 not open
systemctl status shows "failed"         → check script for errors; verify binary path in service file
Script hangs at systemctl status        → add --no-pager to the status command
Grafana can't query Prometheus          → Prometheus SG missing 9090-from-Grafana-SG rule
Old IP doesn't work after restart       → instance got new public IP; check EC2 console
```

***

## One-Line Mental Reload Trigger

> *"Four EC2 instances (Grafana :3000 deb-package, Prometheus :9090 binary-to-service, App server, Loki) — Grafana SG allows 3000, Prometheus SG allows 9090 from my-IP + Grafana-SG — Prometheus scrapes itself by default, enable remote-write-receiver for push — all tools run as systemd services, not bare binaries."*

This single sentence reconstructs the full stack architecture, both installation models, the security group cross-reference pattern, the default self-scrape behavior, the pull-vs-push flag, and the core operational principle. [\[253-settin...nvironment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/253-setting-up-the-monitoring-environment.txt)
