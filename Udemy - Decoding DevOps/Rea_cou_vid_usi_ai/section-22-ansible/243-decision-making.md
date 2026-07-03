# 🎓 Deep Learning Material: Ansible Decision Making — Conditional Task Execution with `when` for Multi-OS Provisioning

**Source:** Video lecture on Ansible playbook conditionals and decision making (from [243-decision-making.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt?EntityRepresentationId=a86881bb-035d-480f-9265-d29f1ae4ddf8) caption file) [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Video Context:** This lecture begins a new exercise series focused on **server provisioning** — setting up the NTP (Network Time Protocol) service across multiple operating systems (CentOS and Ubuntu). The core problem is that different OS families use **different package managers** (yum vs. apt), **different package names** (chrony vs. ntp), and **different service names** (chronyd vs. ntp). Without conditionals, a playbook running on "all" hosts will try to execute every task on every host — causing failures. The instructor introduces the **`when` conditional** to solve this, encounters two real errors along the way (single vs. double equals, and missing `update_cache`), and demonstrates how the same playbook could be generated using ChatGPT. This lecture also sets the stage for a multi-lecture series covering loops, templates, handlers, and roles.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Multi-OS Problem: Why Conditionals Are Necessary

When managing infrastructure, you rarely have a fleet of identical machines. Real environments have **mixed operating systems** — CentOS, Ubuntu, Amazon Linux, RHEL, Debian — often in the same inventory. The instructor has three hosts: web01 and web02 (CentOS) and web03 (Ubuntu). The task is to install and start the NTP time synchronization service on **all** of them. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

The problem: CentOS and Ubuntu differ in three critical ways for this task:

| Aspect                 | CentOS    | Ubuntu |
| ---------------------- | --------- | ------ |
| Package manager module | `yum`     | `apt`  |
| NTP package name       | `chrony`  | `ntp`  |
| NTP service name       | `chronyd` | `ntp`  |

If you write a `yum` task and run it on all hosts, it fails on Ubuntu (Ubuntu doesn't have yum). If you write an `apt` task and run it on all hosts, it fails on CentOS (CentOS doesn't use apt). You need **two sets of tasks** — one for CentOS, one for Ubuntu — and a mechanism to ensure each task runs **only on the correct OS**. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

The instructor explains: *"This will get executed on all the hosts and this will be also getting executed on all the hosts. So this is going to fail. The first Yum task will fail for web03, which is Ubuntu, and this is going to fail for all the other instances except for Ubuntu."* [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## 1.2 — The `when` Conditional: Ansible's Decision-Making Mechanism

In Bash and Python, you use `if` conditions. In Ansible, the equivalent is the **`when`** keyword. It's placed at the **same indentation level as the module name** within a task, and it takes a condition expression. If the condition evaluates to `true`, the task executes. If `false`, the task is **skipped** (shows "skipping" in the output, not "failed"). [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

```yaml
- name: install NTP agent on CentOS
  yum:
    name: chrony
    state: present
  when: ansible_distribution == "CentOS"
```

The instructor draws the direct parallel to prior scripting knowledge: *"in Bash and Python scripting we have seen we use if condition, here instead of if, you have when."* [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Key syntax detail:** The condition uses **double equals** (`==`) for comparison, not single equals. The instructor makes this exact mistake and gets an error: *"I have given single equal to whereas we need to give here a double equal to, to check the condition."* Single `=` is assignment; double `==` is comparison — consistent with Python and most programming languages. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## 1.3 — Fact Variables: How Ansible Knows the OS

The condition `ansible_distribution == "CentOS"` works because Ansible automatically collects **facts** about every target machine before running tasks. Facts include the operating system name, version, architecture, IP addresses, memory, and hundreds of other system properties. These are stored in variables prefixed with `ansible_`. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

`ansible_distribution` is a fact variable that contains the OS distribution name — `"CentOS"` for CentOS machines, `"Ubuntu"` for Ubuntu machines. The values are **case-sensitive**: `CentOS` has capital C and capital OS; `Ubuntu` has capital U. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

The instructor also shows an alternative syntax from the documentation: `ansible_facts['distribution']`. This accesses the same data through the `ansible_facts` dictionary using the key `distribution`. Both forms are equivalent — `ansible_distribution` is the shorthand. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## 1.4 — Complex Conditions: AND and OR Operators

The documentation section the instructor reviews shows more advanced conditional patterns: [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**AND condition** — Both conditions must be true:

```yaml
when: ansible_distribution == "CentOS" and ansible_distribution_major_version == "6"
```

The `and` operator (equivalent to `&&` in Bash) requires **both** sides to be true. The instructor explains: *"If this condition and if this condition, if both the conditions are true then this entire thing will become true. If any of the condition is false, this is going to be false."* [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**OR condition** — Either condition can be true:

```yaml
when: (ansible_distribution == "CentOS" and ansible_distribution_major_version == "6") or
      (ansible_distribution == "Debian" and ansible_distribution_major_version == "7")
```

The `or` operator means if **either** group of conditions is true, the task runs. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**List format for AND** — A cleaner YAML way to express AND conditions:

```yaml
when:
  - ansible_distribution == "CentOS"
  - ansible_distribution_major_version == "6"
```

When conditions are given as a **YAML list** (each item prefixed with `-`), they are implicitly joined with AND — all must be true. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Other operators:** The documentation also shows `>=` (greater than or equal to) and other comparison operators. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## 1.5 — The `update_cache` Parameter: Ubuntu's apt Requirement

The instructor encounters a second problem specific to Ubuntu: even with the correct `apt` module and `when` condition, the NTP package isn't found. This is because Ubuntu's package manager needs to **refresh its package index** (`apt update`) before it can find and install packages. Without refreshing, apt doesn't know about available packages. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

The fix is the `update_cache: yes` parameter in the apt module:

```yaml
- name: install NTP agent on Ubuntu
  apt:
    name: ntp
    state: present
    update_cache: yes
  when: ansible_distribution == "Ubuntu"
```

The instructor explains: *"if you put this to yes, then it is going to run first apt update and then apt install."* [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

This is a CentOS-vs-Ubuntu behavioral difference: yum automatically checks its package metadata, while apt requires an explicit cache refresh. This difference is a common source of failures when writing cross-OS playbooks.

> 🔍 **Deep Dive**
>
> The instructor initially tests with a **dry run** (`-C` flag), which shows the "no package matching NTP" error but **doesn't actually run apt update**. The dry run simulates the task but doesn't change state — so apt's cache remains stale. The real `apt update` only happens during actual execution (without `-C`). The instructor explains: *"obviously it did not execute the apt update. So we are going to now remove the hyphen C and execute it."* This is an important nuance: dry runs cannot resolve dependency chains that require actual state changes. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## 1.6 — Ubuntu Service Auto-Start Behavior

The instructor notes an important behavioral difference between CentOS and Ubuntu regarding service management. On CentOS, installing a package does **not** automatically start or enable the service — you must explicitly use the `service` module. On Ubuntu, *"any service, when you install in Ubuntu, it is going to automatically start and enable."* [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

This means the Ubuntu service start task shows "ok" (no change needed) rather than "changed" — the service was already running after installation. The CentOS chrony package was also already installed and running in this case (pre-existing), so it also showed "ok." Only the NTP installation on Ubuntu showed "changed." [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## 1.7 — The Lecture Series Context: What's Coming Next

The instructor frames this lecture as the beginning of a larger provisioning exercise series that will progressively introduce: [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

1. **Decision making** (this lecture) — `when` conditionals
2. **Loops** — next lecture
3. **Templates** — for dynamic configuration files
4. **Handlers** — for triggered actions (e.g., restart service when config changes)
5. **Ansible Roles** — for organizing everything into reusable structures

The instructor emphasizes that the focus is not on NTP specifically, but on the **general pattern of server provisioning**: *"here we are not really focusing on the NTP service specifically but any service provisioning that you have to do, any server provisioning you have to do, how would you do it in general?"* [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## 1.8 — ChatGPT as a Playbook Generation Tool

The instructor demonstrates generating the same playbook through ChatGPT by providing a clear task description: *"Ansible playbook to install chrony on centos and NTP on Ubuntu. Also start and enable chrony and NTP service."* ChatGPT produces a playbook very close to what was written manually. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

The instructor's key insight: *"if you write the proper text, right? That means you know what you have to do, then you get very close code."* The prerequisite for using AI effectively is **knowing what you need** — the AI generates the how, but you must supply the what. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

However, the instructor recommends documentation over ChatGPT for learning: *"instead of spending time too much on ChatGPT, I recommend you better check the documentation, read the documentation, look at the condition, different ways of giving condition."* Documentation builds understanding; ChatGPT generates output. For operational competence, you need both. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are writing an Ansible playbook that provisions the **NTP time synchronization service** across a mixed fleet of CentOS and Ubuntu servers. The playbook must handle OS differences (package manager, package name, service name) using `when` conditionals. The final outcome: chrony installed and running on CentOS hosts, NTP installed and running on Ubuntu hosts, all from a single playbook targeting "all" hosts.

***

## Step 1: Set Up Exercise 10

```bash
cp -r exercise9 exercise10
cd exercise10
```

Remove old playbooks that aren't needed:

```bash
rm <old-playbook-files>
```

**Verify connectivity to all hosts:**

```bash
ansible -m ping all
```

**Expected:** All hosts respond with `pong`. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## Step 2: Create the Provisioning Playbook

Create a new file:

```bash
vim provisioning.yaml
```

**Write the play header:**

```yaml
---
- name: Provisioning servers
  hosts: all
  become: yes
  tasks:
```

* `hosts: all` — targets every host in the inventory (both CentOS and Ubuntu)
* `become: yes` — escalate to root (package installation requires root) [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## Step 3: Add CentOS Tasks with `when` Conditions

**Install chrony on CentOS:**

```yaml
    - name: install NTP agent on CentOS
      yum:
        name: chrony
        state: present
      when: ansible_distribution == "CentOS"
```

**Start and enable chronyd on CentOS:**

```yaml
    - name: start service on CentOS
      service:
        name: chronyd
        state: started
        enabled: yes
      when: ansible_distribution == "CentOS"
```

 [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Key syntax points:**

* `when:` is at the **same indentation level** as the module name (`yum:`, `service:`)
* Use **double equals** (`==`), not single equals
* String values are case-sensitive: `"CentOS"` (capital C, capital OS) [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## Step 4: Add Ubuntu Tasks with `when` Conditions

**Install ntp on Ubuntu:**

```yaml
    - name: install NTP agent on Ubuntu
      apt:
        name: ntp
        state: present
        update_cache: yes
      when: ansible_distribution == "Ubuntu"
```

* `update_cache: yes` — runs `apt update` before installing (required for Ubuntu to find packages) [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Start and enable ntp on Ubuntu:**

```yaml
    - name: start service on Ubuntu
      service:
        name: ntp
        state: started
        enabled: yes
      when: ansible_distribution == "Ubuntu"
```

 [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## Step 5: Dry Run — First Error (Single Equals)

```bash
ansible-playbook provisioning.yaml -C
```

* `-C` — **check mode** (dry run); simulates without making changes [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Expected result: ERROR** [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Error cause:** Single `=` used instead of `==` in the `when` conditions.

**Fix:** Open the playbook and change all four `when` conditions from `=` to `==`. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## Step 6: Dry Run — Second Error (Package Not Found on Ubuntu)

```bash
ansible-playbook provisioning.yaml -C
```

**Partial result:** CentOS tasks work. Ubuntu install task shows: **"no package matching NTP"** [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**What's happening correctly:** The `when` conditions work — CentOS tasks are **skipped** on web03 (Ubuntu), and Ubuntu tasks are **skipped** on web01/web02 (CentOS). The skipping behavior proves the conditionals are functioning.

**What fails:** The `apt` module can't find the `ntp` package because apt's cache hasn't been refreshed.

**Fix:** Add `update_cache: yes` to the apt task (already shown in Step 4 above). [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Why dry run didn't fix it:** The dry run doesn't actually execute `apt update` — it only simulates. The cache remains stale. You must run without `-C` to actually refresh the cache. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

## Step 7: Full Execution

```bash
ansible-playbook provisioning.yaml
```

(Remove the `-C` flag to execute for real.) [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

**Expected output:** [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

| Task                  | web01 (CentOS)         | web02 (CentOS)         | web03 (Ubuntu)               |
| --------------------- | ---------------------- | ---------------------- | ---------------------------- |
| install NTP on CentOS | ok (already installed) | ok (already installed) | **skipping**                 |
| install NTP on Ubuntu | **skipping**           | **skipping**           | **changed** (installed)      |
| start service CentOS  | ok (already running)   | ok (already running)   | **skipping**                 |
| start service Ubuntu  | **skipping**           | **skipping**           | ok (auto-started on install) |

**Key observations:**

* "skipping" = `when` condition was false → task not executed on that host
* "ok" = task executed but no change needed (idempotent)
* "changed" = task executed and made a change
* Ubuntu auto-starts services on install, so the start task shows "ok" not "changed" [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Problem and Solution

```
PROBLEM:
  hosts: all → includes CentOS + Ubuntu
  yum task → fails on Ubuntu (no yum)
  apt task → fails on CentOS (no apt)

SOLUTION:
  when: ansible_distribution == "CentOS"   → yum tasks
  when: ansible_distribution == "Ubuntu"    → apt tasks
  
  Condition FALSE → task SKIPPED (not failed)
```

***

## 🔷 The Complete Playbook Structure

```yaml
- name: Provisioning servers
  hosts: all
  become: yes
  tasks:
    # ── CentOS tasks ──
    - name: install chrony
      yum: { name: chrony, state: present }
      when: ansible_distribution == "CentOS"

    - name: start chronyd
      service: { name: chronyd, state: started, enabled: yes }
      when: ansible_distribution == "CentOS"

    # ── Ubuntu tasks ──
    - name: install ntp
      apt: { name: ntp, state: present, update_cache: yes }
      when: ansible_distribution == "Ubuntu"

    - name: start ntp
      service: { name: ntp, state: started, enabled: yes }
      when: ansible_distribution == "Ubuntu"
```

***

## 🔷 OS Differences Map

```
                 CentOS              Ubuntu
─────────────    ────────────        ────────────
Pkg manager      yum                 apt
NTP package      chrony              ntp
NTP service      chronyd             ntp
Cache refresh    not needed          update_cache: yes (required)
Auto-start       NO (must enable)    YES (starts on install)
Fact variable    "CentOS" (C, OS)    "Ubuntu" (U)
```

***

## 🔷 `when` Syntax

```yaml
# Simple condition
when: ansible_distribution == "CentOS"

# AND (inline)
when: ansible_distribution == "CentOS" and ansible_distribution_major_version == "6"

# AND (list format — cleaner)
when:
  - ansible_distribution == "CentOS"
  - ansible_distribution_major_version == "6"

# OR
when: (condition_A) or (condition_B)

# Comparison operators: ==, !=, >, <, >=, <=

PLACEMENT: same indentation level as module name
USES: == (double equals, NOT single)
```

***

## 🔷 Fact Variable Access (Two Equivalent Forms)

```
ansible_distribution                    ← shorthand
ansible_facts['distribution']           ← dictionary access

Both return: "CentOS", "Ubuntu", "Debian", etc.
Case-sensitive: CentOS (C + OS), Ubuntu (U)
```

***

## 🔷 Two Errors Encountered and Fixed

```
ERROR 1: Single = instead of ==
  Cause: assignment operator used instead of comparison
  Fix: change = to == at all four when: lines
  
ERROR 2: "no package matching NTP" on Ubuntu
  Cause: apt cache not refreshed (no apt update run)
  Fix: add update_cache: yes to apt module
  Note: dry run (-C) doesn't actually run apt update
        → must run without -C to see the fix work
```

***

## 🔷 Dry Run vs. Real Run

```
ansible-playbook playbook.yaml -C     → DRY RUN (simulate, no changes)
ansible-playbook playbook.yaml        → REAL RUN (execute changes)

DRY RUN LIMITATION:
  Cannot resolve dependencies that require actual state changes
  Example: apt update_cache needs real execution to refresh
           → dry run still shows "package not found"
```

***

## 🔷 Task Status Values

```
STATUS        MEANING
──────        ─────────────────────────────────────
ok            Task ran, no change needed (idempotent)
changed       Task ran, made a change
skipping      when: condition was FALSE → task not executed
failed        Task attempted, error occurred
```

***

## 🔷 Lecture Series Roadmap

```
Exercise 10+: Server Provisioning Series (NTP service)

  1. ✅ Decision making (when:)          ← THIS LECTURE
  2. ⬜ Loops                            ← NEXT
  3. ⬜ Templates (dynamic configs)
  4. ⬜ Handlers (triggered actions)
  5. ⬜ Ansible Roles (structural organization)

Each lecture adds a new playbook feature while building on all previous ones.
Focus: general server provisioning patterns, not NTP-specific knowledge.
```

***

## 🔷 ChatGPT for Playbook Generation

```
INPUT (clear task description):
  "Ansible playbook to install chrony on centos
   and NTP on Ubuntu. Also start and enable
   chrony and NTP service."

OUTPUT: Nearly identical playbook to manual version

PREREQUISITE: You must know WHAT you need → AI generates HOW
RECOMMENDATION: Use docs for learning, AI for speed
  "I recommend you better check the documentation"
```

***

## 🔷 Reusable Engineering Pattern: OS-Conditional Task Pairing

```
PATTERN: Parallel Task Pairs with OS Conditions

For any cross-OS operation:

  TASK A (CentOS version):
    module: yum / systemd-specific
    when: ansible_distribution == "CentOS"

  TASK B (Ubuntu version):
    module: apt / debian-specific
    when: ansible_distribution == "Ubuntu"

Same logical operation → two implementation tasks → one condition each

This pattern scales to:
  - Package installation (yum vs. apt)
  - Service management (different service names)
  - Configuration files (different paths)
  - User management (different defaults)
  - Firewall rules (firewalld vs. ufw)

The condition variable (ansible_distribution) is the ROUTER
that sends each task to the correct OS.
```

***

## 🔷 Execution Flow Visualization

```
PLAYBOOK RUNS ON: all (web01, web02, web03)

Task: install chrony (yum)
  web01 (CentOS) → when: TRUE  → EXECUTE → ok
  web02 (CentOS) → when: TRUE  → EXECUTE → ok
  web03 (Ubuntu) → when: FALSE → SKIP

Task: install ntp (apt)
  web01 (CentOS) → when: FALSE → SKIP
  web02 (CentOS) → when: FALSE → SKIP
  web03 (Ubuntu) → when: TRUE  → EXECUTE → changed

Task: start chronyd
  web01 → TRUE  → ok
  web02 → TRUE  → ok
  web03 → FALSE → SKIP

Task: start ntp
  web01 → FALSE → SKIP
  web02 → FALSE → SKIP
  web03 → TRUE  → ok (auto-started on install)
```

Each task runs on ALL hosts but the `when` condition acts as a **per-host filter** — the task only executes where the condition is true and cleanly skips everywhere else. This is the fundamental mechanism that makes a single playbook work across a heterogeneous fleet. [\[243-decision-making \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/243-decision-making.txt)
