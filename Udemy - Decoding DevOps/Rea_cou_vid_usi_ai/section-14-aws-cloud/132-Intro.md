# Lift and Shift Application Workload on AWS Cloud — vProfile Project

**Source:** Video caption file — *"Lift and Shift Application Workload"* (Introduction lecture from a DevOps/AWS course) [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What is Lift and Shift?

Lift and Shift is a cloud migration strategy where you take an existing application — exactly as it runs today on physical or virtual machines in your data center — and move it onto a cloud platform with minimal or no re-architecture. You "lift" the application out of its current environment and "shift" it onto cloud infrastructure. The application logic, the services, the way components talk to each other — all of that stays fundamentally the same. What changes is **where** and **how** the underlying infrastructure is provisioned, managed, and scaled. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

This strategy exists because many organizations cannot afford the time, risk, or engineering effort to redesign their entire application stack before moving to the cloud. They need the benefits of cloud computing — cost flexibility, elasticity, automation — **now**, without rewriting code. Lift and Shift gives them that entry point. You get cloud benefits immediately, and you can modernize incrementally later. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

In this project, the application being lifted and shifted is **vProfile** — a multi-tier Java web application stack. In a previous project, this exact stack was set up locally using Vagrant on virtual machines. Now, the same stack is being moved to AWS Cloud for production use. The components remain the same; the hosting platform changes from local VMs to AWS services. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.2 — The Problem: Running Application Services On-Premises

To understand why Lift and Shift matters, you need to understand the pain of running applications in a traditional data center. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

In a typical enterprise, application services run on physical or virtual machines inside a local data center. These services can include databases (MySQL, Postgres, Oracle), application servers (Tomcat, LAMP Stack), DNS services, message brokers, caching layers — essentially, all the components that power a production application. Each of these services runs on one or more servers, and all of them live in the organization's own data center. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

Managing this requires **multiple specialized teams** working continuously:

* **Virtualization team** — manages the virtualization platform (hypervisors, VM lifecycle)
* **Data center operations team** — handles physical infrastructure, networking, power, cooling, and related operations
* **Monitoring team** — monitors all services 24/7 for uptime and performance
* **System administration team** — handles OS-level management, patching, configuration, and troubleshooting [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

The core problems are:

**Complexity of management.** Coordinating multiple teams across multiple service layers creates operational overhead. Every change requires coordination. Every incident involves multiple teams.

**Scaling difficulty.** If your application suddenly needs more capacity, you cannot instantly spin up new servers. Scaling up requires procurement, racking, installing, configuring — a process that can take weeks or months. Scaling down is equally difficult; you cannot easily de-provision physical hardware. Yet scaling needs to happen regularly in real production environments.

**High cost.** There is a massive upfront capital expenditure for procuring servers, networking equipment, storage arrays, and data center space. On top of that, there is continuous maintenance cost — power, cooling, hardware replacements, licensing, staffing.

**Manual processes.** Most operations — provisioning, deploying, scaling, patching — are manual. Even if a virtualization layer exists on top of the physical infrastructure, automating those processes is very difficult to implement and even harder to maintain long-term.

**Time consumption.** Every task — from provisioning a new server to deploying a new version of the application — takes significant time due to manual processes and team coordination. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

🔍 **Deep Dive:**
The key insight here is that the problem is not just technical — it is **organizational and economic**. The data center model forces you to pre-commit resources (buy before you need), over-provision for peak load (waste during normal load), and staff teams that are always busy with operational work rather than building value. Cloud computing doesn't just solve the "where do my VMs run" question — it dissolves the organizational and financial constraints that make the data center model painful. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.3 — The Solution: Cloud Computing as Infrastructure-as-a-Service

The solution to all the data center problems is **cloud computing** — specifically, consuming infrastructure as a service (IaaS). Instead of running workloads in your own data center, you run them on a cloud platform. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

The key properties of this model:

**No upfront cost — Pay as you go.** You do not buy servers. You rent compute, storage, and networking on-demand and pay only for what you consume. The analogy used is **electricity** — you don't build a power plant; you consume electricity from a provider and pay your bill. Cloud infrastructure works the same way. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Elasticity and flexibility.** Cloud infrastructure is elastic — you can scale out (add more instances) when load increases and scale in (remove instances) when load decreases. This gives you real control over both capacity and cost, because you're never locked into hardware you don't need. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Easier infrastructure management.** The cloud provider handles the physical infrastructure — data centers, networking, hardware maintenance, power, cooling. Your operational burden drops dramatically.

**Automation.** This is the most important advantage. In the cloud, you can automate every step and every process — provisioning, deployment, scaling, monitoring, recovery. Automation eliminates human errors and saves enormous amounts of time. The phrase used is **"Infrastructure as Code"** — your entire infrastructure can be defined, versioned, and deployed through code rather than manual processes. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.4 — The vProfile Application Stack: Components and Their Roles

The vProfile application is a **multi-tier web application** with distinct layers, each handled by a specific technology:

| Component                                             | Role                                                                              | Tier                     |
| ----------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------ |
| **Nginx** (on-prem) / **Elastic Load Balancer** (AWS) | Entry point — receives user requests and distributes them to the application tier | Load Balancing / Ingress |
| **Apache Tomcat**                                     | Java application server — runs the actual vProfile application code               | Application Tier         |
| **RabbitMQ**                                          | Message broker — handles asynchronous messaging between application components    | Backend Services         |
| **Memcache**                                          | Caching layer — stores frequently accessed data in memory for fast retrieval      | Backend Services         |
| **MySQL**                                             | Relational database — stores persistent application data                          | Backend Services         |

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

In the previous project, all these services ran on local virtual machines managed by Vagrant. In this project, the same logical stack is being shifted to AWS. The application code doesn't change. The service roles don't change. What changes is the infrastructure underneath. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

A critical point: on the local setup, **Nginx** served as the front-end load balancer. On AWS, Nginx is replaced by **AWS Elastic Load Balancer** — a managed service that provides the same functionality (traffic distribution) without you having to manage the Nginx server itself. This is the first small step toward "modernization within a lift and shift" — replacing a self-managed component with a cloud-managed equivalent. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.5 — AWS Services Mapped to Application Needs

Each AWS service in this project exists to solve a specific infrastructure need. Understanding this mapping is fundamental:

**EC2 (Elastic Compute Cloud) Instances** — These are virtual machines. They replace the local VMs that previously ran Tomcat, RabbitMQ, Memcache, and MySQL. Each service gets its own EC2 instance(s). EC2 gives you full control over the OS, installed software, and configuration — exactly what you need for a lift and shift where the application expects a traditional server environment. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Elastic Load Balancer (ELB) — specifically, Application Load Balancer (ALB)** — Replaces Nginx as the traffic entry point. It receives incoming user requests (HTTPS) and routes them to the appropriate Tomcat EC2 instances. Being a managed service, you don't have to manage a server for it — AWS handles its availability, scaling, and maintenance. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Auto Scaling Group** — Manages the Tomcat EC2 instances dynamically. When load is high, Auto Scaling launches more Tomcat instances. When load drops, it terminates excess instances. This directly controls both resource availability and cost — you only run (and pay for) what you need. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Amazon S3 (Simple Storage Service)** — Used to store the application artifact (the compiled application WAR/JAR file). The artifact is built on a local machine, uploaded to S3, and then downloaded to the Tomcat EC2 instances. S3 acts as a centralized, durable, accessible storage layer for deployment artifacts. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Amazon Route 53** — Used as a **private DNS service**. Backend server IP addresses (MySQL, Memcache, RabbitMQ) are registered as DNS entries in a Route 53 Private DNS Zone. Tomcat instances access backend servers **by name** (not by IP address), and Route 53 resolves those names to the correct private IP addresses. This decouples the application from specific IP addresses — if a backend instance is replaced, you only update the DNS record, not the application configuration. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Amazon Certificate Manager (ACM)** — Provides the SSL/TLS certificate for HTTPS encryption. The certificate is attached to the Application Load Balancer so that all traffic between users and the load balancer is encrypted. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Other services mentioned:** IAM (identity and access management for permissions), EBS (block storage for EC2 instances). These are supporting services that enable the core architecture. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

🔍 **Deep Dive:**
Notice the **service replacement mapping**: Nginx → ELB, local file system → S3, `/etc/hosts` or local DNS → Route 53, manual scaling → Auto Scaling Group. This is the essence of Lift and Shift on AWS — each on-prem component has a direct AWS equivalent. The application logic stays identical; only the infrastructure layer is swapped. The few places where a managed service replaces a self-managed one (Nginx → ELB, local DNS → Route 53) represent small modernization wins within the lift and shift. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.6 — Architectural Design: The Three-Tier Security Model

The architecture implements a **three-tier security model** using three separate AWS Security Groups. This is one of the most important architectural decisions in the project. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Security Group 1 — Load Balancer Security Group:**
The Application Load Balancer sits in this group. It allows **only HTTPS traffic** from the internet. No other port, no other protocol is permitted. This is the only component directly exposed to the outside world. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Security Group 2 — Application Tier Security Group (Tomcat):**
The Tomcat EC2 instances sit in this group. They allow traffic **only on port 8080** and **only from the Load Balancer Security Group**. They do not accept traffic from the internet directly. This means even if someone knows the IP address of a Tomcat instance, they cannot reach it unless the request comes through the load balancer. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Security Group 3 — Backend Services Security Group (MySQL, Memcache, RabbitMQ):**
The backend EC2 instances sit in this group. They accept traffic only from the Application Tier Security Group. They are completely isolated from both the internet and the load balancer. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

This creates a strict **traffic flow chain**: Internet → Load Balancer (SG1) → Tomcat (SG2) → Backend (SG3). Each layer can only be reached from the layer directly in front of it. This is a fundamental network security pattern called **defense in depth** — even if one layer is compromised, the attacker cannot directly reach deeper layers. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

⚠️ **Expert Note:**
In production, this security group design is not optional — it is baseline. Real-world implementations often add further restrictions: specific CIDR ranges, VPC flow logs for auditing, NACLs (Network Access Control Lists) as a second layer of network filtering, and private subnets for backend instances with no public IP addresses at all. The video's three-group model is the essential foundation upon which all of that is built. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.7 — Service Discovery via Route 53 Private DNS

One of the most architecturally significant decisions in this project is using **Route 53 Private DNS Zones** for backend service discovery. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

Instead of hardcoding backend server IP addresses into the Tomcat application configuration, the architecture uses **DNS names**. The Tomcat application is configured to reach MySQL at a name like `db01.vprofile.in`, Memcache at `mc01.vprofile.in`, and RabbitMQ at `rmq01.vprofile.in` (example names). These names are registered in a Route 53 Private DNS Zone, which maps them to the **private IP addresses** of the respective backend EC2 instances. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

Why this matters: EC2 instances can be terminated and replaced. When that happens, the new instance gets a new private IP address. If the application used hardcoded IPs, every replacement would require application reconfiguration and redeployment. With DNS-based service discovery, you only update the Route 53 record to point to the new IP address. The application doesn't change at all. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

This is the **name-based decoupling pattern** — a fundamental infrastructure design principle where consumers refer to services by stable names rather than volatile addresses. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.8 — The Artifact Deployment Pipeline

The application deployment follows a specific pipeline:

1. The application **source code is built on the local machine** (developer's laptop) to produce a deployable artifact (typically a WAR file for Tomcat).
2. The artifact is **uploaded to an S3 bucket** — a centralized, durable storage location.
3. The artifact is then **downloaded from S3 to the Tomcat EC2 instance** and deployed.

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

This pipeline exists because you cannot (and should not) build application code directly on production servers. The local build → S3 → EC2 flow provides a clean separation between the **build environment** (local) and the **runtime environment** (EC2). S3 acts as the intermediary — a durable, versioned, accessible handoff point. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

🔍 **Deep Dive:**
In more mature setups, the "local machine" step would be replaced by a CI/CD pipeline (Jenkins, GitHub Actions, etc.) that builds the artifact automatically and pushes it to S3. The fundamental pattern — build → store in central artifact repository → deploy to target — remains the same regardless of whether the build happens on a laptop or in a CI server. This project teaches the manual version of the pattern, which is the foundation for understanding automated pipelines later. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## 1.9 — Auto Scaling: Elastic Capacity Management

The Auto Scaling Group is applied specifically to the **Tomcat application tier** — the tier that directly serves user requests and is most sensitive to load fluctuations. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

Auto Scaling monitors the load on Tomcat instances and makes capacity decisions:

* **High load** → launches additional Tomcat EC2 instances (scale out)
* **Low load** → terminates excess instances (scale in)

This directly addresses two problems from the on-prem model: you never over-provision (wasting money on idle servers), and you never under-provision (degrading user experience during traffic spikes). [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

Note that in this project's execution flow, the Auto Scaling Group is set up **last** — after the entire stack is verified and working. This is intentional. You first prove the system works with a fixed number of instances, then add the dynamic scaling layer on top. This is a common operational pattern: **stabilize first, then automate**. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are taking the vProfile multi-tier Java web application — previously running on local Vagrant VMs — and deploying it on AWS Cloud using the Lift and Shift strategy. The final outcome is a production-ready deployment where users access the application via HTTPS through a load balancer, the application tier scales automatically, backend services are discovered via private DNS, and the entire infrastructure is organized into security-isolated tiers. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Execution Flow Overview

The video defines a precise execution sequence. Each step builds on the previous one. Here is the complete flow, which we will then walk through step by step: [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

1. Log into AWS account
2. Create key pairs
3. Create security groups
4. Launch EC2 instances with user data
5. Update IP-to-name mapping in Route 53
6. Build the application from source code (local machine)
7. Upload artifact to S3
8. Download artifact to Tomcat EC2 instance
9. Set up load balancer with HTTPS
10. Map ELB endpoint in GoDaddy DNS
11. Verify the entire setup
12. Build Auto Scaling Group for Tomcat instances

***

### Step 1: Log into AWS Account

**What we are doing:** Accessing the AWS Management Console to begin infrastructure provisioning.

**Why:** All AWS resources are created and managed through the AWS account. This is the entry point for everything that follows. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 2: Create Key Pairs

**What we are doing:** Generating an SSH key pair within AWS.

**Why:** Key pairs are the authentication mechanism for logging into EC2 instances. When you launch an EC2 instance, you associate a key pair with it. To SSH into that instance later (for configuration, troubleshooting, or deployment), you use the private key from that pair. Without a key pair, you cannot access your instances. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Operational note:** The private key file (`.pem`) is downloaded only once at creation time. If you lose it, you lose SSH access to instances associated with that key pair. Store it securely immediately after creation. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 3: Create Security Groups

**What we are doing:** Creating three separate security groups — one for the load balancer, one for the Tomcat application tier, and one for the backend services (MySQL, Memcache, RabbitMQ). [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** Security groups act as virtual firewalls for EC2 instances. By creating three separate groups with specific rules, we enforce the traffic flow chain described in the Theory section (Internet → LB → Tomcat → Backend). Each group only allows the minimum traffic necessary from the layer directly in front of it. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Operational details:**

* **Load Balancer SG:** Allow inbound HTTPS (port 443) from the internet (0.0.0.0/0).
* **Tomcat SG:** Allow inbound on port 8080 **only** from the Load Balancer Security Group (reference the SG ID, not an IP range).
* **Backend SG:** Allow inbound on the relevant service ports **only** from the Tomcat Security Group.

**How to verify:** After creation, review each security group's inbound rules in the AWS Console. Confirm that each group references the correct source security group (not open IP ranges). [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Common mistake:** Making security groups too permissive (e.g., allowing 0.0.0.0/0 on port 8080 for Tomcat). This defeats the purpose of tiered security. Always reference the upstream security group ID as the source. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 4: Launch EC2 Instances with User Data

**What we are doing:** Launching EC2 instances for each service (Tomcat, MySQL, Memcache, RabbitMQ), each with a **user data script** — a bash script that runs automatically when the instance boots for the first time. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** User data scripts automate the initial setup of each instance. Instead of manually SSHing into each instance and running installation commands, you provide a bash script that installs the required software, configures the service, and starts it — all automatically at boot time. This is the first step toward infrastructure automation. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Operational details:**

* Each service (Tomcat, MySQL, Memcache, RabbitMQ) gets its own EC2 instance.
* Each instance is placed in the appropriate security group (Tomcat instances in Tomcat SG, backend instances in Backend SG).
* Each instance is associated with the key pair created in Step 2.
* The user data field accepts a bash script that runs as root on first boot.

**How to verify:** After the instance reaches "running" state, SSH into it using the key pair and confirm the expected service is installed and running (e.g., `systemctl status tomcat`, `systemctl status mysql`). [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Common mistake:** Errors in user data scripts are silent — the instance launches but the service isn't configured correctly. Always verify by SSHing in and checking service status after launch. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

⚠️ **Expert Note:**
User data scripts run only on the **first boot** of an instance by default. If you stop and start the instance, the script does not re-run. If your script has a bug, you typically need to terminate the instance and launch a new one with the corrected script, rather than trying to fix the running instance. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 5: Update IP-to-Name Mapping in Route 53

**What we are doing:** Creating DNS records in a Route 53 Private DNS Zone that map service names to the private IP addresses of the backend EC2 instances. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** As discussed in the Theory section (1.7 — Service Discovery), the Tomcat application is configured to reach backend services by DNS name, not by IP. After launching backend instances, we know their private IPs. We now register those IPs in Route 53 so the names resolve correctly within the VPC. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Operational details:**

* Go to Route 53 → Create a Private Hosted Zone (associated with your VPC).
* Create A records mapping each backend service name to its instance's private IP address.
* Example: `db01.vprofile.in` → `172.31.x.x` (MySQL instance's private IP).

**How to verify:** From a Tomcat EC2 instance (within the same VPC), run `nslookup db01.vprofile.in` or `ping db01.vprofile.in` and confirm it resolves to the correct private IP. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Common mistake:** Forgetting to associate the Private Hosted Zone with the correct VPC. If the zone is not associated with the VPC where your instances live, DNS resolution will fail. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 6: Build Application from Source Code

**What we are doing:** Compiling the vProfile application source code on the local machine (laptop) to produce a deployable artifact (WAR file). [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** The application needs to be compiled before it can be deployed. This is done locally (not on the EC2 instance) to maintain separation between build and runtime environments.

**Connection to flow:** This artifact is what will be uploaded to S3 in the next step and eventually deployed to the Tomcat instance. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 7: Upload Artifact to S3 Bucket

**What we are doing:** Uploading the compiled application artifact (WAR file) from the local machine to an Amazon S3 bucket. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** S3 serves as the central, durable artifact storage. The Tomcat EC2 instance will pull the artifact from S3 rather than receiving it directly from the local machine. This decouples the build step from the deployment step and makes the artifact available to any instance that needs it (important when Auto Scaling creates new instances later).

**Operational details:**

* Create an S3 bucket (or use an existing one).
* Upload the artifact using the AWS CLI or the Console.
* Ensure the EC2 instance has the IAM permissions necessary to read from the S3 bucket. This is where **IAM roles** come in — attach a role to the Tomcat EC2 instance that grants S3 read access. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 8: Download Artifact to Tomcat EC2 Instance

**What we are doing:** Pulling the artifact from S3 onto the Tomcat EC2 instance and deploying it into Tomcat's webapps directory. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** The Tomcat application server needs the WAR file in its deployment directory to serve the application. By pulling from S3, we complete the build → store → deploy pipeline.

**How to verify:** Access the Tomcat manager or check the webapps directory to confirm the application is deployed. Check Tomcat logs for successful deployment messages. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 9: Set Up Load Balancer with HTTPS

**What we are doing:** Creating an Application Load Balancer, configuring it with an HTTPS listener, attaching the SSL/TLS certificate from ACM, and pointing it to the Tomcat instances as targets. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** The load balancer is the single entry point for all user traffic. HTTPS ensures encrypted communication between users and the application. The ALB distributes requests across Tomcat instances for availability and load distribution.

**Operational details:**

* Create a Target Group containing the Tomcat EC2 instance(s).
* Create an Application Load Balancer in the Load Balancer Security Group.
* Add an HTTPS listener (port 443) and attach the ACM certificate.
* Associate the Target Group with the listener.

**How to verify:** After creation, the ALB provides a DNS endpoint. Access this endpoint in a browser — you should see the vProfile application served over HTTPS. Check the Target Group health checks to ensure Tomcat instances are reported as "healthy." [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Common mistake:** Forgetting to configure the health check correctly in the Target Group. If the health check path or port doesn't match what Tomcat actually serves, instances will be marked "unhealthy" and the ALB will not route traffic to them. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 10: Map ELB Endpoint in GoDaddy DNS

**What we are doing:** Creating a DNS record in GoDaddy (or your domain registrar) that points your application's public domain name to the ALB's DNS endpoint. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** Users access the application via a human-readable URL (like `vprofile.yourdomain.com`), not via the ALB's auto-generated DNS name. This DNS entry connects the public-facing domain name to the actual ALB endpoint. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Operational details:**

* Go to GoDaddy DNS management.
* Create a CNAME record pointing your desired subdomain to the ALB's DNS name.

**How to verify:** After DNS propagation, access the URL in a browser. You should reach the vProfile application via HTTPS through the load balancer. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 11: Verify the Entire Setup

**What we are doing:** End-to-end verification — confirming that a user can access the application URL, the request flows through the load balancer to Tomcat, Tomcat connects to all backend services (MySQL, Memcache, RabbitMQ) via Route 53 DNS, and the application functions correctly. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** Before adding automation (Auto Scaling), you must prove the system works correctly in its static configuration. This is the **stabilize-first-then-automate** principle. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

### Step 12: Build Auto Scaling Group for Tomcat Instances

**What we are doing:** Creating an Auto Scaling Group that manages the Tomcat EC2 instances, enabling dynamic scaling based on load. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

**Why:** This is the final step that transforms the static deployment into an elastic, production-grade setup. The Auto Scaling Group ensures the application tier can handle traffic spikes without manual intervention and reduces cost during low-traffic periods.

**Operational details:**

* Create a Launch Configuration or Launch Template that defines how new Tomcat instances should be created (AMI, instance type, security group, key pair, user data script).
* Create the Auto Scaling Group referencing this template, with minimum, desired, and maximum instance counts.
* Associate the Auto Scaling Group with the ALB Target Group so new instances are automatically registered with the load balancer.

**Connection to the larger system:** Once this is in place, the full architecture is operational — users hit the ALB, the ALB routes to Tomcat instances managed by Auto Scaling, Tomcat accesses backends via Route 53 DNS, and the entire stack is secured by three layered security groups. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

⚠️ **Expert Note:**
The Auto Scaling Group relies on the Launch Template's user data script to configure new instances automatically. If that script has any issues, every newly scaled instance will be broken. Always test the user data script thoroughly on a single instance before enabling Auto Scaling. [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
PROJECT: Lift and Shift — vProfile on AWS
STRATEGY: Take existing multi-tier app → move to AWS with minimal re-architecture
APPLICATION: vProfile (Java web app)
PREVIOUS STATE: All services on local Vagrant VMs
TARGET STATE: Same services on AWS EC2 + managed AWS services
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## On-Prem → AWS Service Mapping

```
Nginx              → Application Load Balancer (managed)
Local VMs          → EC2 Instances
Manual scaling     → Auto Scaling Group
Local filesystem   → Amazon S3
/etc/hosts or DNS  → Route 53 Private DNS Zone
Self-managed SSL   → ACM (Amazon Certificate Manager)
Manual provisioning→ User Data scripts (bash at boot)
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Component Architecture

```
[Internet]
    │
    ▼ (HTTPS / port 443)
┌──────────────────────┐
│  Application Load    │  ← ACM certificate attached
│  Balancer            │  ← Security Group 1 (HTTPS only)
└──────────┬───────────┘
           │ (port 8080, from LB SG only)
           ▼
┌──────────────────────┐
│  Tomcat EC2          │  ← Security Group 2
│  (Auto Scaling Group)│  ← vProfile app deployed here
└──────────┬───────────┘
           │ (service ports, from Tomcat SG only)
           ▼
┌──────────────────────┐
│  Backend EC2s        │  ← Security Group 3
│  MySQL | Memcache |  │
│  RabbitMQ            │
└──────────────────────┘
           ▲
           │ (name resolution)
    Route 53 Private DNS
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Security Model

```
THREE-TIER SECURITY GROUP CHAIN:

SG1 (LB)      : Inbound HTTPS (443) from 0.0.0.0/0
SG2 (Tomcat)   : Inbound 8080 from SG1 ONLY
SG3 (Backend)  : Inbound service ports from SG2 ONLY

FLOW: Internet → SG1 → SG2 → SG3
PRINCIPLE: Defense in depth — each layer reachable only from the layer above
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Service Discovery Pattern

```
Tomcat app config → uses DNS names (not IPs)
                        │
                        ▼
              Route 53 Private DNS Zone
                        │
                        ▼
              Resolves to private IPs of backend EC2s

WHY: EC2 IPs are volatile. DNS names are stable.
UPDATE: Change DNS record, not app config.
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Artifact Deployment Pipeline

```
Local Machine (build)
       │
       ▼ (upload)
   S3 Bucket (store)
       │
       ▼ (download)
   Tomcat EC2 (deploy to webapps)

DECOUPLING: Build env ≠ Runtime env
SCALING: S3 artifact available to any new Auto Scaled instance
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Execution Sequence (Dependency Chain)

```
1. AWS Login
2. Key Pairs              ← needed for EC2 SSH access
3. Security Groups (×3)   ← needed before launching instances
4. EC2 Instances + User Data  ← placed in SGs, use key pairs
5. Route 53 DNS mapping   ← needs backend instance private IPs
6. Build app locally      ← independent of AWS
7. Upload artifact → S3   ← needs S3 bucket + IAM permissions
8. Deploy artifact → Tomcat EC2  ← needs S3 access from instance
9. ALB + HTTPS + ACM      ← needs Tomcat instances as targets
10. GoDaddy DNS → ALB     ← needs ALB endpoint
11. Verify end-to-end     ← needs everything above working
12. Auto Scaling Group    ← added LAST after verification
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Core Problem → Solution Chain

```
On-prem pain:
  Multiple teams + Manual processes + Scaling difficulty + High cost + Time waste
       │
       ▼
Cloud solution:
  Pay-as-you-go + Elasticity + Automation + Managed services + IaC
       │
       ▼
Strategy:
  Lift and Shift (move first, modernize later)
```

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## Reusable Engineering Patterns

| Pattern                                        | Where It Appears                                                            |
| ---------------------------------------------- | --------------------------------------------------------------------------- |
| **Layered Security (Defense in Depth)**        | Three security groups, each allowing traffic only from the layer above      |
| **Name-Based Decoupling**                      | Route 53 DNS names instead of hardcoded IPs for backend discovery           |
| **Artifact Pipeline (Build → Store → Deploy)** | Local build → S3 → Tomcat EC2                                               |
| **Stabilize → Then Automate**                  | Full stack verified before Auto Scaling is added                            |
| **Controller/Worker**                          | ALB (controller/router) → Tomcat instances (workers)                        |
| **Managed Service Substitution**               | Nginx → ALB, local DNS → Route 53 (replace self-managed with cloud-managed) |
| **Elastic Capacity (Scale to Demand)**         | Auto Scaling Group adjusts Tomcat count to match load                       |
| **Infrastructure as Code**                     | User data bash scripts automate instance setup at boot                      |
| **Centralized Artifact Storage**               | S3 as single source of truth for deployable artifacts                       |

 [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

## One-Line System Reconstruction

> **vProfile is a multi-tier Java app lifted from local VMs to AWS, where an ALB with ACM handles HTTPS ingress, routes to Auto Scaled Tomcat instances, which discover MySQL/Memcache/RabbitMQ backends via Route 53 private DNS — all isolated by three layered security groups, with artifacts flowing through S3.** [\[132. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/132.%20Introduction.txt)

***

This completes the full reconstruction. All three sections are designed to work together: **Theory** builds understanding, **Practical** builds execution confidence, and the **Mental Compression Map** enables rapid recall and reconstruction weeks or months later. Let me know if you'd like any section expanded or adjusted! 🚀
