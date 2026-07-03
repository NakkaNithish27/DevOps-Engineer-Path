# 🎓 Deep Learning Material: Ansible Inventory File & Ping Module

**Source:** [233-inventory-and-ping-module.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt?EntityRepresentationId=dbc9af3c-4896-4992-ba33-2c3a7b6b75ca) — Video lecture covering the Ansible inventory file in YAML format, establishing SSH connectivity from the control machine to target EC2 instances, the `ping` module, host key checking configuration in `ansible.cfg`, private key permission requirements, and verifying the first successful Ansible connection. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Ansible Infrastructure Layout

The setup consists of a **control machine** (Ubuntu OS) and three **target machines** — `web01`, `web02`, and `db01` — all running CentOS 9. The control machine is where Ansible runs. The targets are the machines Ansible will manage. From this point forward in the course, the instructor uses the term "targets" to mean these EC2 instances. Ansible follows a **controller/worker** architecture where the control machine pushes configuration to targets — it does not require any agent software on the targets. The only requirement is SSH connectivity. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.2 How Ansible Connects — SSH as the Transport Layer

Ansible uses **SSH** to connect to its targets. When you manually SSH into an EC2 instance, you run `ssh -i <key-path> <username>@<ip-address>`. You provide three pieces of information: the private key, the username, and the IP address. Ansible needs **exactly the same information** — it just gets it from a different place: the **inventory file**. Instead of typing these details into a command every time, you write them into a structured file that Ansible reads automatically. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.3 The Inventory File — What It Is and Why It Exists

The inventory file is Ansible's **address book**. It tells Ansible: here are my targets, here is how to reach each one. Without an inventory file, Ansible doesn't know what machines exist, what their IP addresses are, what username to use, or what key to authenticate with. The inventory file solves the problem of centralizing all target connection information in one place. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

### Default vs Custom Inventory

Ansible has a **default inventory file** located at `/etc/ansible/hosts`. Many people use this default file, but the instructor explicitly recommends **against** it. The reason: if you use the default file, your inventory is tied to that specific control machine. If you set up a new control machine, or someone else needs to run the same Ansible code, the inventory information isn't there. Instead, the recommendation is to keep the inventory file **inside your repository** (your project directory). This way, when you clone the repository on any machine, the inventory comes with it. You tell Ansible where your custom inventory file is by using the `-i` flag followed by the file path. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

### Inventory File Naming

The inventory file name can be **anything**. There is no required naming convention. In this exercise, the file is simply named `inventory` (no extension). Since you always specify the path with `-i`, Ansible doesn't care about the filename. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

### Two Formats: INI and YAML

Inventory files can be written in two formats. **INI** is the older, simpler format. **YAML** is the newer format. The video uses YAML format. The instructor references the Ansible documentation page "How to build your inventory" which shows examples in both formats side by side. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.4 YAML Inventory File Structure

The YAML inventory file follows a specific hierarchy. At the top level, you have `all:` — this is a built-in group name meaning "all hosts." Inside `all`, you have `hosts:` — this is where individual target machines are defined. Inside `hosts`, each target gets a name (your choice — e.g., `web01`) followed by its connection variables. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The hierarchy uses **indentation** to express nesting. The video uses two-space indentation at each level:

```
all:                          ← level 0 (top)
  hosts:                      ← level 1 (2 spaces)
    web01:                    ← level 2 (4 spaces)
      ansible_host: <ip>      ← level 3 (6 spaces)
      ansible_user: ec2-user
      ansible_ssh_private_key_file: clientkey.pem
```

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

### Inventory Variables

Each target host can have **variables** that provide connection details. The key variables demonstrated are:

**`ansible_host`** — The IP address (or hostname) of the target machine. The video uses the **private IP**, not the public IP. This is because the control machine and targets are in the same VPC/network, and a security group rule has been created to allow this internal communication. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**`ansible_user`** — The SSH username for connecting to the target. For CentOS 9 AMIs from Amazon, this is `ec2-user`. This is equivalent to the username you specify in `ssh -i key user@ip`. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**`ansible_ssh_private_key_file`** — The path to the private key file used for SSH authentication. The video gives a relative filename (`clientkey.pem`), meaning the key file must exist in the **current working directory** from which you run the Ansible command. The instructor notes: you don't need to memorize these variable names — they are available in the documentation. But with frequent use, they become automatic. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**`ansible_port`** — Mentioned in the documentation walkthrough. If not specified, it defaults to **22** (the standard SSH port). The video does not set it explicitly because the default is correct. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**`ansible_password`** — The instructor explicitly warns: **never use passwords in inventory files.** Passwords would appear in clear text, which is dangerous. Always use the private key file approach instead. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

🔍 **Deep Dive**
The order of variables under a host doesn't matter — you can list `ansible_user` before `ansible_host` or vice versa. The instructor mentions this explicitly: "you can mention user first, host later, does not matter." However, putting `ansible_host` first is the conventional pattern because it's the most fundamental piece of information. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.5 The Private Key File — Copying and Naming

When the EC2 instances were launched, a key pair was downloaded to the local machine. This key needs to be on the **control machine** for Ansible to use it. The process is: display the key content on the local machine with `cat`, copy it, SSH into the control machine, and create a new file with the copied content. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The instructor makes two important points about this:

**Naming must match exactly.** The inventory file says `ansible_ssh_private_key_file: clientkey.pem`. The file you create on the control machine must have **exactly** this name. The instructor's original key was named `client-key.pem` (with a hyphen), but the inventory file uses `clientkey.pem` (no hyphen). The name in the inventory and the actual filename must be identical. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**Copy carefully.** On macOS, `cat` may display an extra `%` character at the end of the file content. Do **not** copy this character. The content must be copied precisely — from the `-----BEGIN` line to the `-----END` line, including exactly five hyphens on each side. No extra spaces, no extra characters. A corrupted key file will cause authentication failures. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.6 File Permissions on the Private Key

