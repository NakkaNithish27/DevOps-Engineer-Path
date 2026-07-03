# ☁️ GCP Project — Configuring Project Variables, SSH Keys, and Enabling APIs in Google Cloud Shell

**Source:** GCP VPC Project — Configuring Project Variables (Caption File) [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

This video is the **setup and configuration lecture** that prepares the Google Cloud environment before creating any infrastructure. The instructor sets up Google Cloud Shell, configures **project variables** for consistent command execution, generates **SSH key pairs** for instance access, saves all variables to `~/.bashrc` for persistence, and **enables the GCP APIs** required for the project. The upcoming infrastructure includes a VPC with four subnets (two public, two private), a Cloud Router, Cloud NAT, and firewall rules — but this lecture focuses entirely on the preparatory configuration that makes the infrastructure creation commands reusable and aligned between the instructor and the learner. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. The Project Scope — What We Are About to Build

Before diving into configuration, the instructor previews the infrastructure that will be created across this and the following lectures. The complete scope is: [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

* **A VPC** (Virtual Private Cloud) — the network container.
* **Four subnets** — two public and two private.
* **A Cloud Router and Cloud NAT** — connected to the private subnets (to give private instances outbound internet access without public IPs).
* **Two firewall rules** — one allowing SSH to the bastion host (the public entry point), and another allowing SSH from the bastion host to instances in the private subnet.

This lecture does not create any of these yet — it prepares the environment so that every creation command in subsequent lectures executes cleanly and consistently.

***

## 2. Google Cloud Shell — The Execution Environment

Google Cloud Shell is a **browser-based terminal** provided by Google Cloud that comes pre-installed with `gcloud` CLI, authenticated to your account, and ready to run commands against your GCP projects. The instructor accesses it by clicking **"Activate Cloud Shell"** in the GCP console and then opens it in a **separate window** for a better working experience. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

Cloud Shell is the GCP equivalent of a local terminal with the `gcloud` SDK installed — but you don't need to install anything. It provides a persistent home directory (`~/`) that survives session restarts, which is why saving variables to `~/.bashrc` (covered later) makes them persistent across sessions.

***

## 3. Project Selection — Setting the Active Project

GCP organizes resources under **projects**. Before running any command, you must tell `gcloud` which project to target. The instructor demonstrates two commands: [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**List all projects:**

```bash
gcloud projects list
```

This shows all projects in your GCP account. You identify the one you want to use.

**Set the active project:**

```bash
gcloud config set project <PROJECT_NAME>
```

This sets the project context for all subsequent `gcloud` commands in this session. Without this, commands either fail or target the wrong project.

***

## 4. Why Variables — The Alignment and Reusability Problem

This is the most important conceptual insight of the entire lecture. The instructor explains **why** variables are being set before any infrastructure is created: [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**"The reason we are setting the variable is so you and me can execute same command."**

The problem: every learner has a different project ID, possibly a different region preference, a different domain name, and a different SSH public key. If the instructor writes commands with his specific values hardcoded (e.g., `gcloud config set project my-project-123`), every learner must manually find and replace those values in every command. This is error-prone, slow, and leads to mistakes.

The solution: **store all environment-specific values in variables**. Then every command uses variable references (`$PROJECT_ID`, `$REGION`, etc.) instead of literal values. The instructor and every learner execute the **exact same commands** — only the variable values differ. The instructor explicitly states: **"If we use the variables, you and me will be executing same command. This is just so in the project setup we are aligned and you don't make such mistakes."** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

This is a direct application of the **parameterization pattern** from the bash scripting section — the same concept that transformed hardcoded scripts into reusable tools using `$1`, `$2` arguments. Here, environment variables serve the same purpose: separate the values that change (project ID, region, keys) from the commands that stay the same.

<details>
<summary>🔍 Deep Dive</summary>

This pattern is universal in DevOps and infrastructure work. Terraform uses `.tfvars` files for the same reason. Ansible uses `group_vars` and `host_vars`. Kubernetes uses ConfigMaps and Secrets. Docker uses `.env` files. The core principle is always the same: **externalize environment-specific values so that the operational logic (commands, templates, playbooks) remains identical across environments.** The instructor is teaching this principle through direct practice, even though the theoretical explanation is brief.

</details>

***

## 5. The Variable Set — What Gets Configured

The instructor references a file called `VPC.file` (from the lecture resources) that contains all the variables needed for the project. The variables and their purposes: [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

| Variable              | Purpose                                           | Customization                                                 |
| --------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| `PROJECT_ID`          | Your GCP project identifier                       | **Must change** to your own project ID                        |
| `REGION`              | The GCP region for all resources                  | Instructor uses `us-central1`; can change but stay consistent |
| Zone                  | The specific zone within the region               | `us-central1-a` (the `-a` zone)                               |
| `APP_NAME`            | Application name (Vprofile)                       | Keep same                                                     |
| Domain name           | Your domain for the project                       | Set your own or remove the variable                           |
| `MY_IP`               | Your public IP for SSH firewall rules             | Keep default initially; update later                          |
| `SSH_KEY`             | The **public key content** for instance injection | **Must generate** and paste your own                          |
| Bastion tag / App tag | Tags for firewall rule targeting                  | Keep same                                                     |

The instructor explicitly identifies which variables **must be changed** (project ID, SSH key, domain) and which can be kept as-is (region, zone, app name, tags). [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

***

## 6. SSH Key Generation — Creating the Access Credentials

The project requires SSH key pairs to access the instances (bastion host and private backend instances). The instructor generates these keys using the same `ssh-keygen` command covered in the bash scripting SSH key exchange lecture. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

The key pair is generated **locally** (on the learner's machine, not in Cloud Shell) because the **private key must stay on the learner's local machine** for SSH access. The public key content is then copied into the variable set so it can be injected into GCP instances during creation.

The instructor creates the keys in a dedicated folder: `~/Downloads/GCP-keys/`. The key is named `gcp-key`, producing `gcp-key` (private) and `gcp-key.pub` (public). [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

The instructor emphasizes a precision requirement: **"Make sure you don't copy any extra space, just exactly the key content."** Extra whitespace in the public key will cause instance SSH injection to fail silently — the key gets stored incorrectly and authentication fails with no obvious error message.

***

## 7. Persisting Variables in `~/.bashrc` — Surviving Session Restarts

Variables set directly in the shell (e.g., `export MY_VAR="value"`) are lost when the session ends. To make them **persistent** — available every time Cloud Shell starts — the instructor saves them in **`~/.bashrc`**. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

`~/.bashrc` is a shell configuration file that bash executes automatically every time a new shell session starts. By placing `export VARIABLE="value"` lines in this file, the variables are automatically set in every future session. After editing the file, running `source ~/.bashrc` immediately loads the variables into the current session without needing to restart.

This is the **permanent mount equivalent for shell variables** — just as `/etc/fstab` makes disk mounts survive reboots (from the EBS lecture), `~/.bashrc` makes variable definitions survive session restarts. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

***

## 8. GCP API Enablement — The Service Activation Requirement

GCP has a unique architectural requirement that differs from AWS: **before using any GCP service, you must explicitly enable its API in your project.** The instructor explains: **"In GCP when we consume a service we need to enable the APIs for those services."** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

This is a security and governance design — services are disabled by default, and you opt-in to each one. The command to enable an API is: [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

```bash
gcloud services enable <API_NAME>
```

The APIs enabled for this project: [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

| API                                 | Service                                   |
| ----------------------------------- | ----------------------------------------- |
| `compute.googleapis.com`            | Compute Engine (VMs, VPC, firewall, etc.) |
| `dns.googleapis.com`                | Cloud DNS                                 |
| `sqladmin.googleapis.com`           | Cloud SQL Admin                           |
| `sql-component.googleapis.com`      | Cloud SQL Components                      |
| `memcache.googleapis.com`           | Memorystore (Memcache)                    |
| `certificatemanager.googleapis.com` | Certificate Manager                       |
| `servicenetworking.googleapis.com`  | Service Networking                        |

You can enable them one at a time or all at once in a single command. The instructor enables all of them in one command. This is a **one-time operation** per project — once enabled, the API stays enabled. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

<details>
<summary>🔍 Deep Dive</summary>

In AWS, services are enabled by default — you can start using EC2, S3, RDS immediately without any activation step. GCP's explicit enablement model provides tighter control: billing only begins when you enable a service, and administrators can restrict which APIs are available via organization policies. This is particularly useful in enterprise environments where you want to prevent teams from accidentally using expensive or unauthorized services.

</details>

***

## 9. The Trust-but-Verify Practice

The instructor introduces a practical discipline: **before running any command that uses variables, always `echo` the variables first to verify they contain the expected values.** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**"Before running the command, make sure you always do an echo to the variables that you're going to use in the command, just to be sure that you're doing the right thing."**

This is a safety pattern — if a variable is empty or contains the wrong value, the command will either fail cryptically or (worse) execute against the wrong resource. A quick `echo $REGION` before using `$REGION` in a creation command catches errors before they cause damage. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are preparing the Google Cloud Shell environment for the VPC project by: configuring project variables, generating SSH keys, persisting everything in `~/.bashrc`, and enabling all required GCP APIs. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Why it matters:** Every infrastructure creation command in subsequent lectures depends on these variables being correctly set and these APIs being enabled. This is the foundation layer — get it wrong, and everything after it fails.

**Final outcome:** A Cloud Shell environment where running `echo $PROJECT_ID`, `echo $REGION`, `echo $SSH_KEY` returns correct values, and all required GCP APIs are enabled and ready to use.

***

## Step 1: Open Google Cloud Shell

1. Log in to your **Google Cloud Console**. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)
2. Click **"Activate Cloud Shell"** (icon in the top-right toolbar).
3. Click the **"Open in new window"** button to get a full-size terminal.

**Operational reasoning:** Working in a separate window gives more screen space and avoids the small embedded panel at the bottom of the console.

**Connection to flow:** Cloud Shell is your command execution environment for the entire project.

***

## Step 2: List and Set Your Project

**List available projects:** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

```bash
gcloud projects list
```

Identify the project you want to use.

**Set the active project:**

```bash
gcloud config set project <YOUR_PROJECT_ID>
```

* `gcloud config set` — Sets a configuration property.
* `project` — The property being set.
* `<YOUR_PROJECT_ID>` — Your specific project identifier (e.g., `project-vprofile`).

**Expected output:** Confirmation message showing the project is set.

**Common mistake:** Typo in the project ID → command fails or sets the wrong project. Always copy the project ID from the `gcloud projects list` output.

**Connection to flow:** All subsequent commands target this project. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

***

## Step 3: Download and Customize the Variables File

**What we are doing:** Getting the variable template from the lecture resources and customizing it for your environment. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

1. Open the **VPC.file** from the lecture resources.
2. Copy **all variables** from `PROJECT_ID` to the end (bastion tag, app tag).
3. Paste into a **text editor** (Notepad or any editor).

**Customize these values:** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

* **`PROJECT_ID`** — Replace with your own project ID (from Step 2). Keep the double quotes, replace only the value inside.
* **`REGION`** — Keep `us-central1` (recommended to match the instructor).
* **Zone** — Keep `us-central1-a`.
* **`APP_NAME`** — Keep as `vprofile`.
* **Domain name** — Set your own domain if you have one, or remove the variable entirely.
* **`MY_IP`** — Keep the default for now. The instructor will show how to update it to your specific public IP later when doing SSH.
* **`SSH_KEY`** — Will be set in the next step (leave empty for now).

**Connection to flow:** Variables customized. Next, generate the SSH key to complete the variable set.

***

## Step 4: Generate SSH Keys Locally

**What we are doing:** Creating an SSH key pair on your local machine for accessing GCP instances. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Open a local terminal:**

* **Windows:** Open **Git Bash**.
* **Mac/Linux:** Open **Terminal**.

**Navigate to a dedicated folder:**

```bash
cd ~/Downloads
mkdir GCP-keys
cd GCP-keys
```

**Generate the key pair:**

```bash
ssh-keygen
```

When prompted for a file name, enter: `gcp-key` [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

Press **Enter** three times (accept default location, no passphrase, confirm no passphrase).

**Verify the keys:**

```bash
ls
```

Expected: `gcp-key` (private key) and `gcp-key.pub` (public key). [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Copy the public key content:**

```bash
cat gcp-key.pub
```

**⚠️ Critical:** Copy the output **exactly** — no extra spaces before or after. The instructor warns: **"Make sure you don't copy any extra space, just exactly the key content."** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Paste into the variable set:** Go back to your text editor and paste the public key content into the `SSH_KEY` variable between the double quotes.

**Common mistake:** Copying extra whitespace or a trailing newline → the key will be injected incorrectly into instances → SSH login fails with no obvious error.

**Connection to flow:** All variables are now complete. Next, save them to Cloud Shell.

***

## Step 5: Save Variables to `~/.bashrc` in Cloud Shell

**What we are doing:** Persisting all variables in Cloud Shell's bash configuration file so they survive session restarts. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**In Cloud Shell, open the bashrc file:**

```bash
vim ~/.bashrc
```

**Navigate to the end of the file:**

* Press `Shift+G` (go to last line).
* Press `o` (open new line below in insert mode).

**Paste all variables:**

* Use `Shift+Insert` (or right-click paste) to paste all the variable export statements. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Verify the content:**

* Scroll through and check that:
  * No extra characters were introduced during paste.
  * No lines broke incorrectly (the instructor catches and fixes a line break issue).
  * All values are within double quotes.
  * Comments (`#`) are intact and not splitting into wrong lines.

**Save and exit:**

* Press `Esc` → type `:wq` → Enter.

**Load the variables into the current session:**

```bash
source ~/.bashrc
```

* `source` — Executes the file in the current shell session (without starting a new shell).
* `~/.bashrc` — The file containing the variable exports. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Connection to flow:** Variables are now active in this session and will be automatically available in all future sessions.

***

## Step 6: Verify Variables

**What we are doing:** Testing that variables are correctly set before using them in any command. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

```bash
echo $REGION
```

**Expected output:** `us-central1` (or whatever region you set).

Test other variables similarly:

```bash
echo $PROJECT_ID
echo $SSH_KEY
```

**The instructor's practice rule:** **"Before running the command, make sure you always do an echo to the variables that you're going to use in the command, just to be sure that you're doing the right thing."** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Failure scenario:** If `echo` returns empty → the variable wasn't saved correctly in `~/.bashrc` → re-edit the file and re-source.

**Connection to flow:** Variables verified. Next, enable the GCP APIs.

***

## Step 7: Set the Project Again (Using Variable)

```bash
gcloud config set project $PROJECT_ID
```

Cloud Shell may prompt to **authorize** — click authorize. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

This re-sets the project using the variable (instead of the literal value from Step 2), confirming the variable works correctly in actual commands.

**Connection to flow:** Project set via variable. Now enable the service APIs.

***

## Step 8: Enable GCP APIs

**What we are doing:** Activating all the GCP services needed for this project. This is a one-time operation. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Command (all APIs at once):**

```bash
gcloud services enable compute.googleapis.com dns.googleapis.com sqladmin.googleapis.com sql-component.googleapis.com memcache.googleapis.com certificatemanager.googleapis.com servicenetworking.googleapis.com
```

**Breakdown of each API:**

| API                                 | What It Enables                                    |
| ----------------------------------- | -------------------------------------------------- |
| `compute.googleapis.com`            | Compute Engine — VMs, VPC, subnets, firewall rules |
| `dns.googleapis.com`                | Cloud DNS — DNS zone and record management         |
| `sqladmin.googleapis.com`           | Cloud SQL Admin — managed database administration  |
| `sql-component.googleapis.com`      | Cloud SQL Components — SQL service components      |
| `memcache.googleapis.com`           | Memorystore for Memcache — managed caching         |
| `certificatemanager.googleapis.com` | Certificate Manager — SSL/TLS certificates         |
| `servicenetworking.googleapis.com`  | Service Networking — private service connections   |

**What happens:** Each API is enabled in your project. The instructor notes: **"This is going to take some time."** [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

**Expected output:** Success confirmation for each API. The instructor confirms: **"All those APIs got enabled... it got completed successfully."**

**Common mistake:** Forgetting to enable an API → commands for that service fail with "API not enabled" error. The error message usually tells you which API to enable.

**Alternative approach:** You can enable one API at a time:

```bash
gcloud services enable compute.googleapis.com
gcloud services enable dns.googleapis.com
```

**Connection to flow:** All APIs enabled. The environment is now fully prepared for VPC creation in the next lecture. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

<details>
<summary>⚠️ Expert Note</summary>

In production GCP environments, API enablement is often managed through **Organization Policies** and **Terraform** (`google_project_service` resource). APIs are enabled declaratively as part of the infrastructure code, ensuring new projects are automatically configured correctly. The manual `gcloud services enable` approach works for learning and ad-hoc projects, but doesn't scale to multi-project enterprise environments.

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   GCP Project Setup — Variables, SSH Keys, API Enablement
CONTEXT: GCP VPC project → preparation lecture before infrastructure creation
PURPOSE: Configure environment so all infrastructure commands work identically for everyone
```

***

## What Will Be Created (Next Lectures)

```
VPC
├── 2 Public Subnets
├── 2 Private Subnets
├── Cloud Router + Cloud NAT → connected to private subnets
└── 2 Firewall Rules
    ├── SSH → Bastion Host (public)
    └── SSH Bastion → Private Instances
```

***

## Variable Strategy — The Core Idea

```
PROBLEM:  Different users have different project IDs, keys, domains
          → hardcoded commands = different for everyone = errors

SOLUTION: Store all changing values in VARIABLES
          → commands use $VARIABLE references
          → everyone executes SAME commands
          → only variable VALUES differ

PATTERN:  Same as bash $1/$2 parameterization, Terraform .tfvars, Ansible group_vars
```

***

## Variables Configured

```
MUST CHANGE:
  PROJECT_ID    → your GCP project ID
  SSH_KEY       → your public key content (generated locally)
  Domain        → your domain name (or remove variable)

KEEP SAME (recommended):
  REGION        → us-central1
  ZONE          → us-central1-a
  APP_NAME      → vprofile
  MY_IP         → default for now (update later)
  BASTION_TAG   → keep
  APP_TAG       → keep
```

***

## SSH Key Generation Flow

```
LOCAL MACHINE (Git Bash / Terminal):
  cd ~/Downloads → mkdir GCP-keys → cd GCP-keys
  ssh-keygen → name: gcp-key → Enter × 3

OUTPUT:
  gcp-key       ← PRIVATE key (stays local, used for SSH login)
  gcp-key.pub   ← PUBLIC key (content → paste into SSH_KEY variable)

CRITICAL: copy public key content EXACTLY — no extra spaces
```

***

## Variable Persistence Flow

```
1. Customize variables in text editor
2. vim ~/.bashrc → Shift+G → o → paste all variables
3. Verify content → Esc → :wq
4. source ~/.bashrc → loads into current session
5. echo $VARIABLE → verify before using

~/.bashrc = shell config file → auto-executes on every new session
source = reload without restarting session
```

***

## GCP API Enablement

```
GCP RULE: services DISABLED by default → must ENABLE before use
          (different from AWS where services are available immediately)

ONE-TIME COMMAND:
  gcloud services enable compute.googleapis.com dns.googleapis.com \
    sqladmin.googleapis.com sql-component.googleapis.com \
    memcache.googleapis.com certificatemanager.googleapis.com \
    servicenetworking.googleapis.com

APIs enabled for this project:
  Compute Engine (VPC, VMs, firewall)
  Cloud DNS
  Cloud SQL (Admin + Components)
  Memorystore (Memcache)
  Certificate Manager
  Service Networking
```

***

## Command Reference

```
gcloud projects list                        → list all projects
gcloud config set project <ID>              → set active project
gcloud services enable <API>                → enable a GCP service API
ssh-keygen                                  → generate SSH key pair
vim ~/.bashrc                               → edit shell config for variable persistence
source ~/.bashrc                            → reload bashrc into current session
echo $VARIABLE                              → verify variable value
```

***

## Google Cloud Shell

```
Access:    GCP Console → Activate Cloud Shell → Open in new window
Features:  Pre-installed gcloud CLI, authenticated, persistent ~/
Equivalent: local terminal with gcloud SDK installed
```

***

## Trust-but-Verify Pattern

```
BEFORE running any command with variables:
  echo $VAR1 $VAR2 → check values are correct
  THEN run the actual command

WHY: empty/wrong variable → command fails cryptically or targets wrong resource
```

***

## AWS vs GCP: API Enablement Difference

```
AWS:  services available immediately → no enablement step
GCP:  services DISABLED by default → must gcloud services enable
      → tighter governance, billing control, security
```

***

## Reusable Engineering Patterns

```
1. EXTERNALIZE ENVIRONMENT-SPECIFIC VALUES → Variables separate data from logic
                                              Same commands work everywhere
                                              (Terraform .tfvars, Ansible vars, Docker .env, K8s ConfigMaps)

2. PERSIST CONFIGURATION IN DOTFILES      → ~/.bashrc for shell variables
                                              Same as /etc/fstab for mounts
                                              Config file → survives restarts

3. EXPLICIT SERVICE ACTIVATION            → GCP APIs must be enabled before use
                                              Opt-in model → security + governance
                                              (contrast: AWS implicit availability)

4. TRUST-BUT-VERIFY                       → echo variables before using in commands
                                              Catch errors before they cause damage
                                              (same as dry-run, plan, --check patterns)

5. LOCAL KEYS, REMOTE LOCKS               → SSH key generated locally, public key injected remotely
                                              Same lock-and-key pattern from SSH key exchange lecture
                                              Private key never leaves local machine

6. ONE-TIME SETUP, REPEATED USE           → API enablement + variable config = one-time
                                              All subsequent infrastructure commands = repeated use
                                              (same pattern: tool installation, env setup)
```

***

## Rapid Recall Triggers

```
"Why variables for GCP project?"       → Everyone executes same commands, only values differ
"Where to save GCP variables?"         → ~/.bashrc (persists across Cloud Shell sessions)
"How to load bashrc changes?"          → source ~/.bashrc
"SSH keys for GCP — where generated?"  → Locally (Git Bash/Terminal), NOT in Cloud Shell
"Public key goes where?"               → Into SSH_KEY variable → injected into instances
"Private key stays where?"             → Local machine → used for SSH login
"GCP API enablement?"                  → gcloud services enable <api> — one-time, required before use
"AWS vs GCP service availability?"     → AWS = immediate, GCP = must enable API first
"How to verify variables?"             → echo $VARIABLE before running any command
"Cloud Shell is what?"                 → Browser-based terminal, pre-authenticated, persistent ~/
"Key name used?"                       → gcp-key (private) + gcp-key.pub (public)
"What APIs enabled?"                   → Compute, DNS, SQL Admin, SQL Component, Memcache, Cert Manager, Service Networking
"Extra spaces in SSH key?"             → BREAKS key injection silently — copy exactly
```

***

This completes the full reconstruction of the GCP Project Variables Configuration lecture. **Theory** builds the conceptual understanding of why variables exist, how GCP API enablement works, and where keys fit; **Practical** walks through every command from Cloud Shell setup through API enablement with exact syntax and verification steps; and the **Mental Compression Map** compresses the variable strategy, key flow, API model, and all operational patterns into rapid-recall structures. [\[292-config...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/292-configuring-project-variables.txt)

Ready for the next caption file in the GCP series, or shall I generate an **AnkiDeck CSV** covering this lecture or the full course? 🚀
