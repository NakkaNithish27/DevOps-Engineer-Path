# 🧠 Ansible Playbooks & Modules — Structure, Execution, Debugging & Documentation

**Source:** *237. Playbook and Modules* — Ansible Automation Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Is an Ansible Playbook?

In Bash, you write **shell scripts**. In Python, you write **Python scripts**. In Ansible, you write **playbooks**. A playbook is Ansible's equivalent of a script — it's the file where you define the automation work you want performed on remote machines. But unlike a Bash script which is a sequential list of commands, an Ansible playbook has a **specific hierarchical structure** built on YAML, and understanding that structure is the foundation of everything else.

A playbook is a **list of plays**. Each play targets a specific group of servers and defines what tasks should be executed on them. A play contains a **list of tasks**, and each task invokes a specific **module** with arguments. This creates a three-level hierarchy that governs everything you write in Ansible:

**Level 1 — Play level (global area):** Where you declare which hosts to target, whether to use sudo (`become`), and the play name.

**Level 2 — Task level:** Where you declare individual tasks, each with a name and a module invocation.

**Level 3 — Module arguments level:** Where you provide the key-value pairs that configure what the module does (package name, service state, etc.).

The instructor emphasizes this structure deliberately: *"Don't get overwhelmed by looking at many lines and different options."* The structure is always the same three levels — only the modules and their arguments change.

***

## 1.2 The YAML Structure Underneath — Lists and Dictionaries All the Way Down

Understanding playbook structure requires understanding how YAML data types map to playbook components:

A **playbook** is a **YAML list** of plays. That's why each play starts with a hyphen (`-`): the hyphen is YAML's list item indicator. Two plays means two hyphen-prefixed blocks at the top level.

Each **play** is a **dictionary** — a collection of key-value pairs. The keys include `name` (play name, string value), `hosts` (target group, string value), `become` (sudo, boolean value), and `tasks` (another list).

The `tasks` key's value is itself a **list** — a list of task dictionaries. Each task dictionary has a `name` key (string) and a module key whose value is yet another **dictionary** of module arguments.

So the full data type chain is: **list** (of plays) → **dictionary** (play) → **list** (of tasks) → **dictionary** (task) → **dictionary** (module arguments). The instructor walks through this explicitly: *"Playbook is a list of plays. Each item in the list is a dictionary. Task value is again list and again list of dictionary."*

The reason the instructor explains this so carefully: *"When you make mistake — syntax errors in the playbook — you will understand whether you made a mistake at a dictionary or a list level or a string level."* Knowing the data type at each level is the key to debugging YAML syntax errors.

> 🔍 **Deep Dive:** The YAML `---` (three hyphens) at the beginning of a playbook is a document start marker. The instructor notes it's *"not mandatory but a standard practice while writing YAML files."* It signals the beginning of a YAML document and becomes important when multiple YAML documents exist in a single file or stream.

***

## 1.3 Plays — Targeting Server Groups with Automation

A play is a unit of work directed at a **specific group of servers**. The `hosts:` key specifies which inventory group this play targets. In the lecture's example, the first play targets `webservers` (to install and start Apache/httpd), and the second play targets `dbservers` (to install and start MariaDB).

This is an important architectural concept: a single playbook can orchestrate **different actions on different server groups**. The web servers get web server packages; the database servers get database packages. Both happen in one playbook execution, but each play operates independently on its target group.

The `become: yes` key tells Ansible to execute all tasks in this play with **elevated privileges** (sudo). Most system administration tasks — installing packages, managing services — require root access. Setting `become: yes` at the play level applies sudo to every task within that play, so you don't need to specify it on each task individually.

***

## 1.4 Tasks — Individual Units of Work

A task is a single action: install a package, start a service, copy a file, create a user. Each task invokes exactly one **module** and passes arguments to it.

Tasks have a **`name`** field that's purely for human readability — it describes what the task does. The instructor emphasizes: *"You can give any name in the task and any name in the play."* The name appears in the execution output, making it easy to track which task is running and which succeeded or failed. However, within the module arguments, the `name` key has a technical meaning — it's the actual package name or service name, which *"cannot be anything."*

