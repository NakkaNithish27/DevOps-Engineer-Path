# 📦 Ansible Variables & Debug Module — Deep Learning Material

**Source:** *Variables and Debug* (Ansible Video Lecture Caption File) [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Variables in Ansible — The Same Concept, Different Locations

Variables in Ansible work exactly like variables in any other programming language or tool — Bash, Python, Jenkins. They store values that you reference by name, and when the playbook executes, Ansible substitutes the variable name with its value. What makes Ansible variables distinctive is not *what* they are, but **where** they can be defined. Ansible provides multiple locations for variable definitions, each serving a different scope and purpose. The instructor explicitly says: "There are different places where you can define variables in Ansible." [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

The locations form a hierarchy of scope, from narrowest (inside a single playbook) to broadest (available to all hosts):

**1. Inside the playbook (vars section):** You define variables directly in the playbook file using the `vars:` keyword, placed after the host configuration and before the `tasks:` section. This is the simplest method but the instructor stresses: **"it's really not a good way"** — it works for learning, but in practice, hardcoding variables inside playbooks reduces reusability. If you use the same playbook across different projects, you'd have to edit the playbook itself to change values, which defeats the purpose of variables. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**2. Group variables (group\_vars/):** You create a directory called `group_vars` and inside it, create files named after your inventory groups. A file named `all` applies variables to **every host** in the inventory. A file named after a specific group (e.g., `websrvgrp`) applies variables only to hosts in that group. This is where you define **your own custom variables** — not Ansible connection variables like `ansible_user` or `ansible_ssh_private_key_file` (those go in the inventory), but application-level variables like database names, usernames, ports, and passwords. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**3. Host variables (host\_vars/):** You create a directory called `host_vars` and inside it, create files named after specific hostnames (e.g., `web01`). Variables defined here apply **only to that specific host**. This is for host-specific overrides — when one particular server needs different values than the rest of its group.

**4. Role variables (vars/ and defaults/ inside roles):** When using Ansible roles (covered in a later lecture), each role has two directories for variables: `vars/` (high-priority role variables) and `defaults/` (low-priority default values that can be easily overridden). The instructor mentions this but defers the details: "I don't want you to memorize all this right now. We'll be doing this." [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

The progression from playbook vars → group\_vars → host\_vars → role vars represents increasing separation between **logic** (what the playbook does) and **data** (what values it uses). The best practice is maximum separation: playbooks contain tasks, variables live externally. This makes playbooks reusable across projects — you change the variable files, not the playbook code. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

🔍 **Deep Dive:**
The instructor explains **why** variables exist with a practical framing: "Things that come again and again in our scripts, in our code, or the things that might be of reusable property... I use this playbook in this project, I use it in another project, things will change. So the properties, those changes, those things we use as variable." This is the same reasoning behind variables in any language — but in Ansible's infrastructure context, the "things that change" are database names, usernames, ports, passwords, package versions, and file paths that differ between environments (dev vs. staging vs. production).

***

## 1.2 Variable Syntax — How to Reference Variables in Playbooks

When you define a variable (e.g., `dbname: electric`), referencing it inside a task requires a specific syntax: **double quotes containing double curly braces** with the variable name inside. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

```yaml
"{{ dbname }}"
```

The instructor acknowledges this is more verbose than other languages — "In Bash, we have just dollar and the variable name. Here, we have like this" — but it's the Jinja2 templating syntax that Ansible uses. The double curly braces `{{ }}` tell Ansible: "evaluate this as a variable expression, not as a literal string." The double quotes around the entire expression are required when the variable reference is the entire value of a YAML key. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## 1.3 Fact Variables — Ansible's Auto-Generated System Information

Beyond your own custom variables, Ansible automatically generates a large set of variables called **fact variables** (or just "facts"). These are system-level information about each target host — operating system family, CPU cores, kernel version, connected devices, IP addresses, MAC addresses, architecture (32-bit vs. 64-bit), and many more. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**How facts are generated:** When you execute a playbook, the **very first task** that runs (before any of your defined tasks) is called **"Gathering Facts."** This implicit task runs the **setup module** on each target host. The setup module collects all the system information and stores it as variables that you can use throughout the rest of the playbook. You don't need to explicitly run the setup module — it happens automatically. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**Examples of fact variables:**

* `ansible_os_family` — the OS family (e.g., "RedHat", "Debian")
* `ansible_processor_cores` — number of CPU cores
* `ansible_kernel` — kernel version
* `ansible_devices` — connected device information
* `ansible_default_ipv4` — default IPv4 info (MAC address, gateway, IP)
* `ansible_architecture` — system architecture (x86\_64, i386, etc.)

**How facts are used:** You can use fact variables to make decisions in playbooks. For example: if the architecture is 64-bit, install one package; if 32-bit, install a different package. Or: insert the correct IP address into a configuration file template based on the target host's actual IP. Facts turn your playbooks from static scripts into **adaptive automation** that behaves correctly across different hosts with different characteristics. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

🔍 **Deep Dive:**
The Gathering Facts task is why you sometimes see a delay at the beginning of playbook execution before any of your tasks start. Ansible is SSHing into each target host, running the setup module, collecting all system information, and storing it as variables. On large inventories with many hosts, this can add significant time. You can disable fact gathering (`gather_facts: no`) if your playbook doesn't need host information, but for most playbooks, the facts are essential.

***

## 1.4 Register Variables — Capturing Task Output at Runtime

The third category of variables is **register variables** — variables created at runtime by capturing the output of a task. Every Ansible module, when it executes, returns output in **JSON format** (as covered in the YAML/JSON lecture). By default, this output is suppressed — you see Ansible's formatted status messages (ok, changed, failed), not the raw JSON. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

The `register` keyword lets you capture that JSON output into a variable. You place `register:` at the same indentation level as the module name, followed by a variable name of your choice. After the task executes, the variable holds the complete JSON output from that module. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

```yaml
- name: Create database
  mysql_db:
    name: "{{ dbname }}"
  register: dbout
```

Now `dbout` contains the full JSON response from the `mysql_db` module — including whether it changed anything, any error messages, and module-specific return values.

**Why this matters:** Subsequent tasks may need information from previous tasks to make decisions. For example: "Did the previous task actually change something? If yes, restart the service. If no, skip the restart." Or: "What was the output of that command? Parse it and use a value from it in the next task." The register variable is the mechanism that chains tasks together with data flow — without it, each task is isolated and blind to what happened before. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

The instructor notes that the register variable stores **only the exit/return data** from the module, not the visual output you see on screen. The stored data is the structured JSON that includes keys like `changed`, `failed`, and module-specific data.

***

## 1.5 The Debug Module — Ansible's Print Function

The `debug` module is Ansible's equivalent of `echo` in Bash or `print()` in Python. It outputs information to the screen during playbook execution. It has two primary modes: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**Mode 1: `var` — Print a variable's value directly.** You pass just the variable name (no curly braces needed):

```yaml
- debug:
    var: dbname
```

This prints the variable name and its value. Note: with `var`, you do **not** use the `{{ }}` syntax — you give the raw variable name.

**Mode 2: `msg` — Print a custom message with embedded variables.** You write a message string with variables in `{{ }}` syntax:

```yaml
- debug:
    msg: "The DB name is {{ dbname }}"
```

This prints the full message with the variable value substituted.

The instructor emphasizes that debug is primarily a **troubleshooting tool** — hence the name "debug." In normal operation, you don't need to print messages from a playbook because Ansible's output is already verbose. If you name your tasks properly, the task names serve as progress messages. Debug is for when something isn't working as expected and you need to inspect variable values or task outputs to diagnose the problem. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## 1.6 Task Naming — Two Syntax Styles

The instructor demonstrates two equivalent ways to write a task: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**Style 1: Module directly after hyphen**

```yaml
- debug:
    var: dbname
```

**Style 2: Named task with module on next line**

```yaml
- name: Print DB out variable
  debug:
    var: dbout
```

Both are valid. Style 2 is preferred in practice because the `name` field provides a human-readable description that appears in the playbook output during execution, making it easier to understand what each task does. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## 1.7 Verbose Mode — Seeing What Ansible Actually Does

When running a playbook normally, Ansible shows summarized output — task names and status (ok, changed, failed). If you need to see the **detailed internal execution** — what values were actually used, what commands were sent, what the full module response was — you use the **verbose flag**: `-vv` (or `-v`, `-vvv`, `-vvvv` for increasing verbosity levels). [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

The instructor uses `-vv` to verify that variables were correctly substituted: "We see here, DB electric, user current." Without verbose mode, the playbook just reports "changed" without showing what values were used. With `-vv`, you can see the actual parameters that were sent to each module. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are modifying an existing Ansible playbook to use variables instead of hardcoded values, learning to define variables inside the playbook, use them in tasks, print them with the debug module, and capture task output into register variables. After this, the playbook will be parameterized — changing behavior requires only changing variable values, not editing task definitions. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## Step 1: Set Up the Exercise Directory

Copy the previous exercise to a new directory:

```bash
cp -r exercise7 exercise8
cd exercise8
```

This preserves the previous exercise and gives us a clean working copy to modify. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## Step 2: Define Variables Inside the Playbook

Open the playbook file (e.g., `db.yaml`) in a text editor.

Add the `vars:` section **after the host configuration** and **before the `tasks:` section**: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

```yaml
vars:
  dbname: electric
  dbuser: current
  dbpass: tesla
```

**Placement is critical:** The `vars:` keyword must be at the same indentation level as `hosts:` and `tasks:` — it's part of the play-level declaration, not inside a task.

**What we defined:**

* `dbname` — the database name (`electric`)
* `dbuser` — the database username (`current`)
* `dbpass` — the database password (`tesla`)

These are YAML key-value pairs in dictionary format under the `vars:` key. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

⚠️ **Expert Note:**
The instructor explicitly notes: defining variables inside the playbook is "really not a good way" for production. It works for learning, but in practice, variables should be defined externally (group\_vars, host\_vars) so playbooks remain reusable across projects. The next lecture covers external variable definitions.

***

## Step 3: Replace Hardcoded Values with Variable References

Find the tasks that use hardcoded database name, username, and password values. Replace them with variable references using the `{{ }}` syntax: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

```yaml
- name: Create database
  mysql_db:
    name: "{{ dbname }}"
    state: present
    login_user: "{{ dbuser }}"
    login_password: "{{ dbpass }}"
```

**Syntax rules:**

* The entire value must be in **double quotes**: `"{{ dbname }}"`
* Inside the quotes, use **two opening curly braces `{{`** and **two closing curly braces `}}`**
* The variable name goes **inside** the curly braces with spaces: `{{ dbname }}` (spaces around the variable name are conventional for readability) [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**Common mistake:** Forgetting the double quotes. In YAML, if a value starts with `{`, YAML interprets it as a dictionary. The double quotes tell YAML: "this is a string, not a YAML dictionary."

Save the file (`Ctrl+S` or `:wq` in vim).

***

## Step 4: Run the Playbook and Verify with Verbose Mode

```bash
ansible-playbook db.yaml
```

**Expected output:** Tasks execute and show `changed` or `ok` status. But the output doesn't show **what values** were actually used — you can't confirm the variables were substituted correctly from the default output. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**Run with verbose mode to verify:**

```bash
ansible-playbook db.yaml -vv
```

* `-vv` — double verbose; shows the actual parameters sent to each module

**What to look for in the verbose output:** The database name (`electric`), username (`current`), and password should appear in the module invocation details. If you see `DB electric` and `User current` in the output, the variables were substituted correctly. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## Step 5: Add Debug Tasks to Print Variables

Open the playbook and add debug tasks to print the variable values. Two methods: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**Method 1: Using `var` — prints the variable name and its value:**

```yaml
- debug:
    var: dbname
```

Note: with `var`, use the **raw variable name** — no `{{ }}`, no double quotes around the variable name. The `var` parameter expects a variable name, not a Jinja2 expression. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**Method 2: Using `msg` — prints a custom message with embedded variables:**

```yaml
- name: Print dbuser
  debug:
    msg: "The DB user is {{ dbuser }}"
```

With `msg`, the value is a string, so you **must** use the `{{ }}` syntax to embed variables. This is the same syntax used in task parameters. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

Save and run the playbook:

```bash
ansible-playbook db.yaml
```

**Expected output:** The debug tasks produce visible output in the playbook run: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

For the `var` method:

```
ok: [db01] => {
    "dbname": "electric"
}
```

For the `msg` method:

```
ok: [db01] => {
    "msg": "The DB user is current"
}
```

**Key difference between var and msg:**

* `var` outputs the variable name as a key with its value — clean, minimal, useful for quick inspection
* `msg` outputs a custom message string — useful when you want context around the value [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## Step 6: Register Task Output and Print It

Add the `register` keyword to an existing task to capture its JSON output: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

```yaml
- name: Create database
  mysql_db:
    name: "{{ dbname }}"
    state: present
  register: dbout
```

**Placement:** `register:` must be at the **same indentation level as the module name** (not inside the module's parameters). It's a task-level directive, not a module parameter.

* `register: dbout` — stores the complete JSON output of this task into a variable named `dbout`

**Add a debug task to print the registered variable:**

```yaml
- name: Print DB out variable
  debug:
    var: dbout
```

Save and run: [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

```bash
ansible-playbook db.yaml
```

**Expected output:** The last debug task prints the full JSON output from the `mysql_db` module. This includes keys like `changed` (boolean — whether the module made a modification) and any module-specific return data. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

**What to observe:** If the database was already created from a previous run, `changed` will be `false` (the module detected the database already exists and didn't modify anything). If you run it fresh, `changed` will be `true` (the module created the database). This is the same idempotency pattern seen in Python OS automation and referenced in the YAML/JSON lecture's `changed` key explanation.

**Troubleshooting use:** When a task behaves unexpectedly, register its output and print it with debug. The full JSON response often reveals exactly why the task succeeded, failed, or reported `changed` when you didn't expect it. [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

## Summary of the Playbook Structure After All Modifications

```yaml
hosts: dbsrvgrp
become: yes
vars:
  dbname: electric
  dbuser: current
  dbpass: tesla
tasks:
  - debug:
      var: dbname
  - name: Print dbuser
    debug:
      msg: "The DB user is {{ dbuser }}"
  - name: Create database
    mysql_db:
      name: "{{ dbname }}"
      state: present
      login_user: "{{ dbuser }}"
      login_password: "{{ dbpass }}"
    register: dbout
  - name: Print DB out variable
    debug:
      var: dbout
```

 [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Variable Categories in Ansible

```
1. CUSTOM VARIABLES (you define)
   ├─ In playbook: vars: section (simple but NOT best practice)
   ├─ group_vars/all → applies to ALL hosts
   ├─ group_vars/<groupname> → applies to specific group
   ├─ host_vars/<hostname> → applies to specific host
   └─ Roles: vars/ and defaults/ directories

2. FACT VARIABLES (auto-generated)
   ├─ Generated by: setup module
   ├─ Triggered by: "Gathering Facts" task (runs first, automatically)
   ├─ Contains: OS family, CPU cores, kernel, IPs, architecture, devices
   └─ Used for: conditional logic, config file templates

3. REGISTER VARIABLES (runtime capture)
   ├─ Created by: register: keyword on a task
   ├─ Contains: full JSON output of the module
   ├─ Used for: decision-making in subsequent tasks, debugging
   └─ Printed with: debug module
```

## Variable Definition Locations — Scope Hierarchy

```
NARROWEST SCOPE:
  host_vars/<hostname>     → one specific host only
  ↓
  group_vars/<groupname>   → all hosts in one group
  ↓
  group_vars/all           → all hosts in inventory
  ↓
  playbook vars: section   → within the playbook only
  ↓
BROADEST SCOPE:
  role defaults/           → lowest priority, easily overridden
```

## Variable Reference Syntax

```
IN TASKS (Jinja2 syntax):
  "{{ variable_name }}"
  Double quotes + double curly braces

IN DEBUG var:
  var: variable_name
  Raw name — NO {{ }}, NO quotes

IN DEBUG msg:
  msg: "Text {{ variable_name }} more text"
  {{ }} inside double-quoted string
```

## Debug Module — Two Modes

```
MODE 1: var (print raw variable)
  - debug:
      var: dbname
  Output: {"dbname": "electric"}

MODE 2: msg (print custom message)
  - debug:
      msg: "The DB name is {{ dbname }}"
  Output: {"msg": "The DB name is electric"}

Purpose: troubleshooting ONLY ("that's why it's called debug")
         not needed in normal playbook operation
```

## Register Mechanism

```
- name: task name
  module_name:
    param: value
  register: variable_name     ← SAME indentation as module
                                 stores JSON output into variable

- name: print it
  debug:
    var: variable_name         ← prints full JSON output

register captures: changed, failed, module-specific return data
```

## Fact Variables — Auto-Collection Flow

```
Playbook starts
  → FIRST TASK: "Gathering Facts" (implicit, automatic)
    → Runs setup module on each target host
      → Collects: OS, CPU, kernel, IPs, architecture, devices
        → Stores as variables: ansible_os_family, ansible_processor_cores, etc.
          → Available to ALL subsequent tasks in the play

Disable with: gather_facts: no (if not needed)
```

## Fact Variable Examples

```
ansible_os_family           → "RedHat" / "Debian"
ansible_processor_cores     → number of CPU cores
ansible_kernel              → kernel version
ansible_devices             → connected devices
ansible_default_ipv4        → MAC, gateway, IP
ansible_architecture        → "x86_64" / "i386"
```

## Verbose Mode for Variable Verification

```
ansible-playbook db.yaml        → summarized output (task status only)
ansible-playbook db.yaml -vv    → shows actual values sent to modules

Use -vv to verify: variable substitution happened correctly
                   correct values reached the module
```

## Playbook Structure with Variables

```
hosts: <group>
become: yes
vars:                          ← play-level, before tasks
  dbname: electric
  dbuser: current
  dbpass: tesla
tasks:
  - debug:                     ← print variable (var mode)
      var: dbname
  - name: Print user           ← print variable (msg mode)
    debug:
      msg: "{{ dbuser }}"
  - name: Create DB            ← use variables in task
    mysql_db:
      name: "{{ dbname }}"
    register: dbout             ← capture output
  - name: Print output          ← print captured output
    debug:
      var: dbout
```

## Best Practice Progression

```
LEARNING:    vars: inside playbook (quick, simple, coupled)
PRODUCTION:  group_vars/ and host_vars/ (separated, reusable)

WHY: "I use this playbook in this project,
      I use it in another project, things will change"
      → external variables → change data, not logic
```

## Reusable Engineering Patterns

**1. Logic/Data Separation**

```
Playbook = LOGIC (what to do)
Variables = DATA (with what values)

Separation enables: reuse playbook across projects
                    change values without editing logic
                    environment-specific configs (dev/staging/prod)

Same pattern: Terraform variables, Docker ENV, Helm values.yaml
```

**2. Three Sources of Runtime Data**

```
1. Declared (you define):     vars, group_vars, host_vars
2. Discovered (auto-collected): fact variables from setup module
3. Captured (runtime output):   register variables from task execution

Together: declared + discovered + captured = full data context
Same pattern: Terraform (variables + data sources + outputs)
```

**3. Debug as Inspection Layer**

```
Normal execution: module output suppressed (status only)
Debug mode: inject debug tasks to inspect variable values
Verbose mode: -vv to see actual parameters sent to modules

Debugging = making the invisible visible
Same pattern: print debugging in any language,
              terraform plan output, docker inspect
```

***

*This completes the full reconstruction. Theory explains the three categories of Ansible variables and where each can be defined. Practical walks through defining, referencing, printing, and registering variables step by step. The Compression Map enables instant recall of variable syntax, the scope hierarchy, and the debug/register mechanisms.* [\[240-variab...-and-debug \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/240-variables-and-debug.txt)
