# 🎓 Deep Learning Material: Adding a Node to Prometheus — Scrape Configuration & Metrics Exposure

**Source:** [255-adding-a-node-to-prometheus.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt?EntityRepresentationId=8e1e7d79-119e-4304-9be5-523ecabebf4a) — Video lecture covering adding a web server as a monitoring target in Prometheus by editing `prometheus.yml`, the difference between system metrics (Node Exporter on port 9100) and application metrics (Python Flask on port 5000), generating fake load and web traffic for realistic monitoring data, scrape configuration with jobs/labels/targets, and troubleshooting target health. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Prometheus Is — The Monitoring and Alerting Toolkit

Prometheus is an open-source monitoring and alerting toolkit. Its core job is to **collect metrics** from systems and applications — a process called **scraping**. It stores these metrics in a **time-series database**, meaning every data point is associated with a timestamp. To retrieve and analyze this stored data, you use **PromQL** (Prometheus Query Language). The instructor notes that PromQL is a vast subject on its own; this course covers enough to monitor systems, create Grafana dashboards, and send alert notifications, but the complete PromQL training is available on the Prometheus website. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.2 The Scraping Model — How Prometheus Collects Metrics

Prometheus operates on a **pull model**. It does not wait for systems to send data to it. Instead, Prometheus **actively reaches out** to its configured targets at a regular interval, pulls (scrapes) the metrics from them, and stores the results. The scrape interval is configured in the `prometheus.yml` file under `global` settings — in this setup, it is **15 seconds**. Every 15 seconds, Prometheus contacts each target, reads the metrics exposed at that target's endpoint, and records them with a timestamp. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

There is also an `evaluation_interval` setting (also 15 seconds). This controls how often Prometheus evaluates its **alerting rules** — conditions you define to trigger alerts. The instructor deliberately defers this topic: "this might be a little confusing. For now you can just leave evaluation rule. We'll talk about it in Grafana." [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.3 Metrics Exposure — How Targets Make Data Available

For Prometheus to scrape a target, that target must **expose metrics at an HTTP endpoint**. The target doesn't push data — it simply makes its metrics available at a URL, and Prometheus comes and reads them. There are two distinct types of metrics demonstrated in this video:

### System Metrics via Node Exporter (Port 9100)

**Node Exporter** is a Prometheus component that runs on the target machine as a service. It collects **system-level metrics** — CPU usage, disk I/O, memory utilization, network statistics — and exposes them at `http://<ip>:9100/metrics`. When you access this URL in a browser, you see raw metric data in Prometheus exposition format — hundreds of metric lines covering every aspect of the system's hardware and OS state. The Node Exporter was set up on the web server in a previous lecture using a setup script (`web_node_setup.sh`), which downloaded the Node Exporter binary, extracted it, and configured it as a systemd service running on port 9100. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

### Application Metrics via Python Flask (Port 5000)

The web server also runs a **Python Flask application** on port 5000. This application exposes its own **application-level metrics** — things like HTTP request counts, response times, and endpoint-specific statistics. These are not system metrics; they are metrics about the application's behavior. The Flask application has been instrumented to expose metrics in Prometheus format, making them scrapable alongside the system metrics. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

The critical distinction is: **system metrics** tell you about the machine (CPU, memory, disk), while **application metrics** tell you about the software running on it (request counts, page hits). Both are important for complete monitoring, and both are configured as separate scrape jobs in Prometheus because they run on different ports and represent different monitoring dimensions. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

🔍 **Deep Dive**
The metrics exposed at `/metrics` on port 9100 are in Prometheus's own text-based exposition format. Each line contains a metric name, optional labels in curly braces, and a numeric value. For example, `node_cpu_seconds_total{cpu="0",mode="idle"} 12345.67`. Prometheus parses these lines, associates them with the job and instance labels from the scrape config, adds a timestamp, and stores them in its time-series database. The path `/metrics` is the conventional default endpoint, though it can be customized. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.4 The Prometheus Configuration File (`prometheus.yml`)

The central configuration file is located at `/etc/prometheus/prometheus.yml`. This YAML file controls all of Prometheus's behavior. The key sections relevant to this lecture:

**`global`** — Contains settings that apply to all scrape jobs: `scrape_interval` (how often to scrape, default 15s here) and `evaluation_interval` (how often to evaluate alerting rules, also 15s). [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**`alerting`** — Configuration for Alert Manager. The instructor notes this will be managed through Grafana, so it is not the focus here. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**`scrape_configs`** — This is the most important section for this lecture. It defines the **jobs** — each job is a scrape target or group of targets. By default, Prometheus has one job configured: monitoring **itself** on `localhost:9090`. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.5 Jobs, Targets, and Labels — The Scrape Configuration Model

Each entry in `scrape_configs` is a **job**. A job has:

* **`job_name`** — A descriptive name identifying what this job monitors (e.g., `prometheus`, `web-server-system`, `web-server-appstat`).
* **`static_configs`** — Contains the list of **targets** to scrape. Each target is an `<ip>:<port>` pair.
* **`labels`** — Custom key-value pairs attached to every metric scraped from this job. Labels allow you to differentiate and filter metrics in PromQL queries. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

In the default configuration, there is one job called `prometheus` with target `localhost:9090` and label `app: prometheus`. This means Prometheus scrapes its own metrics endpoint. When you look at the targets page in the Prometheus UI, you see this job listed with its labels — both the custom label (`app: prometheus`) and labels that Prometheus adds automatically. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

In this lecture, two new jobs are added:

1. **`web-server-system`** — Targets the Node Exporter on the web server at `<private-ip>:9100`. Label: `app: web01-system`. Scrapes system metrics.
2. **`web-server-appstat`** — Targets the Flask application on the web server at `<private-ip>:5000`. Label: `app: web01-appstat`. Scrapes application metrics. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

The instructor names these distinctly and gives them different labels precisely so they can be differentiated in PromQL: "label helps us differentiate between metrics and find and get the right information." [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.6 Private IP vs Public IP — Network Topology for Monitoring

The web server's target IP in the Prometheus configuration uses the **private IP**, not the public IP. The reason: Prometheus and the web server are in the **same VPC/network**. Internal communication between instances in the same network should use private IPs — it's faster, more reliable, and doesn't route through the internet. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

The instructor generalizes: "There will be always in the same network." In production monitoring setups, the monitoring server and its targets are almost always on the same internal network. If you were running the load scripts from your local computer instead of from the Prometheus instance, you would use the public IP because your computer is outside the VPC. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.7 Generating Fake Load and Traffic — Why It's Needed

Before exploring PromQL and dashboards, you need **actual data** in Prometheus. An idle server with no load produces flat, uninteresting metrics. The video sets up two types of simulated activity:

**System load:** A script (`load.sh`) already running on the web server generates random CPU stress using `stress` commands. The `top` command shows load averages around 3.39 and CPU usage spiking to \~74%, going up and down randomly. This creates realistic CPU/memory metric patterns that will show spikes and valleys in Prometheus graphs. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**Web traffic:** Two scripts (`website-main.sh` and `website-payment.sh`) simulate user access to the web application. They use `curl` commands to hit the main page (`/`) and the payment page (`/payment`) on port 5000. The access is **randomized** to create spikes in the request graphs. These scripts are run from the **Prometheus instance** (not the web server), using the web server's **private IP** and port 5000. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

The instructor explicitly states: "This is just for learning purpose. This is not part of Monitoring stack. We're just trying to replicate the real time behavior." The scripts must run for at least **5-10 minutes** before proceeding to the next lecture so that Prometheus has enough data points to display meaningful graphs. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.8 Restarting Prometheus After Configuration Changes

After editing `prometheus.yml`, the changes do not take effect until Prometheus is restarted. The process requires two commands: `systemctl daemon-reload` (to pick up any systemd-level changes) followed by `systemctl restart prometheus`. After restarting, you must wait briefly (a minute or so) for Prometheus to start scraping the new targets. The targets' status then appears in the Prometheus UI under **Status → Target Health**. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.9 Troubleshooting Targets — Common Failure Causes

The video demonstrates a live mistake: the instructor initially configures the web server system metrics target with port `9090` instead of `9100`. This causes the target to show as **down** in the targets page. The fix: update the port to `9100` in the config file and restart Prometheus. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

The instructor provides a systematic troubleshooting checklist for when targets show down or errors:

1. **Configuration file** — Check `prometheus.yml` for YAML syntax errors. Indentation must be exact. Port numbers and IP addresses must be correct.
2. **Port numbers** — Verify the correct port: 9100 for Node Exporter (system metrics), 5000 for the Flask app (application metrics), 9090 for Prometheus itself.
3. **Security groups** — Ensure AWS security group rules allow traffic on ports 9100 and 5000 from the Prometheus instance (or from anywhere, as a debugging step: "you can open it for anywhere if things are not working").
4. **Restart Prometheus** — After any config change, restart the service. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## 1.10 Security Group Updates — IP Change Awareness

The video begins with a practical operational note: if you're resuming work the next day, your local IP address may have changed (dynamic IP from ISP). All security group rules that reference "My IP" need to be updated. The instructor checks and updates the security group rules for both the web server and Prometheus instances, ensuring SSH (port 22), the Prometheus port (1990 in this setup), and other ports are accessible from the current IP. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

⚠️ **Expert Note**
This is a recurring operational task whenever you work with AWS security groups using "My IP" rules and a dynamic home IP. In production, this is handled differently — either with VPN-based access, static IPs, or bastion hosts — but in a learning environment, manual IP updates in security groups are expected. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are configuring Prometheus to monitor a web server by adding it as a scrape target — once for system metrics (Node Exporter, port 9100) and once for application metrics (Flask app, port 5000). We also set up simulated load and web traffic so Prometheus has realistic data to collect. The final outcome: the Prometheus targets page shows three targets (Prometheus itself + two web server jobs), all with status **UP**. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## Step 1: Update Security Group Rules (If IP Changed)

If you're resuming from a previous session, your public IP may have changed.

Navigate to **AWS Console → EC2 → Security Groups**. For each security group (web server, Prometheus, and optionally Grafana):

1. Click **Edit inbound rules**.
2. Find rules referencing your IP.
3. Update them to your current IP (select "My IP" from the dropdown).
4. **Save rules**. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

Ports to verify:

* Web server: SSH (22), Node Exporter (9100), Flask app (5000)
* Prometheus: SSH (22), Prometheus UI (1990) [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## Step 2: Generate System Load on the Web Server

**2a. SSH into the web server:**

```bash
ssh -i <path-to-key> ubuntu@<web-server-public-ip>
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**2b. Run the load generation script:**

The script `load.sh` should already exist on the web server from previous setup. Execute the command referenced in the setup instructions (available via `cat` of the setup script or from the GitHub repository). This runs stress commands that generate random CPU load. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**2c. Verify the load is running:**

```bash
ps -ef | grep load.sh
```

You should see the script process running. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

```bash
top
```

Verify: load averages should be non-zero (e.g., \~3.39), CPU usage should spike (e.g., \~74%), and you should see `stress` commands in the process list. Press `q` to quit `top`. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## Step 3: Set Up Web Traffic Simulation Scripts

**3a. SSH into the Prometheus server:**

```bash
ssh -i <path-to-key> ubuntu@<prometheus-public-ip>
sudo -i
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

We run the traffic scripts from Prometheus because it's in the same network as the web server, and it's an instance that's already running.

**3b. Download the main page traffic script:**

Navigate to the GitHub repository in your browser: `github.com/hkhcoder/vprofile-project`, switch to the **monitoring** branch. Find `website-main.sh`. Click **Raw**, copy the URL.

```bash
wget <raw-github-url-for-website-main.sh>
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**3c. Edit the script with the web server's private IP:**

```bash
vim website-main.sh
```

Find the IP address in the script (appears at two places). Replace it with the **private IP** of your web server. Ensure the port is **5000**. Save and quit. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**3d. Download and edit the payment page script:**

Repeat the same process for `website-payment.sh`:

```bash
wget <raw-github-url-for-website-payment.sh>
vim website-payment.sh
```

Replace the IP at both places with the web server's private IP. Ensure port is **5000**. Save and quit. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**3e. Make both scripts executable:**

```bash
chmod +x website-main.sh
chmod +x website-payment.sh
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

| Part    | Meaning                 |
| ------- | ----------------------- |
| `chmod` | Change file permissions |
| `+x`    | Add execute permission  |

**3f. Run both scripts in the background:**

```bash
nohup ./website-main.sh &
nohup ./website-payment.sh &
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

| Part                | Meaning                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| `nohup`             | "No hang up" — keeps the process running even if you close the terminal |
| `./website-main.sh` | Execute the script in the current directory                             |
| `&`                 | Run in the background, return control to the shell                      |

**3g. Verify both scripts are running:**

```bash
ps -ef | grep website
```

You should see both `website-main.sh` and `website-payment.sh` processes. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**Let the scripts run for at least 5-10 minutes** before proceeding. This generates enough data points for meaningful Prometheus queries. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## Step 4: Verify Prometheus and Web Server Are Accessible

**4a. Check Prometheus UI:**

Open browser: `http://<prometheus-public-ip>:1990`

Navigate to **Status → Target Health**. You should see one target: `prometheus` with status **UP**. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**4b. Check Node Exporter on web server:**

Open browser: `http://<web-server-public-ip>:9100`

You should see the "Prometheus Node Exporter" page. Click the **Metrics** link (or navigate to `/metrics`). You'll see raw system metrics — CPU, disk, memory — in text format. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**4c. Check the web application:**

Open browser: `http://<web-server-public-ip>:5000`

You should see the main page. Navigate to `/payment` to see the payment page. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## Step 5: Edit the Prometheus Configuration to Add the Web Server

**5a. Open the config file:**

On the Prometheus server (as root):

```bash
vim /etc/prometheus/prometheus.yml
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**5b. Locate the existing scrape config:**

Scroll down to `scrape_configs:`. You'll see the existing job for Prometheus itself:

```yaml
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
        labels:
          app: prometheus
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**5c. Add the system metrics job:**

Copy the existing job block (the instructor uses Vim: position cursor, type `10yy` to yank 10 lines, go to the end with `G`, paste with `p`). Modify the copy:

```yaml
  - job_name: 'web-server-system'
    static_configs:
      - targets: ['<web-server-private-ip>:9100']
        labels:
          app: web01-system
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

| Field         | Value               | Reason                                                         |
| ------------- | ------------------- | -------------------------------------------------------------- |
| `job_name`    | `web-server-system` | Identifies this job as system metrics for the web server       |
| `targets`     | `<private-ip>:9100` | Node Exporter runs on port 9100; use private IP (same network) |
| `labels: app` | `web01-system`      | Custom label to identify and filter these metrics in PromQL    |

⚠️ The port must be **9100**, not 9090. The video shows the instructor initially using 9090 (Prometheus's own port), which causes the target to show as **down**. This is corrected later. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

**5d. Add the application metrics job:**

Copy the same block again and modify:

```yaml
  - job_name: 'web-server-appstat'
    static_configs:
      - targets: ['<web-server-private-ip>:5000']
        labels:
          app: web01-appstat
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

| Field         | Value                | Reason                                            |
| ------------- | -------------------- | ------------------------------------------------- |
| `job_name`    | `web-server-appstat` | Identifies this job as application statistics     |
| `targets`     | `<private-ip>:5000`  | Flask application exposes metrics on port 5000    |
| `labels: app` | `web01-appstat`      | Custom label to differentiate from system metrics |

**5e. Review the entire file:**

Before saving, verify:

* YAML indentation is consistent (spaces, not tabs).
* IP addresses are correct (private IP of web server).
* Port numbers: `9090` for Prometheus self-monitoring, `9100` for Node Exporter, `5000` for Flask app.
* Job names and labels are distinct.

Save and quit: `Esc` → `:wq`. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## Step 6: Restart Prometheus

```bash
systemctl daemon-reload
systemctl restart prometheus
```

 [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

| Command                        | Purpose                                                                   |
| ------------------------------ | ------------------------------------------------------------------------- |
| `systemctl daemon-reload`      | Reloads systemd manager configuration (picks up any service file changes) |
| `systemctl restart prometheus` | Stops and restarts the Prometheus service, loading the new config         |

Wait approximately one minute for Prometheus to start scraping the new targets. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

## Step 7: Verify All Targets Are UP

Open browser: `http://<prometheus-public-ip>:1990`

Navigate to **Status → Target Health**. Refresh the page.

**Expected:** Three targets, all showing status **UP**:

| Job Name             | Target              | Label                | Port |
| -------------------- | ------------------- | -------------------- | ---- |
| `prometheus`         | `localhost:9090`    | `app: prometheus`    | 9090 |
| `web-server-system`  | `<private-ip>:9100` | `app: web01-system`  | 9100 |
| `web-server-appstat` | `<private-ip>:5000` | `app: web01-appstat` | 5000 |

<cite>turn9search10</cite>

### Troubleshooting if a Target Shows DOWN

Follow this sequence:

1. **Check port numbers** in `prometheus.yml` — most common error (9090 vs 9100 confusion).
2. **Check IP addresses** — must be the private IP of the web server.
3. **Check YAML syntax** — indentation errors break the config silently.
4. **Check security groups** — ports 9100 and 5000 must be open from the Prometheus instance. As a debugging step, open them from anywhere (`0.0.0.0/0`).
5. **Restart Prometheus** after every config change: `systemctl restart prometheus`. [\[255-adding...prometheus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/255-adding-a-node-to-prometheus.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture

```
[ Prometheus Server (port 1990/9090) ]
         │
         │  SCRAPES every 15 seconds (pull model)
         │
    ┌────┼──────────────────────┐
    ▼    ▼                      ▼
  self   Node Exporter          Flask App
  :9090  :9100                  :5000
  │      │                      │
  │      └── web server ────────┘
  │          (same machine, 2 different ports)
  │
  Prometheus metrics    System metrics         Application metrics
  (self-monitoring)     (CPU, disk, memory)    (HTTP hits, page access)
```

***

## Port Map (Critical)

```
9090  → Prometheus self-monitoring (localhost only)
9100  → Node Exporter (system metrics) on web server
5000  → Flask application (app metrics) on web server
1990  → Prometheus UI (browser access)

⚠️ 9090 ≠ 9100 — most common config mistake (demonstrated live)
```

***

## Two Types of Metrics

```
SYSTEM metrics (Node Exporter :9100)     APPLICATION metrics (Flask :5000)
─────────────────────────────────────    ──────────────────────────────────
CPU, disk, memory, network               HTTP request counts, page hits
Exposed at: /metrics on port 9100        Exposed by Flask app on port 5000
Installed via: web_node_setup.sh         Built into the Python application
Job name: web-server-system              Job name: web-server-appstat
Label: web01-system                      Label: web01-appstat
```

***

## `prometheus.yml` Structure

```yaml
global:
  scrape_interval: 15s           # how often to pull metrics
  evaluation_interval: 15s       # how often to check alert rules (defer to Grafana lecture)

alerting:                        # Alert Manager config (managed via Grafana)

scrape_configs:                  # THE JOBS
  - job_name: 'prometheus'       # self-monitoring
    targets: ['localhost:9090']
    labels: { app: prometheus }

  - job_name: 'web-server-system'     # Node Exporter
    targets: ['<private-ip>:9100']
    labels: { app: web01-system }

  - job_name: 'web-server-appstat'    # Flask app
    targets: ['<private-ip>:5000']
    labels: { app: web01-appstat }
```

***

## Scrape Config Anatomy

```
job_name        → identifier for this scrape group
static_configs  → list of target endpoints
  targets       → ['<ip>:<port>'] — what to scrape
  labels        → { key: value } — custom metadata attached to all scraped metrics
                   used for filtering in PromQL
```

***

## IP Selection Rule

```
Same network (VPC):     use PRIVATE IP  (Prometheus → web server)
External (your laptop): use PUBLIC IP   (browser → web server)

Monitoring infrastructure → always same network → always private IP
```

***

## Operational Sequence

```
1. Update security groups (if IP changed)
2. SSH to web server → verify/start load.sh           → system load simulation
3. SSH to Prometheus → download traffic scripts        → web traffic simulation
   → edit private IP + port 5000 in both scripts
   → chmod +x both scripts
   → nohup ./script.sh & (both scripts)
4. Wait 5-10 minutes for data accumulation
5. Verify: Prometheus UI (targets), Node Exporter (:9100), Flask app (:5000)
6. Edit /etc/prometheus/prometheus.yml
   → add web-server-system job (:9100)
   → add web-server-appstat job (:5000)
7. systemctl daemon-reload && systemctl restart prometheus
8. Wait ~1 min → verify all 3 targets show UP
```

***

## Load/Traffic Simulation Setup

```
ON WEB SERVER:
  load.sh (already running) → stress commands → random CPU spikes
  Verify: ps -ef | grep load.sh  /  top (load avg, CPU %)

ON PROMETHEUS (same network):
  wget scripts from GitHub (monitoring branch)
  Edit: private IP of web server + port 5000
  chmod +x website-main.sh website-payment.sh
  nohup ./website-main.sh &
  nohup ./website-payment.sh &
  Verify: ps -ef | grep website

Scripts use curl → hit / and /payment on :5000 → random intervals → create traffic spikes
Purpose: generate realistic data for PromQL learning (NOT part of monitoring stack)
```

***

## Config Change Workflow

```
Edit prometheus.yml → systemctl daemon-reload → systemctl restart prometheus → wait → verify targets
                                                                                          │
                                                                               Status → Target Health
                                                                               All targets: UP ✓
```

***

## Troubleshooting Checklist (Target DOWN)

```
1. Port number correct?    (9100 for Node Exporter, NOT 9090)
2. IP address correct?     (private IP of web server)
3. YAML syntax correct?    (indentation, colons, quotes)
4. Security groups open?   (9100, 5000 from Prometheus SG or 0.0.0.0/0)
5. Prometheus restarted?   (systemctl restart prometheus)
```

***

## Labels — Why They Matter

```
Without labels:  all metrics from all jobs mixed together
With labels:     app: web01-system   → filter system metrics only
                 app: web01-appstat  → filter app metrics only
                 app: prometheus     → filter self-monitoring only

Labels are KEY for PromQL queries, dashboard panels, and alert rules
```

***

## Key Engineering Patterns

| Pattern                             | Manifestation                                                                                                                |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Pull-based monitoring**           | Prometheus actively scrapes targets at intervals — targets are passive data exposers                                         |
| **Metrics exposure convention**     | Every target exposes metrics at an HTTP endpoint — standard interface regardless of what's being monitored                   |
| **Separation of metric domains**    | System metrics (Node Exporter) and app metrics (Flask) are separate jobs with separate labels — clean separation of concerns |
| **Same-network communication**      | Monitoring infra uses private IPs — faster, more secure, no internet routing                                                 |
| **Simulated load for learning**     | Fake load + fake traffic replicates real-world patterns — monitoring is meaningless without data                             |
| **Config-driven target management** | Adding/removing targets = editing YAML + restart — no agent installation on Prometheus side                                  |
| **Label-based filtering**           | Custom labels enable precise metric selection — foundational for dashboards and alerts                                       |

***

## Project Continuity

```
BEFORE: Prometheus + Node Exporter + Flask app installed and running
THIS:   Added web server as Prometheus target (system + app metrics) + load/traffic generation
NEXT:   PromQL queries to retrieve and analyze the collected metrics
```

***

This completes the full reconstruction. **Theory** explains the pull-based scraping model, system vs application metrics, and the scrape configuration structure. **Practical** walks through every script download, every config edit, and the port-number debugging episode. The **Compression Map** gives you the architecture, port map, and troubleshooting checklist for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
