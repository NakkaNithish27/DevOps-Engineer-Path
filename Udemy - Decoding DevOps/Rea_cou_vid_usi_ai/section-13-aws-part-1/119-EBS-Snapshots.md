# 🎓 EBS Snapshots: Backup, Recovery, and Data Mobility in AWS — Deep Learning Material

**Source:** Video caption file — *EBS Snapshots (Continuation of EBS Lecture)* [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What EBS Snapshots Are and What Problem They Solve

An **EBS Snapshot** is a **backup of an EBS volume**. EBS volumes are the hard disks attached to EC2 instances (covered in the previous EBS lecture). Snapshots solve the fundamental problem of data protection: what happens when data on a volume is **lost, corrupted, or accidentally deleted**? Without a backup mechanism, the data is gone permanently. Snapshots provide a point-in-time copy of the volume's data that you can use to **recover** from any kind of data loss. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

But snapshots are far more than just backups. They are a **data mobility and transformation tool** that enables several advanced operations — changing volume types, changing volume sizes, moving data across availability zones, moving data across regions, moving data across AWS accounts, and encrypting previously unencrypted volumes. Understanding snapshots as "just backups" is an understatement; they are the primary mechanism for **volume lifecycle management** in AWS.

***

## 1.2 — How Snapshots Work: Full and Incremental

The first time you take a snapshot of a volume, it creates a **full backup** — all the data on the volume is copied. Every subsequent snapshot after that is **incremental** — it only copies the data that has **changed** since the last snapshot. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

This incremental model is critically important for cost and time efficiency. If you have a 100 GB volume and take a snapshot every day, only the first snapshot is 100 GB. If only 2 GB changes daily, each subsequent snapshot is approximately 2 GB. You can take snapshots on a **regular interval** without the storage cost or time penalty of full backups each time.

> 🔍 **Deep Dive:** Despite being incremental, each snapshot is **independently restorable**. You don't need the full chain of snapshots to restore — any single snapshot contains enough metadata to reconstruct the complete volume state at that point in time. This is because AWS manages the block-level references internally. Deleting an older snapshot doesn't break newer ones — AWS automatically moves any blocks that the newer snapshots still need. This is an *implicit concept* — the video mentions "first full, then incremental" but doesn't explain the independence of snapshots.

***

## 1.3 — The Volume → Snapshot → Volume Lifecycle

The core operational pattern for snapshots follows a three-phase cycle:

1. **Volume exists** with data → You take a **snapshot** (creates backup).
2. The snapshot is stored **independently** from the volume (it persists even if the volume is deleted).
3. From the snapshot, you can **create a new volume** — and during creation, you can modify properties.

This cycle is not just for recovery. It's the mechanism for all volume transformations. Need a bigger volume? Snapshot → create volume with larger size. Need faster I/O? Snapshot → create volume with provisioned IOPS type. Need data in a different zone? Snapshot → create volume in target zone. The snapshot is the **intermediary** through which all volume changes flow. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## 1.4 — Snapshot Capabilities Beyond Backup

The video systematically reveals that snapshots enable **five distinct operations** beyond simple backup/recovery:

### 1. Change Volume Type

When creating a volume from a snapshot, you can change the **volume type** — for example, from `gp3` (General Purpose SSD) to **Provisioned IOPS** (high-performance storage). The instructor specifically mentions the database use case: "When you have huge access, huge I/O, then you can change from general purpose to provisioned IOPS." [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### 2. Change Volume Size

You can **increase** the volume size during creation from a snapshot. Decreasing carries a risk of data loss ("there is a chance that you might lose the data"), but increasing is always safe. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### 3. Change Availability Zone

You can move a volume's data from one AZ to another. The volume itself cannot be moved — but you can take a snapshot, then create a new volume from that snapshot **in a different zone**. This is how you attach storage to an instance in a different AZ. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### 4. Copy Snapshot to Another Region (Cross-Region Data Transfer)

Using the **"Copy snapshot"** action, you can copy a snapshot to an entirely different AWS region. Then go to that region and create a volume from the copied snapshot. This is the mechanism for **cross-region data migration**. The instructor frames this as an interview/requirement question: "If someone asks you how to move EBS data from one region to another region, it's through snapshot." [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

> ⚠️ **Expert Note:** Cross-region snapshot copy is **not free** — it incurs data transfer charges and storage charges in the destination region. The video explicitly notes: "We are not going to do that because it's not a free exercise."

### 5. Share Snapshot Across AWS Accounts

Through **"Modify permissions"** in snapshot settings, you can make a snapshot **public** or share it with a **specific AWS account** by providing their Account ID. This enables **cross-account data transfer** — if you need to move data from one AWS account to another, you share the snapshot, and the receiving account creates a volume from it. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### 6. Encrypt an Unencrypted Volume

You can use a snapshot to **encrypt a previously unencrypted volume**. Take a snapshot of the unencrypted volume, then create a new encrypted volume from that snapshot. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### 7. Create AMI from Snapshot

The **"Create image from snapshot"** action creates an AMI (Amazon Machine Image) directly from a snapshot. This is mentioned but deferred to a later lecture. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## 1.5 — The `lsof` Command: Checking What's Using a Directory

Before you can unmount a volume, no process can be using the mount point directory. The command **`lsof`** (List Open Files) shows which processes are connected to a directory or file. If you've `cd`'d into the mounted directory, that counts as a process using it (shown as `cwd` — current working directory). Trying to unmount while a process is using the directory produces the error **"target is busy."** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

The fix: either close/exit the process naturally (e.g., `cd` out of the directory) or forcibly kill it using `kill -9 <PID>`. Only after all processes release the directory can you unmount.

***

## 1.6 — The Database-on-Separate-Volume Pattern

The video demonstrates a critical real-world architectural pattern: **storing database data on a separate EBS volume** rather than on the root volume. The instructor creates a new volume, partitions it, formats it, mounts it at `/var/lib/mysql` (the directory where MariaDB stores its data), and **then** installs MariaDB. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

The order matters: **create the directory and mount point BEFORE installing the service**. When the service starts, it automatically stores data in its default directory (`/var/lib/mysql`), which is now pointing to the separate volume. The service doesn't know or care that the directory is on a different disk — the mount point is transparent to the application.

Why separate the database volume? **Independent lifecycle management.** You can snapshot the database volume independently, resize it independently, change its performance tier independently, and recover it independently — all without touching the root volume or the OS. The root volume holds the OS and application binaries (which are replaceable); the database volume holds the **irreplaceable data**. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

> 🔍 **Deep Dive:** The sequence "create volume → partition → format → mount at data directory → THEN install service" is the standard operational pattern for any stateful service (databases, message queues, log stores). If you install the service first, it creates the data directory on the root volume and starts writing data there. Moving data afterward is more complex. Doing it in the correct order means the service never writes a single byte to the wrong location.

***

## 1.7 — Cleanup Discipline: Volumes Created By You Must Be Deleted By You

When you terminate an EC2 instance, the **root volume** (created automatically with the instance) is deleted along with the instance. But any **additional volumes you created and attached** are **NOT automatically deleted**. They persist in "available" state and continue to incur storage charges. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

The cleanup sequence is explicit: terminate the instance first → wait for it to fully terminate → then go to volumes → detach (if not auto-detached) → delete the volume. Also delete any snapshots you created. The video's final dashboard check confirms: zero running instances, zero volumes, zero snapshots. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

> ⚠️ **Expert Note:** This is a common source of unexpected AWS bills — forgotten EBS volumes and snapshots. In production, teams use tagging, AWS Config rules, or cleanup scripts to identify and remove orphaned volumes and snapshots. Always verify your dashboard is clean after lab exercises.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We're conducting a full **snapshot lifecycle exercise**: attach a new volume to an EC2 instance, set it up as a dedicated MySQL database volume, populate it with data by running MariaDB, take a snapshot, **deliberately corrupt the data**, then **recover** by creating a new volume from the snapshot and reattaching it. Along the way, we also learn volume detachment, the `lsof` diagnostic, and the full cleanup procedure. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

The final outcome: a recovered, running MariaDB service with all data intact — restored from an EBS snapshot after intentional data destruction.

***

## Phase 1: Clean Up the Previous Volume

### Step 1: SSH into the Instance and Check Current Mounts

```bash
ssh -i <key.pem> ec2-user@<PUBLIC_IP>
sudo -i
df -h
```

`df -h` shows all mounted filesystems. You should see the volume from the previous lecture still mounted. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

### Step 2: Check for Processes Using the Mount Point with `lsof`

```bash
cd /path/to/mounted/directory
lsof /path/to/mounted/directory
```

**Breakdown:**

* `lsof` — **List Open Files** — shows all processes that have files or directories open at the specified path.
* Output showing `cwd` means a process has its current working directory set to this path (e.g., you `cd`'d into it). [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Why This Matters

If any process is using the directory, unmounting will fail with **"target is busy."**

### Step 3: Free the Directory and Unmount

```bash
cd /          # Navigate OUT of the mounted directory
umount /path/to/mounted/directory
```

If `umount` still fails (other processes holding it), use `lsof` to find the PID, then:

```bash
kill -9 <PID>
umount /path/to/mounted/directory
```

**`kill -9`** sends the SIGKILL signal — forces immediate process termination. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

### Step 4: Remove the fstab Entry

```bash
vim /etc/fstab
```

Navigate to the **last line** (the mount entry from the previous lecture). Press `dd` to delete that line. Save and quit (`:wq`). [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Why

If the fstab entry remains but the volume is detached, the system may hang or error on next boot trying to mount a nonexistent volume.

***

### Step 5: Detach and Delete the Old Volume (AWS Console)

1. In EC2 Console → **Volumes** → select the old volume (`moso-web01`).
2. **Actions → Detach volume.**
3. Wait for status to change from "in-use" to **"available."** (Refresh if needed.)
4. Select the volume → **Actions → Delete volume.** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Common Mistakes

* **Trying to detach while still mounted** — Always `umount` inside the instance first.
* **Force detach** — Available as an option if normal detach fails, but should be used as a last resort.

***

## Phase 2: Set Up a Database Volume

### Step 6: Create a New EBS Volume

In EC2 Console → **Volumes → Create Volume:**

| Setting           | Value                                                                        |
| ----------------- | ---------------------------------------------------------------------------- |
| Type              | `gp3`                                                                        |
| Size              | `5 GB`                                                                       |
| Availability Zone | **Same zone as your instance** (check instance details — e.g., `us-east-1c`) |
| Tag (Name)        | `db01-mysql-vol`                                                             |

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

Click **Create Volume.**

### Critical: Zone Must Match

A volume can only be attached to an instance **in the same Availability Zone**. If your instance is in `1c`, the volume must be created in `1c`.

***

### Step 7: Attach the Volume to the Instance

Select the new volume → **Actions → Attach volume** → Select your instance → Device name: **`/dev/sdh`** → **Attach volume.** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

### Step 8: Partition and Format the Volume

SSH into the instance:

```bash
fdisk -l
```

Confirm the new volume appears (e.g., `/dev/xvdh`). [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

**Create partition:**

```bash
fdisk /dev/xvdh
```

Inside fdisk: `n` (new) → `p` (primary) → `1` (partition number) → Enter (first sector default) → Enter (last sector default) → `w` (write and exit). [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

**Verify:**

```bash
fdisk -l
```

The partition (e.g., `/dev/xvdh1`) should now appear.

**Format with XFS:**

```bash
mkfs.xfs /dev/xvdh1
```

The video explicitly chooses **XFS** this time (`mkfs.xfs`) — a different filesystem from what might have been used previously. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

### Step 9: Create the MySQL Data Directory and Mount

```bash
mkdir /var/lib/mysql
mount /dev/xvdh1 /var/lib/mysql
df -h
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

**Why `/var/lib/mysql` specifically?** — This is the **default data directory** for MariaDB/MySQL. By creating this directory and mounting the separate volume to it **before** installing MariaDB, all database data will automatically be written to the separate volume when the service starts.

**Verify:** `df -h` should show the partition mounted at `/var/lib/mysql`.

***

### Step 10: Install and Start MariaDB

```bash
dnf install mariadb105-server -y
```

**Before starting the service, observe the empty directory:**

```bash
ls /var/lib/mysql
```

Shows nothing — the directory is empty. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

**Start the service:**

```bash
systemctl start mariadb
```

**Now check again:**

```bash
ls /var/lib/mysql
```

**Data files appear.** MariaDB has initialized its data store. Because `/var/lib/mysql` is mounted on the separate volume, all this data lives on the separate EBS volume — not the root disk. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## Phase 3: Snapshot, Corrupt, Recover

### Step 11: Take a Snapshot of the Database Volume

In EC2 Console → **Volumes** → Select the db volume → **Actions → Create snapshot.**

* Add a **description** and a **Name tag** (e.g., a meaningful identifier).
* Click **Create snapshot.** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

Navigate to **Snapshots** section. Status shows **"pending"** → wait until it shows **"completed."** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Connection to Larger Flow

You now have a point-in-time backup of the database volume with all MariaDB data. This is your safety net.

***

### Step 12: Deliberately Corrupt the Data

```bash
rm -rf /var/lib/mysql/*
systemctl restart mariadb
```

The `rm -rf` deletes all database files. The `systemctl restart` attempts to start MariaDB, which **fails** because its data files are gone. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

**Verify the failure:**

```bash
systemctl status mariadb
```

Shows **exited** state with errors about missing data. The database is broken. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Connection to Larger Flow

This simulates real-world data corruption or accidental deletion. The recovery path follows.

***

### Step 13: Unmount and Detach the Corrupted Volume

```bash
umount /var/lib/mysql
```

If "target is busy," use `lsof /var/lib/mysql` → find PIDs → `kill -9 <PID>` → retry unmount. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

**Verify:**

```bash
df -h
```

The mount is gone.

**In the console:** Rename the volume to **"corrupted"** (for identification) → **Actions → Detach volume.** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

### Step 14: Create a New Volume from the Snapshot

Navigate to **Snapshots** → Select your snapshot → **Actions → Create volume from snapshot.** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Available Options During Volume Creation from Snapshot

| Option            | What You Can Change                     |
| ----------------- | --------------------------------------- |
| Volume Type       | `gp3` → Provisioned IOPS, etc.          |
| Volume Size       | Increase (decrease risks data loss)     |
| IOPS              | Adjust performance                      |
| Availability Zone | Move to a different zone                |
| Encryption        | Encrypt a previously unencrypted volume |

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

For this recovery: keep everything as-is (`gp3`, same size, same zone as instance). Add a **Name tag** (e.g., `recovered`). Click **Create volume.**

***

### Step 15: Delete the Corrupted Volume

Go to **Volumes** → select the corrupted volume → **Detach** (if not already) → wait for "available" → **Actions → Delete volume.** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

### Step 16: Attach the Recovered Volume and Verify

Select the recovered volume → **Actions → Attach volume** → select your instance → provide device name → **Attach volume.** [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

SSH into the instance:

```bash
fdisk -l
```

Confirm the volume and partition are visible.

```bash
mount /dev/xvdh1 /var/lib/mysql
df -h
```

Confirm mounted. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

```bash
ls /var/lib/mysql
```

**The data files are back.** ✅ The snapshot preserved all the data from before corruption. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

```bash
systemctl restart mariadb
systemctl status mariadb
```

**Active (running).** ✅ The database service is fully recovered. [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## Phase 4: Full Cleanup

### Step 17: Delete Everything

**Order matters:**

1. **Delete snapshot:** Snapshots → select → **Actions → Delete snapshot.**
2. **Terminate instance:** Instances → select → **Instance state → Terminate.** Wait for full termination.
3. **Delete manually-created volumes:** Volumes → select → **Actions → Delete volume** (only after instance is terminated and volume shows "available"). [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Final Verification Dashboard Check

| Resource          | Expected Count                   |
| ----------------- | -------------------------------- |
| Running Instances | 0                                |
| Volumes           | 0                                |
| Snapshots         | 0                                |
| Key Pairs         | 1 (can remain)                   |
| Security Groups   | 2 (default + web-sg, can remain) |

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

### Critical Cleanup Rule

**Root volume** = auto-deleted with instance. **Your manually created volumes** = persist after instance termination → YOU must delete them. **Snapshots** = persist indefinitely → YOU must delete them. Both incur ongoing charges if left behind.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 📸 EBS Snapshot Core Identity

```
SNAPSHOT = Point-in-time backup of an EBS Volume
  ├── First snapshot  = FULL copy
  ├── Later snapshots = INCREMENTAL (only changed data)
  ├── Each snapshot independently restorable
  └── Persists independently from the volume (volume can be deleted)
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## 🔄 The Snapshot Lifecycle Cycle

```
VOLUME (live data)
   │
   ├── Actions → Create Snapshot
   │         │
   │         ▼
   │    SNAPSHOT (stored independently)
   │         │
   │         ├── Actions → Create Volume from Snapshot ──▶ NEW VOLUME
   │         │                  (can change: type, size, zone, encryption)
   │         │
   │         ├── Actions → Copy Snapshot ──▶ SNAPSHOT IN ANOTHER REGION
   │         │
   │         ├── Actions → Modify Permissions ──▶ Share to other AWS ACCOUNT
   │         │
   │         └── Actions → Create Image (AMI) ──▶ Bootable AMI
   │
   └── Original volume can be deleted — snapshot persists
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## 🛠️ Seven Things You Can Do With Snapshots

```
1. BACKUP & RECOVERY     → Restore corrupted/lost data
2. CHANGE VOLUME TYPE     → gp3 → Provisioned IOPS (at creation from snapshot)
3. CHANGE VOLUME SIZE     → Increase size (decrease risks data loss)
4. CHANGE ZONE            → Move data to different AZ (create volume in target zone)
5. CHANGE REGION          → Copy snapshot to target region → create volume there
6. CHANGE ACCOUNT         → Share snapshot with another AWS Account ID
7. ENCRYPT                → Create encrypted volume from unencrypted snapshot
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## 🗄️ Database-on-Separate-Volume Pattern

```
CORRECT ORDER:
  1. Create EBS Volume
  2. Attach to instance
  3. Partition (fdisk) → Format (mkfs.xfs)
  4. mkdir /var/lib/mysql          ← Create data dir BEFORE installing service
  5. mount partition → /var/lib/mysql
  6. dnf install mariadb105-server  ← Install AFTER mount
  7. systemctl start mariadb        ← Service writes to separate volume automatically

WHY THIS ORDER:
  Service → finds /var/lib/mysql → already mounted on separate volume
  → All DB data goes to separate disk from first byte
  → Independent snapshot, resize, recovery, performance tuning
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## 🔓 `lsof` — Freeing a Busy Mount Point

```
PROBLEM: umount fails → "target is busy"

DIAGNOSIS:
  lsof /path/to/mount
    └── Shows PIDs holding the directory
    └── cwd = someone cd'd into it

FIX:
  Option A: cd / (leave the directory)  → then umount
  Option B: kill -9 <PID>              → then umount
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## ⚡ Complete Lab Execution Sequence

```
PHASE 1: CLEANUP OLD VOLUME
  1. lsof + cd out + umount                    ← Free mount point
  2. Remove fstab entry (vim /etc/fstab → dd)  ← Prevent boot issues
  3. Console: Detach → Delete old volume

PHASE 2: SET UP DB VOLUME
  4. Create volume (gp3, 5GB, SAME ZONE as instance)
  5. Attach volume (sdh)
  6. fdisk → partition → mkfs.xfs → format
  7. mkdir /var/lib/mysql → mount
  8. dnf install mariadb105-server -y
  9. systemctl start mariadb → data appears in /var/lib/mysql ✅

PHASE 3: SNAPSHOT → CORRUPT → RECOVER
  10. Console: Create snapshot of DB volume → wait for "completed"
  11. rm -rf /var/lib/mysql/* → restart mariadb → FAILS ❌ (data gone)
  12. umount → detach corrupted volume → rename "corrupted"
  13. Console: Snapshot → Create volume from snapshot → tag "recovered"
  14. Delete corrupted volume
  15. Attach recovered volume → mount → ls → DATA IS BACK ✅
  16. systemctl restart mariadb → active (running) ✅

PHASE 4: CLEANUP
  17. Delete snapshot
  18. Terminate instance (root vol auto-deleted)
  19. Delete manually-created volumes (NOT auto-deleted)
  20. Dashboard check: 0 instances, 0 volumes, 0 snapshots
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## ⚠️ Cleanup Rules

```
RESOURCE              AUTO-DELETED WITH INSTANCE?    ACTION REQUIRED
──────────────────    ──────────────────────────     ───────────────
Root Volume           YES                            None
Your Custom Volumes   NO ❌                          Manual delete
Snapshots             NO ❌                          Manual delete
Key Pairs             N/A (persist, no charge)       Optional
Security Groups       N/A (persist, no charge)       Optional

FORGOTTEN VOLUMES + SNAPSHOTS = UNEXPECTED AWS BILLS
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: DATA SEPARATION — STATELESS COMPUTE + STATEFUL STORAGE
  OS/app on root volume (replaceable) | Data on separate volume (irreplaceable)
  → Same as: Docker volumes, Kubernetes PVCs, database-on-SAN,
    stateless containers + external storage

PATTERN 2: SNAPSHOT AS TRANSFORMATION INTERMEDIARY
  Can't modify a live volume's type/zone/encryption directly
  → Take snapshot → Create new volume with desired properties
  → Same as: Database dump → restore into new schema/engine,
    VM snapshot → clone to different hypervisor

PATTERN 3: INCREMENTAL BACKUP STRATEGY
  First = full, subsequent = incremental (only changes)
  → Same as: Git commits, rsync, database WAL/binlog backups,
    Time Machine, any delta-based backup system

PATTERN 4: ORDER-DEPENDENT SETUP (Mount BEFORE Install)
  Create mount point → Mount volume → THEN install service
  → Service auto-discovers the directory and writes there
  → Same as: Prepare storage before deploying stateful app in K8s,
    NFS mount before starting log collector

PATTERN 5: DIAGNOSE-BEFORE-DETACH (lsof pattern)
  Check what's using a resource → free it → then detach
  → Same as: Check connections before stopping DB,
    drain node before removing from cluster,
    check open file handles before unmounting in any OS
```

 [\[119. EBS Snapshots \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/119.%20EBS%20Snapshots.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → EBS Volumes (create, attach, partition, format, mount, fstab)
THIS      → EBS Snapshots (backup, recovery, data mobility, transformation)
NEXT      → Load Balancers (new section)
LATER     → AMI creation (from snapshots, mentioned but deferred)
```

***

Your EBS Snapshots deep learning material is fully reconstructed — covering the complete backup/recovery lifecycle, all seven snapshot capabilities, the database-on-separate-volume pattern, and the full cleanup discipline. Want me to generate **AnkiDroid flashcards (.csv)** from this lecture or across all lectures we've covered? 🃏
