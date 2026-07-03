# 🧠 AWS VPC Peering — Cross-VPC Connectivity, Routing & Security

**Source:** *274. Peering* — AWS VPC / Networking Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why VPC Peering Exists — The Multi-VPC Reality

In the previous lectures, the focus was on building a single VPC with public and private subnets to achieve security and high availability. But in large-scale environments, a single VPC is rarely sufficient. Organizations commonly operate **multiple VPCs** — one for web infrastructure, one for APIs, one for databases, one per team, one per environment (dev/staging/prod), or even VPCs spread across different regions and AWS accounts.

The problem: VPCs are **isolated by design**. An EC2 instance in VPC-A cannot communicate with an EC2 instance in VPC-B — they are separate private networks with no connectivity between them, even if they're in the same AWS account. If your web servers are in one VPC and your database is in another VPC, they simply cannot reach each other.

**VPC Peering** solves this by creating a direct network connection between two VPCs, allowing resources in one to communicate with resources in the other using their private IP addresses. The instructor frames it simply: *"In order to connect your resource from one VPC to other VPC, you need to do VPC peering. It's very easy to do, but very much required."*

***

## 1.2 VPC Peering — What It Is and Its Scope

A VPC peering connection is a **one-to-one networking link** between two VPCs. Once established, instances in both VPCs can communicate as if they were on the same network — using private IPs, without traffic traversing the public internet.

VPC peering is flexible in scope. You can peer:

* Two VPCs in the **same region** (same account)
* Two VPCs in **different regions** (cross-region peering, demonstrated in this lecture)
* Two VPCs in **different AWS accounts** (cross-account peering — the instructor mentions this requires providing the account ID)

The lecture demonstrates cross-region peering: the existing `vprofile-VPC` in **North California** is peered with a new `vpro-db` VPC created in **Oregon**.

***

## 1.3 The CIDR Non-Overlap Rule — The Fundamental Constraint

When creating a VPC that will be peered with another, the **CIDR ranges must not overlap**. This is a hard requirement — if both VPCs use `172.20.0.0/16`, the routing system cannot distinguish which VPC a destination IP belongs to.

The instructor demonstrates this explicitly: the North California VPC uses `172.20.0.0/16`, so the Oregon VPC is created with `172.21.0.0/16` (or `172.22.0.0/16`). The key principle: *"CIDR range cannot overlap."* Any non-overlapping range works — `/16`, `/24`, or any valid CIDR.

> 🔍 **Deep Dive:** CIDR overlap checking is not just about the two VPCs you're peering. In environments with many peered VPCs, you need to plan your entire IP address space to ensure no two VPCs that might ever need to communicate have overlapping ranges. This is why organizations often establish a centralized IP address management (IPAM) strategy before building VPCs.

***

## 1.4 The Peering Request-Accept Model

VPC peering follows a **requester-accepter model** — it's not a one-sided action. This design exists for security: you shouldn't be able to connect to someone else's VPC without their explicit consent.

**Step 1: The requester VPC initiates** — From the requester VPC's region, you create a peering connection request, specifying the accepter VPC (by VPC ID). The status becomes **"Pending Acceptance."**

**Step 2: The accepter VPC approves** — In the accepter VPC's region (Oregon in this case), the request appears in the Peering Connections section as "Pending Acceptance." The owner of that VPC reviews the request — the instructor warns: *"In real time, be careful who is the requester. Match the VPC ID. And you can also check the account ID."* — and explicitly accepts it. The status changes to **"Active."**

This two-step handshake ensures that both VPC owners consent to the connection. In cross-account scenarios, this is especially important — you wouldn't want another AWS account connecting to your VPC without your knowledge.

***

## 1.5 Peering Connection ≠ Working Connectivity — The Route Table Requirement

This is the most important conceptual point in the lecture, and the most common source of confusion: **creating a peering connection does NOT automatically enable communication between the VPCs**. The instructor states it directly: *"There is now a connection between these two VPCs. But the instances, if you launch, they don't know how to route the traffic."*

The peering connection establishes the **link** — but route tables determine whether traffic actually **flows** through that link. Without route table entries, instances in VPC-A have no idea that traffic destined for VPC-B's CIDR range should go through the peering connection. That traffic would instead be routed to the NAT Gateway or Internet Gateway (based on existing default routes), which would fail.

You must **manually add routes** to the route tables in **both VPCs**:

* In VPC-A's route table: "Traffic destined for VPC-B's CIDR range → send to peering connection"
* In VPC-B's route table: "Traffic destined for VPC-A's CIDR range → send to peering connection"

The instructor emphasizes: *"This goes both ways."* Peering is bidirectional by nature, but the routing must be configured in both directions for it to work. And critically: *"As many route tables as you have, you need to edit those route tables and make sure you forward the request to that peering connection."*

### Selective Routing — A Powerful Security Tool

You don't have to add the peering route to **every** route table. The instructor highlights this as a deliberate design choice: *"If you don't want the public subnet to be routed to the peering connection, then don't give it. Only private subnet you want, only give it in the private subnet route table."*

This means you can control exactly which subnets can communicate across the peering connection. Your database subnet might need to reach the other VPC, but your public-facing web subnet might not. By selectively adding peering routes only to the route tables that need them, you implement **fine-grained network-level access control**.

***

## 1.6 Security Groups Across Peered VPCs — The IP-Based Limitation

Within a single VPC, security group rules can reference other **security group IDs** as sources — e.g., "allow port 3306 from the web-server security group." This is convenient because it's dynamic: any instance added to that security group automatically gains access.

Across peered VPCs, **you cannot reference security group IDs from the other VPC**. The instructor states this clearly: *"In the security group, you cannot reference the security group ID which is in another VPC, in the peering connection VPC."*

Instead, you must use **IP addresses or CIDR ranges**:

* For a **specific instance** in the other VPC: use its private IP with `/32` (e.g., `172.22.1.5/32`)
* For an **entire subnet** in the other VPC: use the subnet CIDR (e.g., `172.22.2.0/24`)
* For the **entire VPC**: use the VPC CIDR (e.g., `172.22.0.0/16`)

The `/32` notation means "exactly this one IP address." The `/24` means "this 256-address subnet." The `/16` means "this entire VPC range." Choose the scope based on how broad you want the access to be.

> ⚠️ **Expert Note:** The inability to reference cross-VPC security groups means your security rules are **static** with respect to the other VPC's instances. If an instance in the other VPC gets a new private IP (rare but possible), your security group rule pointing to the old IP would break. Using CIDR ranges for subnets or the entire VPC avoids this problem but at the cost of broader access. This is a trade-off to be aware of when designing cross-VPC security.

***

## 1.7 VPC Peering in the Context of the Full VPC Knowledge

The instructor closes with a broader perspective. VPC knowledge — including peering — is positioned as **highly essential for DevOps engineers**: *"Irrespective of what cloud provider you're using or what you're doing in your work, you should know these entire VPC concepts."* The concepts (private/public segmentation, gateway routing, peering) are cloud-universal — Azure, GCP, and other providers have equivalent constructs.

The instructor also acknowledges the learning curve: *"It's not easy to grasp all of it at once. The only way to make sure all this is imprinted in your mind is with practice. You have to repeat it again and again until you can do all this by yourself without any help."*

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a **VPC peering connection** between the existing `vprofile-VPC` in **North California** and a new `vpro-db` VPC in **Oregon**. This simulates a real-world scenario where database infrastructure in one region/VPC needs to communicate with application infrastructure in another. After establishing the peering connection, we configure route tables for traffic flow and discuss security group rules for cross-VPC access. Finally, we clean up all resources.

**Final outcome:** Two VPCs in different regions connected via an active peering connection, with route tables configured to direct inter-VPC traffic through the peering link.

***

## Step 1: Create a New VPC in a Different Region (Oregon)

Switch to the **Oregon** region in the AWS console.

You'll see the **default VPC** already present. Give it a name tag `default` for identification — do not modify or delete it.

Create a new VPC:

| Field          | Value                                | Reasoning                                                                                              |
| -------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| **Name**       | `vpro-db`                            | Identifies this as the database VPC                                                                    |
| **CIDR block** | `172.21.0.0/16` (or `172.22.0.0/16`) | **Must not overlap** with the North California VPC (`172.20.0.0/16`). Any non-overlapping range works. |

