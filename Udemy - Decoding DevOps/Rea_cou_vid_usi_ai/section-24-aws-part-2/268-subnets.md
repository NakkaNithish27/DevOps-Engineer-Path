# 🎓 Deep Learning Material: AWS VPC Subnets — Creation & Architectural Reality

**Source:** [268-subnets.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt?EntityRepresentationId=bfa22bf2-1414-49cd-8b2e-87a9abacb189) — Video lecture covering the creation of four subnets (two public, two private) inside a custom VPC, the naming convention, availability zone distribution, CIDR block assignment, and the critical conceptual clarification that "public" subnets are not actually public until a route table with an internet gateway is attached. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What a Subnet Is and Why It Exists Inside a VPC

A VPC (Virtual Private Cloud) defines a large private IP address space — in this project, `172.20.0.0/16`, which gives you 65,536 possible IP addresses. But you do not place resources directly into a VPC. You subdivide the VPC into **subnets**, and resources (EC2 instances, RDS databases, etc.) are placed inside subnets. A subnet is a **partition** of the VPC's IP range. Each subnet gets its own smaller CIDR block carved from the VPC's larger block. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

Subnets exist for two primary reasons: **availability zone placement** and **network access control**. Each subnet resides in exactly one availability zone (AZ). By creating subnets in different AZs, you distribute resources across physically separate data centers, enabling resilience. By creating subnets with different routing and access rules, you control which resources can reach the internet and which cannot — this is the public vs. private subnet distinction. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## 1.2 The Four-Subnet Architecture

The design calls for four subnets inside the VPC:

| Subnet Name      | Type    | Availability Zone | CIDR Block      |
| ---------------- | ------- | ----------------- | --------------- |
| `vpro-pubsub-1`  | Public  | us-east-1a        | `172.20.1.0/24` |
| `vpro-pubsub-2`  | Public  | us-east-1b        | `172.20.2.0/24` |
| `vpro-privsub-1` | Private | us-east-1a        | `172.20.3.0/24` |
| `vpro-privsub-2` | Private | us-east-1b        | `172.20.4.0/24` |

 [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

Each `/24` subnet provides 256 IP addresses (AWS reserves 5, so 251 usable). The third octet distinguishes each subnet: `.1.0`, `.2.0`, `.3.0`, `.4.0`. All four fit cleanly inside the VPC's `/16` range of `172.20.0.0/16`.

The public subnets are distributed across two different AZs (1a and 1b), and the private subnets mirror this distribution. This creates **AZ-redundant pairs** — if one AZ goes down, the other AZ has both a public and a private subnet still operational. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## 1.3 The Critical Misconception: "Public" Subnets Are Not Actually Public

This is the most important conceptual point in the lecture, and the instructor states it directly: **"There is nothing public about public subnet."** At the moment of creation, all four subnets are functionally identical. They all have private IP ranges. None of them can reach the internet. If you launch an instance in any of these subnets right now — including the ones named "public" — that instance will have no public IP, cannot access the internet, and cannot be accessed from outside the VPC. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

The word "public" in the subnet name is purely a **label reflecting intent**, not a technical reality. A subnet becomes truly public only when two things happen (covered in the next lecture): (1) a **route table** with a route to an **internet gateway** is attached to it, and (2) instances in that subnet are configured to receive public IPs. Until those steps are completed, the "public" subnets are just as isolated as the "private" ones. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

This is a common misunderstanding. People assume that naming a subnet "public" or selecting some option during creation makes it public. It does not. The subnet's network behavior is entirely determined by its **route table associations** and **gateway attachments**, which are separate resources configured independently. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

🔍 **Deep Dive**
The instructor says: "Functionally, these subnets are useless for now." This is deliberately stated to make clear that subnet creation alone accomplishes nothing operational. The subnet is just an IP address partition within a VPC. It becomes useful only when connected to routing infrastructure (route tables, gateways) that defines how traffic flows in and out. The next lecture creates the route table and internet gateway that will differentiate the public subnets from the private ones. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## 1.4 CIDR Block Planning — Pre-Documented Design

The instructor emphasizes that all subnet details were **documented before creation**: "We have already documented everything, so we are going to just do simple copy paste." The CIDR blocks, names, and AZ assignments were decided in a planning phase. At creation time, it's purely execution — filling in pre-determined values. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

This reflects a fundamental infrastructure engineering principle: network architecture is designed first, then implemented. You don't improvise CIDR ranges during creation. Overlapping ranges, inconsistent AZ distribution, or poorly planned address spaces cause problems that are difficult to fix later. The instructor advises: "Later, you can add, remove subnets, but for now, stick to the plan." [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## 1.5 VPC Selection — A Common Mistake

The instructor warns: "Be careful. Select our VPC, do not select default VPC. Make sure you see the range correct over there." Every AWS account has a **default VPC** that was created automatically. When creating subnets, the VPC selection dropdown may default to the default VPC or show multiple VPCs. Selecting the wrong VPC means your subnets end up in the wrong network — they'll have the wrong IP range and won't be connected to the resources you intend. Verifying the CIDR range displayed after selection confirms you've chosen the correct VPC. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating four subnets inside a custom VPC — two intended as public subnets and two as private subnets, distributed across two availability zones. The final outcome after this lecture: four subnet objects exist in the VPC, correctly named and addressed, ready for route table and gateway attachment in the next lecture. They are not yet functional — no internet access, no public IPs — that comes next. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## Step 1: Navigate to Subnet Creation

In the AWS VPC console, click **Subnets** in the left sidebar. Click **Create subnet**. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## Step 2: Select the Correct VPC

At the top of the creation form, select the **VPC** these subnets will belong to.

⚠️ **Do NOT select the default VPC.** Select your custom VPC (the one created in the previous lecture). Verify by checking the CIDR range displayed — it should show `172.20.0.0/16` (or whatever range you configured). If the range doesn't match, you've selected the wrong VPC. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## Step 3: Create All Four Subnets Simultaneously

AWS allows creating multiple subnets in a single operation. Click **"Add new subnet"** three additional times to get four subnet input blocks. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

Fill in each block with the pre-documented values:

### Subnet 1 — Public Subnet 1

| Field             | Value           |
| ----------------- | --------------- |
| Subnet name       | `vpro-pubsub-1` |
| Availability Zone | `us-east-1a`    |
| IPv4 CIDR block   | `172.20.1.0/24` |

 [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

### Subnet 2 — Public Subnet 2

| Field             | Value           |
| ----------------- | --------------- |
| Subnet name       | `vpro-pubsub-2` |
| Availability Zone | `us-east-1b`    |
| IPv4 CIDR block   | `172.20.2.0/24` |

 [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

### Subnet 3 — Private Subnet 1

| Field             | Value            |
| ----------------- | ---------------- |
| Subnet name       | `vpro-privsub-1` |
| Availability Zone | `us-east-1a`     |
| IPv4 CIDR block   | `172.20.3.0/24`  |

 [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

### Subnet 4 — Private Subnet 2

| Field             | Value            |
| ----------------- | ---------------- |
| Subnet name       | `vpro-privsub-2` |
| Availability Zone | `us-east-1b`     |
| IPv4 CIDR block   | `172.20.4.0/24`  |

 [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

**Verification before clicking Create:**

* Each public subnet pair spans **two different AZs** (1a and 1b).
* Each private subnet pair spans **two different AZs** (1a and 1b).
* All four CIDR blocks are **non-overlapping** and within the VPC's `/16` range.
* Names follow a consistent, identifiable convention (`pubsub` vs `privsub`, numbered).

 [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## Step 4: Create the Subnets

Click **Create subnet**. All four subnets are created simultaneously. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

## Step 5: Verify

After creation, check the subnet list:

* All four subnets appear under the correct VPC.
* CIDR blocks are correct (`.1.0`, `.2.0`, `.3.0`, `.4.0` — each `/24`).
* AZ assignments are correct (1a/1b distribution).
* Names are correct. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

**Current state:** All four subnets exist but are **functionally identical** — all are private, all are isolated, none have internet access. The "public" and "private" distinction does not exist yet. It will be created in the next lecture by attaching route tables and an internet gateway. [\[268-subnets \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/268-subnets.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## VPC Subnet Architecture

```
VPC: 172.20.0.0/16
  │
  ├── vpro-pubsub-1    172.20.1.0/24    AZ: us-east-1a    (public — intent only)
  ├── vpro-pubsub-2    172.20.2.0/24    AZ: us-east-1b    (public — intent only)
  ├── vpro-privsub-1   172.20.3.0/24    AZ: us-east-1a    (private)
  └── vpro-privsub-2   172.20.4.0/24    AZ: us-east-1b    (private)
```

***

## AZ Distribution Pattern

```
        AZ 1a              AZ 1b
  ┌──────────────┐   ┌──────────────┐
  │ pubsub-1     │   │ pubsub-2     │
  │ 172.20.1.0   │   │ 172.20.2.0   │
  ├──────────────┤   ├──────────────┤
  │ privsub-1    │   │ privsub-2    │
  │ 172.20.3.0   │   │ 172.20.4.0   │
  └──────────────┘   └──────────────┘

Each AZ has one public + one private subnet → AZ-redundant pairs
```

***

## CIDR Block Pattern

```
VPC:     172.20.0.0/16    (65,536 IPs)
Subnets: 172.20.X.0/24   (256 IPs each, 251 usable)

X = 1 → pubsub-1
X = 2 → pubsub-2
X = 3 → privsub-1
X = 4 → privsub-2

Third octet = subnet identifier
```

***

## The "Public" Misconception (Critical)

```
AT CREATION:
  "public" subnet = "private" subnet = IDENTICAL
  No internet access. No public IPs. Fully isolated.

BECOMES TRULY PUBLIC only after (next lecture):
  1. Route table with route to Internet Gateway → attached to subnet
  2. Instances configured for public IP auto-assign

Name = INTENT, not REALITY
Reality = Route table + Gateway
```

***

## Operational Checklist

```
1. Navigate: VPC console → Subnets → Create subnet
2. Select VPC: ⚠️ custom VPC, NOT default (verify CIDR range)
3. Add 4 subnets (use "Add new subnet" button)
4. Fill: name, AZ, CIDR for each (from pre-documented plan)
5. Verify: names, AZs (1a/1b pairs), CIDRs (non-overlapping, within /16)
6. Create
7. Confirm: all 4 visible under correct VPC
```

***

## Common Mistakes

```
Wrong VPC selected         → subnets in default VPC, wrong IP range
Overlapping CIDR blocks    → creation fails or routing conflicts
Same AZ for both pub subs  → no AZ redundancy
Expecting internet access  → subnets are isolated until route table + IGW
```

***

## Dependency Chain

```
BEFORE: VPC created (172.20.0.0/16)
THIS:   4 subnets created (address partitions, AZ-distributed)
NEXT:   Route table + Internet Gateway → makes "public" subnets truly public
         ↓
        Instances can then be launched with internet access
```

***

## Key Engineering Patterns

| Pattern                      | Manifestation                                                                    |
| ---------------------------- | -------------------------------------------------------------------------------- |
| **Plan-then-execute**        | All CIDR blocks, names, AZs documented before creation — "simple copy paste"     |
| **AZ-redundant pairs**       | Each subnet type (pub/priv) spans 2 AZs for resilience                           |
| **Name ≠ Behavior**          | "Public" is a label, not a configuration — behavior comes from routing           |
| **Layered activation**       | Subnet alone = inert; subnet + route table + gateway = functional                |
| **Progressive construction** | VPC → Subnets → Route tables → Gateways → Instances (each layer adds capability) |

***

This completes the full reconstruction. **Theory** explains the subnet concept, the four-subnet design rationale, and critically debunks the "public subnet is public" misconception. **Practical** gives you every field to fill and every verification to perform. The **Compression Map** lets you reload the entire architecture — CIDR layout, AZ distribution, and the dependency chain — in under 30 seconds. Let me know if you'd like Anki flashcards or any section expanded! 🚀
