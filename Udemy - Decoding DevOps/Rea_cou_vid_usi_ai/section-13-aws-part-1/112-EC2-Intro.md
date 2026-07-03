# ☁️ AWS EC2 Introduction — Elastic Compute Cloud, Pricing, Components, and Instance Launch Flow

**Source:** AWS EC2 Introduction Session (Caption File) [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

This video is the **foundational introduction to AWS EC2** — the most popular service in Amazon Web Services. The instructor covers what EC2 is, why it's called "elastic," the four pricing models, the six core components that make up an EC2 instance, and the step-by-step wizard flow for creating an instance. This is a theory-heavy lecture that establishes the complete mental architecture of EC2 before the hands-on launch in the next session. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. What EC2 Is — The Core Service

EC2 stands for **Elastic Compute Cloud**. It is one of the **most popular services of AWS**, and its core purpose is straightforward: **EC2 is about virtual machines and the related services around them**. More precisely, EC2 provides **web services for managing and provisioning virtual machines inside Amazon's data centers** (Amazon Cloud). [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

If you've worked with virtual machines locally (the course previously covered Vagrant and VirtualBox), EC2 is the cloud equivalent — but instead of running VMs on your laptop, you're running them on Amazon's infrastructure, accessible over the internet, with AWS managing the underlying physical hardware.

***

## 2. Why "Elastic" — The Scaling Concept

The word **"elastic"** in EC2 is not decorative — it describes the fundamental capability that makes cloud computing different from traditional infrastructure. EC2 lets you **easily scale up or scale down your resources**. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

The instructor gives a concrete example: if your virtual machine has **8 GB of RAM**, you can scale up to **16 GB** or scale down to **4 GB**. This elasticity applies not just to RAM but to **CPU, network, and storage** as well. In traditional infrastructure, changing these would mean buying new hardware, physically installing it, and potentially facing downtime. In EC2, it's a configuration change. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

This elasticity connects directly to the pricing model: **you pay only for what you're using or how much you're using**. If you scale down, you pay less. If you scale up during peak demand, you pay more during that period but only for that period. The resources are not permanently allocated — they're elastic.

<details>
<summary>🔍 Deep Dive</summary>

The elasticity of EC2 is what enables the entire cloud computing economic model. In traditional IT, you must provision for peak capacity (buy servers large enough for your busiest day), which means most of the time you're paying for resources you're not using. EC2 inverts this: you provision for current need and scale up/down as demand changes. This is the fundamental cost advantage of cloud computing over on-premises infrastructure. Every other AWS service that integrates with EC2 (auto-scaling, load balancing, etc.) is built around this elasticity principle.

</details>

***

## 3. EC2 Integration with Other AWS Services

The instructor mentions that EC2 is **"very famous for getting integrated with other services"** and names several: **S3** (object storage), **EFS** (Elastic File System), **RDS** (Relational Database Service), **DynamoDB** (NoSQL database), and **Lambda** (serverless compute). EC2 doesn't exist in isolation — it's a central node in the AWS ecosystem that connects to storage services, database services, compute services, and many others. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

This positions EC2 as the **compute hub** of AWS architectures — the place where your applications run, connected to other services that provide storage, data, and additional capabilities.

***

## 4. EC2 Pricing Models — Four Options

EC2 has four distinct pricing models, each designed for different use cases and commitment levels: [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

### On-Demand

This is the **default and most straightforward** model — **pay per hour** (or per second for some instance types). You launch an instance, you pay for every hour it runs, and you stop paying when you terminate it. No upfront commitment, no long-term contract. The instructor states this is what will be used throughout the course, specifically with the **free tier** (AWS provides a limited amount of free EC2 usage for new accounts). [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

### Reserved

You **reserve EC2 capacity for 1 to 3 years** in advance. In exchange for this commitment, you get **discounts** compared to On-Demand pricing. This is for workloads you know will run continuously for a long period — if you know you need a server running 24/7 for the next year, Reserved is significantly cheaper than On-Demand. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

### Spot Instances

These are the **unused EC2 resources** across Amazon's data centers. You can **bid** on this unused capacity and get **"huge, huge discounts"** — often 60-90% cheaper than On-Demand. But there is a critical trade-off: **if someone outbids you, your EC2 instance will be terminated** (gone). The instructor notes that Spot instances are typically used in a **"mixture of auto scaling group"** — meaning you combine Spot instances with On-Demand or Reserved instances so that losing a Spot instance doesn't kill your application. Used strategically, this **"will save you a lot of money."** [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

<details>
<summary>⚠️ Expert Note</summary>

Spot instances are powerful for stateless, fault-tolerant workloads — batch processing, data analysis, CI/CD build agents, testing environments. Never use Spot for a single critical server (database, primary web server) because it can be taken away at any time. The engineering pattern is: design for disposability, then use Spot to save money. If your architecture can't tolerate sudden instance loss, Spot is dangerous.

</details>

### Dedicated Host

Instead of sharing physical hardware with other AWS customers (which is what happens with On-Demand, Reserved, and Spot — they're all virtual machines on shared hardware), you can **dedicate a complete physical server** to yourself. This is **very expensive** but is used for compliance requirements (some regulations require dedicated hardware), licensing requirements (some software licenses are tied to physical cores), or workloads that need guaranteed hardware isolation. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

***

## 5. The Six Core Components of an EC2 Instance

When you launch an EC2 instance, six components come together. The instructor walks through each one, and understanding their roles and relationships is essential before creating any instance: [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

### AMI — Amazon Machine Image

The AMI is a **ready-made virtual machine image** — a pre-built template that contains an operating system (and optionally pre-installed software). The instructor draws a direct parallel to the course's earlier content: **"like Vagrant, we have seen Vagrant boxes — here we have AMI."** Just as you chose a Vagrant box to create a local VM, you choose an AMI to create an EC2 instance. AWS provides a **huge list** of AMIs to choose from — different operating systems (Amazon Linux, Ubuntu, Windows Server, etc.), different configurations, and community-contributed AMIs. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

### Instance Type

The instance type determines the **size and compute resources** of your instance — specifically, how much **CPU, RAM, network speed, and storage speed** the virtual machine gets. AWS offers a **"huge variety"** of instance types, ranging from tiny (free-tier eligible) to massive (hundreds of vCPUs and terabytes of RAM). Choosing the right instance type means matching the resource profile to your workload's needs. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

### EBS — Elastic Block Store

EBS is the **storage** component — the **virtual hard disks** attached to your EC2 instance. EBS is where you store your **operating system** and your **data**. The instructor notes that AMIs come with default storage: **8 GB for Linux machines** and **30 GB for Windows machines**. You can **add additional storage** beyond the default, choosing from different EBS volume types (varying in speed and cost). [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

The key conceptual relationship: **AMI provides the base OS image → EBS provides the disk it lives on**. The AMI is loaded onto EBS storage when the instance launches. You can also attach additional EBS volumes for data storage.

### Tags

Tags are **simple key-value pairs** that you attach to any AWS resource for identification and organization. The instructor gives examples: **name of the EC2 instance, project, customer who owns it, environment** (dev/staging/production). You can set **as many tags as you want**. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

Tags serve two critical operational purposes: **filtering** (finding specific instances among hundreds) and **billing** (tracking which project or customer is responsible for costs). In any organization running more than a few instances, tags are what prevent chaos.

### Security Group

A security group is a **firewall for inbound and outbound traffic** attached to the EC2 instance. It controls what network traffic can reach the instance (inbound rules) and what traffic the instance can send out (outbound rules). **Every EC2 instance has a security group**. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

This connects to the networking fundamentals covered earlier in the course — security groups operate at Layer 3/4 of the OSI model (IP addresses and ports), controlling which sources can communicate with the instance on which ports.

### Key Pair

To **log in to an EC2 instance**, you need a key pair — the same **SSH public/private key concept** covered in the bash scripting section. The instructor explicitly makes this connection: **"as we have seen in the bash scripting."** [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

The operational flow: you create a key pair in AWS, **download the private key** for yourself, and AWS **injects the public key into the instance**. Then you use the private key to SSH into the instance. This is the same lock-and-key mechanism from the SSH key exchange lecture — the public key (lock) goes on the server, the private key (key) stays with you. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

For **Linux machines**, the key pair is used for **SSH login**. For **Windows machines**, the key pair is used to **generate the password** (you decrypt the auto-generated Windows administrator password using your private key).

<details>
<summary>🔍 Deep Dive</summary>

The six components map to different layers of the infrastructure:

| Component      | What It Provides                                        |
| -------------- | ------------------------------------------------------- |
| AMI            | The software template (OS + pre-installed packages)     |
| Instance Type  | The hardware profile (CPU, RAM, network, storage speed) |
| EBS            | The persistent storage (virtual hard disks)             |
| Tags           | Organizational metadata (names, projects, billing)      |
| Security Group | Network access control (firewall rules)                 |
| Key Pair       | Authentication credentials (SSH access)                 |

Together, these six components fully define an EC2 instance: what OS it runs (AMI), what resources it has (Instance Type), what storage it uses (EBS), how it's identified (Tags), what traffic it allows (Security Group), and how you log in (Key Pair).

</details>

***

## 6. The EC2 Launch Flow — Wizard-Based Creation

The instructor describes the EC2 instance creation process as **"wizard-based"** — a step-by-step guided flow. Understanding this flow conceptually is important because each step maps to one or more of the six components: [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

1. **Choose AMI** — Select the operating system / machine image.
2. **Select Instance Type** — Choose the compute resource size (CPU, RAM, etc.).
3. **Configure Instance** — Set network, permissions, and startup scripts.
4. **Decide Storage (EBS)** — Accept default AMI storage or add extra volumes.
5. **Set Tags** — Define key-value pairs for identification and billing.
6. **Create/Select Security Group** — Define firewall rules.
7. **Review and Launch** — Review all choices, select a login key pair, and launch.

The instructor frames this as **"very easy"** — and it is, because the wizard walks you through each component in sequence. But understanding what each step does (which the six components section above provides) is what makes the wizard meaningful rather than mechanical. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are preparing to **launch an EC2 instance** (a virtual machine in AWS) using the EC2 wizard. This lecture covers the **conceptual preparation** — understanding every component and decision point you'll encounter. The actual hands-on launch happens in the next session. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Why it matters:** EC2 is the foundational compute service in AWS. Every cloud-based application, deployment pipeline, and infrastructure setup you'll work with in this course (and in real DevOps work) will involve EC2 instances. Understanding the launch flow and components is prerequisite knowledge.

**Final outcome:** After this lecture + the next hands-on session, you will have a running EC2 instance in AWS that you can SSH into, with properly configured storage, security, and tagging.

***

## Step 1: Understand the Pricing Decision — Free Tier On-Demand

**What we are doing:** Choosing the pricing model for the course. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

The instructor states: **"we will be doing On-Demand and in course we'll be using the free tier."** This means:

* **On-Demand** — pay per hour, no commitment, launch and terminate freely.
* **Free Tier** — AWS provides limited free EC2 usage (typically 750 hours/month of `t2.micro` or `t3.micro` instances for 12 months after account creation).

**Operational reasoning:** On-Demand with Free Tier is the correct choice for learning — zero upfront cost, no commitment, and you can launch/terminate instances as needed during exercises.

**Common mistake:** Leaving instances running after a lab session → consuming free tier hours or incurring charges. Always **stop or terminate** instances when you're done.

**Connection to flow:** Pricing model selected → now you need to choose the components for the instance.

***

## Step 2: Choose the AMI (Amazon Machine Image)

**What we are doing:** Selecting the base OS template for the virtual machine. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Operational reasoning:** The AMI determines what operating system and pre-installed software your instance starts with. For this course, Linux AMIs are the primary focus (the course has been Linux-focused throughout).

**How to choose:** AWS presents a list of AMIs in the launch wizard. You can filter by:

* OS type (Amazon Linux, Ubuntu, Windows, etc.)
* Architecture (x86, ARM)
* Free tier eligible (look for the "Free tier eligible" label)

**Analogy from the course:** AMI is to EC2 what a **Vagrant box** is to VirtualBox. Same concept, different platform. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Default storage that comes with AMI:**

* **Linux AMI** → **8 GB** default EBS storage
* **Windows AMI** → **30 GB** default EBS storage

**Connection to flow:** AMI chosen → next, select the instance type (hardware size).

***

## Step 3: Select the Instance Type

**What we are doing:** Choosing the compute resource profile — how much CPU, RAM, network, and storage speed the instance gets. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**How to choose:** AWS provides a huge variety of instance types. For the course (free tier), you'll select the smallest available type (typically `t2.micro` or `t3.micro`).

**Operational reasoning:** The instance type must match your workload. For learning, the smallest free-tier type is sufficient. In production, you'd analyze your application's CPU, memory, and network requirements to select the right type.

**Connection to flow:** Instance type chosen → next, configure instance settings.

***

## Step 4: Configure the Instance

**What we are doing:** Setting instance-level configurations — **network, permissions, and scripts to execute** at launch. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

This step includes settings like which VPC (Virtual Private Cloud) and subnet to launch in, IAM roles (permissions), and **user data scripts** (bash scripts that execute automatically when the instance first boots — connecting directly to the bash scripting knowledge from earlier in the course).

**Connection to flow:** Configuration set → next, decide on storage.

***

## Step 5: Decide on Storage (EBS)

**What we are doing:** Choosing the disk storage for the instance. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Default behavior:** The AMI comes with default storage (8 GB for Linux, 30 GB for Windows). You can **accept the default or add extra EBS volumes**.

**Operational reasoning:** EBS volumes are the **virtual hard disks** — they hold the OS and your data. If your workload needs more storage than the default, you add volumes here. Each volume has a type (affecting speed and cost) and a size.

**Connection to flow:** Storage configured → next, set tags.

***

## Step 6: Set Tags

**What we are doing:** Adding key-value pairs for identification and organization. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Minimum recommended tags:** [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

* **Name** — a human-readable identifier for the instance (e.g., "web-server-01")
* **Project** — which project this instance belongs to
* **Environment** — dev, staging, production

**Operational reasoning:** Tags are how you find your instance among potentially hundreds of others. They're also how AWS billing reports break down costs by project, team, or environment. Without tags, you'll have unnamed instances that are impossible to manage at scale.

**Connection to flow:** Tags set → next, configure the firewall.

***

## Step 7: Create or Select a Security Group

**What we are doing:** Defining the firewall rules that control what network traffic can reach the instance and what traffic it can send. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Operational reasoning:** The security group is the first line of network defense for the instance. At minimum, you need to allow **SSH traffic (port 22)** from your IP address so you can log in. For web servers, you'd also allow HTTP (port 80) and HTTPS (port 443).

**Common mistake:** Opening all ports to all IP addresses (`0.0.0.0/0` on all ports) for convenience → this exposes the instance to the entire internet and is a serious security risk.

**Connection to flow:** Security group configured → final step: review and launch.

***

## Step 8: Review and Launch — Choose Key Pair

**What we are doing:** Reviewing all configurations and selecting the login key pair. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Key pair operation:**

1. AWS lets you **create a new key pair** or **select an existing one**.
2. When you create a new key pair, you **download the private key** (`.pem` file). **This is the only time you can download it** — if you lose it, you cannot retrieve it.
3. AWS **injects the public key** into the instance during launch.
4. You use the private key to SSH into the instance (Linux) or decrypt the password (Windows).

**This is the SSH key exchange from the earlier lecture**, applied in the AWS context. The lock (public key) goes on the server (injected by AWS), the key (private key) stays with you (downloaded `.pem` file). [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

**Common mistake:** Not downloading the private key during creation, or losing the `.pem` file after download → you won't be able to SSH into the instance.

**After clicking Launch:** The instance begins provisioning. AWS allocates compute resources, attaches EBS storage, loads the AMI, applies the security group, injects the key, and starts the virtual machine.

<details>
<summary>⚠️ Expert Note</summary>

In production, you'd rarely launch instances through the AWS console wizard. Instead, you'd use Infrastructure as Code tools (Terraform, CloudFormation) to define EC2 instances declaratively — specifying all six components in a configuration file that can be version-controlled, reviewed, and reproduced. The console wizard is for learning and ad-hoc testing; IaC is for production. But understanding what the wizard does is prerequisite to understanding what the IaC templates are configuring.

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   AWS EC2 Introduction — Elastic Compute Cloud
CONTEXT: DevOps course → first AWS service → foundation for all cloud compute
PURPOSE: Understand EC2 conceptually before hands-on launch
```

***

## What EC2 Is

```
EC2 = Elastic Compute Cloud
    = Virtual Machines + related services in AWS
    = Web service for managing/provisioning VMs in Amazon's data centers

"Elastic" = scale up/down (CPU, RAM, network, storage) on demand
Pay model = pay only for what you use
```

***

## Four Pricing Models

```
ON-DEMAND       → Pay per hour/second, no commitment
                   Use case: learning, variable workloads, short-term
                   [Course uses this + free tier]

RESERVED        → 1–3 year commitment → discounts
                   Use case: steady-state, always-on workloads

SPOT            → Bid on unused AWS capacity → HUGE discounts (60-90%)
                   Risk: outbid = instance TERMINATED
                   Use case: fault-tolerant, stateless, batch processing
                   Pattern: mix with On-Demand in auto-scaling group

DEDICATED HOST  → Entire physical server for you → very expensive
                   Use case: compliance, licensing, hardware isolation
```

***

## Six Core Components of an EC2 Instance

```
┌──────────────────────────────────────────────────────┐
│  EC2 INSTANCE                                        │
│                                                      │
│  1. AMI (Amazon Machine Image)                       │
│     = Ready-made VM template (OS + software)         │
│     = Vagrant box equivalent in AWS                  │
│     Default storage: Linux 8GB / Windows 30GB        │
│                                                      │
│  2. INSTANCE TYPE                                    │
│     = Hardware profile (CPU, RAM, network, storage)  │
│     = Size of the VM                                 │
│                                                      │
│  3. EBS (Elastic Block Store)                        │
│     = Virtual hard disks (OS + data storage)         │
│     = Can add extra beyond AMI default               │
│                                                      │
│  4. TAGS                                             │
│     = Key-value pairs (Name, Project, Environment)   │
│     = For filtering + billing                        │
│                                                      │
│  5. SECURITY GROUP                                   │
│     = Firewall (inbound + outbound rules)            │
│     = Every instance has one                         │
│                                                      │
│  6. KEY PAIR                                         │
│     = SSH keys (public injected → private download)  │
│     = Linux: SSH login / Windows: decrypt password   │
│     = Same lock-and-key from SSH key exchange lecture │
└──────────────────────────────────────────────────────┘
```

***

## Component-to-Layer Mapping

```
AMI             → SOFTWARE layer   (what OS/software runs)
Instance Type   → HARDWARE layer   (how much compute power)
EBS             → STORAGE layer    (where data lives)
Tags            → METADATA layer   (how it's identified/tracked)
Security Group  → NETWORK layer    (what traffic is allowed)
Key Pair        → AUTH layer       (how you log in)
```

***

## EC2 Launch Wizard Flow

```
1. Choose AMI              → What OS?
2. Select Instance Type    → What size? (CPU/RAM)
3. Configure Instance      → Network, permissions, startup scripts
4. Decide Storage (EBS)    → Default or add extra volumes
5. Set Tags                → Key-value pairs (Name, Project, Env)
6. Security Group          → Firewall rules (inbound/outbound)
7. Review + Key Pair       → Review all → choose/create key → LAUNCH
```

***

## EC2 ↔ Course Concept Bridges

```
AMI              ↔  Vagrant Box          (same concept: VM template)
Key Pair         ↔  SSH Key Exchange     (same lock-and-key mechanism)
Security Group   ↔  OSI Layer 3/4       (IP + port filtering)
Startup scripts  ↔  Bash Scripting      (automate instance config at boot)
Elasticity       ↔  Containers          (scale resources to match demand)
```

***

## EC2 Integration Map

```
EC2 (compute hub)
  ├── S3        (object storage)
  ├── EFS       (elastic file system)
  ├── RDS       (relational databases)
  ├── DynamoDB  (NoSQL database)
  ├── Lambda    (serverless compute)
  └── many more...
```

***

## Key Pair Flow in EC2

```
CREATE key pair in AWS
  ├── DOWNLOAD private key (.pem) → YOUR machine (one-time download!)
  └── AWS INJECTS public key → into EC2 instance

LOGIN:
  Linux:   ssh -i key.pem user@instance-ip
  Windows: use key to decrypt auto-generated admin password
```

***

## Reusable Engineering Patterns Extracted

```
1. ELASTICITY = RESOURCE DECOUPLING   → Compute resources not permanently allocated
                                         Scale up/down based on demand → pay for use only
                                         (same pattern: containers, serverless, auto-scaling)

2. TEMPLATE-BASED PROVISIONING        → AMI = frozen template → launch identical instances from it
                                         (same pattern: container images, Vagrant boxes, golden images)

3. COMPONENT COMPOSITION              → Instance = AMI + Type + EBS + Tags + SG + Key
                                         Each component is independent, configurable, replaceable
                                         (same pattern: microservices, modular architecture)

4. METADATA-FOR-MANAGEMENT (TAGS)     → Attach key-value metadata to resources → filter + bill
                                         Without metadata, large-scale management is impossible
                                         (same pattern: labels in Kubernetes, tags in Docker)

5. WIZARD-AS-SEQUENTIAL-ASSEMBLY      → Complex creation = step-by-step component selection
                                         Each step configures one dimension of the final system
                                         (same pattern: CI/CD pipeline stages, build systems)
```

***

## Rapid Recall Triggers

```
"What is EC2?"                  → Elastic Compute Cloud = VMs + related services in AWS
"Why elastic?"                  → Scale up/down CPU/RAM/network/storage on demand
"EC2 pricing models?"           → On-Demand (hourly) / Reserved (1-3yr) / Spot (bid, risky) / Dedicated Host (physical)
"What is an AMI?"               → Amazon Machine Image = ready-made VM template (like Vagrant box)
"What is an Instance Type?"     → Hardware profile: CPU, RAM, network speed, storage speed
"What is EBS?"                  → Elastic Block Store = virtual hard disks (OS + data)
"Default EBS size?"             → Linux 8GB / Windows 30GB
"What are Tags?"                → Key-value pairs for filtering + billing (Name, Project, Env)
"What is a Security Group?"     → Firewall for inbound/outbound traffic on EC2
"How to login to EC2?"          → Key pair (SSH keys) — private key downloaded, public injected
"Spot instance risk?"           → Outbid = instance terminated (use for fault-tolerant only)
"Launch wizard steps?"          → AMI → Type → Config → Storage → Tags → SG → Review+Key → Launch
"EC2 integrates with?"          → S3, EFS, RDS, DynamoDB, Lambda, many more
```

***

This completes the full reconstruction of the AWS EC2 Introduction lecture. **Theory** builds the conceptual architecture of EC2's pricing, components, and integration ecosystem; **Practical** maps each wizard step to operational decisions you'll make during launch; and the **Mental Compression Map** compresses the entire six-component model, pricing matrix, and launch flow into rapid-recall structures. [\[112-ec2-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/112-ec2-introduction.txt)

Ready for the next caption file, or shall I generate an **AnkiDroid CSV** covering this lecture or the full series? 🚀
