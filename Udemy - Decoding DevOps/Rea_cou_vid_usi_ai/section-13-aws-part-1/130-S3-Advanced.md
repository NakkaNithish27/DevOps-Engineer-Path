# ☁️ AWS S3 — Lifecycle Rules, Disaster Recovery Replication, and Cost Optimization

**Source:** S3 Advanced Features Session (Caption File) [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

This video covers two **critical S3 bucket features** that every DevOps engineer or architect must know: **Lifecycle Rules** (automatic transition of objects between storage classes based on age to save costs) and **Cross-Region Replication** (copying data to a bucket in another AWS region for disaster recovery compliance). The instructor also covers versioning implications on both features, cleanup procedures, and briefly mentions# 🪣 AWS S3 — Advanced Features: Lifecycle Rules, Cross-Region Replication, and Cost Optimization

**Source:** S3 Advanced Features Session (Caption File) [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

This video covers **two critical S3 bucket features** that every DevOps engineer must know: **Lifecycle Rules** (automatically transitioning objects between storage classes based on age to save costs) and **Cross-Region Replication** (copying objects to a bucket in another AWS region for disaster recovery). The instructor walks through creating both rules in the AWS console, explains the reasoning behind each configuration choice, and covers the interactions with versioning, expiration, delete markers, and cleanup. The session is described as "short and very essential" for a DevOps engineer or architect. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. The Core Problem — Cost and Disaster Recovery

S3 stores objects, and by default, those objects sit in the **Standard** storage class — designed for **frequently accessed** data. But data access patterns change over time. A file uploaded today might be accessed daily for the first month, occasionally for the next few months, and then almost never after that. If it stays in Standard storage forever, you're paying the Standard price for data that nobody is reading. Over time, across thousands or millions of objects, this becomes a significant waste of money. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

The second concern is **disaster recovery**. S3 already replicates data across multiple availability zones within one region, so it's highly durable. But a disaster is a disaster — if an entire region is affected, your data could be lost. Compliance requirements in many organizations mandate that data must exist in **another region** — a different part of the world, potentially a different country or continent. This is the disaster recovery (DR) requirement. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

These two features — **Lifecycle Rules** for cost optimization and **Cross-Region Replication** for disaster recovery — address these two concerns directly.

***

## 2. S3 Storage Classes — The Cost Ladder

Before understanding lifecycle rules, you need to understand the storage classes that objects transition between. The instructor references them in order of decreasing cost (and decreasing access speed): [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Standard** — The default class. Designed for frequently accessed data. Highest cost, fastest access.

**Standard Infrequent Access (Standard-IA)** — For data accessed less frequently but requiring rapid access when needed. Lower cost than Standard.

**One Zone Infrequent Access (One Zone-IA)** — Even cheaper than Standard-IA. The trade-off: data is stored in **only one availability zone** instead of multiple zones. If that zone is lost, the data is gone. Suitable for data that can be recreated or is already a copy.

**Glacier Flexible Retrieval** — The instructor notes this was **"formerly called as Glacier."** Very cheap archival storage. Data retrieval takes minutes to hours (not instant). Designed for long-term archives.

**Glacier Deep Archive** — The **cheapest** S3 storage class. Retrieval takes hours (up to 12 hours). Designed for data that is almost never accessed but must be retained — regulatory archives, compliance data.

The key principle: **the less frequently you access data, the cheaper it should be stored.** Lifecycle rules automate the movement of objects down this cost ladder based on object age. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

***

## 3. Lifecycle Rules — Automated Cost-Driven Transitions

A lifecycle rule defines the **automatic transition of objects from one storage class to another based on the object's age** (number of days since creation). You don't manually move objects — S3 does it automatically according to the rule you define. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

The instructor creates a rule that demonstrates the full transition chain:

| Days After Creation | Storage Class              | Why                                           |
| ------------------- | -------------------------- | --------------------------------------------- |
| 0–29                | Standard                   | Frequently accessed (new data)                |
| 30                  | Standard Infrequent Access | Access decreasing                             |
| 60                  | One Zone Infrequent Access | Rarely accessed, cheaper                      |
| 90                  | Glacier Flexible Retrieval | Archive territory                             |
| 180                 | Glacier Deep Archive       | Deep archive (must be ≥90 days after Glacier) |
| 450                 | Expired (delete marker)    | No longer needed                              |
| 455                 | Permanently deleted        | Data fully removed                            |

The numbers are illustrative — the instructor explicitly states: **"I'm just throwing some numbers over here. These numbers will be based on your use cases."** The pattern is universal; the specific day counts are project-specific. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Critical constraint:** The transition to **Glacier Deep Archive must be at least 90 days after the transition to Glacier Flexible Retrieval**. The instructor explicitly calculates this: "90 plus 90, 180 I can give. 180 or more." This is an AWS-enforced minimum gap. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

***

## 4. Lifecycle Rules and Versioning — The Dual-Track Problem

When a bucket has **versioning enabled**, lifecycle rules become more nuanced because every object can have multiple versions — the **current version** (the latest) and **non-current versions** (previous versions). [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

The instructor makes a critical point: **"This bucket is versioned. So you should define rules for the current object and the non-current version object also if you want to save the cost. Otherwise, there's no point in just transitioning the current version object because the old version still exists over there and it'll be still occupying the space."** [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

This means a lifecycle rule in a versioned bucket must handle **two tracks**:

* **Current version transitions** — moving the latest version through storage classes.
* **Non-current version transitions** — moving older versions through storage classes (typically on a slightly different, often slightly longer, timeline).

Without configuring both tracks, old versions accumulate in Standard storage indefinitely, negating the cost savings on the current version. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

***

## 5. Object Expiration — Delete vs Delete Marker

Lifecycle rules can also **expire** objects — but the behavior depends on whether the bucket is versioned: [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

* **Non-versioned bucket:** Expire = **delete** the object permanently.
* **Versioned bucket:** Expire = **place a delete marker**. The object is hidden (appears deleted to normal access) but the data still exists as a non-current version.

To truly remove data from a versioned bucket, you need a separate rule to **permanently delete non-current versions** after a specified number of days. The instructor configures both: expire at 450 days (places delete marker) and permanently delete non-current versions at 455 days. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

***

## 6. Incomplete Multipart Uploads

When large files are uploaded to S3, they're split into parts (multipart upload). If an upload fails partway through, **incomplete parts remain in the bucket**, consuming storage and costing money. The lifecycle rule can **automatically delete incomplete uploads** after a specified number of days. The instructor sets this to 15 days. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

***

## 7. Cross-Region Replication (CRR) — Disaster Recovery

Cross-region replication copies objects from a **source bucket in one region** to a **destination bucket in a different region** automatically. This is the primary mechanism for S3 disaster recovery. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

The instructor creates a destination bucket in **Oregon** (a different region from the source) and sets up a replication rule. Key architectural points: [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Versioning must be enabled on both buckets.** Replication requires versioning on the destination bucket. The console provides an option to enable it during replication setup.

**IAM role is required.** The replication process needs **permission** to write to the destination bucket. The instructor clicks **"Create new IAM role"** — this creates a role that grants the source bucket permission to copy data into the destination bucket. IAM roles are covered in detail later in the course.

**Destination storage class can be different.** The instructor makes an important cost optimization point: the disaster recovery bucket **won't be accessed frequently** (it's only for disasters), so you should change its storage class to something cheaper like **Standard Infrequent Access** or **One Zone Infrequent Access** instead of keeping it in Standard. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Replication scope:** You can replicate **all objects** or **limit by prefix filter** (e.g., only objects whose keys start with "images/").

**Existing vs new objects:** Replication applies to **new objects uploaded after the rule is created**. Existing objects are **not replicated by default**. There is an option to replicate existing objects, but it incurs additional charges. The instructor advises: **"Don't do that. There will be charges for it."** [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

<details>
<summary>🔍 Deep Dive</summary>

Several optional replication features exist:

* **Replication Time Control (RTC):** Guarantees 99.99% of objects replicated within **15 minutes**. Costs extra. The instructor mentions it but notes: **"for disaster recovery, really we don't do that"** — DR doesn't require real-time replication. RTC is for use cases where near-real-time cross-region copies are needed (e.g., multi-region active-active applications).

* **Delete marker replication:** You can choose to replicate delete markers to the destination bucket. This means if an object is deleted in the source, the deletion is reflected in the destination.

* **Replication metrics:** CloudWatch metrics for monitoring replication progress and lag. Costs extra.

* **Cross-account replication:** You can replicate to a bucket in a **different AWS account** by providing the account ID and bucket path. Used in multi-account enterprise architectures.

</details>

***

## 8. The Encryption Layer

The instructor briefly mentions two encryption contexts: [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Lifecycle rules:** Objects being transitioned between storage classes retain their encryption.

**Replication:** By default, S3 encrypts data. If you need KMS-based encryption on the destination bucket, you can configure it during replication setup. This is optional and adds cost.

***

## 9. Additional S3 Features — Mentioned but Not Deep-Dived

The instructor references several other S3 capabilities to build awareness: [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

* **Metrics:** You can generate storage metrics, replication metrics, and storage class analysis. The instructor says these are "out of the scope of DevOps but go through it. It'll be helpful for you in the interview."
* **Access Points:** Private access to S3 within a VPC. The instructor explicitly says: **"This won't make any sense when I'm saying this, but when you learn VPC, then you will understand this point."** Covered in AWS Part 2.

***

## 10. Cleanup — The Operational Discipline

The instructor demonstrates the cleanup process and emphasizes its importance. The order matters: [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

1. **Delete lifecycle rules and replication rules** first (remove the automation).
2. **Empty the bucket** (permanently delete all objects).
3. **Delete the bucket** itself.

You cannot delete a non-empty bucket — you must empty it first. The instructor shows: empty → confirm permanent deletion → bucket still exists but is empty → then delete the bucket by name.

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are configuring two advanced S3 features on an existing bucket: a **lifecycle rule** that automatically transitions objects through cheaper storage classes as they age (saving costs), and a **cross-region replication rule** that copies new objects to a bucket in another region (disaster recovery). After testing, we clean up everything. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Why it matters:** These two features are "pretty commonly used" in real projects. Every production S3 bucket in a cost-conscious, compliance-aware organization will have some version of these configurations.

**Final outcome:** A lifecycle rule that moves objects Standard → Standard-IA → One Zone-IA → Glacier → Glacier Deep Archive → expire/delete over 455 days, and a replication rule copying new objects to a DR bucket in a different region.

***

## Step 1: Navigate to Lifecycle Rules

1. Open your S3 bucket in the AWS console. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)
2. Go to the **Management** tab.
3. You'll see **Lifecycle rules** section.
4. Click **Create lifecycle rule**.

**Connection to flow:** This is where all automated object management policies are configured.

***

## Step 2: Create the Lifecycle Rule

**Rule name:** `CostEffectiveTransitions` (or any descriptive name). [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Scope:** Choose one of:

* **Apply to all objects** — every object in the bucket follows this rule.
* **Limit scope with prefix** — only objects whose keys start with a specific prefix (e.g., `image`). Useful when different data types need different lifecycle policies.

The instructor selects **all objects** for this exercise.

**Select transition actions (checkboxes):** [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

* ✅ **Move current version objects between storage classes**
* ✅ **Move non-current version objects between storage classes** (critical for versioned buckets — see Theory)
* ✅ **Expire current version of objects** (places delete marker in versioned bucket)
* ✅ **Permanently delete non-current versions**
* ✅ **Delete incomplete multipart uploads**

### Configure Current Version Transitions:

| From        | To                         | After (days) |
| ----------- | -------------------------- | ------------ |
| Standard    | Standard Infrequent Access | 30           |
| Standard-IA | One Zone Infrequent Access | 60           |
| One Zone-IA | Glacier Flexible Retrieval | 90           |
| Glacier     | Glacier Deep Archive       | 180          |

**⚠️ Constraint:** Glacier → Glacier Deep Archive must have **≥ 90 days gap**. (90 + 90 = 180 minimum.) [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Acknowledge** the transition timeline.

### Configure Non-Current Version Transitions:

| To                         | After (days) |
| -------------------------- | ------------ |
| Standard Infrequent Access | 35           |
| One Zone Infrequent Access | 65           |
| Glacier Flexible Retrieval | 95           |
| Glacier Deep Archive       | 185          |

**Acknowledge** the transition timeline. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

### Configure Expiration:

* **Expire current version:** 450 days (places delete marker).
* **Permanently delete non-current versions:** 455 days.

### Configure Incomplete Uploads:

* **Delete incomplete multipart uploads after:** 15 days.

**Click Create Rule.** [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Expected result:** Rule created successfully. Visible in the Management tab.

**Common mistake:** Setting Glacier Deep Archive transition less than 90 days after Glacier → AWS will reject the rule with an error.

**Verification:** Click on the created rule to see its details. You can edit or delete it later.

**Connection to flow:** Objects in this bucket will now automatically transition through cheaper storage classes over time, saving costs without any manual intervention. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

***

## Step 3: Create the Destination Bucket for Disaster Recovery

**What we are doing:** Creating a second S3 bucket in a **different AWS region** to serve as the replication target. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

1. **Switch to a different region** in the AWS console (e.g., **Oregon / us-west-2**).
2. Create a new bucket with a DR-indicating name (e.g., `barista908dr`).
3. Keep all defaults and click **Create Bucket**.

**Operational reasoning:** The DR bucket must be in a different region for geographic redundancy. If the source region experiences a disaster, the DR region is unaffected.

**Connection to flow:** Destination bucket exists. Now configure replication from the source bucket.

***

## Step 4: Create the Replication Rule

1. **Go back to the original bucket** (source bucket, original region). [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)
2. Go to **Management** tab → **Replication rules** → **Create replication rule**.

**Rule name:** `DisasterRecoveryBarista908` (or descriptive name).

**Status:** Enabled.

**Scope:** Replicate all objects (or limit by prefix filter based on requirement). [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Destination:**

1. Choose **"A bucket in this account"** (or cross-account if needed — requires account ID + bucket path).
2. Click **Browse** → find and select the DR bucket (in the different region).
3. If the bucket doesn't appear, **refresh the page** — sometimes it takes a moment.

**Versioning requirement:** The destination bucket **must have versioning enabled**. The console offers to enable it from the replication setup screen, or you can go to the bucket properties and enable it manually. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**IAM Role:** Click **"Create new IAM role"** — this auto-creates the permission that allows the source bucket to write to the destination bucket. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Destination storage class:** Change from Standard to something cheaper (e.g., **Standard Infrequent Access** or **One Zone Infrequent Access**) — the DR bucket won't be accessed frequently. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Optional settings (instructor leaves as default):**

* Replication Time Control (15-min guarantee) — extra cost, not needed for DR.
* Delete marker replication — optional.
* Replication metrics — extra cost.

**Click Save.** [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Prompt about existing objects:** AWS asks if you want to replicate existing objects. The instructor advises: **"Don't do that. There will be charges for it."** Select **"Do not replicate existing objects"** → **Submit**. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Expected result:** Replication rule created. New objects uploaded to the source bucket will be automatically copied to the DR bucket. Existing objects remain only in the source bucket.

**Common mistakes:**

* Forgetting to enable versioning on the destination bucket → replication fails.
* Not refreshing the page when the destination bucket doesn't appear in the browse list.
* Choosing to replicate existing objects during practice → unexpected charges.

**Connection to flow:** The DR pipeline is active. New uploads are replicated across regions automatically.

***

## Step 5: Clean Up — Delete Rules, Empty Buckets, Delete Buckets

**Order of cleanup operations:** [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

### 5a: Delete the automation rules first

1. Go to **Management** tab.
2. Delete the **lifecycle rule**.
3. Delete the **replication rule**.

### 5b: Empty each bucket

1. Select the bucket → click **Delete**.
2. AWS prompts: bucket is not empty → click **Empty the bucket**.
3. Type **"permanently delete"** to confirm.
4. Bucket is now empty (but still exists).

### 5c: Delete each bucket

1. Select the empty bucket → click **Delete bucket**.
2. Type the **bucket name** to confirm → delete.
3. Repeat for all buckets (source and DR). [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

**Operational reasoning:** You cannot delete a non-empty bucket. Rules should be removed first to prevent them from continuing to act on objects or incurring charges during cleanup.

**Connection to flow:** Full cleanup complete. No lingering resources, no unexpected charges.

<details>
<summary>⚠️ Expert Note</summary>

In production, you would never delete these rules. Lifecycle rules run continuously and are a core cost-optimization mechanism. Replication rules run continuously for DR compliance. The cleanup here is specific to the learning exercise. In real environments, you'd iterate on the rules — adjusting transition days based on access pattern analysis (available through S3 Storage Class Analysis metrics) and refining replication scope as the project evolves.

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   S3 Advanced Features — Lifecycle Rules + Cross-Region Replication
CONTEXT: AWS S3 → cost optimization + disaster recovery
PURPOSE: Automate storage cost reduction + geographic data protection
```

***

## Two Features, Two Problems

```
LIFECYCLE RULES           → COST problem
                            Data access frequency decreases over time
                            Don't pay Standard price for rarely-accessed data
                            Solution: auto-transition to cheaper classes by age

CROSS-REGION REPLICATION  → DISASTER RECOVERY problem
                            Region-level failure = data loss
                            Compliance requires geographic redundancy
                            Solution: auto-copy to bucket in another region
```

***

## S3 Storage Class Cost Ladder

```
STANDARD                     ← most expensive, fastest access
    ↓ 30 days
STANDARD INFREQUENT ACCESS   ← cheaper, rapid access when needed
    ↓ 60 days
ONE ZONE INFREQUENT ACCESS   ← cheapest IA, single AZ only (risk: AZ loss = data loss)
    ↓ 90 days
GLACIER FLEXIBLE RETRIEVAL   ← archive, retrieval: minutes-hours (formerly "Glacier")
    ↓ 180 days (must be ≥90 days after Glacier)
GLACIER DEEP ARCHIVE         ← cheapest, retrieval: hours (up to 12h)
    ↓ 450 days
EXPIRE (delete marker)       ← hidden in versioned bucket
    ↓ 455 days
PERMANENTLY DELETE            ← data fully removed
```

***

## Lifecycle Rule — Dual-Track for Versioned Buckets

```
VERSIONED BUCKET requires TWO tracks:

CURRENT VERSION:          Standard → IA → One Zone → Glacier → Deep Archive → Expire
NON-CURRENT VERSIONS:     Standard → IA → One Zone → Glacier → Deep Archive → Permanently Delete

WHY BOTH? Old versions still occupy space + cost money
          Transitioning only current = partial cost savings
```

***

## Expiration Behavior

```
Non-versioned bucket:  expire = DELETE permanently
Versioned bucket:      expire = place DELETE MARKER (data still exists as non-current)
                       → must separately configure "permanently delete non-current versions"
```

***

## Lifecycle Rule Constraints

```
Glacier → Glacier Deep Archive: MINIMUM 90 days gap
All day values: project-specific (instructor numbers are illustrative)
Incomplete multipart uploads: can auto-delete (e.g., after 15 days)
```

***

## Cross-Region Replication Architecture

```
SOURCE BUCKET (Region A)                    DESTINATION BUCKET (Region B)
┌──────────────────────┐                    ┌──────────────────────────┐
│ Standard class       │ ──── CRR rule ───→ │ Standard-IA class        │
│ Versioning: ON       │   (auto-copy)       │ Versioning: ON (required)│
│ Objects + new uploads│                    │ New objects only (default)│
└──────────────────────┘                    └──────────────────────────┘

REQUIREMENTS:
  - Both buckets: versioning ENABLED
  - IAM role: grants source write permission to destination
  - Different regions (that's the whole point)

DEFAULTS:
  - Only NEW objects replicated (existing objects NOT replicated unless opted in + paid)
  - Replication is async (not instant) unless RTC enabled (15 min, extra cost)
```

***

## Replication Options

```
Scope:           all objects OR filter by prefix
Account:         same account OR cross-account (needs account ID)
Storage class:   can change destination class (cheaper for DR)
RTC:             15-min guarantee (paid) — not needed for DR
Delete markers:  optional replication
Metrics:         optional CloudWatch metrics (paid)
Existing objects: not replicated by default (opt-in = charges)
```

***

## Cleanup Order

```
1. Delete RULES first (lifecycle, replication)
2. EMPTY buckets (permanently delete all objects)
3. DELETE buckets (by name confirmation)

Cannot delete non-empty bucket → must empty first
```

***

## Mentioned But Not Deep-Dived

```
Access Points    → private S3 access within VPC (covered in AWS Part 2 with VPC)
Metrics          → storage analysis, replication metrics (out of DevOps scope, good for interviews)
KMS Encryption   → optional on replication destination (extra cost)
```

***

## Reusable Engineering Patterns

```
1. AGE-BASED TIERING           → Data value decreases with age → auto-move to cheaper tier
                                  (same pattern: email archiving, log rotation, backup retention)

2. DUAL-TRACK VERSIONING       → When versioning exists, rules must cover BOTH current + old
                                  Ignoring old versions = hidden cost leak

3. GEOGRAPHIC REDUNDANCY       → Copy critical data to another region/continent
                                  Compliance + disaster protection

4. COST-APPROPRIATE DESTINATION→ DR bucket doesn't need Standard class
                                  Match storage class to access pattern (DR = infrequent access)

5. NEW-ONLY DEFAULT            → Replication/migration defaults to new data only
                                  Backfilling existing data = separate operation + cost

6. RULE-BEFORE-CLEANUP         → Remove automation rules before deleting resources
                                  Prevents rules from acting during cleanup
```

***

## Rapid Recall Triggers

```
"What is a lifecycle rule?"           → Auto-transition objects between storage classes by age (cost saving)
"S3 storage classes in order?"        → Standard → Standard-IA → One Zone-IA → Glacier → Glacier Deep Archive
"Cheapest S3 class?"                  → Glacier Deep Archive
"Glacier Deep Archive constraint?"    → Must be ≥90 days after Glacier Flexible Retrieval
"Expire in versioned bucket?"         → Places delete marker (data still exists as non-current)
"Why configure non-current versions?" → Old versions still occupy space + cost → must transition them too
"What is CRR?"                        → Cross-Region Replication — auto-copy to bucket in different region
"CRR requirements?"                   → Versioning ON both buckets + IAM role + different regions
"Does CRR copy existing objects?"     → No (by default) — only new uploads. Backfill = opt-in + charges
"DR bucket storage class?"            → Use cheaper class (Standard-IA / One Zone-IA) — won't be accessed often
"Cleanup order?"                      → Delete rules → empty buckets → delete buckets
"Incomplete multipart uploads?"       → Lifecycle rule can auto-delete them (e.g., 15 days)
"Access Points?"                      → Private S3 access in VPC — covered in AWS Part 2
"Day numbers in lifecycle rule?"      → Project-specific — instructor numbers are illustrative only
```

***

This completes the full reconstruction of the S3 Advanced Features session. **Theory** builds the conceptual architecture of storage class tiering, versioned lifecycle behavior, and cross-region replication mechanics; **Practical** walks through every console configuration step with operational reasoning and cleanup discipline; and the **Mental Compression Map** compresses the entire cost ladder, dual-track versioning model, and replication architecture into rapid-recall structures. [\[130. More in S3 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/130.%20More%20in%20S3.txt)

Ready for the next caption file, or shall I generate an **AnkiDroid CSV** covering this lecture or the entire series so far? 🚀
