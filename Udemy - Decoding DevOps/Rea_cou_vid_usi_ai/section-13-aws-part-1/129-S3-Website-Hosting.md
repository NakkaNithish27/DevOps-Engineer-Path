# 🎓 Deep Learning Material: S3 Static Website Hosting, Access Logs & Versioning

*Reconstructed from video lecture captions (129. S3 Website Hosting.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 S3 as a Static Website Host: What It Is and Why It Matters

S3 is not just a storage service — it can **directly host static websites**. The instructor calls this *"a very popular use case"* and states: *"There are many websites, static websites basically, that are running on S3 bucket."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

A static website is one that consists only of **fixed files** — HTML, CSS, JavaScript, images, videos — that are served directly to the browser without any server-side processing. There is no backend application generating pages dynamically, no database queries, no user sessions handled on the server. The browser receives the files exactly as they are stored. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

The transformative insight the instructor emphasizes is what you **eliminate** by using S3 for static hosting: *"No more Apache HTTP service, no EC2 instances, no load balancer."*  In the traditional approach, hosting a website requires: a virtual machine (EC2), a web server installed on it (Apache/Nginx), potentially a load balancer for redundancy, security group configuration, OS patching, and ongoing maintenance. S3 static website hosting replaces all of that with a single bucket configuration. You upload files, enable a setting, and the website is live. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Beyond full static websites, the instructor points out a second use case: **dynamic web applications** (where users log in, post content, etc.) often need **publicly available static assets** — images, documents, videos. S3 serves as the storage and delivery layer for these assets.  The dynamic application runs on EC2/containers, but its static resources are served from S3, offloading bandwidth and simplifying the application architecture. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

***

## 1.2 S3 Static Website Hosting: How It Works Internally

When you enable static website hosting on an S3 bucket, AWS creates a **website endpoint** — a special URL that serves the bucket's contents as a website rather than as raw S3 objects. This endpoint behaves like a web server: when a user requests the root URL, S3 serves the **index document** (typically `index.html`); when a request results in an error, S3 serves the **error document** (typically `error.html`). [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

The two required configurations are:

* **Index document** — The default page served when someone accesses the root URL (e.g., `index.html`)
* **Error document** — The page served when a requested resource doesn't exist (e.g., `error.html`)

The instructor notes that even if you don't have an actual error page, you still need to provide the name: *"We don't have any error.html, but we have to give the name."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

After enabling static website hosting, S3 provides a **bucket website endpoint URL**. This URL is how the world accesses your website. The instructor also mentions that in real projects, you'd map your own domain to this URL using **CNAME records** in your domain provider: *"You can use this URL and put it in your domain... we'll see how to enable those CNAME records in your domain."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

🔍 **Deep Dive:**
The S3 website endpoint URL has a specific format (e.g., `http://bucket-name.s3-website-region.amazonaws.com`). This is different from the standard S3 object URL. The website endpoint processes requests like a web server (routing `/` to `index.html`, returning error pages for 404s), while the standard S3 URL treats each request as a direct object key lookup. The website endpoint does **not** support HTTPS natively — for HTTPS, you'd place CloudFront (AWS CDN) in front of it, which also adds edge caching and a custom domain with SSL.

***

## 1.3 Public Access: The Prerequisite for Website Hosting

For a website to be accessible by anyone on the internet, all objects in the bucket must be **publicly readable**. By default, S3 objects are **private** — the instructor emphasizes this as a recurring rule: *"Remember, by default, every object that you upload on S3 bucket is private."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Making objects public requires three steps (previously covered in the course but executed again here): [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

1. **Block Public Access settings** — Must be unchecked (disabled) at the bucket level to allow any public access
2. **Object Ownership / ACLs** — ACLs must be enabled so you can set per-object public permissions
3. **Make objects public using ACL** — Each object (or batch of objects) must be explicitly made public

The critical operational detail: **newly uploaded objects are private by default, even if the bucket already has public objects**. When the instructor uploads a new `index.html` (the overwrite version), it's private, and the website returns "Forbidden" until he explicitly makes the new object public.  This is not inherited — each new object starts private. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

⚠️ **Expert Note:**
The ACL-based approach demonstrated here works for learning but is considered legacy practice. In production, **bucket policies** are the preferred method for managing public access. A single bucket policy can grant public read access to all objects in the bucket (or a prefix), eliminating the need to set ACLs on each object individually. The instructor mentions bucket policies as a future topic.

***

## 1.4 Server Access Logs: Tracking Who Accesses Your Website

When a website is live, you need to know who is accessing it — the requests, the browsers, the regions, the errors. This operational visibility is provided by **S3 server access logs**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

The instructor explains: *"When the user accesses, you should know, right, the access from where it is coming, who is accessing it, what browser they're using, regions. All this information gets stored in the access logs."*  He draws a parallel to the Apache access logs covered earlier in the course. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

The architecture requires **two buckets**: [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

1. **Source bucket** — Hosts the website (e.g., `barista908`)
2. **Destination bucket** — Stores the access logs (e.g., `barista908accesslogs`)

You cannot store access logs in the same bucket that generates them (this would create an infinite logging loop — each log write would generate another log entry). The destination bucket is a separate, dedicated storage location. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

When you enable server access logging and specify the destination bucket, AWS **automatically creates a bucket policy** on the destination bucket that allows the S3 logging service to write log objects there. The instructor shows this: *"If you go to permissions, if you scroll down, bucket policy, this is a JSON policy which is automatically created when we selected this as the destination bucket for access log. This allows the access logs to be stored in this S3 bucket."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

An important timing detail: logs are **not written immediately**. The instructor warns: *"Now it won't be immediately stored. It's going to take some time. You keep accessing your website on the S3 and after some time you will see the access logs appearing over here."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

***

## 1.5 Versioning: S3's Built-In Data Protection System

Versioning is one of the most powerful and most misunderstood features of S3. When enabled, S3 **preserves every version of every object** — every upload, every overwrite, every delete — nothing is truly destroyed. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### How Versioning Handles Overwrites

When you upload a file with the same name as an existing object (overwriting it), S3 does **not replace** the original. Instead, it stores the new upload as a **new version** and marks it as the "latest" version. The old version still exists, with its own unique **version ID**. The instructor demonstrates this by uploading a new `index.html` that replaces the original website with a simple text page. When he clicks "Show versions," both versions are visible — the original and the new one. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### How Versioning Handles Deletes

When you delete an object from a versioned bucket (without specifying a version), S3 does **not actually remove** the data. Instead, it places a **delete marker** on top of the object. The delete marker is a special zero-size object that tells S3: "When someone asks for this object, pretend it doesn't exist." The instructor explains: *"The file already exists over there, and there is a delete marker placed on top of it, so file did not go anywhere. You see, file has a size, delete marker has no size."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

The object appears deleted in the normal view (versions toggled off), but when you toggle "Show versions" on, you see the original object is still there with the delete marker sitting above it.

### Recovery Mechanisms

**Recovering a deleted object:** Remove the delete marker. The instructor demonstrates this: select the delete marker → delete it (this is a permanent delete of the marker itself) → toggle versions off → the original file reappears. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Recovering from an overwrite:** Delete the latest (unwanted) version. The instructor demonstrates this after uploading a bad `index.html`: toggle "Show versions" → select the latest version → permanently delete it → the previous version becomes the current one → the website is restored. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### The Critical Cost Warning

The instructor delivers an important warning about versioning's storage implications: *"If you have S3 bucket where you continuously regularly override the object, it is going to very quickly increase the size, and you will end up paying more."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

The reasoning: when you overwrite, nothing is actually overwritten — both the old and new versions consume storage. If a 10MB file is overwritten 100 times, you're storing 1GB (100 × 10MB), not 10MB. The instructor states clearly: *"Enable versioning if it's really, really required. Otherwise, you need to pay extra because when you override, nothing gets overwritten. It's just the newer version. So data does not go anywhere."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

If you genuinely want to free storage, you must **show versions and delete the individual versions** — not just the visible object. Deleting the visible object only adds a delete marker; the data remains.

🔍 **Deep Dive:**
There are two fundamentally different "delete" operations in a versioned bucket:

1. **Simple delete** (no version ID specified) → Places a delete marker → Recoverable → No storage freed
2. **Version delete** (specific version ID targeted) → **Permanently** removes that version's data → Storage freed → Irreversible

The instructor demonstrates both. The UI makes this distinction visible: simple deletes show "delete" in the confirmation, while version deletes show **"permanently delete"** and require you to type the phrase.  This is a safety mechanism — permanent deletions require explicit confirmation. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are hosting a **static website on an S3 bucket**, configuring **access logs** to a separate bucket, and exploring **versioning** behavior (overwrites, deletes, recovery). The final outcome: a publicly accessible website running entirely on S3 with no servers, plus operational understanding of versioning as a data protection and recovery mechanism. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

***

## Phase 1: Prepare the Website Files

### Step 1: Download a Website Template

Go to **tooplate.com** → select a template (the instructor selects the first one, "Barista") → scroll down → click **Download**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 2: Extract the Downloaded Archive

Locate the downloaded file in your Downloads folder → right-click → **Extract**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Result:** A folder containing all the website files (HTML, CSS, JS, images, etc.). These are the files we'll upload to S3.

***

## Phase 2: Create the S3 Buckets

### Step 3: Create the Website Bucket

Navigate to **S3** service → click **Create bucket**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Configuration:**

* **Bucket name:** `barista908` (or any unique name — the instructor appends numbers to ensure uniqueness)
* **Bucket Versioning:** **Enable** (we'll use this later in the lecture)

Click **Create bucket**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Important naming rule:** Bucket names must be **all lowercase**. The instructor initially tries uppercase and gets an error: *"Oh yeah, I cannot give upper cases. I forgot that."* [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 4: Create the Access Logs Bucket

Create a second bucket for storing access logs: [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

* **Bucket name:** `barista908accesslogs` (all lowercase)
* No special settings needed — just create it

Click **Create bucket**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Why two buckets:** The website bucket generates logs; the logs bucket stores them. They must be separate (see Theory 1.4).

***

## Phase 3: Upload Website Files

### Step 5: Upload All Files to the Website Bucket

Open the website bucket (`barista908`) → click **Upload** → click **Add files**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Method:** Select all files from the extracted template folder, **drag and drop** them into the upload area. Click **Upload**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Note:** The instructor mentions that later in the course, uploading/syncing via command line (`aws s3 sync`) will be covered. For now, the UI method is used. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Verification:** All files appear listed in the bucket after upload completes.

***

## Phase 4: Enable Public Access

### Step 6: Disable Block Public Access

Navigate to the bucket's **Permissions** tab → **Block public access** → click **Edit** → **uncheck** all boxes → **Save changes** → type `confirm`. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 7: Enable ACLs

Still in **Permissions** → **Object Ownership** → **Enable ACLs** → **Save changes**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 8: Make All Objects Public

Go to the bucket's **Objects** tab → **select all objects** → click **Actions** → **Make public using ACL**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

A warning appears: objects will be available to everyone on the internet. Click **Make public**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Connection to flow:** All website files are now publicly readable. Without this, the website would return "403 Forbidden" for every request.

***

## Phase 5: Enable Static Website Hosting

### Step 9: Configure the Website Endpoint

Navigate to the bucket's **Properties** tab → scroll to the bottom → find **Static website hosting** → click **Edit** → select **Enable**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Configuration:**

* **Index document:** `index.html`
* **Error document:** `error.html` (enter the name even if the file doesn't exist — it's required) [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Click **Save changes**.

**Result:** A **website endpoint URL** is generated. Copy this URL. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 10: Access the Website

Paste the URL into your browser → hit Enter. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Expected result:** The website loads and displays correctly. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Verification:** You should see the full Barista template rendered — HTML, CSS, images all loading. If any images are broken, those specific objects may not be public.

**What you've achieved:** A fully functional website with zero servers, zero web server software, zero OS maintenance.

***

## Phase 6: Enable Server Access Logging

### Step 11: Configure Access Logs

Navigate to the website bucket's **Properties** tab → find **Server access logging** → click **Edit** → **Enable**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Destination:** Browse and select the access logs bucket (`barista908accesslogs`). The format should be `s3://barista908accesslogs`. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

There's an option for **log object key format** (how logs are organized by date — year/month/date). Keep the default. Click **Save changes**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Verification (delayed):** Access logs won't appear immediately. Access your website a few times, then check the logs bucket after some time (can take minutes to hours). Log objects will start appearing. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 11a: Observe the Auto-Created Bucket Policy

Navigate to the access logs bucket → **Permissions** → scroll to **Bucket policy**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

You'll see a **JSON policy** that was **automatically created** by AWS when you configured this bucket as the logging destination. This policy grants the S3 logging service permission to write log objects into this bucket. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Why this matters:** This demonstrates AWS's service-to-service permission model — the logging service needs explicit permission to write to your bucket, and AWS handles this automatically during configuration.

***

## Phase 7: Explore Versioning

### Step 12: View Existing Versions

In the website bucket, click the **Show versions** toggle. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**What you'll see:** Each object has a **Version ID**. Since no objects have been overwritten or deleted yet, each has only one version. Folders don't have version IDs — only the files inside them do. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Toggle off** before proceeding.

### Step 13: Test Delete Behavior

Select `ABOUT THIS TEMPLATE.txt` → click **Delete** → in the confirmation, type `delete` (note: NOT "permanently delete") → **Delete objects**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**What happened:** The file disappears from the normal view. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Now **toggle Show versions on**. You'll see: [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

* The original file (with a size and version ID) — **still exists**
* A **delete marker** on top (no size, its own version ID)

**Recovery:** Select the **delete marker** → Delete → this time you see **"permanently delete"** → type it → Delete objects. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Toggle versions off → the file has **reappeared**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 14: Test Overwrite Behavior

Create a simple test file:

* Open **Notepad** → type `this is my website on S3` → **Save As** → filename: `index.html` → save type: **All Files** (not .txt) → save to Desktop [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Important:** Set save type to "All Files" — otherwise Windows saves it as `index.html.txt`. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Upload this new `index.html` to the bucket: click **Upload** → **Add file** → select the Desktop `index.html` → **Upload**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 15: Observe the Overwrite Result

Access the website URL again. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Result:** `403 Forbidden`. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Why:** The new `index.html` is a **new object** — it's private by default. Make it public: select it → **Actions** → **Make public using ACL** → **Make public**. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Refresh the browser. Now you see the plain text "this is my website on S3" instead of the original website. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 16: Recover from the Overwrite

Toggle **Show versions** on → you'll see two versions of `index.html` (the original and the new one). [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Select the **latest version** (the bad one) → Delete → type **"permanently delete"** → Delete objects. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Toggle versions off. Access the website URL again. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

**Result:** The original website is restored. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

### Step 17: Understand the Cost Implication

The instructor warns: versioning stores ALL versions. If objects are overwritten frequently, storage grows linearly with each overwrite, and you pay for all of it. Only **permanently deleting individual versions** frees storage. Simply "deleting" objects only adds delete markers — data remains. [\[129. S3 We...te Hosting \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/129.%20S3%20Website%20Hosting.txt)

Enable versioning only when data protection justifies the cost.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## S3 Website Hosting Identity

```
S3 Static Website Hosting = Serverless web hosting
  Upload files → enable setting → website is live
  Eliminates: EC2, Apache/Nginx, Load Balancer, OS patching

Use cases:
  ├── Full static websites (HTML/CSS/JS/images)
  └── Static asset storage for dynamic apps (images, videos, docs)
```

***

## Architecture: Two Buckets

```
[Website Bucket]  ──hosts──→  static website files
  barista908         ├── index.html (index document)
                     ├── CSS, JS, images
                     └── Versioning: ENABLED

[Access Logs Bucket]  ──stores──→  server access logs
  barista908accesslogs    └── Auto-created bucket policy (S3 logging → write permission)

Website bucket generates traffic → Logs bucket receives log data
Must be SEPARATE buckets (no self-logging loop)
```

***

## Static Website Hosting Config

```
Properties → Static website hosting → Enable
  Index document: index.html  (served for root URL "/")
  Error document: error.html  (served for 404s — name required even if file missing)
  
Result: Website endpoint URL generated
  → Paste in browser → website loads

Custom domain: Map CNAME record to S3 endpoint URL (covered later)
```

***

## Public Access Chain (Required for Website)

```
1. Permissions → Block Public Access → UNCHECK all → Save → Confirm
2. Permissions → Object Ownership → Enable ACLs → Save
3. Objects → Select all → Actions → Make public using ACL

CRITICAL: New uploads are PRIVATE by default
  → New object uploaded → must be made public again
  → Forgetting this → 403 Forbidden
```

***

## Access Logs

```
Properties → Server access logging → Enable
  Destination: s3://logs-bucket-name
  Format: default (year/month/date)

Timing: NOT immediate → logs appear after delay (minutes to hours)
Auto-action: AWS creates bucket policy on destination bucket (JSON, auto-generated)
```

***

## Versioning: Complete Behavior Model

```
VERSIONING ENABLED ON BUCKET

OVERWRITE behavior:
  Upload same filename → OLD version kept → NEW version added on top
  Both consume storage | Both have unique Version IDs
  Normal view: shows latest only | Show versions: shows all

DELETE behavior (simple, no version ID):
  Object "disappears" from normal view
  Actually: DELETE MARKER placed on top (zero size)
  Data: STILL EXISTS underneath marker
  Storage: NOT freed

DELETE behavior (specific version ID):
  PERMANENTLY removes that version's data
  Storage: FREED
  Confirmation: Must type "permanently delete" (safety gate)
```

***

## Versioning Recovery Patterns

```
RECOVER DELETED OBJECT:
  Show versions → select DELETE MARKER → permanently delete marker
  → Toggle off → file reappears

RECOVER FROM BAD OVERWRITE:
  Show versions → select LATEST (bad) version → permanently delete it
  → Previous (good) version becomes current → website restored
```

***

## Versioning Delete: Two Types

```
                    Simple Delete              Version Delete
────────────────────────────────────────────────────────────────
What happens:       Delete marker added        Data permanently removed
Data still exists:  YES                        NO
Storage freed:      NO                         YES
Recoverable:        YES (remove marker)        NO (irreversible)
Confirmation text:  "delete"                   "permanently delete"
```

***

## Versioning Cost Warning

```
Overwrite 10MB file 100 times → 100 versions × 10MB = 1GB stored
  (NOT 10MB — nothing is overwritten, all versions kept)

Enable versioning ONLY when:
  └── Data protection value > storage cost increase

To actually free storage:
  └── Show versions → delete INDIVIDUAL VERSIONS (not just the object)
```

***

## Operational Flow (Complete)

```
── PREPARE ──
Download template (tooplate.com) → extract folder

── CREATE BUCKETS ──
S3 → Create bucket: website (enable versioning) + logs (plain)
  Rule: all lowercase names

── UPLOAD ──
Website bucket → Upload → drag & drop all files

── PUBLIC ACCESS ──
Permissions → unblock public access → enable ACLs
Objects → select all → make public using ACL

── ENABLE WEBSITE ──
Properties → Static website hosting → enable
  Index: index.html | Error: error.html
  → Copy endpoint URL → paste in browser → website live

── ENABLE LOGGING ──
Properties → Server access logging → enable → select logs bucket
  → Logs appear after delay in logs bucket
  → Auto-created bucket policy on logs bucket

── VERSIONING DEMO ──
Delete object → show versions → see delete marker → remove marker → file returns
Upload new index.html → 403 (private!) → make public → see new content
  → Show versions → delete latest → original restored

── CLEANUP (implied) ──
Delete objects + versions | Delete buckets | Or leave for next lecture
```

***

## Reusable Engineering Patterns

| Pattern                         | Manifestation                                                                                         |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Serverless infrastructure**   | S3 replaces EC2 + Apache + LB for static sites — zero server management                               |
| **Separation of data and logs** | Website bucket ≠ logs bucket — prevents self-referential loops                                        |
| **Default-deny security**       | Every new S3 object is private — public access is opt-in, per-object                                  |
| **Soft delete / hard delete**   | Delete marker (recoverable) vs. version delete (permanent) — two-tier safety                          |
| **Immutable history**           | Versioning = append-only log of all changes — nothing truly deleted unless explicitly version-deleted |
| **Auto-generated permissions**  | AWS auto-creates bucket policy for logging destination — service-to-service trust                     |
| **Cost-awareness in features**  | Versioning protects data but multiplies storage cost — must be a deliberate trade-off                 |

***

## Core Mental Model

```
S3 Website Hosting = "Web server as a service"
  Upload files → flip a switch → website live
  No servers, no OS, no patching, no scaling config

Versioning = "Git for S3 objects"
  Every change is a commit (new version)
  Delete = soft delete (marker, recoverable)
  Version delete = force-push/rewrite (permanent, irreversible)
  Storage grows with every "commit" — no auto-cleanup

Two-bucket pattern:
  Bucket A (website) → generates data
  Bucket B (logs)    → observes Bucket A
  Separation = no feedback loops + clean permissions
```

***

This material captures every concept, configuration step, versioning behavior, recovery technique, cost warning, and architectural relationship from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
