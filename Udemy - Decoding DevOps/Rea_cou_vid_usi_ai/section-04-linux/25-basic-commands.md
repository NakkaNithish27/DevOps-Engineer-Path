# 🎓 Complete Deep Learning Material — Essential Linux File Commands: `mkdir`, `cp`, `mv`, `touch`, `rm`, and Core Operational Concepts

**Source:** [25-more-commands-mkdir-cp-mv-touch-etc.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt?EntityRepresentationId=7a6ece33-d0f5-4471-8046-8ae053d5edb5) — Hands-on lecture covering fundamental Linux file and directory manipulation commands, Linux command syntax structure, path systems, wildcard patterns, and critical safety awareness for destructive operations. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — User Context and Session Navigation: `exit`, `sudo -i`, `vagrant ssh`

Before any file operations begin, the video establishes the **user context** you operate within. In Linux, every command executes as a specific user, and that user's identity determines what you can access, where your home directory is, and what permissions you hold. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

The system demonstrated has **two user layers**: the **vagrant** user (a normal, unprivileged user) and the **root** user (the superuser with unrestricted access). You switch between them using specific commands:

* **`sudo -i`** — switches from vagrant to root. The `-i` flag simulates a full login shell, meaning you get root's environment, root's home directory (`/root`), and root's PATH.
* **`exit`** — peels back one layer. If you're root, `exit` drops you back to vagrant. If you're vagrant, `exit` logs you out of the VM entirely, returning you to the host machine (Windows in this case). Running `exit` twice from root takes you all the way out of the VM. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)
* **`vagrant ssh`** — reconnects from the host machine back into the VM as the vagrant user.

This layered session model is important because **your current user determines your current working directory, your permissions, and the impact of every command you run**. The entire rest of the lecture operates from the vagrant user's home directory (`/home/vagrant`), which is the safe sandbox for practice.

> 🔍 **Deep Dive:** The session stack is: `Host OS → vagrant ssh → vagrant user → sudo -i → root user`. Each `exit` pops one level. This is a **stack-based session model** — last in, first out. Understanding this prevents the common confusion of "where am I?" and "who am I?" when running commands.

***

## 1.2 — Creating Directories: `mkdir`

The `mkdir` command creates new directories. It solves the fundamental problem of **organizing the filesystem** — without directories, all files would exist in a flat, unmanageable pile. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

You can create **a single directory** (`mkdir dev`) or **multiple directories in one command** (`mkdir ops backupdir`). The command accepts multiple arguments, and each argument becomes a new directory in the current location. In the video, three directories are created: `dev`, `ops`, and `backupdir`, all inside the vagrant user's home directory. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

The key conceptual point is that `mkdir` creates **empty containers** — structural nodes in the filesystem tree. These directories become the targets for subsequent copy, move, and organizational operations throughout the lecture.

***

## 1.3 — Creating Empty Files and Brace Expansion: `touch`

The `touch` command has **two purposes**: it creates a new empty file if the file doesn't exist, or it updates the timestamp of an existing file. In this lecture, it's used exclusively for file creation. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

A single invocation like `touch testfile.txt` creates one empty file. The file contains nothing — zero bytes of content. The extension (`.txt`) is cosmetic; Linux does not rely on file extensions to determine file type the way Windows does. The instructor notes "the extension is not so important here now" but uses it for clarity. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Brace Expansion for Bulk File Creation

The more powerful usage demonstrated is **brace expansion** with a range: `touch devopsfile{1..10}.txt`. This is not a feature of `touch` itself — it's a **shell feature** (bash). The shell expands `{1..10}` into the sequence `1 2 3 4 5 6 7 8 9 10` **before** `touch` ever sees it. So what `touch` actually receives is ten separate arguments: `devopsfile1.txt devopsfile2.txt ... devopsfile10.txt`. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

The instructor describes this as "something like multiplication" — it generates a range and combines it with the prefix and suffix to produce multiple filenames. This is a reusable pattern: anywhere you need to generate numbered sequences of files, directories, or arguments, brace expansion does the work.

