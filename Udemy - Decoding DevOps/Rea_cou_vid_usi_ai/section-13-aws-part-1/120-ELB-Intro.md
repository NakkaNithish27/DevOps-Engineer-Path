# 🎓 Deep Learning Material: AWS Elastic Load Balancers (ELB) — Introduction

*Reconstructed from video captions — [120. ELB Introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt?EntityRepresentationId=32ae5f90-8966-4f11-b40e-9a40516389e7)* [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Problem: Why One Server Is Not Enough

In production, a single web server serving all user traffic creates two critical problems: **performance limits** and **maintenance vulnerability**. A single server has finite CPU, memory, and network capacity — once user demand exceeds that capacity, the server slows down or crashes. Additionally, when that single server needs a software update, a security patch, or a restart, the entire service goes offline — users experience downtime. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

The solution is a **cluster of web servers** — multiple servers running the **same web service** simultaneously. This cluster architecture enables two fundamental capabilities:

**Scaling out (horizontal scaling):** When traffic increases, you add more servers to the cluster to handle the additional load. When traffic decreases, you remove servers to save cost. This is called **scale out** (add capacity) and **scale in** (reduce capacity). The cluster size adjusts to match demand.

**Maintenance without downtime:** When you need to update servers (OS patches, software upgrades), you can update them one at a time while the others continue serving traffic. The user experience is never interrupted because the service is always running on at least some servers in the cluster.

But a cluster creates its own problem: if you have 5 web servers, each with a different IP address, which IP do you give to users? You can't expect users to know about or choose between 5 different server addresses. You need a **single endpoint** — one address that represents the entire cluster. This is the problem a load balancer solves. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

***

## 1.2 What a Load Balancer Is

A load balancer is a **device or software** — it can be a physical hardware appliance or a software program running on a server — that sits between users and a cluster of servers. It provides a **single endpoint** (one address) that users access, and it **distributes incoming network traffic** across the multiple servers behind it. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

The load balancer is **not the real server**. It does not host the application, it does not store the data, and it does not process the business logic. It is a **proxy** — an intermediary that receives requests on behalf of the real servers, decides which server should handle each request, and forwards the request there. The response flows back through the load balancer to the user. From the user's perspective, they are talking to one system. In reality, the load balancer is transparently routing their requests across a fleet of servers. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

### Frontend Port and Backend Port

A load balancer operates with two port concepts: [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

**Frontend port:** The port on which the load balancer **listens for user requests**. This is the port exposed to the internet. Commonly port 80 (HTTP) or 443 (HTTPS).

**Backend port:** The port on which the actual **web servers** are running. The load balancer forwards requests to this port on the backend servers. For web servers, this is typically port 80.

The frontend and backend ports can be the same (both 80) or different (frontend 443, backend 80). The load balancer handles the translation — users hit the frontend, the load balancer routes to the backend.

> 🔍 **Deep Dive:** The frontend/backend port model reveals the load balancer's proxy nature. Users never communicate directly with backend servers — they communicate with the load balancer's frontend. The load balancer then opens a separate connection to a backend server on the backend port. This two-connection architecture is what enables traffic distribution, SSL termination, health checking, and many other load balancer features. The user's connection terminates at the load balancer, not at the backend server.

***

## 1.3 AWS Elastic Load Balancers (ELB) — Managed Service

On AWS, you do **not** need to launch an EC2 instance and install load balancer software yourself. AWS provides **Elastic Load Balancers (ELB)** as a managed service. You configure the load balancer through the AWS console (or API), and AWS handles the underlying infrastructure — the hardware, the software, the scaling, the high availability. You just define the rules and attach your backend servers. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

The term "Elastic" in ELB reflects the same elasticity concept as in other AWS services — the load balancer scales automatically to handle varying traffic loads without you managing its capacity.

***

## 1.4 The Four Types of AWS Load Balancers

AWS offers four distinct load balancer types, each operating at a different OSI layer and serving different use cases: [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

### 1.4.1 Classic Load Balancer (CLB)

The **simplest** type. It operates at **Layer 4** (Transport Layer) — meaning it understands **IP addresses and port numbers**, but it does **not** understand URLs, HTTP headers, or application-level content. It simply takes a request on the frontend port (e.g., 443) and routes it to a backend server on the backend port (e.g., 80). [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

The setup is straightforward: create EC2 instances, set up your web service, add the instances under a Classic Load Balancer, and provide the CLB's endpoint to users. It's described as **"ideal for a simple solution"** — when you just need basic traffic distribution without any intelligent routing logic.

### 1.4.2 Application Load Balancer (ALB)

The **most commonly used** type for web applications. It operates at **Layer 7** (Application Layer) — meaning it **understands URLs, HTTP headers, and application-level content**. This enables **intelligent routing** — the ability to route requests to different groups of servers based on the URL path or other HTTP attributes. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

The video gives a concrete example: if a user accesses `hkinfotech.in`, the ALB can send that request to one group of servers. But if the user accesses `hkinfotech.in/videos`, the ALB can route that request to a **different cluster** based on a routing rule. This is impossible with a Layer 4 load balancer — it can't read the URL path, only the IP and port.

This is the load balancer type used **most of the time** in the course and the most widely used on AWS for HTTP/HTTPS traffic. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

### 1.4.3 Network Load Balancer (NLB)

Operates at **Layer 4** (like the Classic Load Balancer) but with two key differentiators: it provides a **static IP address** (important for use cases where clients need a fixed IP to whitelist or configure) and it can handle **millions of requests per second** — extreme throughput capacity far beyond what CLB or ALB can manage. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

The video notes that NLB is **very expensive** due to its high-performance capabilities. It also mentions a specific architectural pattern: sometimes an NLB is placed **in front of an ALB** — the NLB provides the static IP and extreme throughput, while the ALB behind it provides intelligent Layer 7 routing. The NLB is out of scope for this course due to cost.

### 1.4.4 Gateway Load Balancer (GLB)

Operates at **Layer 3** (Network Layer). Its purpose is fundamentally different from the other load balancers — it is used to run and manage **security appliances** like firewalls and intrusion detection systems (IDS). [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

The critical distinguishing characteristic: GLB **does not modify the network packet**. The source IP, destination IP, and all other packet information remain **completely unchanged**. It simply forwards the packet to the security appliance for inspection. This is essential because an intrusion detection system needs the **original, unmodified packet data** to perform security analysis — if the load balancer changed the source IP (as ALB and NLB typically do), the IDS couldn't determine where the traffic actually came from.

The video explicitly states this is out of scope and "too early to understand" without experience in AWS VPC networking. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

> 🔍 **Deep Dive:** The four load balancer types map cleanly to OSI layers, and this is the key to understanding when to use each:
>
> * **Layer 3 (Network):** Gateway LB — packet-level, for security appliances
> * **Layer 4 (Transport):** Classic LB and Network LB — IP + port level, for simple routing or extreme throughput
> * **Layer 7 (Application):** Application LB — URL + HTTP level, for intelligent content-based routing
>
> The higher the layer, the more the load balancer "understands" about the traffic, and the more intelligent its routing decisions can be. But higher-layer processing also means more overhead — which is why NLB (Layer 4) can handle millions of requests per second while ALB (Layer 7) has lower raw throughput but smarter routing.

***

## 1.5 The Upcoming Lab Preview

The video previews what will be built in the following lectures: a **cluster of web servers** with a **load balancer** on the frontend, plus the use of **AMIs (Amazon Machine Images)** and **launch templates** to create the server fleet efficiently. This establishes the progression: understand the concept first (this lecture), then build it (next lectures). [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Preparing For

This lecture is a **conceptual foundation** — there are no hands-on commands to execute. The practical work (setting up web server clusters, configuring load balancers, creating AMIs and launch templates) begins in the next lecture. However, there are practical **decision frameworks** taught in this video that directly feed into the upcoming lab work.

***

## Decision Framework 1: Choosing the Right Load Balancer Type

When you're about to set up a load balancer in AWS, the first decision is **which type**. The decision tree based on the video: [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

**Is this for HTTP/HTTPS web traffic that needs URL-based routing?**

* **YES** → **Application Load Balancer (ALB)**. This is the default choice for web applications. It's what the course uses.

**Is this for simple TCP traffic distribution with no URL awareness needed?**

* **YES, and cost matters** → **Classic Load Balancer (CLB)**. Simplest setup, lowest complexity.
* **YES, and you need a static IP or millions of requests/second** → **Network Load Balancer (NLB)**. Expensive, high performance.

**Is this for forwarding traffic to security appliances (firewalls, IDS)?**

* **YES** → **Gateway Load Balancer (GLB)**. Requires VPC networking knowledge.

**For this course:** You will almost always use **ALB**. [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

***

## Decision Framework 2: Understanding Frontend/Backend Port Mapping

When configuring a load balancer, you will be asked to specify:

**Listener (frontend):** What port does the load balancer listen on? For a public website: port 80 (HTTP) or port 443 (HTTPS).

**Target group (backend):** What port are your web servers running on? Typically port 80.

**The mapping:**

```
User → hits LB endpoint on FRONTEND port (80 or 443)
LB   → forwards to backend server on BACKEND port (80)
```

**Common mistake:** Confusing which port goes where. The frontend port faces the user. The backend port faces your servers. They can be the same number but serve different roles.

***

## Decision Framework 3: Architecture Planning for the Lab

The upcoming lab will follow this structure: [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)

```
[Users] → [Load Balancer (ALB, port 80/443)]
              │
              ├── [Web Server 1 (EC2, port 80)]
              ├── [Web Server 2 (EC2, port 80)]
              └── [Web Server 3 (EC2, port 80)]
```

**Components you'll need to create:**

1. Multiple EC2 instances running the same web service
2. An AMI (Amazon Machine Image) to clone instances efficiently
3. A launch template to standardize instance configuration
4. An Application Load Balancer to distribute traffic
5. A target group to register the backend instances

**Connection to previous knowledge:** The EC2 launch process (key pairs, security groups, tags, naming conventions) from video 114 directly applies. Each web server instance follows the same structured launch process. The security group for the instances will need port 80 open (for the LB to reach them). The LB itself will have its own security group with port 80/443 open to the public.

> ⚠️ **Expert Note:** The video mentions AWS provides "really good documentation" for all load balancer types and recommends reading it **after** completing the hands-on exercises. This is a deliberate learning-order recommendation: do the lab first to build practical intuition, then read the documentation with that context. Documentation makes far more sense after you've seen the system work.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ Core Problem → Solution Chain

```
ONE SERVER:
  ├── Performance limit (can't handle all traffic)
  ├── Maintenance = downtime (update = offline)
  └── Single point of failure

CLUSTER OF SERVERS (same service, multiple instances):
  ├── Scale out (add servers) / Scale in (remove servers)
  ├── Update without downtime (rolling updates)
  └── NEW PROBLEM: Multiple IPs → which one for users?

LOAD BALANCER:
  └── Single endpoint → distributes traffic → multiple servers
      └── Proxy: not the real server, intermediary
```

## 🔀 Load Balancer Traffic Flow

```
User → Frontend Port (LB endpoint)
         │
         LB distributes request
         │
         ├── Backend Server 1 : Backend Port
         ├── Backend Server 2 : Backend Port
         └── Backend Server N : Backend Port

Frontend port = user-facing (80/443)
Backend port  = server-facing (typically 80)
```

## 📊 AWS ELB Types — Layer-Based Classification

```
LAYER 7 (Application):
  └── ALB (Application Load Balancer)
        ├── Understands: URLs, HTTP headers, paths
        ├── Routing: URL-path-based (e.g., /videos → cluster B)
        ├── Use case: HTTP/HTTPS web traffic
        └── MOST USED in AWS, used in this course

LAYER 4 (Transport):
  ├── CLB (Classic Load Balancer)
  │     ├── Understands: IP + Port only
  │     ├── Routing: Simple frontend→backend forwarding
  │     └── Use case: Simple, low-complexity setups
  │
  └── NLB (Network Load Balancer)
        ├── Understands: IP + Port only
        ├── STATIC IP address
        ├── Millions of requests/second
        ├── Very EXPENSIVE
        ├── Sometimes placed IN FRONT of ALB
        └── Out of scope (cost)

LAYER 3 (Network):
  └── GLB (Gateway Load Balancer)
        ├── Understands: Network packets
        ├── Does NOT modify packet (source/dest IP preserved)
        ├── Use case: Firewalls, IDS (Intrusion Detection)
        ├── Requires VPC networking knowledge
        └── Out of scope (too advanced)
```

## 🔑 ALB vs. CLB — The Key Distinction

```
CLB (Layer 4):
  hkinfotech.in      → routes to Server Pool A
  hkinfotech.in/videos → routes to Server Pool A  (SAME — can't read URL path)

ALB (Layer 7):
  hkinfotech.in      → routes to Server Pool A
  hkinfotech.in/videos → routes to Server Pool B  (DIFFERENT — reads URL path)

ALB = intelligent routing based on URL content
CLB = dumb forwarding based on IP + port only
```

## 🏢 AWS ELB = Managed Service

```
Traditional:  Launch EC2 → Install LB software → Manage it yourself
AWS ELB:      Configure in console → AWS manages everything

No EC2 instance needed for the LB itself.
AWS handles: infrastructure, scaling, availability.
You handle: rules, ports, target servers.
```

## 📐 Upcoming Lab Architecture

```
[Internet Users]
       │
       ▼
[ALB — frontend port 80/443]  ← single endpoint
       │
       ├── [EC2 Web01 — port 80]
       ├── [EC2 Web02 — port 80]  ← created from AMI + Launch Template
       └── [EC2 Web03 — port 80]

Components to build:
  1. EC2 instances (web servers)
  2. AMI (clone image)
  3. Launch Template (standardized config)
  4. ALB (load balancer)
  5. Target Group (register backend instances)
```

## 🔁 Scaling Model

```
SCALE OUT: Traffic ↑ → Add servers to cluster → LB auto-distributes
SCALE IN:  Traffic ↓ → Remove servers → Save cost
UPDATE:    Take 1 server out → Update → Put back → Next server
           (Zero downtime — LB routes around the updating server)
```

## 🔁 Reusable Engineering Patterns

| Pattern                                 | Manifestation                                                                                            |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Single endpoint / multiple backends** | LB provides one address; cluster provides the capacity. Users see unity; infra provides multiplicity.    |
| **Proxy intermediary**                  | LB is not the real server — it's a transparent forwarder. Same pattern as reverse proxies, API gateways. |
| **Layer determines intelligence**       | Higher OSI layer = more context = smarter routing. Layer 4 sees ports; Layer 7 sees URLs.                |
| **Frontend/Backend port separation**    | User-facing port decoupled from server port. Enables port translation, SSL termination.                  |
| **Horizontal scaling**                  | Add/remove identical nodes behind LB. Scale = more instances, not bigger instances.                      |
| **Managed service over self-managed**   | AWS ELB vs. self-installed LB software — same function, AWS handles infra.                               |
| **Packet transparency (GLB)**           | When downstream needs original data, the intermediary must NOT modify it.                                |

## ⚡ Key Gotchas for Fast Recall

```
❌ "I need a load balancer" → launches EC2 + installs nginx/haproxy
✅ Use AWS ELB (managed service, no EC2 needed for LB)

❌ Uses ALB for raw TCP/millions of req/sec
✅ ALB = HTTP/HTTPS + URL routing | NLB = extreme throughput + static IP

❌ Confuses frontend port (user-facing) with backend port (server-facing)
✅ Frontend = what users hit | Backend = what servers run on

❌ One server for everything
✅ Cluster + LB = scalability + zero-downtime maintenance

❌ CLB for URL-based routing
✅ CLB = Layer 4 (IP+port only) | ALB = Layer 7 (URL-aware)
```

## 📋 Quick Type Selection

```
Web app with URL routing?      → ALB (Layer 7)
Simple port forwarding?        → CLB (Layer 4)
Static IP + extreme scale?     → NLB (Layer 4, expensive)
Security appliance forwarding? → GLB (Layer 3, advanced)
Default for this course?       → ALB
```

***

This completes the full reconstruction of the AWS Elastic Load Balancers Introduction video. Want me to generate Anki flashcards (CSV) from this material, or process another caption file? [\[120. ELB I...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/120.%20ELB%20Introduction.txt)
