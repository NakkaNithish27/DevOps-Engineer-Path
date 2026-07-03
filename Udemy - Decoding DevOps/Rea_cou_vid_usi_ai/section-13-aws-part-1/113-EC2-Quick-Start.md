# 🎓 AWS EC2 Quick Start: Launching Your First Virtual Machine in the Cloud — Deep Learning Material

**Source:** Video caption file — *EC2 Quick Start (AWS Console Walkthrough)* [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — EC2: The Virtual Machine Service of AWS

EC2 stands for **Elastic Compute Cloud**, and it is AWS's core service for running virtual machines. Whenever you hear the terms **EC2**, **EC2 instance**, or just **instance** in the AWS context, it means a **virtual machine** or **virtual server** running in the cloud. This is the cloud equivalent of the VirtualBox VMs created with Vagrant in earlier lectures — except these machines run in AWS data centers, accessible over the Internet, and can be scaled, configured, and managed through the AWS console. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 1.2 — Regions and Availability Zones: Where Your Infrastructure Lives

### Regions

AWS infrastructure is spread across **regions** — geographically separated areas around the world. Each region is identified by a **code** (e.g., `us-east-1`) and a **human-readable name** (e.g., North Virginia). The video uses `us-east-1` (North Virginia) and recommends staying in **any United States region** because they tend to be **cheaper** than some other regions. Different regions have different pricing — this is a real operational consideration. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Availability Zones (AZs)

A region is **not a single data center**. The instructor emphasizes this distinction: "The region is just a label. Region is not the data center. Zones are the physical data centers." Each region contains multiple **Availability Zones** — separate physical data centers within the same geographic area. For `us-east-1`, the zones are `us-east-1a`, `us-east-1b`, `us-east-1c`, `us-east-1d`. Every region has a **minimum of two zones**. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

When you launch an EC2 instance, it runs in a **specific zone**. If you don't explicitly select a zone, **AWS chooses one for you**. The zone determines which physical data center your virtual machine runs in.

> 🔍 **Deep Dive:** The multi-zone architecture exists for **high availability** — the same redundancy concept from the networking lecture, applied at data center scale. If one zone (data center) experiences a hardware failure, power outage, or natural disaster, instances in other zones remain unaffected. Production architectures distribute instances across multiple zones so the application survives any single-zone failure. This is an *implicit concept* — the video introduces zones but doesn't explicitly discuss cross-zone deployment strategies.

***

## 1.3 — The EC2 Dashboard and Left-Panel Navigation

The EC2 Dashboard is the central control panel for all compute resources. The instructor notes an important operational detail: **the dashboard does not auto-refresh** — you must click refresh manually to get the latest status. It also shows a service health indicator: "This service is operating normally." If there's an issue with the selected region, the message changes. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

The left-side navigation panel organizes EC2 resources into sections that map to the key components of a virtual server:

* **Instances** — The VMs themselves (create, manage, monitor)
* **Instance Types** — CPU, RAM, storage, network specifications
* **Images (AMI)** — The OS templates used to launch instances
* **Elastic Block Store** — Hard disks (Volumes) and backups (Snapshots)
* **Network & Security** — Security Groups (firewalls), Elastic IPs (reserved public IPs), Key Pairs (login keys)
* **Load Balancers, Auto Scaling** — Advanced scaling and distribution features [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

Each section will be explored in detail in future lectures, but the overview establishes the mental map of what EC2 manages.

***

## 1.4 — AMI (Amazon Machine Image): The "Vagrant Box" of AWS

An **AMI** is a pre-built operating system image used to launch EC2 instances. There is **no OS installation process** in EC2 — you select a ready-made image, and your instance launches with that OS already configured. The instructor draws a direct parallel: "Like in Vagrant, we have Vagrant boxes — in AWS, we have AMI. AMIs are the Vagrant boxes of AWS." [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### AMI Sources — Three Tiers

**Quick Start AMIs** — The most popular, commonly used images. Amazon Linux, Ubuntu, Windows, Red Hat, SUSE, Debian, macOS. These are the first options presented when launching an instance. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

**AWS Marketplace AMIs** — Images that come **pre-installed with software**. Examples: OpenVPN, Splunk Enterprise, Wowza Streaming Engine. Some are free, some carry additional charges (e.g., $85/month for Wowza). The instructor warns: **"Be careful while selecting the AMI"** — marketplace AMIs can have significant costs attached. Some software requires separate licensing that you purchase and configure after launch. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

**Community AMIs** — Published by individual users. The instructor explicitly states: **"I never use these AMIs. I always trust in building my own AMI instead of using community AMI."** The standard practice is to launch from an official image, configure it to your needs, and then create your own custom AMI from that configured instance. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Amazon Linux and its Relationship to CentOS

**Amazon Linux 2023** is the current Amazon Linux version. It is **very similar to CentOS/Fedora** — the instructor says "most of the CentOS commands will work on Amazon Linux 2023." The key difference is the **software repositories** (where packages are downloaded from). Amazon Linux 2 (the previous version) is the equivalent of CentOS 7 / RHEL 7. The video uses Amazon Linux 2023 for the lab and notes it's **free tier eligible**. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

> ⚠️ **Expert Note:** The `dnf` command used in the user data script is the package manager for Amazon Linux 2023 (same as Fedora/CentOS Stream 9). The instructor explicitly notes: "You can use YUM install or DNF install" — both work because `yum` is an alias/compatibility layer for `dnf` on these newer systems. If you're comfortable with `yum` from the Bash scripting lectures, it works identically on Amazon Linux.

***

## 1.5 — Instance Types: Defining Your Machine's Resources

An instance type defines the **hardware specifications** of your virtual machine — how much CPU, RAM, storage speed, and network bandwidth it gets. The naming follows a pattern (e.g., `t2.micro`, `m8g.medium`), where the letter indicates the family/purpose and the size indicates the resource scale. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Instance Type Families

* **T series** (e.g., `t2.micro`) — General purpose, burstable. Good for low-to-moderate workloads. `t2.micro` is **free tier eligible** — no charge.
* **M series** (e.g., `m8g.medium`) — General purpose, the **most popular** for production. Balanced CPU, memory, network.
* **C series** — **Compute optimized** for CPU-intensive workloads.
* **R series** — **Memory optimized** for databases and memory-heavy applications.
* **Accelerated computing** — GPU instances for machine learning, graphics, etc.
* **Storage optimized** — For storage-intensive workloads (large databases, data warehouses). [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### The Practical Reality of Instance Type Selection

The instructor shares a real-world pattern: "People most of the time in the beginning, in the project, go with M series, then based on the load, based on the computing, they change the instance type." You start general, observe the actual workload characteristics, then optimize by switching to a specialized type if needed. Instance types **can be changed later** — you're not locked in. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 1.6 — Key Pairs: The SSH Authentication System

To log into an EC2 instance, you need a **key pair** — a public key and a private key. When you create a key pair in AWS, the **public key** is stored in AWS (attached to the instance), and the **private key** is **downloaded to your local machine**. This is the lock-and-key model: the public key is the lock on the server door, the private key is the key in your pocket. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Key Formats

* **`.pem`** — Used with SSH clients like Git Bash, Terminal, or any standard SSH tool. This is the format used in the video.
* **`.ppk`** — Used specifically with **PuTTY** (a Windows SSH client). [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

The private key file is downloaded **once** at creation time. If you lose it, you lose SSH access to instances using that key pair. The video downloads `webloginkey.pem` to the Downloads folder.

***

## 1.7 — Security Groups: The Firewall for EC2 Instances

A Security Group is a **firewall** that controls what network traffic can reach your EC2 instance. It is **mandatory** — every instance must have at least one security group. If you don't create your own, the console creates a default one. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

Security groups work through **inbound rules** — each rule specifies a **traffic type** (protocol/port) and a **source** (where the traffic is allowed from). The video demonstrates this critical concept:

**SSH (port 22)** is added first, with source set to **"My IP"** — meaning only the instructor's current public IP address can SSH into the instance. The instructor warns that this IP is **dynamic** for most home users: "Maybe tomorrow it will be different. When it changes, you need to update this rule." [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

**HTTP (port 80)** is **not added initially** — and this becomes the most important teaching moment in the lecture (covered in Section 1.9).

### Source Types

* **My IP** — Restricts access to your current public IP only. Secure but requires updating when your IP changes.
* **Anywhere (IPv4)** — Represented as `0.0.0.0/0`. Allows access from any IPv4 address in the world.
* **Anywhere (IPv6)** — Represented as `::/0`. Allows access from any IPv6 address.
* **Custom** — Specify a specific IP range or CIDR block. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 1.8 — User Data: Automated Commands at Launch (Provisioning)

**User Data** is a field in the EC2 launch configuration where you provide **commands or a script** that the instance executes automatically when it first boots. The instructor draws the direct parallel: "In Vagrant, we have seen Vagrant provisioning — same as that." [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

Since the instance is Linux, the first line must be `#!/bin/bash` — the shebang line that tells the system to use Bash to execute the commands. Everything after that line runs as if you typed it into the terminal after the instance started.

The video's user data:

```bash
#!/bin/bash
dnf install httpd -y
systemctl start httpd
systemctl enable httpd
```

This installs the Apache web server, starts it, and enables it to survive reboots — all automatically, without any manual login. When the instance finishes launching, the web server is already running. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 1.9 — Tags: Organizing and Identifying Resources

**Tags** are key-value metadata labels attached to AWS resources. They don't affect how the resource works — they're purely for **identification, organization, and filtering**. The video creates three tags: [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

* `Name: web01` — The display name of the instance
* `Project: Titan` — Identifies which project this instance belongs to
* `Env: Dev` — Identifies the environment (Dev, QA, Production, etc.)

Tags can be applied not just to the instance but also to associated resources like **volumes** (hard disks) and **network interfaces**. The instructor highlights the practical value: "Tags are very good for filtering. If you want to look for all the instances that belong to Titan Project, you can just query Titan and you'll get the list." In an organization with hundreds of instances, tags are how you find, group, and manage resources. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 1.10 — The Security Group Lesson: Why the Web Page Didn't Load

This is the most important conceptual moment in the lecture. After launching the instance, the instructor verifies **internally** that Apache is running: `systemctl status httpd` shows active, `curl http://127.0.0.1` returns the HTML page, `ps -ef | grep http` shows the Apache processes, and `ss -tunlp | grep 3374` confirms port 80 is open. Everything is working **inside the instance**. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

But when trying to access the web page from a browser using the **public IP over the Internet**, the page **doesn't load**. It just hangs. The instructor pauses and challenges: "Any guesses? Pause the lecture and think. Everything is running. Still, I'm not able to access it." [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

The answer: the **Security Group** only allows **SSH (port 22)**. **HTTP (port 80) is not allowed** in the inbound rules. The firewall is blocking web traffic. The service is running, the port is open on the instance, but the security group — the external firewall — is not permitting traffic on that port to reach the instance. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

After adding an HTTP rule allowing port 80 from anywhere (IPv4 and IPv6), the web page immediately loads.

> 🔍 **Deep Dive:** This demonstrates a critical debugging mental model: **the difference between "the service is running" and "the service is reachable."** A service can be perfectly healthy internally but completely inaccessible externally if the network/firewall layer blocks traffic. When troubleshooting connectivity issues in cloud environments, always check the firewall (security group) rules alongside the service status. The diagnostic sequence shown — check process → check port → check firewall → check from outside — is the standard cloud debugging workflow. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 1.11 — Public IP vs. Private IP vs. Elastic IP

Every EC2 instance has both a **private IP** (internal to the AWS network) and optionally a **public IP** (accessible from the Internet). The instructor emphasizes: "Public IP is accessible over the internet. Private IP is internal." When connecting from outside AWS, you must use the public IP. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

AWS also provides a **public DNS name** that resolves to the public IP. The instructor notes: "I use public IP all the time" rather than the DNS name.

**Elastic IP** is a **reserved public IP** that you can allocate and attach to instances. Unlike the regular public IP (which can change when an instance is stopped and restarted), an Elastic IP remains fixed. This is mentioned but deferred to a later lecture. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 1.12 — Instance Lifecycle: States and Health Checks

After launch, an instance enters the **running** state. AWS performs **two health checks**: one on the **hardware** layer and one on the **VM** layer. These show as "initializing" initially. However, the instance is **usable before the health checks complete** — you can log in and use it while checks are still running. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

**Instance states** available from the console:

* **Stop** — Shuts down the instance (preserves the volume/data, stops billing for compute).
* **Reboot** — Restarts the instance.
* **Terminate** — **Deletes** the instance permanently. "Terminate means delete instance, gone, poof." Recovery options exist (covered in later lectures). [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We're launching a **fully functional web server** on AWS from scratch — an EC2 instance running Amazon Linux 2023 with Apache (httpd) automatically installed and started via user data. We'll configure security, log in via SSH, verify the service, troubleshoot a connectivity issue caused by the security group, fix it, verify the web page loads from the Internet, and then clean up by terminating the instance. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## Step 1: Select the Region

### What We're Doing

Choosing the AWS region where our instance will be created.

### The Action

In the AWS Console, look at the **top-right corner** for the region selector. Select **US East (N. Virginia) `us-east-1`**. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Why This Region

US regions are generally cheaper. `us-east-1` is the most commonly used region with the most services available. Free tier is available here.

### Connection to Larger Flow

The region determines which data centers (Availability Zones) are available for your instance and affects latency for users accessing your services.

***

## Step 2: Navigate to EC2

### The Action

In the AWS Console search bar at the top, type **`EC2`**. Click on **"EC2 — Virtual Servers in the Cloud."** You land on the EC2 Dashboard. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Operational Note

Click **Refresh** on the dashboard to get the latest resource status — it does not auto-refresh.

***

## Step 3: Launch Instance — Name and Tags

### The Action

Click **"Launch Instance"** (either from the Dashboard or from the Instances section).

### Step 3a: Name Tag

Enter the name: **`web01`** [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Step 3b: Additional Tags

Click **"Add additional tags"** and add:

| Key       | Value   | Apply to                               |
| --------- | ------- | -------------------------------------- |
| `Name`    | `web01` | Instances, Volumes, Network Interfaces |
| `Project` | `Titan` | Instances, Volumes, Network Interfaces |
| `Env`     | `Dev`   | Instances, Volumes, Network Interfaces |

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Why Tags Matter

In production with hundreds of instances, tags are how you filter, search, and organize. Your project's naming convention should define standard tags.

***

## Step 4: Select the AMI

### The Action

In the **Quick Start** section, select **Amazon Linux 2023 AMI**. Confirm it shows **"Free tier eligible."** [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Important: Check the Username

After selecting the AMI, note the **default username**: **`ec2-user`**. This is the username you'll use for SSH login. Different AMIs have different default users (e.g., `ubuntu` for Ubuntu AMIs).

### Exploration (No Action Needed)

* Click **"Browse more AMIs"** to see the full catalog.
* Check the **Marketplace** — note that some AMIs have charges (e.g., Wowza at $85/month).
* Check **Community AMIs** — the instructor recommends against using these. Build your own instead.
* Search for **CentOS** to see available CentOS versions (most are free, some have support charges). [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Common Mistakes

* **Selecting a non-free-tier AMI** — Always verify "Free tier eligible" is displayed.
* **Selecting a Marketplace AMI with charges** — Check the pricing before selecting.

***

## Step 5: Select the Instance Type

### The Action

Select **`t2.micro`**. Confirm it shows **"Free tier eligible."** [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Why t2.micro

It's free. For learning and testing, it's sufficient. For production, you'd evaluate your workload and choose an appropriate type (M series for general purpose, C for compute, etc.).

### Common Mistakes

* **Accidentally selecting a larger instance type** — This will incur charges. Double-check before proceeding.

***

## Step 6: Create a Key Pair

### The Action

1. Click **"Create new key pair."**
2. Name: **`webloginkey`**
3. Key pair type: **`.pem`** (for Git Bash / Terminal / SSH client)
4. Click **"Create key pair."** [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### What Happens

The **private key file** (`webloginkey.pem`) is **downloaded to your machine** (typically the Downloads folder). The public key is stored in AWS.

### Critical Warning

This file downloads **once**. If you lose it, you cannot download it again. Know where it was saved.

### Connection to Larger Flow

This key is your authentication credential for SSH login to the instance. You'll reference it with the `-i` flag in the SSH command.

***

## Step 7: Configure Network Settings (Security Group)

### The Action

1. Click **"Edit"** in the Network settings section.
2. Change Security group name to: **`web-sg`**
3. Add a meaningful description. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Step 7a: SSH Inbound Rule

| Setting     | Value                     |
| ----------- | ------------------------- |
| Type        | SSH                       |
| Port        | 22                        |
| Source type | **My IP**                 |
| Description | `Allow 22 from my office` |

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

"My IP" auto-detects your current public IP. Remember: if your IP changes (dynamic IP from ISP), you'll need to update this rule.

### Important: HTTP Rule is NOT Added Yet

The video intentionally does **not** add port 80 here — this creates the teaching moment later when the web page won't load.

***

## Step 8: Configure Storage

### The Action

Keep the default: **gp3, 8 GB**. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

`gp3` = General Purpose SSD version 3, the most common storage type.

***

## Step 9: Add User Data (Provisioning Script)

### The Action

Expand **"Advanced details"** → scroll to the bottom → find the **"User data"** field.

Enter:

```bash
#!/bin/bash
dnf install httpd -y
systemctl start httpd
systemctl enable httpd
```

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

**Line-by-line breakdown:**

* `#!/bin/bash` — Shebang: tells the system to execute with Bash (same concept from Bash scripting lectures)
* `dnf install httpd -y` — Install Apache web server. `dnf` is the package manager for Amazon Linux 2023 (equivalent to `yum`). `-y` auto-confirms.
* `systemctl start httpd` — Start the Apache service immediately.
* `systemctl enable httpd` — Enable Apache to start automatically on reboot.

### What Happens

These commands execute **automatically** when the instance first boots. By the time you log in, Apache is already installed and running.

***

## Step 10: Launch the Instance

### The Action

Click **"Launch instance."** [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### What Happens

AWS creates the instance. You receive an **Instance ID** — a unique identifier for this resource (every AWS resource gets one). Click the Instance ID link to navigate to the instance details.

### Post-Launch Observations

| Field             | Value/Note                                |
| ----------------- | ----------------------------------------- |
| Name              | `web01` (from tag)                        |
| Instance State    | Running                                   |
| Instance Type     | `t2.micro`                                |
| Status Checks     | Initializing (two checks: hardware + VM)  |
| Availability Zone | Auto-selected by AWS (e.g., `us-east-1a`) |
| Public DNS        | Auto-assigned (resolves to public IP)     |
| Public IPv4       | Auto-assigned                             |
| Security Group    | `web-sg`                                  |
| Key Pair          | `webloginkey`                             |

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

The instance is usable **before** status checks complete.

***

## Step 11: SSH into the Instance

### Step 11a: Get the SSH Command

In the console, select the instance → click **"Connect"** → go to the **"SSH client"** tab. Copy the provided SSH command. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Step 11b: Execute the SSH Command

Open **Git Bash** (or Terminal). The command format:

```bash
ssh -i Downloads/webloginkey.pem ec2-user@<PUBLIC_IP>
```

**Breakdown:**

* `ssh` — SSH client command
* `-i Downloads/webloginkey.pem` — `-i` specifies the **identity file** (private key). The path must point to where the `.pem` file was downloaded.
* `ec2-user` — The default username for Amazon Linux AMIs
* `@<PUBLIC_IP>` — The public IP of your instance (copy from the EC2 console) [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### First Connection

On first connect, SSH asks: "Are you sure you want to continue connecting?" Type **`yes`**. You're now inside the EC2 instance.

### Common Errors and Their Meanings

| Error Message                | Cause                             | Fix                                         |
| ---------------------------- | --------------------------------- | ------------------------------------------- |
| `No such file or directory`  | Wrong path to the `.pem` key file | Find the correct path (`ls ~/Downloads/`)   |
| `Permission denied`          | Wrong username OR wrong key       | Verify `ec2-user` and correct `.pem` file   |
| `Could not resolve hostname` | Wrong IP address or DNS name      | Copy the correct public IP from the console |

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Connection to Larger Flow

You're now inside the cloud VM — same as being inside a Vagrant VM via `vagrant ssh`, but this machine is running in an AWS data center.

***

## Step 12: Verify the Web Server (Internal)

### Switch to Root

```bash
sudo -i
```

### Check the OS

```bash
cat /etc/os-release
```

Confirms: Amazon Linux 2023 (Fedora/CentOS family). [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Check Apache Status

```bash
systemctl status httpd
```

Expected: **`active (running)`** — confirms user data provisioning worked. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Test the Web Page Internally

```bash
curl http://127.0.0.1
```

Returns HTML content including "It works" — the default Apache test page is being served. `127.0.0.1` is the loopback/localhost IP. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Check the Running Processes

```bash
ps -ef | grep http
```

Shows Apache processes running. Note one of the process IDs (e.g., `3374`). [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Check the Listening Port

```bash
ss -tunlp | grep 3374
```

Confirms **port 80** is open and associated with the Apache process. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

**Breakdown of `ss -tunlp`:**

* `ss` — Socket statistics (modern replacement for `netstat`)
* `-t` — Show TCP sockets
* `-u` — Show UDP sockets
* `-n` — Show numeric port numbers (not service names)
* `-l` — Show only listening sockets
* `-p` — Show the process using the socket

### Internal Verification Complete

Service is running ✅, page is served locally ✅, process is alive ✅, port is open ✅.

***

## Step 13: Access from Browser (and Hit the Security Group Wall)

### The Action

Open a browser. Navigate to:

```
http://<PUBLIC_IP>
```

(Port 80 is HTTP's default — no need to specify `:80`.) [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Expected Result

The page **does not load**. It hangs indefinitely.

### Why It Fails

The security group `web-sg` only has an inbound rule for **SSH (port 22)**. There is **no rule allowing HTTP (port 80)**. The instance's firewall is blocking all web traffic from reaching Apache, even though Apache is running perfectly internally. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### The Debugging Lesson

The diagnostic chain: process running ✅ → port open ✅ → internal access works ✅ → external access fails ❌ → **the problem is between the Internet and the instance** → check the firewall (security group).

***

## Step 14: Fix the Security Group — Add HTTP Rule

### The Action

1. In the EC2 console, select the instance → **Security** tab → click on the **Security Group** link.
2. Click **"Edit inbound rules."**
3. Click **"Add rule."** [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### The Rules to Add

| Type | Port | Source                      | Description              |
| ---- | ---- | --------------------------- | ------------------------ |
| HTTP | 80   | `0.0.0.0/0` (Anywhere IPv4) | Allow HTTP from anywhere |
| HTTP | 80   | `::/0` (Anywhere IPv6)      | Allow HTTP from anywhere |

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

`0.0.0.0/0` = all IPv4 addresses. `::/0` = all IPv6 addresses. Both are needed if you want the website accessible to everyone on the Internet.

4. Click **"Save rules."**

### Verify the Fix

Go back to the browser. Refresh the page.

**Expected:** The Apache test page loads — **"It works."** ✅ [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### Connection to Larger Flow

The security group rule change takes effect **immediately** — no instance restart needed. This is a live firewall update.

***

## Step 15: Clean Up — Terminate the Instance

### The Action

1. Select the instance in the EC2 console.
2. Click **Instance state** → **Terminate instance**. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

### What This Does

**Terminate = delete permanently.** The instance is gone. The instructor acknowledges: "I know you'll have questions like how to recover if the instances are gone — we'll talk about that later."

### Post-Cleanup Recommendation

The instructor emphasizes: **"Do this exercise at least three times. It's free, so please do it."** Repetition builds muscle memory for the launch workflow. [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ EC2 Core Identity

```
EC2 = Virtual Machine service of AWS
EC2 Instance = Virtual Machine = Virtual Server
"Instance" in AWS context ALWAYS means VM
```

***

## 🌍 Region → Zone → Instance

```
AWS Region (e.g., us-east-1 / North Virginia)
  ├── Availability Zone 1a  ← Physical data center
  ├── Availability Zone 1b  ← Physical data center
  ├── Availability Zone 1c  ← Physical data center
  └── Availability Zone 1d  ← Physical data center
        └── Your EC2 Instance runs HERE

RULE: Region = label, NOT a data center
      Zone = actual physical data center
      Min 2 zones per region
      If no zone selected → AWS picks for you
```

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 🚀 EC2 Launch Configuration — 7 Decisions

```
1. REGION        → Where geographically (us-east-1 recommended, cheaper)
2. TAGS          → Name, Project, Env (for filtering/organization)
3. AMI           → OS image (Amazon Linux 2023 = free tier, CentOS-like)
                   Sources: Quick Start | Marketplace (⚠️ charges!) | Community (❌ avoid)
4. INSTANCE TYPE → Hardware specs (t2.micro = free tier)
                   Families: T(burstable) M(general) C(compute) R(memory) Storage/GPU
5. KEY PAIR      → SSH auth (.pem for Git Bash, .ppk for PuTTY)
                   ⚠️ Private key downloads ONCE — don't lose it
6. SECURITY GROUP → Firewall rules (port + source)
                   ⚠️ Must explicitly allow each port
7. USER DATA     → Bootstrap script (runs at first boot)
                   = Vagrant provisioning equivalent
```

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 🔗 Concept Mapping: Vagrant → AWS

```
VAGRANT CONCEPT          AWS EQUIVALENT
───────────────          ──────────────
Vagrant Box        →     AMI (Amazon Machine Image)
vagrant up         →     Launch Instance
vagrant ssh        →     ssh -i key.pem ec2-user@IP
Vagrantfile        →     Launch Configuration
Provisioning       →     User Data (#!/bin/bash + commands)
VirtualBox         →     EC2 (the hypervisor is hidden)
Private network IP →     Private IP (internal)
(no equivalent)    →     Public IP (Internet-accessible)
(no equivalent)    →     Security Group (cloud firewall)
```

***

## 🔐 SSH Login Command Structure

```
ssh -i <path/to/key.pem> <username>@<public_ip>

EXAMPLE:
ssh -i Downloads/webloginkey.pem ec2-user@54.123.45.67

ERROR DIAGNOSIS:
  "No such file or directory"  → Wrong key path
  "Permission denied"          → Wrong username or wrong key
  "Could not resolve"          → Wrong IP address
```

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 🛡️ Security Group = Cloud Firewall

```
INBOUND RULES (traffic TO instance):
  ┌──────────┬──────┬─────────────────┐
  │ Type     │ Port │ Source           │
  ├──────────┼──────┼─────────────────┤
  │ SSH      │ 22   │ My IP           │ ← Restricted (changes with dynamic IP)
  │ HTTP     │ 80   │ 0.0.0.0/0       │ ← Open to world (IPv4)
  │ HTTP     │ 80   │ ::/0            │ ← Open to world (IPv6)
  └──────────┴──────┴─────────────────┘

KEY RULE: If port NOT in security group → traffic BLOCKED
          Even if service is running internally
          Changes take effect IMMEDIATELY (no restart)
```

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 🔍 The Debugging Sequence (Critical Mental Model)

```
PROBLEM: Web page doesn't load from browser

DIAGNOSTIC CHAIN:
  1. systemctl status httpd     → Running? ✅
  2. curl http://127.0.0.1      → Responds locally? ✅
  3. ps -ef | grep http         → Process alive? ✅
  4. ss -tunlp | grep <PID>    → Port 80 open? ✅
  5. Browser http://<PUBLIC_IP>  → Loads? ❌
  
  ALL INTERNAL CHECKS PASS + EXTERNAL FAILS
  → Problem is BETWEEN Internet and instance
  → CHECK SECURITY GROUP
  → Port 80 not in inbound rules
  → ADD HTTP rule → FIXED ✅

MENTAL MODEL:
  Service OK + Firewall blocks = Unreachable
  Always check: process → port → firewall → external access
```

***

## 📐 User Data Script (Provisioning)

```bash
#!/bin/bash              ← Shebang (Bash interpreter)
dnf install httpd -y     ← Install Apache (dnf = yum on Amazon Linux 2023)
systemctl start httpd    ← Start service NOW
systemctl enable httpd   ← Start on every boot

EXECUTES: Automatically at FIRST BOOT (no manual login needed)
EQUIVALENT: Vagrant provisioning block
```

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## ⚡ Instance Lifecycle

```
Launch → Running → [Stop | Reboot | Terminate]
                      │       │          │
                      │       │          └── DELETE permanently (gone)
                      │       └── Restart (same instance)
                      └── Shutdown (data preserved, compute billing stops)

Health Checks: 2 checks (hardware + VM) → "initializing" → pass/fail
               Instance USABLE before checks complete
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: DECLARATIVE PROVISIONING (User Data)
  Define desired state in a script → system auto-configures at boot
  → Same as: Vagrant provisioning, cloud-init, Ansible playbooks,
    Dockerfile RUN commands, Terraform user_data blocks

PATTERN 2: LAYERED SECURITY (Security Groups)
  Service running ≠ Service reachable
  Explicit allow-list firewall: deny-all by default, allow per rule
  → Same as: Network firewalls, Kubernetes NetworkPolicies,
    API gateway rules, WAF rules

PATTERN 3: IMAGE-BASED DEPLOYMENT (AMI)
  No OS installation → Select pre-built image → Launch
  → Same as: Docker images, Vagrant boxes, VM snapshots,
    golden image pipeline, immutable infrastructure

PATTERN 4: RESOURCE TAGGING FOR FLEET MANAGEMENT
  Tag everything → Filter/search/organize at scale
  → Same as: Kubernetes labels, Docker labels,
    Terraform resource tags, any metadata-driven inventory

PATTERN 5: PROGRESSIVE DIAGNOSTIC CHAIN
  Internal → Port → Firewall → External
  Narrow the failure domain from inside out
  → Universal troubleshooting: check closest layer first,
    expand outward until you find the broken layer
```

 [\[113-ec2-quick-start \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/113-ec2-quick-start.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → Bash scripting (variables, conditions, loops, remote exec, best practices)
           → Vagrant (local VMs, provisioning, multi-VM)
           → Networking (IPs, public/private, subnets)
THIS      → EC2 Quick Start: first cloud VM, all concepts converge
NEXT      → EC2 best practices, detailed services (EBS, VPC, EIP, etc.)
LATER     → AWS VPC (subnet design using IP knowledge from networking lecture)

INSTRUCTOR: "Do this exercise at least 3 times. It's free."
```

***

Your EC2 Quick Start deep learning material is fully reconstructed — this is the biggest and most concept-dense lecture so far, bringing together networking, Bash scripting, Vagrant, and cloud infrastructure into one operational flow. Want me to generate **AnkiDroid flashcards (.csv)** from this lecture or across all lectures? 🃏