> 🔍 **Deep Dive:** Brace expansion happens at the **shell level**, before command execution. This means it works with any command, not just `touch`. You could use `mkdir project{1..5}` or `rm file{A..Z}.log`. The shell preprocesses the pattern and passes the expanded list as individual arguments to the command. This is a **shell preprocessing pattern** — the command is unaware that expansion happened.

***

## 1.4 — Relative Path vs. Absolute Path

This is one of the most important conceptual foundations in the lecture, and the instructor repeatedly reinforces it throughout multiple commands. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

An **absolute path** starts from the root of the filesystem (`/`) and specifies the complete location: `/home/vagrant/dev/`. It works identically **regardless of where you currently are** in the filesystem. It is unambiguous and self-contained.

A **relative path** is specified relative to your **current working directory**. If you're in `/home/vagrant/` and you say `dev/`, the system resolves it as `/home/vagrant/dev/`. But if you were in `/tmp/`, the same `dev/` would resolve to `/tmp/dev/`, which is a completely different location.

The instructor gives a clear practical guideline: **"As long as you don't become comfortable with the Linux filesystem, use absolute path."** Even if you're already in the correct directory, using absolute paths for the first few days builds filesystem awareness and prevents location-dependent errors. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

The key engineering insight: **relative paths are convenient but context-dependent; absolute paths are verbose but context-free.** In scripts and automation, absolute paths are strongly preferred because scripts don't always run from the directory you expect.

***

## 1.5 — Home Directory Shortcuts: `cd`, `cd ~`

