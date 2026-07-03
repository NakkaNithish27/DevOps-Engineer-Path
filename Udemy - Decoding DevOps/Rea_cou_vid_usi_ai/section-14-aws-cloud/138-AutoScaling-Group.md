# AWS Auto Scaling Group — vProfile Lift & Shift Project

**Source:** Video caption file — *"Autoscaling Group"* (lecture from the vProfile AWS Lift & Shift course) [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is an Auto Scaling Group and Why Does It Exist?

An Auto Scaling Group (ASG) is an AWS service that automatically manages the number of EC2 instances running a particular workload. It can **scale out** (launch new instances) when load increases and **scale in** (terminate instances) when load decreases. The fundamental problem it solves is that in a production environment, traffic is never constant — it fluctuates throughout the day, week, and year. Without Auto Scaling, you either over-provision (waste money running idle servers) or under-provision (degrade user experience during spikes). An ASG eliminates this tradeoff by dynamically adjusting capacity to match actual demand. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

In this project, the ASG is applied specifically to **app01** — the Tomcat application instance that serves the vProfile application. The backend services (MySQL, Memcache, RabbitMQ) are not placed in an Auto Scaling Group because they are stateful services that don't scale horizontally the same way a stateless application server does. The application tier, however, is the one directly receiving user traffic through the load balancer, making it the natural candidate for elastic scaling. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.2 — The Three Prerequisites: AMI → Launch Template → Auto Scaling Group

An Auto Scaling Group does not create instances from scratch — it needs to know **what** to launch and **how** to launch it. This information is organized into a strict dependency chain of three components. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**AMI (Amazon Machine Image)** is the first prerequisite. An AMI is a snapshot — a complete image — of an existing EC2 instance, capturing its operating system, installed software, configuration, and application state at the moment the image is taken. When the ASG needs to launch a new instance, it uses this AMI as the base. The reason you create the AMI from the existing app01 instance (rather than starting from a blank OS) is that app01 is already fully configured — Tomcat is installed, the application is deployed, all settings are in place. The AMI captures all of that, so every new instance launched from it is an exact clone of the working app01. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Launch Template** is the second prerequisite. While the AMI defines **what** is on the instance, the Launch Template defines **how** the instance is launched — the operational context. It specifies: which AMI to use, the instance type (t2.micro or t3.micro for free tier), which key pair for SSH access, which security group (the app security group in this case), resource tags, and optionally an IAM instance profile (role). The Launch Template is essentially an instruction sheet that the ASG reads every time it needs to launch a new instance. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Auto Scaling Group** is the final component. It references the Launch Template and adds the scaling logic on top: how many instances to maintain (desired capacity), the minimum it can scale down to, the maximum it can scale up to, which availability zones to spread instances across, which load balancer/target group to register new instances with, health check configuration, and the scaling policy that triggers scale-out and scale-in events. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The dependency chain is strictly linear: **AMI → Launch Template → Auto Scaling Group**. You cannot create a Launch Template without an AMI to reference, and you cannot create an ASG without a Launch Template to reference. This is why the video follows this exact order. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

🔍 **Deep Dive:**
The AMI creation process takes time because AWS is creating a full block-level snapshot of the instance's EBS volume(s). During this time, the AMI is in a "pending" state and cannot be used. The video leverages this wait time to create the Launch Template in parallel — a practical example of optimizing workflow by doing independent tasks while waiting for blocking operations. Note that the AMI appears in the Launch Template's AMI selection list even while still pending (you can select it by name), but the ASG won't be able to actually launch instances from it until the AMI reaches "available" state. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.3 — Launch Template: The Instance Blueprint

The Launch Template is more than just a configuration form — it is the **single source of truth** for how every auto-scaled instance will be created. Understanding what each field controls is critical because any mistake in the Launch Template gets replicated to every instance the ASG launches. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**AMI selection** — You select your own AMI from "My AMIs" (not the AWS marketplace). This is the image you just created from app01. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Instance type** — Determines the compute capacity (CPU, memory) of each launched instance. In this project, t2.micro or t3.micro is used because they are free tier eligible. In production, you would choose an instance type that matches your application's resource needs. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Key pair** — The SSH key pair (vprofile-prod-key) that will be associated with every launched instance. This ensures you can SSH into any auto-scaled instance for troubleshooting or inspection. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Security group** — The app security group, which (as covered in the project's earlier lectures) only allows traffic on port 8080 from the load balancer security group. Every instance launched by the ASG inherits this security posture. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Resource tags** — Tags are applied to both instances and their EBS volumes. The video uses a Name tag of "vprofile-app" (without a number suffix like 01 or 02, because ASG-managed instances are interchangeable — they don't need unique names) and a Project tag of "vprofile". Tagging volumes is explicitly highlighted — if you don't check the "volumes" checkbox, only the instance gets tagged, and the attached storage remains untagged (making cost tracking and resource management harder). [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**IAM Instance Profile** — This is where you attach an IAM role to every launched instance. The video notes that it's not strictly necessary for this stage of the project, but emphasizes that **in real-world production, you will very frequently need to attach IAM roles to instances** — for example, to grant S3 access, CloudWatch logging permissions, or secrets retrieval. If you need a role, it **must** be specified in the Launch Template; otherwise, auto-scaled instances will launch without the role, even if the original app01 had it. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

⚠️ **Expert Note:**
The Launch Template is the most critical configuration artifact in the entire ASG setup. A misconfigured security group, a wrong AMI, a missing IAM role — any of these errors in the Launch Template means every single instance the ASG launches will be broken. In production, Launch Templates should be version-controlled, tested with a single manual launch before being connected to an ASG, and updated through new versions (not in-place edits) to maintain rollback capability. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.4 — Auto Scaling Group: Capacity Model (Min / Desired / Max)

The ASG's capacity model is defined by three numbers that form a bounded range: **minimum size**, **desired capacity**, and **maximum size**. Understanding how these three interact is essential. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Minimum size** is the absolute floor. The ASG will never terminate instances below this count, even during aggressive scale-in events. If minimum is set to 2, you are guaranteed to always have at least 2 instances running. This protects against the ASG scaling down to zero and leaving your application unavailable. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Desired capacity** is the number of instances the ASG actively tries to maintain under normal conditions. If an instance is terminated (manually, by a health check failure, or by a scale-in event), the ASG will launch a replacement to return to the desired count. In the video, desired capacity is set to 1. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Maximum size** is the absolute ceiling. Even during extreme scale-out events, the ASG will never launch more instances than this number. In the video, maximum is set to 4. This protects against runaway scaling (and runaway costs) during unexpected traffic spikes or metric anomalies. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The relationship: **minimum ≤ desired ≤ maximum**. During normal operation, the ASG maintains the desired count. Scaling policies can push the actual count above desired (toward maximum) or below desired (toward minimum), but never outside the min-max boundary. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

In the video's configuration: min=1, desired=1, max=4. This means: always have at least 1 instance, try to keep 1 running normally, but allow up to 4 if load demands it. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.5 — Scaling Policies: How the ASG Decides When to Scale

The ASG needs a decision mechanism to determine when to add or remove instances. The video uses **Target Tracking Scaling Policy**, which is the simplest and most common approach. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

Target Tracking works like a thermostat: you specify a metric and a target value. The ASG continuously monitors the metric and adjusts the instance count to keep the metric close to the target. If the metric rises above the target, instances are added. If it drops below, instances are removed. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The available metrics mentioned are:

* **CPU Utilization** — the average CPU usage across all instances in the ASG. The video calls this "the best bet" and the most commonly used metric. The target is set to 50% — if average CPU exceeds 50%, scale out; if it drops below 50%, scale in. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)
* **Network Out** — the amount of outbound network traffic. The video notes this is "very popular for web applications" because web servers that are under heavy load tend to send more data out to clients. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

A critical detail: the metric is computed as the **average across all instances** in the ASG, not per individual instance. This means one instance at 90% CPU and another at 10% CPU would average to 50% — which might not trigger scaling even though one instance is overloaded. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Disable Scale-In option** — The video mentions a checkbox that allows you to disable scale-in entirely. If checked, the ASG will only scale out (add instances) but will never automatically scale in (remove instances). You would then manually decide when to reduce capacity. This is useful in scenarios where you want to handle scale-down cautiously — for example, if you're unsure whether a traffic drop is temporary or sustained. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.6 — Health Checks: Instance-Level vs. Load Balancer-Level

The ASG can use two types of health checks to determine whether an instance is healthy, and the distinction between them is operationally significant. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**EC2 Instance Health Check (default)** — This only checks whether the EC2 instance itself is running at the infrastructure level. If the instance is in a "running" state (not stopped, terminated, or impaired at the hardware/hypervisor level), it is considered healthy. This check does **not** know or care whether the application (Tomcat) running inside the instance is actually working. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Elastic Load Balancing (ELB) Health Check (optional, must be explicitly enabled)** — When this is turned on, the ASG also considers the health check results from the load balancer's target group. The target group's health check actively probes the instance on a specific port and path (e.g., HTTP request to port 8080 on a health check URL). If the Tomcat service crashes, stops responding, or returns errors, the target group marks the instance as unhealthy. With ELB health check enabled in the ASG, this unhealthy status triggers the ASG to **terminate the broken instance and launch a fresh replacement**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

Without ELB health check enabled, a scenario is possible where the EC2 instance is running (infrastructure is fine) but Tomcat has crashed. The default EC2 health check would report the instance as healthy because the VM is still running. The load balancer would stop sending traffic to it (because the target group health check failed), but the ASG would not replace it — leaving you with a dead instance consuming resources and reducing your effective capacity. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The video explicitly recommends turning on ELB health check: "We don't want any unhealthy instance in our auto scaling group." [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

⚠️ **Expert Note:**
In production, always enable ELB health checks for any ASG behind a load balancer. The default EC2-only health check is insufficient for application-level reliability. However, be cautious with health check grace periods — if your application takes a long time to start (e.g., JVM warmup, database connection pool initialization), the health check might fail before the instance is ready, causing the ASG to terminate it in a loop. Configure the health check grace period to be longer than your application's startup time. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.7 — Scale-In Protection: Preserving Instances for Troubleshooting

Scale-In Protection is an option within the ASG that changes what happens when an instance is deemed unhealthy. Without it, the ASG terminates the unhealthy instance and replaces it. With scale-in protection enabled, the ASG **does not terminate** the unhealthy instance. Instead, it stops routing traffic to it, launches a new healthy instance, and routes traffic to the new one — but the old unhealthy instance remains alive and accessible. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The purpose is **troubleshooting**. When an instance becomes unhealthy, the immediate question is: *why?* If the ASG terminates it before you can investigate, you lose the evidence — logs, process state, memory state, configuration drift, whatever caused the failure. Scale-in protection preserves the "crime scene" so you can SSH into the unhealthy instance, inspect logs, check processes, and find the root cause. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The video leaves this unchecked for the project because the vProfile application is simple and root-cause investigation is not the focus. But the instructor explicitly explains the mechanism and its purpose, signaling that it matters in real operations. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.8 — ASG and Load Balancer Integration: Target Group Registration

When the ASG is connected to a load balancer, every new instance launched by the ASG is **automatically registered** with the load balancer's target group. This is the mechanism that makes scaling seamless from the user's perspective — users continue hitting the same load balancer URL, and the load balancer automatically distributes traffic to whatever instances exist in the target group at any given moment. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The integration is configured during ASG creation by selecting "Attach to an existing load balancer" and choosing the target group. The video notes a distinction: if you have a **Classic Load Balancer**, you select the load balancer directly. If you have an **Application Load Balancer** (which this project uses), you select the **target group** instead, because ALBs route traffic through target groups, not directly to instances. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

This integration also means that when the ASG scales in and terminates an instance, the instance is automatically **deregistered** from the target group first. The load balancer stops sending new requests to it, existing connections drain, and then the instance is terminated. This ensures no user requests are dropped during scale-in. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.9 — Network Configuration: Availability Zones

During ASG creation, you select which **availability zones** the ASG can launch instances into. In the video, all available availability zones are selected. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

This is an availability decision. If you select only one availability zone and that zone experiences an outage, your entire ASG fleet goes down. By selecting multiple (or all) zones, the ASG spreads instances across zones, providing resilience against zone-level failures. The ASG also attempts to balance the number of instances evenly across selected zones. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The video also mentions you can **restrict** to specific zones if needed — for example, if your backend services (database) are in a specific zone and you want to minimize cross-zone latency. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.10 — Stickiness (Session Affinity): Why and How

Stickiness is a load balancer target group setting (not an ASG setting) that ensures a user who connects to a specific instance continues to be routed to **that same instance** on subsequent requests. It is configured in the target group's attributes, not in the ASG itself. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**How it works:** When a user first accesses the application, the load balancer routes them to one of the available instances (say, app01). The load balancer then injects a **cookie** into the user's browser. On subsequent requests, the browser sends this cookie back, and the load balancer reads it to route the request to the same instance that handled the first request. You can also configure a **stickiness duration** — how long this affinity persists (e.g., one day). [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Why it's needed for vProfile:** The vProfile application stores authentication state locally on the instance. If a user logs in on app01 and is then routed to app02 on the next request, app02 has no knowledge of the authentication — the user appears logged out and must log in again. Stickiness prevents this by keeping the user on the same instance. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The video is explicit that this is **application-specific** behavior. Not all applications need stickiness. Applications that store session state in a shared external store (like a Redis cluster or a database) can handle requests on any instance without stickiness. The vProfile application, being simple, does not have this external session management, so stickiness is required. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

⚠️ **Expert Note:**
Stickiness introduces a tradeoff: it can cause **uneven load distribution**. If most sticky sessions land on one instance, that instance becomes overloaded while others are idle. In production, the better solution is to externalize session state (e.g., to Memcache, Redis, or a database) so that any instance can serve any request. Stickiness is a workaround for applications that cannot do this. The video acknowledges this implicitly by calling vProfile "a pretty simple application" that "cannot handle authentication like this." [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.11 — The Handoff: From Manually Managed to ASG-Managed

The final conceptual step in the video is the **transition from manual instance management to ASG management**. Once the ASG is running and has launched its own instance (cloned from the AMI), the original app01 instance is no longer needed. The video demonstrates: (1) deregistering app01 from the target group, and (2) terminating app01. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

This is the operational handoff moment — from this point forward, the ASG owns the lifecycle of the application instances. You do not manually launch, configure, or terminate app instances anymore. The ASG handles all of that based on the Launch Template, scaling policies, and health checks. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

The video adds an important safety note: "Don't worry, we also have the AMI of the instance. So even if something goes wrong, we can launch the instance once again." The AMI serves as a **recovery artifact** — a snapshot you can always fall back to if the ASG configuration is wrong or something breaks. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## 1.12 — SNS Notifications for ASG Events

The ASG can be configured to send **notifications** via Amazon SNS (Simple Notification Service) when specific lifecycle events occur. The video mentions four event types: **launch**, **terminate**, **fail to launch**, and **fail to terminate**. These notifications are sent to an SNS topic (configured in a prerequisite lecture) which forwards them to an email address. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

This gives you operational visibility into what the ASG is doing — especially important for understanding scaling behavior, catching failures, and auditing instance lifecycle in production. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating an Auto Scaling Group for the vProfile Tomcat application instance (app01) so that the application tier scales automatically — launching new instances when demand increases and removing them when demand drops. The final outcome: the ASG owns and manages all application instances, the original manually-created app01 is terminated, and the load balancer seamlessly routes traffic to ASG-managed instances. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Execution Flow Overview

```
Step 1: Create AMI from app01
Step 2: Create Launch Template (referencing the AMI)
Step 3: Create Auto Scaling Group (referencing the Launch Template)
Step 4: Configure stickiness on the Target Group
Step 5: Deregister and terminate the original app01
Step 6: Verify
```

***

### Step 1: Create AMI from app01

**What we are doing:** Capturing a complete image of the running app01 instance.

**Why:** The ASG will use this image to launch identical clones of app01 whenever it needs to scale out.

**Execution:**

1. Go to the **EC2 Console → Instances**.
2. **Select the app01 instance** — make sure you select the correct instance.
3. Click **Actions → Image and Templates → Create Image**.
4. Set the AMI name: `vprofile-las-app-ami`
5. Set the description: `vprofile-las-app-ami` (same as the name).
6. Click **Create Image**.

**What happens internally:** AWS creates a snapshot of the instance's root EBS volume (and any additional volumes). This snapshot is packaged as an AMI. The AMI enters a **"pending"** state while the snapshot is being created. It will transition to **"available"** once the snapshot is complete. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**How to verify:** Click the AMI link that appears after creation, or navigate to **EC2 → Images → AMIs**. Check the state column — it should eventually show "available." [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Common mistake:** Not waiting for the AMI to become "available" before trying to launch instances from it. The AMI name appears in selection lists even while pending, but instances cannot be launched from a pending AMI.

**Connection to flow:** This AMI will be referenced in the Launch Template (Step 2). While the AMI is being created (pending state), we proceed to create the Launch Template in parallel to save time. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

### Step 2: Create Launch Template

**What we are doing:** Defining the blueprint for how every auto-scaled instance will be launched.

**Why:** The ASG reads this template every time it needs to launch a new instance. Every setting here is applied to every instance.

**Execution:**

1. Navigate to **EC2 → Instances → Launch Templates**.

2. Click **Create Launch Template**.

3. **Name:** `vprofile-las-app-LT`

4. **AMI:** Scroll down → select **My AMIs** → find and select `vprofile-las-app-ami`. (It may still be in pending state, but you can select it by name.) [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

5. **Instance type:** `t2.micro` or `t3.micro` — whichever is free tier eligible.

6. **Key pair:** `vprofile-prod-key` — the SSH key pair created earlier in the project.

7. **Network settings → Security Group:** Select **existing security group** → choose the **app security group**. This ensures every launched instance inherits the correct firewall rules (port 8080 from LB SG only). [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

8. **Resource tags:**
   * Click **Add new tag**.
   * Tag 1: Key = `Name`, Value = `vprofile-app`. **Do not** use a numbered suffix (01, 02) because ASG instances are interchangeable. Check both **Instances** and **Volumes**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)
   * Tag 2: Key = `Project`, Value = `vprofile`. Check **Volumes** here as well.
   **Important:** Always check the **Volumes** checkbox when adding tags. If you only tag instances, the attached EBS volumes remain untagged, making cost allocation and resource tracking incomplete. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

9. **Advanced Details → IAM Instance Profile:**
   * If you need instances to have an IAM role (e.g., for S3 access, CloudWatch, etc.), select the role here.
   * The video notes: "It's really not necessary now because in CI/CD, in Jenkins, we'll see how we can automatically deploy the artifact." However, the instructor emphasizes: "In real time, there may be cases where you need to add roles to your instances. Many times, many, many times." [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)
   * **If you need a role and forget to add it here, every auto-scaled instance launches without it.** The only fix is to create a new Launch Template version with the role and update the ASG to use it.

10. Skip remaining advanced settings and click **Create Launch Template**.

**How to verify:** You should see "Launch template created successfully." Navigate to Launch Templates and confirm `vprofile-las-app-LT` appears with the correct settings. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Connection to flow:** This Launch Template is referenced in Step 3 when creating the ASG.

***

### Step 3: Create Auto Scaling Group

**What we are doing:** Creating the ASG that will manage the Tomcat application tier — controlling instance count based on demand.

**Execution:**

1. Navigate to **EC2 → Auto Scaling Groups**.
2. Click **Create Auto Scaling Group**.
3. **Name:** `vprofile-las-app-asg`
4. **Launch Template:** Select `vprofile-las-app-LT`. The ASG will use this template for every instance it launches. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)
5. Click **Next**.

**Network Configuration:**
6\. **VPC:** Keep the default VPC.
7\. **Availability Zones:** Select **all available** availability zones. This spreads instances across zones for fault tolerance. (You can restrict to specific zones if needed.) &#x20;
8\. Click **Next**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Load Balancer Integration:**
9\. Select **Attach to an existing load balancer**.
10\. Since we have an **Application Load Balancer** (not Classic), select **Choose from your load balancer target groups**.
11\. Select the **vprofile app target group**. Every instance launched by this ASG will be automatically registered in this target group and receive traffic from the ALB. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Health Check Configuration:**
12\. **Turn on Elastic Load Balancing health checks.** This is critical — without it, the ASG only checks if the EC2 VM is running, not if Tomcat is actually healthy. With ELB health check enabled, if Tomcat crashes, the target group marks the instance as unhealthy, and the ASG terminates and replaces it.&#x20;
13\. Click **Next**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Group Size:**
14\. **Desired capacity:** `1`
15\. **Minimum:** `1`
16\. **Maximum:** `4`

This means: always keep at least 1 instance, normally maintain 1, but allow scaling up to 4 during high load. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Scaling Policy:**
17\. **Scaling policy type:** Target Tracking Scaling Policy.
18\. **Metric:** CPU Utilization (the video calls this "the best bet").
19\. **Target value:** `50` — if average CPU across all ASG instances exceeds 50%, scale out; if below 50%, scale in. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Optional: Disable Scale-In:** There is a checkbox to disable automatic scale-in. If checked, the ASG only adds instances but never removes them automatically. Left unchecked in this project. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Scale-In Protection:**
20\. **Instance scale-in protection:** Left unchecked. If enabled, unhealthy instances would be preserved (not terminated) for troubleshooting — traffic is redirected to new instances while the unhealthy one stays alive for investigation.&#x20;
21\. Click **Next**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Notifications:**
22\. Click **Add notification**.
23\. Select the **SNS topic** configured in the prerequisite lecture.
24\. Select all four events: **Launch**, **Terminate**, **Fail to launch**, **Fail to terminate**.
25\. Click **Next**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

26. Click **Create Auto Scaling Group**.

**What happens internally:** The ASG immediately begins working toward the desired capacity. Since desired=1 and no instances are currently managed by the ASG, it launches one new EC2 instance using the Launch Template (which references the AMI). This instance is automatically registered in the target group. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**How to verify:** Go to **Target Groups → select vprofile app target group → Targets tab**. You should see the newly launched instance with status **"healthy"**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

### Step 4: Configure Stickiness on the Target Group

**What we are doing:** Enabling session stickiness so users stay connected to the same instance across requests.

**Why:** The vProfile application stores authentication state locally. Without stickiness, a user authenticated on one instance gets routed to a different instance on the next request and appears logged out.

**Execution:**

1. Navigate to **EC2 → Target Groups**.
2. Select the **vprofile app target group**.
3. Go to **Attributes → Edit**.
4. Find the **Stickiness** option and **turn it on**.
5. Configure the stickiness duration (e.g., 1 day).
6. Click **Save Changes**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**How it works operationally:** The ALB injects a cookie into the user's browser on the first request. On subsequent requests, the browser sends the cookie back, and the ALB reads it to route the request to the same backend instance.

**Important context:** This is application-specific. The video is explicit: "This is very specific to vprofile application. Some other application where you work may also have this one and you can turn on stickiness in that case." Applications with externalized session storage (Redis, database-backed sessions) do not need stickiness. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Connection to flow:** This must be configured before users start accessing the application through the ASG-managed instances, especially if more than one instance is running.

***

### Step 5: Deregister and Terminate the Original app01

**What we are doing:** Removing the original manually-created app01 instance and letting the ASG take full control.

**Why:** The ASG has launched its own instance (cloned from app01's AMI). Having both the original app01 and the ASG-managed instance in the target group creates confusion — manual instances outside the ASG's control undermine the purpose of auto-scaling.

**Execution:**

1. Go to **Target Groups → vprofile app → Targets tab**.
2. Select the original **app01 instance** (not the ASG-launched one).
3. Click **Deregister**. The instance enters a **"draining"** state — the load balancer stops sending new requests to it and allows existing connections to complete. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)
4. Wait for the instance to fully deregister (draining → removed from target group).
5. Go to **EC2 → Instances**.
6. Select the original **app01** instance.
7. Click **Instance State → Terminate**. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**Safety note from the video:** "Don't worry, we also have the AMI of the instance. So even if something goes wrong, we can launch the instance once again." The AMI is your safety net — if the ASG setup has issues, you can always launch a new instance from the AMI manually. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

**How to verify:** After deregistration completes and the old instance is terminated, check the Target Group — only ASG-managed instance(s) should remain, in "healthy" status. Access the application URL and confirm it works. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

### Step 6: Verify

**What we are doing:** End-to-end verification that the ASG-managed setup works correctly.

**Checks to perform:**

* Target Group shows only ASG-managed instance(s) in "healthy" state.
* The application URL loads correctly in the browser.
* Login/authentication works (stickiness functioning).
* The ASG shows the correct desired/min/max values in the console.
* SNS notifications were received for the instance launch event.

**The video notes:** "We'll validate all that and we'll summarize it in the last lecture." The instructor suggests taking a 5-10 minute break to allow deregistration and DNS propagation to complete before final validation. [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
COMPONENT: Auto Scaling Group for vProfile Tomcat app tier
PURPOSE:   Elastic instance management — auto scale-out/scale-in
SCOPE:     Application tier only (not backend services)
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Dependency Chain (Strict Order)

```
app01 (running instance)
   │
   ▼ (snapshot)
AMI: vprofile-las-app-ami
   │
   ▼ (referenced by)
Launch Template: vprofile-las-app-LT
   │  ├── AMI
   │  ├── Instance type (t2/t3.micro)
   │  ├── Key pair (vprofile-prod-key)
   │  ├── Security Group (app SG)
   │  ├── Tags (Name: vprofile-app, Project: vprofile) → instances + volumes
   │  └── IAM Instance Profile (optional but common in production)
   │
   ▼ (referenced by)
Auto Scaling Group: vprofile-las-app-asg
   ├── Capacity: min=1, desired=1, max=4
   ├── AZs: all selected
   ├── Target Group: vprofile app TG (ALB integration)
   ├── Health Check: EC2 + ELB (both)
   ├── Scaling Policy: Target Tracking → CPU avg > 50% → scale out
   ├── Scale-in protection: OFF
   └── Notifications: SNS → launch, terminate, fail-to-launch, fail-to-terminate
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## ASG Capacity Model

```
         ┌─────── max (4) ─── ceiling, never exceeded
         │
scale-out│
         │
    ─────┼─── desired (1) ── actively maintained
         │
scale-in │
         │
         └─────── min (1) ─── floor, never breached

TRIGGER: avg CPU utilization across all ASG instances vs. 50% threshold
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Health Check: Two Levels

```
Level 1 (Default): EC2 Instance Check
  └── Is the VM running?     → YES = healthy
                              → NO  = unhealthy

Level 2 (Must enable): ELB Health Check
  └── Is the application responding on the expected port/path?
                              → YES = healthy
                              → NO  = unhealthy → ASG terminates + replaces

WITHOUT Level 2: Instance running + Tomcat crashed = ASG thinks healthy ❌
WITH Level 2:    Instance running + Tomcat crashed = ASG detects, replaces ✅
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Scale-In Protection (Decision Tree)

```
Instance becomes unhealthy:

  Scale-in protection OFF (default):
    └── ASG terminates instance → launches replacement
        (Evidence lost, fast recovery)

  Scale-in protection ON:
    └── ASG keeps instance alive (no traffic)
        └── Launches new instance (gets traffic)
        └── You SSH into unhealthy instance → troubleshoot → find root cause
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Load Balancer Integration

```
ASG ──── attached to ──── Target Group (ALB)

Scale out: ASG launches instance → auto-registered in TG → receives traffic
Scale in:  Instance drains → deregistered from TG → terminated

Classic LB: select LB directly
Application LB: select Target Group (not LB)
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Stickiness (Session Affinity)

```
PROBLEM: vProfile stores auth state locally per instance
         User on app01 → routed to app02 → appears logged out

SOLUTION: Target Group → Attributes → Stickiness ON

MECHANISM:
  First request → ALB routes to app01 → injects cookie in browser
  Next request  → browser sends cookie → ALB reads → routes to app01 again

SCOPE: Application-specific workaround (not needed if sessions are externalized)
TRADEOFF: Can cause uneven load distribution
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Operational Handoff Sequence

```
BEFORE:  app01 (manual) serves traffic via Target Group

TRANSITION:
  1. ASG created → launches clone instance from AMI
  2. Clone registers in Target Group → healthy
  3. Deregister app01 from Target Group → draining → removed
  4. Terminate app01

AFTER:   ASG owns all app instances. Manual management ends.
SAFETY:  AMI preserved → can always relaunch manually if ASG breaks
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Notification Events (SNS)

```
ASG → SNS Topic → Email

Events monitored:
  ├── Instance Launch
  ├── Instance Terminate
  ├── Fail to Launch
  └── Fail to Terminate
```

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## Reusable Engineering Patterns

| Pattern                    | Manifestation                                                 |
| -------------------------- | ------------------------------------------------------------- |
| **Golden Image (AMI)**     | Capture working state → replicate infinitely via ASG          |
| **Blueprint/Template**     | Launch Template = single source of truth for instance config  |
| **Bounded Elasticity**     | min/desired/max = scale within guardrails, never runaway      |
| **Thermostat Control**     | Target Tracking = metric vs. threshold → auto-adjust          |
| **Two-Layer Health Check** | Infra health (EC2) + App health (ELB) = complete detection    |
| **Preserve-for-Forensics** | Scale-in protection = keep broken instances for investigation |
| **Graceful Drain**         | Deregister before terminate → no dropped connections          |
| **Ownership Handoff**      | Manual → Automated (ASG replaces human instance management)   |
| **Cookie-Based Affinity**  | Stickiness = route user to same backend via injected cookie   |
| **Safety Snapshot**        | AMI = rollback artifact if automation fails                   |

 [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

## One-Line System Reconstruction

> **An ASG manages the vProfile Tomcat tier by cloning app01's AMI via a Launch Template, auto-registering instances in the ALB target group, scaling between 1–4 instances based on 50% CPU threshold, with ELB health checks ensuring only healthy instances serve traffic, and stickiness maintaining user session affinity.** [\[138. Autos...ling Group \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/138.%20Autoscaling%20Group.txt)

***

This completes the full reconstruction of the Auto Scaling Group lecture. It builds directly on top of the Introduction lecture material we covered previously — the ASG is the final piece that transforms the static Lift & Shift deployment into an elastic, self-managing production setup. Let me know if you'd like any section expanded or adjusted! 🚀
