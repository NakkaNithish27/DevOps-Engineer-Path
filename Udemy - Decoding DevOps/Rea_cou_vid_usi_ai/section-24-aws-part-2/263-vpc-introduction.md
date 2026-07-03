# AWS VPC Introduction & IPv4 Subnetting — Deep Learning Material

**Source:** AWS/DevOps course lecture on VPC Introduction (caption file: [263-vpc-introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt?EntityRepresentationId=40cd21b1-a7e4-4f08-ae9f-1012a968f992)) [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem That Created VPC: From Data Centers to EC2 Classic to VPC

To understand VPC, you need to understand what came before it and what was missing. In traditional corporate data centers, the networking team has **complete control** over every aspect of the network: switches, routers, firewalls, multiple networks, subnets within those networks (some dedicated to front-end services, others to back-end), network access control lists that decide what traffic enters and leaves, IP addressing schemes — everything. The networking team designs and manages all of it.

When AWS launched its early cloud services (SQS, S3, and the original **EC2 Classic**), users could launch virtual machines in Amazon's data centers and use them for computing. But there was a critical gap: **users had no control over networking**. They couldn't decide their own IP addressing scheme, couldn't control what traffic comes in or goes out with fine granularity, couldn't design public and private network segments. The networking was managed entirely by AWS, and users got whatever AWS provided.

Users wanted the same level of network control they had in their own data centers — but in the cloud. AWS responded by creating **VPC: Virtual Private Cloud**. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

## 1.2 — What VPC Actually Is

VPC stands for **Virtual Private Cloud**, and it does exactly what the name implies: on a **public** cloud platform (AWS), you create your own **private** network — a logically isolated section of the AWS cloud where you have complete control.

Think of VPC as creating **your own logical data center** within an AWS region. You design it like you'd design a local area network (LAN): you choose the IP addressing scheme, define the security rules (firewalls), create public-facing networks and private networks, distribute your subnets across multiple availability zones for high availability — all under your control.

Once the VPC network layout is in place, *then* you launch infrastructure inside it — EC2 instances, databases, load balancers, storage. The majority of AWS services depend on VPC. This is why **network design comes first** in any AWS account setup: you lay out the VPC, design the subnets, set up routing tables, and only then start creating your infrastructure inside it. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

Every AWS region comes with a **default VPC** — the one you've been using implicitly when launching EC2 instances without specifying a VPC. But when you create your own VPC, you gain far more control over the network design than the default provides.

> 🔍 **Deep Dive**
> The sequence in a real AWS account setup is: **(1)** Design network layout → **(2)** Create VPC → **(3)** Create subnets → **(4)** Configure routing tables → **(5)** Set up security (NACLs, security groups) → **(6)** Launch instances, databases, storage inside the subnets. Understanding VPC is prerequisite to understanding almost everything else in AWS infrastructure.

***

## 1.3 — IPv4 Address: What It Really Is

Before you can design a VPC, you must understand IP addressing — because VPC design is fundamentally about choosing and dividing IP address ranges. The video covers **IPv4** specifically.

What you see when you run `ipconfig` (Windows) or `ifconfig` (Linux) — something like `192.168.1.74` — is the **decimal representation** of a **32-bit binary number**. The actual IP address is a sequence of 32 ones and zeros, divided into four groups of 8 bits each. Each 8-bit group is called an **octet** (because it contains eight binary digits).

```
192      .  168      .  1        .  74
11000000 .  10101000 .  00000001 .  01001010
 octet 1     octet 2    octet 3    octet 4
```

8 + 8 + 8 + 8 = 32 bits total. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

**Why each octet maxes out at 255:** The largest 8-bit binary number is `11111111`. Convert that to decimal: 128+64+32+16+8+4+2+1 = **255**. The smallest is `00000000` = **0**. So each octet ranges from 0 to 255, and the entire IPv4 range spans from `0.0.0.0` to `255.255.255.255`. You will never see an IP address with any octet above 255 — it's physically impossible in 8-bit binary.

Understanding that IP addresses are binary numbers is not academic trivia — it's essential for understanding subnet masks and CIDR notation, which are the tools you use to design VPC networks.

***

## 1.4 — Public vs Private IP Ranges

The entire IPv4 address space is divided into two categories: **public IPs** (used on the internet — every device on the internet has a unique public IP) and **private IPs** (used within local/internal networks — not routable on the internet).

When you create a VPC, you're creating a private network, so you use **private IP ranges**. Three classes of private IP ranges are defined:

| Class       | Start         | End               | Fixed Octets               | Variable Octets       |
| ----------- | ------------- | ----------------- | -------------------------- | --------------------- |
| **Class A** | `10.0.0.0`    | `10.255.255.255`  | 1st                        | 2nd, 3rd, 4th         |
| **Class B** | `172.16.0.0`  | `172.31.255.255`  | 1st, partially 2nd (16–31) | 2nd (16–31), 3rd, 4th |
| **Class C** | `192.168.0.0` | `192.168.255.255` | 1st, 2nd                   | 3rd, 4th              |

**How to identify which class an IP belongs to:** Look at where it falls in these ranges. `10.16.251.20` → Class A. `172.20.4.12` → Class B (first octet 172, second octet 20 which is between 16 and 31). `192.168.1.74` → Class C. An IP like `107.23.25.65` falls **outside** all private ranges — it's a **public IP**. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

Classes D and E also exist (for multicast and research), but they are not used in network design for VPC. When designing a VPC network, you select from Class A, B, or C based on how many IP addresses you need, then divide the chosen range into smaller subnets.

***

## 1.5 — Subnet Masks: The Network/Host Boundary Decider

An IP address alone tells you the address of a specific network interface. But it doesn't tell you **which part of that address identifies the network** and **which part identifies the individual host** within that network. That's the job of the **subnet mask**.

The subnet mask determines:

* Where the network's IP range **starts** (network address)
* Where it **ends** (broadcast address)
* How many IP addresses exist in the range
* Which IPs are **usable** (assignable to devices)
* What is the **network part** vs the **host part** of the address

**The street/house analogy from the video:** Think of the network part as the **street address** — it stays the same for everyone on that street. The host part is the **house number** — it's unique for each house on the street. The subnet mask tells you where the street name ends and the house number begins. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

**The three classful subnet masks:**

| Subnet Mask     | Binary                                | Full Octets     | Meaning                             |
| --------------- | ------------------------------------- | --------------- | ----------------------------------- |
| `255.0.0.0`     | `11111111.00000000.00000000.00000000` | 1st octet fixed | 1st octet = network, 2nd–4th = host |
| `255.255.0.0`   | `11111111.11111111.00000000.00000000` | 1st–2nd fixed   | 1st–2nd = network, 3rd–4th = host   |
| `255.255.255.0` | `11111111.11111111.11111111.00000000` | 1st–3rd fixed   | 1st–3rd = network, 4th = host       |

**How to read it:** Wherever the subnet mask has `255` (all ones in binary), that octet is the **network part** — it cannot change. Wherever the subnet mask has `0` (all zeros in binary), that octet is the **host part** — it varies to create individual IP addresses.

***

## 1.6 — Worked Example: Class C with Subnet Mask `255.255.255.0`

The video uses the instructor's own IP: `192.168.0.74` with subnet mask `255.255.255.0`.

Since the first three octets are full (255.255.255), the network part is `192.168.0` — this cannot change. The fourth octet (currently 74) is the host part — it ranges from 0 to 255.

**Derived values:**

| Property                    | Value           | Explanation                                                                                      |
| --------------------------- | --------------- | ------------------------------------------------------------------------------------------------ |
| First IP (Network Address)  | `192.168.0.0`   | Host part = 0. **Reserved** — identifies the network itself. Cannot be assigned to any device.   |
| First Usable IP             | `192.168.0.1`   | First assignable address                                                                         |
| Last Usable IP              | `192.168.0.254` | Last assignable address                                                                          |
| Last IP (Broadcast Address) | `192.168.0.255` | Host part = max. **Reserved** — used to send data to ALL devices on this network simultaneously. |
| Total IPs                   | 256             | 0 through 255                                                                                    |
| Usable IPs                  | 254             | Total minus 2 (network + broadcast)                                                              |

The **two reserved addresses** are a universal rule: in any subnet, the **first IP** is always the network address and the **last IP** is always the broadcast address. Neither can be assigned to a device. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

> 🔍 **Deep Dive**
> The DHCP server (running on your WiFi router, for example) is given the subnet mask and network range. It then automatically assigns IPs from the usable range to devices that connect. The instructor's IP (`192.168.0.74`) was assigned by DHCP from this range. The DHCP server itself knows not to assign `.0` (network) or `.255` (broadcast).

***

## 1.7 — Worked Example: Class B with Subnet Mask `255.255.0.0`

IP: `172.16.12.36`, Subnet mask: `255.255.0.0`.

First two octets are network (fixed at `172.16`). Third and fourth octets are host — **both** can vary from 0 to 255.

| Property                    | Value                  |
| --------------------------- | ---------------------- |
| First IP (Network Address)  | `172.16.0.0`           |
| First Usable IP             | `172.16.0.1`           |
| Last Usable IP              | `172.16.255.254`       |
| Last IP (Broadcast Address) | `172.16.255.255`       |
| Total IPs                   | 256 × 256 = **65,536** |
| Usable IPs                  | 65,534                 |

**How the host part cycles:** The fourth octet cycles 0→255, then the third octet increments by 1 and the fourth restarts: `172.16.0.0` → `172.16.0.1` → ... → `172.16.0.255` → `172.16.1.0` → `172.16.1.1` → ... → `172.16.1.255` → `172.16.2.0` → ... all the way to `172.16.255.255`. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

This is a huge network (65,536 IPs). You wouldn't use it as a single flat network — you'd divide it into **smaller subnets**. For example, using `255.255.255.0` as the subnet mask for each subnet, you can carve out 256 subnets of 256 IPs each: `172.16.0.0/24`, `172.16.1.0/24`, `172.16.2.0/24`, etc.

***

## 1.8 — Worked Example: Class A with Subnet Mask `255.0.0.0`

IP: `10.23.12.56`, Subnet mask: `255.0.0.0`.

Only the first octet is network (fixed at `10`). The remaining three octets are all host.

| Property  | Value                            |
| --------- | -------------------------------- |
| First IP  | `10.0.0.0`                       |
| Last IP   | `10.255.255.255`                 |
| Total IPs | 256 × 256 × 256 = **16,777,216** |

This is an enormous address space — and you'd always divide it into much smaller subnets for practical use. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

## 1.9 — CIDR Notation: The Modern Shorthand

In traditional networking, you write the full subnet mask: `255.255.255.0`. In cloud computing and virtualization, the same information is expressed using **CIDR notation** (Classless Inter-Domain Routing).

CIDR notation works by counting the number of **1-bits** in the binary representation of the subnet mask and expressing it as a slash followed by that count:

| Subnet Mask     | Binary                                | Count of 1s | CIDR  |
| --------------- | ------------------------------------- | ----------- | ----- |
| `255.0.0.0`     | `11111111.00000000.00000000.00000000` | 8           | `/8`  |
| `255.255.0.0`   | `11111111.11111111.00000000.00000000` | 16          | `/16` |
| `255.255.255.0` | `11111111.11111111.11111111.00000000` | 24          | `/24` |

So when you see `172.20.0.0/16`, you should instantly understand: the first 16 bits (first two octets) are the network part, the remaining 16 bits (last two octets) are the host part. This is equivalent to subnet mask `255.255.0.0`. When you see `/24`, you know: first three octets are network, last octet is host. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

CIDR notation is what you'll use exclusively in AWS VPC configuration. You won't type `255.255.255.0` — you'll type `/24`.

> 🔍 **Deep Dive**
> CIDR is called "classless" because the slash number doesn't have to align with class boundaries. You can have `/20`, `/18`, `/28` — values that don't correspond to any traditional class. This gives much finer control over network size. For example, `/28` gives you only 16 IPs (14 usable) — perfect for a tiny management subnet. The video mentions that if you encounter non-standard CIDR values and aren't confident calculating them manually, online subnet calculators are readily available. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

## 1.10 — Dividing Networks into Subnets

The video demonstrates the practical pattern of taking a large network and carving it into smaller subnets. Starting with `172.20.0.0/16` (65,536 IPs), you can create `/24` subnets within it:

* `172.20.0.0/24` — first subnet (256 IPs, 254 usable)
* `172.20.1.0/24` — second subnet
* `172.20.2.0/24` — third subnet
* ... up to 256 subnets total

Each subnet is an independent network segment. In a VPC context, different subnets can be placed in different availability zones, have different routing rules (public vs private), and serve different purposes (front-end, back-end, database, management).

The key skill the video emphasizes: given an IP address and a CIDR notation, you should be able to determine the first IP, last IP, total IPs, network part, host part, and usable range. If you can do this, **VPC setup becomes straightforward** — because VPC design is fundamentally about choosing and subdividing IP ranges. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

## 1.11 — Online Subnet Calculators

For non-standard CIDR values (like `/20`, `/18`, `/28`) where manual calculation is less intuitive, the video recommends using **online subnet calculators**. You input an IP address and CIDR notation, and the calculator returns: subnet mask, wildcard mask (the inverse of subnet mask — tells you about host addresses), network address, broadcast address, first usable IP, last usable IP, total IPs, and the IP class. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

This lecture is **conceptual preparation**, not a hands-on VPC build. We are building the **networking knowledge foundation** required to design and create VPCs in subsequent lectures. The final operational outcome: you will be able to look at any IP address with a CIDR notation and immediately determine the network range, usable IPs, network address, broadcast address, and how to subdivide the range into subnets. This skill directly translates into VPC subnet design on AWS.

***

## Step 1 — Identify IP Class from an Address

Given any IP address, determine whether it's a private or public IP, and which class it belongs to.

**Method:** Compare the IP against the three private ranges:

```
Class A:  10.0.0.0    –  10.255.255.255
Class B:  172.16.0.0  –  172.31.255.255
Class C:  192.168.0.0 –  192.168.255.255
```

**Practice examples from the video:**

| IP Address     | Class           | Reasoning                                       |
| -------------- | --------------- | ----------------------------------------------- |
| `10.16.251.20` | Class A Private | First octet is 10                               |
| `172.16.25.10` | Class B Private | First octet 172, second octet 16 (within 16–31) |
| `172.20.4.12`  | Class B Private | First octet 172, second octet 20 (within 16–31) |
| `192.168.0.74` | Class C Private | First two octets 192.168                        |
| `107.23.25.65` | **Public**      | Does not fall in any private range              |

 [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

**Common mistake:** Assuming any IP starting with `172` is Class B. It's only Class B if the second octet is between **16 and 31**. `172.32.x.x` is **not** a private Class B IP.

***

## Step 2 — Apply a Subnet Mask to Determine Network Properties

Given an IP and subnet mask, derive all network properties.

### Example A — Class C

**Given:** IP `192.168.0.74`, Subnet mask `255.255.255.0`

**Process:**

1. Identify fixed octets: 1st, 2nd, 3rd (all 255) → Network part: `192.168.0`
2. Identify variable octet: 4th (0) → Host part ranges 0–255
3. Calculate:

```
Network Address:     192.168.0.0     (host part = 0, RESERVED)
First Usable IP:     192.168.0.1
Last Usable IP:      192.168.0.254
Broadcast Address:   192.168.0.255   (host part = max, RESERVED)
Total IPs:           256
Usable IPs:          254             (256 - 2)
```

 [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

### Example B — Class B

**Given:** IP `172.16.12.36`, Subnet mask `255.255.0.0`

**Process:**

1. Fixed octets: 1st, 2nd → Network part: `172.16`
2. Variable octets: 3rd, 4th → Both range 0–255
3. Calculate:

```
Network Address:     172.16.0.0      (RESERVED)
First Usable IP:     172.16.0.1
Last Usable IP:      172.16.255.254
Broadcast Address:   172.16.255.255  (RESERVED)
Total IPs:           256 × 256 = 65,536
Usable IPs:          65,534
```

**How to verify the last usable IP:** The broadcast is `172.16.255.255`. Subtract one from the last octet: `172.16.255.254`. That's the last usable. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

### Example C — Class A

**Given:** IP `10.23.12.56`, Subnet mask `255.0.0.0`

```
Network Address:     10.0.0.0
First Usable IP:     10.0.0.1
Last Usable IP:      10.255.255.254
Broadcast Address:   10.255.255.255
Total IPs:           256 × 256 × 256 = 16,777,216
Usable IPs:          16,777,214
```

 [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

## Step 3 — Convert Subnet Masks to CIDR Notation

**Method:** Convert the subnet mask to binary, count the number of `1` bits.

**Conversion table:**

```
255.0.0.0       →  11111111.00000000.00000000.00000000  →  8 ones   →  /8
255.255.0.0     →  11111111.11111111.00000000.00000000  →  16 ones  →  /16
255.255.255.0   →  11111111.11111111.11111111.00000000  →  24 ones  →  /24
```

**Practical usage:** In AWS VPC configuration, you'll write `172.20.0.0/16` instead of specifying IP `172.20.0.0` with subnet mask `255.255.0.0`. They mean exactly the same thing. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

## Step 4 — Divide a Network into Subnets

**Scenario from the video:** You have `172.20.0.0/16` (65,536 IPs). You want to create `/24` subnets within it.

**Process:**

Each `/24` subnet uses 256 IPs. Total available host bits in `/16` = 65,536. Number of `/24` subnets possible = 65,536 ÷ 256 = **256 subnets**.

**Resulting subnets:**

```
172.20.0.0/24    →  first subnet   (172.20.0.0 – 172.20.0.255)
172.20.1.0/24    →  second subnet  (172.20.1.0 – 172.20.1.255)
172.20.2.0/24    →  third subnet   (172.20.2.0 – 172.20.2.255)
...
172.20.255.0/24  →  256th subnet   (172.20.255.0 – 172.20.255.255)
```

Each subnet gets 256 total IPs (254 usable). In VPC design, each of these subnets could be placed in a different availability zone or serve a different purpose (public, private, database, etc.). [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

***

## Step 5 — Use an Online Subnet Calculator for Verification or Complex CIDR

When you encounter non-standard CIDR values (like `/20`, `/18`, `/28`) or want to verify your manual calculation:

1. Google **"online subnet calculator"**.
2. Enter the IP address and CIDR notation.
3. The calculator returns: subnet mask, wildcard mask, network address, broadcast address, first usable, last usable, total IPs, IP class.

**Video example:** IP `172.20.16.54/16` → Calculator confirms Class B, shows network `172.20.0.0`, broadcast `172.20.255.255`, and all derived values. [\[263-vpc-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/263-vpc-introduction.txt)

> ⚠️ **Expert Note**
> The video emphasizes strongly: **if you understand IP addressing and subnetting, VPC setup becomes very easy.** If you don't, VPC will be confusing. This is the prerequisite knowledge. The video recommends re-watching the basics of networking lecture if any of this is unclear, and practicing with the subnet calculator until the calculations feel natural.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## VPC — Core Identity

```
VPC = Your own private network inside AWS (per region)
    = Logical data center you design and control
    = Network layout FIRST → then launch infrastructure inside it

Default VPC exists per region → custom VPC = more control

Setup sequence: Design network → Create VPC → Subnets → Routing → Security → Launch resources
```

***

## Historical Evolution

```
Corporate Data Center (full network control)
        ↓
EC2 Classic (compute only, no network control)
        ↓
VPC (full network control restored, but in the cloud)
```

***

## IPv4 Address Structure

```
192     .  168     .  0       .  74
XXXXXXXX . XXXXXXXX . XXXXXXXX . XXXXXXXX    ← 32 bits total
 octet 1    octet 2   octet 3    octet 4

Each octet: 8 bits → range 0–255
Min: 00000000 = 0
Max: 11111111 = 255

Total IPv4 range: 0.0.0.0 → 255.255.255.255
```

***

## Private IP Ranges (for VPC Design)

```
Class A:  10.0.0.0      –  10.255.255.255       1 fixed octet
Class B:  172.16.0.0    –  172.31.255.255        1.5 fixed octets (2nd: 16–31)
Class C:  192.168.0.0   –  192.168.255.255       2 fixed octets

Anything outside these = PUBLIC IP

Class D/E = research/multicast, not used in VPC
```

***

## Subnet Mask → Network/Host Boundary

```
Subnet Mask         Binary                                    CIDR    Network Part    Host Part
255.0.0.0           11111111.00000000.00000000.00000000       /8      1st octet       2nd–4th
255.255.0.0         11111111.11111111.00000000.00000000       /16     1st–2nd         3rd–4th
255.255.255.0       11111111.11111111.11111111.00000000       /24     1st–3rd         4th only

RULE: 255 (all 1s) = NETWORK (fixed, cannot change)
      0   (all 0s) = HOST    (variable, generates IP range)
```

***

## CIDR Notation — Quick Conversion

```
CIDR = count of 1-bits in subnet mask binary

/8  = 255.0.0.0         (8 ones)
/16 = 255.255.0.0       (16 ones)
/24 = 255.255.255.0     (24 ones)

AWS uses CIDR exclusively: 172.20.0.0/16, not 172.20.0.0 mask 255.255.0.0
```

***

## Universal IP Range Derivation Formula

```
Given: IP + Subnet Mask (or CIDR)

1. Identify NETWORK part (fixed octets) vs HOST part (variable octets)
2. Network Address    = network part + all HOST octets set to 0         ← RESERVED
3. Broadcast Address  = network part + all HOST octets set to 255       ← RESERVED
4. First Usable IP    = Network Address + 1
5. Last Usable IP     = Broadcast Address - 1
6. Total IPs          = 256^(number of host octets)
7. Usable IPs         = Total - 2
```

***

## Quick Reference — Sizes

```
/24  →  1 host octet   →  256 IPs     →  254 usable
/16  →  2 host octets  →  65,536 IPs  →  65,534 usable
/8   →  3 host octets  →  16,777,216  →  16,777,214 usable
```

***

## Subnetting — Division Pattern

```
Large Network: 172.20.0.0/16 (65,536 IPs)
        ↓ divide into /24 subnets
172.20.0.0/24     ← subnet 1 (256 IPs)
172.20.1.0/24     ← subnet 2
172.20.2.0/24     ← subnet 3
...
172.20.255.0/24   ← subnet 256

Total /24 subnets from /16 = 256
Each: 254 usable IPs

VPC APPLICATION: each subnet → different AZ / different purpose (public/private/DB)
```

***

## Reserved Addresses — Always Two Per Subnet

```
FIRST IP  = Network Address   (identifies the network)    → CANNOT assign
LAST IP   = Broadcast Address (reaches all hosts on net)   → CANNOT assign

Usable = Total - 2    ← ALWAYS
```

***

## Octet Cycling Behavior (Multi-Octet Host Range)

```
For /16 (2 host octets):
  172.16.0.0 → 172.16.0.1 → ... → 172.16.0.255
                                         ↓
  172.16.1.0 → 172.16.1.1 → ... → 172.16.1.255
                                         ↓
  172.16.2.0 → ... → 172.16.255.255

4th octet cycles 0→255, then 3rd octet increments
Like an odometer: rightmost digit rolls over, next digit ticks up
```

***

## Diagnostic Decision Tree

```
Given an IP:
  ├── In 10.x.x.x?           → Class A Private
  ├── In 172.16–31.x.x?      → Class B Private
  ├── In 192.168.x.x?        → Class C Private
  └── None of the above?     → Public IP

Given CIDR:
  ├── /8   → 1 network octet, 3 host octets
  ├── /16  → 2 network octets, 2 host octets
  ├── /24  → 3 network octets, 1 host octet
  └── Other (/20, /28, etc.) → Use subnet calculator or binary math
```

***

## Prerequisite Chain for VPC

```
Binary numbers → IPv4 structure → Public vs Private ranges → Subnet masks
     → CIDR notation → Network/Host identification → Subnetting
          → VPC design (next lecture)

THIS LECTURE = everything before "VPC design"
If this is solid → VPC setup is straightforward
```

***

## Tools

```
ipconfig / ifconfig     → view your own IP and subnet mask
Online subnet calculator → verify calculations for any IP/CIDR combo
    Input: IP + CIDR
    Output: subnet mask, wildcard, network addr, broadcast, first/last usable, total IPs, class
```

***

This completes the full reconstruction. Theory builds progressive understanding from binary to subnetting, Practical provides the calculation procedures you'll apply during VPC design, and the Compression Map enables instant recall of ranges, formulas, and relationships. This is the foundation for the VPC creation lectures that follow. Let me know if you'd like AnkiDeck cards generated from this, or if you're ready for the next lecture! 🚀
