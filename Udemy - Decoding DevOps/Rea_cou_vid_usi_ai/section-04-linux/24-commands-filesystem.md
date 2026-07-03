# 🎓 Linux Commands & File System Structure — Deep Learning Material

*Reconstructed from the video lecture on basic Linux commands and the Linux directory hierarchy* [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Lab Environment — Vagrant VM as Your Linux Playground

This lecture and the entire section require a **Vagrant VM** created in a previous section. The course uses **CentOS** as the primary distribution, with **openSUSE** available as an alternative. Vagrant is a tool that manages virtual machines through simple commands — you don't interact with VirtualBox directly. Instead, Vagrant wraps the VM lifecycle into commands like `vagrant up` (start), `vagrant ssh` (connect), and `vagrant global-status` (check state and location of all VMs). [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The VM here is not freshly created — it was already provisioned earlier, so `vagrant up` simply **powers on** an existing machine rather than building one from scratch. Once inside via `vagrant ssh`, you land as the **vagrant** user in a full CentOS Linux environment where everything that follows is executed. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

## 2. Four Foundational Commands — Your First Orientation Tools

Before navigating the system, you need to answer two fundamental questions: *who am I?* and *where am I?* Linux provides four basic commands that together form your orientation toolkit: [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**`whoami`** tells you the username of the currently logged-in user. When you SSH into the Vagrant VM, you land as the `vagrant` user. This command doesn't tell you what permissions you have or what groups you belong to — it simply returns the username. But knowing your identity is the first step to understanding what you're allowed to do. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**`pwd`** (present working directory) tells you your current location in the filesystem as an **absolute path** — the full path starting from the root directory `/`. When the vagrant user first logs in, `pwd` returns `/home/vagrant`, which is the vagrant user's **home directory**. Every user has a home directory — it's their personal workspace in the filesystem. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**`ls`** lists the contents (files and directories) of the current directory. Running it in a freshly provisioned vagrant user's home directory may show nothing — the directory is empty by default. But `ls` becomes essential as you navigate to other directories with rich content. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**`cat`** reads and displays the contents of a file. The instructor demonstrates it with `cat /etc/os-release`, a file that contains the operating system name and version. `cat` is a read-only operation — it simply prints file content to the terminal. It's your first tool for inspecting configuration files, logs, and system information. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

## 3. The Linux Prompt — A Live Status Display

The Linux command prompt is not just a cursor waiting for input — it's a **compressed status indicator** that tells you three things at all times: [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```
vagrant@localhost ~$
│         │        │ │
│         │        │ └─ $ = normal user shell
│         │        └─── ~ = you are in your home directory
│         └──────────── hostname (localhost = no hostname set)
└────────────────────── username (vagrant)
```

The **username** portion matches what `whoami` returns. The **hostname** is the machine's network name — if none is explicitly set, it defaults to `localhost`. The **tilde `~`** is a shorthand symbol representing the current user's home directory (so for `vagrant`, `~` means `/home/vagrant`; for `root`, `~` means `/root`). The **trailing character** indicates privilege level: `$` means a normal user shell, `#` means the root user's shell. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

This prompt dynamically updates as you change users or directories. When you switch to root via `sudo -i`, the prompt changes to `root@localhost ~#` — the username changes, the tilde now represents root's home directory, and `$` becomes `#`. This is not cosmetic — it's a real-time safety indicator that tells you the power level of every command you're about to execute. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

## 4. Root User vs. Normal User — The Privilege Boundary

Linux enforces a strict **privilege separation** between the **root user** (superuser/administrator) and **normal users**. The `vagrant` user is a normal user — it can perform everyday tasks but cannot execute system-level operations like formatting disks, rebooting the system, or modifying core configuration without elevated permissions. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The command **`sudo -i`** switches you from the vagrant user to the root user. The `-i` flag means "login shell" — it doesn't just give you root permissions for one command; it fully transitions you into a root session with root's environment, home directory, and prompt. After running `sudo -i`, `whoami` returns `root` and `pwd` returns `/root`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

Critically, only the vagrant user has permission to execute `sudo -i` in this Vagrant-managed VM. This is a Vagrant-specific configuration — in production systems, sudo access is carefully controlled through the `/etc/sudoers` file. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

> 🔍 **Deep Dive**
> The privilege boundary is not just about preventing mistakes — it's a **security architecture**. Even if a normal user's account is compromised, the attacker cannot perform system-level damage without also obtaining sudo/root access. This layered defense is fundamental to Linux security design. The prompt's `$` vs `#` indicator serves as a constant visual reminder of which side of this boundary you're operating on.

***

## 5. Root Directory vs. Root User's Home Directory — The Critical Distinction

This is the single most important conceptual clarification in the lecture, and the instructor emphasizes it repeatedly because it causes persistent confusion: [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**`/` (root directory)** is the **top-level directory** of the entire Linux filesystem. Every file, directory, and device on the system exists somewhere under `/`. It is the starting point of the entire directory tree. When you run `cd /` and then `ls`, you see **all top-level directories** of the operating system — `bin`, `etc`, `home`, `root`, `boot`, `tmp`, `var`, `proc`, and everything else. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**`/root` (root user's home directory)** is simply a directory that lives inside `/` — it's the personal home directory of the root user, just as `/home/vagrant` is the home directory of the vagrant user. It is one directory among many under `/`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The confusion arises because the word "root" is used for both concepts. The resolution is structural: `/` alone (just the forward slash) always means the root directory. `/root` (slash-root) always means root user's home directory. They are at different levels of the filesystem hierarchy — `/` is the parent that *contains* `/root`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The instructor also introduces a critical navigational shortcut: typing **`cd` with no arguments** and pressing Enter always returns you to the current user's home directory, regardless of where you are in the filesystem. If you're root, `cd` takes you to `/root`. If you're vagrant, `cd` takes you to `/home/vagrant`. This is the "when you're lost" recovery command. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

## 6. The Linux Directory Structure — A Purposeful Architecture

The Linux filesystem is not a random collection of folders. Every top-level directory under `/` has a **specific, well-defined purpose**. Understanding this structure means understanding where Linux keeps everything and why. The instructor walks through each major directory: [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/home` — Normal Users' Home Directories

Contains a subdirectory for each non-root user on the system (e.g., `/home/vagrant`). This is where normal users store personal files, configurations, and data. Each user's home directory is their default landing location upon login. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/root` — Root User's Home Directory

The root user's home directory. It exists at `/root` rather than `/home/root` — this is by design, ensuring root's home is accessible even if the `/home` partition fails to mount (since `/root` is on the root filesystem itself). [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/bin` — User Executable Programs

Contains **commands and programs that normal users can execute**. When you run `whoami`, `pwd`, `ls`, `mv` (move files), `scp` (secure copy to remote machines), or `yum` (package manager), you're running binaries located in `/bin`. The instructor explicitly navigates into `/bin` and runs `ls` to show the density of available user commands. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/sbin` — System Executable Programs

Contains **commands that require root/system-level privileges**. Examples include `mkfs.ext4` (format a partition with ext4 filesystem — a destructive operation no normal user should perform casually) and `reboot` (restart the operating system). Some `/sbin` commands *can* be run by normal users if prefixed with `sudo`, but they are fundamentally system administration tools. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The `/bin` vs `/sbin` separation is an architectural expression of the privilege boundary discussed earlier — user-level operations are physically separated from system-level operations at the filesystem level. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/etc` — Configuration Files

The central location for **system and application configuration files**. The instructor shows several examples: `/etc/hostname` contains (and allows changing) the system's hostname. Yum (the Red Hat/CentOS package manager, compared to Google Play Store on Android) stores its configuration here. Network configuration files live here. Throughout the course, many files from `/etc` will be examined and modified. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

Editing files in `/etc` is done through a text editor — the instructor mentions the **vi editor** will be taught later for this purpose. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/tmp` — Temporary Files

A directory for **temporary data** that is not expected to persist. Scripts use it to store intermediate data during execution. Many automation tools and system processes write temporary files here during operations. The instructor gives an explicit warning: **do not store anything in `/tmp` that you want to keep**. It exists purely for transient use. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/boot` — Kernel and Bootloader

Contains the files required to **boot the operating system**: the Linux kernel (`vmlinuz`), the initial RAM filesystem (`initramfs`), and the GRUB bootloader configuration (inside a `grub2` subdirectory). Modifying boot parameters, changing kernel versions, or troubleshooting boot failures involves files in this directory. The instructor notes this becomes relevant in deeper system administration work. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/var` and `/srv` — Server/Variable Data

Used to store **server data** and **variable data** that changes during system operation (logs, mail spools, web server content, database files). The instructor mentions these will be explored in later lectures. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/opt` — Optional Software

A directory for **optional, add-on software** that doesn't come with the base OS installation. Third-party applications are often installed here. The instructor notes it will be used later in the course. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/media` and `/mnt` — Mount Points

Used for **mounting** external filesystems — USB drives, CD-ROMs, network shares, or additional partitions. `/media` is typically used for automatically mounted removable media; `/mnt` is used for temporary manual mounts. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/proc` and `/sys` — Dynamic System Information

These are **virtual filesystems** — they don't contain real files stored on disk. Instead, they expose **live, dynamic system information** generated by the kernel in real-time. The content changes constantly as the system's state changes. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The instructor demonstrates this with two examples. The command **`uptime`** shows how long the system has been running (13 minutes in the demo), the number of logged-in users, and the current load average. This command reads its data from `/proc/uptime` — but the raw file content may not be human-readable, so the `uptime` command formats it. Similarly, **`free -m`** shows RAM usage in megabytes, and this information is also sourced from files in `/proc`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The key insight: many Linux commands are essentially **human-readable interfaces** to raw data stored in `/proc` and `/sys`. The data in these directories is dynamic — it reflects the system's current state and changes continuously. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

> 🔍 **Deep Dive**
> The `/proc` filesystem reveals a fundamental Linux design principle: **everything is a file**. Even running processes, CPU information, memory statistics, and kernel parameters are exposed as files in `/proc`. This uniform interface means you can inspect (and sometimes modify) nearly any aspect of the system using the same file-reading tools (`cat`, etc.) you'd use on regular files. This is why Linux is so scriptable and automatable — system state is always accessible through the filesystem.

***

## 7. Absolute Paths — Unambiguous Location Specification

When navigating the filesystem, the instructor introduces the concept of **absolute paths**. An absolute path **always begins with `/`** (the root directory) and specifies the complete route from the top of the filesystem to the target. For example, `/bin`, `/etc/hostname`, `/proc/uptime` are all absolute paths. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

The alternative is a **relative path**, demonstrated when the instructor, already in the root directory `/`, types `cd bin` instead of `cd /bin`. Since they're already at `/`, `bin` is relative to the current location and resolves to `/bin`. Absolute paths work from anywhere; relative paths depend on your current location. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We are **booting an existing CentOS Vagrant VM**, logging into it, and **learning to orient ourselves** inside a Linux system using basic commands. Then we **systematically explore the Linux directory structure** to understand where things live. The outcome: you can navigate any Linux system, identify your user and location, read files, and know the purpose of every top-level directory. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

## Step 1: Check VM Status and Navigate to the VM Directory

**What we're doing:** Verifying the state and location of our Vagrant VMs before starting.

```bash
vagrant global-status
```

* **`vagrant`** — the Vagrant CLI tool
* **`global-status`** — shows the status (running, poweroff, etc.) and **filesystem path** of every Vagrant VM on your system [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**What happens:** You see a table listing all VMs, their states, and the directories where their Vagrantfiles live. Find the CentOS VM entry and note its directory path.

**Next**, navigate to that directory:

```bash
cd /f/vagrant-vm/centos/
```

This changes your terminal's working directory to where the CentOS VM's Vagrantfile is located. The path `/f/vagrant-vm/centos/` is specific to the instructor's setup — yours will be wherever you created the VM in the previous section. Vagrant commands must be run from the directory containing the Vagrantfile for the target VM. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

***

## Step 2: Start the VM and Log In

**What we're doing:** Powering on the existing VM and connecting to it via SSH.

```bash
clear
```

* Clears the terminal screen for readability. Purely cosmetic — no system effect. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
vagrant up
```

* **`vagrant up`** — starts the VM. Since this VM was already created previously, it simply **powers on** the existing machine (not provisioning from scratch). Takes under a minute. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**How to verify:** The command output will show the VM booting and eventually indicate it's running.

```bash
vagrant ssh
```

* **`vagrant ssh`** — opens an SSH session into the running VM. You are now inside the CentOS Linux environment as the `vagrant` user. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**How to verify:** Your terminal prompt changes to something like `vagrant@localhost ~$`, confirming you're logged in as `vagrant` on the VM.

***

## Step 3: Orient Yourself — The Four Basic Commands

**What we're doing:** Establishing identity, location, contents, and reading system information.

```bash
clear
```

Clears the VM's terminal screen. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
whoami
```

**Output:** `vagrant` — confirms your username. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
pwd
```

**Output:** `/home/vagrant` — confirms you're in the vagrant user's home directory. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
ls
```

**Output:** (empty or minimal) — the home directory of a fresh vagrant user has nothing in it. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
cat /etc/os-release
```

* **`cat`** — concatenate/display file contents
* **`/etc/os-release`** — absolute path to a file containing OS name and version information [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**Output:** Displays CentOS version details. This confirms you're on the correct OS inside the VM.

**Connection to larger flow:** These four commands are your orientation toolkit. Before doing anything on a Linux system, you should know who you are (`whoami`), where you are (`pwd`), what's around you (`ls`), and what system you're on (`cat /etc/os-release`).

***

## Step 4: Switch to Root User

**What we're doing:** Elevating privileges from normal user to root (superuser).

```bash
sudo -i
```

* **`sudo`** — execute a command as another user (default: root)
* **`-i`** — simulate a full login shell for root (sets root's environment, home directory, prompt) [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**What happens internally:** Your session transitions from the `vagrant` user to `root`. The prompt changes from `vagrant@localhost ~$` to `root@localhost ~#`.

**Verify the switch:**

```bash
whoami
```

**Output:** `root` [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
pwd
```

**Output:** `/root` — you're now in root's home directory, not `/home/vagrant`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**Common mistake:** Confusing `/root` (where you land after `sudo -i`) with `/` (the root directory of the entire filesystem). They are different locations — see Step 5.

***

## Step 5: Navigate the Root Directory vs. Root's Home Directory

**What we're doing:** Physically demonstrating the difference between `/` and `/root`.

```bash
cd /
```

* Changes directory to **`/`**, the top-level root directory of the entire filesystem. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
pwd
```

**Output:** `/` — confirms you are at the filesystem root, NOT in `/root`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
ls
```

**Output:** Lists all top-level directories: `bin`, `boot`, `dev`, `etc`, `home`, `lib`, `media`, `mnt`, `opt`, `proc`, `root`, `sbin`, `srv`, `sys`, `tmp`, `usr`, `var`, etc. These are **all the directories in the operating system**. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

Notice that both `home` and `root` appear in this listing — `/home` contains normal user directories, and `/root` is root's home directory, both living under `/`.

**Recovery command — returning home:**

```bash
cd
```

Typing `cd` with no arguments always returns you to the current user's home directory. Since you're root, this takes you to `/root`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
pwd
```

**Output:** `/root` — confirmed you're back in root's home directory. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**When to use this:** Whenever you're lost in the filesystem, `cd` (no arguments) + Enter is your reset button.

***

## Step 6: Explore the Directory Structure

**What we're doing:** Navigating into each major directory to see its contents and understand its purpose.

### `/bin` — User Executables

```bash
cd /bin
ls
```

**Output:** A large list of executable programs: `mv`, `scp`, `yum`, `whoami`, `pwd`, and many more. These are the commands available to normal users. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**Note on path usage:** From `/`, you can type `cd bin` (relative path). From anywhere else, use `cd /bin` (absolute path). [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/sbin` — System Executables

```bash
cd /sbin
ls
```

**Output:** System administration commands like `mkfs.ext4` (format partitions), `reboot`, etc. These require root privileges or `sudo`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/etc` — Configuration Files

```bash
cd /etc
ls
```

**Output:** Configuration files and directories: `hostname`, yum configs, network configs, and many more. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**Reading a specific config file:**

```bash
cat /etc/hostname
```

**Output:** The current hostname of the system. This file can be edited (using vi editor, taught later) to change the hostname. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/tmp` — Temporary Files

Referenced as a directory for transient data. Scripts and automation tools write temporary files here. **Do not store persistent data in `/tmp`**. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/boot` — Kernel and Bootloader

```bash
cd /boot
ls
```

**Output:** `vmlinuz` (the kernel), `initramfs` (initial RAM filesystem), and a `grub2` directory containing boot configuration. Relevant for system administration tasks like changing boot parameters or kernel versions. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

### `/proc` — Dynamic System Information

```bash
cd /proc
ls
```

**Output:** Virtual files representing live system state. Content changes dynamically. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**Demonstrating dynamic data:**

```bash
uptime
```

**Output:** System uptime (e.g., "13 minutes"), number of users, load average. This command reads from `/proc/uptime`. [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

```bash
free -m
```

* **`free`** — displays memory (RAM) usage
* **`-m`** — show values in megabytes [\[24-command...le-systems \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/24-commands-and-file-systems.txt)

**Output:** Total, used, free, and available RAM. This data comes from `/proc` and is dynamic — it changes as the system's memory usage changes.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Lab Entry Sequence

```
vagrant global-status       → find VM path + state
cd <vm-directory>           → navigate to Vagrantfile location
vagrant up                  → power on existing VM
vagrant ssh                 → SSH into VM as 'vagrant' user
```

***

## Orientation Toolkit (First 4 Commands)

```
whoami              → current username
pwd                 → current absolute path (where am I?)
ls                  → contents of current directory
cat <filepath>      → read/display a file
```

***

## Privilege Model

```
vagrant user ($)  ──sudo -i──▶  root user (#)

$  = normal user shell     (limited operations)
#  = root user shell       (full system control)
~  = current user's home   (vagrant: /home/vagrant │ root: /root)

cd (no args) = always return to current user's home directory
```

***

## The Critical `/` vs `/root` Distinction

```
/           = ROOT DIRECTORY (top of entire filesystem, contains EVERYTHING)
/root       = root user's HOME DIRECTORY (one folder inside /)

/           contains →  bin, boot, etc, home, root, sbin, tmp, var, proc, sys ...
/root       is just one of those contained directories
```

***

## Linux Directory Structure Map

```
/ (root directory — top of everything)
├── /bin        User executables (whoami, pwd, ls, mv, scp, yum)
├── /sbin       System executables (mkfs.ext4, reboot) — root/sudo required
├── /etc        Configuration files (hostname, yum, network configs)
│                 → editable via vi editor
├── /home       Normal users' home directories (/home/<username>)
├── /root       Root user's home directory
├── /boot       Kernel (vmlinuz) + initramfs + grub2 bootloader config
├── /tmp        Temporary files — NOT persistent, used by scripts/tools
├── /var        Variable/server data (logs, mail, web content)
├── /srv        Server data
├── /opt        Optional/third-party software
├── /media      Auto-mounted removable media
├── /mnt        Manual mount points
├── /proc       Virtual FS — dynamic system info (uptime, memory, processes)
├── /sys        Virtual FS — kernel/device system info
└── /usr        User system resources
```

***

## Path Types

```
Absolute:   starts with /     →  /etc/hostname  (works from anywhere)
Relative:   no leading /      →  cd bin         (depends on current location)
```

***

## Key Relationships

```
/bin vs /sbin         = user-level vs system-level privilege separation at filesystem level
/home/<user> vs /root = normal user home vs root user home
Commands vs /proc     = commands (uptime, free) are human-readable wrappers around /proc raw data
/etc                  = central control plane for all system/app configuration
/tmp                  = ephemeral scratch space (never trust for persistence)
```

***

## Commands Demonstrated

```
clear                    → clear terminal screen
sudo -i                  → switch to root login shell
cd /                     → go to root directory
cd                       → go to current user's home
cd /bin | cd bin          → absolute vs relative navigation
cat /etc/os-release      → check OS name/version
cat /etc/hostname        → check/verify hostname
uptime                   → system uptime + load (reads /proc/uptime)
free -m                  → RAM usage in MB (reads /proc/meminfo)
```

***

## Reusable Patterns

```
PATTERN 1: Privilege Separation at Every Layer
  Users: normal ($) vs root (#)
  Filesystem: /bin vs /sbin
  Prompt: visual indicator of current privilege level
  → Defense-in-depth: identity, filesystem, and UI all enforce the boundary

PATTERN 2: "Everything is a File"
  Config   → files in /etc
  Programs → files in /bin, /sbin
  System state → virtual files in /proc, /sys
  VMs → files on host (from previous lecture)
  → Uniform interface enables scripting, automation, inspection with same tools

PATTERN 3: Commands as Abstraction Over Raw Data
  uptime command → reads /proc/uptime → formats for humans
  free -m        → reads /proc/meminfo → formats for humans
  → Commands are UI layers over filesystem-exposed kernel data

PATTERN 4: Purpose-Driven Directory Architecture
  Each directory has ONE clear responsibility
  No ambiguity about where things belong
  → Predictable system layout enables navigation without memorization
```

***

This gives you complete orientation capability on any Linux system. The next logical steps in the course will be **editing files (vi editor)**, **package management (yum)**, and **deeper command-line operations** — all of which build directly on this directory structure understanding. Ready for the next lecture whenever you are! 🚀
