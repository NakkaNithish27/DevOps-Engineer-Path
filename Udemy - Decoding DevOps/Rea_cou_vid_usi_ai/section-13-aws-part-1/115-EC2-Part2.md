# ☁️ AWS EC2 — More in EC2 (Part 2) — Deep Learning Material

**Source:** Video caption file — [115-more-in-ec2-part2.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt?EntityRepresentationId=b2a32263-a8e3-4dc6-9ef3-ea0de1e4469f) [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Video Context:** The instructor continues exploring EC2 instance properties beyond basic launch — covering the public/private IP behavior, Elastic IPs, network interfaces, volumes, instance type changes (elasticity), termination protection, security group modifications, system logs, and proper cleanup. A recurring theme: "You're not just learning EC2 — you're learning many basic concepts of cloud computing through EC2."

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Private IP vs. Public IP — Static vs. Dynamic Behavior

When you create an EC2 instance, it receives two IP addresses: a **private IP** and a **public IP**. These behave fundamentally differently in terms of persistence. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The **private IP is static** — once assigned to your instance, it remains the same for the entire lifetime of that instance. It will not change through stop/start cycles. It is only released when you **terminate (delete)** the instance. The private IP is the instance's identity within the VPC (Virtual Private Cloud) — other services and instances within the same network use this IP to communicate with it.

The **public IP is dynamic** — it changes every time the instance is stopped and started. When you stop the instance, the public IP is **released back** to AWS's pool of available public addresses. When you start the instance again, AWS assigns a **new, different** public IP from the pool. The instructor demonstrates this live: stops the instance, shows the public IP disappears while the private IP remains, then starts the instance and shows a completely different public IP is assigned. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The instructor notes that "in majority of the cases this is not a big problem because we will have load balancer and other services that access the instance." This is a critical architectural insight: in properly designed cloud systems, you rarely need to access an instance directly by its public IP. Load balancers, DNS names, and service discovery layers abstract away the specific IP addresses. The dynamic public IP is a problem only when something needs to reach the instance at a **known, fixed** public address.

***

## 1.2 Elastic IP — The Static Public IP Solution

When you **do** need a static public IP for an EC2 instance, the solution is an **Elastic IP**. An Elastic IP is a public IPv4 address that AWS reserves for **your account**. Unlike a regular public IP, it does not change — it persists across stop/start cycles and can be reassociated between instances. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

Key characteristics of Elastic IPs:

**Globally unique:** The instructor states it's "a unique IP address in the world that will be reserved for you." Once allocated, no one else on the internet gets this IP — it's yours until you release it.

**Limited to five per account:** AWS gives you five Elastic IPs by default. If you need more, you must contact AWS support. This limit exists because IPv4 addresses are a scarce global resource.

**Not free:** Elastic IPs carry charges. The instructor explicitly warns about this multiple times and says "you can skip this practice and you can just watch it." The charges are described as "really negligible" but they exist — specifically, AWS charges for Elastic IPs that are **allocated but not associated** with a running instance (to discourage hoarding scarce IPv4 addresses). [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The workflow: allocate an Elastic IP → associate it with an instance (or network interface) → the instance now has a static public IP that survives stop/start cycles. The instructor demonstrates this: after associating the Elastic IP, he stops the instance, and shows that the IP remains attached even in the stopped state. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

⚠️ **Expert Note:** The instructor repeatedly emphasizes: "In most of the cases you will not need elastic IP to your instance. You will realize after completing this course." This is important architectural guidance — Elastic IPs are a specific solution for specific problems (like a server that must be reachable at a known IP, or a legacy system that whitelists specific IPs). Over-using Elastic IPs is an anti-pattern that creates rigid, hard-to-manage infrastructure.

***

## 1.3 Network Interfaces — The Networking Foundation of EC2

This is one of the most architecturally important concepts in the video. The instructor reveals that IPs, security groups, and Elastic IPs are **not directly attached to the instance itself** — they are attached to the instance's **network interface**. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

Every EC2 instance comes with a **default network interface** when launched. This interface holds the private IP, the public IP (if any), the Elastic IP (if associated), and the security group. The instructor navigates to the instance's Networking tab, scrolls to the interface section, and shows all these elements attached to the single default network interface.

The key insight: **"Anything that is related to the networking of the instance is attached to the network interface."** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

An instance can have **multiple network interfaces**. Each additional network interface can have its own:

* Private IP
* Public IP
* Elastic IP
* Security group(s)

The instructor shows where to find and create network interfaces: **Network and Security → Network Interfaces** in the EC2 console. You can create a new network interface and attach it to your instance, giving the instance multiple network identities. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

When associating an Elastic IP, you get two options: **Instance** or **Network Interface**. If the instance has only one network interface, selecting "Instance" simply targets that default interface. If the instance has multiple interfaces, you'd select the specific "Network Interface" to target. This explains why both options exist in the association dialog.

🔍 **Deep Dive:** The network interface abstraction is fundamental to AWS networking. It's the actual entity that participates in the VPC network. An instance is a compute unit; a network interface is its network identity. This separation allows advanced patterns like: moving a network interface (with its IP and security groups) from one instance to another during failover, giving an instance multiple network presences in different subnets, or applying different security policies to different interfaces on the same instance.

***

## 1.4 Volumes — The Storage Component

Every EC2 instance has at least one **volume** (disk storage). This default volume is created automatically when you launch the instance, and its size comes from the **AMI** (Amazon Machine Image) you selected. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The instructor shows how to find the volume: go to the instance's **Storage** tab to see the Volume ID, or navigate to **Elastic Block Store → Volumes** in the left panel. The volume listing shows the Volume ID, the instance it's attached to, and its size.

Default volume sizes vary by AMI: "Some AMI might give you 20 GB, some might give you 30, some might give you 120. Really depends on the AMI. Most of the default Linux AMIs come with 8 GB." [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The instructor notes that volumes will have a **dedicated lecture** later — this is just showing the default relationship: instance launch → AMI selected → default volume created from AMI specification.

***

## 1.5 Instance Type Change — Cloud Elasticity in Action

One of the core properties of cloud computing is **elasticity** — the ability to scale resources up or down based on need. The instructor demonstrates this through **changing the instance type** of a running instance. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The process requires the instance to be **stopped first** — you cannot change the instance type of a running instance (the option is grayed out while running). After stopping, you go to **Actions → Instance Settings → Change Instance Type**. The instructor changes from `t2.micro` (1 vCPU, 1 GB RAM) to `t2.small` (1 vCPU, 2 GB RAM). [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

When changing, AWS shows a **comparison** between the current and target instance types: CPU cores, memory, and even pricing. The instructor highlights this as genuinely useful: "That really helps you decide, should you go for it or not?" After applying the change and starting the instance, it now runs with the new (larger) specifications. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The instructor warns about cost: "When we change to a bigger instance type, there will be charges on hourly basis." And closes with practical advice: "Just make sure you keep it at T2 micro, T3 micro in the free tier limit and just play with it." [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

⚠️ **Expert Note:** The stop-required behavior means instance type changes involve **downtime**. The instance must be fully stopped, the type changed, and the instance restarted. During this time, the instance is unreachable. In production, this is managed through strategies like: using Auto Scaling Groups that launch new instances of the desired type while draining old ones, or having redundant instances behind a load balancer so one can be changed without service interruption.

***

## 1.6 Termination Protection — Guarding Against Accidental Deletion

Termination protection is a safety mechanism that **prevents accidental deletion** of an instance. When enabled, any attempt to terminate (delete) the instance will be rejected with an error. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The instructor enables it via **Actions → Instance Settings → Change Termination Protection → Enable**. Then, when attempting to terminate the instance, it fails. To actually terminate, you must first go back, **disable** the protection, and then terminate.

The instructor explains the use case: "Some people, you know, accidentally delete the instance — it's going to not allow that." This is a simple but critical safeguard, especially in shared environments where multiple people have access to the AWS console. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

The full deletion flow demonstrated: attempt terminate → fail (protection enabled) → disable protection → terminate again → succeeds.

***

## 1.7 Security Group Modifications on a Live Instance

Security groups can be changed on a running instance without stopping it. The instructor navigates to **Actions → Security → Change Security Groups**. You can: [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

* **Add** additional security groups to the instance
* **Remove** existing security groups

The instructor demonstrates: adds the "default" security group alongside the existing one, then removes it again to keep the original configuration. This shows that security group changes are **live, non-disruptive** operations — unlike instance type changes which require a stop.

The security group is attached to the network interface (as covered in §1.3), so changing security groups effectively updates the firewall rules on the network interface.

***

## 1.8 Other Instance Settings — Brief Mentions

Several additional capabilities are shown briefly without deep exploration: [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**IAM Role (Actions → Security → Modify IAM Role):** The instructor describes these as "basically permissions on which servers can access this instance or from this instance what you can access." Detailed coverage is deferred to a later lecture.

**Image and Templates (Actions → Image and Templates → Create Image):** You can create a new AMI from the current state of the instance. This will be covered in upcoming lectures.

**Monitor and Troubleshoot → System Log:** If the instance doesn't boot properly after OS-level changes, you can view the **system log** (boot log). The instructor notes: "It's not like live system log. It takes time to load. It's like the monitor, the computer monitor to your EC2 instance. But this is not live." You can download the log to inspect boot issues. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

***

## 1.9 The EC2 Dashboard — Resource Tracking

The EC2 dashboard provides an overview of all EC2-related resources in the current region: running instances, key pairs, security groups, elastic IPs, volumes, etc. The instructor emphasizes: "Always keep track of your EC2 dashboard. So if you have any extra volumes or elastic IP, anything — you can find it from here and then you can go there and delete it if you don't need it." [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

This is a resource hygiene practice — cloud resources that exist but aren't needed still incur charges (Elastic IPs, volumes, running instances). The dashboard is the single-pane-of-glass for detecting orphaned or forgotten resources.

***

## 1.10 Cleanup — Terminate Instance and Release Elastic IP

The video ends with a complete cleanup sequence: [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

1. **Disable termination protection** (because it was enabled earlier)
2. **Terminate the instance** (permanent deletion)
3. **Release the Elastic IP** back to AWS's pool

The instructor explicitly warns about Elastic IP cleanup: "Elastic IPs are not free, so make sure you release it back to the AWS pool if you find any elastic IP." An allocated-but-unassociated Elastic IP incurs charges — releasing it stops those charges.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Exploring

We are exploring the **post-launch properties and management capabilities** of an EC2 instance — IP behavior, Elastic IPs, network interfaces, volumes, instance type changes, termination protection, security group modifications, and proper cleanup. The final outcome: understanding how to manage, modify, and safely clean up EC2 resources. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

***

## Step 1: Observe Public IP Dynamic Behavior

Starting with a running instance that has both a public IP and a private IP.

### Stop the instance:

**Actions → Instance State → Stop Instance → Confirm Stop**

Wait a few seconds, then **refresh** the instance details page. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Expected result:**

* Private IP: **still present** (static, persists through stop/start)
* Public IP: **gone** (released back to AWS pool)

### Start the instance:

**Actions → Instance State → Start Instance**

Wait for the instance to reach the "running" state, then refresh.

**Expected result:**

* Private IP: **same as before**
* Public IP: **different from before** (new IP assigned from pool) [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Verification:** Compare the new public IP with what you noted before stopping. They will be different.

**Connection to flow:** This demonstrates why Elastic IPs exist — to solve the dynamic public IP problem when a fixed address is needed.

***

## Step 2: Allocate an Elastic IP

Navigate to: **EC2 Console → Network and Security → Elastic IPs**

Click **Allocate Elastic IP Address**. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Settings:**

* Region: keep the same region as your instance (this is the default selection)

Click **Allocate**.

**Expected result:** A new Elastic IP appears in the list — this is your reserved public IP address.

**Cost warning:** Elastic IPs are not free. The instructor advises you can skip this practice and just watch. Charges are negligible but real. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

***

## Step 3: Associate the Elastic IP with Your Instance

Select the Elastic IP → **Actions → Associate Elastic IP Address**

**Association options:** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

* **Instance** — Select your instance by name/ID. If the instance has only one network interface, the Elastic IP attaches to that default interface automatically.
* **Network Interface** — Select a specific network interface. Use this when the instance has multiple interfaces and you need to target a specific one.

For this exercise: select **Instance** → select your instance from the dropdown → click **Associate**.

**Verification:** Go back to the instance details, refresh, and the Elastic IP should appear as the instance's public IP. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

### Verify persistence through stop/start:

Stop the instance (**Actions → Instance State → Stop Instance**).

After stopping, check the instance details: **the Elastic IP is still there**, even though the instance is stopped. This proves the Elastic IP is static — unlike the regular public IP that disappeared in Step 1. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

Start the instance again — the same IP remains.

***

## Step 4: Explore Network Interfaces

Navigate to your instance → **Networking tab** → scroll down to the **Interface** section.

**What you see:** The default network interface, with:

* Private IP attached to it
* Public IP (or Elastic IP) attached to it
* Security group attached to it [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Key observation:** All networking properties are on the **network interface**, not directly on the instance (see Theory §1.3).

### View all network interfaces:

Navigate to: **EC2 Console → Network and Security → Network Interfaces**

Here you can see your instance's default network interface, and you can **create additional** network interfaces and attach them to the instance. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Note:** The instructor says "you don't need to really do all this in this lecture — you can just watch it." This is informational, not a required exercise.

***

## Step 5: View the Default Volume

Navigate to your instance → **Storage tab**.

**What you see:** The Volume ID linked to this instance. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

### Alternative path:

**EC2 Console → Elastic Block Store → Volumes**

**What you see:** The volume ID, the instance it's attached to (shown in the Attachment column), and the size (e.g., 8 GB for most default Linux AMIs). [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Note:** Detailed volume operations are covered in a dedicated future lecture. This step is just about knowing where to find the default volume.

***

## Step 6: Check the EC2 Dashboard

Navigate to: **EC2 Console → Dashboard**

Refresh and observe the resource counts: [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

* Running instances: 1
* Key pairs: 1
* Security groups: 2
* Elastic IPs: 1
* Volumes: 1

**Operational habit:** Check this dashboard regularly to detect orphaned resources that may be incurring charges.

***

## Step 7: Change the Instance Type (Vertical Scaling)

### Stop the instance first:

**Actions → Instance State → Stop Instance → Confirm**

Wait for "Stopped" state. The instance type change option is **grayed out while running** — it only works on stopped instances. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

### Change the type:

**Actions → Instance Settings → Change Instance Type**

Current type: `t2.micro` (1 vCPU, 1 GB RAM)

Change to: `t2.small` (1 vCPU, 2 GB RAM) [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**What you see:** A comparison table showing vCPU, memory, and pricing between the current and target types.

Click **Apply**.

### Start the instance:

**Actions → Instance State → Start Instance**

**Expected result:** The instance now runs as `t2.small` with 2 GB RAM. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**Cost warning:** `t2.small` is NOT in the free tier. The instructor warns: "You don't need to do this. Just watch." If you did it, change back to `t2.micro` afterward to avoid charges. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

***

## Step 8: Enable Termination Protection

**Actions → Instance Settings → Change Termination Protection**

Check the box to **Enable** → **Save** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

### Test it:

Try to terminate: **Actions → Instance State → Terminate (Delete)**

**Expected result:** An error. The termination is blocked because protection is enabled.

**Connection to flow:** This must be disabled before the instance can be deleted in the cleanup step.

***

## Step 9: Modify Security Groups (Live)

**Actions → Security → Change Security Groups**

**What you can do:** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

* Click **Add Security Group** to add another security group
* Click the **X** next to a security group to remove it

The instructor adds the "default" security group, then removes it again — demonstrating that this is a live, non-disruptive change. No instance stop required.

Click **Save** after making changes.

***

## Step 10: View the System Log

**Actions → Monitor and Troubleshoot → Get System Log** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

**What you see:** The boot log of the instance. This is not live — it's a snapshot that takes time to load.

**When to use:** When the instance won't boot after OS-level changes. The boot log reveals where the startup process failed.

You can also **download** the log for offline analysis.

***

## Step 11: Full Cleanup

### 11a. Disable termination protection:

**Actions → Instance Settings → Change Termination Protection → Uncheck → Save** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

### 11b. Terminate the instance:

**Actions → Instance State → Terminate (Delete) → Confirm**

The instance enters "shutting-down" then "terminated" state. [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

### 11c. Release the Elastic IP:

Navigate to: **EC2 Console → Network and Security → Elastic IPs**

**Refresh** the page. Select the Elastic IP → **Actions → Release Elastic IP Address → Confirm Release** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)

⚠️ **Critical:** Do not skip this. An unreleased Elastic IP that's not associated with a running instance **incurs charges**. Always release Elastic IPs you no longer need.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ EC2 Instance — Component Architecture

```
EC2 Instance
│
├── COMPUTE
│   ├── Instance Type (t2.micro, t2.small, ...)
│   │   └── changeable (requires STOP first)
│   └── AMI (source image)
│
├── STORAGE
│   └── Volume (EBS)
│       ├── Created from AMI on launch
│       ├── Default Linux: 8 GB (varies by AMI)
│       └── Detailed in future lecture
│
├── NETWORKING ──→ attached to NETWORK INTERFACE (not directly to instance)
│   ├── Network Interface (default: 1, can have multiple)
│   │   ├── Private IP (STATIC — persists until instance terminated)
│   │   ├── Public IP (DYNAMIC — released on stop, new on start)
│   │   ├── Elastic IP (STATIC PUBLIC — survives stop/start)
│   │   └── Security Group(s) (changeable LIVE, no stop needed)
│   │
│   └── Additional Network Interfaces (optional)
│       └── Each has own: Private IP, Public IP, Elastic IP, Security Groups
│
├── SECURITY
│   ├── Security Group → on network interface
│   ├── Termination Protection (enable/disable)
│   ├── IAM Role (covered later)
│   └── Key Pair
│
└── MONITORING
    └── System Log (boot log, not live, downloadable)
```

***

## ⚡ IP Behavior — Instant Recall

```
PRIVATE IP:
  Assigned on launch → NEVER changes → released only on TERMINATE
  Used for: internal VPC communication

PUBLIC IP (regular):
  Assigned on launch → RELEASED on stop → NEW IP on start
  Used for: internet access (dynamic, non-persistent)

ELASTIC IP:
  Manually allocated → associated to instance/interface
  → PERSISTS through stop/start → released manually
  Limit: 5 per account | NOT free | must release when done
```

***

## 🔗 Network Interface — Central Attachment Point

```
"Anything related to networking → attached to NETWORK INTERFACE"

Network Interface holds:
  ├── Private IP
  ├── Public IP
  ├── Elastic IP
  └── Security Group(s)

Instance can have 1+ network interfaces
Each interface = independent network identity

Elastic IP association options:
  Instance → targets default interface (simple)
  Network Interface → targets specific interface (multi-interface)
```

***

## 🔄 Operations Requiring STOP vs. LIVE

```
REQUIRES STOP:
  ├── Change Instance Type (vertical scaling)
  └── (grayed out while running)

LIVE (no stop needed):
  ├── Change Security Groups
  ├── Enable/Disable Termination Protection
  ├── Associate/Disassociate Elastic IP
  ├── Attach/Detach Network Interface
  └── Modify IAM Role
```

***

## 🔒 Termination Protection Flow

```
Enable Protection:
  Actions → Instance Settings → Change Termination Protection → Enable

With Protection ON:
  Terminate attempt → BLOCKED (error)

To terminate:
  Disable protection FIRST → then terminate succeeds

Purpose: prevent accidental deletion in shared environments
```

***

## 🧹 Cleanup Sequence — Critical

```
1. Disable termination protection (if enabled)
      Actions → Instance Settings → Uncheck → Save
2. Terminate instance
      Actions → Instance State → Terminate
3. Release Elastic IP
      Network & Security → Elastic IPs → Select → Release
      ⚠️ Unreleased Elastic IP = ongoing charges

DASHBOARD CHECK:
  EC2 Dashboard → verify: 0 instances, 0 elastic IPs, 0 extra volumes
  "Always keep track of your EC2 dashboard"
```

***

## 📊 Instance Type Change — Vertical Scaling

```
FLOW:
  Stop instance → Actions → Instance Settings → Change Instance Type
  → Select new type → see comparison (vCPU, RAM, price)
  → Apply → Start instance

t2.micro: 1 vCPU, 1 GB (free tier)
t2.small: 1 vCPU, 2 GB (NOT free tier)

KEY: Cloud elasticity = scale up/down by changing type
COST: Bigger type = higher hourly rate
DOWNTIME: Required (must stop to change)
```

***

## 📦 Volume — Default Relationship

```
Launch Instance → Select AMI → AMI defines default volume
  ├── Most Linux AMIs → 8 GB
  ├── Some AMIs → 20, 30, 120 GB
  └── Volume visible: Instance → Storage tab → Volume ID
      OR: EC2 → Elastic Block Store → Volumes
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Networking-as-Interface-Attachment**
Network properties (IP, security, elastic IP) don't attach to the compute unit directly — they attach to a **network interface** which the compute unit uses. This decoupling allows: interface migration between instances, multiple network identities per instance, independent security policies per interface. This pattern appears throughout cloud and virtualized networking.

**Pattern 2: Static-by-Reservation**
Default resources are dynamic/ephemeral (public IP changes). Static behavior requires **explicit reservation** (Elastic IP allocation). Reserved resources are scarce and cost money. This trade-off — dynamic-default, static-costs-extra — is a recurring cloud economics pattern.

**Pattern 3: Protection-Before-Destruction**
Critical resources should have deletion protection enabled. Destruction requires a deliberate two-step: disable protection → then delete. This guard-then-destroy pattern prevents accidental data loss and appears across AWS services (RDS deletion protection, S3 bucket policies, etc.).

**Pattern 4: Dashboard-as-Resource-Hygiene**
A centralized dashboard showing all active resources is the primary tool for preventing cost leaks. Regularly checking it catches orphaned resources (unused Elastic IPs, detached volumes, forgotten instances) before they accumulate charges.

***

## 🎯 One-Line System Summary

> **An EC2 instance's networking (private IP, public IP, Elastic IP, security groups) is attached to its network interface — not directly to the instance — enabling flexible multi-interface configurations; the public IP is dynamic (changes on stop/start) while Elastic IPs provide static public addressing at a cost; instance types can be vertically scaled (requires stop); termination protection prevents accidental deletion; and proper cleanup (terminate + release Elastic IP) is essential to avoid ongoing charges.** [\[115-more-i...-ec2-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/115-more-in-ec2-part2.txt)
