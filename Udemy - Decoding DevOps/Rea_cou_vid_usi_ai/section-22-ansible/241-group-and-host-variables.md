# Ansible Group & Host Variables — Deep Learning Material

**Source:** Ansible course lecture on Group and Host Variables / Variable Precedence (caption file: [241-group-and-host-variables.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt?EntityRepresentationId=078cdfd2-5402-4e26-9de7-5f2494c384fe)) [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Why Variables Move Outside the Playbook

In the previous lecture, variables were defined *inside* the playbook itself using the `vars:` section. That approach works, but it has a fundamental limitation: **reusability**. If the variable values are hardcoded into the playbook, every environment, every group of servers, every individual host gets the same values. You'd need to edit the playbook itself to change values — which defeats the purpose of automation and version-controlled infrastructure.

The solution is **inventory-based variables** — defining variables *outside* the playbook in a structured directory layout that Ansible automatically discovers. This separates the **logic** (what to do) from the **data** (what values to use), and allows different hosts and groups to receive different variable values without touching the playbook at all. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

## 1.2 — The `group_vars` Directory and the `all` File

Ansible has a convention-based variable discovery system. When you create a directory named exactly `group_vars` (this name is not arbitrary — it must be spelled precisely) at the same level as your playbook or inventory, Ansible automatically reads variable files from inside it.

The most fundamental file inside `group_vars` is named **`all`**. This file defines variables that apply to **every host** in your inventory, regardless of which group they belong to. The name `all` corresponds to the implicit Ansible group that always contains every host. If you have `web01`, `web02`, and `db01` in your inventory, variables defined in `group_vars/all` apply to all three.

The file format is simple YAML — each line is a `variable_name: value` pair:

```yaml
db_name: Sky
db_user: pilot
db_pass: Aircraft
```

When a playbook runs and references these variables, Ansible first checks the playbook itself. If the variables are **not** found in the playbook, it looks outward — and `group_vars/all` is one of the places it searches. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

## 1.3 — Group-Level Variable Files

Beyond the `all` file, you can create files inside `group_vars` named after **specific inventory groups**. If your inventory defines a group called `webservers`, you create a file `group_vars/webservers`. Variables in that file apply **only to hosts that belong to the `webservers` group**.

This enables a powerful pattern: shared baseline values in `all`, overridden by group-specific values in group files. For example:

* `group_vars/all` defines `USRNM: common_user` → applies to everyone.
* `group_vars/webservers` defines `USRNM: web_group` → overrides the `all` value, but only for `web01` and `web02`.
* `db01` still gets the `all` file's value because there's no `group_vars/dbservers` file.

The video demonstrates exactly this: after creating the `webservers` file, `web01` and `web02` pick up the group-specific variable, while `db01` falls back to the `all` file. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

> 🔍 **Deep Dive**
> The file name inside `group_vars` must **exactly match** the group name as defined in the inventory. If your inventory group is `webservers`, the file must be `group_vars/webservers` — not `group_vars/web_servers` or `group_vars/Webservers`. Ansible performs exact string matching between inventory group names and file names.

***

## 1.4 — Host-Level Variable Files: `host_vars`

For even finer granularity, Ansible supports a `host_vars` directory. Inside it, you create files named after **individual host names**. Variables defined there apply to **that specific host only** and override both `group_vars/all` and `group_vars/<group_name>`.

The structure: create a directory `host_vars`, then inside it a file named `web02` (matching the exact host name from the inventory). Variables in that file apply exclusively to `web02`.

The video demonstrates this clearly: after creating `host_vars/web02`, the playbook runs and:

* `db01` → uses `group_vars/all` (no group file, no host file).
* `web01` → uses `group_vars/webservers` (group file exists, no host file for `web01`).
* `web02` → uses `host_vars/web02` (host file overrides both group and all). [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

## 1.5 — Variable Precedence: The Priority Hierarchy

This is the central conceptual pillar of the entire video. When the same variable is defined in multiple places, Ansible must decide which value to use. The precedence rules, from **lowest to highest priority**, are:

```
1. group_vars/all          (lowest — applies to everyone, easily overridden)
2. group_vars/<group_name> (overrides all, for specific groups)
3. host_vars/<hostname>    (overrides group, for specific hosts)
4. Playbook vars:          (overrides all external definitions)
5. Command-line -e         (HIGHEST — overrides everything)
```

The video methodically tests each level by defining the same variables with different values at each layer, then running the playbook and observing which value appears in the output. The key findings:

* **Playbook `vars:` override all inventory-based variables.** When variables are defined both in the playbook and in `group_vars`, the playbook wins. Ansible doesn't even look outside when it finds the variable internally.
* **Command-line `-e` overrides even the playbook.** This is the ultimate override — the highest priority of all. The `-e` (or `--extra-vars`) flag passes variables directly on the command line and they supersede everything.
* **In real-world usage**, the video advises: command-line variables are very rarely used (mostly for testing). Variables are rarely defined in the playbook either. **`group_vars/all` is the most common place** to define variables, with group and host files used as needed for specialization. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

> ⚠️ **Expert Note**
> The video mentions that there are *additional* places where variables can be defined beyond these five (the Ansible documentation lists over 20 precedence levels). However, the five covered here represent the most common real-world usage. The instructor recommends starting with `group_vars/all` and expanding to group/host files only as requirements demand. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

## 1.6 — Variable Types: Simple, List, and Dictionary

The video covers three types of variables via the Ansible documentation:

**Simple variables** — A name and a single value. This is what we've been using throughout: `db_name: Sky`. Referenced as `{{ db_name }}`. The video reiterates the earlier rule: when using variables in YAML, the curly brace expression **must be inside quotes** (e.g., `"{{ db_name }}"`) or Ansible will throw a syntax error. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

**List variables** — A single variable name with multiple values, defined vertically with hyphens:

```yaml
region:
  - northeast
  - southeast
  - midwest
```

Accessed by index: `{{ region[0] }}` returns `northeast`, `{{ region[1] }}` returns `southeast`, `{{ region[2] }}` returns `midwest`. Same zero-based indexing as Python.

**Dictionary variables** — Key-value pairs nested under a variable name:

```yaml
foo:
  field1: one
  field2: two
```

Accessed using **dot notation**: `{{ foo.field1 }}` returns `one`. There's an alternative bracket notation (`{{ foo['field1'] }}`), but dot notation is the most commonly used. The video notes dictionaries are useful when you want to **group related variables together** under a single parent name. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

## 1.7 — Registering Output and Accessing Dictionary Keys

When a task executes in Ansible, it produces a result object (a dictionary) containing details about what happened. You capture this using `register`:

```yaml
register: usr_out
```

The registered variable `usr_out` is a dictionary. To access specific values from it, you use dot notation: `usr_out.name` returns the username, `usr_out.comment` returns the comment field. This is the same dictionary access pattern described in §1.6 — the registered output is just another dictionary, and you navigate it with `dictionary.key` syntax.

The video shows that without specifying keys, the `debug` module prints the entire JSON output for all hosts — which is overwhelming. By targeting specific keys (`usr_out.name`, `usr_out.comment`), you extract only the information you need. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

## 1.8 — `vars_files`: Importing External Variable Files into the Playbook

Beyond inventory-based variable files (`group_vars`, `host_vars`), you can also import variable files directly into a playbook using the `vars_files` directive:

```yaml
vars_files:
  - /path/to/variable_file.yml
```

The critical distinction: even though the variables are physically stored in an external file, they are **imported into the playbook**. This means they inherit **playbook-level priority** — higher than `group_vars` and `host_vars`. They are not inventory-based; they are playbook-based variables loaded from an external source. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a variable precedence testing system across two exercises (Exercise 8 continuation and Exercise 9). We create variables at every possible level — `group_vars/all`, `group_vars/<group>`, `host_vars/<host>`, playbook `vars:`, and command line `-e` — and systematically observe which value Ansible selects at each layer. By the end, we have a fully tested understanding of Ansible's variable priority hierarchy and the directory structure needed to use inventory-based variables.

***

## Part A — Exercise 8: Moving Variables from Playbook to `group_vars/all`

### Step 1 — Create the `group_vars` Directory and `all` File

**What we're doing:** Creating the standard directory structure that Ansible looks for when resolving variables externally.

**Actions:**

1. Inside the `exercise8` directory, create a folder named **exactly** `group_vars`:

```bash
mkdir group_vars
```

2. Inside `group_vars`, create a file named **exactly** `all`:

```bash
vim group_vars/all
```

3. Define the three variables with **different values** than the playbook (to test precedence):

```yaml
db_name: Sky
db_user: pilot
db_pass: Aircraft
```

Save and exit. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

**Why different values:** We intentionally use different values than the playbook's variables so we can tell which source Ansible chose by looking at the output.

***

### Step 2 — Run the Playbook with Both Sources Active

**Command:**

```bash
ansible-playbook <playbook_name>.yml -i inventory
```

**Expected output:** The playbook prints the **playbook's** variable values, not the `group_vars/all` values. This confirms: **playbook `vars:` have higher priority than `group_vars/all`**. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

### Step 3 — Comment Out Playbook Variables and Rerun

**Action:** Open the playbook and put `#` (hash) in front of each variable line under `vars:` to comment them out.

**Rerun the playbook:**

```bash
ansible-playbook <playbook_name>.yml -i inventory
```

**Expected output:** Now the values from `group_vars/all` appear (Sky, pilot, Aircraft). With playbook variables removed, Ansible searches externally and finds them in `group_vars/all`. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

**Verification:** The `db_name` should show `Sky` (from `group_vars/all`), not the original playbook value. The debug output confirms this.

***

## Part B — Exercise 9: Full Precedence Testing

### Step 4 — Set Up Exercise 9

**Actions:**

1. Create `exercise9` directory.
2. Remove any leftover files from the copy (db playbook, old group\_vars).
3. Create a new playbook called `vars_precedence.yaml`.

**Playbook content:**

```yaml
- hosts: all
  become: true
  vars:
    USRNM: play_user
    com: "variable from playbook"
  tasks:
    - name: Creating user
      ansible.builtin.user:
        name: "{{ USRNM }}"
        comment: "{{ com }}"
      register: usr_out

    - debug:
        msg:
          - "{{ usr_out.name }}"
          - "{{ usr_out.comment }}"
```

**Breakdown:**

* `hosts: all` — run on every host in inventory.
* `become: true` — user creation requires root privileges (covered in ad hoc commands lecture).
* `vars:` — defines `USRNM` and `com` at playbook level.
* `ansible.builtin.user` — module to create/manage system users.
  * `name:` — the username to create.
  * `comment:` — a comment field on the user account (used here as a tracking label).
* `register: usr_out` — captures the task's output dictionary.
* `debug: msg:` — prints specific keys from the registered dictionary. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

> 🔍 **Deep Dive**
> The first version of the playbook used `debug: var: usr_out` which printed the entire JSON output for all three hosts — too much information. The refined version uses `usr_out.name` and `usr_out.comment` to extract only the relevant fields. This is dictionary key access: `usr_out` is the dictionary, `.name` and `.comment` are keys within it.

***

### Step 5 — Run with Playbook Variables Only

```bash
ansible-playbook vars_precedence.yaml -i inventory
```

**Expected output:** All three hosts (`web01`, `web02`, `db01`) show `play_user` and `variable from playbook`. This is the baseline — playbook variables applied uniformly. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

### Step 6 — Add `group_vars/all` and Test

**Create structure:**

```bash
mkdir group_vars
vim group_vars/all
```

**Content:**

```yaml
USRNM: common_user
com: "variable from group_vars all file"
```

**Run playbook:** Output still shows playbook values → **playbook > group\_vars/all** confirmed.

**Comment out playbook vars** (add `#` before each line), then rerun:

Output now shows `common_user` and `variable from group_vars all file` for all hosts. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

### Step 7 — Add `group_vars/webservers` and Test

**Create the group-specific file:**

```bash
vim group_vars/webservers
```

**Content:**

```yaml
USRNM: web_group
com: "variable from group_vars webservers file"
```

The file name `webservers` must **exactly match** the inventory group name.

**Run playbook (playbook vars still commented out):**

**Expected output:**

* `web01` → `web_group` / `variable from group_vars webservers file`
* `web02` → `web_group` / `variable from group_vars webservers file`
* `db01` → `common_user` / `variable from group_vars all file`

Web servers use the group file; `db01` falls back to `all` because no `dbservers` group file exists. **group\_vars/<group> > group\_vars/all** confirmed. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

### Step 8 — Add `host_vars/web02` and Test

**Create structure:**

```bash
mkdir host_vars
vim host_vars/web02
```

**Content:**

```yaml
USRNM: web02_user
com: "variable from host_vars web02 file"
```

**Run playbook:**

**Expected output:**

* `db01` → `common_user` (from `group_vars/all`)
* `web01` → `web_group` (from `group_vars/webservers`)
* `web02` → `web02_user` (from `host_vars/web02`)

Each host now resolves from a different source. **host\_vars > group\_vars/<group> > group\_vars/all** confirmed. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

### Step 9 — Uncomment Playbook Variables and Test

**Action:** Remove the `#` from the playbook `vars:` section, restoring the original playbook variables.

**Run playbook:**

**Expected output:** All three hosts show `play_user` / `variable from playbook`. The playbook overrides everything external. **playbook > host\_vars > group\_vars** confirmed. [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

***

### Step 10 — Command-Line Override with `-e`

**Command:**

```bash
ansible-playbook vars_precedence.yaml -i inventory -e "USRNM=cli_user" -e "com=CLI user"
```

**Breakdown:**

* `-e` — extra variables flag. Passes variable values directly from the command line.
* `"USRNM=cli_user"` — sets the `USRNM` variable to `cli_user`.
* Each `-e` flag sets one variable. Multiple `-e` flags for multiple variables.

**Expected output:** All three hosts show `cli_user` / `CLI user`. Command-line variables override even playbook variables. **`-e` has the absolute highest priority.** [\[241-group-...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/241-group-and-host-variables.txt)

**Operational note from the video:** Command-line variables are **very rarely used** in real systems. They're primarily for quick testing or one-off overrides. In production, `group_vars/all` is the standard starting point.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Variable Precedence Hierarchy (Highest → Lowest)

```
PRIORITY 1 (HIGHEST):  Command-line  →  -e "VAR=value"
         │
PRIORITY 2:            Playbook vars: / vars_files:
         │
PRIORITY 3:            host_vars/<hostname>
         │
PRIORITY 4:            group_vars/<group_name>
         │
PRIORITY 5 (LOWEST):   group_vars/all
```

```
Resolution logic:  FIND FIRST → STOP LOOKING
  Ansible checks from top → finds variable → uses it → ignores lower layers
```

***

## Directory Structure

```
exercise/
├── playbook.yaml            ← vars: defined inside (Priority 2)
├── inventory
├── group_vars/
│   ├── all                  ← applies to ALL hosts (Priority 5)
│   └── webservers           ← applies to webservers group only (Priority 4)
└── host_vars/
    └── web02                ← applies to web02 only (Priority 3)
```

```
NAMING RULES:
  group_vars/  → exact directory name, no variation
  all          → exact file name, means "every host"
  <group_name> → must EXACTLY match inventory group name
  <hostname>   → must EXACTLY match inventory host name
```

***

## Variable Resolution Per Host (Exercise 9 Final State)

```
                  group_vars/all    group_vars/webservers    host_vars/web02    playbook    -e
db01:                 ✅ ←──────────── (no group file) ──── (no host file) ── (commented) ── (not used)
web01:                               ✅ ←───────────────── (no host file) ── (commented) ── (not used)
web02:                                                      ✅ ←──────────── (commented) ── (not used)

With playbook uncommented:  ALL hosts → playbook values (overrides everything external)
With -e flag:               ALL hosts → CLI values (overrides even playbook)
```

***

## Variable Types

```
Simple:      var_name: value              → {{ var_name }}
List:        var_name:                    → {{ var_name[0] }}  (zero-indexed)
               - val1
               - val2
Dictionary:  var_name:                    → {{ var_name.key }}  (dot notation)
               key1: val1
               key2: val2
```

***

## Registered Output Access Pattern

```
Task executes → produces result dictionary
         │
    register: usr_out     ← captures entire result dict
         │
    usr_out.name          ← dot notation to access specific key
    usr_out.comment       ← another key
    
    debug: var: usr_out   → prints ENTIRE dict (noisy)
    debug: msg: "{{ usr_out.name }}"  → prints SPECIFIC value (clean)
```

***

## Scope Layering Model

```
NARROW SCOPE (specific)                    HIGH PRIORITY
    │                                          │
    │  host_vars/web02    → only web02         │
    │  group_vars/webservers → web01 + web02   │
    │  group_vars/all     → everyone           │
    ▼                                          ▼
WIDE SCOPE (general)                       LOW PRIORITY

PATTERN: More specific scope = higher priority
         Narrower target = wins over broader target
```

***

## Real-World Usage Guidance (from video)

```
COMMON:       group_vars/all         ← start here, define most variables
WHEN NEEDED:  group_vars/<group>     ← override for specific server roles
WHEN NEEDED:  host_vars/<host>       ← override for individual servers
RARE:         playbook vars:         ← tightly coupled, less reusable
VERY RARE:    -e command line        ← testing/debugging only

vars_files: /path/to/file.yml       ← external file BUT imported into playbook
                                        → inherits PLAYBOOK-level priority
```

***

## Testing Methodology (Reusable)

```
1. Define SAME variable at MULTIPLE levels with DIFFERENT values
2. Run playbook → observe which value appears
3. Remove highest-priority source → rerun → next level takes over
4. Repeat until all levels tested

KEY: use distinguishable values (e.g., embed source name in comment field)
     so output immediately reveals which source won
```

***

## YAML Variable Syntax Reminder

```
Referencing:   "{{ variable_name }}"     ← MUST be in quotes in YAML
Without quotes → YAML parser error

Commenting:    # in front of line        ← disables variable/line
```

***

## Cause → Effect Chains

```
No group file for a group  →  falls back to group_vars/all
No host file for a host    →  falls back to group file → then all
Playbook vars present      →  external files ignored entirely
-e flag used               →  everything else overridden

Variable name mismatch between file and playbook  →  variable not found  →  error
File name mismatch with inventory group/host      →  file ignored silently
```

***

This completes the full reconstruction. Theory explains *why* the precedence system exists, Practical walks through *every test* that proves it, and the Compression Map enables instant *recall* of the hierarchy and structure. Let me know if you'd like AnkiDeck cards generated from this, or if you're ready for the next lecture! 🚀
