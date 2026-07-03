# 🎓 Deep Learning Material: Ansible Infrastructure Setup — Control Machine, Clients & SSH Fingerprints

**Source:** [232-setup-ansible-and-infra.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt?EntityRepresentationId=d09a5813-491e-4974-a4c1-0b6af8ede280) — Video lecture covering the setup of an Ansible control machine on Ubuntu EC2, launching CentOS client EC2 instances (web + DB servers), SSH fingerprint mechanics and the `known_hosts` file, security group configuration for Ansible SSH connectivity, and installing Ansible from the Ubuntu PPA repository. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Ansible Architecture — Control Machine and Client Machines

Ansible operates on a **controller/worker architecture** with one critical simplification: the worker machines (called "clients," "targets," or "managed nodes") do not need Ansible installed on them. The entire Ansible engine runs on a single machine called the **control machine**. The control machine connects to client machines over **SSH**, translates the automation code into Python scripts, pushes those scripts to the target machines, and executes them remotely. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

In this setup, the infrastructure consists of four EC2 instances:

* **1 control machine** — Ubuntu 22, where Ansible is installed. This is the command center.
* **2 web servers** (`web01`, `web02`) — CentOS Stream 9. These are the targets Ansible will configure.
* **1 DB server** (`db01`) — CentOS Stream 9. Another target Ansible will configure.

Later, the course will also add an **Ubuntu EC2 instance** as an additional web server, introducing multi-OS management. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

