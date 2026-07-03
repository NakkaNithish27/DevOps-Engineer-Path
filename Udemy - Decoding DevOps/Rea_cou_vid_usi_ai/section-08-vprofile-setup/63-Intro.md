*Reconstructed from video lecture captions — [63-introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/63-introduction.txt?EntityRepresentationId=0482a2f0-9ea9-46df-95e2-1455dc24901d)*

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What This Project Is

This lecture introduces the **V Profile Project** — a complete multi-tier web application stack that will be set up **locally** on your laptop/desktop using virtual machines. The application itself is a **social networking site written in Java**. But the project isn't about building the application — it's about understanding, deploying, and operating the **infrastructure stack** that makes it run.

The word **"stack"** is explicitly defined in the lecture: a collection of services working together to create an experience — in this case, a web application experience. A single web app doesn't run in isolation; it depends on a web server, an application server, a database, a caching layer, a message broker, and a load balancer. Setting up and connecting all of these is the work of a DevOps engineer.

## 1.2 Why This Project Exists — Two Reasons

The instructor gives two distinct reasons for this project:

**Reason 1: Baseline for all upcoming projects.** This exact stack will be reused throughout the entire course — deployed on AWS, refactored, containerized with Docker, deployed on Kubernetes, managed with Ansible, automated with Jenkins, and more. Every future project assumes you understand the V Profile stack. This lecture is the foundation that everything else builds on.

**Reason 2: Learn to set up local R\&D labs.** In real work environments, you deal with services like MySQL, PostgreSQL, Apache, Nginx, Tomcat, JBoss, GlassFish, and others. You typically have a runbook or setup document. But you may **not feel confident making changes on real production servers**. The solution is to replicate the entire stack locally using VMs, do all your experimentation and R\&D there, gain confidence, and then apply changes to real systems.

## 1.3 The Problem with Manual Local Setup

Setting up a multi-service stack locally by hand has three problems:

1. **Complex** — multiple services, each with its own configuration, dependencies, and inter-service connections
2. **Time-consuming** — installing and configuring each service manually takes significant effort
3. **Not repeatable** — if you destroy the environment, you have to redo everything from scratch. Manual steps are error-prone and hard to reproduce exactly

These three problems combine to create a situation where engineers **avoid local setup altogether**, even though it would be valuable for learning and R\&D.

## 1.4 The Solution: Automated, Repeatable Infrastructure as Code

The solution is to make the local setup **automated** and **repeatable** through Infrastructure as Code (IAC). Instead of manually installing and configuring services, you write code (Vagrantfile + shell scripts) that does everything automatically. With IAC:

* Run one command → entire stack comes up
* Destroy everything → run the same command → identical stack again
* Do as much R\&D as you want → zero cost of rebuilding

This is the same IAC principle from the earlier Vagrant lectures, now applied to a **multi-service production-like stack** instead of a single WordPress VM.

## 1.5 Tools Required

The lecture identifies four categories of tools, all of which should already be installed from prerequisite videos:

| Tool                                             | Role                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------------ |
| **Oracle VM VirtualBox**                         | Hypervisor — runs the virtual machines                                   |
| **Vagrant**                                      | Automation — creates and configures VMs automatically from a Vagrantfile |
| **Git Bash**                                     | Command-line tool — execute commands + version control (multipurpose)    |
| **IDE** (Sublime Text, VS Code, Notepad++, etc.) | Code/config editor — edit Vagrantfiles, scripts, configs                 |

The relationship: **Vagrant communicates with VirtualBox** to create VMs. You interact with Vagrant through **Git Bash**. You edit configuration files in your **IDE**.

## 1.6 Application Architecture — The Service Stack

This is the most important conceptual section of the lecture. The V Profile application uses **five services**, each running in its own VM. Understanding what each service does and how they connect is essential for every future project.

### Nginx — Load Balancer / Entry Point

