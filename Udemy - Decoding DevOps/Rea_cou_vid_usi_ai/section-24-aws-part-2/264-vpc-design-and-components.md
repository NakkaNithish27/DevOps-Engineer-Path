# 🧠 AWS VPC Design & Components — Network Architecture for Security and High Availability

**Source:** *264. VPC Design and Components* — AWS Networking Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Is a VPC and Why Does It Exist?

A **VPC (Virtual Private Cloud)** is the foundational network container in AWS. It is your own isolated section of the AWS cloud — a private network where you launch resources like EC2 instances, databases, load balancers, and everything else. Every AWS resource that needs network connectivity lives inside a VPC. Think of it as your own private data center's network, but virtualized within AWS infrastructure.

The VPC itself is the top-level boundary. Inside it, you divide the network into smaller segments called **subnets**. The entire lecture is about understanding the components that exist within and around a VPC, how they interact, and how they combine to provide both **security** (controlling who can reach what) and **high availability** (surviving the failure of physical infrastructure).

***

## 1.2 Subnets — Dividing the VPC into Public and Private Zones

A VPC is divided into **subnets** — smaller network segments that serve different purposes. There are exactly two kinds of subnets in a VPC:

### Public Subnet

A public subnet is one where resources can be **reached directly from the internet**, and resources can **reach the internet directly**. If you have an EC2 instance in a public subnet, it gets a public IP address. You can SSH into it from your laptop using that public IP. Web servers, load balancers, and anything that needs to face the internet live in public subnets.

What *makes* a subnet public is not a label or a setting on the subnet itself — it's the **Internet Gateway** connected to it via a route table (covered below). Without an Internet Gateway route, a subnet is private by default.

### Private Subnet

A private subnet is one where resources **cannot be reached directly from the internet**. Instances in a private subnet have only **private IP addresses** — no public IPs. Traffic originating from the internet cannot get into a private subnet directly. This is the security layer: databases, application backends, internal services — anything that shouldn't be publicly accessible — live in private subnets.

However, instances in private subnets often still need **outbound internet access** — to download packages, pull updates, or connect to external APIs. This outbound-only access is provided by a **NAT Gateway** (covered below).

***

## 1.3 Internet Gateway — The Door to the Internet

An **Internet Gateway** is a virtual networking device that connects your VPC to the public internet. It is the component that enables **bidirectional** internet traffic: traffic from the internet can reach instances in public subnets, and instances in public subnets can reach the internet.

The Internet Gateway is a **fully managed, highly available** AWS component. The instructor emphasizes: *"Internet gateway you create, it's going to be totally managed by AWS. You don't need to worry about the high availability, redundancy. Everything is managed."* You don't need to create multiple Internet Gateways for redundancy — AWS handles that internally.

An Internet Gateway is attached to the VPC itself (one per VPC), and public subnets have route table entries that direct internet-bound traffic to it.

***

## 1.4 NAT Gateway — Outbound-Only Internet for Private Subnets

A **NAT Gateway** solves a specific problem: instances in private subnets need to access the internet (download packages, pull updates) but must not be reachable *from* the internet. NAT Gateway provides **outbound-only internet connectivity** — traffic from private instances can go out to the internet, and the *responses* to that traffic come back, but no new traffic originating from the internet can initiate a connection into the private subnet.

The instructor provides a powerful real-world analogy: *"Think of NAT Gateway as your WiFi router. The instances in the private subnet are like your laptop. From your laptop you can connect to the internet, but from the internet you cannot connect to your laptop."* Your laptop has a private IP (like `192.168.x.x`), and your WiFi router has a public IP from your ISP. The router performs NAT (Network Address Translation) — it translates between private and public addresses, allowing outbound connections while blocking inbound ones. The NAT Gateway does exactly the same thing for your private subnet instances.

**Placement:** The NAT Gateway itself lives in a **public subnet** — because it needs to connect to the Internet Gateway for internet access. The traffic flow is: private instance → NAT Gateway (in public subnet) → Internet Gateway → internet. The response follows the reverse path.

> 🔍 **Deep Dive:** The key behavioral distinction between Internet Gateway and NAT Gateway: Internet Gateway allows **bidirectional** traffic (internet ↔ instance). NAT Gateway allows only **outbound-initiated** traffic (instance → internet, and the response back). Traffic originating from the internet **cannot** initiate a connection through the NAT Gateway into the private subnet. This one-way initiation property is the security guarantee of private subnets.

***

## 1.5 Route Tables — The Traffic Decision Engine

An EC2 instance in a subnet doesn't inherently "know" whether it's in a public or private subnet, or where to send internet-bound traffic. The **route table** attached to the subnet makes this decision. A route table is a set of rules (routes) that determine where network traffic is directed.

**For a public subnet:** The route table contains a route that says "all internet-bound traffic (destination `0.0.0.0/0`) → send to the Internet Gateway." This is what makes the subnet public.

**For a private subnet:** The route table contains a route that says "all internet-bound traffic (destination `0.0.0.0/0`) → send to the NAT Gateway." This enables outbound internet access while maintaining private subnet isolation.

Every subnet must have a route table attached. The route table is the **control plane** that determines the networking behavior of the subnet — it's the mechanism that implements the public/private distinction.

The instructor frames Internet Gateway and NAT Gateway as **routers**: *"Internet Gateway and NAT Gateway, both are routers. But Internet Gateway is for the direct to-and-fro internet connection. NAT Gateway is for only traffic that goes to the internet."*

***

## 1.6 VPN Gateway — Connecting from Corporate Networks

The instructor briefly introduces another connectivity option: if you want to connect to instances in your private subnet directly from your **corporate data center, office, or organization**, you can set up a **VPN Gateway**. When users dial the VPN from their corporate network, they can connect to private subnet instances using their private IPs, as if they were on the same local network.

This is a lighter mention — the main focus remains on Internet Gateway and NAT Gateway — but it establishes that private subnets aren't completely isolated from all external access. They're isolated from the *public internet*, but controlled, authenticated access from corporate networks is possible through VPN.

***

## 1.7 Bastion Host (Jump Server) — Accessing Private Instances

Since private subnet instances have no public IPs and can't be SSHed into directly from the internet, how do you administer them? One approach is the **bastion host** (also called a **jump server**).

A bastion host is an EC2 instance that lives in a **public subnet**. You SSH into the bastion host from the internet (it has a public IP). Then, from the bastion host, you SSH into instances in the private subnet. This works because **all subnets within a VPC — public and private — can communicate with each other by default**. An instance in a public subnet can connect to an instance in a private subnet and vice versa. The VPC's internal routing handles this.

The traffic flow is: your laptop → (internet) → bastion host (public subnet) → (VPC internal) → private instance. This is the "jump" — you jump through the bastion host to reach private infrastructure.

> ⚠️ **Expert Note:** The bastion host becomes a critical security point — it's the only public-facing entry point into your private infrastructure. In production, bastion hosts are heavily hardened: minimal software installed, strict security group rules (SSH from specific IPs only), often with session logging and multi-factor authentication. Some organizations replace bastion hosts entirely with AWS Systems Manager Session Manager, which provides shell access without any public IP or open SSH ports.

***

## 1.8 High Availability — Multi-Zone Subnet Distribution

Security alone isn't enough — you also need **high availability**. Subnets are created **within specific availability zones**. An availability zone is a cluster of data centers — if a zone goes down (hardware failure, power outage, network issues), everything in that zone becomes unavailable.

To achieve high availability, you create **multiple subnets across multiple zones**:

* **Public subnet in Zone 1** + **Public subnet in Zone 2**
* **Private subnet in Zone 1** + **Private subnet in Zone 2**

The instructor illustrates with a concrete example: *"You have four web servers. You can put two in public subnet \[Zone 1] and the other two in the other public subnet \[Zone 2]. So if Zone 1 goes down, only half of your infrastructure is down."* With more instances and more zones, you can distribute even more evenly.

Every region has **minimum two zones** (some have three, some have six). The minimum viable high-availability design uses two zones with one public and one private subnet in each.

**NAT Gateway high availability** follows the same logic: if you need highly available outbound internet access for private subnets, you create a **NAT Gateway in each public subnet** (one per zone). If one zone's NAT Gateway goes down, the other zone's private instances can still reach the internet through their zone's NAT Gateway.

***

## 1.9 Cost Model — What's Chargeable and What's Not

The instructor provides a critical cost distinction for the VPC components:

| Component        | Cost              |
| ---------------- | ----------------- |
| VPC              | **Free**          |
| Subnets          | **Free**          |
| Route tables     | **Free**          |
| Internet Gateway | **Free**          |
| **NAT Gateway**  | **💰 Chargeable** |

*"NAT Gateway is the only piece that is chargeable. AWS is going to charge you on the NAT Gateway."* This has design implications: creating two NAT Gateways for high availability doubles the NAT Gateway cost. In development/learning environments, you might use a single NAT Gateway to save money, accepting reduced availability. In production, the cost is justified by the availability guarantee.

