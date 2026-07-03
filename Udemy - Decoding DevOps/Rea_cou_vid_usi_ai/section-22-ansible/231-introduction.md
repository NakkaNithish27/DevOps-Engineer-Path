# 🎓 Deep Learning Material: Introduction to Ansible — History, Architecture & Core Concepts

**Source:** [231-introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt?EntityRepresentationId=ff0fd657-76c9-492b-bc5f-271aa3730228) — Video lecture introducing Ansible as a DevOps automation tool, covering the history of automation (from bash scripting through configuration management tools to Ansible and Terraform), Ansible's architecture (agentless, control machine, inventory, modules, playbooks), how it connects to targets (SSH, WinRM, APIs), its execution model (remote vs. local), and its position in the modern automation landscape. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The History of Automation — Why Ansible Exists

Ansible didn't appear in a vacuum. Understanding the automation tools that came before it — and the problems each solved and created — is essential to understanding why Ansible was designed the way it was. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Phase 1: OS-Level Scripting

The earliest automation was **operating-system-specific scripting**. **Bash scripting** automated Linux tasks. **Batch scripting** automated Windows tasks. These were powerful for their target platform but limited in scope — they could automate OS tasks on a single machine, but as infrastructure grew beyond a single operating system into virtualization, cloud computing, databases, and build systems, scripting alone became insufficient. There was a need to automate things beyond just operating system commands. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Phase 2: Programming Languages for Automation

System administrators and operations teams began adopting general-purpose programming languages for broader automation: **Perl**, then **Python**, then **Ruby** — in that historical order. Among these, **Python won the race** because of its enormous library ecosystem — libraries existed to automate virtually anything (cloud tasks, database operations, virtualization management). Perl was also popular but became "too much complicated" with excessive syntax complexity. Separately, **PowerShell** emerged as a Windows-specific automation language, though it could also automate other things like VMware. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Phase 3: Configuration Management Tools

The next evolutionary step was purpose-built **configuration management tools**. These were fundamentally different from scripts and programming — they introduced the concept of **desired state management**.

**Puppet** was the first major tool in this category. Its original perspective was not "run these commands" but "ensure this state." Consider a cluster of web servers — all should have identical configuration, identical packages, identical service states. But over time, manual changes cause **configuration drift** — servers go out of sync. Some config file gets edited, a service stops, a package version diverges. Puppet solved this by establishing a **centralized Puppet server** that held the desired configuration of all servers. Every managed machine had a **Puppet agent** that regularly queried the Puppet server, checked whether its current state matched the desired state, and corrected any deviations. The configuration state across your entire infrastructure was enforced like a law from the central server. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

When the DevOps movement arrived, Puppet started being adopted as an automation tool — not just for state management, but for actively setting up and configuring infrastructure. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

**Salt Stack** emerged alongside Puppet. It was "very nice and simple" for executing commands on remote machines. A popular combination was using **Salt Stack for initial setup** (bootstrapping machines, running Puppet agents) and **Puppet for ongoing configuration management**. This combination-of-tools approach was common — multiple automation tools working together, each handling what it did best. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

**Chef** came next, offering "more manageability and more power." Unlike Puppet's domain-specific language (DSL), Chef gave users the power to write **Ruby code** directly. It had more templating features, a strong graphical user interface for reports and management. But with all these features came **more complications** — "too many moving parts." Chef had a server, a client, and a workstation — three components to manage before you could automate anything. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

Important note from the instructor: Puppet and Chef are not bad tools. The choice between tools is a matter of **use case and personal inclination**. Each tool has strengths in specific contexts. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

A key detail about all three (Puppet, Chef, Salt Stack): they are **built on** programming languages (Puppet and Chef on Ruby, Salt Stack on Python), but you don't write Ruby or Python code to use them. Each has its **own language** — Puppet has its DSL (Domain Specific Language), Chef uses Ruby-based recipes, Salt Stack has its own state files. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Phase 4: Ansible

And then came **Ansible**, developed by **Michael DeHaan**, written in **Python**, and later **acquired by Red Hat**. Ansible was another configuration management tool, but it was designed with a radically different principle: **simplicity**. Out of all the tools in the automation landscape, the instructor calls Ansible "the most simplest automation tool." [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

Ansible initially focused on **Linux machines**, then expanded to Windows automation, cloud automation, networking equipment automation, database automation, and many more integrations. Being simple, it also became very powerful through this breadth of integration. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Phase 5: Infrastructure-as-Code (IaC) Tools

The video also mentions **Terraform** and **CloudFormation** as tools that emerged for **cloud-specific automation**. While Ansible can do cloud automation, Terraform is described as "more cloud specific automation tool" — its specialization is in provisioning and managing cloud infrastructure. The instructor notes that if you're doing heavy cloud automation, Terraform may be better suited than Ansible for that particular use case, while Ansible excels at system-level automation, configuration, and orchestration. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

## 1.2 Ansible's Core Design Principles

### Simplicity

This is Ansible's founding principle and the instructor repeats it throughout the lecture: "Ansible was built on the principle of simplicity." The code (called **playbooks**) is written in **YAML** — a format that is easy to read and easy to write, structured, and has "very less complication compared to any programming language." You don't need to know a programming language to use Ansible. The instructor explicitly advises: "try to keep your code as simple as possible." Ansible has many features, but you should use them only when the need arises, not because they exist. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Agentless Architecture

This is the most architecturally significant difference between Ansible and its predecessors (Puppet, Chef, Salt Stack). In Puppet, Chef, and Salt Stack, you have a **server** that manages configuration, and every target machine needs an **agent** installed. If you manage 100 servers, you install agents on all 100 machines. These agents run as services, consume resources, need updating, and add operational complexity. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

Ansible has **no agents**. It uses **existing connection methods** that are already present on target machines:

* **Linux** → SSH (already running on every Linux server — Ubuntu, CentOS, RHEL)
* **Windows** → WinRM (already present, just needs remote connection enabled in PowerShell)
* **Cloud** (AWS, Azure, GCP) → APIs (RESTful calls; for AWS specifically, Ansible uses the **boto** library)
* **Network devices** (switches, routers) → Ansible's network modules
* **Databases** → Python libraries (e.g., Python MySQL library for MySQL)

You don't need to set up anything on the target machine. You just need the connection details (IP, username, password/key), and Ansible can connect and manage. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

🔍 **Deep Dive**
The instructor makes an important terminological distinction: Ansible's central machine is called the **control machine**, not the "Ansible server." This is deliberate. Puppet Server, Chef Server, and Salt Master all run persistent **services** — daemon processes that are always active, listening for agent connections. Ansible does **not** run any service. It is a command-line tool (technically a Python library) that executes when you invoke it and stops when it's done. There is no persistent daemon, no listening port, no always-on process. Calling it a "server" would misrepresent its nature. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### No Complex Storage

Ansible has no database, no complicated storage backend. Your playbooks, scripts, and configuration are stored in **YAML, INI, or text format** — simple, human-readable files. Output is returned in **JSON format**. There is no state database to manage, no complex backend to maintain. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Simple Setup and Upgrade

Installing Ansible is trivial: it is a **Python library**, so you can install it with `pip install ansible` or through your operating system's package manager. Upgrading is equally simple. There is no multi-component installation, no server/client/workstation setup like Chef. You install it and start using it immediately. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### No Residual Software

When Ansible runs, it creates Python scripts, sends them to the target, executes them, and gets the output back. After execution, **there is no residual software left** on the target machine or even on the control machine beyond the Ansible installation itself. Nothing is left behind — no agent process, no daemon, no temporary services. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

## 1.3 How Ansible Works — The Execution Model

The instructor describes this not as a "great architecture" but as a practical explanation of "how it really works." Ansible's operational model has four core components: **Inventory**, **Modules**, **Playbooks**, and the **Execution Engine**. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Inventory

The **inventory file** is where you define your target machines. It contains the information Ansible needs to connect: IP addresses, usernames, passwords (or SSH key references). This is the "who" — which machines does Ansible manage? The inventory can be a simple INI or YAML file listing hosts and groups. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Modules

Ansible has **hundreds — more than 1000 — built-in modules**, each designed to do a particular task. One module installs a package. Another restarts a service. Another takes a snapshot of an EBS volume. Another launches an EC2 instance. Modules are the atomic units of work in Ansible — each one knows how to perform a specific operation on a specific type of target. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

Modules come in different categories:

* **System modules** — manage OS-level tasks (packages, services, files, users)
* **API-based modules** — interact with cloud services, network equipment, databases
* **Command/shell modules** — execute existing shell commands, PowerShell commands, or scripts directly [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

You can also execute existing scripts through Ansible — if you have bash scripts, you can run them via Ansible without rewriting them. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Playbooks

A **playbook** is the Ansible code file (written in YAML) where you describe what you want to happen. In a playbook, you define **tasks**. Each task says: "On this host (from the inventory), execute this module." A playbook is a sequence of such tasks. Because it's YAML, if you write clear titles for your tasks, the playbook itself can serve as **documentation** — "it's not going to be very complicated script to understand." [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

### Execution Flow

When you execute a playbook, Ansible's engine:

1. Reads the playbook to understand what tasks to run on which hosts.
2. Reads the inventory to get connection details for those hosts.
3. Uses the Ansible configuration to create **Python scripts** (technically **Python packages** — groups of Python modules, as covered in the Python course).
4. **Delivers** the Python package to the target machine and **executes it there**, then **returns the output** — this is the **remote execution** path (used for Linux via SSH, Windows via WinRM).
5. **OR**, if the target is not an operating system but something like a cloud account (e.g., launching an EC2 instance via API), Ansible creates the Python package and **executes it locally** on the control machine — this is the **local execution** path. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

🔍 **Deep Dive**
The distinction between remote and local execution is **entirely dependent on the target type** and is handled automatically by the module. When you use an SSH/WinRM module, Ansible sends scripts to the target. When you use an API-based module (like AWS EC2), there is no remote machine to send scripts to — the API call is made from the control machine itself. The user doesn't need to specify which execution mode to use — "all those things are abstracted from you. Ansible will do all the kind of connection and execution behind the scene." You just use the module and specify the destination; Ansible handles the rest. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

## 1.4 Popular Use Cases of Ansible

The instructor outlines several categories of use:

**System Automation** — Linux and Windows automation: setting up web services, database services, configuring them, starting/restarting services. This is the foundational use case. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

**Change Management** — Managing production servers. Any changes to production infrastructure go through Ansible playbooks. Because playbooks are readable YAML with descriptive task titles, they can double as change documentation. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

**Provisioning** — Setting up infrastructure from scratch. Launch cloud instances (like EC2), then install and configure services (frontend, backend, database, web services) — complete end-to-end provisioning. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

**Orchestration** — Combining multiple automation tools and scripts, executing them in proper order. Ansible integrates with Jenkins, cloud services, and many other tools. It can serve as the orchestrator that ties together different automation components into a coherent workflow. When security is deeply integrated into DevOps CI/CD pipelines alongside tools like Ansible, this is part of the broader **DevSecOps** practice. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

⚠️ **Expert Note**
The instructor gives a pragmatic guideline for tool selection: Ansible *can* replace all other automation tools, but it *shouldn't always*. If you're doing heavy cloud infrastructure management, Terraform is likely better suited. The choice should be based on **need and use case**, not loyalty to a single tool. "But when the time comes, Ansible can do most of the automation that you need." [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

This is an introductory lecture — there is no hands-on lab or command execution. However, it establishes the practical foundation for everything that follows in the Ansible course. The instructor ends with "Enough talk now. Let's get into some action" — meaning the next lectures will begin actual Ansible usage. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

What follows below are the **practical operational facts** extracted from the lecture that you will need when you start working with Ansible.

***

## Practical Fact 1: Installing Ansible

Ansible is a Python library. You can install it with:

```bash
pip install ansible
```

Or through your OS package manager (e.g., `apt install ansible` on Ubuntu, `yum install ansible` on CentOS/RHEL). [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

Upgrading is the same process — `pip install --upgrade ansible` or the equivalent package manager command.

There is no multi-component installation. No server setup. No database initialization. You install one package and you're ready.

***

## Practical Fact 2: What You Need to Create

When working with Ansible, you will create and work with these artifacts:

| Artifact           | Format            | Purpose                                                         |
| ------------------ | ----------------- | --------------------------------------------------------------- |
| **Inventory file** | INI / YAML / text | Lists target machines (IP addresses, usernames, passwords/keys) |
| **Playbooks**      | YAML              | Define tasks — which modules to execute on which hosts          |
| **Configuration**  | INI (ansible.cfg) | Ansible settings (implied — not detailed in this lecture)       |

 [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

There is no database to configure, no server to run, no agents to install on targets.

***

## Practical Fact 3: Connection Requirements by Target Type

Before you can manage a target with Ansible, ensure the following:

| Target Type             | Connection Method       | Prerequisite                                                                         |
| ----------------------- | ----------------------- | ------------------------------------------------------------------------------------ |
| Linux server            | SSH                     | SSH must be running (default on Ubuntu, CentOS, RHEL) — just need SSH credentials    |
| Windows server          | WinRM                   | WinRM service exists but remote connection must be **enabled** in PowerShell         |
| AWS / Azure / GCP       | APIs                    | API credentials configured (for AWS: boto library used by Ansible)                   |
| Network devices         | Ansible network modules | Device-specific access configured                                                    |
| Databases (e.g., MySQL) | Python libraries        | Appropriate Python library installed on control machine (e.g., Python MySQL library) |

 [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

No agents need to be installed on any target. You work with what's already there.

***

## Practical Fact 4: Remote vs. Local Execution — What Happens Operationally

When you run a playbook:

**For OS targets (Linux/Windows):**

1. Ansible creates Python scripts/packages on the control machine.
2. Sends them to the target via SSH (Linux) or WinRM (Windows).
3. Executes them on the target.
4. Returns the output (JSON format) to the control machine.
5. **No residual software** left on the target. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

**For API targets (cloud, network via API):**

1. Ansible creates Python scripts/packages on the control machine.
2. Executes them **locally** on the control machine (API calls go out over the network).
3. Returns the output. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

You don't choose between these modes — the **module** determines the execution mode automatically. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

## Practical Fact 5: Playbook as Documentation

When writing playbooks, give clear, descriptive **titles to your tasks**. Because YAML is human-readable and task titles appear in both the code and the execution output, a well-written playbook can serve directly as change management documentation. This is a practical discipline to adopt from the start. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

## Practical Fact 6: Ansible's Position — When to Use What

| Scenario                                                     | Recommended Tool                                         |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| System automation (Linux/Windows services, packages, config) | **Ansible** (primary strength)                           |
| Configuration management across server clusters              | **Ansible** (replaces Puppet/Chef with simpler approach) |
| End-to-end provisioning (launch + configure)                 | **Ansible**                                              |
| Orchestration (combining tools, ordering execution)          | **Ansible** (integrates with Jenkins, cloud services)    |
| Heavy cloud infrastructure management                        | **Terraform** (more specialized)                         |
| Cloud-specific IaC (AWS only)                                | **CloudFormation**                                       |

 [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

The instructor's guideline: Ansible can do most automation, but match the tool to the use case. If cloud infrastructure is the primary focus, Terraform is likely better. For everything else — and especially for system-level automation, configuration, and orchestration — Ansible is the go-to. [\[231-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/231-introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Automation Evolution Timeline

```
Phase 1: OS Scripting
  Bash (Linux) → Batch (Windows)
  └── Limited to single-OS tasks

Phase 2: Programming Languages
  Perl → Python → Ruby  (+ PowerShell for Windows)
  └── Python won: huge library ecosystem
  └── Broader automation possible but requires coding skill

Phase 3: Configuration Management Tools
  Puppet  → centralized server + agents + DSL → config drift enforcement
  Salt Stack → simple remote command execution (often paired with Puppet)
  Chef    → Ruby-based, more features, more power, MORE COMPLEXITY (server+client+workstation)
  └── All require: SERVER + AGENTS on every target machine

Phase 4: Ansible
  Creator: Michael DeHaan → acquired by Red Hat
  Written in: Python
  Principle: SIMPLICITY
  └── No agents, no server, no database, no residual software
  └── Uses existing connections (SSH, WinRM, APIs)

Phase 5: Cloud IaC
  Terraform → cloud-specific automation
  CloudFormation → AWS-specific
```

***

## Ansible vs. Predecessors (Core Differentiator)

```
Puppet/Chef/Salt Stack              │  Ansible
─────────────────────────────────── │ ──────────────────────────
Server (runs service)               │  Control machine (no service)
Agents on ALL targets               │  NO agents
Complex setup                       │  pip install ansible
DSL / Ruby code                     │  YAML (playbooks)
Database / complex storage          │  Files only (YAML, INI, text)
Persistent daemon                   │  Runs on demand, exits when done
Residual software on targets        │  Nothing left after execution
```

***

## Ansible Architecture

```
CONTROL MACHINE (your laptop/server — NOT a "server")
  │
  ├── Inventory (INI/YAML)     → WHO: target IPs, usernames, credentials
  ├── Playbooks (YAML)         → WHAT: tasks = host + module
  ├── Modules (1000+ built-in) → HOW: one module = one specific task
  └── Configuration            → settings
  │
  │ Execution Engine creates Python packages
  │
  ├──── OS Target (Linux/Windows) ──→ REMOTE EXECUTION
  │     │                              Send scripts via SSH/WinRM
  │     │                              Execute on target → return JSON output
  │     └── No residual software
  │
  └──── API Target (Cloud/Network) ──→ LOCAL EXECUTION
        │                              Execute on control machine
        │                              API calls go to cloud/network
        └── No script sent anywhere
```

***

## Connection Method Map

```
Target         → Connection    → Prerequisite
───────────────────────────────────────────────
Linux          → SSH           → Already running (nothing to do)
Windows        → WinRM         → Enable remote connection in PowerShell
AWS            → API (boto)    → API credentials configured
Azure/GCP      → API           → API credentials configured
Network        → Modules       → Device access configured
Database       → Python lib    → e.g., Python MySQL library on control machine
```

***

## Ansible Use Cases

```
System Automation   → Linux/Windows services, packages, config
Change Management   → Production changes via playbooks (doubles as documentation)
Provisioning        → Launch cloud instances + configure from scratch
Orchestration       → Combine tools (Jenkins, cloud) + execute in order
```

***

## Execution Model (Two Paths)

```
Playbook executed
  │
  ├── Module type = system (SSH/WinRM target)
  │     → Create Python package
  │     → SEND to target
  │     → Execute REMOTELY
  │     → Return JSON output
  │     → Clean up (no residue)
  │
  └── Module type = API (cloud/network target)
        → Create Python package
        → Execute LOCALLY on control machine
        → API calls reach target
        → Return JSON output
```

Decision: automatic (module determines path). User doesn't specify.

***

## Tool Selection Guide

```
System/config automation  → Ansible (strongest)
Orchestration             → Ansible (integrates with everything)
Provisioning (full stack) → Ansible
Heavy cloud IaC           → Terraform (specialized)
AWS-only IaC              → CloudFormation

Rule: Ansible CAN do almost everything, but match tool to primary use case
```

***

## Ansible's Design Principles (Recall Anchors)

```
SIMPLE     → YAML, no programming language needed
AGENTLESS  → SSH / WinRM / API — uses what's already there
CLEAN      → no database, no complex storage, files only
POWERFUL   → 1000+ modules, cloud/network/DB/OS, integrations
EPHEMERAL  → no service running, no residual software, runs and exits
```

***

## Key Terminology

```
Control Machine   ≠  Server (no service runs)
Playbook          =  YAML file defining tasks
Task              =  host + module (from inventory, run this module)
Module            =  atomic unit of work (install package, restart service, launch EC2)
Inventory         =  list of targets + connection details
Python Package    =  what Ansible creates and sends/executes (group of Python modules)
```

***

## Puppet's Configuration Drift Model (Context for Ansible)

```
Cluster of servers → should be identical config
  └── Manual changes → config drift (out of sync)
      └── Puppet server holds DESIRED state
          └── Puppet agents on each machine POLL server regularly
              └── Agent corrects drift → enforces state

Ansible's alternative: no agents, no polling, no central server
  → Run playbook ON DEMAND → apply desired state → exit
```

***

## Project Continuity

```
THIS LECTURE:  Conceptual foundation — what Ansible is, why it exists, how it works
NEXT LECTURE:  Hands-on action begins — actual Ansible usage, commands, playbooks
```

***

This completes the full reconstruction. **Theory** builds the complete conceptual foundation — from automation history through Ansible's architecture and execution model. **Practical** extracts every operationally relevant fact you'll need when you start using Ansible. The **Compression Map** lets you mentally reload the entire landscape — evolution, architecture, execution paths, tool selection — in under two minutes. Let me know if you'd like Anki flashcards or any section expanded! 🚀
