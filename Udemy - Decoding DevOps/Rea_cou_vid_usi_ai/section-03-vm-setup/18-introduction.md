# 🎓 Complete Deep Learning Material — Introduction to VM Creation for Linux Practice

**Source:** [18-introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt?EntityRepresentationId=32c89017-3ec2-4b59-af3d-2aab438ea635) — Introductory lecture on creating Virtual Machines (VMs) for Linux practice, covering manual and automated approaches, required tools, and foundational DevOps engineering principles. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Goal: Why We Create Virtual Machines for Linux Practice

The overarching objective of this section is to create **two Linux Virtual Machines** — one running **CentOS** and the other running **Ubuntu**. These are two of the most widely used distributions (flavors) of the Linux operating system. The differences between CentOS and Ubuntu are not covered here; they will be explored in depth in a dedicated Linux section later. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

The reason for creating VMs instead of installing Linux directly on the physical machine is foundational: VMs provide **isolated, disposable, repeatable environments** for safe practice. You can break things, experiment, rebuild — without affecting your host operating system. This is the standard engineering approach in DevOps and systems work.

> 🔍 **Deep Dive:** Even if your host machine already runs Linux as a desktop OS, you still need to create separate Linux VMs. This is because the course exercises depend on a controlled, reproducible VM environment — not your personal desktop configuration. The VMs serve as **standardized practice sandboxes** for everyone regardless of host OS. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

The course follows a **progressive infrastructure path**: initially, all practice happens on **local VMs** running on your own computer. Later, the course migrates to **AWS (Amazon Web Services)**, where everything moves to cloud computing. Local VMs are the training ground before operating in production-grade cloud environments. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 1.2 — Two Methods of VM Creation: Manual vs. Automated

