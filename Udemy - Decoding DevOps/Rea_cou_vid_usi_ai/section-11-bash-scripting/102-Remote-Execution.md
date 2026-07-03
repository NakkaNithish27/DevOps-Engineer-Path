# 🎓 Deep Learning Material: Remote Command Execution over SSH

*Reconstructed from video lecture captions (102-remote-command-execution.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Core Idea: Remote Command Execution

The central concept of this lecture is **executing commands on remote machines from a central control machine without manually logging in, running the command, and logging out**. The instructor calls the control machine the **"script box"** and the target machines **web01, web02, and web03**. The script box is where you write and execute your scripts; the web servers are where those commands actually run. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The mechanism that makes this possible is **SSH (Secure Shell)**. Normally, when you SSH into a machine (`ssh user@host`), you get an **interactive shell** — you land inside the remote machine, run commands manually, and then exit. But SSH has a second mode: if you append a command after the host name (`ssh user@host <command>`), SSH logs in, executes that single command on the remote machine, and **immediately returns you to the local machine**. There is no interactive shell session. The command runs remotely, its output is displayed locally, and you're back where you started. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The instructor demonstrates this explicitly: *"When you do SSH, it gives us the shell. But if with that we give a command, let's say uptime — it executed uptime command, and then we are still in the script box. So we really don't need to login, execute command and log out. We can execute the command from here itself."* [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

This is the foundational mechanism behind all remote automation in DevOps. Configuration management tools like Ansible, remote deployment scripts, and multi-server orchestration systems all rely on this capability — the ability to issue commands from a central point that execute on remote targets.

🔍 **Deep Dive:**
The two SSH modes represent fundamentally different interaction models. **Interactive mode** (`ssh user@host`) establishes a persistent session — the remote shell stays open, waiting for input until you explicitly `exit`. **Command mode** (`ssh user@host <command>`) establishes a transient session — SSH connects, authenticates, runs the command in a non-interactive shell on the remote side, captures the output, sends it back, and tears down the connection. The exit code of the remote command becomes the exit code of the local SSH command, which means you can chain remote commands with `&&` or check their success in scripts using `$?`.

***

## 1.2 The Multi-Machine Architecture

The environment consists of four machines, all managed by Vagrant: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

| Machine       | Role                         | OS               | IP Address    |
| ------------- | ---------------------------- | ---------------- | ------------- |
| **scriptbox** | Control/central machine      | (CentOS implied) | —             |
| **web01**     | Target web server            | CentOS           | 192.168.56.13 |
| **web02**     | Target web server            | CentOS           | 192.168.56.14 |
| **web03**     | Target web server (optional) | Ubuntu Bionic 64 | 192.168.56.15 |

The instructor deliberately introduces **web03 as an Ubuntu machine** to demonstrate that different operating systems have different defaults and different commands — a critical real-world scenario. He explicitly notes this is optional if you lack resources, but he proceeds with it because *"we will be using some techniques in our script that we have learned previously to execute script for a different operating system."* [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

This multi-OS setup teaches an important operational truth: in real infrastructure, you rarely manage a homogeneous fleet. You will encounter CentOS, Ubuntu, Amazon Linux, Debian — and commands for user management, service management, and SSH configuration differ across them. A robust automation approach must account for these differences.

***

## 1.3 Hostname Configuration: Machine Identity

The first preparation step is setting the **hostname** on each machine by editing `/etc/hostname`. The instructor sets web01's hostname to `web01`, web02's to `web02`, and web03's to `web03`. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The hostname serves a critical operational purpose: **it identifies which machine you're currently on in the shell prompt**. The instructor explains this directly: *"When we log in to that machine, we can see we're connected to that machine. So that was the benefit of setting the hostname."*  When you're SSH-ing between multiple machines rapidly, the shell prompt showing the hostname is your primary visual confirmation that you're executing commands on the correct machine. Without distinct hostnames, every machine's prompt looks the same, and you risk running destructive commands on the wrong server. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

***

## 1.4 Name-to-IP Mapping: The `/etc/hosts` File

After setting hostnames, the instructor configures the **`/etc/hosts` file on the script box** to map machine names to their IP addresses. This allows the script box to refer to remote machines by **name** (web01, web02, web03) instead of IP addresses (192.168.56.13, 192.168.56.14, 192.168.56.15). [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The `/etc/hosts` file is a local DNS-like mechanism. When any program on the script box tries to resolve a hostname (e.g., when SSH tries to connect to "web01"), the system first checks `/etc/hosts`. If it finds a matching entry, it uses the corresponding IP address without consulting any external DNS server. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The instructor validates this by pinging: *"Let's try to ping web01 from script box. It should result in the IP address."*  If the ping resolves the name to the correct IP and gets a response, the mapping is working. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

This is operationally important for two reasons. First, **readability**: `ssh devops@web01` is far more readable in a script than `ssh devops@192.168.56.13`. Second, **maintainability**: if an IP address changes, you update one line in `/etc/hosts` instead of finding and replacing the IP in every script.

***

## 1.5 SSH Authentication: Password vs. Key-Based Login

This is where the lecture surfaces a critical operational difference between CentOS and Ubuntu defaults. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

When the instructor SSHs from script box to **web01** and **web02** (CentOS), SSH asks for a **password**. The user types the password, authentication succeeds, and they're logged in. This is **password-based authentication** — the standard interactive model where the user proves their identity by knowing a secret.

When the instructor tries the same with **web03** (Ubuntu), something different happens: *"It says permission denied public. It's not even asking the password for vagrant user."*  The connection is immediately rejected without even prompting for a password. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The cause is a configuration setting in the SSH daemon's config file: **`/etc/ssh/sshd_config`**. On Ubuntu, the line `PasswordAuthentication no` (at line 56 in the video) means the SSH server **refuses to accept passwords at all**. It only accepts **key-based authentication** — where the client proves its identity using a cryptographic key pair rather than a password. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The instructor's diagnostic approach is important: *"To any Linux machine, if you're trying to login with password and if it throws you that error, 'public access denied', then huge chances the password login is disabled. So open this file and find the line PasswordAuthentication."*  This is a reusable troubleshooting pattern: SSH rejection without password prompt → check `sshd_config` → look for `PasswordAuthentication`. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The fix is to change `PasswordAuthentication no` to `PasswordAuthentication yes` and restart the SSH service. On Ubuntu, the SSH service name is simply `ssh` (not `sshd` as on CentOS). [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

🔍 **Deep Dive:**
Since password login is disabled on Ubuntu's web03, the instructor cannot SSH into it from the script box. Instead, he uses `vagrant ssh web03` from the **host machine**. This works because Vagrant uses its own pre-configured SSH key pair (inserted during `vagrant up`) to authenticate — it doesn't need password authentication. This highlights an important distinction: `vagrant ssh` uses Vagrant's managed keys, while manual `ssh user@host` from within VMs uses whatever authentication methods the SSH server allows. They are two different SSH sessions with different authentication paths.

⚠️ **Expert Note:**
Enabling password authentication is convenient for learning but is considered a **security downgrade** in production. Password-based SSH is vulnerable to brute-force attacks. Production servers typically use key-based authentication exclusively, with password auth disabled. The instructor enables it here for practical convenience in a lab environment, not as a production recommendation.

***

## 1.6 User Creation: CentOS vs. Ubuntu Commands

The instructor creates a dedicated **`devops` user** on all three web servers for remote command execution. The commands differ by operating system: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

* **CentOS (web01, web02):** `useradd devops` — creates the user. Password is set separately.
* **Ubuntu (web03):** `adduser devops` — an interactive wrapper that creates the user and prompts for password and additional info in one step.

This difference is not just cosmetic. `useradd` is the low-level binary present on all Linux distributions, but it requires manual steps for password setting. `adduser` on Ubuntu/Debian is a higher-level script that wraps `useradd` with interactive prompts, making it more user-friendly but also more opinionated. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

***

## 1.7 Sudoers Configuration: Passwordless Privilege Escalation

The `devops` user needs to execute **system-level commands** (installing packages, managing services) on the remote machines. These operations require root privileges. The solution is to add the `devops` user to the **sudoers file** with the **NOPASSWD** directive. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

The instructor edits the sudoers file (using `visudo` on Ubuntu, direct editing on CentOS) and adds a line granting `devops` the ability to run any command as root **without being prompted for a password**. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

Why NOPASSWD? Because the goal is **remote execution from a script**. If `sudo` on the remote machine prompts for a password, a remote command like `ssh devops@web01 sudo yum install httpd -y` would hang waiting for password input that cannot be provided non-interactively. NOPASSWD eliminates this blocking point, making remote sudo commands fully automatable. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

On Ubuntu, the instructor first sets the default editor to vim (`export EDITOR=vim`) before running `visudo`. This is because `visudo` uses the system's default editor, which on Ubuntu is typically `nano`. The `EDITOR` environment variable overrides this default. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

🔍 **Deep Dive:**
`visudo` is specifically designed for editing the sudoers file safely. Unlike directly editing `/etc/sudoers` with a text editor, `visudo` performs **syntax validation** before saving. If you introduce a syntax error in the sudoers file (as the instructor almost does — *"Oops, I made a syntax error"*), `visudo` catches it and prevents the save. A corrupted sudoers file can lock you out of `sudo` entirely, making the machine very difficult to administer. This is why `visudo` exists and why direct editing is risky.

***

## 1.8 The Preparation vs. Execution Distinction

The instructor explicitly marks a boundary in the lecture: *"So what are we doing so far in this lecture was the preparations, so we can execute command over SSH or remote execution."* [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

Everything before this point — setting hostnames, configuring `/etc/hosts`, enabling password auth, creating users, configuring sudoers — is **infrastructure preparation**. None of it is the actual remote execution. This distinction is important because in real DevOps work, the preparation (provisioning users, configuring SSH, setting up networking) is typically done **once** (often automated via provisioning tools), while the remote execution is done **repeatedly** as part of ongoing operations.

The preparation creates the **trust relationship** and **authorization pathway** between the control machine and the target machines. Once this is established, the actual remote execution becomes a simple, repeatable operation.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a **remote execution environment** where a central machine (script box) can execute commands on multiple web servers (web01, web02, web03) over SSH without manual interactive login. The final outcome: from the script box, running `ssh devops@web01 <command>` executes the command on web01 and returns the output to the script box — no interactive session needed. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

***

## Phase 1: Infrastructure Setup (Vagrant)

### Step 1: Modify the Vagrantfile

Add web03 (Ubuntu Bionic 64) to the existing Vagrantfile alongside web01 and web02. Assign IP addresses: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```
web01  → 192.168.56.13
web02  → 192.168.56.14
web03  → 192.168.56.15
```

**Note:** Web03 is optional. If your machine lacks resources (RAM/CPU), skip it. The instructor adds it to demonstrate multi-OS handling. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

### Step 2: Bring Up All Machines

```bash
vagrant up
```

**What happens:** Vagrant reads the Vagrantfile and creates/starts all defined VMs (scriptbox, web01, web02, web03). Each gets its assigned OS and IP address.

***

## Phase 2: Hostname Configuration

### Step 3: Set Hostname on Each Machine

Log into each machine and edit `/etc/hostname`:

**For web01:**

```bash
vagrant ssh web01
sudo -i
vim /etc/hostname
```

Set the content to `web01`. Save and exit. Log out. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Repeat for web02** (set to `web02`) and **web03** (set to `web03`).

**Why:** The hostname appears in the shell prompt. When SSH-ing between machines, this is your visual confirmation of which machine you're on (see Theory 1.3).

**Verification:** After logging back in, the prompt should display the machine's hostname.

***

## Phase 3: Name Resolution Setup

### Step 4: Note Down IP Addresses

Record the IP addresses of all target machines: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```
web01 → 192.168.56.13
web02 → 192.168.56.14
web03 → 192.168.56.15
```

### Step 5: Configure `/etc/hosts` on the Script Box

```bash
vagrant ssh scriptbox
sudo -i
vim /etc/hosts
```

Add entries mapping names to IPs: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```
192.168.56.13  web01
192.168.56.14  web02
192.168.56.15  web03
```

Save and exit.

### Step 6: Verify Name Resolution

```bash
ping web01
ping web02
ping web03
```

 [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Expected output:** Each ping should resolve to the correct IP address and receive responses. If ping resolves the name but gets no response, the VM might not be running. If ping fails to resolve the name, the `/etc/hosts` entry has a typo.

**Connection to flow:** Name resolution must work before any SSH operation. SSH needs to translate `web01` into an IP address to connect.

***

## Phase 4: SSH Connectivity Test

### Step 7: Test SSH from Script Box to Web01

```bash
ssh vagrant@web01
```

 [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Breakdown:**

* `ssh` — Secure Shell client
* `vagrant` — Username to log in as (default Vagrant user)
* `web01` — Target machine (resolved via `/etc/hosts`)

**What happens:**

1. SSH asks: *"Should I login?"* (first-time host key verification) — type `yes`
2. SSH asks for the password — type `vagrant` (default Vagrant password)
3. You're now inside web01 — the prompt shows the web01 hostname

**Verification:** The prompt changes to show `web01`. Run `hostname` to confirm. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```bash
logout
```

Return to script box.

### Step 7a: Test SSH to Web03 (Ubuntu) — The Failure

```bash
ssh vagrant@web03
```

 [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Expected failure:** `Permission denied (publickey)` — no password prompt appears at all.

**Cause:** Ubuntu has `PasswordAuthentication no` in `/etc/ssh/sshd_config` by default (see Theory 1.5).

**Recovery — must access web03 via Vagrant from the host machine:**

```bash
logout          # exit scriptbox back to host
vagrant ssh web03
sudo -i
```

 [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

### Step 8: Enable Password Authentication on Web03

```bash
vim /etc/ssh/sshd_config
```

Find line 56 (approximately): `PasswordAuthentication no`

Change to: `PasswordAuthentication yes`

Save and exit. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Restart the SSH service:**

```bash
systemctl restart ssh
```

 [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Important:** On Ubuntu, the SSH service name is `ssh`, not `sshd` (which is the CentOS convention).

**Verification:** Log out back to script box, then:

```bash
ssh vagrant@web03
```

It should now **ask for the password**. Enter `vagrant`. You should successfully log in. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

***

## Phase 5: User and Privilege Setup

### Step 9: Create the `devops` User on CentOS Machines (web01, web02)

From script box, SSH into each CentOS machine:

```bash
ssh vagrant@web01
sudo -i
```

Create the user: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```bash
useradd devops
passwd devops
```

**Breakdown:**

* `useradd devops` — Creates a new user account named `devops`
* `passwd devops` — Sets the password for the `devops` user (you'll be prompted to type it twice)

### Step 10: Add `devops` to Sudoers with NOPASSWD (CentOS)

```bash
visudo
```

Add the following line: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```
devops ALL=(ALL) NOPASSWD: ALL
```

**Breakdown:**

* `devops` — The user this rule applies to
* `ALL=(ALL)` — From any host, can run as any user
* `NOPASSWD: ALL` — Can run all commands without entering a password for sudo

Save and exit. Log out. Repeat for web02. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Common mistake:** Syntax errors in the sudoers file. The instructor makes one during the lecture. Always use `visudo` which validates syntax before saving.

### Step 11: Create the `devops` User on Ubuntu (web03)

SSH into web03 and switch to root:

```bash
ssh vagrant@web03
sudo -i
```

On Ubuntu, use `adduser` instead of `useradd`: [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```bash
adduser devops
```

This interactively prompts for password and user information.

### Step 12: Add `devops` to Sudoers on Ubuntu

Set the editor to vim first (Ubuntu defaults to nano): [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

```bash
export EDITOR=vim
visudo
```

Add the same line:

```
devops ALL=(ALL) NOPASSWD: ALL
```

Save and exit. Log out back to script box. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

***

## Phase 6: Remote Command Execution

### Step 13: Test Interactive SSH with the `devops` User

```bash
ssh devops@web01
```

 [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

Enter the devops password. You should land in an interactive shell on web01.

```bash
logout
```

### Step 14: Execute a Remote Command Without Interactive Login

This is the core technique of the entire lecture:

```bash
ssh devops@web01 uptime
```

 [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Breakdown:**

* `ssh` — SSH client
* `devops@web01` — Log in as `devops` user on `web01`
* `uptime` — The command to execute **on the remote machine**

**What happens internally:**

1. SSH connects to web01
2. Authenticates as `devops` (asks for password)
3. Executes `uptime` on web01 in a non-interactive shell
4. Captures the output and displays it on the script box terminal
5. The SSH connection closes
6. **You are still on the script box** — you never entered an interactive session

**Verification:** Check your prompt after the command completes — it should still show the script box hostname, not web01. [\[102-remote...-execution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/102-remote-command-execution.txt)

**Connection to the larger system:** This is the atomic operation that all remote automation builds upon. A script can loop through multiple servers, executing commands on each one remotely, without ever entering an interactive session.

⚠️ **Expert Note:**
In this demonstration, SSH still prompts for a password. In full automation, you would set up **SSH key-based authentication** between the script box and all target machines, eliminating the password prompt entirely. Combined with NOPASSWD in sudoers, this creates a fully non-interactive execution pipeline: `ssh devops@web01 sudo yum install httpd -y` would execute silently, install the package with root privileges, and return — zero human interaction required. Key-based auth setup is implied as a next step but not covered in this lecture.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Architecture

```
[Script Box] ──SSH──→ [web01] CentOS  (192.168.56.13)
      │
      ├────SSH──→ [web02] CentOS  (192.168.56.14)
      │
      └────SSH──→ [web03] Ubuntu  (192.168.56.15)

Control model: Central → Targets (one-to-many)
Protocol: SSH
User: devops (created on all targets, sudoers NOPASSWD)
```

***

## Two SSH Modes

```
INTERACTIVE:     ssh devops@web01         → lands in remote shell → manual work → exit
COMMAND MODE:    ssh devops@web01 uptime  → runs command → shows output → stays local

Command mode = the foundation of remote automation
```

***

## Preparation Stack (Done Once)

```
1. HOSTNAMES     /etc/hostname on each machine → visual identity in prompt
2. NAME MAPPING  /etc/hosts on scriptbox → name→IP resolution (web01→192.168.56.13)
3. SSH ACCESS    PasswordAuthentication yes (Ubuntu fix) → allows password login
4. USER SETUP    devops user on all targets → dedicated execution identity
5. SUDO ACCESS   visudo → devops NOPASSWD → passwordless privilege escalation

Preparation = trust + authorization + reachability
Execution = ssh user@host command (repeatable)
```

***

## CentOS vs. Ubuntu Differences

```
                CentOS                    Ubuntu
──────────────────────────────────────────────────────────
User creation:  useradd + passwd          adduser (interactive)
SSH default:    Password auth ON          Password auth OFF
SSH service:    sshd                      ssh
SSH config:     /etc/ssh/sshd_config      /etc/ssh/sshd_config (same)
visudo editor:  vim (default)             nano (default → export EDITOR=vim)
```

***

## SSH Password Auth Troubleshooting

```
ssh user@host → "Permission denied (publickey)" → NO password prompt
  └── Cause: /etc/ssh/sshd_config → PasswordAuthentication no
  └── Fix:   Change to "yes" → systemctl restart ssh (Ubuntu) / sshd (CentOS)
  
Diagnostic rule: No password prompt = password auth disabled in sshd_config
```

***

## Sudoers Entry

```
devops ALL=(ALL) NOPASSWD: ALL

devops   = user
ALL      = from any host
(ALL)    = can act as any user
NOPASSWD = no sudo password prompt
ALL      = for all commands

Purpose: Remote sudo commands must not hang waiting for password input
Tool: visudo (syntax-validates before saving → protects against lockout)
```

***

## Operational Sequence (Complete)

```
── VAGRANT SETUP ──
Edit Vagrantfile → add web03 (Ubuntu), assign IPs
vagrant up → all 4 machines running

── HOSTNAME SETUP (each machine) ──
vagrant ssh <machine> → sudo -i
vim /etc/hostname → set name → logout

── NAME RESOLUTION (scriptbox only) ──
vim /etc/hosts → add web01/02/03 IP mappings
ping web01/02/03 → verify resolution

── SSH FIX (Ubuntu web03 only) ──
vagrant ssh web03 (from host, key-based)
vim /etc/ssh/sshd_config → PasswordAuthentication yes
systemctl restart ssh → logout

── USER SETUP (each target) ──
ssh vagrant@webXX → sudo -i
CentOS: useradd devops + passwd devops
Ubuntu: adduser devops
visudo → devops ALL=(ALL) NOPASSWD: ALL → logout

── REMOTE EXECUTION ──
ssh devops@web01 uptime → runs remotely, returns locally
```

***

## Cause → Effect Chains

```
No hostname set → all prompts look identical → risk of wrong-machine commands
No /etc/hosts entry → must use IP addresses → poor readability, hard maintenance
PasswordAuth=no (Ubuntu) → ssh rejects with "publickey" → cannot login with password
No devops user → must use vagrant user → not a clean separation of concerns
No NOPASSWD → remote sudo commands hang waiting for password → blocks automation
No visudo → direct edit risk → syntax error → sudo lockout
```

***

## Reusable Engineering Patterns

| Pattern                                  | Manifestation                                                       |
| ---------------------------------------- | ------------------------------------------------------------------- |
| **Central controller → remote targets**  | Script box sends commands; web servers execute                      |
| **Preparation vs. execution separation** | Setup once (users, keys, config) → execute many times               |
| **Name abstraction over addresses**      | `/etc/hosts` decouples scripts from IP changes                      |
| **Dedicated execution identity**         | `devops` user — not root, not vagrant; purpose-built                |
| **OS-aware operations**                  | Different commands/configs for CentOS vs. Ubuntu                    |
| **Diagnostic pattern**                   | Symptom (no password prompt) → config check → fix → restart service |
| **Non-interactive authorization**        | NOPASSWD + (future) SSH keys = zero human interaction               |

***

## Core Mental Model

```
Remote execution = SSH in command mode

Prerequisites (the trust chain):
  Reachability:  network + name resolution (/etc/hosts)
  Authentication: SSH password or key-based login
  Authorization:  user exists + sudoers NOPASSWD

Once the trust chain is complete:
  ssh devops@webXX <any_command>
  = runs on remote, output on local, no interactive session

This is the atomic unit of all remote automation.
```

***

This material captures every concept, command, troubleshooting step, OS difference, and architectural relationship from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
