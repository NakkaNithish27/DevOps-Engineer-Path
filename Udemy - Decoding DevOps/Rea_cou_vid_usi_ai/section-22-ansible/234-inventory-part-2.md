# Ansible Inventory Part 2 — Grouping, Variables, and Multi-Host Management

**Source:** Video caption file — *"Inventory Part 2"* (from an Ansible / DevOps course) [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Scaling Beyond a Single Host

In the previous lecture, the inventory file was set up with a single host. That works for learning, but in any real environment you have many machines — 10, 20, 50, or hundreds. The moment you have multiple hosts, two problems emerge: **how do you organize them?** and **how do you execute tasks against logical groups of them without targeting each one individually?** [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

This lecture solves both problems through Ansible's **grouping** and **variable inheritance** mechanisms in the inventory file.

***

## 1.2 — Adding Multiple Hosts to Inventory

Adding more hosts to an inventory file follows the exact same pattern as the first host. Each host entry needs a name (like `web01`, `web02`, `db01`) and its connection details. The minimum required detail is the `ansible_host` variable — the private IP address of the machine. If the username and login key are the same across hosts, they're repeated for each host (for now — this repetition is addressed later with group variables). [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

The structure is YAML-based, and the video repeatedly emphasizes: **"YAML space is very important. In the same column I should say, not line."** Every host entry must be at the same indentation level. Every variable under a host must be indented consistently. A single misaligned space in YAML breaks the entire file. This is the most common source of errors when editing Ansible inventory files. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

Each host has a unique IP address, but all other connection parameters (username, SSH key path) may be identical — which creates visible redundancy. This redundancy is the motivation for group-level variables, covered later in this lecture. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## 1.3 — Grouping: Organizing Hosts into Logical Units

Grouping is Ansible's mechanism for organizing hosts into logical collections that can be targeted as a single unit. Instead of running a command against `web01`, then `web02`, then `web03` individually, you create a group called `webservers` containing all three, and run the command against `webservers` once. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

Groups are defined in the inventory file under a `children:` section at the same indentation level as the `hosts:` section. Inside `children:`, you define group names, and under each group name you specify a `hosts:` section listing which hosts belong to that group. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

The hosts referenced in a group **must already be defined** in the `hosts:` section at the top of the inventory file. The group doesn't redefine the host — it references the host by name. The host's connection details (IP, username, key) come from its definition in the `hosts:` section. The group simply creates a named collection of those hosts. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

In the video, two groups are created:

* **`webservers`** — contains `web01` and `web02`
* **`dbservers`** — contains `db01` [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

A group can contain a single host or multiple hosts. There's no minimum size requirement. The `dbservers` group has only one host (`db01`), which is perfectly valid — the grouping still provides a logical label for targeting. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## 1.4 — Parent Groups: Group of Groups

Ansible supports **hierarchical grouping** — a group can contain other groups instead of (or in addition to) hosts. This is called a parent group. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

In the video, a parent group called `dc_oregon` is created. Instead of listing hosts directly, its `children:` section lists the group names `webservers` and `dbservers`. When you target `dc_oregon`, Ansible resolves the children groups, finds all hosts within those groups, and executes against all of them. So `dc_oregon` effectively targets all three hosts (`web01`, `web02`, `db01`) through the two child groups. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

The resolution is recursive: parent group → finds child groups → finds hosts in each child group. The parent group's children **must be group names**, not host names. Ansible "will look for this group here and find the hosts from that group." [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Naming convention warning:** The video initially uses a hyphen (`-`) in the group name `dc-oregon` and immediately corrects: "'-' is not at all recommended. It'll give you a warning or it may also give you error if you're using a different version of Ansible. So don't use '-', you can use '\_'." The correct name is `dc_oregon` with an underscore. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**YAML syntax detail:** Host names and group names referenced inside `children:` sections must end with a colon (`:`). The video explicitly adds colons to `web01:`, `web02:`, `db01:`, `webservers:`, `dbservers:`, and `dc_oregon:`. This is YAML mapping syntax — each entry is a key (potentially with sub-keys), and keys require trailing colons. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

🔍 **Deep Dive:**
The hierarchical grouping creates a tree structure:

```
dc_oregon (parent group)
  ├── webservers (child group)
  │     ├── web01 (host)
  │     └── web02 (host)
  └── dbservers (child group)
        └── db01 (host)
```

This maps to real infrastructure organization: `dc_oregon` could represent a data center or AWS region, `webservers` and `dbservers` represent functional roles within that data center. You can target any level of the tree — a single host, a role group, or the entire data center. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## 1.5 — Targeting: How to Select Which Hosts to Execute Against

Once groups exist, Ansible provides multiple ways to select which hosts a command targets. The video demonstrates all of them using the `ping` module: [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**By host name:** `ansible web02 ...` — targets a single specific host.

**By group name:** `ansible webservers ...` — targets all hosts in the `webservers` group (two hosts: `web01`, `web02`). The group name must match exactly what's defined in the inventory file — "make sure the group name is correct as whatever is mentioned in the inventory file, otherwise it won't work." [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**By parent group name:** `ansible dc_oregon ...` — targets all hosts in all child groups of `dc_oregon` (all three hosts).

**By `all`:** `ansible all ...` — targets every host defined in the inventory file. The keyword `all` is a built-in Ansible target that refers to the top-level `all:` group in the inventory, which implicitly contains every host.

**By `*` (wildcard):** `ansible '*' ...` — also means all hosts. The asterisk must be in **single quotes** to prevent shell interpretation.

**By pattern:** `ansible 'web*' ...` — targets any host whose name starts with `web`. This uses pattern matching similar to Linux shell globbing. `web*` matches `web01` and `web02` but not `db01`. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

The video notes: "This is not just about ping. Any module like that you can execute for the group." The targeting mechanism is universal — it works with every Ansible module, not just `ping`. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## 1.6 — Variables: Host-Level vs. Group-Level and Priority

This is described as "a very simple concept, but very very important concept." Variables in Ansible can be defined at different levels, and each level has a **priority** that determines which value wins when the same variable is defined at multiple levels. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Host-level variables** are defined directly under each host in the `hosts:` section. In the initial setup, each host had `ansible_user` and `ansible_ssh_private_key_file` defined individually. Host-level variables have the **highest priority**. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Group-level variables** are defined under a group using the `vars:` section. Instead of repeating the same username and SSH key path under every host, you define them once at the group level, and every host in that group inherits those values. Group-level variables have **lower priority** than host-level variables. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**The priority rule:** If a variable is defined at both the host level and the group level, the **host-level value wins**. Ansible first checks if the variable exists at the host level. If yes, it uses that value. If no, it falls back to the group level. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

The video demonstrates this by defining `ansible_user` and `ansible_ssh_private_key_file` at the `dc_oregon` group level, then **removing** those variables from each individual host. After removal, each host only has `ansible_host` (the IP address) — the login credentials are inherited from the group. This eliminates the repetition that existed when every host had its own copy of the same username and key path. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

The practical benefit is significant: if you have 50 hosts that all use the same SSH key and username, you define those variables once at the group level instead of 50 times at the host level. If the key changes, you update one place instead of 50. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

⚠️ **Expert Note:**
The video introduces the basic two-level priority (host > group). In full Ansible, variable precedence has many more levels — inventory variables, playbook variables, role defaults, role variables, extra variables from the command line, and more. The principle remains the same: more specific overrides less specific. Host is more specific than group. Understanding this two-level model is the foundation for understanding the full precedence system in later lectures. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## 1.7 — Debugging: Permission Denied Errors

The video deliberately introduces a wrong username to demonstrate error diagnosis. When the `ansible_user` is changed to an incorrect value (`ec2-` instead of `ec2-user`), the `ping` module fails with **"permission denied."** [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

The diagnostic rule: "Permission denied you'll get if the username or the login key — any of this is wrong, or both of them are wrong." A `permission denied` error in Ansible always points to authentication failure, which means either: [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

1. The username (`ansible_user`) is wrong.
2. The SSH private key path (`ansible_ssh_private_key_file`) is wrong or the key doesn't match.
3. Both are wrong.

This is the first debugging pattern for Ansible connectivity: if `ping` fails with permission denied, check your authentication variables — at whatever level they're defined (host or group). [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are expanding the Ansible inventory from a single host to multiple hosts, organizing them into groups and a parent group, moving shared variables to the group level to eliminate repetition, and testing connectivity against groups and patterns. The final outcome: a cleanly organized inventory file where three hosts (`web01`, `web02`, `db01`) are grouped into `webservers` and `dbservers`, rolled up into a parent group `dc_oregon`, with shared login credentials defined once at the group level. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Exercise Setup

The video uses an exercise-based workflow. Each exercise builds on the previous one by copying the directory:

```bash
cp -r exercise1 exercise2
cd exercise2
```

And later:

```bash
cp -r exercise2 exercise3
```

This preserves previous work while creating a clean workspace for new concepts. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

### Step 1: Add Multiple Hosts to the Inventory File

**What we are doing:** Adding `web02` and `db01` to the inventory file that previously only had `web01`.

**Execution:**

1. Open the inventory file in vim.
2. The existing `web01` entry has four lines: the host name, `ansible_host` (IP), `ansible_user`, and `ansible_ssh_private_key_file`.
3. Copy these four lines using vim: position cursor on the first line of `web01`, type `4yy` (yank 4 lines), go to the last line, type `P` (paste). Repeat for the third host. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)
4. Change the host names: `web01` → `web02` for the second block, `web01` → `db01` for the third block.
5. **Update the IP addresses** — each host has a different private IP:
   * Go to the AWS console or wherever your instances are running.
   * Get the **private IP** of `web02` and replace the IP in its `ansible_host` line.
   * Get the **private IP** of `db01` and replace its IP. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Critical formatting rule:** "Make sure they are all in the same column. YAML space is very important." Every host name must be at the same indentation level. Every variable under a host must be at the same deeper indentation level. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**What stays the same:** The `ansible_user` and `ansible_ssh_private_key_file` values are identical across all three hosts (same username, same SSH key). Only the `ansible_host` (IP address) differs per host.

***

### Step 2: Test Individual Hosts

**What we are doing:** Verifying connectivity to each newly added host using the `ping` module.

```bash
ansible web02 -m ping -i inventory
```

```bash
ansible db01 -m ping -i inventory
```

**Expected output:** `SUCCESS` with `"ping": "pong"` for each host.

**Why we test individually first:** Before building groups, confirm that each host's connection details are correct. If a host fails at this stage, the problem is in its specific `ansible_host`, `ansible_user`, or `ansible_ssh_private_key_file` values. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**The scaling problem:** "But what if like this you have 10, 20, 50, and like that many, many hosts? Doing a ping to each and every machine is going to take like forever." This motivates the grouping concept that follows.

***

### Step 3: Create Groups in the Inventory File

**What we are doing:** Adding group definitions under the `children:` section.

**Inventory structure to add** (below the existing `hosts:` section, at the same indentation level):

```yaml
  children:
    webservers:
      hosts:
        web01:
        web02:
    dbservers:
      hosts:
        db01:
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Breakdown:**

* `children:` — at the same indentation level as `hosts:` (two spaces from the left edge). This tells Ansible that groups are being defined.
* `webservers:` — a group name. Indented inside `children:`.
* `hosts:` — inside `webservers:`, specifies which hosts belong to this group.
* `web01:` and `web02:` — the host names (must match exactly the names defined in the `hosts:` section above). **Must end with a colon** `:`. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)
* `dbservers:` — second group, with `db01:` as its only host.

**Common mistake:** Forgetting the trailing colon on host names inside groups. In YAML, these are mapping keys and require colons.

**Common mistake:** Indentation mismatch. Every level must be consistently indented (the video uses 2-space indentation throughout). [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

### Step 4: Create a Parent Group (Group of Groups)

**What we are doing:** Creating `dc_oregon` as a parent group containing `webservers` and `dbservers`.

**Add to the inventory file** (at the same level as `webservers:` and `dbservers:` inside `children:`):

```yaml
    dc_oregon:
      children:
        webservers:
        dbservers:
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Breakdown:**

* `dc_oregon:` — the parent group name. **Use underscores, NOT hyphens.** `dc-oregon` will give warnings or errors depending on Ansible version.
* `children:` — inside `dc_oregon`, this tells Ansible that its members are groups (not hosts).
* `webservers:` and `dbservers:` — the child group names. Ansible resolves these to find all hosts within them. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Naming warning:** "'-' is not at all recommended. It'll give you a warning or it may also give you error if you're using a different version of Ansible. So don't use '-', you can use '\_'." [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

### Step 5: Test Groups

**What we are doing:** Running the `ping` module against groups and patterns instead of individual hosts.

**By group name:**

```bash
ansible webservers -m ping -i inventory
```

**Expected output:** Two hosts respond (`web01` and `web02`). [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

```bash
ansible dbservers -m ping -i inventory
```

**Expected output:** One host responds (`db01`). [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**By parent group:**

```bash
ansible dc_oregon -m ping -i inventory
```

**Expected output:** All three hosts respond. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**By `all`:**

```bash
ansible all -m ping -i inventory
```

**Expected output:** All hosts in the inventory respond. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**By wildcard `*`:**

```bash
ansible '*' -m ping -i inventory
```

**Expected output:** Same as `all`. The `*` must be in **single quotes** to prevent shell expansion. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**By pattern:**

```bash
ansible 'web*' -m ping -i inventory
```

**Expected output:** Only hosts whose names start with `web` respond (`web01`, `web02`). `db01` does not match and is excluded. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Common mistake:** Misspelling the group name. If the group name in the command doesn't match the inventory file exactly, Ansible reports no hosts matched.

***

### Step 6: Move Variables to Group Level (Exercise 3)

**What we are doing:** Eliminating variable repetition by defining shared variables at the `dc_oregon` group level instead of at each individual host.

**Setup:**

```bash
cp -r exercise2 exercise3
cd exercise3
```

**Edit the inventory file:**

1. Under the `dc_oregon:` group, at the same indentation level as `children:`, add `vars:`:

```yaml
    dc_oregon:
      children:
        webservers:
        dbservers:
      vars:
        ansible_user: ec2-user
        ansible_ssh_private_key_file: /path/to/key
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

2. **Remove** `ansible_user` and `ansible_ssh_private_key_file` from each individual host (`web01`, `web02`, `db01`). Each host should now only have `ansible_host` (the IP address). [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Why this works:** When Ansible connects to a host, it checks the host level first for variables. Since `ansible_user` and `ansible_ssh_private_key_file` are no longer at the host level, Ansible falls back to the group level (`dc_oregon`) and finds them there. All three hosts inherit the same values.

**How to verify:**

```bash
ansible all -m ping -i inventory
```

**Expected output:** `SUCCESS` for all three hosts — confirming that group-level variables are being used for authentication. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

### Step 7: Verify Variable Priority (Deliberate Error Test)

**What we are doing:** Proving that group-level variables are actually being used by introducing a deliberate error.

**Test:** Change the `ansible_user` at the group level to an incorrect value (e.g., `ec2-`):

```yaml
      vars:
        ansible_user: ec2-
```

Run the ping:

```bash
ansible all -m ping -i inventory
```

**Expected output:** All three hosts **fail** with **"permission denied."** This proves Ansible is using the group-level variable — if it weren't, the error wouldn't occur. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Error diagnosis:** "Permission denied you'll get if the username or the login key — any of this is wrong, or both of them are wrong." [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Recovery:** Change `ansible_user` back to `ec2-user`. Re-run the ping. All hosts should succeed again. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

**Connection to flow:** This lecture focused entirely on the inventory file and used the simple `ping` module for testing. The next lectures will use modules that make actual changes to the managed machines — installing packages, managing services, managing files. [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Ansible Inventory — Part 2
PURPOSE:  Multi-host management, grouping, variable inheritance
CONTEXT:  Builds on single-host inventory from Part 1
MODULE:   ping (for connectivity testing only)
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Inventory File Structure (Complete)

```yaml
all:
  hosts:
    web01:
      ansible_host: <private_IP_1>      ← unique per host
    web02:
      ansible_host: <private_IP_2>      ← unique per host
    db01:
      ansible_host: <private_IP_3>      ← unique per host
  children:
    webservers:
      hosts:
        web01:
        web02:
    dbservers:
      hosts:
        db01:
    dc_oregon:                          ← parent group (group of groups)
      children:
        webservers:
        dbservers:
      vars:                             ← group-level variables
        ansible_user: ec2-user
        ansible_ssh_private_key_file: /path/to/key
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Group Hierarchy (Tree)

```
all (implicit top-level)
 └── dc_oregon (parent group)
       ├── webservers (child group)
       │     ├── web01
       │     └── web02
       └── dbservers (child group)
             └── db01

RESOLUTION:
  dc_oregon → children → webservers + dbservers → web01, web02, db01
  Ansible resolves groups recursively to find hosts
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Targeting Methods

```
METHOD          COMMAND SYNTAX              TARGETS
──────────      ────────────────            ───────
Single host     ansible web02 ...           web02 only
Group           ansible webservers ...      web01 + web02
Parent group    ansible dc_oregon ...       web01 + web02 + db01
All hosts       ansible all ...             every host in inventory
Wildcard        ansible '*' ...             same as all (single quotes!)
Pattern         ansible 'web*' ...          hosts starting with "web"
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Variable Priority (Precedence)

```
HOST LEVEL (highest priority)
    │
    │  If variable found at host level → USE IT
    │  If NOT found at host level ↓
    │
    ▼
GROUP LEVEL (lower priority)
    │
    │  Use group-level value as fallback

RESULT:
  Host-specific values (like IP) → define at HOST level
  Shared values (like username, key) → define at GROUP level
  If both exist → HOST wins
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Variable Deduplication Pattern

```
BEFORE (repetitive):
  web01:
    ansible_host: 10.0.0.1
    ansible_user: ec2-user           ← repeated
    ansible_ssh_private_key_file: …  ← repeated
  web02:
    ansible_host: 10.0.0.2
    ansible_user: ec2-user           ← repeated
    ansible_ssh_private_key_file: …  ← repeated
  db01:
    ansible_host: 10.0.0.3
    ansible_user: ec2-user           ← repeated
    ansible_ssh_private_key_file: …  ← repeated

AFTER (DRY):
  web01:
    ansible_host: 10.0.0.1           ← unique only
  web02:
    ansible_host: 10.0.0.2           ← unique only
  db01:
    ansible_host: 10.0.0.3           ← unique only
  dc_oregon:
    vars:
      ansible_user: ec2-user         ← defined ONCE
      ansible_ssh_private_key_file: … ← defined ONCE
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## YAML Rules (Critical)

```
INDENTATION:
  Same level = same column (2-space indent per level)
  Misaligned space = broken file

COLONS:
  Host names in groups → must end with :   (web01:)
  Group names → must end with :            (webservers:)
  Variable keys → must end with :          (ansible_user:)

NAMING:
  ❌ dc-oregon  (hyphen → warning/error)
  ✅ dc_oregon  (underscore → safe)
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Debugging: Permission Denied

```
ansible all -m ping -i inventory → PERMISSION DENIED

CAUSE: authentication failure
  ├── ansible_user is wrong
  ├── ansible_ssh_private_key_file is wrong/missing
  └── or BOTH are wrong

CHECK:
  1. Is the username correct? (ec2-user, ubuntu, etc.)
  2. Is the key path correct?
  3. At which level are they defined? (host or group)
  4. Is host-level overriding group-level unintentionally?
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Exercise Workflow Pattern

```
cp -r exercise1 exercise2    ← preserve previous, create new workspace
cd exercise2                  ← work in isolated copy

cp -r exercise2 exercise3    ← next exercise builds on previous
cd exercise3

PATTERN: Incremental, non-destructive progression
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Execution Sequence (This Lecture)

```
1. Copy exercise1 → exercise2
2. Add web02, db01 to inventory (IPs from AWS)
3. Test each host individually (ansible <host> -m ping)
4. Add groups: webservers, dbservers
5. Add parent group: dc_oregon
6. Test groups (ansible webservers/dbservers/dc_oregon/all/'*'/'web*' -m ping)
7. Copy exercise2 → exercise3
8. Move ansible_user + key to dc_oregon vars:
9. Remove from individual hosts
10. Test all → SUCCESS
11. Deliberately break username → permission denied
12. Fix → SUCCESS (proves group vars work)
```

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## Reusable Engineering Patterns

| Pattern                                | Manifestation                                                            |
| -------------------------------------- | ------------------------------------------------------------------------ |
| **Hierarchical Grouping**              | Hosts → groups → parent groups = tree targeting at any level             |
| **DRY (Don't Repeat Yourself)**        | Shared variables defined once at group level, not per host               |
| **Priority / Specificity Override**    | Host-level > group-level — more specific wins                            |
| **Pattern Matching for Targeting**     | `web*`, `*`, `all` — select hosts by name patterns                       |
| **Deliberate Error Testing**           | Break a value intentionally → verify the system uses that value          |
| **Incremental Exercise Isolation**     | `cp -r` previous → work in copy → preserves rollback point               |
| **Separation of Identity from Config** | Host-level: unique identity (IP). Group-level: shared config (user, key) |
| **Recursive Resolution**               | Parent group → child groups → hosts (tree traversal for targeting)       |

 [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

## One-Line System Reconstruction

> **Ansible inventory organizes multiple hosts under `hosts:` with unique IPs, groups them via `children:` into functional groups (`webservers`, `dbservers`) and parent groups (`dc_oregon` with nested `children:`), targets them by host/group/pattern/`all`/`*`/`web*`, and eliminates variable repetition by defining shared credentials in group-level `vars:` which are inherited by all member hosts — with host-level variables always overriding group-level when both exist.** [\[234-inventory-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/234-inventory-part-2.txt)

***

This completes the full reconstruction of the Ansible Inventory Part 2 lecture. It builds directly on Part 1 (single host setup) and establishes the inventory organization patterns needed for all subsequent Ansible lectures — where modules will be used to make real changes (installing packages, managing services, managing files) against these grouped hosts. Let me know if you'd like any section expanded or adjusted! 🚀
