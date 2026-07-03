# 🎓 Deep Learning Material: AWS VPC Route Tables & Public Subnet Configuration

**Source:** [270-route-tables.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt?EntityRepresentationId=38c81506-3930-4a53-9099-18648b38d8f4) — Video lecture covering AWS VPC route tables — connecting an internet gateway to public subnets through route table creation, subnet association, the `0.0.0.0/0` route entry that makes subnets public, enabling auto-assign public IP on subnets, and foreshadowing NAT gateway for private subnets. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: A VPC with Subnets and an Internet Gateway — But No Connection Between Them

At this point in the VPC build, three components exist independently: the **vprofile-VPC**, two **public subnets** inside it, and an **internet gateway** attached to the VPC. However, none of these components are functionally connected yet. The subnets exist as network address spaces, and the internet gateway exists as an attachment to the VPC, but there is no routing instruction that tells traffic from the subnets how to reach the internet gateway. Traffic originating from an instance in a subnet has no path to the internet. The **route table** is the component that creates this path. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

## 1.2 What a Route Table Is

A route table is a set of **routing rules** (called routes) that determine where network traffic from a subnet is directed. Every subnet in a VPC must be associated with a route table. When an instance in a subnet sends a packet, the VPC looks at the destination IP address of that packet, checks the route table associated with that subnet, and forwards the packet according to the matching rule. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

When you create a VPC, AWS automatically creates a **default route table** for it. This default route table has a single route: traffic destined for the VPC's own CIDR range is routed locally (within the VPC). But it has **no route to the internet**. This is why subnets associated with only the default route table are effectively private — they can communicate within the VPC but cannot reach the outside world. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

The video shows this: after creating the vprofile-VPC, a route table called `vprofile-default-RT` appeared automatically. The instructor explicitly says: "I did not create this route table. It got created automatically when we created the VPC." This default route table is not used for public subnets — it is left as-is. A **new** route table is created specifically for the public subnets. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

## 1.3 The Default VPC's Route Table — The Reference Pattern

The video examines the **default VPC's** route table (the one AWS creates for every account's default VPC) to show what a working public route table looks like. Its routes contain the entry `0.0.0.0/0 → Internet Gateway`. This is the pattern to replicate. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

