# 🌐 GCP VPC, Subnets & Network Setup — Deep Learning Material

**Source:** Video caption file — [293-vpc-subnets-and-network-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt?EntityRepresentationId=5e67125d-c25b-431b-8206-0b50baa81e1e) [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Video Context:** The instructor builds a custom VPC networking infrastructure on Google Cloud Platform (GCP) using `gcloud` CLI commands from Google Cloud Shell. The setup includes: a custom-mode VPC, four subnets (two public, two private) with specific CIDR ranges, a Cloud Router, and a Cloud NAT gateway for private subnet internet access. Firewall rules and bastion host are deferred to the next lecture. Variables for resource names were pre-set in `.bashrc` in a prior session.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Custom-Mode VPC — Manual Control Over Network Design

In GCP, when you create a VPC, you choose between **auto-mode** and **custom-mode** subnets. Auto-mode automatically creates one subnet in every GCP region with pre-assigned CIDR ranges. Custom-mode creates the VPC as an **empty shell** — no subnets at all — and you manually create each subnet with your own chosen CIDR ranges, in your chosen regions. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

The instructor uses `--subnet-mode=custom` explicitly. The reason is architectural control: in a real project like Vprofile, you need specific subnets (public and private) in specific regions with specific IP ranges that fit your network design. Auto-mode gives you no control over these choices — you get whatever Google assigns. Custom-mode gives you full control.

After creating the VPC, GCP responds with a warning: **"The instances on this network will not be reachable until firewall rules are created."** This is a fundamental GCP networking principle: a custom VPC starts with **zero firewall rules**. Unlike the default VPC which has permissive rules, a custom VPC is fully locked down by default. All inbound and outbound traffic is denied until you explicitly create firewall rules. This is a security-by-default design. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

The instructor verifies in the Google Cloud Console: navigating to **VPC Networks** shows the new VPC alongside the default VPC. The new VPC has no subnets, no firewall rules, and no routing configured yet — it's a blank canvas.

***

## 1.2 Subnets — Dividing the VPC Address Space

Subnets are subdivisions of the VPC's IP address space. Each subnet exists in a specific **region** (not availability zone — GCP subnets are regional, spanning all zones within that region). The instructor creates four subnets within the VPC: [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

| Subnet            | Variable Name    | CIDR Range     | Purpose                    |
| ----------------- | ---------------- | -------------- | -------------------------- |
| Public Subnet 01  | `PUB_SUBNET_01`  | `172.2.1.0/24` | Public-facing resources    |
| Public Subnet 02  | `PUB_SUBNET_02`  | `172.2.2.0/24` | Public-facing resources    |
| Private Subnet 01 | `PRIV_SUBNET_01` | `172.2.3.0/24` | Backend/internal resources |
| Private Subnet 02 | `PRIV_SUBNET_02` | `172.2.4.0/24` | Backend/internal resources |

The overall VPC CIDR is `172.2.0.0/16`, which provides 65,536 IP addresses. Each `/24` subnet carves out 256 IPs from that space. In GCP, **5 IPs are reserved** per subnet (for network address, gateway, and GCP internal use), leaving **251 usable** IPs per subnet. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

A critical conceptual point: **the command to create subnets differs from VPCs in what parameters are required**. VPC creation does not require a region (VPCs are global in GCP). Subnet creation **does** require a region, a network (which VPC to belong to), and a range (the CIDR block). The instructor explicitly calls this out: "In creating VPC we did not mention the region. But in creating subnet we have to mention all those things."

🔍 **Deep Dive:** The naming convention the instructor uses — `PUB_SUBNET_01`, `PUB_SUBNET_02`, `PRIV_SUBNET_01`, `PRIV_SUBNET_02` — is purely organizational. GCP itself does not enforce a concept of "public" vs. "private" subnets the way AWS does (AWS has route table associations that make subnets public or private). In GCP, what makes a subnet "private" is whether the VMs in it have public IPs or not. This distinction is covered in §1.5. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

***

## 1.3 Variables in `.bashrc` — Pre-configured Naming System

All resource names and configuration values are stored as **shell variables** set in the `.bashrc` file from a previous session. The instructor references variables like `$VPC`, `$REGION`, `$PUB_SUBNET_01`, `$PRIV_SUBNET_02`, `$ROUTER`, `$NAT` throughout the commands. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

This is a deliberate operational pattern: by defining all names and values as variables, every `gcloud` command uses consistent, typo-free references. If a name needs to change, you change it in one place (`.bashrc`) rather than in every command. The instructor's variable values (visible from command outputs) include:

* `$VPC` → `vprofile` (or similar)
* `$REGION` → a specific GCP region
* `$ROUTER` → `vprofile-router`
* `$NAT` → the NAT gateway name

***

## 1.4 Cloud Router — The Routing Foundation

A **Cloud Router** is a GCP-managed router that provides dynamic routing for your VPC. The instructor creates it as a prerequisite for Cloud NAT. The router is associated with a specific VPC and region. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

The command requires three things: the router name, the network (VPC), and the region. The router itself doesn't do anything visible yet — it becomes useful when Cloud NAT is attached to it (next step) and in more advanced scenarios like VPN and interconnect where dynamic route exchange (BGP) is needed.

The instructor verifies in the console: Cloud Router appears under **Network Connectivity** (not under VPC). This is a GCP console organizational detail — "You won't see this in the VPC section like in AWS. Here the routers are in network connectivity section." [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

***

## 1.5 Cloud NAT — Internet Access for Private Subnets

**Cloud NAT** (Network Address Translation) provides **outbound** internet access to VMs that have **only private IPs** (no public IP). VMs in private subnets need to download packages, pull updates, communicate with external APIs — but they shouldn't be directly reachable from the internet. Cloud NAT solves this by translating their private IPs to a public IP for outbound traffic, while keeping them unreachable from inbound internet traffic. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

Cloud NAT is created **on top of a Cloud Router** — this is why the router was created first. The NAT gateway uses the router to know how to route traffic between the VPC and the internet.

Two critical configuration options in the NAT creation command:

**`--auto-allocate-nat-external-ips`:** This tells GCP to automatically allocate a public IP and attach it to the NAT gateway. "A NAT gateway needs to have a public IP so it can communicate to the internet." This public IP is the address that external servers see when private VMs make outbound connections. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**`--nat-all-subnet-ip-ranges`:** This tells the NAT gateway to provide NAT service to **all subnets** in the VPC. But the instructor raises an important question: "Right now we just have subnets. And there is just the name to the subnet — private or public. So how does it decide which is the private subnet?"

The answer reveals a fundamental GCP networking concept: **"Any VM without public IP — it has just the private IP — will be considered as the instance in the private subnet. If the VM has the public IP in the private subnet, the private subnet is not private anymore. It just becomes public."** [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

This is radically different from AWS where public/private is determined by route table associations. In GCP, it's determined by **whether the individual VM has a public IP or not**. The subnet name is just a label — the actual public/private behavior is a per-VM configuration decision made at instance launch time. Cloud NAT only acts on VMs without public IPs; VMs with public IPs access the internet directly and bypass NAT.

⚠️ **Expert Note:** This "all about configuration" model means you must be disciplined when launching VMs. If you accidentally assign a public IP to a VM in a "private" subnet, that VM is now publicly accessible — the subnet name won't protect you. The privacy is enforced at the VM level, not the subnet level. This is a common GCP vs. AWS conceptual trap.

***

## 1.6 Console Navigation — Where to Find Things

The instructor shows that GCP services are organized differently in the console than AWS: [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

* **VPC Networks** → under the hamburger menu (main navigation)
* **Cloud Router** → under **Network Connectivity** (not under VPC)
* **Cloud NAT** → under **Network Services** (not under VPC)
* **Load Balancing** → also under **Network Services**
* **Cloud DNS** → also under **Network Services**

The instructor notes: "It's not in the VPC, but that's fine as long as we can just search our services we can find it." The search bar is the practical way to find any GCP service regardless of its menu location.

***

## 1.7 What Remains — Firewall Rules and Bastion Host

The instructor closes by noting what's been completed and what's left: VPC created, four subnets created, Cloud Router created, Cloud NAT created. Remaining for the next lecture: **firewall rules** (to allow specific traffic into and out of the VPC) and a **bastion host** (a jump server to SSH into private VMs). [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a **complete VPC networking foundation** on GCP for the Vprofile project: a custom VPC with four subnets (two public, two private), a Cloud Router, and a Cloud NAT gateway for private subnet internet access. The final outcome: a fully prepared network infrastructure ready to host instances, with private subnets able to reach the internet for updates while remaining unreachable from outside. Firewall rules and bastion host come in the next lecture. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Prerequisite:** Variables for all resource names must already be set in `.bashrc` (done in a prior lecture).

***

## Step 1: Create the Custom VPC

```bash
gcloud compute networks create "$VPC" --subnet-mode=custom
```

**Breakdown:** [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

* `gcloud compute networks create` — the GCP CLI command to create a VPC network
* `"$VPC"` — the VPC name, pulled from the variable set in `.bashrc` (e.g., `vprofile`)
* `--subnet-mode=custom` — creates the VPC with no subnets; you'll add them manually

**Expected output:** Success message + a warning: *"Instances on this network will not be reachable until firewall rules are created."* The warning also shows the syntax for creating firewall rules — that's deferred to the next lecture. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Verification:** In the Google Cloud Console → navigate via hamburger menu → **VPC Networks**. Scroll down — you should see the new VPC alongside the `default` VPC. It will have no subnets, no firewall rules. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Connection to flow:** The VPC is the container. Everything else (subnets, router, NAT, firewall rules, instances) lives inside it.

***

## Step 2: Create the Four Subnets

Each subnet requires: a name, the network (VPC) it belongs to, the region, and the CIDR range.

### Subnet 1 — Public Subnet 01:

```bash
gcloud compute networks subnets create "$PUB_SUBNET_01" \
  --network="$VPC" \
  --region="$REGION" \
  --range=172.2.1.0/24
```

**Breakdown:** [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

* `gcloud compute networks subnets create` — command to create a subnet (note: **`subnets`** with an "s" — the instructor made a typo initially using `subnet` without the "s" and got an error)
* `"$PUB_SUBNET_01"` — subnet name from variable
* `--network="$VPC"` — which VPC this subnet belongs to
* `--region="$REGION"` — which region (subnets are regional in GCP, spanning all zones in that region)
* `--range=172.2.1.0/24` — the CIDR block (256 IPs, 251 usable after 5 GCP-reserved)

⚠️ **Common mistake caught in the video:** Using `subnet` (singular) instead of `subnets` (plural) in the command. The instructor hit this error and fixed it with the up arrow. If you get a "command not found" type error, check for this typo. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

### Subnet 2 — Public Subnet 02:

```bash
gcloud compute networks subnets create "$PUB_SUBNET_02" \
  --network="$VPC" \
  --region="$REGION" \
  --range=172.2.2.0/24
```

Use the **up arrow** to recall the previous command and change the variable name to `$PUB_SUBNET_02` and the range to `172.2.2.0/24`. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

### Subnet 3 — Private Subnet 01:

```bash
gcloud compute networks subnets create "$PRIV_SUBNET_01" \
  --network="$VPC" \
  --region="$REGION" \
  --range=172.2.3.0/24
```

Change variable to `$PRIV_SUBNET_01`, range to `172.2.3.0/24`. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

### Subnet 4 — Private Subnet 02:

```bash
gcloud compute networks subnets create "$PRIV_SUBNET_02" \
  --network="$VPC" \
  --region="$REGION" \
  --range=172.2.4.0/24
```

Change variable to `$PRIV_SUBNET_02`, range to `172.2.4.0/24`. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**The instructor's warning:** "Do not rush. Make sure all the values are correct." Specifically: "Make sure you change the variable names" when reusing the previous command with the up arrow. Using the wrong variable name means the subnet gets the wrong name, causing confusion later. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

### Verification:

Navigate to **VPC Networks** → click on your VPC → click on **Subnets** tab → refresh.

**Expected result:** Four subnets listed with: [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

* Correct names: `pub-subnet-01`, `pub-subnet-02`, `priv-subnet-01`, `priv-subnet-02` (actual names from variables)
* Correct region: all in the same region
* Correct ranges: `172.2.1.0/24`, `172.2.2.0/24`, `172.2.3.0/24`, `172.2.4.0/24`

**If anything is wrong:** "Select it and delete it and execute that particular command." Don't try to rename or modify — delete the incorrect subnet and recreate it with the right values. The instructor emphasizes: "You need to have these four subnets with these names and these exact ranges." [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Connection to flow:** The four subnets define where VMs will be placed. Public subnets hold internet-facing resources; private subnets hold backend resources that access the internet through Cloud NAT.

***

## Step 3: Create the Cloud Router

```bash
gcloud compute routers create "$ROUTER" \
  --network="$VPC" \
  --region="$REGION"
```

**Breakdown:** [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

* `gcloud compute routers create` — command to create a Cloud Router
* `"$ROUTER"` — router name from variable (e.g., `vprofile-router`)
* `--network="$VPC"` — the VPC this router serves
* `--region="$REGION"` — the region (router is regional)

**Expected output:** Quick success. Output shows the router name, region, and VPC.

**Verification:** Search for **Cloud Router** in the console → appears under **Network Connectivity**. You should see the router with the correct name, VPC, and region. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Connection to flow:** The router is the foundation on which Cloud NAT is built. Without the router, you cannot create NAT.

***

## Step 4: Create the Cloud NAT Gateway

```bash
gcloud compute routers nats create "$NAT" \
  --router="$ROUTER" \
  --region="$REGION" \
  --auto-allocate-nat-external-ips \
  --nat-all-subnet-ip-ranges
```

**Breakdown:** [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

* `gcloud compute routers nats create` — command to create a Cloud NAT (note: NAT is created as a sub-resource of the router, hence `routers nats`)
* `"$NAT"` — NAT gateway name from variable
* `--router="$ROUTER"` — which router to attach this NAT to
* `--region="$REGION"` — must match the router's region
* `--auto-allocate-nat-external-ips` — GCP automatically assigns a public IP to the NAT gateway so it can communicate with the internet
* `--nat-all-subnet-ip-ranges` — provide NAT service to all subnets in the VPC (but only VMs **without** public IPs will actually use it — see Theory §1.5) [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Expected output:** Success message confirming Cloud NAT creation.

**Verification:** Search for **Cloud NAT** in the console → appears under **Network Services**. You should see the NAT gateway associated with your router. [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)

**Connection to flow:** Cloud NAT completes the network infrastructure. Private VMs (no public IP) can now reach the internet for updates and external communication, while remaining unreachable from outside. The next lecture adds firewall rules (to control what traffic is allowed) and a bastion host (to SSH into private VMs).

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Network Architecture — What We Built

```
VPC: $VPC (custom-mode, 172.2.0.0/16)
│
├── PUBLIC SUBNETS (VMs WITH public IP)
│   ├── pub-subnet-01:  172.2.1.0/24  (251 usable IPs)
│   └── pub-subnet-02:  172.2.2.0/24  (251 usable IPs)
│
├── PRIVATE SUBNETS (VMs WITHOUT public IP)
│   ├── priv-subnet-01: 172.2.3.0/24  (251 usable IPs)
│   └── priv-subnet-02: 172.2.4.0/24  (251 usable IPs)
│
├── CLOUD ROUTER: $ROUTER (vprofile-router)
│   └── CLOUD NAT: $NAT
│       ├── auto-allocated public IP
│       └── NATs all subnets (only affects VMs without public IP)
│
├── FIREWALL RULES: (next lecture)
└── BASTION HOST:    (next lecture)
```

***

## ⚡ Command Sequence — Operational Flow

```
1. CREATE VPC:
   gcloud compute networks create "$VPC" --subnet-mode=custom

2. CREATE 4 SUBNETS (same pattern, change name + range):
   gcloud compute networks subnets create "$SUBNET_VAR" \
     --network="$VPC" --region="$REGION" --range=172.2.X.0/24
   
   X=1 → pub-subnet-01    X=3 → priv-subnet-01
   X=2 → pub-subnet-02    X=4 → priv-subnet-02
   ⚠️ subnets (with S), NOT subnet

3. CREATE CLOUD ROUTER:
   gcloud compute routers create "$ROUTER" \
     --network="$VPC" --region="$REGION"

4. CREATE CLOUD NAT:
   gcloud compute routers nats create "$NAT" \
     --router="$ROUTER" --region="$REGION" \
     --auto-allocate-nat-external-ips \
     --nat-all-subnet-ip-ranges
```

***

## 🔗 GCP vs. AWS — Public/Private Subnet Logic

```
AWS:
  Public/Private = determined by ROUTE TABLE association
  Subnet is public if route table has IGW route
  Subnet is private if route table has NO IGW route
  → Structural (subnet-level decision)

GCP:
  Public/Private = determined by VM's PUBLIC IP assignment
  VM with public IP → acts as public (direct internet)
  VM without public IP → acts as private (uses Cloud NAT)
  → Behavioral (per-VM decision at launch time)

⚠️ GCP subnet NAME (pub/priv) is just a LABEL
   Actual public/private behavior = VM config, not subnet config
```

***

## 📦 Resource Parameter Requirements

```
VPC:     name + subnet-mode              (NO region — VPCs are GLOBAL)
SUBNET:  name + network + region + range (REGION required)
ROUTER:  name + network + region
NAT:     name + router + region + IP allocation + subnet scope
```

***

## 🔄 GCP Console Navigation — Where to Find What

```
VPC Networks:        Hamburger menu → VPC Networks
Cloud Router:        Network Connectivity → Cloud Routers
Cloud NAT:           Network Services → Cloud NAT
Load Balancing:      Network Services → Load Balancing
Cloud DNS:           Network Services → Cloud DNS

SHORTCUT: Use search bar for any service
```

***

## 🛡️ Security Default — Custom VPC

```
Custom VPC created → ZERO firewall rules → ALL traffic DENIED
  "Instances will not be reachable until firewall rules are created"

vs. Default VPC → has permissive default rules

ACTION: Must create firewall rules explicitly (next lecture)
```

***

## 🧱 IP Addressing Scheme

```
VPC CIDR:           172.2.0.0/16     → 65,536 IPs total
├── pub-subnet-01:  172.2.1.0/24    → 256 total, 251 usable (5 reserved)
├── pub-subnet-02:  172.2.2.0/24    → 256 total, 251 usable
├── priv-subnet-01: 172.2.3.0/24    → 256 total, 251 usable
└── priv-subnet-02: 172.2.4.0/24    → 256 total, 251 usable

GCP reserves 5 IPs per subnet (vs. AWS reserves 5)
```

***

## 🔄 Cloud NAT — How Private Internet Access Works

```
PRIVATE VM (no public IP)
    │ outbound request (e.g., apt update)
    ▼
CLOUD NAT
    │ translates private IP → NAT's public IP
    ▼
INTERNET
    │ response
    ▼
CLOUD NAT
    │ translates back → private IP
    ▼
PRIVATE VM

INBOUND from internet → BLOCKED (NAT is outbound-only)

WHO USES NAT: Only VMs without public IP
WHO BYPASSES NAT: VMs with public IP (direct internet access)
```

***

## ⚠️ Error Recall

```
SYMPTOM: "command not found" on subnet creation
CAUSE:   gcloud compute networks subnet create  ← missing 'S'
FIX:     gcloud compute networks subnets create  ← add 'S'

SYMPTOM: Wrong subnet name or range after creation
FIX:     Delete the wrong subnet → recreate with correct values
         (do NOT try to rename or modify)

GENERAL: "Do not rush. Make sure all the values are correct."
         Especially when reusing commands with up-arrow — change BOTH
         the variable name AND the range value.
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Variable-Driven Infrastructure Commands**
Store all resource names in `.bashrc` variables → reference `$VAR` in every command. Benefits: consistency (no typos across 10+ commands), single-point-of-change (rename by changing one variable), and documentation (variable names describe the resource's purpose). This is the manual-CLI equivalent of Terraform variables.

**Pattern 2: Empty-Shell-Then-Populate**
Create the container (VPC) empty → add components (subnets) one by one → add services (router, NAT) on top. Each layer depends on the previous. This progressive construction pattern ensures you can verify each layer before adding the next.

**Pattern 3: Privacy-by-Configuration, Not by Structure**
In GCP, public/private is a per-instance decision (public IP yes/no), not a per-subnet structural decision. This means the same subnet can hold both public and private VMs. The operational discipline falls on the person launching the VM, not on the network architect. This is more flexible but requires more careful instance-level configuration.

***

## 🎯 One-Line System Summary

> **A custom-mode GCP VPC starts as an empty, fully-locked-down network shell; four subnets (`/24` each from a `/16` VPC range) are created in one region; a Cloud Router provides the routing foundation; Cloud NAT attached to the router gives outbound internet access to VMs without public IPs (the GCP definition of "private"); and public/private distinction is determined per-VM at launch time, not per-subnet structurally.** [\[293-vpc-su...work-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/293-vpc-subnets-and-network-setup.txt)
