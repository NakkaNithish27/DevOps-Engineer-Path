# 📘 Disk Space Issue in Jenkins — Deep Learning Material

> **Source:** Lecture 162 — *Disk Space Issue* (Caption file analysis) [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

***

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. The Disk Space Problem in Jenkins

When you run Jenkins on a cloud-based virtual machine — in this course, an **AWS EC2 instance** — the server comes with a finite amount of storage. By default, a standard EC2 instance is provisioned with an **8 GB root volume** (an EBS volume). This 8 GB is not just for Jenkins; it holds the entire operating system, system libraries, logs, temporary files, and everything else that lives on that machine. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

Jenkins, by its nature, is a storage-hungry application. There are three main reasons why it consumes disk space aggressively:

**Plugins** — Jenkins' power comes from its plugin ecosystem. As you progress through a course or a real project, you install many plugins (build tools, SCM integrations, notification plugins, pipeline libraries, etc.). Each plugin is a `.hpi` or `.jpi` file that gets extracted into the Jenkins home directory. Individually they're small, but collectively — especially with dependencies — they accumulate. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**Jobs and build artifacts** — Every Jenkins job creates a **workspace** directory where it checks out source code, compiles, runs tests, and stores artifacts. Each build run can leave behind compiled binaries, test reports, Docker layers, logs, and more. If you have multiple jobs running frequently, workspace sizes grow rapidly. Jenkins also retains build history (console logs, build metadata) by default, which compounds over time. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**General accumulation** — System logs (`/var/log`), package manager caches, temporary files from builds, and even Docker images (if Docker is installed on the same host) all eat into that 8 GB ceiling.

The result: your Jenkins job fails, and in the **console output** (the build log), you see the error:

    No space left on device

This is a Linux-level error (`ENOSPC`), meaning the filesystem literally cannot write another byte. It's not a Jenkins-specific error — any process on the machine that tries to write will fail. But because Jenkins is the most write-heavy application on this instance, it's the one that surfaces the error first. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

> 🔍 **Deep Dive (Optional)**
>
> The "no space left on device" error maps to Linux errno `ENOSPC` (error code 28). When any process issues a `write()` system call and the filesystem has zero free blocks, the kernel returns this error. In Jenkins, this can manifest in many ways: a Git clone failing mid-checkout, a Maven build failing during compilation, or even Jenkins itself failing to save its own configuration XML files — which can corrupt your Jenkins setup if it happens at the wrong moment.

> ⚠️ **Expert Note (Optional)**
>
> In production, you should never wait for "no space left" to appear. Set up disk monitoring (CloudWatch alarms on EBS, or Prometheus `node_filesystem_avail_bytes`) to alert at 80% usage. Jenkins also has a built-in **Disk Space Monitor** (under Manage Jenkins → Configure System) that can take nodes offline when free space drops below a threshold.

***

### 2. AWS EC2 Root Volumes and EBS

When you launch an EC2 instance, AWS attaches a **root volume** to it. This root volume is an **EBS (Elastic Block Store)** volume — essentially a virtual hard drive that lives on AWS's storage infrastructure and is network-attached to your EC2 instance. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

The default size of this root volume depends on the AMI (Amazon Machine Image) you launched from, but for most standard Linux AMIs, it's **8 GB**. This is a general-purpose default designed for lightweight workloads. For a CI/CD server like Jenkins that accumulates data over time, 8 GB is insufficient. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

The key insight is: **EBS volumes are elastic** — you can resize them without destroying or detaching them. AWS allows you to **modify** a volume's size, type, and IOPS while it's still attached and even while the instance is running. This is the solution the video teaches. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

> 🔍 **Deep Dive (Optional)**
>
> EBS volumes are not physically inside your EC2 instance. They communicate over AWS's internal network. This is why you can resize, snapshot, and even detach/reattach them independently. The volume's device name in Linux (e.g., `/dev/xvda`) is a virtual device that the hypervisor maps to the remote EBS block device. The `xvda` naming convention comes from Xen virtualization (`xv` = Xen virtual, `d` = disk, `a` = first disk). Newer Nitro-based instances may show `/dev/nvme0n1` instead.

***

### 3. Disk Partitions vs. Volumes — Understanding the Size Difference

A concept the video demonstrates practically but doesn't explicitly name is the relationship between a **volume** (the raw block device) and a **partition** (a logical division within that block device).

When the instructor runs `fdisk -l`, the output shows: [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

*   **Disk `/dev/xvda`**: 8 GB — this is the entire raw EBS volume
*   **Partition `/dev/xvda1`**: \~7 GB — this is the usable partition within that volume

The reason the partition is smaller than the volume is that a small portion of the disk is reserved for the **partition table** (the data structure that tells the OS where partitions begin and end) and potential boot sectors. In a typical Linux setup with a single partition, you lose a tiny amount of space to this overhead, which is why 8 GB becomes \~7 GB usable. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

Similarly, when `df -h` is run, it shows **6.8 GB** — even less than the 7 GB partition — because every filesystem reserves a percentage of blocks (typically 5% on ext4) for the root user and system operations, and the filesystem metadata (inodes, superblocks, journal) also consumes space. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

After the resize to 20 GB, `df -h` shows **19 GB** — the same principle applies, just proportionally less noticeable at larger sizes. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

> 🔍 **Deep Dive (Optional)**
>
> The three layers of "size" you see are:
>
> 1.  **EBS Volume size** (what you set in AWS Console) — the raw block device capacity
> 2.  **Partition size** (what `fdisk -l` reports for `/dev/xvda1`) — slightly smaller due to partition table overhead
> 3.  **Filesystem usable size** (what `df -h` reports) — smaller still due to filesystem reserved blocks and metadata
>
> Modern Amazon Linux 2 / Ubuntu AMIs include `cloud-init` scripts and `growpart` utilities that **automatically** grow the partition and filesystem on reboot when they detect the underlying volume has been enlarged. This is why the instructor's reboot "just works" without manually running `growpart` or `resize2fs`. On older or custom AMIs, you might need to do this manually.

***

### 4. The `df -h` and `fdisk -l` Commands — Diagnostic Tools

These two commands are fundamental Linux disk diagnostic tools, and understanding the difference between them is critical:

**`df -h`** (disk free, human-readable) shows **filesystem-level** usage — how much space is used, available, and the mount point. It answers: "How much room does my OS think it has right now?" The `-h` flag converts bytes into human-readable units (GB, MB). [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**`fdisk -l`** (fixed disk, list) shows **partition-level** information — the raw disk devices, their total size, and how they're partitioned. It answers: "What physical/virtual disks does the machine have, and how are they divided?" The `-l` flag means "list" (display without entering interactive mode). [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

You use both together because they answer different questions. After resizing an EBS volume, `fdisk -l` confirms the raw volume and partition have grown, while `df -h` confirms the filesystem is actually using that new space. If `fdisk` shows 20 GB but `df` still shows 8 GB, it means the partition or filesystem hasn't been expanded yet. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

***

### 5. Root User Access (`sudo -i`)

The instructor switches to the root user with `sudo -i` before running disk commands. This is because `fdisk -l` requires root privileges to read raw block device information. `df -h` can be run by any user, but it's simpler to switch to root once and run everything from there. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

The `sudo -i` command means "simulate an initial login as root" — it gives you a root shell with root's environment variables. It's equivalent to `sudo su -` in most setups.

> ⚠️ **Expert Note (Optional)**
>
> In production, avoid staying in a root shell for extended periods. Use `sudo` per-command instead (e.g., `sudo fdisk -l`). Root shells are risky because any typo executes with full system privileges. The instructor uses `sudo -i` here for convenience during a quick diagnostic, which is acceptable in a lab/course context.

***

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building

We are **expanding the root disk of a Jenkins EC2 instance from 8 GB to 20 GB** to prevent "no space left on device" errors. This is a real-world operation that every DevOps engineer performs — cloud servers are provisioned with conservative defaults, and you resize storage as workload demands grow. The final outcome is a Jenkins server with 20 GB of usable disk space, confirmed via Linux commands. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

***

### Step 1: Identify the Problem

Before resizing anything, you should understand **why** you're doing it. In this course, as you install plugins, create jobs, and run builds, the 8 GB default volume fills up. Your Jenkins job fails, and the console output shows: [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

    No space left on device

The instructor notes you can either **do this exercise right away** (proactively, before hitting the error) or **after witnessing the error** (reactively). For this section of the course, 20 GB is needed. Doing it proactively is recommended to avoid interruption. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

***

### Step 2: Navigate to the EC2 Volume in AWS Console

Open the **AWS Management Console** and navigate to your Jenkins EC2 instance. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

1.  Go to **EC2 Dashboard** → find your Jenkins instance
2.  Click on the instance → go to the **Storage** tab
3.  You'll see the **root volume** listed — it shows as **8 GB** by default

This volume is the EBS block device attached to your instance. It's the only disk your Jenkins server has. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**Click on the volume ID** (the link in the Storage tab). This takes you to the EBS Volumes section of the EC2 console, with that specific volume selected.

***

### Step 3: Name the Volume

Once you're on the volume's detail page, **give it a name** so you can identify it later. The instructor names it: [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

    JenkinsRootVolume

To do this, click the **Name** field (or the pencil/edit icon next to it) and type the name. This is a tag (`Name` tag) — it doesn't affect the volume's function, but in a real AWS account with dozens of volumes, naming them is essential for identification.

***

### Step 4: Check Current Disk Space (Before Modification)

Before modifying the volume, SSH into the Jenkins server to see the current state. This gives you a "before" snapshot to compare against after resizing. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**Switch to root user:**

```bash
sudo -i
```

*   `sudo` — execute a command with superuser (root) privileges
*   `-i` — simulate an initial login shell (gives you a full root environment)

You now have a root prompt. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**Clear the screen:**

```bash
clear
```

This simply clears the terminal for readability. No functional impact.

**Check filesystem usage:**

```bash
df -h
```

*   `df` — **d**isk **f**ree: reports filesystem disk space usage
*   `-h` — **h**uman-readable: shows sizes in GB/MB instead of raw bytes

**Expected output:** The root partition shows approximately **6.8 GB** of total size. This is your usable filesystem space on the 8 GB volume. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**Check partition layout:**

```bash
fdisk -l
```

*   `fdisk` — **f**ixed **disk**: a partition manipulation utility
*   `-l` — **l**ist: display partition tables for all disks (read-only, doesn't modify anything)

**Expected output:** [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

*   **Disk `/dev/xvda`**: 8 GB — the raw EBS volume
*   **Partition `/dev/xvda1`**: \~7 GB — the single partition on that volume

This confirms: the volume is 8 GB, the partition is \~7 GB, and the usable filesystem is \~6.8 GB. Everything is consistent.

***

### Step 5: Modify the Volume Size to 20 GB

Back in the **AWS Console**, on the volume detail page: [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

1.  Click **Actions** (dropdown button at the top)
2.  Select **Modify Volume**
3.  Change the **Size** field from `8` to `20` (GB)
4.  Click **Modify**
5.  A confirmation dialog appears — click **Modify** again to confirm

AWS now begins resizing the volume in the background. The volume state will briefly show "modifying" and then "optimizing" before returning to "in-use." [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

> 🔍 **Deep Dive (Optional)**
>
> When you modify an EBS volume, AWS doesn't physically "stretch" the existing blocks. It allocates additional storage capacity on its backend infrastructure and extends the block device presented to your instance. This operation is non-destructive — your existing data is untouched. However, the OS inside the instance doesn't automatically know the volume grew (until reboot triggers cloud-init/growpart, or you manually expand).

***

### Step 6: Reboot the Jenkins Instance

After the volume modification is initiated, **reboot the EC2 instance** so the operating system recognizes the new volume size and automatically expands the partition and filesystem. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

In the AWS Console:

1.  Go back to **EC2 Instances**
2.  Select the **Jenkins Server** instance
3.  Click **Instance State** (dropdown)
4.  Select **Reboot Instance**

**Wait approximately 2–3 minutes** for the instance to fully come back up. During reboot, the OS detects the larger volume, and cloud-init/growpart utilities automatically resize the partition and filesystem to use the full 20 GB. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

> ⚠️ **Expert Note (Optional)**
>
> Reboot ≠ Stop/Start. A **reboot** keeps the instance on the same physical host and preserves its public IP (if it has an Elastic IP) and instance store data. A **stop/start** migrates the instance to potentially different hardware and loses the public IP (unless Elastic IP is assigned) and any instance store data. For a simple volume resize, reboot is sufficient and less disruptive.

***

### Step 7: Verify the New Disk Space (After Reboot)

After 2–3 minutes, SSH back into the Jenkins instance. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

**Switch to root:**

```bash
sudo -i
```

**Clear the screen:**

```bash
clear
```

**Check partition layout:**

```bash
fdisk -l
```

**Expected output:** [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

*   **Disk `/dev/xvda`**: now shows **20 GB** — the volume has been resized
*   **Partition `/dev/xvda1`**: has also increased to match — the partition has auto-expanded

**Check filesystem usage:**

```bash
df -h
```

**Expected output:** The root partition now shows approximately **19 GB** of usable space. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

This confirms the entire pipeline worked:

*   AWS resized the EBS volume → `fdisk -l` confirms 20 GB raw disk
*   The OS expanded the partition on reboot → `fdisk -l` confirms partition growth
*   The filesystem was grown to fill the partition → `df -h` confirms 19 GB usable

Your Jenkins server now has sufficient space to handle all the plugins, jobs, and workspace data for the rest of the course. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

***

### Connection to the Overall System

This is a **foundational infrastructure step**. Everything you do in Jenkins — installing plugins, configuring pipelines, running builds, storing artifacts — depends on having enough disk space. By proactively resizing to 20 GB, you eliminate a class of failures ("no space left on device") that would otherwise interrupt your learning and, in production, interrupt your CI/CD pipelines. This is also your first practical exposure to **AWS EBS volume management**, which is a routine DevOps skill — you'll resize, snapshot, and manage volumes regularly in real infrastructure work. [\[162.-Disk-...pace-Issue \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/162.-Disk-Space-Issue.txt)

***

Want me to save this as a downloadable Markdown file?
