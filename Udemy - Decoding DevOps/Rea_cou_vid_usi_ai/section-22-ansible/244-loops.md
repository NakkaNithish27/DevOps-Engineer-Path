# 🎓 Deep Learning Material: Ansible Loops — Repeating Tasks Across Multiple Items Without Code Duplication

**Source:** Video lecture on Ansible playbook loops (from [244-loops.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt?EntityRepresentationId=2f141360-aa13-4040-8235-b818daf844a0) caption file) [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

**Video Context:** This is the second lecture in the server provisioning series (following the Decision Making lecture). The instructor takes the existing NTP provisioning playbook from exercise 10 and extends it to install **multiple packages** using loops instead of duplicating tasks. The lecture covers the basic `loop` keyword with a list of strings, introduces the `item` variable, shows how loops interact with `when` conditions, briefly covers dictionary-based loops from the documentation, and mentions `with_items` as the older equivalent. The lecture is concise but introduces a fundamental automation pattern — iterating over a collection of items with a single task definition.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Task Duplication for Multiple Items

The instructor frames the problem directly: the existing playbook installs a **single package** per task. But real-world provisioning requires installing many packages — 2, 5, 10, 20, or more. Without loops, you would need to **copy and paste the same task** for every package, changing only the package name each time. This creates massive duplication, makes the playbook hard to maintain, and violates basic engineering principles. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

The instructor asks: *"What if we need to install 2, 5, 10, 20 packages? Many, many packages. What if you want to do that? Do we copy these tasks again and again for that many times? No, we will use loops."* [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## 1.2 — The `loop` Keyword: How It Works

The **`loop`** keyword is placed at the same indentation level as the module name within a task. Its value is a **list** — either defined inline or referenced as a variable. The loop causes the task to **repeat once for each item** in the list. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

```yaml
- name: install packages
  yum:
    name: "{{ item }}"
    state: present
  loop:
    - chrony
    - wget
    - git
    - zip
    - unzip
```

The loop executes the `yum` task **five times** — once for each item in the list. On each iteration, the current item's value is available through a special variable called **`item`**. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## 1.3 — The `item` Variable: The Loop Iterator

`item` is a **reserved variable name** that Ansible automatically creates during loop execution. On each iteration, `item` holds the current value from the list. You reference it in the task using Jinja2 template syntax: `"{{ item }}"` (double curly braces inside double quotes). [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

The instructor explains the iteration flow: *"this loop is going to have a variable called item and it is going to loop your task as many times as you have the items. So this task, yum task is going to run how many times? Five times. And every time the value of item will be changing. First it'll be chrony, then it will be wget, git, zip, unzip, like that."* [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

The variable name **must be `item`** — this exact name. It's not user-defined for basic loops; it's what the loop mechanism returns.

***

## 1.4 — Loop Placement with `when` Conditions

When a task has both a `loop` and a `when` condition, both apply. The `when` condition determines whether the task runs **on a given host**, and the `loop` determines **how many times** it runs on that host. The instructor demonstrates this by adding loops to both the CentOS (yum) and Ubuntu (apt) tasks — each has its own `when` condition from the previous lecture. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

The placement is important: the `loop` block goes **below the `when` condition** (or alongside it at the same indentation level as the module name). If there is no condition, the loop goes directly at the module indentation level. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## 1.5 — Two Loop Syntaxes: `loop` vs. `with_items`

The instructor briefly mentions from the documentation that there are **two ways** to write loops: [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

* **`loop:`** — the modern syntax, provides more functionality
* **`with_items:`** — the older syntax, still works, functionally similar for basic cases

The instructor states: *"this is similar, with\_items, or you can give loop also, but loop gives you much more functionality."* For new playbooks, `loop` is preferred. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## 1.6 — List Sources: Inline vs. Variable

The list of items can be defined in two ways: [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

**Inline list** (directly in the playbook):

```yaml
loop:
  - chrony
  - wget
  - git
```

**Variable reference** (list defined elsewhere — in `group_vars/all`, a vars file, etc.):

```yaml
loop: "{{ package_list }}"
```

Where `package_list` is a list variable defined in a variables file. The instructor mentions: *"we can have a list variable and we can give this variable value over here. Sorry, variable name over here."* [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## 1.7 — Dictionary Loops: Passing Multiple Values Per Iteration

The documentation section the instructor reviews shows a more advanced pattern: instead of passing a simple string per iteration, you can pass a **dictionary** with multiple key-value pairs. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

```yaml
loop:
  - { name: 'testuser1', groups: 'wheel' }
  - { name: 'testuser2', groups: 'root' }
```

In this case, each iteration's `item` is a dictionary, and you access individual values with dot notation: `item.name` returns `testuser1` on the first iteration, `item.groups` returns `wheel`. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

The instructor highlights this feature: *"you can pass multiple values also per iteration. Then you need to have a dictionary variable instead of mentioning a string."* This is used when a task needs **multiple pieces of information** per iteration — for example, creating users where each user has both a name and a group. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## 1.8 — Advanced Loop Patterns (Mentioned, Not Demonstrated)

The instructor briefly mentions more complex loop capabilities from the documentation, including **retrying a task until a condition is met** (a retry loop). He advises: *"for now we'll keep it simple, is enough for now. When the need comes, then you can go with the complex one. But mostly we use this one only and the max, the dictionary variables."* [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are extending the NTP provisioning playbook from exercise 10 to install **multiple packages** (chrony, wget, git, zip, unzip) using loops instead of duplicating tasks. The final outcome: a single `yum` task and a single `apt` task that each iterate over a list of packages, installing all of them — combined with the `when` conditions from the previous lecture to handle OS-specific execution.

***

## Step 1: Set Up Exercise 11

```bash
cp -r exercise10 exercise11
cd exercise11
```

 [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

The playbook from exercise 10 (with `when` conditions for CentOS and Ubuntu) is the starting point.

***

## Step 2: Add a Loop to the CentOS yum Task

Open the playbook:

```bash
vim provisioning.yaml
```

**Modify the CentOS package installation task:**

**Before (single package):**

```yaml
- name: install NTP agent on CentOS
  yum:
    name: chrony
    state: present
  when: ansible_distribution == "CentOS"
```

**After (loop with multiple packages):**

```yaml
- name: install NTP agent on CentOS
  yum:
    name: "{{ item }}"
    state: present
  loop:
    - chrony
    - wget
    - git
    - zip
    - unzip
  when: ansible_distribution == "CentOS"
```

 [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

**What changed:**

1. `name: chrony` → `name: "{{ item }}"` — replaced the hardcoded package name with the loop variable
2. Added `loop:` block with a list of five packages
3. The `when:` condition remains — this task only runs on CentOS hosts

**Syntax details:**

* `"{{ item }}"` — double quotes wrapping double curly braces; `item` is the reserved loop variable name
* `loop:` is at the same indentation level as `yum:` and `when:`
* Each list item under `loop:` is prefixed with `- ` (standard YAML list syntax) [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## Step 3: Add a Loop to the Ubuntu apt Task

**Copy the loop structure** and apply it to the apt task. The Ubuntu package list differs slightly (ntp instead of chrony):

```yaml
- name: install NTP agent on Ubuntu
  apt:
    name: "{{ item }}"
    state: present
    update_cache: yes
  loop:
    - ntp
    - wget
    - git
    - zip
    - unzip
  when: ansible_distribution == "Ubuntu"
```

 [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

**Placement note:** The `loop:` block goes below the `when:` condition (or alongside it — the order between `loop` and `when` at the same indentation level doesn't matter, but the instructor places `loop` first, then `when`). [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

## Step 4: Execute the Playbook

```bash
ansible-playbook provisioning.yaml
```

(No `-i inventory` shown in this lecture — likely using the default inventory from the exercise directory.) [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

**Expected output characteristics:** [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

* The output is **longer than before** — the instructor notes: *"look at the output. It's going to be a little bigger."*
* Each task now shows **multiple sub-results** — one per loop iteration, per host
* Each sub-result shows the package name and whether it was `ok` (already installed) or `changed` (newly installed)

**Specific results on web03 (Ubuntu):** [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

* `ntp` — already installed (from exercise 10)
* `wget` — already installed
* `git` — already installed
* `zip` — **changed** (newly installed)
* `unzip` — status depends on existing state

The instructor observes: *"on web03, ntp, wget and git was already installed. The zip was not installed so it installed that one."* [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

**Connection to system flow:** The loop eliminates the need for separate tasks per package. As you need more packages in the future, you simply add items to the list — no structural changes to the playbook.

***

## Step 5: Practice Suggestion

The instructor recommends trying additional loop tasks as practice: *"Try to add some more tasks like adding multiple users in the playbook. Try that also."* This would use the `user` module with a loop of usernames — a direct application of the pattern learned. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept (One-Line Reconstruction)

> **`loop:` repeats a task for each item in a list; the current item is accessed via `"{{ item }}"`.**

***

## 🔷 Loop Syntax (Complete)

```yaml
- name: task description
  module:
    parameter: "{{ item }}"     # loop variable
    state: present
  loop:                          # list of values to iterate
    - value1
    - value2
    - value3
  when: condition                # optional; filters by host
```

***

## 🔷 Before vs. After Loop

```
BEFORE (no loop):                    AFTER (with loop):
─────────────────                    ──────────────────
- yum: name: chrony                  - yum: name: "{{ item }}"
- yum: name: wget                     loop:
- yum: name: git                        - chrony
- yum: name: zip                        - wget
- yum: name: unzip                      - git
                                        - zip
5 tasks                                 - unzip
                                     1 task (runs 5 times)
```

***

## 🔷 Loop Iteration Flow

```
loop: [chrony, wget, git, zip, unzip]

Iteration 1: item = "chrony"   → yum install chrony
Iteration 2: item = "wget"    → yum install wget
Iteration 3: item = "git"     → yum install git
Iteration 4: item = "zip"     → yum install zip
Iteration 5: item = "unzip"   → yum install unzip

Each iteration = independent task execution
Each shows ok/changed/failed independently
```

***

## 🔷 Loop + When (Combined)

```
Task: install packages (yum + loop + when: CentOS)

  web01 (CentOS): when TRUE  → loop runs 5 times (5 packages)
  web02 (CentOS): when TRUE  → loop runs 5 times
  web03 (Ubuntu): when FALSE → SKIP entirely (loop never starts)

EVALUATION ORDER:
  1. when: evaluated per HOST
  2. loop: evaluated per ITEM (only if when passed)
```

***

## 🔷 Three List Sources

```
1. INLINE LIST:
   loop:
     - chrony
     - wget

2. VARIABLE REFERENCE:
   loop: "{{ package_list }}"
   # package_list defined in group_vars/all or vars file

3. DICTIONARY LIST:
   loop:
     - { name: 'user1', groups: 'wheel' }
     - { name: 'user2', groups: 'root' }
   # Access: item.name, item.groups
```

***

## 🔷 Dictionary Loop (Multi-Value Per Iteration)

```yaml
- name: add users
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
  loop:
    - { name: 'testuser1', groups: 'wheel' }
    - { name: 'testuser2', groups: 'root' }

Iteration 1: item.name = 'testuser1', item.groups = 'wheel'
Iteration 2: item.name = 'testuser2', item.groups = 'root'

USE CASE: when each iteration needs MULTIPLE values
          (string loop = 1 value, dict loop = N values)
```

***

## 🔷 `loop` vs. `with_items`

```
loop:           → modern syntax, more features (PREFERRED)
with_items:     → older syntax, same basic behavior

Both work for simple lists. Use loop: for new playbooks.
```

***

## 🔷 Key Syntax Rules

```
"{{ item }}"     → double quotes + double curly braces (mandatory)
item             → reserved name (cannot change for basic loops)
loop:            → same indentation as module name and when:
List items       → standard YAML list (- prefix)
```

***

## 🔷 Exercise File Changes

```
exercise10/provisioning.yaml          exercise11/provisioning.yaml
─────────────────────────────          ─────────────────────────────
yum: name: chrony                      yum: name: "{{ item }}"
                                       loop: [chrony, wget, git, zip, unzip]

apt: name: ntp                         apt: name: "{{ item }}"
                                       loop: [ntp, wget, git, zip, unzip]

when: conditions remain identical in both exercises
```

***

## 🔷 Lecture Series Progress

```
  1. ✅ Decision making (when:)
  2. ✅ Loops (loop:)                    ← THIS LECTURE
  3. ⬜ Templates (dynamic configs)      ← NEXT
  4. ⬜ Handlers (triggered actions)
  5. ⬜ Ansible Roles
```

***

## 🔷 Reusable Engineering Pattern: Iteration Over Collections

```
PATTERN: Single Definition + List-Driven Repetition

WITHOUT LOOP:
  Task A (item 1)
  Task A (item 2)
  Task A (item 3)
  → N tasks for N items
  → duplication, maintenance burden

WITH LOOP:
  Task A ({{ item }})
  loop: [item1, item2, item3]
  → 1 task definition for N items
  → add items to list = automatic scaling

SCALING PROPERTY:
  Adding a new package = adding one line to the list
  No structural playbook changes needed
  
This pattern maps to:
  - Python: for item in list
  - Bash: for item in list; do ... done
  - Terraform: count / for_each
  - Kubernetes: range in Helm templates
  - Programming: foreach / map / iterate

The abstraction: separate WHAT to do (task definition)
                 from WHAT to do it on (list of items).
```

This is the core engineering insight: loops **decouple the action from the data**. The task defines the action once; the list defines the data set. Changing one doesn't require changing the other. [\[244-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/244-loops.txt)
