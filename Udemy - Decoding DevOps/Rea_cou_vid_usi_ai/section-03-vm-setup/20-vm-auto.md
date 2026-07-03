# Vagrant — VM Automation Tool: Complete Deep Learning Material

*Reconstructed from the video lecture on managing virtual machines automatically with Vagrant (Windows & macOS Intel Chip)* [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Problem: Manual VM Management

Before understanding Vagrant, you must understand the pain it eliminates. When you create and manage virtual machines manually through a hypervisor's graphical interface, you face a cluster of compounding problems. **OS installation** requires walking through multiple interactive screens — choosing language, disk layout, network settings, user accounts — every single time. This process is **time-consuming**: a single OS installation can take 15–30 minutes, and if you need five VMs, you multiply that time linearly. Every manual step introduces the possibility of **human error** — a wrong IP address, a forgotten package, a misconfigured setting. And perhaps the most painful problem: **reproducibility**. If you carefully built five VMs on your laptop and now need to replicate the exact same setup on a colleague's machine, you must repeat the entire process from scratch, or maintain detailed documentation that itself can become outdated or inaccurate. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

These are not Vagrant-specific problems — they are the universal problems that **any automation** addresses. Automation exists because manual processes don't scale, don't reproduce reliably, and don't tolerate human inconsistency. Vagrant is one specific solution to these problems in the domain of virtual machine lifecycle management. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## 2. What Vagrant Is — And What It Is Not

**Vagrant is a VM automation tool** that manages the entire lifecycle of virtual machines: creating them, configuring them, starting them, stopping them, and destroying them. The critical architectural distinction to understand immediately is that **Vagrant is NOT a hypervisor**. It does not replace Oracle VM VirtualBox, VMware Workstation, or any other hypervisor. Vagrant sits **on top of** a hypervisor. It is an orchestration layer that sends instructions to the hypervisor, which does the actual work of running the VM. Think of it as a manager who gives orders versus a worker who executes them — Vagrant is the manager, VirtualBox is the worker. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

The default hypervisor that Vagrant works with is **Oracle VM VirtualBox**, but it can also use VMware Workstation and others. This is an important design choice: Vagrant is hypervisor-agnostic in principle, but defaults to VirtualBox because it's free and widely available. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Vagrant is a **command-line tool**, not a graphical application. All interaction happens through typed commands in a terminal. This is deliberate — command-line tools are scriptable, automatable, and composable in ways that GUIs are not. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## 3. Vagrant Boxes — Pre-Built VM Images

One of Vagrant's most powerful design decisions is eliminating OS installation entirely. Instead of installing an operating system from scratch, Vagrant uses **Boxes** — pre-built, ready-made VM images that already contain a fully installed OS. These boxes are stored on **Vagrant Cloud**, a public registry where anyone can publish and download VM images. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

When you tell Vagrant to create a VM using a specific box, Vagrant first checks if that box already exists on your local machine. If it doesn't, Vagrant downloads it from Vagrant Cloud and caches it locally. From that single downloaded box, you can create as many VMs as you want, as many times as you want. The box is a template — each VM created from it is an independent copy. Destroying a VM doesn't destroy the box; the box remains cached for future use. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

🔍 **Deep Dive:** The box download happens only once per box. On subsequent `vagrant up` commands using the same box, Vagrant finds it locally and skips the download. This is a classic **cache-on-first-use** pattern — expensive operations (network download) happen once, and subsequent operations use the local cache. The command `vagrant box list` shows all cached boxes on your computer.

***

## 4. The Vagrantfile — Configuration as Code

All VM settings live in a single text file called **Vagrantfile** (capital V, no extension). This file defines everything about the VM: which box to use, how much RAM and CPU to allocate, what IP address to assign, and what provisioning commands to run after the OS boots. Because it's a plain text file, it can be version-controlled, shared, reviewed, and edited with any text editor. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

The Vagrantfile is the heart of Vagrant's automation model. Instead of clicking through GUI settings, you declare what you want in this file, and Vagrant reads it and makes it happen. This is the **Infrastructure as Code** principle: your infrastructure configuration is code, not a series of manual actions. The Vagrantfile is created by the `vagrant init` command, which generates a template file with the specified box name pre-filled in the `config.vm.box` setting. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

A critical operational rule: **Vagrant commands are folder-scoped**. Vagrant looks for the Vagrantfile in your current working directory. If you're in the wrong folder, Vagrant either operates on the wrong VM or fails entirely. One folder = one Vagrantfile = one VM configuration. This creates a clean, predictable mapping between directory structure and VM identity. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

🔍 **Deep Dive:** When Vagrant boots or reboots a VM (via `vagrant up` or `vagrant reload`), it re-reads the Vagrantfile and applies any changes to VM settings like RAM, CPU, or IP addresses. However, changing the box name requires destroying and recreating the VM — the box is the foundation image, and you cannot swap it on a running VM. This is a fundamental constraint: settings are mutable, but the base image is immutable once a VM exists.

***

## 5. Provisioning — Post-Boot Automation

**Provisioning** in Vagrant means executing commands on the VM after the OS has fully booted. The use case is straightforward: after the bare OS is running, you often need to install software — a web server, a database, development tools. Instead of logging in and typing these commands manually, you define them in the Vagrantfile, and Vagrant runs them automatically during VM creation. This completes the automation loop: Vagrant handles not just VM creation but also the initial software setup inside the VM. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## 6. Vagrant Architecture — The Execution Flow

The architecture of Vagrant follows a clear chain of interactions. When you run `vagrant up`, Vagrant reads the Vagrantfile to determine the desired VM configuration. It then checks whether the specified box exists locally. If not, it downloads the box from Vagrant Cloud. Next, Vagrant contacts the hypervisor (VirtualBox by default) and provides the VM creation instructions — box image, RAM, CPU, network settings. The hypervisor creates and starts the VM. If provisioning commands are defined, Vagrant executes them inside the VM after boot. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

This architecture has a clear **layered separation**: the user interacts with Vagrant (the orchestration layer), Vagrant interacts with the hypervisor (the execution layer), and the hypervisor manages the actual VM (the compute layer). The user never needs to touch the hypervisor directly — in fact, the lecture explicitly warns against making changes through VirtualBox's GUI once Vagrant is managing the VM, because Vagrant won't be aware of those changes and may report false status information. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

⚠️ **Expert Note:** The warning about not using VirtualBox GUI to control Vagrant-managed VMs is architecturally important. Vagrant maintains its own state tracking of each VM. If you power off a VM through VirtualBox instead of `vagrant halt`, Vagrant's internal state becomes inconsistent with reality. This is a common problem in any system where two controllers can act on the same resource — it creates **split-brain** scenarios. The rule is simple: once Vagrant manages a VM, all lifecycle operations go through Vagrant.

***

## 7. User Identity Layers Inside a VM

When you log into a Vagrant VM using `vagrant ssh`, you enter as the **vagrant** user — a non-root user that Vagrant creates by default. The command `whoami` confirms this. From the vagrant user, you can escalate to the **root** user (the superuser with full system control) using `sudo -i`. Each `exit` command steps you back one layer: from root to vagrant, from vagrant back to your host machine. The **prompt changes** at each level — this visual indicator tells you which identity context you're currently in. The host prompt shows your computer's username, the vagrant prompt shows `vagrant@`, and the root prompt typically shows `root@` with a `#` symbol instead of `$`. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## 8. Vagrant Command Model — Lifecycle Verbs

Vagrant's command set maps directly to VM lifecycle states. Each command is a verb that transitions the VM from one state to another:

**`vagrant init <boxname>`** — Initializes a new Vagrantfile in the current directory with the specified box. Does not create a VM — it only creates the configuration file.

**`vagrant up`** — The primary command. If the VM doesn't exist, it creates it (downloading the box if needed) and starts it. If the VM exists but is powered off, it simply starts it. This dual behavior (create-or-start) makes `vagrant up` idempotent in intent — "make sure this VM is running."

**`vagrant ssh`** — Opens an SSH session into the running VM. Uses SSH in the background to connect.

**`vagrant halt`** — Gracefully powers off the VM. The VM still exists on disk; it's just not running. For CentOS specifically, this can take a long time as it waits for a graceful shutdown before force-powering off.

**`vagrant reload`** — Reboots the VM. Critically, during the boot phase, it **re-reads the Vagrantfile** and applies any setting changes. This is how you apply configuration changes without destroying the VM.

**`vagrant destroy`** — Permanently deletes the VM. All data inside the VM is lost. The box remains cached. Prompts for confirmation (answer `Y`). After destruction, `vagrant up` creates a completely fresh VM.

**`vagrant status`** — Shows the state of the VM in the current folder (running, powered off, not created).

**`vagrant global-status`** — Shows the state of all Vagrant VMs across all folders on the computer. The `--prune` flag cleans up stale entries that no longer correspond to actual VMs.

**`vagrant box list`** — Lists all downloaded boxes cached on your computer. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

🔍 **Deep Dive:** The `vagrant destroy` + `vagrant up` cycle is Vagrant's version of **immutable infrastructure** at the development level. Instead of fixing a broken VM, you delete it and recreate it from the clean box image. Any changes you made inside the VM are gone — only what's defined in the Vagrantfile (including provisioning) survives destruction. This teaches a critical operational mindset: VMs are disposable, configuration is permanent.

***

## 9. Shell Navigation Fundamentals (Supporting Context)

The lecture introduces essential shell navigation commands that are prerequisites for operating Vagrant. **`pwd`** prints the present working directory — your current location in the filesystem. **`cd <path>`** changes directory. **`ls`** lists the contents of the current directory. **`mkdir <name>`** creates a new directory. **`cat <filename>`** prints file contents to the screen. **`clear`** clears the terminal screen. **`history`** shows all previously executed commands. The **up/down arrows** cycle through command history. **Tab completion** auto-completes file and directory names. **`cd ..`** moves one level up in the directory hierarchy. **Tilde (`~`)** represents the user's home directory. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Windows users use **Git Bash** as the terminal (which provides a Unix-like shell on Windows). macOS users use the built-in **Terminal**. Path conventions differ: Windows users reference drives like `/f/` or `/c/`, while macOS users use `~/Desktop`. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating **two Vagrant-managed virtual machines** — one CentOS Stream 9 and one Ubuntu Jammy (22.04) — that will serve as Linux learning environments in upcoming sections. By the end, both VMs will be operational, and you'll be fluent in the full Vagrant lifecycle: create, login, power off, reboot, destroy, and recreate. The final state: two VMs powered off and preserved for the Linux section, with you confident in managing them entirely through Vagrant commands. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## Step 1: Open Your Terminal

**Windows:** Open **Git Bash** (not CMD, not PowerShell — Git Bash provides the Unix-like commands we need).
**macOS:** Open **Terminal**. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Run:

```bash
pwd
```

* **`pwd`** = Print Working Directory. Shows where you currently are.
* Expected output (Windows): `/c/Users/yourname` — your home directory.
* The `~` (tilde) symbol in your prompt also represents this home directory.

**Connection to flow:** We need to know our starting location before creating the project directory structure.

***

## Step 2: Create the Project Directory Structure

**Windows:**

```bash
mkdir /f/vagrant-vms
```

**macOS:**

```bash
mkdir ~/Desktop/vagrant-vms
```

* **`mkdir`** = Make Directory. Creates a new folder.
* **`/f/vagrant-vms`** = Creates the folder `vagrant-vms` in the F drive. If you don't have an F drive, use `/c/vagrant-vms` or any drive you have.
* **macOS** users create it on the Desktop for easy access. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Now navigate into it:

**Windows:**

```bash
cd /f/vagrant-vms/
```

**macOS:**

```bash
cd ~/Desktop/vagrant-vms/
```

* **`cd`** = Change Directory.

Verify:

```bash
pwd
```

Expected output: `/f/vagrant-vms` (or your equivalent path).

```bash
ls
```

* **`ls`** = List. Shows folder contents. Should be empty right now.

Now create two sub-folders — one per VM:

```bash
mkdir centos
mkdir ubuntu
```

Verify:

```bash
ls
```

Expected output: `centos  ubuntu` [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Connection to flow:** Each VM gets its own folder. Vagrant is folder-scoped — one Vagrantfile per folder, one VM per Vagrantfile.

***

## Step 3: Initialize the CentOS VM

Navigate into the centos folder:

```bash
cd centos
```

You can verify with `pwd`. You can also reach this folder using the full path:

```bash
cd /f/vagrant-vms/centos/
```

Or step by step: `cd /f/` → `cd vagrant-vms` → `cd centos`. All three approaches are equivalent. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Find the box name:** Open a browser, search for **Vagrant Cloud**, and go to `app.vagrantup.com`. Search for **CentOS nine**. The box to use is **`eurolinux-vagrant/centos-stream-9`**. Click on it and verify it supports **VirtualBox** as a provider. Copy the box name — **copy from the title text, not from the URL bar**, as the URL may add extra spaces. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Now initialize:

```bash
vagrant init eurolinux-vagrant/centos-stream-9
```

* **`vagrant init`** = Creates a Vagrantfile in the current directory.
* **`eurolinux-vagrant/centos-stream-9`** = The box name (format: `publisher/boxname`).
* Output: `A Vagrantfile has been placed in this directory.` [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Verify the file was created:

```bash
ls
```

Expected: `Vagrantfile`

Inspect the file:

```bash
cat Vagrantfile
```

* **`cat`** = Concatenate/print file content. You can also type `cat Vag` and press **Tab** to auto-complete.
* Look for the line: `config.vm.box = "eurolinux-vagrant/centos-stream-9"` — this confirms the box name is correctly set.
* The file contains many commented lines — ignore them for now. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**If you made a mistake** with the box name: navigate to the folder in your file explorer, open the Vagrantfile with Notepad or Notepad++, edit the `config.vm.box` line, and save. No need to re-run `vagrant init`.

**Connection to flow:** The Vagrantfile is created. The next step brings the VM to life.

***

## Step 4: Create and Start the CentOS VM

```bash
vagrant up
```

* **`vagrant up`** = Create (if not exists) and start the VM.
* On first run: Vagrant downloads the box from Vagrant Cloud (may take several minutes depending on internet speed), caches it locally, then creates the VM in VirtualBox and boots it. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**⚠️ Common Errors and Fixes:**

| Error                                      | Cause                         | Fix                                        |
| ------------------------------------------ | ----------------------------- | ------------------------------------------ |
| `schannel: next InitializeSecurityContext` | Antivirus interference        | Fully disable antivirus, retry             |
| `Vbox hardening 0x80...`                   | Antivirus blocking VirtualBox | Fully disable antivirus, retry             |
| Download/network failures                  | VPN or corporate proxy        | Disconnect VPN; use non-corporate internet |

Some antivirus software is difficult to fully disable — ensure it's completely stopped, not just paused. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Verify the VM is running:**

```bash
vagrant status
```

Expected output: `default    running (virtualbox)` — confirms the VM is running on VirtualBox.

```bash
vagrant box list
```

Shows all downloaded boxes. You should see `eurolinux-vagrant/centos-stream-9` listed. This box is now cached — future `vagrant up` commands won't re-download it. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

You can also open **VirtualBox** to visually confirm — you'll see a VM named `centos_default` (derived from the folder name). **Observe only — do not make any changes through VirtualBox.** All management goes through Vagrant commands to avoid state inconsistency (as explained in Theory §6).

***

## Step 5: Log Into the CentOS VM

```bash
vagrant ssh
```

* **`vagrant ssh`** = Opens an SSH connection into the VM.
* The prompt changes — this is your visual indicator that you're now **inside the VM**, no longer on your host machine. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Explore the VM environment:

```bash
whoami
```

Output: `vagrant` — you're logged in as the `vagrant` user.

```bash
pwd
```

Output: `/home/vagrant` — the vagrant user's home directory inside the VM.

Switch to root user:

```bash
sudo -i
```

* **`sudo -i`** = Switch to root (superuser) with a login shell.
* The prompt changes again (typically shows `root@` and `#` instead of `$`).

```bash
whoami
```

Output: `root` [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Exit back through the layers:

```bash
exit
```

→ Returns from root to vagrant user.

```bash
exit
```

→ Returns from VM to your host machine. The prompt returns to your host prompt — this confirms you've left the VM. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## Step 6: Power Off, Power On, Reboot, and Destroy

**Power off the VM:**

```bash
vagrant halt
```

* Performs a **graceful shutdown**. CentOS may take extra time — this is normal. If graceful shutdown times out, Vagrant force-powers off.

Verify:

```bash
vagrant status
```

Expected: `poweroff`

You can also check VirtualBox — the VM should show as stopped. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Power on the existing VM:**

```bash
vagrant up
```

* This time, the VM already exists and the box is already cached. Vagrant simply powers it on — no download, no creation. Much faster. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Reboot the VM:**

```bash
vagrant reload
```

* Reboots the VM and **re-reads the Vagrantfile** during boot, applying any setting changes (RAM, CPU, IP, etc.). Box name changes require destroy + recreate. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Destroy (delete) the VM:**

```bash
vagrant destroy
```

* Prompts: `Are you sure you want to destroy the 'default' VM? [y/N]` → type `Y`.
* The VM is permanently deleted. All data inside it is gone.

Verify:

```bash
vagrant status
```

Expected: `not created` — the VM no longer exists.

VirtualBox will also show it's gone. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Recreate from scratch:**

```bash
vagrant up
```

* Creates a **brand new VM** from the cached box. The box is already local (`Importing base box...` appears instead of downloading). This is a fresh VM — nothing from the destroyed VM carries over. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

⚠️ **Expert Note:** Always power off VMs (`vagrant halt`) before shutting down your computer. Abruptly killing a running VM can corrupt its virtual disk, leading to a VM that won't boot. If that happens, `vagrant destroy` + `vagrant up` recovers you, but any unsaved work inside the VM is lost.

***

## Step 7: Set Up the Ubuntu VM

Navigate to the ubuntu folder:

```bash
cd ..
```

* **`cd ..`** = Move one level up in the directory tree (from `centos` back to `vagrant-vms`).

Verify and enter ubuntu:

```bash
ls
```

Expected: `centos  ubuntu`

```bash
cd ubuntu
```

(Tip: type `cd ub` then press **Tab** — it auto-completes to `cd ubuntu` if it's the only match.) [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Find the Ubuntu box:** Go to Vagrant Cloud, search for **ubuntu jammy**. The box is **`ubuntu/jammy64`** (Ubuntu 22 "Jammy Jellyfish" server). Copy the box name. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

Initialize and create:

```bash
vagrant init ubuntu/jammy64
```

```bash
vagrant up
```

Verify:

```bash
vagrant status
```

Expected: `running (virtualbox)` [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

**Log in, explore, log out** (same pattern as CentOS):

```bash
vagrant ssh
whoami        # → vagrant
sudo -i       # → switch to root
exit          # → back to vagrant user
exit          # → back to host
```

Power off:

```bash
vagrant halt
```

 [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## Step 8: Global VM Status and Cross-Folder Management

From any directory, you can check the status of **all** Vagrant VMs on your machine:

```bash
vagrant global-status
```

* Shows every VM, its state (running/poweroff/not created), its provider (virtualbox), and **the folder path** where each VM's Vagrantfile lives. This is how you find and navigate to any VM. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

If you see stale/phantom entries (VMs that were deleted outside Vagrant):

```bash
vagrant global-status --prune
```

* **`--prune`** = Removes entries that no longer correspond to real VMs. Only needed if the table shows orphaned entries. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

To manage a specific VM, `cd` to its folder and run commands there:

```bash
cd /f/vagrant-vms/centos
vagrant up
```

 [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## Step 9: View Command History

```bash
history
```

* Shows all previously executed commands with line numbers. Useful for reviewing what you did and replaying commands. Scroll up to trace the full session flow. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## Step 10: Clean Up Manually Created VMs

If you previously created VMs manually through VirtualBox (from earlier lectures), you can now delete them — Vagrant-managed VMs replace them. In VirtualBox, right-click the old VM → **Remove** → **Delete all files**. **Be careful to delete only the old manual VMs, not the Vagrant-managed ones** (named `centos_default` and `ubuntu_default`). [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

## Final State

* **CentOS VM:** powered off, preserved in `/f/vagrant-vms/centos/` (or equivalent)
* **Ubuntu VM:** powered off, preserved in `/f/vagrant-vms/ubuntu/` (or equivalent)
* **Both boxes:** cached locally (no re-download needed)
* Both VMs will be used in the Linux section

Keep these VMs intact. If you accidentally destroy one, simply `cd` into its folder and run `vagrant up` — it recreates from the cached box. [\[20-vm-auto...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/20-vm-automatically-windows-and-macos-intel-chip.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Architecture

```
User (Git Bash / Terminal)
  │
  ├── vagrant commands (CLI)
  │     │
  │     ├── Reads → Vagrantfile (config: box, RAM, CPU, IP, provisioning)
  │     │
  │     ├── Checks → Local Box Cache
  │     │     ├── Found? → Use local box
  │     │     └── Not found? → Download from Vagrant Cloud → Cache locally
  │     │
  │     └── Instructs → Hypervisor (VirtualBox default)
  │           │
  │           └── Creates/Manages → VM (running instance)
  │
  └── NEVER interact with VirtualBox GUI for Vagrant VMs
```

***

## Vagrant ≠ Hypervisor

```
Vagrant = Orchestration Layer (manager)     → sends instructions
VirtualBox = Execution Layer (worker)       → runs VMs
Box = Template Image (blueprint)            → source for VM creation
VM = Running Instance (product)             → disposable, recreatable
Vagrantfile = Configuration-as-Code (spec)  → text file, version-controllable
```

***

## Command → State Transition Map

```
                    ┌─────────────┐
       vagrant init │  Vagrantfile │  (no VM yet)
                    │   Created    │
                    └──────┬──────┘
                           │ vagrant up (first time)
                           ▼
                    ┌─────────────┐
                    │   RUNNING   │◄──── vagrant up (existing, powered off)
                    │             │◄──── vagrant reload (reboot + re-read config)
                    └──┬───┬───┬──┘
                       │   │   │
          vagrant ssh  │   │   │ vagrant halt
               ▼       │   │       ▼
        ┌──────────┐   │   │  ┌───────────┐
        │ SSH into │   │   │  │ POWERED   │
        │   VM     │   │   │  │   OFF     │
        └──────────┘   │   │  └───────────┘
           exit ↑──────┘   │
                           │ vagrant destroy
                           ▼
                    ┌─────────────┐
                    │ NOT CREATED │ (VM deleted, box remains)
                    │             │──── vagrant up → back to RUNNING
                    └─────────────┘
```

***

## Identity Stack (Inside VM)

```
Host Machine (imran@hostname ~$)
  └── vagrant ssh →
        Vagrant User (vagrant@localhost ~$)
          └── sudo -i →
                Root User (root@localhost ~#)
                  └── exit → back to vagrant
                        └── exit → back to host

Prompt signals: $ = normal user │ # = root │ ~ = home dir
```

***

## Folder-Scoping Rule

```
/f/vagrant-vms/
  ├── centos/
  │     └── Vagrantfile (box: eurolinux-vagrant/centos-stream-9)
  │         → vagrant commands here control CentOS VM only
  │
  └── ubuntu/
        └── Vagrantfile (box: ubuntu/jammy64)
            → vagrant commands here control Ubuntu VM only

RULE: cd into folder FIRST → then run vagrant commands
EXCEPTION: vagrant global-status works from anywhere
```

***

## Box Lifecycle (Cache Pattern)

```
First vagrant up → box not local → download from Vagrant Cloud → cache
Subsequent vagrant up → box found locally → skip download → "Importing base box"
vagrant destroy → VM deleted → box stays cached
vagrant box list → shows all cached boxes
```

***

## Vagrantfile Mutability Rules

```
Mutable (apply via vagrant reload):    RAM, CPU, IP, provisioning, network
Immutable (requires destroy+recreate): box name (base image)
Editable via: any text editor (Notepad, Notepad++, vim)
```

***

## Common Failure Patterns

```
Error: schannel / Vbox hardening → Cause: Antivirus → Fix: Fully disable antivirus
Error: Download fails            → Cause: VPN / Proxy → Fix: Disconnect VPN, non-corporate internet
Error: Commands fail silently    → Cause: Wrong folder → Fix: pwd, cd to correct Vagrantfile folder
Warning: VBox shows wrong state  → Cause: Used VBox GUI → Fix: Only use vagrant commands
Slow vagrant halt (CentOS)       → Normal: Graceful shutdown → waits → then force-off
```

***

## Essential Command Quick-Reference

| Command                         | Purpose                       |
| ------------------------------- | ----------------------------- |
| `vagrant init <box>`            | Create Vagrantfile            |
| `vagrant up`                    | Create (or start) VM          |
| `vagrant ssh`                   | Login to VM                   |
| `vagrant halt`                  | Graceful power off            |
| `vagrant reload`                | Reboot + apply config changes |
| `vagrant destroy`               | Delete VM permanently         |
| `vagrant status`                | VM state (current folder)     |
| `vagrant global-status`         | All VMs state (any folder)    |
| `vagrant global-status --prune` | Clean stale entries           |
| `vagrant box list`              | Show cached boxes             |

| Shell Command  | Purpose                      |
| -------------- | ---------------------------- |
| `pwd`          | Where am I?                  |
| `cd <path>`    | Move to directory            |
| `ls`           | List contents                |
| `mkdir <name>` | Create directory             |
| `cat <file>`   | Print file content           |
| `cd ..`        | Go one level up              |
| `history`      | Show all past commands       |
| `whoami`       | Current user identity        |
| `sudo -i`      | Escalate to root             |
| `exit`         | Step back one identity layer |

***

## Reusable Engineering Patterns

| Pattern                                  | Manifestation                                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Orchestrator / Worker separation**     | Vagrant (orchestrator) → VirtualBox (worker). User never touches the worker directly.       |
| **Configuration as Code**                | Vagrantfile replaces GUI clicks. Text file = reproducible, shareable, version-controllable. |
| **Cache-on-first-use**                   | Box downloaded once → reused indefinitely. Expensive operation (download) happens once.     |
| **Immutable infrastructure (dev-level)** | `destroy` + `up` = fresh VM. Don't fix — replace. Config survives, state doesn't.           |
| **Folder-scoped context binding**        | One directory = one config = one resource. Context determined by location, not flags.       |
| **Single controller principle**          | Only Vagrant controls Vagrant VMs. Dual control (Vagrant + VBox GUI) = state inconsistency. |
| **Layered identity escalation**          | host → vagrant user → root. Each layer has different privileges. `exit` unwinds one layer.  |
| **Idempotent intent commands**           | `vagrant up` = "ensure running" whether VM needs creation or just power-on.                 |

***

This completes the full reconstruction. The three sections work together: **Theory** builds your mental model of *why* and *how*, **Practical** gives you confident execution with exact commands and troubleshooting, and the **Compression Map** lets you rapidly reload the entire system — architecture, commands, patterns, and failure modes — in minutes rather than re-reading everything. 🚀