SSH (and by extension Ansible) enforces strict **file permissions** on private key files. The private key must have permissions set to `400` (read-only by the owner, no access for group or others). If the permissions are more open than this (like `664`, which is the default when you create a file with `vim`), SSH refuses to use the key with the error: *"Permissions 0664 for clientkey.pem are too open. Unprotected private key file."* [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The rationale is security: a private key that other users on the system can read is considered compromised. SSH rejects it as a protective measure. The fix is `chmod 400 clientkey.pem`. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The video deliberately demonstrates this error **before** fixing it, so you learn to recognize it. The Ansible output shows the failure in **red** — red is Ansible's default color for failures. The status shows `UNREACHABLE` with the message about unprotected private key file. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.7 The Host Key Checking Problem

When you SSH to a machine for the first time, SSH asks: *"The authenticity of this host can't be established. Are you sure you want to continue connecting? (yes/no)"*. This is **host key verification** — SSH is asking you to confirm that the target machine is who it claims to be, and to store its fingerprint for future verification. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

This interactive prompt is a problem for Ansible. Ansible is designed for **automation** — it should run without human interaction. If you're managing 50 machines, you don't want to type "yes" 50 times. If Ansible is running from a background process (a scheduled job, a CI/CD pipeline), there is no human to type "yes" at all. The execution would hang or fail. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The solution is to **disable host key checking** in the Ansible configuration. This tells Ansible: "Don't ask. Just accept the connection and store the fingerprint automatically." [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

⚠️ **Expert Note**
Disabling host key checking is standard practice in controlled environments (like an internal infrastructure where you trust all machines). In highly sensitive production environments, you might instead pre-populate the `known_hosts` file with the fingerprints of all target machines, allowing verification without interactive prompts. But for learning and most operational environments, disabling the check is the pragmatic approach. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.8 The Ansible Configuration File (`ansible.cfg`)

Ansible's behavior is controlled by a configuration file. The default location is `/etc/ansible/ansible.cfg`. This file controls settings like host key checking, default inventory location, connection timeouts, and many other operational parameters. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The default `ansible.cfg` file that ships with Ansible installation is essentially **empty** — it doesn't contain usable settings. To get a full configuration file with all available options (commented out), you must **generate** it using a specific command. This command creates a comprehensive file where every setting is listed but commented out (with semicolons or hashes). You then uncomment and modify only the settings you need. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

In this exercise, the only setting modified is `host_key_checking`. The line exists in the generated file but is **commented out** (preceded by a semicolon). A semicolon at the beginning of a line means it is a comment (same as `#`). To activate the setting, you remove the semicolon and change the value from `True` to `False`. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The instructor notes that a dedicated lecture on Ansible configuration will come later. For now, this single setting change is all that's needed to proceed. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.9 The Ping Module — What It Actually Does

The `ping` module is the first Ansible module demonstrated. It is critically important to understand: **Ansible's ping is NOT a network ping (ICMP)**. It does not send ICMP packets. Instead, it performs an SSH connection to the target machine, logs in, and returns a response. It validates that the entire SSH connectivity chain works — network reachability, authentication, username, key file, permissions — everything. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

If the ping succeeds, Ansible returns a response with `"ping": "pong"` and a status of `SUCCESS`. It also reports `"changed": false` — meaning it did not modify anything on the target machine. This is expected because the ping module only tests connectivity; it doesn't alter state. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The instructor mentions that Ansible has **tons of modules** — ping is just the first, simplest one. Every module produces a response. In later exercises, modules that install packages, copy files, or configure services will show different responses reflecting the changes they made. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## 1.10 Project Directory Structure

The video establishes a project organization pattern. A top-level directory (`vprofile`) acts as the repository root. Inside it, separate folders are created for each exercise (`exercise1`, `exercise2`, etc.). This allows you to preserve the code from each exercise for revision while building new exercises independently. The instructor says: "Assume this as the Git repository." [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are establishing the **first Ansible connection** from the control machine to target `web01`. This involves writing a YAML inventory file with web01's connection details, copying the SSH private key to the control machine, configuring Ansible to skip interactive host key prompts, fixing file permissions, and verifying connectivity using the `ping` module. The final outcome: running `ansible web01 -m ping -i inventory` returns `SUCCESS` with `"pong"`. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## Step 1: Create the Project Directory Structure

SSH into the control machine. Create the project hierarchy:

```bash
mkdir vprofile
cd vprofile
mkdir exercise1
cd exercise1
```

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

`vprofile` is the top-level project directory (treat it as the Git repository root). `exercise1` is specifically for the inventory file exercise. Future exercises will get their own folders.

***

## Step 2: Write the Inventory File

```bash
vim inventory
```

The filename `inventory` is arbitrary — you could name it anything. Enter insert mode (`i`) and write:

```yaml
all:
  hosts:
    web01:
      ansible_host: <web01-private-ip>
      ansible_user: ec2-user
      ansible_ssh_private_key_file: clientkey.pem
```

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**Line-by-line breakdown:**

| Line                                          | Indentation | Meaning                                                            |
| --------------------------------------------- | ----------- | ------------------------------------------------------------------ |
| `all:`                                        | 0 spaces    | Top-level group containing all hosts                               |
| `hosts:`                                      | 2 spaces    | Declares the hosts section within `all`                            |
| `web01:`                                      | 4 spaces    | A target machine named `web01` (your chosen name)                  |
| `ansible_host: <ip>`                          | 6 spaces    | The **private** IP address of the web01 EC2 instance               |
| `ansible_user: ec2-user`                      | 6 spaces    | SSH username — `ec2-user` for CentOS 9 AMIs                        |
| `ansible_ssh_private_key_file: clientkey.pem` | 6 spaces    | Path to the private key — relative to where you'll run the command |

**Where to find the private IP:** Go to the AWS EC2 console, find the web01 instance, and copy its **private IPv4 address** (not the public IP). [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

Save and quit: `Esc` → `:wq` → `Enter`.

**Common mistakes:**

* Using the public IP instead of the private IP.
* Inconsistent indentation (mixing tabs and spaces, or wrong number of spaces).
* Missing colons at the end of `all:`, `hosts:`, `web01:`.
* Mismatched key filename between the inventory and the actual file (covered in Step 3).

***

## Step 3: Copy the Private Key to the Control Machine

The SSH private key was downloaded to your **local machine** when the EC2 instances were launched. It needs to be on the control machine.

**3a. Exit the control machine:**

```bash
exit
```

**3b. Display the key content on your local machine:**

```bash
cat client-key.pem
```

(Use whatever name your key has locally.) [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**3c. Copy the output carefully:**

Select from `-----BEGIN RSA PRIVATE KEY-----` through `-----END RSA PRIVATE KEY-----` (including the five hyphens on each side). On macOS, if there's an extra `%` character at the end, do **not** copy it. No extra spaces, no extra characters. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**3d. SSH back into the control machine and navigate to the exercise directory:**

```bash
ssh -i <key-path> ubuntu@<control-machine-ip>
cd vprofile/exercise1
```

**3e. Create the key file with the exact name from the inventory:**

```bash
vim clientkey.pem
```

⚠️ The name must be **exactly** `clientkey.pem` — matching what you wrote in the inventory file. The instructor's local key was `client-key.pem` (with a hyphen) but the inventory says `clientkey.pem` (no hyphen). Use the name from the inventory. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

Enter insert mode (`i`), paste the key content, then save: `Esc` → `:wq` → `Enter`. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## Step 4: Attempt the First Ping (Expected to Fail — Host Key Prompt)

```bash
ansible web01 -m ping -i inventory
```

| Part           | Meaning                                                                |
| -------------- | ---------------------------------------------------------------------- |
| `ansible`      | The Ansible command-line tool                                          |
| `web01`        | The target host name — must match a name defined in the inventory file |
| `-m ping`      | Use the `ping` module (`-m` = module)                                  |
| `-i inventory` | Use this file as the inventory (`-i` = inventory path)                 |

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**What happens:** Ansible reads the inventory, finds web01's connection details, and attempts to SSH. SSH encounters a new host and asks: *"Are you sure you want to continue connecting? (yes/no)"*. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**Say `No`.** We are going to fix this properly rather than answering interactively.

**Error message:** `UNREACHABLE — failed to connect to the host via SSH: Host key verification failed.` [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**Connection to larger flow:** This failure demonstrates why Ansible configuration is needed — interactive prompts break automation.

***

## Step 5: Configure Ansible to Disable Host Key Checking

**5a. Examine the current config file:**

```bash
sudo cat /etc/ansible/ansible.cfg
```

This file is essentially empty. It needs to be regenerated. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**5b. Switch to root and navigate to the Ansible directory:**

```bash
sudo -i
cd /etc/ansible
ls
```

You should see the `ansible.cfg` file. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**5c. Backup the existing file:**

```bash
mv ansible.cfg ansible.cfg.backup
```

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**5d. Generate a full configuration file:**

The existing `ansible.cfg` contains a command inside it (as a comment) that generates the complete configuration. The instructor references this command. Run it:

```bash
ansible-config init --disabled > ansible.cfg
```

(The exact command is found inside the original config file.) This creates a new `ansible.cfg` with every possible setting listed but commented out. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**5e. Open the configuration file and find the host key setting:**

```bash
vim ansible.cfg
```

Search for the setting:

```
/host_key_checking
```

Press `Enter` to jump to the line. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**5f. Edit the setting:**

The line looks like: `;host_key_checking=True`

1. Enter insert mode (`i`).
2. **Remove the semicolon** at the beginning (semicolon = comment).
3. Change `True` to `False`.

Result: `host_key_checking=False`

Save and quit: `Esc` → `:wq` → `Enter`. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**5g. Return to the regular user:**

```bash
exit
```

This logs out of root and returns to the `ubuntu` user. Navigate back:

```bash
cd ~/vprofile/exercise1
```

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## Step 6: Attempt the Second Ping (Expected to Fail — Key Permissions)

```bash
ansible web01 -m ping -i inventory
```

**Error message (in red):** `UNREACHABLE — Permissions 0664 for 'clientkey.pem' are too open. It is required that your private key files are NOT accessible by others. This private key will be ignored. Unprotected private key file.` [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

The key file was created with `vim`, which gives default permissions of `664` (owner read/write, group read/write, others read). SSH requires `400` (owner read only). [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**Connection to larger flow:** This is the second of two common first-run failures. The video deliberately demonstrates both so you learn to recognize and fix them.

***

## Step 7: Fix the Key Permissions

```bash
chmod 400 clientkey.pem
```

| Part            | Meaning                                     |
| --------------- | ------------------------------------------- |
| `chmod`         | Change file permissions                     |
| `400`           | Owner: read-only. Group: none. Others: none |
| `clientkey.pem` | The private key file                        |

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

***

## Step 8: Run the Final Ping (Expected to Succeed)

```bash
ansible web01 -m ping -i inventory
```

**Expected output (in green):**

```
web01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

 [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**Reading the output:**

| Field              | Meaning                                                           |
| ------------------ | ----------------------------------------------------------------- |
| `web01`            | The target that was contacted                                     |
| `SUCCESS`          | The module executed successfully                                  |
| `"changed": false` | Nothing was modified on the target (ping only tests connectivity) |
| `"ping": "pong"`   | The module's response — the ping module returns "pong" on success |

**What happened internally:** Ansible read the inventory file, found web01's IP, username, and key path. It opened an SSH connection using those details (without prompting for host key verification, because we disabled that). It ran the ping module, which logged in and returned. No changes were made on the target. [\[233-invent...ing-module \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/233-inventory-and-ping-module.txt)

**Final state:** The first Ansible connection is established and verified. In the next lecture, the remaining targets (web02, db01) will be added to the inventory, and more inventory features will be explored.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture

```
[ Control Machine (Ubuntu) ]
         │
         │  SSH (port 22, private IP, private key)
         │
    ┌────┼────────────┐
    ▼    ▼            ▼
 web01  web02       db01        ← all CentOS 9, username: ec2-user
                                ← collectively called "targets"
```

***

## Inventory File Structure

```yaml
all:                                    # 0 spaces — top group
  hosts:                                # 2 spaces — hosts section
    web01:                              # 4 spaces — target name (your choice)
      ansible_host: <private-ip>        # 6 spaces — IP (use PRIVATE, not public)
      ansible_user: ec2-user            # 6 spaces — SSH username
      ansible_ssh_private_key_file: clientkey.pem  # 6 spaces — key path (relative to CWD)
```

File name: anything (specified via `-i`). Format: YAML. Default location: `/etc/ansible/hosts` (don't use it — keep in repo).

***

## Key Inventory Variables

```
ansible_host                   → IP address or hostname
ansible_user                   → SSH username
ansible_ssh_private_key_file   → path to private key
ansible_port                   → SSH port (default: 22, usually omitted)
ansible_password               → ⚠️ NEVER USE (clear text = dangerous)
```

***

## Ansible Ping Command

```
ansible web01 -m ping -i inventory
        │       │        │
        target   module   inventory file path

ping module ≠ network ICMP ping
ping module = SSH login test → returns "pong" on success
```

***

## Two-Failure Sequence (First Run)

```
Attempt 1: ansible web01 -m ping -i inventory
  FAIL → "Host key verification failed"
  Cause: SSH prompts yes/no for new host fingerprint (interactive = bad for automation)
  Fix:   ansible.cfg → host_key_checking = False

Attempt 2: ansible web01 -m ping -i inventory
  FAIL → "Permissions 0664 are too open"
  Cause: Private key file permissions too permissive
  Fix:   chmod 400 clientkey.pem

Attempt 3: ansible web01 -m ping -i inventory
  SUCCESS → "pong"
```

***

## Ansible Configuration Fix Sequence

```
1. sudo -i                                          (become root)
2. cd /etc/ansible
3. mv ansible.cfg ansible.cfg.backup                (backup original)
4. ansible-config init --disabled > ansible.cfg     (generate full config)
5. vim ansible.cfg
6. /host_key_checking                               (search)
7. Remove semicolon, change True → False
8. :wq
9. exit                                             (back to ubuntu user)
```

***

## Private Key Handling

```
Local machine: cat client-key.pem → copy content carefully
                                     ⚠️ No extra %, no extra spaces
                                     ⚠️ Include all 5 hyphens on BEGIN/END lines

Control machine: vim clientkey.pem → paste → :wq
                 chmod 400 clientkey.pem

⚠️ Filename must EXACTLY match inventory's ansible_ssh_private_key_file value
   Local name: client-key.pem (with hyphen)
   Inventory name: clientkey.pem (no hyphen) ← use THIS name for the file
```

***

## Project Directory Structure

```
~/vprofile/                    ← "Git repository" root
  └── exercise1/               ← this exercise
        ├── inventory          ← YAML inventory file
        └── clientkey.pem      ← private key (chmod 400)
```

***

## File System Locations

```
/etc/ansible/ansible.cfg       → global Ansible config (host_key_checking = False)
/etc/ansible/hosts             → default inventory (don't use — keep in repo instead)
~/vprofile/exercise1/inventory → custom inventory (specified with -i)
~/vprofile/exercise1/clientkey.pem → private key (permissions: 400)
```

***

## Ansible Output Color Coding

```
GREEN  = SUCCESS
RED    = FAILURE / UNREACHABLE

"changed": false  → nothing modified on target (expected for ping)
"ping": "pong"    → module response (every module returns a response)
```

***

## Key Engineering Patterns

| Pattern                              | Manifestation                                                                                                               |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **Inventory-as-code**                | Connection details live in a file inside the repo — portable, versionable, not tied to one machine                          |
| **Configuration-over-interaction**   | Disable host key checking to eliminate interactive prompts — automation must be non-interactive                             |
| **Deliberate failure demonstration** | Run the command knowing it will fail → recognize the error → apply the fix → understand the why                             |
| **Permission enforcement**           | SSH refuses keys with open permissions — security enforced at the OS level, not just by convention                          |
| **Validate-before-proceed**          | Use `ping` module to verify connectivity before attempting any real configuration — test the transport layer first          |
| **Separation of concerns**           | Inventory (what to connect to) is separate from configuration (how Ansible behaves) is separate from playbooks (what to do) |

***

## Conceptual Anchors

```
Inventory    = WHERE to connect (hosts, IPs, credentials)
ansible.cfg  = HOW Ansible behaves (settings, defaults)
Module       = WHAT to do on the target (ping, install, copy, etc.)
-i flag      = pointer to custom inventory
-m flag      = which module to execute
```

***

## Project Continuity

```
BEFORE: Ansible infrastructure set up (control + 3 targets as EC2 instances)
THIS:   First connection established — inventory for web01, ping succeeds
NEXT:   Add web02 + db01 to inventory, explore more inventory features
```

***

This completes the full reconstruction. **Theory** explains the inventory concept, host key checking, and the ping module's true nature. **Practical** walks through every command, every failure, and every fix in sequence. The **Compression Map** lets you mentally reload the entire setup — from YAML structure to the two-failure debugging pattern — in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀
