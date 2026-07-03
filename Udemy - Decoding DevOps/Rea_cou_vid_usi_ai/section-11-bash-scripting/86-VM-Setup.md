# 🎓 VM Setup for Bash Scripting Practice — Deep Learning Material

**Source:** Video caption file — *VM Setup for Bash Scripts* + accompanying Vagrantfile [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt), [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Lab Architecture: Why Multiple VMs for Bash Scripting?

The purpose of this setup is to create a **multi-machine lab environment** for practicing Bash scripts. This is not about running a single VM and typing commands — it's about building an infrastructure where you can write scripts on one machine and eventually **push and execute them on other machines**. This mirrors real-world operations where you write automation on a control node and deploy it to target servers. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

The architecture uses **three primary virtual machines** (with a fourth defined in the Vagrantfile for later use):

* **scriptbox** — The machine where all scripts are written and developed. This is the **control node** — your workstation in the lab.
* **web01** and **web02** — Target machines. In the first part of the course, they aren't needed. Later, scripts written on scriptbox will be pushed to these machines. They represent the **remote servers** you'd manage in a real environment.

This separation — a dedicated scripting machine and separate target machines — is a deliberate design choice. It forces you to think about scripts not just as local utilities but as **deployable automation** that must work across machines. Writing on one machine and executing on another introduces real-world concerns: file transfer, remote execution, path differences, OS differences, and permissions.

> 🔍 **Deep Dive:** The Vagrantfile actually defines a **fourth VM** — `web03` — running **Ubuntu Bionic** instead of CentOS. While the video doesn't discuss it directly, its presence in the Vagrantfile is significant: it introduces an **OS heterogeneity** layer into the lab. Later exercises likely test whether scripts work across different Linux distributions — a critical real-world concern since CentOS and Ubuntu use different package managers (`yum`/`dnf` vs `apt`), different default paths, and different service management conventions. [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)

***

## 1.2 — The Vagrantfile: Infrastructure as Code for the Lab

The entire multi-VM lab is defined in a single **Vagrantfile**. This is a Ruby-syntax configuration file that Vagrant reads to know what VMs to create, how to configure them, and what resources to allocate. The Vagrantfile is placed in the course resources section for download. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

The Vagrantfile uses the `Vagrant.configure("2")` block (Vagrant configuration version 2) and defines each VM using `config.vm.define` blocks. Each VM definition specifies:

* **Box** — The base OS image. `eurolinux-vagrant/centos-stream-9` for scriptbox, web01, and web02. `ubuntu/bionic64` for web03. A box is a pre-built virtual machine image that Vagrant downloads and uses as the starting point. [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)
* **Private network IP** — Each VM gets a unique static IP on a private network (`192.168.10.12` through `192.168.10.15`). This private network allows the VMs to communicate with each other and with your host machine, but the IPs are not reachable from the public Internet. [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)
* **Hostname** — Each VM is assigned a hostname matching its role (`scriptbox`, `web01`, `web02`, `web03`). [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)
* **Provider-specific settings** — scriptbox is allocated **1024 MB of memory** via VirtualBox provider settings. The other VMs use default memory allocation. [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)

The IP addresses used (`192.168.10.x`) are **Class C private IPs** — they're from the `192.168.0.0/16` private range, which means they're safe for local lab use and won't conflict with public Internet addresses.

> ⚠️ **Expert Note:** scriptbox gets explicit memory allocation (1024 MB) while the others don't. This is because scriptbox is the primary working machine — you'll have editors open, scripts running, potentially multiple processes during development. The target VMs (web01/02/03) are simpler — they just need to receive and run scripts, so default memory is sufficient. This is a **resource allocation by role** pattern — give more resources to the machine that does more work. [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)

***

## 1.3 — Selective VM Startup: `vagrant up` vs. `vagrant up <name>`

When a Vagrantfile defines multiple VMs, `vagrant up` (with no arguments) brings up **all** of them. But you don't always need all machines running. The video explicitly explains this: `vagrant up scriptbox` brings up **only scriptbox**, saving time and system resources. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

This is an important operational concept: in a multi-VM Vagrantfile, you can **selectively start individual VMs by name**. The name used in the command matches the name defined in the `config.vm.define "<name>"` block in the Vagrantfile. Since the first part of the course only requires scriptbox, there's no reason to start web01 and web02 yet.

***

## 1.4 — Hostname Configuration: Why It Matters

After logging into the VM, the first thing done is **setting the hostname**. The hostname is set by editing `/etc/hostname` and writing the desired name (`scriptbox`), then running the `hostname` command to apply it. After logging out and back in, the hostname appears in the shell prompt. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

Why does this matter? When you're working with multiple VMs, you need to **immediately know which machine you're connected to** by looking at the prompt. Without a properly set hostname, the prompt might show a generic or auto-generated name, and you could accidentally run destructive commands on the wrong machine. The hostname in the prompt is your **situational awareness indicator**. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

The video notes that the same hostname-setting process will be done for the other VMs later — every machine in the lab gets a clear, identifiable hostname.

***

## 1.5 — Working as Root: The `sudo -i` Decision

All scripts in this course are written and executed as the **root user**. The command `sudo -i` is used to switch to an interactive root shell. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

This is a deliberate simplification for learning. In a scripting practice environment, working as root removes permission barriers that would distract from learning scripting itself. You don't want to debug "permission denied" errors when you're trying to learn loops and conditionals.

> ⚠️ **Expert Note:** In production environments, running everything as root is generally avoided. The principle of least privilege dictates that you should operate with the minimum permissions necessary. But for a learning lab, root access simplifies the experience and lets you focus on scripting logic rather than permission management. The video explicitly frames this as a lab setup decision. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We're setting up a **multi-VM lab environment** for Bash scripting practice. By the end of this process, we'll have a running CentOS virtual machine called **scriptbox** with its hostname properly configured, logged in as root and ready for script development. The other VMs (web01, web02) will be brought up later when needed. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

***

## Step 1: Create a Working Directory

### What We're Doing

Creating a dedicated directory on your host machine to hold the Vagrantfile and serve as the Vagrant project root.

### Why We're Doing It

Vagrant operates from the directory where the Vagrantfile lives. Every `vagrant` command you run must be executed from this directory. Having a dedicated, clearly named directory keeps your lab organized. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### The Action

Create a directory somewhere on your system. The video uses a directory on the **D: drive** called something like `bash-scripts`. The exact path is your choice, but it should be easy to navigate to.

```
mkdir bash-scripts
```

### Connection to Larger Flow

This directory becomes your Vagrant project root. All subsequent `vagrant` commands will be run from here.

***

## Step 2: Download and Place the Vagrantfile

### What We're Doing

Downloading the Vagrantfile from the course **resources section** and placing it into the directory created in Step 1. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### Why We're Doing It

The Vagrantfile contains all VM definitions. Without it in the correct directory, Vagrant has no instructions for what to create.

### The Action

The video shows copying the Vagrantfile from the Downloads directory to the bash-scripts directory:

```
cp ~/Downloads/Vagrantfile /d/bash-scripts/
```

**Breakdown:**

* `cp` — Copy command
* `~/Downloads/Vagrantfile` — Source: the downloaded Vagrantfile in your Downloads folder
* `/d/bash-scripts/` — Destination: your project directory (the video uses Git Bash path notation for the D: drive)

### How to Verify

Navigate into the directory and confirm the Vagrantfile is present:

```
cd /d/bash-scripts/
ls
```

You should see `Vagrantfile` listed.

***

## Step 3: Inspect the Vagrantfile

### What We're Doing

Opening the Vagrantfile to understand what VMs are defined and how they're configured. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### The Command

```
vim Vagrantfile
```

The video uses **vim in Git Bash**. You can alternatively use **Notepad++** or any text editor. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### What You Should See

The Vagrantfile defines the following VMs: [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)

| VM Name       | Box (OS Image)                      | Private IP      | Memory  | Hostname  |
| ------------- | ----------------------------------- | --------------- | ------- | --------- |
| **scriptbox** | `eurolinux-vagrant/centos-stream-9` | `192.168.10.12` | 1024 MB | scriptbox |
| **web01**     | `eurolinux-vagrant/centos-stream-9` | `192.168.10.13` | default | web01     |
| **web02**     | `eurolinux-vagrant/centos-stream-9` | `192.168.10.14` | default | web02     |
| **web03**     | `ubuntu/bionic64`                   | `192.168.10.15` | default | web03     |

### Key Observations

* The instructor mentions three VMs in the video (scriptbox, web01, web02), but the Vagrantfile includes a fourth (web03 running Ubuntu). [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt), [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)
* All CentOS machines use the same box: `eurolinux-vagrant/centos-stream-9`.
* All machines are on the **same private network** (`192.168.10.x`), which means they can communicate with each other.
* Only scriptbox has explicit memory configuration (1024 MB).

### Connection to Larger Flow

Understanding the Vagrantfile is essential before running `vagrant up` — you need to know what machines exist and what their names are so you can selectively start the one you need.

***

## Step 4: Bring Up Only scriptbox

### What We're Doing

Starting only the scriptbox VM, not all VMs defined in the Vagrantfile. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### Why We're Doing It

For the first part of the course, only scriptbox is needed. Starting all VMs would waste time (downloading boxes, booting VMs) and consume unnecessary host system resources (RAM, CPU).

### The Command

```
vagrant up scriptbox
```

**Breakdown:**

* `vagrant` — The Vagrant CLI tool
* `up` — Subcommand that creates and starts a VM
* `scriptbox` — The specific VM name (matches `config.vm.define "scriptbox"` in the Vagrantfile). Without this argument, **all VMs would start**. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### What Happens Internally

1. Vagrant reads the Vagrantfile and finds the `scriptbox` definition.
2. If the box (`eurolinux-vagrant/centos-stream-9`) isn't already downloaded, Vagrant downloads it from the Vagrant Cloud registry.
3. Vagrant instructs VirtualBox to create a new VM with the specified settings (1024 MB RAM, private network IP `192.168.10.12`, hostname `scriptbox`).
4. The VM boots up with CentOS Stream 9.

### Expected Output

Vagrant will show progress messages — downloading the box (first time only), configuring network interfaces, booting the machine. The final message indicates the VM is running.

### How to Verify

```
vagrant status
```

This should show `scriptbox` as `running` and the other VMs as `not created`.

### Common Mistakes

* **Running `vagrant up` without specifying `scriptbox`** — This brings up ALL VMs, which is unnecessary and resource-heavy at this stage.
* **Running the command from the wrong directory** — Vagrant looks for a Vagrantfile in the current directory. If you're not in the project directory, it will fail.
* **VirtualBox not installed** — Vagrant uses VirtualBox as the provider. If VirtualBox isn't installed, `vagrant up` will fail.

### Connection to Larger Flow

After this step, scriptbox is running and ready for login. The VM is a fresh CentOS machine that needs hostname configuration and root login setup.

***

## Step 5: Log into scriptbox

### What We're Doing

SSH-ing into the running scriptbox VM. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### The Command

```
vagrant ssh scriptbox
```

**Breakdown:**

* `vagrant` — Vagrant CLI
* `ssh` — Subcommand to open an SSH session to a VM
* `scriptbox` — The target VM name

### What Happens Internally

Vagrant uses the SSH key it automatically configured during `vagrant up` to establish an SSH connection to scriptbox. You land in the VM as the `vagrant` user (the default Vagrant user).

### Expected Result

You're now inside the scriptbox VM's terminal. The prompt will show you're logged in, but the hostname may not yet display `scriptbox` clearly until you configure it in the next step.

***

## Step 6: Set the Hostname

### What We're Doing

Configuring the hostname so it displays in the shell prompt, making it immediately obvious which machine you're on. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### Why We're Doing It

When working with multiple VMs, the prompt hostname is your **visual indicator of location**. Without it, you risk running commands on the wrong machine.

### The Commands

**Step 6a: Edit the hostname file**

```
sudo vi /etc/hostname
```

Inside the file, replace any existing content with:

```
scriptbox
```

Save and exit (`:wq` in vim).

**Breakdown:**

* `sudo` — Execute with elevated privileges (editing system files requires root)
* `vi` — Text editor (the video uses vim)
* `/etc/hostname` — The system file that stores the machine's hostname persistently

**Step 6b: Apply the hostname immediately**

```
hostname scriptbox
```

This sets the hostname for the current session without requiring a reboot. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

**Step 6c: Logout and login to see the change in the prompt**

```
exit
vagrant ssh scriptbox
```

### Expected Result

After logging back in, the shell prompt now shows `scriptbox`, confirming the hostname is set. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### How to Verify

Simply look at the prompt — it should include `scriptbox`. You can also run:

```
hostname
```

This should output `scriptbox`.

### Connection to Larger Flow

The video notes that the **same hostname-setting process** will be repeated for web01 and web02 when those VMs are brought up later. Each machine gets its own identifying hostname.

***

## Step 7: Switch to Root User

### What We're Doing

Switching to an interactive root shell for all scripting work. [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

### The Command

```
sudo -i
```

**Breakdown:**

* `sudo` — Execute a command with superuser privileges
* `-i` — Simulate an **initial login** as root. This gives you a full root shell with root's environment variables, home directory (`/root`), and PATH. It's different from just `sudo su` because `-i` loads root's complete login environment.

### Expected Result

Your prompt changes to indicate you're now the root user (typically `#` instead of `$`, and the username portion shows `root`).

### Connection to Larger Flow

From this point forward, all scripting work happens as root. This is the final setup step — your environment is now ready: VM running, hostname set, root access established. **The next video begins actual script writing.** [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

> ⚠️ **Expert Note:** The `-i` flag is specifically chosen over alternatives like `sudo su` or `sudo -s` because it provides the cleanest root environment — it sources root's `.profile` and `.bashrc`, sets `HOME=/root`, and resets the environment variables. This avoids subtle bugs where scripts behave differently because the environment was only partially elevated.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Lab Architecture

```
HOST MACHINE (your laptop/desktop)
  └── Vagrant Project Directory (contains Vagrantfile)
        └── VirtualBox Provider
              ├── scriptbox  [CentOS Stream 9 | 192.168.10.12 | 1024MB] ◄── CONTROL NODE (write scripts here)
              ├── web01      [CentOS Stream 9 | 192.168.10.13 | default] ◄── TARGET (later)
              ├── web02      [CentOS Stream 9 | 192.168.10.14 | default] ◄── TARGET (later)
              └── web03      [Ubuntu Bionic   | 192.168.10.15 | default] ◄── TARGET (cross-OS testing, later)
              
              All VMs on SAME private network: 192.168.10.0/24
```

 [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt), [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

***

## 🔄 Operational Execution Sequence

```
1. mkdir bash-scripts                          ← Create project directory
2. cp Vagrantfile → bash-scripts/              ← Place Vagrantfile (from course resources)
3. cd bash-scripts/
4. vim Vagrantfile                             ← Inspect: 4 VMs, IPs, boxes, memory
5. vagrant up scriptbox                        ← Start ONLY scriptbox (not all VMs)
6. vagrant ssh scriptbox                       ← SSH into the VM
7. sudo vi /etc/hostname → write "scriptbox"   ← Set persistent hostname
8. hostname scriptbox                          ← Apply hostname immediately
9. exit → vagrant ssh scriptbox                ← Re-login to see hostname in prompt
10. sudo -i                                    ← Switch to root (all scripts run as root)

✅ READY — Begin writing Bash scripts
```

 [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

***

## 🔑 Key Decisions & Their Reasoning

```
DECISION                              WHY
─────────────────────────────────────────────────────────────
vagrant up scriptbox (not vagrant up) → Only scriptbox needed now; saves resources + time
Set hostname manually                 → Prompt must show VM name → prevents wrong-machine mistakes
sudo -i (not sudo su)                → Full root login environment (clean PATH, HOME=/root)
All scripts as root                  → Eliminates permission distractions during learning
scriptbox gets 1024MB, others default → Control node does more work → needs more resources
web03 = Ubuntu (others = CentOS)      → Cross-OS script testing capability (implicit)
```

***

## 📐 Vagrantfile Structure Map

```
Vagrant.configure("2") do |config|
  │
  ├── config.vm.define "scriptbox"
  │     ├── .vm.box = "eurolinux-vagrant/centos-stream-9"
  │     ├── .vm.network "private_network", ip: "192.168.10.12"
  │     ├── .vm.hostname = "scriptbox"
  │     └── .vm.provider "virtualbox" → vb.memory = "1024"
  │
  ├── config.vm.define "web01"
  │     ├── .vm.box = "eurolinux-vagrant/centos-stream-9"
  │     ├── .vm.network "private_network", ip: "192.168.10.13"
  │     └── .vm.hostname = "web01"
  │
  ├── config.vm.define "web02"
  │     ├── .vm.box = "eurolinux-vagrant/centos-stream-9"
  │     ├── .vm.network "private_network", ip: "192.168.10.14"
  │     └── .vm.hostname = "web02"
  │
  └── config.vm.define "web03"
        ├── .vm.box = "ubuntu/bionic64"
        ├── .vm.network "private_network", ip: "192.168.10.15"
        └── .vm.hostname = "web03"
```

 [\[86.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86.Vagrantfile.txt)

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: CONTROL NODE + TARGET NODES
  scriptbox = where you write/develop
  web01/02/03 = where you deploy/execute
  → Same pattern as: Ansible control node → managed hosts
                      Jenkins master → build agents
                      Terraform workstation → cloud infra

PATTERN 2: SELECTIVE RESOURCE STARTUP
  Don't start what you don't need yet.
  vagrant up <name> instead of vagrant up
  → Same pattern as: starting only needed microservices during dev
                      scaling specific service replicas, not all

PATTERN 3: INFRASTRUCTURE AS CODE (IaC)
  Entire lab defined in one declarative file (Vagrantfile)
  Reproducible, version-controllable, shareable
  → Same pattern as: Terraform .tf files, Docker Compose YAML,
                      Kubernetes manifests, CloudFormation templates

PATTERN 4: IDENTITY VIA HOSTNAME (Situational Awareness)
  Set hostname → appears in prompt → know where you are
  → Same pattern as: PS1 prompt customization, Kubernetes context/namespace display,
                      AWS CLI profile indicators

PATTERN 5: HETEROGENEOUS TARGET ENVIRONMENT
  CentOS (web01/02) + Ubuntu (web03) = test cross-platform compatibility
  → Same pattern as: multi-OS CI matrices, cross-distro package testing,
                      hybrid cloud deployments
```

***

## 🧭 Course Flow Context

```
THIS video   → Set up scriptbox VM, configure hostname, get root shell
NEXT video   → Begin writing Bash scripts on scriptbox
LATER         → Bring up web01/web02, push scripts from scriptbox → targets
LATER STILL   → Cross-OS execution on web03 (Ubuntu)
```

 [\[86-vm-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/86-vm-setup.txt)

***

Your lab environment blueprint is now fully mapped. Want me to generate **AnkiDroid flashcards (.csv)** from this material, or shall we proceed to the next caption file? 🃏
