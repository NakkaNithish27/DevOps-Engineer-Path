# 📘 DevOps Course — Tools & Prerequisites Setup

**Source:** Captions from a DevOps course video — *"Tools: Prerequisite Information"* section [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

This video is the opening orientation lecture of a DevOps course. It explains **what tools, accounts, and cloud infrastructure** the learner must prepare before hands-on work begins, **why** each is needed, and **how the course repository is structured**. No installation is performed in this lecture — it is a roadmap and reasoning session.

***

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. Course Structure & the Prerequisites Philosophy

The course is structured so that all foundational setup — tools, accounts, cloud configuration — happens **upfront, before any project work begins**. The instructor explicitly acknowledges that some commands and steps introduced during this setup phase will look unfamiliar and will only make full sense later as the course progresses deeper into actual DevOps workflows. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

This is a deliberate pedagogical choice: **install first, understand later**. The reasoning is that DevOps workflows involve many interconnected tools, and trying to fully understand each tool before installing it would stall progress. Instead, the course front-loads all environment preparation into one block, so that when project work begins, no setup interruptions occur. The prerequisites are divided into three distinct categories: **tool installation**, **platform account creation**, and **AWS cloud account configuration**. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

This three-part division reflects a real-world pattern: DevOps environments depend on **local tooling** (what runs on your machine), **external platform integrations** (where code, images, and analysis live), and **cloud infrastructure** (where workloads run). Setting up all three layers before starting ensures the learner has a complete operational environment ready.

***

### 2. The GitHub Repository — Central Source Code Hub

All source code, scripts, and configuration files used throughout the course are hosted in a single GitHub repository at the URL: `github.com/coder/v-profile-project`. This is the **V Profile project**, which serves as the primary application the course builds, deploys, and manages across various DevOps scenarios. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

A critical concept here is **branching**. Any Git repository can have multiple branches, and this course uses branches to organize code **per section and per project**. As the learner moves through different course sections, the instructor will guide them to switch to the appropriate branch. This means the same repository contains different states/versions of the project tailored to each lecture's needs. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

🔍 **Deep Dive:**
Branching in this context is not just version control — it acts as a **section-navigation mechanism**. Each branch represents a snapshot of the project at the stage relevant to a particular lecture. This allows learners to start any section with the correct codebase without manually building up from scratch. It also means that if a learner falls behind or makes errors, they can always check out the correct branch to reset to a known-good state.

***

### 3. Package Managers — Chocolatey & Homebrew

The course installs all tools through **command-line package managers** rather than manual GUI-based downloads. This is explicitly framed as the professional approach — "like a pro." [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**For Windows: Chocolatey.** This is a command-line package manager that lets you install, update, and manage software from the terminal. It eliminates the need to visit individual websites, download installers, and click through setup wizards.

**For macOS: Homebrew.** This serves the same purpose on macOS — a command-line tool for installing and managing software packages.

The reason this matters in DevOps is foundational: **DevOps is a command-line-first discipline.** Nearly every tool in the DevOps ecosystem — from provisioning to deployment to monitoring — is operated via CLI. Starting with CLI-based installation builds the right muscle memory from day one. Package managers also ensure **reproducibility** — the same command installs the same version of a tool on any machine, which is critical when standardizing environments.

macOS has two chip architectures in current circulation: **Intel chips** (older MacBooks) and **ARM chips** (Apple Silicon, latest MacBooks). Homebrew must be set up for both, and the instructor provides guidance for each. This distinction becomes important for virtualization tool selection (covered next). [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

***

### 4. Virtualization Tools — Hypervisors (VirtualBox & VMware Fusion)

A hypervisor is software that allows you to create and run **virtual machines (VMs)** — isolated operating system instances running on top of your physical hardware. The course uses two hypervisors depending on the learner's platform: [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Oracle VM VirtualBox** — used on **Windows** and **macOS with Intel chips**. VirtualBox is a free, open-source hypervisor. It is the default choice for the course.

**VMware Fusion** — used on **macOS with ARM chips** (latest MacBook Air/Pro with Apple Silicon). The reason for this split is a hard technical constraint: **VirtualBox does not support the latest ARM-based MacBooks.** VMware Fusion provides equivalent virtualization capability on ARM architecture. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

Both tools serve the same functional purpose — they are virtualization platforms that let you run VMs locally. The choice between them is purely driven by **hardware compatibility**, not feature preference.

🔍 **Deep Dive:**
This is an example of a common DevOps reality: **tooling decisions are often constrained by infrastructure compatibility, not personal preference.** The transition from Intel to ARM in Apple's lineup broke compatibility with several established tools. In production environments, similar situations arise when migrating between architectures (x86 to ARM in cloud, for example), and engineers must identify functionally equivalent alternatives.

⚠️ **Expert Note:**
The ARM compatibility issue with VirtualBox is a known, ongoing limitation. If you're purchasing hardware specifically for this course or for DevOps work in general, be aware that ARM-based machines may require alternative tooling for virtualization layers.

***

### 5. Git Bash — Linux Command Line on Windows

Git Bash is a **Windows-only** tool that provides a Linux-like terminal environment. It is explicitly described as much more convenient than the default Windows Command Prompt. Its core value is that it gives you **Linux command-line capabilities on a Windows machine**. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

This matters because the vast majority of DevOps tooling, scripting, and server environments are Linux-based. Commands, file paths, shell scripting syntax, and operational patterns in DevOps follow Linux conventions. Git Bash bridges this gap for Windows users, ensuring they can follow the same commands and workflows as macOS/Linux users without translation.

***

### 6. Vagrant — VM Automation

Vagrant is described as a **VM automation tool**, and it is installed on **all operating systems** regardless of platform. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

While VirtualBox/VMware Fusion provide the virtualization engine (the hypervisor), Vagrant sits **on top** of the hypervisor and automates the process of creating, configuring, and managing VMs. Instead of manually clicking through a GUI to create a VM, set its resources, attach an OS image, and configure networking, Vagrant lets you define all of this in a configuration file and spin up VMs with a single command.

This is the first instance in the course of a **controller/engine pattern**: the hypervisor is the engine that runs VMs, and Vagrant is the controller that orchestrates them. Vagrant doesn't replace the hypervisor — it requires one underneath. This is why both are installed. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

These tools (package manager + hypervisor + Vagrant) are all used in the **next section of the course: VM Setup**. This confirms the front-loading pattern — install everything now, use it immediately after.

***

### 7. Extended Tool Ecosystem (Later in the Course)

Beyond the immediate prerequisites, the course will introduce additional tools as it progresses: [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

* **JDK (Java Development Kit)** — required for building Java-based applications (the V Profile project is Java-based, implied by the presence of Maven).
* **Maven** — a build automation tool for Java projects. It compiles code, runs tests, and packages applications.
* **VSCode (Visual Studio Code)** — the primary code editor used throughout the course.
* **Sublime Text Editor** — an additional lightweight text editor.
* **AWS CLI** — the command-line interface for interacting with Amazon Web Services.
* **Terraform** — an infrastructure-as-code tool for provisioning cloud resources.

These tools are not installed in this section — they will be introduced **when their respective course sections begin**. The mention here serves as a roadmap so learners know what's coming.

🔍 **Deep Dive:**
Notice the tool categories emerging: **build tools** (JDK, Maven), **editors** (VSCode, Sublime), **cloud interaction** (AWS CLI), and **infrastructure automation** (Terraform). This mirrors the real DevOps toolchain: you write code, build it, interact with cloud providers, and automate infrastructure — each layer has its own specialized tooling.

***

### 8. Platform Accounts — External Service Dependencies

The course requires accounts on several external platforms, each serving a distinct role in the DevOps pipeline: [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**GitHub** — for hosting and version-controlling source code. The learner needs their own account to interact with repositories (forking, cloning, pushing code).

**Docker Hub** — a container image registry. When the course builds Docker images (containerized applications), Docker Hub is where those images are stored and distributed. It functions as the central repository for container images, analogous to how GitHub hosts source code.

**Sonarcloud** — a cloud-based code quality and security analysis platform. It scans code for bugs, vulnerabilities, and code smells. Its role in the course will be covered in later sections.

**Domain Purchase (Optional)** — for production use cases in the course, a purchased domain name is needed. This is explicitly marked as optional — learners who don't want to spend money can skip it. The instructor will guide how to purchase a very low-cost domain. The production use cases requiring a domain likely involve DNS configuration, HTTPS setup, and real-world deployment simulations. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

***

### 9. AWS Free Tier Account — Cloud Infrastructure Foundation

AWS (Amazon Web Services) is the **primary cloud provider** for the course. The setup involves four distinct configuration steps, each addressing a different concern: [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Creating a Free Tier Account** — AWS offers a free tier that provides limited usage of many services at no cost. This allows learners to practice cloud operations without incurring charges, as long as usage stays within free-tier limits.

**Creating an IAM User with Multi-Factor Authentication (MFA)** — rather than using the root account (which has unrestricted access to everything), the course creates a separate user. MFA adds a second authentication factor (typically a phone-based code) beyond just a password. This is a **security best practice** — the root account should rarely be used directly, and MFA protects against credential compromise. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Setting Up a Billing Alarm** — this is a cost-protection mechanism. A billing alarm notifies you when your AWS charges exceed a threshold you define. This prevents accidental cost overruns from resources left running or misconfigured services. The instructor emphasizes configuring AWS **safely, securely, and without unnecessary cost** — this alarm is the operational enforcement of that principle. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Requesting an SSL Certificate** — SSL (Secure Sockets Layer) certificates enable HTTPS connections (encrypted web traffic). This is requested upfront because production deployments and domain-based access in later sections will require secure connections. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

⚠️ **Expert Note:**
The AWS setup sequence — free tier → IAM user → MFA → billing alarm → SSL — is not arbitrary. It follows a **security-first, cost-aware** configuration pattern that mirrors real-world AWS onboarding best practices. In production environments, these are among the first things configured when a new AWS account is provisioned.

***

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Setting Up and Why

In this section, we are preparing the **complete development and operations environment** needed for the entire DevOps course. The final outcome is: a local machine with all required tools installed via command line, accounts on all necessary external platforms, and a fully configured AWS cloud account ready for secure, cost-controlled usage. No actual project work happens here — this is purely environment preparation. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

The video covered in this lecture is a **roadmap lecture** — it explains what will be installed and why, but the actual installation commands are performed in subsequent lectures. Below is the precise operational sequence and decision logic the learner must follow.

***

### Step 1: Access and Bookmark the GitHub Repository

**What:** Open a browser and navigate to:

```
github.com/coder/v-profile-project
```

**Why:** This repository contains all source code, scripts, and configuration files for the entire course. It is the single source of truth for project assets. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Action:** Bookmark this URL. You will return to it repeatedly throughout the course.

**Branch Selection Logic:** The repository has multiple branches. You do **not** need to select a branch now. As each course section begins, the instructor will specify which branch to check out. Each branch corresponds to a specific section/project state. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Verification:** Confirm you can see the repository page with its branch dropdown and file listing.

***

### Step 2: Install the Package Manager for Your OS

**Decision point — choose based on your operating system:** [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

| OS                   | Package Manager | Purpose                                  |
| -------------------- | --------------- | ---------------------------------------- |
| Windows              | **Chocolatey**  | CLI-based software installer for Windows |
| macOS (Intel or ARM) | **Homebrew**    | CLI-based software installer for macOS   |

**What:** Install the appropriate package manager first, before any other tool. All subsequent tool installations will be done **through** this package manager via command line.

**Why operationally:** Every other tool installation depends on this. The package manager is the foundation of the installation workflow. Without it, you'd need to manually download and install each tool individually. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**macOS note:** Whether your Mac has an Intel chip or an ARM chip (Apple Silicon), you install Homebrew either way. The Homebrew installation process handles the architecture difference internally. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Verification:** After installation, confirm the package manager works by running its version or help command in your terminal.

**Connection to larger flow:** This is the first tool installed because it is the **installer for all other tools**. Everything downstream depends on it.

***

### Step 3: Install the Hypervisor (Virtualization Tool)

**Decision point — choose based on your OS and chip architecture:** [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

| Platform                         | Hypervisor to Install    |
| -------------------------------- | ------------------------ |
| Windows                          | **Oracle VM VirtualBox** |
| macOS — Intel chip               | **Oracle VM VirtualBox** |
| macOS — ARM chip (Apple Silicon) | **VMware Fusion**        |

**What:** Install the virtualization software that will run virtual machines on your local computer.

**Why operationally:** The next course section (VM Setup) requires you to create and run VMs. The hypervisor is the engine that makes this possible.

**Critical constraint:** If you have a latest MacBook with an ARM chip, you **cannot** use VirtualBox — it is not supported. You **must** use VMware Fusion instead. This is a hard technical limitation, not a preference. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**How to check your Mac's chip:** Go to Apple menu → About This Mac. If it says "Apple M1/M2/M3" etc., you have ARM. If it says "Intel," you have Intel.

**Verification:** After installation, open the hypervisor application to confirm it launches without errors.

***

### Step 4: Install Git Bash (Windows Only)

**What:** Install Git Bash on your Windows machine. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Why operationally:** Git Bash provides a Linux-like terminal on Windows. The course commands use Linux syntax (paths with `/`, commands like `ls`, `cat`, `ssh`, etc.). The default Windows Command Prompt does not support these. Git Bash ensures you can execute the same commands as macOS/Linux users.

**Skip condition:** If you are on macOS or Linux, skip this step — your terminal already provides Linux command-line capabilities natively.

**Verification:** Open Git Bash and run a basic Linux command (e.g., `ls` or `pwd`) to confirm it works.

***

### Step 5: Install Vagrant (All Operating Systems)

**What:** Install Vagrant on your machine regardless of your OS. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Why operationally:** Vagrant automates VM creation and management. Instead of manually configuring VMs through the hypervisor's GUI, you'll use Vagrant to define and launch VMs from configuration files via CLI. It works **on top of** the hypervisor installed in Step 3.

**Dependency:** Vagrant requires a hypervisor underneath it. This is why the hypervisor was installed first (Step 3). Vagrant alone cannot run VMs — it orchestrates them through VirtualBox or VMware Fusion.

**Verification:** Run `vagrant --version` in your terminal to confirm successful installation.

**Connection to larger flow:** With the package manager (Step 2), hypervisor (Step 3), and Vagrant (Step 5) installed, you have the complete local VM automation stack ready for the next course section. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

***

### Step 6: Create Platform Accounts

Create accounts on the following platforms: [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

| Platform             | Purpose                                    | Required?  |
| -------------------- | ------------------------------------------ | ---------- |
| **GitHub**           | Source code hosting and version control    | ✅ Yes      |
| **Docker Hub**       | Container image hosting and distribution   | ✅ Yes      |
| **Sonarcloud**       | Code quality and security analysis         | ✅ Yes      |
| **Domain Registrar** | Purchase a domain for production use cases | ❌ Optional |

**Domain purchase guidance:** The instructor will show how to purchase a very low-cost domain. If you are not comfortable spending money, you can skip this. The domain is needed only for specific production-scenario lectures. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Verification:** For each platform, confirm you can log in and access your dashboard.

***

### Step 7: AWS Free Tier Account — Full Setup

This is described as the **longest but most rewarding** part of the prerequisites. It involves four sub-steps: [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**7a. Create an AWS Free Tier Account**

* Sign up at the AWS website for a free-tier account.
* The free tier provides limited free usage of many AWS services.
* The instructor emphasizes using AWS **safely, securely, and without unnecessary cost**. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**7b. Create an IAM User with MFA**

* After account creation, create a separate IAM (Identity and Access Management) user.
* Do **not** use the root account for daily operations.
* Enable Multi-Factor Authentication (MFA) on this user for security.
* MFA requires a second verification step (e.g., authenticator app on your phone) during login. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**7c. Set Up a Billing Alarm**

* Configure a billing alarm that triggers a notification when charges exceed a defined threshold.
* This protects against unexpected costs from forgotten or misconfigured resources. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**7d. Request an SSL Certificate**

* Request an SSL certificate through AWS (likely via AWS Certificate Manager).
* This certificate enables HTTPS connections for deployments later in the course. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)

**Verification:** Confirm you can log in as the IAM user (not root) with MFA, verify the billing alarm is active in CloudWatch, and confirm the SSL certificate request is in a pending or issued state.

**Connection to larger flow:** AWS is the primary cloud provider for the entire course. This setup ensures every subsequent cloud-based lecture can proceed without interruption, and that you are protected against security risks and unexpected billing.

***

### Execution Sequence Summary

```
1. Bookmark GitHub repo
2. Install Package Manager (Chocolatey / Homebrew)
3. Install Hypervisor (VirtualBox / VMware Fusion) ← depends on OS + chip
4. Install Git Bash (Windows only)
5. Install Vagrant (all OS) ← depends on hypervisor
6. Create accounts (GitHub, Docker Hub, Sonarcloud, optional domain)
7. AWS setup (Free tier → IAM user + MFA → Billing alarm → SSL cert)
→ Ready for course Section 2: VM Setup
```

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### System Architecture — Prerequisites Stack

```
LOCAL MACHINE
├── Package Manager (Chocolatey | Homebrew)
│   └── installs everything below ↓
├── Hypervisor (VirtualBox | VMware Fusion)
│   └── runs VMs
├── Vagrant
│   └── automates VM lifecycle via ↑ Hypervisor
├── Git Bash (Windows only)
│   └── Linux CLI on Windows
└── [Later] JDK, Maven, VSCode, Sublime, AWS CLI, Terraform

EXTERNAL PLATFORMS
├── GitHub → source code + course branches
├── Docker Hub → container image registry
├── Sonarcloud → code quality analysis
└── Domain (optional) → production DNS/HTTPS scenarios

CLOUD (AWS)
├── Free Tier Account
├── IAM User + MFA → security
├── Billing Alarm → cost protection
└── SSL Certificate → HTTPS readiness
```

***

### Key Decision Tree — Tool Selection

```
OS = Windows?
  → Chocolatey + VirtualBox + Git Bash + Vagrant

OS = macOS + Intel?
  → Homebrew + VirtualBox + Vagrant

OS = macOS + ARM?
  → Homebrew + VMware Fusion + Vagrant
         ↑
    VirtualBox NOT supported on ARM
```

***

### Dependency Chain

```
Package Manager → installs → Hypervisor → required by → Vagrant
                → installs → Git Bash (Win)
                → installs → Vagrant
                → installs → [future tools]
```

**Vagrant cannot function without a hypervisor.** The hypervisor is the engine; Vagrant is the controller.

***

### Controller / Engine Pattern (Reusable)

```
Controller (orchestrator)  →  Engine (executor)
─────────────────────────────────────────────
Vagrant                    →  VirtualBox / VMware Fusion
[Later] Terraform          →  AWS / Cloud APIs
[Later] Maven              →  JDK / Compiler
```

This pattern recurs throughout DevOps: **an automation layer sits on top of an execution engine**, abstracting away manual operations into declarative configuration.

***

### AWS Setup — Security-Cost-Readiness Sequence

```
Free Tier Account
  → IAM User (don't use root)
    → MFA (protect credentials)
      → Billing Alarm (protect wallet)
        → SSL Certificate (enable HTTPS for later)
```

**Pattern:** Security first → Cost protection → Operational readiness

***

### GitHub Repository — Branch-as-Section-Navigator

```
Repo: github.com/coder/v-profile-project
  ├── Branch A → Section/Project 1
  ├── Branch B → Section/Project 2
  ├── Branch C → Section/Project 3
  └── ...
```

**Mental model:** Branches = course checkpoints. Wrong section? Checkout the right branch.

***

### Three-Layer Environment Model

```
Layer 1: LOCAL TOOLS    → build, edit, automate locally
Layer 2: PLATFORMS      → store code, images, analysis externally
Layer 3: CLOUD (AWS)    → run workloads in production-like infra
```

All three layers must be ready before project work begins. This mirrors real DevOps environment architecture: **local dev → external services → cloud infrastructure**.

***

### Recall Triggers

| If you need to remember...               | Think...                                                             |
| ---------------------------------------- | -------------------------------------------------------------------- |
| Why VMware Fusion instead of VirtualBox? | ARM Mac → VirtualBox incompatible                                    |
| Why Chocolatey/Homebrew first?           | They install everything else                                         |
| Why not use AWS root account?            | Security — IAM user + MFA instead                                    |
| Why billing alarm?                       | Cost protection — prevent surprise charges                           |
| Why SSL cert upfront?                    | HTTPS needed later — request early, ready when needed                |
| Why Vagrant + Hypervisor?                | Controller + Engine pattern — Vagrant automates, hypervisor executes |
| Why Git Bash on Windows?                 | Linux CLI commands in a Windows environment                          |
| How to reset to correct project state?   | Checkout the right branch in the GitHub repo                         |

***

This completes the full analysis of the caption file. All unique information has been preserved, no external concepts were introduced, and each section serves its distinct purpose — **Theory** for understanding, **Practical** for execution, and **Mental Compression Map** for rapid future recall. [\[07-tools-p...nformation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/07-tools-prerequisite-information.txt)
