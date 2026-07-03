# 🎓 Deep Learning Material: Ansible Handlers — Event-Driven Task Execution

**Source:** [246-handlers.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt?EntityRepresentationId=144ab4e0-3c31-4ec6-a681-58560df440df) — Video lecture covering Ansible handlers as a mechanism for conditional task execution based on change detection, the `notify`/`handler` relationship, handler naming rules, the template + handler pattern for configuration management, and the distinction between handlers and regular tasks. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: Unnecessary Service Restarts

In the exercises leading up to this lecture, the playbook has been **restarting the service every single time it runs** — regardless of whether anything actually changed. If you run the playbook ten times, the service restarts ten times. This is wasteful and operationally dangerous. Restarting a service causes a brief downtime window. In production, an unnecessary restart on a web server means dropped connections; on a database, it means interrupted queries. The desired behavior is: restart the service **only when the configuration file actually changes**. If nothing changed, don't touch the service. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

You *could* solve this with a `when` condition (covered in the previous decision-making lecture), but Ansible provides a **purpose-built mechanism** that is cleaner and more expressive: **handlers**. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## 1.2 What Handlers Are — The Core Concept

A handler is a task that **exists in a dormant state**. It is defined in the playbook but it does **not** execute during normal task flow. It sits idle, waiting. It only executes when it is **notified** by another task. And a task only sends a notification when its execution results in a **change** — when the `changed` status is `true`. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

This creates an event-driven relationship:

1. A regular task runs (e.g., deploy a configuration file using the template module).
2. If the file was already identical on the target → `changed: false` → **no notification sent** → handler stays dormant.
3. If the file was different and got updated → `changed: true` → **notification sent** → handler wakes up and executes (e.g., restarts the service).

The mechanism piggybacks on Ansible's built-in change detection. Every module already reports whether it changed anything (the JSON `changed: true` or `changed: false` value in the output). Handlers simply react to this existing signal. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

The instructor uses an analogy: handlers are like **agents in spy movies** (CIA handlers, NSA handlers). They remain in a dormant state. When there is a requirement, they receive a notification. Only then do they execute their task. Without notification, they do nothing. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## 1.3 How Handlers Relate to Tasks — Structure and Placement

Handlers look syntactically **identical** to regular tasks — same format, same module usage, same parameters. The difference is purely in **where they are declared** and **how they are triggered**. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

Regular tasks are listed under the `tasks:` section. Handlers are listed under a separate `handlers:` section. The `handlers:` keyword must be placed at the **same indentation level (same column)** as the `tasks:` keyword. This is a structural requirement — if `handlers:` is indented differently from `tasks:`, the YAML structure breaks and Ansible won't parse it correctly. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

Inside the `handlers:` section, each handler is defined exactly like a task: it has a `name:`, a module, and module parameters. The `name` is critically important — it is the **identifier** that the notification system uses to find and trigger the correct handler. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## 1.4 The `notify` Keyword — Linking Tasks to Handlers

The connection between a task and a handler is made with the `notify` keyword. You add `notify:` to any task that should trigger a handler when it produces a change. The `notify` keyword must be at the **same indentation level as the module name** within that task. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

Under `notify:`, you provide a list of handler names. The format uses YAML list syntax (`- handler_name`). You can notify **one or many handlers** from a single task. The video shows notifying one handler per task, but explicitly references the documentation showing multiple handlers being notified from a single task — for example, when changing a configuration requires restarting one service, which in turn requires restarting another dependent service. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

⚠️ **Expert Note**
The handler name in the `notify` list must **exactly match** the `name:` field of the handler. This includes capitalization, spacing, and spelling. If there is any mismatch, Ansible will report "handler not found." This is one of the most common mistakes with handlers — a typo in either the handler name or the notify reference silently breaks the notification chain. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## 1.5 The Change Detection Mechanism — `changed: true` / `changed: false`

Every Ansible module reports whether it made a change. When you deploy a file using the `template` module, Ansible compares the source template with the file currently on the target. If they are **identical** (content matches), the module reports `changed: false` — nothing was modified. If they are **different** (even by a single character, a space, or a comment hash), the module pushes the new file and reports `changed: true`. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

The `notify` mechanism reads this `changed` value:

* `changed: true` → notification is sent → handler executes.
* `changed: false` → no notification → handler stays dormant. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

The video demonstrates this directly. First, the playbook runs with no changes to source files — all template tasks report `ok` (no change), and no handlers execute. Then, a trivial change is made to the CentOS configuration file (adding a hash comment or a space — not changing actual configuration content). On the next run, the template module detects the difference, pushes the updated file (`changed: true`), and the CentOS handler fires. The Ubuntu handler does **not** fire because the Ubuntu configuration file was not modified. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

🔍 **Deep Dive**
The change comparison happens between the **source** (on the control machine) and the **destination** (on the target). If you modify either one, a difference is detected. The video says: "You can change source or destination, anything. Whenever there is a difference in both the files, it is going to push the file and the handler will get executed." This means even if someone manually edits the config on the target server, the next playbook run will detect the drift, re-push the correct file, and trigger the handler. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## 1.6 Handlers Are Not Only for Service Restarts

The instructor emphasizes this point explicitly and repeatedly: "handler is not only for restarting service. You can give any task over there." The common misconception is that handlers exist solely for `service: state: restarted`. In reality, a handler is just a **conditionally-triggered task** — it can contain any module. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

The instructor gives a concrete alternative example: you create a user with the `user` module as a regular task. The handler, triggered by the user creation (`changed: true`), copies files to the user's home directory using the `copy` module. The task is user creation; the handler is file provisioning that should only happen when a new user is actually created. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

That said, the most common real-world combination is **template module + handler for service restart**. The instructor states from personal experience: "We use template module a lot, and along with template we use handler. It's a very common or very general combination — templates and handler for configuration files." The pattern is: push configuration → if changed → restart service to pick up the new configuration. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## 1.7 Where Handlers Fit in the Series

This lecture is part of a provisioning exercise series. The trajectory so far: decision making (`when`) → loops → templates → **handlers** (this lecture) → roles (next lecture). Handlers are the mechanism that makes template-based configuration management operationally correct — without handlers, every template push would require a manual decision about whether to restart. The next lecture on **roles** will show how to organize all these elements (tasks, templates, handlers, variables) into reusable, structured units. The documentation explicitly discusses "handlers in roles," and the instructor notes that handler behavior is mostly the same whether used in a standalone playbook or within a role. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are converting a regular restart task into a **handler** so that the NTP service only restarts when its configuration file actually changes. The final outcome: running the playbook with no configuration changes produces no restart; modifying a configuration source file triggers only the relevant OS-specific handler to restart the corresponding service. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## Step 1: Set Up the Exercise Directory