There are exactly **two methods** for creating VMs taught in this course: [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

### Manual Method

The manual method is a **wizard-based, step-by-step** process. You walk through a graphical interface, select multiple options (such as memory, disk size, OS type), and configure the VM by hand. You then **download an ISO file** (the operating system installation image) and attach it to the VM to install the operating system manually. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

Every step is visible, every decision is explicit. This is intentionally slow and deliberate — because the purpose is **learning**, not speed.

### Automated Method

The automated method replaces the entire manual process with a **text file and a single command**. You create a configuration file (called a **Vagrantfile**), specify what you want (including the **box name**, which identifies the OS image), and issue the command `vagrant up`. The VM is created and brought to a running state automatically. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

This is faster, simpler, and reproducible — but it hides all the underlying steps.

***

## 1.3 — The Manual-First Automation Principle (Core DevOps Thinking)

This is the **most important engineering principle** taught in this lecture, and the instructor emphasizes it with strong language ("never, ever forget this rule in your DevOps career"): [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

> **If you want to automate something, make sure you know how to do it manually first.**

The reasoning is precise and structural:

* When you perform a task **manually**, you learn **each and every step** — the "entire recipe."
* **Automation** is nothing more than **assembling all those manual steps together in a logical way**, using a tool, scripting, or any programming language. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

This means automation is not a replacement for understanding — it is a **layer built on top of understanding**. If you don't know the manual steps, you cannot debug automation when it fails, you cannot customize it, and you cannot extend it to new situations.

This is why the course teaches the manual method first, even though the automated method is faster and simpler.

> 🔍 **Deep Dive:** This principle maps to a universal engineering pattern: **Recipe → Assembly**. First, you discover and validate each individual step (the recipe). Then, you encode those steps into an automated sequence (the assembly). In DevOps, this translates directly to workflows like: manually configuring a server → writing an Ansible playbook; manually deploying an app → writing a CI/CD pipeline; manually provisioning infrastructure → writing Terraform code. The manual phase is the **knowledge acquisition** phase. The automation phase is the **knowledge encoding** phase. Skipping the first phase produces brittle, poorly understood automation. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

> ⚠️ **Expert Note:** In real-world DevOps, the most dangerous automation is automation written by someone who never did the task manually. When it breaks (and it will), nobody understands the underlying steps well enough to diagnose the failure. The manual-first rule is a **reliability and debugging insurance policy**.

***

## 1.4 — The Hypervisor: Oracle VM VirtualBox

A **hypervisor** is the software layer that makes virtual machines possible. It sits between the physical hardware and the virtual machines, allocating resources (CPU, memory, disk, network) to each VM. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

The hypervisor used in this course is **Oracle VM VirtualBox**. The instructor explicitly asks you to remember this name and to **not use any other hypervisor** (such as VMware Desktop or others) during the course. The reason is **standardization** — ensuring everyone follows the same steps, sees the same interfaces, and encounters the same behavior. This eliminates variables when troubleshooting. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Exception:** If you are on **MacOS with an M1 or M2 chip** (Apple Silicon), VirtualBox is not compatible. A **different tool** is used instead, covered in a separate dedicated lecture. This exception exists because Apple Silicon uses ARM architecture, which VirtualBox (designed for x86/x64) does not natively support. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 1.5 — ISO Files: The Operating System Installation Images

An **ISO file** is a complete disk image of an operating system installer. It is the digital equivalent of a physical installation DVD. In this course, you download ISO files for **CentOS** and **Ubuntu**. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

These ISO files are **attached to the VM** (mounted as a virtual CD/DVD drive), and the operating system is installed from them during the manual VM creation process. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

This concept only applies to the manual method. In the automated method, Vagrant handles OS provisioning internally through **box images** (pre-built VM templates), so you don't manually download or attach ISO files.

***

## 1.6 — Vagrant: The Automation Engine

**Vagrant** is the tool used for the automated VM creation method. It abstracts away all the manual steps — VM creation, OS installation, configuration — into a declarative workflow. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

The core workflow is:

1. Create a **Vagrantfile** — a text-based configuration file.
2. Specify the **box name** — an identifier that tells Vagrant which pre-built OS image to use.
3. Run the command **`vagrant up`** — Vagrant reads the file, downloads the box (if needed), creates the VM in VirtualBox, and starts it. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

Vagrant still requires a hypervisor underneath (VirtualBox for Windows and MacOS Intel). It does not replace the hypervisor — it **orchestrates** it. Vagrant is the **controller**; VirtualBox is the **worker** that actually runs the VM.

> 🔍 **Deep Dive:** This is a classic **controller/worker** or **orchestrator/engine** pattern. Vagrant issues instructions; VirtualBox executes them. The Vagrantfile is the **declarative specification** — it says *what* you want, not *how* to build it step by step. This same pattern appears in Terraform (controller) + AWS (worker), Ansible (controller) + target servers (workers), Kubernetes (controller) + container runtime (worker). Recognizing this pattern early builds strong architectural intuition. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 1.7 — Login Tools: Git Bash and Putty

Once a VM is running, you need a way to **connect to it** (log in remotely via terminal). Two login tools are mentioned: **Git Bash** and **Putty**. Both will be demonstrated. These are SSH clients that allow you to open a terminal session into the running Linux VM from your host machine. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 1.8 — Prerequisites and System Requirements

**Hardware requirements:** A **64-bit computer** with a **high-speed internet connection** (needed for downloading ISO files, Vagrant boxes, and later for AWS operations). [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Supported host operating systems:** Windows 10 or 11, MacOS with Intel chip, MacOS with M1/M2 chip, or Linux. The course accommodates all major platforms, with platform-specific instructions where needed (especially for Apple Silicon). [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Prerequisite tools:** The course has a **prerequisites section** where all necessary tools were already installed. The instructor assumes you have completed that section and have all tools ready before proceeding. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 1.9 — Tool Matrix by Method and Platform

| Method    | Tool                              | Platform                    | Purpose                        |
| --------- | --------------------------------- | --------------------------- | ------------------------------ |
| Manual    | Oracle VM VirtualBox              | Windows, MacOS Intel, Linux | Hypervisor — runs VMs          |
| Manual    | ISO files (CentOS, Ubuntu)        | All                         | OS installation images         |
| Manual    | Git Bash / Putty                  | All                         | SSH login to VMs               |
| Automated | Oracle VM VirtualBox              | Windows, MacOS Intel        | Hypervisor (worker)            |
| Automated | Vagrant                           | Windows, MacOS Intel        | Automation engine (controller) |
| Automated | Vagrantfile                       | All                         | Declarative VM configuration   |
| Both      | Different tool (separate lecture) | MacOS M1/M2                 | Replaces VirtualBox            |

 [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up **two Linux virtual machines** — one CentOS, one Ubuntu — on our local computer. These VMs will serve as the practice environment for all Linux exercises in the course. We will do this using **two approaches**: first manually (to learn every step), then automatically using Vagrant (to learn efficient, repeatable provisioning). The final outcome is two running, accessible Linux VMs that we can SSH into and use for hands-on practice. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## Lab 1: Manual VM Setup

### Step 1 — Open Oracle VM VirtualBox

Launch VirtualBox on your machine. This is the hypervisor that will host your VMs. It should already be installed from the prerequisites section. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Verification:** VirtualBox opens without errors and shows the main manager window.

**Common mistake:** Using a different hypervisor (VMware, Hyper-V, etc.). The course requires VirtualBox specifically for consistency. If you're on MacOS M1/M2, refer to the separate dedicated lecture for the alternative tool. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

### Step 2 — Create a New VM (Wizard-Based)

Inside VirtualBox, initiate the creation of a new VM. This is a **wizard-based process** where you will select multiple options: VM name, OS type, memory allocation, disk configuration, etc. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

The specific options and detailed walkthrough are covered in the next lecture. This introductory lecture establishes that the process is **step-by-step and visual** — you make explicit choices at each stage. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Connection to system flow:** This step creates the **empty container** — a VM with allocated resources but no operating system yet.

### Step 3 — Download ISO Files (CentOS and Ubuntu)

Download the ISO installation files for both CentOS and Ubuntu. These are the operating system images that you will install onto your VMs. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**What to look for:** Ensure you download the correct architecture (64-bit) matching your hardware.

**Connection to system flow:** The ISO file is the **input** that transforms an empty VM into a functional Linux system.

### Step 4 — Attach ISO and Install Operating System

Mount the downloaded ISO file to the VM (as a virtual CD/DVD) and boot the VM from it. Follow the OS installation wizard to install Linux on the VM. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Connection to system flow:** After this step, your VM transitions from an empty container to a **bootable Linux system**.

### Step 5 — Connect to the VM Using Git Bash or Putty

Once the VM is running with the OS installed, use **Git Bash** or **Putty** to SSH into the VM. Both tools will be demonstrated in subsequent lectures. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Verification:** You get a Linux terminal prompt inside your SSH client, confirming the VM is accessible and the OS is operational.

> ⚠️ **Expert Note:** The manual process is deliberately slow. Resist the urge to skip ahead to automation. Every option you select in the wizard, every step you perform — this is the "recipe" that automation will later encode. Understanding these steps is what makes you capable of debugging Vagrant or any other automation tool when things go wrong. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## Lab 2: Automated VM Setup

### Step 1 — Ensure VirtualBox and Vagrant Are Installed

Vagrant requires a hypervisor underneath it. On **Windows** and **MacOS Intel**, this is VirtualBox. On **MacOS M1/M2**, use the alternative tool from the separate lecture. Vagrant itself should also be installed from the prerequisites section. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Verification:** Run `vagrant --version` in your terminal to confirm Vagrant is installed and accessible.

### Step 2 — Create a Vagrantfile

Create a **Vagrantfile** — a plain text configuration file that tells Vagrant what VM to create. Inside this file, you specify the **box name**, which identifies the pre-built OS image Vagrant should use. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**What is a box name?** It's a reference to a pre-packaged VM image (e.g., `centos/7`, `ubuntu/focal64`). Vagrant downloads this image automatically if it's not already cached locally. [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**Connection to system flow:** The Vagrantfile is the **declarative specification** — the single source of truth for what your VM should look like. It replaces all the manual wizard selections.

### Step 3 — Run `vagrant up`

```bash
vagrant up
```

**Command breakdown:**

* **`vagrant`** — the Vagrant CLI tool
* **`up`** — the subcommand that tells Vagrant to read the Vagrantfile, create the VM, download the box if needed, and start the VM [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

**What happens internally:**

1. Vagrant reads the Vagrantfile in the current directory.
2. It identifies the box name and checks if the box image is cached locally.
3. If not cached, it downloads the box from the Vagrant Cloud registry.
4. It instructs VirtualBox to create a new VM with the specifications.
5. It boots the VM and provisions it.
6. The VM is up and running — ready for SSH access.

**Verification:** Vagrant outputs progress logs during execution. The final state should show the VM running. You can verify with `vagrant status`.

**Common mistake:** Running `vagrant up` from a directory that doesn't contain a Vagrantfile. Vagrant looks for the file in the **current working directory**.

> 🔍 **Deep Dive:** Notice the dramatic difference in effort: Lab 1 required multiple manual steps (create VM, download ISO, attach ISO, install OS, configure). Lab 2 collapsed all of that into **one file + one command**. This is the power of automation — but it only works reliably when the person writing the Vagrantfile understands every step it replaces (the manual-first principle in action). [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ System Architecture

```
HOST MACHINE (Windows / MacOS / Linux)
  │
  ├── Oracle VM VirtualBox (Hypervisor)
  │     ├── VM 1: CentOS (Linux)
  │     └── VM 2: Ubuntu (Linux)
  │
  ├── Vagrant (Automation Controller)
  │     ├── Reads → Vagrantfile (declarative config)
  │     ├── Downloads → Box image (pre-built OS)
  │     └── Instructs → VirtualBox (create + start VM)
  │
  └── SSH Clients (Git Bash / Putty)
        └── Connect to → Running VMs
```

 [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 🔗 Core Relationship Chain

```
Manual-first principle
  └── Do manually → learn recipe → encode into automation

Manual method:
  VirtualBox → Create VM (wizard) → Attach ISO → Install OS → SSH in

Automated method:
  Vagrantfile (box name) → vagrant up → VirtualBox creates VM → VM runs → SSH in

Vagrant ←controls→ VirtualBox
Vagrant = Controller | VirtualBox = Worker
Vagrantfile = Declarative spec | ISO = Raw installer
```

 [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 🔑 Key Retrieval Anchors

| Concept          | Compressed Recall                                              |
| ---------------- | -------------------------------------------------------------- |
| Two VMs          | CentOS + Ubuntu (two Linux flavors)                            |
| Two methods      | Manual (wizard + ISO) → Automated (Vagrantfile + `vagrant up`) |
| Core rule        | **Manual first, automate second** — recipe before assembly     |
| Hypervisor       | Oracle VM VirtualBox (not VMware, not others)                  |
| M1/M2 exception  | Separate tool, separate lecture                                |
| Vagrant workflow | Vagrantfile → box name → `vagrant up`                          |
| ISO purpose      | OS installation image, attached to VM (manual only)            |
| Login tools      | Git Bash or Putty (SSH into VM)                                |
| Course path      | Local VMs → AWS cloud (progressive infrastructure)             |
| Prerequisites    | Already installed in earlier section                           |

 [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## ⚡ Reusable Engineering Patterns

| Pattern                             | Instance in This Lecture                               |
| ----------------------------------- | ------------------------------------------------------ |
| **Manual-First Automation**         | Learn steps manually → encode into Vagrant             |
| **Controller / Worker**             | Vagrant (controller) → VirtualBox (worker)             |
| **Declarative Specification**       | Vagrantfile defines *what*, not *how*                  |
| **Progressive Infrastructure**      | Local VMs → Cloud (AWS)                                |
| **Standardization for Consistency** | Everyone uses same hypervisor → same experience        |
| **Platform Adaptation**             | M1/M2 gets separate tooling; core workflow unchanged   |
| **Recipe → Assembly**               | Manual steps = recipe; Automation = assembly of recipe |

 [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 🔄 Execution Flow (Compressed)

```
MANUAL:
  Install VirtualBox ✓ (prereqs)
  → Open VirtualBox
  → Create VM (wizard options)
  → Download ISO (CentOS / Ubuntu)
  → Attach ISO → Boot → Install OS
  → SSH in (Git Bash / Putty)
  → ✅ Working Linux VM

AUTOMATED:
  Install VirtualBox + Vagrant ✓ (prereqs)
  → Create Vagrantfile (specify box name)
  → Run: vagrant up
  → Vagrant → VirtualBox → VM created + started
  → SSH in
  → ✅ Working Linux VM
```

 [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)

***

## 🧭 One-Line Mental Reload

> **Two Linux VMs (CentOS + Ubuntu) created two ways — manually via VirtualBox wizard + ISO to learn the recipe, then automatically via Vagrant + Vagrantfile + `vagrant up` to encode that recipe — because you must always understand manually before you automate.** [\[18-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/18-introduction.txt)
