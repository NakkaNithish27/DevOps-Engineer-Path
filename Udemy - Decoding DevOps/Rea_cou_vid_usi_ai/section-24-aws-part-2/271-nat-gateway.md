# AWS VPC — NAT Gateway, Private Route Table, and DNS Hostnames

**Source:** Video caption file — *"NAT Gateway"* (from an AWS VPC / DevOps course) [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Private Subnets Need Internet Access Without Being Exposed

In the previous lectures, the VPC was built with two public subnets and two private subnets. Public subnets have a route table that sends internet-bound traffic to the Internet Gateway (IGW), giving instances direct internet access and making them reachable from the internet. Private subnets, by design, should **not** be reachable from the internet — that's the entire point of making them private. But instances in private subnets still need to **reach out** to the internet — to download software updates, pull packages, access external APIs, etc. They need **outbound** internet access without having **inbound** internet exposure. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

This is exactly the problem a **NAT Gateway** solves.

***

## 1.2 — What Is a NAT Gateway?

A NAT Gateway (Network Address Translation Gateway) allows instances in **private subnets** to initiate outbound connections to the internet while preventing the internet from initiating inbound connections to those instances. It performs address translation — when a private instance sends a request to the internet, the NAT Gateway replaces the instance's private IP with its own public IP, forwards the request, receives the response, and routes it back to the private instance. The internet only ever sees the NAT Gateway's public IP, never the private instance's IP. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

The key architectural rule, stated twice in the video for emphasis: **"NAT Gateway lives in the public subnet and it connects to the internet through the Internet Gateway."** This is the most important placement concept. The NAT Gateway itself needs internet access to perform its job — it gets that access by being placed in a public subnet (which has a route to the IGW). The private subnets then route their internet-bound traffic to the NAT Gateway instead of directly to the IGW. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

The relationship chain: **Private instance → NAT Gateway (in public subnet) → Internet Gateway → Internet**. The private instance never touches the IGW directly. The NAT Gateway acts as an intermediary that provides outbound-only internet access. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

🔍 **Deep Dive:**
The NAT Gateway "serves the private subnet but needs to stay in the public subnet" — this creates a cross-subnet dependency that is architecturally important. The NAT Gateway has one foot in the public world (it has a public IP and lives in a public subnet) and one foot in the private world (private subnets route through it). This is the classic **proxy/gateway pattern**: a component that sits at a boundary between two network zones and mediates traffic between them. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## 1.3 — Elastic IP: Why the NAT Gateway Needs a Static Public IP

To connect to the internet, you need a public IP address. Public IPs can be **dynamic** (assigned by AWS, may change when the resource restarts) or **static** (permanently assigned, doesn't change). The video explains: "This entire VPC network is controlled by us and we are not allocating dynamic IPs. We are allocating an Elastic IP, which is a static public IP." [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

An **Elastic IP (EIP)** is AWS's mechanism for static public IPs. You allocate an EIP, and it remains yours until you explicitly release it. The NAT Gateway requires an Elastic IP because the NAT Gateway is a persistent network component — if its public IP changed, all outbound connections from private instances would be disrupted, and any external services that whitelist your outbound IP would break. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

The Elastic IP is created **before** the NAT Gateway and then **associated** with it during NAT Gateway creation. The EIP is a separate resource with its own lifecycle — you create it independently, attach it to the NAT Gateway, and if you ever delete the NAT Gateway, you need to separately release the EIP (otherwise you continue paying for an unattached EIP). [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## 1.4 — The Private Route Table: What Makes a Subnet Private

A subnet is not inherently "public" or "private" based on its CIDR block or name. What makes a subnet private or public is its **route table**. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

In the public route table (created in a previous lecture), the route `0.0.0.0/0 → Internet Gateway` sends all non-local traffic directly to the internet. This is what makes a subnet public — instances can both reach and be reached from the internet.

In the **private route table** (created in this lecture), the route `0.0.0.0/0 → NAT Gateway` sends all non-local traffic to the NAT Gateway instead. The video states: "This rule makes your private subnet private because the traffic is routed through the NAT Gateway." The NAT Gateway only allows outbound connections — it doesn't accept inbound connections from the internet. So instances in subnets associated with this route table can reach the internet but cannot be reached from it. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

The route table is then associated with the **two private subnets**. After this association, those subnets are functionally private — their internet traffic flows through the NAT Gateway, not directly through the IGW. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

⚠️ **Expert Note:**
The NAT Gateway is the first non-free resource in this VPC build. The video explicitly warns: "So far, whatever we have created is free of cost. We're not going to get any bill for this, but now, we are going to create a NAT Gateway, and that is not free." NAT Gateways are billed per hour of availability plus per GB of data processed. The video advises completing the entire remaining VPC section in one sitting and doing cleanup afterward to minimize costs: "Once you start with NAT Gateway, you have to go until you finish this entire VPC. Complete all the lectures and then we are going to do the cleanup." [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## 1.5 — NAT Gateway Subnet Placement: Public, Not Private

This is the single most commonly misunderstood aspect of NAT Gateways, and the video emphasizes it strongly. The NAT Gateway **serves** private subnets (private instances route through it), but it **lives in** a public subnet. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

The reasoning is simple: the NAT Gateway itself needs internet access to forward traffic. It gets internet access from the public subnet's route table, which routes to the IGW. If you placed the NAT Gateway in a private subnet, it would have no internet access itself and couldn't forward anything. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

The video places it in `vpro-public-subnet-1` and notes: "You can place it in public subnet one or two, does not matter because we are just creating one NAT gateway." The choice between public subnets is arbitrary for a single NAT Gateway — what matters is that it's in **a** public subnet, not in a private one. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## 1.6 — DNS Hostnames: Beyond IP Addresses

After the NAT Gateway and route table are configured, the video addresses one more VPC-level setting: **DNS hostnames**. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

When you launch an EC2 instance, it gets IP addresses — private IP in any subnet, public IP in public subnets. But beyond IPs, AWS can also assign **DNS hostnames** to instances — names like `ec2-172-31-xx-xx.compute.amazonaws.com`. These hostnames resolve to the instance's IP address and are useful for service discovery, configuration, and human-readable identification. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

By default, DNS hostnames are **not enabled** in a custom VPC. The video enables them: "The instances will also get the host names along with the IPs, public or private both." This is done at the VPC level — once enabled, all instances launched in this VPC receive DNS hostnames automatically. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## 1.7 — Complete VPC Architecture Summary

At the end of this lecture, the VPC is architecturally complete. The video recaps: "We have created VPC. We have created four subnets — two public, two private. We have Internet Gateway and NAT Gateway connected through the route tables." [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

The complete architecture:

* **VPC** — the isolated network boundary.
* **2 Public Subnets** — associated with the public route table → IGW. Instances get public + private IPs.
* **2 Private Subnets** — associated with the private route table → NAT Gateway. Instances get private IPs only.
* **Internet Gateway** — provides direct internet access for public subnets.
* **NAT Gateway** — placed in a public subnet, provides outbound-only internet access for private subnets. Has an Elastic IP.
* **Public Route Table** — `0.0.0.0/0 → IGW`.
* **Private Route Table** — `0.0.0.0/0 → NAT Gateway`.
* **DNS Hostnames** — enabled at VPC level.

The next lecture will put this VPC into use: creating bastion hosts, launching instances in private subnets, setting up a load balancer, and testing the entire setup. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are completing the VPC network by creating the NAT Gateway (with its Elastic IP), the private route table (with its route and subnet associations), and enabling DNS hostnames. The final outcome: private subnets that can reach the internet outbound (through the NAT Gateway) but cannot be reached inbound, plus DNS hostname resolution for all instances. After this, the VPC is fully functional and ready for use. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**⚠️ Cost Warning:** The NAT Gateway is **not free**. Everything created up to this point in the VPC section was free. Once the NAT Gateway is created, billing starts. Complete all remaining VPC lectures in one session and perform cleanup to minimize costs. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Execution Flow Overview

```
Step 1: Allocate Elastic IP
Step 2: Create NAT Gateway (in public subnet, attach EIP)
Step 3: Create Private Route Table
Step 4: Associate Private Subnets with Private Route Table
Step 5: Add Route: 0.0.0.0/0 → NAT Gateway
Step 6: Enable DNS Hostnames on VPC
```

***

### Step 1: Allocate Elastic IP

**What we are doing:** Creating a static public IP address that will be attached to the NAT Gateway.

**Why first:** The EIP must exist before the NAT Gateway can be created, because the NAT Gateway requires an EIP during creation. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**Execution:**

1. Navigate to **VPC → Elastic IPs** (in the left sidebar).
2. Click **Allocate Elastic IP Address**.
3. Add a **Name tag:** `vprofile-NAT-Elastic-IP`. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)
4. Click **Allocate**.

**Expected result:** An Elastic IP appears in the list with a public IPv4 address assigned.

**How to verify:** The EIP shows in the Elastic IPs list with status "Allocated" and no association (it's not attached to anything yet).

**Common mistake:** Forgetting to release the EIP during cleanup. An unattached EIP incurs charges — AWS charges for EIPs that are allocated but not associated with a running resource.

**Connection to flow:** This EIP will be selected in Step 2 when creating the NAT Gateway. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

### Step 2: Create NAT Gateway

**What we are doing:** Creating the NAT Gateway that will provide outbound internet access for private subnets.

**Execution:**

1. Navigate to **VPC → NAT Gateways**.
2. Click **Create NAT Gateway**.
3. **Name:** `vpro-NAT-Gateway`. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)
4. **Subnet:** Select **`vpro-public-subnet-1`**.
   * ⚠️ **Critical:** The NAT Gateway must be placed in a **public** subnet. "Make sure you place it in the right subnet." It can be public subnet 1 or 2 — doesn't matter. But it must NOT be in a private subnet. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)
5. **Elastic IP allocation ID:** Select the EIP created in Step 1 (`vprofile-NAT-Elastic-IP`).
   * If you haven't created it, you can click **Allocate Elastic IP** directly from this page. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)
6. Click **Create NAT Gateway**.

**Expected result:** The NAT Gateway appears with status **Pending**. It takes a few minutes to become **Available**. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**How to verify:** After a few minutes, refresh the NAT Gateways page. Status should change from "Pending" to "Available."

**Common mistake:** Placing the NAT Gateway in a private subnet. It will be created but won't function — it can't reach the internet from a private subnet.

**What to do while waiting:** The video uses this time productively: "Let's not waste time. Let's go to the route table." Proceed to Step 3 while the NAT Gateway provisions. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

### Step 3: Create Private Route Table

**What we are doing:** Creating the route table that will be associated with the private subnets, routing their internet traffic through the NAT Gateway.

**Execution:**

1. Navigate to **VPC → Route Tables**.
2. Click **Create Route Table**.
3. **Name:** `vpro-private-route-table`. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)
4. **VPC:** Select the vProfile VPC.
5. Click **Create Route Table**.

**Expected result:** A new route table appears. By default, it only has the local route (VPC CIDR → local).

**Connection to flow:** This route table needs subnet associations (Step 4) and a route to the NAT Gateway (Step 5).

***

### Step 4: Associate Private Subnets

**What we are doing:** Linking the two private subnets to this route table so they use its routes.

**Execution:**

1. Select the `vpro-private-route-table`.
2. Go to the **Subnet Associations** tab.
3. Click **Edit Subnet Associations**.
4. Select the **two private subnets** (and only the private subnets — do not select public subnets). [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)
5. Click **Save**.

**How to verify:** The Subnet Associations tab shows both private subnets listed under "Explicit subnet associations."

**Common mistake:** Accidentally associating a public subnet with the private route table. This would route the public subnet's traffic through the NAT Gateway instead of the IGW, breaking direct internet access for public instances. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

### Step 5: Add Route to NAT Gateway

**What we are doing:** Adding the route that sends all non-local traffic from the private subnets to the NAT Gateway.

**Execution:**

1. With `vpro-private-route-table` selected, go to the **Routes** tab.
2. Click **Edit Routes** → **Add Route**.
3. **Destination:** `0.0.0.0/0` (all traffic not matching the local VPC CIDR). [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)
4. **Target:** Select **NAT Gateway** → select the NAT Gateway created in Step 2.
5. Click **Save Changes**. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**What this route means:** "All the traffic that doesn't belong to the local goes to the NAT Gateway." Any traffic destined for IPs outside the VPC CIDR is forwarded to the NAT Gateway, which then forwards it to the internet through the IGW.

**How to verify:** The Routes tab shows two routes:

* `VPC CIDR → local` (automatically created)
* `0.0.0.0/0 → NAT Gateway` (just added) [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**Verify NAT Gateway status:** Check that the NAT Gateway status is now **Available** (it should be by now). [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**Connection to flow:** With this route in place, the private subnets are now functionally private with outbound internet access through the NAT Gateway.

***

### Step 6: Enable DNS Hostnames

**What we are doing:** Enabling DNS hostname assignment for all instances in this VPC.

**Why:** By default, custom VPCs do not assign DNS hostnames to instances. Without this, instances only get IP addresses — no human-readable names. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**Execution:**

1. Navigate to **VPC → Your VPCs**.
2. Select the vProfile VPC.
3. Click **Actions → Edit VPC Settings**.
4. Scroll down to find **Enable DNS Hostnames**.
5. Check the box to enable it.
6. Click **Save**. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

**Expected result:** All instances launched in this VPC will now receive DNS hostnames (both public and private) in addition to their IP addresses.

**How to verify:** Launch a test instance in the VPC and check its details — it should show a DNS hostname like `ec2-x-x-x-x.region.compute.amazonaws.com`.

**Connection to flow:** The VPC is now fully configured — four subnets, two route tables, IGW, NAT Gateway with EIP, and DNS hostnames. The next lecture begins using this VPC by launching bastion hosts, private instances, and load balancers. [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    NAT Gateway + Private Route Table + DNS Hostnames
PURPOSE:  Give private subnets outbound-only internet access; complete VPC
CONTEXT:  Final infrastructure step before launching instances in the VPC
⚠️ COST:  NAT Gateway is NOT FREE — first paid resource in VPC build
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Complete VPC Architecture (After This Lecture)

```
                    INTERNET
                       │
                       ▼
               ┌───────────────┐
               │ Internet GW   │
               └───────┬───────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
  ┌──────┴──────┐            ┌───────┴──────┐
  │ Public Sub 1│            │ Public Sub 2 │
  │             │            │              │
  │ NAT Gateway │            │              │
  │ (EIP)       │            │              │
  └──────┬──────┘            └──────────────┘
         │
         │  (0.0.0.0/0 → NAT GW)
         │
  ┌──────┴──────┐            ┌──────────────┐
  │ Private Sub1│            │ Private Sub 2│
  │             │            │              │
  └─────────────┘            └──────────────┘

PUBLIC ROUTE TABLE:   0.0.0.0/0 → IGW         (public sub 1 + 2)
PRIVATE ROUTE TABLE:  0.0.0.0/0 → NAT Gateway (private sub 1 + 2)
DNS HOSTNAMES:        Enabled at VPC level
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## NAT Gateway Core Rules

```
SERVES:      Private subnets (outbound internet for private instances)
LIVES IN:    Public subnet (needs internet access via IGW)
REQUIRES:    Elastic IP (static public IP)
DIRECTION:   Outbound ONLY — internet cannot initiate inbound connections

TRAFFIC FLOW:
  Private instance → NAT Gateway (public subnet) → IGW → Internet
  Internet → ❌ BLOCKED (cannot reach private instance)

COMMON MISTAKE: Placing NAT GW in private subnet → can't reach internet → useless
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Elastic IP → NAT Gateway Dependency

```
1. Allocate Elastic IP (static public IP)     ← must exist FIRST
2. Create NAT Gateway → attach EIP            ← references EIP
3. NAT Gateway uses EIP to communicate with internet

CLEANUP ORDER (reverse):
  1. Delete NAT Gateway
  2. Release Elastic IP         ← unattached EIP still costs money!

NAMING: vprofile-NAT-Elastic-IP → vpro-NAT-Gateway (easy to identify for cleanup)
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## What Makes a Subnet Public vs. Private

```
SUBNET TYPE    ROUTE TABLE RULE              EFFECT
───────────    ────────────────              ──────
Public         0.0.0.0/0 → IGW              Direct internet access (in + out)
Private        0.0.0.0/0 → NAT Gateway      Outbound only (out via NAT, no inbound)

KEY INSIGHT: "This rule makes your private subnet private
             because the traffic is routed through the NAT Gateway"

IT'S THE ROUTE TABLE that defines public vs. private — not the subnet name or CIDR
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Private Route Table Setup

```
1. Create route table: vpro-private-route-table
2. Associate: private subnet 1 + private subnet 2
3. Add route: 0.0.0.0/0 → NAT Gateway

RESULT:
  Route 1: VPC CIDR → local       (auto-created, internal VPC traffic)
  Route 2: 0.0.0.0/0 → NAT GW    (internet-bound traffic via NAT)
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## DNS Hostnames

```
DEFAULT (custom VPC):  Disabled — instances get IPs only
AFTER ENABLING:        Instances get IPs + DNS hostnames

WHERE: VPC → Actions → Edit VPC Settings → Enable DNS Hostnames

HOSTNAME FORMAT: ec2-x-x-x-x.region.compute.amazonaws.com
APPLIES TO: Both public and private instances in the VPC
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## IP Assignment Rules

```
SUBNET TYPE    PRIVATE IP    PUBLIC IP    DNS HOSTNAME
───────────    ──────────    ─────────    ────────────
Public         ✅            ✅           ✅ (after enabling)
Private        ✅            ❌           ✅ (after enabling)
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Execution Sequence

```
1. Allocate Elastic IP           ← tag: vprofile-NAT-Elastic-IP
2. Create NAT Gateway            ← in PUBLIC subnet, attach EIP
     └── Status: Pending → Available (wait ~2 min)
3. Create Private Route Table    ← while NAT GW provisions (don't waste time)
4. Associate private subnets     ← both private subs to private RT
5. Add route 0.0.0.0/0 → NAT GW ← makes subnets functionally private
6. Enable DNS Hostnames          ← VPC → Actions → Edit VPC Settings

VPC IS NOW COMPLETE ✅
NEXT: Bastion host, private instances, load balancer
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Cost Management Pattern

```
FREE RESOURCES (created earlier):
  VPC, Subnets, IGW, Route Tables, Security Groups

PAID RESOURCES (this lecture):
  NAT Gateway    → billed per hour + per GB processed
  Elastic IP     → free when attached to running resource
                 → CHARGED when unattached or attached to stopped instance

STRATEGY:
  "Once you start with NAT Gateway, go until you finish"
  Complete all lectures → cleanup → stop billing
  Don't leave NAT Gateway running overnight unnecessarily
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Complete VPC Component Inventory

```
COMPONENT                    NAME                          COST
─────────                    ────                          ────
VPC                          vProfile VPC                  Free
Public Subnet 1              vpro-public-subnet-1          Free
Public Subnet 2              vpro-public-subnet-2          Free
Private Subnet 1             vpro-private-subnet-1         Free
Private Subnet 2             vpro-private-subnet-2         Free
Internet Gateway             (attached to VPC)             Free
Public Route Table           (0.0.0.0/0 → IGW)            Free
Elastic IP                   vprofile-NAT-Elastic-IP       Conditional
NAT Gateway                  vpro-NAT-Gateway              💰 PAID
Private Route Table          vpro-private-route-table      Free
DNS Hostnames                Enabled                       Free
```

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## Reusable Engineering Patterns

| Pattern                                    | Manifestation                                                                           |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Gateway/Proxy at Boundary**              | NAT Gateway sits between private network and public internet — mediates traffic         |
| **Outbound-Only Access**                   | Private instances can reach internet but internet cannot reach them — security boundary |
| **Dependency-First Creation**              | EIP must exist before NAT Gateway; NAT Gateway before private route                     |
| **Route-Table-Defines-Behavior**           | Same subnet becomes public or private based solely on its route table association       |
| **Static Identity for Network Components** | Elastic IP = permanent public identity for NAT Gateway (no IP changes)                  |
| **Parallel Work During Provisioning**      | Create route table while NAT Gateway provisions — don't waste time waiting              |
| **Cost-Aware Resource Lifecycle**          | NAT Gateway triggers billing — plan work sessions to minimize idle cost                 |
| **Named Resources for Cleanup**            | Clear naming (`vprofile-NAT-Elastic-IP`) enables easy identification during teardown    |

 [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

## One-Line System Reconstruction

> **A NAT Gateway requires an Elastic IP (static public IP, allocated first), is placed in a public subnet (so it can reach the internet via the IGW), and is targeted by the private route table's `0.0.0.0/0` route — making associated subnets functionally private (outbound-only internet access), while DNS hostnames are enabled at the VPC level to give all instances human-readable names alongside their IPs — completing the VPC architecture (VPC + 4 subnets + IGW + NAT GW + 2 route tables + DNS) ready for bastion hosts and load balancers.** [\[271-nat-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/271-nat-gateway.txt)

***

This completes the full reconstruction of the NAT Gateway lecture. It connects to the previous VPC lectures (VPC creation, subnets, IGW, public route table) and leads directly into the next lecture where the VPC is put to use with bastion hosts, private instances, and load balancers. Let me know if you'd like any section expanded or adjusted! 🚀
