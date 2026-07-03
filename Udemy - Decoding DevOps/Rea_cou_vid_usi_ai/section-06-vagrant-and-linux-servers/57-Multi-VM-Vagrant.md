**Source:** [57-multi-vm-vagrant-file.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/57-multi-vm-vagrant-file.txt?EntityRepresentationId=c9677330-65e5-4d53-b63e-d4cffe609827) — Video lecture on defining and managing multiple virtual machines from a single Vagrantfile

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Problem — One VM Per Folder Limitation

In the standard Vagrant workflow covered in earlier lectures, each project folder contains one Vagrantfile, and that Vagrantfile defines exactly **one VM**. If you need three VMs — say a database server, an application server, and a frontend server — you'd need three separate folders, each with its own Vagrantfile. You'd manage each VM independently: `cd` into folder A and run `vagrant up`, then `cd` into folder B and run `vagrant up`, and so on. This works, but it's operationally fragmented. You're managing pieces of what is logically **one system** as if they were unrelated machines.

The real-world trigger for this problem is the **application stack**. Most non-trivial applications are not monolithic single-server deployments. They consist of multiple services — a database on one machine, an application layer on another, a web frontend on a third — that collectively form one application. These VMs need to exist together, be configured to talk to each other, and ideally be brought up, torn down, and managed as a unit. Managing them from separate folders breaks this conceptual unity and creates operational overhead.

## 1.2 The Solution — Multi VM Vagrantfile

A Multi VM Vagrantfile solves this by allowing you to define **multiple VMs inside a single Vagrantfile**. One file, one folder, one `vagrant up` command — and all the VMs in your stack come up together. Each VM gets its own configuration block within the file: its own box, its own IP, its own hostname, its own provisioning. But they're all siblings inside one parent configuration.

The key syntactic mechanism is `config.vm.define`. Inside the outer `Vagrant.configure("2") do |config| ... end` block, you create sub-blocks using:

```ruby
config.vm.define "web01" do |web01|
  web01.vm.box = "ubuntu/focal64"
  web01.vm.hostname = "web01"
  web01.vm.network "private_network", ip: "192.168.56.41"
end
```

The string `"web01"` after `config.vm.define` serves as the **VM's identity name** — this is the name Vagrant uses to refer to this specific VM in all CLI commands, and it's the name that appears during `vagrant up` output instead of the generic "default" you see with single-VM Vagrantfiles. The variable in the pipe symbols (`|web01|`) is a **scoped configuration object** — all settings inside that block use this variable as a prefix (`web01.vm.box`, `web01.vm.hostname`, etc.).

> 🔍 **Deep Dive:** The instructor draws an analogy for programmers: the pipe-symbol variable is like a class object — `web01` is an instance, and `.vm.box`, `.vm.hostname` are its properties. For non-programmers, the rule is simpler: whatever name appears between the pipes must be the prefix for every setting line inside that block. This scoping mechanism is what allows multiple VM definitions to coexist without their settings colliding.

## 1.3 VM Naming and Settings Scoping

Each `config.vm.define` block creates an isolated namespace. The name you give to the VM (the string after `define`) and the block variable (the pipe symbol name) work together:

* The **define name** (`"web01"`) is the VM's external identity — used in CLI commands like `vagrant ssh web01`, `vagrant halt web01`, `vagrant destroy web01`.
* The **block variable** (`|web01|`) is the internal configuration prefix — used to set that specific VM's properties without affecting others.

These two names don't technically have to match, but by convention they always do for clarity. The critical operational implication: when you copy-paste a VM block to add a new VM (say, `web03`), you must change **both** the define name and the block variable, **and** change every setting line's prefix inside the block, **and** change the IP address to avoid duplication. Forgetting any of these creates either naming collisions or IP conflicts.

## 1.4 IP Address Management in Multi VM Environments

