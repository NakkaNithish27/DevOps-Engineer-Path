# 🎓 Deep Learning Material: VPC Setup Details — Network Blueprint Design Before Implementation

**Source:** Video lecture on VPC setup planning and blueprint (from [265-vpc-setup-details.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt?EntityRepresentationId=7f9da167-87f6-4f62-9eda-5e05f0704566) caption file) [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

**Video Context:** This is a **planning lecture** — no resources are created yet. The instructor designs the complete VPC blueprint on paper/screen before touching the AWS Console. Every component is named, numbered, and justified: VPC CIDR, four subnets across two availability zones, internet gateway, NAT gateway with elastic IP, two route tables, a bastion host, NACL, and a second VPC for peering. The lecture's primary value is in the **network architecture design thinking** — understanding why each component exists, how many you need, where they go, and what connects to what. The instructor explicitly states this is the blueprint they will follow in the implementation lecture that follows.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Blueprint-First Approach: Design Before Build

The instructor opens with a critical engineering principle: *"before we start doing it, we'll create the blueprint."* This means designing the complete network architecture — with specific CIDR ranges, zone placements, and component counts — before touching the AWS Console. This prevents ad-hoc decisions during creation that lead to inconsistent architectures, IP conflicts, and design gaps. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

The blueprint captures: the VPC CIDR range, the number and type of subnets, their zone distribution, every networking component needed (gateways, route tables, elastic IPs), and additional features to explore (NACL, VPC peering). This is the **design document** that the implementation will follow.

***

## 1.2 — VPC CIDR Range: The Master Network Address Space

The VPC is assigned the CIDR block **`172.20.0.0/16`**. The `/16` subnet mask means the first two octets (`172.20`) are fixed (the network portion), and the remaining two octets are available for host addresses. This provides **65,536 IP addresses** (2^16) — the instructor confirms: *"You know that gives us like, more than 65,000 IP addresses."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

This is the **master range** — every subnet, instance, load balancer, and internal resource within this VPC will get an IP address from this pool. The `172.20.x.x` range falls within the RFC 1918 private address space (`172.16.0.0 – 172.31.255.255`), meaning these addresses are only valid inside the VPC and are not routable on the public internet. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

## 1.3 — Subnets: Dividing the Network into Smaller, Purpose-Specific Segments

The `/16` range must be divided into **smaller subnets** — each subnet gets a portion of the address space and serves a specific purpose. The instructor creates **four subnets**: [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

| Subnet   | CIDR            | Type        | Availability Zone |
| -------- | --------------- | ----------- | ----------------- |
| Subnet 1 | `172.20.1.0/24` | **Public**  | US-West-1A        |
| Subnet 2 | `172.20.2.0/24` | **Public**  | US-West-1B        |
| Subnet 3 | `172.20.3.0/24` | **Private** | US-West-1A        |
| Subnet 4 | `172.20.4.0/24` | **Private** | US-West-1B        |

Each `/24` subnet provides **256 IP addresses** (2^8, minus AWS-reserved addresses). [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

**Why two of each type:** High availability. Each subnet type (public and private) is distributed across **two different availability zones** (US-West-1A and US-West-1B). If one AZ experiences a failure, the other AZ still has both a public and private subnet operational. The instructor explicitly states: *"two for high availability, we are going to divide it among multiple zones, two zones, specifically."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

**Public vs. Private subnets:** The difference is not inherent to the subnet itself — it's determined by the **route table** attached to the subnet. A subnet whose route table has a route to an **internet gateway** is public (instances can reach the internet directly). A subnet whose route table routes through a **NAT gateway** is private (instances can reach the internet only through NAT, and cannot be directly reached from the internet). [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

## 1.4 — Region and Availability Zone Selection

The instructor selects **US-West-1 (North California)** as the region. This region has exactly **two availability zones**: `US-West-1A` and `US-West-1B`. The four subnets are distributed evenly across these two zones — one public and one private in each zone. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

The zone choice is driven by the high-availability requirement. Having resources in only one zone creates a single point of failure at the zone level. Distributing across two zones means a zone-level failure only affects half the infrastructure. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

## 1.5 — Internet Gateway: The Door to the Public Internet

The VPC needs **one internet gateway** — this is the component that enables communication between the VPC and the public internet. Without it, nothing in the VPC can reach the internet, and nothing on the internet can reach the VPC. The internet gateway is attached to the VPC (not to individual subnets) and is referenced in route tables. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

Only **one** internet gateway is needed per VPC — it's a highly available, redundant component managed by AWS. You don't need multiple for HA. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

## 1.6 — NAT Gateway: Internet Access for Private Subnets

Private subnets need to reach the internet (for package updates, downloading patches, accessing external APIs) but should **not** be directly accessible from the internet. The **NAT gateway** solves this: it sits in a **public subnet**, has a public-facing **elastic IP**, and translates outbound traffic from private subnet instances to the internet. Return traffic comes back through the NAT gateway, but unsolicited inbound traffic cannot reach the private instances. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

The instructor makes a deliberate cost-saving decision: *"We need two NAT gateways, but for the sake of saving cost, we'll just create one single NAT gateway."* He immediately notes the production standard: *"if you're doing high availability for NAT gateway, then you should have minimum two NAT gateways distributed in two different zones."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

Unlike the internet gateway (which is HA by default), NAT gateways are **zone-specific**. If the zone containing the single NAT gateway fails, private subnets in the other zone lose internet access. For production, you need one NAT gateway per zone.

**Elastic IP:** The NAT gateway requires an **elastic IP** — a static public IP address that doesn't change. The instructor includes this as a separate component: *"You also need one elastic IP, which will be assigned for the NAT gateway."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

## 1.7 — Route Tables: The Traffic Routing Rules

**Two route tables** are needed — one for public subnets and one for private subnets: [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

**Public route table:** Contains a route that sends internet-bound traffic (`0.0.0.0/0`) to the **internet gateway**. This is attached to both public subnets.

**Private route table:** Contains a route that sends internet-bound traffic (`0.0.0.0/0`) to the **NAT gateway**. This is attached to both private subnets.

The instructor explains: *"this subnets route table will be attached to these subnets, and it will tell public subnet to go to the internet gateway, and private subnet to go to the NAT gateway."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

This is the mechanism that **defines** whether a subnet is public or private. The subnet itself doesn't have a "public" or "private" property — it's entirely determined by its associated route table.

***

## 1.8 — Bastion Host (Jump Server): Accessing Private Instances

Instances in private subnets have no public IP and no direct internet-facing route. So how do you SSH into them for administration? Through a **bastion host** (also called a jump server) — an instance placed in the **public subnet** that you SSH into first, and from there SSH into private instances. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

The instructor plans: *"We'll need also one bastion host or the jump server in the public subnet so we can access instances in the private subnet."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

The bastion host is the **only entry point** from the outside into the private network. Its security group is tightly controlled (typically SSH from specific IPs only), and it acts as a security checkpoint.

***

## 1.9 — NACL (Network Access Control List): Subnet-Level Firewall

After the VPC is fully set up, the instructor plans to demonstrate **NACLs** — network access control lists. NACLs are **subnet-level firewalls**, as opposed to security groups which are **instance-level firewalls**. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

The key differences the instructor highlights: [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

| Feature | Security Group | NACL               |
| ------- | -------------- | ------------------ |
| Level   | Instance       | Subnet             |
| Rules   | **Allow only** | **Allow AND Deny** |
| Control | Basic          | More granular      |

The instructor explains: *"It's like a firewall, like you have security group. It's gonna be similar to that, but will give you more control, and this is for the subnet. Like security group is for the instance, NACL is for the subnet, and in NACL, you have allow and deny rule both. In security group, you just have the allow rule."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

## 1.10 — VPC Peering: Connecting Two VPCs

The instructor plans to create a **second VPC** — not a full VPC with subnets and gateways, just the VPC shell — to demonstrate **VPC peering**. VPC peering connects two VPCs so that instances in one VPC can communicate with instances in the other VPC using private IP addresses, as if they were on the same network. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

*"We'll just create the VPC, and we'll peer our main VPC with the other VPC that we just created."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are designing a **complete VPC network blueprint** that will be implemented in the next lecture. The blueprint specifies every component, its configuration values, and its placement. The final outcome of this lecture is a **documented design** — not running infrastructure — that serves as the implementation guide.

This blueprint-first approach prevents ad-hoc decisions during creation and ensures all components are accounted for before any resources are provisioned.

***

## The Complete Blueprint

### Network Foundation

| Component    | Value                        | Notes             |
| ------------ | ---------------------------- | ----------------- |
| **Region**   | US-West-1 (North California) | Has exactly 2 AZs |
| **VPC CIDR** | `172.20.0.0/16`              | \~65,000 IPs      |

 [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

### Subnets (4 total)

| # | Name/Purpose     | CIDR            | Type    | AZ         |
| - | ---------------- | --------------- | ------- | ---------- |
| 1 | Public Subnet 1  | `172.20.1.0/24` | Public  | US-West-1A |
| 2 | Public Subnet 2  | `172.20.2.0/24` | Public  | US-West-1B |
| 3 | Private Subnet 1 | `172.20.3.0/24` | Private | US-West-1A |
| 4 | Private Subnet 2 | `172.20.4.0/24` | Private | US-West-1B |

Each `/24` = 256 addresses. Two of each type across two AZs for HA. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

### Networking Components

| Component            | Count | Notes                                                 |
| -------------------- | ----- | ----------------------------------------------------- |
| **Internet Gateway** | 1     | Attached to VPC; HA by default                        |
| **NAT Gateway**      | 1     | In a public subnet; ideally 2 for HA (cost saving: 1) |
| **Elastic IP**       | 1     | Assigned to the NAT Gateway                           |
| **Route Tables**     | 2     | 1 public (→ IGW), 1 private (→ NAT GW)                |
| **Bastion Host**     | 1     | In public subnet; SSH jump point to private instances |

 [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

### Additional Features to Explore

| Feature         | Purpose                                                            |
| --------------- | ------------------------------------------------------------------ |
| **NACL**        | Subnet-level firewall with allow + deny rules (for public subnet)  |
| **VPC Peering** | Connect main VPC with a second VPC for cross-VPC communication     |
| **Second VPC**  | Created minimally (just VPC, no subnets) for peering demonstration |

 [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

### Route Table Associations

| Route Table | Associated Subnets                  | Default Route (`0.0.0.0/0`) |
| ----------- | ----------------------------------- | --------------------------- |
| Public RT   | Public Subnet 1 + Public Subnet 2   | → Internet Gateway          |
| Private RT  | Private Subnet 1 + Private Subnet 2 | → NAT Gateway               |

 [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

### Design Decisions and Trade-offs

**NAT Gateway count (1 vs. 2):**

* Production: 2 NAT gateways, one per AZ (HA)
* This exercise: 1 NAT gateway (cost saving)
* Risk: if the NAT GW's AZ fails, private subnets in the other AZ lose internet access [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

**Region selection (US-West-1):**

* Chosen because it has exactly 2 AZs — matches the 2-zone design
* Different regions have different numbers of AZs (some have 3+) [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

**CIDR planning:**

* VPC: `/16` (large pool, room for growth)
* Subnets: `/24` (256 addresses each, 4 subnets = 1,024 used out of 65,536 available)
* Leaves room for future subnets if needed [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

**Connection to next lecture:** *"with all that information, we can go to AWS console and start creating our VPC."* [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Complete VPC Architecture

```
REGION: US-West-1 (North California)
VPC: 172.20.0.0/16

                    US-West-1A                    US-West-1B
                ┌─────────────────┐          ┌─────────────────┐
  PUBLIC        │  172.20.1.0/24  │          │  172.20.2.0/24  │
                │  [Bastion Host] │          │                 │
                │  [NAT Gateway]  │          │                 │
                └────────┬────────┘          └────────┬────────┘
                         │                            │
              Public Route Table (→ Internet Gateway)
                         │
                ┌────────┴─────────────────────────────┐
                │          INTERNET GATEWAY             │
                └──────────────────────────────────────┘
                                  │
                              INTERNET

                    US-West-1A                    US-West-1B
                ┌─────────────────┐          ┌─────────────────┐
  PRIVATE       │  172.20.3.0/24  │          │  172.20.4.0/24  │
                │  [App servers]  │          │  [App servers]  │
                └────────┬────────┘          └────────┬────────┘
                         │                            │
              Private Route Table (→ NAT Gateway)
```

***

## 🔷 Component Inventory

```
VPC:              1  (172.20.0.0/16)
Subnets:          4  (2 public + 2 private, across 2 AZs)
Internet Gateway: 1  (HA by default)
NAT Gateway:      1  (should be 2 for HA; cost saving)
Elastic IP:       1  (for NAT Gateway)
Route Tables:     2  (1 public → IGW, 1 private → NAT GW)
Bastion Host:     1  (in public subnet, SSH jump to private)
NACL:             1  (for public subnet, allow + deny rules)
Second VPC:       1  (minimal, for peering demo only)
```

***

## 🔷 Subnet CIDR Map

```
VPC: 172.20.0.0/16 (65,536 IPs)
  │
  ├── 172.20.1.0/24  → Public,  AZ-1A  (256 IPs)
  ├── 172.20.2.0/24  → Public,  AZ-1B  (256 IPs)
  ├── 172.20.3.0/24  → Private, AZ-1A  (256 IPs)
  └── 172.20.4.0/24  → Private, AZ-1B  (256 IPs)
  
  Used: 1,024 / 65,536 → room for many more subnets
```

***

## 🔷 What Makes a Subnet Public vs. Private

```
SUBNET itself has NO "public" or "private" property.

It's determined by ROUTE TABLE:

  Route Table has 0.0.0.0/0 → Internet Gateway   = PUBLIC subnet
  Route Table has 0.0.0.0/0 → NAT Gateway         = PRIVATE subnet
```

***

## 🔷 Traffic Flow

```
PUBLIC SUBNET INSTANCE → Internet:
  Instance → Route Table → Internet Gateway → Internet
  (bidirectional: internet can also reach instance)

PRIVATE SUBNET INSTANCE → Internet:
  Instance → Route Table → NAT Gateway → Internet Gateway → Internet
  (outbound only: internet CANNOT reach instance directly)

ADMIN → PRIVATE INSTANCE:
  Admin → SSH to Bastion (public subnet) → SSH to private instance
```

***

## 🔷 Security Layers

```
LAYER 1: NACL (subnet-level)
  → Allow AND Deny rules
  → Applied to entire subnet
  → Stateless

LAYER 2: Security Group (instance-level)
  → Allow rules ONLY
  → Applied to individual instances
  → Stateful
```

***

## 🔷 HA Design Decisions

```
COMPONENT         IDEAL (HA)     THIS EXERCISE    RISK
────────────      ──────────     ──────────────   ─────────────────
Internet GW       1 (auto-HA)    1                None (AWS manages)
NAT GW            2 (per AZ)     1 (cost save)    AZ failure → no internet for private
Subnets           2+ per type    2 per type       ✅ Covered
Bastion           2 (per AZ)     1                Minor (can recreate)
```

***

## 🔷 VPC Peering (Planned)

```
VPC-1 (main, fully built)  ←── PEERING ──→  VPC-2 (minimal, just VPC shell)

Peering = private IP communication between two VPCs
        = as if they're on the same network
        = no internet traversal
```

***

## 🔷 Reusable Engineering Pattern: Blueprint-First Network Design

```
PATTERN: Design → Document → Build

1. DEFINE address space (VPC CIDR — large enough for growth)
2. DIVIDE into subnets (public/private × availability zones)
3. LIST all components (gateways, route tables, EIPs, bastion)
4. MAP routing rules (which subnet → which gateway)
5. IDENTIFY security layers (SG + NACL)
6. NOTE trade-offs (HA vs. cost: NAT GW count)
7. THEN build in AWS Console

WHY:
  → Prevents IP conflicts and overlapping CIDRs
  → Ensures HA requirements are met before creation
  → Creates a reference document for the team
  → Makes the implementation step mechanical (just follow the blueprint)

This pattern applies to:
  → Any cloud VPC/VNet design
  → On-premises network architecture
  → Kubernetes cluster networking
  → Multi-region/multi-account architectures
```

This is a **planning lecture**, not an execution lecture. Its value is entirely in the architectural thinking: knowing what components exist, why each is needed, how many you need, where they go, and what connects to what. The implementation that follows in the next lecture is just mechanical execution of this blueprint. [\[265-vpc-se...up-details \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/265-vpc-setup-details.txt)
