# Ansible Configuration — Settings, Priority Levels, and Local Config Files

**Source:** Video caption file — *"Ansible Configuration"* (from an Ansible / DevOps course) [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Why Ansible Configuration Exists

Ansible works out of the box with default settings — the previous lectures proved this. The inventory was created, hosts were added, modules were executed, playbooks were run, and no configuration changes were needed (except one: `host_key_checking = false`). Ansible has a **default nature** — a set of built-in behaviors that it follows unless you tell it otherwise. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The question is: what happens when the defaults don't match your environment? The video uses a concrete example: Ansible connects to Linux machines via SSH on **port 22** — that's the default SSH port, and Ansible uses it by default. But in many environments, especially for security reasons, the SSH port is changed from 22 to something else, like 2020. If your servers use port 2020 for SSH and you haven't told Ansible, it will try port 22, fail, and you'll have a connectivity problem that has nothing to do with your playbooks or inventory — it's a **configuration mismatch**. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

This is the purpose of Ansible configuration: **when you want to change Ansible's default behavior, you change the configuration**. Configuration controls how Ansible operates — which port to use for SSH, how many machines to automate simultaneously, where to store logs, whether to ask for passwords, whether to escalate privileges, and hundreds of other behavioral settings. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## 1.2 — The Four Configuration Levels and Their Priority Order

Ansible configuration can be defined at **four different levels**, and each level has a specific **priority**. When Ansible starts, it looks for configuration files in a specific order and uses the first one it finds. If a setting exists at multiple levels, the higher-priority level wins. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The priority order, from **highest to lowest**: [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### Priority 1 (Highest): `ANSIBLE_CONFIG` Environment Variable

If you set the `ANSIBLE_CONFIG` environment variable (using `export ANSIBLE_CONFIG=/path/to/custom/ansible.cfg`), Ansible uses the configuration file at that path. This overrides everything else. This is a **system-level** setting — it's set in the shell environment, not in a file within your project.

### Priority 2: `ansible.cfg` in the Current Working Directory

If the environment variable is not set, Ansible looks for a file named `ansible.cfg` in the **current directory** — the directory from which you're running the `ansible` or `ansible-playbook` command. This is **repository-specific** — it lives alongside your playbooks and inventory in your project folder.

### Priority 3: `~/.ansible.cfg` (Hidden File in Home Directory)

If no config is found in the current directory, Ansible looks for a hidden file `.ansible.cfg` in your **home directory** (`~/`). This is a **system-level, user-specific** setting.

### Priority 4 (Lowest): `/etc/ansible/ansible.cfg` (Global Config)

If none of the above exist, Ansible falls back to the **global configuration file** at `/etc/ansible/ansible.cfg`. This is a **system-level** setting that applies to all users and all projects on the machine.

The critical insight from the video: **"Mostly we use ansible.cfg file in the current directory."** The reasoning is directly tied to DevOps workflow: as a DevOps engineer, you write Ansible playbooks and commit them to a version control repository. That repository is shared with the entire team. **Everyone should have the same settings.** If you rely on global config (`/etc/ansible/ansible.cfg`) or home directory config (`~/.ansible.cfg`), each team member's machine may have different settings, leading to inconsistent behavior. If you commit `ansible.cfg` alongside your playbooks in the repository, everyone who clones the repo gets the same configuration automatically. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The video explicitly states: "Always, always, always you should have an Ansible configuration file in the repository where you have your playbook." This is presented as a non-negotiable best practice. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

🔍 **Deep Dive:**
The four levels create a **specificity hierarchy** — the same pattern seen in Ansible inventory variables (host > group) and in CSS (inline > class > global). The most specific context wins. The environment variable is the most specific because it's an explicit, intentional override. The current directory config is specific to the project. The home directory config is specific to the user. The global config is the least specific — it's a system-wide default. This specificity hierarchy is a recurring engineering pattern: **defaults at the bottom, overrides at the top, most-specific wins.** [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## 1.3 — The Structure of `ansible.cfg`: Sections and Settings

The Ansible configuration file uses **INI format** — settings organized into sections denoted by square brackets (`[section_name]`), with individual settings as `key = value` pairs within each section. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**Comments** are denoted by `#` (hash) or `;` (semicolon). [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The global config file (`/etc/ansible/ansible.cfg`) is large — the video notes it's **more than a thousand lines**. It contains many sections, including: [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

* **`[defaults]`** — the most commonly used section, containing the maximum number of settings. This is where most configuration changes are made.
* **`[privilege_escalation]`** — settings for how Ansible escalates privileges (sudo/become) on target machines.
* **`[ssh_connection]`** — SSH-specific settings (port, timeouts, etc.).
* **`[inventory]`** — inventory-related settings.
* Other sections: `[powershell]`, `[winrm]`, `[sudo_become_plugin]`, `[su_become_plugin]`, and many more for specialized use cases. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The video's advice: **"Don't waste time going through all of them."** The file is a reference, not a textbook. You use it when you need to change a specific behavior — "whenever you require to change something in Ansible, you want Ansible to do something like this instead of that, then check the configuration settings and make the changes." [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

Documentation is available at `docs.ansible.com` — you can search "Ansible configuration file" and find every setting with its description and usage. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## 1.4 — Key Configuration Settings Explained

The video walks through several important settings from the `[defaults]` section, each representing a different aspect of Ansible's behavior. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### `host_key_checking`

Controls whether Ansible verifies the SSH host key when connecting to a target machine for the first time. Default is `true` (Ansible checks and prompts for confirmation). Set to `false` to skip this check — essential in automated environments where you don't want interactive prompts blocking execution. This setting was already used in earlier lectures at the global level. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### `inventory`

Specifies the **default inventory file path**. Without this setting, you must pass `-i inventory` on every `ansible` or `ansible-playbook` command. By setting `inventory = ./inventory` in the config file, Ansible automatically uses the `inventory` file in the current directory. This eliminates the repetitive `-i` flag from every command. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The video demonstrates this directly: after setting the inventory path in the local `ansible.cfg`, the playbook command drops the `-i inventory` flag entirely — "I'm just going to give the name of the playbook, that's all. I'm not going to say `-i inventory` because it's already there in the Ansible configuration file." [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### `forks`

Controls **how many target machines Ansible connects to simultaneously** during execution. Default is 5. If you have a group of 20 hosts, Ansible will connect to 5 at a time, execute the task, then move to the next 5, and so on. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The video makes a crucial clarification: **"This is not the limitation of Ansible, this is limitation of the control machine where your Ansible is running."** The fork count is limited by the CPU, RAM, and network bandwidth of the machine running Ansible. If you have a powerful control machine with plenty of resources, you can increase forks to automate more machines simultaneously. If your control machine is small, you keep forks low to avoid overloading it. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### `log_path`

By default, **Ansible does not store any log of execution**. Output goes to the terminal and disappears. If you set `log_path = /var/log/ansible.log`, Ansible writes all execution output to that file. This is essential for auditing, debugging, and operational record-keeping. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

There's an operational catch: the log file path must be **writable** by the user running Ansible. If you specify `/var/log/ansible.log` and the Ansible user (e.g., `ubuntu`) doesn't have write permission to `/var/log/`, Ansible produces a warning: "is not writeable." You must create the file and set correct ownership before Ansible can write to it. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### `force_colors`

Controls whether Ansible output includes colors. Default is enabled. "Who doesn't like colors?" — but in some environments (CI/CD pipelines, log aggregation systems), colors produce unreadable escape characters, and you may want to disable them. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### `ask_pass`

Controls whether Ansible prompts for a password to log into target machines. Default is `false` — Ansible expects to use SSH keys or pre-configured passwords. If set to `true`, Ansible will interactively ask for the SSH password. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

### `debug`

Controls whether Ansible outputs debug information during playbook execution. Default is `false`. Enable for deeper troubleshooting. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## 1.5 — The `[privilege_escalation]` Section

This section controls how Ansible escalates privileges on target machines — the equivalent of using `sudo` when you need root access to install packages, manage services, or modify system files. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

In previous lectures, `become: yes` was specified **inside each playbook**. If you have multiple playbooks and all of them need privilege escalation, repeating `become: yes` in every playbook is redundant. By setting it in the configuration file, it becomes a **global setting** that applies to all playbooks executed from the current directory. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

The settings:

* **`become = true`** — enables privilege escalation for all playbook executions. Equivalent to `become: yes` in every playbook.
* **`become_method = sudo`** — specifies the escalation method. `sudo` is the standard for Linux. Other methods exist (like `su`, `pbrun`, etc.) for different systems.
* **`become_ask_pass = false`** — specifies whether Ansible should ask for the sudo password. In the video's environment, `ec2-user` can run `sudo` without a password prompt, so this is set to `false`. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

⚠️ **Expert Note:**
Moving `become` from playbooks to configuration is a design decision. It simplifies playbooks but makes the privilege escalation implicit — someone reading the playbook doesn't see `become: yes` and may not realize tasks run with elevated privileges. In teams, the convention should be documented. Some teams prefer explicit `become` in playbooks for clarity; others prefer the config file for DRY (Don't Repeat Yourself) compliance. Both are valid — the key is consistency across the team. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## 1.6 — Verbosity Levels for Debugging

The video briefly mentions the `-vv` flag when running playbooks: "If we mention `-vv`, two levels of verbosity, then we should have more logs." Ansible supports multiple verbosity levels (`-v`, `-vv`, `-vvv`, `-vvvv`), each providing progressively more detailed output. This is useful for debugging connectivity issues, module failures, or understanding exactly what Ansible is doing internally. When combined with `log_path`, the verbose output is captured in the log file for later analysis. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a **local `ansible.cfg` file** in the project directory that replaces reliance on the global configuration. The final outcome: Ansible commands no longer need the `-i inventory` flag, logging is enabled, privilege escalation is configured globally, and the configuration travels with the repository so every team member uses the same settings. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Execution Flow Overview

```
Step 1: Examine the global ansible.cfg (understand what's there)
Step 2: Create a local ansible.cfg in the project directory
Step 3: Configure key settings ([defaults] + [privilege_escalation])
Step 4: Fix the log file permissions
Step 5: Test — run playbook without -i flag
Step 6: Verify logging works
```

***

### Step 1: Examine the Global Configuration File

**What we are doing:** Reading the global `ansible.cfg` to understand the available settings before creating our own local version.

```bash
sudo -i
vim /etc/ansible/ansible.cfg
```

**Breakdown:**

* `sudo -i` — switches to the root user (the global config is in `/etc/`, which requires elevated access to read comfortably).
* `vim /etc/ansible/ansible.cfg` — opens the global config file. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**What you see:** A file with 1000+ lines organized into sections (`[defaults]`, `[privilege_escalation]`, `[ssh_connection]`, etc.). Most lines are commented out (prefixed with `#` or `;`), showing default values.

**How to navigate:**

* `:set nu` — shows line numbers in vim.
* `gg` — go to top of file.
* `G` — go to bottom of file.
* `/setting_name` — search for a specific setting. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**Purpose of this step:** Orientation only. We will NOT modify this file. We're reading it to understand what settings are available, then creating our own local version with only the settings we need.

***

### Step 2: Create Local `ansible.cfg` in the Project Directory

**What we are doing:** Creating a project-specific configuration file that overrides the global config.

**Where to create it:** In the exercise directory (the video uses exercise 7). The file must be named exactly `ansible.cfg` — no leading dot, no extension change. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

```bash
vim ansible.cfg
```

**Why here:** This is the current working directory where `ansible-playbook` commands will be executed. Ansible automatically detects `ansible.cfg` in the current directory (Priority 2 — higher than the global config).

***

### Step 3: Configure Settings

**What we are doing:** Writing the configuration with two sections: `[defaults]` and `[privilege_escalation]`.

**Complete file content:**

```ini
[defaults]
host_key_checking = false
inventory = ./inventory
forks = 5
log_path = /var/log/ansible.log

[privilege_escalation]
become = true
become_method = sudo
become_ask_pass = false
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**Line-by-line breakdown:**

**`[defaults]`** — Section header. Contains the most commonly used settings.

**`host_key_checking = false`** — Disables SSH host key verification prompts. Previously set in the global config; now moved to the local file so it's repository-specific and portable. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**`inventory = ./inventory`** — Sets the default inventory file path to `./inventory` (a file named `inventory` in the current directory). After this, you never need to pass `-i inventory` on the command line again. The video clarifies potential confusion: "My inventory file name is `inventory`. Don't get confused. This is the path of my file, this is the setting name." [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**`forks = 5`** — Sets the parallelism level to 5 machines simultaneously. The video notes: "It really doesn't matter. I just have three hosts at the max. It can anyways go with three machines at a time. You can mention the settings just to learn." In production with many hosts, this becomes operationally significant. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**`log_path = /var/log/ansible.log`** — Enables execution logging. All Ansible output will be written to this file. Default behavior (no logging) is overridden. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**`[privilege_escalation]`** — Section header for sudo/become settings.

**`become = true`** — Enables privilege escalation globally. Every playbook executed from this directory will use `sudo` on target machines. Replaces `become: yes` inside individual playbooks. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**`become_method = sudo`** — Specifies `sudo` as the escalation method. "Anyways become means sudo in Linux." [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**`become_ask_pass = false`** — Don't prompt for the sudo password. The EC2 user can sudo without a password, so this is appropriate for this environment. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**Save and exit:** `:wq` in vim. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

### Step 4: Fix Log File Permissions

**What we are doing:** Creating the log file and setting correct ownership so the Ansible user can write to it.

**The problem:** If you run the playbook now, you'll get a warning: `/var/log/ansible.log is not writeable.` The `/var/log/` directory is owned by root, and the `ubuntu` user (who runs Ansible) cannot create files there. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**Fix:**

```bash
sudo touch /var/log/ansible.log
```

**Breakdown:**

* `sudo` — run as root (needed to create files in `/var/log/`).
* `touch` — creates an empty file (or updates timestamp if it exists).
* `/var/log/ansible.log` — the path specified in the config. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

```bash
sudo chown ubuntu:ubuntu /var/log/ansible.log
```

**Breakdown:**

* `chown` — change ownership.
* `ubuntu:ubuntu` — set both owner and group to `ubuntu` (the user running Ansible).
* `/var/log/ansible.log` — the file to change ownership of. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**How to verify:** After these commands, `ls -la /var/log/ansible.log` should show `ubuntu ubuntu` as owner and group.

**Common mistake:** Skipping this step and getting the "not writeable" warning on every Ansible run. The warning doesn't stop execution, but logs won't be recorded.

***

### Step 5: Test — Run Playbook Without `-i` Flag

**What we are doing:** Verifying that the local `ansible.cfg` is working by running a playbook without specifying the inventory path.

```bash
ansible-playbook playbook_name.yml
```

**What's different:** No `-i inventory` flag. Previously, every command required `-i inventory` to specify the inventory file. Now, the `inventory = ./inventory` setting in `ansible.cfg` provides this automatically. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**Expected output:** The playbook executes successfully, targeting all hosts defined in the `./inventory` file. No warnings about unwritable log files (after Step 4 fix).

**How to verify the config is being used:** The absence of the `-i` flag and successful execution proves Ansible found and used the local `ansible.cfg`. If the config wasn't found, Ansible would error about missing inventory.

***

### Step 6: Verify Logging

**What we are doing:** Confirming that Ansible is writing execution logs to the configured path.

```bash
cat /var/log/ansible.log
```

**Expected output:** The full output of the playbook execution — task names, host results, success/failure status — recorded in the log file. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**With increased verbosity:**

```bash
ansible-playbook playbook_name.yml -vv
```

**Breakdown:**

* `-vv` — two levels of verbosity. Produces significantly more detailed output.

**Verify:**

```bash
cat /var/log/ansible.log
```

**Expected output:** Much more detailed logs compared to the previous run — including connection details, module arguments, and internal processing information. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

**Connection to flow:** With the local `ansible.cfg` in place, all future Ansible work in this project directory uses these settings automatically. The configuration file should be committed to version control alongside the playbooks and inventory, ensuring the entire team operates with identical settings.

⚠️ **Expert Note:**
In CI/CD pipelines, the `ansible.cfg` in the repository is critical — the pipeline runner clones the repo, enters the directory, and Ansible automatically picks up the local config. Without it, you'd need to configure Ansible on every CI/CD runner individually, which is fragile and inconsistent. The local config pattern makes Ansible pipelines portable and reproducible. [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Ansible Configuration
PURPOSE:  Change Ansible's default behavior (SSH port, parallelism, logging, sudo, etc.)
FORMAT:   INI file — [section] + key = value
CORE RULE: "When you want to change defaults, you change Ansible configuration"
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Four Configuration Levels (Priority Order)

```
PRIORITY   LOCATION                              SCOPE          USE CASE
────────   ────────                              ─────          ────────
1 (HIGH)   ANSIBLE_CONFIG env variable            System-level   Explicit override
2          ./ansible.cfg (current directory)      Repo-level     ✅ RECOMMENDED
3          ~/.ansible.cfg (home dir, hidden)      User-level     Personal defaults
4 (LOW)    /etc/ansible/ansible.cfg (global)      System-level   Machine-wide defaults

RULE: Higher priority wins when same setting exists at multiple levels
BEST PRACTICE: "Always, always, always use ansible.cfg in the repository"

WHY REPO-LEVEL?
  ├── Committed to version control
  ├── Shared by entire team
  ├── Everyone gets same settings
  └── Portable across machines/CI/CD
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Configuration File Structure

```ini
[defaults]                          ← most commonly used section
host_key_checking = false           ← skip SSH host key prompt
inventory = ./inventory             ← default inventory path (no more -i flag)
forks = 5                           ← parallel connections (limited by control machine)
log_path = /var/log/ansible.log     ← enable execution logging (off by default!)

[privilege_escalation]              ← sudo/become settings
become = true                       ← enable sudo globally (replaces become: yes in playbooks)
become_method = sudo                ← escalation method
become_ask_pass = false             ← don't prompt for sudo password

# Other sections exist: [ssh_connection], [inventory], [powershell], [winrm], etc.
# File can be 1000+ lines at global level — only set what you need locally
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Key Settings Quick Reference

```
SETTING              DEFAULT        WHAT IT CONTROLS
───────────          ───────        ────────────────
host_key_checking    true           SSH host key verification prompt
inventory            /etc/ansible/  Default inventory file path
forks                5              Max parallel target connections
log_path             (none)         Execution log file (OFF by default)
ask_pass             false          Prompt for SSH password
debug                false          Debug output during execution
force_colors         true           Colored terminal output
become               false          Privilege escalation (sudo)
become_method        sudo           How to escalate
become_ask_pass      false          Prompt for sudo password
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Forks: Parallelism Model

```
GROUP: webservers (20 hosts)
forks = 5

EXECUTION:
  Batch 1: host1, host2, host3, host4, host5    (simultaneous)
  Batch 2: host6, host7, host8, host9, host10   (simultaneous)
  Batch 3: ...
  Batch 4: ...

BOTTLENECK: Control machine (CPU, RAM, bandwidth) — NOT Ansible itself
MORE RESOURCES → can increase forks → faster automation
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Log File Setup (Operational)

```
PROBLEM:
  log_path = /var/log/ansible.log
  /var/log/ owned by root → ubuntu user can't write → WARNING

FIX:
  sudo touch /var/log/ansible.log
  sudo chown ubuntu:ubuntu /var/log/ansible.log

VERBOSITY:
  (default)  → standard output logged
  -v         → verbose
  -vv        → more verbose
  -vvv       → connection debugging
  -vvvv      → maximum detail
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Privilege Escalation: Playbook vs. Config

```
BEFORE (in every playbook):
  - hosts: all
    become: yes           ← repeated in EVERY playbook
    tasks: ...

AFTER (in ansible.cfg):
  [privilege_escalation]
  become = true           ← defined ONCE, applies to ALL playbooks

SAME PATTERN AS:
  inventory -i flag → inventory setting in config
  become: yes → become = true in config
  
PRINCIPLE: Move repetitive per-command/per-playbook settings into config
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Command Simplification Chain

```
BEFORE ansible.cfg:
  ansible-playbook -i inventory playbook.yml

AFTER ansible.cfg (with inventory setting):
  ansible-playbook playbook.yml

ELIMINATED:
  -i inventory  → inventory = ./inventory in config
  become: yes   → become = true in config
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Priority Pattern (Recurring Across Ansible)

```
ANSIBLE INVENTORY VARIABLES:    host-level > group-level
ANSIBLE CONFIGURATION:          env var > current dir > home dir > global
GENERAL PATTERN:                most-specific > least-specific

SAME PRINCIPLE:
  Specific overrides general
  Local overrides global
  Explicit overrides default
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## When to Change Configuration

```
DON'T: Go through all 1000+ settings preemptively
DO:    Change settings only when you need different behavior

TRIGGER: "I want Ansible to do X instead of Y"
  → Check docs.ansible.com for the setting
  → Add to local ansible.cfg
  → Commit to repository
```

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## Reusable Engineering Patterns

| Pattern                                | Manifestation                                                                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Specificity Hierarchy**              | 4 config levels: env var > current dir > home > global — most specific wins              |
| **Convention Over Configuration**      | Ansible works with defaults; only configure what you need to change                      |
| **Config-as-Code in Repository**       | `ansible.cfg` committed alongside playbooks = portable, shared, versioned settings       |
| **DRY via Config Promotion**           | Move repetitive flags/settings (`-i`, `become: yes`) from commands/playbooks into config |
| **Control Plane Resource Awareness**   | Forks limited by control machine resources, not by Ansible itself                        |
| **Opt-In Logging**                     | Logging disabled by default — must be explicitly enabled (log\_path)                     |
| **Permission-Aware File Creation**     | Log file needs correct ownership before non-root user can write                          |
| **Documentation-Driven Configuration** | Don't memorize settings — look them up when needed (docs.ansible.com)                    |

 [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

## One-Line System Reconstruction

> **Ansible configuration uses a four-level INI-format priority hierarchy (env var > current dir `ansible.cfg` > home dir > global `/etc/ansible/ansible.cfg`) where the local repo-level config is the recommended practice, containing `[defaults]` settings (host\_key\_checking, inventory path, forks for parallelism, log\_path) and `[privilege_escalation]` settings (become/sudo) — eliminating repetitive command-line flags and playbook directives while ensuring the entire team shares identical settings through version control.** [\[239-ansibl...figuration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/239-ansible-configuration.txt)

***

This completes the full reconstruction of the Ansible Configuration lecture. It builds on the inventory and playbook knowledge from previous lectures by introducing the configuration layer that controls Ansible's operational behavior — how it connects, how many machines it handles simultaneously, where it logs, and how it escalates privileges. The next lectures will continue with more advanced modules and playbook patterns. Let me know if you'd like any section expanded or adjusted! 🚀