All VMs in a multi VM Vagrantfile typically sit on the same **private network** (`192.168.56.x` in this case). The network prefix (`192.168.56`) is the shared network — all VMs are on the same subnet and can reach each other. The **host portion** (the last octet: `.41`, `.42`, `.43`) must be **unique per VM**. Duplicate IPs on the same network cause network failures for both VMs involved.

The instructor explicitly calls this out as a rule: "In the network, you cannot have duplicate IP addresses, so IPs should be different." The deeper networking concepts behind this are deferred to a later networking section, but the operational rule is absolute and must be followed now.

## 1.5 Provisioning Within Multi VM Vagrantfiles

Each VM block can include its own **provisioning** section — shell commands that run automatically after the VM boots for the first time. In the lecture, only `db01` (the database VM) gets provisioning, which installs `wget`, `unzip`, and `mariadb-server`, then starts and enables the MariaDB service.

An important package naming detail surfaces here: on CentOS, the MySQL-compatible database is packaged as **`mariadb-server`** (package name) with the service name **`mariadb`**. This is another instance of the distribution-specific naming pattern (like `httpd` vs `apache2` from the previous lecture). The provisioning block executes these as shell commands:

```bash
yum install wget unzip mariadb-server -y
systemctl start mariadb
systemctl enable mariadb
```

This is the same install → start → enable pattern from the manual server setup lecture, but now automated inside the Vagrantfile so it runs without human intervention.

## 1.6 Multi VM CLI Behavior — The Targeting Rule

When you have a single-VM Vagrantfile, commands like `vagrant ssh`, `vagrant halt`, `vagrant destroy` implicitly target the only VM that exists. In a multi VM environment, this changes significantly:

**Commands that require a VM name:**

* `vagrant ssh web01` — you **must** specify which VM to SSH into. Running `vagrant ssh` without a name produces an error: *"This command requires a specific VM name to target in a multi VM environment."*

**Commands that accept an optional name:**

* `vagrant halt web02` — powers off only `web02`. But `vagrant halt` without a name powers off **all VMs**.
* `vagrant destroy web01` — destroys only `web01`. But `vagrant destroy` without a name destroys **all VMs**.
* `vagrant up web03` — brings up only `web03`. But `vagrant up` without a name brings up **all VMs**.

The behavioral pattern: `vagrant ssh` is the exception that **always requires** a name (because you can only be inside one shell at a time). All other commands default to **all VMs** when no name is given, but can be narrowed to a specific VM by appending its name. This is a source of real operational mistakes — running `vagrant destroy` intending to destroy one VM but destroying all of them because you forgot the name.

## 1.7 Adding VMs Dynamically — Copy-Paste-Modify Pattern

To add a new VM to an existing multi VM Vagrantfile, you copy an existing VM block, paste it, and modify: the define name, the block variable, all setting prefixes, the box (if different), the hostname, and critically the IP address. The instructor demonstrates this by duplicating `web02`'s block to create `web03`, changing the name references and assigning a new IP (`.44`).

After saving the modified Vagrantfile, you can bring up **only the new VM** with `vagrant up web03`. Vagrant reads the Vagrantfile, finds the `web03` definition, and creates only that VM — it doesn't recreate the existing ones. This is an important operational property: the Vagrantfile is declarative, and Vagrant is smart enough to know which VMs already exist and which are new.

## 1.8 Project Segregation — When to Use Multi VM vs. Separate Folders

The instructor makes a clear distinction: multi VM Vagrantfiles are for VMs that **belong to the same project or application stack**. The example given is the upcoming "vprofile" project, which requires multiple VMs that work together as one application. All of those VMs belong in one multi VM Vagrantfile.

However, **different projects** or **different use cases** should have **different folders with different Vagrantfiles**. Don't put every VM you ever create into one giant Vagrantfile. The segregation principle: one Vagrantfile per logical project/stack, separate folders for separate projects.

## 1.9 Vagrant Documentation as a Reference System

The instructor spends time showing the official Vagrant documentation, accessible by Googling "Vagrant documentation." Key sections highlighted:

* **CLI section** — documents all commands (`vagrant box add`, `box list`, `box prune`, `box remove`, `vagrant init` with flags like `-m` for minimal/no-comments and `-f` to force-overwrite an existing Vagrantfile)
* **Vagrantfile section** — documents `config.vm` settings and all available options
* **Multi-Machine section** — contains a ready-made example of a multi VM Vagrantfile that you can copy-paste as a starting template

The documentation is positioned as the authoritative reference for all Vagrantfile configuration options.

## 1.10 ChatGPT as a DevOps Assistant — Philosophy of Use

The instructor introduces ChatGPT as a tool for generating configuration files, scripts, and code. The demonstration asks ChatGPT to generate a multi VM Vagrantfile with specific parameters (web01 Ubuntu, web02 Ubuntu, db01 CentOS, private IPs, provisioning for db01, hostnames). ChatGPT produces a working Vagrantfile with explanations.

However, the instructor delivers a **strong philosophical boundary**:

* **During learning:** Do NOT use ChatGPT for convenience. Write everything yourself. If you rely on it during learning, you won't internalize the knowledge.
* **After learning:** Once you're confident in your ability to write scripts and configs from scratch, use ChatGPT as an assistant to speed up work, debug errors, or generate boilerplate.
* **The key insight:** To use ChatGPT effectively, you must already know *what to ask*. The instructor points out that the prompt he gave required knowledge of what a multi VM Vagrantfile is, what boxes are, what private IPs mean, what provisioning is. ChatGPT is an amplifier of existing knowledge, not a replacement for it.

The instructor also notes ChatGPT can be used for: searching for error solutions, generating bash scripts, Ansible playbooks, Terraform code, and Jenkinsfiles — all topics in the broader DevOps curriculum.

## 1.11 The `--force` Flag on Destroy

When running `vagrant destroy`, Vagrant normally prompts "Are you sure?" for each VM. The `--force` flag (`vagrant destroy --force`) skips all confirmation prompts and immediately destroys all VMs. This is useful for quick cleanup but dangerous if used carelessly — there's no undo. The instructor uses it here because he's intentionally cleaning up everything and doesn't want to confirm three times.

If a VM was already destroyed (like `web01` which was destroyed individually earlier), Vagrant simply reports *"not created. Moving on..."* and continues to the next VM — it doesn't error out. This is idempotent behavior: destroying something that doesn't exist is a no-op, not a failure.

## 1.12 Resource Awareness — VM Count vs. Host Capacity

The instructor warns: when running multiple VMs, check that other VMs from previous exercises are powered off or destroyed. Three VMs running simultaneously consume significant RAM and CPU from the host machine. If you have additional VMs from earlier lectures still running, you risk running out of resources. The `vagrant global-status` command shows all tracked VMs across all folders, making it easy to identify stragglers.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating a **single Vagrantfile that defines three virtual machines** — two Ubuntu web servers (`web01`, `web02`) and one CentOS database server (`db01`) — each with its own private IP and hostname. The database VM includes automated provisioning that installs and starts MariaDB. The final outcome: running one `vagrant up` command and having an entire multi-service environment come online, manageable as a unit.

## Step 1: Explore the Vagrant Documentation

Before building, the instructor visits the Vagrant documentation (Google "Vagrant documentation") to review the multi-machine example.

Key areas to note:

* **CLI section** → reveals useful `vagrant init` flags:
  * `vagrant init -m <box>` — creates a Vagrantfile without comments (minimal/clean)
  * `vagrant init -f <box>` — overwrites an existing Vagrantfile without asking
* **Vagrantfile > config.vm** → lists all available VM settings
* **Multi-Machine section** → contains a copy-pasteable example of the `config.vm.define` syntax

This is the starting reference for building your own multi VM file. You can copy the example directly and modify it.

**Connection to flow:** This establishes the template structure before we generate our specific version.

## Step 2: Generate the Base Vagrantfile Using ChatGPT

Open ChatGPT and provide a specific prompt:

> *"Multi VM Vagrantfile with web01 Ubuntu20, web02 Ubuntu20, db01 with CentOS7. Private IP for all the VMs. And provisioning for db01. Set hostname also."*

ChatGPT generates a working Vagrantfile with all three VM blocks, IPs, hostnames, and a provisioning section for `db01`.

**Critical mindset:** You must already know what each of these terms means to write an effective prompt. ChatGPT generates the syntax; you supply the architecture knowledge.

**What to do with the output:** Copy the generated code. Do **not** use it as-is — treat it as a starting template that requires your review and modification.

**Connection to flow:** This gives us the raw Vagrantfile content to refine.

## Step 3: Create the Project Folder and Vagrantfile

In VS Code (or any editor):

1. Create a new folder: `multivm` (inside your vagrant-vms directory)
2. Inside it, create a new file named exactly: **`Vagrantfile`** — capital `V`, **no file extension**
3. Paste the ChatGPT-generated content into this file

**Common mistake:** Naming it `Vagrantfile.txt` or `vagrantfile` (lowercase). Vagrant looks for exactly `Vagrantfile` with a capital V and no extension.

## Step 4: Modify the Vagrantfile — IP Addresses

The ChatGPT output likely has placeholder IPs. Adjust them to the `192.168.56.x` range with unique host portions:

| VM      | IP Address      |
| ------- | --------------- |
| `web01` | `192.168.56.41` |
| `web02` | `192.168.56.42` |
| `db01`  | `192.168.56.43` |

**Why these specific values:** `56` is the network range for VirtualBox host-only networks. The last octet (`.41`, `.42`, `.43`) must be unique across all VMs on this network — including VMs from other Vagrantfiles if they're running simultaneously.

**Connection to flow:** Correct IPs ensure the VMs can communicate and are reachable from the host.

## Step 5: Modify the Vagrantfile — Provisioning for db01

Inside `db01`'s define block, set up the shell provisioning:

```ruby
db01.vm.provision "shell", inline: <<-SHELL
  yum install wget unzip mariadb-server -y
  systemctl start mariadb
  systemctl enable mariadb
SHELL
```

**Command breakdown:**

| Command                                    | Purpose                                                                                   |
| ------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `yum install wget unzip mariadb-server -y` | Installs download utility, unzip utility, and MariaDB database server; `-y` auto-confirms |
| `systemctl start mariadb`                  | Starts the MariaDB service immediately                                                    |
| `systemctl enable mariadb`                 | Ensures MariaDB starts on every boot                                                      |

**Key naming detail:** On CentOS, the package is `mariadb-server` but the service name is `mariadb` (without `-server`). Using the wrong name in `systemctl` commands will fail.

**Connection to flow:** This automates the install → start → enable pattern from the manual server setup lecture, removing the need to SSH in and run these commands manually.

## Step 6: Verify the Vagrantfile Structure

Before running, review the complete structure. Each VM block follows this pattern:

```ruby
config.vm.define "vmname" do |vmname|
  vmname.vm.box = "<box-name>"
  vmname.vm.hostname = "vmname"
  vmname.vm.network "private_network", ip: "192.168.56.XX"
  # optional: provisioning block
end
```

**Checklist before proceeding:**

* [ ] Each VM has a unique define name
* [ ] Each block variable matches its define name
* [ ] All setting lines inside each block use the correct prefix
* [ ] All IPs are unique
* [ ] Provisioning commands use correct package and service names
* [ ] File is saved as `Vagrantfile` (capital V, no extension)

## Step 7: Ensure Clean Environment

```bash
vagrant global-status
```

This shows all Vagrant-tracked VMs. If any are running from previous exercises, navigate to their directories and destroy or halt them. Three new VMs will consume significant resources — you don't want old VMs competing.

## Step 8: Bring Up All VMs

```bash
cd F:/vagrant-vms/multivm
vagrant up
```

**What happens internally:** Vagrant reads the Vagrantfile, identifies three VM definitions, and creates them sequentially. For each VM, it:

1. Downloads the box if not locally cached
2. Creates the VM in VirtualBox
3. Configures networking (assigns the private IP)
4. Sets the hostname
5. Runs provisioning (if defined — only `db01` in this case)

**Expected output observation:** Instead of seeing `default` as the VM name (which happens with single-VM files), you now see `web01`, `web02`, `db01` — the define names from your Vagrantfile. If a box isn't cached locally (e.g., the CentOS box), Vagrant downloads it first, which takes extra time.

**This step takes significant time.** The instructor pauses the recording and resumes after completion.

## Step 9: SSH into a Specific VM

```bash
vagrant ssh web01
```

**Why the name is required:** In a multi VM environment, `vagrant ssh` without a name produces an error: *"This command requires a specific VM name to target in a multi VM environment."* You must always specify which VM to enter.

**Verification inside the VM:** The hostname prompt should show `web01` (confirming the hostname setting worked).

```bash
exit
```

Exit back to the host to continue managing other VMs.

## Step 10: Managing Individual VMs

**Power off a specific VM:**

```bash
vagrant halt web02
```

Only `web02` powers off. `web01` and `db01` remain running.

**Power off all VMs:**

```bash
vagrant halt
```

Without a name, **all VMs** power down.

**Destroy a specific VM:**

```bash
vagrant destroy web01
```

Only `web01` is deleted. Others are untouched.

**Bring up a specific VM:**

```bash
vagrant up web02
```

Only `web02` starts. Vagrant reads the Vagrantfile, finds the `web02` block, and acts on it alone.

> ⚠️ **Expert Note:** The most dangerous operational mistake in multi VM management is running `vagrant destroy` without a VM name — it destroys everything. The `--force` flag makes this even more dangerous by skipping confirmation. Always double-check your command before pressing Enter when destroy is involved.

## Step 11: Adding a New VM to an Existing Vagrantfile

Open the Vagrantfile in your editor. Copy an existing VM block (e.g., `web02`'s block), paste it below, and modify:

1. Change `"web02"` → `"web03"` in the define line
2. Change `|web02|` → `|web03|` in the pipe symbols
3. Change every `web02.vm.` → `web03.vm.` in the settings
4. Change the IP to a new unique value (e.g., `192.168.56.44`)
5. Change the hostname to `"web03"`

Save the file, then bring up only the new VM:

```bash
vagrant up web03
```

Vagrant reads the updated Vagrantfile, sees `web03` doesn't exist yet, and creates it. Existing VMs are unaffected.

**Common mistake:** Forgetting to change the IP address after copy-pasting, resulting in an IP collision with an existing VM.

## Step 12: Full Cleanup

```bash
vagrant destroy --force
```

**Command breakdown:**

| Part              | Meaning                                       |
| ----------------- | --------------------------------------------- |
| `vagrant destroy` | Delete all VMs defined in this Vagrantfile    |
| `--force`         | Skip all "Are you sure?" confirmation prompts |

**Expected output:** Each VM is destroyed. If a VM was already destroyed earlier (e.g., `web01`), Vagrant prints *"not created. Moving on..."* and continues — no error.

**Connection to flow:** Clean environment for the next section of the course.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ System Architecture

```
Vagrantfile (single file, one folder)
│
├── config.vm.define "web01" do |web01|
│   ├── box: ubuntu/focal64
│   ├── hostname: web01
│   ├── IP: 192.168.56.41
│   └── provisioning: none
│
├── config.vm.define "web02" do |web02|
│   ├── box: ubuntu/focal64
│   ├── hostname: web02
│   ├── IP: 192.168.56.42
│   └── provisioning: none
│
└── config.vm.define "db01" do |db01|
    ├── box: centos/7
    ├── hostname: db01
    ├── IP: 192.168.56.43
    └── provisioning: shell
        ├── yum install wget unzip mariadb-server -y
        ├── systemctl start mariadb
        └── systemctl enable mariadb
```

## 🔑 Core Syntax Pattern

```ruby
config.vm.define "<NAME>" do |<NAME>|
  <NAME>.vm.box      = "<box>"
  <NAME>.vm.hostname = "<hostname>"
  <NAME>.vm.network "private_network", ip: "<unique-IP>"
  # optional: <NAME>.vm.provision "shell", inline: <<-SHELL ... SHELL
end
```

**Rule:** define name = pipe variable = setting prefix (always match all three)

## ⚡ Multi VM CLI Behavior Map

```
                    No VM name given          VM name given
                    ─────────────────         ──────────────
vagrant up          → ALL VMs up              → only <name> up
vagrant halt        → ALL VMs halt            → only <name> halt
vagrant destroy     → ALL VMs destroyed ⚠️    → only <name> destroyed
vagrant ssh         → ERROR ❌                → enters <name> ✓
vagrant destroy --force → ALL destroyed, no prompts
```

**Exception:** `vagrant ssh` ALWAYS requires a name.
**Danger zone:** `vagrant destroy` without a name = everything gone.

## 🔄 Add-VM Workflow

```
Copy existing VM block
  → Change define name
    → Change pipe variable
      → Change ALL setting prefixes
        → Change IP (MUST be unique)
          → Change hostname
            → Save → vagrant up <new-name>
```

**Forget IP change → network collision → both VMs broken**

## 📁 Project Segregation Rule

```
Same project / application stack  →  ONE multi VM Vagrantfile
Different project / use case      →  DIFFERENT folder + DIFFERENT Vagrantfile
```

*Multi VM ≠ "put everything in one file"*

## 🔗 Dependency & Naming Chains

```
CentOS MySQL package:  mariadb-server
CentOS MySQL service:  mariadb
(package ≠ service name)

Vagrantfile naming:    capital V, no extension
VM identity:           define name → used in all CLI commands
Block variable:        pipe symbol name → used in all settings
```

## 🛠️ Vagrant CLI Quick Reference (from documentation)

```
vagrant init <box>         → generate Vagrantfile
vagrant init -m <box>      → minimal Vagrantfile (no comments)
vagrant init -f <box>      → overwrite existing Vagrantfile
vagrant box list           → show cached boxes
vagrant box prune          → remove old box versions
vagrant box remove <name>  → remove specific box
vagrant global-status      → show ALL VMs across all folders
vagrant destroy --force    → destroy all, skip confirmation
```

## 🧩 Reusable Patterns Extracted

| Pattern                                           | Instance                                                                                |
| ------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Scoped configuration blocks**                   | `config.vm.define` creates isolated namespaces per VM — same pattern as class instances |
| **Declarative infrastructure**                    | Vagrantfile describes desired state; Vagrant figures out what to create/skip            |
| **Idempotent operations**                         | Destroying an already-destroyed VM → "not created, moving on" (no error)                |
| **Copy-paste-modify for scaling**                 | Add VMs by duplicating blocks + changing identifiers — template-driven expansion        |
| **Selective targeting in multi-resource systems** | `<command> <name>` operates on one; `<command>` alone operates on all                   |
| **Manual-first → generate-later**                 | Learn to write configs yourself, then use AI to accelerate known patterns               |
| **Provisioning = embedded automation**            | Shell commands inside Vagrantfile = the manual install→start→enable pattern, automated  |

## 🗺️ Course Progression Context

```
[PREVIOUS] Single VM Vagrantfiles + manual server setup (httpd on CentOS)
       ↓
[THIS LECTURE] Multi VM Vagrantfile (manage application stacks as a unit)
       ↓
[UPCOMING] vprofile project (real multi-service application using multi VM)
       ↓
[LATER] Bash scripting, Ansible, Terraform, Jenkins (all generatable via ChatGPT after learning)
```

## 💡 ChatGPT Usage Philosophy (Compressed)

```
Learning phase:   Write everything yourself → build ability
Working phase:    Use ChatGPT as assistant → amplify ability
Key requirement:  You must know WHAT to ask → ChatGPT generates HOW
Error debugging:  Always valid use case at any stage
```

*ChatGPT = amplifier of existing knowledge, not a replacement for it.*
