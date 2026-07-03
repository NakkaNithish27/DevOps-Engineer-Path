# 🧠 Ansible Fact Variables — Runtime System Discovery & Data Access Patterns

**Source:** *242. Fact Variables* — Ansible Automation Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Are Fact Variables and Why Do They Exist?

When Ansible connects to a target machine to execute tasks, it often needs to know things about that machine — what operating system is it running? How much RAM does it have? What's its IP address? What processor architecture does it use? You could manually define all this information in variables, but that's fragile, tedious, and quickly goes out of date. Instead, Ansible has a mechanism to **automatically discover this information at runtime**: **fact variables**.

Fact variables are **runtime variables** — they don't exist in any file you write. They are generated dynamically every time a playbook runs, by a module called **`setup`**. This module connects to the target machine, collects a comprehensive inventory of system information, and stores it as a structured data object (a giant JSON dictionary) that your playbook can reference during execution. The data lives only in memory for the duration of the play — it's not saved to disk anywhere by default.

Examples of what fact variables contain: **operating system name** (`ansible_distribution`), **processor cores**, **kernel version**, **connected devices**, **IP address**, **MAC address**, **system architecture**, **date and time**, **BIOS information**, **memory details**. It's essentially a complete system profile, automatically generated.

***

## 1.2 The Setup Module and Gathering Facts — The Hidden First Task

As covered in the previous playbook lecture, every play in an Ansible playbook automatically executes a **"Gathering Facts"** task as the very first step before any user-defined tasks run. This gathering facts task is the `setup` module running behind the scenes. It connects to every host in the play's target group, collects all system information, and makes it available as variables for the rest of the play.

The instructor connects this directly: *"Gathering facts executes a module called setup. This module collects information about the host in JSON format. And it's only in the runtime."* The data exists purely in memory during the playbook run — Ansible doesn't persist it to a file or database unless you explicitly tell it to.

The `setup` module can also be run **manually** via an ad hoc command: `ansible -m setup web01`. This produces the full JSON output of all fact variables for that host, which is invaluable for discovering what variables are available and what their exact names are.

***

## 1.3 Disabling Gathering Facts — When and Why

If your playbook doesn't use any fact variables, the gathering facts step is wasted time — it adds a network round-trip and processing delay for every host in the play. You can disable it by adding `gather_facts: false` to the play definition (at the same level as `hosts:` and `tasks:`).

When gathering facts is disabled, the setup module does not execute, and **no fact variables are available**. If your tasks try to reference a fact variable (like `ansible_distribution`), the playbook will fail with a **"variable is not defined"** error. The instructor demonstrates this explicitly: disabling gathering facts and then trying to print `ansible_distribution` produces an error because the variable was never populated.

The decision is simple: if you use fact variables → leave gathering facts enabled (the default). If you don't use them → disable for performance.

***

## 1.4 The Fact Data Structure — A Giant Nested Dictionary

The output of the setup module is a **large JSON dictionary**. Understanding its structure is essential for accessing the right values. The top-level key is `ansible_facts`, whose value is another dictionary containing all the individual fact variables. Within this dictionary:

* Some values are **strings**: `ansible_distribution: "CentOS"` or `ansible_distribution: "Ubuntu"`
* Some values are **lists** (square brackets): `ansible_processor: ["0", "GenuineIntel", "Intel(R) Xeon(R) ..."]`
* Some values are **nested dictionaries** (curly braces): `ansible_memory_mb: { "real": { "free": 345, "total": 983, ... }, ... }`

The instructor emphasizes a common source of confusion: *"Here the word 'ansible' does not mean the Ansible control machine. This is all information about web01."* Every fact variable prefixed with `ansible_` refers to the **target machine**, not the machine running Ansible.

***

## 1.5 Accessing Fact Variables — Three Data Access Patterns

The way you access a fact variable depends on its **data type** in the JSON structure. The lecture teaches three distinct patterns:

### Pattern 1: Direct String Access

For fact variables whose value is a simple string, you reference them directly by name:

```yaml
var: ansible_distribution
```

This returns the value directly — e.g., `CentOS` or `Ubuntu`.

### Pattern 2: Nested Dictionary Access (Dot Notation)

For fact variables whose value is a nested dictionary, you chain keys using **dot notation** to drill into the structure:

```yaml
var: ansible_memory_mb.real.free
```

This navigates: `ansible_memory_mb` (dictionary) → `real` (nested dictionary) → `free` (final value). The instructor walks through this carefully: *"Free was the string, but it was inside the dictionary real. And that dictionary was inside the dictionary ansible\_memory\_mb."*

### Pattern 3: List Element Access (Square Bracket Index)

For fact variables whose value is a list, you use **square bracket indexing** to access specific elements:

```yaml
var: ansible_processor[2]
```

This accesses the element at position 2 (zero-indexed) in the `ansible_processor` list. In the video's example, position 0 is `"0"`, position 1 is `"GenuineIntel"`, and position 2 is the processor name string (e.g., `"Intel(R) Xeon(R) ..."`).

> 🔍 **Deep Dive:** These three access patterns mirror standard data structure traversal in any programming language. The fact that Ansible uses the same dot-notation and bracket-indexing syntax as Python (and JSON path navigation) makes the mental model transferable. If you can navigate a Python dictionary or a JSON object, you can navigate Ansible facts. The key skill is running `ansible -m setup <host>` first to see the raw structure, then constructing the correct access path from it.

***

## 1.6 The Debug Module — Printing Variables During Execution

To inspect fact variable values during a playbook run, you use the **`debug`** module. In this lecture, the `debug` module is used with the `var:` argument to print the value of a specified variable. This is Ansible's equivalent of a `print()` statement — it outputs a variable's value in the playbook execution log.

The `debug` module is purely for inspection and troubleshooting. It doesn't change anything on the target machine. It's used here to verify that fact variables contain the expected values and to demonstrate the data access patterns.

***

## 1.7 Multi-OS Inventory and Variable Precedence in Practice

The lecture introduces a practical scenario that demonstrates both fact variables and **variable precedence** (from a previous lecture). The instructor adds a new EC2 instance running **Ubuntu** (`web03`) alongside the existing CentOS instances (`web01`, `web02`).

When pinging `web03`, the connection fails with **"permission denied."** The cause: the global variable for the SSH user is set to the CentOS default user, but Ubuntu instances use the `ubuntu` username. The ping fails because Ansible tries to connect with the wrong user.

The fix leverages **host variable precedence**: host-level variables take **higher priority** than global (group-level) variables. By defining the SSH user specifically for `web03` in the inventory file (as a host variable), it overrides the global setting. The instructor reinforces the precedence rule: *"Host variable takes higher priority. It'll check first whether the host has those values or not. If it's not, then only it'll go for global."*

Once the host variable is set correctly, pinging succeeds, and running the `print_facts` playbook shows the practical power of fact variables: the same `ansible_distribution` variable automatically returns `CentOS` for `web01`/`web02` and `Ubuntu` for `web03`. The fact variables are **host-specific** — each host's facts reflect its own system, collected independently by the setup module.

***

## 1.8 Use Cases for Fact Variables — What They Enable

The instructor outlines several practical applications of fact variables, positioning them as the bridge to more advanced Ansible capabilities:

**Conditional task execution** — Check whether RAM is free before deciding whether a task should run. Check the OS distribution to install the right package (`yum` for CentOS, `apt` for Ubuntu). Decision-making based on runtime facts is covered in the next lecture.

**File operations** — Use date/time facts (`ansible_date_time`) to name backup files with timestamps. Push system-specific content into configuration files.

**Dynamic configuration** — Adapt playbook behavior to each host's actual characteristics rather than hardcoding assumptions. This is what makes a single playbook work across heterogeneous infrastructure.

> ⚠️ **Expert Note:** Fact variables are the foundation of **writing OS-agnostic playbooks**. Without them, you'd need separate playbooks for CentOS and Ubuntu (different package managers, different service names, different paths). With fact variables and conditional logic, a single playbook can detect the OS and choose the right module and package names automatically. This is the standard approach in production Ansible automation.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are exploring **Ansible fact variables** — learning how to view them, access their values from different data structures (strings, dictionaries, lists), and print them during playbook execution. We also add an Ubuntu instance to our inventory to see fact variables working across different operating systems.

**Final outcome:** A working `print_facts.yaml` playbook that prints OS name, RAM information, and processor name from automatically collected system facts, running successfully against both CentOS and Ubuntu hosts.

***

## Step 1: Observe Gathering Facts in Action

Navigate to your exercise directory on the control machine:

```bash
cd vprofile/exercise9
```

Run any existing playbook (the instructor uses `vars_precedence` from the previous lecture):

```bash
ansible-playbook vars_precedence.yaml
```

**Observe:** The first task in the output is always **"Gathering Facts"** with status `ok`. This is the setup module running automatically.

***