***

## 1.10 Intra-VPC Communication — The Default Behavior

A subtle but important point: **all subnets within a VPC can communicate with each other by default** — regardless of whether they're public or private, or in different zones. An instance in a public subnet can reach an instance in a private subnet using its private IP, and vice versa. This is what makes the bastion host pattern work, and it's what allows application servers in public subnets to connect to databases in private subnets.

This default connectivity is controlled by route tables (local routes) and further refined by security groups. The public/private distinction only affects **internet-facing** behavior — not VPC-internal communication.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are designing a **complete VPC network architecture** that achieves both **security** (private subnets for backend services) and **high availability** (multi-zone distribution). The next lecture will implement this design — this lecture establishes the blueprint.

**Final design:**

* 1 VPC
* 2 public subnets (one per availability zone)
* 2 private subnets (one per availability zone)
* 1 Internet Gateway (attached to VPC, routes from public subnets)
* 2 NAT Gateways (one in each public subnet, for private subnet outbound traffic)
* Route tables connecting subnets to the appropriate gateways
* Bastion host in public subnet for SSH access to private instances

***

## Component 1: VPC — The Network Container

The VPC is the top-level container. All subnets, gateways, route tables, and instances live inside it. You define its IP address range (CIDR block) when creating it, and all subnets get their IP ranges from within the VPC's range.

**Connection to flow:** Everything else is built inside this boundary.

***

## Component 2: Public Subnets (×2, one per zone)

Create two public subnets, each in a different availability zone.

**What makes them public:** Their route tables will have an entry directing internet traffic (`0.0.0.0/0`) to the Internet Gateway.

**What lives here:** Web servers, load balancers, bastion hosts, NAT Gateways — anything that needs internet-facing access.

**High availability logic:** If Zone 1 goes down, instances in Zone 2's public subnet remain accessible. Distribute instances across both subnets for resilience.

***

## Component 3: Private Subnets (×2, one per zone)

Create two private subnets, each in a different availability zone (same zones as the public subnets).

**What makes them private:** Their route tables direct internet traffic to the NAT Gateway (not the Internet Gateway). Instances have only private IPs.

**What lives here:** Databases, application backends, internal services — anything that should not be directly accessible from the internet.

**Outbound internet access:** Through the NAT Gateway in the corresponding zone's public subnet.

***

## Component 4: Internet Gateway (×1)

Create one Internet Gateway and attach it to the VPC.

**No redundancy needed:** AWS manages the Internet Gateway's availability internally. One is sufficient for the entire VPC.

**Route table integration:** Public subnet route tables get a route: `0.0.0.0/0 → Internet Gateway`.

**Cost:** Free.

***

## Component 5: NAT Gateways (×2, one per public subnet)

Create one NAT Gateway in each public subnet (one per zone).

**Why in the public subnet:** The NAT Gateway needs to reach the Internet Gateway, which is only accessible from public subnets.

