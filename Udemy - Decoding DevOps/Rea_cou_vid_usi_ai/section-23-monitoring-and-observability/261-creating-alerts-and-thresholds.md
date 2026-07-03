# 🚨 Grafana Alerts & Thresholds — Creating Monitoring Rules with Prometheus — Deep Learning Material

**Source:** *Creating Alerts and Thresholds* (Video Lecture Caption File) [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Core Concept — Thresholds and Alerts

A **threshold** is a boundary value you define for a metric. It represents the line between "normal" and "problematic." An **alert** is the automated action that triggers when a metric crosses (breaches) that threshold. Together, they form the core mechanism of proactive monitoring: instead of staring at dashboards waiting for something to go wrong, you define the conditions that constitute a problem, and the system notifies you automatically when those conditions are met. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

In this lecture, the monitoring stack is: **Prometheus** (collects and stores metrics) → **Grafana** (visualizes metrics and manages alerts) → **Slack** (receives notifications). The integration between Grafana and Slack was configured in a previous lecture. This lecture connects all three by creating a Prometheus query, a Grafana panel, a threshold, an alert rule, and a notification policy — the full chain from raw metric to human-readable notification.

***

## 1.2 The PromQL Query — Constructing a Meaningful Metric

Raw metrics from Prometheus are low-level system measurements. To make them useful for alerting, you need to **compose** them into meaningful indicators using PromQL (Prometheus Query Language). The instructor builds a query that calculates **root filesystem usage as a percentage**: [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

```promql
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100
```

**How this query is constructed step by step:**

1. **`node_filesystem_avail_bytes`** — a raw metric that reports the available (free) space on a filesystem, in bytes.
2. **`{mountpoint="/"}`** — a **label filter** that selects only the root partition. Without this filter, you'd get data for every mounted filesystem. The instructor also uses a label to select a specific system (the web server).
3. **`node_filesystem_size_bytes{mountpoint="/"}`** — the total size of the root filesystem in bytes.
4. **Division: `avail / size`** — produces the **available fraction** (e.g., 0.53 means 53% free).
5. **Multiply by 100** — converts the fraction to a percentage.
6. **`1 - (avail / size)`** — inverts from "available" to "used." If 53% is available, then `1 - 0.53 = 0.47`, meaning 47% is used.
7. **Final multiplication by 100** — produces the used percentage (47%).

The instructor builds this query incrementally in the Prometheus UI, testing each step. This is the correct approach: start with the raw metric, add filters, perform arithmetic, and verify the result at each step before using the query in Grafana. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

🔍 **Deep Dive:**
The query demonstrates a fundamental PromQL pattern: **derived metrics**. Raw Prometheus metrics are often just numbers (bytes available, bytes total). Useful monitoring requires computing ratios, percentages, rates of change, or averages — derived values that tell you something meaningful about system health. The formula `(1 - available/total) * 100` is a universal utilization pattern: it works for disk, memory, CPU, or any resource where you know the available amount and the total capacity.

***

## 1.3 Grafana Panels — Visualizing the Metric

A **panel** in Grafana is a single visualization widget (graph, gauge, stat, table, etc.) that displays the result of one or more queries. The instructor creates a panel inside an existing dashboard, in the "system" row, that shows the root filesystem usage percentage over time as a line graph. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

Key panel configuration choices:

* **Data source:** Prometheus (where the metric data comes from)
* **Query:** The PromQL query constructed above
* **Legend:** Uses the `app` label from the metric, which produces a readable name like `web01-system` with the mount point
* **Title:** "Root File System Usage in Percentage"
* **Transparent background:** A visual preference for cleaner dashboards
* **Unit:** Percentage (0-100), which sets the Y-axis to show percentage values [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

## 1.4 Thresholds on Panels — Visual Warning Lines

A **threshold** on a panel is a visual indicator — a horizontal line (or filled region) drawn at a specific value on the graph. It doesn't trigger any action; it's purely visual. It helps anyone looking at the dashboard immediately see whether the metric is in a normal or abnormal range. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

The instructor configures a threshold at **65%** on the panel. Configuration options include:

* **Threshold mode:** "Absolute" (the threshold is a fixed value like 65) vs. "Percentage" (the threshold is a percentage of the Y-axis range). The instructor initially selects "Percentage" but switches to "Absolute" because the metric itself is already a percentage value — using "Percentage" mode would interpret 65 as 65% of the Y-axis range (which is 0-100), not as the literal value 65.
* **Display style:** Line only, filled region, or filled region with lines. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Important distinction:** The threshold on the panel is **visual only**. It does NOT trigger alerts. Alerts are configured separately through alert rules. The panel threshold and the alert rule threshold should match, but they are configured independently.

***

## 1.5 Alert Rules — The Automated Detection Mechanism

An **alert rule** is the core alerting component. It defines: what query to evaluate, what condition constitutes a breach, how often to evaluate, and how long to wait before firing. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Creating an alert rule — two entry points:**

1. From the panel itself: click the "Alert" tab on the panel → "New alert rule." The query is pre-populated from the panel.
2. From the Grafana sidebar: go to "Alert rules" → create manually. You must write the query yourself.

The instructor uses the first approach (from the panel), which automatically carries over the Prometheus data source and query. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Alert rule configuration:**

**Name:** `Root Disk Usage Alert` — a descriptive name for identification.

**Condition:** `when query is above 65` — this means: if the query result exceeds 65 (which represents 65% disk usage), the alert condition is met. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Evaluation group and interval:** Alert rules are organized into **evaluation groups**. Each group defines how frequently Grafana evaluates the rules within it. The instructor creates a group called `high frequency check` with an evaluation interval of **1 minute** — meaning Grafana runs the query every 60 seconds and checks if the condition is breached. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

Once created, an evaluation group can be reused for other rules that need the same check frequency. You can create multiple groups with different intervals (e.g., `high frequency check` at 1 minute, `low frequency check` at 5 minutes) and assign rules to the appropriate group based on how urgently you need to detect breaches.

**Pending period:** By default, there is a **1-minute pending period** before an alert transitions from "pending" to "firing." This means the condition must be continuously breached for at least 1 minute before a notification is sent. This prevents **flapping** — short transient spikes that breach the threshold momentarily but don't represent a real problem. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

🔍 **Deep Dive:**
The alert lifecycle has three states: **Normal** (metric is below threshold), **Pending** (metric breached threshold but pending period hasn't elapsed), and **Firing** (metric has been above threshold for longer than the pending period — notifications are sent). When the metric drops back below the threshold, the alert transitions to **Resolved**, and a resolution notification can be sent (as demonstrated at the end of the lecture).

***

## 1.6 Labels on Alert Rules — The Routing Mechanism

Alert rules can have **labels** — key-value pairs that you attach to an alert. Labels serve a critical purpose: they are used by **notification policies** to route alerts to the correct contact point. Without labels, you cannot create targeted notification policies. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

The instructor adds a label to the alert rule: `alertname = root disk alert`. This label will be used in the notification policy to match this specific alert and route it to the Slack contact point. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

## 1.7 Notification Policies — Routing Alerts to Contact Points

A **notification policy** defines the rules for how alerts are routed to contact points (Slack, email, PagerDuty, etc.) and the timing of notifications. Grafana has a **default policy** that catches all alerts, and you can create **child policies** that match specific alerts based on labels and override the default routing. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

The instructor creates a child policy:

* **Label matcher:** `alertname = root disk alert` — this policy applies only to alerts that have this label
* **Contact point:** Slack (the integration configured in the previous lecture)

The child policy inherits timing from the default policy but overrides the contact point. This is a hierarchical routing system: the default policy is the catch-all, and child policies provide specific routing for specific alerts. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

## 1.8 Notification Timing — Three Key Parameters

The **default policy** has timing options that control notification behavior: [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Group interval:** The wait time before sending a notification about **changes** to an already-sent alert. If an alert fires and a notification is sent, and then the alert state changes (e.g., more instances are affected, or the alert resolves), Grafana waits this long before sending an update. Default is typically several minutes.

**Repeat interval:** The wait time before **re-sending** a notification for an alert that is still in the firing state and hasn't changed. Default is **4 hours**. This prevents notification spam — if an alert fires and stays firing, you get a notification, then another one 4 hours later, then another 4 hours after that.

**Pending period (from the alert rule):** The wait time between the metric breaching the threshold and the alert actually firing. This is configured on the alert rule itself, not in the notification policy.

The instructor changes the timing to very short intervals (1-2 minutes) **for testing purposes only**, and explicitly notes these values should not be used in production: "should not be this low\... but we are just testing it." [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

⚠️ **Expert Note:**
Setting repeat intervals too low in production creates alert fatigue — the team receives so many notifications that they start ignoring them, which defeats the purpose of monitoring. The default 4-hour repeat interval exists for good reason. In production, tune these values based on the severity of the alert: critical alerts might warrant shorter repeat intervals (30 minutes), while warning-level alerts can use the default or longer.

***

## 1.9 The Resolved Notification — Closing the Loop

When the metric drops back below the threshold (after the instructor deletes the large file), the alert transitions from **Firing** to **Resolved**. Grafana sends a **resolved notification** to Slack, confirming that the condition is no longer breached. This closes the feedback loop: you know when something breaks AND when it's fixed. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

## 1.10 Testing Alerts — Artificially Triggering a Threshold Breach

The instructor uses a deliberate technique to test the alert: creating a large file on the monitored server to artificially increase disk usage above the threshold. This is a common practice in monitoring setup — you need to verify that the entire alert chain works (query → threshold → evaluation → notification) before relying on it in production. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

The instructor is careful about this: the server only has 8GB of disk, and filling it completely would crash the system. He creates a 1.5GB file (using `fallocate`) to push usage from 47% to 70% — above the 65% threshold but not dangerously close to 100%.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating a **complete alerting pipeline**: a Prometheus query that calculates root disk usage percentage → a Grafana panel that visualizes it with a threshold line → an alert rule that fires when usage exceeds 65% → a notification policy that routes the alert to Slack. We then test the entire chain by artificially filling the disk, receiving the Slack notification, clearing the disk, and receiving the resolved notification. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

## Step 1: Test the Query in Prometheus

Open the **Prometheus UI** in your browser.

**Build the query incrementally:**

First, test the raw available bytes metric with the root mountpoint filter:

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

This returns the raw available bytes for the root partition.

**Add the division to get the available fraction:**

```promql
node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}
```

This returns a decimal fraction (e.g., 0.53 for 53% available). [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Multiply by 100 for percentage:**

```promql
node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} * 100
```

This shows available percentage. But we want **used** percentage.

**Invert to get used percentage:**

```promql
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100
```

**Expected result:** Around 47% used (depending on your server's actual disk usage). [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Verification:** The result should be a reasonable percentage that matches what `df -h` shows on the target server.

***

## Step 2: Create the Grafana Panel

In Grafana, open your existing dashboard. Navigate to the **system row**.

Click **Add visualization** (or "Add panel").

**Configure the panel:**

1. **Data source:** Select **Prometheus**
2. **Query:** Paste the full PromQL query from Step 1
3. Click **Run query** to verify the graph appears
4. **Legend:** Change to use the `app` label — this produces a readable name like `web01-system` with the mountpoint
5. **Panel title:** `Root File System Usage in Percentage`
6. **Transparent background:** Enable
7. **Standard options → Unit:** Select **Percentage (0-100)** — this sets the Y-axis to show 0-100%

Click **Save** (save the dashboard). [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

## Step 3: Create the Alert Rule

**From the panel:** Click on the panel → go to the **Alert** tab → click **New alert rule**. The query is automatically populated from the panel.

Alternatively, go to **Alerting → Alert rules** in the sidebar and create manually (you'll need to write the query yourself). [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Configure the alert rule:**

1. **Name:** `Root Disk Usage Alert`
2. **Data source:** Verify **Prometheus** is selected
3. **Query:** Should be pre-populated. Verify it matches the PromQL query
4. **Condition:** Scroll to the conditions section. Set: `when query is above 65` [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Create an evaluation group:**

5. Scroll to **Evaluation period**. Click **New evaluation group**
6. **Group name:** `high frequency check`
7. **Evaluation interval:** `1m` (every 1 minute)
8. Click **Create** [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)
9. The pending period defaults to **1 minute** — the alert will wait 1 minute after the threshold is breached before firing

**Add a label (needed for notification routing):**

10. Scroll to **Labels** section. Click **Add label**
11. **Label key:** `alertname`
12. **Label value:** `root disk alert`

**Configure notification:**

13. Scroll to **Configure notification**. Your Slack contact point should appear (configured in a previous lecture)
14. Optionally customize the **summary** and **description** fields for the Slack message. If left blank, the default message is sent. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

Click **Save**.

***

## Step 4: Add the Threshold Visualization to the Panel

Go back to **Dashboards** → select your dashboard → find the root filesystem panel → click **Edit**.

In the right-hand panel options, scroll down to find **Thresholds**:

1. Set threshold value: **65**
2. **Threshold mode:** Select **Absolute** (not "Percentage" — since the metric itself is already a percentage value, you want the threshold at the absolute value of 65)
3. **Show threshold:** Choose display style — line, filled region, or both [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

Click **Save** (save the dashboard).

**Why "Absolute" not "Percentage":** If you select "Percentage" mode, Grafana interprets 65 as 65% of the Y-axis range (0-100), which would place the line at 65 — coincidentally correct here. But the instructor initially had the wrong mode selected and the line didn't display properly because the graph's visible range was narrower than 0-100. "Absolute" is the correct choice when your threshold is a literal metric value.

***

## Step 5: Create the Notification Policy

Go to **Alerting → Notification policies** in the Grafana sidebar.

Click **New child policy** (this creates a child of the default policy): [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

1. **Label matcher:** `alertname = root disk alert` (must exactly match the label added to the alert rule in Step 3)
2. **Contact point:** Select **Slack** (your configured Slack integration)
3. Click **Save policy**

**Connection to the flow:** This policy tells Grafana: "When an alert fires that has the label `alertname = root disk alert`, send the notification to the Slack contact point." [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Adjust timing for testing (optional — revert after testing):**

Go to the **default policy** → Edit → **Timing options**:

* **Group interval:** Change to `1m` (for testing — default is higher)
* **Repeat interval:** Change to `2m` (for testing — default is 4 hours)
* Click **Update policy** [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

⚠️ **These timing values are for testing only.** In production, the defaults (or higher values) are appropriate. Setting repeat interval to 2 minutes in production would flood your Slack channel with repeated alerts.

***

## Step 6: Test the Alert — Artificially Fill the Disk

SSH into the **web server** being monitored:

```bash
ssh -i <key> <user>@<web-server-public-ip>
```

Make sure security group allows port 22 from your IP.

Switch to root:

```bash
sudo -i
```

Check current disk usage:

```bash
df -h
```

**Expected:** Around 47% used on the root partition (`/`), with approximately 3.6GB available. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Create a large file to push usage above 65%:**

```bash
fallocate -l 1.5G /tmp/largefile
```

* `fallocate` — creates a file of a specified size without actually writing data (fast)
* `-l 1.5G` — size of 1.5 gigabytes
* `/tmp/largefile` — path for the temporary file

**Verify disk usage increased:**

```bash
df -h
```

**Expected:** Around 70% used — above the 65% threshold. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

⚠️ **Be careful:** The instructor warns explicitly: "I just don't want to fill this disk because it's just 8GB of size and root partition system will hang totally. So being very careful with this." Don't create files larger than necessary. If the disk fills to 100%, the system becomes unresponsive.

**What happens now:** Prometheus scrapes the metric → the query result jumps to \~70% → Grafana evaluates the alert rule (every 1 minute) → detects the value is above 65 → alert enters "Pending" state → after 1 minute pending period → alert enters "Firing" state → notification is sent to Slack. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

***

## Step 7: Verify the Alert in Grafana and Slack

**In Grafana:**

* Go to **Alerting → Alert rules**. Your rule should show status **Firing**.
* Go to the dashboard panel. The graph should show the metric line crossing above the threshold line.

**In Slack:**

* Log into your Slack workspace (the instructor uses `titan-monitoring`)
* Navigate to the alerts channel
* You should see the alert notification from Grafana [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**If you set repeat interval to 2 minutes:** You'll see additional notifications every 2 minutes as long as the alert remains firing.

***

## Step 8: Resolve the Alert — Delete the File

Back on the web server SSH session:

```bash
rm /tmp/largefile
```

If your SSH session hung (the instructor's did — likely due to disk pressure from Grafana writing to the same disk), log out and log back in, then delete the file. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Wait a few minutes** for Prometheus to scrape the updated metric and for Grafana to evaluate the alert rule.

**Verify in Grafana:** The graph should show the metric dropping back below 65%. The alert should transition from **Firing** to **Resolved**.

**Verify in Slack:** A **resolved notification** should appear, confirming the alert condition is no longer active. [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

**Save the dashboard** before leaving the page.

***

## Step 9: Explore and Experiment

The instructor encourages spending time experimenting: [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)

* Create more panels using additional queries (referenced in the lecture resources)
* Create more alert rules for different metrics
* Explore different panel visualization types and threshold display options
* Use ChatGPT to learn more about specific Grafana settings
* Once comfortable, proceed to the next lecture on Log Aggregation

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Full Alerting Pipeline

```
Prometheus (collects metrics)
  → PromQL query (transforms raw metric → meaningful percentage)
    → Grafana Panel (visualizes with threshold line)
      → Alert Rule (evaluates condition every N minutes)
        → Label (routes to correct notification policy)
          → Notification Policy (matches label → contact point)
            → Slack (receives notification)
              → [Resolved notification when metric drops below threshold]
```

## PromQL Query Construction — Disk Usage Pattern

```
RAW:      node_filesystem_avail_bytes{mountpoint="/"}
FRACTION: avail / total
PERCENT:  fraction * 100
INVERT:   (1 - fraction) * 100 = USED percentage

Final: (1 - avail_bytes{mountpoint="/"} / size_bytes{mountpoint="/"}) * 100

Pattern: (1 - available/total) * 100
  → works for: disk, memory, any resource utilization
```

## Alert Rule Configuration

```
Name:        Root Disk Usage Alert
Data source: Prometheus
Query:       (auto from panel or manual)
Condition:   when query is ABOVE 65
Eval group:  high frequency check (1m interval)
Pending:     1m (wait before firing)
Label:       alertname = root disk alert
```

## Alert State Machine

```
NORMAL → metric below threshold
  ↓ (metric breaches threshold)
PENDING → threshold breached, waiting pending period (1m)
  ↓ (pending period elapsed, still breached)
FIRING → notification sent to Slack
  ↓ (metric drops below threshold)
RESOLVED → resolved notification sent to Slack
  ↓
NORMAL
```

## Notification Policy Hierarchy

```
DEFAULT POLICY (catches all alerts)
  ├─ Timing: group interval, repeat interval (4h default)
  └─ CHILD POLICY (matches specific labels)
       Label: alertname = root disk alert
       Contact point: Slack
       Inherits timing from default unless overridden
```

## Notification Timing Parameters

```
Pending period:  time between breach and firing (alert rule level)
Group interval:  time before sending change notifications (policy level)
Repeat interval: time before re-sending same firing alert (policy level, default 4h)

TESTING: 1-2 minutes (for verification)
PRODUCTION: default or higher (prevent alert fatigue)
```

## Grafana Panel Threshold Config

```
Threshold value: 65
Mode: ABSOLUTE (not Percentage)
  → Absolute = literal metric value (65% disk usage)
  → Percentage = % of Y-axis range (wrong for this use case)
Display: line / filled region / both
```

## Testing Alert — Disk Fill Technique

```
CHECK:  df -h                          → current usage
CREATE: fallocate -l 1.5G /tmp/largefile → push above threshold
VERIFY: df -h                          → should show ~70%
WAIT:   ~2 minutes (eval interval + pending period)
CHECK:  Grafana alert rules → Firing
CHECK:  Slack → notification received
DELETE: rm /tmp/largefile              → resolve alert
WAIT:   ~2 minutes
CHECK:  Slack → resolved notification received

⚠️ Don't fill disk to 100% → system hangs (only 8GB total)
```

## Label → Policy Routing

```
Alert Rule: label "alertname = root disk alert"
                     ↓ (must match exactly)
Notification Policy: label matcher "alertname = root disk alert"
                     → routes to Slack contact point

No label → no targeted routing → falls to default policy
```

## Two Ways to Create Alert Rules

```
FROM PANEL: panel → Alert tab → New alert rule
  → query auto-populated from panel ✓
  → faster, less error-prone

FROM SIDEBAR: Alerting → Alert rules → New
  → must write query manually
  → useful when no panel exists yet
```

## Reusable Engineering Patterns

**1. Derived Metric → Threshold → Alert → Notification**

```
Raw metric alone = not actionable
Derived metric (ratio, percentage) = meaningful
Threshold on derived metric = defines "problem"
Alert on threshold = automated detection
Notification from alert = human awareness

Pattern: raw data → transform → boundary → automation → communication
Same chain in: CloudWatch Alarms, Datadog Monitors, PagerDuty
```

**2. Evaluation Groups = Reusable Check Frequencies**

```
Create once: "high frequency check" (1m)
Assign to: multiple alert rules that need same frequency

Pattern: define policy once → apply to many instances
Same as: security groups (define rules once, attach to many instances)
```

**3. Label-Based Routing**

```
Alerts carry labels (metadata)
Policies match labels → route to contact points

Pattern: metadata on events → routing rules match metadata → directed action
Same as: email filters, message queue topic routing, K8s label selectors
```

**4. Test with Synthetic Load, Verify Full Chain**

```
Don't wait for real incidents to test monitoring
Artificially trigger conditions → verify entire pipeline works
Delete synthetic load → verify resolved notification works

Pattern: end-to-end testing of observability pipelines
         before relying on them in production
```

***

*This completes the full reconstruction. Theory explains the PromQL query construction, alert lifecycle, and notification routing model. Practical walks through every configuration step and the synthetic test procedure. The Compression Map enables instant recall of the full alerting pipeline, the state machine, and the label-based routing pattern.* [\[261-creati...thresholds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/261-creating-alerts-and-thresholds.txt)
