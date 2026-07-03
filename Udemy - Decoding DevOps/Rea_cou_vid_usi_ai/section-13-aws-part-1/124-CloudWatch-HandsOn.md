# 📊 AWS CloudWatch Hands-On — Monitoring, Stress Testing, Alarms, and Notifications

**Source:** CloudWatch Hands-On Session (Caption File) + STRESS Installation Guide [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt), [\[124.STRESS...nLinux2023 \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B7051411C-CFEC-4942-836D-8D9DDEB191B6%7D&file=124.STRESS_Install_and_Usage_AmazonLinux2023.docx&action=default&mobileredirect=true)

This is a **complete hands-on session** covering the AWS CloudWatch monitoring service through a real exercise: launching an EC2 instance, understanding the default metrics CloudWatch collects, installing the `stress` tool to generate artificial CPU load, observing the resulting graphs, creating a CloudWatch alarm with an SNS email notification, and triggering that alarm. The instructor builds the entire monitoring → alert → notification pipeline from scratch, and uses a powerful **blood pressure analogy** to explain when high resource usage becomes a real problem. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. What CloudWatch Is — The Monitoring Service

CloudWatch is an **AWS monitoring service** that automatically collects data about your AWS resources and presents it as metrics and graphs. The instructor describes it as an "amazing service" and clarifies that this exercise is "just a very small glimpse of CloudWatch" — it can do much more, including log monitoring (covered in AWS Part 2) and AI-powered operations investigations. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

The core concept: every AWS service you use (EC2, EBS, S3, Application Load Balancer, etc.) has **default metrics** that CloudWatch automatically collects. You don't need to install anything or configure anything for these defaults — CloudWatch begins collecting the moment you launch a resource. Each service has **its own set of metrics** appropriate to what that service does. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 2. Default Metrics on EC2 — What CloudWatch Collects Automatically

For EC2 instances, CloudWatch collects these **default metrics**: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

* **CPU Utilization** — Percentage of allocated compute power being used.
* **Network In (bytes)** — Amount of incoming network data.
* **Network Out (bytes)** — Amount of outgoing network data.
* **Network Packets In** — Number of incoming network packets.
* **Network Packets Out** — Number of outgoing network packets.
* **CPU Credit Usage** — How many CPU credits are being consumed (relevant for burstable instance types like `t2.micro`).
* **CPU Credit Balance** — How many CPU credits remain.

The instructor explicitly shows these as separate graphs in the EC2 **Monitoring tab**. Each graph represents one metric. These are the **out-of-the-box checks** — no setup required. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

Beyond defaults, you can create **custom metrics** — your own defined checks. However, the instructor notes that **"usually organizations prefer using their own monitoring tool for custom metrics"** — meaning in practice, CloudWatch handles infrastructure-level defaults while specialized tools (Datadog, Prometheus, Grafana) handle application-level custom metrics. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 3. Default vs Detailed Monitoring — Collection Frequency

CloudWatch collects EC2 data at two frequencies: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Default monitoring (free):** Collects data **every 5 minutes**. This is what every EC2 instance gets automatically at no extra cost.

**Detailed monitoring (paid):** Collects data **every 1 minute**. The instructor enables this in the video but explicitly states: **"You don't need to enable that. You just need to wait a little longer."** If you keep default monitoring, the graphs take longer to populate but the exercise works the same way — you just need to wait more.

The trade-off is straightforward: more frequent data = faster graphs and more granular alerting, but it costs money. For learning, default monitoring is sufficient. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 4. Per-Service Metrics — CloudWatch's Universal Pattern

The instructor makes an important architectural observation: **"whichever service you use, you have different kinds of metrics for every service."** When you navigate to CloudWatch and select a metric, you see categories for every AWS service you've used in that account and region — EC2, EBS, S3, ALB, etc. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

This reveals CloudWatch's design pattern: it is a **universal metrics collector** that adapts its data collection to whatever services are active. It's not an EC2-specific tool — it's the **central nervous system** of AWS monitoring. The metrics it collects for EBS are different from EC2, which are different from S3, but they all flow into the same CloudWatch dashboard, graphing, and alarming system. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 5. The Blood Pressure Analogy — When High Load Becomes a Problem

The instructor provides a critical conceptual insight using a **blood pressure analogy** that defines when monitoring should trigger action: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**"It's not a big deal that happens in real servers"** — CPU utilization spiking up and coming back down is normal. The instructor compares it to blood pressure: you climb stairs or exercise, your blood pressure goes up. When you rest, it comes back down. **That's not a problem.**

**"The problem is when it goes up and stays there for a longer time."** If CPU utilization spikes to 90% and stays at 90% for five minutes, ten minutes, or longer — that indicates a real problem. The service might crash. The instance might become unresponsive.

This is the fundamental principle behind alarm design: you don't alert on **momentary spikes** — you alert on **sustained high values**. The alarm threshold has two dimensions: the **value** (how high) and the **duration** (how long it stays there). Both must be met before the alarm triggers. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

<details>
<summary>🔍 Deep Dive</summary>

This is why CloudWatch alarms have a "period" setting. When you set "greater than or equal to 60% for a period of 1 minute," you're defining both dimensions. The alarm doesn't fire the instant CPU hits 60% — it fires when the average over the period exceeds the threshold. In production, you'd typically set 5-minute periods to avoid alerting on transient spikes. The 1-minute period used in this lab is for faster demonstration, not for production practice.

</details>

***

## 6. The Three CloudWatch Concepts — Metric, Alarm, Notification

The instructor explicitly names these as the core concepts the exercise teaches: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Metric (Check):** A measurable value that CloudWatch collects over time — CPU utilization, network bytes, disk I/O, etc. Metrics are the raw data. They become graphs.

**Alarm:** A rule applied to a metric — "if CPU utilization is ≥ 60% for 1 minute, trigger." An alarm has three states:

* **OK** — the metric is within normal bounds.
* **ALARM** — the metric has breached the threshold for the specified duration.
* **INSUFFICIENT DATA** — not enough data has been collected yet to evaluate (common when alarms are first created).

**Notification:** The action taken when an alarm enters the ALARM state — typically an email sent via **SNS (Simple Notification Service)**. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 7. Alarm Actions — Beyond Notification

The instructor reveals that CloudWatch alarms can do more than just send emails. When an alarm triggers, you can configure: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

* **SNS Notification** — send an email (or SMS, or trigger other systems).
* **EC2 Actions** — **stop, terminate, or reboot** the instance automatically. The instructor explicitly says: **"I have personally used this."** If the only fix for a known bug is a reboot, CloudWatch can automate it.
* **Lambda Function** — run a Python script (or any Lambda-supported language) that performs custom actions.
* **Systems Manager Action** — trigger operational automation through AWS Systems Manager.

The instructor emphasizes: **"There are many other actions, not just sending notification. You can take some action also."** This positions CloudWatch alarms not just as a notification system, but as an **automated response system** — the alarm detects the problem, and the action fixes it (or escalates it). [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

<details>
<summary>⚠️ Expert Note</summary>

The EC2 reboot action is a real production pattern. When an application has a known memory leak that causes it to become unresponsive after days of running, an automated reboot (triggered by a memory or CPU alarm) provides a stopgap while the engineering team works on a permanent fix. This is not ideal — it's operational pragmatism. Lambda actions are more powerful: they can trigger auto-scaling, invoke remediation scripts, create JIRA tickets, or send Slack messages. In mature DevOps organizations, CloudWatch alarms feed into incident management pipelines.

</details>

***

## 8. Alarm Naming and Threshold Conventions

The instructor introduces a naming and threshold convention used in real organizations: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

* **Warning** (e.g., CPU ≥ 60%) — something needs attention; investigate and take preventive action.
* **Critical** (e.g., CPU ≥ 80%) — immediate action required; service is in danger.
* **OK** (e.g., CPU < 50%) — everything is normal.

The alarm name should be descriptive: the instructor names his alarm **"Warning – High CPU Utilization"** and includes the server name. This naming makes the notification email immediately understandable without needing to look up instance IDs. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

The instructor explicitly states that deciding the right threshold value **"depends on what service you're running... comes with experience... comes with time that you spend with your application."** There is no universal "correct" threshold — it's application-specific and learned through operational experience. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 9. The DevOps vs Monitoring Team Distinction

The instructor makes an important organizational observation: **"Your job as a DevOps is not to set monitoring."** DevOps engineers can set up the monitoring infrastructure and automate the process, but **"there should be a 24/7 monitoring team who are working, supporting these activities for production."** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

This clarifies the role boundary: DevOps **builds and automates** the monitoring pipeline. The monitoring/operations team **operates** it 24/7, responds to alerts, and escalates issues. The DevOps engineer makes it possible; the monitoring team makes it operational.

***

## 10. The `stress` Tool — Artificial Load Generation

The `stress` tool is a Linux utility that **imposes compute stress on the system** — it can generate CPU load, memory pressure, disk I/O, and other forms of stress. The instructor uses it to artificially spike CPU utilization so the CloudWatch graphs show meaningful data and the alarm triggers. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

When you run `stress` without arguments, it tells you: **"stress imposes certain types of compute stress on your system."** The instructor clarifies its purpose: **"This is used to test your operating system performance. We are using it so we can see the graph going up and down."** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

The key flag is `-c` (or `--cpu`), which specifies the **number of CPU worker processes** to spawn. Each worker continuously runs the `sqrt()` (square root) function — a CPU-intensive mathematical operation that keeps the processor busy. The `-t` flag specifies a **timeout** in seconds — after which `stress` stops automatically. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 11. SNS — Simple Notification Service (Brief)

When creating an alarm, notifications are sent through **SNS topics**. An SNS topic is a messaging channel — you subscribe email addresses (or other endpoints) to the topic. When the alarm triggers, CloudWatch publishes a message to the topic, and SNS delivers it to all subscribers. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

The instructor creates a new SNS topic during alarm creation and notes: **"If you have set the billing alarm in the prerequisite lecture, you should see your SNS topic over here."** After creating a new topic, you must **confirm the subscription** by clicking the link in the confirmation email. Without confirmation, no notifications are delivered. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## 12. Free Tier Awareness

The instructor provides explicit free tier guidance: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

* **10 CloudWatch alarms** are free.
* **Default 5-minute monitoring** is free; detailed 1-minute monitoring is paid.
* The entire exercise is free if you stay within these limits.
* After the exercise, **clean up**: delete the instance, and optionally delete alarms (alarms persist even after the instance is deleted — they just stop receiving data).

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are building a **complete monitoring and alerting pipeline**: EC2 instance → stress the CPU → CloudWatch collects metrics → graphs show load → CloudWatch alarm triggers when CPU stays high → SNS sends email notification. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Why it matters:** This is the fundamental pattern for all production monitoring — detect, measure, alert, act. Every real system you manage will have some version of this pipeline.

**Final outcome:** An email arriving in your inbox saying "ALARM — Warning: High CPU Utilization" with a link to the CloudWatch graph.

***

## Step 1: Launch EC2 Instance from Launch Template

**What we are doing:** Quickly launching an instance using a pre-configured launch template (created in previous lectures). [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

1. Go to **Launch Templates** in EC2 console.
2. Select the launch template → **Actions** → **Launch instance from template**.
3. Change the instance **Name** to something unique (e.g., `web12`) — important because terminated instances still appear in the list.
4. Click **Launch Instance**.

**Operational reasoning:** The launch template has AMI, instance type, key pair, and security group pre-configured. Changing only the name avoids confusion with previous instances.

**Connection to flow:** Instance launching → CloudWatch begins collecting default metrics immediately.

***

## Step 2: View the Monitoring Tab and Understand Default Metrics

1. Go to **Instances** → select the instance → click the **Monitoring** tab. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)
2. You'll see empty graphs initially — CloudWatch needs time to collect data.

**Default metrics visible:** CPU Utilization, Network In/Out (bytes), Network Packets In/Out, CPU Credit Usage/Balance.

**Wait time:** At default 5-minute monitoring, wait **15-20 minutes** for graphs to start populating. The instructor recommends taking a break.

**Connection to flow:** Graphs are collecting baseline data. Next, we install the stress tool.

***

## Step 3: (Optional) Enable Detailed Monitoring

**Only if you want 1-minute granularity (costs money):** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

1. In the Monitoring tab → click **Manage Detailed Monitoring**.
2. Check **Enable** → click **Confirm**.

**The instructor's advice:** "You don't need to enable that. You just need to wait a little longer." Default monitoring works fine — just requires patience.

***

## Step 4: SSH into the Instance

**Ensure security group allows SSH:**

1. Go to instance's **Security Group** → **Edit Inbound Rules**.
2. Ensure port **22** is open from **My IP**. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**SSH command:**

```bash
ssh -i <key_path> ec2-user@<public_ip>
```

**Verify OS version:**

```bash
cat /etc/os-release
```

This confirms you're on Amazon Linux (which determines the installation commands). If using Ubuntu, the installation steps differ. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

## Step 5: Install the `stress` Tool

**For Amazon Linux 2023:** [\[124.STRESS...nLinux2023 \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B7051411C-CFEC-4942-836D-8D9DDEB191B6%7D&file=124.STRESS_Install_and_Usage_AmazonLinux2023.docx&action=default&mobileredirect=true)

```bash
sudo dnf install stress -y
```

* `dnf` — Package manager for Amazon Linux 2023 (replaces `yum`).
* `install stress` — Install the stress testing utility.
* `-y` — Auto-confirm.

**For Ubuntu (if applicable):**

```bash
sudo apt update
sudo apt install stress -y
```

**Verify installation:**

```bash
stress
```

Output: `"stress imposes certain types of compute stress on your system"` — confirms installation. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Connection to flow:** Tool installed. Now we generate CPU load.

***

## Step 6: Understand and Run the `stress` Command

**Basic syntax:** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

```bash
stress -c 4 -t 5
```

* `stress` — The load generation tool.
* `-c 4` (or `--cpu 4`) — Spawn **4 worker processes**, each spinning on the `sqrt()` function. More workers = more CPU load.
* `-t 5` (or `--timeout 5`) — Run for **5 seconds** then stop automatically.

**What happens internally:** 4 processes are spawned, each consuming 100% of one CPU thread. On a `t2.micro` (1 vCPU), even 4 workers will saturate the CPU. The output says: **"stress: info: \[PID] dispatching hogs: 4 cpu..."** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Without `-t`:** Stress runs indefinitely until you press **Ctrl+C**.

**The stress test script** (from the resource document): [\[124.STRESS...nLinux2023 \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B7051411C-CFEC-4942-836D-8D9DDEB191B6%7D&file=124.STRESS_Install_and_Usage_AmazonLinux2023.docx&action=default&mobileredirect=true)

```bash
stress -c 4 -t 60 && sleep 60 \
&& stress -c 4 -t 60 && sleep 60 \
&& stress -c 4 -t 360 && sleep 30 \
&& stress -c 4 -t 460 && sleep 30 \
&& stress -c 4 -t 360 && sleep 60
```

This creates a **stress-then-rest pattern**: stress for 60s → rest 60s → stress 60s → rest 60s → stress 360s → rest 30s → etc. This simulates realistic load patterns (up and down) rather than constant max load.

**Running in the background:** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

```bash
nohup ./stress.sh &
```

* `nohup` — Detaches the process from the terminal session. The process continues even if you close SSH.
* `./stress.sh` — The script to run.
* `&` — Puts the process in the background.

**Verify CPU load with `top`:**

```bash
top
```

Shows real-time CPU utilization going up and down as the stress script cycles. The instructor observes: **"CPU utilization is 23.2% and now it's down and it's increasing... 40, 90 CPU utilization and the load average you see going up."** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Connection to flow:** CPU is being stressed. CloudWatch is collecting the data. Graphs will show the spikes. Let it run for 5-10 minutes.

***

## Step 7: Observe CloudWatch Graphs

After waiting, return to the EC2 Monitoring tab or CloudWatch console: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

1. **Refresh** the page.
2. The CPU Utilization graph should show spikes going up and coming down.
3. You can change the time window: view per 5 minutes, per 1 minute, custom (e.g., every 10 minutes).

**What to observe:** The graph shows the **up-and-down pattern** — stress spikes followed by rest periods. The instructor notes: **"In real systems or servers the graphs usually will be something like this. The load going up and down."** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Connection to flow:** Graphs confirmed working. Now set up the alarm.

***

## Step 8: Create a CloudWatch Alarm

**Navigate:** CloudWatch service → **All Alarms** → **Create Alarm**. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

### 8a: Select the Metric

1. Click **Select Metric**.
2. Choose **EC2** (you'll see other services too — EBS, S3, ALB — whatever you've used).
3. Select **Per-Instance Metrics**.
4. **Search by Instance ID** — copy your instance ID from the EC2 console and paste it.
5. Find **CPU Utilization** → select it.
6. Click **Select Metric**. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

### 8b: Configure Conditions

1. **Period:** Set to **1 minute** (or keep 5 minutes for free tier).
2. **Condition:** **Greater than or equal to** → enter **60** (meaning 60% CPU utilization).
3. Click **Next**. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Operational reasoning:** The threshold value (60%) is chosen as a **warning level**. The instructor explicitly says this is a "random number" for the exercise — in production, the value depends on your application's behavior and crash thresholds. **"Comes with experience. Comes with time that you spend with your application."** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

### 8c: Configure Notification

1. **Alarm state trigger:** In Alarm.
2. **SNS Topic:** Select existing topic OR **Create new topic**.
   * Give the topic a name.
   * Enter your email address.
   * Click **Create Topic**.
3. **If new topic:** Check your email and **click Confirm Subscription** in the confirmation email. Without this, no notifications will be delivered. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

### 8d: (Optional) Configure EC2 Actions

The instructor shows but does **not** keep these for this exercise:

* **Stop instance** — automatically stop the instance on alarm.
* **Terminate instance** — automatically terminate on alarm.
* **Reboot instance** — automatically reboot on alarm.

The instructor notes: **"I have personally used this"** — it's a real production pattern for automated remediation. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

### 8e: Name the Alarm

* **Name:** `Warning – High CPU Utilization` (or similar descriptive name including the server name).
* **Description:** Optional.
* Click **Next** → **Create Alarm**. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Initial state:** The alarm shows **"Insufficient Data"** — it hasn't collected enough data points yet. After a few minutes, it transitions to **OK** or **ALARM** based on current CPU load.

**Connection to flow:** Alarm created. Now we need the CPU to breach the threshold.

***

## Step 9: Increase Stress to Trigger the Alarm

If the current stress level isn't breaching 60%, increase the load: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Kill the existing stress process:**

```bash
ps -ef | grep stress.sh
kill <PID>
```

* `ps -ef` — List all processes.
* `| grep stress.sh` — Filter for the stress script.
* `kill <PID>` — Terminate the process by its ID.

**Modify the script** to use more CPU workers (e.g., change `-c 4` to `-c 35`) and longer timeouts, then re-run: [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

```bash
nohup ./stress.sh &
```

**Verify with `top`** — CPU utilization should now spike higher and sustain longer.

**Wait** for CloudWatch to collect data points above the threshold for the required period. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Connection to flow:** The alarm will transition from OK → ALARM once the sustained threshold is breached.

***

## Step 10: Verify Alarm Trigger and Notification

**In CloudWatch console:** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

1. The alarm state changes to **"In alarm"** (red).
2. The graph shows CPU utilization crossing the threshold line and staying above it.

**In your email inbox:**

An email arrives with:

* **Subject:** Contains the alarm name and state change.
* **Body:** **"Notification state change from OK to ALARM"** with the alarm name ("Warning – High CPU Utilization on web server").
* **Link:** Direct link to the CloudWatch graph.

The instructor confirms: **"See that. Notification state change from okay to alarm."** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

**Connection to flow:** The complete pipeline is verified: metric collection → threshold breach → alarm state change → SNS notification → email delivery.

***

## Step 11: Clean Up

**After the exercise:** [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

1. **Terminate the EC2 instance** — stop paying for compute.
2. **Delete the alarm** (optional — alarms persist even after instance deletion, just stop receiving data). Up to 10 alarms are free.
3. If detailed monitoring was enabled, consider that it incurs charges until the instance is terminated.

**The instructor's extra exercise suggestion:** Create a **reverse alarm** — if CPU drops below 50% and stays there for 5 minutes, send an "OK state" notification. This practices the opposite direction of alerting. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   AWS CloudWatch Hands-On — Monitoring, Alarms, Notifications
CONTEXT: AWS EC2 → monitoring layer → detect, alert, act
PURPOSE: Build the complete metric → alarm → notification pipeline
```

***

## CloudWatch Core Concepts (Triad)

```
METRIC       = measurable value collected over time (CPU%, network bytes, etc.)
ALARM        = rule applied to a metric (if X ≥ threshold for Y duration → trigger)
NOTIFICATION = action taken when alarm triggers (email via SNS, EC2 action, Lambda)
```

***

## Alarm States

```
INSUFFICIENT DATA → not enough data yet (just created)
         ↓
OK                → metric within normal bounds
         ↓↑
ALARM             → metric breached threshold for specified duration
```

***

## The Blood Pressure Mental Model

```
Spike up then down = NORMAL (like exercise → rest)
Spike up and STAY HIGH = PROBLEM (sustained load → potential crash)

ALARM DESIGN: threshold VALUE + sustained DURATION → both must be met
              e.g., CPU ≥ 60% for ≥ 1 minute
```

***

## Default EC2 Metrics (Auto-Collected)

```
CPU Utilization
Network In (bytes)        Network Out (bytes)
Network Packets In        Network Packets Out
CPU Credit Usage          CPU Credit Balance
```

***

## Monitoring Frequency

```
DEFAULT (free):   every 5 minutes
DETAILED (paid):  every 1 minute
```

***

## Per-Service Metrics Pattern

```
CloudWatch = UNIVERSAL collector
  ├── EC2  → CPU, network, credits
  ├── EBS  → disk I/O metrics
  ├── S3   → bucket-level metrics
  ├── ALB  → request count, latency
  └── [any AWS service] → its own default metrics

Pattern: use a service → CloudWatch auto-collects its metrics
```

***

## Complete Pipeline Flow

```
EC2 Instance (running workload)
    ↓ CloudWatch auto-collects metrics every 5min/1min
CLOUDWATCH METRICS (graphs form)
    ↓ alarm evaluates: metric ≥ threshold for ≥ period?
ALARM STATE CHANGE (OK → ALARM)
    ↓ triggers configured action
SNS TOPIC → EMAIL NOTIFICATION
    └── or: EC2 Action (stop/reboot/terminate)
    └── or: Lambda function (custom automation)
    └── or: Systems Manager action
```

***

## Alarm Creation Flow

```
1. Select Metric     → EC2 → Per-Instance → search by Instance ID → CPU Utilization
2. Set Conditions    → ≥ 60% for 1 minute (period)
3. Configure Action  → SNS topic (create or select) + email
                       Optional: EC2 action, Lambda
4. Name the Alarm    → "Warning – High CPU Utilization – <server>"
5. Create            → starts in INSUFFICIENT DATA → transitions to OK or ALARM
```

***

## Alarm Actions (Not Just Notification)

```
SNS Notification    → email, SMS, trigger downstream systems
EC2 Actions         → STOP / TERMINATE / REBOOT instance (automated remediation)
Lambda              → custom Python script (create ticket, scale, remediate)
Systems Manager     → operational automation
```

***

## `stress` Tool — Command Reference

```
stress                        → show help (verify installation)
stress -c 4                   → spawn 4 CPU workers (runs forever, Ctrl+C to stop)
stress -c 4 -t 60             → spawn 4 CPU workers for 60 seconds
nohup ./stress.sh &           → run script in background, survives session close
top                           → verify CPU load in real-time
ps -ef | grep stress.sh       → find stress process
kill <PID>                    → stop the stress process
```

***

## `stress` Installation

```
Amazon Linux 2023:  sudo dnf install stress -y
Ubuntu:             sudo apt update && sudo apt install stress -y
```

***

## Threshold Convention (Organizational Pattern)

```
OK        → CPU < 50%    → normal
WARNING   → CPU ≥ 60%    → investigate, take preventive action
CRITICAL  → CPU ≥ 80%    → immediate action, service in danger

Values are APPLICATION-SPECIFIC → learned through operational experience
```

***

## Role Boundary

```
DEVOPS ENGINEER:      builds + automates monitoring pipeline
MONITORING TEAM (24/7): operates, responds to alerts, escalates
DevOps makes it possible → Monitoring team makes it operational
```

***

## Free Tier Boundaries

```
10 CloudWatch alarms     → FREE
Default 5-min monitoring → FREE
Detailed 1-min monitoring→ PAID
Alarms persist after instance deletion → clean up manually
```

***

## SNS Topic Flow

```
Create topic → add email subscriber → MUST confirm subscription email
                                        (without confirm → no notifications)
Topic reusable → same topic for billing alarm + CloudWatch alarms
```

***

## Reusable Engineering Patterns

```
1. DETECT-MEASURE-ALERT-ACT       → Universal monitoring pipeline
                                     metric → threshold → alarm → action
                                     (same in Prometheus, Nagios, Datadog, etc.)

2. SUSTAINED BREACH, NOT SPIKE    → Alert on duration, not instant
                                     Blood pressure model: spike = OK, sustained = problem

3. UNIVERSAL ADAPTER PATTERN      → CloudWatch adapts metrics per service
                                     One monitoring system → many service types → different metrics each

4. AUTOMATED REMEDIATION          → Alarm triggers action (reboot, Lambda, etc.)
                                     Not just notification — actual system response

5. STRESS TESTING FOR VALIDATION  → Generate artificial load → verify monitoring detects it
                                     Test the monitoring before production needs it

6. CONVENTION-BASED NAMING        → Warning/Critical levels + server name in alarm name
                                     Makes notification emails self-explanatory
```

***

## Rapid Recall Triggers

```
"What is CloudWatch?"              → AWS monitoring service, auto-collects metrics per service
"Default EC2 metrics?"             → CPU util, network in/out (bytes+packets), CPU credits
"Default vs detailed monitoring?"  → 5 min (free) vs 1 min (paid)
"What triggers an alarm?"          → Metric ≥ threshold for ≥ period (sustained, not spike)
"Alarm states?"                    → Insufficient Data → OK ↔ ALARM
"What actions can alarm take?"     → SNS notification, EC2 stop/reboot/terminate, Lambda, SSM
"What is stress tool?"             → Generates artificial CPU/memory/disk load for testing
"stress -c 4 -t 60?"              → 4 CPU workers for 60 seconds
"How to run stress in background?" → nohup ./script.sh &
"SNS topic setup?"                 → Create topic + email → MUST confirm subscription email
"Free tier alarms?"                → 10 free alarms, default 5-min monitoring
"Who sets monitoring?"             → DevOps builds it, 24/7 monitoring team operates it
"When is high CPU a problem?"      → When it goes up AND STAYS up (blood pressure analogy)
"Extra exercise?"                  → Reverse alarm: CPU < 50% for 5 min → send OK notification
```

***

This completes the full reconstruction of the CloudWatch Hands-On session — covering theory, the complete hands-on alarm pipeline, and the stress-testing methodology. **Theory** builds the conceptual framework of metrics, alarms, and the blood pressure mental model; **Practical** walks through every click, command, and configuration step; and the **Mental Compression Map** compresses the entire pipeline into fast-recall structures. [\[124. Cloud...h Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/124.%20Cloudwatch%20Hands%20On.txt), [\[124.STRESS...nLinux2023 \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B7051411C-CFEC-4942-836D-8D9DDEB191B6%7D&file=124.STRESS_Install_and_Usage_AmazonLinux2023.docx&action=default&mobileredirect=true)

Ready for the next caption file, or shall I generate an **AnkiDroid CSV** covering this lecture or the entire series? 🚀
