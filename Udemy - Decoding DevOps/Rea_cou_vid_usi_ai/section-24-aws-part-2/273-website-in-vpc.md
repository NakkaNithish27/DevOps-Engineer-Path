# 🌐 AWS VPC — Hosting a Website in a Private Subnet with Load Balancer — Deep Learning Material

**Source:** *Website in VPC* (Video Lecture Caption File) [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Architecture — What We Are Building and Why

This lecture brings together every VPC concept covered in previous lectures into a complete, working system. The architecture is: a **web server running in a private subnet** (no public IP, no direct internet access) with a **load balancer in the public subnet** that routes internet traffic to it. Access to the web server for administration is exclusively through the **bastion host** (also in the public subnet) via SSH. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

This is the standard production architecture for web applications on AWS: application servers are never directly exposed to the internet. They sit in private subnets, protected by security groups, reachable only through controlled entry points — the load balancer for user traffic and the bastion host for administrator access. This separation is the fundamental reason VPCs have public and private subnets.

***

## 1.2 The Bastion Host SSH Chain — Why Two Hops Are Required

An instance in a private subnet has **no public IP** and **no route to the internet gateway**. You cannot SSH to it directly from your laptop because your laptop is on the internet, and the private subnet is, by design, unreachable from the internet. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

The solution is a **two-hop SSH chain**: your laptop → bastion host (in the public subnet, has a public IP) → private instance (in the private subnet, has only a private IP). The bastion host acts as a bridge — it exists in the VPC and can reach both the internet (via its public IP and the internet gateway) and the private subnet (via internal VPC routing).

For this chain to work, the **login key for the private instance must be present on the bastion host**. You can't use a key stored on your laptop to authenticate to the private instance because you're not connecting directly — you're connecting from the bastion host. So the key must be **copied to the bastion host** using `scp` (secure copy). [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

🔍 **Deep Dive:**
The instructor creates a **separate key pair** (`web-key`) for the private instance, distinct from the bastion host's key. This is a security practice: if the bastion host is compromised, the attacker has the web-key, but that key only grants access to the web server — not to other infrastructure. Each layer has its own credentials, limiting blast radius.

⚠️ **Expert Note:**
After copying the key to the bastion host via `scp`, the file permissions change. SSH requires private keys to have restrictive permissions (`400` — read-only by owner). The instructor hits this error: `"Unprotected private key file"` — SSH refuses to use a key with overly permissive permissions. The fix is `chmod 400 web-key.pem`. This is a common stumbling block when transferring keys between machines.

***

## 1.3 VPC Internal Routing — How Public and Private Subnets Communicate

A critical concept the instructor emphasizes: **resources within the same VPC, regardless of which subnet they're in, can access each other by default**, provided the security group rules allow it. The bastion host (public subnet) can reach the web server (private subnet) because they're both in the same VPC. The traffic routes through the VPC's internal routing tables — no internet gateway or NAT gateway is involved in this intra-VPC communication. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

The route table entries handle this: every route table in a VPC has a **local route** (automatically created, cannot be deleted) that covers the VPC's entire CIDR block. This local route ensures that any traffic destined for any IP within the VPC stays within the VPC and is routed internally.

So the question is not "can the bastion host reach the private instance?" (it always can, at the network level). The question is "does the security group on the private instance allow the traffic?" — and that's what the security group rules control.

***

## 1.4 Security Group Design — Three Layers of Access Control

This lecture creates a complete security group architecture with three distinct groups, each controlling a different type of access: [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**1. Bastion host security group** (created in a previous lecture): Allows SSH (port 22) from your IP. This is the entry point for administrative access.

**2. Web server security group (`web01-sg`)**: Two rules:

* **SSH (port 22) from the bastion host security group** — NOT from "My IP" or "Anywhere." The instructor explicitly says: "SSH from anywhere, definitely not from my IP. Also not possible because you cannot SSH from your IP to this private instance." The only SSH path is through the bastion host, so the source must be the bastion's security group.
* **HTTP (port 80) from the load balancer security group** — This rule is added **after** the load balancer is created (because the LB security group doesn't exist yet during instance creation). This is the same temporal dependency pattern seen in the re-architecture project.

**3. Load balancer security group (`web-elb-sg`)**: Allows HTTP (port 80) from anywhere (IPv4 and IPv6). The load balancer is the public-facing entry point for user traffic, so it must accept connections from the entire internet. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

The security group chaining enforces the traffic flow: **Internet → LB SG (port 80) → Web SG (port 80 from LB SG)**. No other path exists. The web server cannot be reached directly from the internet on any port.

***

## 1.5 The Load Balancer — Bridging Public and Private Subnets

The **Application Load Balancer (ALB)** sits in the **public subnets** and routes traffic to instances in the **private subnets**. This is the mechanism that makes the website accessible from the internet even though the web server has no public IP and no internet gateway route. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

The load balancer must be placed in the **public subnets** — the instructor stresses this: "This is extremely important. Otherwise the load balancer also goes into the private subnet, load balancer will be inaccessible from the internet." When creating the ALB, you select the VPC, then for each availability zone, you must select the **public subnet**, not the private one.

The ALB needs to be in at least **two availability zones** — the instructor selects public subnet 1 and public subnet 2. This is an AWS requirement for ALBs: they must span multiple AZs for high availability. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

The **target group** connects the load balancer to the web server. You create a target group, add the web server instance to it, and then configure the ALB to forward traffic to this target group on port 80. The target group also performs **health checks** — it periodically sends HTTP requests to the instance to verify it's responding. If the instance is healthy, traffic is routed to it. If unhealthy, traffic is withheld. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## 1.6 Why a Public IP Won't Help — The NAT Gateway Is for Outbound Only

The instructor makes a point that even if you assigned a public IP to the private instance, it wouldn't make the website accessible from the internet. The private subnet's route table routes internet-bound traffic through the **NAT gateway**, and the NAT gateway only supports **outbound** connections (instances reaching the internet) — it does not allow **inbound** connections (the internet reaching instances). [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

This is a common misunderstanding: a public IP on a private-subnet instance does NOT make it publicly accessible. Public accessibility requires a route through the **internet gateway** (which only the public subnet has) and the appropriate security group rules. The private subnet's route table points to the NAT gateway for outbound traffic, not the internet gateway.

***

## 1.7 The Target Group Health Check — Unhealthy Troubleshooting

After creating the load balancer and target group, the instructor waits for the instance to become **healthy** in the target group. If it shows **unhealthy**, the most common cause is: the security group on the instance doesn't allow port 80 from the load balancer security group. The health check sends HTTP requests to the instance on port 80 — if those requests are blocked by the security group, the health check fails, and the instance stays unhealthy. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

This is the same troubleshooting pattern from earlier lectures: if the load balancer can't reach the instance, check the instance's security group for the correct inbound rule (port 80 from the LB SG).

***

## 1.8 Cleanup — Cost-Aware Resource Management

The instructor walks through a deliberate cleanup process, distinguishing between **resources that cost money** and **resources that are free**: [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**Must delete (costs money):**

* Load balancer
* EC2 instances (bastion host, web server)
* NAT gateway (charges per hour + data processing)
* Elastic IP (charges when not associated with a running instance)

**Keep (no charges):**

* VPC
* Subnets
* Internet gateway
* Route tables

The instructor explicitly says: "Do not delete the VPC, subnets, internet gateway, and route table. We will need this in the next lecture" (VPC peering). [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**NAT gateway deletion order:** Delete the NAT gateway first, wait for it to fully delete, then release the Elastic IP. The Elastic IP cannot be released while the NAT gateway still references it — even after deletion, it takes time for the association to fully clear.

**Route table impact:** After deleting the NAT gateway, the private route table's NAT gateway route shows **"black hole"** — the route exists but points to a resource that no longer exists. When you recreate the NAT gateway, you update this route to point to the new NAT gateway. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are launching a web server in a VPC private subnet, installing a website on it (from tooplate.com), creating a load balancer in the public subnet to serve the website to the internet, and establishing the full SSH access chain through the bastion host. After this, the website will be accessible via the load balancer's DNS name, while the web server itself remains completely hidden from the internet. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## Step 1: Create a Key Pair for the Web Server

Go to **EC2 → Key Pairs → Create key pair**.

**Name:** `web-key`
**Format:** `.pem`

Click **Create key pair**. The key downloads automatically. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**Why a separate key?** This key is specifically for the private-subnet instance. The bastion host has its own key. Separate keys per tier limits blast radius.

***

## Step 2: Copy the Key to the Bastion Host

If you're currently SSH'd into the bastion host, **exit** first (you need to run `scp` from your local machine).

```bash
scp -i <path-to-bastion-key> ~/Downloads/web-key.pem ubuntu@<bastion-public-ip>:/home/ubuntu/
```

* `scp` — secure copy over SSH
* `-i <path-to-bastion-key>` — authenticate to the bastion host using its key
* `~/Downloads/web-key.pem` — the file to copy (the web server's key)
* `ubuntu@<bastion-public-ip>` — destination user and host
* `:/home/ubuntu/` — destination directory on the bastion host (Ubuntu user's home directory — the user has write permission here)

**Expected output:** Transfer progress indicator showing the file was copied successfully. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## Step 3: SSH into the Bastion Host and Verify the Key

```bash
ssh -i <path-to-bastion-key> ubuntu@<bastion-public-ip>
```

Once connected:

```bash
ls
```

You should see `web-key.pem` in the home directory. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## Step 4: Launch the Web Server Instance in the Private Subnet

Go to **EC2 → Launch Instance**.

| Setting       | Value                                                       |
| ------------- | ----------------------------------------------------------- |
| Name          | `web01-priv`                                                |
| AMI           | Amazon Linux 2                                              |
| Instance type | t2.micro                                                    |
| Key pair      | `web-key` (the key created in Step 1 — NOT the bastion key) |

**Network settings → Edit:**

| Setting               | Value                                                          |
| --------------------- | -------------------------------------------------------------- |
| VPC                   | `vprofile-VPC`                                                 |
| Subnet                | Private subnet 1 (or 2)                                        |
| Auto-assign public IP | Disabled (automatic — private subnets don't assign public IPs) |

**Create a new security group:**

| Setting | Value                                                                                       |
| ------- | ------------------------------------------------------------------------------------------- |
| Name    | `web01-sg`                                                                                  |
| Rule 1  | SSH (22) from **bastion host security group** (select Custom → type `sg` → pick bastion SG) |

**Do NOT add port 80 rule yet** — the load balancer security group doesn't exist yet. We'll add it later. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

Click **Launch instance**.

**Verification:** The instance will show **no public IP** in the console — only a private IP. This confirms it's correctly placed in the private subnet.

***

## Step 5: SSH from the Bastion Host to the Web Server

From the bastion host terminal, first fix the key permissions:

```bash
chmod 400 web-key.pem
```

* `chmod 400` — sets file permissions to read-only by owner. SSH requires this restrictive permission on private keys.

**Common error without this step:** `"WARNING: UNPROTECTED PRIVATE KEY FILE!"` — SSH refuses to use the key because the permissions are too open (the `scp` copy changed them). [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

Now SSH to the web server using its **private IP**:

```bash
ssh -i web-key.pem ec2-user@<web01-private-ip>
```

* `ec2-user` — the default username for Amazon Linux 2 AMIs (not `ubuntu` — that's for Ubuntu AMIs)
* `<web01-private-ip>` — get this from the EC2 console

Type `yes` when prompted. You should be logged into the Amazon Linux 2 instance. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**Why this works:** Both instances are in the same VPC. The VPC's local route handles the traffic. The bastion's traffic to the web server's private IP stays within the VPC — no internet gateway or NAT gateway involved. The web server's security group allows port 22 from the bastion's security group. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## Step 6: Set Up the Website on the Web Server

**Install required packages:**

```bash
sudo yum install httpd wget unzip -y
```

* `httpd` — Apache HTTP Server (the web server software)
* `wget` — command-line download tool (to download the website template)
* `unzip` — to extract the downloaded ZIP file

**Download the website template:**

Go to **tooplate.com** in your browser. Choose a template. Press **F12** (developer tools) → click **Download** → find the download URL in the Network tab → copy the URL. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

On the web server:

```bash
wget <template-download-URL>
```

**Extract and deploy:**

```bash
ls                                    # find the downloaded zip filename
unzip <filename>.zip                  # extract the template
cp -r <extracted-folder>/* /var/www/html/   # copy to Apache's document root
```

**Start and enable Apache:**

```bash
sudo systemctl restart httpd
sudo systemctl enable httpd
```

* `restart` — starts the service (or restarts if already running)
* `enable` — ensures the service starts automatically on boot [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**The website is now running** on the private instance, but there's no way to access it from the internet yet. No public IP, no internet gateway route. The load balancer is needed.

***

## Step 7: Create the Target Group

Go to **EC2 → Target Groups → Create target group**.

| Setting       | Value          |
| ------------- | -------------- |
| Target type   | Instances      |
| Name          | `web-tg`       |
| Protocol/Port | HTTP / 80      |
| VPC           | `vprofile-VPC` |

Click **Next**. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

Select the `web01-priv` instance → click **Include as pending below** → click **Create target group**.

***

## Step 8: Create the Load Balancer Security Group

Go to **EC2 → Security Groups → Create security group**.

| Setting | Value                                                        |
| ------- | ------------------------------------------------------------ |
| Name    | `web-elb-sg`                                                 |
| VPC     | `vprofile-VPC` (**always select your VPC, not the default**) |
| Rule 1  | HTTP (80) from Anywhere-IPv4                                 |
| Rule 2  | HTTP (80) from Anywhere-IPv6                                 |

Click **Create security group**. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## Step 9: Create the Application Load Balancer

Go to **EC2 → Load Balancers → Create load balancer → Application Load Balancer**.

| Setting | Value                     |
| ------- | ------------------------- |
| Name    | (give a descriptive name) |
| Scheme  | Internet-facing           |
| VPC     | `vprofile-VPC`            |

**Network mapping — ⚠️ CRITICAL:**

For each availability zone, select the **PUBLIC subnet**:

* Zone 1 → `public subnet 1`
* Zone 2 → `public subnet 2`

**Do NOT select private subnets.** If the load balancer is placed in private subnets, it cannot receive internet traffic and the website will be inaccessible. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

| Setting        | Value                         |
| -------------- | ----------------------------- |
| Security group | `web-elb-sg`                  |
| Listener       | HTTP:80 → forward to `web-tg` |

Click **Create load balancer**. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## Step 10: Add Port 80 Rule to the Web Server Security Group

Now that the load balancer security group exists, add the deferred rule.

Go to **EC2 → Security Groups** → select `web01-sg` → **Edit inbound rules** → **Add rule**:

| Type | Port | Source                                      |
| ---- | ---- | ------------------------------------------- |
| HTTP | 80   | `web-elb-sg` (load balancer security group) |

Click **Save rules**. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**This completes the security chain:** Internet → LB SG (port 80 from anywhere) → Web SG (port 80 from LB SG).

***

## Step 11: Verify and Access the Website

**Wait 5-10 minutes** for the load balancer to become **Active** and the target group instance to become **Healthy**. [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**If the instance stays Unhealthy:**

* Check the security group on `web01-priv` — it must allow port 80 from the load balancer security group
* Verify Apache (`httpd`) is running on the instance
* Wait longer — health checks take time to converge

**Access the website:** Go to **EC2 → Load Balancers** → copy the **DNS name** of the load balancer → paste into a browser.

**Expected result:** The tooplate website template appears. The traffic path: your browser → load balancer (public subnet) → web server (private subnet). [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

***

## Step 12: Cleanup (Cost-Saving)

Delete in this order: [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

1. **Load balancer:** EC2 → Load Balancers → Actions → Delete
2. **Instances:** EC2 → Instances → select all → Instance state → Terminate
3. **NAT gateway:** VPC → NAT Gateways → Actions → Delete NAT gateway → type `delete` to confirm
4. **Wait** for NAT gateway to fully delete (state shows "Deleted")
5. **Elastic IP:** VPC → Elastic IPs → Actions → Release Elastic IP address

**Do NOT delete:** VPC, subnets, internet gateway, route tables — these are free and needed for the next lecture (VPC peering). [\[273-website-in-vpc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/273-website-in-vpc.txt)

**After NAT gateway deletion:** The private route table's NAT gateway route shows **"black hole"**. This is expected. When you recreate the NAT gateway, update this route to point to the new one.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Full Architecture

```
INTERNET
  │
  ▼ (HTTP 80 — from anywhere)
[ALB — web-elb-sg — PUBLIC subnet 1 + 2]
  │
  ▼ (HTTP 80 — source: web-elb-sg)
[Web Server — web01-sg — PRIVATE subnet]
  ▲
  │ (SSH 22 — source: bastion-sg)
[Bastion Host — bastion-sg — PUBLIC subnet]
  ▲
  │ (SSH 22 — from My IP)
[Your Laptop]
```

## SSH Access Chain

```
Laptop → (bastion key) → Bastion Host → (web-key, copied via scp) → Web Server

Key storage:
  Bastion key: on your laptop
  Web key: on your laptop (for scp) AND on bastion host (for SSH hop)

chmod 400 web-key.pem ← REQUIRED after scp (fixes permissions)
```

## SCP Command Structure

```
scp -i <bastion-key> <file-to-copy> ubuntu@<bastion-ip>:/home/ubuntu/

-i = authenticate to bastion with bastion's key
<file-to-copy> = the web server's key (web-key.pem)
destination = bastion host's home directory
```

## Security Group Chain

```
bastion-sg:    SSH(22) ← My IP
web01-sg:      SSH(22) ← bastion-sg     (admin access via bastion)
               HTTP(80) ← web-elb-sg    (user traffic via LB)
web-elb-sg:    HTTP(80) ← anywhere      (internet-facing)

RULE: web01-sg NEVER allows traffic from "anywhere" or "My IP"
      ALL access is through intermediaries (bastion or LB)
```

## Load Balancer Placement — Critical

```
ALB MUST go in PUBLIC subnets (subnet 1 + subnet 2)
  → requires 2 AZs minimum
  → if placed in private subnets → inaccessible from internet

"This is extremely important. Otherwise the load balancer
 also goes into the private subnet, load balancer will
 be inaccessible from the internet."
```

## Why Public IP on Private Instance Doesn't Work

```
Private subnet route table → NAT gateway (outbound only)
NAT gateway does NOT support inbound connections
Public IP + NAT gateway route = outbound works, inbound blocked

Only way to receive internet traffic:
  → route through internet gateway (only in public subnet route table)
  → or use load balancer in public subnet as proxy
```

## VPC Internal Routing

```
Resources in SAME VPC can communicate regardless of subnet
  → local route in every route table covers entire VPC CIDR
  → traffic stays within VPC (no IGW/NAT needed)
  → ONLY requirement: security group rules allow it

Bastion (public) → Web Server (private) = works via local route
  IF web01-sg allows SSH from bastion-sg ✓
```

## Target Group Health Check

```
LB sends HTTP requests to instance on port 80
  ├─ Healthy: instance responds → LB routes traffic
  └─ Unhealthy: no response → LB withholds traffic

UNHEALTHY troubleshooting:
  1. Security group on instance allows port 80 from LB SG?
  2. httpd service running on instance?
  3. Wait longer (health checks need time)
```

## Website Setup Commands (Amazon Linux 2)

```
yum install httpd wget unzip -y
wget <template-URL>
unzip <file>.zip
cp -r <folder>/* /var/www/html/
systemctl restart httpd
systemctl enable httpd
```

## Cleanup — Cost vs. Free

```
DELETE (costs money):
  1. Load balancer
  2. EC2 instances
  3. NAT gateway → wait for full deletion
  4. Elastic IP → release AFTER NAT gateway deleted

KEEP (free, needed for next lecture):
  - VPC
  - Subnets
  - Internet gateway
  - Route tables

After NAT gateway deletion:
  Private route table → NAT route shows "black hole"
  Fix later: create new NAT gateway → update route
```

## Temporal Dependency (Recurring Pattern)

```
web01-sg port 80 rule needs LB SG as source
LB SG doesn't exist during instance creation
  → create instance with SSH rule only
  → create LB + LB SG
  → THEN add port 80 rule to web01-sg

Same pattern as: re-architecture backend SG + Beanstalk SG
```

## AMI → Username Map

```
Amazon Linux 2: ec2-user
Ubuntu:         ubuntu

Wrong username = "Permission denied" on SSH
```

## Reusable Engineering Patterns

**1. Private Compute + Public Proxy**

```
Application servers → private subnet (no direct internet access)
Load balancer → public subnet (internet-facing proxy)

Pattern: never expose application instances directly
         always proxy through a controlled entry point
Same in: any production web architecture, K8s Ingress + pods
```

**2. Two-Hop Administrative Access**

```
Laptop → Bastion (public) → Target (private)
Key must exist at each hop point
Permissions must be restrictive (chmod 400)

Pattern: jump host / bastion host pattern
Same in: any secure network with DMZ architecture
```

**3. Deferred Security Rule (Cross-Reference After Creation)**

```
Resource A needs rule referencing Resource B
Resource B doesn't exist yet
  → Create A with partial rules
  → Create B
  → Edit A → add rule referencing B

Pattern: temporal dependency in resource creation
Applies to: any system with cross-referencing identities
```

***

*This completes the full reconstruction. Theory explains the architecture of private-subnet hosting with load balancer access and the bastion SSH chain. Practical walks through every step from key creation to website access to cleanup. The Compression Map enables instant recall of the full architecture, the security group chain, and the critical ALB placement requirement.* <cite>turn14search17</cite>
