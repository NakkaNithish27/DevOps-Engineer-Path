# 📈 AWS Auto Scaling Group — Hands On — Deep Learning Material

**Source:** Video caption file — [127. Autoscaling Group Hands On.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt?EntityRepresentationId=09e7ec8b-c7f5-465d-92c9-dcea51785638) [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Video Context:** The instructor performs a comprehensive hands-on exercise for Auto Scaling Groups (ASG), starting from the prerequisites (launch template, target group, load balancer), through ASG creation with scaling policies and health checks, to application update via instance refresh, advanced ASG management options, and full cleanup. This is explicitly described as the lecture that "really binds everything together" — EC2 instances, key pairs, security groups, load balancers, target groups, AMIs, launch templates, CloudWatch alarms, and EFS storage.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Auto Scaling Group Is and the Problem It Solves

An **Auto Scaling Group (ASG)** is an AWS service that **manages a group of EC2 instances** for you. Instead of you manually launching, monitoring, and terminating instances, the ASG does it automatically based on rules you define. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The core problem: in a production environment, demand fluctuates. At peak times, you need more instances to handle the load. At quiet times, you're paying for idle capacity. Manually scaling — watching metrics, launching instances, registering them with load balancers, terminating them later — is slow, error-prone, and not feasible at scale. ASG automates the entire lifecycle: it launches instances when demand rises, removes them when demand falls, and replaces any that become unhealthy — all without human intervention.

***

## 1.2 The Prerequisite Chain — Four Ingredients

The instructor opens by listing the components needed **before** creating an ASG: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**1. Launch Template** — Tells ASG *how* to configure each instance it launches: which AMI to use, what instance type, which key pair, which security group, resource tags, etc. "Based on this information, Auto Scaling Group will decide everything." Previously, AWS also supported "Launch Configurations" which were similar, but now **only Launch Templates are supported**.

**2. Target Group** — The container that will hold the instances for health checking and load balancer routing. The critical point: **you create the target group empty**. The instructor explicitly states: "We are not adding any instance in the target group. Auto Scaling Group is going to fill this target group with instances." Even if you have existing instances, "do not add it." ASG owns the membership of this target group.

**3. Application Load Balancer (ALB)** — Distributes incoming web traffic across the instances in the target group. The ALB listens on port 80 and forwards traffic to the target group.

**4. AMI** — The disk image from which instances are launched. The instructor uses an AMI that includes EFS connectivity (from a previous lecture) to demonstrate shared storage, but notes "it's not mandatory to have the EFS AMI — you can use the previous AMI also." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The dependency chain is: **AMI → Launch Template → Target Group + ALB → ASG**. ASG sits at the top and orchestrates everything below it.

🔍 **Deep Dive:** The instructor's choice to use the EFS-connected AMI is deliberate and serves a later teaching point: ASG instances must be **stateless** (data stored outside the instance). Using an AMI pre-configured for EFS ensures all instances share a common filesystem for dynamic data. This is not just a convenience — it's an architectural requirement for auto-scaled environments. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## 1.3 The Relationship Between ASG, Target Group, and Load Balancer

This three-way relationship is the architectural core of the exercise. Understanding it prevents a common confusion about who manages what. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The **Load Balancer** receives traffic from the internet and forwards it to the **Target Group**. The Target Group contains registered instances and performs health checks on them. The **ASG** adds and removes instances from the Target Group based on scaling rules and health status.

The critical ownership model: **ASG owns instance lifecycle**. You don't manually add instances to the target group. You don't manually launch or terminate instances. The ASG does all of this. If you terminate an instance manually, ASG will launch a replacement because it maintains the **desired capacity**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The instructor also clarifies that a load balancer is **not mandatory** for ASG: "Auto Scaling Group does not mean you should have load balancer. Usually if you're serving web traffic, you will have load balancer. But there are use cases where the instances should do some shared working, internal syncing, internal communication. They don't need load balancer." ASG can manage instance groups for any purpose — not just web serving. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## 1.4 Health Checks — Three Layers of Instance Health

This is one of the most important concepts in the video. ASG needs to know if an instance is healthy. If unhealthy, ASG removes it and launches a replacement. But "healthy" has multiple meanings, and ASG offers three health check mechanisms: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**EC2 Health Check (default):** This is basic — it checks the underlying hardware and the VM itself. "This is just going to check the hardware on which it is running and the VM health." If the hardware is fine and the VM is running, it reports healthy. **The critical limitation:** if the Apache process crashes inside the instance, EC2 health check still reports healthy because the VM itself is fine. "Auto Scaling Group will not know in that case whether the process is crashed or not." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Elastic Load Balancer (ELB) Health Check:** This uses the target group's health check mechanism — it checks the **application layer**. It sends HTTP requests to a specific port (80) and path, and if the response is healthy, the instance is considered healthy. If the web service crashes, the HTTP check fails, the target group marks the instance as unhealthy, and ASG receives this signal. The instructor strongly recommends enabling this: it's the "very good way of deciding whether the instance is healthy or not." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Amazon EBS Health Check:** Checks the health of the root volume and any attached EBS volumes. "When these volumes are unhealthy, definitely the instance will be unhealthy. The process will be dead." This catches storage-level failures that neither EC2 nor ELB checks would detect directly. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The unhealthy instance flow: **service crashes → ELB health check fails → target group marks unhealthy → ASG detects → ASG launches replacement → ASG removes unhealthy instance**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## 1.5 Stateless Application Design — The ASG Data Imperative

The instructor delivers this as a fundamental architectural requirement, not just advice: "If you are storing data in the instance, make sure it is stored into a shared storage or into any file storage out of the instance — not on the hard disk, not on the EBS volume." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The reasoning is direct: ASG **will delete** unhealthy instances. When an instance is deleted, its local storage is gone. If application data was stored locally, it's lost. Therefore, any dynamic data must live **outside** the instance — in EFS, S3, RDS, or any shared storage.

This leads to two architectural terms the instructor defines:

**Stateless application:** "The application that doesn't store any data locally." Even if the instance is removed and replaced, nothing is lost because all data lives externally. "You are using instance only for its resource capacity — CPU, memory, operating system — but not for the data."

**Stateful application:** Stores data locally. "But you can store it outside and your instance becomes stateless." The design pattern is: take a stateful app and externalize its state to make it ASG-compatible. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

⚠️ **Expert Note:** The instructor mentions there is "an option later to preserve that instance" (scaling protection), but even with protection, designing for statelessness is the correct approach. Protection is a temporary operational tool (e.g., for debugging), not an architecture strategy.

***

## 1.6 Scaling Policies — How ASG Decides Instance Count

ASG manages instance count through three parameters and scaling policies: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Desired Capacity:** How many instances ASG should maintain right now. The instructor sets this to 2.

**Minimum Capacity:** The floor — ASG will never go below this number. Set to 1. "In any case, even if there is no load, there's nothing — at least I should have 1 or 2 based on your requirement."

**Maximum Capacity:** The ceiling — ASG will never exceed this number. Set to 4.

**Target Tracking Scaling Policy:** The instructor enables this with **CPU utilization** as the metric and a **target value of 50%**. The behavior: "If the combined group CPU utilization is above 50, then it is going to add instances — how many maximum it can go: four. If it's below 50, it can remove instances — minimum it can have: one." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Other available metrics: **Network In** and **Network Out** — "This is also very useful in web traffic where more traffic coming in, you add more instances; when traffic reducing, you remove instances."

**Disable Scale-In option:** You can check a box to "disable scaling to create only a scale-out policy." This means ASG will add instances when load increases but will **never remove** instances when load decreases. Useful when you want to scale up automatically but control scale-down manually. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The instructor emphasizes these are "random numbers" — in production: "You need to decide this based on performance testing. There should be a testing team who makes the performance testing on your application. You need to have proper information that your instance works till how much and crashes when."

***

## 1.7 Advanced Scaling Options

Beyond target tracking, the instructor shows additional scaling mechanisms: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Step Scaling Policy:** More granular than target tracking. You define steps: "If CPU above 50, launch 1 instance. But if it goes above 60, launch maybe 2 instances." Each step corresponds to a CloudWatch alarm threshold. This requires creating **CloudWatch alarms** first. You can have separate step policies for scale-up and scale-down.

**Predictive Scaling Policy:** Uses **historical data** to predict future demand and scales out **in advance**. "Totally depends on the historical data — what happened previously. Based on that, if you enable this, it can scale out in advance." The instructor notes this is out of scope for this course but important to know it exists. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Scheduled Actions:** Scale based on time rather than metrics. "Let's say you know there's a sale coming on a website. You can decide at what particular time it starts." You set desired, minimum, and maximum capacity for a specific time window, with options for one-time or recurring schedules (daily, weekly). You can also set an end time when the scaling reverts. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## 1.8 Instance Maintenance Policy — Replacement Ordering

When ASG needs to replace instances (during refresh or unhealthy replacement), you can control the order: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Launch before terminating:** Launch the new instance, wait for it to be ready, **then** terminate the old one. "This is good, but this adds cost because the instance needs to be ready — then only it is going to delete the old one."

**Terminate and launch at the same time:** Terminate the old and launch the new simultaneously. "This controls cost."

**No policy (default):** "Instance will launch before terminating the unhealthy one. But it's not going to wait for it to be healthy." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The trade-off is always **availability vs. cost**: launching first ensures zero downtime but doubles capacity temporarily. Simultaneous replacement minimizes cost but creates a brief capacity gap.

***

## 1.9 Application Updates — The Instance Refresh Mechanism

A critical operational concept: "You cannot directly log into the instance and make changes. These are the group maintained by Auto Scaling Group. So there is no manual changes." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

The update workflow:

1. Build a **new AMI** with your changes
2. Update the **Launch Template** (new version or new template entirely)
3. Update the ASG to use the new Launch Template

But changing the launch template only affects **future** instances. "If a new scaling event comes in, the new instance will be from the new launch template that you have updated. But existing instances will be there as it is." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

To replace **existing** instances with the new template: use **Instance Refresh**. This triggers ASG to systematically replace all current instances with new ones built from the updated template. You choose the replacement strategy (terminate and launch simultaneously, or launch first then terminate). ASG handles the rolling replacement. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## 1.10 Instance Management — Detach, Standby, and Scale Protection

ASG provides per-instance management actions: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Detach:** Remove an instance from the ASG entirely. The instance keeps running but is no longer managed by ASG.

**Set to Standby:** The instance stays in the group but is excluded from scaling events and load balancer traffic. Useful during maintenance.

**Scale Protection:** Prevents ASG from terminating a specific instance. The instructor gives the use case: "You're troubleshooting. You don't want the instance to get deleted. Maybe you're bringing down services, looking for some information. That might trigger a scaling event if the process goes down. So while you're doing that, you can set scaling protection so you can safely log into the instance." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

There's also a global option during ASG creation: **scaling protection for newly launched instances** — when enabled, all new instances are protected from scale-in by default.

***

## 1.11 Availability Zone Distribution

When configuring ASG, you select which **Availability Zones (AZs)** instances can be launched in. The instructor selects all available AZs. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

A new option is shown: **Balanced Best Effort** — "If launches fail in one AZ, Auto Scaling Group will attempt to launch in another healthy AZ." This is contrasted with **Balanced Only** — "If it fails, it's going to keep attempting to launch into the same AZ again." The instructor recommends Balanced Best Effort unless you have a specific use case requiring instances in a particular AZ. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## 1.12 Cleanup Architecture — Deletion Order Matters

The instructor demonstrates the cleanup order and explains why: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

"You cannot just directly delete the instance in an auto scaling group — even if you delete it, auto scaling group will create it again, because you have mentioned the desired capacity, it will always keep that capacity." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Two options to remove instances:

1. Set desired/minimum capacity to **0, 0, 0** — ASG deletes all instances but the ASG itself remains (no cost for the ASG itself)
2. Delete the ASG entirely — instances are terminated as part of deletion

The load balancer must be deleted separately, and **it does incur cost** even without instances behind it. The instructor emphasizes: "You cannot keep this load balancer for a long time, otherwise you'll get some cost." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

AMI cleanup is two-step: **deregister AMI → delete snapshot** (as covered in the previous ELB lecture).

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a **fully automated, self-healing, auto-scaling web server infrastructure**: an Auto Scaling Group that maintains a fleet of EC2 instances behind an Application Load Balancer, with automatic scaling based on CPU utilization and automatic replacement of unhealthy instances. The final outcome: a website accessible through the load balancer DNS, backed by instances that scale up under load, scale down when quiet, and self-heal when any instance fails. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## Phase A: Create the Prerequisites

### Step A1: Create the Launch Template

Navigate to **EC2 Console → Instances → Launch Templates → Create Launch Template**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Settings:**

* **Name:** `Inner Peace Shared` (or any descriptive name)
* **AMI:** Select your AMI from "My AMIs" (the instructor uses the EFS-connected AMI, but any working AMI is fine)
* **Instance type:** `t2.micro` (or `t3.micro` — stay in free tier)
* **Key pair:** Select your existing key pair (e.g., `inner peace key`)
* **Security group:** Select the instance security group (e.g., `inner peace security group`). Make sure you select the correct one — not the load balancer security group or EFS security group.
* **Resource tags:** Add a Name tag: `Inner Peace Web` — check "Tag instances" and "Tag volumes" and "Tag network interfaces"

Click **Create Launch Template**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Verification:** The template appears in the Launch Templates list with status "Created."

**Connection to flow:** This template is what ASG reads to know how to configure every instance it launches.

***

### Step A2: Create the Target Group (Empty)

Navigate to **EC2 Console → Load Balancing → Target Groups → Create Target Group**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Settings:**

* **Target type:** Instances
* **Name:** `inner-peace-ASG-tg` (the `-tg` suffix indicates this is a target group for the ASG)
* **Port:** 80 (default)
* **Health check:** Default settings, but **reduce Healthy threshold to 2** — "So then the instance becomes healthy quickly, as in just two health checks"

Click **Next**.

**Do NOT register any targets.** Leave the instances section empty. Click **Create Target Group**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Critical point:** ASG will populate this target group. If you manually add instances, ASG's management conflicts with your manual entries.

***

### Step A3: Create the Application Load Balancer

Navigate to **EC2 Console → Load Balancing → Load Balancers → Create Load Balancer → Application Load Balancer → Create**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Settings:**

* **Name:** `inner-peace-ASG-alb` (the `-alb` suffix indicates this is the ALB for the ASG)
* **Availability Zones:** Select **all** available zones — "the instance can be in any of the zones and the load balancer is going to serve the traffic to those instances"
* **Security group:** Remove the default security group. Add the **load balancer security group** (not the instance security group)
* **Listener:** Port 80, forward to target group: `inner-peace-ASG-tg`

Click **Create Load Balancer**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Wait** until the load balancer state changes from **Provisioning** to **Active** (takes a few minutes).

**Verification:** Load Balancer shows "Active" state in the console.

**Connection to flow:** The ALB is now ready to receive traffic and forward it to the (currently empty) target group. ASG will fill the target group with instances.

***

## Phase B: Create the Auto Scaling Group

Navigate to **EC2 Console → Auto Scaling → Auto Scaling Groups → Create Auto Scaling Group**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

### Step B1: Name and Launch Template

* **Name:** `NRP-ASG` (or any name)
* **Launch Template:** Select the template created in Step A1

Click **Next**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

### Step B2: Network Configuration

* **VPC:** Keep the default VPC
* **Availability Zones:** Select **all** available zones (or specific zones if you have a use case)
* **AZ distribution:** Select **Balanced Best Effort** — if launches fail in one AZ, ASG will attempt another healthy AZ [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Click **Next**.

***

### Step B3: Load Balancer Integration

* Select **Attach to an existing load balancer**
* For Application Load Balancer, you select the **target group** (not the load balancer directly): select `inner-peace-ASG-tg`
* **Turn on ELB health checks** — this enables application-layer health checking (see Theory §1.4)
* **Turn on Amazon EBS health checks** — catches volume-level failures [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Click **Next**.

🔍 **Deep Dive:** The reason you select the target group (not the load balancer) is architectural: the ALB routes to target groups, and ASG manages target group membership. The ALB is already configured to forward to this target group (from Step A3). By telling ASG which target group to manage, the chain is complete: ALB → target group ← ASG. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

### Step B4: Scaling Configuration

**Capacity:**

* **Desired:** `2` (ASG will immediately launch 2 instances)
* **Minimum:** `1` (never fewer than 1)
* **Maximum:** `4` (never more than 4) [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Scaling Policy:**

* Enable **Target Tracking Scaling Policy**
* **Metric:** CPU Utilization (other options: Network In, Network Out)
* **Target value:** `50` — if combined group CPU exceeds 50%, add instances; if below 50%, remove instances

**Instance Maintenance Policy:** Keep as "No policy" (default behavior — launch before terminating but don't wait for healthy). [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Click **Next**.

***

### Step B5: Notifications (Optional)

You can configure SNS notifications for events: Launch, Terminate, Fail to Launch, Fail to Terminate. The instructor shows the option but does not configure it. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Click **Next**.

***

### Step B6: Tags

Add a **Name** tag: `Inner Peace Web ASG` — this tag will be applied to all instances launched by the ASG, making them identifiable in the console. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Click **Next**.

***

### Step B7: Review and Create

Review all settings. Click **Create Auto Scaling Group**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**What happens immediately:** ASG begins launching instances to reach the desired capacity of 2. This takes approximately 5 minutes.

***

### Step B8: Verify the Complete System

**Verify ASG:** Check the ASG console — it should show 2 instances.

**Verify instances:** Navigate to EC2 → Instances — two new instances should be running with the name tag "Inner Peace Web ASG."

**Verify target group:** Navigate to Target Groups → select the target group — should show 2 registered targets, both with status **Healthy**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Verify through load balancer:** Copy the **DNS name** of the load balancer → paste in browser → the website should load.

The instructor confirms: "It's coming. And also the images — yes, those are coming from EFS." This validates the entire chain: ALB → target group → healthy instances → EFS shared storage. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

## Phase C: Application Update via Instance Refresh

### Step C1: Update the Launch Template in ASG

Navigate to ASG → select the ASG → **Details → Edit**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

Change the **Launch Template** to a different template (or a different version of the same template). In the video, the instructor switches to the previous template (without EFS) as a demonstration.

Click **Update**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**What this does:** Future instances will use the new template. **Existing instances are unaffected.**

***

### Step C2: Trigger Instance Refresh

Navigate to the **Instance Refresh** tab → Click **Start Instance Refresh**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Replacement strategy:** The instructor selects "Terminate and launch at the same time" (cost-controlled). The other option is "Launch first, then terminate" (availability-focused).

Click **Start Instance Refresh**. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**What happens:** ASG systematically replaces all existing instances with new ones built from the updated launch template. You can monitor progress in the Instance Refresh history and in the Activity tab.

**Activity tab shows:** "Launching a new instance... Terminating instance..." — both happening simultaneously (per the selected strategy).

***

## Phase D: Cleanup

**Order matters.** Follow this sequence: [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

### D1: Delete the Load Balancer

**EC2 → Load Balancers → Select → Actions → Delete → Confirm**

⚠️ Load balancers incur cost even without instances. Delete first. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

### D2: Delete the Auto Scaling Group

**EC2 → Auto Scaling Groups → Select → Delete → Confirm**

This terminates all managed instances. Alternatively, set Desired/Min/Max to **0/0/0** to keep the ASG but remove all instances (no cost for ASG itself). [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

**Important:** Do NOT try to terminate instances directly while ASG exists — "even if you delete it, Auto Scaling Group will create it again." [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

### D3: Delete the Target Group

**EC2 → Target Groups → Select → Actions → Delete**

No cost, but clean up for hygiene. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

### D4: Deregister unused AMIs + Delete orphaned Snapshots

**AMIs → Select → Actions → Deregister** then **Snapshots → Select → Actions → Delete**

The instructor keeps one AMI (EFS-connected) for future use and deletes the rest. He notes: "This is the problem if you don't name stuff properly" — when two snapshots exist and aren't named, it's hard to tell which belongs to which AMI. [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

### D5: Dashboard Check

**EC2 → Dashboard → Refresh** — verify no unexpected resources remain (instances, elastic IPs, volumes, etc.). [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Full System Architecture

```
INTERNET
    │
    ▼
┌──────────────────────────┐
│  Application Load        │
│  Balancer (ALB)          │
│  DNS: *.elb.amazonaws.com│
│  Listener: :80           │
│  SG: LB Security Group   │
└──────────┬───────────────┘
           │ forwards to
           ▼
┌──────────────────────────┐
│  Target Group            │
│  (inner-peace-ASG-tg)    │
│  Port: 80                │
│  Health Check: HTTP :80   │
│  Healthy Threshold: 2    │
│  ⚠️ EMPTY at creation     │
│  ← ASG fills this        │
└──────────┬───────────────┘
           │ contains
           ▼
┌──────────────────────────────────────────┐
│  Auto Scaling Group (NRP-ASG)            │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │Instance 1│  │Instance 2│  │ ... N  │ │
│  │(from LT) │  │(from LT) │  │        │ │
│  └──────────┘  └──────────┘  └────────┘ │
│  Desired: 2 | Min: 1 | Max: 4           │
│  Scaling: CPU > 50% → add | < 50% → rm  │
│  Health: EC2 + ELB + EBS                 │
│  Source: Launch Template → AMI           │
└──────────────────────────────────────────┘
           │ instances connect to
           ▼
┌──────────────────────────┐
│  EFS (shared storage)    │
│  Dynamic data lives HERE │
│  NOT on instance disk    │
└──────────────────────────┘
```

***

## ⚡ Prerequisite Chain — Build Order

```
1. AMI               ← disk image (OS + app + config)
2. Launch Template    ← AMI + instance type + key + SG + tags
3. Target Group       ← EMPTY, port 80, health check, threshold 2
4. Load Balancer (ALB)← all AZs, LB security group, listener :80 → TG
5. Auto Scaling Group ← launch template + TG + scaling policy + health checks

DEPENDENCY:  AMI → LT → ASG → fills TG → ALB routes to TG
```

***

## 🔗 Health Check Layers

```
LAYER 1: EC2 Health Check (default, basic)
  └── Checks: hardware + VM running
  └── MISSES: crashed application process

LAYER 2: ELB Health Check (enable this!)
  └── Checks: HTTP request to port 80 → response OK?
  └── CATCHES: crashed web service, unresponsive app

LAYER 3: EBS Health Check
  └── Checks: root volume + attached volumes healthy?
  └── CATCHES: storage failures

UNHEALTHY FLOW:
  Service crashes → ELB health check fails → TG marks unhealthy
  → ASG detects → launches replacement → removes unhealthy instance
```

***

## 📊 Scaling Policy Map

```
TARGET TRACKING (simple):
  Metric: CPU / Network In / Network Out
  Target: 50%
  Above target → scale OUT (add instances, up to Max)
  Below target → scale IN (remove instances, down to Min)
  Option: disable scale-in (scale out only)

STEP SCALING (granular):
  Requires CloudWatch Alarms
  CPU > 50% → add 1 instance
  CPU > 60% → add 2 instances
  (custom steps per alarm threshold)

PREDICTIVE SCALING:
  Uses historical data → scales in advance
  (advanced, out of scope)

SCHEDULED ACTIONS:
  Time-based scaling (e.g., sale event)
  Set desired/min/max for specific time window
  One-time or recurring (daily/weekly)
  Can set end time
```

***

## 🔄 Application Update Flow

```
OLD WAY (manual): SSH → change code → ❌ WRONG with ASG
  "You cannot directly log into the instance and make changes"

CORRECT WAY:
  1. Build new AMI (with changes)
  2. Update Launch Template (new version or new template)
  3. Update ASG → point to new Launch Template
     └── Only affects FUTURE instances
  4. Instance Refresh → replace ALL existing instances
     ├── Option A: Terminate + Launch simultaneously (cost)
     └── Option B: Launch first, wait healthy, then terminate (availability)

  Activity tab shows: launching new ↔ terminating old
```

***

## 🛡️ Instance Management Actions

```
DETACH      → Remove from ASG entirely (instance keeps running independently)
STANDBY     → Stays in ASG but excluded from scaling/traffic
PROTECTION  → Prevent ASG from terminating (for troubleshooting)
              "Safely log in, make changes, instance won't get deleted"

GLOBAL PROTECTION: Enable for all newly launched instances
```

***

## 🧱 Stateless Design Rule

```
ASG WILL DELETE unhealthy instances → local data LOST

RULE: Dynamic data must live OUTSIDE the instance
  ├── EFS (shared filesystem)
  ├── S3 (object storage)
  ├── RDS (database)
  └── Any external storage

STATELESS = instance stores NO local data
  → "Using instance only for CPU, memory, OS"
  → Safe to delete/replace anytime

STATEFUL  = instance stores local data
  → ⚠️ INCOMPATIBLE with ASG unless externalized
```

***

## 🧹 Cleanup Sequence + Cost Map

```
DELETE ORDER:
  1. Load Balancer     ← COSTS MONEY even idle, delete first
  2. Auto Scaling Group ← terminates all managed instances
     (OR set desired/min/max to 0/0/0 → keeps ASG, removes instances)
  3. Target Group      ← no cost, cleanup hygiene
  4. AMIs → Deregister ← then delete associated Snapshots
  5. Dashboard check   ← verify nothing orphaned

⚠️ Cannot delete instances directly while ASG manages them
   → ASG will recreate to maintain desired capacity
   → Must delete ASG or set capacity to 0

COST ITEMS: Load Balancer (always), Instances (running), Elastic IPs, Snapshots
NO COST:    ASG itself (0 instances), Target Group, Launch Template
```

***

## 📦 AZ Distribution Options

```
BALANCED BEST EFFORT (recommended):
  Launch fails in AZ-A → try AZ-B → try AZ-C
  Resilient to AZ capacity issues

BALANCED ONLY:
  Launch fails in AZ-A → retry AZ-A → retry AZ-A
  Use only when instances MUST be in specific AZ
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Controller/Worker Orchestration**
ASG is the **controller** — it decides how many worker instances exist, launches them, monitors their health, and removes/replaces them. Workers (instances) don't manage themselves. All lifecycle decisions are centralized in the controller. This pattern appears in Kubernetes (scheduler/pods), Docker Swarm (manager/workers), and any orchestration system.

**Pattern 2: Empty Container → Auto-Population**
Create the target group empty → ASG fills it. Create the ALB pointing to the empty target group → ASG makes it useful. The infrastructure is wired together **before** instances exist. Components are designed to work once populated, not requiring pre-population. This is declarative infrastructure: describe the desired state, let the system achieve it.

**Pattern 3: Immutable Deployment**
Never modify running instances. Build a new AMI → update template → refresh instances. Every instance is created from a known template and never modified in place. Replacement, not mutation. This ensures consistency and eliminates configuration drift.

**Pattern 4: Externalize State for Replaceability**
Any component that might be destroyed and recreated (ASG instances) must not hold irreplaceable state. Push state to durable external services (EFS, S3, RDS). This makes compute disposable — the fundamental principle enabling auto-scaling, self-healing, and rolling updates.

***

## 🎯 One-Line System Summary

> **An Auto Scaling Group uses a Launch Template to automatically launch/terminate EC2 instances (maintaining desired capacity within min/max bounds based on CPU/network metrics or schedules), registers them in a Target Group behind an Application Load Balancer, replaces unhealthy instances detected by ELB+EBS health checks, and supports zero-downtime application updates via Instance Refresh — requiring stateless instance design with all dynamic data stored externally.** [\[127. Autos...p Hands On \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/127.%20Autoscaling%20Group%20Hands%20On.txt)
