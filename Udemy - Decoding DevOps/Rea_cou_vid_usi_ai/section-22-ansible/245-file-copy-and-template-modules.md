# 🎓 Deep Learning Material: Ansible File Operations — Copy Module, Template Module & the Restart Problem

**Source:** [245-file-copy-and-template-modules.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt?EntityRepresentationId=d33492d8-0adc-4268-9ca3-ba21bf1824b3) — Video lecture covering Ansible file modules overview, the `copy` module with the `content` option, the `template` module with Jinja2 variable substitution in NTP configuration files, deploying OS-specific configuration files with `backup: yes`, using `group_vars/all` for shared variables, the `file` module for directory creation, and the critical problem of unconditional service restarts that leads into the next lecture on handlers. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 File Operations in DevOps — The Landscape

As a DevOps engineer, a huge portion of server provisioning involves **file operations**: pushing configuration files, modifying existing files, changing permissions, creating directories, archiving, syncing. Ansible provides a dedicated family of **file modules** for these tasks. The video walks through the documentation page listing all of them, and several are mentioned explicitly to build awareness of what's available:

* **`archive`** — Archive files (tar, zip, etc.)
* **`blockinfile`** — Add or remove blocks of content within a file.
* **`copy`** — Push a file from the control machine to the target.
* **`fetch`** — The opposite of copy — pull a file from the target to the control machine.
* **`file`** — Manage file and directory properties: change permissions, ownership, create directories, create empty files. This is explicitly distinguished from `copy` — the `file` module works on **existing files** or creates empty structures; it does not push content.
* **`find`** — Search for files matching criteria.
* **`lineinfile`** — Add, modify, or remove a single line in a file.
* **`replace`** — Replace content within a file using regex.
* **`synchronize`** — Uses `rsync` to sync content between directories (local-to-local or remote-to-local).
* **`template`** — Like copy, but processes Jinja2 templating before pushing. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The two modules this lecture focuses on are `copy` and `template`, with `file` used briefly for directory creation.

***

## 1.2 The Copy Module — Two Modes of Operation

The `copy` module pushes content to a target machine. It has two distinct modes based on which option you use:

