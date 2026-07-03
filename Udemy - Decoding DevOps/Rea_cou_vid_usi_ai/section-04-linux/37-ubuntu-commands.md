# Ubuntu Operating System Commands — Complete Deep Learning Material

*Reconstructed from the video lecture on Ubuntu-specific commands and their differences from CentOS* [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. Ubuntu vs CentOS — Same Core, Different Surface

Linux distributions share the same kernel and a vast majority of commands, but they differ in specific tooling, package management, and default behaviors. Ubuntu and CentOS are the two distributions used in this course, and the lecture establishes a critical mental model: **most commands you learned on CentOS work identically on Ubuntu**. The differences are concentrated in a few specific areas — user creation, default editor, and package management. Understanding these differences is not about memorizing two separate operating systems; it's about recognizing **which layer changes and which stays stable** across distributions. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

Ubuntu belongs to the **Debian** family of Linux distributions, while CentOS belongs to the **Red Hat** family. This ancestry determines the package format (`.deb` vs `.rpm`), the package manager (`apt` vs `yum`), and some default tool choices. The underlying filesystem structure, user management concepts, permissions model, and shell behavior remain fundamentally the same. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

## 2. User Creation — `useradd` vs `adduser`

In CentOS, the `useradd` command creates a user with all essential components: home directory, mail spool, default shell, and skeleton files. In Ubuntu, **`useradd` exists but behaves differently** — it creates the user entry but does **not** create the home directory, does not set up the mail spool, and does not perform other initialization steps. If you switch to a user created with `useradd` on Ubuntu, you'll land in the root directory (`/`) instead of a home directory, because no home directory was created. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

The Ubuntu-preferred command is **`adduser`** (note: `adduser`, not `useradd`). `adduser` is a higher-level, interactive wrapper that performs the complete user setup: it creates the user, creates a group with the same name, adds the user to that group, creates the home directory, copies skeleton files from `/etc/skel` into the new home directory, prompts for a password, and optionally collects additional information (full name, room number, work phone). This is the same end result that CentOS's `useradd` achieves, but through a different command name and an interactive flow. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

The skeleton directory **`/etc/skel`** is mentioned as the source of default files copied into every new user's home directory. These are template files (like `.bashrc`, `.profile`) that provide the initial shell configuration for the user. This mechanism is common to both distributions — the difference is only in which command triggers the copy automatically. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

🔍 **Deep Dive:** You *can* use `useradd` on Ubuntu with additional options to manually specify the home directory and other settings, but `adduser` is the idiomatic Ubuntu approach because it handles everything in one interactive flow. The `userdel -r` command works the same on both systems — the `-r` flag removes the home directory and mail spool. On Ubuntu, if these were never created (because `useradd` was used), `userdel -r` reports that no home directory or mail spool was found.

All other user management commands — `passwd`, `groupadd`, `usermod` — work identically on both distributions. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

## 3. Default Editor Difference — nano vs vim

On CentOS, when you run `visudo`, it opens the sudoers file in **vim**. On Ubuntu, the default editor is **nano** — a simpler, different text editor. When you run `visudo` on Ubuntu, it opens in nano instead of vim. If you're comfortable with nano, this is fine. If you prefer vim (as taught throughout the course), you need to change the default editor. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

The command **`export EDITOR=vim`** sets an **environment variable** called `EDITOR` to the value `vim`. This tells the system: "whenever a program needs to open a text editor, use vim." After running this command, `visudo` opens in vim as expected. However, this setting is **temporary** — it applies only to the current shell session. If you log out and log back in, the variable is gone and nano becomes the default again. The lecture mentions that making this permanent is covered in Bash scripting (it involves adding the export command to a shell configuration file like `.bashrc`). [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

🔍 **Deep Dive:** The `export` keyword makes the variable available to child processes (not just the current shell). `EDITOR` is a well-known environment variable that many Linux programs respect — not just `visudo`, but also `crontab -e`, `git commit`, and other tools that invoke an editor. This is a general Linux mechanism: behavior is configured through environment variables rather than application-specific settings.

***

## 4. Package Management — The Major Divergence

Package management is where Ubuntu and CentOS differ most significantly. The entire ecosystem — package format, package manager tool, repository configuration, and operational workflow — changes between the two distribution families. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### 4.1 Package Format: `.deb` vs `.rpm`

CentOS uses **RPM** (Red Hat Package Manager) format packages. Ubuntu uses **Debian packages** (`.deb` format). These are different binary package formats — you cannot install a `.deb` on CentOS or an `.rpm` on Ubuntu. When the lecture downloads a package manually, it downloads a `.deb` file for tree from `ubuntu.package.org`. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### 4.2 Low-Level Package Tool: `dpkg`

**`dpkg`** is the low-level Debian package manager — it operates on individual `.deb` files directly. It is the Ubuntu equivalent of the `rpm` command on CentOS. `dpkg` can install a downloaded `.deb` file, list all installed packages, search for a specific package, and remove packages. However, like `rpm`, `dpkg` does **not handle dependencies** — it works with single package files in isolation. If a package requires other packages, `dpkg` will not automatically fetch them. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### 4.3 High-Level Package Manager: `apt`

**`apt`** is Ubuntu's high-level package manager — the equivalent of `yum` on CentOS. `apt` handles dependency resolution automatically: when you install a package that requires other packages, `apt` downloads and installs all dependencies. It communicates with online **repositories** to find, download, and install packages. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

Repository information is configured in **`/etc/apt/sources.list`** — this file contains URLs pointing to package repositories around the world. You can add additional repository URLs to this file to access more software. The lecture notes that this is where **Ubuntu really beats Red Hat systems** — Ubuntu/Debian has access to "tons and tons of software" from many repositories worldwide, giving it a broader software ecosystem. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

There is also **`apt-get`**, which is the older version of the `apt` command. The lecture mentions it but recommends using `apt` (the newer, more user-friendly interface). [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### 4.4 The `apt update` Requirement — A Critical Workflow Difference

Before installing any software on Ubuntu, you should run **`apt update`**. This command contacts all configured repositories, checks for the latest available packages, and **updates the local package list**. This is a mandatory step because `apt` works from a cached local list — if the list is outdated, you may not find packages or may install older versions.

This is a workflow difference from CentOS: **`yum` does not require a separate update step** — it automatically searches repositories, creates its list, and refreshes it every 24 hours. On Ubuntu, the update step is explicit and manual. The mental model: `apt update` refreshes the **index/catalog**, not the actual packages. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

**`apt upgrade`** is a different command entirely — it actually **upgrades all installed packages** to their latest versions from the repositories. `update` refreshes the list; `upgrade` upgrades the software. This distinction is a common point of confusion. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

## 5. Service Behavior Difference — Auto-Start on Install

When you install a service package on Ubuntu (like Apache2), **it starts automatically after installation and is also enabled to start on boot**. You don't need to manually run `systemctl start` or `systemctl enable` — Ubuntu does both by default. On CentOS, services typically need to be started and enabled manually after installation. This is a significant operational difference: on Ubuntu, installing a service means it's immediately live and serving traffic. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

The lecture verifies this with Apache2: after `apt install apache2`, checking the service status shows it as **active (running)** and **enabled**. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

⚠️ **Expert Note:** The auto-start behavior is convenient for development but can be surprising in production. Installing a service on Ubuntu means it's immediately listening on its port — if you intended to configure it first before exposing it to traffic, you've already missed that window. In production pipelines, some teams disable auto-start during installation and enable services only after configuration is complete.

***

## 6. Service Name Differences — Apache2 vs httpd

The same software can have different package names across distributions. The Apache web server is called **`httpd`** on CentOS and **`apache2`** on Ubuntu. This is purely a naming convention difference — the underlying software is identical. The lecture explicitly maps this: "Apache2 which is same as httpd." [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

## 7. `apt remove` vs `apt purge` — Clean vs Dirty Uninstall

`apt` provides two levels of package removal. **`apt remove`** uninstalls the package binaries but **leaves configuration files and data behind**. This is useful if you plan to reinstall later and want to keep your settings. **`apt purge`** removes the package along with **all its configuration and data** — a complete, clean uninstall. The lecture describes `apt purge` as "a clean uninstall." [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

## 8. UFW — Ubuntu Firewall

When installing or uninstalling network services like Apache2, Ubuntu also **updates firewall rules** through **UFW (Uncomplicated Firewall)**. This is mentioned briefly — UFW is Ubuntu's firewall management tool. The lecture notes this as a difference but does not go into depth, indicating it will be covered later. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning to operate Ubuntu by working through the specific commands and workflows that differ from CentOS. The final outcome: you can create users, manage packages, install/remove services, and navigate the `apt` ecosystem on Ubuntu confidently, knowing exactly where Ubuntu diverges from CentOS and where everything stays the same. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

## Step 1: Bring Up and Log Into the Ubuntu VM

Navigate to the Ubuntu VM folder and start it:

```bash
cd /f/vagrant-vms/ubuntu
vagrant global-status
```

* Confirms both VMs exist — CentOS (powered off) and Ubuntu (powered off). [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

```bash
vagrant up
```

* VM already exists, so this simply powers it on.

```bash
vagrant ssh
```

* Logs in as the `vagrant` user.

Verify the OS:

```bash
cat /etc/os-release
```

* Confirms Ubuntu 22.

Switch to root:

```bash
sudo -i
whoami
pwd
```

* Confirms root user, home directory `/root`. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

***

## Step 2: User Creation — The Ubuntu Way

### Demonstrate the `useradd` Problem

```bash
useradd devops
```

* Creates the user entry but **no home directory, no mail spool**.

Switch to that user to see the effect:

```bash
su - devops
pwd
```

* You land in `/` (root of filesystem), not `/home/devops`. No home directory exists. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

Exit back to root and clean up:

```bash
exit
userdel -r devops
```

* **`userdel`** = delete user.
* **`-r`** = remove home directory and mail spool.
* Output warns: "no home directory found" and "no mail spool found" — because `useradd` never created them. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### Use `adduser` Instead (Correct Ubuntu Approach)

```bash
adduser devops
```

Interactive output flow:

1. Creates user `devops`
2. Creates group `devops`
3. Adds user `devops` to group `devops`
4. Creates home directory `/home/devops`
5. Copies files from `/etc/skel` to `/home/devops`
6. Prompts for **password** — enter it
7. Prompts for optional info (full name, room number, work phone) — press Enter to skip each
8. Confirm with `Y` [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

**Verification:** The user `devops` is now fully functional with a home directory, group, and password.

**All other user commands work the same as CentOS:** `passwd`, `groupadd`, `usermod`.

**Connection to flow:** User creation is settled. Next difference: the default editor.

***

## Step 3: Set Default Editor to vim

Run `visudo` to see the default behavior:

```bash
visudo
```

* Opens in **nano** editor (Ubuntu's default), not vim.
* Quit nano: press `Ctrl + X`. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

Set vim as the default editor:

```bash
export EDITOR=vim
```

* **`export`** = set an environment variable and make it available to child processes.
* **`EDITOR`** = the standard variable that programs check when they need to open a text editor.
* **`vim`** = the value — use vim.

Now run visudo again:

```bash
visudo
```

* Opens in **vim**. Quit with `:q`. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

⚠️ **This is temporary.** If you log out and log back in, nano becomes the default again. You must run `export EDITOR=vim` each session, or make it permanent (covered in Bash scripting section).

***

## Step 4: Manual Package Download and Install with `dpkg`

Search the web for **"tree debian package for Ubuntu"**. Find the `.deb` package URL on `ubuntu.package.org` (or similar mirror sites). Copy the binary package URL. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

Download the package:

```bash
wget <paste-URL-here>
```

* **`wget`** = download a file from the web (you can also use `curl`).
* Downloads the `.deb` file to the current directory. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

Install it with `dpkg`:

```bash
dpkg -i tree
```

* **`dpkg`** = Debian Package manager (low-level tool).
* **`-i`** = install.
* Installs the `tree` package from the local `.deb` file.

Verify:

```bash
tree
```

* Should display directory structure — the command works. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

List all installed packages:

```bash
dpkg -l
```

* **`-l`** = list all installed debian packages.

Search for a specific package:

```bash
dpkg -l | grep tree
```

* **`|`** = pipe output to next command.
* **`grep tree`** = filter lines containing "tree".

Remove the package:

```bash
dpkg -r tree
```

* **`-r`** = remove. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

**Connection to flow:** `dpkg` handles individual packages without dependency resolution — just like `rpm` on CentOS. For real-world use, the high-level `apt` tool is preferred.

***

## Step 5: Package Management with `apt`

### Explore Repository Configuration

```bash
cd /etc/apt
ls
cat sources.list
```

* **`sources.list`** contains URLs to package repositories. You can add new repository URLs here to access additional software. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### Update the Package List (REQUIRED before installing)

```bash
apt update
```

* Contacts all repositories in `sources.list`, checks for the latest available packages, and **refreshes the local package index**.
* This does NOT install or upgrade anything — it only updates the catalog.
* **Must be run before `apt install`** to ensure you're working with current data. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### Search for a Package

```bash
apt search tree
```

* Searches the (now-updated) package index for packages matching "tree". Returns many results. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### Install a Package

```bash
apt install tree
```

* Downloads and installs the `tree` package with all dependencies.
* `tree` has no dependencies, so it installs directly. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### Install a Service Package (Apache2)

```bash
apt install apache2
```

* **`apache2`** = Ubuntu's name for the Apache web server (called `httpd` on CentOS).
* Shows a list of dependencies that will also be installed, plus suggested packages.
* Confirm with `Y`.
* Downloads and installs apache2 and all its dependencies. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

**Auto-start behavior (Ubuntu-specific):** After installation, check the service:

```bash
systemctl status apache2
```

* Shows **active (running)** — the service started automatically.
* Press `Q` to exit the status view.

Check if enabled on boot:

```bash
systemctl is-enabled apache2
```

* Shows **enabled** — the service will start on every boot. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

No manual `systemctl start` or `systemctl enable` needed — Ubuntu handles both automatically on install. (Contrast with CentOS where you must do both manually.)

***

## Step 6: Upgrade All Packages

```bash
apt upgrade
```

* **Upgrades all installed packages** to their latest versions from the repositories.
* Shows how many packages will be upgraded and asks for confirmation.
* Enter `N` if you don't want to upgrade now. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

**Critical distinction:**

* `apt update` = refresh the **package index** (what's available)
* `apt upgrade` = upgrade the **installed packages** (actually change software)

***

## Step 7: Remove and Purge Packages

### Standard Remove (keeps config/data)

```bash
apt remove apache2
```

* Removes the apache2 binaries but **leaves configuration files and data**. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

### Clean Uninstall (removes everything)

First reinstall:

```bash
apt install apache2
```

Then purge:

```bash
apt purge apache2
```

* Removes the package **plus all configuration and data** — complete clean uninstall. [\[37-ubuntu-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/37-ubuntu-commands.txt)

**When installing or removing network services like Apache2**, Ubuntu also updates firewall rules via **UFW** (Ubuntu's firewall tool).

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## CentOS → Ubuntu Difference Map

```
SAME (no change):
  ├── Filesystem structure
  ├── Permissions model
  ├── passwd, groupadd, usermod
  ├── systemctl (start/stop/status/enable)
  ├── vim, cat, ls, cd, pwd, etc.
  └── sudo, visudo (behavior same, editor differs)

DIFFERENT:
  ├── User creation:   useradd (CentOS) → adduser (Ubuntu)
  ├── Default editor:  vim (CentOS) → nano (Ubuntu)
  ├── Package format:  .rpm (CentOS) → .deb (Ubuntu)
  ├── Low-level pkg:   rpm (CentOS) → dpkg (Ubuntu)
  ├── High-level pkg:  yum (CentOS) → apt (Ubuntu)
  ├── Web server name: httpd (CentOS) → apache2 (Ubuntu)
  ├── Firewall:        firewalld (CentOS) → ufw (Ubuntu)
  └── Service install: manual start/enable (CentOS) → auto-start+enable (Ubuntu)
```

***

## User Creation Comparison

```
CentOS:
  useradd <user> → creates user + home + mail + skel copy → done

Ubuntu:
  useradd <user> → creates user ONLY (no home, no mail, no skel) → broken
  adduser <user> → interactive: user + group + home + skel + password → complete

Delete (both): userdel -r <user>
```

***

## Editor Override

```
visudo → opens nano (Ubuntu default)
  ↓
export EDITOR=vim → sets env variable → visudo now opens vim
  ↓
TEMPORARY: lost on logout → re-run each session OR make permanent in .bashrc
```

***

## Package Management — Two Layers

```
Layer 1: Low-Level (single package, no dependency resolution)
  dpkg -i <pkg.deb>     → install
  dpkg -l               → list all installed
  dpkg -l | grep <name> → search installed
  dpkg -r <name>        → remove

Layer 2: High-Level (repositories, dependency resolution)
  apt update             → refresh package index (REQUIRED first)
  apt search <name>      → search available packages
  apt install <name>     → install with dependencies
  apt remove <name>      → remove (keep config/data)
  apt purge <name>       → remove + config + data (clean uninstall)
  apt upgrade            → upgrade ALL installed packages

Repository config: /etc/apt/sources.list (add URLs for more software)
```

***

## `apt update` vs `apt upgrade` — Critical Distinction

```
apt update  → refreshes the CATALOG (what's available) → no software changes
apt upgrade → upgrades the SOFTWARE (installs newer versions) → actual changes

Workflow: apt update → apt install/upgrade (always update index first)

CentOS yum: auto-refreshes every 24h → no separate update step needed
Ubuntu apt: manual refresh required → apt update before install
```

***

## Service Auto-Start (Ubuntu-Specific)

```
CentOS: apt install httpd → stopped + disabled → must manually start + enable
Ubuntu: apt install apache2 → RUNNING + ENABLED → immediately live

Verify:
  systemctl status apache2 → active (running)
  systemctl is-enabled apache2 → enabled
```

***

## `apt remove` vs `apt purge`

```
apt remove <pkg> → removes binaries → KEEPS config + data → reinstall restores settings
apt purge  <pkg> → removes binaries + config + data → CLEAN slate
```

***

## dpkg Command Quick-Reference

| Command                  | CentOS Equivalent        | Purpose               |
| ------------------------ | ------------------------ | --------------------- |
| `dpkg -i <file.deb>`     | `rpm -i <file.rpm>`      | Install local package |
| `dpkg -l`                | `rpm -qa`                | List all installed    |
| `dpkg -l \| grep <name>` | `rpm -qa \| grep <name>` | Search installed      |
| `dpkg -r <name>`         | `rpm -e <name>`          | Remove package        |

## apt Command Quick-Reference

| Command              | CentOS Equivalent    | Purpose               |
| -------------------- | -------------------- | --------------------- |
| `apt update`         | *(automatic in yum)* | Refresh package index |
| `apt search <name>`  | `yum search <name>`  | Search available      |
| `apt install <name>` | `yum install <name>` | Install with deps     |
| `apt remove <name>`  | `yum remove <name>`  | Remove (keep config)  |
| `apt purge <name>`   | *(no direct equiv)*  | Remove + clean config |
| `apt upgrade`        | `yum update`         | Upgrade all packages  |

***

## Reusable Engineering Patterns

| Pattern                                   | Manifestation                                                                                                                                             |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Same core, different interface**        | CentOS and Ubuntu share kernel, filesystem, permissions — differ only in tooling layer. Distribution differences are surface-level, not architectural.    |
| **Two-tier package management**           | Low-level tool (dpkg/rpm) handles single files; high-level tool (apt/yum) handles repositories + dependencies. Same abstraction pattern in both families. |
| **Explicit vs implicit index refresh**    | apt requires manual `update` before install; yum auto-refreshes. Trade-off: explicit control vs convenience.                                              |
| **Install-time activation**               | Ubuntu auto-starts services on install — convention-over-configuration. CentOS requires explicit activation — explicit-over-convention.                   |
| **Environment variable behavior control** | `export EDITOR=vim` changes program behavior without modifying the program. System-wide pattern for configuring tool defaults.                            |
| **Remove vs purge (graduated cleanup)**   | Two levels of uninstall — keep state (remove) vs clean slate (purge). Same pattern in many systems: soft delete vs hard delete.                           |

***

This completes the full reconstruction. **Theory** explains *why* Ubuntu differs and what the conceptual model behind each difference is. **Practical** walks through every command with exact syntax and expected results. The **Compression Map** gives you an instant side-by-side CentOS↔Ubuntu reference, the apt workflow chain, and the reusable patterns — all designed for rapid recall when you're switching between the two systems. 🚀
