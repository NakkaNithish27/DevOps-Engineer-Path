# 🔐 AWS Security Groups & Key Pairs — Deep Learning Material

**Source:** *Security Group & Keypairs* (Video Lecture Caption File) [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Architecture We Are Securing

The vprofile application is a multi-tier web application deployed on AWS. Its traffic flow follows a strict layered path:

**Internet → Application Load Balancer → Tomcat Application Servers → Backend Services (MySQL, Memcache, RabbitMQ)**

Each layer exists on separate EC2 instances. The critical engineering question is: **how do we control which layer is allowed to talk to which, and on what port?** This is the problem that AWS Security Groups solve in this architecture. Without security groups, every instance would be reachable from everywhere — a massive security exposure. Security groups act as **virtual firewalls attached to individual instances**, controlling exactly what traffic is allowed in and out. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

The three distinct tiers map to three distinct security groups, each with its own set of rules tuned to the role of that tier. This is not arbitrary — it directly mirrors the application's traffic flow and the principle of **least privilege**: each layer should only accept traffic from the layer directly in front of it, and nothing else. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## 1.2 What Is an AWS Security Group?

A security group is a **stateful virtual firewall** that controls inbound and outbound traffic for EC2 instances. Every rule you define specifies a port (or port range), a protocol, and a source (for inbound) or destination (for outbound).

The critical mental model here is: **a security group is NOT a container**. You do not "put instances inside" a security group. Instead, when you launch an EC2 instance and assign it a security group, that instance **borrows all the rules** defined in that security group. The rules become part of the instance's own network behavior. This distinction matters because it changes how you think about inter-instance communication — if Instance A and Instance B share the same security group, they don't automatically talk to each other. Communication still depends on whether the rules explicitly permit traffic between them. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

🔍 **Deep Dive:**
The "borrowing" model means security group rules are evaluated at the instance's network interface level, not at some external perimeter. When you modify a security group's rules, the change applies immediately to all instances using that security group — there's no restart, no reattachment needed. This is powerful but also dangerous: a misconfiguration instantly affects every associated instance.

⚠️ **Expert Note:**
In production, the fact that security groups are stateful means if you allow an inbound request on port 8080, the response traffic is automatically allowed out — you don't need a matching outbound rule for response packets. This is why the instructor emphasizes: **do not touch the outbound rules**. The default outbound rule allows all outgoing traffic, which ensures instances can reach the internet (for package updates, DNS resolution, etc.). If you restrict outbound rules without understanding this, your instances will silently break. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## 1.3 Inbound Rules vs. Outbound Rules

**Inbound rules** control what traffic is allowed to **reach** the instance. This is where all the security design happens in this lecture. You specify: which port, which protocol, and from which source.

**Outbound rules** control what traffic the instance is allowed to **send out**. The default allows all outbound traffic to all destinations. The instructor explicitly warns: **do not modify outbound rules** — if you restrict them, the instance won't be able to reach the internet, pull updates, or even respond to legitimate inbound connections (in edge cases where statefulness doesn't cover certain traffic patterns). [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

The entire security design in this architecture is built exclusively through inbound rules. Outbound remains permissive by default.

***

## 1.4 Security Group Chaining — Source as Another Security Group

This is the most important engineering concept in the lecture. Instead of specifying an IP address or CIDR block as the source of an inbound rule, you can specify **another security group** as the source.

**What this means:** When you create a rule on the backend security group that says "allow port 3306 from the app security group," you're saying: any instance that is associated with the app security group is allowed to connect to port 3306 on any instance associated with the backend security group. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**Why this is powerful:** You never have to know or hardcode the private IP addresses of your Tomcat instances. If you scale horizontally and add 10 more Tomcat instances, as long as they use the same app security group, they're automatically allowed to reach the backend. The rule is **identity-based** (tied to the security group membership), not **address-based** (tied to specific IPs). [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**The chain in this architecture:**

* Load Balancer SG → allows HTTP/HTTPS from **anywhere** (the internet)
* App SG → allows port 8080 from **Load Balancer SG** (only the load balancer can reach Tomcat)
* Backend SG → allows ports 3306, 11211, 5672 from **App SG** (only Tomcat instances can reach backend services)

This creates a **layered security chain** where each tier only trusts the tier directly upstream. No tier can be reached by skipping a layer. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

🔍 **Deep Dive:**
This chaining pattern is a form of **micro-segmentation**. Even if an attacker compromises the load balancer, they cannot directly reach backend services because the backend SG only allows traffic from the app SG. The attacker would need to compromise each layer sequentially. This dramatically increases the difficulty of lateral movement inside the infrastructure.

***

## 1.5 Self-Referencing Security Group — Internal Peer Communication

After creating the backend security group, the instructor adds one more rule: **all traffic allowed from the backend security group itself**. This is a self-referencing rule. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**Why it's needed:** The backend services (MySQL, Memcache, RabbitMQ) run on separate instances but may need to communicate with each other. For example, the instructor mentions Memcache connecting to MySQL. Without this self-referencing rule, MySQL's security group has no rule that says "allow traffic from Memcache's instance." Since both belong to the same backend security group, a self-referencing rule saying "allow all traffic from my own security group" solves this — every backend instance can talk to every other backend instance on any port. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**The tradeoff:** This rule is convenient but opens all ports between backend instances. The instructor notes: **this rule is perfectly safe, provided the instances are not compromised.** If one backend instance is compromised, the attacker has unrestricted access to all other backend instances. In highly sensitive environments, you might replace this with individual port-specific rules between backend services, but for most deployments, the self-referencing approach is standard practice. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## 1.6 Port Numbers and the Application.Properties File

Every service in the backend tier listens on a specific port:

* **MySQL** → port 3306
* **Memcache** → port 11211
* **RabbitMQ** → port 5672
* **Tomcat** → port 8080

The instructor emphasizes: if you're unsure about which ports to use, check the **application.properties** file in the source code. In the vprofile project, this file is located at `src/main/resources/application.properties` and contains the connection strings with the port numbers embedded (e.g., `db01:3306`, `mc01:11211`, `rmq01:5672`). [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

This is an important operational habit: **never guess port numbers — always verify them from the application's configuration.** The application.properties file is the single source of truth for which ports your application expects to use, and your security group rules must match exactly. A mismatch means the application will fail to connect to its backend services, often with cryptic timeout errors.

***

## 1.7 The "My IP" Rule and Dynamic IP Problem

For SSH access (port 22), the instructor uses the **My IP** option in the AWS console. This automatically detects your current public IP address and creates a rule allowing SSH only from that IP. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**The problem:** If you're on a residential broadband connection, your public IP address changes periodically (it's dynamically assigned by your ISP). The next day, your IP might be different, and your SSH rule will block you because it still references yesterday's IP. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**The fix:** Go back to the security group, edit the inbound rule, and select "My IP" again — this updates the rule with your new current IP. The instructor flags this as a common troubleshooting scenario: if you suddenly can't SSH to your instance, the first thing to check is whether your IP has changed. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

⚠️ **Expert Note:**
In production environments, you would never rely on "My IP" for access. Instead, you'd use a bastion host (jump server) with a static Elastic IP, or use AWS Systems Manager Session Manager which requires no inbound SSH rules at all. The "My IP" approach is suitable only for development and learning environments.

***

## 1.8 Why Not "All Traffic from Anywhere"?

The instructor explicitly warns against the lazy approach: opening all traffic from anywhere. He stresses that **understanding the port number of your service and the traffic flow** is essential knowledge for a DevOps engineer. If you allow all traffic from anywhere, any compromised instance or external attacker can reach any service on any port — the security groups become meaningless. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

He also mentions a less extreme but still risky shortcut: instead of adding individual port rules (3306, 11211, 5672) from the app security group, you could add one rule saying "all traffic from app SG." This works, but it means the Tomcat instances can reach backend instances on **any** port, not just the three required. From a security perspective, this violates least privilege — the Tomcat instance should only be able to reach the exact ports it needs. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## 1.9 AWS Key Pairs — Login Credentials for EC2 Instances

A key pair is a cryptographic key used to SSH into EC2 instances. AWS stores the public key, and you download the private key. You use the private key to authenticate when connecting via SSH. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**Two formats:**

* **.pem** — used with Git Bash, macOS Terminal, or any OpenSSH-compatible client
* **.ppk** — used with PuTTY (a Windows SSH client that uses its own key format)

The instructor creates a key pair named `vprofile-prod-key` in `.pem` format because he uses Git Bash. The private key file downloads immediately — this is the only time you can download it. If you lose it, you lose SSH access to any instance launched with that key pair. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## 1.10 IPv4 and IPv6 — Dual Rule Requirement

When creating the load balancer security group, the instructor adds both IPv4 and IPv6 rules for HTTP and HTTPS. This is because internet traffic can arrive over either protocol version. If you only create IPv4 rules, clients connecting over IPv6 will be blocked. For a public-facing load balancer that should accept traffic from **anywhere on the internet**, both versions must be covered. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## 1.11 HTTPS and the Domain Certificate

The load balancer initially allows both HTTP (port 80) and HTTPS (port 443). The instructor mentions that later in the project, HTTP will be removed, leaving only HTTPS. This requires a **domain certificate** that was created in a prerequisite lecture using AWS Certificate Manager. The certificate enables encrypted TLS connections. The plan is: start with HTTP for initial setup/testing, then switch to HTTPS-only once the certificate is attached to the load balancer. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating the **network security layer** for the vprofile application on AWS. This consists of three security groups (one per application tier) and one SSH key pair. After completing this section, the infrastructure will have firewall rules that enforce the correct traffic flow: Internet → Load Balancer → Tomcat → Backend Services, with SSH access restricted to our IP only. The key pair will be ready for use when launching EC2 instances in the next lecture. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## Step 1: Navigate to Security Groups

Go to the **EC2 service** in the AWS Management Console. In the left sidebar, find and click **Security Groups** (it's under the "Network & Security" section). You can also reach it from the EC2 dashboard overview page. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## Step 2: Create the Load Balancer Security Group

Click **Create security group**.

**Name:** `vprofile-ELB-SG`
**Description:** `Security Group for the vprofile load balancer`

Scroll down to **Inbound rules** and click **Add rule**. Add four rules: [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

| Type  | Port | Source        | Purpose                        |
| ----- | ---- | ------------- | ------------------------------ |
| HTTP  | 80   | Anywhere-IPv4 | Accept HTTP from IPv4 clients  |
| HTTP  | 80   | Anywhere-IPv6 | Accept HTTP from IPv6 clients  |
| HTTPS | 443  | Anywhere-IPv4 | Accept HTTPS from IPv4 clients |
| HTTPS | 443  | Anywhere-IPv6 | Accept HTTPS from IPv6 clients |

**Why Anywhere?** This is a public-facing load balancer. It must accept traffic from any client on the internet. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**Why both IPv4 and IPv6?** Internet clients may connect over either protocol. Missing one version means blocking a subset of users.

⚠️ **Critical:** Do NOT modify the **outbound rules**. Leave them at the default (all traffic allowed to all destinations). Changing outbound rules can prevent your instances from accessing the internet entirely. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

Click **Create security group**.

**Connection to the larger flow:** This security group will be attached to the Application Load Balancer when it's created later. It's also referenced as a **source** in the next security group.

***

## Step 3: Create the Application (Tomcat) Security Group

Click **Create security group**.

**Name:** `vprofile-app-sg`
**Description:** `Security group for tomcat app server`

Add inbound rules: [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

| Type       | Port | Source                             | Purpose                                   |
| ---------- | ---- | ---------------------------------- | ----------------------------------------- |
| Custom TCP | 8080 | `vprofile-ELB-SG` (security group) | Allow traffic only from the load balancer |
| SSH        | 22   | My IP                              | Allow SSH from your current IP            |

**How to select a security group as source:** In the "Source" field, type `sg` and a dropdown will appear listing all your security groups. Select `vprofile-ELB-SG`. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**Why port 8080?** Tomcat's default HTTP connector listens on port 8080. This is confirmed in the application.properties file.

**Why "My IP" for SSH?** This restricts SSH access to only your current public IP address, preventing unauthorized SSH connections from other IPs.

**Optional description field:** You can add `Allows traffic from vprofile load balancer` for the 8080 rule for documentation clarity. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

⚠️ **Do NOT touch outbound rules.** Click **Create security group**.

**Troubleshooting — SSH not working the next day:** If you're on broadband, your public IP may change overnight. Go back to this security group → Edit inbound rules → Delete the old SSH rule → Add a new SSH rule with "My IP" to update to your current IP. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**Connection to the larger flow:** This security group will be assigned to the Tomcat EC2 instances. It's also referenced as a **source** in the backend security group.

***

## Step 4: Create the Backend Security Group

Click **Create security group**.

**Name:** `vprofile-backend-sg`
**Description:** `Security group for mysql, memcache & rabbitmq allowed from tomcat app server`

Add inbound rules: [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

| Type                         | Port  | Source                             | Purpose                          |
| ---------------------------- | ----- | ---------------------------------- | -------------------------------- |
| MYSQL/Aurora (or Custom TCP) | 3306  | `vprofile-app-sg` (security group) | MySQL access from Tomcat only    |
| Custom TCP                   | 11211 | `vprofile-app-sg` (security group) | Memcache access from Tomcat only |
| Custom TCP                   | 5672  | `vprofile-app-sg` (security group) | RabbitMQ access from Tomcat only |
| SSH                          | 22    | My IP                              | SSH access from your current IP  |

**How to find the correct ports:** Navigate to the vprofile source code repository, switch to the `awsliftandshift` branch, and open `src/main/resources/application.properties`. The connection strings show: `db01:3306`, `mc01:11211`, `rmq01:5672`. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**Source selection — be careful:** For ports 3306, 11211, and 5672, the source must be `vprofile-app-sg` (the **application** security group), NOT the load balancer security group. The backend services should only be reachable from Tomcat instances, not from the load balancer. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**The shortcut the instructor mentions (and warns against):** Instead of three separate port rules, you could add one rule: "All traffic" from `vprofile-app-sg`. This works functionally but violates least privilege — Tomcat would be allowed to reach any port on backend instances, not just the three it needs. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

⚠️ **Do NOT touch outbound rules.** Click **Create security group**.

***

## Step 5: Add the Self-Referencing Rule to the Backend Security Group

After creation, the backend security group needs one more rule to allow backend instances to communicate with each other (e.g., Memcache connecting to MySQL). [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

1. Go back to the Security Groups list
2. Select `vprofile-backend-sg`
3. Click **Edit inbound rules**
4. Click **Add rule**
5. Set:
   * **Type:** All traffic
   * **Source:** `vprofile-backend-sg` (select itself)
6. Click **Save rules**

**Why this is a separate step:** You can't reference a security group as a source during its own creation (it doesn't exist yet). You must create it first, then edit it to add the self-referencing rule. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

**What this achieves:** Every instance assigned to `vprofile-backend-sg` can now communicate with every other instance in the same security group on any port. This covers inter-service communication (MySQL ↔ Memcache ↔ RabbitMQ) without needing to specify individual cross-service port rules.

**Verification:** After saving, review the inbound rules for `vprofile-backend-sg`. You should see 5 rules total: MySQL (3306), Memcache (11211), RabbitMQ (5672), SSH (22), and All Traffic (self-reference). [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

⚠️ **Expert Note:**
The self-referencing "All Traffic" rule is safe as long as none of the backend instances are compromised. In a high-security environment, you would replace this with explicit port-to-port rules between each service pair, but the operational complexity increases significantly.

***

## Step 6: Create the Key Pair

Navigate to **Key Pairs** in the EC2 console (under "Network & Security" in the left sidebar).

Click **Create key pair**.

**Name:** `vprofile-prod-key`
**Format:** `.pem`

The instructor chooses `.pem` because he uses Git Bash (or a Unix-like terminal). If you use **PuTTY** on Windows, select `.ppk` instead. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

Click **Create key pair**. The private key file downloads automatically to your browser's default download location.

**Critical:** This is the **only time** the private key can be downloaded. Store it securely. If lost, you cannot recover it and will lose SSH access to instances launched with this key pair.

**Connection to the larger flow:** This key pair will be specified when launching EC2 instances in the next lecture. Combined with the SSH rules (port 22 from My IP) in the app and backend security groups, it enables secure terminal access to all instances. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

## Final State Summary

After completing all steps, your AWS account should have:

| Resource       | Name                  | Purpose                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------- |
| Security Group | `vprofile-ELB-SG`     | Load Balancer — HTTP/HTTPS from internet                                                    |
| Security Group | `vprofile-app-sg`     | Tomcat — port 8080 from LB SG, SSH from My IP                                               |
| Security Group | `vprofile-backend-sg` | Backend services — ports 3306/11211/5672 from App SG, SSH from My IP, all traffic from self |
| Key Pair       | `vprofile-prod-key`   | SSH authentication for all EC2 instances                                                    |

These resources form the **security foundation** on top of which EC2 instances will be launched and configured in the next lecture. [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Architecture Chain

```
Internet
  │
  ▼ (HTTP 80 / HTTPS 443 — from anywhere IPv4+IPv6)
[ALB — vprofile-ELB-SG]
  │
  ▼ (TCP 8080 — source: ELB-SG only)
[Tomcat Instances — vprofile-app-sg]
  │
  ▼ (TCP 3306 / 11211 / 5672 — source: app-sg only)
[Backend Instances — vprofile-backend-sg]
  │
  ↺ (All traffic — source: self — inter-service communication)
```

## Security Group Mental Model

```
SG ≠ container
SG = rule template → instances BORROW rules
Modify SG → instantly affects ALL associated instances
Stateful → inbound allow = automatic outbound response
```

## Rule Design Pattern

```
Each tier's SG allows traffic ONLY from the tier directly upstream:
  LB SG    ← anywhere (public-facing)
  App SG   ← LB SG (chained)
  Back SG  ← App SG (chained)

SSH (22) ← My IP (all tiers, management access)
Self-ref ← backend SG only (peer communication)
```

## Port → Service Map

```
80    → HTTP (ALB)
443   → HTTPS (ALB, after certificate)
8080  → Tomcat
3306  → MySQL
11211 → Memcache
5672  → RabbitMQ
22    → SSH
```

**Source of truth for ports:** `src/main/resources/application.properties`

## Key Pair Quick Reference

```
Name: vprofile-prod-key
.pem → Git Bash / Terminal / OpenSSH
.ppk → PuTTY
One-time download only → store securely
```

## Operational Gotchas

```
Can't SSH?
  → Check if IP changed (broadband = dynamic IP)
  → Fix: Edit SG rule → re-select "My IP"

Outbound rules:
  → NEVER modify → default = allow all out
  → Breaking outbound = instance loses internet

Self-ref rule:
  → Can't add during SG creation (SG doesn't exist yet)
  → Must add AFTER creation via Edit Inbound Rules

Source selection:
  → Backend rules source = App SG (NOT LB SG)
  → Common mistake: selecting wrong SG in dropdown
```

## Reusable Engineering Patterns

**1. Layered Trust Chain**

```
Each layer trusts only its immediate upstream → no layer-skipping
Internet → LB → App → Backend
Compromise at layer N does NOT give access to layer N+2
```

**2. Identity-Based Access (SG as Source)**

```
Rules reference SG identity, not IP addresses
→ Auto-scales: new instances with same SG = auto-permitted
→ No hardcoded IPs → no rule updates on scaling
```

**3. Self-Referencing for Peer Mesh**

```
Same-tier instances need mutual communication?
→ SG allows all traffic from itself
→ Creates implicit peer mesh within the tier
→ Tradeoff: convenience vs. blast radius if compromised
```

**4. Configuration-Driven Security**

```
Port numbers don't come from memory
→ They come from application config (application.properties)
→ Security rules must MIRROR application config
→ Mismatch = silent connection failures (timeouts)
```

**5. Progressive Security Tightening**

```
Start permissive (HTTP + HTTPS) → Tighten later (HTTPS only)
Enables initial testing → Enforces production security
Certificate attachment triggers the transition
```

***

*This completes the full reconstruction of the video content. All three sections are designed to be complementary — Theory builds understanding, Practical enables execution, and the Compression Map enables rapid future recall without re-reading the full material.* [\[133. Secur...& Keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/133.%20Security%20Group%20%26%20Keypairs.txt)
