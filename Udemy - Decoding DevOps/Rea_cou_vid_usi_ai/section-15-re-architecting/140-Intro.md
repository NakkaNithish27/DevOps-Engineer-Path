# Refactoring with AWS — vProfile Project (Re-Architecture Strategy)

**Source:** Video caption file — *"Refactoring with AWS"* (Introduction lecture from the vProfile AWS course) [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is Refactoring / Re-Architecture?

Refactoring (also called re-architecture) is a cloud migration strategy where you don't just move your existing application to the cloud as-is — you **redesign how the application's infrastructure is provided** by replacing self-managed services with cloud-managed (PaaS and SaaS) equivalents. The application logic may remain largely the same, but the infrastructure underneath is fundamentally transformed. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

This is the **next evolution** beyond Lift and Shift. In the previous project, the vProfile application was lifted from local VMs and shifted onto AWS EC2 instances — but you still had to manage those EC2 instances yourself: install software, configure services, handle scaling, manage backups, troubleshoot OS-level issues. The infrastructure burden was reduced but not eliminated. Refactoring goes further by offloading that remaining burden to AWS-managed services. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

The purpose of refactoring is to **boost agility and improve business continuity**. Specifically, it enables you to add new features more easily, scale effectively without manual intervention, and achieve better performance — all while dramatically reducing the number of teams and operational effort required. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.2 — The Problem: Operational Overhead Even After Cloud Migration

The starting scenario is familiar: application services (databases, application servers, web servers, network services like DNS and DHCP) are running on physical machines, virtual machines, or even cloud machines like EC2 instances. Managing all of this requires multiple specialized teams — cloud computing team, virtualization team, data center operations team, monitoring team, sys admin team, and others. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

The core pain points remain even if you've already done a Lift and Shift to the cloud:

**Too much operational overhead.** Even on EC2, you're still responsible for OS patching, service installation, configuration management, health monitoring, and troubleshooting at the instance level. Teams are still "struggling for uptime and regular scaling requirements." [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**Capital and operational expenditure.** If still using an on-premises data center, there's upfront capital expenditure for hardware plus ongoing operational costs. Even on EC2 (IaaS), there's continuous management cost in terms of human effort.

**Manual and hard-to-automate processes.** Even with virtualization, automating the full lifecycle of services running on VMs is difficult and expensive to maintain. These processes remain time-consuming.

The key insight the video presents: simply moving to cloud infrastructure (IaaS / EC2) solves the hardware procurement problem but doesn't solve the **operational management problem**. You've shifted *where* the servers run, but you're still managing servers. Refactoring eliminates the server management layer itself. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.3 — The Solution: PaaS and SaaS Instead of IaaS

Instead of using Infrastructure as a Service (IaaS) — where you get raw virtual machines and manage everything on top — the refactoring approach uses **Platform as a Service (PaaS)** and **Software as a Service (SaaS)** offerings. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**IaaS (what Lift and Shift used):** You get a VM (EC2). You install the OS, the database, the application server, configure networking, manage scaling, handle backups — everything above the hypervisor is your responsibility.

**PaaS (what Refactoring uses):** You get a managed platform. For example, Amazon RDS gives you a database platform — you choose the database engine, specify the size, and the database is "up and running in no time." AWS handles the installation, patching, backups, replication, and scaling of the database infrastructure. You only interact with the database as a consumer, not as an administrator. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**SaaS:** Fully managed services where you consume functionality without managing any infrastructure at all.

The advantages of PaaS/SaaS services highlighted in the video:

* **Easy to manage** — the cloud vendor handles most operational work
* **Flexible and elastic** — scaling is mostly handled by the vendor
* **Pay as you go** — no upfront commitment
* **Infrastructure as Code** — cloud-managed services can be defined and deployed through code
* **Massive automation potential** — deployment, scaling, monitoring, and recovery can all be automated
* **Small teams needed** — you don't need large dedicated teams for each service layer [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

The summary: refactoring gives you "easy infrastructure to manage, very good performance, very convenient to scale, and you will not need huge teams to manage all this." [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.4 — Service-by-Service Replacement: From Self-Managed to AWS-Managed

This is the architectural core of the project. Each self-managed service from the previous Lift and Shift project is replaced with an AWS-managed equivalent. Understanding each replacement and *why* it's better is essential. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

### Elastic Beanstalk → Replaces Tomcat on EC2 + Manual ELB + Manual Auto Scaling + Manual S3

In the Lift and Shift project, the Tomcat application ran on an EC2 instance, the Application Load Balancer was created manually, the Auto Scaling Group was configured manually, and the artifact was stored in S3 and deployed manually. **Elastic Beanstalk wraps all of this into a single managed service.** [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

Beanstalk "will in turn create an EC2 instance and host our application on it. We don't need to manage this instance manually. Beanstalk service will take care of it." Additionally, Beanstalk automatically provisions a load balancer, an auto scaling group, and an S3 bucket for artifact storage. The entire frontend tier — instance, load balancing, scaling, artifact storage — becomes a single managed environment. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

A critical capability: with Beanstalk, deploying a new version of your application becomes as simple as "clicking a button" — uploading the new artifact to the Beanstalk environment. No SSH-ing into instances, no manual file copying, no service restarts. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

🔍 **Deep Dive:**
Beanstalk doesn't eliminate EC2 instances — it **abstracts their management**. Underneath, there are still EC2 instances, EBS volumes, security groups, an ALB, and an ASG. The difference is that Beanstalk creates, configures, monitors, and manages all of these for you. You interact with the Beanstalk environment as a single unit, not with individual infrastructure components. However, the key pair creation step still exists because "in case you need to login" — Beanstalk doesn't prevent SSH access, it just makes it rarely necessary. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

### Amazon RDS → Replaces MySQL on EC2

In Lift and Shift, MySQL ran on an EC2 instance that you managed yourself — installation, configuration, backups, patching, scaling were all your responsibility. **Amazon RDS provides a managed database platform.** You choose the database engine (MySQL, PostgreSQL, etc.), specify requirements, and the database is operational. Scaling is easy. Backups are automatic. The video emphasizes: "Regular backups will be taken automatically. And so many more amazing things with it." [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

### Amazon ElastiCache → Replaces Memcache on EC2

Instead of installing and managing Memcache on an EC2 instance, you use ElastiCache — a managed caching service. AWS handles the cache cluster provisioning, patching, monitoring, and failover. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

### Amazon MQ (ActiveMQ) → Replaces RabbitMQ on EC2

Instead of installing and managing RabbitMQ on an EC2 instance, you use Amazon MQ with the ActiveMQ engine — a managed message broker service. The video notes the engine change: ActiveMQ "in place of RabbitMQ." While both are message brokers, the managed service uses ActiveMQ as the engine. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

### Amazon Route 53 → DNS Service

Route 53 continues to serve as the DNS service, same as in the Lift and Shift project. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

### Amazon CloudFront → Content Delivery Network (NEW)

This is a **new service** not present in the Lift and Shift project. CloudFront is a Content Delivery Network (CDN) that caches content at edge locations around the world. The video explains: "If you have a global audience, then using CloudFront for content delivery network will be very easy and convenient." [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

CloudFront sits **in front of the load balancer** in the request flow. Users hit CloudFront first, which serves cached content from the nearest edge location. Requests that aren't cached are forwarded to the ALB (in Beanstalk), which routes them to the application instances. This reduces latency for global users and offloads traffic from the origin servers. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

### Amazon CloudWatch Alarms → Monitoring and Auto Scaling Triggers (NEW)

Another new component: CloudWatch Alarms monitor the auto scaling group within Beanstalk and trigger scale-out/scale-in events based on metrics. In the Lift and Shift project, this was configured manually in the ASG scaling policy. In Beanstalk, CloudWatch integration is part of the managed environment. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.5 — Architectural Design: The Request Flow

The full request flow in the refactored architecture introduces two new layers compared to Lift and Shift — CloudFront at the front and managed backend services at the back. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**The complete request path:**

The user accesses a URL. This URL is resolved by **Amazon Route 53** to an endpoint. That endpoint belongs to **Amazon CloudFront**, the CDN, which caches content to serve the global audience. From CloudFront, the request is forwarded to the **Application Load Balancer**, which is part of the **Elastic Beanstalk** environment. The ALB forwards the request to **EC2 instances** running Tomcat, which are in an **Auto Scaling Group** — all managed by Beanstalk. **CloudWatch Alarms** monitor the ASG and trigger scaling events. The application artifact is stored in an **S3 bucket** and can be deployed with a single click. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

For backend access, the Tomcat application connects to **Amazon MQ** (replacing RabbitMQ), **Amazon ElastiCache** (replacing Memcache), and **Amazon RDS** (replacing MySQL). All backend services are in their own security group. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

The critical architectural shift from Lift and Shift: the frontend tier (Tomcat + LB + ASG + S3) is now a **single Beanstalk environment** rather than individually managed components, and the backend tier uses **managed services** (RDS, ElastiCache, Amazon MQ) rather than software installed on EC2 instances. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.6 — The Beanstalk Security Group Relationship

One of the most important operational details in the architecture is **how security groups connect Beanstalk to the backend services**. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

When Beanstalk creates its environment, it automatically creates security groups for its EC2 instances and its load balancer. You don't control these security groups at creation time — Beanstalk generates them. The backend services (RDS, ElastiCache, Amazon MQ) are placed in a **backend security group** that you create manually before Beanstalk exists. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

The problem: at the time you create the backend security group, the Beanstalk security group doesn't exist yet (because you haven't created the Beanstalk environment). So you **cannot** set up the correct inbound rules on the backend security group at creation time. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

The solution: the execution flow explicitly includes a step — **after** Beanstalk is created — to go back and **update the backend security group** to allow traffic from the Beanstalk instance security group. This is a sequential dependency that cannot be avoided: backend SG → create backend services → create Beanstalk → update backend SG with Beanstalk SG reference. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

Additionally, the backend services need to communicate with **each other** (e.g., the application on Beanstalk connects to RDS, which may need to interact with ElastiCache in some configurations). So the backend security group also needs a rule allowing **internal traffic** — traffic from the backend security group to itself. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.7 — RDS Database Initialization Pattern

Amazon RDS provides a managed database instance, but it gives you an **empty database**. The vProfile application requires a specific database schema with tables and initial data. RDS doesn't allow direct SSH access to the database server (it's managed), so you cannot log into the RDS machine to run initialization scripts. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

The solution is a **jump box pattern**: launch a temporary EC2 instance, use it to connect to the RDS endpoint via MySQL client, run the initialization SQL scripts, and then (implicitly) terminate the jump box. This is how you interact with managed database services that don't expose OS-level access. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.8 — Health Check Customization in Beanstalk

Beanstalk performs health checks on the application to determine if instances are healthy. By default, it checks the root path (`/`). However, the vProfile application's actual entry point is `/login` — the application "returns to page at /login." If the health check hits `/` and gets a redirect or error, Beanstalk will think the application is unhealthy even though it's working perfectly. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

Therefore, the health check path in Beanstalk must be changed to `/login` so it matches the application's actual response behavior. This is a small but critical configuration detail — a mismatch between health check path and application behavior causes false-negative health results, leading to instances being marked unhealthy and potentially replaced in a loop. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.9 — Artifact Building with Backend Endpoints

In the Lift and Shift project, backend services were discovered via Route 53 private DNS names. In the refactored architecture, backend services are AWS-managed and each has its own **endpoint** — RDS has an endpoint, Amazon MQ has an endpoint, ElastiCache has an endpoint. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

These endpoints must be fed into the application's **properties file** (application configuration) before the artifact is built. The build sequence is therefore: first create all backend services → collect their endpoints → update the application properties file with these endpoints → build the artifact → deploy to Beanstalk. This is a strict data dependency — you cannot build the artifact until all backend endpoints are known. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## 1.10 — HTTPS and SSL via Beanstalk's ELB + CloudFront

The architecture has **two layers** of HTTPS/SSL:

1. **CloudFront** — configured with an SSL certificate for the public-facing URL. Users connect to CloudFront over HTTPS.
2. **Beanstalk's ELB** — a 443 HTTPS listener is added to the load balancer. The video explicitly states this listener must be added manually because Beanstalk's default configuration may not include HTTPS.

CloudFront receives the user request (HTTPS), then forwards it to the Beanstalk ELB (which can also be HTTPS). This provides encryption at both the CDN layer and the origin layer. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are re-architecting the vProfile application from the Lift and Shift setup (EC2-based, manually managed) to a fully managed AWS architecture. The final outcome: Elastic Beanstalk manages the entire frontend tier (Tomcat + ALB + ASG + S3), backend services run on RDS, ElastiCache, and Amazon MQ (all managed), CloudFront serves global users via CDN, and the entire stack requires minimal operational management. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Execution Flow Overview

The video defines a precise execution sequence with important dependency ordering: [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

```
 1. Login to AWS Account
 2. Create Key Pair (for Beanstalk EC2 instance SSH access)
 3. Create Security Group for backend services
 4. Create RDS instance
 5. Create ElastiCache cluster
 6. Create Amazon MQ (ActiveMQ) broker
 7. Create Elastic Beanstalk Environment
 8. Update backend Security Group:
    a. Allow traffic from Beanstalk instance SG
    b. Allow internal traffic (backend SG to itself)
 9. Initialize RDS database (via temporary EC2 jump box)
10. Change Beanstalk health check to /login
11. Add HTTPS (443) listener to Beanstalk's ELB
12. Build artifact with backend endpoint information
13. Deploy artifact to Beanstalk environment
14. Create CloudFront distribution with SSL certificate
15. Update DNS (GoDaddy or Route 53 public zone) with CloudFront/ELB endpoint
16. Test from the URL
```

***

### Step 1: Login to AWS Account

**What we are doing:** Accessing the AWS Management Console to begin all provisioning work. This is the entry point for the entire project. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 2: Create Key Pair

**What we are doing:** Generating an SSH key pair that will be associated with the EC2 instance Beanstalk launches.

**Why:** Beanstalk creates and manages EC2 instances automatically, but you may still need SSH access for troubleshooting or inspection. The key pair enables this access. In normal operations, you rarely need to SSH into Beanstalk instances — but having the key pair available is a safety measure. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 3: Create Backend Security Group

**What we are doing:** Creating a single security group that will contain all backend services — RDS, ElastiCache, and Amazon MQ.

**Why:** All backend services are grouped together because they need to be accessed by the Beanstalk application tier and may need to communicate with each other. A single security group simplifies this by allowing you to set up internal traffic rules once. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**Important operational note:** At this point, you **cannot** add the inbound rule allowing traffic from Beanstalk's security group because Beanstalk hasn't been created yet. You'll come back to update this security group in Step 8. For now, create the security group with basic rules (internal communication between backend services). [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 4: Create RDS Instance

**What we are doing:** Provisioning a managed MySQL database instance via Amazon RDS.

**Why:** Replaces the manually managed MySQL on EC2 from the Lift and Shift project. RDS handles installation, patching, backups, and scaling.

**Operational details:**

* Choose MySQL as the database engine.
* Configure instance size, storage, credentials.
* Place the instance in the **backend security group** created in Step 3.
* Note the **RDS endpoint** once the instance is available — you will need this for the application properties file in Step 12. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**How to verify:** RDS dashboard shows the instance status as "Available." The endpoint is displayed in the instance details.

⚠️ **Expert Note:**
RDS instance creation can take significant time (10-20+ minutes). Plan your workflow to create all backend services (RDS, ElastiCache, Amazon MQ) and proceed with other tasks while they provision. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 5: Create ElastiCache Cluster

**What we are doing:** Provisioning a managed caching cluster via Amazon ElastiCache.

**Why:** Replaces Memcache on EC2. ElastiCache handles cache node management, patching, and failover.

**Operational details:**

* Choose Memcached (or Redis) as the engine, matching the application's caching needs.
* Place in the **backend security group**.
* Note the **ElastiCache endpoint** once available — needed for the application properties file. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 6: Create Amazon MQ Broker

**What we are doing:** Provisioning a managed message broker via Amazon MQ with the ActiveMQ engine.

**Why:** Replaces RabbitMQ on EC2. Amazon MQ handles broker management, patching, and availability.

**Operational details:**

* Choose ActiveMQ as the engine.
* Place in the **backend security group**.
* Note the **Amazon MQ endpoint** once available — needed for the application properties file. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 7: Create Elastic Beanstalk Environment

**What we are doing:** Creating a Beanstalk environment that will automatically provision the entire frontend tier — EC2 instance(s) running Tomcat, Application Load Balancer, Auto Scaling Group, and S3 bucket.

**Why:** This single action replaces multiple manual steps from the Lift and Shift project (creating EC2 instances, configuring ALB, setting up ASG, managing S3 deployment). Beanstalk abstracts all of this into one managed environment.

**Operational details:**

* Choose the platform (Tomcat/Java).
* Associate the key pair from Step 2.
* Beanstalk will automatically create: EC2 instance(s), an ALB, an ASG, security groups for the instance and LB, and an S3 bucket. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**What happens internally:** Beanstalk provisions a CloudFormation stack (implicitly) that creates all the resources. It also creates its own security groups — these are the security groups you'll reference in the next step.

**How to verify:** Beanstalk dashboard shows the environment health as "Ok" (green). You can see the auto-generated ALB, ASG, and EC2 instances in the respective AWS console sections.

**Connection to flow:** Once Beanstalk is created and its security group IDs are known, you can proceed to update the backend security group (Step 8). [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 8: Update Backend Security Group

**What we are doing:** Two updates to the backend security group:

**8a — Allow traffic from Beanstalk instance security group:**

* Go to the backend security group.
* Add an inbound rule allowing traffic on the relevant service ports (MySQL 3306, Memcache 11211, ActiveMQ 61616/8162, etc.) from the **Beanstalk instance security group ID** as the source.
* This is the step that **connects the frontend to the backend** at the network level. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**8b — Allow internal traffic within backend security group:**

* Add an inbound rule allowing all traffic (or relevant ports) from the **backend security group itself** as the source.
* This allows backend services to communicate with each other (e.g., if the application flow requires it). [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**Why this step is deferred:** As explained in Theory section 1.6, the Beanstalk security group doesn't exist until Beanstalk is created. This is a sequential dependency that forces the update to happen after Step 7.

**How to verify:** Check the backend security group's inbound rules — you should see entries referencing both the Beanstalk instance SG and the backend SG itself. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 9: Initialize RDS Database

**What we are doing:** Connecting to the RDS instance and running SQL scripts to create the vProfile database schema and load initial data.

**Why:** RDS provides an empty database engine. The vProfile application needs specific tables and data to function.

**Execution:**

1. Launch a temporary **EC2 instance** (jump box) — this is needed because RDS doesn't provide OS-level access.
2. SSH into the EC2 instance.
3. Install the MySQL client (if not already present).
4. Connect to the RDS endpoint using the MySQL client with the credentials configured during RDS creation.
5. Run the database initialization SQL scripts (schema creation, data insertion).
6. Verify the database is properly initialized.
7. (Implicitly) The jump box can be terminated after initialization. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**Connection to flow:** The database must be initialized before the application can function. This step must be completed before deploying the artifact (Step 13).

***

### Step 10: Change Beanstalk Health Check to /login

**What we are doing:** Updating the Beanstalk health check path from the default (`/`) to `/login`.

**Why:** The vProfile application's entry point is `/login`. If the health check probes `/` and doesn't get a successful response, Beanstalk marks the instance as unhealthy — even though the application is working correctly at `/login`. Changing the health check path prevents false-negative health assessments. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**How to verify:** After changing, check the Beanstalk environment health dashboard — instances should report as healthy.

**Common mistake:** Forgetting this step and deploying the artifact, then seeing Beanstalk continuously mark instances as unhealthy and potentially terminate/replace them in a loop.

***

### Step 11: Add HTTPS Listener to Beanstalk's ELB

**What we are doing:** Adding a port 443 (HTTPS) listener to the Application Load Balancer that Beanstalk created.

**Why:** By default, Beanstalk's ELB may only have an HTTP listener. For production use and for CloudFront integration with SSL, the ELB needs to accept HTTPS connections.

**Operational details:**

* Navigate to the Beanstalk environment's load balancer configuration (or directly to the EC2 → Load Balancers console).
* Add a listener on port 443 with an SSL certificate (from ACM). [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

### Step 12: Build Artifact with Backend Endpoints

**What we are doing:** Compiling the vProfile application source code into a deployable artifact (WAR file), with the correct backend service endpoints configured.

**Why:** The application needs to know where RDS, ElastiCache, and Amazon MQ are located. These are specified in the **application properties file** within the source code.

**Execution:**

1. Collect the endpoints: RDS endpoint, ElastiCache endpoint, Amazon MQ endpoint (all from their respective AWS console pages).
2. Update the `application.properties` file (or equivalent configuration file) with these endpoints.
3. Build the artifact (e.g., using Maven: `mvn install`). [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**Critical dependency:** All three backend services must be created and their endpoints available before this step. This is why backend services are created early in the execution flow (Steps 4-6).

**Connection to flow:** The built artifact is deployed to Beanstalk in the next step.

***

### Step 13: Deploy Artifact to Beanstalk

**What we are doing:** Uploading the compiled WAR file to the Beanstalk environment.

**Why:** This is the actual application deployment. Beanstalk handles the rest — distributing the artifact to instances, restarting Tomcat, and verifying the deployment.

**Operational simplicity:** The video emphasizes this is as simple as "clicking a button" — upload the artifact through the Beanstalk console, and Beanstalk deploys it to all instances in the environment. No SSH, no manual file copying, no service restarts. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**How to verify:** The Beanstalk environment health remains green. Accessing the application URL shows the vProfile login page.

***

### Step 14: Create CloudFront Distribution

**What we are doing:** Setting up a CloudFront CDN distribution that sits in front of the Beanstalk environment.

**Why:** CloudFront caches content at edge locations globally, reducing latency for users far from the AWS region where the application runs. It also provides an additional SSL termination point.

**Operational details:**

* Create a CloudFront distribution with the Beanstalk ELB endpoint as the **origin**.
* Attach an **SSL certificate** for HTTPS. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**Connection to flow:** CloudFront provides its own endpoint (a `*.cloudfront.net` domain), which becomes the entry point for user traffic. DNS (Step 15) will point to this endpoint.

***

### Step 15: Update DNS

**What we are doing:** Creating a DNS record (in GoDaddy or Route 53 public DNS zones) that points the application's public domain name to the CloudFront distribution endpoint (or directly to the Beanstalk ELB endpoint). [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

**Why:** Users access the application via a human-readable URL, not via auto-generated AWS endpoints.

***

### Step 16: Test from the URL

**What we are doing:** End-to-end verification of the entire refactored stack.

**Verification path:** User URL → Route 53 → CloudFront → Beanstalk ALB → Tomcat EC2 (ASG) → Backend services (RDS, ElastiCache, Amazon MQ).

**Checks:** Application loads, login works, data is retrieved from RDS, caching functions via ElastiCache, messaging works via Amazon MQ. [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
PROJECT:   Refactoring with AWS — vProfile
STRATEGY:  Re-architecture / Refactoring (NOT Lift and Shift)
CORE IDEA: Replace self-managed services with AWS PaaS/SaaS managed services
EVOLUTION: Lift & Shift (IaaS) → Refactoring (PaaS/SaaS)
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Lift & Shift → Refactoring: Service Replacement Map

```
FRONTEND:
  Tomcat on EC2 (manual)          → Elastic Beanstalk (managed)
  ALB (manual)                    → Beanstalk ALB (auto-created)
  ASG (manual)                    → Beanstalk ASG (auto-created)
  S3 artifact (manual upload)     → Beanstalk S3 (one-click deploy)
  CloudWatch scaling (manual)     → Beanstalk CloudWatch Alarms (auto)
  [none]                          → CloudFront CDN (NEW)

BACKEND:
  MySQL on EC2                    → Amazon RDS (managed)
  Memcache on EC2                 → Amazon ElastiCache (managed)
  RabbitMQ on EC2                 → Amazon MQ / ActiveMQ (managed)

DNS:
  Route 53                        → Route 53 (same)
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Architecture: Request Flow

```
[User]
  │
  ▼ (URL resolution)
[Route 53]
  │
  ▼ (HTTPS)
[CloudFront CDN]  ← SSL cert, global edge caching
  │
  ▼
┌──────────────────────────────────────────┐
│         ELASTIC BEANSTALK ENVIRONMENT    │
│                                          │
│  [ALB] ← HTTPS listener (443)           │
│    │                                     │
│    ▼                                     │
│  [EC2 Tomcat] ← Auto Scaling Group      │
│       ↕        ← CloudWatch Alarms      │
│  [S3 Bucket]   ← artifact storage       │
└──────────────────────────────────────────┘
         │
         ▼ (service ports, via backend SG)
┌──────────────────────────────────────────┐
│       BACKEND SECURITY GROUP             │
│                                          │
│  [Amazon RDS]        ← MySQL (managed)   │
│  [Amazon ElastiCache]← Memcache (managed)│
│  [Amazon MQ]         ← ActiveMQ (managed)│
└──────────────────────────────────────────┘
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Security Group Dependency Problem

```
TIMELINE:

  T1: Create backend SG                    ← Beanstalk SG doesn't exist yet
  T2: Create RDS, ElastiCache, Amazon MQ   ← placed in backend SG
  T3: Create Beanstalk                     ← auto-creates its own SG
  T4: Update backend SG:
      ├── Allow inbound from Beanstalk instance SG  (frontend → backend)
      └── Allow inbound from backend SG itself       (backend ↔ backend)

REASON: Circular dependency — backend SG needs Beanstalk SG ID,
        but Beanstalk SG is created only when Beanstalk is created.
SOLUTION: Deferred update (create SG first, update rules after Beanstalk exists)
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## RDS Initialization: Jump Box Pattern

```
RDS = managed → no OS access → can't run SQL scripts directly

WORKAROUND:
  Launch temp EC2 (jump box)
    → SSH into EC2
      → MySQL client connects to RDS endpoint
        → Run SQL init scripts
          → Schema + data loaded
            → (terminate jump box)
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Health Check Customization

```
DEFAULT:    Beanstalk checks /        → vProfile doesn't respond there → UNHEALTHY ❌
CORRECTED:  Beanstalk checks /login   → vProfile responds correctly   → HEALTHY ✅

RISK IF MISSED: Instance marked unhealthy → ASG replaces → new instance also "unhealthy" → replacement loop
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Artifact Build Dependency Chain

```
Create RDS          → get RDS endpoint
Create ElastiCache  → get ElastiCache endpoint       ALL MUST EXIST
Create Amazon MQ    → get Amazon MQ endpoint    ─────  BEFORE BUILD
                          │
                          ▼
              Update application.properties
                          │
                          ▼
                Build artifact (mvn install)
                          │
                          ▼
              Deploy to Beanstalk (one-click)
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Execution Sequence (Full Dependency Chain)

```
 1. AWS Login
 2. Key Pair                       ← for Beanstalk EC2 SSH access
 3. Backend SG                     ← needed before backend services
 4. RDS                            ← in backend SG, takes time
 5. ElastiCache                    ← in backend SG, takes time
 6. Amazon MQ                      ← in backend SG, takes time
 7. Beanstalk Environment          ← creates ALB, ASG, EC2, SG, S3
 8. Update Backend SG              ← add Beanstalk SG + self-reference
 9. Initialize RDS (jump box)      ← needs RDS available
10. Health check → /login          ← needs Beanstalk environment
11. Add HTTPS to Beanstalk ELB     ← needs Beanstalk ELB + ACM cert
12. Build artifact (with endpoints)← needs all backend endpoints
13. Deploy artifact to Beanstalk   ← needs artifact + Beanstalk env
14. CloudFront + SSL               ← needs Beanstalk ELB as origin
15. DNS update                     ← needs CloudFront endpoint
16. Test end-to-end                ← needs everything
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## IaaS vs. PaaS/SaaS: Core Distinction

```
IaaS (Lift & Shift):
  You get: raw VM
  You manage: OS, software, config, scaling, backups, patching, monitoring
  Teams needed: many

PaaS/SaaS (Refactoring):
  You get: managed platform/service
  You manage: application code + configuration
  Vendor manages: infrastructure, scaling, backups, patching, availability
  Teams needed: few
```

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## Reusable Engineering Patterns

| Pattern                            | Manifestation                                                                    |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| **Platform Abstraction**           | Beanstalk abstracts EC2 + ALB + ASG + S3 into a single managed unit              |
| **Managed Service Substitution**   | MySQL→RDS, Memcache→ElastiCache, RabbitMQ→Amazon MQ                              |
| **Deferred Security Binding**      | Create backend SG first, update rules after dependent service (Beanstalk) exists |
| **Jump Box / Bastion**             | Temp EC2 to reach managed services (RDS) that don't expose OS access             |
| **CDN Front-Loading**              | CloudFront placed before origin to cache + reduce latency globally               |
| **Health Check Alignment**         | Match probe path to actual application entry point (`/login`)                    |
| **Endpoint-Driven Configuration**  | Collect managed service endpoints → inject into app config → build               |
| **One-Click Deployment**           | Beanstalk reduces deploy to artifact upload (no SSH, no manual steps)            |
| **Operational Overhead Reduction** | Core motivation — fewer teams, less manual work, same (or better) outcome        |

 [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

## One-Line System Reconstruction

> **vProfile is re-architected from EC2-based Lift & Shift to AWS PaaS/SaaS: Elastic Beanstalk manages the entire frontend tier (Tomcat + ALB + ASG + S3 + CloudWatch), backend uses RDS + ElastiCache + Amazon MQ (all managed), CloudFront provides global CDN, and the security group dependency is resolved by deferred update after Beanstalk creates its SG.** [\[140-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/140-introduction.txt)

***

This completes the full reconstruction of the Refactoring with AWS Introduction lecture. It builds directly on top of the Lift and Shift material — the same vProfile application, same logical architecture, but with the infrastructure layer fundamentally upgraded from IaaS to PaaS/SaaS. Let me know if you'd like any section expanded or adjusted! 🚀
