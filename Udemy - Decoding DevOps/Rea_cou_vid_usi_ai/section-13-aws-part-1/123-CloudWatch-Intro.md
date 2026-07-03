# 🎓 Deep Learning Material: AWS CloudWatch Introduction — Monitoring, Metrics, Alarms & Notifications

*Reconstructed from video lecture captions (123. Cloudwatch Introduction.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What AWS CloudWatch Is: From Monitoring Service to Observability Platform

AWS CloudWatch is fundamentally a **monitoring service** — but the instructor immediately clarifies that it has expanded far beyond basic monitoring. It is now also a **logging solution**, an **events system**, and provides additional features like **Log Insights**. However, its **primary identity** remains: a service that monitors the performance of your AWS environment. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

The key phrase the instructor uses is: *"Primarily it's a service that will be monitoring performance of your AWS environment."*  This positions CloudWatch as the built-in observability backbone of AWS — the system that watches everything else. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

***

## 1.2 Metrics: The Core Concept of CloudWatch

**Metrics** are the primary building block of CloudWatch. The instructor states this clearly: *"Metrics is the primary thing in CloudWatch."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

A metric is a **time-series data point** that represents a measurable aspect of an AWS resource's behavior — like CPU utilization of an EC2 instance, or read bandwidth of an EBS volume. In other monitoring tools, these would be called "checks" — the instructor draws this parallel: *"In other monitoring tools, these things are called checks — like for a virtual machine, CPU utilization or disk utilization or network utilization."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

The critical insight about CloudWatch metrics is that they are **automatic**. The instructor emphasizes: *"You really don't need to set up monitoring. Monitoring is anyways set up through CloudWatch. There is a by default monitoring set up."*  This means that the moment you create an AWS resource (an EC2 instance, an EBS volume, an RDS database, etc.), CloudWatch **automatically begins collecting standard metrics** for that resource. You don't install an agent, you don't configure a monitoring tool, you don't register the resource — it happens by default. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

These automatically collected metrics are called **standard metrics**. For EC2 instances, the standard metrics include: [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

* **CPU Utilization**
* **Status Checks**
* **Network In / Network Out**
* **Network Packets In / Network Packets Out**
* **Disk Read / Disk Read Operations**
* **Disk Write / Disk Write Operations**

For EBS volumes, the standard metrics include: [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

* **Read Bandwidth / Write Bandwidth**
* **Read Throughput / Write Throughput**

The instructor generalizes: *"You take any service that you're using in your AWS account, it will have metrics which will be set by CloudWatch."*   This means CloudWatch is not EC2-specific — it monitors every AWS service that generates operational data. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

Beyond standard metrics, you can create **custom metrics** — additional measurements of your choice that go beyond what AWS collects by default. The instructor mentions: *"You can add more metrics of your choice, which are called custom metrics also."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

🔍 **Deep Dive:**
There's a timing nuance the instructor reveals through direct observation. After launching a fresh EC2 instance, he navigates to the monitoring tab and sees: *"Currently there is no data available, it says, because it's going to take some time to collect this data. I have recently just launched this instance, so it's going to take some time to collect the metrics and then you should see the graphs."*  Metrics are not instantaneous — there is a collection interval. Standard monitoring collects at 5-minute intervals (detailed monitoring, which costs extra, collects at 1-minute intervals). This delay means you won't see data for a newly launched resource immediately. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

***

## 1.3 Where Metrics Appear: The Monitoring Tab Pattern

Metrics are not something you only find in the CloudWatch console — they surface **inside each service's own interface** through a **Monitoring tab**. The instructor demonstrates this with EC2: *"There is an EC2 instance and EC2 instance will have a monitoring tab. And these metrics are coming from CloudWatch."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

He then shows the same pattern for EBS volumes: *"If you go to volume section, if you see your volumes, volume will also have monitoring and will be metrics for volumes as well."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

This is a consistent AWS design pattern: the service-specific console (EC2, EBS, RDS, etc.) embeds CloudWatch metrics directly into its interface. The data originates from CloudWatch, but it's presented within the context of the resource you're looking at. You can view metrics either from the resource's Monitoring tab or from the CloudWatch console itself.

***

## 1.4 Events: Real-Time Stream of What's Happening

Beyond metrics, CloudWatch captures **events** — a real-time stream of actions and state changes happening in your AWS environment. The instructor explains: *"AWS events will give you a real-time stream of any events that is happening. For example, you launching an instance or terminating or taking a snapshot or creating a volume. These are events and CloudWatch is going to capture all the events."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

Events represent **actions** (things that happen), while metrics represent **measurements** (things you measure over time). An event is discrete ("instance launched at 3:42 PM"), while a metric is continuous ("CPU was at 45% at 3:42 PM").

The practical value of events is in **setting triggers**. The instructor says: *"What can you do with those events? Well, you can set triggers from those events. Mostly it's used to integrate with Lambda functions."*  This means events can automatically trigger automated responses — for example, when a new instance is launched, a Lambda function could automatically configure it, tag it, or register it with a load balancer. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

The instructor defers detailed coverage of events to a later course section (AWS Part 2). [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

***

## 1.5 Logs: Centralized Log Collection

CloudWatch also serves as a **centralized logging solution**. The instructor explains: *"Almost all the services will have an option to stream the logs."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

However, there's an important distinction for EC2: *"In EC2 you don't have a direct option. You can set it from your operating system. From your operating system, you can set an agent which can stream logs to CloudWatch service."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

This means:

* **Most AWS services** (RDS, Lambda, ELB, etc.) can stream logs to CloudWatch natively — you enable it in the service configuration
* **EC2 instances** require you to install and configure a **CloudWatch agent** on the OS level to push logs to CloudWatch

The instructor defers detailed coverage of logs (and setting metrics on logs) to AWS Part 2, keeping this lecture focused on metrics and alarms. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

***

## 1.6 Alarms: Turning Metrics into Actionable Notifications

Metrics are data. Looking at graphs is passive. **Alarms** make metrics **actionable** by triggering notifications when a metric crosses a threshold. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

The instructor frames the problem clearly: *"If you really want to monitor the activity, you can't be 24/7 looking at the graphs of CloudWatch. But if something goes wrong, if the graph is spiking high, you should get some notifications. So alarms will help set you notifications."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

An alarm is a rule that says: "Watch this metric. If it crosses this threshold, take this action." The action is typically sending a notification through **SNS (Simple Notification Service)** — specifically, an email notification. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

The instructor's concrete example: *"We can see if the CPU utilization is crossing above 60, I should receive an email notification."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

***

## 1.7 The Three-Service Interaction Model

The instructor explicitly identifies the **three services** that work together in the monitoring-to-notification pipeline: [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

1. **EC2** — Generates the metrics (the data source)
2. **CloudWatch** — Collects the metrics and hosts the alarm configuration
3. **SNS** — Delivers the notification (email) when the alarm triggers

The instructor articulates this clearly: *"There are three services in play over here. EC2 instance that is generating the metrics, CloudWatch which is collecting the metrics, CloudWatch is also setting up alarm — or we are setting alarms in the CloudWatch — and then the SNS service."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

This three-component model — **data source → monitoring/evaluation → notification delivery** — is the fundamental pattern for all CloudWatch-based alerting.

🔍 **Deep Dive:**
This is a recurring architectural pattern in AWS: services are designed to work together through integration, not as monolithic tools. CloudWatch doesn't send emails — it delegates that to SNS. SNS doesn't collect metrics — that's CloudWatch's job. EC2 doesn't evaluate its own health — CloudWatch does that. Each service has a single responsibility, and they compose together. This is the same microservice/single-responsibility principle applied at the platform level.

***

## 1.8 Scope of This Lecture vs. Future Coverage

The instructor clearly delineates what this lecture covers and what's deferred: [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**This lecture (current):**

* Metrics (standard metrics, custom metrics concept)
* Alarms on metrics
* SNS email notification integration
* Practical: Set CPU utilization alarm → email notification

**AWS Part 2 (future):**

* Collecting **logs** from EC2 instances (via agent)
* Setting **metrics on logs** (log-based metrics)
* **Events** and triggers (Lambda integration)
* Additional actions based on log-derived metrics

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a **CPU utilization alarm** on an EC2 instance that sends an **email notification via SNS** when CPU usage crosses a defined threshold (60%). This involves three AWS services working together: EC2 (data source), CloudWatch (metric collection + alarm), and SNS (email delivery). [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

The final outcome: if the EC2 instance's CPU spikes above 60%, you receive an email — automatically, without watching dashboards.

***

## Step 1: Verify the EC2 Instance and Its Standard Metrics

Navigate to **EC2** → select your running instance → click the **Monitoring** tab. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**What you'll see:** Graphs for the standard metrics — CPU Utilization, Status Checks, Network In/Out, Network Packets In/Out, Disk Read/Write, Disk Operations. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**Important:** If the instance was recently launched, the graphs may show **"No data available"**. This is normal — CloudWatch needs time to collect initial data points. Wait a few minutes and refresh. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**Verification:** After some time, graphs should begin populating with data. CPU Utilization should show a line (likely near 0% for an idle instance).

**Connection to flow:** These metrics are being collected automatically by CloudWatch. Our next step is to set an alarm on one of them.

***

## Step 2: Verify EBS Volume Metrics (Optional Observation)

Navigate to **EC2 → Volumes** → select your volume → click the **Monitoring** tab. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**What you'll see:** Read Bandwidth, Write Bandwidth, Read Throughput, Write Throughput graphs. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**Why observe this:** This confirms the instructor's point that every AWS service has CloudWatch metrics — not just EC2. The Monitoring tab pattern is consistent across services.

***

## Step 3: Set Up the CloudWatch Alarm with SNS Notification

The instructor states the goal: *"We are going to set alarm on that metrics. We are going to say if my CPU utilization at a certain level, then it should trigger an email notification."* [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

This step involves configuring three things:

1. **The metric to watch** — EC2 CPU Utilization
2. **The alarm threshold** — Above 60%
3. **The notification action** — Send email via SNS

Navigate to **CloudWatch** service → **Alarms** → **Create Alarm**. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

### 3a. Select the Metric

Choose **EC2** → **Per-Instance Metrics** → find your instance → select **CPUUtilization**.

**Why CPUUtilization:** This is the most commonly monitored metric for compute instances. A CPU spike often indicates the application is under heavy load, is stuck in a loop, or is being attacked.

### 3b. Define the Threshold

Set the condition: **Greater than 60** (percent).

This means: if CPU utilization exceeds 60% for the evaluation period, the alarm transitions to the ALARM state.

### 3c. Configure the SNS Notification

Create a new **SNS topic** or select an existing one. Add your **email address** as a subscriber. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**Important:** When you add an email subscriber to an SNS topic, AWS sends a **confirmation email**. You must click the confirmation link in that email before you can receive alarm notifications. If you skip this, notifications will silently fail.

### 3d. Name and Create the Alarm

Give the alarm a descriptive name → review → **Create Alarm**. [\[123. Cloud...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/123.%20Cloudwatch%20Introduction.txt)

**Verification:** The alarm should appear in the CloudWatch Alarms list with state **OK** (meaning the metric is currently below the threshold) or **INSUFFICIENT\_DATA** (if metrics haven't been collected yet).

**Connection to flow:** The pipeline is now complete: EC2 generates CPU metrics → CloudWatch collects them and evaluates the alarm → if threshold is breached, CloudWatch triggers SNS → SNS sends email.

***

## Step 4: Test the Alarm (Implied)

To verify the alarm works, you would need to generate CPU load on the instance (e.g., using a stress tool). When CPU exceeds 60%, the alarm transitions from **OK** to **ALARM** state, and you receive the email notification.

**Common mistakes:**

* Not confirming the SNS email subscription → no emails arrive
* Setting the threshold too high (e.g., 99%) → alarm never triggers under normal load
* Instance recently launched → "Insufficient Data" state persists until enough data points are collected

***

## Step 5: Cleanup (Implied)

After completing the lab:

* **Delete the alarm** in CloudWatch
* **Delete the SNS topic** (or unsubscribe your email)
* **Terminate the EC2 instance** if no longer needed

Standard cost-prevention cleanup applies (see previous AWS material).

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## CloudWatch Identity

```
CloudWatch = AWS built-in observability platform
  ├── Metrics   (performance data — PRIMARY focus of this lecture)
  ├── Alarms    (threshold-based notifications)
  ├── Events    (real-time action stream — covered in Part 2)
  ├── Logs      (centralized log collection — covered in Part 2)
  └── Log Insights & more
```

***

## CloudWatch Three Pillars

```
METRICS         = What is measured     (CPU, disk, network, bandwidth...)
EVENTS          = What happened        (instance launched, snapshot taken...)
LOGS            = What was recorded    (application logs, system logs...)

This lecture: METRICS + ALARMS
Part 2:       LOGS + EVENTS + log-based metrics
```

***

## Metrics: Automatic Collection

```
Launch ANY AWS resource → CloudWatch automatically collects standard metrics
  NO setup needed | NO agent needed (except EC2 logs) | NO registration

EC2 standard metrics:
  CPU Utilization | Status Checks
  Network In/Out | Network Packets In/Out
  Disk Read/Write | Disk Read/Write Operations

EBS standard metrics:
  Read/Write Bandwidth | Read/Write Throughput

ANY AWS service → has metrics → viewable via Monitoring tab

Custom metrics = additional measurements beyond standard (you define them)
```

***

## Metrics Visibility Pattern

```
Metrics originate from: CloudWatch (collection engine)
Metrics appear in:
  ├── CloudWatch console (centralized view)
  └── Each service's own Monitoring tab (contextual view)
        EC2 instance → Monitoring tab → CPU, Network, Disk graphs
        EBS volume → Monitoring tab → Bandwidth, Throughput graphs
        (Same data, different presentation location)
```

***

## Three-Service Alarm Pipeline

```
[EC2 Instance]  ──generates metrics──→  [CloudWatch]  ──triggers alarm──→  [SNS]  ──sends──→  [Email]
   (data source)                     (collect + evaluate)                (deliver notification)

Config: "If CPUUtilization > 60% → send email"

Each service = single responsibility:
  EC2 = produce data
  CloudWatch = watch + evaluate
  SNS = notify
```

***

## Alarm State Machine

```
INSUFFICIENT_DATA → (metrics start flowing) → OK → (threshold breached) → ALARM → (back below) → OK

INSUFFICIENT_DATA = not enough data yet (new instance, new alarm)
OK                = metric is within acceptable range
ALARM             = metric crossed threshold → action triggered
```

***

## Timing Nuance

```
New instance launched → Monitoring tab shows "No data available"
  → CloudWatch needs time to collect first data points
  → Standard monitoring = 5-min intervals
  → Wait, then refresh → graphs appear
```

***

## Logs: EC2 Difference

```
Most AWS services → native log streaming to CloudWatch (enable in config)
EC2 instances     → NO direct option
  └── Must install CloudWatch Agent on OS → agent streams logs to CloudWatch

(Covered in Part 2)
```

***

## Events: Action Stream

```
Events = discrete actions in AWS environment
  Examples: instance launched, terminated, snapshot created, volume created
  
Use case: Set triggers → integrate with Lambda functions
  "When instance launched → Lambda auto-configures it"

(Covered in Part 2)
```

***

## Operational Flow

```
── OBSERVE METRICS ──
EC2 → Instance → Monitoring tab → standard metrics (auto-collected)
EBS → Volume → Monitoring tab → standard metrics (auto-collected)

── SET ALARM ──
CloudWatch → Alarms → Create Alarm
  → Select metric: EC2 → Per-Instance → CPUUtilization
  → Set threshold: > 60%
  → Configure action: SNS topic → email subscriber
  → Name → Create

── VERIFY ──
Alarm state: OK (normal) or INSUFFICIENT_DATA (new)
Generate CPU load → state transitions to ALARM → email arrives

── CLEANUP ──
Delete alarm | Delete SNS topic | Terminate instance
```

***

## This Lecture vs. Part 2

```
THIS LECTURE (current):                 PART 2 (future):
  Metrics (standard + custom concept)     Logs (agent, streaming)
  Alarms (threshold → SNS → email)        Metrics on logs
  Three-service pipeline (EC2+CW+SNS)     Events + triggers (Lambda)
                                           Additional actions
```

***

## Reusable Engineering Patterns

| Pattern                       | Manifestation                                                              |
| ----------------------------- | -------------------------------------------------------------------------- |
| **Automatic instrumentation** | Every AWS resource gets metrics by default — zero setup                    |
| **Embedded observability**    | Monitoring tab inside each service — metrics at point of use               |
| **Threshold-based alerting**  | Metric → threshold → alarm → notification (universal pattern)              |
| **Service composition**       | EC2 + CloudWatch + SNS — each has single responsibility, composed together |
| **Data → Evaluate → Act**     | Generate data → watch for anomaly → take automated action                  |

***

## Core Mental Model

```
CloudWatch = The nervous system of your AWS environment
  Automatically senses everything (metrics)
  Watches for problems (alarms)
  Alerts you when something is wrong (SNS)
  Records what happened (events)
  Stores what was said (logs)

You don't build monitoring — it's already there.
You BUILD ON IT: alarms, triggers, automations.

Three-service pattern: Source → Monitor → Notify
  (This pattern repeats across all AWS alerting)
```

***

This material captures every concept, service relationship, metric detail, and operational pattern from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
