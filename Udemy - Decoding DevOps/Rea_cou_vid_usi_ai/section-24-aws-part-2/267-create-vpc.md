# 🎓 Deep Learning Material: AWS VPC Creation — CIDR Block and Architectural Foundation

**Source:** [267-create-vpc.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt?EntityRepresentationId=47480b88-39f7-4889-85c6-01016341678b) — Video lecture covering AWS VPC creation approaches (automated full-stack vs manual component-by-component), the VPC CIDR block, the architectural diagram with public/private subnets across two availability zones, NAT gateway cost considerations, VPC tenancy, VPC endpoints, the automated flow visualization, and the deliberate choice to build each component manually for deep learning. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Two Ways to Create a VPC — And Why We Choose the Hard Way

AWS provides two approaches to creating a VPC through the console UI. The first is the **automated approach** — "VPC and more" — where you fill in a form specifying your CIDR range, number of availability zones, number of public and private subnets, NAT gateways, and VPC endpoints. AWS then creates the entire networking stack in one click: VPC, all subnets, internet gateway, NAT gateway, route tables, and their associations. This is fast and convenient, especially if you already have an architectural diagram and know your network ranges. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The second approach is **manual creation** — creating each component individually (VPC range first, then subnets, then internet gateway, then NAT gateway, then route tables) and joining them together step by step. This is slower but provides deep understanding of how each component works and how they interconnect. Critically, it also teaches you what to check and fix when something goes wrong — because you understand the assembly, you can diagnose the breakdown. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The video explicitly chooses the manual approach for learning purposes. The instructor walks through the automated form to show what it does and to visualize the architecture, but then cancels the creation and starts over with "VPC only." The message is clear: the automated method is for production speed once you understand the system; the manual method is for building that understanding. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## 1.2 The VPC CIDR Block — What It Is

A VPC (Virtual Private Cloud) is an isolated network within AWS. The first and most fundamental thing you define when creating a VPC is its **CIDR block** — the IP address range that the entire VPC will use. In this project, the CIDR block is `172.20.0.0/16`. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The `/16` means the first 16 bits of the address are fixed (the network portion: `172.20`), and the remaining 16 bits are available for hosts and subnets. This gives 65,536 possible IP addresses within the VPC — a large range that can be subdivided into many subnets. Every resource launched inside this VPC (EC2 instances, RDS databases, Lambda functions, etc.) will receive an IP address from within this range. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The CIDR block is the **boundary** of the VPC. No IP address outside this range belongs to the VPC. No two VPCs in the same account should have overlapping CIDR blocks if you intend to peer them. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## 1.3 The Target Architecture — Subnets, Zones, and Gateways

The video references an architectural diagram that defines the target VPC layout. The architecture has:

**Two Availability Zones:** `us-west-1a` and `us-west-1b`. Distributing resources across two AZs provides **high availability** — if one data center (AZ) fails, the other continues operating. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Four Subnets:** Two public subnets and two private subnets — one of each per availability zone.

| Subnet   | Type    | CIDR            | AZ         |
| -------- | ------- | --------------- | ---------- |
| Subnet 1 | Public  | `172.20.1.0/24` | us-west-1a |
| Subnet 2 | Public  | `172.20.2.0/24` | us-west-1b |
| Subnet 3 | Private | `172.20.3.0/24` | us-west-1a |
| Subnet 4 | Private | `172.20.4.0/24` | us-west-1b |

Each subnet uses `/24`, which allocates 256 addresses (the last octet is variable). The sequential numbering (1.0, 2.0, 3.0, 4.0) is not mandatory — you could use any non-overlapping ranges within the VPC's `/16` — but sequential numbering is easier to identify and manage. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Internet Gateway:** Connects the VPC to the public internet. Public subnet traffic is routed through the internet gateway via the route table. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**NAT Gateway:** Allows private subnet instances to reach the internet (for updates, API calls, etc.) without being directly accessible from the internet. Private subnet traffic is routed through the NAT gateway. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Route Tables:** The mechanism that directs traffic. Public subnets have a route table pointing to the internet gateway. Private subnets have a route table pointing to the NAT gateway. The video shows this flow visually in the automated VPC creation preview. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## 1.4 NAT Gateway Cost Awareness

The instructor makes a deliberate architectural deviation from the ideal design: instead of creating **two NAT gateways** (one per AZ, for high availability), only **one NAT gateway** and **one elastic IP** will be created. The reason is purely cost: "NAT gateways are expensive. If you keep it running for a longer time, you will see the bills that you will get worried about." [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

For production high availability, you **should** have two NAT gateways (one per AZ) each with its own elastic IP. If the single NAT gateway's AZ goes down, private instances in the other AZ lose internet access. But for learning, one is sufficient to understand the mechanism, and the cost savings are significant. The instructor also reassures: once the VPC section is complete, cleanup will be performed to avoid ongoing charges. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The AWS console itself signals the cost implication — the NAT gateway option shows a **dollar symbol** indicating additional charges. The instructor notes: "Click on info and find out, but don't worry for now." [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## 1.5 VPC Tenancy

When creating a VPC, you choose between **default** and **dedicated** tenancy. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Default tenancy** means your VPC's resources run on **shared hardware** — your EC2 instances share the physical server with instances from other AWS customers. This is the standard, cost-effective option. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Dedicated tenancy** means your VPC gets **dedicated physical hardware** — no other customer's workloads run on the same server. This is significantly more expensive but is required by some compliance frameworks (financial, healthcare, government) that mandate physical isolation. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The video selects **default** tenancy. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## 1.6 VPC Endpoints — Private Access to AWS Services

The automated VPC creation form includes an option for **VPC endpoints**. VPC endpoints allow resources in your **private subnet** to access AWS services (like S3 buckets) **without going through the internet**. Normally, accessing S3 from a private subnet would require traffic to go through the NAT gateway → internet → S3 and back. A VPC endpoint creates a private pathway directly from the VPC to the AWS service, bypassing the internet entirely. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The video mentions this briefly as part of the automated form walkthrough but does not create VPC endpoints in this project. It is introduced conceptually so you know the option exists. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## 1.7 The Default Route Table

When you create a VPC (even with "VPC only"), AWS automatically creates a **default route table** for it. The instructor explicitly states: "We are not going to use that route table." Custom route tables will be created separately and associated with the appropriate subnets. The default route table exists as a fallback — any subnet not explicitly associated with a custom route table uses the default one. But for clean, explicit architecture, custom route tables are preferred. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## 1.8 The Traffic Flow Model

The automated VPC preview shows the traffic routing visually:

**Public subnet instances:** Traffic flows through the **route table** → **internet gateway** → internet. This allows both inbound and outbound internet access. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Private subnet instances:** Traffic flows through the **route table** → **NAT gateway** → internet. This allows outbound internet access (instance can reach the internet) but prevents inbound access (internet cannot initiate connections to the instance). [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**VPC endpoint traffic (if configured):** Traffic from private subnets to AWS services (like S3) flows through the VPC endpoint, staying entirely within the AWS network. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

This flow model is the core architectural logic that all subsequent lectures (subnets, internet gateway, NAT gateway, route tables) will implement piece by piece. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating the foundational VPC CIDR block (`172.20.0.0/16`) for the vProfile project in the `us-west-1` region. This is only the network range — no subnets, no gateways, no route tables yet. Those will be created in subsequent lectures and connected to this VPC. The final outcome of this lecture: a VPC exists in AWS with the defined IP range, ready to receive subnets. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

***

## Step 1: Explore the Automated VPC Creation (Do Not Create)

This step is observational — we fill in the form to see the architecture visualization but do NOT click Create.

**1a.** Navigate to **VPC → Your VPCs → Create VPC**. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**1b.** Select **"VPC and more"** (the full-stack option). [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**1c.** Fill in the fields for visualization:

| Field                     | Value           |
| ------------------------- | --------------- |
| Name tag                  | `vprofile`      |
| IPv4 CIDR block           | `172.20.0.0/16` |
| Tenancy                   | Default         |
| Number of AZs             | 2               |
| AZ 1                      | `us-west-1a`    |
| AZ 2                      | `us-west-1b`    |
| Number of public subnets  | 2               |
| Number of private subnets | 2               |

 [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**1d.** Customize subnet CIDR blocks:

| Subnet           | CIDR            |
| ---------------- | --------------- |
| Public subnet 1  | `172.20.1.0/24` |
| Public subnet 2  | `172.20.2.0/24` |
| Private subnet 3 | `172.20.3.0/24` |
| Private subnet 4 | `172.20.4.0/24` |

 [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**1e.** NAT gateway: Observe the **dollar symbol** — this means additional charges. You can select "1 per AZ" (creates 2) or "In 1 AZ" (creates 1). For learning, we will create 1 manually in a later lecture. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**1f.** VPC endpoints: Note the option exists for private access to S3 and other services. We skip it for now. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**1g.** Observe the **architecture preview** on the right side:

* Public subnets route through route tables → internet gateway
* Private subnets route through route tables → NAT gateway
* VPC endpoint traffic flows separately to AWS services

This visualization confirms the target architecture. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**1h.** ⚠️ **DO NOT click Create VPC.** Click **Cancel**. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Connection to larger flow:** This step builds a mental picture of the complete VPC before we create each component manually.

***

## Step 2: Create the VPC (CIDR Block Only)

**2a.** From the VPC dashboard, click **Create VPC** again. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**2b.** This time, select **"VPC only"** (not "VPC and more"). [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**2c.** Fill in the fields:

| Field           | Value           |
| --------------- | --------------- |
| Name tag        | `vprofile-vpc`  |
| IPv4 CIDR block | `172.20.0.0/16` |
| Tenancy         | Default         |

 [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

The name tag is automatically applied. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**2d.** Click **Create VPC**. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Expected result:** The VPC is created and appears in your VPC list. You will see:

* The VPC with its CIDR range `172.20.0.0/16`
* A **default route table** automatically created (we will NOT use this — custom route tables will be created later)
* **No subnets** — those are next lecture
* **No internet gateway** — created later
* **No NAT gateway** — created later

 [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Verification:** Navigate to **Your VPCs** and confirm `vprofile-vpc` appears with the correct CIDR block. [\[267-create-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/267-create-vpc.txt)

**Connection to larger flow:** The VPC is now the empty container — the network boundary. The next lecture creates four subnets inside this VPC, followed by internet gateway, NAT gateway, and route tables in subsequent lectures.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Target VPC Architecture

```
VPC: 172.20.0.0/16 (vprofile-vpc)
│
├── AZ: us-west-1a
│     ├── Public Subnet:  172.20.1.0/24  ──→ Route Table ──→ Internet Gateway ──→ Internet
│     └── Private Subnet: 172.20.3.0/24  ──→ Route Table ──→ NAT Gateway ──→ Internet
│
├── AZ: us-west-1b
│     ├── Public Subnet:  172.20.2.0/24  ──→ Route Table ──→ Internet Gateway ──→ Internet
│     └── Private Subnet: 172.20.4.0/24  ──→ Route Table ──→ NAT Gateway ──→ Internet
│
├── Internet Gateway (1)
├── NAT Gateway (1, cost saving — ideally 2 for HA)
├── Elastic IP (1, for NAT Gateway)
└── VPC Endpoint (optional — private access to S3/AWS services)
```

***

## Two Creation Approaches

```
"VPC and more":
  → Fill form → AWS creates EVERYTHING (VPC + subnets + IGW + NAT + routes)
  → Fast, convenient, production-ready
  → Requires: architectural diagram + CIDR plan already done

"VPC only":
  → Creates ONLY the CIDR block
  → Subnets, IGW, NAT, routes created manually in separate steps
  → Slow, but deep understanding + debugging capability

Choice for learning: VPC only → build each component → join together
```

***

## CIDR Block

```
VPC:     172.20.0.0/16     → 65,536 IPs (first 16 bits fixed)
Subnets: 172.20.x.0/24    → 256 IPs each (first 24 bits fixed)

Subnet CIDR plan:
  1.0/24  →  public,  us-west-1a
  2.0/24  →  public,  us-west-1b
  3.0/24  →  private, us-west-1a
  4.0/24  →  private, us-west-1b

Sequential numbering = convention (not mandatory), easier to manage
```

***

## Traffic Flow Model

```
PUBLIC subnet instance:
  Instance → Route Table → Internet Gateway → Internet
  (bidirectional — inbound + outbound)

PRIVATE subnet instance:
  Instance → Route Table → NAT Gateway → Internet
  (outbound only — internet cannot initiate inbound)

PRIVATE to AWS service (S3):
  Instance → VPC Endpoint → S3  (bypasses internet entirely)
```

***

## Cost Considerations

```
NAT Gateway:
  Ideal: 2 (one per AZ) + 2 Elastic IPs → high availability
  Lab:   1 + 1 Elastic IP → cost saving
  ⚠️ Dollar symbol in AWS UI = extra charges
  ⚠️ Clean up after completing VPC section

Dedicated tenancy:
  Default = shared hardware (use this)
  Dedicated = isolated hardware (expensive, compliance-driven)
```

***

## What Gets Auto-Created

```
Creating "VPC only":
  ✓ VPC with CIDR block
  ✓ Default route table (DO NOT USE — create custom ones)
  ✗ No subnets
  ✗ No internet gateway
  ✗ No NAT gateway
  ✗ No custom route tables
```

***

## Build Sequence (This Lecture → Future)

```
THIS:   VPC CIDR block (172.20.0.0/16)                    ← done
NEXT:   4 subnets (public × 2, private × 2)               ← next lecture
THEN:   Internet gateway → attach to VPC
THEN:   NAT gateway + elastic IP → in public subnet
THEN:   Route tables → associate with subnets
THEN:   Cleanup (delete NAT/EIP to stop charges)
```

***

## Key Engineering Patterns

| Pattern                          | Manifestation                                                                                      |
| -------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Manual assembly for learning** | Build each component separately → understand connections → debug when broken                       |
| **Cost-aware architecture**      | Deviate from ideal (2 NAT GW) for lab to minimize charges — know what you sacrifice (HA)           |
| **Network boundary first**       | VPC CIDR block = outer boundary → everything else lives inside it                                  |
| **Sequential CIDR allocation**   | 1.0, 2.0, 3.0, 4.0 — convention for readability, not requirement                                   |
| **Public vs private = routing**  | The subnet itself isn't inherently public or private — the route table association makes it so     |
| **Default resource awareness**   | AWS auto-creates default route table — explicitly choose not to use it → create custom for clarity |

***

This completes the full reconstruction. **Theory** explains the VPC concept, CIDR planning, traffic flow model, and cost tradeoffs. **Practical** walks through both the automated preview and the manual VPC-only creation. The **Compression Map** gives you the complete target architecture diagram, CIDR plan, traffic flow, and build sequence for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
