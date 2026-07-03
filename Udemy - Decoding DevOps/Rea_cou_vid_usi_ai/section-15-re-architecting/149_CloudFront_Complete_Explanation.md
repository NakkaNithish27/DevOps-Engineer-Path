# 🧠 AWS CloudFront — Content Delivery Network for Global Application Distribution

**Source:** *149. CloudFront* — vProfile Application Cloud Deployment Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Core Problem: Geographic Latency for Globally Distributed Users

The vProfile application is hosted in the **North Virginia (us-east-1)** AWS region, which is physically located in the United States. Users in the US access the website quickly because their requests travel a short network distance to the servers. But users on other continents — Asia, Europe, Africa — experience significantly slower access because their HTTP requests must travel across the globe, pass through many network hops, and the round-trip latency adds up for every page load, every image, every API call.

The naive solution would be: "deploy copies of the entire website infrastructure around the world." But this is wildly impractical — it would mean running duplicate load balancers, application servers, databases, and caching layers in every region where you want fast access. The cost, operational complexity, and data synchronization challenges would be enormous. The instructor explicitly rejects this: *"Do we create our website around the world? No, we don't need to do that."*

Instead, the solution is a **Content Delivery Network (CDN)** — a globally distributed network of caching servers that store copies of your content close to users everywhere, without duplicating your actual infrastructure.

***

## 1.2 Content Delivery Network (CDN) — The Concept

A CDN is a system of geographically distributed servers — called **edge locations** — that **cache** your website's content and serve it to users from the location nearest to them. The original infrastructure (your load balancer, application servers, database) stays in one region. The CDN's edge locations around the world pull content from your origin, cache it locally, and serve it to nearby users.

When a user in Asia requests your website, instead of their request traveling all the way to North Virginia, it hits the nearest CDN edge location — perhaps in Mumbai or Singapore. If that edge location already has the cached content, it serves it immediately with very low latency. If it doesn't have the content yet, it fetches it from the origin (your load balancer in North Virginia), caches it, and then serves it. Subsequent users in that region get the cached version directly.

The result: **low latency and high transfer speeds** for users everywhere in the world, without deploying your infrastructure in multiple regions.

***

## 1.3 AWS CloudFront — The CDN Service

AWS's CDN service is called **CloudFront**. The instructor provides concrete scale numbers: AWS has **more than 30 regions**, **more than 100 availability zones**, and — critically — **more than 600 CloudFront edge locations**. The edge location count is far higher than the region count because CDN nodes need to be everywhere users are, not just where you deploy infrastructure.

Regions and availability zones are where you **create services** (EC2 instances, RDS databases, load balancers). CloudFront edge locations are where you **distribute content**. These are two fundamentally different layers of the AWS infrastructure: the compute/service layer and the distribution/caching layer.

CloudFront's value proposition, as described by the instructor: *"You see that it's that easy and you get access to AWS global edge locations around the world. Imagine doing that all by yourself. The amount of money, time it will take."* CloudFront abstracts away the enormous operational complexity of running a global content distribution network.

> 🔍 **Deep Dive:** CloudFront is not just a cache — it also provides **secure delivery**. The instructor's description states it "securely delivers content with low latency and high transfer speeds." This means CloudFront handles TLS termination at edge locations, integrates with ACM (AWS Certificate Manager) for SSL certificates, and can enforce HTTPS — all at the edge, before traffic even reaches your origin.

***

## 1.4 The Architecture Shift: URL → Load Balancer to URL → CloudFront → Load Balancer

Before CloudFront, the vProfile application's URL pointed directly to the **Beanstalk load balancer endpoint**. The DNS resolution chain was: `vpro.yourdomain.com → load balancer DNS name → load balancer IP → application servers`. Every request from every user, anywhere in the world, went directly to the load balancer in North Virginia.

After CloudFront, the architecture changes to: `vpro.yourdomain.com → CloudFront distribution → (edge location serves cached content OR forwards to load balancer origin)`. The DNS entry for the domain is changed from pointing to the load balancer to pointing to the **CloudFront distribution domain name**. The load balancer becomes the **origin** — the source that CloudFront pulls content from — rather than the direct point of contact for end users.

This is an important architectural shift: the load balancer doesn't disappear. It still runs and serves the application. But it's no longer the public-facing endpoint. CloudFront sits in front of it, absorbing the global traffic, caching what it can, and only forwarding to the origin what it must.