Two methods return you to your home directory: [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

* **`cd`** (with no arguments) — automatically navigates to the current user's home directory.
* **`cd ~`** — the tilde `~` is a shell shorthand that expands to the home directory path. For the vagrant user, `~` expands to `/home/vagrant`.

The instructor notes the tilde key is "just below your escape button" on the keyboard. Both methods produce the same result; `~` is useful when you need to **reference** the home directory as part of a longer path (e.g., `~/dev/project/` means `/home/vagrant/dev/project/`). [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 1.6 — Copying Files and Directories: `cp`

The `cp` command copies files from a source to a destination. It creates a **duplicate** — the original remains untouched at its source location. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Copying Files

For files, `cp` is straightforward: `cp source destination`. You can use relative paths (`cp devopsfile1.txt dev/`) or absolute paths (`cp /home/vagrant/devopsfile2.txt /home/vagrant/dev/`). Both achieve the same result; the choice depends on clarity and your current location. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Copying Directories: The `-r` Requirement

Here the video teaches a critical lesson through **failure**. When you try `cp dev backupdir/`, it fails with an error: "omitting directory." You cannot copy a directory with plain `cp`. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

The reason: a directory is not a single object — it's a **tree structure** that may contain files, subdirectories, and nested content. To copy all of that, you need **recursive** behavior, which is activated with the `-r` option: `cp -r dev backupdir/`. The `-r` tells `cp` to descend into the directory, copying everything inside it at every level. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

> 🔍 **Deep Dive:** The `-r` option stands for "recursive." Recursion here means: copy this directory, then enter it, copy everything inside, and if there are subdirectories inside, enter those too, and repeat — all the way down. This is the same recursive traversal concept used in programming (tree traversal). The command without `-r` only knows how to handle **leaf nodes** (individual files), not **branch nodes** (directories with children). [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 1.7 — Linux Command Syntax: `command [options] [arguments]`

After demonstrating `cp -r`, the instructor pauses to formalize the **universal syntax structure** that every Linux command follows: [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

```
command   [options]   [arguments]
```

* **Command** — the program you're running (`cp`, `ls`, `mv`, `rm`, etc.)
* **Options** — modifiers that change the command's behavior (e.g., `-r` for recursive, `-l` for long listing, `-f` for force). Options are optional — some commands work fine without them.
* **Arguments** — the targets the command operates on (file paths, directory paths, etc.). Some commands require arguments (`cp` always needs source and destination); others work without them (`ls` alone lists the current directory). [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Option Format Conventions

Options follow two formatting patterns: [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

* **Short form:** single hyphen + single letter → `-r`, `-f`, `-i`, `-l`
* **Long form:** double hyphen + full word → `--recursive`, `--force`, `--interactive`

Both forms do the same thing. Short forms are faster to type; long forms are more readable and self-documenting, especially in scripts. The video shows that `cp` accepts `-r`, `-R` (capital), and `--recursive` — all three are equivalent for recursive copying. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### The `--help` Option: Built-in Documentation

Every command has its own set of options, and the instructor makes a critical engineering point: **you should not memorize all options.** Instead, use `--help` (e.g., `cp --help`) to see the full list of available options, usage patterns, and brief descriptions. Help is "always at your fingertips." You can also search online ("simply Google it"), but `--help` works even without internet access. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

> ⚠️ **Expert Note:** The `--help` habit is a professional marker. Engineers who reach for `--help` or `man` pages instead of memorizing option tables are more adaptable — they can operate any command they encounter, even unfamiliar ones. Memorization is fragile; the discovery reflex is durable.

***

## 1.8 — Moving and Renaming: `mv`

The `mv` command serves **two distinct purposes** depending on context: [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Moving Files and Directories

`mv source destination` relocates a file or directory from one location to another. Unlike `cp`, the original is **removed** from the source — this is a move, not a copy. Critically, **`mv` does not require `-r` to move directories.** You can move a directory with plain `mv ops dev/` — the entire directory (with all its contents) is relocated. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

This is a conceptual asymmetry worth remembering: `cp` needs `-r` for directories, but `mv` does not. The reason (implicit): moving a directory is essentially **renaming its path** in the filesystem metadata — the actual data blocks on disk don't move. Copying requires reading and duplicating every byte recursively, which is why explicit recursive permission is needed.

### Renaming Files and Directories

`mv` is also the **rename command** in Linux. There is no separate `rename` command for basic use. `mv testfile1.txt testfile22.txt` renames the file in place. The instructor notes: "when we say file, it means any file in Linux" — this includes directories, because in Linux, **directories are a type of file.** [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 1.9 — Wildcards (Glob Patterns): `*`

The `*` (asterisk) is a **wildcard** character that means "match everything" in the current context. It is another **shell-level feature** — the shell expands `*` into a list of matching filenames before the command runs. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

* `*` alone matches **all files and directories** in the current directory.
* `*.txt` matches everything that **ends with `.txt`**.

The video demonstrates: `mv *.txt textdir/` — this moves all `.txt` files from the current directory into `textdir`. The instructor calls this "little regular expression," though technically it's a **glob pattern**, not a regex. The key point is that it enables **bulk operations** on files matching a pattern, eliminating the need to name each file individually. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

> 🔍 **Deep Dive:** Like brace expansion, glob expansion is a **shell preprocessing step**. The command never sees `*.txt` — it sees the expanded list of matching filenames. If no files match the pattern, behavior depends on shell settings (bash by default passes the literal `*.txt` string, which usually causes an error). This expansion-before-execution model is fundamental to how the shell works.

***

## 1.10 — Removing Files and Directories: `rm` and the Danger of `rm -rf *`

The `rm` command **permanently deletes** files. `rm devopsfile10.txt` removes that single file. Like `cp`, removing a **directory** requires the `-r` option: `rm -r dirname`. Without `-r`, `rm` refuses to delete directories, throwing an error. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### The Dangerous Command: `rm -rf *`

The video builds to a critical safety lesson. The command `rm -rf *` combines three elements: [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

* **`rm`** — remove
* **`-r`** — recursive (delete directories and everything inside them)
* **`-f`** — force (do not ask for confirmation, do not prompt, just delete)
* **`*`** — everything in the current working directory

This command **silently, irreversibly deletes everything** in your current directory. The instructor explicitly calls it "a very dangerous command" and warns about its consequences with strong emphasis. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### No Safety Net in Linux

Linux has **no recycle bin, no trash, no undo** for command-line deletions. Once `rm` deletes a file, the only recovery path is **disk/hard disk restoration**, which is "complicated and not 100 percent assurance that you'll get back all your files." [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

The critical danger scenario: if you run `rm -rf *` while in the **wrong directory** (e.g., `/etc`, `/home`, or a server's data directory), you destroy critical system files or irreplaceable data. The instructor emphasizes: **"be careful before you delete anything in Linux system."** [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

> ⚠️ **Expert Note:** In production environments, `rm -rf *` (or worse, `rm -rf /`) has caused catastrophic, company-wide data loss incidents. The mitigation strategies are: always run `pwd` before destructive commands to confirm your location; use `ls` with the same pattern first to preview what would be affected (`ls *.txt` before `rm *.txt`); and in critical systems, use `rm -i` (interactive mode) which prompts before each deletion.

***

## 1.11 — The `history` Command

The `history` command displays a **numbered list of all commands you have executed** in the current session (and often across past sessions, depending on shell configuration). The instructor mentions it at the end as a review tool: "you can run your history command and see all the commands that you executed." [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

This is useful for **auditing your own work**, recalling a command you ran earlier, and learning from your own command sequence.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning to **create, copy, move, rename, and delete files and directories** in a Linux VM using fundamental commands. By the end, you will be able to organize a Linux filesystem confidently, use both relative and absolute paths, leverage wildcards for bulk operations, and understand the safety implications of destructive commands. The final operational outcome is **full command-line fluency for basic file manipulation.** [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## Step 1 — Establish Your User Context

Log into the VM and confirm you're operating as the right user in the right location.

```bash
vagrant ssh
```

This connects you from your host machine into the VM as the **vagrant** user. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

If you need root access:

```bash
sudo -i
```

This switches to the **root** user (full privileges). [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

To step back:

```bash
exit
```

* From root → returns to vagrant user.
* From vagrant → logs out of VM entirely, back to host. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:** Run `whoami` to confirm your current user. Run `pwd` to confirm your current directory.

**Connection to flow:** All subsequent commands in this lecture are executed as the vagrant user from `/home/vagrant`.

***

## Step 2 — Create Directories with `mkdir`

```bash
mkdir dev ops backupdir
```

**Breakdown:**

* **`mkdir`** — the command to create directories
* **`dev ops backupdir`** — three separate arguments, each becomes a new directory [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**What happens internally:** Three empty directories are created in the current working directory (`/home/vagrant/`).

**Verification:**

```bash
ls
```

You should see `dev`, `ops`, and `backupdir` listed. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Common mistake:** Typos in directory names. Linux is case-sensitive — `Dev` and `dev` are different directories.

***

## Step 3 — Create Files with `touch`

### Single file:

```bash
touch testfile.txt
```

* **`touch`** — creates an empty file (or updates timestamp if it exists)
* **`testfile.txt`** — the filename to create [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Multiple files using brace expansion:

```bash
touch devopsfile{1..10}.txt
```

* **`devopsfile`** — the prefix
* **`{1..10}`** — shell expands this into numbers 1 through 10
* **`.txt`** — the suffix appended to each [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**What happens internally:** The shell expands the brace expression first, producing: `devopsfile1.txt devopsfile2.txt ... devopsfile10.txt`. Then `touch` receives all 10 filenames as arguments and creates each one.

**Verification:**

```bash
ls
```

You should see 10 files: `devopsfile1.txt` through `devopsfile10.txt`, plus `testfile.txt`. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## Step 4 — Copy Files with `cp`

### Copy using relative path:

```bash
cp devopsfile1.txt dev/
```

* **`cp`** — copy command
* **`devopsfile1.txt`** — source (relative to current directory)
* **`dev/`** — destination directory (relative) [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:**

```bash
ls dev/
```

Should show `devopsfile1.txt` inside `dev/`. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Copy using absolute paths (from any location):

```bash
cp /home/vagrant/devopsfile2.txt /home/vagrant/dev/
```

* Both source and destination use **absolute paths** — works regardless of your current directory. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification (with absolute path):**

```bash
ls /home/vagrant/dev/
```

**Instructor's guideline:** Use absolute paths until you're comfortable with the filesystem structure. Even if you're already in the right directory, absolute paths build awareness and prevent mistakes. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Copy a directory (requires `-r`):

**First, the failure:**

```bash
cp dev backupdir/
```

**Result:** Error — "omitting directory." This fails because `cp` without `-r` cannot handle directories. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Correct command:**

```bash
cp -r dev backupdir/
```

* **`-r`** — recursive; copies the directory and everything inside it [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:**

```bash
ls backupdir/
```

Should show `dev` directory inside `backupdir/`. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## Step 5 — Navigate Home with `cd` and `cd ~`

```bash
cd
```

Returns to your home directory (`/home/vagrant`). [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

```bash
cd ~
```

Same result — `~` expands to the home directory path. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:** `pwd` should output `/home/vagrant`.

***

## Step 6 — Discover Command Options with `--help`

```bash
cp --help
```

**What happens:** Displays the usage syntax, all available options with descriptions, and examples. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Key options shown for `cp`:**

* `-a` — archive (preserve all attributes)
* `-f` — force
* `-i` — interactive (prompt before overwrite)
* `-r`, `-R`, `--recursive` — copy directories recursively [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Operational point:** This works for any command (`mv --help`, `rm --help`, `ls --help`, etc.). Use this instead of memorizing options.

***

## Step 7 — Move Files and Directories with `mv`

### Move a file:

```bash
mv devopsfile3.txt ops/
```

* **`mv`** — move command
* File is **relocated** (removed from source, placed in destination) [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:**

```bash
ls ops/
```

### Move a directory (no `-r` needed):

```bash
mv ops dev/
```

Moves the entire `ops` directory (with contents) into `dev/`. No `-r` required. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:**

```bash
ls dev/
```

Should show `ops` inside `dev/`. The original `ops` in the home directory is gone. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Rename a file:

```bash
mv testfile1.txt testfile22.txt
```

Renames the file in place. Works identically for directories. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:**

```bash
ls
```

`testfile1.txt` is gone; `testfile22.txt` exists.

***

## Step 8 — Use Wildcards for Bulk Operations

### Create a target directory:

```bash
mkdir textdir
```

### Move all `.txt` files at once:

```bash
mv *.txt textdir/
```

* **`*.txt`** — wildcard pattern matching all files ending in `.txt`
* All matching files are moved into `textdir/` in one command [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:**

```bash
ls textdir/
```

Should contain all the `.txt` files. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Operational tip:** Before executing a destructive or bulk operation, preview the match:

```bash
ls *.txt
```

This shows what would be affected without actually moving or deleting anything.

***

## Step 9 — Remove Files and Directories with `rm`

### Remove a single file:

```bash
rm devopsfile10.txt
```

Permanently deletes the file. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Remove a directory (requires `-r`):

```bash
rm -r mobile
```

* **`-r`** — recursive, required for directories (same concept as `cp -r`) [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Create test content for bulk deletion:

```bash
mkdir testdir{1..5}
```

Creates 5 directories using brace expansion. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

### Delete everything in current directory:

```bash
rm -rf *
```

* **`-r`** — recursive
* **`-f`** — force (no confirmation prompts)
* **`*`** — everything in the current directory [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**⚠️ CRITICAL WARNING:** This command is **irreversible**. Linux has no recycle bin. Recovery requires disk restoration (complicated, not guaranteed). **Always run `pwd` first** to confirm you are in the intended directory. If you're in the wrong directory (e.g., `/etc`, `/home`, or a data directory), this command causes catastrophic, unrecoverable damage. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

**Verification:**

```bash
ls
```

Should show an empty directory.

***

## Step 10 — Review Your Command History

```bash
history
```

Displays all commands executed in your session. Use this to review your work, recall syntax, or audit what you did. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Command Architecture Map

```
FILE COMMANDS
├── CREATE
│   ├── mkdir <name(s)>          → create directories
│   └── touch <name(s)>          → create empty files
│       └── brace expansion: {1..N} → shell generates range
│
├── COPY
│   └── cp <src> <dst>
│       ├── files: works directly
│       └── directories: REQUIRES -r (recursive)
│
├── MOVE / RENAME
│   └── mv <src> <dst>
│       ├── move file: works directly
│       ├── move directory: works directly (NO -r needed)
│       └── rename: mv oldname newname
│
├── DELETE
│   └── rm <target>
│       ├── files: works directly
│       ├── directories: REQUIRES -r
│       └── rm -rf * → ⚠️ DANGER: deletes everything, NO UNDO
│
└── INSPECT
    ├── ls [path]               → list contents
    └── history                 → review executed commands
```

 [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 🔗 Core Concept Relationships

```
PATH SYSTEM:
  Absolute: /home/vagrant/dev/     → context-free, always works
  Relative: dev/                   → context-dependent, needs correct cwd
  ~        = home directory shorthand
  Guideline: use absolute until comfortable

COMMAND SYNTAX (universal):
  command  [options]  [arguments]
  ├── options: -r (short) = --recursive (long)
  ├── arguments: targets (files, paths)
  └── --help → discover all options for any command

SHELL PREPROCESSING (happens before command runs):
  {1..10}  → brace expansion → generates sequence
  *.txt    → glob expansion  → matches filenames
  ~        → tilde expansion → expands to home path
```

 [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## ⚡ Critical Asymmetries (High-Recall Anchors)

| Operation | Files  | Directories          |
| --------- | ------ | -------------------- |
| `cp`      | Direct | **Needs `-r`**       |
| `mv`      | Direct | **Direct (no `-r`)** |
| `rm`      | Direct | **Needs `-r`**       |

**Why the asymmetry?** `mv` only changes the path metadata — no data copying occurs. `cp` and `rm` must traverse the directory tree recursively, so they need explicit recursive permission. [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 🛡️ Safety Model

```
rm -rf * 
  │
  ├── Irreversible (no trash, no recycle bin, no undo)
  ├── Scope = current working directory (pwd)
  ├── -f = no prompts, silent execution
  ├── Wrong directory → catastrophic data loss
  └── Recovery = disk restoration (complex, unreliable)

SAFETY PROTOCOL:
  1. pwd           → confirm location
  2. ls <pattern>  → preview targets
  3. rm <pattern>  → execute deletion
```

 [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 🔄 Session Layer Stack

```
Host OS (Windows)
  └── vagrant ssh → Vagrant user (/home/vagrant)
       └── sudo -i → Root user (/root)

exit = pop one layer (LIFO)
exit × 2 from root = back to host
```

 [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 🧩 Reusable Patterns

| Pattern                         | Instance                                                                     |
| ------------------------------- | ---------------------------------------------------------------------------- |
| **Shell Preprocessing**         | `{1..10}`, `*.txt`, `~` all expand before command executes                   |
| **Recursive Traversal Gate**    | `-r` required for tree operations (`cp`, `rm`); not for `mv` (metadata-only) |
| **Discovery over Memorization** | `--help` on any command; don't memorize option tables                        |
| **Preview before Destroy**      | `ls <pattern>` before `rm <pattern>`                                         |
| **Dual-purpose command**        | `mv` = move AND rename (same mechanism: path change)                         |
| **Failure-as-teacher**          | `cp dir` fails → teaches why `-r` exists                                     |

 [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)

***

## 🧭 One-Line Mental Reload

> **`mkdir`/`touch` create structure; `cp` duplicates (needs `-r` for dirs); `mv` moves AND renames (no `-r` needed); `rm` deletes (needs `-r` for dirs, `-rf *` is irreversible and dangerous); all commands follow `command [options] [arguments]` syntax; shell expands `{}`, `*`, `~` before the command runs; use `--help` instead of memorizing; always `pwd` before deleting.** [\[25-more-co...-touch-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/25-more-commands-mkdir-cp-mv-touch-etc.txt)
