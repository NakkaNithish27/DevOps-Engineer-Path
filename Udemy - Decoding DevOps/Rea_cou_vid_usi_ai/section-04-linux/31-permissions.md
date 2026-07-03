# Linux File Permissions and Ownership

### Understanding, Modifying, and Securing Access Control on Files and Directories

*Reconstructed from video lecture captions* [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Every File Has an Owner: The Dual-Ownership Model

In Linux, **every single file** — whether it's a text file, a directory, or a link — has two ownership attributes attached to it: a **user owner** and a **group owner**. This is not optional or configurable at a system level — it is a fundamental property of how the Linux filesystem works. When you run `ls -l`, every line shows you these two ownership fields. For example, a file owned by the root user with the root group will display `root root` in its listing. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

The reason Linux uses *dual* ownership rather than just a single owner is to enable **layered access control**. A file can belong to one specific user (the owner) AND simultaneously belong to a group of users. This lets you create permission schemes where the owner has one level of access, members of the owning group have a different level, and everyone else on the system has yet another level. This three-tier system (user, group, others) is the foundation of all Linux file security. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## 1.2 — The Permission String: Decoding the 10-Character Block

When you run `ls -l`, the very first column shows a **10-character permission string** like `-rw-------` or `drwxr-xr-x`. This string encodes two distinct pieces of information: the **file type** and the **access permissions** for three categories of users. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

### Character 1: File Type Indicator

The first character identifies **what kind of file** this is:

* **`-`** (hyphen) → regular file
* **`d`** → directory
* **`l`** → link (symbolic link) [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

This character is NOT a permission — it's metadata about the entity type.

### Characters 2–10: Three Permission Triplets

The remaining 9 characters are divided into **three groups of three**, each representing the permissions for a specific category: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```
Position:   1    2 3 4    5 6 7    8 9 10
            │    └─┬─┘    └─┬─┘    └─┬─┘
         Type   USER     GROUP    OTHERS
               (owner)  (group)  (everyone else)
```

Each triplet has three positions, always in the same order: **r** (read), **w** (write), **x** (execute). If the permission is granted, the letter appears. If denied, a **`-`** (hyphen) appears in its place. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

For example, `rw-` means read and write are granted, but execute is not. `r-x` means read and execute are granted, but write is not. `---` means no permissions at all.

The video walks through a concrete example: the file `anaconda-ks.cfg` has permissions `-rw-------`. Breaking this down: it's a regular file (`-`), the user owner has read and write (`rw-`), the group has no permissions (`---`), and others have no permissions (`---`). Only the root user who owns this file can read or modify it. Nobody else on the system can access it at all. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## 1.3 — What Read, Write, and Execute Actually Mean

The meaning of `r`, `w`, and `x` changes depending on whether the entity is a **file** or a **directory**. This is a crucial distinction that causes confusion. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

### For Regular Files

* **r (read)** — you can view/read the file contents
* **w (write)** — you can modify the file contents, and can even delete it
* **x (execute)** — you can run the file as a program/script [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

### For Directories

* **r (read)** — you can **list** the contents of the directory (i.e., `ls` works)
* **w (write)** — you can **make changes** inside the directory: create files, delete files, rename files. The video emphasizes "can even delete it"
* **x (execute)** — you can **`cd` into** the directory. Without execute permission on a directory, you cannot enter it at all [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

The video demonstrates this concretely: the `devops` directory has `rwxr-xr-x` permissions. The owner (root) can read, write, and cd into it. The group and others can read (ls) and cd into it (execute), but cannot write (create/delete files inside it). [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

> 🔍 **Deep Dive**
> The execute permission on directories is the most unintuitive concept for beginners. On a file, "execute" means "run it as a program." On a directory, "execute" means "traverse it" — you can pass through it, `cd` into it, and access files within it by name. Without execute permission, even if you have read permission, you can list filenames but cannot actually open or interact with the files inside. In practice, a directory with `r--` but no `x` is nearly useless — you can see file names but cannot do anything with them.

***

## 1.4 — Link File Permissions: The Deceptive Full Permission

The video makes a specific observation about **link files** (symbolic links): when you run `ls -l`, link files typically show **full permissions** (`lrwxrwxrwx`). But this is deceptive — those are the permissions **on the link itself**, not on the actual target file the link points to. The target file has its own separate permissions, which could be much more restrictive. When you access a file through a symbolic link, the **target file's permissions** are what actually govern your access. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## 1.5 — The Permission-Ownership Evaluation Logic

Permissions and ownership work **together** as a combined access-control system. When a user tries to access a file, the system evaluates in a specific order: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

1. **Is this user the file's owner?** → Apply the user/owner permission triplet
2. **Is this user a member of the file's group?** → Apply the group permission triplet
3. **Neither?** → Apply the others permission triplet

Only **one** triplet applies per access attempt. The system checks in order and stops at the first match. This means the owner's permissions override the group's, and the group's override others'. The video demonstrates this with the user `miles` (who is not in the devops group) getting "Permission denied" on a directory where others have no permissions, while the user `aws` (who IS in the devops group) gets full access because the group has `rwx`. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

> ⚠️ **Expert Note**
> The video explicitly warns about the `chown -r` (recursive) option: "be very careful with using recursive option, if you really mean to do that, then only use recursive. If you have like hundreds of files and directories inside that, remember, every file will have this user and this group ownership then. It will not be easy to roll back." This is a real production concern — mass ownership changes are difficult to reverse because the original per-file ownership information is lost.

***

## 1.6 — Changing Ownership: The `chown` Concept

Ownership changes are done with the `chown` (change owner) command. You can change the user owner, the group owner, or both simultaneously. The syntax uses a **colon `:` or dot `.`** as the separator between user and group: `chown user:group path`. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

The `-R` flag makes the change recursive — it applies to the target directory AND everything inside it (all subdirectories and files). As noted in the expert warning above, this should be used with caution. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## 1.7 — Changing Permissions: Two Methods

Linux provides two ways to modify permissions using the `chmod` (change mode) command. The video calls permissions "mode" — this is the formal Linux terminology. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

### Symbolic Method

Uses letters and operators to describe changes relative to current permissions:

* **Target:** `u` (user/owner), `g` (group), `o` (others)
* **Operator:** `+` (add permission), `-` (remove permission)
* **Permission:** `r` (read), `w` (write), `x` (execute)

Example: `chmod o-x /opt/devopsdir` means "for others, remove execute permission." `chmod g+w /opt/devopsdir` means "for group, add write permission." Each `chmod` call changes one specific aspect of the permissions. The symbolic method is **incremental** — you modify individual permissions without affecting the rest. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

### Numeric Method

Uses a **three-digit number** where each digit represents the complete permissions for one category:

* **First digit** → user/owner permissions
* **Second digit** → group permissions
* **Third digit** → others permissions

Each digit is calculated by **adding** the numeric values of the permissions you want to grant:

| Permission  | Value |
| ----------- | ----- |
| Read (r)    | **4** |
| Write (w)   | **2** |
| Execute (x) | **1** |
| None        | **0** |

So full permissions (rwx) = 4+2+1 = **7**. Read+write (rw-) = 4+2 = **6**. Read+execute (r-x) = 4+1 = **5**. Read only (r--) = **4**. No permissions (---) = **0**. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

Example: `chmod 770 /opt/devopsdir` means: user gets 7 (rwx), group gets 7 (rwx), others get 0 (---). The numeric method is **absolute** — it sets ALL permissions at once for all three categories in a single command, rather than incrementally adding or removing individual permissions. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

The video explicitly states: "numeric method is easy or quick way to give permission for user group and others at the same time." It positions numeric as the faster approach and symbolic as the more readable, granular approach — you can use whichever you're more comfortable with. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

> 🔍 **Deep Dive**
> The reason the numeric values are 4, 2, and 1 (rather than, say, 1, 2, 3) is that they are **powers of 2** — they correspond to individual bits in a 3-bit binary number. Read = bit 2 (100 = 4), Write = bit 1 (010 = 2), Execute = bit 0 (001 = 1). When you add them, you get a unique number from 0 to 7 for every possible combination of permissions. `chmod 754` is really setting binary `111 101 100` → `rwx r-x r--`. This is why it's sometimes called the "octal" method — each digit is an octal (base-8) number representing three binary permission bits.

***

## 1.8 — Users and Groups: The Supporting Infrastructure

The video creates supporting infrastructure to demonstrate permissions in action. Groups are created with `groupadd`, users with `useradd`, and users are added to groups by **directly editing the group file**. The video adds users `ansible`, `jenkins`, and `aws` to the `devops` group, but intentionally leaves user `miles` OUT of the group to demonstrate the "others" permission behavior. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

The `id` command verifies a user's group membership (e.g., `id ansible` shows the devops group). [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

A practical note from the video: when creating users, if a mail spool already exists (e.g., from a previous creation), you'll see a message like "mailing pool already exist." The video explicitly says "that's not an error" — it's informational and can be safely ignored. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a controlled access environment where a specific directory (`/opt/devopsdir`) is fully accessible to one user and one group, while completely locked out from all other users on the system. This demonstrates the full lifecycle of Linux access control: creating users/groups, creating a resource, assigning ownership, and setting precise permissions — then verifying the result by logging in as different users. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## Step 1 — Examine Existing Permissions

Start as the root user. List files in root's home directory to observe the permission structure: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
ls -l
```

* `ls` — list directory contents
* `-l` — long format, shows permissions, ownership, size, date

**What you'll see:** Each line starts with a 10-character permission string (as explained in Theory §1.2), followed by owner and group names. Observe different permission patterns on files, directories, and links. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

For example, `anaconda-ks.cfg` shows `-rw-------` — only the root user has read/write access. The `devops` directory shows `drwxr-xr-x` — everyone can read and enter it, but only root can write. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## Step 2 — Create the Target Directory

```bash
mkdir /opt/devopsdir
```

* `mkdir` — make directory
* `/opt/devopsdir` — the full path of the new directory under `/opt`

Verify creation and current permissions: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
ls -ld /opt/devopsdir
```

* `-ld` — the `d` flag tells `ls` to show information **about the directory itself**, not its contents. Without `d`, `ls -l` would try to list the contents inside the directory.

**Expected result:** The directory is owned by `root:root` with default permissions (typically `drwxr-xr-x`). [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Connection to flow:** We now have a resource to assign ownership and permissions to.

***

## Step 3 — Create Users and a Group

Create the group: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
groupadd devops
```

* `groupadd` — creates a new group on the system
* `devops` — the name of the group

Create users: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
useradd ansible
useradd jenkins
useradd aws
useradd miles
```

* `useradd` — creates a new user account

**Note:** If you see "mailing pool already exist," this is not an error — it's an informational message that can be safely ignored. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Connection to flow:** `ansible`, `jenkins`, and `aws` will be added to the devops group. `miles` will intentionally be left OUT — he represents "others" for testing.

***

## Step 4 — Add Users to the Group

The video adds users to the group by **directly editing the group file**: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
vim /etc/group
```

Find the line for `devops` and append the usernames:

```
devops:x:1001:aws,ansible,jenkins
```

Save and quit (`:wq`). [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Verification:** [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
id ansible
```

* `id` — shows the user's UID, GID, and group memberships

**Expected output:** The output should show `devops` listed among ansible's groups.

**Key decision:** `miles` is NOT added to the devops group. This is intentional — miles will serve as the test case for "others" permissions.

***

## Step 5 — Change Directory Ownership

```bash
chown ansible:devops /opt/devopsdir
```

* `chown` — change owner
* `ansible` — the new user owner
* `:` — separator (a dot `.` also works)
* `devops` — the new group owner
* `/opt/devopsdir` — the target path [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Verify:** [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
ls -ld /opt/devopsdir
```

**Expected result:** Owner is now `ansible`, group is now `devops`.

> ⚠️ **Expert Note**
> For recursive ownership change on directories with contents, add `-R`: `chown -R ansible:devops /opt/devopsdir`. But be careful — this changes ownership on EVERY file and subdirectory inside. If those files had different owners for good reasons, that information is lost and hard to recover. Use recursive only when you deliberately want uniform ownership throughout.

**Connection to flow:** Ownership is set. Now we configure what each ownership tier (user/group/others) can actually do.

***

## Step 6 — Modify Permissions Using Symbolic Method

The directory currently has default permissions where "others" have read and execute. We want to remove all permissions from others and add write permission for the group. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Remove execute from others:**

```bash
chmod o-x /opt/devopsdir
```

* `chmod` — change mode (permissions)
* `o` — target: others
* `-` — operator: remove
* `x` — permission: execute
* `/opt/devopsdir` — target path [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**What this does:** Other users can no longer `cd` into this directory.

**Remove read from others:** [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
chmod o-r /opt/devopsdir
```

**What this does:** Other users can no longer `ls` the directory contents either. Others now have `---` (no permissions at all).

**Add write to group:** [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
chmod g+w /opt/devopsdir
```

* `g` — target: group
* `+` — operator: add
* `w` — permission: write

**What this does:** Members of the devops group can now create and delete files inside this directory. Combined with existing read and execute, the group now has full `rwx`.

**Verify final state:** [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
ls -ld /opt/devopsdir
```

**Expected result:** `drwxrwx---` — owner (ansible) has `rwx`, group (devops) has `rwx`, others have `---`. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Connection to flow:** Permissions are now set. Time to verify by logging in as different users.

***

## Step 7 — Test as "Others" (Miles)

Switch to the miles user: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
su - miles
```

Test all three permission types: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
ls /opt/devopsdir
```

**Result:** `Permission denied` — read is blocked for others.

```bash
cd /opt/devopsdir
```

**Result:** `Permission denied` — execute (traverse) is blocked for others.

```bash
touch /opt/devopsdir/test1
```

**Result:** `Permission denied` — write is blocked for others.

All three operations fail because miles is not the owner, not in the devops group, so "others" permissions apply — and others have `---`. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## Step 8 — Test as Group Member (AWS)

Exit from miles and switch to aws. Since no password was set for aws, you must switch from root: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
exit
su - aws
```

Test the same operations: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
ls /opt/devopsdir
```

**Result:** ✅ Success — read permission granted via group.

```bash
cd /opt/devopsdir
```

**Result:** ✅ Success — execute permission granted via group.

```bash
touch awsfiles
```

**Result:** ✅ Success — write permission granted via group. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Key insight demonstrated:** The same directory, accessed by two different users, produces completely different results based on group membership. Ownership + permissions work together as the access control mechanism. [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

## Step 9 — Numeric Method: Create and Secure Another Directory

Exit to root and create a new directory for practicing numeric permissions: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
exit
mkdir /opt/webdata
```

Change ownership: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
chown aws:devops /opt/webdata
```

**Set full permissions for user and group, none for others:**

```bash
chmod 770 /opt/webdata
```

* `7` (first digit, user) = 4+2+1 = rwx (full permission)
* `7` (second digit, group) = 4+2+1 = rwx (full permission)
* `0` (third digit, others) = no permission [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Alternative example — mixed permissions:** [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
chmod 754 /opt/webdata
```

* `7` (user) = rwx
* `5` (group) = 4+1 = r-x (read + execute, no write)
* `4` (others) = 4 = r-- (read only) [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Recursive application:** To apply permissions to all contents inside a directory: [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
chmod -R 770 /opt/webdata
```

* `-R` — recursive: applies to the directory AND all files/subdirectories within it

**Another example from the video:** [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

```bash
chmod 640 somefile
```

* `6` (user) = 4+2 = rw- (read + write)
* `4` (group) = r-- (read only)
* `0` (others) = --- (no permission) [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

**Connection to flow:** The numeric method achieves the same result as multiple symbolic chmod commands but in a single operation. Choose whichever method fits the situation.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Permission String Anatomy

```
 d   r w x   r - x   r - x
 │   └─┬─┘   └─┬─┘   └─┬─┘
Type  USER    GROUP   OTHERS
      (owner)

Types:  - = file    d = directory    l = link
Perms:  r = read    w = write        x = execute
        - = denied
```

***

## rwx Meaning: File vs. Directory

```
         FILE                    DIRECTORY
r  →  view contents         →  ls (list contents)
w  →  modify/delete         →  create/delete files inside
x  →  run as program        →  cd into directory

⚠️ Link files show lrwxrwxrwx but actual access = target file's permissions
```

***

## Access Evaluation Flow

```
User tries to access file/dir
         │
         ├── Is user the OWNER?  → Apply USER triplet (chars 2-4)
         │
         ├── Is user in GROUP?   → Apply GROUP triplet (chars 5-7)
         │
         └── Neither             → Apply OTHERS triplet (chars 8-10)

Only ONE triplet applies. First match wins.
```

***

## Ownership + Permission = Access Control

```
┌──────────────────────────────────────────────────┐
│           /opt/devopsdir                          │
│           Owner: ansible    Group: devops         │
│           Perms: rwx rwx ---                      │
│                                                   │
│  ansible (owner)     → rwx  ✅ full access        │
│  aws (in devops grp) → rwx  ✅ full access        │
│  jenkins (in devops) → rwx  ✅ full access        │
│  miles (NOT in grp)  → ---  ❌ all denied         │
└──────────────────────────────────────────────────┘
```

***

## Two chmod Methods

```
SYMBOLIC METHOD (incremental, one change at a time):
  chmod [target][operator][permission] path
  
  Targets:    u = user/owner    g = group    o = others
  Operators:  + = add           - = remove
  Perms:      r   w   x

  Examples:
    chmod o-x dir   → remove execute from others
    chmod g+w dir   → add write to group

NUMERIC METHOD (absolute, sets all at once):
  chmod [user][group][others] path
  
  Values:  r=4  w=2  x=1  none=0
  
  Digit = sum of granted permissions
    7 = rwx (4+2+1)    6 = rw- (4+2)
    5 = r-x (4+1)      4 = r-- (4)
    3 = -wx (2+1)      2 = -w- (2)
    1 = --x (1)        0 = --- (0)

  Examples:
    chmod 770 dir  → rwxrwx---
    chmod 754 dir  → rwxr-xr--
    chmod 640 file → rw-r-----
```

***

## chown: Changing Ownership

```
chown user:group path       ← change both user and group
chown user path             ← change user only
chown :group path           ← change group only
chown -R user:group path    ← recursive (all contents)

⚠️ Recursive = every file inside gets same owner/group
   Hard to rollback → use deliberately
```

***

## Command Quick-Reference

```
ls -l              → show permissions + ownership
ls -ld dir         → show directory's own permissions (not contents)
chown u:g path     → change ownership
chmod <spec> path  → change permissions (symbolic or numeric)
chmod -R           → recursive permission change
groupadd name      → create group
useradd name       → create user
id username        → verify user's group membership
su - username      → switch to user
```

***

## Operational Setup Flow

```
1. Create resource        →  mkdir /opt/devopsdir
2. Create group           →  groupadd devops
3. Create users           →  useradd ansible, jenkins, aws, miles
4. Assign users to group  →  edit /etc/group (add users to devops line)
   (leave miles out)
5. Change ownership       →  chown ansible:devops /opt/devopsdir
6. Set permissions         →  chmod (symbolic or numeric)
7. Verify                  →  ls -ld, su - user, test ls/cd/touch
```

***

## Numeric Permission Cheat Sheet

```
 #   Binary   Perms
 7   111      rwx
 6   110      rw-
 5   101      r-x
 4   100      r--
 3   011      -wx
 2   010      -w-
 1   001      --x
 0   000      ---

Common patterns:
  770 → full owner + full group + locked others
  755 → full owner + read/exec group + read/exec others
  750 → full owner + read/exec group + locked others
  700 → full owner only
  644 → read/write owner + read group + read others
  640 → read/write owner + read group + locked others
  600 → read/write owner only
```

***

## Key Failure Points

```
❌ Can't cd into directory        → missing x on directory for your tier
❌ Can't ls directory              → missing r on directory for your tier
❌ Can't create file in directory  → missing w on directory for your tier
❌ Permission denied on everything → you're in "others" tier with ---
❌ Recursive chown/chmod mistake   → no easy rollback; original per-file 
                                     permissions/ownership are lost
❌ Link shows full perms but       → link perms ≠ target file perms;
   access denied                     check the actual target's permissions
```

***

## Reusable Engineering Patterns

**1. Tiered Access Control Pattern:** Three tiers of access (owner → group → others) evaluated in priority order. First matching tier determines access. *Transferable to:* IAM role evaluation in cloud (user policies → group policies → organization policies), firewall rule evaluation (most specific match wins), RBAC in Kubernetes.

**2. Dual Notation Pattern:** Same underlying system (permission bits) expressed in two ways — symbolic (human-readable, incremental) and numeric (compact, absolute). Both produce identical results; choice depends on the operation. *Transferable to:* any system with multiple interface modes for the same underlying state (e.g., CLI vs. GUI, declarative vs. imperative configuration).

**3. Ownership + Permission Separation:** WHO owns something and WHAT they can do are configured independently. Changing ownership doesn't change permissions; changing permissions doesn't change ownership. They combine at access-evaluation time. *Transferable to:* cloud IAM (resource ownership vs. policy attachment), database access (schema ownership vs. GRANT privileges). [\[31-file-permissions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/31-file-permissions.txt)

***

*This completes the full reconstruction of the file permissions lecture. Theory builds the conceptual model of how ownership and permissions interact. Practical walks through the exact command sequence to set up and verify access control. Mental Compression Map provides rapid-recall structures for the permission system, numeric values, and operational flow.*
