# Bastion Host — Deep Learning Material

**Source:** [272-bastion-host.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt?EntityRepresentationId=d5f639b3-eeb2-4776-aa9f-079392eb60bf) (VTT Caption File) [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Is a Bastion Host?

A bastion host — also called a **jump server** — is a dedicated, hardened instance placed in a **public subnet** that serves as the **sole gateway** for administrators to reach resources inside **private subnets**. This is not an AWS-specific or VPC-specific term; it is a **general networking concept** applicable to any secure network architecture. Wherever you have resources intentionally isolated from the internet (private subnets, internal networks), a bastion host is the controlled entry point through which authorized humans access those resources. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

The reason a bastion host exists comes from a fundamental networking reality: any resource placed inside a private subnet **cannot be accessed directly from the internet** — for two independent reasons. First, a private subnet instance **does not receive a public IP address**, so there is no internet-routable address to connect to. Second, even if you hypothetically assigned a public IP to a private-subnet instance, the **route table of a private subnet does not have a route to an Internet Gateway**, so inbound traffic from the internet simply cannot reach it. Both conditions independently block access. The bastion host solves this by living in the public subnet (which has internet connectivity), and from there, you initiate a **second hop** into the private subnet. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

The critical mental model here is **two-hop SSH chaining**: you SSH from your local machine to the bastion host (hop 1 — internet → public subnet), and then from the bastion host you SSH to the private-subnet instance (hop 2 — public subnet → private subnet). Your local machine never directly touches the private resource. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

### The Fort Analogy

The instructor uses a powerful analogy: think of your VPC as a **fort**. All your valuable resources (databases, application servers, sensitive workloads) are safely inside the fort walls (private subnets). The bastion host is the **single door** of that fort. Everything inside is protected — but only as long as the door is strong and well-guarded. If the door is weak or unguarded, the entire fort is compromised regardless of how strong the walls are. This analogy encodes a deep security principle: **the security of your entire private infrastructure is only as strong as the security of your bastion host**. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

> 🔍 **Deep Dive**
> The "single point of entry" characteristic is both a strength and a risk. It is a strength because it creates a **choke point** — all administrative access funnels through one controlled location, which means you only need to harden, monitor, and audit one entry point. It is a risk because if this single point is compromised, an attacker gains a foothold into the entire private network. This is why bastion hosts receive disproportionate security attention compared to other instances. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## 1.2 Security Group — VPC-Scoped Access Control

A security group in AWS acts as a **virtual firewall** at the instance level. The critical concept emphasized in this lecture is that **security groups are VPC-specific**. A security group created inside VPC-A cannot be attached to an instance inside VPC-B. This is an architectural boundary enforced by AWS. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

For the bastion host, the security group has a single, tightly scoped rule: **allow SSH (port 22) only from a specific IP** — specifically "My IP" (the administrator's current public IP). In a production environment, this IP would be your **corporate office network's public IP**, meaning only people physically or VPN-connected to the corporate network can SSH to the bastion host. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

The engineering reasoning is simple: the bastion host is the door of the fort. The security group rule decides **who is allowed to even approach the door**. Setting it to "Anywhere" (0.0.0.0/0) is like leaving the fort door open to the world — anyone can try to break in. Setting it to a specific corporate IP is like posting guards who only let recognized personnel approach. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

> ⚠️ **Expert Note**
> For learning environments, "Anywhere" can be used if connectivity issues arise, but this must **never** be done in production. In real-time setups, the source IP should be the static public IP of your corporate network. If your team works remotely, a VPN gateway IP would replace the office IP. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## 1.3 Key Pair — The Key to the Fort Door

The key pair (specifically the **private key** in `.pem` format) is the cryptographic credential used to SSH into the bastion host. The instructor explicitly calls this out: the private key is **"the key to open the door of your fort."** If someone obtains this key, they can access the bastion host, and from there, potentially reach everything inside the private subnets. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

This means the private key must be treated as an extremely sensitive secret. It should be stored securely, never shared carelessly, and access to it should be tightly controlled. Losing control of the key is equivalent to handing the fort's door key to an adversary. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

Together, the **security group** and the **key pair** form the two layers of bastion host security:

* Security group = **who can approach the door** (network-level access control)
* Key pair = **who can open the door** (authentication-level access control)

Both must be strong for the bastion to be secure. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## 1.4 AMI Hardening — Vulnerability-Tested Images

Beyond network rules and authentication, there is a **third security dimension**: the operating system itself. Every OS has known vulnerabilities. If the bastion host runs a default, unhardened AMI, those vulnerabilities become attack vectors. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

The instructor introduces **CIS (Center for Internet Security)** as a provider that sells AMIs on the AWS Marketplace. These are the **same base operating systems** (Amazon Linux 2, CentOS 7, Ubuntu, Windows) but they have been **scanned for known security vulnerabilities, patched, and hardened** according to CIS benchmarks. These AMIs come at a cost (the example mentioned is approximately $130/year), but for production bastion hosts protecting a secure VPC, this is a justified investment. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

For learning purposes, the lecture uses a **standard free-tier Ubuntu Server 22.04 AMI** from the Quickstart catalog to avoid costs. But the key takeaway is clear: in real-time production environments, always prefer vulnerability-tested AMIs for bastion hosts. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

> 🔍 **Deep Dive**
> The three layers of bastion host security form a **defense-in-depth model**:
>
> 1. **Network layer** — Security group restricts who can reach the bastion (IP-level filtering).
> 2. **Authentication layer** — Key pair restricts who can log in (cryptographic identity).
> 3. **OS layer** — Hardened AMI reduces the attack surface of the bastion itself (vulnerability patching).
>
> Each layer is independent. Even if one layer is somehow bypassed, the others still provide protection. This layered security approach is a core infrastructure engineering pattern. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## 1.5 VPC Validation Through the Bastion Host

A successful SSH connection to the bastion host is not just an operational achievement — it is a **validation event** for the entire public subnet configuration. If you can SSH in, it confirms: [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

* The **Internet Gateway** is attached and functional.
* The **route table** for the public subnet has a route to the IGW.
* **Auto-assign public IP** is enabled on the subnet (so the instance received a public IP).
* The **security group** allows inbound SSH from your IP.
* The **key pair** authentication is working.
* DNS resolution is functioning (public DNS name is resolvable).

This single test validates the entire chain of VPC public-subnet networking. If it fails, the problem is in one of these links. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## 1.6 Architectural Context — Where the Bastion Fits

The bastion host is being built inside an existing VPC called **vprofile-VPC**. This VPC already has: [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

* A **NAT Gateway** (confirmed by the existing elastic IP visible in the EC2 dashboard).
* **Public and private subnets** already configured.
* **Default security groups** auto-created during VPC creation (one for the default VPC, one for vprofile-VPC).
* **Auto-assign public IP** already enabled on the public subnets.

The bastion host is the next piece being added. The upcoming architecture (previewed at the end of the lecture) will involve launching instances in the **private subnet**, accessing them via the bastion host, setting up a **website** on the private instance, and exposing that website through a **load balancer**. The bastion host is the administrative entry point that enables all subsequent private-subnet operations. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are launching a **bastion host** — a hardened EC2 instance in the **public subnet** of our vprofile-VPC — that will serve as the sole SSH entry point into private-subnet resources. By the end of this process, we will SSH into the bastion host from our local machine, validating the entire public subnet networking stack. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Step 1: Verify Existing VPC Resources

Navigate to **AWS Console → EC2 Dashboard**. Before creating anything new, confirm the existing state of your VPC resources in the same region: [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

* **1 Elastic IP** — this belongs to the NAT Gateway created earlier. Its presence confirms the NAT Gateway is in place.
* **2 Security Groups** — these are the **default security groups** automatically created when VPCs are created. One belongs to the default VPC; the other belongs to vprofile-VPC.

This verification step ensures you are working in the correct region and that prior infrastructure is intact. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Step 2: Create a Security Group for the Bastion Host

Go to **EC2 → Security Groups → Create Security Group**.

| Field           | Value                                               |
| --------------- | --------------------------------------------------- |
| **Name**        | `vpro-bastion-sg`                                   |
| **Description** | `vpro-bastion-sg` (same as name)                    |
| **VPC**         | `vprofile-VPC` (**critical — change from default**) |

**Inbound Rule:**

| Type          | Source |
| ------------- | ------ |
| SSH (port 22) | My IP  |

Click **Create security group**. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

**Why this matters operationally:** The VPC selection is the most common mistake here. The console defaults to the **default VPC**. If you create the security group in the default VPC, you **will not be able to attach it** to an instance in vprofile-VPC later — security groups are VPC-scoped. Always confirm the VPC selection **twice** before creating. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

The SSH rule is set to "My IP" — AWS auto-detects your current public IP and restricts SSH access to only that address. In production, this would be replaced with your corporate/office network IP. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Step 3: Create a Key Pair

Go to **EC2 → Key Pairs → Create key pair**.

| Field      | Value              |
| ---------- | ------------------ |
| **Name**   | `vpro-bastion-key` |
| **Format** | `.pem`             |

Click **Create key pair**. The `.pem` file will automatically download to your machine. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

**Operational security:** This downloaded file is the **only copy** of the private key. AWS does not store it. If you lose it, you lose SSH access to any instance using this key pair. Store it in a secure location immediately. As discussed in Theory (§1.3), this key is the authentication credential for the fort's door. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Step 4: Choose the AMI

Go to **EC2 → Launch Instance**.

For **production** bastion hosts, navigate to **Browse more AMIs → AWS Marketplace** and search for **CIS**. You will find hardened versions of Amazon Linux 2, CentOS 7, Ubuntu, and Windows — tested and patched for security vulnerabilities by the Center for Internet Security. These come with a cost (e.g., \~$130/year). [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

For **learning purposes**, go to **Quickstart** and select:

| Field   | Value                                        |
| ------- | -------------------------------------------- |
| **AMI** | Ubuntu Server 22.04 LTS (Free tier eligible) |

The functional requirement is minimal — we only need to SSH into this instance. Any Linux AMI works. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Step 5: Configure and Launch the Instance

Fill in the launch configuration:

| Field             | Value                                  |
| ----------------- | -------------------------------------- |
| **Name**          | `bastion`                              |
| **Instance type** | `t2.micro` (free tier eligible)        |
| **Key pair**      | `vpro-bastion-key` (created in Step 3) |

**Network Settings** — click **Edit**:

| Field                     | Value                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------- |
| **VPC**                   | `vprofile-VPC`                                                                                |
| **Subnet**                | Public subnet (either public-1 or public-2)                                                   |
| **Auto-assign public IP** | Enabled (should already be enabled by default because we configured this during subnet setup) |
| **Security group**        | `vpro-bastion-sg` (select existing — created in Step 2)                                       |

Click **Launch instance**. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

**Operational checkpoints before launching:**

1. VPC is `vprofile-VPC`, not the default VPC.
2. Subnet is a **public** subnet — not a private one.
3. Auto-assign public IP shows **Enabled**.
4. Security group is `vpro-bastion-sg` — if you don't see it in the dropdown, you likely created it in the wrong VPC (go back to Step 2).

These four checks prevent the most common launch mistakes. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Step 6: Wait for Instance to Reach Running State

Monitor the instance in **EC2 → Instances**. Wait until:

* **Instance state** = `Running`
* A **Public IP** and **Public DNS name** are assigned and visible.

Only proceed to SSH once both conditions are met. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Step 7: SSH to the Bastion Host

Copy the **public IP** of the bastion instance from the EC2 console.

Open a terminal:

* **Windows**: Git Bash
* **macOS/Linux**: Terminal

Run the SSH command:

```bash
ssh -i <path-to-vpro-bastion-key.pem> ubuntu@<public-ip>
```

**Command breakdown:**

| Part                   | Meaning                                                          |
| ---------------------- | ---------------------------------------------------------------- |
| `ssh`                  | Invokes the SSH client to establish a secure shell connection    |
| `-i <path-to-key.pem>` | Specifies the **identity file** (private key) for authentication |
| `ubuntu`               | The default SSH username for Ubuntu AMIs                         |
| `@<public-ip>`         | The target host — the bastion's public IP address                |

On first connection, you will see a host authenticity prompt. Type **`yes`** to accept and add the bastion's fingerprint to your known\_hosts file. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

**Expected result:** You are dropped into the bastion host's shell. This confirms:

* The entire public subnet networking chain is functional (IGW → route table → subnet → security group → instance).
* Authentication via key pair is working.
* The bastion host is operational and ready to serve as a jump point to private subnet resources. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

**Common failures and debugging:**

| Symptom                                | Likely Cause                                                                                            |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Connection timeout                     | Security group doesn't allow SSH from your IP, or instance is in a private subnet, or no IGW route      |
| Permission denied (publickey)          | Wrong key file, wrong username (e.g., `ec2-user` instead of `ubuntu`), or key file permissions too open |
| No public IP visible                   | Auto-assign public IP was not enabled on the subnet, or instance is in a private subnet                 |
| Security group not found during launch | Security group was created in the wrong VPC                                                             |

> ⚠️ **Expert Note**
> On Linux/macOS, if SSH complains about key permissions being too open, run `chmod 400 vpro-bastion-key.pem` before retrying. SSH refuses to use a private key file that is readable by others. [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## What Comes Next

The bastion host is now operational. In the next lecture, the workflow extends to: [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

1. **Launching an instance in the private subnet.**
2. **SSH-ing from the bastion host into that private instance** (completing the two-hop chain).
3. **Setting up a website** on the private instance.
4. **Exposing the website through a load balancer** (so end users access the site without touching the private instance directly).

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
Bastion Host = Jump Server = Single controlled SSH entry point into private subnets
Not AWS-specific → General networking concept
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Why It Exists

```
Private Subnet Instance:
  ├── No public IP → unreachable from internet
  └── Even with public IP → no IGW route → still unreachable

∴ Need intermediary in public subnet → Bastion Host
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Access Flow (Two-Hop SSH Chain)

```
Local Machine ──SSH──► Bastion Host (public subnet) ──SSH──► Private Instance (private subnet)
     │                        │                                      │
  Internet               Hop 1 (internet → IGW → public)       Hop 2 (internal VPC routing)
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Fort Analogy (Security Mental Model)

```
VPC = Fort
Private Subnet Resources = Valuables inside the fort
Bastion Host = The single door

Door security = Entire fort security
Weak door → entire fort compromised
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Three-Layer Defense-in-Depth

```
Layer 1: NETWORK    → Security Group    → WHO can approach the door (IP restriction)
Layer 2: AUTH       → Key Pair (.pem)   → WHO can open the door (cryptographic identity)  
Layer 3: OS         → Hardened AMI (CIS)→ HOW strong the door itself is (vulnerability patching)

All three independent. Each protects even if another fails.
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Resource Creation Sequence

```
1. Security Group (vpro-bastion-sg)
   └── VPC: vprofile-VPC (NOT default!) ← most common mistake
   └── Rule: SSH from My IP only

2. Key Pair (vpro-bastion-key.pem)
   └── Download = only copy. Lose it = lose access.

3. EC2 Instance (bastion)
   ├── AMI: Ubuntu 22.04 (learning) | CIS-hardened (production)
   ├── Type: t2.micro
   ├── Network: vprofile-VPC → Public Subnet → Auto-assign public IP: Enabled
   └── SG: vpro-bastion-sg
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## VPC-Scoping Rule

```
Security Group ──scoped to──► VPC
  └── SG in VPC-A ≠ attachable to instance in VPC-B
  └── If SG not visible in dropdown → wrong VPC during creation
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## SSH Validation = Public Subnet Validation

```
Successful SSH to bastion confirms ENTIRE chain:
  IGW attached ✓
  Route table → IGW ✓  
  Public subnet auto-assign IP ✓
  Security group inbound rule ✓
  Key pair auth ✓
  DNS resolution ✓
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Failure Diagnosis Map

```
Timeout         → SG rule / wrong subnet (private) / no IGW route
Permission denied → wrong key / wrong username / key permissions too open
No public IP    → auto-assign disabled / private subnet
SG not found    → created in wrong VPC
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Existing Infrastructure Context

```
vprofile-VPC (pre-existing):
  ├── NAT Gateway (confirmed by elastic IP in dashboard)
  ├── Public subnets (auto-assign IP enabled)
  ├── Private subnets
  ├── Default SGs (auto-created with VPC)
  └── + Bastion Host ← [this lecture]

Next steps:
  ├── Private instance (accessed via bastion)
  ├── Website on private instance
  └── Load balancer → exposes website to internet
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

## Reusable Engineering Patterns

**Single Point of Entry (Choke Point) Pattern**

```
All access funneled through one controlled node
  Benefit: centralized hardening, monitoring, auditing
  Risk: single point of failure/compromise
  Mitigation: defense-in-depth (multiple independent security layers)
```

**Validation-by-Usage Pattern**

```
Testing the component simultaneously validates the entire dependency chain beneath it
  Bastion SSH test → validates IGW + route table + subnet config + SG + key pair + DNS
```

**VPC-Scoped Resource Binding**

```
Certain resources (SGs) are bound to their VPC at creation time
  Cannot cross VPC boundaries → must verify scope before creation
  Pattern recurs across AWS (subnets, route tables, NACLs, etc.)
```

 [\[272-bastion-host \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/272-bastion-host.txt)

***

This completes the full reconstruction. The three sections are designed to work together — **Theory** for deep understanding, **Practical** for confident execution, and the **Compression Map** for rapid future recall without re-reading the full material. Let me know if you'd like any section expanded or adjusted! 🚀
