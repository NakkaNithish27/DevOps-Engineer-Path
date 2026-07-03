# 🔐 AWS Re-Architecture — Backend Security Group & Key Pair — Deep Learning Material

**Source:** *Security Group and Keypairs* (vprofile Re-Architecture Project Lecture) [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Architectural Shift — From Lift & Shift to Re-Architecture

In the previous project (lift and shift), we manually created **three security groups** (load balancer, application, backend), launched raw EC2 instances, installed all software ourselves, and managed the entire infrastructure. Every security group, every rule, every port mapping was our responsibility.

In this re-architecture project, the approach fundamentally changes. The application tier is now managed by **Elastic Beanstalk**, and the backend services are replaced by **AWS managed services**: Amazon RDS (replacing MySQL), ElastiCache (replacing Memcache), and Amazon MQ (replacing RabbitMQ). This means we are no longer managing individual EC2 instances for backend services — AWS handles the compute, patching, scaling, and availability of these services. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

The critical consequence for security groups is: **we create far fewer things manually, because Beanstalk automates the application-tier security setup.** Our manual responsibility shrinks to just the backend security group and a key pair. This is the direct benefit of re-architecture — operational burden moves from us to AWS.

***

## 1.2 What Elastic Beanstalk Creates Automatically

When you create an Elastic Beanstalk environment, Beanstalk doesn't just launch an EC2 instance — it creates an entire infrastructure stack. For security groups specifically, Beanstalk automatically creates **two security groups**: [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

1. **An application security group** — attached to the EC2 instance(s) where the vprofile application runs.
2. **A load balancer security group** — attached to the load balancer that Beanstalk creates in front of the application.

Beanstalk also **automatically configures the rules** between these two security groups, allowing traffic from the load balancer security group to reach the application security group. In the lift and shift project, we did all of this manually — we created the ELB security group, the app security group, and wrote the inbound rule on the app SG to allow port 8080 from the ELB SG. Now Beanstalk does all of that for us. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

🔍 **Deep Dive:**
This is a direct manifestation of the "managed service" philosophy: Beanstalk understands that a web application needs a load balancer in front and EC2 behind, and it knows the security relationship between them. Rather than making you figure out and configure these networking rules, it provisions them as part of its environment creation. The security group IDs are generated at creation time, which is why we can't reference the Beanstalk security group before Beanstalk exists — this creates the **temporal dependency** that shapes our entire workflow ordering.

***

## 1.3 The Backend Security Group — What We Must Create Manually

The backend services (RDS, ElastiCache, Amazon MQ) are **not** managed by Beanstalk. They are standalone AWS managed services that we provision separately. Because Beanstalk doesn't know about them, it cannot create security groups for them or configure rules to reach them. This is **our responsibility**. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

We create a single backend security group called `vprofile-rearch-backend-SG` and assign all three backend services to it. This is the same pattern as the lift and shift project — one security group for all backend services — but the services themselves are fundamentally different. Instead of EC2 instances running MySQL, Memcache, and RabbitMQ, we now have RDS, ElastiCache, and Amazon MQ. The security group concept, however, remains identical: it controls which network traffic can reach these services. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

***

## 1.4 The Two-Phase Rule Addition Strategy

This is the most important engineering concept in this lecture: the backend security group's rules are added in **two separate phases**, and this is driven by a temporal dependency, not by choice. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

**Phase 1 (this lecture):** Create the backend security group with **only one rule** — a self-referencing rule that allows all traffic within itself. This enables the backend services (RDS, ElastiCache, Amazon MQ) to communicate with each other. This is the same self-referencing pattern from the lift and shift project. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

**Phase 2 (later lecture, after Beanstalk is created):** Come back and add a second rule to the backend security group that says "allow traffic from the Beanstalk application security group." This rule cannot be added now because **the Beanstalk security group doesn't exist yet** — Beanstalk hasn't been created. You can't reference a security group that doesn't have an ID. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

This two-phase approach is not a workaround — it's the natural consequence of the dependency chain: backend services must exist before Beanstalk (because Beanstalk's application needs to connect to them), but Beanstalk's security group only exists after Beanstalk is created. So the backend SG is created first with internal rules only, and the cross-tier rule is added later once the Beanstalk SG ID is available. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