Tasks within a play execute **sequentially, top to bottom**. Each task must complete on all target hosts before the next task begins. The order matters — you must install a package before you can start its service.

***

## 1.5 Modules — The Executable Units

Modules are the actual tools that perform work. When you write a task, you specify a module and its arguments. The module handles the implementation details — it knows how to install a package on the target OS, how to manage a service, how to copy a file.

The lecture uses two modules:

**`ansible.builtin.yum`** — Manages packages on Red Hat/CentOS systems using the yum package manager. Key arguments: `name` (package name) and `state` (`present` to install, `absent` to remove).

**`ansible.builtin.service`** — Manages system services. Key arguments: `name` (service name), `state` (`started`, `stopped`, etc.), and `enabled` (`yes` to enable on boot).

The module naming has evolved. The instructor notes that previously, you could use just the short name (`yum`, `service`), but the newer Ansible versions use a **fully qualified collection name** (FQCN): `ansible.builtin.yum`, `ansible.builtin.service`. This reflects Ansible's module organization into **collections** — structured groupings of modules by source and purpose.

The relationship between playbook tasks and the ad hoc commands from the previous lecture is direct: in ad hoc, you used `-m yum -a "name=httpd state=present"`. In a playbook, the same operation becomes a structured YAML block with the module name as a key and arguments as a nested dictionary. Same module, same arguments, different format.

***

## 1.6 Module Collections — The Organizational Structure

The instructor navigates the Ansible documentation to show the module ecosystem. Modules are organized into **collections**:

* **`ansible.builtin`** — Core modules shipped with Ansible (yum, service, copy, file, etc.)
* **Community modules** — Contributed by the community
* **Provider-specific collections** — `amazon.aws` (AWS modules), Azure modules, Google Cloud modules, Cisco modules, Windows modules, POSIX utilities

The collection list is massive — the instructor scrolls through it and is *"still at the A"* before reaching C. The key takeaway isn't memorization: *"Don't go get into that by-hearting thing. You have documentation. Know how to use the documentation. That's all you need to do."*

Each module's documentation page contains: a description, **requirements** (prerequisites needed on the target machine), **parameters** (all available options with descriptions), and **examples** (copy-paste-ready playbook snippets). The instructor's workflow advice: search for your module, scroll to the examples, copy-paste, then modify.

> ⚠️ **Expert Note:** The instructor specifically points out the **parameters** section: *"When you visit the documentation of any module, look at the parameters, what all you can pass. There are many amazing options."* The examples show common use cases, but the parameters section reveals the full capability of each module — options you might not know exist until you read the documentation.

***

## 1.7 Gathering Facts — The Hidden Default Task

When the playbook executes, the output shows **three** tasks for the web server play, even though only **two** were defined. The extra task is **"Gathering Facts"** — a default behavior where Ansible automatically runs the `setup` module at the beginning of each play to collect information about the target machine (OS type, IP addresses, memory, disk, etc.).

The instructor briefly explains: *"Ansible by default uses a module called setup that collects the target machine information in the runtime. It does not save anywhere."* This information is collected in memory for the duration of the play and can be used in conditional logic and templates (covered in later lectures). The gathering facts task doesn't make any changes to the target — it's read-only.

***

## 1.8 Idempotency in Playbook Execution

When you run the same playbook twice, the output changes. The first run shows **`changed`** for tasks that modified the system (installed packages, started services). The second run shows **`ok`** for those same tasks — because the packages are already installed and the services are already running. Ansible detects the current state and only makes changes when needed.

This is the same idempotency behavior seen in ad hoc commands, now visible in playbook execution output. The `changed` vs `ok` status tells you whether Ansible actually modified anything or found the system already in the desired state.

***

## 1.9 Debugging — The Verbosity Levels

When something goes wrong — or when you need to understand what Ansible is doing internally — you can increase the **verbosity** of the output by adding `-v` flags to the command:

| Flag    | Level   | What It Shows                                                                                                              |
| ------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| `-v`    | Level 1 | Extra information, JSON data output from modules                                                                           |
| `-vv`   | Level 2 | Ansible version, config file, Python version, playbook path, **line numbers** in the playbook                              |
| `-vvv`  | Level 3 | Huge output — Linux command options being used internally, **which login key** is being used, **which user** is connecting |
| `-vvvv` | Level 4 | Maximum verbosity — final level, most detailed                                                                             |