Nginx (pronounced "Engine X") is a **web service** similar to Apache HTTPD. In this stack, it functions as a **load balancer**. It is the first service the user's request hits. The user opens a browser, enters the IP address (no URL/domain in this project — that comes in the next project), and the request arrives at the Nginx VM. Nginx's job is to **route the request to the Tomcat server**.

> 🔍 **Deep Dive**
> In a production environment, Nginx as a load balancer would distribute traffic across **multiple** Tomcat instances for scalability and fault tolerance. In this local setup, there's only one Tomcat, but the load balancing architecture is still in place to mirror real-world design. This is a common pattern: even single-instance setups use a reverse proxy/load balancer in front to maintain architectural consistency with production.

### Apache Tomcat — Java Web Application Service

Tomcat is where the **application code lives**. The instructor emphasizes this definition explicitly: Tomcat is a **Java Web Application Service**. If you have a web application written in Java, Tomcat is one of the most famous services to host it. The Java social networking application built by developers is deployed here.

When a user's request arrives (routed from Nginx), Tomcat serves the web pages and processes the application logic. If the application needs external shared storage, an **NFS server** (Network File System) can be used — a centralized storage accessible by a cluster of servers. NFS is mentioned briefly as a concept to be aware of but not deeply used in this project.

### MySQL — Database Service

MySQL stores the **user information** — login credentials and other persistent data. When a user logs in with a username and password, the application running in Tomcat executes an **SQL query** against the MySQL database to verify the user's identity and retrieve their data.

### Memcached — Database Caching Service

Memcached sits **between Tomcat and MySQL** as a caching layer. The first time a request hits MySQL, the data is returned to Tomcat **and also cached in Memcached**. The next time the **same request** comes, the data is served from Memcached instead of querying MySQL again. This is **database caching** — the same concept as browser caching, but for database queries.

The purpose is performance: database queries are expensive (disk I/O, query parsing, execution). Cached responses from Memcached are served from memory, which is orders of magnitude faster.

> 🔍 **Deep Dive**
> The request flow for user login is: Tomcat → Memcached (cache check) → if miss → MySQL → response to Tomcat → cache the result in Memcached. On subsequent identical requests: Tomcat → Memcached (cache hit) → response to Tomcat. MySQL is never hit for cached data. This is a classic **cache-aside pattern** (also called lazy-loading cache).

### RabbitMQ — Message Broker (Dummy in This Project)

RabbitMQ is a **message broker**, also called a **queuing agent**. Its purpose is to connect two applications together by allowing them to stream data through a message queue. In this project, RabbitMQ is **connected to Tomcat but is not functional** — it's a dummy service included deliberately to **add complexity for practice**. The instructor is transparent: "The reason I included this is to create a little more complexity so you can practice more."

As a DevOps engineer, you don't need to understand the internal workings of a message broker deeply, but you should know that such services exist and what their role is: **decoupling applications by allowing asynchronous communication through message queues**.

> ⚠️ **Expert Note**
> The instructor's comment about adding dummy services for complexity reflects a real-world reality: production stacks always have services you don't fully understand. A DevOps engineer must be able to set up, configure, and troubleshoot services even when their internal functionality is opaque. Getting comfortable operating "black box" services is an essential skill.

## 1.7 Understanding the Full Application Request Flow

The instructor emphasizes that understanding the **flow of the stack** is critical for a DevOps engineer. When something breaks, you need to reason about **where in the flow** the failure is occurring. The complete request flow:

```
User → Browser → IP Address → Nginx (load balancer)
    → Tomcat (application server, serves web page)
    → User logs in (username + password)
    → Tomcat runs SQL query
    → Request goes to Memcached first (cache check)
        → Cache HIT → data returned to Tomcat → user sees result
        → Cache MISS → query forwarded to MySQL
            → MySQL returns data → Tomcat receives it
            → Data cached in Memcached for future requests
            → User sees result
```

The instructor gives two diagnostic examples based on this flow:

* **User can't log in, but web page loads** → Likely a **database service** issue (MySQL not connected to the application, or credentials wrong)
* **Web page doesn't display properly** → Likely a **Tomcat** issue (application not deployed correctly, or Tomcat not running)

This diagnostic reasoning — mapping symptoms to service layers — is what separates a DevOps engineer from someone who just follows scripts.

## 1.8 Automation Architecture — The Implementation Stack

Separate from the application architecture, there's a second architecture for **how we implement the setup**:

| Component                   | Role                                                                                                       |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Vagrant**                 | Reads the Vagrantfile, communicates with VirtualBox to create VMs automatically                            |
| **VirtualBox**              | Hypervisor — actually runs the VMs                                                                         |
| **Bash scripts / commands** | Provision each VM — install and configure the specific service (Nginx, Tomcat, Memcached, RabbitMQ, MySQL) |

Vagrant creates **one VM per service**: an Nginx VM, a Tomcat VM, a Memcached VM, a RabbitMQ VM, and a MySQL VM. Each VM is provisioned with scripts that install and configure only the service it's responsible for. This is a **one-service-per-VM** architecture — the same pattern used in production (and later, one-service-per-container in Docker/Kubernetes).

## 1.9 The DevOps Engineer's Relationship with Services

The instructor makes an important philosophical point about scope: as a DevOps engineer, you are **more involved in implementation than functionality**. You don't need to understand the internal Java code of the application or the internals of MySQL's query optimizer. But you **must** understand:

* What each service does at a high level
* How services connect to each other
* The flow of requests through the stack
* How to set up, configure, and troubleshoot each service
* Where failures originate based on symptoms

The instructor encourages self-research for any service you feel you need to understand more deeply. These same services (Nginx, Tomcat, Memcached, RabbitMQ, MySQL) will be used repeatedly throughout the course in AWS, Docker, Kubernetes, Jenkins, and Ansible contexts.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up a **complete multi-tier web application stack** on our local machine using **automated virtual machines**. The final outcome: five VMs running five services (Nginx, Tomcat, Memcached, RabbitMQ, MySQL), all configured and connected, serving a Java-based social networking web application accessible from your browser. The entire setup is automated — one command brings up everything.

## Flow of Execution — The Complete Process

The instructor outlines the execution steps at the end of the lecture. This is the roadmap for the upcoming practical lectures:

### Step 1: Prerequisite Tool Setup

Ensure all four tools are installed and working:

* Oracle VM VirtualBox (hypervisor)
* Vagrant (VM automation)
* Git Bash (command line)
* IDE of choice (Sublime Text, VS Code, Notepad++, etc.)

**How to verify:** Each tool should be callable from Git Bash (e.g., `vagrant --version`, `VBoxManage --version`).

**Connection:** These tools form the automation layer that makes everything else possible.

### Step 2: Clone the Source Code

The V Profile project source code will be provided (details in the next project lecture). Clone it using Git:

```bash
git clone <repository_URL>
```

* `git` — version control tool
* `clone` — download a complete copy of the repository
* `<repository_URL>` — the URL provided in the project materials

The cloned repository contains the **Java application source code**, the **Vagrantfile**, and the **provisioning scripts** for all services.

**Connection:** The source code repository is the single source of truth for both the application and its infrastructure.

### Step 3: Navigate to the Vagrant Directory

```bash
cd <source_code>/vagrant_directory
```

Inside the cloned source code, there is a directory containing the **Vagrantfile**. This Vagrantfile defines all five VMs — one per service — with their respective provisioning scripts.

**Connection:** All Vagrant commands must be run from the directory containing the Vagrantfile.

### Step 4: Bring Up All VMs

```bash
vagrant up
```

This single command reads the Vagrantfile and creates **all five virtual machines** automatically through VirtualBox. Each VM is provisioned with the scripts/commands that install and configure its designated service.

**What happens internally:** Vagrant parses the Vagrantfile → communicates with VirtualBox → creates VM 1 (MySQL) → provisions it → creates VM 2 (Memcached) → provisions it → ... continues for all five VMs. The order matters (see Step 6).

**Expected output:** Terminal shows each VM being created, booted, and provisioned sequentially.

**Common mistakes:**

* Not being in the correct directory (Vagrantfile not found)
* VirtualBox not running or not installed
* Insufficient system resources (RAM/CPU) for five simultaneous VMs

> ⚠️ **Expert Note**
> Running five VMs locally requires significant system resources. Ensure your machine has enough RAM (8GB+ recommended, 16GB ideal). If resources are tight, VMs may fail to start or run extremely slowly.

### Step 5: Validate All VMs

After `vagrant up` completes, verify that all VMs are running and can communicate with each other.

```bash
vagrant status
```

Check that all five VMs show as "running."

Then SSH into individual VMs to verify services are running and inter-VM connectivity works (e.g., can the Tomcat VM reach the MySQL VM on the expected port).

**Why validation matters:** A multi-service stack can fail silently — a VM might be running but its service might not be started, or two VMs might not be able to reach each other on the network. Validation catches these issues before you spend time debugging the application.

**Connection:** Validation confirms the infrastructure layer is solid before moving to service configuration.

### Step 6: Set Up Services — One by One, in Order

The services are configured in a specific sequence that respects **dependencies**:

```
1. MySQL          ← database must exist first
2. Memcached      ← caching layer connects to MySQL
3. RabbitMQ       ← message broker connects to Tomcat
4. Tomcat         ← application server needs DB + cache + broker ready
5. Nginx          ← load balancer needs Tomcat running to route to
```

**Why this order:** Each service depends on the one before it. Tomcat needs MySQL to be running before it can connect to the database. Nginx needs Tomcat to be running before it can route requests. Setting up services out of order means connection failures during configuration.

> 🔍 **Deep Dive**
> This dependency-ordered setup is a general infrastructure pattern. In any multi-service stack, you start from the **innermost dependency** (data layer) and work outward toward the **user-facing layer**. The order is: storage → data services → application services → routing/load balancing → user access. This same ordering applies when deploying with Docker Compose (`depends_on`), Kubernetes (readiness probes), or Terraform (resource dependencies).

### Step 7: Build and Deploy the Java Application

The Java application source code is compiled (built) and then deployed to the Tomcat server. This step produces the deployable artifact (typically a `.war` file for Java web apps) and places it where Tomcat can serve it.

**Connection:** This is where the application code meets the infrastructure. All previous steps built the infrastructure; this step puts the application on it.

### Step 8: Verify from Browser

Open a browser and enter the **IP address** of the Nginx VM (the load balancer):

```
http://<Nginx_VM_IP>
```

**Expected result:** The V Profile social networking web application loads. You can log in with test credentials, and the full request flow executes: Nginx → Tomcat → Memcached/MySQL.

**If the page doesn't load:** Check Nginx is running and routing to the correct Tomcat IP.
**If the page loads but login fails:** Check MySQL connectivity from Tomcat, verify database has user data.
**If the page loads slowly:** Check Memcached is running and connected (all requests hitting MySQL directly).

**Note:** This project uses an **IP address**, not a URL/domain name. The next project will cover setting up a proper URL.

**Connection:** This final verification confirms the entire stack — all five services, their configurations, and their interconnections — is working end to end.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Application Architecture — The 5-Service Stack

```
USER → Browser → IP Address
                    │
                    ▼
            ┌──────────────┐
            │    NGINX      │  ← Load Balancer (entry point)
            │   (Web Svc)   │
            └──────┬───────┘
                   │ routes request
                   ▼
            ┌──────────────┐        ┌──────────────┐
            │   TOMCAT      │◄──────►│  RABBITMQ     │
            │ (Java App Svc)│        │ (Msg Broker)  │
            │  [app lives   │        │  [DUMMY]      │
            │   here]       │        └──────────────┘
            └──────┬───────┘
                   │ SQL query (login)
                   ▼
            ┌──────────────┐
            │  MEMCACHED    │  ← Cache check FIRST
            │ (DB Caching)  │
            └──────┬───────┘
                   │ cache MISS only
                   ▼
            ┌──────────────┐
            │    MYSQL      │  ← Persistent user data
            │  (Database)   │
            └──────────────┘
```