🔍 **Deep Dive:**
This same temporal dependency existed in the lift and shift project when we added the self-referencing rule to the backend SG — we couldn't reference the SG as a source during its own creation because it didn't have an ID yet. In re-architecture, this pattern extends across services: you can't reference Beanstalk's SG before Beanstalk exists. The general principle is: **in AWS, security group cross-references require both security groups to already exist.** Any rule that references another SG must be added as an edit after both SGs are created.

⚠️ **Expert Note:**
In a fully automated setup (using CloudFormation or Terraform), both security groups would be declared in the same template, and the infrastructure-as-code tool handles the dependency resolution — it creates the SGs first (without cross-referencing rules), then adds the rules in a second pass. What the instructor does manually in two lectures is exactly what automation tools do internally in two phases.

***

## 1.5 Why the Backend Security Group Starts With No Inbound Rules

The instructor explicitly creates the security group with **no inbound rules at all** during the initial creation step. Only after creation does he edit it to add the self-referencing rule. This is the same reason as above: to reference a security group as a source in a rule, that security group must already exist and have an ID. Since you're creating it for the first time, it has no ID yet during the creation form. So: create it empty → get its ID → edit it → add the self-referencing rule using its own ID. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

The instructor also emphasizes: **do not modify the outbound rules.** The default outbound rule allows all outgoing traffic, which is necessary for the backend services to function (DNS resolution, AWS API communication, etc.). This is consistent with the lift and shift project's guidance.

***

## 1.6 Key Pair — Troubleshooting Access, Not Operational Necessity

The instructor creates a key pair named `vprofile-rearch-key`. But the reasoning here is fundamentally different from the lift and shift project. In lift and shift, the key pair was essential — you SSH'd into every instance to install software, configure services, and deploy the application. Without the key pair, you couldn't operate the system at all. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

In the re-architecture project, Beanstalk manages the EC2 instances. You don't SSH in to deploy code, configure Tomcat, or manage the application. **Everything is managed by Beanstalk.** The key pair exists solely for **troubleshooting** — if something goes wrong inside the instance and you need to investigate, you need a way to get in. The instructor explicitly says: "It's not mandatory to log in. Everything will be managed by Beanstalk. But in case where we need to do troubleshooting, that time, we need to log into the instance to see what's happening inside." [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

This shift in the key pair's purpose reflects the larger architectural change: in IaaS (lift and shift), SSH access is an operational tool. In PaaS (Beanstalk), SSH access is a diagnostic escape hatch.

***

## 1.7 Naming Convention — Project Identification Through Names

The instructor names the security group `vprofile-rearch-backend-SG` and the key pair `vprofile-rearch-key`. The `-rearch` suffix is deliberate — it distinguishes these resources from the lift and shift project's resources (which used names like `vprofile-ELB-SG`, `vprofile-app-sg`, `vprofile-prod-key`). In an AWS account where you might have resources from multiple projects, this naming convention immediately tells you which project a resource belongs to. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

***

## 1.8 Comparing Security Group Design: Lift & Shift vs. Re-Architecture

In lift and shift, we created **three** security groups manually with detailed port-specific rules:

* LB SG: HTTP/HTTPS from anywhere
* App SG: port 8080 from LB SG, SSH from My IP
* Backend SG: ports 3306/11211/5672 from App SG, self-referencing all traffic, SSH from My IP

In re-architecture, we create **one** security group manually:

* Backend SG: self-referencing all traffic (Phase 1), traffic from Beanstalk SG (Phase 2, later)

The LB SG and App SG are entirely Beanstalk's responsibility. The backend SG doesn't need SSH from My IP because we're not managing EC2 instances for backend services — RDS, ElastiCache, and Amazon MQ are managed services accessed through AWS-provided endpoints, not via SSH. The port-specific rules (3306, 11211, 5672) from the Beanstalk SG will be part of Phase 2. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating the **network security foundation** for the vprofile re-architecture project. This consists of one backend security group (for RDS, ElastiCache, and Amazon MQ) and one key pair (for emergency SSH access to Beanstalk EC2 instances). After this lecture, the backend security group will be ready with internal communication rules, waiting for the Beanstalk security group reference to be added in a later lecture. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

***

## Step 1: Navigate to the Security Group Console

Log into the **AWS Management Console**. Confirm you are in the **North Virginia (us-east-1)** region — the instructor explicitly mentions this. Go to the **EC2** service. In the left sidebar, click **Security Groups**. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

**Why region matters:** All resources in this project must be in the same region. If you create the security group in a different region than where you'll later create RDS, ElastiCache, Amazon MQ, and Beanstalk, the security group won't be visible or usable by those services.

***

## Step 2: Create the Backend Security Group (Empty)

Click **Create security group**.

**Name:** `vprofile-rearch-backend-SG`
**Description:** The instructor uses a descriptive name indicating this is for the re-architecture project's backend.

**Inbound rules:** Do **NOT** add any rules. Leave this section completely empty. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

**Outbound rules:** Do **NOT** modify. Leave the default (all traffic allowed to all destinations).

Click **Create security group**.

**Why no inbound rules during creation?** We need to add a self-referencing rule (the SG referencing its own ID as a source), but the SG doesn't have an ID until it's created. So we create it empty first to generate the ID, then edit it in the next step.

**Connection to the larger flow:** This security group will be attached to RDS, ElastiCache, and Amazon MQ when those services are created in subsequent lectures. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

***

## Step 3: Add the Self-Referencing Rule

Now that the security group exists and has an ID, we add the internal communication rule.

1. Select the newly created `vprofile-rearch-backend-SG`
2. Click **Edit inbound rules**
3. Click **Add rule**
4. Set:
   * **Type:** All traffic
   * **Source:** Start typing the security group name or ID → select `vprofile-rearch-backend-SG` (itself)
5. Optionally add a **description** (e.g., "Allow all backend services to communicate with each other")
6. Click **Save rules** [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

**What this achieves:** All services assigned to this security group (RDS, ElastiCache, Amazon MQ) can communicate with each other on any port. This is essential because the managed services may need to interact (the same pattern as the lift and shift backend SG).

**Verification:** After saving, the inbound rules tab should show exactly one rule: All traffic, source = the backend SG's own ID. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

**What is NOT added yet:** There is no rule allowing traffic from the application tier (Beanstalk). This will be added in a later lecture after Beanstalk is created and its security group ID is available. Until that rule is added, the Beanstalk EC2 instances will **not** be able to reach the backend services.

***

## Step 4: Create the Key Pair

Navigate to **EC2 → Key Pairs** (under "Network & Security" in the left sidebar).

Click **Create key pair**.

**Name:** `vprofile-rearch-key`
**Format:** The instructor uses the default (`.pem` implied from context of the course — same as the lift and shift lecture). [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

Click **Create key pair**. The private key file downloads automatically.

**Purpose reminder:** This key pair is **not for regular operations**. Beanstalk manages the EC2 instances. This key is exclusively for troubleshooting — if you need to SSH into a Beanstalk instance to diagnose issues, this is your way in. You'll associate this key pair with the Beanstalk environment when creating it in a later lecture. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

**Store securely:** As always, this is a one-time download. If lost, you cannot retrieve it.

***

## Step 5: What Comes Next (Workflow Context)

At this point, the security foundation is set. The next lecture creates the **RDS instance**, which will be placed inside the backend security group we just created. The sequence continues with ElastiCache, Amazon MQ, and finally Elastic Beanstalk. Once Beanstalk is created and its security group ID is available, we return to the backend SG and add the cross-tier rule. [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Architecture — Re-Architecture vs. Lift & Shift

```
LIFT & SHIFT (previous project):
  3 SGs created manually (LB, App, Backend)
  All rules configured manually
  All services on raw EC2 instances
  Key pair = essential operational tool

RE-ARCHITECTURE (this project):
  1 SG created manually (Backend only)
  LB SG + App SG = auto-created by Beanstalk
  LB→App rules = auto-configured by Beanstalk
  Backend services = managed (RDS, ElastiCache, Amazon MQ)
  Key pair = troubleshooting-only escape hatch
```

## Security Group Responsibility Split

```
BEANSTALK creates & manages:
  ├─ Load Balancer SG (rules: auto)
  ├─ Application SG (rules: auto — allows traffic from LB SG)
  └─ Cross-rules between LB SG ↔ App SG (auto)

WE create & manage:
  └─ Backend SG
       ├─ Phase 1: self-referencing rule (all traffic within itself)
       └─ Phase 2: allow traffic from Beanstalk App SG (added LATER)
```

## Two-Phase Rule Strategy

```
Phase 1 (NOW — this lecture):
  Create Backend SG → empty
  Edit → add self-ref rule (all traffic from itself)
  WHY: Beanstalk SG doesn't exist yet → can't reference it

Phase 2 (LATER — after Beanstalk creation):
  Edit Backend SG → add rule: traffic from Beanstalk App SG
  WHY: Now Beanstalk SG exists → ID is available

ROOT CAUSE: cross-referencing requires both SGs to exist
```

## Creation Sequence

```
1. Backend SG (empty — no rules during creation)
2. Edit Backend SG → self-referencing "all traffic" rule
3. Key pair (vprofile-rearch-key)
4. [Next lectures] → RDS, ElastiCache, Amazon MQ (placed in Backend SG)
5. [Later lecture] → Beanstalk (auto-creates LB SG + App SG)
6. [After Beanstalk] → Edit Backend SG → add Beanstalk SG rule
```

## Backend SG Rule State Over Time

```
After this lecture:
  Inbound: [All traffic ← self]
  Outbound: [All traffic → anywhere (default)]

After Beanstalk lecture:
  Inbound: [All traffic ← self] + [traffic ← Beanstalk App SG]
  Outbound: [All traffic → anywhere (default)]
```

## Key Pair Role Shift

```
Lift & Shift:  Key pair → SSH for installation, deployment, operations
Re-Architecture: Key pair → SSH for troubleshooting ONLY
                  "Everything will be managed by Beanstalk"
```

## Self-Referencing Rule — Why Two Steps

```
Create SG (no rules) → SG gets an ID
Edit SG → add rule referencing own ID as source
WHY: can't reference an ID that doesn't exist yet
SAME PATTERN as lift & shift backend SG
```

## Resource Naming Convention

```
vprofile-rearch-backend-SG  → "-rearch" = re-architecture project
vprofile-rearch-key          → distinguishes from lift & shift "-prod-key"
Purpose: instant project identification in multi-project AWS accounts
```

## Reusable Engineering Patterns

**1. Managed Service = Reduced Manual Security Surface**

```
More managed services → fewer manual SGs + rules
Beanstalk manages: LB SG, App SG, cross-rules
You manage: only what Beanstalk doesn't know about (backend SG)
Pattern: managed orchestrators absorb networking config
```

**2. Temporal Dependency → Phased Configuration**

```
Resource B depends on Resource A's ID
But Resource A is created later in the workflow
→ Create Resource B with partial config
→ Complete Resource B's config after Resource A exists

General: any cross-reference between resources
         requires both to exist first
Automation tools (CloudFormation/Terraform) handle this
         with dependency graphs + two-pass creation
```

**3. Diagnostic Access ≠ Operational Access**

```
IaaS (EC2): SSH = daily operational tool
PaaS (Beanstalk): SSH = emergency diagnostic tool
Pattern: as abstraction level rises, direct access
         shifts from operational to exceptional
```

***

*This completes the full reconstruction. Theory explains why only one SG is manually created and the two-phase rule strategy. Practical walks through the exact creation steps. The Compression Map enables instant recall of the re-architecture security model and how it differs from lift and shift.* [\[141-securi...d-keypairs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/141-security-group-and-keypairs.txt)