The instructor highlights the practical debugging value: at `-vvv`, you can see **what identity file (key)** and **what user** Ansible is using to connect. These are the kinds of **logical errors** that are hard to catch otherwise — using the wrong key, wrong user, or a user without sudo privileges. The instructor distinguishes: *"Syntactical errors are very easy to solve. But logical mistakes are difficult to catch — what user are you using? The right user? Are you using the right key? Does that user have sudo privilege?"*

***

## 1.10 Syntax Check and Dry Run — Pre-Execution Validation

Before executing a playbook against live infrastructure, Ansible provides two pre-execution validation mechanisms:

**`--syntax-check`** — Validates the YAML structure and playbook syntax without executing anything. If the syntax is correct, it simply prints the playbook name. If there's an error, it shows the offending line.

However, the instructor provides a critical caveat about syntax error line numbers: *"Sometimes you make mistakes in some other line and it tells you the mistake is in some other line. That is because of the YAML structure."* YAML's indentation-based structure means an error in one line can cascade and be reported at a different line. Don't blindly trust the line number — examine the broader playbook structure.

**`-C` (dry run / check mode)** — Simulates the playbook execution without making any actual changes. It goes through the motions — connecting to hosts, evaluating tasks — but doesn't apply changes. The instructor calls it a **"very good practice"** to do before actual execution, but immediately warns: *"Don't take it as a guarantee. If it runs in the dry run, there is no guarantee it is going to run actually."* Dry runs can fail or succeed differently than actual runs when runtime variables or dynamic conditions are involved.

The recommended pre-execution workflow: **syntax check first → dry run second → actual execution third**.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are writing and executing an **Ansible playbook** that configures two groups of servers: **web servers** (installing and starting Apache/httpd) and **database servers** (installing and starting MariaDB). This replaces the ad hoc commands from previous lectures with a structured, repeatable, version-controllable automation file.

**Final outcome:** A single `ansible-playbook` command that installs packages and starts services on multiple server groups, with full output showing task status, and the ability to debug, syntax-check, and dry-run before execution.

***

## Step 1: Set Up the Exercise Directory

Copy the previous exercise directory (Exercise 5) to create the working directory for this lecture. Remove the `index.html` file — it's not needed here.

**What you should have:**

* Inventory file (defines server groups: webservers, dbservers)
* Login key file (SSH private key for connecting to target machines)
* Empty space for the new playbook file

***

## Step 2: Create the Playbook File — `web-db.yaml`

Create a new file named `web-db.yaml`. The name is descriptive (one play for web, one for db) but can be anything — you pass the filename explicitly when running the playbook.

### The Complete Playbook:

```yaml
---
- name: Webserver setup
  hosts: webservers
  become: yes
  tasks:
    - name: Install httpd
      ansible.builtin.yum:
        name: httpd
        state: present

    - name: Start httpd service
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: yes

- name: DBserver setup
  hosts: dbservers
  become: yes
  tasks:
    - name: Install mariadb server
      ansible.builtin.yum:
        name: mariadb-server
        state: present

    - name: Start mariadb service
      ansible.builtin.service:
        name: mariadb
        state: started
        enabled: yes
```

**Structure breakdown (by indentation level):**

**Level 1 (column 0) — Play start:** `- name:`, `hosts:`, `become:`, `tasks:` — These define the play's identity and scope. Each play starts with a `-` at the leftmost column.

**Level 2 (indented under `tasks:`) — Task start:** `- name:` and the module key (e.g., `ansible.builtin.yum:`) — These define individual tasks. Each task starts with `-` indented under `tasks:`. Both tasks within a play must be in the **same column**.

**Level 3 (indented under module) — Module arguments:** `name:`, `state:`, `enabled:` — These are key-value pairs configuring what the module does.

**Critical indentation rules:**

* Tasks under the same play must align at the same column
* Module arguments must be indented under the module name
* The second play starts back at column 0 (same level as the first play)
* Use consistent spacing (2 spaces per level is standard)

**Common mistakes:**

| Mistake                                                                                | Symptom                                            | Fix                                                               |
| -------------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------- |
| Module arguments at wrong indentation                                                  | YAML syntax error                                  | Indent arguments one level deeper than the module name            |
| Second play not starting at column 0                                                   | Interpreted as part of first play, or syntax error | Ensure each play's `-` is at the leftmost column                  |
| Tasks at different indentation levels within same play                                 | YAML parsing error                                 | Align all `-name:` entries under the same play at the same column |
| Confusing task `name` (human label) with module argument `name` (package/service name) | Wrong package installed, or task just has a label  | Task name = any description; module `name` = exact technical name |

***

## Step 3: Remove Previously Installed Packages (Clean Slate)

Before testing the playbook, remove packages that were installed via ad hoc commands in previous lectures. This ensures the playbook has real work to do (install fresh).

```bash
ansible webservers -m ansible.builtin.yum -a "name=httpd state=absent" --become
```

**Breakdown:**

* `ansible webservers` — Target the webservers group (ad hoc command, not playbook)
* `-m ansible.builtin.yum` — Use the yum module (fully qualified name)
* `-a "name=httpd state=absent"` — Arguments: package `httpd`, state `absent` (remove)
* `--become` — Execute with sudo

**Expected output:** `changed` (package removed). This resets the state so the playbook execution shows meaningful `changed` output.

***

## Step 4: Execute the Playbook

```bash
ansible-playbook -i <inventory-path> web-db.yaml
```

**Command breakdown:**

* `ansible-playbook` — The playbook execution command (distinct from the `ansible` command used for ad hoc). For ad hoc: `ansible`. For playbooks: `ansible-playbook`.
* `-i <inventory-path>` — Path to the inventory file defining server groups
* `web-db.yaml` — The playbook file to execute

**Expected output structure:**

```
PLAY [Webserver setup] ********************************************************

TASK [Gathering Facts] ********************************************************
ok: [web01]

TASK [Install httpd] **********************************************************
changed: [web01]

TASK [Start httpd service] ****************************************************
changed: [web01]

PLAY [DBserver setup] *********************************************************

TASK [Gathering Facts] ********************************************************
ok: [db01]

TASK [Install mariadb server] *************************************************
changed: [db01]

TASK [Start mariadb service] **************************************************
changed: [db01]

PLAY RECAP ********************************************************************
```

**Key observations:**

* **Gathering Facts** appears as the first task of each play — this is automatic (see Theory §1.7). It shows `ok` because it's read-only.
* Tasks that modified the system show **`changed`**.
* Each play section is clearly labeled with the play name.

**Running the playbook a second time:**

* Tasks that were already applied show **`ok`** instead of `changed` — idempotency in action.

***

## Step 5: Debugging with Verbosity Flags

If something goes wrong, or you need to understand Ansible's internal behavior:

```bash
ansible-playbook -i <inventory-path> web-db.yaml -v
```

**Increasing verbosity levels:**

| Command | What You Get                                                                      |
| ------- | --------------------------------------------------------------------------------- |
| `-v`    | Module JSON output, extra task details                                            |
| `-vv`   | Ansible version, config file path, Python version, **playbook line numbers**      |
| `-vvv`  | Full connection details: **which SSH key**, **which user**, Linux command options |
| `-vvvv` | Maximum detail — final verbosity level                                            |

**When to use each level:**

* Start with `-v` for basic troubleshooting
* Use `-vv` when you need to locate which line in the playbook is causing issues
* Use `-vvv` when you suspect **connection problems** — wrong user, wrong key, no sudo privilege
* `-vvvv` is rarely needed but available for deep investigation

**Debugging logical errors** (the hard ones): The instructor lists the questions to ask at `-vvv` level: *"What user are you using? The right user? Are you using the right key? Does that user have sudo privilege? The module that you are using — is it correct?"*

***

## Step 6: Syntax Check (Pre-Execution Validation)

```bash
ansible-playbook -i <inventory-path> web-db.yaml --syntax-check
```

**Expected on success:** Prints the playbook name — nothing else. This means the YAML structure is valid.

**Expected on failure:** Shows the offending line and an error message. Example:

```
The offending line appears to be:
...
```

⚠️ **Critical caveat:** The line number reported may not be the actual error location. YAML indentation errors cascade — an error on line 8 might be reported on line 12. If the reported line looks correct, **examine the surrounding lines and overall structure**.

***

## Step 7: Dry Run (Check Mode)

```bash
ansible-playbook -i <inventory-path> web-db.yaml -C
```

**What it does:** Simulates execution — connects to hosts, evaluates tasks, reports what *would* change — without actually making changes.

**What it does NOT guarantee:** The instructor explicitly warns: *"Don't take it as a guarantee."* Dry runs can behave differently from actual runs when runtime variables or dynamic conditions are involved. A successful dry run doesn't guarantee successful execution, and a failed dry run doesn't necessarily mean actual execution would fail.

**Recommended pre-execution workflow:**

```
1. --syntax-check   → validate YAML structure
2. -C               → dry run (simulate execution)
3. (no flag)         → actual execution
```

***

## Step 8: Navigating Ansible Module Documentation

Go to **`docs.ansible.com/ansible/latest`** → navigate to **"Using Ansible modules and plugins"** → **"Index of all modules"**.

**How to find and use a module:**

1. **Search** for the module name (e.g., search "yum")
2. Find the fully qualified name (e.g., `ansible.builtin.yum`)
3. Click to open the module documentation page
4. **Scroll to Examples** — copy-paste the playbook snippet, then modify for your use case
5. **Check Parameters** — see all available options beyond what the examples show
6. **Check Requirements** — prerequisites needed on the target machine

**Module documentation page structure:**

* Description → what the module does
* Requirements → what needs to be on the target
* Parameters → all configurable options
* Examples → ready-to-use playbook snippets

The instructor's advice: *"Learn the basic structure and learn the documentation. That's all you need to do."*

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Playbook Data Structure Hierarchy

```
PLAYBOOK (YAML file)
│
├── LIST of PLAYS
│     │
│     ├── PLAY 1 (DICTIONARY)
│     │     ├── name: "Webserver setup"         (string)
│     │     ├── hosts: webservers               (string → inventory group)
│     │     ├── become: yes                     (boolean → sudo)
│     │     └── tasks:                          (LIST of TASK DICTIONARIES)
│     │           ├── TASK 1 (DICTIONARY)
│     │           │     ├── name: "Install httpd"           (human label)
│     │           │     └── ansible.builtin.yum:            (module key)
│     │           │           ├── name: httpd               (package name)
│     │           │           └── state: present            (desired state)
│     │           │
│     │           └── TASK 2 (DICTIONARY)
│     │                 ├── name: "Start httpd service"
│     │                 └── ansible.builtin.service:
│     │                       ├── name: httpd
│     │                       ├── state: started
│     │                       └── enabled: yes
│     │
│     └── PLAY 2 (DICTIONARY)
│           ├── name: "DBserver setup"
│           ├── hosts: dbservers
│           ├── become: yes
│           └── tasks: [...]
│
DATA TYPE CHAIN:
  list → dict → list → dict → dict
  (plays) (play) (tasks) (task) (module args)
```

***

## Three Indentation Levels

```
LEVEL 1 (column 0):     Play definition    → hosts, become, tasks
LEVEL 2 (indented):     Task definition    → - name, module key
LEVEL 3 (deeper):       Module arguments   → name, state, enabled

Rule: tasks in same play = same column
Rule: second play starts back at column 0
```

***

## Ad Hoc ↔ Playbook Mapping

```
AD HOC:
  ansible webservers -m yum -a "name=httpd state=present" --become

PLAYBOOK EQUIVALENT:
  - name: Install httpd
    ansible.builtin.yum:
      name: httpd
      state: present

Same module, same arguments, different format
Ad hoc = one-off commands | Playbook = structured, repeatable, version-controlled
```

***

## Module Naming Evolution

```
OLD:     yum, service, copy
NEW:     ansible.builtin.yum, ansible.builtin.service

Structure: <namespace>.<collection>.<module>

Collections:
  ansible.builtin    →  core modules (yum, service, copy, file...)
  amazon.aws         →  AWS modules
  azure.*            →  Azure modules
  community.*        →  community-contributed
  cisco.*            →  Cisco modules
```

***

## Execution Output States

```
Gathering Facts  →  ok (always — read-only, collects target info via setup module)
Install package  →  changed (first run) | ok (second run — idempotent)
Start service    →  changed (first run) | ok (already running)

changed = Ansible modified the system
ok      = system already in desired state, no change made
```

***

## Pre-Execution Validation Flow

```
1. --syntax-check     →  validates YAML structure only
                          success: prints playbook name
                          failure: shows offending line (⚠️ line number may be inaccurate)

2. -C (dry run)       →  simulates execution without changes
                          ⚠️ NOT a guarantee of actual success
                          useful for: connection testing, flow verification

3. (actual run)       →  real execution

RULE: syntax check → dry run → execute
```

***

## Debugging Verbosity Ladder

```
-v      →  module JSON output
-vv     →  + version, config, python, LINE NUMBERS
-vvv    →  + SSH KEY used, USER used, Linux command options
-vvvv   →  maximum detail (final level)

USE -vvv FOR:
  "Wrong user? Wrong key? No sudo? Wrong module?"
  → logical errors that syntax check can't catch
```

***

## YAML Syntax Error Debugging Rule

```
⚠️ Error line number ≠ always actual error location

YAML indentation errors CASCADE:
  mistake on line 8 → reported on line 12

STRATEGY:
  1. Check reported line first
  2. If line looks correct → examine surrounding lines
  3. Verify overall list/dict/indentation structure
  4. Check column alignment of tasks within same play
```

***

## Commands Reference

```
# Remove package (ad hoc — clean slate)
ansible webservers -m ansible.builtin.yum -a "name=httpd state=absent" --become

# Execute playbook
ansible-playbook -i <inventory> web-db.yaml

# Syntax check only
ansible-playbook -i <inventory> web-db.yaml --syntax-check

# Dry run (check mode)
ansible-playbook -i <inventory> web-db.yaml -C

# Debug with verbosity
ansible-playbook -i <inventory> web-db.yaml -v    # level 1
ansible-playbook -i <inventory> web-db.yaml -vvv  # level 3 (most useful for logical errors)
```

***

## Documentation Workflow

```
docs.ansible.com/ansible/latest
  → Using Ansible modules and plugins
    → Index of all modules
      → Search module name
        → Module page:
            1. Requirements (prerequisites)
            2. Parameters (ALL options)
            3. Examples (copy-paste snippets)

RULE: "Learn the basic structure and learn the documentation. That's all you need to do."
```

***

## Reusable Engineering Pattern: Declarative Hierarchical Task Orchestration

```
PATTERN:
  PLAYBOOK     = ordered list of PLAYS         (what server groups to target)
  PLAY         = ordered list of TASKS          (what work to do on that group)
  TASK         = MODULE + ARGUMENTS             (what specific action to take)

PROPERTIES:
  - Declarative: you declare desired state, not imperative commands
  - Idempotent: safe to re-run (changed vs ok)
  - Hierarchical: play → task → module (clear scope boundaries)
  - Sequential: tasks execute top-to-bottom within a play
  - Multi-target: one playbook orchestrates multiple server groups

WHERE ELSE:
  • Kubernetes manifests: Deployment → Pod → Container (hierarchical declaration)
  • Terraform: resource blocks with arguments (declarative state)
  • Docker Compose: services → containers → config (multi-service orchestration)
  • CI/CD pipelines: stages → jobs → steps (hierarchical execution)
```

***

## One-Line Mental Reload Trigger

> *"Playbook = list of plays (each targeting a host group), play = dict with hosts/become/tasks, tasks = list of module invocations with args — three indentation levels, FQCN module names, Gathering Facts is automatic, syntax-check then dry-run (-C) then execute, -vvv for logical debugging."*

This single sentence reconstructs the full data structure, the three-level hierarchy, module naming, the hidden default task, the pre-execution validation flow, and the debugging strategy. [\[237-playbo...nd-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/237-playbook-and-modules.txt)