## Cache Flow (Login Request)

```
Tomcat → Memcached
           ├── HIT  → return cached data → done
           └── MISS → MySQL → return data → cache in Memcached → done
```

## Automation Architecture

```
YOU (Git Bash)
  │
  ├── vagrant up
  │      │
  │      ▼
  │   VAGRANT ──reads──→ Vagrantfile
  │      │
  │      ├──creates──→ VIRTUALBOX
  │      │                │
  │      │                ├── VM: Nginx
  │      │                ├── VM: Tomcat
  │      │                ├── VM: Memcached
  │      │                ├── VM: RabbitMQ
  │      │                └── VM: MySQL
  │      │
  │      └──provisions──→ Bash Scripts (per VM)
  │                         │
  │                         └── installs + configures each service
  │
  └── IDE (edit Vagrantfile, scripts, configs)
```

## Execution Flow (Setup Order)

```
1. Install tools       (VirtualBox, Vagrant, Git Bash, IDE)
2. Clone source code   (git clone)
3. cd vagrant dir      (where Vagrantfile lives)
4. vagrant up          (creates + provisions all 5 VMs)
5. Validate VMs        (running? connected? services up?)
6. Setup services      (MySQL → Memcached → RabbitMQ → Tomcat → Nginx)
                        ← DEPENDENCY ORDER: data layer → app layer → routing layer
7. Build + deploy app  (Java → .war → Tomcat)
8. Browser verify      (http://<Nginx_IP>)
```

## Service Setup Dependency Chain

```
MySQL ← must exist first (data store)
  ↓
Memcached ← connects to MySQL (cache layer)
  ↓
RabbitMQ ← connects to Tomcat (message layer)
  ↓
Tomcat ← needs DB + cache + broker ready (application layer)
  ↓
Nginx ← needs Tomcat running (routing layer)
```

**Pattern:** Always build from **innermost dependency outward** → data → app → routing → user.

## Diagnostic Map — Symptom → Service

```
SYMPTOM                              LIKELY PROBLEM SERVICE
──────                               ─────────────────────
Page doesn't load at all         →   Nginx (not running / wrong routing)
Page loads, login fails          →   MySQL (not connected / no data)
Page loads, login slow           →   Memcached (not caching / not running)
Application errors on page       →   Tomcat (app not deployed / crashed)
```

## Why This Project — Dual Purpose

```
PURPOSE 1: Baseline
  This stack → reused in AWS, Docker, K8s, Ansible, Jenkins, Terraform
  Understand once → applies everywhere

PURPOSE 2: Local R&D Lab Pattern
  Real project → afraid to change prod
  → Replicate stack locally (VMs) → experiment freely
  → Manual = complex, slow, not repeatable
  → IAC = automated, repeatable, unlimited R&D
```

## Key Definitions (Quick Recall)

```
Stack           = collection of services working together for an experience
Nginx           = web service / load balancer (routes requests)
Tomcat          = Java web application service (hosts Java apps)
MySQL           = relational database (persistent storage)
Memcached       = database caching (memory-speed query responses)
RabbitMQ        = message broker / queuing agent (async app-to-app comms)
NFS             = network file system (shared/centralized storage for clusters)
IAC             = Infrastructure as Code (automated, repeatable setup)
```

## Transferable Engineering Pattern

**Layered Dependency Stack Pattern:**

```
Every multi-service system follows:

  DATA LAYER      → databases, persistent storage
       ↓
  CACHE LAYER     → reduce load on data layer
       ↓
  MESSAGE LAYER   → decouple services, async communication
       ↓
  APP LAYER       → business logic, user-facing functionality
       ↓
  ROUTING LAYER   → load balancing, request distribution, entry point

Setup order: bottom → top
Debug order: symptom → trace backward through layers
Destroy order: top → bottom (reverse)
```

This pattern applies identically to Docker Compose stacks, Kubernetes deployments, AWS architectures, and any multi-tier system. The technology names change; the layered dependency structure never does.
