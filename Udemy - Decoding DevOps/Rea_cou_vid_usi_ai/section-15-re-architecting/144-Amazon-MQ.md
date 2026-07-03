# 🎓 Deep Learning Material: Amazon MQ — Creating a Managed RabbitMQ Broker for the vProfile Backend

**Source:** Video lecture on creating an Amazon MQ RabbitMQ instance (from [144-amazon-mq.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt?EntityRepresentationId=515fcc57-5d7e-4425-a02c-5f7af47ca378) caption file) [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Video Context:** This lecture is part of a larger project where the instructor is re-architecting the vProfile application's backend services from manually managed EC2 instances to **AWS-managed services**. Two backend services have already been created: **Amazon RDS** (MySQL database) and **ElastiCache** (Memcached). This lecture creates the third and final backend service: **Amazon MQ** (RabbitMQ message broker). The lecture is primarily operational — the conceptual weight is in understanding Amazon MQ's place in the managed-services architecture, the configuration decisions made, and how they connect to the broader project.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Amazon MQ: A Fully Managed Message Broker Service

Amazon MQ is AWS's **fully managed message broker service**. In this project, it is used to provide a **RabbitMQ** instance — a message queuing system that the vProfile application uses for asynchronous communication between components. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

The key architectural property the instructor highlights is that Amazon MQ is **"fully managed"** — meaning you don't need to handle the infrastructure plumbing that other managed services sometimes require. Specifically, the instructor contrasts it with Amazon RDS, where you needed to create **subnet groups** as part of the setup. With Amazon MQ, you don't: *"You don't need to create subnet groups and all those things."* You simply create the broker, configure it, and it works within your existing VPC and subnet infrastructure. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

Amazon MQ supports multiple broker engines. The two visible in the console are **RabbitMQ** and (implied) **ActiveMQ**. For this project, the instructor selects **RabbitMQ** because that's what the vProfile application is designed to communicate with. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

> 🔍 **Deep Dive**
>
> The re-architecture pattern across this project section is consistent: every manually managed backend service is being replaced by an AWS-managed equivalent. The database moved from a self-managed MySQL on EC2 to **Amazon RDS**. The caching layer moved from self-managed Memcached on EC2 to **ElastiCache**. The message broker moves from self-managed RabbitMQ on EC2 to **Amazon MQ**. In each case, the tradeoff is the same: you give up OS-level control in exchange for AWS handling provisioning, patching, backups, and availability. The application code doesn't change — only the infrastructure underneath it changes.

***

## 1.2 — Deployment Type: Single-Instance vs. Cluster

Amazon MQ offers two deployment options: **Single-instance broker** and **Cluster deployment**. A cluster provides high availability and fault tolerance — multiple broker nodes working together so that if one fails, the others continue serving. The instructor explicitly selects **single-instance** because *"this is for learning purpose."* He notes: *"In real time, you might need a cluster deployment for production workloads."* [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

This is a recurring decision pattern across the course: for learning and development, use the smallest/cheapest configuration; for production, scale up to the resilient option. The architecture supports both — the application connects to the broker endpoint regardless of whether it's a single node or a cluster behind that endpoint.

***

## 1.3 — Broker Engine Version: Stability Over Recency

The instructor makes a deliberate version choice: select engine version **3.13**, not the latest 4.x. The reasoning: *"This is more a stable, more matured engine version and it works with vprofile application also."* [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

This reflects an important operational principle: **application compatibility drives version selection, not recency.** The vProfile application's `awsrefactor` branch is tested and known to work with RabbitMQ 3.x. Choosing 4.x might introduce breaking changes in the broker protocol or behavior. In production, you always validate application compatibility before upgrading broker/database/cache engine versions.

***

## 1.4 — Access Type: Private Access Within the VPC

The instructor selects **Private access** for the broker. The vProfile application instances and the RabbitMQ broker are all within the same AWS network (the default VPC). The application accesses RabbitMQ **internally** — there is no need for the broker to be accessible from the public internet. *"Our vProfile application is going to internally access the RabbitMQ service within AWS internal network, the default VPC, so use case is definitely Private access."* [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

This is architecturally correct for a backend service. Message brokers, databases, and caches should **never** be publicly accessible. They serve internal application components, not end users. Public access would create an unnecessary attack surface.

***

## 1.5 — Data Encryption: Mandatory and Application-Aware

The instructor notes that there is **no option to disable encryption** for the RabbitMQ broker in Amazon MQ. Unlike some older AWS services where encryption was optional, Amazon MQ enforces it. The instructor confirms this works because: *"Our vProfile source code, which is an awsrefactor branch, is customized to encrypt the traffic for RabbitMQ, so this will work."* [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

This is an important compatibility detail: if the application code was **not** configured to handle encrypted connections to RabbitMQ, the mandatory encryption would cause connection failures. The `awsrefactor` branch of the source code has been specifically modified to support this — it's not the same configuration as the original vProfile code that connected to a plain, unencrypted RabbitMQ on EC2. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

## 1.6 — Security Group: Reusing the Backend Security Group

The broker is placed into the **vprofile-backend-sg** security group — the same security group used by the other backend services (RDS, ElastiCache). This is a deliberate architectural choice: all backend services share the same security group, which has rules allowing traffic from the application tier. This simplifies security management and follows the **tiered security group pattern** seen in earlier lectures (application SG → backend SG). [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

## 1.7 — The Three Backend Services: Completing the Managed Architecture

With Amazon MQ created, all three backend services for the vProfile re-architecture are now provisioned: [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

1. **Amazon RDS** — MySQL database (created in a previous lecture)
2. **ElastiCache** — Memcached caching layer (created in a previous lecture)
3. **Amazon MQ** — RabbitMQ message broker (created in this lecture)

The instructor notes that one more step remains before the application can function: *"We need to initialize the database with our SQL file, db\_backup.sql file. That's what we're going to do in the next lecture."* The database exists but is empty — it needs schema and data loaded. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a **managed RabbitMQ message broker** using Amazon MQ — the third and final backend service in the vProfile re-architecture project. The final outcome: a running RabbitMQ broker accessible privately within the VPC, with the correct engine version and security group, ready for the vProfile application to connect to. After this, the remaining step is database initialization (next lecture).

***

## Step 1: Navigate to Amazon MQ

1. In AWS Console, search for **Amazon MQ** (or just "RabbitMQ") [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

   ⚠️ **Be careful:** *"Make sure it's Amazon MQ and not Amazon Q. That is a different AI tool."* Amazon Q is the AI assistant; Amazon MQ is the message broker service. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

2. Click **Create brokers** → **Get started** [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

## Step 2: Select Broker Engine and Deployment Type

1. **Broker engine:** Select **RabbitMQ** (not ActiveMQ) [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)
2. Click **Next**
3. **Deployment mode:** Select **Single-instance broker** [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)
   * Cluster deployment is for production HA; single-instance is sufficient for learning
4. Click **Next** [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

## Step 3: Configure Broker Settings

| Setting                  | Value                                                  | Reasoning                                                                      |
| ------------------------ | ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **Broker name**          | `vprofile-rearch-rabbitmq`                             | Descriptive project naming convention                                          |
| **Broker instance type** | 1 CPU, 4GB (minimum)                                   | No 1GB option available; smallest possible. Delete after use to avoid charges. |
| **Username**             | `rabbit`                                               | Login credential for broker access                                             |
| **Password**             | `BlueBunny980` (or any 12+ char, mixed case + numbers) | Must save this — needed for application config                                 |

 [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Critical:** Save the password immediately. The instructor saves it in a sticky note: *"whatever password you're giving over here, make sure you save it somewhere."* [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

## Step 4: Configure Additional Settings

Click **Additional settings** to expand: [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Broker engine version:** Select **3.13** (any 3.x version). [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

* Do NOT select 4.x: *"Don't go with 4.2, just go with three dot. Any three is fine."*
* Reason: 3.x is stable, mature, and compatible with the vProfile application code

**CloudWatch Logs monitoring:** [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

* For this exercise: not checked (optional)
* For production: *"In real time, you will need logs, so make sure in real time, you put this check mark on."*

**Access type:** Select **Private access** [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

* The application connects to RabbitMQ internally within the VPC
* Never expose message brokers publicly

**VPC and Subnet:** Use **default VPC** and **default subnet** (should be pre-selected) [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Security group:** Select **existing security group** → choose **vprofile-backend-sg** [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

* This is the same backend SG used by RDS and ElastiCache
* Ensures the application tier can reach this broker through the existing SG rules

**Data encryption:** No option to disable — **encryption is mandatory**. This is compatible with the `awsrefactor` branch of the source code, which is configured for encrypted RabbitMQ connections. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Maintenance:** No preferences (leave default) [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Tags:** Add a Name tag: `vprofile-rearch-rabbitmq` [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

## Step 5: Review and Create

1. Click **Next** to reach the review page [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)
2. **Verify:**
   * RabbitMQ engine version is 3.x (not 4.x)
   * Password is saved
   * Security group is `vprofile-backend-sg`
   * Access type is Private
3. Click **Create broker** [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Expected state:** Broker shows as **"Creating"** — this takes several minutes. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

**Connection to system flow:** With this broker created, all three backend managed services are provisioned. The next step (next lecture) is to initialize the RDS MySQL database with the `db_backup.sql` schema file before the application can function. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

> ⚠️ **Expert Note**
>
> The minimum instance type for Amazon MQ RabbitMQ (1 CPU, 4GB) is significantly more expensive than a small EC2 instance running self-managed RabbitMQ. For learning, always **delete the broker promptly** after completing the exercise. The instructor acknowledges this: *"don't worry, we're going to anyways delete it once we are done."* In production, the cost is justified by the operational overhead you avoid (patching, monitoring, failover management). [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Where This Fits in the Project

```
vProfile Re-Architecture: EC2-managed → AWS-managed backend

LECTURE SEQUENCE:
  1. ✅ Amazon RDS        → MySQL database (managed)
  2. ✅ ElastiCache       → Memcached (managed)
  3. ✅ Amazon MQ         → RabbitMQ (managed)     ← THIS LECTURE
  4. ⬜ DB initialization → load db_backup.sql     ← NEXT LECTURE
  5. ⬜ Application deployment + Load Balancer      ← FUTURE
```

***

## 🔷 Amazon MQ Configuration Map

```
BROKER SETTINGS:
  ├── Engine:         RabbitMQ (not ActiveMQ)
  ├── Deployment:     Single-instance (learning) | Cluster (production)
  ├── Name:           vprofile-rearch-rabbitmq
  ├── Instance type:  1 CPU / 4GB (minimum available)
  ├── Username:       rabbit
  ├── Password:       <saved in sticky note> (12+ chars, mixed case + numbers)
  ├── Engine version: 3.13 (NOT 4.x — stability + app compatibility)
  ├── Logs:           Off for learning | ON for production (CloudWatch)
  ├── Access:         PRIVATE (internal VPC only, never public)
  ├── VPC/Subnet:     Default VPC, default subnet
  ├── Security group: vprofile-backend-sg (shared with RDS + ElastiCache)
  ├── Encryption:     MANDATORY (no disable option)
  │                   Source code (awsrefactor branch) handles encrypted connections
  └── Tag:            Name = vprofile-rearch-rabbitmq
```

***

## 🔷 Three Backend Services (Complete View)

```
SERVICE          AWS MANAGED BY      SECURITY GROUP         ACCESS TYPE
────────────     ──────────────      ──────────────         ───────────
MySQL DB         Amazon RDS          vprofile-backend-sg    Private
Memcached        ElastiCache         vprofile-backend-sg    Private
RabbitMQ         Amazon MQ           vprofile-backend-sg    Private

ALL share the same backend SG → application SG has rules to reach backend SG
ALL are private → no public internet exposure
ALL are fully managed → AWS handles patching, availability, backups
```

***

## 🔷 Key Decision Points and Why

```
DECISION                          WHY
────────────────────────          ─────────────────────────────────
Single-instance (not cluster)     Learning exercise, cost savings
Engine version 3.13 (not 4.x)    Stability + vProfile app compatibility
Private access (not public)       Backend service → internal only
vprofile-backend-sg               Shared SG for all backend services
Encryption stays on (mandatory)   awsrefactor branch handles encrypted traffic
Min instance type (1CPU/4GB)      Smallest available; delete after exercise
```

***

## 🔷 Amazon MQ vs. Other Managed Services (Setup Simplicity)

```
Amazon RDS:      Needs subnet group creation + parameter groups
ElastiCache:     Needs subnet group creation + parameter groups
Amazon MQ:       NO subnet group needed → "fully managed, just click create"
                 Simpler setup, fewer infrastructure prerequisites
```

***

## 🔷 Compatibility Chain (Critical for Application Success)

```
Source code branch: awsrefactor
  │
  ├── Configured for encrypted RabbitMQ connections ← matches mandatory encryption
  ├── Connects to RabbitMQ 3.x protocol            ← matches engine version 3.13
  ├── Uses credentials: rabbit / <password>         ← must match broker config
  └── Connects via private VPC endpoint             ← matches private access type

ANY MISMATCH = application connection failure at runtime
```

***

## 🔷 Common Pitfalls

```
"Amazon Q" selected instead of "Amazon MQ"
  → Wrong service entirely (AI tool vs message broker)

Engine version 4.x selected
  → Potential incompatibility with vProfile application code

Password not saved
  → Cannot configure application to connect; must recreate credentials

Public access selected
  → Security risk; backend services should never be publicly exposed

Encryption disabled (not possible here, but conceptually)
  → Would mismatch with awsrefactor branch's encrypted connection code

Forgot to delete broker after exercise
  → Continuous billing at 1CPU/4GB rate (no free tier for this)
```

***

## 🔷 Remaining Step Before Application Works

```
Backend services created:
  ✅ RDS MySQL     → exists but EMPTY
  ✅ ElastiCache   → ready
  ✅ Amazon MQ     → ready

NEXT: Initialize RDS MySQL with db_backup.sql
      (schema + data must be loaded before app can query the database)
```

***

## 🔷 Reusable Engineering Pattern: Managed Service Replacement

```
PATTERN: Replace Self-Managed with Managed Service

SELF-MANAGED (EC2-based):
  You install → you configure → you patch → you monitor → you scale → you fix

MANAGED (AWS service):
  You configure → AWS does everything else

Migration checklist:
  1. Identify the service (MySQL, Memcached, RabbitMQ)
  2. Find the AWS equivalent (RDS, ElastiCache, Amazon MQ)
  3. Match the configuration (engine version, access type, encryption)
  4. Verify application compatibility (source code branch, connection settings)
  5. Place in same security group tier (backend SG)
  6. Use private access (never public for backend)
  7. Test application connectivity

The application code changes minimally (connection strings/endpoints).
The infrastructure underneath changes completely.
```

This pattern is the core engineering idea of the entire re-architecture project section — the application stays the same, the infrastructure becomes managed. [\[144-amazon-mq \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/144-amazon-mq.txt)
