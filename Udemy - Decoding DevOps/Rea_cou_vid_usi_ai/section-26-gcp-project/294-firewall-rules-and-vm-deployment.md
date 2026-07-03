# 🎓 Deep Learning Material: GCP Firewall Rules & Bastion Host VM Deployment

*Reconstructed from video lecture captions (294-firewall-rules-and-vm-deployment.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Architecture Being Built: Where This Lecture Fits

This lecture sits within a larger project where a VPC with four subnets, a Cloud Router, and Cloud NAT have already been created in previous lectures. The current goal is to create the **network access rules** (firewall rules) and launch the **bastion host** — a VM in the public subnet that serves as the secure entry point to the entire infrastructure. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

The full architecture involves:

* A **bastion host** in the public subnet — the only instance directly accessible from the internet via SSH
* An **app server** in the private subnet — running the vprofile application on Tomcat (port 8080), not directly reachable from the internet
* A **load balancer** (created in a later lecture) — receiving public traffic and forwarding to the app server
* **Cloud SQL** (created in the next lecture) — the database backend

This lecture creates **three firewall rules** to control traffic flow between these components and then launches the bastion host VM. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## 1.2 GCP Firewall Rules vs. AWS Security Groups: The Tag-Based Model

This is the most conceptually important distinction in the lecture. The instructor explicitly contrasts the two cloud platforms' approaches to network security. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**In AWS:** You create a security group, then when you launch an instance, you **directly select** that security group. The security group is attached to the instance by explicit selection during launch. The binding is direct: instance → security group.

**In GCP:** You create a firewall rule and assign it a **target tag** — a label like `bastion` or `app`. When you launch an instance, you give it **tags**. Any firewall rule whose target tag matches an instance's tag is **automatically applied** to that instance. There is no direct selection — the binding happens **through tag matching**. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

The instructor states: *"There is no direct attaching. It will be attaching through the tags."* [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

This is a fundamentally different architectural model. In AWS, the relationship is **explicit and direct** (you pick the security group). In GCP, the relationship is **implicit and declarative** (you declare tags, and matching happens automatically). This tag-based model has a powerful consequence: if you launch 100 instances with the tag `app`, all 100 automatically receive every firewall rule that targets `app`. You never manually attach anything.

🔍 **Deep Dive:**
GCP firewall rules have two tag concepts that serve different purposes:

* **Target tag** — Defines which instances the rule **applies to** (the destination). An instance with a matching tag receives this firewall rule.
* **Source tag** — Defines where traffic is **allowed to come from**. If a source tag is specified, only traffic originating from instances with that tag is permitted.

The instructor demonstrates both: the bastion firewall uses a **source range** (IP address) and a **target tag** (`bastion`). The bastion-to-app firewall uses a **source tag** (`bastion`) and a **target tag** (`app`). This means only traffic from instances tagged `bastion` can reach instances tagged `app` on port 22. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## 1.3 The Three Firewall Rules: A Layered Access Control Architecture

The instructor creates three firewall rules, each controlling a specific traffic path. Together, they form a **layered security architecture** where traffic can only flow through explicitly permitted channels. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

### Firewall 1: `allow-ssh-internet` (Internet → Bastion)

* **Purpose:** Allow SSH access from the internet to the bastion host
* **Port:** TCP 22
* **Source:** IP range (ideally your specific public IP, but initially set to `0.0.0.0/0` for all IPs)
* **Target tag:** `bastion`
* **Direction:** Ingress (inbound)

This is the **only entry point** from the outside world into the infrastructure. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

The instructor provides a critical security warning: *"Do not give 0.0.0.0/0. That allows all the IP address on port 22."* He explains that in production, you should restrict the source to your specific public IP with a `/32` mask (single IP). However, he warns that your public IP changes over time, so *"whenever you're not able to do SSH to your bastion host, you need to come back here, edit the rule and make sure you add your latest IP address."* [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

### Firewall 2: `allow-ssh-bastion` (Bastion → App Server)

* **Purpose:** Allow SSH from the bastion host to the app server in the private subnet
* **Port:** TCP 22
* **Source tag:** `bastion` (not an IP — traffic must originate from an instance tagged `bastion`)
* **Target tag:** `app`
* **Direction:** Ingress (inbound)

This is the **hop** that allows administrators to reach the private subnet. You first SSH into the bastion (using firewall 1), then from the bastion, SSH into the app server (using firewall 2). The private app server is never directly accessible from the internet. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

The instructor explains the source tag concept: *"Source can be a range, source can be a specific IP address like my IP, or source can be another firewall rule."* Using a source tag means the rule trusts any instance that belongs to the bastion group — not a specific IP, but an identity. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

### Firewall 3: `allow-elb-to-app` (Load Balancer → App Server)

* **Purpose:** Allow the GCP load balancer to send traffic to the app server on Tomcat's port
* **Port:** TCP 8080 (Tomcat default)
* **Source range:** `130.211.0.0/22, 35.191.0.0/16` (GCP load balancer's public IP range)
* **Target tag:** `app`
* **Direction:** Ingress (inbound)

This firewall rule enables the production traffic flow: users → load balancer → app server. The instructor explains that GCP load balancers use **specific public IP ranges** that are known and documented. The source range `130.211.0.0/22` and `35.191.0.0/16` covers the IP addresses from which GCP load balancer health checks and traffic forwarding originate. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

The instructor draws the AWS parallel: *"In AWS term, we have created a security group for the app server to allow connection from the load balancer."* He also notes a difference in load balancer networking: in AWS, you create a security group for the load balancer and reference it. In GCP, the load balancer gets a public IP (which can be static) from a known range, so you reference that IP range as the source. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

⚠️ **Expert Note:**
The GCP load balancer IP ranges (`130.211.0.0/22`, `35.191.0.0/16`) are Google's documented ranges for health checks and load balancer traffic. These are stable — Google publishes them officially. Using these ranges is the correct approach, not a workaround. In contrast, AWS load balancers live within your VPC and have security groups, so you reference the security group directly. This is a fundamental networking architecture difference between the two cloud platforms.

***

## 1.4 SSH Key Management: GCP vs. AWS Approach

In AWS, you create a **key pair** through the AWS console, download the private key, and select that key pair when launching an instance. AWS handles injecting the public key into the instance automatically. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

In GCP, this is fundamentally different. The instructor explains: *"In AWS we have key pair. When we launch the instance we select the key pair. In GCP, that is not the case."* [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

Instead, GCP uses a **startup script** (called an "automation script" in the GCP GUI) to handle SSH key setup. The startup script executes during the instance's first boot and performs these operations: [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

1. Creates a user (e.g., `devops`)
2. Adds that user to the sudoers file (for root access)
3. Injects the **public SSH key** into that user's `~/.ssh/authorized_keys` file

You previously generated a key pair (public and private key) locally. The public key content is embedded in the startup script. When the instance boots, the script runs, creates the user, and installs the key. You then use the **private key** to SSH into the instance as that user. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

This means in GCP, key management is **manual and explicit** — you control the user creation, the key placement, and the sudo configuration through your own script. In AWS, the platform handles it implicitly through the key pair mechanism.

***

## 1.5 Instance Launch: Zone Selection, Machine Types, and Image Families

The instructor covers several GCP-specific concepts during instance creation: [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Zone vs. Region:** When launching a GCP instance, you specify a **zone** (e.g., `us-central1-a`), not just a region. A region contains multiple zones. The instructor notes: *"Yes, that's the zone name, not the region name. In one region you have multiple zones."* [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Machine Type:** The instructor selects `e2-micro` — 1 shared vCPU, 1 GB RAM. In the GUI walkthrough, he shows the machine type hierarchy: E2 series → e2-medium, e2-micro, e2-small. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Image Family:** The instance uses an Ubuntu image specified as `--image-family` with the project `ubuntu-os-cloud`. The instructor shows in the GUI that you can choose the OS (Ubuntu), the version (e.g., Ubuntu 24), and the architecture (AMD vs. ARM). [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Boot Disk Types:** The GUI shows several options — Balanced (cheapest), SSD (fastest), with configurable size. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Snapshot Warning:** The instructor warns about snapshot schedules in the GUI: *"Be very careful when you are doing it through the GUI. You know you have snapshot schedules and if you don't delete the instances, it's going to keep taking snapshots. And the monthly estimate can go to $6 for 10GB disk."* [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Network Service Tier:** The GUI offers Premium (higher cost, better performance) and Standard (lower cost, suitable for learning). [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## 1.6 What the Bastion Host Verifies About the VPC

The instructor makes an important point after successfully SSHing into the bastion host and running `apt update`: this single test validates **multiple infrastructure layers simultaneously**. He states: *"This is not just the VM test. We are also testing the VPC. It's in the public subnet. It is getting the internet. We are able to SSH to it."* [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

The verifications achieved by one successful SSH + apt update: [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

* **VPC** is correctly configured
* **Public subnet** has internet access
* **Firewall rule** allows SSH (port 22) to instances tagged `bastion`
* **Tag matching** works (instance has the `bastion` tag, firewall applies)
* **Startup script** ran correctly (user `devops` exists, SSH key works, sudo works)
* **Cloud NAT / Cloud Router** is functioning (the instance can reach the internet for `apt update`)
* **Instance itself** is running properly

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating **three GCP firewall rules** that define the allowed traffic paths in our infrastructure, and then launching a **bastion host VM** in the public subnet. The final outcome: a bastion host we can SSH into from our local machine, which will serve as the jump point to reach private instances and initialize Cloud SQL in the next lecture. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## Phase 1: Set Up Variables

### Step 1: Define Variables in Cloud Shell

Open your **GCP Cloud Shell** and set the variables used across all commands: [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

```bash
VPC=<your_vpc_name>
SSH_KEY=<path_to_your_public_key>
MY_IP=0.0.0.0/0
TAG_BASTION=bastion
TAG_APP=app
PROJECT_ID=<your_project_id>
```

**Key variables explained:**

* `MY_IP` — Set to `0.0.0.0/0` initially (all IPs). The instructor shows how to restrict this later.
* `TAG_BASTION` / `TAG_APP` — The tags that link firewall rules to instances. These exact values must match what you give instances at launch time.
* `SSH_KEY` — The SSH public key created in a previous lecture.

### Step 2: Set the Active Project

```bash
gcloud config set project "$PROJECT_ID"
```

 [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Why:** GCP CLI commands require a project context. If this isn't set, commands fail with "project is not set." The instructor encounters this error and fixes it. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## Phase 2: Create Firewall Rules

### Step 3: Create Firewall Rule — Internet to Bastion (SSH)

```bash
gcloud compute firewall-rules create allow-ssh-internet \
  --network=$VPC \
  --allow=tcp:22 \
  --source-ranges=$MY_IP \
  --target-tags="$TAG_BASTION" \
  --direction=INGRESS
```

 [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Breakdown:**

* `gcloud compute firewall-rules create` — Creates a new firewall rule
* `allow-ssh-internet` — Name of the rule (descriptive: allows SSH from the internet)
* `--network=$VPC` — Associates the rule with your VPC
* `--allow=tcp:22` — Permits TCP traffic on port 22 (SSH). Format: `protocol:port`
* `--source-ranges=$MY_IP` — Who can send traffic. Currently `0.0.0.0/0` (all IPs)
* `--target-tags="$TAG_BASTION"` — Applies to instances tagged `bastion`
* `--direction=INGRESS` — Inbound rule (traffic coming INTO instances)

**Verification:** Check the output shows the rule name, VPC, and TCP:22. Also verify in the GCP console: **VPC → Firewalls** → the rule `allow-ssh-internet` should appear. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

### Step 3a: (Optional) Restrict Source IP for Security

In the GCP Console → VPC → Firewalls → click `allow-ssh-internet` → **Edit**: [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

1. Remove `0.0.0.0/0`
2. Find your public IP: Google "what is my IP" or visit a site that shows it
3. Enter your IP followed by `/32` (e.g., `203.0.113.45/32`) — restricts to exactly one IP
4. Save

**Operational warning:** Your public IP changes (dynamic ISP assignment). When SSH suddenly stops working, return here and update to your current IP. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

### Step 4: Create Firewall Rule — Bastion to App Server (SSH)

```bash
gcloud compute firewall-rules create allow-ssh-bastion \
  --network=$VPC \
  --allow=tcp:22 \
  --source-tags="$TAG_BASTION" \
  --target-tags="$TAG_APP" \
  --direction=INGRESS
```

 [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Breakdown:**

* `allow-ssh-bastion` — Name (allows SSH from bastion)
* `--source-tags="$TAG_BASTION"` — **Source tag** (not range): only traffic from instances tagged `bastion` is allowed. This is the tag-to-tag referencing model.
* `--target-tags="$TAG_APP"` — Applies to instances tagged `app`

**Key difference from Step 3:** This rule uses `--source-tags` instead of `--source-ranges`. Source tags reference instances by identity (tag membership), not by IP address.

**Verification:** In the console, the rule should show source filter = `bastion`, target = `app`. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

### Step 5: Create Firewall Rule — Load Balancer to App Server (8080)

```bash
gcloud compute firewall-rules create allow-elb-to-app \
  --network=$VPC \
  --allow=tcp:8080 \
  --source-ranges=130.211.0.0/22,35.191.0.0/16 \
  --target-tags="$TAG_APP" \
  --direction=INGRESS
```

 [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Breakdown:**

* `allow-elb-to-app` — Name (allows load balancer to reach app)
* `--allow=tcp:8080` — Tomcat's default port
* `--source-ranges=130.211.0.0/22,35.191.0.0/16` — GCP's documented load balancer IP ranges
* `--target-tags="$TAG_APP"` — Applies to instances tagged `app`

**Verification:** In the console, rule shows target tag `app`, source ranges for LB, port 8080. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## Phase 3: Prepare the Bastion Startup Script

### Step 6: Create the bastion.sh File

Create a file named `bastion.sh` in Cloud Shell with the user setup commands: [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

```bash
cat > bastion.sh <<EOF
#!/bin/bash
useradd -m -s /bin/bash devops
echo "devops ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
mkdir -p /home/devops/.ssh
echo "<YOUR_PUBLIC_KEY_CONTENT>" > /home/devops/.ssh/authorized_keys
chown -R devops:devops /home/devops/.ssh
chmod 700 /home/devops/.ssh
chmod 600 /home/devops/.ssh/authorized_keys
EOF
```

(The exact script content comes from the course materials — copy it as provided.) [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**What this script does when the instance boots:**

1. Creates a user named `devops`
2. Adds `devops` to sudoers with NOPASSWD (passwordless sudo)
3. Creates the `.ssh` directory in the user's home
4. Injects your **public key** into `authorized_keys`
5. Sets correct ownership and permissions

**Verification:**

```bash
cat bastion.sh
```

Confirm the username is `devops` and the public key content is correct. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## Phase 4: Launch the Bastion Host

### Step 7: Create the Instance

```bash
gcloud compute instances create bastion-host \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --subnet=<PUBLIC_SUBNET_NAME> \
  --tags="$TAG_BASTION" \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=bastion.sh
```

 [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Breakdown:**

* `gcloud compute instances create bastion-host` — Creates a VM named `bastion-host`
* `--zone=us-central1-a` — Specific zone (not just region)
* `--machine-type=e2-micro` — 1 shared vCPU, 1 GB RAM
* `--subnet=<PUBLIC_SUBNET_NAME>` — Launches in the public subnet (internet-accessible)
* `--tags="$TAG_BASTION"` — Assigns the `bastion` tag → firewall rule `allow-ssh-internet` automatically applies
* `--image-family=ubuntu-2404-lts-amd64` — Ubuntu OS image
* `--image-project=ubuntu-os-cloud` — Google's official Ubuntu image project
* `--metadata-from-file=startup-script=bastion.sh` — Runs `bastion.sh` on first boot (creates user, injects key)

**Wait** for the command to complete. You can also watch the instance appear in the GCP Console → Compute Engine → VM Instances. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Result:** The instance will show an **external (public) IP address**. Copy this IP. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

## Phase 5: Verify the Setup

### Step 8: SSH into the Bastion Host

From your local terminal (where your private key is stored): [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

```bash
ssh -i gcp devops@<EXTERNAL_IP>
```

**Breakdown:**

* `ssh` — SSH client
* `-i gcp` — Private key file (named `gcp` — the pair to the public key in the startup script)
* `devops` — The username created by the startup script
* `@<EXTERNAL_IP>` — The bastion host's public IP

Type `yes` for host key verification. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Expected result:** You land in a shell on the bastion host as user `devops`. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

### Step 9: Verify Root Access

```bash
sudo -i
```

 [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Expected:** You switch to root without being asked for a password (NOPASSWD in sudoers).

### Step 10: Verify Internet Connectivity

```bash
apt update
```

 [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

**Expected:** Package lists are fetched successfully, confirming the instance can reach the internet through the public subnet + Cloud NAT/Router.

**What this single test verifies** (see Theory 1.6): VPC, public subnet, firewall rule, tag matching, startup script, Cloud NAT, instance health — all confirmed by one successful SSH + apt update.

**Keep the instance running** — it's needed for the next lecture to initialize Cloud SQL. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

### GUI Walkthrough Reference (Not for Execution — For Understanding)

The instructor also shows the GUI path for creating instances: Compute Engine → VM Instances → **Create Instance**. The GUI exposes: [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

| GUI Section                     | What You Configure                                                           |
| ------------------------------- | ---------------------------------------------------------------------------- |
| Name                            | Instance name                                                                |
| Region & Zone                   | Where to launch (specific zone required)                                     |
| Machine configuration           | Series (E2) → Type (e2-micro, e2-small, etc.)                                |
| OS and storage → Boot disk      | OS (Ubuntu), version, architecture (AMD/ARM), disk type (Balanced/SSD), size |
| Data protection                 | Snapshot schedules (**⚠️ can incur costs if left enabled**)                  |
| Networking → Tags               | Tags for firewall matching                                                   |
| Networking → Network interfaces | VPC and subnet selection; Network service tier (Premium/Standard)            |
| Advanced → Automation           | Startup script (same as `--metadata-from-file=startup-script=`)              |

⚠️ **Expert Note:**
The instructor specifically warns about the **snapshot schedule** in the GUI: if enabled and instances aren't deleted, snapshots accumulate and cost money (\~$6/month for 10GB). Always check this setting when creating instances through the GUI. [\[294-firewa...deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/294-firewall-rules-and-vm-deployment.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture

```
[Internet]
    │
    │ port 22 (allow-ssh-internet: source=MY_IP, target=bastion)
    ▼
[Bastion Host]  ── public subnet ── tag: bastion
    │
    │ port 22 (allow-ssh-bastion: source-tag=bastion, target-tag=app)
    ▼
[App Server]    ── private subnet ── tag: app
    ▲
    │ port 8080 (allow-elb-to-app: source=130.211.0.0/22,35.191.0.0/16, target=app)
    │
[GCP Load Balancer]  ── public IP from known ranges
```

***

## GCP Firewall vs. AWS Security Groups

```
AWS:                                    GCP:
  Create SG → Launch instance →           Create firewall rule with TARGET TAG
  SELECT SG directly                      Launch instance with TAGS
                                          Matching happens automatically via tags

AWS: Direct binding (select SG)
GCP: Declarative binding (tag matching)
  → No manual attachment
  → 100 instances with tag "app" → all get "app" firewall rules automatically
```

***

## Three Firewall Rules

```
RULE 1: allow-ssh-internet
  Internet ──tcp:22──→ [tag: bastion]
  source-ranges: 0.0.0.0/0 (restrict to YOUR_IP/32 in production)
  
RULE 2: allow-ssh-bastion
  [source-tag: bastion] ──tcp:22──→ [target-tag: app]
  Tag-to-tag referencing (identity, not IP)

RULE 3: allow-elb-to-app
  [source: 130.211.0.0/22, 35.191.0.0/16] ──tcp:8080──→ [target-tag: app]
  GCP LB known IP ranges → Tomcat port
```

***

## Source Types in Firewall Rules

```
--source-ranges=IP/CIDR       → Allow from specific IP or range
--source-tags=TAG_NAME         → Allow from instances with matching tag

Source can be:
  ├── 0.0.0.0/0         (all IPs — insecure for SSH)
  ├── YOUR_IP/32         (single IP — secure but changes)
  ├── CIDR range         (IP block — e.g., LB ranges)
  └── Source TAG         (identity-based — bastion→app)
```

***

## SSH Key Injection: GCP vs AWS

```
AWS:
  Console → Create key pair → Download private key
  Launch instance → Select key pair → AWS injects public key automatically

GCP:
  Generate key pair locally (ssh-keygen)
  Write startup script (bastion.sh):
    ├── useradd devops
    ├── Add to sudoers (NOPASSWD)
    └── Echo public key → ~/.ssh/authorized_keys
  Launch instance with --metadata-from-file=startup-script=bastion.sh
  SSH with: ssh -i <private_key> devops@<IP>

AWS: Platform-managed key injection
GCP: User-managed key injection via startup script
```

***

## Instance Launch Command

```
gcloud compute instances create bastion-host \
  --zone=us-central1-a \              ← ZONE, not region
  --machine-type=e2-micro \           ← 1 vCPU, 1GB RAM
  --subnet=<PUBLIC_SUBNET> \          ← which subnet
  --tags="bastion" \                  ← firewall matching tag
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \   ← Google's Ubuntu images
  --metadata-from-file=startup-script=bastion.sh  ← runs on first boot
```

***

## Verification: What One SSH Test Proves

```
ssh -i gcp devops@<IP> → sudo -i → apt update

This single test validates:
  ├── VPC              ✓ (network exists and routes)
  ├── Public subnet    ✓ (has internet path)
  ├── Firewall rule    ✓ (port 22 allowed from source)
  ├── Tag matching     ✓ (bastion tag → firewall applied)
  ├── Startup script   ✓ (user devops exists, key works, sudo works)
  ├── Cloud NAT/Router ✓ (apt update reaches internet)
  └── Instance health  ✓ (VM is running)
```

***

## GCP Project Gotcha

```
gcloud commands fail with "project not set"?
  → gcloud config set project "$PROJECT_ID"
  Must be set before any compute commands
```

***

## Dynamic IP Warning

```
Source restricted to YOUR_IP/32 in firewall rule
  → Your ISP changes your public IP periodically
  → SSH suddenly fails (timeout)
  → Fix: Edit firewall rule → update to current IP → save
  
Find current IP: Google "what is my IP"
```

***

## GUI Snapshot Cost Warning

```
GUI → Data protection → Snapshot schedule
  Default may have snapshots ENABLED
  If instance not deleted → snapshots accumulate → ~$6/month/10GB
  
Always check: Set to "No backup" if not needed
```

***

## Operational Flow

```
── SET VARIABLES ──
VPC, SSH_KEY, MY_IP, TAG_BASTION, TAG_APP, PROJECT_ID
gcloud config set project "$PROJECT_ID"

── CREATE FIREWALLS ──
1. allow-ssh-internet:  tcp:22,  source=MY_IP,        target=bastion,  INGRESS
2. allow-ssh-bastion:   tcp:22,  source-tag=bastion,   target=app,     INGRESS
3. allow-elb-to-app:    tcp:8080, source=LB_IP_ranges, target=app,     INGRESS

── PREPARE STARTUP SCRIPT ──
Create bastion.sh → useradd + sudoers + SSH key injection

── LAUNCH BASTION ──
gcloud compute instances create bastion-host \
  → zone, machine-type, subnet (public), tags (bastion), image, startup-script

── VERIFY ──
ssh -i gcp devops@<IP> → sudo -i → apt update → all layers confirmed

── KEEP RUNNING → needed for Cloud SQL init in next lecture
```

***

## Reusable Engineering Patterns

| Pattern                                | Manifestation                                                          |
| -------------------------------------- | ---------------------------------------------------------------------- |
| **Tag-based declarative binding**      | Firewall rules bind to instances via tags, not direct selection        |
| **Bastion/jump host**                  | Single public entry point → all private access goes through it         |
| **Layered firewall architecture**      | Internet→bastion (rule 1), bastion→app (rule 2), LB→app (rule 3)       |
| **Source identity referencing**        | Source tag = trust by group membership, not by IP address              |
| **Known IP range trust**               | GCP LB ranges are documented → use as source for backend access        |
| **Startup script provisioning**        | User, key, and sudo setup automated at boot — no manual SSH config     |
| **Single-test multi-layer validation** | One SSH+apt test verifies VPC, subnet, firewall, NAT, script, instance |

***

## Core Mental Model

```
GCP Network Security = Tag-based declarative matching
  Firewall rule declares: "I apply to tag X, I allow from tag Y / IP range Z"
  Instance declares: "I have tag X"
  GCP matches them automatically → no manual attachment

Traffic flow control:
  Internet → bastion (only SSH)
  bastion → app (only SSH, identity-based)
  LB → app (only 8080, range-based)
  Everything else → DENIED by default

Key injection:
  GCP = you manage it (startup script)
  AWS = platform manages it (key pair selection)
```

***

This material captures every firewall rule, CLI command, GCP-vs-AWS distinction, security warning, GUI detail, and verification pattern from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
