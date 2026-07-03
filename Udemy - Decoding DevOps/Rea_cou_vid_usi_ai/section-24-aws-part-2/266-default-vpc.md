# 🎓 Deep Learning Material: AWS Default VPC — Structure, Components & Routing Logic

**Source:** [266-default-vpc.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt?EntityRepresentationId=324886c1-40de-45a6-956b-485d514a54b4) — Video lecture covering the AWS default VPC in the North California (us-west-1) region, examining its structure: VPC with /16 CIDR, two public subnets across availability zones, route table entries, internet gateway attachment, and the routing logic that defines public vs private subnets. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why North California (us-west-1) for Learning

The instructor deliberately chooses the **North California region (US-West-1)** for this VPC section. The reason is purely practical: this region has only **two availability zones**. Regions like US-East-1 (North Virginia) have six or more zones, which means more subnets, more route tables, and more complexity to navigate while learning. With only two zones, the default VPC has just two subnets — the simplest possible setup to study. The instructor emphasizes that everything learned here applies to any region; only the number of zones and subnets differs. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.2 What the Default VPC Is

Every AWS region comes with a **default VPC** — a pre-created Virtual Private Cloud that exists automatically in your account. You do not create it. AWS creates it for you. It is the network that all your EC2 instances, RDS databases, and other resources land in when you don't specify a custom VPC. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

A critical property: **you cannot create a default VPC yourself**. You can create custom VPCs, but you cannot designate any of them as "default." If you accidentally delete the default VPC, you must **contact AWS support** to have it recreated. The instructor repeats this warning at both the beginning and end of the lecture: "never delete the default VPC." This also applies to the default internet gateway and default route tables — do not delete them. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

To identify the default VPC in the console, navigate to **VPC → Your VPCs**. You will see a VPC without a name, and if you scroll horizontally, a column labeled "Default VPC" shows "Yes." The instructor renames it to "DEFAULT VPC" in all caps for easy visual identification — a recommended practice for every region you work in. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.3 The VPC CIDR Block — 172.31.0.0/16

The default VPC has the CIDR range **172.31.0.0/16**. The `/16` subnet mask means the first 16 bits of the IP address are fixed (172.31), and the remaining 16 bits can vary. This gives approximately **65,536 IP addresses** (2^16). This is the same range in every region's default VPC — 172.31.0.0/16. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

This range defines the **private IP address space** of the VPC. Every resource inside this VPC (EC2 instances, RDS databases, Lambda functions connected to the VPC) receives a private IP address from within this range. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.4 Subnets — Subdivisions of the VPC

Inside the default VPC, AWS creates **one subnet per availability zone**. Since us-west-1 has two availability zones (us-west-1a and us-west-1b), there are **two subnets**. Each subnet is placed in a different zone. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

Each subnet has its own CIDR block — a **subset** of the VPC's range. Both subnets use `/20`, which provides approximately **4,096 IP addresses** each (2^12). However, AWS **reserves 5 IP addresses per subnet** for internal use (network address, VPC router, DNS server, future use, and broadcast address), so the actual usable count is slightly less. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

The subnets have different IP ranges within the 172.31.x.x space. The instructor points out that the ranges start at different points — one might be `172.31.0.0/20` and the other `172.31.16.0/20`. This means you can **identify which subnet an instance belongs to by looking at its private IP address**. If an instance has the IP `172.31.16.x`, it belongs to the subnet whose range starts at 172.31.16.0. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

Each subnet is also identifiable by its **subnet ID** and its **VPC ID** (which links it to its parent VPC). The instructor renames them to `Default-pubsub1` and `Default-pubsub2` for clarity. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.5 The Route Table — How Traffic Finds Its Way

Every subnet is associated with a **route table**. The route table contains **routing rules** (called routes) that determine where outgoing network traffic is sent. You can examine a subnet's route table by selecting the subnet and clicking on the "Route table" tab. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

The default route table in the default VPC has **two entries**: [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**Route 1 — Local traffic:** Destination `172.31.0.0/16` → Target `local`. This means: if a network packet's destination IP falls within the VPC's own CIDR range (172.31.x.x), route it **locally** — within the VPC. This is how instances in different subnets within the same VPC communicate with each other without going through any gateway. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**Route 2 — Internet traffic:** Destination `0.0.0.0/0` → Target `igw-xxxxxxx` (Internet Gateway ID). In networking, `0.0.0.0/0` means **all IP addresses** — it is the default route, the catch-all. Any packet whose destination does NOT match the local VPC range gets routed to the **internet gateway**. This is what makes the subnets **public**. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

The route table evaluation works by **most-specific match first**. A packet destined for `172.31.16.5` matches the more specific `172.31.0.0/16` rule and stays local. A packet destined for `8.8.8.8` (Google DNS, an external IP) doesn't match the VPC range, so it falls through to the `0.0.0.0/0` catch-all and goes to the internet gateway. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.6 The Internet Gateway — The Bridge to the Public Internet

The **Internet Gateway (IGW)** is the component that connects the VPC to the public internet. It is a managed AWS resource — you don't install or configure software on it. You can find it in the VPC console under "Internet Gateways." The default VPC comes with a default internet gateway already attached. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

The internet gateway shows which VPC it is attached to. You can also see its route table associations — confirming that the same route table with the `0.0.0.0/0 → igw` entry is associated with both public subnets. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.7 Public vs Private Subnets — The Definitive Rule

This is the most important conceptual takeaway of the lecture, and the instructor explicitly asks you to "rewind it and listen again" and notes it is an interview question.

**A subnet is public if its route table routes outgoing traffic (`0.0.0.0/0`) to an Internet Gateway.** [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**A subnet is private if its route table routes outgoing traffic (`0.0.0.0/0`) to a NAT Gateway.** [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

There is no "public" or "private" checkbox on a subnet. The subnet's nature is **entirely determined by its route table entries**. If the default route points to an IGW, instances in that subnet can send and receive traffic directly from the internet (assuming they have public IPs and their security groups allow it). If the default route points to a NAT gateway, instances can initiate outbound connections to the internet (through the NAT), but cannot be reached directly from the internet — making them private. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

Both subnets in the default VPC route to the internet gateway, which is why both are **public subnets**. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

🔍 **Deep Dive**
The route table is the single source of truth for subnet classification. A common misconception is that "public" and "private" are inherent properties of a subnet. They are not — they are emergent properties of the routing configuration. You can change a public subnet to private by modifying its route table to point to a NAT gateway instead of an internet gateway. The subnet itself doesn't change; only its route table association does. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.8 Other VPC Components — Scope and Boundaries

The VPC console shows many other components: NAT Gateways, Elastic IPs, Network ACLs, Egress-only Internet Gateways, DHCP Option Sets, Endpoints, Endpoint Services. The instructor explicitly scopes the course: **NAT Gateways, Elastic IPs, and Network ACLs** will be covered in upcoming lectures. The rest (Egress-only IGW, DHCP Option Sets, Endpoints, Endpoint Services) are "out of the scope of our course" and require deeper networking expertise. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

The instructor notes: "you really need to be a network geek to understand the advanced concepts of VPC." The course covers the essential operational concepts that a DevOps engineer needs. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## 1.9 What Comes Next

By the end of the VPC lecture series, you should be able to **create your own VPC**, add subnets, create internet gateways and route tables, and attach them. But the default VPC and its components should never be deleted — they serve as a safety net and as the default landing zone for resources when no custom VPC is specified. The next lecture covers creating a custom VPC and adding subnets. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing

We are examining the **default VPC** in the AWS console to understand its pre-built components: the VPC itself, its subnets, the route table, and the internet gateway. The goal is not to build anything — it is to navigate, identify, and understand what AWS has already created for us, and to learn how to determine whether a subnet is public or private by reading route table entries. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## Step 1: Switch to the North California Region

In the AWS Management Console, click the **region selector** (top-right) and switch to **US West 1 (N. California)**. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

This region has only two availability zones, making the default VPC structure simple to study. All concepts transfer to any other region.

***

## Step 2: Open the VPC Service

Search for **VPC** in the AWS service search bar and open it. You will land on the **VPC Dashboard**, which shows a summary of all VPC components in this region. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

Take a moment to browse the left sidebar — note the sections: Your VPCs, Subnets, Route Tables, Internet Gateways, NAT Gateways, Elastic IPs, Network ACLs, and more. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## Step 3: Identify the Default VPC

Click **Your VPCs** in the left sidebar. You will see one VPC listed. It has no name by default. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**3a. Confirm it is the default:**

Scroll horizontally in the table. Find the "Default VPC" column — it should say **Yes**. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**3b. Rename it for easy identification:**

Click the name field (or the pencil icon) and rename it to **DEFAULT VPC** (all caps). This makes it visually distinct in any region. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**3c. Note the CIDR block:**

The IPv4 CIDR column shows **172.31.0.0/16**. This provides \~65,000 IP addresses. This range is the same in every region's default VPC. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## Step 4: Examine the Subnets

Click **Subnets** in the left sidebar. You should see **two subnets** (one per availability zone in us-west-1). [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**4a. Verify they belong to the default VPC:**

Check the **VPC ID** column for each subnet. It should match the VPC ID of the default VPC you just examined. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**4b. Rename them:**

Rename them to `Default-pubsub1` and `Default-pubsub2` for clarity. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**4c. Note the key details:**

| Property      | Subnet 1                        | Subnet 2                      |
| ------------- | ------------------------------- | ----------------------------- |
| CIDR          | `172.31.0.0/20` (or similar)    | `172.31.16.0/20` (or similar) |
| AZ            | us-west-1a                      | us-west-1b                    |
| IPs available | \~4,091 (4096 minus 5 reserved) | \~4,091                       |

 [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**4d. Understand IP-to-subnet identification:**

An instance with private IP `172.31.16.x` belongs to the subnet whose range starts at 172.31.16.0. You can identify which subnet an instance is in by looking at its private IP address. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## Step 5: Examine the Route Table and Determine Public/Private

**5a. Find the route table:**

Click **Route Tables** in the left sidebar. You should see **one route table** for the default VPC. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

Alternatively: select any subnet from the Subnets page, then click the **Route table** tab at the bottom. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**5b. Read the routes:**

| Destination     | Target        | Meaning                                        |
| --------------- | ------------- | ---------------------------------------------- |
| `172.31.0.0/16` | `local`       | Traffic within the VPC stays local             |
| `0.0.0.0/0`     | `igw-xxxxxxx` | All other traffic goes to the Internet Gateway |

 [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**5c. Determine subnet type:**

The `0.0.0.0/0` route points to an **Internet Gateway** (`igw-`). Therefore, both subnets associated with this route table are **public subnets**. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**The definitive rule:**

* Route `0.0.0.0/0` → Internet Gateway = **Public subnet**
* Route `0.0.0.0/0` → NAT Gateway = **Private subnet**

 [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**5d. Check subnet associations:**

Click the **Subnet associations** tab on the route table. It should show both subnets (`Default-pubsub1` and `Default-pubsub2`) associated with this route table. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## Step 6: Examine the Internet Gateway

Click **Internet Gateways** in the left sidebar. You should see **one internet gateway**. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**6a. Verify the VPC attachment:**

The "VPC ID" column (or "Attached VPC" field) shows which VPC this IGW is connected to. It should match the default VPC's ID. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**6b. Verify the route table reference:**

The IGW's ID (e.g., `igw-xxxxxxx`) is the same ID that appears in the route table's `0.0.0.0/0` target. This confirms the connection chain: subnet → route table → internet gateway → internet. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

***

## Step 7: Understand What NOT to Do

⚠️ **Do NOT delete:**

* The default VPC
* The default internet gateway
* The default route tables

If you accidentally delete the default VPC, you must contact **AWS support** to recreate it. You cannot create a default VPC yourself — only custom VPCs. [\[266-default-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/266-default-vpc.txt)

**Connection to larger flow:** The next lecture covers creating a **custom VPC** with your own subnets, route tables, and internet gateways. Understanding the default VPC's structure is the prerequisite — you will replicate this pattern manually.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Default VPC Architecture

```
REGION: us-west-1 (N. California) — 2 AZs

┌─────────────────────────────────────────────────────────┐
│  DEFAULT VPC: 172.31.0.0/16  (~65,000 IPs)             │
│                                                         │
│  ┌──────────────────┐     ┌──────────────────┐          │
│  │ Default-pubsub1  │     │ Default-pubsub2  │          │
│  │ 172.31.0.0/20    │     │ 172.31.16.0/20   │          │
│  │ AZ: us-west-1a   │     │ AZ: us-west-1b   │          │
│  │ ~4,091 usable IPs│     │ ~4,091 usable IPs│          │
│  └────────┬─────────┘     └────────┬─────────┘          │
│           │                        │                     │
│           └──────────┬─────────────┘                     │
│                      │                                   │
│              ┌───────▼───────┐                           │
│              │  Route Table  │                           │
│              │───────────────│                           │
│              │ 172.31.0.0/16 │ → local                   │
│              │ 0.0.0.0/0     │ → igw-xxxxx               │
│              └───────┬───────┘                           │
│                      │                                   │
└──────────────────────┼───────────────────────────────────┘
                       │
               ┌───────▼───────┐
               │ Internet GW   │
               │ (igw-xxxxx)   │
               └───────┬───────┘
                       │
                   INTERNET
```

***

## The Definitive Rule (Public vs Private)

```
Route 0.0.0.0/0 → Internet Gateway (igw-)   = PUBLIC subnet
Route 0.0.0.0/0 → NAT Gateway (nat-)        = PRIVATE subnet

There is NO "public/private" property on the subnet itself.
The route table ENTRY determines the nature.
```

***

## Route Table Logic

```
Packet destination IP evaluation (most-specific match first):

172.31.x.x  → matches 172.31.0.0/16  → route: LOCAL (within VPC)
anything else → matches 0.0.0.0/0    → route: Internet Gateway

0.0.0.0/0 = ALL IP addresses = default/catch-all route
```

***

## CIDR Quick Reference

```
/16 → ~65,536 IPs  (VPC level)
/20 → ~4,096 IPs   (subnet level, minus 5 reserved by AWS)

AWS reserves 5 IPs per subnet:
  .0  = network address
  .1  = VPC router
  .2  = DNS server
  .3  = future use
  .255 = broadcast
```

***

## IP-to-Subnet Identification

```
Instance IP: 172.31.16.42
Subnet CIDR: 172.31.16.0/20  ← belongs here (third octet matches)

Instance IP: 172.31.0.15
Subnet CIDR: 172.31.0.0/20   ← belongs here
```

***

## Component Relationship Chain

```
VPC (172.31.0.0/16)
  ├── Subnet 1 (/20, AZ-a) ──┐
  ├── Subnet 2 (/20, AZ-b) ──┤
  │                           │
  │               Route Table ◄┘  (associated to both subnets)
  │                    │
  │              0.0.0.0/0 → IGW
  │                    │
  └── Internet Gateway ◄┘  (attached to VPC)
            │
        INTERNET
```

***

## Default VPC Properties

```
Property              │ Value
──────────────────────┼──────────────────────
CIDR                  │ 172.31.0.0/16 (same in every region)
Subnets               │ 1 per AZ (all public by default)
Route table           │ local + 0.0.0.0/0 → IGW
Internet Gateway      │ pre-attached
Can be recreated?     │ NO — contact AWS support
Can create custom?    │ YES — but cannot make it "default"
```

***

## Region Choice Reasoning

```
us-west-1 (N. California):  2 AZs → 2 subnets → simplest to learn
us-east-1 (N. Virginia):    6 AZs → 6 subnets → more complex

All VPC concepts are region-agnostic. Only AZ count varies.
```

***

## ⚠️ Critical Warnings

```
NEVER DELETE:
  ✗ Default VPC
  ✗ Default Internet Gateway
  ✗ Default Route Tables

If deleted: contact AWS Support (cannot self-create default VPC)
```

***

## VPC Console Navigation

```
VPC Dashboard (left sidebar):
  Your VPCs         → see/rename default VPC
  Subnets            → see subnets, AZs, CIDRs
  Route Tables       → see routes (local + 0.0.0.0/0)
  Internet Gateways  → see IGW attachment to VPC

IN SCOPE (this course):     NAT Gateways, Elastic IPs, Network ACLs
OUT OF SCOPE:               Egress-only IGW, DHCP Option Sets, Endpoints, Endpoint Services
```

***

## Course Components Covered (Upcoming)

```
THIS:   Default VPC examination (read-only)
NEXT:   Create custom VPC + add subnets
LATER:  NAT Gateways, Elastic IPs, Network ACLs
GOAL:   Create IGW + route table + attach to VPC independently
```

***

## Key Engineering Patterns

| Pattern                                     | Manifestation                                                                                    |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Pre-built defaults as learning scaffold** | Default VPC exists as a reference implementation — study before building custom                  |
| **Classification by behavior, not label**   | Public/private is determined by route table target, not by any subnet property                   |
| **Hierarchical CIDR subdivision**           | VPC /16 → subnets /20 — parent range split into child ranges per AZ                              |
| **Catch-all routing**                       | `0.0.0.0/0` is the universal default route — anything not matched by specific rules falls here   |
| **AZ-per-subnet mapping**                   | One subnet per AZ provides fault isolation — resources in different AZs survive zone failures    |
| **IP-as-location-identifier**               | Private IP third octet reveals subnet membership — operationally useful for quick identification |
| **Non-recreatable infrastructure**          | Default VPC is unique — treat it as irreplaceable, unlike custom resources which can be rebuilt  |

***

This completes the full reconstruction. **Theory** explains every VPC component and the routing logic that defines public vs private subnets. **Practical** walks through every console navigation step to examine and identify each component. The **Compression Map** gives you the architecture diagram, the definitive public/private rule, and the CIDR reference for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
