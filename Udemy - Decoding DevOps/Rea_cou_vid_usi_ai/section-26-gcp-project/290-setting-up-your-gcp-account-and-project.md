# 🎓 Deep Learning Material: Setting Up Your GCP Account and Project — Google Cloud Platform Entry Point

**Source:** Video lecture on GCP account setup and project creation (from [290-setting-up-your-gcp-account-and-project.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt?EntityRepresentationId=b9fb7d08-bbf0-4369-be78-3feaa5455d6f) caption file) [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Video Context:** This is an introductory lecture that establishes the Google Cloud Platform environment for a project series. The instructor covers GCP's global infrastructure (regions, zones, edge points), creates a free-tier account with $300 credit, creates a project (`vprofile-project`), navigates the GCP Console, and introduces Cloud Shell with essential `gcloud` commands. This lecture is the GCP equivalent of the "AWS account setup" lecture from earlier in the course — it's a gateway lecture that establishes the platform before any services are used. The content is primarily practical setup, but the infrastructure concepts and the AWS-to-GCP mental mapping provide important theoretical grounding.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What GCP Is: The Same Infrastructure That Powers Google

Google Cloud Platform is **not** a separate infrastructure Google built for customers — it is the **same distributed global infrastructure** that powers Google Search, YouTube, Gmail, and all Google services. The instructor states this directly: *"Google Cloud Platform, also called as GCP in short, is the same distributed global infrastructure that powers Google Search, YouTube, Gmail, and all the Google services."* [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

This is architecturally significant. When you use GCP, you're running on the same network backbone, the same data centers, and the same infrastructure software that handles billions of daily requests for Google's own products. This is Google's core differentiator — the infrastructure was battle-tested at massive scale before it was offered as a cloud service.

***

## 1.2 — GCP Global Infrastructure: Regions, Zones, Edge Points, and Fiber

GCP's infrastructure follows the same hierarchical model as AWS, and the instructor draws a direct parallel: *"Just like AWS, GCP has regions, zones, edge points, and fiber network."* [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Region** — A geographical area containing multiple clustered data centers. The instructor explains: *"A region is a geographical area with multiple clustered data centers."* At the time of recording, GCP had **42 regions**. The instructor selects **`us-central1`** for the project. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Zone** — A clustered data center within a region. *"This clustered data center is called as a zone. So multiple zones together makes a region."* GCP had **127 zones** across its 42 regions. This is the same concept as AWS Availability Zones — isolated failure domains within a region that provide high availability when you distribute resources across them. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Edge Points** — *"GCP also has edge points across the globe to provide low latency to the user."* **200+ network edge locations** existed at the time of recording. These serve the same function as AWS CloudFront edge locations — caching and delivering content closer to end users. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Fiber Network** — *"It's a fiber network that is scattered across the globe. This is Google's private network for connecting its data centers, edge points, zones."* This is Google's proprietary undersea and terrestrial fiber infrastructure that interconnects all its data centers. This private network means traffic between GCP regions and zones doesn't traverse the public internet. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Low CO2 Regions** — Some regions have a green leaf symbol indicating low carbon dioxide emissions. *"This region emits low carbon dioxide, so less carbon footprint."* This is a GCP-specific feature that helps organizations choose environmentally responsible hosting locations. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

> 🔍 **Deep Dive**
>
> The AWS-to-GCP terminology mapping is important for learners coming from the AWS section of the course:
>
> | Concept               | AWS Term           | GCP Term                 |
> | --------------------- | ------------------ | ------------------------ |
> | Geographical cluster  | Region             | Region                   |
> | Isolated data center  | Availability Zone  | Zone                     |
> | Content caching point | Edge Location      | Edge Point               |
> | Private backbone      | AWS Global Network | Google Fiber Network     |
> | CLI tool              | AWS CLI            | GCloud CLI / Cloud Shell |
> | Resource container    | Account            | Project                  |
>
> The structures are architecturally equivalent — the names and some mechanics differ, but the design principles are identical. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## 1.3 — The GCP Free Tier: $300 Credit for Learning

GCP offers a **free tier account** with **$300 in credit** for testing and learning. There is no upfront cost, but a payment method is required. A small verification charge is placed (approximately $1 USD, or ₹2 in India) — this is a **temporary hold** that gets returned. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

The instructor provides a practical warning for Indian users: *"If you're based out in India, do not use UPI. Use debit or credit card. There's no problem in using UPI, but the only thing is you will get scared if it shows 15,000 autopay debit, which will not happen because we are not going to use even the $300 credit also."* [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## 1.4 — Projects: GCP's Resource Organization Model

In AWS, resources are organized by **account** (and optionally by tags, resource groups, or AWS Organizations). In GCP, the fundamental organizational unit is the **project**. A project is a container that holds all your GCP resources — Compute Engine instances, Cloud SQL databases, networking, storage, everything. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

The instructor creates a project named **`vprofile-project`** and explains: *"I'm going to create all the resources in this project. And this makes everything very manageable."* [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

Projects provide: isolation (resources in different projects don't interact by default), billing separation (each project can have its own billing), access control (IAM permissions are scoped to projects), and easy cleanup (deleting a project deletes all its resources). The project dropdown in the Console lets you switch between projects. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## 1.5 — The GCP Console: Navigation Model

The GCP Console (web UI) is accessed at `console.cloud.google.com`. The instructor highlights three navigation methods: [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

1. **Search bar** — Search for services by name (e.g., "Compute Engine", "Cloud SQL")
2. **Navigation menu** (hamburger icon) — Lists the most-used services
3. **View all products** — Shows every GCP service available

The instructor notes: *"We're going to set up everything from the command line."* The Console is for navigation and verification; the actual work in the project will use Cloud Shell. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## 1.6 — Cloud Shell: GCP's Built-In Command Line

**Cloud Shell** is a browser-based command-line environment that comes with GCP — equivalent to having the AWS CLI pre-installed and pre-configured. You access it by clicking the terminal icon in the Console header. It opens directly in the browser (or can be opened in a new window). [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

The key difference from AWS CLI: Cloud Shell runs **in the cloud**, not on your local machine. It's a small VM provided by Google that has the `gcloud` CLI pre-installed. You don't need to install anything locally. However, you **can** also install and use `gcloud` CLI on your local computer — in that case, you need to authenticate with `gcloud auth login`. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## 1.7 — Essential `gcloud` Commands: Authentication and Project Selection

The instructor introduces three critical commands that must be known before using GCP: [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

### `gcloud auth login`

Authenticates you to your GCP account from the CLI. When you run this command, it generates a URL that you must open in a browser where your Google account is logged in. The browser shows a verification code, which you copy and paste back into the terminal. After that, the CLI is authenticated. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

*"If you're running GCloud Shell in your computer from command line and you run gcloud auth login, if you click on this, it's going to open your default browser, and you have to just make sure your default browser, you have logged in with that Google account."* [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

In the browser-based Cloud Shell, you're usually already authenticated (same Google session), but from a local terminal, this step is mandatory.

### `gcloud projects list`

Lists all projects in your GCP account. Shows project names, IDs, and numbers. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

### `gcloud config set project <project-id>`

Sets the active project for all subsequent `gcloud` commands. After running this, the project name appears in the shell prompt, confirming the context. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

*"I'm going to select the project name and paste it there. And then you should see your project name also in the prompt."* [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are setting up a **GCP account, project, and CLI environment** — the foundation for all GCP work in the upcoming project lectures. The final outcome: a GCP account with $300 credit, a project named `vprofile-project`, and a working Cloud Shell authenticated and configured to target that project.

***

## Step 1: View GCP Regions and Zones

Navigate to: `cloud.google.com/about/locations` [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

Browse the global map of regions. Note:

* 42 regions, 127 zones, 200+ edge locations (at time of recording)
* `us-central1` will be used for the project (you can choose another)
* Green leaf icon = low CO2 region [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## Step 2: Create the GCP Account

1. Go to `cloud.google.com` [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
2. Click **Console** (top right) — logs you into GCP Console using your Google account
3. Click **Start free** to activate the free tier [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
4. Select your **country** → **Agree & continue**
5. Fill in: name, address, **payment method** [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Payment notes:**

* No upfront cost — temporary verification hold only (\~$1 USD / ₹2 INR)
* The hold is returned to your account
* **India-specific:** Use debit/credit card, NOT UPI (UPI may show a misleading ₹15,000 autopay authorization that won't actually be charged) [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## Step 3: Create a Project

1. In the GCP Console, you'll see **"My First Project"** (default) [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
2. Click the project dropdown → **New project**
3. Project name: `vprofile-project` [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
4. Click **Create**
5. Select the new project from the dropdown to make it active [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Why a dedicated project:** All resources will be created here — keeps everything organized, easy to manage, and easy to clean up later.

***

## Step 4: Open Cloud Shell

1. In the GCP Console, click the **terminal icon** (top right, near the search bar) [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
2. Click **Continue** → **Authorize** [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
3. A terminal panel opens at the bottom of the browser (or open in a new window for more space)

**What you get:** A pre-configured Linux VM with `gcloud` CLI already installed and authenticated with your Google account. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## Step 5: Authenticate (If Needed)

If using Cloud Shell from the browser, you're likely already authenticated. If using `gcloud` CLI on your local machine:

```bash
gcloud auth login
```

* Generates a URL → open in browser where your Google account is logged in [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
* Browser shows a verification code → copy it
* Paste the code back in the terminal → press Enter
* You're now authenticated

**Common mistake:** Opening the verification URL in a browser where a **different** Google account is logged in → authentication succeeds but for the wrong account. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

## Step 6: List and Select Your Project

**List all projects:**

```bash
gcloud projects list
```

Shows project name, ID, and number. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Set the active project:**

```bash
gcloud config set project <project-id>
```

* Replace `<project-id>` with the project ID from the list output (copy-paste to avoid typos)
* The project name should appear in the shell prompt after this command [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Verification:** The prompt now shows the project name — confirms all subsequent commands target the correct project. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

**Connection to system flow:** With the account, project, and CLI ready, you can now create GCP resources (Compute Engine, Cloud SQL, networking, etc.) in the next lectures. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 GCP Infrastructure Hierarchy

```
GOOGLE'S PRIVATE FIBER NETWORK (global backbone)
  │
  ├── REGIONS (42) — geographical areas
  │     └── ZONES (127) — clustered data centers within regions
  │
  └── EDGE POINTS (200+) — low-latency content delivery
  
Selected for project: us-central1
```

***

## 🔷 AWS → GCP Terminology Map

```
AWS                     GCP
───────────────         ───────────────
Region                  Region
Availability Zone       Zone
Edge Location           Edge Point
AWS CLI                 GCloud CLI / Cloud Shell
Account                 Project (resource container)
aws configure           gcloud auth login + gcloud config set project
CloudFormation          Deployment Manager / Terraform
EC2                     Compute Engine
RDS                     Cloud SQL
S3                      Cloud Storage
```

***

## 🔷 Account Setup Flow

```
1. cloud.google.com → Console → login with Google account
2. Start free → country → payment method → $300 credit activated
3. Create project: vprofile-project
4. Open Cloud Shell (browser terminal icon)
5. gcloud auth login (if local CLI)
6. gcloud projects list → find project ID
7. gcloud config set project <project-id>
8. Prompt shows project name → READY
```

***

## 🔷 Three Essential gcloud Commands

```bash
gcloud auth login              # authenticate to GCP account
                               # generates URL → browser → verification code → paste

gcloud projects list           # list all projects (name, ID, number)

gcloud config set project <id> # set active project for all commands
                               # prompt shows project name after this
```

***

## 🔷 Cloud Shell vs. Local CLI

```
CLOUD SHELL (browser):
  ✅ Pre-installed gcloud
  ✅ Pre-authenticated (same Google session)
  ✅ No local setup needed
  ❌ Ephemeral VM (files may not persist long-term)

LOCAL CLI (your machine):
  ✅ Persistent environment
  ✅ Can use your own tools alongside
  ❌ Must install gcloud SDK
  ❌ Must run gcloud auth login manually
  ❌ Must ensure correct browser/account for auth
```

***

## 🔷 GCP Console Navigation

```
TOP BAR:
  ├── Search bar → search any service by name
  ├── Project dropdown → switch projects
  └── Cloud Shell icon → open terminal

LEFT MENU (hamburger):
  ├── Most used services (pinned)
  └── View all products → complete service catalog

SERVICES TO KNOW:
  Compute Engine = VMs (like EC2)
  Cloud SQL = managed databases (like RDS)
  + many more explored in project lectures
```

***

## 🔷 Free Tier Details

```
CREDIT:     $300 (for testing/learning)
COST:       $0 upfront
HOLD:       ~$1 USD / ₹2 INR (temporary, returned)
PAYMENT:    Credit/debit card required

INDIA WARNING:
  UPI → may show ₹15,000 autopay (misleading, won't charge)
  USE → debit/credit card instead
```

***

## 🔷 Project = GCP's Organizational Unit

```
PROJECT:
  ├── Contains ALL resources (VMs, databases, networks, storage)
  ├── Provides isolation between workloads
  ├── Scopes IAM permissions
  ├── Scopes billing
  └── Easy cleanup: delete project = delete everything

Name chosen: vprofile-project
All project resources will be created here.
```

***

## 🔷 Reusable Engineering Pattern: Platform Entry Point Setup

```
PATTERN: Account → Container → CLI → Verify → Build

STEP              AWS                         GCP
────────          ─────────────────           ─────────────────
1. Account        AWS Account                 Google Cloud Account
2. Container      (account-level / tags)      Project
3. CLI            aws configure               gcloud auth login + config set project
4. Verify         aws sts get-caller-identity gcloud projects list
5. Build          Create resources            Create resources

This pattern applies to EVERY cloud platform:
  Azure: Account → Subscription → Resource Group → az login
  GCP:   Account → Project → gcloud config set project
  AWS:   Account → (region) → aws configure

The setup sequence is always:
  authenticate → select scope → verify → start building

Once this pattern is internalized, entering any new cloud
platform becomes a mechanical process:
  "How do I auth? What's the resource container? What's the CLI?"
```

This is a gateway lecture — minimal technical depth, but it establishes the entire platform context for everything that follows. The key takeaway is the **AWS-to-GCP mental mapping**: same concepts, different names, same infrastructure patterns underneath. [\[290-settin...nd-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/290-setting-up-your-gcp-account-and-project.txt)
