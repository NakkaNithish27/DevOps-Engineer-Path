# 🎓 Complete Deep Learning Material — Linux Users and Groups: Access Control Architecture, User Management, and Group Operations

**Source:** [30-users-and-groups.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt?EntityRepresentationId=84e0152e-911f-4e51-ba5c-f6635fd2c3da) — Comprehensive lecture on Linux user and group management, covering the three user types, critical system files (`/etc/passwd`, `/etc/shadow`, `/etc/group`), user/group creation and deletion, password management, user switching, and operational inspection commands. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Fundamental Purpose of Users and Groups

In Linux, **users and groups exist to control access** to files and resources. The instructor expands "resources" to include programs, processes, and essentially everything on the system — because in Linux, **everything is a file**. Every process is represented by a file (in `/proc`), every device is a file (in `/dev`), every configuration is a file. Therefore, controlling access to files means controlling access to the entire system. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

The access control model works like this: **every file in the system is owned by a user and has an associated group.** You then control access by specifying how much permission (authorization) that user and group have over the file. This lecture focuses on the user and group side of this equation; file permissions and `sudo` are covered separately, and the instructor explicitly states that the real power of users and groups becomes clear when combined with those topics. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 1.2 — User Identity: UID and the `/etc/passwd` File

Every user in Linux has a **unique user ID (UID)** — a numeric identifier that the system actually uses internally. Usernames are human-friendly labels; the kernel works with UIDs. All user information — UID, home directory, login shell, group association — is stored in the **`/etc/passwd`** file. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

