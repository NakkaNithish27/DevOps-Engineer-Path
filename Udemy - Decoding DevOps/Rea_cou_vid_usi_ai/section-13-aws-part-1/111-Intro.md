# 🎓 Deep Learning Material: AWS Introduction — Global Infrastructure, Service Landscape & Operational Foundations

*Reconstructed from video lecture captions and accompanying course slides*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 AWS: The Dominant Public Cloud Provider

AWS (Amazon Web Services) is the **biggest public cloud computing provider** in the world, holding more than **46 percent market share** at the time of the lecture (December 2020). The instructor frames this upfront to establish why learning AWS matters: it is the platform most likely to be encountered in real infrastructure work. Because of its dominance, AWS has built the most extensive global infrastructure of any cloud provider, which directly affects how you design, deploy, and operate systems on it. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

The key word here is **public cloud** — meaning AWS owns and operates the physical data centers, hardware, networking, and cooling, and you rent computing resources on demand. You don't build or manage physical infrastructure. You consume it as a service. This is the fundamental value proposition: instead of building your own data centers around the world, you leverage AWS's existing global infrastructure. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

***

## 1.2 AWS Global Infrastructure: The Three-Level Hierarchy

The physical foundation of AWS is organized into a clear hierarchy: **Regions → Availability Zones → Data Centers**. Understanding this hierarchy is essential because almost every decision you make on AWS — where to place your servers, how to design for high availability, how to meet compliance requirements — is rooted in this structure. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

### Regions

A **Region** is a geographic area — typically a country or part of a country — where AWS has established its presence. As of the lecture, AWS has **24 geographic regions** with **5 more announced** (India/Hyderabad, Indonesia, Japan, Spain, Switzerland).  Each region is a fully independent cluster of infrastructure. Your data in the North California region does not automatically go to any other region. Regions are **isolated from each other by design** — this is fundamental to both data residency and disaster recovery. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

When you select a region in the AWS console, all resources you create (virtual machines, databases, storage) are physically located in data centers within that region. The instructor demonstrates this: *"When you select a particular region, right now it's North California. So it will be using the zones in the North California region. So my data, whatever data I am storing over here, is going to North California data centers."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

### Availability Zones (AZs)

Within each region, there are multiple **Availability Zones**. An Availability Zone is **not** a single data center — it is a **cluster of multiple data centers** that are physically close together and connected with high-bandwidth, low-latency networking. The instructor emphasizes: *"One zone is multiple data centers. A single zone means multiple data centers, clustered data centers."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

Each region has a **minimum of 2 zones** and the instructor has seen up to **6 zones** in a single region. As of the lecture, there are **77 Availability Zones globally** with **15 more announced**. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

The purpose of having multiple AZs within a region is **high availability**. If you distribute your infrastructure across multiple zones — for example, 2 web servers in zone A and 2 web servers in zone B — and one zone experiences a failure (power outage, network issue, natural disaster affecting that cluster of data centers), the other zone keeps serving traffic. The slides state this explicitly: *"If you distribute your instances across multiple Availability Zones and one instance fails, you can design your application so that an instance in another Availability Zone can handle requests."* [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

When you launch a virtual machine (called an **instance** in AWS), you can **select the Availability Zone** yourself, or you can **let AWS choose one** for you. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

### Data Centers

At the bottom of the hierarchy are the actual **physical data centers** — buildings with servers, storage, networking equipment, power systems, cooling, and physical security (surveillance, controlled access). These are grouped into Availability Zones. You never directly interact with individual data centers — the Availability Zone is the lowest level of abstraction exposed to you as a user. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

🔍 **Deep Dive:**
The relationship between these three levels creates a layered isolation model. Data centers within an AZ are close enough for synchronous replication (millisecond latency). AZs within a region are far enough apart to survive localized failures but close enough for low-latency communication. Regions are fully independent — cross-region communication requires explicit configuration (replication, VPN, etc.). This layered model allows you to choose your level of redundancy based on your requirements and budget.

***

## 1.3 Why Multiple Regions and Zones Exist: The Four Strategic Benefits

The instructor and slides identify four distinct reasons why AWS has built this distributed infrastructure, and each maps to a real engineering or business requirement: [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

**1. High Availability through Multiple Availability Zones.** By distributing your infrastructure across AZs within a single region, you survive zone-level failures. This is the most commonly used benefit — almost every production deployment should span multiple AZs. The instructor gives a concrete example: *"You can place 2 web servers in one zone and other 2 in the other zones. So if you have total 4 web servers, you can distribute them to get high availability. Even if a zone goes down or becomes slow, then other part of your infrastructure will still be up and running."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**2. Improving Continuity with Replication Between Regions (Disaster Recovery).** By replicating data and infrastructure across multiple regions, you can survive region-level catastrophes. The instructor adds an important caveat: *"This is not a feature that you can just enable. You have to do a lot of things when you are doing a disaster recovery in between two regions."*   Disaster recovery is an architectural effort, not a checkbox. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**3. Meeting Compliance and Data Residency Requirements.** Many projects have legal or regulatory requirements about where data must be stored. For example, European data protection laws may require that EU customer data stays in EU data centers. Having regions in different countries allows you to choose where your data physically resides. The instructor says: *"For some compliance reason, you don't want to keep it in US. You can probably go to European regions."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**4. Geographic Expansion.** If your business serves a global audience, you want your infrastructure close to your users for lower latency. Instead of building data centers worldwide, you simply deploy to the AWS region nearest to your user base. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

***

## 1.4 Additional Infrastructure Types: Local Zones, Edge Locations, and Ground Stations

Beyond the core Region/AZ hierarchy, the instructor mentions additional infrastructure types visible on the infrastructure.aws globe: [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**Local Zones** are a newer type of AWS infrastructure that places **compute, storage, database, and some other services closer to large populations** — like in a big city where there are many customers. They extend a region's capabilities to a geographic location that doesn't have a full region nearby, reducing latency for users in that area. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**Points of Presence (Edge Locations)** are for AWS's **Content Delivery Network (CDN)** — specifically CloudFront. These are **very small data centers** compared to AZs, and their purpose is to **cache data** closer to end users. When users request content, it's served from the nearest edge location rather than traveling all the way to the origin region. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**Ground Stations** and **Network** infrastructure are also visible on the globe but are mentioned only briefly. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

The instructor references a specific website for exploring all of this visually: **<https://infrastructure.aws/>** — an interactive 3D globe showing regions (yellow), upcoming regions (green), AZs, local zones, edge locations, and more. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

***

## 1.5 AWS Services: Scale, Categories, and the "Don't Get Scared" Principle

As of the lecture, AWS offers **175+ fully featured services**. The instructor immediately addresses the natural reaction to this overwhelming number: *"Really don't get scared by looking at the number of services. You don't have to learn all of them. It's based on what area you're working in, where is your expertise. Based on that, you will be using a particular service."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

He gives a concrete example: if you're a **system admin or DevOps engineer**, you'll use **EC2** (virtual machines). But you probably won't need **Amazon Bracket** (quantum technology) or media services or robotics services. AWS categorizes services by domain, and each user role only needs a subset. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

The course focuses on **SysOps and DevOps services**, which the instructor identifies as a **solid foundation** — once you understand these, learning other AWS services becomes much easier. The specific services mentioned for the course: [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

* **Compute:** EC2, Elastic Beanstalk
* **Storage:** S3, EFS, Glacier
* **Database:** RDS, ElastiCache
* **Networking:** VPC, CloudFront, Route 53
* **Developer Tools:** CodeCommit, CodeArtifact, CodeBuild, CodeDeploy, CodePipeline
* **Monitoring:** CloudWatch
* **Compliance services**

The instructor explicitly states the learning path logic: *"If you have good hands on the SysOps services of AWS, then you should be able to learn the DevOps services, the developer services, security services, networking services. Again then the path is based on your requirement."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

The slides provide additional context for many of these services (IAM, S3 details, EC2 details, EBS, ELB, Auto Scaling, VPC, Route 53, etc.) which will be covered in subsequent lectures. [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

***

## 1.6 Region Selection: The Decision Framework

Choosing a region is one of the first decisions you make in any AWS project, and the instructor outlines the decision logic: [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**Option 1: You're told which region to use.** In many projects, the region is pre-decided based on compliance, existing infrastructure, or organizational policy. You simply use what you're told.

**Option 2: You choose based on requirements.** The factors include:

* **Compliance/data residency:** Legal requirements about where data must be stored
* **Audience proximity:** Deploy close to your users for lower latency
* **Cost:** Different regions have different pricing. The instructor specifically warns: *"Some other regions like Singapore, Mumbai, Tokyo are expensive compared to US region."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

For the course, the instructor recommends a **US-based region** because it's generally the cheapest, and since the course will occasionally exceed free tier limits, minimizing cost matters. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

***

## 1.7 The Free Tier and Cost Awareness

The instructor sets up a critical operational awareness: while the course uses **AWS Free Tier** as much as possible, there will be moments where free tier limits are exceeded and real money is spent. He makes three promises/warnings: [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

1. He will **alert** when costs are about to be incurred
2. He will show **how to clean up** after each exercise to stop charges
3. Using a US-based region helps minimize costs

The prerequisites (covered in a separate video) include: creating an AWS Free Tier account, setting a **billing alarm** (so you're notified if costs exceed a threshold), and setting up an **IAM user** (so you don't use the root account for daily work). [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

⚠️ **Expert Note:**
The billing alarm is not a luxury — it's a safety mechanism. Without it, you can accidentally leave resources running (an EC2 instance, a load balancer, an RDS database) and accumulate charges without realizing it. In a learning environment, this is especially dangerous because you're experimenting frequently. The cleanup-after-every-exercise discipline the instructor emphasizes is a real operational habit that prevents cost overruns in production too.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

This is an **orientation lecture** — we are not building a system yet. Instead, we are establishing the foundational knowledge and environment needed for all subsequent AWS labs. The practical outcome is: understanding how to navigate the AWS global infrastructure visualization, understanding the AWS Management Console layout, and being prepared with prerequisites (account, billing alarm, IAM user). [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

***

## Step 1: Prerequisites Verification

Before proceeding, ensure you have completed the prerequisites from the earlier video: [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

1. **AWS Free Tier account** — Created and active
2. **Billing alarm** — Set to notify you when costs exceed your threshold
3. **IAM user** — Created with appropriate permissions (you should log into the console with this IAM user, not the root account)

If any of these are not done, stop and complete them before continuing. The instructor is explicit: *"If you don't know what I'm talking about right now, then check the prerequisites video."* [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

***

## Step 2: Explore the AWS Global Infrastructure Globe

Navigate to: **<https://infrastructure.aws/>** [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt), [\[111.AWSSlides \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111.AWSSlides.pdf)

**What you'll see:** An interactive 3D globe showing AWS's entire global infrastructure.

**How to interact:**

* Use your cursor to **rotate the globe** and explore different geographic areas
* **Click on a Region** (yellow marker) — it will show you information about that region
* **Click on an Availability Zone** — it will show sample data center information, including security, surveillance, and uptime details
* **Look for green markers** — these indicate **upcoming regions** (e.g., Hyderabad was green/upcoming at the time of the lecture)

**What to observe:** [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

* Regions are spread across multiple continents — Americas, Europe, Asia, Middle East, Africa
* Each region contains multiple AZs (click to see how many — e.g., a region in China shows 3 AZs)
* Additional infrastructure types are color-coded: Local Zones, Points of Presence, Ground Stations, Network

**Why this matters:** This gives you a spatial mental model of where your infrastructure physically exists when you select a region. It also helps you understand proximity to your users and the scale of AWS's physical presence.

***

## Step 3: Log Into the AWS Management Console

Open your browser and navigate to the AWS Management Console. Log in with your **IAM user** credentials (not the root account). [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**Verification:** You should see the main console dashboard with the service search bar and service categories.

**Common mistake:** Logging in with the root account. The instructor explicitly says: *"Login into the AWS management console with an IAM user."*  The root account has unrestricted access and should be reserved for account-level operations only. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

***

## Step 4: Navigate the Service Categories

In the console, you'll see the full list of AWS services organized by category. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**What to observe:**

* There are **many** service categories: Compute, Storage, Database, Networking, Developer Tools, Machine Learning, Analytics, IoT, Robotics, Quantum Technology, Media Services, etc.
* Each category contains multiple services
* The sheer volume can be overwhelming — but remember, you only need the services relevant to your role

**Course-relevant services to locate:** [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

* **Compute:** EC2, Elastic Beanstalk
* **Storage:** S3, EFS, Glacier
* **Database:** RDS, ElastiCache
* **Networking:** VPC, CloudFront, Route 53
* **Developer Tools:** CodeCommit, CodeArtifact, CodeBuild, CodeDeploy, CodePipeline
* **Management & Monitoring:** CloudWatch

**Connection to flow:** Familiarizing yourself with where services live in the console saves time in every future lab.

***

## Step 5: Select a Region

In the top-right corner of the console, you'll see a **region selector** dropdown. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**How to choose:**

* For this course, select a **US-based region** (e.g., US East - N. Virginia, US West - N. California)
* **Why US:** US regions are generally the cheapest, and since some exercises will exceed free tier, this minimizes cost

**What happens when you select a region:** All services and resources displayed in the console are scoped to that region. If you create an EC2 instance in North California, it will only be visible when North California is selected. If you switch to Mumbai, you won't see it. [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

**Critical operational awareness:** If you "can't find" a resource you just created, check that you're in the correct region. This is one of the most common beginner mistakes on AWS.

⚠️ **Expert Note:**
Some AWS services are **global** (not region-scoped) — IAM, Route 53, CloudFront, and S3 bucket names are examples. But most infrastructure services (EC2, RDS, VPC, EBS) are region-scoped. Understanding which services are global vs. regional prevents confusion when navigating the console.

***

## Step 6: Cost Awareness Discipline

The instructor establishes an important operational pattern for the entire course: [\[111-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/111-introduction.txt)

1. **Before each lab:** Be aware of whether it uses free tier or costs money (the instructor will alert you)
2. **After each lab:** **Clean up all resources** — terminate instances, delete volumes, remove load balancers, etc.
3. **Ongoing:** Monitor your billing dashboard and billing alarm

**Why this discipline matters:** AWS charges by the hour/second for running resources. A forgotten t2.micro instance running 24/7 costs little, but a forgotten RDS instance or load balancer can accumulate significant charges over days. The cleanup habit must become automatic.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## AWS Identity

```
AWS = Largest public cloud provider (~46% market share)
175+ services | 24 regions | 77 AZs (as of Dec 2020)
You rent infrastructure → No physical data centers to manage
```

***

## Infrastructure Hierarchy

```
AWS Global Infrastructure
  └── Region (geographic area, e.g., North California)
        ├── Availability Zone A (cluster of data centers)
        ├── Availability Zone B (cluster of data centers)
        └── Availability Zone C (cluster of data centers)
             └── Multiple physical data centers (not directly exposed)

Min 2 AZs per region | Max ~6 AZs per region
1 AZ = multiple clustered data centers (NOT a single building)
```

***

## Additional Infrastructure Types

```
Local Zones      → Compute/storage closer to large populations (cities)
Edge Locations   → CDN cache (CloudFront) → tiny data centers → near users
Ground Stations  → Satellite connectivity
Network          → AWS backbone connectivity

Explore: https://infrastructure.aws/
```

***

## Four Strategic Benefits of Global Infrastructure

```
1. HIGH AVAILABILITY    → Distribute across AZs within a region
                          Zone fails → other zones keep serving
                          
2. DISASTER RECOVERY    → Replicate across regions
                          NOT a checkbox → requires architectural effort
                          
3. COMPLIANCE           → Data residency laws → choose region by country
                          EU data stays in EU regions
                          
4. GEOGRAPHIC EXPANSION → Deploy near your users → lower latency
                          No need to build your own data centers
```

***

## Region Selection Logic

```
GIVEN region by project/compliance? → Use it
CHOOSING yourself? →
  ├── Compliance: Where must data reside legally?
  ├── Audience: Where are your users?
  └── Cost: US regions cheapest; Singapore/Mumbai/Tokyo more expensive

For learning: Use US-based region (cheapest for free-tier overflows)
```

***

## Service Landscape (Course Focus)

```
175+ services → Don't learn all → Learn by ROLE

SysOps/DevOps Focus (this course):
  Compute:    EC2, Beanstalk
  Storage:    S3, EFS, Glacier
  Database:   RDS, ElastiCache
  Networking: VPC, CloudFront, Route 53
  Dev Tools:  CodeCommit, CodeArtifact, CodeBuild, CodeDeploy, CodePipeline
  Monitoring: CloudWatch
  
Learning path: SysOps → DevOps → Developer → Security → Networking
               (each builds on previous)
```

***

## Slides Reference Map (Future Lectures)

```
The course slides cover these services in detail (upcoming lectures):
  IAM         → Access control (users, roles, permissions, MFA, federation)
  S3          → Object storage (buckets, objects, 6 storage classes, lifecycle)
  EC2         → Virtual machines (AMI, instance types, EBS, tags, security groups, key pairs)
  EBS         → Block storage (5 types, snapshots, backup/restore)
  ELB         → Load balancing (Classic, Application, Network)
  CloudWatch  → Monitoring (metrics, events, logs, alarms → SNS notifications)
  Auto Scaling→ Dynamic capacity (launch templates, scaling policies, groups)
  RDS         → Managed databases (multi-AZ, read replicas, scaling)
  VPC         → Networking (subnets, public/private, NAT, IGW, NACL, peering)
  Route 53    → DNS (registration, routing, health checks)
  AWS CLI     → Command-line control
  CI/CD       → CodeCommit → CodeBuild → CodeDeploy → CodePipeline
```

***

## Prerequisites Checklist

```
□ AWS Free Tier account created
□ Billing alarm set (safety net against runaway costs)
□ IAM user created (never use root for daily work)
□ Log in with IAM user, NOT root
```

***

## Cost Awareness Pattern

```
BEFORE lab: Know if it exceeds free tier (instructor alerts)
DURING lab: Use US region (cheapest)
AFTER lab:  CLEAN UP everything (terminate, delete, remove)
ALWAYS:     Monitor billing dashboard + alarm

Forgotten resources → silent cost accumulation → billing surprise
```

***

## Key Operational Facts

```
Region scoping:  Most resources visible ONLY in the region where created
                 Can't find resource? → Check region selector (top-right)
                 
Global services: IAM, Route 53, CloudFront, S3 bucket names → NOT region-scoped

Instance = virtual machine in AWS terminology
AZ selection: Choose manually OR let AWS decide
```

***

## Core Mental Model

```
AWS = Global network of rented infrastructure
  ├── Organized: Regions → AZs → Data Centers
  ├── Purpose: HA (multi-AZ), DR (multi-region), Compliance, Expansion
  ├── Consumed: Via Console, CLI, or API
  └── Charged: By usage → cleanup is a survival habit

Your role determines your services (not all 175+)
SysOps foundation → unlocks all other AWS learning paths
```

***

This material captures every concept, infrastructure detail, service reference, operational advice, and cost warning from the lecture and supporting slides — structured for deep understanding (Theory), confident navigation (Practical), and rapid future recall (Compression Map). 🚀