The practical implication: the existing DNS entry in the domain registrar (GoDaddy) that pointed to the load balancer must be **removed** and **replaced** with a CNAME entry pointing to the CloudFront distribution.

***

## 1.5 CloudFront Distribution — The Core Resource

The primary resource you create in CloudFront is called a **distribution**. A distribution is a configuration object that defines: where content comes from (the **origin**), how it's cached, what protocols are supported, what domain names are associated with it, and what security settings apply.

When you create a distribution, AWS deploys your configuration across all 600+ edge locations worldwide. This deployment takes time — the instructor notes it takes **5–10 minutes** for the distribution to move from "Deploying" state to fully available. During deployment, AWS is propagating your configuration globally.

**Distribution type:** For the vProfile project, the distribution type is set for a **single website or app** — the simplest configuration where one distribution serves one application.

***

## 1.6 Origin Configuration — Where CloudFront Fetches Content From

The **origin** is the source server (or service) from which CloudFront fetches content when it doesn't have a cached copy. For vProfile, the origin is the **Elastic Load Balancer** from the Beanstalk environment — specifically the **Application Load Balancer (ALB)**.

When configuring the origin, you select the load balancer from a browser/picker in the AWS console. Two things must be correct: the **region** must match where your load balancer actually exists, and the **ELB version** must be correct (Application Load Balancer in this case, since that's what Beanstalk provisions).

**Origin Path** is an optional field that appends a sub-path to the origin URL. If your application is served from a specific path (like `/app` or `/login`), you'd specify it here. For vProfile, the load balancer serves the website directly at the root, so origin path is left **blank**.

**Origin settings:** The instructor selects **Customize Origin settings**, which allows manual control over how CloudFront communicates with the origin.

***

## 1.7 Protocol Policy — How CloudFront Talks to Viewers and Origin

CloudFront handles two distinct traffic legs: **viewer-to-edge** (the user's browser to the nearest edge location) and **edge-to-origin** (the edge location to your load balancer). The protocol policy controls which protocols are used.

The instructor selects **Match viewer** for the origin protocol — meaning CloudFront will use the same protocol to talk to the origin that the viewer used to talk to the edge. If a user requests via HTTP, CloudFront fetches from origin via HTTP. If via HTTPS, it fetches via HTTPS.

The default ports are standard: **HTTP port 80** and **HTTPS port 443**. The instructor notes these are the standard ports and only need changing if your origin uses non-standard ports for specific security or architectural reasons.

***

## 1.8 Cache Settings and Viewer Protocol Policy

CDN's fundamental purpose is **caching regularly visited pages**. The cache settings control what gets cached, for how long, and under what conditions cached content is considered stale. The instructor keeps **default cache settings** for this project, noting that defaults work most of the time.

Within the customizable cache settings, the **viewer protocol policy** offers three options:

1. **HTTP and HTTPS both** — accepts both protocols from viewers (selected for this project, though the instructor notes HTTPS-only is generally recommended)
2. **Redirect HTTP to HTTPS** — if a user accesses via HTTP, automatically redirect them to HTTPS
3. **HTTPS only** — reject HTTP connections entirely

The instructor selects **HTTP and HTTPS both** for this project, while explicitly noting that **HTTPS is the recommended approach** for most production scenarios.

**Allowed HTTP methods** are set to include **all methods**: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE. This is important because the vProfile application isn't just serving static content — it's a dynamic web application that uses various HTTP methods for API interactions. Restricting to GET/HEAD only would break any form submissions, API calls, or state-changing operations.

> ⚠️ **Expert Note:** CloudFront and CDN settings are extensive — the instructor acknowledges there are "seriously many, many more settings." In real organizations, CDN configuration is typically managed by a **dedicated network team**. As a DevOps engineer, you should understand the concepts well enough to "interact with the network team and make the right decision in the automation" — you don't need to be the CDN expert, but you need to speak the language and understand the architecture.

***

## 1.9 WAF — Web Application Firewall (Application-Level Security)

The CloudFront creation flow presents an option to enable **WAF (Web Application Firewall)**. The instructor draws a critical distinction: the firewalls discussed so far in the course (security groups) are **network-level firewalls** — they operate at the port/IP level, controlling which traffic can reach a resource based on protocol, port, and source IP.

WAF is fundamentally different. It's an **application-level firewall** that inspects the *content* of HTTP requests. It blocks common web vulnerabilities and attacks like **SQL injection** (malicious database queries embedded in form inputs) and **DDoS attacks** (overwhelming the application with massive volumes of requests).

The instructor's recommendation is clear: *"A publicly hosted website should definitely have a web application firewall."* AWS WAF integrates directly with CloudFront, meaning it can inspect and filter malicious traffic at the edge — before it even reaches your origin infrastructure. However, WAF is **not free**, and for this learning project, it's not enabled.

> 🔍 **Deep Dive:** WAF at the CloudFront level is strategically powerful because it filters malicious traffic at the **600+ edge locations**, before it consumes bandwidth or processing power at your origin. This is far more effective than running a WAF only at the origin, because DDoS traffic would still saturate your origin's network even if the WAF blocks it at the application layer. Edge-level filtering is the preferred architecture for web application security at scale.

***

## 1.10 Domain Association and SSL Certificate — Connecting Your Domain to CloudFront

After creating the distribution, you associate your **custom domain name** with it. The instructor goes to the distribution's General settings → **Add domain**, and enters the hostname (e.g., `vpro.infotech.xyz`).

During this process, CloudFront requires an **SSL certificate** from **ACM (AWS Certificate Manager)** that matches the domain being added. The instructor notes this certificate was "created earlier in prerequisites." The critical validation: the domain name on the certificate **must match** the domain name you're adding to CloudFront. If they don't match, CloudFront cannot serve HTTPS traffic for that domain, and the association won't work.

This is the CNAME record that will be created in the domain registrar — the same hostname given as the alternate domain name in CloudFront is what you'll point via CNAME to the CloudFront distribution.

***

## 1.11 DNS Reconfiguration — Pointing the Domain to CloudFront

The final architectural step is updating DNS at the domain registrar (GoDaddy in this case). The existing DNS entry that pointed the domain directly to the Beanstalk load balancer must be **removed**. A new **CNAME record** is created:

* **Type:** CNAME (name-to-name mapping)
* **Name:** The hostname portion (e.g., `vpro`)
* **Value:** The CloudFront **distribution domain name** (the auto-generated `.cloudfront.net` URL from the distribution)

The instructor specifically warns: when pasting the CloudFront distribution domain name, **remove the `https://` prefix** — only the hostname portion should go into the CNAME value field.

After this DNS change, the resolution chain becomes: `vpro.yourdomain.com → (CNAME) → xxxx.cloudfront.net → (nearest edge location) → cached content or fetch from origin (ALB)`.

> ⚠️ **Expert Note:** DNS propagation takes time — the CNAME change won't be instant globally. Combined with the CloudFront distribution deployment time (5–10 minutes), there's a window where the site may be intermittently accessible. In production, this transition should be planned during a maintenance window or done with careful TTL management on the old DNS record before the switchover.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are placing **AWS CloudFront** — a global CDN — in front of the vProfile application's load balancer. Instead of users worldwide hitting the load balancer in North Virginia directly, their requests will be served by the nearest CloudFront edge location. The domain's DNS will be updated to point to the CloudFront distribution instead of the load balancer.

**Final outcome:** `vpro.yourdomain.com` → CloudFront distribution → (edge-cached content or origin fetch from ALB) → global low-latency access. The application infrastructure stays in one region; CloudFront distributes it globally.

***

## Step 1: Remove the Existing DNS Entry in GoDaddy

Go to your **GoDaddy account** (or whatever domain registrar you use). Find and **remove** the existing DNS record that points your domain (e.g., `vpro.yourdomain.com`) directly to the Beanstalk load balancer endpoint.

**Why:** We're replacing the direct load-balancer-pointing entry with a CloudFront-pointing entry. The old entry must be removed to avoid conflicts.

**Connection to flow:** This clears the DNS path for the new CloudFront CNAME we'll create at the end.

***

## Step 2: Navigate to CloudFront and Begin Creating a Distribution

In the **AWS Management Console**, search for **CloudFront** and open it (in a new tab for convenience).

Click **Create distribution**.

***

## Step 3: Configure Distribution Name and Type

| Field                 | Value                    | Reasoning                                             |
| --------------------- | ------------------------ | ----------------------------------------------------- |
| **Name**              | `vprofile-<description>` | Use a project-meaningful name for easy identification |
| **Description**       | Same descriptive text    | Helps identify the distribution in the console        |
| **Distribution type** | Single website or app    | vProfile is a single application                      |

***

## Step 4: Skip Domain Setup (For Now)

The form asks for a **domain name** (e.g., `vpro.yourdomain.com`). You can enter it, but the instructor notes this setting will be configured **later** after the distribution is created. The form will attempt to validate the domain, and you can click **Skip domain setup** to proceed without configuring it now.

**Why later:** The domain association requires the distribution to exist first, and the ACM certificate validation is easier to handle as a separate step.

***

## Step 5: Configure the Origin (Load Balancer)

This is where you tell CloudFront where to fetch content from.

| Field               | Value                                                      | Reasoning                                                                                       |
| ------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Origin type**     | **Elastic Load Balancer**                                  | The ALB from Beanstalk is the origin                                                            |
| **Load balancer**   | Click **Browse load balancer** → select your Beanstalk ALB | Make sure the **region is correct** and the **ELB version** matches (Application Load Balancer) |
| **Origin Path**     | **Leave blank**                                            | The load balancer serves the site at the root path; no sub-path needed                          |
| **Origin settings** | **Customize Origin settings**                              | Allows manual control over origin communication                                                 |

**Verification:** Confirm the selected load balancer is the correct one from your Beanstalk environment. Wrong load balancer = CloudFront fetches content from the wrong application.

***

## Step 6: Configure Protocol and Port Settings

| Field                      | Value            | Reasoning                                                                      |
| -------------------------- | ---------------- | ------------------------------------------------------------------------------ |
| **Origin protocol policy** | **Match viewer** | CloudFront uses same protocol as the viewer's request (HTTP→HTTP, HTTPS→HTTPS) |
| **HTTP port**              | `80`             | Standard HTTP port (default)                                                   |
| **HTTPS port**             | `443`            | Standard HTTPS port (default)                                                  |

Keep default **timeout settings** as-is.

**Common mistake:** Changing ports here when your origin uses standard ports. Only change these if your load balancer listens on non-standard ports.

***

## Step 7: Configure Cache and Viewer Settings

Start with **default cache settings**. Then select **Customize cache settings** to access protocol and method options:

| Field                      | Value                                                  | Reasoning                                                                                                |
| -------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| **Viewer protocol policy** | **HTTP and HTTPS**                                     | Accept both protocols (instructor notes HTTPS-only is recommended for production, but selects both here) |
| **Allowed HTTP methods**   | **All** (GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE) | vProfile is a dynamic app using multiple HTTP methods for forms, API calls, etc.                         |

Click **Next**.

> ⚠️ **Expert Note:** Restricting to GET/HEAD would break any dynamic functionality (form submissions, login, data updates). Always match allowed methods to your application's actual needs.

***

## Step 8: WAF (Web Application Firewall) Decision

The next screen presents the option to enable **WAF**.

| Field   | Value             | Reasoning                                        |
| ------- | ----------------- | ------------------------------------------------ |
| **WAF** | **Do not enable** | Not free; not required for this learning project |

The instructor recommends understanding WAF conceptually (application-level firewall blocking SQL injection, DDoS — see Theory §1.9) even though we're not enabling it here.

Click **Next**.

***

## Step 9: Review and Create the Distribution

Review all selected settings. If anything is wrong, go back and correct it.

Click **Create distribution**.

**What happens:** The distribution enters **"Deploying"** state. AWS is propagating your configuration to 600+ edge locations worldwide. This takes **5–10 minutes** (the instructor suggests taking a break during this time).

**Verification:** Wait until the status changes from "Deploying" to **"Enabled"** / fully available.

***

## Step 10: Add the Custom Domain to the Distribution

Once the distribution exists (even while still deploying), go to the distribution's **General** settings and click **Add domain**.

| Field           | Value                                             |
| --------------- | ------------------------------------------------- |
| **Domain name** | `vpro.yourdomain.com` (e.g., `vpro.infotech.xyz`) |

Click **Next**.

The form should show your **ACM certificate** (created in a previous prerequisite step). **Critical validation:** The domain on the certificate **must match** the domain you're adding. If they don't match, HTTPS won't work and the association will fail.

Click **Next** → **Add domain**.

**Connection to flow:** The distribution now knows it serves content for `vpro.yourdomain.com`. Next, DNS must point that domain to this distribution.

***

## Step 11: Create the CNAME Record in GoDaddy

Go to your **GoDaddy account** (or domain registrar). Click **Add new record**.

| Field     | Value                               | Notes                                                                                                                                |
| --------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Type**  | **CNAME**                           | Name-to-name mapping (see Theory §1.11)                                                                                              |
| **Name**  | `vpro`                              | The hostname portion — must match the alternate domain name added in CloudFront                                                      |
| **Value** | CloudFront distribution domain name | Copy from the CloudFront console. ⚠️ **Remove the `https://` prefix** — paste only the hostname (e.g., `d1234abcdef.cloudfront.net`) |

Click **Save**.

**Where to find the distribution domain name:** In the CloudFront console → your distribution → the **Distribution domain name** field shows the auto-generated `.cloudfront.net` URL.

**Common mistakes:**

| Mistake                                                        | Consequence                                                     | Fix                                                                     |
| -------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Left `https://` in CNAME value                                 | DNS resolution fails — CNAME values must be hostnames, not URLs | Remove the protocol prefix                                              |
| Hostname in CNAME doesn't match alternate domain in CloudFront | Certificate mismatch, HTTPS errors                              | Ensure exact match between GoDaddy name and CloudFront alternate domain |
| Old load balancer DNS entry still exists                       | DNS conflict or users hit LB directly instead of CloudFront     | Verify the old entry was removed in Step 1                              |
| ACM certificate domain doesn't match                           | HTTPS will not work; browsers show certificate errors           | Use the correct certificate that covers the exact domain                |

**Post-creation:** The CNAME takes some time for DNS propagation. Combined with the distribution deployment time, allow **5–10+ minutes** before testing.

**Final verification:** After the distribution status shows fully available and DNS has propagated, accessing `vpro.yourdomain.com` in a browser should load the vProfile application — now served through CloudFront's global edge network.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture Shift

```
BEFORE CloudFront:
  User (anywhere) → DNS → Load Balancer (N. Virginia) → App Servers
  Problem: High latency for non-US users

AFTER CloudFront:
  User (anywhere) → DNS → CloudFront Edge (nearest of 600+) → Cached content
                                    │ (cache miss)
                                    └──→ Load Balancer (N. Virginia) → App Servers
  Result: Low latency globally, origin only hit on cache misses
```

***

## AWS Infrastructure Scale Context

```
Regions:               30+    (where you CREATE services)
Availability Zones:   100+    (fault isolation within regions)
CloudFront Locations: 600+    (where you DISTRIBUTE content)
```

***

## CloudFront Distribution — Resource Structure

```
CloudFront Distribution
  ├── Name: vprofile-<desc>
  ├── Type: Single website/app
  │
  ├── ORIGIN
  │     ├── Type: Elastic Load Balancer (ALB from Beanstalk)
  │     ├── Region: must match LB region
  │     ├── Origin Path: blank (root-level serving)
  │     └── Settings: Customize Origin
  │
  ├── PROTOCOL
  │     ├── Origin policy: Match viewer
  │     ├── HTTP: 80 │ HTTPS: 443 (defaults)
  │     └── Viewer policy: HTTP and HTTPS both
  │
  ├── CACHE
  │     ├── Settings: Default
  │     └── HTTP methods: ALL (GET/HEAD/OPTIONS/PUT/POST/PATCH/DELETE)
  │
  ├── SECURITY
  │     └── WAF: Not enabled (not free; recommended for production)
  │
  ├── DOMAIN
  │     ├── Alternate domain: vpro.yourdomain.com
  │     └── ACM certificate: must match domain exactly
  │
  └── STATUS: Deploying → Available (5-10 min)
```

***

## DNS Reconfiguration Flow

```
1. GoDaddy: REMOVE old record (domain → load balancer)

2. CloudFront: Create distribution → get distribution domain name
     (e.g., d1234abcdef.cloudfront.net)

3. CloudFront: Add domain → vpro.yourdomain.com → verify ACM cert match

4. GoDaddy: ADD new CNAME record
     Name:  vpro
     Value: d1234abcdef.cloudfront.net  (⚠️ NO https:// prefix)

RESULT:
  vpro.yourdomain.com → CNAME → d1234abcdef.cloudfront.net → nearest edge → origin (ALB)
```

***

## Two Firewall Layers (Conceptual Distinction)

```
Security Groups (already configured):
  Layer:   NETWORK level
  Scope:   Port + IP filtering
  Where:   On individual AWS resources

WAF (Web Application Firewall):
  Layer:   APPLICATION level
  Scope:   HTTP request content inspection
  Blocks:  SQL injection, DDoS, common web attacks
  Where:   At CloudFront edge (before traffic reaches origin)
  Cost:    Not free
  Rule:    Publicly hosted websites SHOULD have WAF
```

***

## Decision Map

| Decision                                | Choice                      | Reason                                               |
| --------------------------------------- | --------------------------- | ---------------------------------------------------- |
| Distribute globally vs. deploy globally | **Distribute via CDN**      | Vastly cheaper, simpler than multi-region deployment |
| Origin                                  | ALB (Beanstalk)             | Existing app infrastructure serves as content source |
| Origin path                             | Blank                       | App served at root                                   |
| Origin protocol                         | Match viewer                | Mirror viewer's protocol choice to origin            |
| Viewer protocol                         | HTTP + HTTPS both           | Flexibility (HTTPS-only recommended for prod)        |
| HTTP methods                            | All                         | Dynamic app needs POST, PUT, DELETE etc.             |
| WAF                                     | Disabled                    | Not free; learning project                           |
| Domain association                      | After distribution creation | Requires distribution to exist first                 |
| DNS record type                         | CNAME                       | Name→name mapping (domain → CloudFront hostname)     |

***

## Execution Sequence (Compressed)

```
1. GoDaddy → remove old LB-pointing DNS record

2. AWS Console → CloudFront → Create Distribution
     type: single site │ origin: ALB (Beanstalk)
     origin path: blank │ protocol: match viewer
     ports: 80/443 │ cache: default │ methods: ALL
     WAF: skip │ Review → Create
     → Wait 5-10 min (Deploying → Available)

3. Distribution → General → Add Domain
     hostname: vpro.yourdomain.com
     verify ACM cert match → Add domain

4. Copy distribution domain name (remove https://)

5. GoDaddy → Add CNAME record
     name: vpro │ value: <distribution-domain>.cloudfront.net
     Save → wait for DNS propagation
```

***

## Failure Signature Index

```
Site not loading after switch         → distribution still "Deploying" OR DNS not propagated yet
HTTPS certificate error in browser    → ACM cert domain ≠ CloudFront alternate domain
DNS not resolving                     → CNAME value contains "https://" prefix (must be hostname only)
Old site still showing                → old DNS record not removed; cached DNS
Dynamic features broken (forms, API)  → HTTP methods restricted to GET/HEAD only
Origin fetch failing                  → wrong LB selected, or wrong region
High latency persisting               → distribution not yet fully deployed to all edges
```

***

## Reusable Engineering Pattern: Edge Distribution Layer

```
PATTERN:
  Application infrastructure stays CENTRALIZED (one region)
  Distribution layer DECENTRALIZED (global edge network)
  Edge caches content → serves locally → fetches from origin on miss

WHY:
  Deploying infra globally = massive cost + operational complexity
  Distributing content globally = managed service, 600+ locations, minutes to set up

COMPONENTS:
  Origin (stable, centralized)     →  your ALB / app servers
  Edge (distributed, ephemeral)    →  CloudFront locations worldwide
  DNS (routing layer)              →  CNAME pointing domain to CDN

WHERE ELSE:
  • Cloudflare CDN
  • Akamai
  • Azure Front Door / CDN
  • Google Cloud CDN
  • Any static asset delivery (S3 + CloudFront)
```

***

## Reusable Pattern: Layered Security Architecture

```
LAYER 1: Security Groups     → network/port level filtering (already in place)
LAYER 2: WAF at CDN edge     → application-level request inspection (optional, recommended)

Security groups block unauthorized NETWORK access.
WAF blocks malicious APPLICATION traffic (SQL injection, DDoS).

Both layers complement each other — they don't replace each other.
```

***

## One-Line Mental Reload Trigger

> *"CloudFront distribution: origin = ALB, 600+ edges cache content globally, CNAME domain → distribution hostname, ACM cert must match domain, WAF optional but recommended — remove old DNS, create new CNAME without https\:// prefix."*

This single sentence reconstructs the entire architecture, origin chain, DNS setup, certificate requirement, security layer, and the most common mistake. [\[149. Cloud front \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/149.%20Cloud%20front.txt)
