# 🎓 Deep Learning Material: Amazon S3 Introduction — Object Storage, Storage Classes, Access Control, and Lifecycle Management

**Source:** Video lecture on Amazon S3 (Simple Storage Service) introduction (from [128. S3 Introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt?EntityRepresentationId=27b430be-0e05-4b30-b1ee-af6891ea8d32) caption file) [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Video Context:** This is a comprehensive introductory lecture on Amazon S3 — one of the most heavily used and oldest AWS services. The instructor covers the conceptual foundation (what S3 is, how it stores data, how replication works), the full range of storage classes with cost/performance tradeoffs, lifecycle policies, the multi-layer access control model (bucket-level public access block → ACL enablement → per-object public access), bucket creation with all its options, object upload with per-object settings, and a hands-on demonstration of the complete flow from "private by default" to "publicly accessible." The lecture's core engineering value is in understanding the **layered security model** where multiple gates must be opened in sequence before an object becomes public.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What S3 Is: Object Storage Accessible Over the Internet

Amazon S3 (Simple Storage Service) is a **storage service** where you can store any amount of data and access it over the internet from anywhere. The instructor frames it initially with a familiar analogy: *"think of it as like Google Drive or Dropbox, but it's much more than that with many, many features."* [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

S3 is described as one of the **most popular and oldest** AWS services. Its popularity comes from the enormous breadth of use cases it supports — from simple file hosting to application data storage to website hosting to archival to disaster recovery.

The fundamental data model has two elements: **buckets** and **objects**. A **bucket** is the top-level storage container — think of it as a root folder. An **object** is any piece of data you store inside a bucket: a file, a document, a picture, a video. You can also create folders within buckets to organize objects. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

There is **no limit** on the amount of data you can store — S3 provides unlimited storage. When you upload data into a bucket, that data is **automatically replicated in multiple facilities** (availability zones) — you don't need to configure or manage this replication. It happens by default for most storage classes. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Bucket names must be globally unique** across all of AWS — not just unique within your account, but unique across every AWS account in the world. This is because each bucket gets a **public endpoint URL** that contains the bucket name, and that URL must be unique on the internet. The instructor demonstrates this: even a common name like "test" fails because someone else already has a bucket with that name. The convention to achieve uniqueness is to append numbers or organization-specific identifiers to the name. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.2 — S3 vs. EFS: Object Storage vs. File System Storage

The instructor draws an important architectural distinction between S3 and EFS (Elastic File System), since both involve storing data that EC2 instances can access. With **EFS**, you **mount** a file system at the operating system level — you get a folder on the OS, and your applications write to that folder as if it were a local disk. With **S3**, you **programmatically access** the storage through your application — developers code their applications to read from and write to S3 using the S3 API. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

There is a way to mount S3 to a folder (via **S3 FS** — a separate driver), but the primary and most common access pattern is programmatic via the API. The key difference: EFS is filesystem-level integration, S3 is application-level integration. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

A very common use case: EC2 instances running web services or application services need to store file-based data. Instead of storing files locally on the instance's disk (which is ephemeral and not shared), developers program the application to store data in S3. This gives the data durability, accessibility from anywhere, and independence from any specific instance. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.3 — Storage Classes: The Cost-Performance Spectrum

S3 offers multiple **storage classes** (storage types) that represent different points on a spectrum between **fast access + high cost** and **slow access + low cost**. You choose the storage class based on how frequently you need to access the data. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

### S3 Standard

The default and most common storage class. Data access is **fast**. Objects are replicated across **multiple availability zones** (minimum 3). You pay the highest per-GB storage rate, but there are no retrieval fees. Use this for data you access frequently and continuously. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

### S3 Infrequent Access (IA)

For data you don't access continuously — maybe once a day, once a week, a few times a week. Data access is **slower** compared to Standard. Objects are still replicated across **multiple availability zones** (same durability guarantee). But storage costs are lower, and you pay a **per-GB retrieval fee** when you access the data. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

### S3 One Zone Infrequent Access

For data where you **don't care about durability** — maybe you already have it stored elsewhere, or it's non-critical. Data is stored in **only one availability zone** — no replication across zones. Access is slower. Cost is even lower. The tradeoff is clear: if that single AZ has a failure, your data could be lost. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

### S3 Intelligent Tiering

An automated class where **data automatically moves to the most cost-effective tier** based on access patterns. You don't need to manually manage which tier your data sits in — S3 monitors access frequency and shifts objects accordingly. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

### S3 Glacier

**Very low cost** storage designed for **data archiving** — data you rarely access. Typical use cases: audit data accessed once a year, compliance data that must be retained for a specific period (1 year, 2 years), then deleted. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

### S3 Glacier Deep Archive

The **lowest cost** storage class in S3. Retrieval time can be **up to 12 hours**. Designed for data stored for **decades** — old medical records, government records, long-term legal archives. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Important cross-cutting facts from the AWS documentation table the instructor shows:** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

* **Durability** is **99.999999999%** (eleven 9's) across **all** storage classes — even Glacier Deep Archive. Your data is extremely unlikely to be lost regardless of which class you choose.
* **Availability** varies: S3 Standard is 99.99%, most others are 99.9%, One Zone IA is 99.5%.
* **Replication**: Standard, Intelligent Tiering, and IA all replicate across minimum **3 availability zones**. One Zone IA replicates within **1 zone only**.
* **Retrieval fees**: Standard and Intelligent Tiering have no retrieval fees. IA, One Zone IA, Glacier, and Glacier Deep Archive charge per GB retrieved.

> 🔍 **Deep Dive**
>
> The durability vs. availability distinction is important and often confused. **Durability** (99.999999999%) means the probability that your data will not be lost or corrupted — extremely high across all classes. **Availability** (99.5% – 99.99%) means the probability that you can access your data at any given moment. Even S3 Standard, at 99.99% availability, means approximately 53 minutes of potential inaccessibility per year. One Zone IA at 99.5% means roughly 44 hours per year. The data is still there (durable); it's just temporarily inaccessible (less available). [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.4 — Lifecycle Policies: Automated Data Tiering Based on Age

You don't have to manually move objects between storage classes as they age. S3 provides **lifecycle policies** that automatically transition objects from one storage class to another based on the object's **age** (time since upload). [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

The instructor gives a concrete example: you upload data, and set a policy that after **30 days**, move it to S3 Infrequent Access. After another 30 days (total **60 days**), move it to One Zone Infrequent Access. After **90 days**, move it to Glacier. You can also set an **expiry** — after one year, delete the data automatically. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

This creates a **fully automated data lifecycle**: hot data starts in Standard (fast, expensive), automatically moves to cooler tiers as it ages (slower, cheaper), and eventually gets archived or deleted. The primary use case the instructor mentions is **log archival** — logs are accessed frequently when fresh, rarely after a few weeks, and can be archived or deleted after a retention period. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

The entire purpose of lifecycle policies is **cost optimization** — ensuring you're not paying Standard-tier prices for data that hasn't been accessed in months.

***

## 1.5 — S3 Charges: The Four Cost Dimensions

S3 charges are based on four factors: [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

1. **Storage** — the amount of data stored (per GB/month)
2. **Requests** — the number of I/O operations (PUT, GET, LIST, etc.) and which storage tier is being accessed
3. **Data Transfer** — moving data out of S3 (egress)
4. **Cross-Region Replication** — if you replicate your bucket to another AWS region (for disaster recovery or data synchronization), there are additional charges [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.6 — The Multi-Layer Access Control Model (Most Important Architectural Concept)

S3 has a **layered security model** where multiple independent security gates must all be open before an object becomes publicly accessible. This is the most important concept in the lecture from an engineering perspective, and the instructor demonstrates it through a deliberate step-by-step unlocking process. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Layer 1: Block Public Access (Bucket Level)** — By default, **all public access is blocked** at the bucket level. This is a master switch. Even if you configure everything else correctly, if this is enabled (which it is by default), nothing in the bucket can be made public. The instructor explains: *"Whenever you upload any object in the S3 bucket, it's by default private. It cannot be accessed publicly. Even if you want to make it public, you cannot do it because by default, all the public access is blocked."* AWS does this as *"an extra level of safety or security"* to prevent accidental data exposure. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Layer 2: ACL (Access Control List) Enablement** — ACLs are **disabled by default**. Even after you unblock public access, you still can't make objects public through ACLs until you explicitly enable ACLs in the bucket's Object Ownership settings. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Layer 3: Per-Object Public Access** — Even after Layers 1 and 2 are open, each **individual object remains private** until you explicitly make it public. The instructor demonstrates: uploading a second object after the bucket is already public — the new object is still private by default. *"Even though bucket is public, ACLs are enabled, but the object is still private."* You must explicitly make each object public (via ACL or policy). [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

This three-layer model means **accidental public exposure requires three separate mistakes** — you'd have to disable block public access, enable ACLs, and then set per-object public access. This defense-in-depth design is intentional. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

The instructor also mentions that bucket permissions can be managed through **policies** (not just ACLs) — this is the more common method in production. Policies offer finer-grained control. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

> ⚠️ **Expert Note**
>
> The instructor notes that making objects public is legitimate in many use cases: *"hosting publicly available images, documents, or even websites."* But AWS's default-private, multi-layer-locked design reflects a fundamental principle: **data should be private unless there's an explicit, intentional reason to make it public.** In production, accidental public S3 buckets have been the source of some of the largest data breaches in cloud computing history. The multi-gate design exists specifically to prevent this. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.7 — Object URL and Access Methods

Every object in S3 has a **publicly addressable URL** (the Object URL). This URL exists regardless of whether the object is public or private. If the object is private, accessing the URL returns **"Access Denied."** If the object is made public, the same URL returns the object content. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

The instructor also demonstrates the **Open** button in the S3 console. This opens the object using the **current AWS user's privileges** (the logged-in user who owns or has access to the bucket). This is **not** public access — it's authenticated access. The fact that the owner can open the object does not mean anyone else can. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.8 — Bucket Versioning

Versioning is an optional feature that, when enabled, keeps **multiple versions** of every object. The instructor addresses a common question: *"What happens if you delete the data in the S3 bucket? Can we recover it?"* If versioning is enabled, yes — you can see older versions and revert to them. This provides a safety net against accidental deletion or overwriting. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.9 — Encryption

S3 now **enforces encryption by default** — you cannot store unencrypted data (this was optional previously). There are three encryption options: [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**SSE-S3 (Server-Side Encryption with S3 Managed Keys)** — AWS S3 manages the encryption keys. Cheapest option. Simplest to use. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**SSE-KMS (Server-Side Encryption with KMS Keys)** — You create and manage your own encryption keys using AWS KMS (Key Management Service). This is **not free**, and KMS keys **cannot be immediately deleted** (there's a minimum 7-day waiting period after disabling). This is used for **compliance** scenarios where the organization needs ownership of encryption keys rather than delegating to AWS. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**DSSE-KMS (Dual-Layer Server-Side Encryption with KMS)** — Two layers of encryption. Higher security, higher cost. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.10 — Bucket Types: General Purpose vs. Directory

When creating a bucket, there's a newer option: **Directory** buckets. These provide **lower latency** processing but are limited to a **single availability zone**. The default and most common type is **General Purpose**, which supports multi-AZ replication and covers the vast majority of use cases. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## 1.11 — S3 is a Global Service with Regional Buckets

S3 is described as a **global service** — it's accessible from everywhere. But when you create a bucket, it's created **in a specific region**. The instructor advises choosing the region based on where users are located, for latency and compliance reasons. The global accessibility means you can reach any bucket from any location over the internet, but the data physically resides in the selected region. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating an S3 bucket, uploading objects (files) into it, understanding the default private access behavior, and then systematically unlocking the three security layers to make objects publicly accessible. The final outcome: understanding the complete operational flow from bucket creation to public object access, including every security gate that must be opened and in what order.

***

## Step 1: Create an S3 Bucket

**What we're doing:** Creating the top-level storage container.

1. Open AWS Console → search for **S3** → open the service [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. Click **Create bucket**

**Configuration options:**

| Setting             | Value                                | Why                                                          |
| ------------------- | ------------------------------------ | ------------------------------------------------------------ |
| Bucket type         | **General purpose**                  | Default; multi-AZ, covers most use cases                     |
| Region              | Your current region                  | Data resides here; choose based on user location             |
| Bucket name         | Unique name (e.g., `devops-doc-623`) | Must be globally unique; append numbers to ensure uniqueness |
| Object Ownership    | **ACLs disabled** (default)          | Leave default for now; we'll enable later when needed        |
| Block Public Access | **Enabled** (all blocked — default)  | Leave default; we'll modify later when needed                |
| Bucket Versioning   | **Enabled**                          | Allows recovery of deleted/overwritten objects               |
| Encryption          | **SSE-S3** (S3 managed keys)         | Cheapest, simplest; sufficient for non-compliance use cases  |

 [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

3. Click **Create Bucket**

**Common mistake — bucket name not unique:** If you get *"Bucket with the same name already exists"*, the name is taken by another AWS account globally. Add numbers or organization-specific identifiers. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Connection to system flow:** The bucket is now created and empty. It's the container we'll upload objects into.

***

## Step 2: Upload an Object

**What we're doing:** Storing a file (PDF, image, etc.) in the bucket.

1. Click on the bucket to open it → click **Upload** → **Add files** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. Select a file from your local machine (PDF, image, etc.)

**During upload, optional settings are available:**

* **Properties → Storage Class:** You can select the storage class for this specific object (Standard, IA, One Zone IA, Glacier, etc.). Default is Standard. The instructor demonstrates selecting One Zone IA for the second upload. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
* **Properties → Encryption:** You can specify a different encryption key for this specific object (overriding the bucket-level encryption). The instructor keeps the default. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
* **Permissions → Predefined ACL:** If ACLs are enabled, you can set public-read access during upload. The instructor does not do this, preferring to demonstrate the default-private behavior first. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

3. Click **Upload** → **Close** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Post-upload action:** The instructor recommends pausing to explore all tabs and settings of both the bucket and the uploaded object.

**Connection to system flow:** The object is now stored in S3, replicated across multiple AZs (for Standard class), encrypted, and **private by default**.

***

## Step 3: Verify the Object Is Private by Default

**What we're doing:** Confirming that the uploaded object cannot be accessed publicly.

1. Click on the uploaded object [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. Note the **Open** button — clicking this opens the object using your AWS user credentials (authenticated access, not public)
3. Copy the **Object URL** — this is the public endpoint
4. Paste the Object URL in a browser

**Expected result:** **"Access Denied"** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Why:** The object is private by default. Three security layers are preventing public access: block public access is on, ACLs are disabled, and the object has no public permission.

***

## Step 4: Attempt to Make the Object Public (First Failure — ACLs Disabled)

**What we're doing:** Trying to make the object public, encountering the first security gate.

1. Select the object → **Actions** → scroll down → **Make public using ACL** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. **Observation:** The option is **grayed out** — you cannot click it [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Why:** ACLs are disabled on the bucket (the default). You cannot use ACL-based public access until ACLs are enabled.

**Fix — Enable ACLs:**

1. Go to bucket → **Permissions** tab → **Object Ownership** → **Edit** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. Select **ACLs enabled**
3. Check **"I acknowledge"** → **Save Changes** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Connection to system flow:** Layer 2 (ACL enablement) is now open. But Layer 1 (block public access) is still blocking.

***

## Step 5: Attempt to Make the Object Public (Second Failure — Block Public Access)

**What we're doing:** Trying again now that ACLs are enabled.

1. Go back to the object → select it → **Actions** → **Make public using ACL** → click **Make public** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. **Expected result:** **Error** — public access is still blocked at the bucket level [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Why:** The bucket-level "Block Public Access" setting is still enabled, overriding any ACL changes.

**Fix — Disable Block Public Access:**

1. Go to bucket → **Permissions** tab → **Block public access** → **Edit** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. **Uncheck** the block public access checkbox
3. **Save Changes** → type **"confirm"** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Connection to system flow:** Layer 1 (block public access) is now open. Both gates are open. Now per-object access can be set.

> ⚠️ **Expert Note**
>
> Only disable Block Public Access when there is a genuine business requirement for public objects (hosting images, static websites, public documents). In all other cases, keep it enabled. The instructor warns: *"Only do it if it's really required. Otherwise just keep it blocked."* [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## Step 6: Successfully Make the Object Public

**What we're doing:** Now that both security gates are open, making the specific object publicly accessible.

1. Go back to the object → select it → **Actions** → **Make public using ACL** → **Make public** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. **Expected result:** Success — no error this time [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Verify:** Go back to the Object URL in the browser → refresh

**Expected result:** The object content (PDF) loads in the browser. **Publicly accessible.** [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

## Step 7: Upload a Second Object and Verify It's Still Private

**What we're doing:** Demonstrating that even after the bucket is "public," new objects are still private by default.

1. Upload a second file (same process as Step 2) [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)
2. Copy the new object's Object URL → paste in browser

**Expected result:** **"Access Denied"** — even though the bucket's public access block is disabled and ACLs are enabled, this specific object has not been made public yet. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**To make it public:** Same process — select object → Actions → Make public using ACL → Make public. Then the Object URL works. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Key operational insight:** Public access is a **per-object** decision, not a bucket-wide toggle. Opening the bucket-level gates just *allows* objects to be made public — it doesn't automatically *make* them public. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Alternative method the instructor briefly shows:** You can also make an object public by going to the object → **Permissions** tab → **Edit** → check **"Everyone: Read"**. This is the ACL-level edit directly on the object. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

**Connection to system flow:** You now understand the complete access control lifecycle. The next lecture will cover hosting a static website on S3, which is one of the primary use cases for public objects. [\[128. S3 Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/128.%20S3%20Introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept (One-Line Reconstruction)

> **S3 = unlimited object storage accessible over the internet, private by default with a three-layer security gate system, and a spectrum of storage classes optimized for cost vs. access frequency.**

***

## 🔷 S3 Data Model

```
S3 SERVICE
  └── BUCKET (top-level container, globally unique name)
        ├── Folder (optional, organizational)
        │     └── OBJECT (any file: doc, image, video)
        └── OBJECT (any file stored directly in bucket)

Object = the data
Bucket = the container
Bucket name = globally unique (used in public endpoint URL)
```

***

## 🔷 Storage Class Spectrum (Cost ↔ Access Speed)

```
FAST ACCESS / HIGH COST                    SLOW ACCESS / LOW COST
◄──────────────────────────────────────────────────────────────►

S3 Standard    Intelligent   Infrequent    One Zone IA    Glacier    Glacier
               Tiering       Access                                  Deep Archive
─────────────  ───────────   ──────────    ───────────    ────────   ────────────
Fast access    Auto-tiers    Slower        Slower         Archive    Decades
Multi-AZ       Multi-AZ      Multi-AZ      1 AZ ONLY     Multi-AZ   Multi-AZ
No retrieval$  No retrieval$ Retrieval $   Retrieval $    Retrieval$ Up to 12hr
                                           No redundancy             retrieval

ALL classes: 99.999999999% durability (eleven 9's)
```

***

## 🔷 Lifecycle Policy Flow

```
OBJECT UPLOADED (Day 0)
  │  Storage: S3 Standard
  │
  ├── Day 30 → auto-move to S3 Infrequent Access
  │
  ├── Day 60 → auto-move to One Zone IA
  │
  ├── Day 90 → auto-move to Glacier
  │
  └── Day 365 → auto-DELETE

All automated via lifecycle policy. Primary use: logs archival, cost optimization.
```

***

## 🔷 The Three-Layer Security Gate (Most Critical Pattern)

```
LAYER 1: Block Public Access (bucket-level master switch)
  │  DEFAULT: ON (all public access blocked)
  │  Must: Edit → uncheck → confirm
  │
  ▼
LAYER 2: ACL Enablement (bucket-level)
  │  DEFAULT: DISABLED
  │  Must: Object Ownership → Edit → Enable ACLs → acknowledge
  │
  ▼
LAYER 3: Per-Object Public Access
  │  DEFAULT: PRIVATE (every new object, even in "public" bucket)
  │  Must: Select object → Actions → Make public using ACL
  │
  ▼
RESULT: Object URL returns content (not "Access Denied")

ALL THREE layers must be opened. Missing ANY layer = Access Denied.
New objects ALWAYS start private at Layer 3 regardless of Layers 1 & 2.
```

***

## 🔷 Failure → Fix Sequence (From the Lecture)

```
ATTEMPT 1: Make public using ACL → GRAYED OUT
  Cause: ACLs disabled (Layer 2)
  Fix: Permissions → Object Ownership → Enable ACLs

ATTEMPT 2: Make public using ACL → ERROR
  Cause: Block Public Access still ON (Layer 1)
  Fix: Permissions → Block Public Access → Edit → Uncheck → Confirm

ATTEMPT 3: Make public using ACL → SUCCESS ✅
  All three layers now open
  Object URL → content loads
```

***

## 🔷 S3 vs. EFS

```
EFS                                 S3
──────────────────────              ──────────────────────
Mounted at OS level                 Accessed programmatically (API)
Appears as a folder                 Accessed via URL/SDK/CLI
File system storage                 Object storage
Shared across instances (NFS)       Accessible from anywhere (internet)
S3 FS driver can mount S3           But primary access = application-level
```

***

## 🔷 Encryption Options

```
SSE-S3          → AWS manages keys → cheapest, simplest, DEFAULT
SSE-KMS         → You manage keys (via KMS) → not free, 7-day delete wait
                  Used for: compliance (key ownership requirement)
DSSE-KMS        → Dual-layer encryption → highest security, highest cost

Encryption is NOW MANDATORY (cannot store unencrypted)
Per-object encryption key can override bucket-level key
```

***

## 🔷 Versioning

```
Enabled? → Multiple versions of every object retained
         → Accidental delete/overwrite → recoverable (view older version, revert)

Disabled? → Delete = permanent, overwrite = permanent
```

***

## 🔷 S3 Charges (Four Dimensions)

```
1. STORAGE     → amount of data (per GB/month)
2. REQUESTS    → I/O operations + storage tier accessed
3. DATA TRANSFER → egress (data out of S3)
4. CROSS-REGION REPLICATION → if enabled (for DR or sync)
```

***

## 🔷 Bucket Configuration Map

```
BUCKET CREATION OPTIONS:
  ├── Type: General Purpose (default) | Directory (low latency, 1 AZ)
  ├── Region: where data physically resides (S3 globally accessible)
  ├── Name: globally unique
  ├── Object Ownership: ACLs disabled (default) | enabled
  ├── Block Public Access: ON (default) — master security switch
  ├── Versioning: disabled (default) | enabled
  └── Encryption: SSE-S3 (default) | SSE-KMS | DSSE-KMS
```

***

## 🔷 Object-Level Settings (Per Upload)

```
Each object can independently specify:
  ├── Storage class (can differ from bucket default)
  ├── Encryption key (can override bucket encryption)
  ├── ACL permissions (if ACLs enabled)
  └── Metadata/tags
```

***

## 🔷 Access Methods

```
Object URL (public endpoint):
  → Private object: "Access Denied"
  → Public object: content returned

"Open" button (console):
  → Uses logged-in AWS user credentials (authenticated)
  → NOT public access (owner can always open)

IAM policies, bucket policies, ACLs:
  → Fine-grained access control for users, roles, accounts
```

***

## 🔷 Reusable Engineering Pattern: Defense-in-Depth with Independent Security Layers

```
PATTERN: Multiple Independent Security Gates (All Must Be Open)

In this lecture (S3):
  Gate 1: Block Public Access (bucket-level master switch)
  Gate 2: ACL Enablement (bucket-level mechanism switch)
  Gate 3: Per-Object Permission (object-level access grant)

Accidental exposure requires THREE separate mistakes.

This pattern appears in:
  - Network security: Internet → ALB SG → Instance SG → OS firewall
  - IAM: Account policy → Group policy → User policy → Resource policy
  - Kubernetes: NetworkPolicy → RBAC → PodSecurityPolicy
  - Database: Network access → DB user auth → Table-level grants

Core principle: security defaults should be restrictive.
               Opening access should require explicit, layered, intentional action.
               Each layer is independently verifiable.
```

***

## 🔷 Common Operational Trap

```
"My S3 object won't become public!"

CHECKLIST:
  □ Block Public Access disabled? (Permissions → Block Public Access)
  □ ACLs enabled? (Permissions → Object Ownership)
  □ Object specifically made public? (Select → Actions → Make public)
  
All three must be YES. Missing any one = Access Denied.
New uploads are ALWAYS private at Layer 3 regardless of Layers 1 & 2.
```

***

## 🔷 Forward Path

```
This lecture: S3 fundamentals, storage classes, access control, basic upload
    │
    ▼
Next lecture: Static website hosting on S3
    └── + more advanced S3 features
```

This lecture gives you the foundational mental model for S3 — the storage classes tell you *how* to optimize cost, the lifecycle policies tell you *how* to automate that optimization, and the three-layer security gate tells you *how* to safely control who sees your data. Everything that follows (website hosting, cross-region replication, programmatic access) builds on these foundations. 🪣
