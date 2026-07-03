# 🎓 Deep Learning Material: EC2 Instance Launch — Requirement Gathering, Key Pairs, Security Groups & Web Deployment

*Reconstructed from video captions — [114-more-in-ec2-part1.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt?EntityRepresentationId=4abdeb96-cfca-4a54-a2fc-447952d79fe0), with supporting commands from [114.morInEec2\_part1.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114.morInEec2_part1.txt?EntityRepresentationId=44707d4d-3f3c-4626-8d70-7279c2077972)* [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt), [\[114.morInEec2_part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114.morInEec2_part1.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The General Best Practice: A Structured Launch Process

The video opens with a critical operational principle: launching an EC2 instance is **not** a one-click action you improvise. It is a **structured process** with a specific order. The instructor presents four sequential phases: [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

1. **Gather the requirements** — understand what you need before touching AWS
2. **Create the key pair** — prepare your authentication mechanism
3. **Create the security group** — prepare your firewall rules
4. **Launch the instance** — execute the launch, selecting the pre-created key pair and security group during the process

This order exists because the launch wizard asks you to **select** a key pair and a security group. If you haven't created them beforehand, you'll be creating them inline under pressure, likely with poor naming, wrong settings, or defaults that compromise security. By front-loading these decisions, each component is created thoughtfully, with proper naming and correct configuration.

> ⚠️ **Expert Note:** The instructor acknowledges you *can* create a key pair during the launch process, but explicitly recommends doing it **before**. This is a process-discipline point — separating preparation from execution reduces errors and produces cleaner, more auditable infrastructure.

***

## 1.2 Requirement Gathering — What You Need to Know Before Launch

Before creating anything in AWS, you should collect specific information that drives every decision during the launch. The video lists these requirements: [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Operating System** → determines which **AMI** (Amazon Machine Image) you select. Ubuntu, Amazon Linux, CentOS, Windows — the AMI is the template for the machine's base OS.

**Size (RAM, CPU, network speed)** → determines the **instance type** (e.g., `t2.micro`). A development environment can use minimum resources; production may need significantly more. The instance type is the compute capacity you're paying for.

**Storage size** → determines the **EBS volume** configuration. Storage covers two things: the operating system itself, and any application or data that runs on the instance. The video uses 10 GB as an example for a lightweight use case.

**Project information** → used for **tagging**. Knowing which project this instance belongs to is essential for cost tracking, ownership identification, and organizational clarity.

**Services/applications that will run** → determines **security group rules**. If you know SSH, HTTP, and MySQL will run, you know you'll need ports 22, 80, and 3306 open. This directly feeds firewall configuration.

**Environment** → dev, QA, staging, pre-prod, production. This affects naming conventions, tagging, key pair assignment, and security group grouping. Many decisions differ by environment (dev can be more permissive; production must be locked down).

**Login user / owner** → used for tagging and tracking. Who is responsible for this instance? Who should be contacted if something goes wrong?

The instructor emphasizes: this is not an exhaustive list — "you could be doing less or more based on your requirements." But these are the **general baseline** for any EC2 launch. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.3 Key Pairs — Authentication Mechanism for SSH

A key pair in AWS consists of a **public key** (stored by AWS, attached to the instance) and a **private key** (downloaded to your computer at creation time). The public key is the "lock" placed on the instance; the private key is the "key" you hold to open that lock. When you SSH to the instance, your private key authenticates you against the public key on the instance. Without the matching private key, you cannot log in. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### Key Pair Scope and Granularity

**Key pairs are region-specific.** A key pair created in North Virginia (us-east-1) is only available in that region. If you have instances in different regions, you need separate key pairs per region. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Key pair assignment strategy** is an important design decision. The video presents three approaches and evaluates them:

* **One key for all instances** → ❌ Wrong. If the key is compromised, every instance is compromised.
* **One separate key per instance** → ❌ Wrong. With 100 instances, you'd have 100 keys to manage — operationally unmanageable.
* **One key per environment per region** → ✅ Correct. Group keys by environment (dev, QA, staging, production) and region. This balances security isolation with management simplicity. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### Key Format

**PEM format** — used with terminal/Git Bash (macOS, Linux, Windows Git Bash). This is the standard OpenSSH format.

**PPK format** — used with PuTTY (a Windows SSH client). If you use PuTTY, select PPK; otherwise, PEM. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### Private Key Lifecycle

When you create a key pair, the private key is downloaded **once**. AWS does not store it. If you lose it, you cannot recover it. If you delete the key pair in AWS, the public key is removed and the private key you downloaded becomes useless — it has no matching lock anymore. The video demonstrates this: deleting the old key pair and noting that the previously downloaded private key should also be deleted from your Downloads folder to avoid confusion. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.4 Security Groups — Virtual Firewalls for EC2

A security group is a **virtual firewall** that controls traffic to and from your EC2 instance. It is not a physical device — it's a set of rules that AWS enforces at the network level around your instance. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### Inbound vs. Outbound Rules

**Inbound rules** control traffic **coming toward** your instance — requests from the internet, from other servers, from users trying to access your services. Example: allowing SSH (port 22) or HTTP (port 80) traffic in.

**Outbound rules** control traffic **going out** from your instance — your instance reaching the internet, downloading packages, contacting other services. By default, outbound allows **all traffic to anywhere**, which enables your instance to access the internet for updates, package downloads, etc. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

The video uses an analogy: think of a security group as a **bouncer (watchman/gatekeeper) at a party**. The bouncer has a **register** (the rule list). When someone arrives (inbound traffic), the bouncer checks: are you on the list? Are you coming from an allowed location? If yes, you enter. If not, you're blocked. The same applies for people leaving (outbound traffic) — are they allowed to leave, and where are they going? [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### Stateful Behavior

Security groups are **stateful**. If you create an inbound rule allowing SSH on port 22, the corresponding outbound traffic for that SSH session is **automatically allowed** — you don't need to create a matching outbound rule. The "state" of the connection is tracked: if traffic was allowed in, the response is automatically allowed out. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### Security Group Granularity Strategy

The same principle as key pairs applies: [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

* **One security group for all instances** → ❌ Wrong. Different services need different ports; one group can't properly protect diverse workloads.
* **One security group per instance** → ❌ Wrong. Unmanageable at scale.
* **Divide by environment and service type** → ✅ Correct. All web servers in dev environment share one security group. All database servers in dev share another. This groups instances with identical access requirements.

### The Anti-Pattern: Allow All Traffic

The video shows what many people do when "things are not working" — they create rules that allow **all TCP** and **all traffic** from **any IPv4 and any IPv6**. The instructor explicitly warns: "I'm not kidding, but in some very sophisticated projects also I have seen these things." This effectively disables the firewall — "there are no gates, no doors, no windows. Anybody can come to the party." This is a severe security anti-pattern. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### Outbound Rule Warning

The instructor gives a firm directive about outbound rules: **"Do not touch outbound rule ever until unless I tell you to."** Modifying outbound rules can break internet connectivity for the instance — the instance won't be able to download packages, reach repositories, or communicate externally. In corporate environments, outbound traffic is typically routed through a **proxy server**, and outbound rules are restricted to the proxy's IP. But for this course's purposes, outbound must remain open to allow the instance to function. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

### The "Add Rules Only When Needed" Principle

The video teaches a specific operational discipline: **do not add security group rules in advance for services that aren't running yet.** When the instance is first launched, only SSH is needed (to log in and set things up). So only port 22 is added. Port 80 for HTTP is added **later**, only after the web service is actually installed and running. This principle — add rules as services come online — keeps the firewall as tight as possible at every point in time. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

> 🔍 **Deep Dive:** The `My IP` option in the SSH inbound rule source automatically fills in your current public IP address. In corporate networks, public IPs are typically **static** — they don't change. This restricts SSH access to only people sitting in that specific network. When working from home or dynamic IPs, this setting may need frequent updates, which is why some environments use VPNs or bastion hosts instead. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.5 Naming Conventions — An Operational Discipline

The video repeatedly emphasizes proper naming as a **non-negotiable practice**. The naming pattern demonstrated is: **`ProjectName-Environment-Region`** (for key pairs) and **`ProjectName-ServiceType`** (for security groups). [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

Examples from the video:

* Key pair: `moso-dev-virginia`
* Security group: `moso-web`

The instructor is blunt about ignoring naming conventions: "Trust me, it's a very, very bad practice. You're going to suffer a lot in real time due to this." The practical pain: imagine 50 security groups with generic names like `sg-1`, `sg-2`, `my-sg`. Finding the right one during an incident is impossible. Proper naming makes selection, auditing, and troubleshooting possible at scale. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.6 Network Interfaces — The Connection Between Instance and Security Group

When an EC2 instance is created, AWS also creates a **network interface** for it — the virtual equivalent of a physical network adapter (like a Wi-Fi adapter or ethernet adapter on your laptop). The security group rules are actually applied to this **network interface**, not directly to the instance. The network interface is then **attached** to the instance. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

This matters operationally when cleaning up: if you try to delete a security group that still has a network interface attached, AWS returns an error. You must first **detach** the network interface, then **delete** the network interface, and then delete the security group. The video demonstrates this cleanup sequence when removing the security group from the previous lecture. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.7 Tagging Strategy

The video applies four tags to the EC2 instance: **Name**, **Project**, **Environment**, and **Owner**. Additionally, the **resource types** checkbox is set to also tag **volumes** (storage) and **network interfaces** — so that these sub-resources can be traced back to which project, owner, and instance they belong to. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

The instructor notes: "I usually use these tags if no naming conventions are mentioned, but if naming conventions are mentioned, there is a standard in the organization, you better follow that." Tags serve multiple purposes: cost allocation (which project is spending how much), ownership tracking (who to contact), environment identification (is this prod or dev?), and general organizational clarity. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.8 Terminated State — Instance Lifecycle

The video references the previously deleted instance being in **terminated** state. Terminated means the instance is permanently gone — no recovery possible. However, AWS retains the terminated instance's **metadata** (name, ID, etc.) in the console for approximately **two hours** before it disappears entirely. During this time, if you select it, all state-change actions are grayed out — "you cannot do anything over here." [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.9 The Web Deployment Flow and the Security Group Gate

After the instance launches, the web server (Apache2) is installed, a website template is downloaded and deployed, and the service is running on port 80. But when the browser tries to access the instance's public IP, **it fails**. The reason: the security group only allows port 22 (SSH). Port 80 (HTTP) was deliberately not added earlier because the web service wasn't running yet. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

This is the **security group gate** in action — the firewall is doing exactly what it was configured to do: block all traffic except what's explicitly allowed. Only after adding port 80 to the inbound rules and saving does the website become accessible. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

The port 80 rule is allowed from **anywhere** (both IPv4 and IPv6), and the video addresses the apparent contradiction: earlier, allowing all traffic from anywhere was called a bad practice. But for a **public website**, allowing HTTP from anywhere is correct — the whole point is that the public can access it. The "from anywhere" restriction applies to management ports like SSH, not to public service ports like HTTP. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## 1.10 How the Template Download URL Is Obtained

The video demonstrates a specific technique for getting the direct download URL of a website template from tooplate.com: open the browser's developer tools (F12), switch to the **Network tab**, click the Download button on the website, and inspect the request — the **Request URL** in the headers contains the direct `.zip` URL that can be used with `wget` on the server. The instructor recommends **Brave browser** to avoid excessive ads on the template site. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are launching a properly configured EC2 instance following best practices: creating a named key pair, creating a named security group with minimal initial rules, launching an Ubuntu instance with proper tags, SSHing in, installing Apache2, deploying a website template, and then opening port 80 in the security group to make the website publicly accessible. The final outcome: a properly tagged, properly secured, publicly accessible web server on AWS. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

## Phase 1: Preparation — Key Pair and Security Group

### Step 1 — Delete the Old Key Pair

**What we are doing:** Cleaning up the key pair from the previous lecture to start fresh.

Navigate to **EC2 → Network and Security → Key Pairs**.

Select the existing key pair → **Actions → Delete**. Type `Delete` (capital D) to confirm. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Important:** Also go to your local **Downloads folder** and delete the previously downloaded `.pem` file. The public key in AWS is gone, so the private key is now useless. Keeping it creates confusion about which keys are valid.

***

### Step 2 — Create a New Key Pair with Proper Naming

Click **Create key pair**.

**Name:** `moso-dev-virginia` [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Naming breakdown:**

* `moso` — project name (the template selected from tooplate.com)
* `dev` — environment (development)
* `virginia` — region (North Virginia / us-east-1)

**Key pair type:** RSA (default)

**Private key file format:** `.pem` (for terminal/Git Bash). Select `.ppk` only if using PuTTY.

**Tags:** Add a Name tag with the same value: `moso-dev-virginia`.

Click **Create key pair**.

**What happens:** The private key (`.pem` file) is automatically downloaded to your computer. This is a **one-time download** — AWS does not store the private key. The public key is stored in AWS and will be injected into any instance that selects this key pair.

**Connection to flow:** The key pair is ready. It will be selected during instance launch.

***

### Step 3 — Delete the Old Security Group

Navigate to **EC2 → Network and Security → Security Groups**.

Select the old security group → **Actions → Delete Security Group** → confirm. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**If you get an error** ("cannot delete — network interface attached"):

1. Go to **Network and Security → Network Interfaces**
2. Select the lingering network interface
3. **Actions → Detach** first
4. Then **Actions → Delete** the network interface
5. Go back to Security Groups and delete again

**Why this happens:** The terminated instance left behind its network interface, which still references the security group. AWS won't delete a security group that's still attached to anything. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

### Step 4 — Create a New Security Group with Proper Naming

Click **Create security group**.

**Name:** `moso-web` [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Naming breakdown:**

* `moso` — project name
* `web` — service type (this group is for web servers)

**Description:** Provide a meaningful description.

**Inbound Rules — Add only SSH for now:**

| Type | Protocol | Port | Source                                    |
| ---- | -------- | ---- | ----------------------------------------- |
| SSH  | TCP      | 22   | My IP (auto-fills your current public IP) |

**Do NOT add port 80 yet.** No web service is running, so no HTTP rule is needed. Rules are added when services come online — not before. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Outbound Rules:** Leave as default — **All traffic, All ports, Destination: Anywhere (0.0.0.0/0)**. Do not modify outbound rules — changing them breaks internet connectivity for the instance.

**Tags:** Add Name tag: `moso-web`.

Click **Create security group**.

**Connection to flow:** The security group is ready. It will be selected during instance launch.

***

## Phase 2: Launch the Instance

### Step 5 — Launch Instance with Proper Configuration

Navigate to **EC2 → Instances → Launch Instances**. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Tags (apply four):**

| Key         | Value            |
| ----------- | ---------------- |
| Name        | web01            |
| Project     | moso             |
| Environment | dev              |
| Owner       | (your name/team) |

**Resource types:** Check boxes to also apply tags to **Volumes** and **Network Interfaces**. This ensures sub-resources are traceable to the project and owner. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**AMI:** Ubuntu Server 24 (latest, Free Tier eligible). Select the default one.

**Instance type:** `t2.micro` (Free Tier eligible).

**Key pair:** Select `moso-dev-virginia` from the dropdown. The proper naming makes this selection obvious and unambiguous.

**Network settings → Edit:**

* **Security group:** Select existing → choose `moso-web` from the dropdown. Again, proper naming makes this easy even among many security groups.

**Storage:** Keep default (covered in later lectures).

**Advanced Details (User Data):** Leave empty. No user data script this time — we will SSH in and execute commands manually. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

Click **Launch instance**.

**Connection to flow:** The instance is now launching with proper key, proper security group, and proper tags. Next: SSH in.

***

## Phase 3: SSH and Web Server Setup

### Step 6 — SSH into the Instance

Wait for the instance state to show **Running**. Select the instance and copy its **Public IP address**.

```bash
ssh -i ~/Downloads/moso-dev-virginia.pem ubuntu@<PUBLIC_IP>
```

**Breakdown:**

* `ssh` — SSH client
* `-i ~/Downloads/moso-dev-virginia.pem` — specifies the private key file. `-i` = identity file. Path points to the downloaded `.pem` key.
* `ubuntu` — the default login username for official Ubuntu AMIs. (Amazon Linux uses `ec2-user`, CentOS uses `centos` — each AMI has its own default user.)
* `@<PUBLIC_IP>` — the instance's public IP address [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**First-time prompt:** "Are you sure you want to continue connecting?" → Type `yes`.

**Switch to root:**

```bash
sudo -i
```

***

### Step 7 — Install Apache2 and Dependencies

```bash
apt update && apt install apache2 wget unzip -y
```

**Breakdown:**

* `apt update` — refreshes the package index (required before installing anything on Ubuntu)
* `&&` — run the next command only if the previous one succeeds
* `apt install apache2 wget unzip -y` — installs three packages: `apache2` (the web server), `wget` (for downloading files via URL), `unzip` (for extracting zip archives). `-y` auto-confirms [\[114.morInEec2_part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114.morInEec2_part1.txt)

**Expected behavior on Ubuntu:** When you install Apache2, it automatically starts and enables itself. No need for `systemctl start` or `systemctl enable`.

**Verification:**

```bash
systemctl status apache2
```

**Expected output:** `active (running)`. Press `q` to quit the status view. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

***

### Step 8 — Get the Template Download URL

**On your local browser** (Brave recommended to avoid ads), go to **tooplate.com**, select your template (Moso in this case). [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

1. Press **F12** to open Developer Tools
2. Switch to the **Network** tab
3. Click the **Download** button on the template page
4. In the Network tab, click on the `.zip` request
5. In the **Headers** section, find the **Request URL**
6. Copy this URL

This gives you the direct download link (e.g., `https://www.tooplate.com/zip-templates/2128_tween_agency.zip`).

***

### Step 9 — Download and Deploy the Template

**Back in the SSH session (as root):**

```bash
wget https://www.tooplate.com/zip-templates/2128_tween_agency.zip
```

**Breakdown:**

* `wget` — downloads a file from a URL to the current directory [\[114.morInEec2_part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114.morInEec2_part1.txt)

```bash
unzip 2128_tween_agency.zip
```

**Breakdown:**

* `unzip` — extracts the zip archive into a folder of the same name

```bash
sudo cp -r 2128_tween_agency/* /var/www/html/
```

**Breakdown:**

* `cp -r` — copy recursively (all files and subdirectories)
* `2128_tween_agency/*` — everything inside the extracted template folder
* `/var/www/html/` — Apache2's default document root. Files placed here are served by the web server [\[114.morInEec2_part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114.morInEec2_part1.txt)

```bash
sudo systemctl restart apache2
```

**Breakdown:**

* Restarts Apache2 to ensure it picks up the new content cleanly [\[114.morInEec2_part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114.morInEec2_part1.txt)

**Verification — confirm the service is running and the port:**

```bash
ss -tunlp | grep <apache2_PID>
```

**Breakdown:**

* `ss -tunlp` — shows listening sockets. `-t` = TCP, `-u` = UDP, `-n` = numeric ports, `-l` = listening only, `-p` = show process
* `| grep <PID>` — filters output to show only Apache's entries [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Expected output:** Apache is listening on port **80** from all interfaces (0.0.0.0:80).

***

### Step 10 — Attempt Browser Access (Expected Failure)

In your browser, enter: `http://<PUBLIC_IP>`

**Expected result:** **Connection timeout / cannot reach.** [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Why:** The security group only allows port 22 (SSH). Port 80 (HTTP) is blocked. The firewall is doing its job — the web server is running, but the network gate is closed.

***

### Step 11 — Add HTTP Rule to Security Group

Go to **EC2 → select the running instance → Security tab → click the security group link → Edit inbound rules**. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**Add two rules:**

| Type | Protocol | Port | Source                    |
| ---- | -------- | ---- | ------------------------- |
| HTTP | TCP      | 80   | Anywhere-IPv4 (0.0.0.0/0) |
| HTTP | TCP      | 80   | Anywhere-IPv6 (::/0)      |

**Why from anywhere?** This is a **public website**. The whole purpose is for anyone on the internet to access it. Allowing HTTP from anywhere is correct for public-facing web services. The "don't allow from anywhere" rule applies to management ports (SSH), not to public service ports (HTTP). [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

Click **Save rules**.

***

### Step 12 — Verify Website Access

Refresh the browser at `http://<PUBLIC_IP>`.

**Expected result:** The website template (Moso) loads correctly. [\[114-more-i...-ec2-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/114-more-in-ec2-part1.txt)

**What changed:** The security group now allows inbound traffic on port 80. The browser's HTTP request reaches the instance → Apache serves the content from `/var/www/html/` → the response returns to the browser.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ EC2 Launch Process (Proper Order)

```
1. GATHER REQUIREMENTS
   ├── OS → AMI selection
   ├── Size (RAM/CPU) → Instance type
   ├── Storage → Volume config
   ├── Services → Security group ports
   ├── Environment → Naming, tagging, key grouping
   └── Owner/Project → Tags

2. CREATE KEY PAIR
   ├── Name: project-environment-region
   ├── Format: .pem (terminal) or .ppk (PuTTY)
   ├── Region-specific (only available in creation region)
   └── Private key downloads ONCE (AWS doesn't store it)

3. CREATE SECURITY GROUP
   ├── Name: project-servicetype
   ├── Inbound: ONLY ports needed NOW
   ├── Outbound: DO NOT TOUCH (leave all traffic)
   └── Stateful: inbound rule auto-allows matching outbound

4. LAUNCH INSTANCE
   ├── Select AMI, instance type
   ├── Select pre-created key pair
   ├── Select pre-created security group
   ├── Add tags (Name, Project, Environment, Owner)
   └── Tag volumes + network interfaces too
```

## 🔑 Key Pair Strategy

```
❌ 1 key for ALL instances     → Single point of compromise
❌ 1 key PER instance          → Unmanageable at scale
✅ 1 key PER environment/region → Balanced security + management

Key is REGION-SPECIFIC (us-east-1 key ≠ eu-west-1 key)
Private key: ONE-TIME download. Lost = unrecoverable.
Delete key in AWS → downloaded private key = USELESS
```

## 🔒 Security Group Architecture

```
Security Group = Virtual Firewall (bouncer/gatekeeper)
  │
  ├── INBOUND RULES (traffic → instance)
  │     ├── Type + Port + Source
  │     ├── Add ONLY when service is running
  │     └── SSH (22): My IP only | HTTP (80): Anywhere (if public)
  │
  ├── OUTBOUND RULES (instance → outside)
  │     ├── Default: All traffic → Anywhere
  │     └── DO NOT MODIFY (breaks internet access)
  │
  └── STATEFUL: Inbound allowed → return traffic auto-allowed

GRANULARITY:
  ❌ 1 SG for all          → No proper access control
  ❌ 1 SG per instance     → Unmanageable
  ✅ 1 SG per env+service  → e.g., moso-web (all dev web servers)
```

## 🏷️ Naming Convention Pattern

```
KEY PAIR:        project-environment-region    → moso-dev-virginia
SECURITY GROUP:  project-servicetype           → moso-web
INSTANCE TAG:    Name=web01, Project=moso, Env=dev, Owner=name

BAD naming → can't find resources in console → operational chaos
GOOD naming → instant identification at any scale
```

## 🔗 Network Interface Chain

```
Security Group Rules → applied to → Network Interface → attached to → EC2 Instance

Cleanup order (when deleting SG):
  1. Detach network interface from instance
  2. Delete network interface
  3. Delete security group
  (SG can't be deleted while NI references it)
```

## 🌐 Web Deployment Flow on EC2

```
SSH in (port 22 allowed)
  │
  apt update && apt install apache2 wget unzip -y
  │
  wget <template_URL>    ← Get URL from browser DevTools (F12 → Network tab)
  unzip <file>.zip
  cp -r <folder>/* /var/www/html/
  systemctl restart apache2
  │
  Verify: ss -tunlp | grep <PID>  → port 80 listening
  │
  Browser: http://<IP>  → ❌ BLOCKED (SG has only port 22)
  │
  Add inbound rule: port 80 from Anywhere (IPv4 + IPv6)
  │
  Browser: http://<IP>  → ✅ Website loads
```

## ⚡ Security Group Gate Logic

```
Service running + Port CLOSED in SG → ❌ Cannot access from outside
Service running + Port OPEN in SG   → ✅ Accessible

SSH (port 22):  Allow from MY IP only (management = restricted)
HTTP (port 80): Allow from ANYWHERE  (public website = open)

Rule: "Don't allow from anywhere" applies to MANAGEMENT ports
      Public service ports MUST allow from anywhere (that's their purpose)
```

## 📋 Ubuntu AMI Specifics

```
Default user: ubuntu (not root, not ec2-user)
Apache install: apt install apache2
Auto-starts: Yes (no systemctl start needed)
Document root: /var/www/html/
```

## 🏷️ Tagging Strategy

```
INSTANCE TAGS:
  Name        → web01
  Project     → moso
  Environment → dev
  Owner       → your name

ALSO TAG: Volumes + Network Interfaces
  → Trace sub-resources to project/owner/instance
```

## 📊 Terminated Instance Behavior

```
Terminated = permanently destroyed
Metadata visible in console for ~2 hours → then disappears
No actions possible on terminated instance
```

## 🔁 Reusable Engineering Patterns

| Pattern                                  | Manifestation                                                                                             |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Preparation before execution**         | Create key + SG BEFORE launch — not during                                                                |
| **Minimum-privilege firewall**           | Open only the ports you need, only when you need them                                                     |
| **Environment-based grouping**           | Keys, SGs, and tags organized by environment (dev/qa/prod)                                                |
| **Naming as operational infrastructure** | Proper names = findable resources = faster operations                                                     |
| **Stateful firewall**                    | Inbound rule auto-covers return traffic — no outbound duplication needed                                  |
| **Security != convenience**              | "Allow all" fixes connectivity but destroys security. Proper rules take more effort but prevent breaches. |
| **Add rules incrementally**              | Don't pre-open ports for future services. Open when service is live.                                      |
| **Tag everything**                       | Instances + volumes + network interfaces — all traceable to project/owner                                 |

## ⚡ Key Gotchas for Fast Recall

```
❌ Allow all traffic in SG inbound        → No firewall, anyone can access anything
✅ Allow only specific ports from specific sources

❌ Modify outbound rules                  → Instance loses internet connectivity
✅ Leave outbound as "All traffic → Anywhere"

❌ One key for 100 instances              → Compromise one = compromise all
✅ One key per environment per region      → Isolated, manageable

❌ Add HTTP rule before web server exists  → Unnecessary open port
✅ Add HTTP rule AFTER web server is running → Minimum-privilege timing

❌ Generic names (sg-1, mykey)            → Unfindable at scale
✅ project-env-region / project-service   → Instantly identifiable

❌ Forget to tag volumes/network interfaces → Orphaned resources, no ownership tracking
✅ Tag all resource types during launch     → Full traceability
```

***

This completes the full reconstruction of the EC2 Instance Launch Best Practices video.<cite>turn11search12</cite><cite>turn11search11</cite> Want me to generate Anki flashcards (CSV) from this material, or process another caption file?