The `/etc/passwd` file has **seven columns** per line, separated by colons: [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

| Column | Content                | Example (root)            | Example (vagrant) |
| ------ | ---------------------- | ------------------------- | ----------------- |
| 1      | Username               | `root`                    | `vagrant`         |
| 2      | Password link          | `x` (link to shadow file) | `x`               |
| 3      | User ID (UID)          | `0`                       | `1000`            |
| 4      | Primary Group ID (GID) | `0`                       | `1000`            |
| 5      | Comment/description    | `root`                    | (comment)         |
| 6      | Home directory         | `/root`                   | `/home/vagrant`   |
| 7      | Login shell            | `/bin/bash`               | `/bin/bash`       |

The second column is always `x` for all users — this is not the actual password. The `x` means the password is stored elsewhere, in the **`/etc/shadow`** file. This separation is a security design: `/etc/passwd` is readable by all users (it needs to be, for name-to-UID lookups), but `/etc/shadow` is restricted to root only. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 1.3 — The `/etc/shadow` File

The `/etc/shadow` file stores the **encrypted password** for each user, along with password-related metadata: expiry dates, password age, and other security parameters. The instructor mentions this file briefly — it holds "encrypted password and some other information like expiry of the user." The critical design point is the **separation of identity (`/etc/passwd`) from credentials (`/etc/shadow`)** for security. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

> 🔍 **Deep Dive:** This separation exists because many system processes need to look up user information (username ↔ UID mapping), and making `/etc/passwd` world-readable enables that. If passwords were stored in `/etc/passwd`, every user on the system could read everyone else's encrypted passwords and attempt offline cracking. The shadow file architecture eliminates this attack surface by isolating credentials in a root-only file.

***

## 1.4 — The Three Types of Users

Linux categorizes users into **three distinct types**, each with different UID ranges, purposes, and capabilities: [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Root User (UID 0)

The **root** user is the superuser — the single most powerful account on the system. Its UID is `0`, its GID is `0`, its home directory is `/root` (not `/home/root`), and its login shell is `/bin/bash`. Root has **unrestricted access** to everything on the system. There is exactly one root user, and its identity is always UID 0. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

A critical privilege demonstrated later: root can switch to **any** user with `su - username` **without needing that user's password**. This is because root's authority bypasses all access checks. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Regular Users (UID 1000+)

Regular users are the **human login accounts** — the people who actually use the system. Examples include `vagrant`, `imran`, or any user you create for a person. Their UIDs start at **1000 and go upward** (these are default ranges, configurable if needed). They have group IDs also starting at **1000+**, a home directory under `/home/` (e.g., `/home/vagrant`), and a login shell like `/bin/bash`. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Service/System Users (UID 1–999)

Service users (also called system users) are accounts created **for processes, not people**. Examples include `ftp`, `sshd` (for the SSH daemon), `apache` (for the web server), and others. When you install server packages (web server, database server, etc.), a service user is automatically created for that software. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

Their UIDs range from **1 to 999**, and their GIDs also range from **1 to 999**. Their home directories are often in `/var` or `/etc`, or may not even have a proper home directory at all. Critically, their login shell is set to **`/sbin/nologin`** or **`/sbin/false`** — this is a deliberate security measure. If someone gains access to these credentials, they **cannot get a shell** to execute commands. These users also typically have **no password set**. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

> 🔍 **Deep Dive:** The reason service users exist at all (rather than running everything as root or as a regular user) is the **principle of least privilege**. If a web server process runs as root and gets compromised, the attacker has root access to the entire system. If it runs as the `apache` user with limited permissions, the blast radius is contained. The nologin shell and absence of password create **two layers of defense**: even if the account is somehow accessed, there's no shell to exploit and no password to authenticate with. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 1.5 — Groups and the `/etc/group` File

Every user belongs to at least one group. Groups are a mechanism for **collective access control** — instead of granting permissions to each user individually, you grant permissions to a group and then add users to that group. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

Group information is stored in the **`/etc/group`** file. Its structure is: `groupname:x:GID:members`. After the GID, a comma-separated list of usernames shows which users belong to that group. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Primary Group vs. Supplementary (Secondary) Groups

Every user has exactly **one primary group**. This is the group specified in column 4 of `/etc/passwd` (the GID field). When a user creates a file, the file's group ownership is set to the user's primary group by default. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

A user can also belong to **additional groups** called supplementary or secondary groups. These provide extra access beyond the primary group. The `id` command shows both: for example, `id vagrant` reveals that vagrant belongs to its primary group `vagrant` and also to the supplementary group `wheel`. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### The Name-Matching Convention

The video highlights a pattern that initially seems confusing but is actually simple: **when you create a user, a group with the same name and the same ID is automatically created.** So user `ansible` (UID 1001) gets a primary group `ansible` (GID 1001). The username and group name are the same, the UID and GID are the same — but they are fundamentally **different entities** stored in different files (`/etc/passwd` vs. `/etc/group`). The instructor acknowledges this is "confusing" at first but says "it's really very easy to understand" once you see them as separate systems that happen to share naming conventions. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 1.6 — Password Management and User Switching

### Setting Passwords with `passwd`

Newly created users have **no password** by default — nobody can log in as them from outside the system. The `passwd` command sets (or resets) a user's password. When run as root (`passwd ansible`), root can set any user's password. This is also how you **reset** a forgotten password — but only root can do this. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### User Switching with `su -`

The `su -` command switches your identity to another user. The behavior depends on **who you currently are**: [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

* **Root → any user:** No password required. Root's authority is absolute; it bypasses authentication. `su - ansible` switches to ansible immediately.
* **Normal user → another normal user:** Password required. You must know the target user's password. `su - aws` from the ansible user prompts for aws's password. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

The `-` flag after `su` is important — it simulates a full login, loading the target user's environment, home directory, and shell configuration. Without `-`, you switch user identity but may retain the previous user's environment, which can cause subtle issues.

The `exit` command returns you to the previous user, following the **stack-based session model**: each `su -` pushes a new layer, and `exit` pops it. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 1.7 — User Inspection Commands

The video introduces several commands for **observing user state** on the system: [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

* **`id <username>`** — Shows the user's UID, primary GID, and all groups (primary + supplementary). This is the primary command for inspecting a user's identity and group memberships.
* **`last`** — Shows the history of user logins to the system, including timestamps. Useful for auditing who accessed the system and when.
* **`who`** — Shows currently logged-in users.
* **`whoami`** — Shows the username of the current session.
* **`lsof -u <username>`** — Lists all files currently opened by a specific user. The instructor presents this as a **pre-deletion safety check**: before deleting a user or performing serious user operations, check what files they have open. If `lsof -u aws` returns nothing, that user isn't logged in or actively using anything. If it returns results, you need to consider the impact. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

> ⚠️ **Expert Note:** `lsof` may not be installed by default. The video shows installing it with `yum install lsof -y`. In production, `lsof -u` is invaluable for troubleshooting — it tells you which processes a user has running, which files they're holding open (potentially blocking deletions or unmounts), and whether a supposedly "inactive" user actually has live sessions.

***

## 1.8 — Deleting Users and Groups

User and group deletion has **two levels of thoroughness**: [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**`userdel <username>`** — Deletes the user account but **leaves the home directory and mail spool intact.** The user entry is removed from `/etc/passwd` and `/etc/shadow`, but `/home/username` still exists on disk.

**`userdel -r <username>`** — Deletes the user **and** removes the home directory and mail spool. This is the clean, complete deletion.

**`groupdel <groupname>`** — Deletes a group from `/etc/group`.

If you used `userdel` (without `-r`) and the home directory remains, you must manually clean it up: `rm -rf /home/username`. The video demonstrates this for the `aws` user. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

> 🔍 **Deep Dive:** The reason `userdel` doesn't delete the home directory by default is **data safety**. The home directory may contain important files, and deleting a user doesn't necessarily mean you want to destroy their data. The `-r` flag is an explicit "I'm sure, delete everything" confirmation. This follows the same conservative design philosophy seen in `cp` and `rm` requiring `-r` for recursive operations — destructive actions require explicit intent.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning to **create, inspect, manage, and delete users and groups** on a Linux system. By the end, you will be able to add users, assign them to groups (using two different methods), set passwords, switch between users, inspect user activity, and cleanly remove users and groups. The final operational outcome is **full command-line competency for Linux identity management.** [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## Step 1 — Log In and Switch to Root

```bash
vagrant ssh
sudo -i
```

All user management commands require **root privileges**. Switch to root before proceeding. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Verification:** `whoami` should output `root`.

***

## Step 2 — Examine the `/etc/passwd` File

### View the entire file:

```bash
cat /etc/passwd
```

### View a single user's entry (root):

```bash
head -1 /etc/passwd
```

* **`head -1`** — shows only the first line of the file
* Output shows 7 colon-separated columns: `root:x:0:0:root:/root:/bin/bash` [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Search for a specific user:

```bash
grep vagrant /etc/passwd
```

* **`grep`** — searches for a text pattern in a file
* **`vagrant`** — the pattern to match
* **`/etc/passwd`** — the file to search in [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Expected output:** `vagrant:x:1000:1000:vagrant:/home/vagrant:/bin/bash`

**How to read it:** username (`vagrant`), password link (`x` → shadow file), UID (`1000`), primary GID (`1000`), comment, home dir (`/home/vagrant`), login shell (`/bin/bash`). [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

Observe the **system/service users** in the file — entries like `bin`, `daemon`, `adm`, `lp`, `sshd`. Notice their UIDs are below 1000 and their login shells are `/sbin/nologin`. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Connection to flow:** Understanding this file structure is essential for interpreting user operations throughout the rest of the lecture.

***

## Step 3 — Examine the `/etc/group` File

```bash
grep vagrant /etc/group
```

**Expected output:** `vagrant:x:1000:vagrant`

**How to read it:** group name (`vagrant`), password placeholder (`x`), GID (`1000`), members (`vagrant`). [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Key observation:** The username and group name are the same (`vagrant`), and UID and GID are the same (`1000`). These are separate entities in separate files — the group was auto-created when the user was created. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

Also check:

```bash
grep root /etc/group
```

***

## Step 4 — Inspect a User with `id`

```bash
id vagrant
```

**Breakdown:**

* **`id`** — displays identity information for a user
* **`vagrant`** — the target username [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Expected output:** Shows UID, primary GID, and all group memberships (primary + supplementary). The vagrant user belongs to group `vagrant` (primary) and group `wheel` (supplementary). [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## Step 5 — Create Users with `useradd`

```bash
useradd ansible
useradd jenkins
useradd aws
```

**Breakdown:**

* **`useradd`** — creates a new user account
* **`ansible`** / **`jenkins`** / **`aws`** — the username to create (can be any name) [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**What happens internally for each:** A new entry is added to `/etc/passwd`, a new entry is added to `/etc/shadow`, a **primary group with the same name** is automatically created in `/etc/group`, and a home directory is created under `/home/`. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Verification:**

```bash
tail -4 /etc/passwd
```

* **`tail -4`** — shows the last 4 lines of the file
* You should see the three new users listed at the bottom [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

Also verify groups:

```bash
tail -4 /etc/group
```

You should see matching group entries auto-created for each user. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

```bash
id ansible
```

Confirms the UID, GID, and group memberships for the new user.

**Connection to flow:** Users are created, but they have **no password** yet — nobody can log in as them. Groups exist but are only primary groups — no shared group yet.

***

## Step 6 — Create a Custom Group

```bash
groupadd devops
```

**Breakdown:**

* **`groupadd`** — creates a new group
* **`devops`** — the group name [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**What happens internally:** A new entry is added to `/etc/group` with an auto-assigned GID and no members initially.

**Connection to flow:** This group will be used to demonstrate adding users to a shared supplementary group.

***

## Step 7 — Add Users to a Group (Method 1: `usermod`)

```bash
usermod -aG devops ansible
```

**Breakdown:**

* **`usermod`** — modifies an existing user account
* **`-aG`** — two combined options:
  * **`-a`** — append (add to the group without removing from existing groups)
  * **`-G`** — supplementary/secondary group (capital G)
* **`devops`** — the group to add the user to
* **`ansible`** — the user being modified [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Critical distinction:** Capital `-G` = supplementary group. Lowercase `-g` = primary group. Using `-g` would **change** the user's primary group, which is usually not what you want. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Verification:**

```bash
id ansible
```

Should now show `devops` in the group list. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

```bash
grep devops /etc/group
```

Should show `devops:x:GID:ansible` — the ansible user is listed as a member. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Common mistake:** Forgetting `-a` (append). Without `-a`, `-G` **replaces** all supplementary groups with only the one specified, removing the user from any other supplementary groups they belonged to.

***

## Step 8 — Add Users to a Group (Method 2: Direct File Edit)

```bash
vi /etc/group
```

Find the `devops` line and add users **comma-separated** after the existing member:

```
devops:x:GID:ansible,jenkins,aws
```

Save and exit the file. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Verification:**

```bash
id aws
```

Should show `devops` in the group list. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

> ⚠️ **Expert Note:** Directly editing `/etc/group` works but bypasses any validation that `usermod` performs. In production, prefer `usermod -aG`. Direct editing is useful for adding multiple users at once quickly, but a typo (wrong format, missing colon, extra space) can corrupt the group file and cause authentication failures system-wide. The safer production tool is `vigr`, which validates syntax before saving.

***

## Step 9 — Set Passwords with `passwd`

```bash
passwd ansible
```

**Breakdown:**

* **`passwd`** — sets or resets a user's password
* **`ansible`** — the target user [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

You'll be prompted to enter the new password twice. The video sets simple passwords for practice. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

Repeat for other users:

```bash
passwd aws
passwd jenkins
```

**Operational note:** Only root can set/reset another user's password. A normal user running `passwd` (without a username) changes their own password. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Connection to flow:** Users can now be logged into from outside the system or switched to by other normal users.

***

## Step 10 — Switch Between Users with `su -`

### Root switching to any user (no password needed):

```bash
su - ansible
```

Switches to ansible immediately. No password prompt. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Verification:** `whoami` outputs `ansible`. `pwd` outputs `/home/ansible`.

### Normal user switching to another user (password required):

```bash
su - aws
```

From the ansible session, this prompts for aws's password. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Return to previous user:

```bash
exit
```

Each `exit` pops one layer of the session stack. Multiple `su -` calls create nested layers; multiple `exit` calls unwind them. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

The video demonstrates: root → ansible → aws → jenkins, then exit × 3 back to root. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## Step 11 — Inspect User Activity

### Login history:

```bash
last
```

Shows who logged in, when, and from where. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Currently logged-in users:

```bash
who
```

### Current user identity:

```bash
whoami
```

### Files opened by a user:

```bash
lsof -u vagrant
```

* **`lsof`** — list open files
* **`-u vagrant`** — filter by username [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

If `lsof` is not installed:

```bash
yum install lsof -y
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

```bash
lsof -u aws
```

Returns nothing if aws is not logged in — useful for confirming a user is inactive before deletion. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## Step 12 — Delete Users and Groups

### Delete user only (home directory preserved):

```bash
userdel aws
```

Removes user from `/etc/passwd` and `/etc/shadow`, but `/home/aws` still exists. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Delete user AND home directory:

```bash
userdel -r jenkins
```

* **`-r`** — removes home directory and mail spool along with the user account [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

**Verification:** `ls /home/` — jenkins directory should be gone; aws directory may still exist. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Clean up orphaned home directory manually:

```bash
rm -rf /home/aws
```

Required if you used `userdel` without `-r`. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Delete a group:

```bash
groupdel devops
```

* **`groupdel`** — removes a group from `/etc/group` [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

### Clean up remaining user:

```bash
userdel -r ansible
```

**Final verification:**

```bash
tail -5 /etc/passwd
tail -5 /etc/group
```

All created users and the devops group should be gone. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## Step 13 — Review All Commands

```bash
history
```

Displays the full command history for review and practice. [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ User/Group System Architecture

```
LINUX ACCESS CONTROL
├── Every file → owned by 1 user + 1 group
├── Access controlled via permissions on that user/group
└── "Everything is a file" → users/groups control ALL system access

THREE USER TYPES:
├── Root         → UID 0, GID 0, /root, /bin/bash, unlimited power
├── Regular      → UID 1000+, GID 1000+, /home/<name>, /bin/bash
└── Service      → UID 1-999, GID 1-999, /var or /etc, /sbin/nologin
                   └── No password, no shell → security containment
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 📁 Critical System Files

```
/etc/passwd  → User identity (7 columns)
  user : x : UID : GID : comment : home : shell
  └── x = password stored in shadow (not here)
  └── World-readable (needed for UID lookups)

/etc/shadow  → Encrypted passwords + expiry
  └── Root-only access (security isolation)

/etc/group   → Group definitions
  group : x : GID : member1,member2,...
  └── Members listed comma-separated after GID
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 🔗 User Creation Chain

```
useradd <name>
  ├── Creates entry in /etc/passwd (UID auto-assigned, 1000+)
  ├── Creates entry in /etc/shadow (no password set)
  ├── Creates PRIMARY GROUP with SAME name + SAME ID in /etc/group
  └── Creates /home/<name>

⚠️ User created but CANNOT log in → no password yet
  └── passwd <name> → sets password → enables login
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 👥 Group Membership Model

```
USER
├── Primary Group (1, mandatory)
│   └── Set at creation, stored in /etc/passwd col 4
│   └── Files created by user → owned by this group
│
└── Supplementary Groups (0+, optional)
    └── Additional access grants
    └── Stored in /etc/group member lists

ADDING TO SUPPLEMENTARY GROUP:
  Method 1: usermod -aG <group> <user>
    └── -a = append (CRITICAL: without -a, replaces all supplementary groups)
    └── -G = supplementary (capital G)
    └── -g = primary (lowercase g) ← DIFFERENT OPERATION
  
  Method 2: vi /etc/group → add username comma-separated
    └── Fast for multiple users, but no validation
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 🔐 User Switching Rules

```
su - <username>

ROOT → any user:    NO password required (absolute authority)
USER → other user:  Password REQUIRED

exit = pop one session layer (stack model)

Session stack example:
  root → su - ansible → su - aws → su - jenkins
  exit ← jenkins | exit ← aws | exit ← ansible | back to root
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 🔍 Inspection Commands

```
id <user>       → UID, GID, all groups
last            → login history (who, when)
who             → currently logged-in users
whoami          → current user identity
lsof -u <user>  → all files opened by user
                  └── Pre-deletion safety check
                  └── May need: yum install lsof -y
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 🗑️ Deletion Model

```
userdel <user>        → removes account, KEEPS /home/<user>
userdel -r <user>     → removes account + home dir + mail spool
  └── -r = recursive/complete cleanup

groupdel <group>      → removes group from /etc/group

Orphaned home dir cleanup:
  rm -rf /home/<user>  → manual cleanup if -r was not used
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## ⚡ Command Reference (Compact)

```
CREATE:    useradd <name>       | groupadd <name>
MODIFY:    usermod -aG <grp> <user>  | passwd <user>  | vi /etc/group
INSPECT:   id <user>  | grep <user> /etc/passwd  | grep <grp> /etc/group
           last  | who  | whoami  | lsof -u <user>
SWITCH:    su - <user>  | exit
DELETE:    userdel [-r] <user>  | groupdel <grp>
VIEW:      head -N /etc/passwd  | tail -N /etc/passwd
```

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 🧩 Reusable Patterns

| Pattern                              | Instance                                                                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| **Identity / Credential Separation** | `/etc/passwd` (readable) vs `/etc/shadow` (restricted) — separate what needs to be public from what must be secret      |
| **Auto-paired Creation**             | `useradd` creates both user AND matching primary group — one action, two coordinated entities                           |
| **Least Privilege via Role Users**   | Service users: no password + no shell = minimal attack surface for daemon processes                                     |
| **Append vs. Replace Semantics**     | `-aG` (append to groups) vs `-G` (replace groups) — same flag, catastrophically different without `-a`                  |
| **Conservative Deletion Default**    | `userdel` preserves data; `-r` required for complete cleanup — same pattern as `cp`/`rm` requiring `-r` for directories |
| **Pre-action Inspection**            | `lsof -u` before deletion; `ls` before `rm` — verify impact before executing destructive operations                     |
| **Stack-based Session Model**        | `su -` pushes layer; `exit` pops — consistent with `vagrant ssh` / `sudo -i` / `exit` from earlier lectures             |

 [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)

***

## 🧭 One-Line Mental Reload

> **Users (3 types: root=0, regular=1000+, service=1-999) and groups control all file access; user info in `/etc/passwd` (7 cols), passwords in `/etc/shadow`, groups in `/etc/group`; `useradd` auto-creates matching primary group; `usermod -aG` adds to supplementary groups (never forget `-a`); `passwd` enables login; root switches to any user without password; `userdel -r` for clean deletion; inspect with `id`/`last`/`who`/`lsof -u` before acting.** [\[30-users-and-groups \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/30-users-and-groups.txt)
