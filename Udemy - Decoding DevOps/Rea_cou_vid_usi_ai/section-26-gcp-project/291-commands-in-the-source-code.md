# 🎓 GCP V-Profile Project: Navigating Source Code & Variable Setup — Deep Learning Material

**Source:** Video caption file — *Commands in the Source Code (GCP V-Profile Project Preparation)* [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Project Structure: Four-Part Infrastructure Deployment

The V-Profile project on GCP is structured into **four sequential execution phases**, each represented as a separate script file in the repository. This decomposition reflects how a real multi-tier application is built on cloud infrastructure — you build from the foundation upward: [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

1. **VPC** — The network foundation. Creates the Virtual Private Cloud, subnets, and firewall rules. Nothing else can exist without the network.
2. **Backend** — The data/application tier. Deploys backend services (databases, application servers) into the network.
3. **Frontend Part 1** — The first half of the web-facing tier.
4. **Frontend Part 2** — The second half of the web-facing tier, completing the public-facing setup.

This ordering is not arbitrary — it follows a strict **dependency chain**. The VPC must exist before any instances can be created inside it. Backend services must be running before the frontend can connect to them. Each phase depends on the output of the previous phase. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

> 🔍 **Deep Dive:** This four-part structure mirrors the architectural layers of the V-Profile application itself. The project was previously deployed on AWS (earlier in the course) and on local VMs (with Vagrant). Now it's being deployed on GCP — demonstrating that the same application architecture (network → backend → frontend) applies regardless of the cloud provider. The **concepts transfer**; only the **commands change** (AWS CLI → gcloud CLI, Security Groups → Firewall Rules, Key Pairs → injected SSH keys).

***

## 1.2 — The Repository and Branch Strategy

The project code lives in a **GitHub repository**: `github.com/vprofile-project`. The repository contains multiple branches for different deployment targets. The GCP-specific code lives on the **GCP branch** — not the main/default branch. This is a common pattern in multi-environment projects: one repository, multiple branches for different infrastructure targets (AWS, GCP, Azure, local, etc.). [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

The repository is cloned using VS Code's built-in **Source Control** feature. After cloning, you switch to the GCP branch to access the GCP-specific scripts and variables.

***

## 1.3 — Variables: The Consistency and Safety Mechanism

Every script in the project uses **variables** instead of hardcoded values for project-specific information (project ID, region, names, passwords, IPs). The instructor explains the engineering reasoning behind this choice explicitly: "The only reason I am using variables is because you and me, we both can execute the same commands. Otherwise, there is a huge chance of making mistakes while you execute the commands." [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

This is the **variable adapter pattern** seen throughout the course (Bash scripting multi-OS scripts, Terraform variables, etc.) — but applied at the infrastructure-as-code level. You set the variable values once at the top, and every command below uses those variables. If two people set different values (different project IDs, different regions), they can both run the **exact same commands** and get correctly personalized results.

***

## 1.4 — Key Variables and What They Control

### `PROJECT_ID` — Your GCP Project Identifier

Every GCP resource belongs to a **project**. The project ID is the unique identifier for your GCP project. This is analogous to an AWS account — it's the organizational boundary within which all resources are created. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### `REGION` — Geographic Deployment Target

The GCP region where resources will be created (e.g., `us-central1`). Same concept as AWS regions (`us-east-1`), same purpose — determines which data center(s) host your infrastructure. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### `APP_NAME` — Application Identifier

Set to `vprofile`. Used as a naming prefix throughout all resource names for consistent identification and filtering.

### `DOMAIN` — The Public URL

If you have a purchased domain, you set it here for production-style HTTPS access. If not, you can use a fake domain name. The instructor demonstrates using a subdomain: `vpro.gcp.info.xyz`. This variable defines the **final public URL** of the deployed website. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### `MY_IP` — Firewall Source Restriction

This is the equivalent of **"My IP"** in AWS Security Group rules. It restricts SSH access to your public IP address. Initially set to `0.0.0.0/0` (anywhere) for convenience, but will be edited later to your actual public IP for proper security. The instructor explicitly draws the AWS parallel: "Like in AWS Security Group we mentioned there, SSH from my IP — here we are going to do the same thing." [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### `SSH_KEY` — Public Key Content

This variable holds the **content of your public SSH key** — not a key pair name, but the actual key data. This is a significant difference from AWS (covered in Section 1.5 below). [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### `DB_PASSWORD` — Database Credential

The database password. The instructor recommends keeping the **same value as in the source code** to avoid needing to also edit the `application.properties` file. If you change this password, you must **also update** the application configuration file — otherwise the application can't authenticate to the database. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

> ⚠️ **Expert Note:** The coupling between `DB_PASSWORD` variable and `application.properties` is a common source of deployment failures. This is a configuration consistency problem — when the same credential must exist in two places (infrastructure provisioning and application configuration), any mismatch causes authentication failures that can be difficult to diagnose. In production, this is solved with secrets management (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault) where both the infrastructure and the application read the credential from a single source of truth. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## 1.5 — GCP vs AWS: SSH Key Handling — A Critical Difference

This is one of the most important conceptual points in the lecture. In **AWS**, when you launch an EC2 instance, you **create a key pair in AWS**, AWS stores the public key, and you **download the private key**. The key pair is a named AWS resource that you attach to instances at launch time. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

In **GCP**, there is **no such concept of creating key pairs as a service-level resource**. The instructor states directly: "In GCP, that's not the case. There is no such option of creating key pairs." Instead, you must: [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

1. **Generate a key pair yourself** (on your local machine, before or during launch).
2. **Inject the public key into the instance** at launch time (via metadata or startup script).
3. **Use the private key** to SSH into the instance.

This means the SSH key variable must contain the **actual public key content** — not a reference to a key stored in the cloud. The responsibility for key generation and management shifts from the cloud provider to **you**.

> 🔍 **Deep Dive:** This difference reflects a philosophical distinction between the two clouds. AWS provides a managed key pair service (convenient but vendor-locked). GCP follows the standard Linux/SSH model (you manage your own keys, same as any Linux server). Neither approach is objectively better — AWS is more convenient for beginners, GCP gives you more control and follows open standards more closely. Understanding both models means you can work on either platform.

***

## 1.6 — The `gcloud` CLI: GCP's Command-Line Interface

All infrastructure in this project is created using **`gcloud` commands** — GCP's command-line interface. This is the GCP equivalent of the AWS CLI. The execution flow visible in the scripts follows a logical infrastructure build sequence: [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

1. `gcloud` **set the project** — Tell the CLI which GCP project to operate in.
2. `gcloud` **enable APIs** — Activate the GCP services needed (Compute Engine, etc.). GCP requires you to explicitly enable service APIs before using them — unlike AWS where most services are available by default.
3. `gcloud` **create VPC** — Build the network.
4. `gcloud` **create subnets** — Create network segments within the VPC.
5. Continue with firewall rules, instances, load balancers, etc.

The instructor emphasizes the learning approach: **don't execute scripts blindly**. Instead: "We're going to execute one command at a time. And we understand it and then we run it." After each command, you verify the result in the **Google Cloud Console** (the web UI) — see the VPC that was created, see the subnet, see the firewall rule. Command → understand → execute → verify visually. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## 1.7 — The Learning Methodology: Understand → Execute → Verify

The instructor defines a three-phase approach for every command in the project: [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

1. **Understand the command** — Read it, understand each flag and argument, understand what resource it creates and why.
2. **Execute the command** — Type it (not copy-paste mindlessly), run it, observe the output.
3. **Verify in the Console** — Open the Google Cloud Console in the browser and visually confirm the resource was created correctly.

This mirrors the "local test → remote deploy" validation pattern from the Bash scripting grand finale — but applied to cloud infrastructure. The instructor explicitly asks you to **go through all four scripts first** (VPC, Backend, Frontend 1, Frontend 2), reading and understanding the flow, **before executing anything** in the next lectures. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Doing

We're **cloning the V-Profile project repository**, switching to the GCP branch, and **reading through the source code scripts and variables** to understand the entire deployment flow before executing any commands. This is the preparation phase — no infrastructure is created yet. The outcome: a complete mental map of the project structure, all variables identified and understood, and readiness to execute commands one by one in subsequent lectures. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## Step 1: Clone the Repository in VS Code

### The Action

1. Open **VS Code** (or any editor).
2. Go to **Source Control** (left sidebar, branch icon).
3. Click **"Clone Repository."**
4. Go to the repository: `github.com/vprofile-project` — copy the **HTTPS clone URL**.
5. Paste the URL into VS Code's clone prompt.
6. Select a **destination folder** (e.g., `F:\GCP_vprofile` or any folder you prefer). [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### What Happens

VS Code clones the repository to your local machine. By default, you land on the **main/default branch** — which is NOT the GCP code.

***

## Step 2: Switch to the GCP Branch

### The Action

Click on the **branch name** in the bottom-left of VS Code → search for **"GCP"** → click on the GCP branch. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### What Happens

The file explorer updates to show the GCP-specific scripts. You should see script files organized by phase: VPC, Backend, Frontend Part 1, Frontend Part 2.

### How to Verify

The branch indicator in VS Code's bottom bar should show the GCP branch name. The files should contain `gcloud` commands, not AWS CLI commands.

***

## Step 3: Review the Variables Section

### What We're Doing

Going through the variables defined at the top of the scripts and understanding what each one controls before setting values.

### The Variables to Set

| Variable      | What It Is                  | Recommendation                                                   |
| ------------- | --------------------------- | ---------------------------------------------------------------- |
| `PROJECT_ID`  | Your GCP project ID         | Get from GCP Console                                             |
| `REGION`      | GCP region                  | `us-central1` (same as instructor)                               |
| `APP_NAME`    | Application name prefix     | `vprofile` (keep same)                                           |
| `DOMAIN`      | Public URL domain           | Your domain OR fake domain name                                  |
| `MY_IP`       | Your public IP for firewall | Initially `0.0.0.0/0`, edit later                                |
| `SSH_KEY`     | Public SSH key **content**  | Generate key pair, paste public key content                      |
| `DB_PASSWORD` | Database password           | **Keep same as source** (or update `application.properties` too) |

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### Other Variables

Additional variables define resource names: public subnet names, bastion host name, etc. The instructor says: "You don't need to memorize these things." They exist for naming consistency — just review them and understand what they name. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### Critical Points

* **`DB_PASSWORD`**: If changed, you MUST also update `application.properties`. If kept the same, no additional changes needed. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)
* **`SSH_KEY`**: Must contain the **actual public key content**, not a filename or reference. You'll generate this key pair before launching instances.
* **`MY_IP`**: Will be updated from `0.0.0.0/0` to your actual public IP for proper SSH security.

***

## Step 4: Read Through All Four Scripts (No Execution)

### What We're Doing

Reading through every script file — VPC, Backend, Frontend 1, Frontend 2 — to understand the **entire deployment flow** before running anything.

### How to Read

The instructor's guidance: [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

1. **Focus on `gcloud` commands** — These are the infrastructure commands.
2. **Go through them one by one** — Understand the flow, not every flag.
3. **Look at variable names** — See which variables are used in each command.
4. **Compare variable names to their values** — Understand what gets substituted where.
5. **Understand the flow** — Project setup → API enablement → VPC → Subnets → Firewall → Instances → etc.

### The Execution Flow You Should Identify

```
VPC Script:      Set project → Enable APIs → Create VPC → Create subnets → Firewall rules
Backend Script:  Create backend instances → Configure services → Database setup
Frontend 1:      Create frontend instances → Web server setup
Frontend 2:      Load balancer → DNS → HTTPS → Final public access
```

### What NOT to Do

* **Don't execute any commands yet** — This is read-only preparation.
* **Don't try to memorize commands** — Understanding the flow is the goal.
* **Don't rush** — Take time to compare variables with their values. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

### Connection to Larger Flow

Starting from the **next lecture**, commands will be executed one at a time. For each command: type it → understand it → execute it → verify the result in the Google Cloud Console. The preparation done here ensures you understand the big picture before diving into individual commands. [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Project Architecture: 4-Phase Build

```
PHASE 1: VPC          → Network foundation (VPC, subnets, firewall rules)
PHASE 2: BACKEND      → Data/app tier (DB, app servers inside VPC)
PHASE 3: FRONTEND-1   → Web tier setup (web servers, configuration)
PHASE 4: FRONTEND-2   → Public access (load balancer, DNS, HTTPS)

DEPENDENCY CHAIN:
  VPC → Backend → Frontend-1 → Frontend-2
  (each phase requires the previous phase's resources to exist)
```

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## 🔑 Variables: Set Once, Used Everywhere

```
VARIABLE          PURPOSE                        ACTION
──────────        ───────                        ──────
PROJECT_ID        GCP project identifier          Get from GCP Console
REGION            Deployment region               us-central1 (recommended)
APP_NAME          Resource naming prefix          vprofile (keep same)
DOMAIN            Public website URL              Your domain or fake
MY_IP             SSH firewall source             0.0.0.0/0 → your IP later
SSH_KEY           Public key CONTENT              Generate keypair, paste pubkey
DB_PASSWORD       Database credential             ⚠️ Keep same OR update app.properties too

OTHER VARS: Subnet names, bastion host name, etc. → naming consistency, don't memorize
```

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## 🔄 AWS → GCP Concept Mapping

```
AWS CONCEPT              GCP EQUIVALENT                  KEY DIFFERENCE
───────────              ──────────────                  ──────────────
AWS CLI                  gcloud CLI                      Different syntax, same purpose
AWS Account              GCP Project                     Project ID = scope boundary
Security Group           Firewall Rule                   Same function, different name
Key Pair (managed)       SSH Key (self-managed)          ⚠️ GCP: YOU generate + inject pubkey
                                                         AWS: AWS creates + stores + you download
Services always on       APIs must be ENABLED            gcloud: enable APIs before using them
EC2 Console              Google Cloud Console            Both: visual verification of resources
User Data                Startup Script                  Same concept: commands at first boot
```

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## 🔐 SSH Key Difference (Critical)

```
AWS:
  1. Create key pair IN AWS (named resource)
  2. AWS stores public key
  3. You download private key (.pem)
  4. Attach key pair name at instance launch
  
GCP:
  1. YOU generate key pair locally (ssh-keygen)
  2. Paste PUBLIC KEY CONTENT into variable/metadata
  3. Inject public key INTO instance at launch
  4. Use YOUR private key to SSH in
  
  ⚠️ No cloud-managed key pair service in GCP
  → You manage keys yourself (standard Linux SSH model)
```

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## ⚡ Execution Flow (gcloud Commands in VPC Script)

```
gcloud set project          ← Tell CLI which project to use
    │
    ▼
gcloud enable APIs          ← Activate required GCP services
    │                         (GCP requires explicit API enablement)
    ▼
gcloud create VPC           ← Build the network
    │
    ▼
gcloud create subnets       ← Create network segments
    │
    ▼
gcloud create firewall      ← Define access rules (= AWS Security Groups)
    │
    ▼
... (continue in Backend/Frontend scripts)
```

***

## 📐 Learning Methodology

```
FOR EACH COMMAND:
  1. UNDERSTAND → Read command, flags, arguments, purpose
  2. EXECUTE    → Type command (don't just copy-paste)
  3. VERIFY     → Open Google Cloud Console → visually confirm resource created

THIS LECTURE (preparation):
  → Read ALL scripts (VPC → Backend → Frontend 1 → Frontend 2)
  → Understand flow and variable usage
  → DO NOT execute anything yet

NEXT LECTURES (execution):
  → Execute one command at a time
  → Verify each result in Console
```

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## ⚠️ Configuration Coupling Warning

```
DB_PASSWORD variable
       │
       ├── Used in: Infrastructure scripts (create DB with this password)
       │
       └── Must match: application.properties file (app connects with this password)

  IF password changed in variable BUT NOT in app.properties:
    → App launches → tries to connect to DB → authentication failure
    → Debugging: check if password matches in BOTH places

  SAFEST: Keep default password → no changes needed in app.properties
```

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## 🔗 Repository Structure

```
github.com/vprofile-project
    │
    ├── main branch     → (other deployment targets)
    ├── AWS branch      → AWS CLI commands (done in earlier lectures)
    └── GCP branch ◄── THIS PROJECT
          ├── VPC script         (Phase 1)
          ├── Backend script     (Phase 2)
          ├── Frontend-1 script  (Phase 3)
          └── Frontend-2 script  (Phase 4)
          
          Each script:
            ├── Variables section (top)
            └── gcloud commands (body)
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: VARIABLE-DRIVEN INFRASTRUCTURE COMMANDS
  Set variables once → all commands use variables → same commands work for everyone
  → Same as: Terraform variables, Ansible vars, Helm values,
    .env files, CI/CD pipeline parameters
  → PURPOSE: Consistency + error reduction + portability

PATTERN 2: PHASED DEPENDENCY-ORDERED DEPLOYMENT
  Network → Backend → Frontend → Public access
  → Same as: Terraform dependency graph, Ansible role ordering,
    Docker Compose depends_on, Kubernetes deployment order
  → RULE: Lower layers must exist before upper layers

PATTERN 3: MULTI-CLOUD CONCEPT TRANSFER
  Same application architecture, different cloud commands
  AWS Security Group = GCP Firewall Rule
  AWS Key Pair = GCP SSH Key injection
  → The CONCEPTS are stable; the IMPLEMENTATIONS change per provider
  → Learning one cloud deeply → rapid learning of second cloud

PATTERN 4: UNDERSTAND → EXECUTE → VERIFY (Operational Discipline)
  Never run commands blindly
  → Same as: Code review before merge, test before deploy,
    plan before apply (Terraform), dry-run before execute
```

 [\[291-comman...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/291-commands-in-the-source-code.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → V-Profile on AWS (EC2, EBS, EFS, RDS, ELB, S3, etc.)
           → Lambda, serverless automation
THIS      → V-Profile on GCP — PREPARATION (clone repo, read scripts, understand variables)
NEXT      → Execute VPC commands one by one (gcloud CLI)
LATER     → Backend deployment → Frontend → Load balancer → Full GCP deployment

LEARNING ARC:
  Local VMs (Vagrant) → AWS (Console + CLI) → GCP (gcloud CLI)
  Same application → different infrastructure → concepts transfer
```

***

Your GCP V-Profile preparation material is fully reconstructed — covering the project structure, all variable meanings, the critical AWS-vs-GCP SSH key difference, and the phased execution approach. Ready for the next caption file when you start executing VPC commands, or want me to generate **AnkiDroid flashcards (.csv)** from any of the lectures we've covered? 🃏