Click **Create VPC**.

**What gets created automatically:** A **route table** is created for the new VPC. Name it `vprodb-rt` for identification — you'll need it when adding peering routes later.

**Connection to flow:** This VPC is the "accepter" side of the peering connection.

***

## Step 2: Create the Peering Connection (From North California)

Switch back to the **North California** region. Navigate to **VPC → Peering Connections** → click **Create Peering Connection**.

| Field               | Value                                     | Reasoning                                                                                                     |
| ------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Name**            | `vpro-NC` (or similar)                    | Identifies the peering with a meaningful name                                                                 |
| **Requester VPC**   | Select `vprofile-VPC`                     | The VPC initiating the peering request                                                                        |
| **Account**         | **My account**                            | Both VPCs are in the same AWS account. For cross-account: select "Another account" and provide the account ID |
| **Region**          | **Another region → Oregon**               | The accepter VPC is in a different region                                                                     |
| **Accepter VPC ID** | Paste the VPC ID of `vpro-db` from Oregon | Copy the VPC ID from the Oregon VPC dashboard                                                                 |

Click **Create Peering Connection**.

**Expected status:** `Pending Acceptance` — the request has been sent but not yet approved by the accepter side.

***

## Step 3: Accept the Peering Request (From Oregon)

Switch to the **Oregon** region. Navigate to **VPC → Peering Connections**.

You should see the peering request with status **`Pending Acceptance`**.

**⚠️ Verification before accepting (instructor's warning):** In real environments, verify:

* The **requester VPC ID** matches what you expect
* The **account ID** of the requester is correct
* You recognize and trust the peering request

Select the peering connection → **Actions → Accept Request → Accept Request**.

**Expected status:** Changes to **`Active`** — the peering link is now established.

**What has been achieved:** A network link exists between the two VPCs. But instances still cannot communicate — route table configuration is required next.

***

## Step 4: Add Peering Routes to North California Route Tables

Switch to **North California**. Navigate to **VPC → Route Tables**.

Select the route table you want to enable peering on (the instructor demonstrates with a **private route table**). Click **Routes → Edit Routes → Add Route**.

| Field           | Value                                                  |
| --------------- | ------------------------------------------------------ |
| **Destination** | `172.21.0.0/16` (or whatever CIDR the Oregon VPC uses) |
| **Target**      | Type `peer` → select the peering connection            |

Click **Save Changes**.

**What this does:** Any traffic from instances in this subnet destined for an IP in `172.21.0.0/16` will now be routed through the peering connection to the Oregon VPC, instead of going to the NAT Gateway or Internet Gateway.

**Selective routing decision:** You choose which route tables get this entry. If you only want private subnets to reach the other VPC, add the route only to private subnet route tables. Don't add it to public subnet route tables if public instances shouldn't have cross-VPC access.

**Repeat for all route tables** that need cross-VPC connectivity.

***

## Step 5: Add Peering Routes to Oregon Route Table

Switch to **Oregon**. Navigate to **VPC → Route Tables**. Select `vprodb-rt`.

Click **Routes → Edit Routes → Add Route**.

| Field           | Value                                             |
| --------------- | ------------------------------------------------- |
| **Destination** | `172.20.0.0/16` (the North California VPC's CIDR) |
| **Target**      | Select the peering connection                     |

Click **Save Changes**.

**Critical reminder:** *"This goes both ways."* Both VPCs need routes pointing to the peering connection for the other VPC's CIDR range. If you only add a route in one direction, traffic flows one way but responses can't get back.

***

## Step 6: Configure Security Groups for Cross-VPC Access

Navigate to the relevant **security group** in either VPC. When adding inbound rules for traffic from the peered VPC, you **cannot use security group IDs** from the other VPC.

Instead, use **IP addresses or CIDR ranges**:

| Scenario          | Source Value      | Example         |
| ----------------- | ----------------- | --------------- |
| Specific instance | `<private-ip>/32` | `172.22.1.5/32` |
| Entire subnet     | `<subnet-CIDR>`   | `172.22.2.0/24` |
| Entire VPC        | `<VPC-CIDR>`      | `172.22.0.0/16` |

**Example rule:** Allow SSH (port 22) from a specific instance in the other VPC:

| Type | Port | Source          |
| ---- | ---- | --------------- |
| SSH  | 22   | `172.22.1.5/32` |

**Common mistake:** Trying to reference a security group ID from the other VPC — this will not work. Always use CIDR notation for cross-VPC rules.

***

## Step 7: Cleanup — Delete Resources in Correct Order

Cleanup has a **dependency order**. You cannot delete a VPC that has an active peering connection.

### 7a: Delete the Peering Connection

In **Oregon** → **VPC → Peering Connections** → select the connection → **Actions → Delete Peering Connection**.

Check the option: **"Delete related route table entries"** → Confirm delete.

The peering connection is deleted from **both regions** simultaneously.

### 7b: Delete the Oregon VPC

In **Oregon** → **VPC → Your VPCs** → select `vpro-db` → **Actions → Delete VPC**.

**⚠️ Critical warning:** Do **NOT** delete the default VPC. Ensure you've selected the correct VPC.

### 7c: Delete the North California VPC

In **North California** → first ensure NAT Gateways are deleted and Elastic IPs are released (from previous lectures — these are the chargeable resources). Then **delete the VPC**.

When you delete a VPC, it cascades: **subnets, route tables, and Internet Gateway** are all deleted along with it.

**Deletion order summary:**

```
1. Delete NAT Gateway(s) (if not already done — chargeable)
2. Release Elastic IP(s) (if not already done)
3. Delete Peering Connection (required before VPC deletion)
4. Delete the VPC (cascades: subnets, route tables, IGW)
```

> ⚠️ **Expert Note:** In the cleanup, the instructor notes: *"We have already deleted the resources which are not free."* NAT Gateways and Elastic IPs are the cost-bearing components. VPCs, subnets, route tables, Internet Gateways, and peering connections themselves are free. Always prioritize deleting chargeable resources first to stop cost accumulation.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## VPC Peering — Core Concept

```
PROBLEM:
  VPCs are isolated by default → resources in VPC-A cannot reach VPC-B

SOLUTION:
  VPC Peering = direct private network link between two VPCs

SCOPE:
  Same region ✅ | Cross-region ✅ | Cross-account ✅

CONSTRAINT:
  CIDR ranges MUST NOT overlap
```

***

## Peering Establishment Flow

```
1. REQUESTER VPC (North California)
     → Create Peering Connection
     → Specify: requester VPC, account, region, accepter VPC ID
     → Status: PENDING ACCEPTANCE

2. ACCEPTER VPC (Oregon)
     → View Peering Connections
     → Verify requester VPC ID + account ID
     → Actions → Accept Request
     → Status: ACTIVE

RESULT: Link established — but NOT yet functional (needs routes)
```

***

## Three Layers to Functional Peering

```
LAYER 1: PEERING CONNECTION
  Create + Accept → link exists
  ⚠️ Without Layer 2, traffic can't flow

LAYER 2: ROUTE TABLES (both VPCs)
  VPC-A route table: VPC-B CIDR → peering connection
  VPC-B route table: VPC-A CIDR → peering connection
  ⚠️ MUST be configured in BOTH directions
  ⚠️ Add to EACH route table that needs access (selective)

LAYER 3: SECURITY GROUPS
  Cannot reference cross-VPC security group IDs
  Must use CIDR notation:
    /32  → specific instance IP
    /24  → specific subnet
    /16  → entire VPC
```

***

## Route Table Entry for Peering

```
VPC-A route table (North California, 172.20.0.0/16):
  Destination: 172.21.0.0/16   →   Target: pcx-xxxxx (peering connection)

VPC-B route table (Oregon, 172.21.0.0/16):
  Destination: 172.20.0.0/16   →   Target: pcx-xxxxx (peering connection)

BOTH directions required. Per-route-table decision = selective access control.
```

***

## Selective Routing — Security Through Route Tables

```
Want private subnets to reach peered VPC?
  → Add peering route to PRIVATE route tables only

Don't want public subnets to reach peered VPC?
  → DON'T add peering route to PUBLIC route tables

RESULT: Network-level access control per subnet
```

***

## Cross-VPC Security Group Rules

```
WITHIN same VPC:
  Source: sg-xxxxxxx (security group ID)    ✅ works

ACROSS peered VPCs:
  Source: sg-xxxxxxx                         ❌ does NOT work

MUST USE CIDR:
  Specific instance:  172.22.1.5/32
  Specific subnet:    172.22.2.0/24
  Entire VPC:         172.22.0.0/16
```

***

## CIDR Non-Overlap Rule

```
VPC-A: 172.20.0.0/16
VPC-B: 172.21.0.0/16  ✅ (no overlap)
VPC-B: 172.20.0.0/16  ❌ (overlaps with VPC-A → peering impossible)

RULE: Plan IP address space BEFORE creating VPCs
```

***

## Cleanup Dependency Chain

```
1. Delete NAT Gateways     (💰 stop cost)
2. Release Elastic IPs     (💰 stop cost)
3. Delete Peering Connection (required before VPC delete)
     → also deletes related route table entries (if checked)
4. Delete VPC              (cascades: subnets, route tables, IGW)

⚠️ Cannot delete VPC with active peering
⚠️ NEVER delete the default VPC
```

***

## Full VPC Knowledge Map (Cumulative — This + Previous Lectures)

```
VPC
├── Public Subnets (×2, multi-zone)
│     ├── Route Table → IGW (internet bidirectional)
│     ├── NAT Gateways (for private subnet outbound)
│     ├── Bastion Host (SSH jump to private)
│     └── Web Servers, Load Balancers
│
├── Private Subnets (×2, multi-zone)
│     ├── Route Table → NAT GW (outbound-only internet)
│     ├── DB Servers, App Backends
│     └── Access: Bastion Host or VPN
│
├── Internet Gateway (×1, managed HA, FREE)
├── NAT Gateways (×2 for HA, 💰 PAID)
├── Route Tables (traffic decision engine, FREE)
│
└── VPC PEERING (this lecture)
      ├── Links to other VPCs (same/cross region/account)
      ├── CIDR must not overlap
      ├── Requester → Accepter handshake
      ├── Route tables BOTH sides required
      ├── Selective routing per route table
      └── Security groups: CIDR only (no cross-VPC SG IDs)
```

***

## Reusable Engineering Pattern: Establish Link → Configure Routing → Authorize Access

```
PATTERN (observed in VPC peering):

  STEP 1: ESTABLISH THE LINK
    Create the connectivity mechanism between two systems
    (Peering connection, VPN tunnel, Direct Connect, etc.)
    Link exists but traffic can't flow yet

  STEP 2: CONFIGURE ROUTING
    Tell each system HOW to reach the other
    (Route table entries pointing to the link)
    Both directions required
    Selective per-subnet control possible

  STEP 3: AUTHORIZE ACCESS
    Define WHO can communicate WHAT
    (Security group rules with CIDR ranges)
    Most restrictive layer — final gatekeeper

THREE LAYERS: Link → Routing → Authorization
MISS ANY LAYER: connectivity fails

WHERE ELSE:
  • VPN connections (tunnel + routes + firewall rules)
  • Transit Gateway attachments (attach + routes + SG)
  • Direct Connect (physical link + virtual interface + routes + SG)
  • On-premise networking (cable + routing protocol + ACLs)
  • Any network connectivity: physical/logical link, then routing, then access control
```

***

## Failure Signature Index

```
Peering active but instances can't communicate     → route table entries missing (one or both sides)
Route exists but traffic blocked                    → security group rule missing or wrong CIDR
Peering creation fails                              → CIDR ranges overlap between VPCs
Can't reference SG from other VPC                   → expected behavior; use CIDR notation instead
VPC deletion fails                                  → active peering connection exists; delete peering first
Traffic works one direction only                    → route table entry missing on the return side
```

***

## One-Line Mental Reload Trigger

> *"VPC peering: request-accept handshake (CIDRs must not overlap), then add routes in BOTH VPCs' route tables pointing to peering connection (selective per route table), then security groups use CIDR not SG-IDs — three layers: link, routing, authorization."*

This single sentence reconstructs the full peering workflow, the CIDR constraint, the bidirectional route requirement, the selective routing capability, the security group limitation, and the three-layer connectivity model. [\[274-peering \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/274-peering.txt)