```bash
cp -r exercise12 exercise13
cd exercise13
```

 [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

This preserves the existing playbook (with template tasks, `when` conditions, loops) as the starting point.

***

## Step 2: Reorganize the Playbook — Move Restart Task to the End

Open the playbook:

```bash
vim provisioning.yaml
```

The restart service task currently sits somewhere in the middle of the tasks list. Move it to the **end** of the tasks section. The instructor uses Vim commands: `4dd` to cut the task lines, then navigates to the desired position and pastes. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

**Why move it to the end?** Handlers execute at the end of the play (after all tasks complete). By positioning the restart task at the bottom of the tasks list first, the conversion to a handler is cleaner — the logical flow matches what handlers will do naturally. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## Step 3: Convert the Restart Task to a Handler

The restart task currently looks something like this under `tasks:`:

```yaml
  tasks:
    # ... other tasks ...
    - name: Restart NTP on CentOS
      service:
        name: chronyd
        state: restarted
      when: ansible_distribution == "CentOS"

    - name: Restart NTP on Ubuntu
      service:
        name: ntp
        state: restarted
      when: ansible_distribution == "Ubuntu"
```

**Remove these from the `tasks:` section** and create a new `handlers:` section at the **same indentation level** as `tasks:`:

```yaml
  tasks:
    # ... all other tasks remain here ...

  handlers:
    - name: Restart NTP on CentOS
      service:
        name: chronyd
        state: restarted
      when: ansible_distribution == "CentOS"

    - name: Restart NTP on Ubuntu
      service:
        name: ntp
        state: restarted
      when: ansible_distribution == "Ubuntu"
```

 [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

**Critical alignment:** `handlers:` must be in the **same column** as `tasks:`. If `tasks:` is indented 2 spaces from the play header, `handlers:` must also be indented 2 spaces from the play header. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

The handler definitions look exactly like the tasks they replaced — same `name`, same `service` module, same `when` conditions. The only change is their location: they now live under `handlers:` instead of `tasks:`.

***

## Step 4: Add `notify` to the Configuration File Tasks

Find the tasks that deploy configuration files (the template tasks). Add a `notify:` entry to each one.

**For the CentOS configuration task:**

```yaml
    - name: Deploy NTP configuration file on CentOS
      template:
        src: <centos-template-source>
        dest: <centos-config-destination>
      when: ansible_distribution == "CentOS"
      notify:
        - Restart NTP on CentOS
```

**For the Ubuntu configuration task:**

```yaml
    - name: Deploy NTP configuration file on Ubuntu
      template:
        src: <ubuntu-template-source>
        dest: <ubuntu-config-destination>
      when: ansible_distribution == "Ubuntu"
      notify:
        - Restart NTP on Ubuntu
```

 [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

**Breakdown of the `notify` block:**

| Part                                     | Meaning                                                                  |
| ---------------------------------------- | ------------------------------------------------------------------------ |
| `notify:`                                | Declares that this task should notify handlers when it produces a change |
| Same column as module name (`template:`) | Structural requirement — must align with the module                      |
| `- Restart NTP on CentOS`                | List item — the **exact name** of the handler to notify                  |

⚠️ The handler name in the `notify` list must **exactly match** the `name:` field of the corresponding handler. Any spelling mismatch → "handler not found" error. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

You can list multiple handlers under `notify:` using additional `- handler_name` entries. In this exercise, each task notifies only one handler. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

Save and quit: `Esc` → `:wq` → `Enter`.

***

## Step 5: First Run — No Changes Expected

Execute the playbook without making any changes to the configuration source files:

```bash
ansible-playbook provisioning.yaml
```

 [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

**Expected output:**

The template tasks for deploying configuration files should show status `ok` — meaning the source and destination files are identical, no change occurred. Because `changed: false`, no notification is sent. The handlers section should show **nothing** — no handler names appear in the output because none were triggered.

**What to verify:** Look at the "Deploy NTP configuration" tasks — they should all show `ok`. Look at the end of the output — no handler execution should appear. This confirms: **no change → no notification → no handler execution**. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## Step 6: Make a Trivial Change to Trigger the Handler

Modify the **CentOS** NTP configuration source file on the control machine. The goal is to create a difference between the source and the destination so that the template module detects a change.

```bash
vim <centos-ntp-config-source-file>
```

Add a trivial change — a comment hash (`#`) on a blank line, or an extra space. **Do not change actual configuration content.** The point is to trigger change detection without affecting service behavior. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

Save and quit. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

**Why only CentOS?** To demonstrate that handlers fire independently per OS. Only the CentOS configuration changed, so only the CentOS handler should execute. The Ubuntu handler should remain dormant.

***

## Step 7: Second Run — Handler Should Fire

```bash
ansible-playbook provisioning.yaml
```

 [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

**Expected output:**

| Task / Handler      | CentOS hosts | Ubuntu host     |
| ------------------- | ------------ | --------------- |
| Deploy NTP config   | `changed`    | `ok`            |
| Restart NTP handler | **EXECUTES** | does not appear |

The CentOS configuration task detects a difference (the hash/space you added), pushes the updated file (`changed: true`), and sends a notification to the "Restart NTP on CentOS" handler. The handler executes and restarts `chronyd`.

The Ubuntu configuration task finds no difference (`ok`), sends no notification, and the Ubuntu handler remains dormant. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

**What to verify:**

* The deploy task for CentOS shows `changed`.
* The handler "Restart NTP on CentOS" appears in the output and executes.
* No Ubuntu handler appears.

**Connection to larger flow:** The handler mechanism is now proven. Configuration changes trigger restarts; no changes mean no restarts. This completes the configuration management pattern: template (push config) + handler (restart on change). The next lecture covers **roles**, which organize tasks, templates, handlers, and variables into reusable directory structures.

⚠️ **Expert Note**
You can test the reverse: modify only the Ubuntu source file, or modify both. Modifying both source files will trigger both handlers. The handler system evaluates independently per notification — each `notify` is a separate signal from a separate task on a separate host. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

## Step 8: Documentation Reference

Search for "Ansible handlers" or navigate to the Ansible documentation page "Running operations on change."

Key sections in the documentation:

* **Basic handler example:** Template module → `notify: Restart Apache` → handler restarts Apache. This is the canonical pattern. [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)
* **Calling multiple handlers:** A single task can notify multiple handlers — useful when one configuration change requires multiple service restarts.
* **Naming handlers:** Proper, descriptive names are essential for the notification matching.
* **Controlling handlers:** Advanced execution control options.
* **Using variables in handlers:** Dynamic handler behavior.
* **Handlers in roles:** Handler behavior within the role directory structure (covered in the next lecture). [\[246-handlers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/246-handlers.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Mechanism

```
TASK executes
  ├── changed: false → NO notification → handler DORMANT
  └── changed: true  → notify sent     → handler EXECUTES
```

***

## Playbook Structure (Handler Placement)

```yaml
- name: Play name
  hosts: all
  become: yes

  tasks:              ← regular tasks (always execute in order)
    - name: Deploy config
      template: ...
      notify:
        - Handler Name    ← triggers handler ONLY on change

  handlers:           ← same column as tasks: (CRITICAL)
    - name: Handler Name   ← exact name match required
      service: ...         ← any module, not just service
```

***

## Notify → Handler Matching

```
Task's notify list         Handler's name field
─────────────────          ──────────────────
"Restart NTP on CentOS" ══► name: Restart NTP on CentOS

⚠️ EXACT string match (case, spacing, spelling)
⚠️ Mismatch → "handler not found" error
```

***

## Event-Driven Flow

```
Template pushes config file
    │
    ├── Source == Destination → ok (no change) → handler sleeps
    │
    └── Source ≠ Destination → changed → notify → handler wakes → restarts service
                                                                        │
                                                          (or any task — not just restart)
```

***

## Indentation Rules

```
tasks:       ← column X (aligned with play-level keys)
  - name:
    module:
    notify:  ← same column as module name

handlers:    ← column X (SAME column as tasks:)
  - name:
    module:
```

***

## Test Sequence (Proving Handler Behavior)

```
Run 1: No source changes → all template tasks = ok → NO handlers fire
Run 2: Modify CentOS source (add # or space) → CentOS template = changed
       → CentOS handler fires → Ubuntu handler stays dormant
```

***

## Handler ≠ Service Restart (Common Misconception)

```
Handler = any task in dormant state, triggered by notification

Common use:     template → notify → service restart
But also:       user creation → notify → copy files to home dir
                package install → notify → push initial config
                ANY task → notify → ANY other task
```

***

## The Canonical Pattern (DevOps Standard)

```
template module ──(config file changes)──→ notify ──→ handler (service restart)

Instructor: "We use template module a lot, and along with template we use handler.
             It's a very common combination — templates and handler for configuration files."
```

***

## Multiple Handlers from One Task

```
- name: Push main config
  template: ...
  notify:
    - Restart Service A
    - Restart Service B      ← both handlers fire if task changes
    - Send notification
```

***

## Change Detection Trigger

```
Source file (control machine)  vs  Destination file (target)
         │                                    │
         └──── ANY difference ────────────────┘
                    │
              changed: true
                    │
              notify sent → handler executes

Difference can be: content, comment, space, hash — anything
Modify source OR destination → next run detects drift → pushes file → handler fires
```

***

## Operational Sequence

```
1. cp -r exercise12 exercise13 && cd exercise13
2. vim provisioning.yaml
3. Move restart tasks to end of tasks section
4. Cut restart tasks from tasks: → paste under new handlers: section
5. Add notify: to each template/config task (exact handler name)
6. Run playbook (no source changes) → verify NO handlers fire
7. Modify CentOS source file (trivial: add #)
8. Run playbook → verify ONLY CentOS handler fires
9. Verify Ubuntu handler stays dormant
```

***

## Handler vs Task Comparison

```
                    Task                    Handler
────────────────────────────────────────────────────────
Location            tasks:                  handlers:
Execution           Always (in order)       Only when notified
Trigger             Play flow               changed: true from a task
Default state       Active                  Dormant
Timing              Sequential in task list After all tasks complete
Syntax              Identical               Identical (same modules)
```

***

## Key Engineering Patterns

| Pattern                    | Manifestation                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| **Event-driven execution** | Handlers execute only on state change — no change = no action                               |
| **Change-as-signal**       | Ansible's built-in `changed` boolean becomes a trigger for downstream actions               |
| **Dormant-until-notified** | Handlers decouple "what to react to" from "what to do" — task doesn't restart, it notifies  |
| **Name-based binding**     | Task → handler link is by string name match, not by position or reference — loose coupling  |
| **Config-push + restart**  | Template + handler = the standard configuration management cycle                            |
| **Drift detection**        | Source ≠ destination → correction pushed → dependent action triggered                       |
| **Selective reaction**     | Only the OS whose config changed gets its handler fired — granular, per-host event response |

***

## Series Continuity

```
Decision making (when)  →  Loops  →  Templates  →  HANDLERS (this)  →  Roles (next)

Handlers complete the configuration management cycle:
  Templates PUSH config  +  Handlers REACT to changes

Roles will ORGANIZE all of these into reusable directory structures
```

***

This completes the full reconstruction. **Theory** explains *why* handlers exist (unnecessary restarts), *how* they work (dormant-until-notified via `changed` signal), and *what* they really are (any task, not just restarts). **Practical** gives you every structural change, every test run, and every expected output to reproduce the exercise. The **Compression Map** lets you reload the entire event-driven mechanism — from change detection to handler firing — in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀
