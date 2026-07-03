# ✅ AWS Lift & Shift — Validate, Cleanup & Summarize — Deep Learning Material

**Source:** *Validate & Summarize* (Final Lecture, vprofile AWS Lift & Shift Project) [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Final System State — What "Done" Looks Like

At the end of the vprofile lift and shift project, the entire application architecture has been migrated from a local environment to AWS using an **Infrastructure as a Service (IaaS)** approach. The instructor initially misspoke as "Infrastructure as Code" and immediately corrected to "Infrastructure as a Service" — a meaningful distinction. IaaS means we are using raw AWS compute instances (EC2) to host our services, not higher-level managed services. We manually provisioned VMs and installed the same software stack that ran locally. The application itself, its architecture, and its services remain identical — only the underlying infrastructure changed from local machines to cloud instances. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

The final running state consists of **five EC2 instances** visible in the console. Of these, the original `app01` instance should be in a **terminated** state. It was replaced by a new instance launched and managed by the **Auto Scaling group**. The other instances are the backend services (MySQL, Memcache, RabbitMQ) which remain running as manually managed instances. The key architectural shift is that the application tier is no longer a manually managed instance — it is now controlled by the Auto Scaling group, which means AWS handles its lifecycle: if the instance dies, Auto Scaling launches a replacement automatically from the AMI. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

🔍 **Deep Dive:**
The reason `app01` is terminated is the operational sequence from the previous lecture: we created an AMI from `app01`, built a launch configuration/template from that AMI, created an Auto Scaling group using that template, and the Auto Scaling group launched its own fresh instance from the AMI. At that point, `app01` became redundant — the Auto Scaling group's instance replaced it. The original `app01` was either manually terminated or replaced as part of the Auto Scaling group's desired capacity management.

***

## 1.2 Lift and Shift — What It Means and What It Doesn't

The instructor defines what was accomplished as a **lift and shift** migration. This means taking an existing application running in one environment and moving it — with minimal or no changes to its architecture — to another environment (in this case, AWS). [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

A critical clarification the instructor makes: **we did not actually migrate any data.** In a real lift and shift, if you have a production database with real data, you would use tools like **DBSync** to replicate database content, or **S3 Sync** for file storage migration. In this project, since there was no real production data, we migrated only the application itself — the code, the services, and the infrastructure configuration. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

This distinction matters because in real-world migrations, the data migration is often the hardest and riskiest part. The application migration (what we did) is the structural work; the data migration is the operational risk. The instructor intentionally highlights this gap so learners understand that a complete production migration involves more than what was shown. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

The instructor then foreshadows the next project: **re-architecting** the application. Instead of running everything on EC2 instances (IaaS), the next project will use higher-level AWS managed services. The motivation is clear: maintaining many EC2 instances is operationally expensive — patching, monitoring, scaling, and replacing instances is your responsibility. Managed cloud services shift that operational burden to AWS. This is the natural evolution path: lift and shift first (to get off on-premises), then re-architect (to become cloud-native). [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## 1.3 Target Group Health and the Auto Scaling Group Relationship

The instructor checks that the target group has **one healthy instance** managed by the Auto Scaling group. This confirms the end-to-end chain is working: the Auto Scaling group launched an instance → the instance registered itself with the target group → the target group health check passed → the load balancer is routing traffic to it. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

The health state is the critical validation signal. A "Healthy" status in the target group means the load balancer sent a health check request to the instance (typically an HTTP request to a specific path on port 8080) and received a valid response. If the instance were misconfigured, the health check would fail, the target group would mark it "Unhealthy," and the load balancer would stop routing traffic to it. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## 1.4 Stickiness — Why Login Breaks Without It

The instructor demonstrates logging in with credentials `admin_vp` / `admin_vp` and then flags an important behavior: **if you click LOGIN and the page just refreshes without logging in, stickiness is disabled.** [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

This is only relevant when you have **multiple instances** behind the load balancer. Here's why: when a user logs in, the application creates a session on the specific Tomcat instance that handled the login request. The session data (the fact that this user is authenticated) lives in that instance's memory. If the next request from the same user gets routed to a **different** instance by the load balancer, that instance has no knowledge of the session — from its perspective, the user is not logged in. So the page appears to just refresh. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Stickiness** (also called session affinity) solves this by instructing the load balancer to route all subsequent requests from the same user to the **same backend instance** for a configured duration. It does this using a cookie — either an application-generated cookie or a load-balancer-generated cookie. Once stickiness is enabled in the target group, the login problem disappears because the session and the user's requests stay on the same instance. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

⚠️ **Expert Note:**
Stickiness is a pragmatic solution but introduces a tradeoff: it reduces the load balancer's ability to distribute traffic evenly. If one instance accumulates many sticky sessions, it becomes overloaded while others are underutilized. The cloud-native solution is **externalized session management** — storing sessions in a shared store like Memcache or Redis so any instance can serve any request. The vprofile application already uses Memcache in its backend, which could serve this purpose, but in this project's lift and shift approach, the application's session behavior was not modified, so stickiness at the load balancer level is the necessary fix.

***

## 1.5 Accessing the Application — DNS Name vs. Custom Domain

There are two ways to reach the deployed application: [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Option 1: Load Balancer DNS Name.** Every AWS load balancer gets an auto-generated DNS name (a long, ugly AWS hostname). You can copy this from the Load Balancers section in the EC2 console and paste it directly into a browser. This always works and requires no DNS configuration.

**Option 2: Custom Domain with HTTPS.** If you own a domain and created a CNAME record pointing to the load balancer's DNS name (using GoDaddy or another registrar), you can access the application via `https://yourdomain.com`. This requires the ACM certificate (created in the prerequisites) to be attached to the load balancer for the HTTPS connection to work. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## 1.6 The Cleanup Order — Why Sequence Matters

Cleanup is not just deleting resources — **the order in which you delete them is critical**. The instructor is very explicit about this, and the reasoning reveals important dependency relationships between AWS resources. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**The Auto Scaling group must be deleted first.** If you try to terminate the app instance without deleting the Auto Scaling group, the Auto Scaling group will detect that its desired capacity has dropped below the configured minimum and will **immediately launch a new replacement instance**. You'll be stuck in an infinite loop of terminating instances that keep coming back. This is the Auto Scaling group doing exactly what it's designed to do — maintain desired capacity — but during cleanup, it becomes an obstacle. Deleting the Auto Scaling group first removes this self-healing behavior, and it automatically terminates the instance it was managing. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**The AMI must be deregistered before its snapshot can be deleted.** An AMI is not a standalone object that can be "deleted" — the concept of deleting doesn't exist for AMIs. An AMI is essentially a **registration record** that points to an underlying EBS snapshot. The AMI says "this snapshot, with these configurations, constitutes a launchable image." To remove it, you **deregister** the AMI (remove the registration), and then separately **delete the snapshot** it was pointing to. If you try to delete the snapshot first, AWS will block you because the AMI still references it. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

🔍 **Deep Dive:**
The AMI-snapshot relationship is an important AWS concept. The AMI is metadata — it contains the architecture type, block device mappings, and a pointer to one or more EBS snapshots. The snapshot is the actual data — a point-in-time copy of the EBS volume. When you launch an instance from an AMI, AWS creates new EBS volumes from those snapshots. Deregistering the AMI removes the metadata, but the snapshot persists independently until you explicitly delete it. This is why cleanup requires two steps: deregister AMI, then delete snapshot.

**S3 buckets must be emptied before deletion.** AWS does not allow you to delete a non-empty bucket. You must first **empty** the bucket (which permanently deletes all objects inside it), then delete the bucket itself. The instructor notes the bucket is very small, so there's essentially no cost to keeping it, but for clean project teardown, it should be removed. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Route 53 hosted zones cannot be deleted with records still in them.** You must first delete all the custom DNS records you created, then delete the hosted zone itself. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Resources with no ongoing charges** (target groups, key pairs, security groups) can be cleaned up optionally. They don't incur costs, but removing them prevents clutter and confusion in future projects.

***

## 1.7 The Complete Architecture Recap — What Was Built

The instructor walks through the architecture diagram one final time, tracing the entire project sequence. This is the full system that was constructed across all lectures: [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

1. **Security groups and key pairs** were created first — establishing the network security layer and SSH access credentials.
2. **EC2 instances were launched** and initialized using **user data scripts** — automating the initial software installation and configuration on each instance at boot time.
3. **The application artifact was built** (compiled from source code) and **deployed via S3** — the artifact was uploaded to an S3 bucket and then pulled down to the Tomcat instance.
4. **A load balancer was created** with HTTPS using an **ACM certificate** — providing encrypted public-facing access to the application.
5. **The app instance was captured as an AMI** and placed into an **Auto Scaling group** — automating the application tier's lifecycle and self-healing.
6. **Private DNS entries were created in Route 53** — allowing instances to communicate with each other using names (like `db01`, `mc01`, `rmq01`) instead of IP addresses, which is what the application.properties file expects. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What This Lecture Covers

This is the final lecture of the vprofile lift and shift project. We are doing three things: **validating** that the entire deployed system works end-to-end, **cleaning up** all AWS resources to avoid ongoing charges, and **revisiting** the architecture to solidify understanding. After this, the AWS account should be clean with no billable resources remaining from this project. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## Step 1: Validate the Target Group Health

Go to **EC2 → Target Groups** in the AWS console. Select the target group associated with your load balancer.

**What to check:** There should be **one instance** registered, and its status should be **Healthy**. This instance should be the one launched by the Auto Scaling group (not the original `app01`). [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**How to confirm it's the Auto Scaling-managed instance:** Go to **EC2 → Instances**. You should see five instances total. The original `app01` should show a **Terminated** state. The running app instance should have a name or tag indicating it was launched by the Auto Scaling group.

**If the instance is Unhealthy:** The health check is failing — typically meaning the application on the instance isn't responding correctly on port 8080. Verify the instance is running, the Tomcat service is up, and the security group allows traffic from the load balancer on port 8080 (as configured in the earlier security group lecture). [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## Step 2: Access the Application via Browser

**Option A — No custom domain:** Go to **EC2 → Load Balancers**. Copy the **DNS name** of your load balancer. Paste it into a browser. The vprofile application login page should appear. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Option B — Custom domain configured:** If you created a CNAME record at your domain registrar (e.g., GoDaddy) pointing to the load balancer DNS name, type `https://yourdomain.com` in the browser. The HTTPS connection works because the ACM certificate is attached to the load balancer.

**Login test:** Enter username `admin_vp` and password `admin_vp`. Click LOGIN. You should be logged in and able to verify backend connectivity — check the RabbitMQ and Memcached status pages within the application. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Troubleshooting — Login just refreshes the page:** This means **stickiness is not enabled** on the target group, and you have multiple instances. Go to the target group → Attributes → Edit → Enable stickiness. This only applies if your Auto Scaling group has more than one instance. With a single instance, stickiness is irrelevant since all requests go to the same place. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## Step 3: Cleanup — Delete the Auto Scaling Group (FIRST)

⚠️ **This must be done before terminating any app instances.**

Go to **EC2 → Auto Scaling Groups**. Select your Auto Scaling group. Click **Delete**. Confirm by typing the confirmation text.

**What happens internally:** The Auto Scaling group will terminate the instance it manages as part of its deletion process. You do not need to terminate that instance separately. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Why this must be first:** If you terminate the instance without deleting the Auto Scaling group, it will immediately launch a new one to maintain its desired capacity. You'll see instances appearing right after you terminate them — this is the Auto Scaling group's self-healing behavior working against your cleanup intent.

***

## Step 4: Terminate Remaining Backend Instances

Go to **EC2 → Instances**. Refresh the page. The Auto Scaling-managed app instance should already be terminating (from Step 3).

Select all remaining instances **except** the Auto Scaling app instance (which is already being handled). The instructor specifically says: uncheck the app instance, select the backend instances (MySQL, Memcache, RabbitMQ), then **Terminate (Delete)**. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Verification:** After a few minutes, refresh the instances list. All instances should show "Terminated" state. This information will persist briefly in the console and then disappear automatically.

***

## Step 5: Delete the Load Balancer

Go to **EC2 → Load Balancers**. Select your load balancer. Click **Delete**. Confirm.

This can be done in parallel while instances are terminating — there's no dependency requiring instances to be terminated first. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## Step 6: Delete the Target Group (Optional)

Go to **EC2 → Target Groups**. Select the target group. Delete it.

The instructor notes: **target groups have no charges**. Deleting is optional and purely for cleanliness. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## Step 7: Check and Clean Volumes

Go to **EC2 → Volumes**. Verify there are no orphaned EBS volumes. The volumes that were attached to the instances should be automatically deleted when the instances terminate (if "Delete on Termination" was enabled, which is the default). If any volumes remain, delete them manually. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## Step 8: Clean Route 53 Records and Hosted Zone

Go to **Route 53 → Hosted Zones**. Select the private hosted zone you created.

**Important:** You **cannot delete a hosted zone directly** if it contains records. You must first delete all the custom records you created (the A records or CNAME records for `db01`, `mc01`, `rmq01`, etc.). Select those records and click **Delete records**. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

After all custom records are removed, you can then delete the hosted zone itself.

***

## Step 9: Deregister the AMI, Then Delete the Snapshot

Go to **EC2 → Images → AMIs**. Select the AMI you created from `app01`. Click **Actions → Deregister AMI**. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Critical concept:** There is no "delete" option for AMIs. AMIs are metadata registrations pointing to snapshots. **Deregister** removes the metadata.

After deregistering, go to **EC2 → Snapshots**. Refresh the page. The snapshot that backed the AMI should now appear as deletable (it was previously protected by the AMI reference). Select it → **Actions → Delete snapshot**. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Verification:** Go to the EC2 Dashboard. Refresh. The Snapshots count should be zero. The AMIs count should be zero.

***

## Step 10: Delete the S3 Bucket (Optional)

Go to **S3**. Select the bucket used for artifact deployment.

**Two-step process:**

1. Click **Empty**. Type `permanently delete` in the confirmation field. Click **Empty**. This deletes all objects inside the bucket.
2. After emptying, select the bucket again. Click **Delete bucket**. Type the bucket name to confirm. Click **Delete bucket**. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

**Why two steps:** AWS does not allow deletion of non-empty buckets. Emptying is a destructive, irreversible action — all objects are permanently removed.

The instructor notes: the bucket size is very small, so charges are negligible. This is purely for cleanup completeness.

***

## Step 11: Clean Security Groups and Key Pairs (Optional)

Go to **EC2 → Security Groups**. Delete the three security groups created for this project (`vprofile-ELB-SG`, `vprofile-app-sg`, `vprofile-backend-sg`).

Go to **EC2 → Key Pairs**. Delete `vprofile-prod-key`.

Neither security groups nor key pairs incur charges. Cleanup is optional but recommended to avoid confusion in future projects. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

## Step 12: Final Verification

Go to the **EC2 Dashboard**. Refresh the page. Verify:

* Running instances: 0 (terminated instances may still show temporarily)
* Volumes: 0
* Snapshots: 0
* AMIs: 0
* Load Balancers: 0
* Auto Scaling Groups: 0

The terminated instance entries will disappear from the console automatically after some time. [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Full Project Architecture — What Was Built

```
Security Groups + Key Pairs
  → EC2 Instances (launched with User Data scripts)
    → Artifact built + deployed via S3
      → Load Balancer + HTTPS (ACM certificate)
        → AMI created from app01 → Auto Scaling Group
          → Route 53 Private DNS (name-based inter-instance communication)
```

 [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)

## Final Running State

```
5 instances visible:
  - app01 → TERMINATED (replaced by ASG)
  - 1 app instance → HEALTHY, managed by Auto Scaling Group
  - 3 backend instances → MySQL, Memcache, RabbitMQ (manually managed)

Target Group: 1 healthy instance (ASG-managed)
Load Balancer: routing to target group via HTTPS
Route 53: private DNS names → instance IPs
```

## Access Paths

```
No custom domain → copy LB DNS name → paste in browser
Custom domain    → https://yourdomain.com (CNAME → LB DNS)

Login: admin_vp / admin_vp
Verify: RabbitMQ status, Memcached status pages
```

## Stickiness Decision Tree

```
Multiple instances behind LB?
  ├─ YES → Stickiness MUST be enabled in target group
  │         (login refreshes without logging in = stickiness disabled)
  └─ NO  → Stickiness irrelevant (single instance gets all traffic)
```

## Lift and Shift — Core Concept

```
Same application + Same architecture + Different infrastructure
Local VMs → AWS EC2 instances (IaaS)

What was migrated: application code, services, configuration
What was NOT migrated: data (no DBSync, no S3 Sync needed here)

Evolution path:
  Lift & Shift (IaaS) → Re-Architecture (managed cloud services)
  "many instances to maintain" → "let AWS manage the services"
```

## Cleanup — Dependency-Ordered Sequence

```
⚠️ ORDER MATTERS

1. Auto Scaling Group  ← MUST be first (prevents instance respawn loop)
     └─ automatically terminates its managed instance

2. Remaining EC2 Instances (backend: MySQL, Memcache, RabbitMQ)

3. Load Balancer

4. Target Group (optional — no charges)

5. Volumes (verify none orphaned)

6. Route 53:
     Delete records FIRST → then delete hosted zone
     (hosted zone cannot be deleted with records inside)

7. AMI → Deregister (not "delete" — no such operation)
     └─ then Snapshot → Delete
     (snapshot blocked while AMI references it)

8. S3 Bucket:
     Empty FIRST (type "permanently delete") → then Delete bucket
     (non-empty bucket cannot be deleted)

9. Security Groups + Key Pairs (optional — no charges)
```

## Resource Dependency Chains

```
Auto Scaling Group ──manages──▶ App Instance
  (delete ASG → instance auto-terminates)
  (terminate instance without deleting ASG → new instance spawns)

AMI ──references──▶ EBS Snapshot
  (deregister AMI first → then delete snapshot)
  (cannot delete snapshot while AMI exists)

Hosted Zone ──contains──▶ DNS Records
  (delete records first → then delete hosted zone)

S3 Bucket ──contains──▶ Objects
  (empty bucket first → then delete bucket)
```

## Cleanup Gotchas

```
Instance keeps coming back after termination?
  → Auto Scaling Group still exists → delete it first

Can't delete snapshot?
  → AMI still registered → deregister AMI first

Can't delete hosted zone?
  → Records still exist → delete records first

Can't delete S3 bucket?
  → Bucket not empty → empty it first

No "delete" option for AMI?
  → Correct — AMIs are "deregistered," not deleted
  → AMI = metadata pointer → Snapshot = actual data
```

## Verification Checklist (Post-Cleanup)

```
EC2 Dashboard:
  Running Instances  → 0
  Volumes            → 0
  Snapshots          → 0
  AMIs               → 0
  Load Balancers     → 0
  Auto Scaling Groups → 0
  Target Groups      → 0 (if deleted)

Route 53: Hosted zone removed
S3: Bucket removed
```

## Reusable Engineering Patterns

**1. Self-Healing Creates Cleanup Resistance**

```
Auto Scaling Group's purpose: maintain desired instance count
During operation: this is resilience
During cleanup: this blocks deletion

Pattern: any self-healing/auto-recovery system must be disabled
         BEFORE removing the resources it manages
General rule: delete the CONTROLLER before the WORKER
```

**2. Metadata → Data Dependency Chain**

```
AMI (metadata) → Snapshot (data)
Hosted Zone (container) → Records (content)
S3 Bucket (container) → Objects (content)

Pattern: in layered resource systems, always delete
         inner content before outer container
         and metadata consumers before data sources
```

**3. Lift and Shift → Re-Architecture Evolution**

```
Phase 1: Move as-is to cloud (IaaS) — minimize risk, prove cloud works
Phase 2: Replace IaaS with managed services — reduce operational burden

Trigger for Phase 2: "maintaining too many instances"
Benefit of Phase 2: AWS handles patching, scaling, availability
```

***

*This completes the full reconstruction of the final lecture. Theory explains the system's validated state and the reasoning behind cleanup order. Practical provides the exact step-by-step cleanup execution. The Compression Map enables rapid recall of the dependency chains, cleanup sequence, and architectural overview of the entire project.* [\[139. Valid...Summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/139.%20Validate%20%26%20Summarize.txt)