`0.0.0.0/0` is a **CIDR notation** that means "any IP address" — it is the default route, the catch-all. When no other, more specific route matches the destination, this rule applies. By pointing it at the internet gateway, it says: "Any traffic whose destination is not within the VPC itself should be sent to the internet gateway, which forwards it to the public internet." [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

## 1.4 The Three-Step Process That Makes a Subnet Public

A subnet is not inherently public or private. It becomes **public** through three specific configurations: [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**Step 1 — Create a route table** with a route to the internet gateway (`0.0.0.0/0 → IGW`).

**Step 2 — Associate the route table with the subnet(s)**. A subnet can only be associated with one route table at a time. By associating the public route table with a subnet, all instances in that subnet use these routing rules.

**Step 3 — Enable auto-assign public IP** on the subnet. Without this, instances launched in the subnet receive only private IPs. They can reach the internet (through the route table → internet gateway path), but nothing from the internet can reach them because there is no public IP to address. Enabling auto-assign means every new instance automatically gets a public IP alongside its private IP.

The instructor emphasizes the distinction: "The instance can access the internet but you cannot access the instance because the instance will not have the public IP." This is a crucial nuance — **outbound connectivity** (instance → internet) works with just the route, but **inbound reachability** (internet → instance) requires a public IP on the instance. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

🔍 **Deep Dive**
The instructor describes the single route entry `0.0.0.0/0 → Internet Gateway` as: "This one single entry will make this route table and the subnets public." This is technically the defining characteristic. Any subnet whose route table has a route to an internet gateway is, by AWS definition, a **public subnet**. Any subnet without such a route is a **private subnet**. The distinction is entirely determined by the route table content, not by any property of the subnet object itself. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

## 1.5 Naming Conventions — Why They Matter

The video demonstrates a deliberate naming practice. Every resource gets a descriptive name immediately:

* `Default-PubRT` — Default VPC's public route table
* `vprofile-default-RT` — vprofile VPC's auto-created default route table (not used for public routing)
* `vpro-public-RT` — The new route table for vprofile's public subnets

The instructor says the naming makes resources "easy to identify" — particularly when selecting subnets for association. When the subnet association screen appears, the instructor notes: "Easy to identify because we named it properly." In an environment with dozens of subnets across multiple VPCs, unnamed resources become operationally dangerous — you risk associating the wrong subnet or editing the wrong route table. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

## 1.6 The Private Subnet Foreshadow — NAT Gateway

The lecture closes by stating that private subnets will follow the same structural pattern: create a route table, associate it with subnets, and add a route. But instead of routing `0.0.0.0/0` to an internet gateway, private subnets will route to a **NAT gateway**. A NAT gateway allows instances in private subnets to initiate outbound connections to the internet (for updates, API calls, etc.) while preventing any inbound connections from the internet. This is the next lecture's topic. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are connecting the vprofile-VPC's internet gateway to its two public subnets through a route table, making those subnets fully functional public subnets. The final outcome: instances launched in these subnets will have internet access (outbound) and be reachable from the internet (inbound) via auto-assigned public IPs. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

## Step 1: Identify Existing Route Tables

Navigate to **VPC → Route Tables** in the AWS console.

You should see **two** route tables: [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

| Route Table              | VPC          | Created By                                       |
| ------------------------ | ------------ | ------------------------------------------------ |
| (unnamed — default VPC)  | Default VPC  | AWS (auto-created with default VPC)              |
| (unnamed — vprofile VPC) | vprofile-VPC | AWS (auto-created when vprofile-VPC was created) |

**1a. Name the default VPC's route table:**

Select it → give it the name `Default-PubRT`. This is the default VPC's public route table. It already has a route `0.0.0.0/0 → Internet Gateway`. We are not modifying it — just naming it for identification. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**1b. Name the vprofile VPC's auto-created route table:**

Select it → name it `vprofile-default-RT`. We are **not using** this route table for our public subnets. It was auto-created with the VPC and only has the local route. We name it to avoid confusion. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**1c. Examine the default VPC's route table routes:**

Click on `Default-PubRT` → go to the **Routes** tab. You will see:

| Destination | Target                                     |
| ----------- | ------------------------------------------ |
| (VPC CIDR)  | local                                      |
| `0.0.0.0/0` | igw-xxxxx (default VPC's internet gateway) |

This is the pattern we will replicate for the vprofile VPC. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**Connection to larger flow:** Naming and understanding existing route tables prevents accidental modifications to the wrong resources.

***

## Step 2: Create the Public Route Table

Click **Create Route Table**.

| Setting | Value                                 |
| ------- | ------------------------------------- |
| Name    | `vpro-public-RT`                      |
| VPC     | `vprofile-VPC` (select from dropdown) |

Click **Create**. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

The route table is created with only the default local route (VPC internal traffic). It has **no internet route yet** and is **not associated with any subnet** yet.

**Connection to larger flow:** The route table exists but is non-functional until we associate it with subnets and add the internet gateway route.

***

## Step 3: Associate the Route Table with Public Subnets

Select `vpro-public-RT`. Go to the **Subnet Associations** tab. Click **Edit Subnet Associations**.

Select **both public subnets** (the two subnets created in the previous lecture). The instructor notes they are "easy to identify because we named them properly." [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

Click **Save Associations**. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**What this does:** Both public subnets now use `vpro-public-RT` as their route table instead of the VPC's default route table. Any routing rules in `vpro-public-RT` apply to all instances in these subnets.

**Connection to larger flow:** The subnets are now linked to the route table, but the route table still has no internet route — so these subnets are still effectively private.

***

## Step 4: Add the Internet Gateway Route (The Critical Step)

Select `vpro-public-RT`. Go to the **Routes** tab. Click **Edit Routes**.

Click **Add Route**:

| Destination | Target                                                                 |
| ----------- | ---------------------------------------------------------------------- |
| `0.0.0.0/0` | Internet Gateway → select `vprofile-IGW` (your VPC's internet gateway) |

Click **Save Changes**. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**What this single entry does:** It tells the VPC: "For any traffic from these subnets whose destination is outside the VPC (any IP on the internet), forward it through the internet gateway." This is the **defining action** that makes the subnets public. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**Connection to larger flow:** The routing path is now complete: Instance → Subnet → Route Table → `0.0.0.0/0` → Internet Gateway → Internet. Outbound connectivity is established.

***

## Step 5: Enable Auto-Assign Public IP on Each Public Subnet

Even with the route to the internet gateway, instances won't be **reachable from the internet** without a public IP. Subnets do not assign public IPs by default.

**5a. First public subnet:**

Navigate to **VPC → Subnets**. Find your first public subnet. Select it (check mark). [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

Go to **Actions → Edit Subnet Settings**.

Find the option **Auto-assign IP settings**. **Enable** the checkbox for auto-assign public IPv4 address. Click **Save**. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**5b. Second public subnet:**

Select your second public subnet. **Actions → Edit Subnet Settings → Enable auto-assign public IPv4 → Save.** [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**What this does:** Every EC2 instance launched in these subnets will automatically receive a public IPv4 address in addition to its private IP. This makes the instance addressable from the internet — you can SSH to it, access its web server, etc. (subject to security group rules). [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

⚠️ **Expert Note**
Without enabling auto-assign, you can still manually assign an **Elastic IP** to instances for public access. But auto-assign is the convenient approach for subnets where every instance should be publicly reachable. For subnets where only some instances need public access, you might leave auto-assign disabled and use Elastic IPs selectively. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

**Final state:** The public subnets are fully functional. Instances launched in them will have internet access (outbound via IGW) and be reachable from the internet (inbound via auto-assigned public IP + security group rules).

**What's next:** Private subnets need a similar setup, but with a **NAT gateway** instead of an internet gateway — covered in the next lecture. [\[270-route-tables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/270-route-tables.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture After This Lecture

```
                    INTERNET
                       │
                       ▼
              [ Internet Gateway ]
                  (vprofile-IGW)
                       │
                       │  route: 0.0.0.0/0 → IGW
                       │
              [ vpro-public-RT ]
                  ┌────┴────┐
                  ▼         ▼
          [ Public Sub 1 ] [ Public Sub 2 ]
          (auto-assign IP)  (auto-assign IP)
                  │              │
              instances      instances
          (public + private IP)
```

***

## What Makes a Subnet Public (Three Requirements)

```
1. Route Table with:  0.0.0.0/0 → Internet Gateway     ← THE defining entry
2. Route Table associated with the subnet
3. Auto-assign public IP enabled on the subnet

Missing #1 → no internet path (private subnet)
Missing #2 → route table exists but doesn't apply
Missing #3 → outbound works, but inbound unreachable (no public IP)
```

***

## Route Table Objects in This VPC

```
Default-PubRT          → Default VPC's route table (has IGW route, don't touch)
vprofile-default-RT    → Auto-created with vprofile-VPC (local only, not used for public)
vpro-public-RT         → NEW: created for public subnets, has 0.0.0.0/0 → IGW
```

***

## Operational Sequence

```
1. Identify existing route tables → name them for clarity
2. Examine default VPC's route table → see 0.0.0.0/0 → IGW pattern
3. Create vpro-public-RT → attach to vprofile-VPC
4. Subnet Associations → link both public subnets
5. Edit Routes → add 0.0.0.0/0 → vprofile-IGW     ← subnets become public
6. Subnets → Edit Settings → Enable auto-assign public IP (each subnet)
```

***

## The `0.0.0.0/0` Route Entry

```
Destination: 0.0.0.0/0     = ANY IP address (default route / catch-all)
Target: Internet Gateway    = forward to IGW for internet access

Without this entry:  subnet is PRIVATE (local traffic only)
With this entry:     subnet is PUBLIC
```

***

## Outbound vs Inbound Reachability

```
Route to IGW only (no public IP):
  Instance → Internet:  ✓ works (outbound via IGW)
  Internet → Instance:  ✗ fails (no public IP to address)

Route to IGW + auto-assign public IP:
  Instance → Internet:  ✓ works
  Internet → Instance:  ✓ works (via public IP, subject to security group)
```

***

## Auto-Created vs Manually Created Resources

```
AUTO-CREATED (by VPC creation):
  - Default route table (vprofile-default-RT)
  - Local route within that table

MANUALLY CREATED (this lecture):
  - vpro-public-RT (new route table)
  - 0.0.0.0/0 → IGW route
  - Subnet associations
  - Auto-assign public IP setting
```

***

## Public vs Private Subnet Pattern (Foreshadow)

```
PUBLIC SUBNET:
  Route Table → 0.0.0.0/0 → Internet Gateway
  Instances get public IP → bidirectional internet access

PRIVATE SUBNET (next lecture):
  Route Table → 0.0.0.0/0 → NAT Gateway
  Instances have NO public IP → outbound only (no inbound from internet)

Same structure: create RT → associate subnets → add route
Different target: IGW (public) vs NAT GW (private)
```

***

## Naming Convention Pattern

```
vpro-public-RT        → project-purpose-resourceType
Default-PubRT         → scope-purpose-resourceType
vprofile-default-RT   → project-default-resourceType

Why: prevents selecting wrong resource in crowded AWS console
When: name IMMEDIATELY after creation, before any other action
```

***

## Key Engineering Patterns

| Pattern                                            | Manifestation                                                                                                                 |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Route table as the public/private switch**       | The single `0.0.0.0/0 → IGW` entry is what defines a subnet as public — not any property of the subnet itself                 |
| **Reference pattern from existing infrastructure** | Examine the default VPC's working route table → replicate the pattern for your custom VPC                                     |
| **Three-layer connectivity**                       | Route table (path) + association (link to subnet) + public IP (addressability) — all three needed for full public access      |
| **Auto-created defaults as baseline**              | VPC auto-creates a default route table — understand it, name it, but don't use it for public routing                          |
| **Structural symmetry**                            | Public and private subnets follow the same create-RT → associate → add-route pattern, only the target differs (IGW vs NAT GW) |
| **Name-before-use**                                | Naming resources immediately prevents operational errors when selecting from lists of unnamed resources                       |

***

## Project Continuity

```
BEFORE: Created VPC + 2 public subnets + internet gateway (all disconnected)
THIS:   Connected IGW to public subnets via route table + enabled public IPs
NEXT:   NAT gateway + route table for private subnets
```

***

This completes the full reconstruction. **Theory** explains why route tables exist, what makes a subnet public, and the distinction between outbound and inbound reachability. **Practical** walks through every click and configuration in sequence. The **Compression Map** gives you the architecture diagram, the three-requirement checklist, and the public-vs-private structural symmetry for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
