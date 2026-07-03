# Complete Analysis of Video: DevOps Toolchain — Account Signups & Infrastructure Prerequisites

This caption file covers the **foundational setup phase** of a DevOps project pipeline. The instructor walks through creating accounts on **GitHub**, purchasing a **domain via GoDaddy**, creating an account on **Docker Hub**, and signing up for **Sonar Cloud** — establishing the prerequisite service layer before any actual project work begins. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The DevOps Toolchain — Why Multiple Services Exist Before You Write Any Code

Before a single line of application code is written, a DevOps workflow requires an ecosystem of interconnected external services. Each service owns a specific responsibility in the software delivery lifecycle. The video sets up four such services, and understanding **why** each one exists reveals the architecture of a modern DevOps pipeline.

The four services are: **GitHub** (source code management), **a purchased domain** (production identity and routing), **Docker Hub** (container image registry), and **Sonar Cloud** (automated code quality analysis). None of these services operate in isolation — they form a **dependency chain** where code flows from source → analysis → packaging → deployment, and the domain provides the production-facing identity for the deployed application. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

***

## 1.2 GitHub — Source Code Management Platform

GitHub is a cloud-hosted platform for storing, versioning, and collaborating on source code using Git. In this DevOps pipeline, GitHub serves as the **single source of truth** for all project code. Every other service in the toolchain either pulls from GitHub or is triggered by events in GitHub.

The reason GitHub is set up **first** is architectural: it is the origin point of the entire pipeline. Sonar Cloud authenticates through GitHub. CI/CD pipelines (configured later in the course) will trigger on GitHub events like pushes or pull requests. Docker images will be built from code stored in GitHub. Without GitHub, no downstream service has anything to work with. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

The instructor selects the **free plan**, which is sufficient for course-level and most personal projects. GitHub's free tier provides unlimited public and private repositories, which eliminates any cost barrier for learning.

🔍 **Deep Dive**: GitHub also serves as an **identity provider** for other services in this pipeline. When Sonar Cloud is set up later, it uses GitHub OAuth for authentication — meaning your GitHub account becomes a centralized identity across the toolchain. This is an important implicit concept: GitHub is not just a code host; it is an **authentication hub** for the DevOps ecosystem. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

***

## 1.3 Domain Purchase — Why a Paid Domain Is Needed

A domain name (like `hkhinfo.xyz`) is a human-readable address that maps to an IP address where your application is deployed. The instructor explains that a domain is required to perform **real-time or production use cases** — meaning exercises that simulate how applications are deployed and accessed in real production environments. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

Without a domain, you cannot:

* Configure DNS records pointing to your infrastructure
* Set up SSL/TLS certificates for HTTPS
* Simulate production routing, load balancing, or CDN configurations
* Practice real-world deployment workflows that involve domain-based access

The instructor explicitly marks domain purchase as **optional but strongly recommended**. If you skip the domain, you can still complete most of the course, but you will miss the production deployment exercises. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

### 1.3.1 Cost Optimization Strategy for Domain Selection

This is the most operationally valuable concept in this section. The instructor reveals a **cost optimization trick**: domain pricing varies dramatically based on two factors — the **TLD (Top-Level Domain)** extension and the **name popularity**.

* **Common TLDs** like `.com` or `.in` with common names (e.g., `mydevops.com`) are expensive because of high demand.
* **Uncommon TLDs** like `.xyz` with unique/random names (e.g., `hkhinfo.xyz`) are significantly cheaper.

The instructor demonstrates this by searching for `hkhinfo.xyz` on GoDaddy, showing it at **₹169 for one year**. The `.com` variant appears cheaper initially at ₹139, but the instructor warns that the **cart price inflates to \~₹900** due to add-ons and multi-year defaults. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

The key cost traps to avoid:

* **Multi-year auto-selection**: GoDaddy defaults to 5 years; reduce to 1 year
* **Upsell add-ons**: Full domain protection, website builders — none are needed
* **TLD price illusion**: `.com` looks cheaper in search results but costs more at checkout

The instructor selects the **free privacy protection** (which hides your WHOIS registration details) and declines the website builder since the project will deploy its own application. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

⚠️ **Expert Note**: In production environments, `.com` domains carry more trust and brand recognition. But for learning, experimentation, and non-public-facing projects, `.xyz` or similar budget TLDs are functionally identical. The DNS system treats all TLDs equally at the protocol level — the difference is purely economic and perceptual.

***

## 1.4 Docker Hub — Container Image Registry

Docker Hub (`hub.docker.com`) is a cloud-based registry for storing and distributing **Docker container images**. In this DevOps pipeline, after application code is built and packaged into a Docker image, that image is **pushed to Docker Hub** so it can be pulled and deployed onto servers or orchestration platforms. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

The instructor explicitly states the purpose: *"We are going to store our Docker images on this in the Docker projects."* This positions Docker Hub as the **artifact storage layer** — the intermediate station between building an application and deploying it. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

The instructor creates a free account with a username (`kubeimran`) and selects the **free plan**. For learning purposes, the free tier provides sufficient image storage and pull limits.

🔍 **Deep Dive**: Docker Hub functions similarly to GitHub but for a different artifact type. GitHub stores **source code**; Docker Hub stores **built container images**. This separation is architecturally significant: source code and built artifacts have different lifecycles, versioning needs, and access patterns. Keeping them in separate specialized registries is a core DevOps principle — **separation of concerns at the artifact level**.

***

## 1.5 Sonar Cloud — Code Quality Analysis Platform

Sonar Cloud (`sonarcloud.io`) is a cloud-hosted service for **automated static code analysis**. It scans source code for bugs, vulnerabilities, code smells, and maintainability issues without executing the code. In this pipeline, Sonar Cloud acts as a **quality gate** — code that fails quality checks can be blocked from proceeding through the pipeline. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

### 1.5.1 GitHub OAuth Integration — The Authentication Chain

The most architecturally interesting aspect of the Sonar Cloud setup is **how** it is created. The instructor explicitly requires that **GitHub must be logged in first in the same browser**, then navigates to Sonar Cloud and signs up using the **"Sign up with GitHub"** option. This triggers an **OAuth authorization flow** where Sonar Cloud requests permission to access your GitHub account and repositories. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

This is not just a convenience feature — it establishes a **service integration link**. By authorizing Sonar Cloud through GitHub, Sonar Cloud gains the ability to:

* Read your repositories for code analysis
* Post analysis results back to pull requests
* Integrate into CI/CD workflows triggered by GitHub events

The instructor clicks **"Authorize Sonar Cloud"**, completing the OAuth handshake. After authorization, Sonar Cloud automatically configures an **organization and project** linked to the GitHub account. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

⚠️ **Expert Note**: OAuth-based service linking is a common pattern in DevOps toolchains. The important implication is that **revoking GitHub access later will break Sonar Cloud integration**. In production setups, teams often use dedicated service accounts (bot accounts) for these integrations rather than personal accounts, to avoid disruption when team members leave.

***

## 1.6 The Implicit Architecture — How These Services Form a Pipeline

While the video presents these as independent signups, there is a clear **implicit pipeline architecture** connecting all four services:

```
GitHub (Code) → Sonar Cloud (Quality Gate) → Docker Hub (Image Registry) → Domain (Production Access)
```

* **GitHub** holds the source code and triggers pipeline events
* **Sonar Cloud** analyzes code quality (connected to GitHub via OAuth)
* **Docker Hub** stores the built container images
* **Domain** provides the production URL where the deployed application is accessed

This is a classic **CI/CD pipeline structure**: Source → Analyze → Build/Package → Deploy → Serve. The video is setting up the **external service accounts** that this pipeline will use. The pipeline orchestration itself (likely using Jenkins, GitHub Actions, or similar) will be configured in later parts of the course. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up **four prerequisite service accounts** that form the external infrastructure for a DevOps project pipeline. By the end of this process, you will have:

1. A **GitHub** account (code repository)
2. A **purchased domain** (production identity)
3. A **Docker Hub** account (image registry)
4. A **Sonar Cloud** account linked to GitHub (code quality)

These accounts must exist before any project work begins, as every subsequent pipeline step depends on one or more of them. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

***

## Step 1: Create a GitHub Account

**What we are doing**: Registering a free account on GitHub to host project source code.

**Why**: GitHub is the origin point of the pipeline. All other services either pull from or integrate with GitHub.

### Execution:

1. Open your browser and navigate to:
   ```
   https://github.com
   ```
   This is the main GitHub site. Look for the **Sign Up** button. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

2. Fill in the registration form:
   * **Username**: Choose a unique identifier (this becomes your public GitHub identity)
   * **Email address**: Use a valid email you can access immediately (verification required)
   * **Password**: Set a strong password

3. Click **Sign Up**. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

4. Complete the **verification challenge** (e.g., image identification puzzle — the instructor encounters a "Spiral Galaxy" identification). [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

5. When asked about offers/announcements, you can **decline** — these are marketing emails and not required.

6. Select the **Free plan**. The instructor confirms: *"I'm going to go for a free plan and that should be fine for our projects."* [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

7. Fill in the optional profile questions:
   * Work type: Select what applies (instructor selects "Teacher" and "Software Engineer")
   * Programming experience: Select your level
   * Planned use: "Learn Git and GitHub" and "Host project" are relevant selections [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

8. Click **Complete Setup**.

9. **Critical step**: Go to your **email inbox**, find the verification email from GitHub, and **click the verification link**. Your account is not fully active until email is verified. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

**Verification**: After email verification, you should be able to log into `github.com` and see your dashboard. The instructor confirms: *"My email is verified. So that is done."* [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

**Connection to pipeline**: This account will be used for code storage, CI/CD triggers, and as an authentication provider for Sonar Cloud (Step 4).

***

## Step 2: Purchase a Domain on GoDaddy

**What we are doing**: Buying an inexpensive domain name for production deployment exercises.

**Why**: A real domain is needed to simulate production use cases — DNS configuration, SSL, routing, and public access to deployed applications.

### Execution:

1. Navigate to **GoDaddy** (`godaddy.com`). If you don't have an account, create one first (standard signup — fill details, log in). [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

2. In the domain search bar, **search for a unique, uncommon name with a `.xyz` TLD**. The instructor uses:
   ```
   hkhinfo.xyz
   ```
   * **Why `.xyz`?** It's significantly cheaper than `.com` or `.in`
   * **Why a unique name?** Common names have premium pricing due to demand [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

3. Review the search results. You will see prices for different TLDs:
   * `hkhinfo.xyz` → ₹169
   * `hkhinfo.com` → ₹139 (appears cheaper but inflates at checkout to \~₹900)
   Select the **`.xyz` option** and click **"Make it yours"**. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

4. **Reduce the registration period to 1 year**. GoDaddy defaults to 5 years — this is a major cost trap. Change it to 1 year to keep the price at \~₹169. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

5. Click **Continue to Cart**.

6. On the upsell page:
   * **Domain protection**: Select **"Free privacy protection"** (protects your WHOIS info at no cost)
   * **Website builder**: **Decline** — *"We don't need any website from GoDaddy. We will deploy our own website."* [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

7. Click **Continue to Cart** again.

8. **Final price verification checklist** before payment:
   * Registration period = **1 year** (not 5)
   * TLD = **`.xyz`** (not `.com`)
   * No add-ons selected (no full domain protection, no website builder)
   * Price should be approximately **₹169 INR** (or equivalent in your currency) [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

9. Click **"I'm ready to pay"**, fill in payment details, and complete the purchase.

**Common mistakes**:

* Not reducing the year count from 5 to 1
* Selecting `.com` thinking it's cheaper (search price ≠ cart price)
* Accidentally adding upsell products

**If you skip this step**: The instructor explicitly states you can skip domain purchase and the associated production exercises. You can also purchase later when you reach those exercises. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

**Connection to pipeline**: This domain will be used in later sections for DNS configuration pointing to deployed infrastructure (likely AWS-hosted).

***

## Step 3: Create a Docker Hub Account

**What we are doing**: Registering a free account on Docker Hub to store container images.

**Why**: Docker images built from project code need a registry for storage and distribution. Docker Hub serves as this artifact repository.

### Execution:

1. Navigate to Docker Hub:
   ```
   https://hub.docker.com
   ```
   The instructor notes to search for "Docker Hub" if you can't remember the URL. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

2. Click **Sign Up**.

3. Fill in the registration form:
   * **Username**: Choose a Docker-specific identifier (instructor uses `kubeimran`)
   * **Email address**: Valid email for verification
   * **Password**: Set a strong password [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

4. Complete the CAPTCHA ("I'm not a robot") and click **Sign Up**. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

5. When prompted to choose a plan, select the **Free plan**. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

6. Verify your email address from your inbox (similar to GitHub verification). [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

**Verification**: You should be able to log into `hub.docker.com` and see your dashboard. The instructor confirms the account is created and states: *"That's all for now on Docker Hub."* [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

**Connection to pipeline**: Docker images built during CI/CD will be pushed to this registry using `docker push` commands with your Docker Hub username as the namespace.

***

## Step 4: Create a Sonar Cloud Account (via GitHub OAuth)

**What we are doing**: Signing up for Sonar Cloud using GitHub as the authentication provider, establishing a code quality analysis integration.

**Why**: Sonar Cloud will analyze project code for quality issues. Linking it to GitHub allows it to access repositories and integrate with the CI/CD workflow.

### Pre-requisite Check:

**You MUST be logged into your GitHub account in the same browser before starting this step.** The instructor explicitly warns about this: *"Make sure you're logged into your GitHub account in the same browser because we are going to sign up with GitHub account on Sonar Cloud."* [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

### Execution:

1. Open a new tab in the **same browser** where GitHub is logged in.

2. Navigate to:
   ```
   https://sonarcloud.io
   ```
   Or simply Google "Sonar Cloud" to find the link. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

3. Click **Sign Up** (not "Login" — these are different buttons on the page). [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

4. Select **GitHub** as the authentication provider. The instructor notes you can use other providers, but GitHub is preferred since the account already exists and the integration is needed. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

5. Click **"Authorize Sonar Cloud"**. This is the OAuth consent step — you are granting Sonar Cloud permission to access your GitHub account and repositories. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

6. After authorization, Sonar Cloud automatically sets up an **organization and project** linked to your GitHub account. [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

**Verification**: You should land on the Sonar Cloud dashboard with your organization visible. The instructor confirms: *"We have configured the organization and project in Sonar Cloud."* [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

**Common mistake**: Attempting to sign up for Sonar Cloud without being logged into GitHub in the same browser — the OAuth flow will fail or redirect you to GitHub login first, potentially causing confusion.

**Connection to pipeline**: Sonar Cloud will be configured in later project sections to automatically scan code on push/PR events and report quality metrics.

***

## Final State After All Steps

After completing all four steps, your DevOps toolchain prerequisites are: [\[13-signups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/13-signups.txt)

| Service        | Account Type      | Purpose in Pipeline                    | Status                       |
| -------------- | ----------------- | -------------------------------------- | ---------------------------- |
| GitHub         | Free              | Source code management + Auth provider | ✅ Created & verified         |
| GoDaddy Domain | Paid (\~₹169/yr)  | Production DNS identity                | ✅ Purchased (or skipped)     |
| Docker Hub     | Free              | Container image registry               | ✅ Created & verified         |
| Sonar Cloud    | Free (via GitHub) | Code quality analysis                  | ✅ Created & linked to GitHub |

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Pipeline Architecture Chain

```
GitHub ──OAuth──→ Sonar Cloud
  │                    │
  │ (source code)      │ (quality gate)
  ▼                    ▼
CI/CD Pipeline ──build──→ Docker Image ──push──→ Docker Hub
                                                     │
                                                     │ (pull & deploy)
                                                     ▼
                                              Infrastructure (AWS)
                                                     │
                                                     │ (DNS routing)
                                                     ▼
                                                Domain (.xyz)
                                                     │
                                                     ▼
                                              End User Access
```

***

## Service Dependency Map

```
GitHub ← FOUNDATION (set up FIRST)
  ├── Sonar Cloud DEPENDS on GitHub (OAuth auth)
  ├── CI/CD pipelines TRIGGER from GitHub events
  └── Docker builds USE code from GitHub

Domain ← INDEPENDENT (can be done anytime, can be skipped)

Docker Hub ← INDEPENDENT (no dependencies on other accounts)

Sonar Cloud ← DEPENDENT (requires GitHub logged in, same browser)
```

***

## Setup Sequence & Why

```
1. GitHub     → Origin of all code + auth provider for Sonar Cloud
2. Domain     → Independent, but instructor places here logically
3. Docker Hub → Independent, quick setup
4. Sonar Cloud → MUST come after GitHub (OAuth dependency)
```

***

## Cost Optimization Pattern

```
ALL services → Free tier EXCEPT domain

Domain cost trap:
  .com appears cheap (₹139) → inflates to ~₹900 at checkout
  .xyz with unique name      → stays at ~₹169

GoDaddy traps to avoid:
  ├── 5-year default → reduce to 1 year
  ├── Full domain protection upsell → decline (use free privacy)
  └── Website builder upsell → decline (deploy own app)
```

***

## OAuth Integration Pattern (Reusable)

```
Precondition: Service A (GitHub) logged in, same browser
  ↓
Navigate to Service B (Sonar Cloud) → Sign Up
  ↓
Select "Sign up with Service A" → OAuth consent screen
  ↓
"Authorize" → Service B gains read access to Service A resources
  ↓
Auto-configuration: org + project created in Service B

KEY INSIGHT: Service A becomes identity hub + data source
RISK: Revoking Service A access breaks Service B integration
```

***

## Verification Checklist (All Services)

```
GitHub      → Email verified → Can log in to github.com dashboard
Domain      → Payment confirmed → Domain visible in GoDaddy account
Docker Hub  → Email verified → Can log in to hub.docker.com dashboard  
Sonar Cloud → GitHub authorized → Org + project visible in Sonar Cloud dashboard
```

***

## Reusable Engineering Pattern: Prerequisite Infrastructure Layer

```
PATTERN: Before building anything, establish the external service layer

WHY: Modern applications don't run in isolation — they depend on:
  ├── Source control (GitHub)
  ├── Quality gates (Sonar Cloud)
  ├── Artifact registries (Docker Hub)
  ├── DNS identity (Domain)
  └── Cloud infrastructure (AWS — mentioned, set up next)

PRINCIPLE: Service accounts are infrastructure.
           Set them up before writing code, not during deployment.

TRANSFERABLE TO: Any project — Kubernetes clusters, microservices,
                 ML pipelines, mobile app backends
```

***

## Rapid Recall Anchors

| Service     | One-line purpose     | Key detail                                   |
| ----------- | -------------------- | -------------------------------------------- |
| GitHub      | Code lives here      | Set up FIRST — auth hub for others           |
| Domain      | Production URL       | `.xyz` + unique name = cheapest; 1 year only |
| Docker Hub  | Image storage        | `hub.docker.com`; free plan sufficient       |
| Sonar Cloud | Code quality scanner | MUST use GitHub OAuth; same browser required |