**Mode 1: `src` (source file).** You have an actual file on the control machine, and you push it to a destination path on the target. This is the traditional "file transfer" use case. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Mode 2: `content` (inline content).** Instead of referencing a file, you write the content directly in the playbook task. No source file exists — the content is embedded in the YAML. The video demonstrates this by creating a Linux **banner file** (`/etc/motd`). The content is just two lines: "This server is managed by Ansible" and "No manual changes please." [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The decision logic between the two modes is practical: if your content is very simple (one or two lines), use `content` — it avoids managing an extra file. If the content is complex (a full configuration file), use `src` with an actual file. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The `/etc/motd` file is a standard Linux **Message of the Day** banner. Whatever text is in this file gets displayed to every user upon SSH login. Setting it to "managed by Ansible, no manual changes" is a real-world practice that communicates to anyone logging in that the server is under configuration management and should not be manually modified. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## 1.3 The Template Module — Why It Exists and How It Differs from Copy

The `template` module is the most important concept in this lecture. On the surface, it looks identical to `copy` — it has a `src` option, a `dest` option, and it pushes a file from the control machine to the target. But there is one **fundamental difference**: the template module is **intelligent**. Before pushing the file, it **reads** the source file and looks for **Jinja2 templating** — variables, conditions, loops. If it finds any, it **resolves** them: it looks up variable values, evaluates conditions, expands loops, and generates the **final content**. It then pushes this processed content — not the raw template — to the target. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The `copy` module, by contrast, is dumb. It takes the file exactly as it is and dumps it on the target. If your file contains `{{ ntp0 }}`, the copy module will literally write `{{ ntp0 }}` to the target file. The template module will replace `{{ ntp0 }}` with the actual value of the `ntp0` variable (e.g., `0.north-america.pool.ntp.org`). [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

### Why This Matters

Configuration files across different servers or operating systems often share **most** of their content but differ in a few values — like which NTP server to sync with, which port to listen on, or which domain to use. Without templates, you would need to maintain separate, complete configuration files for every variation. With templates, you maintain **one template file** with variables in place of the changing values, and a **single variable file** that defines those values. To change the NTP server for all machines, you change one variable in one place — every configuration file that uses that variable is automatically updated on the next playbook run. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

🔍 **Deep Dive**
The Jinja2 templating language is much more than just variables. The instructor mentions you can put **conditions** and **loops** inside templates — meaning you can design configuration files that dynamically include or exclude sections based on host facts or variables. However, this lecture only uses the variable substitution feature (`{{ variable_name }}`). The syntax for variables in templates is identical to the syntax used in playbooks: double curly braces `{{ }}`. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## 1.4 The Configuration File Workflow — Extract, Template, Deploy

The video demonstrates a specific workflow for managing configuration files that is a reusable pattern for any service provisioning:

**Step 1: Extract.** SSH into a target machine that has the service installed. Find the configuration file (e.g., `/etc/chrony.conf` on CentOS, `/etc/ntp.conf` on Ubuntu). `cat` the entire file, copy its contents. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Step 2: Store locally.** On the control machine, create a `templates/` directory inside the exercise folder. Create files with descriptive names (e.g., `ntpconf_centos`, `ntpconf_ubuntu`) and paste the configuration content into them. The file names are arbitrary — they're for human identification. What matters is the `dest` path in the playbook task, which determines the actual filename on the target. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Step 3: Templatize.** Replace the static values in the configuration files with Jinja2 variables. In this case, the four NTP server pool entries are replaced with `{{ ntp0 }}`, `{{ ntp1 }}`, `{{ ntp2 }}`, `{{ ntp3 }}`. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Step 4: Define variables.** In `group_vars/all`, define the actual NTP server values. These are looked up from the internet — the instructor Googles "NTP servers in Oregon" and picks four servers from a pool. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Step 5: Deploy.** The playbook uses the `template` module to push the files. The template module resolves the variables and delivers the final, complete configuration to the target. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The instructor notes the `templates/` folder name: "It's not mandatory to create with the name templates. But when we see in the roles, we will need this name." This foreshadows Ansible roles, which have a conventional directory structure where the `templates/` folder is expected by name. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## 1.5 The `backup: yes` Option

When deploying configuration files, the `template` module (and `copy` module) supports a `backup: yes` option. When enabled, Ansible creates a **backup copy** of the existing configuration file on the target before overwriting it. This is a safety net — if the new configuration causes problems, you can find the backup file on the target and restore it. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## 1.6 Variables in `group_vars/all`

The `group_vars/all` file is a variable definition file that applies to **all** hosts in the inventory. Any variable defined here is accessible in every playbook task and every template. In this exercise, four NTP server variables are defined:

```yaml
ntp0: "0.north-america.pool.ntp.org"
ntp1: "1.north-america.pool.ntp.org"
ntp2: "2.north-america.pool.ntp.org"
ntp3: "3.north-america.pool.ntp.org"
```

These values are sourced from the internet (NTP pool project). The instructor emphasizes: you can use any NTP server from any location. The values are just examples. The engineering point is: by centralizing these values in a variable file, changing all four NTP servers across all configuration files requires editing only this one file. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## 1.7 The `file` Module — Creating Directories

The `file` module manages files and file properties. The video uses it briefly to create a directory: `path: /opt/test21`, `state: directory`. When `state` is set to `directory`, Ansible creates the directory (and any parent directories) if it doesn't exist. The `file` module can also set permissions (`mode`) and change ownership. This task is added specifically to set up the demonstration of the **restart problem** (covered next). [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## 1.8 The Restart Problem — Why Handlers Are Needed

This is the most important conceptual takeaway of the entire lecture — and it's deliberately left **unsolved** to motivate the next lecture.

The playbook has tasks that: (1) deploy the NTP configuration file, and (2) restart the NTP/chrony service. The restart task runs **unconditionally** — every time the playbook executes, the service gets restarted, regardless of whether the configuration file actually changed. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The video demonstrates this in two stages:

**First demonstration:** After deploying the configuration files, the instructor runs the playbook again without making any changes. The template module detects no difference (configuration is already correct), but the restart task still executes — because it's a regular task with no condition linking it to whether the configuration changed. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Second demonstration:** The instructor adds a completely unrelated task (creating a directory with the `file` module). Running the playbook causes the directory to be created (the only actual change), but the service **also gets restarted** — even though the configuration file was untouched. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The instructor frames the problem clearly: "In a production environment, this can disrupt so many things which is really not a good thing. We need to restart the service only when we need to restart the service. Not unnecessarily." The solution — **handlers** — is the topic of the next lecture. Handlers are tasks that only execute when **notified** by another task that actually made a change. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

⚠️ **Expert Note**
Unnecessary service restarts in production can cause downtime, dropped connections, cache invalidation, and cascading failures in dependent services. This is not a theoretical concern — it is one of the most common mistakes in Ansible playbooks. The handler pattern exists specifically to solve this, and understanding *why* it exists (from this lecture's demonstration) makes the *how* (next lecture) immediately clear. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## 1.9 The Extra-Space Problem — Why Copy/Template Reports "Changed" Incorrectly

During the first deployment of the Ubuntu NTP configuration file, the template module reports `changed` even though the instructor didn't modify the content. Investigation reveals that an **extra space** was accidentally copied when extracting the configuration from the target machine. The template module compares the file it would push against the file that already exists on the target. Any difference — even a trailing space — is detected as a change, causing it to overwrite the file and report `changed`. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

This highlights the importance of **careful copying** when extracting configuration files, and also demonstrates Ansible's precise diff-based change detection — it's comparing files byte-for-byte, not just "close enough." [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are extending the NTP provisioning playbook to deploy NTP configuration files to CentOS and Ubuntu targets using the template module, with NTP server addresses defined as variables. We also deploy a banner file using the copy module's `content` option, create a directory with the `file` module, and observe the unconditional restart problem that motivates the next lecture on handlers. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## Step 1: Set Up the Exercise

```bash
cp -r exercise11 exercise12
cd exercise12
```

This preserves the existing playbook, inventory, keys, and `group_vars` from the previous exercise. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## Step 2: Add the Banner File Task (Copy Module with `content`)

Open the playbook:

```bash
vim provisioning.yaml
```

Go to the end of the tasks section and add:

```yaml
    - name: Banner file
      copy:
        content: |
          This server is managed by Ansible.
          No manual changes please.
        dest: /etc/motd
```

 [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

| Part              | Meaning                                                    |
| ----------------- | ---------------------------------------------------------- |
| `copy:`           | The copy module                                            |
| `content:`        | Inline content mode — no source file needed                |
| `dest: /etc/motd` | The Linux Message of the Day file — displayed on SSH login |

**Why `content` instead of `src`:** The content is only two lines. Managing a separate file for this would be unnecessary overhead. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

Save, quit, and run the playbook to verify:

```bash
ansible-playbook provisioning.yaml
```

**Verification:** SSH into any target. Upon login, you should see the banner message. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## Step 3: Extract Configuration Files from Targets

You need the NTP configuration file from one CentOS host and one Ubuntu host.

### 3a. CentOS configuration:

```bash
ssh -i clientkey.pem ec2-user@<db01-private-ip>
cat /etc/chrony.conf
```

Select and copy the **entire** file content. Note the `pool` lines — these are the NTP server entries you will templatize. Exit:

```bash
exit
```

 [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

### 3b. Ubuntu configuration:

```bash
ssh -i clientkey.pem ubuntu@<web03-private-ip>
sudo -i
cat /etc/ntp.conf
```

Select and copy the entire file content. Note the `pool` lines (similar structure, different values). Exit:

```bash
exit
exit
```

 [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

⚠️ Copy carefully — no extra spaces, no trailing characters. An extra space causes Ansible to detect a "change" even when no real modification was intended.

***

## Step 4: Create the Templates Directory and Files

Back on the control machine, inside the exercise12 directory:

```bash
mkdir templates
```

The folder name `templates` is not mandatory for now, but it **will be required** when using Ansible roles (future lecture). [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

### 4a. Create the CentOS template:

```bash
vim templates/ntpconf_centos
```

Paste the CentOS chrony configuration content. Save and quit. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

### 4b. Create the Ubuntu template:

```bash
vim templates/ntpconf_ubuntu
```

Paste the Ubuntu NTP configuration content. Save and quit. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

The filenames are for human identification only — the actual destination filename is controlled by the `dest` option in the playbook task.

***

## Step 5: Define NTP Server Variables

Open the group variables file:

```bash
vim group_vars/all
```

Add the NTP server variables (values sourced from the internet — search "NTP servers in \[your region]"):

```yaml
ntp0: "0.north-america.pool.ntp.org"
ntp1: "1.north-america.pool.ntp.org"
ntp2: "2.north-america.pool.ntp.org"
ntp3: "3.north-america.pool.ntp.org"
```

 [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

If the `group_vars/all` file doesn't exist, create it (along with the `group_vars` directory if needed). These variables are accessible by all hosts and all templates.

Save and quit.

***

## Step 6: Templatize the Configuration Files

### 6a. Edit the CentOS template:

```bash
vim templates/ntpconf_centos
```

Find the `pool` lines (there are four). Replace each static NTP server value with a Jinja2 variable:

```
pool {{ ntp0 }} iburst
pool {{ ntp1 }} iburst
pool {{ ntp2 }} iburst
pool {{ ntp3 }} iburst
```

Save and quit. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

### 6b. Edit the Ubuntu template:

```bash
vim templates/ntpconf_ubuntu
```

Same operation — replace the four static pool values with `{{ ntp0 }}` through `{{ ntp3 }}`.

Save and quit. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Connection to larger flow:** The configuration files now contain variables instead of hardcoded values. The `template` module will resolve these at deployment time. Changing the NTP servers in `group_vars/all` will automatically update both configuration files on the next run.

***

## Step 7: Add Template Deployment Tasks to the Playbook

Open the playbook:

```bash
vim provisioning.yaml
```

Add two tasks — one for CentOS, one for Ubuntu:

```yaml
    - name: Deploy NTP agent conf on CentOS
      template:
        src: templates/ntpconf_centos
        dest: /etc/chrony.conf
        backup: yes
      when: ansible_distribution == "CentOS"

    - name: Deploy NTP agent conf on Ubuntu
      template:
        src: templates/ntpconf_ubuntu
        dest: /etc/ntp.conf
        backup: yes
      when: ansible_distribution == "Ubuntu"
```

 [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

| Part          | Meaning                                                                          |
| ------------- | -------------------------------------------------------------------------------- |
| `template:`   | The template module — processes Jinja2 before pushing                            |
| `src:`        | Path to the template file on the control machine (relative to playbook location) |
| `dest:`       | Destination path on the target — this is the **actual** configuration file path  |
| `backup: yes` | Create a backup of the existing file before overwriting                          |
| `when:`       | OS-conditional execution (same pattern as previous lecture)                      |

**Destination paths matter:** CentOS uses `/etc/chrony.conf`, Ubuntu uses `/etc/ntp.conf`. These are the actual filenames the OS expects.

***

## Step 8: Add Service Restart Tasks

Copy the existing service start tasks and modify them for restart:

```yaml
    - name: Restart service on CentOS
      service:
        name: chronyd
        state: restarted
      when: ansible_distribution == "CentOS"

    - name: Restart service on Ubuntu
      service:
        name: ntp
        state: restarted
      when: ansible_distribution == "Ubuntu"
```

 [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

| Change from start tasks                        | Meaning                                 |
| ---------------------------------------------- | --------------------------------------- |
| `state: restarted` instead of `state: started` | Forces a service restart (stop + start) |

Save and quit.

***

## Step 9: Execute and Verify

```bash
ansible-playbook provisioning.yaml
```

**Expected output:** Configuration files deployed (`changed`), services restarted (`changed`). [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**Verification:** SSH into a target and check the configuration file content — the Jinja2 variables should be resolved to actual NTP server addresses. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

## Step 10: Observe the Restart Problem

### 10a. Add an unrelated task:

Open the playbook and add a directory creation task:

```yaml
    - name: Create a folder
      file:
        path: /opt/test21
        state: directory
```

 [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

| Part               | Meaning                                     |
| ------------------ | ------------------------------------------- |
| `file:`            | File module — manages files and directories |
| `path:`            | The directory path to create                |
| `state: directory` | Ensure this path exists as a directory      |

### 10b. Execute:

```bash
ansible-playbook provisioning.yaml
```

**Observe the output:** The directory is created (`changed`). But the service is **also restarted** (`changed`) — even though the configuration file was not modified (the template task shows `ok`, not `changed`). [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

**This is the problem:** The restart task is unconditional — it runs every time the playbook executes, regardless of whether a restart is actually needed. The solution is **handlers** (next lecture), which only execute when explicitly notified by a task that made a change. [\[245-file-c...te-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/245-file-copy-and-template-modules.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## File Module Landscape

```
copy        → push file from control → target (dumb transfer)
template    → push file from control → target (resolves Jinja2 first)
file        → manage EXISTING files/dirs (permissions, create dir, create empty file)
fetch       → pull file from target → control (reverse of copy)
blockinfile → add/remove blocks within a file
lineinfile  → add/modify/remove single line
replace     → regex-based content replacement
synchronize → rsync between directories
archive     → compress files
```

***

## Copy vs Template — The Core Distinction

```
copy module:
  src file → [as-is] → target dest
  {{ ntp0 }} on target file = literally "{{ ntp0 }}"

template module:
  src file → [Jinja2 processing] → target dest
  {{ ntp0 }} → resolved to "0.north-america.pool.ntp.org"

USE template WHEN: configuration files contain ANY variables/conditions/loops
USE copy WHEN: file is static OR content is inline (content: option)
```

***

## Copy Module — Two Modes

```
Mode 1: src: /path/to/file       → push existing file
Mode 2: content: "inline text"   → push inline content (no file needed)

Rule: simple content (1-2 lines) → content option
      complex content            → src option (or use template)
```

***

## Configuration File Workflow

```
1. SSH into target → cat /etc/<service>.conf → copy content
2. Control machine → mkdir templates/ → paste into templates/filename
3. Replace static values with {{ variables }}
4. Define variables in group_vars/all
5. Playbook: template module → src: templates/file, dest: /etc/<service>.conf
6. Template module resolves variables → pushes final config → backup: yes
```

***

## Variable Flow

```
group_vars/all                    templates/ntpconf_centos
  ntp0: "0.north-america..."  →    pool {{ ntp0 }} iburst
  ntp1: "1.north-america..."  →    pool {{ ntp1 }} iburst
  ntp2: "2.north-america..."  →    pool {{ ntp2 }} iburst
  ntp3: "3.north-america..."  →    pool {{ ntp3 }} iburst

template module reads template → resolves variables → pushes resolved file

Change NTP servers = edit ONE file (group_vars/all) → ALL configs updated
```

***

## OS-Specific Config Mapping

```
              CentOS                    Ubuntu
Config path   /etc/chrony.conf          /etc/ntp.conf
Template      templates/ntpconf_centos  templates/ntpconf_ubuntu
Service       chronyd                   ntp
Condition     ansible_distribution ==   ansible_distribution ==
              "CentOS"                  "Ubuntu"
```

***

## The Restart Problem (Critical — Motivates Handlers)

```
Current playbook:
  Task: Deploy config  → runs → changed OR ok
  Task: Restart service → runs → ALWAYS restarts (unconditional)

Problem:
  Config unchanged + unrelated task added
    → restart still executes
    → unnecessary service disruption

  Run 1: deploy config (changed) + restart (changed) ← correct
  Run 2: no config change (ok) + restart (changed)   ← WRONG
  Run 3: add folder (changed) + restart (changed)    ← WRONG

Solution (next lecture): HANDLERS
  → restart only when NOTIFIED by config task
  → config changed → notify handler → restart
  → config unchanged → no notification → no restart
```

***

## Directory Structure

```
exercise12/
├── provisioning.yaml          ← playbook
├── inventory                  ← host definitions
├── clientkey.pem              ← SSH key (chmod 400)
├── group_vars/
│   └── all                    ← variables (ntp0-ntp3)
└── templates/
    ├── ntpconf_centos         ← chrony.conf template with {{ vars }}
    └── ntpconf_ubuntu         ← ntp.conf template with {{ vars }}
```

`templates/` name: optional now, **required** in Ansible roles.

***

## Banner File Pattern (Quick Reference)

```yaml
- name: Banner file
  copy:
    content: "This server is managed by Ansible.\nNo manual changes please."
    dest: /etc/motd

/etc/motd = Linux Message of the Day → displayed on every SSH login
```

***

## File Module (Directory Creation)

```yaml
- name: Create a folder
  file:
    path: /opt/test21
    state: directory

state: directory → create dir if not exists
Also supports: mode (permissions), owner, group
```

***

## Change Detection Behavior

```
Template module compares: rendered template vs existing file on target
  ANY difference (even trailing space) → changed → overwrites
  Identical → ok → no action

⚠️ Extra spaces copied during extraction → false "changed" status
```

***

## Key Engineering Patterns

| Pattern                                | Manifestation                                                                       |
| -------------------------------------- | ----------------------------------------------------------------------------------- |
| **Template-driven configuration**      | Variables in templates + central variable file = one change point for all configs   |
| **Extract → Templatize → Deploy**      | Get real config → replace dynamic values with variables → push via template module  |
| **Content vs Source decision**         | Simple inline content = `content:` option; complex files = `src:` with file         |
| **Backup before overwrite**            | `backup: yes` creates safety net on target before replacing config                  |
| **Unconditional restart anti-pattern** | Regular tasks always execute → service restarts unnecessarily → handlers solve this |
| **Convention-ready naming**            | `templates/` folder prepares for Ansible roles convention even before using roles   |

***

## Series Continuity

```
PREVIOUS: Decision making (when conditions for multi-OS)
THIS:     File operations — copy (content), template (Jinja2 variables), file (directories)
          + identified the RESTART PROBLEM
NEXT:     Handlers — conditional restart only when configuration actually changes
LATER:    Ansible Roles (templates/ folder becomes mandatory)
```

***

This completes the full reconstruction. **Theory** explains why template exists over copy, how the variable resolution chain works, and what the restart problem is. **Practical** gives you every file, every command, and every extraction step. The **Compression Map** lets you rapidly reload the copy-vs-template distinction, the config workflow, and the restart anti-pattern in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀
