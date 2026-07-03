# 🎓 Deep Learning Material: Ansible Roles — Modular Playbook Architecture

**Source:** [247-roles.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt?EntityRepresentationId=d5fc6488-c5f7-4d9f-8074-1f418bedd279) — Video lecture covering the conceptual reasoning behind Ansible roles, converting an existing multi-component playbook into a role directory structure using `ansible-galaxy init`, distributing tasks/handlers/variables/files/templates into their dedicated directories, the `vars` vs `defaults` priority system, overriding variables from the playbook, downloading and studying community roles from Ansible Galaxy, and the `include_tasks` pattern for OS-specific task files. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: Playbook Complexity at Scale

By this point in the course, the provisioning playbook has accumulated significant content: global declarations (`become`), variables defined inside the playbook and externally in `group_vars` and `host_vars`, numerous tasks (package installation, service management, directory creation, file copying), templates with Jinja2 logic, handlers for service restarts, and a `files` directory for static files pushed via the `copy` module. The directory structure has grown to include `group_vars/`, `host_vars/`, `files/`, `templates/`, and the playbook itself — all at the same level. And this is for a relatively simple service (NTP). In real infrastructure, where you provision databases, application servers, monitoring agents, and custom configurations, this approach becomes unmanageable. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The fundamental problem is that a single playbook file and a flat directory structure mixes everything together. When you need to change a variable, you might have to look inside the playbook, or in `group_vars`, or in `host_vars`. When you need to modify a task, you scroll through a long playbook that also contains handlers and variable definitions. There is no separation of concerns. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.2 What Ansible Roles Are

Ansible roles are a **structural mechanism** that takes all the content that would otherwise live inside a single playbook and distributes it across a standardized directory hierarchy. Instead of one monolithic playbook with tasks, handlers, variables, templates, and files all intermingled, a role provides dedicated directories for each component type. Tasks go into `tasks/main.yml`. Handlers go into `handlers/main.yml`. Variables go into `vars/main.yml` or `defaults/main.yml`. Templates go into `templates/`. Files go into `files/`. Each directory has a single, clear responsibility. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The playbook itself becomes extremely simple — it only declares which **roles** to apply to which hosts. All the implementation detail lives inside the role's directory structure. The instructor demonstrates this transformation: the original playbook had variables, dozens of task lines, handlers, and template references. After converting to a role, the playbook is reduced to just the play header (`hosts`, `become`) and a `roles:` list with a single entry. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.3 Identifying Roles — Thinking About Server Purpose

Before creating roles, you must **identify what roles your servers play**. This is not an Ansible concept — it is an infrastructure concept. In any organization's infrastructure, different servers serve different purposes: some are MySQL database servers, some are Tomcat application servers, some are Apache web servers, some are build servers. And some configurations are **common** across all servers — NTP time synchronization, monitoring agents, logging agents, security baselines. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

Each of these purposes becomes a potential Ansible role. You might have a `post-install` role for common setup, a `mysql` role for database servers, a `tomcat` role for application servers. The role encapsulates everything needed to configure a server for that purpose. The NTP provisioning done in previous exercises is an example of a common role that applies to all servers. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.4 The Role Directory Structure

When you create a role, it follows a standardized directory layout:

```
roles/
  <role-name>/
    tasks/main.yml        ← the task list (executed when the role runs)
    handlers/main.yml     ← handler definitions
    templates/            ← Jinja2 template files
    files/                ← static files for the copy module
    vars/main.yml         ← variables (HIGH priority)
    defaults/main.yml     ← variables (LOW priority)
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The `tasks/main.yml` is the most important file. When Ansible executes a role, it runs this file. The tasks inside it reference templates, files, handlers, and variables — and Ansible knows to look for those resources **within the role's own directory structure**. This is a key architectural behavior: the `template` and `copy` modules are "smart enough" to know where to look. If a task references a template called `ntp_centos.conf.j2`, Ansible automatically looks inside the role's `templates/` directory. You do not need to specify the full path — just the filename. Similarly, the `copy` module looks inside the role's `files/` directory. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

This automatic path resolution means that when you convert a playbook to a role, you must **remove directory prefixes** from your template and file references. If the original playbook said `src: templates/ntp_centos.conf`, the role's task should say `src: ntp_centos.conf.j2` — just the filename, because Ansible will look in `templates/` automatically. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

🔍 **Deep Dive**
The video also mentions that template files should follow the `.j2` extension convention. This is not mandatory — Ansible doesn't require it — but it is a **standard** practice. The instructor renames the template files from their original names to `.j2` extensions during the conversion, and updates the task references to match. If the filename in the task doesn't match the actual file on disk, Ansible will fail to find the template. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.5 The `ansible-galaxy init` Command

You do not need to create the role directory structure manually. The command `ansible-galaxy init <role-name>` generates the entire standardized directory tree for you — `tasks/`, `handlers/`, `templates/`, `files/`, `vars/`, `defaults/`, and more, each with a `main.yml` file where appropriate. You run this command from inside a `roles/` directory, and it creates a subdirectory with the role name containing the full skeleton. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.6 `vars` vs `defaults` — The Variable Priority System

A role has **two** places to define variables: `vars/main.yml` and `defaults/main.yml`. They serve different purposes through the **priority system**:

**`defaults/main.yml`** has **low priority**. This is where you define the default values for all variables your role uses. These are the values that apply unless someone overrides them. The general practice is to put variables here. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**`vars/main.yml`** has **higher priority**. Variables defined here override those in `defaults`. Because of this higher priority, if you put variables in `vars` and then try to override them from the playbook, you may get unexpected behavior (playbook variables have a specific place in the priority chain). [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The instructor initially puts variables in `vars/main.yml` for demonstration purposes, then explicitly moves them to `defaults/main.yml` in a subsequent exercise, explaining: "In general, it's a general practice to define variables into the defaults main.yml." [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The reason `defaults` is preferred is directly tied to **reusability**. Roles are designed to be used across multiple projects and environments. The default values work for the common case, but different projects or data centers may need different values. By putting variables in `defaults`, they can be easily overridden from the playbook without touching the role itself. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

### Overriding Variables from the Playbook

When you reference a role in your playbook, you can override its variables inline:

```yaml
roles:
  - role: post-install
    vars:
      ntp0: "india.ntp.server.0"
      ntp1: "india.ntp.server.1"
```

Playbook-level variables have **higher priority** than `defaults`. So the values specified here will be used instead of whatever is in `defaults/main.yml`. This is the mechanism that makes roles reusable across environments — same role, different variable values per deployment. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The video demonstrates this with NTP servers: the defaults contain generic NTP server addresses, but for an India-region deployment, the playbook overrides them with India-specific NTP servers. When the playbook runs, the template module detects that the variable values have changed (the source file content is now different), pushes the new configuration, and triggers the handlers to restart the service. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

⚠️ **Expert Note**
If variables are in `vars/main.yml` (high priority) instead of `defaults/main.yml`, overriding them from the playbook becomes more complicated because `vars` in the role may take precedence over playbook variables depending on the exact context. This is why the instructor explicitly moves them to `defaults` and removes the `vars/main.yml` content — to ensure the override mechanism works cleanly. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.7 Reusability — The Core Purpose of Roles

The instructor states this directly: "If you are not doing reusability then there is no use of creating roles." Roles exist at the **organization level**. If most projects in your organization use a Tomcat application server, you create a Tomcat role once and reuse it across projects. If every server needs NTP configured, the NTP role is written once and applied everywhere. The role creates a **standard** — consistent configuration across the organization — while variables handle the **variation** between environments, regions, or projects. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

Without reusability intent, roles add structural overhead without benefit. A single-use playbook can stay as a playbook. Roles become valuable when the same configuration pattern is needed in multiple places. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.8 Converting a Playbook to a Role — The Recommended Workflow

The instructor explicitly recommends: write the **playbook first**, get it working, and **then** convert it to a role. Writing roles from scratch is harder because "we need to do a lot of things." But converting an existing, working playbook into a role is straightforward — you're just redistributing content from one file into the role's directory structure: tasks go to `tasks/main.yml`, handlers to `handlers/main.yml`, variables to `defaults/main.yml`, templates to `templates/`, files to `files/`. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

During conversion, two adjustments are needed:

1. **Remove leading indentation** from tasks and handlers. In the playbook, tasks are indented under `tasks:`. In the role's `main.yml`, they are at the top level of the list. The video uses Vim's substitution command (`:%s/^    //`) to strip four leading spaces from all lines at once. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)
2. **Remove directory prefixes** from template `src` and file `src` paths, since the role's modules auto-resolve paths within the role structure. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.9 Ansible Galaxy — Community Roles

Ansible Galaxy (`galaxy.ansible.com`) is a public repository of roles created by the community. Instead of writing every role from scratch, you can search for existing roles — for Java installation, database setup, monitoring, NTP, and virtually anything else. Roles have quality scores and community ratings. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

You download a community role with: `ansible-galaxy install <role-name>`. The role is downloaded from GitHub and stored in `~/.ansible/roles/<role-name>/`. Once downloaded, you reference it by name in your playbook's `roles:` list, just like a local role. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The video demonstrates downloading `geerlingguy.java` — a popular role by a well-known community author. After downloading, the instructor adds it to the playbook's roles list before the custom `post-install` role. When executed, it installs the correct version of Java based on the target's operating system, using internal conditions and OS-specific task files. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## 1.10 Studying Community Roles — The `include_tasks` Pattern

The instructor opens the `geerlingguy.java` role's internal structure to show how industry experts write roles. The key pattern revealed is **`include_tasks`**: instead of putting all tasks in one `main.yml` with `when` conditions, the role creates separate task files for each OS family (e.g., `setup-RedHat.yml`, `setup-Debian.yml`). The `main.yml` uses `include_tasks` to dynamically import the correct file based on `ansible_os_family` or `ansible_distribution` fact variables. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

Similarly, the role uses `include_vars` to load OS-specific variable files. The filename itself is constructed from a fact variable — for example, loading `CentOS.yml` when the distribution is CentOS. This approach is more sophisticated than the inline `when` conditions used in earlier exercises. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The instructor's personal recommendation: "I use these roles to study them and see how they're writing. These are the industry experts in writing the Ansible playbooks or roles. And we can learn from them." He also candidly shares that he personally uses Galaxy roles "very less" in production because modifying someone else's role requires reverse engineering — understanding all their tasks, handlers, and conditions before making changes. Since Ansible playbooks are relatively easy to write (with documentation and ChatGPT), he prefers writing from scratch for full control. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are converting an existing multi-component Ansible playbook (with tasks, handlers, variables, templates, and files) into an Ansible **role** called `post-install`. The final outcome: a drastically simplified playbook that just lists roles, with all implementation details distributed into the role's standardized directory structure. We also demonstrate variable overriding and downloading a community role from Ansible Galaxy. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 1: Prepare the Exercise Directory

Copy the previous exercise to preserve it:

```bash
cp -r exercise13 exercise14
cd exercise14
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 2: Complicate the Playbook (Setup for Demonstration)

Open the playbook and add additional content to make the role conversion more meaningful:

**2a. Add a copy task:**

```yaml
    - name: Dump file
      copy:
        src: files/myfile.txt
        dest: /tmp/myfile.txt
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**2b. Add a variable-driven task:**

Change an existing directory-creation task to use a variable `mydir` instead of a hardcoded path. Then define the variable in the playbook:

```yaml
  vars:
    dir1: /opt/dir22
```

And reference it in the task as `{{ dir1 }}`. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**2c. Create the source file:**

```bash
mkdir -p files
vim files/myfile.txt
```

Add any content, save and quit. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**2d. Test the playbook:**

```bash
ansible-playbook provisioning.yaml
```

**Common errors caught live in the video:**

| Error                                     | Cause                                                        | Fix                              |
| ----------------------------------------- | ------------------------------------------------------------ | -------------------------------- |
| `mydir is undefined`                      | Task references variable `mydir` but playbook defines `dir1` | Match the variable names exactly |
| `src or content required` for copy module | Used `files:` instead of `src:`                              | Change the key to `src:`         |

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

After fixing, the playbook runs successfully. The repository now has enough content (variables, tasks, handlers, templates, files) to justify role conversion.

***

## Step 3: View the Current Directory Structure

Install the `tree` utility for visualization:

```bash
sudo apt install tree
cd ..
tree exercise14
```

**Expected structure:** Ansible config, `files/`, `group_vars/`, `host_vars/`, `templates/`, the playbook, inventory — everything at the same flat level. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 4: Create the Role Skeleton

```bash
cd exercise14
mkdir roles
cd roles
ansible-galaxy init post-install
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

| Part                               | Meaning                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------- |
| `mkdir roles`                      | Create the roles directory (Ansible looks here by default)              |
| `cd roles`                         | Enter the roles directory                                               |
| `ansible-galaxy init post-install` | Generate the full role directory structure with the name `post-install` |

Run `tree` to verify the structure was created — `tasks/`, `handlers/`, `templates/`, `files/`, `vars/`, `defaults/`, each with `main.yml` files. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 5: Move Variables into the Role

**5a. Copy external variables:**

```bash
cd ..   # back to exercise14
cat group_vars/all
```

Copy the variable content. Open the role's vars file:

```bash
vim roles/post-install/vars/main.yml
```

Paste the variables. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**5b. Move inline playbook variables:**

Open the playbook (`cat provisioning.yaml`), find the `vars:` section, copy those variables, and add them to the same `vars/main.yml` file. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**5c. Clean up external variable files:**

```bash
rm -rf group_vars
rm -rf host_vars
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 6: Move Files and Templates into the Role

```bash
cp files/* roles/post-install/files/
cp templates/* roles/post-install/templates/
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

After copying, remove the original directories from the exercise root:

```bash
rm -rf files
rm -rf templates
```

***

## Step 7: Move Handlers into the Role

Open the playbook and copy all handler definitions. Then:

```bash
vim roles/post-install/handlers/main.yml
```

Paste the handlers. **Critical step:** Remove the leading indentation. In the playbook, handlers are indented (typically 4 spaces) under the `handlers:` key. In the role's `main.yml`, they must start at the YAML list level (no leading spaces). Use Vim's substitution:

```vim
:%s/^    //
```

This replaces 4 leading spaces with nothing on every line. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 8: Move Tasks into the Role

Copy all tasks from the playbook. Open:

```bash
vim roles/post-install/tasks/main.yml
```

Paste and strip leading indentation:

```vim
:%s/^    //
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**Then fix the path references:**

In the tasks, find any `template` module references like `src: templates/ntp_centos.conf` and change them to just `src: ntp_centos.conf.j2`. The role's template module auto-resolves to the `templates/` directory within the role structure. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

Similarly, for `copy` module references, change `src: files/myfile.txt` to just `src: myfile.txt`. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**Rename template files to `.j2`:**

```bash
cd roles/post-install/templates
mv ntp_centos.conf ntp_centos.conf.j2
mv ntp_ubuntu.conf ntp_ubuntu.conf.j2
```

The filenames must match exactly what the tasks reference. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 9: Simplify the Playbook

Open the playbook and remove: all `vars:` definitions, all `tasks:`, all `handlers:`. Replace with:

```yaml
---
- name: Provisioning servers
  hosts: all
  become: yes
  roles:
    - post-install
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

The `roles:` key takes a YAML list. Each entry is a role name. You can list multiple roles — they execute in order.

Save and quit. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 10: Test the Role-Based Playbook

```bash
ansible-playbook provisioning.yaml
```

**Expected output:** The tasks execute with a slightly different format — each task is prefixed with the role name: `TASK [post-install : <task name>]`. This confirms Ansible is executing tasks from the role, not from the playbook directly. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 11: Move Variables from `vars` to `defaults`

Create a new exercise for this:

```bash
cp -r exercise14 exercise15
cd exercise15
```

**11a. Copy variables from vars to defaults:**

```bash
cat roles/post-install/vars/main.yml
```

Copy the content. Open:

```bash
vim roles/post-install/defaults/main.yml
```

Paste. Then clear `vars/main.yml`:

```bash
vim roles/post-install/vars/main.yml
```

Remove all variable content (leave the file empty or with just `---`). [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**11b. Test:**

```bash
ansible-playbook provisioning.yaml
```

It works — Ansible finds the variables in `defaults`. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 12: Override Variables from the Playbook

Modify the playbook to override NTP server values for a different region:

```yaml
roles:
  - role: post-install
    vars:
      ntp0: "0.in.pool.ntp.org"
      ntp1: "1.in.pool.ntp.org"
      ntp2: "2.in.pool.ntp.org"
      ntp3: "3.in.pool.ntp.org"
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

Note the syntax change: instead of `- post-install` (simple list entry), you use `- role: post-install` followed by `vars:` for the overrides.

**Test:**

```bash
ansible-playbook provisioning.yaml
```

**Expected:** The template module detects the variable values have changed (configuration file content is different), pushes new files, and triggers handlers to restart services. Tasks show `changed` for the template and handler tasks. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

## Step 13: Download and Use a Community Role from Ansible Galaxy

**13a. Download the role:**

```bash
ansible-galaxy install geerlingguy.java
```

 [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

| Part                     | Meaning                                |
| ------------------------ | -------------------------------------- |
| `ansible-galaxy install` | Download a role from Ansible Galaxy    |
| `geerlingguy.java`       | The role name (author.rolename format) |

The role downloads from GitHub and installs to `~/.ansible/roles/geerlingguy.java/`. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**13b. Add it to the playbook:**

```yaml
roles:
  - geerlingguy.java
  - role: post-install
    vars:
      ntp0: "0.in.pool.ntp.org"
      # ...
```

The Java role is listed first — it executes before `post-install`. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**13c. Test:**

```bash
ansible-playbook provisioning.yaml
```

The Java role installs the correct version of Java based on each target's operating system, using internal OS-detection logic. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

**13d. Study the role's internal structure:**

```bash
tree ~/.ansible/roles/geerlingguy.java/
cat ~/.ansible/roles/geerlingguy.java/tasks/main.yml
```

Observe the `include_tasks` and `include_vars` patterns — OS-specific task and variable files loaded dynamically based on fact variables. [\[247-roles \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/247-roles.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Transformation

```
BEFORE (monolithic):
  playbook.yaml = vars + tasks + handlers + template refs + file refs
  exercise14/   = files/ + templates/ + group_vars/ + host_vars/ + playbook

AFTER (role-based):
  playbook.yaml = hosts + become + roles: [post-install]
  roles/post-install/ = tasks/ + handlers/ + templates/ + files/ + defaults/ + vars/
```

***

## Role Directory Structure

```
roles/
  post-install/
    tasks/main.yml         ← EXECUTES when role runs (core file)
    handlers/main.yml      ← handler definitions
    templates/             ← .j2 files (auto-resolved by template module)
    files/                 ← static files (auto-resolved by copy module)
    defaults/main.yml      ← variables, LOW priority (preferred location)
    vars/main.yml          ← variables, HIGH priority (use sparingly)
```

***

## Creation Command

```
mkdir roles && cd roles
ansible-galaxy init <role-name>    → generates full directory skeleton
```

***

## Playbook Syntax — Two Forms

```yaml
# Simple (no overrides):
roles:
  - post-install

# With variable overrides:
roles:
  - role: post-install
    vars:
      ntp0: "0.in.pool.ntp.org"
```

***

## Variable Priority Chain

```
defaults/main.yml    → LOW priority  (default values, easily overridden)
                          ↑ overridden by
playbook vars:       → HIGHER priority (per-role overrides)
                          ↑ overridden by
vars/main.yml        → HIGH priority  (hard to override — avoid for reusable roles)

Best practice: put variables in defaults/ → override from playbook when needed
```

***

## Conversion Checklist (Playbook → Role)

```
1. ansible-galaxy init <role-name>     (inside roles/ directory)
2. Move vars        → defaults/main.yml (or vars/main.yml)
3. Move files       → roles/<name>/files/
4. Move templates   → roles/<name>/templates/   (rename to .j2)
5. Move handlers    → handlers/main.yml          (strip 4-space indent)
6. Move tasks       → tasks/main.yml             (strip 4-space indent)
7. Fix template src → remove "templates/" prefix (auto-resolved)
8. Fix copy src     → remove "files/" prefix     (auto-resolved)
9. Replace playbook tasks/handlers/vars with:  roles: [<name>]
10. Delete group_vars/, host_vars/, files/, templates/ from root
```

***

## Vim Indent Strip Command

```vim
:%s/^    //
       ^^^^
       4 spaces (match playbook indentation depth)
       replace with nothing → left-aligns for role's main.yml
```

***

## Auto-Path Resolution (Critical)

```
In playbook:   src: templates/ntp_centos.conf     (explicit path)
In role task:  src: ntp_centos.conf.j2             (filename only)

template module → looks in roles/<name>/templates/ automatically
copy module     → looks in roles/<name>/files/ automatically

⚠️ If filename in task ≠ filename on disk → file not found error
⚠️ Rename templates to .j2 (standard, not mandatory)
```

***

## Ansible Galaxy — Community Roles

```
Search:     galaxy.ansible.com
Download:   ansible-galaxy install geerlingguy.java
Location:   ~/.ansible/roles/geerlingguy.java/
Use:        roles: [geerlingguy.java]

Quality signals: quality score (5/5), community score (4.3/5)
```

***

## Community Role Internal Pattern (geerlingguy.java)

```
tasks/main.yml:
  include_vars: "{{ ansible_distribution }}.yml"     ← load OS-specific variables
  include_tasks: "setup-RedHat.yml"                  ← load OS-specific tasks
    when: ansible_os_family == "RedHat"
  include_tasks: "setup-Debian.yml"
    when: ansible_os_family == "Debian"

Pattern: separate files per OS + include dynamically
  vs. our approach: single file with when: conditions per task
```

***

## Galaxy Roles — Instructor's Pragmatic View

```
USE FOR:     learning (study expert code structure)
             quick standard setups (Java, NTP, monitoring)

AVOID FOR:   heavily customized deployments
             → reverse engineering someone else's role is harder
                than writing a new playbook with docs + ChatGPT

Recommendation: write from scratch for control, study Galaxy for patterns
```

***

## Role Execution Output

```
Without role:  TASK [Install NTP agent on CentOS]
With role:     TASK [post-install : Install NTP agent on CentOS]
                     ^^^^^^^^^^^^
                     role name prefix in output
```

***

## Variable Override Flow (NTP Example)

```
defaults/main.yml:  ntp0 = "0.us.pool.ntp.org"    (generic default)
                          ↓ overridden by
playbook vars:      ntp0 = "0.in.pool.ntp.org"    (India-specific)
                          ↓
template renders with India values → config file content CHANGES
                          ↓
template module detects change → pushes new file → triggers handler
                          ↓
handler restarts NTP service with new config
```

***

## Reusability Model

```
ROLE = standard configuration logic (organization-wide)
VARIABLES = environment/project-specific values (overridden per deployment)

Same role → different projects:
  Project A (US):    ntp0 = "0.us.pool.ntp.org"
  Project B (India): ntp0 = "0.in.pool.ntp.org"
  
Role code: UNCHANGED
Variables: OVERRIDDEN from each project's playbook

⚠️ No reusability intent → no point creating a role
```

***

## Additional Playbook Flexibility

```
Playbook with role CAN also have:
  tasks:      ← additional tasks alongside roles
  handlers:   ← additional handlers alongside roles

Roles don't lock out direct playbook content.
But primary content should live in the role for reusability.
```

***

## Key Engineering Patterns

| Pattern                            | Manifestation                                                                                                    |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Separation of concerns**         | Each directory has one responsibility — tasks, handlers, vars, templates, files                                  |
| **Convention over configuration**  | Standardized directory names → modules auto-resolve paths without explicit configuration                         |
| **Defaults + override**            | Low-priority defaults enable reuse; playbook overrides enable customization                                      |
| **Working-first → refactor**       | Write playbook first, get it working, then convert to role — don't start with role structure                     |
| **Organization-level abstraction** | Roles exist above projects — reusable across teams, environments, data centers                                   |
| **Community as learning resource** | Galaxy roles studied for expert patterns (`include_tasks`, `include_vars`) rather than used blindly              |
| **Indirection via include**        | `include_tasks` / `include_vars` dynamically loads OS-specific content — cleaner than inline conditions at scale |

***

## Series Context

```
BEFORE: Decision making (when) → Loops → Templates → Handlers
THIS:   Roles (combine everything into reusable modular structure)
NEXT:   Cloud automation with Ansible
```

***

This completes the full reconstruction. **Theory** explains *why* roles exist, how the directory structure works, and the variable priority system. **Practical** walks through every move, every file rename, and every syntax change during the conversion. The **Compression Map** gives you the conversion checklist, priority chain, and auto-resolution rules for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