## Step 2: Disable Gathering Facts (Demonstration)

Open the playbook and add `gather_facts: false` just before the `tasks:` key, at the same indentation level:

```yaml
- name: Some play
  hosts: all
  gather_facts: false
  tasks:
    ...
```

Run the playbook again. **Observe:** The "Gathering Facts" task is gone from the output. If any task references a fact variable, it will fail with **"variable is not defined."**

Re-enable by commenting out with `#`:

```yaml
  # gather_facts: false
```

**Connection to flow:** This demonstrates that fact variables only exist when gathering facts runs. Keep it enabled for the rest of this exercise.

***

## Step 3: Run the Setup Module Manually via Ad Hoc Command

```bash
ansible -m setup web01
```

**Command breakdown:**

* `ansible` — ad hoc command
* `-m setup` — use the setup module
* `web01` — target host

**Expected output:** A massive JSON dictionary containing all system information about `web01`. Scroll through it to observe:

* `ansible_architecture` — system architecture (e.g., `x86_64`)
* `ansible_bios_date` — BIOS date
* `ansible_date_time` — full date/time dictionary
* `ansible_distribution` — OS name (e.g., `CentOS`)
* `ansible_memory_mb` — memory dictionary with nested `real` and `swap` sub-dictionaries
* `ansible_processor` — list of processor information strings

**Why this matters:** This is your **reference command** for discovering variable names. Before using any fact variable in a playbook, run `ansible -m setup <host>` and find the exact variable name and its data type (string, dict, list).

***

## Step 4: Create the print\_facts.yaml Playbook

Create a new file:

```yaml
---
- name: Print facts
  hosts: all
  tasks:
    - name: Print OS name
      debug:
        var: ansible_distribution
```

**Structure notes:**

* `hosts: all` — targets every host in inventory (so we see facts from all machines)
* `debug` module with `var:` argument — prints the value of the specified variable
* `ansible_distribution` — the fact variable for the OS name (verify spelling by checking setup module output)

***

## Step 5: Execute and Verify OS Name Printing

```bash
ansible-playbook print_facts.yaml
```

**Expected output:**

```
TASK [Gathering Facts] ****
ok: [web01]
ok: [web02]

TASK [Print OS name] ****
ok: [web01] => {
    "ansible_distribution": "CentOS"
}
ok: [web02] => {
    "ansible_distribution": "CentOS"
}
```

Each host shows its own OS distribution value. Gathering facts runs first (populating the variables), then the debug task prints them.

**Failure test:** If you add `gather_facts: false` and rerun, the "Print OS name" task fails with `"ansible_distribution is not defined"`. This confirms the dependency: no gathering facts → no fact variables.

***

## Step 6: Add an Ubuntu Instance to the Inventory

### 6a: Launch the EC2 Instance

In the **AWS EC2 Console** → **Launch Instance**:

| Field          | Value                                     |
| -------------- | ----------------------------------------- |
| Name           | `vprofile-web03`                          |
| AMI            | **Ubuntu 22**                             |
| Instance type  | `t3.micro`                                |
| Key pair       | Same client key used for other instances  |
| Security group | Select existing **client security group** |

Click **Launch Instance**.

### 6b: Update the Inventory File

Copy the private IP of the new instance. Open your inventory file and add `web03`:

```ini
web03 ansible_host=<web03-private-ip>
```

Add `web03` to the webservers group:

```ini
[webservers]
web01 ansible_host=...
web02 ansible_host=...
web03 ansible_host=...
```

***

## Step 7: Fix the SSH User for Ubuntu — Host Variable Precedence

Test connectivity:

```bash
ansible -m ping all
```

**Expected failure for web03:** `"Failed to connect to host, permission denied."` The global variable sets the SSH user to the CentOS default, but Ubuntu AMIs require the `ubuntu` username.

**Fix:** Add a **host variable** for `web03` in the inventory file:

```ini
web03 ansible_host=<ip> ansible_user=ubuntu
```

This host-level variable **overrides** the global/group-level user variable (host variable precedence — covered in the previous lecture).

**Verify:**

```bash
ansible -m ping all
```

**Expected:** All hosts return `SUCCESS`, including `web03`.

***

## Step 8: Verify Multi-OS Fact Variables

Run the print\_facts playbook again:

```bash
ansible-playbook print_facts.yaml
```

**Expected output for the "Print OS name" task:**

```
ok: [web01] => { "ansible_distribution": "CentOS" }
ok: [web02] => { "ansible_distribution": "CentOS" }
ok: [web03] => { "ansible_distribution": "Ubuntu" }
```

The **same variable** (`ansible_distribution`) returns **different values** for different hosts — because fact variables are collected per-host by the setup module. This is the power of facts: a single playbook adapts to heterogeneous infrastructure automatically.

***

## Step 9: Access Nested Dictionary Values — RAM Memory

Run setup again to find the variable structure:

```bash
ansible -m setup web01
```

Find `ansible_memory_mb` in the output — it's a dictionary containing a `real` sub-dictionary, which contains a `free` key.

Add a new task to the playbook:

```yaml
    - name: Print RAM
      debug:
        var: ansible_memory_mb.real.free
```

**Dot notation breakdown:** `ansible_memory_mb` → enters the top dictionary → `.real` → enters the nested dictionary → `.free` → gets the value (a number representing free RAM in MB).

Execute:

```bash
ansible-playbook print_facts.yaml
```

**Expected:** Each host prints its free RAM value (a number like `345`, varying per host).

***

## Step 10: Access List Elements — Processor Name

Find `ansible_processor` in the setup output — it's a **list** with elements at positions 0, 1, 2:

* `[0]` → typically `"0"` (processor index)
* `[1]` → typically `"GenuineIntel"` (vendor)
* `[2]` → the processor model name string

Add a new task:

```yaml
    - name: Print processor name
      debug:
        var: ansible_processor[2]
```

**Square bracket notation:** `ansible_processor[2]` accesses the element at index 2 (zero-based) in the list.

Execute:

```bash
ansible-playbook print_facts.yaml
```

**Expected:** Each host prints its processor model name string.

***

## The Complete print\_facts.yaml Playbook

```yaml
---
- name: Print facts
  hosts: all
  # gather_facts: false
  tasks:
    - name: Print OS name
      debug:
        var: ansible_distribution

    - name: Print RAM
      debug:
        var: ansible_memory_mb.real.free

    - name: Print processor name
      debug:
        var: ansible_processor[2]
```

> ⚠️ **Expert Note:** The instructor frames this as a **discovery exercise**: *"Try to print different variables, values. Try to access them, print them. This is a very good exercise."* The real skill isn't memorizing variable names — it's the workflow: run `ansible -m setup <host>` → find the variable → identify its type (string/dict/list) → construct the correct access path → use it in your playbook.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Fact Variable System Architecture

```
PLAYBOOK EXECUTION
  │
  ├── PLAY starts
  │     │
  │     ├── [AUTO] Gathering Facts (setup module)
  │     │     │
  │     │     ├── Connects to EACH host in play's target group
  │     │     ├── Collects ALL system info → JSON dictionary
  │     │     ├── Stores in MEMORY only (runtime, not persisted)
  │     │     └── Variables available for ALL subsequent tasks in this play
  │     │
  │     └── TASKS execute (can reference fact variables)
  │
  └── gather_facts: false → setup module SKIPPED → NO fact variables → NameError if referenced
```

***

## Three Data Access Patterns

```
TYPE 1: STRING (direct access)
  ansible_distribution                         →  "CentOS" or "Ubuntu"

TYPE 2: NESTED DICTIONARY (dot notation)
  ansible_memory_mb.real.free                  →  345
  ├── ansible_memory_mb   (dict)
  │     └── real          (dict)
  │           └── free    (value)

TYPE 3: LIST (bracket index, zero-based)
  ansible_processor[2]                         →  "Intel(R) Xeon(R) ..."
  ├── [0] = "0"
  ├── [1] = "GenuineIntel"
  └── [2] = processor name string
```

***

## Fact Variable Discovery Workflow

```
1. ansible -m setup <host>        →  see ALL available variables + structure
2. Find target variable            →  note exact name + data type
3. Construct access path:
     string → direct name
     dict   → dot.notation.chain
     list   → name[index]
4. Use in playbook via debug module (var: <access_path>)
5. Later: use in conditions, templates, file names, etc.
```

***

## Key Fact Variables (From This Lecture)

```
ansible_distribution          →  OS name (CentOS, Ubuntu, etc.)
ansible_architecture          →  system arch (x86_64)
ansible_date_time             →  dict: date/time info (useful for backup naming)
ansible_memory_mb             →  dict: { real: { free, total }, swap: {...} }
ansible_processor             →  list: [index, vendor, model_name]
ansible_bios_date             →  BIOS date string
ansible_devices               →  connected devices
```

***

## Multi-OS Host Variable Precedence Demo

```
PROBLEM:
  Global SSH user = centos_user
  web03 is Ubuntu → needs user "ubuntu"
  → ping fails: "permission denied"

SOLUTION:
  Host variable for web03: ansible_user=ubuntu
  Host var OVERRIDES global var

PRECEDENCE RULE:
  host variable > group variable > global variable

RESULT:
  web01/web02 → use global user (CentOS)
  web03       → use host variable "ubuntu" (Ubuntu)
```

***

## Gathering Facts Control

```
DEFAULT:     gather_facts: true (implicit)
             → setup module runs → fact variables populated

DISABLED:    gather_facts: false
             → setup module SKIPPED → fact variables UNDEFINED
             → any task referencing fact var → ERROR: "variable is not defined"

WHEN TO DISABLE:
  Playbook doesn't use any fact variables → skip for performance
```

***

## Fact Variables Are Host-Specific

```
Same variable, different hosts, different values:

ansible_distribution:
  web01 → "CentOS"
  web02 → "CentOS"
  web03 → "Ubuntu"

WHY: setup module runs independently on EACH host
     collects THAT host's system info
     stores separately per host
```

***

## Debug Module Usage Pattern

```yaml
- name: <descriptive task name>
  debug:
    var: <fact_variable_access_path>

# Prints variable value in playbook output
# Read-only — no changes to target machine
# Used for: inspection, verification, troubleshooting
```

***

## Commands Reference

```bash
# Run setup module manually (discover all fact variables)
ansible -m setup web01

# Run playbook with fact printing
ansible-playbook print_facts.yaml

# Test connectivity after adding new host
ansible -m ping all
```

***

## Complete Playbook Structure

```yaml
---
- name: Print facts
  hosts: all
  # gather_facts: false    ← uncomment to disable (breaks fact variable access)
  tasks:
    - name: Print OS name
      debug:
        var: ansible_distribution                    # string access

    - name: Print RAM
      debug:
        var: ansible_memory_mb.real.free              # nested dict access

    - name: Print processor name
      debug:
        var: ansible_processor[2]                     # list index access
```

***

## Use Cases (Bridge to Next Lectures)

```
CONDITIONAL EXECUTION:
  "if ansible_distribution == 'Ubuntu' → use apt module"
  "if ansible_distribution == 'CentOS' → use yum module"
  "if ansible_memory_mb.real.free < 100 → skip heavy task"

FILE OPERATIONS:
  "name backup as backup_{{ ansible_date_time.date }}.tar.gz"

DYNAMIC CONFIG:
  "push host-specific IP/OS info into config templates"

→ Decision-making (conditions) covered in NEXT lecture
```

***

## Reusable Engineering Pattern: Runtime System Introspection

```
PATTERN:
  Before executing work on a target system,
  AUTOMATICALLY DISCOVER the system's properties at runtime.
  Store as structured data. Use for conditional decisions.

COMPONENTS:
  Discovery agent  → setup module (runs on target)
  Data format      → JSON (nested dicts + lists)
  Storage          → runtime memory (not persisted)
  Access syntax    → dot notation (dicts) + bracket index (lists)
  Trigger          → automatic (gather_facts) or manual (ad hoc -m setup)

WHY:
  Targets are heterogeneous (different OS, different hardware)
  Hardcoding assumptions breaks across environments
  Runtime discovery → adaptive automation

WHERE ELSE:
  • Terraform data sources (discover existing infrastructure before provisioning)
  • Kubernetes node labels / pod environment detection
  • Cloud-init metadata service (EC2 instance identity)
  • Docker container environment inspection
  • Monitoring agents (Prometheus node_exporter → system metrics)
```

***

## Failure Signature Index

```
"variable is not defined"                    → gather_facts disabled or variable name misspelled
Permission denied on new host                → wrong SSH user; fix with host variable override
Setup module returns empty/error             → connectivity issue to target host
Dot notation returns error                   → wrong key name in nested dict; verify via -m setup
List index out of range                      → index exceeds list length; check via -m setup
```

***

## One-Line Mental Reload Trigger

> *"Setup module auto-collects host info as JSON facts at play start — access strings directly, dicts with dot notation, lists with \[index] — disable with gather\_facts: false, discover names with ansible -m setup, host vars override globals for multi-OS inventory."*

This single sentence reconstructs the entire system: what generates facts, when it runs, the data structure, all three access patterns, how to disable, how to discover, and the variable precedence lesson from the multi-OS scenario. [\[242-fact-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/242-fact-variables.txt)