The key architectural insight is: **you do not install Ansible on client machines.** These machines only need SSH (which EC2 instances already have by default). Ansible leverages the existing SSH infrastructure — the same SSH you use to manually log in is the same SSH Ansible uses to automate. No agent, no daemon, no special software on the targets. This is what makes Ansible "agentless." [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

🔍 **Deep Dive**
The video mentions that Ansible code written on the control machine gets **translated to Python scripts** that run on the **target machines**, not on the control machine itself. Different Ansible modules may use different Python interpreters (Python 2 or Python 3) on the client side. The control machine only runs Python scripts locally when you explicitly target `localhost`. This means the Python environment that matters most is the one on the client machines — that's where the actual execution happens. Ansible on the control machine is itself a Python library, and it installs Python 3 (and potentially Python 2) as dependencies. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## 1.2 Security Group Design for Ansible — Why Two SSH Rules

The security group configuration reveals the network architecture that makes Ansible work. The **control machine** has a simple security group (`control-sg`): SSH (port 22) from "My IP" only. This lets you — the human operator — SSH into the control machine to run Ansible commands. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

The **client machines** (web and DB servers) have a different security group (`client-sg`) with **two** SSH rules:

1. **Port 22 from "My IP"** — So you can manually SSH into these machines for debugging or verification.
2. **Port 22 from the control machine's security group (`control-sg`)** — So that Ansible, running on the control machine, can SSH into these clients to execute automation.

The second rule is critical. Without it, Ansible on the control machine would be unable to reach the client machines, and every automation attempt would fail with a connection error. The instructor explicitly warns: "Be careful in this one. Otherwise Ansible will not be able to SSH or connect to these machines." [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

This is the same **security-group-referencing pattern** seen in previous lectures — using a security group ID as the source rather than an IP address. It means: "allow any machine that belongs to `control-sg` to connect on port 22." [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## 1.3 SSH Fingerprints and the `known_hosts` File

The video dedicates significant time to explaining SSH fingerprints because this concept directly impacts how Ansible operates. This is not just SSH trivia — it's a prerequisite for understanding a problem Ansible must solve.

When you SSH into any machine **for the first time**, the SSH client displays a message: "The authenticity of host ... can't be established. Are you sure you want to continue connecting?" This message presents the machine's **fingerprint** — a cryptographic identifier unique to that specific machine. The instructor emphasizes: "These are not SSH keys. These are called fingerprints." SSH keys are for authentication (proving who you are). Fingerprints are for **identity verification** (proving which machine you're connecting to). [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

When you type `yes`, two things happen: (1) the connection proceeds, and (2) the fingerprint is stored in a file at `~/.ssh/known_hosts`. On all subsequent SSH connections to the same machine, the SSH client checks the incoming fingerprint against the stored one in `known_hosts`. If they match, the connection proceeds silently — no question asked. If they don't match (which could indicate a man-in-the-middle attack or a machine replacement), SSH will warn or refuse the connection. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

The video demonstrates this cycle completely:

1. **First SSH** → Question appears → type `yes` → fingerprint stored → connected.
2. **Second SSH** → No question → connected immediately (fingerprint already known).
3. **Clear `known_hosts`** → Fingerprint data is lost.
4. **Third SSH** → Question appears again (machine is "unknown" again).

The `known_hosts` file lives at `~/.ssh/known_hosts` and contains fingerprint entries for every machine you've connected to. Each entry includes the IP address and the fingerprint data. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

The instructor clears the file using: `cat /dev/null > ~/.ssh/known_hosts`. This redirects "nothing" (`/dev/null`) into the file, effectively emptying it. After clearing, the next SSH attempt asks the fingerprint question again because the file no longer contains any stored fingerprints. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**Why this matters for Ansible:** Ansible connects to client machines via SSH. When Ansible connects to a machine for the first time, the same fingerprint question arises. But Ansible runs non-interactively — there's no human to type `yes`. This creates a problem that must be resolved differently. The instructor foreshadows: "We are going to resolve that very differently" — the solution will be covered in upcoming lectures. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## 1.4 CentOS AMI Selection from the AWS Marketplace

The client machines use **CentOS Stream 9** instead of Ubuntu. This is selected through the AWS Marketplace: Browse More AMIs → AWS Marketplace → search "CentOS 9" → select "CentOS Stream 9 by Amazon Web Services." The instructor notes that this AMI is **free** as long as you use it with `t2.micro` or `t3.micro` instance types — there's no additional marketplace charge beyond normal EC2 costs. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

A critical detail: the **login username** for CentOS AMIs is `ec2-user`, not `ubuntu`. This is displayed on the AMI selection page. Different AMIs have different default usernames — a common source of SSH login failures. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## 1.5 Key Pair Separation — Control vs. Client

Two separate key pairs are created:

* **`control`** (`.pem`) — For the control machine. Used by you to SSH into the control machine.
* **`client-key`** (`.pem`) — For all three client machines. This key will also be needed by Ansible to connect to the clients.

The separation is deliberate — the control machine and client machines are different tiers with different access patterns. The control machine is accessed by you; the client machines are accessed by both you and Ansible. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## 1.6 Installing Ansible — Package Manager Approach

Ansible is installed on the control machine (Ubuntu) using `apt`, the standard Ubuntu package manager. The process involves three steps: update the package index, add the Ansible PPA (Personal Package Archive) repository, and install Ansible. The Ansible installation documentation at `docs.ansible.com` covers multiple installation methods (pip, apt, platform-specific) for multiple operating systems (Fedora, Ubuntu, Debian, Windows). The video follows the Ubuntu-specific instructions. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

The instructor notes that Ansible is "basically a Python library" — it's written in Python and installs Python dependencies (Python 3, and potentially Python 2) alongside it. After installation, `ansible --version` shows the installed version (2.4.6 in the video, though versions will vary), the Python version Ansible is using, and the path to the Ansible configuration file. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

⚠️ **Expert Note**
The instructor emphasizes that Ansible documentation is "very readable" and will be referenced heavily throughout the course. This establishes a workflow pattern: use official documentation as the primary reference for installation, configuration, and module usage — not memorization. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up the foundational Ansible infrastructure: one control machine with Ansible installed, and three target machines (two web servers + one DB server) that Ansible will manage. We also configure security groups to enable SSH connectivity between the control machine and the targets. The final outcome: Ansible is installed and ready on the control machine, all target machines are running, and the network allows the control machine to SSH into every target. The next lecture will cover actually connecting Ansible to these targets using an inventory file. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## Step 1: Launch the Control Machine

Navigate to **EC2 → Launch Instance**.

**1a. Configure the instance:**

| Setting       | Value      |
| ------------- | ---------- |
| Name          | `control`  |
| AMI           | Ubuntu 22  |
| Instance type | `t2.micro` |

 [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**1b. Create a key pair:**

| Setting       | Value     |
| ------------- | --------- |
| Key pair name | `control` |
| Format        | `.pem`    |

Click **Create key pair**. The `.pem` file downloads automatically. Keep it safe. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**1c. Configure the security group:**

Click **Edit network settings**. Create a new security group:

| Setting | Value                        |
| ------- | ---------------------------- |
| Name    | `control-sg`                 |
| Rule    | SSH (port 22) from **My IP** |

 [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**1d. Launch the instance.**

While it provisions, proceed to launch the client machines. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## Step 2: Launch Three Client Machines (Web + DB) Simultaneously

Navigate to **EC2 → Launch Instance**.

**2a. Configure the instances:**

| Setting                 | Value                                                            |
| ----------------------- | ---------------------------------------------------------------- |
| Name                    | `vprofile-web00` (temporary — all three get this name initially) |
| **Number of instances** | **3**                                                            |

 [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**2b. Select the CentOS AMI:**

Click **Browse more AMIs → AWS Marketplace**. Search for `CentOS 9`. Select **CentOS Stream 9 by Amazon Web Services**. Click **Subscribe Now**.

Note the login username displayed: **`ec2-user`** (not `ubuntu`). [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

This AMI is free with `t2.micro` / `t3.micro`. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**2c. Set instance type:**

Change to **`t2.micro`**. The video emphasizes: "Make sure you change it to t2.micro." Marketplace AMIs sometimes default to larger instance types. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**2d. Create a key pair:**

| Setting       | Value        |
| ------------- | ------------ |
| Key pair name | `client-key` |
| Format        | `.pem`       |

 [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**2e. Configure the security group:**

Create a new security group:

| Setting     | Value                                              |
| ----------- | -------------------------------------------------- |
| Name        | `client-sg`                                        |
| Description | `client-sg`                                        |
| Rule 1      | SSH (port 22) from **My IP**                       |
| Rule 2      | SSH (port 22) from **control-sg** (security group) |

Rule 2 is critical — this allows Ansible on the control machine to SSH into these clients. Without it, Ansible cannot connect. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**2f. Launch the instances.**

All three launch with the same name tag `vprofile-web00`. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## Step 3: Rename the Client Instances

All three instances have the same name. Rename them in the EC2 console:

| Instance | New Name |
| -------- | -------- |
| 1st      | `web01`  |
| 2nd      | `web02`  |
| 3rd      | `db01`   |

 [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## Step 4: SSH into the Control Machine

Copy the **public IP** of the `control` instance.

```bash
ssh -i ~/Downloads/control.pem ubuntu@<control-public-ip>
```

| Part                         | Meaning                                              |
| ---------------------------- | ---------------------------------------------------- |
| `ssh`                        | Secure Shell client                                  |
| `-i ~/Downloads/control.pem` | Path to the private key file for the control machine |
| `ubuntu`                     | Default username for Ubuntu AMIs                     |
| `@<control-public-ip>`       | Public IP of the control instance                    |

When prompted "Are you sure you want to continue connecting?", type **`yes`**. This stores the machine's fingerprint in `~/.ssh/known_hosts` (see Theory §1.3). [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

***

## Step 5: Understand the SSH Fingerprint Behavior

This step is a learning exercise, not a setup requirement.

**5a. Exit and reconnect:**

```bash
exit
ssh -i ~/Downloads/control.pem ubuntu@<control-public-ip>
```

Notice: **no fingerprint question** this time. The fingerprint is already in `known_hosts`. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**5b. View the `known_hosts` file:**

```bash
exit
cat ~/.ssh/known_hosts
```

You'll see fingerprint entries including the control machine's IP address. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**5c. Clear the `known_hosts` file:**

```bash
cat /dev/null > ~/.ssh/known_hosts
```

| Part                 | Meaning                                                           |
| -------------------- | ----------------------------------------------------------------- |
| `cat /dev/null`      | Outputs nothing (`/dev/null` is the system's "black hole" device) |
| `>`                  | Redirect — overwrites the file's contents                         |
| `~/.ssh/known_hosts` | The target file — now emptied                                     |

 [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**5d. Verify the file is empty:**

```bash
cat ~/.ssh/known_hosts
```

Empty output confirms the file was cleared. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**5e. SSH again — fingerprint question returns:**

```bash
ssh -i ~/Downloads/control.pem ubuntu@<control-public-ip>
```

The question reappears because the machine is now "unknown" again. Type `yes`. The fingerprint is re-stored. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**Connection to larger flow:** Ansible will face this same fingerprint challenge when connecting to client machines non-interactively. The solution will be covered in a future lecture.

***

## Step 6: Install Ansible on the Control Machine

SSH into the control machine if not already connected.

**6a. Update package index:**

```bash
sudo apt update
```

 [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**6b. Add the Ansible PPA repository:**

The video copies a command from the Ansible documentation (`docs.ansible.com` → Installing Ansible → Ubuntu section). This command adds the official Ansible PPA so that `apt install` can find the Ansible package. The exact command varies — follow the current documentation. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**6c. Install Ansible:**

```bash
sudo apt install ansible -y
```

| Part          | Meaning                                |
| ------------- | -------------------------------------- |
| `sudo`        | Run with root privileges               |
| `apt install` | Ubuntu package manager install command |
| `ansible`     | The package name                       |
| `-y`          | Auto-confirm prompts                   |

This installs Ansible and its dependencies (Python 3, Python 2, and various Python libraries). [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**6d. Verify the installation:**

```bash
ansible --version
```

**Expected output:** Ansible version (e.g., `2.4.6`), Python version (e.g., Python 3.x), path to the Ansible configuration file, and other metadata. Your version number will likely differ. [\[232-setup-...-and-infra \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/232-setup-ansible-and-infra.txt)

**Connection to larger flow:** Ansible is now installed on the control machine. The next lecture will configure the **inventory file** — which tells Ansible which machines to manage and how to connect to them.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Infrastructure Architecture

```
YOU (local laptop)
  │
  │ SSH (port 22, My IP)       SSH (port 22, My IP)
  ▼                            ▼
[ CONTROL MACHINE ]          [ CLIENT MACHINES ]
  Ubuntu 22, t2.micro          CentOS Stream 9, t2.micro
  Key: control.pem             Key: client-key.pem
  SG: control-sg               SG: client-sg
  Ansible INSTALLED            Ansible NOT installed
  User: ubuntu                 User: ec2-user
  │                              ▲
  │ SSH (port 22)                │
  └──────────────────────────────┘
    Allowed via: client-sg inbound ← control-sg
```

***

## EC2 Instance Map

```
control     → Ubuntu 22   → control.pem   → control-sg    → Ansible HERE
web01       → CentOS 9    → client-key    → client-sg     → target
web02       → CentOS 9    → client-key    → client-sg     → target
db01        → CentOS 9    → client-key    → client-sg     → target
(later: Ubuntu web server → added later)
```

***

## Security Group Rules

```
control-sg:
  └── inbound: SSH (22) ← My IP

client-sg:
  ├── inbound: SSH (22) ← My IP           (human access)
  └── inbound: SSH (22) ← control-sg      (Ansible access) ← CRITICAL
```

Without the `control-sg` rule on clients → Ansible cannot connect → all automation fails.

***

## SSH Fingerprint Lifecycle

```
1st SSH to machine → "Are you sure?" → type yes → fingerprint stored in ~/.ssh/known_hosts
2nd SSH to machine → no question (fingerprint already known)

Clear: cat /dev/null > ~/.ssh/known_hosts → file emptied → all machines "unknown"
Next SSH → question returns

File: ~/.ssh/known_hosts
  Contains: IP + fingerprint for every machine you've SSH'd to

⚠️ Fingerprint ≠ SSH key
   Fingerprint = machine identity verification
   SSH key     = user authentication

Ansible problem: connects via SSH non-interactively → can't type "yes"
                 → solution covered in future lecture
```

***

## Ansible Installation Sequence (Ubuntu)

```
1. sudo apt update
2. Add Ansible PPA repository (from docs.ansible.com → Ubuntu section)
3. sudo apt install ansible -y
4. ansible --version  → verify

Ansible = Python library
  → installs Python 3 (+ possibly Python 2) as dependencies
  → code written on control → translated to Python scripts → executed on TARGETS
```

***

## Ansible Execution Model

```
Control Machine                          Target Machine
  │                                        │
  │ Ansible code (.yml)                    │
  │     ↓                                 │
  │ Translates to Python scripts           │
  │     ↓                                 │
  │ Pushes scripts via SSH ──────────────→ │ Python interpreter executes scripts
  │                                        │
  │ Control runs Python only for localhost │
  │ Targets run Python for everything else │

Python version on TARGET matters most (modules use different interpreters)
```

***

## Key Pair Separation

```
control.pem  → for YOU → SSH into control machine
client-key   → for YOU + ANSIBLE → SSH into web01, web02, db01
```

***

## CentOS AMI Selection

```
EC2 → Browse More AMIs → AWS Marketplace → search "CentOS 9"
  → CentOS Stream 9 by Amazon Web Services
  → Free with t2.micro / t3.micro
  → ⚠️ Change instance type manually (may default larger)
  → Login username: ec2-user (NOT ubuntu)
```

***

## `known_hosts` Commands

```
View:   cat ~/.ssh/known_hosts
Clear:  cat /dev/null > ~/.ssh/known_hosts
```

***

## Operational Sequence

```
1. Launch control (Ubuntu, control.pem, control-sg: SSH from My IP)
2. Launch 3 clients at once (CentOS 9, client-key, client-sg: SSH from My IP + control-sg)
3. Rename: web01, web02, db01
4. SSH into control machine
5. Understand fingerprint behavior (demo cycle)
6. Install Ansible: apt update → add PPA → apt install ansible -y
7. Verify: ansible --version
→ NEXT: inventory file + connecting Ansible to targets
```

***

## Key Engineering Patterns

| Pattern                                     | Manifestation                                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Agentless architecture**                  | No software installed on targets; SSH is the only requirement — pre-existing on all EC2 instances |
| **Controller/worker via SSH**               | Control machine orchestrates; targets execute; SSH is the transport layer                         |
| **Security group as access control**        | `client-sg` allows `control-sg` — network-level authorization for automation                      |
| **Separate keys per tier**                  | Control key ≠ client key — different access patterns, different credentials                       |
| **Bulk launch + rename**                    | Launch identical instances at once, differentiate by renaming afterward                           |
| **Documentation-driven installation**       | Follow `docs.ansible.com` for current install commands — don't memorize                           |
| **Fingerprint as machine identity**         | `known_hosts` stores verified machine identities; clearing it forces re-verification              |
| **Code-on-controller, execution-on-target** | Ansible translates YAML → Python, pushes to target, target's Python runs it                       |

***

## Project Continuity

```
THIS LECTURE:  Infrastructure setup (control + 3 clients + Ansible installed)
NEXT LECTURE:  Inventory file → Ansible connects to targets → testing
LATER:         Add Ubuntu web server (multi-OS management)
```

***

This completes the full reconstruction. **Theory** explains the Ansible architecture, SSH fingerprint mechanics, and security group design. **Practical** gives you every instance launch configuration, every command, and the full installation procedure. The **Compression Map** lets you mentally reload the entire four-machine infrastructure, the security group chain, and the fingerprint lifecycle in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀
