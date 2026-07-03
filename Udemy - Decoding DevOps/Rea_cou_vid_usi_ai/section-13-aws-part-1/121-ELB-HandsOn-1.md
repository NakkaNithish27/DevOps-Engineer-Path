# ⚖️ ELB Hands On Part 1 — AMIs, Snapshots & Launch Templates — Deep Learning Material

**Source:** Video caption file — [121. ELB Hands On Part 1.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt?EntityRepresentationId=070cee8c-eff6-4b8d-9659-aa081f521fb3), with supporting script — [121.multios\_websetup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.multios_websetup.txt?EntityRepresentationId=95c50d21-edf0-474c-b263-9a28ea9e50eb) [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt), [\[121.multios_websetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.multios_websetup.txt)

**Video Context:** The instructor begins the Elastic Load Balancer (ELB) section, but before creating the load balancer itself, builds the prerequisite infrastructure: launching an EC2 instance running a website via user data, creating an AMI (Amazon Machine Image) from that instance to enable replica creation, and introducing launch templates to standardize and speed up instance launches. The core goal: prepare the ability to create **multiple identical instances** that will sit behind a load balancer.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Bigger Picture — Why We Need Replicas Before a Load Balancer

The instructor opens with: "First we need to have an instance running a website." But the real purpose emerges quickly: "If we need a group of instances — usually this will be the case — behind the load balancer, there will be multiple instances that will be basically replica of each other." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

A load balancer distributes incoming traffic across multiple backend instances. For this to work, those backend instances must be **identical** — same OS, same application, same configuration. Creating each one manually from scratch (install packages, deploy code, configure services) would be slow and error-prone. The solution is a two-step process: first, build **one** perfectly configured instance. Second, create an **image** (AMI) of that instance. From the AMI, you can stamp out as many identical replicas as needed, quickly and reliably.

This entire lecture is about building that pipeline: **running instance → AMI → replica instances → (future) load balancer**.

***

## 1.2 User Data — Automating Instance Configuration at Launch

When launching the EC2 instance, the instructor uses the **User Data** field under Advanced Details to provide a shell script. This script runs **automatically when the instance first boots**. The instructor states: "This is a multi-OS script for Linux. So it can be an RPM-based or Debian-based. It's going to set up Inner Peace website on CentOS type or Debian type like Ubuntu." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

User Data is the mechanism by which EC2 instances can **self-configure** on first boot without manual SSH intervention. You paste a script into the User Data field during launch, and the EC2 service injects it into the instance and executes it as part of the boot process. This is what transforms a bare OS image into a fully configured web server — automatically.

The script provided is the `multios_websetup.txt` — a bash script that detects the OS type (by testing if `yum` works), sets the appropriate package names and service names (`httpd` for CentOS, `apache2` for Ubuntu), installs packages, starts and enables the web service, downloads a website template from tooplate.com, deploys it to `/var/www/html`, restarts the service, and cleans up. [\[121.multios_websetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.multios_websetup.txt)

🔍 **Deep Dive:** The OS detection mechanism in the script is clever: it runs `yum --help &> /dev/null` and checks the exit code (`$?`). If `yum` succeeds (exit code 0), the system is RPM-based (CentOS/Amazon Linux), and it sets `PACKAGE="httpd wget unzip"` and `SVC="httpd"`. If `yum` fails (non-zero exit), it falls into the `else` branch and sets `PACKAGE="apache2 wget unzip"` and `SVC="apache2"` for Debian/Ubuntu. The `&> /dev/null` redirects both stdout and stderr to suppress all output — we only care about the exit code, not the output. This pattern — **probe a system tool and branch based on success/failure** — is a reusable OS-detection technique. [\[121.multios_websetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.multios_websetup.txt)

***

## 1.3 Security Group Configuration — Preparing for Load Balancer Architecture

The instructor creates a security group with two inbound rules: **port 22 (SSH) from "My IP"** and **port 80 (HTTP) from "My IP"**. Critically, the instructor notes: "Later we'll have some work on the security group because we are not going to directly access this instance website. We are going to access it through the load balancer. And I'm going to teach you some important points to keep in mind when doing security group." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

This foreshadows a key architectural principle: in a load-balanced setup, users don't hit the backend instances directly — they hit the load balancer. The security group on the instances should eventually be restricted to accept traffic **only from the load balancer**, not from the open internet. Setting it to "My IP" for now is a temporary development convenience that will be tightened later.

***

## 1.4 AMI (Amazon Machine Image) — The Instance Replication Mechanism

An **AMI** is the core concept of this lecture. The instructor explains it precisely: "This basically takes the snapshot of the EBS volume plus the metadata. So snapshot is just simply the copy of the EBS volume. But AMI is the snapshot plus the metadata, the instance information." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

This distinction is critical:

**Snapshot** = a point-in-time copy of the EBS volume (the disk). It captures everything on the disk — the OS, installed packages, deployed application, configuration files, data. It's a raw disk image.

**AMI** = Snapshot + **metadata**. The metadata includes the instance information: what instance type was used, the architecture (x86, ARM), the root device mapping, block device mappings, virtualization type, and other launch parameters. The AMI is what you actually use to **launch new instances** — it contains both the disk content (via the snapshot) AND the information needed to configure the instance correctly.

Think of it this way: a snapshot is a hard drive clone. An AMI is a hard drive clone + the blueprint for the computer it goes into.

When you create an AMI from a running instance, AWS automatically creates a snapshot of the instance's EBS volume(s) as part of the process. The AMI then references that snapshot. You can see the snapshot appear in the Snapshots section of the EC2 console. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

***

## 1.5 AMI Creation — The Reboot Consideration

When creating an AMI, there is an option: **"Reboot instance"** (enabled by default). The instructor explains: "When the image is taken, the instance will get rebooted. But for some reason you do not want any downtime — this is a production live instance, you don't want any reboot — then you can uncheck this option, and that takes a longer time to create the AMI." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

**Why reboot?** To ensure filesystem consistency. When an instance is running, data may be in memory buffers that haven't been flushed to disk yet. Rebooting forces all data to be written to disk, ensuring the snapshot captures a clean, consistent state.

**Why skip reboot?** If the instance is serving live production traffic and any downtime is unacceptable. Without reboot, AWS takes the snapshot of the live disk, which may have minor inconsistencies (unflushed buffers). The trade-off: longer creation time and potential minor inconsistencies vs. zero downtime.

The instructor keeps the default (reboot enabled) for this exercise.

***

## 1.6 AMI Lifecycle — States and Timing

After creation, the AMI goes through states: **pending → available**. The instructor shows: "It's not yet created, it's in the pending state. So let's wait for a few minutes until this becomes available." The wait is approximately five minutes. Only after reaching "available" can the AMI be used to launch instances. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

***

## 1.7 Cross-Region AMI Copy — Moving Instances Between Regions

The instructor highlights a specific AMI action: **Copy AMI**. "If you want to copy an instance from one region to another region, you need to create its AMI. And then you can do the copy option and select the destination region." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

This is significant because **EC2 instances cannot be directly moved between regions**. They exist in one region. The only way to "move" or replicate an instance to another region is:

1. Create an AMI of the instance (in the source region)
2. Copy the AMI to the destination region
3. Launch a new instance from the copied AMI in the destination region

The instructor notes this is a "pretty interesting interview question" — a common AWS knowledge checkpoint. During the copy, you also get the option to **encrypt** the AMI in the destination region. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

***

## 1.8 Cross-Account AMI Sharing — Moving Instances Between Accounts

Through **Edit Permissions** on an AMI, you can share it with other AWS accounts. You add the target account ID, and the AMI becomes available in that account. The instructor frames this as: "That is how to copy an AMI or instance from one account to another account. So it's not a direct copy. You need to take always the AMI." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

The pattern is consistent: **the AMI is always the transfer vehicle**. Whether you're replicating within a region, copying across regions, or sharing across accounts — you always go through the AMI.

***

## 1.9 AMI Cleanup — Deregister + Delete Snapshot

The instructor explicitly covers the cleanup process: "If you're not using the AMI, you need to deregister the AMI. And then you need to delete the snapshot." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

This is a **two-step cleanup** — deregistering the AMI removes it from the AMI catalog, but the underlying snapshot still exists (and incurs storage charges). You must separately delete the snapshot. Forgetting the snapshot is a common resource leak.

***

## 1.10 EC2 Image Builder — Automated AMI Pipeline (Brief Mention)

The instructor briefly mentions **EC2 Image Builder**: "There is a service that can build the image automatically like we built it manually. There's a way to build it automatically and also keep patching, updating your AMI regularly. That can be done automatically. You can also call it as image pipeline." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

He notes this won't make full sense until the CI/CD section — but the key concept is that AMI creation can be automated into a **pipeline** that regularly rebuilds and patches images, rather than being a manual point-in-time operation.

***

## 1.11 Launch Templates — Standardized Instance Configuration

After AMIs solve the "what's on the disk" problem, **Launch Templates** solve the "how to configure the instance" problem. The instructor explains: "You can save all this information into a template and you just say launch instance from the template and that's it. The instance will be up and running in a minute or so." [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

When launching an instance manually, you specify many parameters: name, AMI, instance type, key pair, security group, network settings, user data, etc. A Launch Template saves all of these settings into a reusable template. Future launches reference the template instead of re-specifying every parameter.

The AWS console describes them as: "Streamline, simplify, and standardize instance launches." This is directly relevant to load balancers: when you need to quickly spin up additional identical instances behind a load balancer, a launch template ensures every new instance is configured exactly the same way — same AMI, same instance type, same security group, same everything. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

The relationship: **AMI captures the disk state** (OS + application + data). **Launch Template captures the launch configuration** (instance type, key pair, security group, network, user data). Together, they fully define a reproducible instance.

🔍 **Deep Dive:** Launch Templates become essential when combined with **Auto Scaling Groups** (covered in future lectures). An Auto Scaling Group uses a Launch Template to automatically launch new instances when demand increases and terminate them when demand decreases. Without a Launch Template, Auto Scaling wouldn't know how to configure the new instances. The chain is: Launch Template defines the instance spec → Auto Scaling Group manages the instance count → Load Balancer distributes traffic across instances.

***

## 1.12 The Multi-OS Web Setup Script — Architecture

The supporting script (`multios_websetup.txt`) deserves analysis as it's used as the User Data for the EC2 instance. Its structure: [\[121.multios_websetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.multios_websetup.txt)

**Variables declared at the top:**

* `URL` — the download URL for the website template
* `ART_NAME` — the artifact name (template folder name after extraction)
* `TEMPDIR` — temporary workspace directory

**OS detection:** `yum --help &> /dev/null` + exit code check. If `yum` works → CentOS path. If not → Ubuntu path.

**CentOS path:** Sets `PACKAGE="httpd wget unzip"`, `SVC="httpd"`, uses `yum install`.

**Ubuntu path:** Sets `PACKAGE="apache2 wget unzip"`, `SVC="apache2"`, uses `apt update` + `apt install`.

**Both paths then follow identical logic:** install packages → start/enable service → create temp dir → download artifact → unzip → copy to `/var/www/html` → restart service → cleanup → verify (status + ls).

The script uses all the patterns from earlier scripting lectures: variables for configurability, `> /dev/null` for output suppression, `mkdir -p` for idempotency, echo statements with hash separators for readability, `sudo` for privilege elevation, and verification commands at the end.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building the **prerequisite infrastructure for an Elastic Load Balancer**: a running EC2 instance serving a website, an AMI created from that instance (enabling rapid replica creation), and a Launch Template (standardizing instance configuration). The final outcome: the ability to launch multiple identical web server instances quickly, ready to be placed behind a load balancer. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

***

## Step 1: Prepare the Web Setup Script

Download the script from the lecture resource section. This is the multi-OS web setup script (`multios_websetup.txt`). [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt), [\[121.multios_websetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.multios_websetup.txt)

**What the script does (brief):** Detects the OS (RPM or Debian), installs the web server and tools, downloads a website template from tooplate.com ("Inner Peace" template), deploys it to the web root, starts the service, and cleans up. It will be used as **User Data** during instance launch.

**Verification:** Open the script and confirm it starts with `#!/bin/bash` and contains the `yum --help` OS detection block.

***

## Step 2: Launch the EC2 Instance

Navigate to **EC2 Console → Launch Instance**.

### Configuration: [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

**Name:** `web01`

**AMI:** Amazon Linux 2023 (or Ubuntu — the script handles both). The instructor uses Amazon Linux 2023.

**Instance Type:** `t2.micro` (free tier)

**Key Pair:** Create a new key pair. The instructor names it `inner peace key`. Click **Create Key Pair** and **download** the `.pem` file.

**Security Group:** Create a new security group. Click **Edit** next to Security Groups.

* **Name:** `inner security`
* **Rule 1:** SSH (port 22) — Source: **My IP**
* **Rule 2:** HTTP (port 80) — Source: **My IP**

**Important:** The instructor emphasizes setting port 80 to "My IP" specifically. This will be modified later when the load balancer is introduced — at that point, the instances should only accept traffic from the load balancer, not directly from the internet. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### User Data:

Scroll down to **Advanced Details → User Data**.

Paste the entire content of the `multios_websetup.txt` script into the User Data field. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

Click **Launch Instance**.

### Verification:

Wait **2-5 minutes** for the instance to boot, run the user data script, and have the website fully deployed. Then:

1. Go to the instance details, copy the **Public IP**
2. Open a browser, navigate to `http://<Public_IP>`
3. The "Inner Peace" website should load [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

**If the website doesn't load:**

* Check the instance is in "running" state
* Verify the security group allows port 80 from your IP
* SSH into the instance and check if the web service is running (`systemctl status httpd` or `systemctl status apache2`)
* Check `/var/log/cloud-init-output.log` for user data script execution errors

**Connection to flow:** This running instance with its fully configured website is the "golden instance" — the source from which we'll create the AMI.

***

## Step 3: Create an AMI from the Running Instance

Navigate to **EC2 Console → Instances**. Select the instance.

**Actions → Image and Templates → Create Image** [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### Settings:

**Image name:** `Inner Peace image` (or any descriptive name)

**Reboot instance:** Leave **checked** (default). This reboots the instance during AMI creation to ensure disk consistency. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

⚠️ **Expert Note:** If this were a production instance serving live traffic, you could **uncheck** "Reboot instance" to avoid downtime. The trade-off: longer creation time and potential minor filesystem inconsistencies. For this exercise, keep the default.

Click **Create Image**.

### Monitor AMI creation:

Navigate to **EC2 Console → Images → AMIs** (left panel).

**Expected state:** The AMI shows as **"Pending"**. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

**Wait approximately 5 minutes** until the status changes to **"Available"**.

### Tag the AMI:

While waiting, edit the **Name tag** of the AMI: give it the same descriptive name (`Inner Peace image`). [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### Verify the associated snapshot:

Navigate to **EC2 Console → Elastic Block Store → Snapshots**.

A new snapshot should appear, created automatically as part of the AMI process. This is the disk copy that the AMI references. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

**Connection to flow:** The AMI is now the reusable template for creating identical instances. Any instance launched from this AMI will have the same OS, packages, website, and configuration.

***

## Step 4: Explore AMI Operations (Informational — No Action Required)

Select the AMI → **Actions**. The following options are available: [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### 4a. Copy AMI (Cross-Region):

**Actions → Copy AMI**

**Destination:** Select any other AWS region.

**Use case:** Replicating an instance to another region. This is the **only** way to move/copy an instance across regions.

**Optional:** Enable encryption during copy.

**Do NOT actually copy** — this is informational. Just observe the option. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### 4b. Edit AMI Permissions (Cross-Account):

**Actions → Edit AMI Permissions**

**What you can do:** Add another AWS account ID to share the AMI with that account.

**Use case:** Sharing an instance configuration with another team or organization's AWS account. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### 4c. EC2 Image Builder:

A separate AWS service (not an AMI action) that automates AMI creation, patching, and updates as a pipeline. Mentioned for awareness — detailed coverage comes later with CI/CD. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

***

## Step 5: Launch an Instance from the AMI (Manual Method)

Select the AMI → **Launch Instance from AMI** [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

This opens the standard instance launch wizard, but with the AMI **pre-selected** (under "My AMIs" section). You still need to specify:

* Instance name
* Instance type
* Key pair
* Security group
* All other launch parameters

**This is the manual method** — functional but requires re-specifying all parameters every time. The instructor demonstrates this to show it works, then introduces Launch Templates as the better approach.

**The instructor cancels this** to proceed to Launch Templates instead. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

***

## Step 6: Create a Launch Template

Navigate to **EC2 Console → Instances → Launch Templates** (left panel).

Click **Create Launch Template**. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

**What to include in the template:**

* **AMI:** Select your "Inner Peace image" AMI (from My AMIs)
* **Instance type:** `t2.micro`
* **Key pair:** Select the existing key pair
* **Security group:** Select the existing security group
* **Any other settings** you want standardized (network, storage, user data, etc.)

**Purpose:** Once saved, launching a new instance requires only: **select template → launch**. All parameters are pre-filled from the template. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

**Connection to flow:** Launch Templates are the bridge to automated scaling. When an Auto Scaling Group (future lecture) needs to launch new instances, it reads the Launch Template to know exactly how to configure them. This is also what makes load balancer setups practical — you can quickly spin up identical instances as needed.

🔍 **Deep Dive:** The relationship chain for a production load-balanced setup: **Launch Template** (defines how to build an instance) → **Auto Scaling Group** (decides when and how many to launch) → **Load Balancer** (distributes traffic across launched instances). The Launch Template is the foundational building block that everything else depends on.

***

## Step 7: Cleanup (When Done with the Entire ELB Exercise)

When you're finished with the full ELB exercise (across future lectures), clean up in this order: [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### 7a. Terminate instances:

Terminate all instances launched from the AMI.

### 7b. Deregister the AMI:

**EC2 → Images → AMIs → Select → Actions → Deregister AMI**

This removes the AMI from your catalog but does **NOT** delete the snapshot.

### 7c. Delete the snapshot:

**EC2 → Elastic Block Store → Snapshots → Select → Actions → Delete Snapshot**

⚠️ **Critical:** Both steps are required. Deregistering the AMI without deleting the snapshot leaves an orphaned snapshot that still incurs storage charges. [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt)

### 7d. Delete the Launch Template:

**EC2 → Launch Templates → Select → Actions → Delete**

### 7e. Release any Elastic IPs, delete security groups and key pairs if no longer needed.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ The Replica Pipeline — Why This Lecture Exists

```
GOAL: Multiple identical instances behind a Load Balancer

PIPELINE:
  1. Launch ONE instance with User Data script → configured web server
  2. Create AMI from that instance → reusable disk image + metadata
  3. Create Launch Template → reusable launch configuration
  4. (Future) Launch multiple instances from template → identical replicas
  5. (Future) Place replicas behind Load Balancer → distributed traffic
```

***

## 🏗️ AMI Architecture — Core Concept

```
AMI = Snapshot + Metadata

Snapshot:
  └── Point-in-time copy of EBS volume (disk content)
      └── OS + packages + application + data + config

Metadata:
  └── Instance information (type, architecture, device mappings, etc.)

TOGETHER → complete blueprint to launch identical instances

STATES: Pending → Available (wait ~5 min)
```

***

## 🔗 AMI as Transfer Vehicle

```
WITHIN REGION:
  AMI → Launch Instance → identical replica

CROSS-REGION:
  AMI → Copy AMI (select destination region) → new AMI in target region
  → Launch Instance in target region
  (option: encrypt during copy)

CROSS-ACCOUNT:
  AMI → Edit Permissions → Add Account ID → AMI shared to other account

PATTERN: Instance can NEVER be directly moved/copied.
         ALWAYS go through AMI.
```

***

## ⚡ AMI Creation — Decision Points

```
Create Image from Instance:
  ├── Reboot: CHECKED (default)
  │   └── Forces filesystem consistency
  │   └── Causes brief downtime
  │
  └── Reboot: UNCHECKED
      └── No downtime (production-safe)
      └── Longer creation time
      └── Possible minor disk inconsistencies

SIDE EFFECT: Snapshot auto-created in EBS → Snapshots section
```

***

## 📦 Launch Template vs. Manual Launch

```
MANUAL LAUNCH (from AMI):
  Select AMI → specify name, type, key, SG, network... → launch
  ⚠️ Must re-enter ALL parameters every time

LAUNCH TEMPLATE:
  Save ALL parameters once → future launches = select template → launch
  ✅ Consistent, fast, automatable

TEMPLATE CAPTURES:
  AMI + Instance Type + Key Pair + Security Group + Network + User Data + ...

CRITICAL LINK:
  Launch Template → Auto Scaling Group → Load Balancer
  (template is the foundation of automated scaling)
```

***

## 🔄 AMI Cleanup Sequence — Two-Step (Don't Forget Snapshot)

```
STEP 1: Deregister AMI
  EC2 → AMIs → Select → Actions → Deregister
  (removes AMI from catalog, snapshot STILL EXISTS)

STEP 2: Delete Snapshot
  EC2 → Snapshots → Select → Actions → Delete
  (removes the actual disk copy, stops storage charges)

⚠️ Forgetting Step 2 = orphaned snapshot = ongoing charges
```

***

## 🛡️ Security Group — Current vs. Future State

```
CURRENT (this lecture):
  Port 22: My IP      ← SSH access for management
  Port 80: My IP      ← HTTP for testing directly

FUTURE (with Load Balancer):
  Port 22: My IP      ← SSH stays same
  Port 80: Load Balancer SG only  ← instances accept HTTP ONLY from LB
  
  Users → Load Balancer → Instances (not Users → Instances directly)
```

***

## 📜 Multi-OS Web Setup Script — Logic Map

```
#!/bin/bash
│
├── VARIABLES: URL, ART_NAME, TEMPDIR
│
├── OS DETECTION: yum --help &> /dev/null
│   ├── exit 0 (yum works) → CentOS/Amazon Linux path
│   │   └── PACKAGE="httpd wget unzip", SVC="httpd"
│   │   └── yum install
│   │
│   └── exit ≠ 0 (yum fails) → Ubuntu/Debian path
│       └── PACKAGE="apache2 wget unzip", SVC="apache2"
│       └── apt update + apt install
│
├── BOTH PATHS (identical logic):
│   ├── Install $PACKAGE
│   ├── Start + Enable $SVC
│   ├── mkdir -p $TEMPDIR → cd → wget $URL → unzip
│   ├── cp -r to /var/www/html
│   ├── Restart $SVC
│   ├── Cleanup $TEMPDIR
│   └── Verify: systemctl status + ls
│
└── Used as: EC2 User Data (runs on first boot)
```

***

## 🔁 EC2 Image Builder (Brief Recall)

```
Manual AMI creation: one-time, point-in-time, human-triggered
EC2 Image Builder: automated pipeline, regular patching/updates
  └── "Image Pipeline" — builds, tests, distributes AMIs automatically
  └── Full understanding after CI/CD section
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Golden Image Pipeline**
Build one instance perfectly → capture as image (AMI) → stamp out replicas. This is the standard pattern for creating consistent server fleets in any cloud or virtualized environment. The "golden image" is the single source of truth for what an instance should look like.

**Pattern 2: AMI = Universal Transfer Medium**
Any instance movement — within region, across regions, across accounts — requires going through the AMI. There is no direct instance copy. The AMI is the serialization format for EC2 instances, just like a Docker image is the serialization format for containers.

**Pattern 3: Configuration Layering (AMI + Launch Template)**
AMI captures **what's on the disk** (OS, application, data). Launch Template captures **how to launch** (instance type, network, security, key pair). Together they fully define a reproducible instance. Neither alone is sufficient — both layers are needed.

**Pattern 4: Two-Step Cleanup for Composite Resources**
When a resource is composed of multiple sub-resources (AMI = catalog entry + snapshot), deleting the parent doesn't delete the children. You must clean up each layer independently. This pattern recurs across AWS: deleting a CloudFormation stack vs. its resources, removing a load balancer vs. its target groups, etc.

***

## 🎯 One-Line System Summary

> **To prepare for load balancing, launch one EC2 instance configured via User Data script, create an AMI (snapshot + metadata) to capture its state as a reusable image, and save launch parameters in a Launch Template — enabling rapid, consistent creation of identical replica instances that can be placed behind a load balancer for traffic distribution.** [\[121. ELB H...On Part 1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.%20ELB%20Hands%20On%20Part%201.txt), [\[121.multios_websetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/121.multios_websetup.txt)