**Route table integration:** Private subnet route tables get a route: `0.0.0.0/0 → NAT Gateway` (pointing to the NAT Gateway in the same zone's public subnet).

**High availability logic:** Two NAT Gateways ensure that if one zone goes down, private instances in the other zone still have outbound internet access.

**Cost:** 💰 This is the **only chargeable component** in this design. Two NAT Gateways = double the cost. In learning/dev environments, you might use just one to save money.

***

## Component 6: Route Tables

Each subnet needs a route table:

**Public subnet route table:**

| Destination      | Target                    |
| ---------------- | ------------------------- |
| VPC CIDR (local) | Local (intra-VPC traffic) |
| `0.0.0.0/0`      | Internet Gateway          |

**Private subnet route table:**

| Destination      | Target                    |
| ---------------- | ------------------------- |
| VPC CIDR (local) | Local (intra-VPC traffic) |
| `0.0.0.0/0`      | NAT Gateway               |

**Cost:** Free.

***

## Component 7: Bastion Host (Jump Server)

An EC2 instance in a **public subnet** that serves as the SSH entry point for accessing private instances.

**Access flow:** Your laptop → SSH to bastion host (public IP) → SSH from bastion host to private instance (private IP).

**Why it works:** All VPC subnets can communicate internally by default.

**Security consideration:** Lock down the bastion host's security group — SSH (port 22) from your IP only.

***

## Verification Checklist for the Design

Before building in the next lecture, verify the design mentally:

* ✅ Public subnets have routes to Internet Gateway
* ✅ Private subnets have routes to NAT Gateway
* ✅ NAT Gateways are placed in public subnets (not private)
* ✅ Subnets are distributed across at least 2 zones
* ✅ Bastion host is in a public subnet with a public IP
* ✅ Private instances have only private IPs
* ✅ NAT Gateway is the only cost-bearing component

> ⚠️ **Expert Note:** This design represents the **minimum viable production VPC** — two zones, public/private separation, HA on NAT Gateways. Scaling up means adding more zones, more subnets, and potentially transit gateways for multi-VPC connectivity. But the architectural pattern — public/private separation with gateway-based routing — remains the same at any scale.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## VPC Architecture — Complete Design

```
┌────────────────────────────── VPC ──────────────────────────────┐
│                                                                  │
│         Zone 1                           Zone 2                  │
│  ┌──────────────────┐            ┌──────────────────┐           │
│  │  PUBLIC SUBNET 1 │            │  PUBLIC SUBNET 2 │           │
│  │                  │            │                  │           │
│  │  [Bastion Host]  │            │                  │           │
│  │  [NAT GW 1] ─────┼──────┐    │  [NAT GW 2] ─────┼─────┐    │
│  │  [Web Servers]   │      │    │  [Web Servers]   │     │    │
│  └────────┬─────────┘      │    └────────┬─────────┘     │    │
│           │                │             │               │    │
│    ┌──────┴──────┐         │      ┌──────┴──────┐        │    │
│    │ Route Table │         │      │ Route Table │        │    │
│    │ 0.0.0.0/0   │         │      │ 0.0.0.0/0   │        │    │
│    │  → IGW      │         │      │  → IGW      │        │    │
│    └─────────────┘         │      └─────────────┘        │    │
│                            │                             │    │
│  ┌──────────────────┐      │    ┌──────────────────┐     │    │
│  │ PRIVATE SUBNET 1 │      │    │ PRIVATE SUBNET 2 │     │    │
│  │                  │      │    │                  │     │    │
│  │  [DB Servers]    │      │    │  [DB Servers]    │     │    │
│  │  [App Backends]  │      │    │  [App Backends]  │     │    │
│  └────────┬─────────┘      │    └────────┬─────────┘     │    │
│           │                │             │               │    │
│    ┌──────┴──────┐         │      ┌──────┴──────┐        │    │
│    │ Route Table │         │      │ Route Table │        │    │
│    │ 0.0.0.0/0   │─────────┘      │ 0.0.0.0/0   │────────┘    │
│    │  → NAT GW 1 │               │  → NAT GW 2 │             │
│    └─────────────┘               └─────────────┘             │
│                                                                  │
│                    ┌─────────────────┐                           │
│                    │ INTERNET GATEWAY│ ← 1 per VPC (managed)    │
│                    └────────┬────────┘                           │
└─────────────────────────────┼────────────────────────────────────┘
                              │
                         INTERNET
```

***

## Component Inventory

```
VPC                    ×1    FREE     ← network container
Public Subnets         ×2    FREE     ← internet-facing (1 per zone)
Private Subnets        ×2    FREE     ← isolated (1 per zone)
Internet Gateway       ×1    FREE     ← bidirectional internet (managed HA)
NAT Gateways           ×2    💰 PAID  ← outbound-only internet (1 per zone for HA)
Route Tables           ×4    FREE     ← 1 per subnet (traffic decision engine)
Bastion Host           ×1    EC2 cost ← SSH jump point to private instances
```

***

## Gateway Comparison

```
INTERNET GATEWAY                    NAT GATEWAY
─────────────────                   ────────────
Bidirectional (in + out)            Outbound-only (out + response)
Attached to VPC                     Lives in PUBLIC subnet
1 per VPC (sufficient)              1 per zone (for HA)
FREE                                💰 CHARGEABLE
Managed HA by AWS                   Manual HA (create in each zone)
Public subnets route to it          Private subnets route to it
```

***

## What Makes a Subnet Public vs. Private

```
PUBLIC SUBNET:
  Route table: 0.0.0.0/0 → Internet Gateway
  Instances: have public IPs
  Traffic: bidirectional internet

PRIVATE SUBNET:
  Route table: 0.0.0.0/0 → NAT Gateway
  Instances: private IPs only
  Traffic: outbound internet only (+ responses)

KEY INSIGHT: The ROUTE TABLE determines public/private, not a label on the subnet
```

***

## Traffic Flow Patterns

```
INBOUND FROM INTERNET → PUBLIC INSTANCE:
  Internet → IGW → public subnet → instance
  (SSH to EC2 via public IP)

OUTBOUND FROM PRIVATE INSTANCE → INTERNET:
  Private instance → NAT GW (public subnet) → IGW → Internet → response back
  (apt install, download packages)

INBOUND FROM INTERNET → PRIVATE INSTANCE:
  ❌ BLOCKED — no path exists (no public IP, no IGW route)

ADMIN ACCESS TO PRIVATE INSTANCE:
  Laptop → SSH → Bastion Host (public) → SSH → Private Instance
  (all VPC subnets communicate internally by default)

CORPORATE ACCESS TO PRIVATE INSTANCE:
  Corporate network → VPN Gateway → private subnet (via private IP)
```

***

## WiFi Router Analogy (NAT Gateway)

```
YOUR HOME NETWORK           ←→      AWS PRIVATE SUBNET
─────────────────                    ─────────────────
Laptop (private IP)          =       EC2 instance (private IP)
WiFi Router (public IP)      =       NAT Gateway (in public subnet)
ISP                          =       Internet Gateway
Internet                     =       Internet

Laptop → Router → Internet   ✅      Private EC2 → NAT GW → IGW → Internet  ✅
Internet → Laptop            ❌      Internet → Private EC2                   ❌
```

***

## High Availability Pattern

```
PROBLEM:  Zone failure takes down all resources in that zone
SOLUTION: Distribute subnets and resources across multiple zones

MINIMUM VIABLE HA DESIGN (2 zones):
  Zone 1: 1 public subnet + 1 private subnet + 1 NAT GW
  Zone 2: 1 public subnet + 1 private subnet + 1 NAT GW

INSTANCE DISTRIBUTION:
  4 web servers → 2 in Zone 1 public, 2 in Zone 2 public
  Zone 1 fails → 2 servers still running in Zone 2

NAT GW HA:
  1 NAT GW per zone → zone failure doesn't kill other zone's outbound access
```

***

## Intra-VPC Communication Rule

```
ALL subnets in a VPC communicate with each other BY DEFAULT
  Public ↔ Public     ✅
  Private ↔ Private   ✅
  Public ↔ Private    ✅ (this enables bastion host pattern)

Controlled by: local routes in route tables + security groups
Public/Private distinction = INTERNET-FACING behavior only
```

***

## Cost Decision Map

```
Component          Cost      HA Implication
────────────       ──────    ──────────────
VPC                Free      N/A
Subnets            Free      Create in multiple zones
Route Tables       Free      One per subnet
Internet Gateway   Free      Managed HA (single is sufficient)
NAT Gateway        💰 PAID   Need one per zone for HA → cost doubles
                             Dev: 1 NAT GW (cheaper, lower HA)
                             Prod: 2+ NAT GWs (HA, higher cost)
```

***

## Bastion Host Access Pattern

```
YOUR LAPTOP
    │
    │ SSH (public IP)
    ▼
BASTION HOST (public subnet)
    │
    │ SSH (private IP, VPC-internal)
    ▼
PRIVATE INSTANCE (private subnet)

PREREQUISITE: all VPC subnets can communicate internally
SECURITY: bastion host SG → SSH from your IP only
```

***

## Reusable Engineering Pattern: Public-Private Network Segmentation with Gateway Routing

```
PATTERN:
  Divide network into PUBLIC zone (internet-facing) and PRIVATE zone (isolated)
  Use GATEWAY DEVICES to control traffic flow between zones and internet
  Use ROUTE TABLES as the decision engine for traffic direction

SECURITY PROPERTY:
  Private zone cannot be reached from internet
  Private zone CAN reach internet (outbound-only via NAT)

HA PROPERTY:
  Replicate zones across fault domains (AZs)
  Replicate gateways for each zone

COST PROPERTY:
  Most networking components are free
  NAT (outbound translation) is the cost center

WHERE ELSE:
  • Any cloud provider VPC (Azure VNet, GCP VPC — same pattern)
  • On-premise DMZ architecture (public-facing DMZ + internal network)
  • Container networking (public ingress + private service mesh)
  • Home networking (router NAT = same concept at small scale)
```

***

## One-Line Mental Reload Trigger

> *"VPC splits into public subnets (route to IGW, bidirectional internet) and private subnets (route to NAT GW in public subnet, outbound-only) — distribute across 2+ zones for HA, bastion host jumps into private, NAT GW is the only paid component, all VPC subnets communicate internally by default."*

This single sentence reconstructs the full architecture, both gateway types and their behavioral difference, the routing mechanism, the HA strategy, the access pattern for private instances, the cost model, and the default communication rule. [\[264-vpc-de...components \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/264-vpc-design-and-components.txt)
