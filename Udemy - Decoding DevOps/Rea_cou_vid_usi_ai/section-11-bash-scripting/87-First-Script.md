# 🎓 Deep Learning Material: Writing Your First Bash Shell Script

*Reconstructed from video captions — [87-first-script.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt?EntityRepresentationId=07e1d8a0-3dea-4ebd-8beb-6ae81405ca82)* [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What Is a Shell Script?

A script is fundamentally a **text file that contains bash commands**. That is the entire definition — nothing more exotic. Every command you type manually in the terminal can be placed into a text file, and that file becomes a script. The purpose is straightforward: instead of typing commands one by one every time you need them, you write them once into a file and execute that file whenever needed. The script runs each command sequentially, exactly as if you were typing them interactively. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

This is the foundational mental model for all shell scripting: **a script is just a stored sequence of terminal commands made reusable.** You are not learning a separate programming language in isolation — you are learning to capture and automate the exact same commands you already use manually.

***

## 1.2 Script File Location and the `.sh` Extension Convention

The video establishes `/opt/scripts` as the directory for storing scripts. This is a deliberate organizational choice — keeping scripts in a known, centralized directory rather than scattering them across the filesystem. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

The file extension `.sh` is the **conventional** extension for shell scripts, but the video explicitly states it is **not mandatory**. The operating system does not require `.sh` to recognize or execute a script. The extension is purely a human-readability convention — it helps you and others immediately identify the file as a shell script when browsing a directory. The actual mechanism that determines how the file executes is the **shebang line**, not the extension. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

> 🔍 **Deep Dive:** This is a common misunderstanding. In Windows, file extensions determine which program opens a file (`.docx` → Word, `.py` → Python). In Linux, extensions are **informational only**. A script named `firstscript` with no extension would execute identically to `firstscript.sh` — as long as the shebang line and execute permissions are correct. The extension helps humans, not the operating system.

***

## 1.3 The Shebang Line (`#!`) — The Interpreter Directive

The **first line** of every script must be the **shebang** — written as `#!/bin/bash`. This is not a comment. The characters `#!` together form a **single special character sequence** called the shebang (also called hashbang). It tells the operating system: "When this file is executed, open the interpreter at the specified path and run all the commands in this file through that interpreter." [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

For a bash script, the shebang is `#!/bin/bash` — meaning the bash interpreter located at `/bin/bash` will execute the file. If you were writing a Python script, the shebang would be `#!/usr/bin/python` (or `#!/usr/bin/env python`). For Ruby, it would be `#!/usr/bin/ruby`. The shebang is the **universal mechanism** that links a script file to its execution engine. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

The video makes a critical distinction: **`#!` (shebang) is NOT the same as `#` (comment)**. A line starting with `#` alone is a comment — the interpreter ignores everything after it. But `#!` on the very first line is a special directive to the operating system's kernel. The exclamation mark after the hash transforms it from "ignore this" into "use this as the interpreter path." This distinction is essential — confusing the two means your script either won't run or will run with the wrong interpreter. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

> 🔍 **Deep Dive:** When you execute a script, the Linux kernel reads the first two bytes of the file. If they are `#!` (hex: `0x23 0x21`), the kernel knows this is an interpreted script. It reads the rest of that first line to get the interpreter path, then launches that interpreter with the script file as its argument. Effectively, running `./firstscript.sh` becomes the kernel internally executing `/bin/bash ./firstscript.sh`. Without the shebang, the kernel doesn't know which interpreter to use and defaults to the current shell — which may or may not be bash, leading to unpredictable behavior.

***

## 1.4 The `echo` Command — Printing Output

`echo` is the **print command** in bash. Whatever you provide after `echo` inside double quotes is printed to the terminal. For example, `echo "Welcome to my script"` prints that exact text. Running `echo` with nothing after it (just `echo` followed by Enter) prints a **blank line** — this is used to add visual spacing in script output to improve readability. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

The video uses `echo` for two distinct purposes: printing informational messages (like "The uptime of the system is") and printing formatting elements (blank lines and hash-separator lines like `############`). Both uses serve **output readability** — making the script's output understandable to the person reading it in the terminal. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

***

## 1.5 System Information Commands Used in the Script

The script uses three system commands to gather information: [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**`uptime`** — Reports how long the system has been running since its last boot, along with the current time, number of logged-in users, and system load averages.

**`free -m`** — Displays memory (RAM) utilization. The `-m` flag formats the output in **megabytes**, making the numbers human-readable instead of showing raw bytes.

**`df -h`** — Shows disk filesystem utilization. The `-h` flag stands for **human-readable**, converting raw byte counts into KB, MB, GB, etc.

These commands are not unique to scripting — they are standard terminal commands. The script simply runs them in sequence, proving the core concept: a script is just commands in a file.

***

## 1.6 File Permissions and the Execute Permission Requirement

When you create a text file in Linux, it is created with **read and write permissions** but **no execute permission**. This is a security design: the system does not assume that every text file is meant to be run as a program. If you try to execute a file that lacks execute permission, the system returns **"Permission denied"** — not because the content is wrong, but because the file's permission metadata does not allow execution. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

The video demonstrates this directly: after creating the script, attempting to run it with `./firstscript.sh` immediately fails with "Permission denied." Checking the file's permissions confirms there is no `x` (execute) flag for the user, group, or others. The solution is `chmod +x`, which **adds execute permission** to the file. After this, the same `./firstscript.sh` command works. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

This is a deliberate Linux security model: **you must explicitly grant a file the right to be executed.** This prevents accidental execution of arbitrary text files and is the reason every script requires this one-time permission setup.

> ⚠️ **Expert Note:** `chmod +x` adds execute permission for **all** (user, group, others). In production environments, you may want more restrictive permissions — `chmod u+x` grants execute only to the file owner. Overly permissive execute permissions on scripts is a common security oversight.

***

## 1.7 Script Execution: Relative Path vs. Absolute Path

To run a script, you must provide its **path** — the operating system needs to know where the file is. There are two ways to specify this: [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Relative path:** A path relative to your current working directory. If you are inside `/opt/scripts/`, the relative path is `./firstscript.sh`. The `./` prefix means "current directory." This prefix is required — typing just `firstscript.sh` without `./` will not work because the current directory is not in the system's default command search path (`$PATH`).

**Absolute path:** The full path from the filesystem root: `/opt/scripts/firstscript.sh`. This works from **any** directory on the system because it specifies the complete location. You don't need to be in the script's directory to use the absolute path. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

Both methods execute the exact same file with the exact same result. The choice is purely about convenience — relative paths are shorter when you're already in the right directory; absolute paths work from anywhere.

***

## 1.8 Comments — Making Scripts Readable for Humans

The `#` character (hash) at the beginning of a line marks everything after it as a **comment**. The bash interpreter completely ignores comment lines — they exist solely for human readers. The video emphasizes this as a **habit** that must be developed: even when a script is simple and you think comments are unnecessary, adding them ensures that you (or someone else) can understand the script's purpose when reopening it weeks or months later without reading every line of code. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

The video demonstrates a commenting pattern: a **title block** at the top of the script (e.g., `### This script prints System info ###`) that describes the script's overall purpose, followed by **inline section comments** before each functional block (e.g., `# Checking system uptime`, `# Memory utilization`). This creates a two-level documentation structure — the title tells you *what the script does* and the section comments tell you *what each part does*. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

The critical reminder from the video: `#` is a comment and is ignored. `#!` on line 1 is the shebang and is NOT ignored — it is a kernel-level instruction. Every other `#` in the script is a comment. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

***

## 1.9 Output Readability — Formatting Script Output

Without formatting, a script that runs multiple commands dumps all output into the terminal as a continuous wall of text — hard to read and hard to distinguish where one command's output ends and another's begins. The video addresses this by inserting `echo` statements between commands: blank `echo` lines create **visual spacing**, and `echo "############"` lines create **visual separators**. Combined with descriptive `echo` statements before each command (e.g., "The uptime of the system is"), the output becomes structured and immediately understandable. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

This is a dual-readability principle demonstrated in the video: **the script itself must be readable** (via comments) and **the script's output must be readable** (via formatting echo statements). Both serve different audiences — the script's code serves the developer who maintains it; the script's output serves the operator who runs it. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are writing a simple shell script that prints system information — uptime, memory utilization, and disk utilization — with formatted, readable output. Along the way, we learn the complete operational cycle: creating a script file, handling permissions, executing it, improving its output formatting, and adding comments for maintainability. The final outcome: a reusable, well-documented system info script and the foundational operational skills to write and run any bash script. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

***

## Step 1 — Create the Scripts Directory

**What we are doing:** Creating a dedicated directory to organize all our scripts.

```bash
mkdir /opt/scripts
cd /opt/scripts
```

**Breakdown:**

* `mkdir /opt/scripts` — creates the directory `/opt/scripts`. `mkdir` = make directory
* `cd /opt/scripts` — changes your current working directory into it

**Connection to flow:** This is our workspace. All scripts in this course are written here. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

***

## Step 2 — Install Vim Editor

**What we are doing:** Installing the text editor we'll use to write scripts.

```bash
yum install vim -y
```

**Why this is needed:** The video notes that vim is **not installed by default** on the CentOS box being used. Since a script is a text file, we need a text editor to create it. Vim is the editor of choice throughout this course. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Breakdown:**

* `yum` — CentOS/RHEL package manager
* `install vim` — install the vim package
* `-y` — auto-confirm the installation prompt

**Common mistake:** Trying to use `vim` before installing it → "command not found" error. Always verify tool availability on a fresh system.

***

## Step 3 — Create and Write the Script

**What we are doing:** Creating the script file and writing our first version.

```bash
vim firstscript.sh
```

**Breakdown:**

* `vim` — opens the vim text editor
* `firstscript.sh` — the filename. `.sh` is conventional for shell scripts (not mandatory, as covered in Theory) [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Inside vim, write the following initial content:**

```bash
#!/bin/bash
echo "Welcome"
echo
echo "The uptime of the system is"
uptime
echo "Memory utilization"
free -m
echo "Disk utilization"
df -h
```

**Line-by-line breakdown:**

| Line | Content                              | Purpose                                                   |
| ---- | ------------------------------------ | --------------------------------------------------------- |
| 1    | `#!/bin/bash`                        | Shebang — tells OS to use bash interpreter at `/bin/bash` |
| 2    | `echo "Welcome"`                     | Prints the text "Welcome"                                 |
| 3    | `echo`                               | Prints a blank line (visual spacing)                      |
| 4    | `echo "The uptime of the system is"` | Descriptive label before uptime output                    |
| 5    | `uptime`                             | Runs the uptime command, output appears here              |
| 6    | `echo "Memory utilization"`          | Descriptive label before memory output                    |
| 7    | `free -m`                            | Runs memory check in megabytes                            |
| 8    | `echo "Disk utilization"`            | Descriptive label before disk output                      |
| 9    | `df -h`                              | Runs disk check in human-readable format                  |

**Save and exit vim:** Press `Esc`, then type `:wq` and press Enter. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Connection to flow:** The script file now exists but cannot be executed yet — it lacks execute permission.

***

## Step 4 — Attempt Execution (Permission Denied)

**What we are doing:** Trying to run the script to demonstrate the permission requirement.

```bash
./firstscript.sh
```

**Breakdown:**

* `./` — current directory prefix (relative path)
* `firstscript.sh` — the script filename

**Expected result:** **Permission denied.** The script was just created as a regular text file with no execute permission. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Verification — check current permissions:**

```bash
ls -l firstscript.sh
```

**What to look for:** The permission string (e.g., `-rw-r--r--`). Notice there is no `x` in any position — no execute permission for user, group, or others.

**Why this happens:** As covered in Theory §1.6, Linux does not grant execute permission to new files by default. This is intentional security behavior.

***

## Step 5 — Grant Execute Permission

**What we are doing:** Adding execute permission to make the script runnable.

```bash
chmod +x ./firstscript.sh
```

**Breakdown:**

* `chmod` — **ch**ange file **mod**e (permissions)
* `+x` — **add** e**x**ecute permission
* `./firstscript.sh` — the target file (relative path) [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**What happens internally:** The file's permission metadata is updated. The permission string changes from something like `-rw-r--r--` to `-rwxr-xr-x` — the `x` flag is now present.

**Verification:**

```bash
ls -l firstscript.sh
```

Confirm `x` appears in the permission string.

**Common mistake:** Forgetting `chmod +x` and repeatedly getting "Permission denied." This is the single most common beginner mistake with scripts. It only needs to be done **once per file** — the permission persists.

**Connection to flow:** The script is now executable. We can run it.

***

## Step 6 — Execute with Relative Path

```bash
./firstscript.sh
```

**Expected output:** The script runs each command in sequence. You see "Welcome", a blank line, "The uptime of the system is" followed by uptime output, "Memory utilization" followed by `free -m` output, and "Disk utilization" followed by `df -h` output. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Observation from the video:** The output works but is described as "not much readable" — the different sections run together visually. This motivates the formatting improvement in the next step.

***

## Step 7 — Improve Output Formatting

**What we are doing:** Editing the script to add visual separators and spacing between output sections.

```bash
vim firstscript.sh
```

**Add `echo` blank lines and hash-separator lines between command blocks.** The video uses vim line numbers (`:set nu` to enable) to navigate. Insert formatting lines like:

```bash
echo "############"
echo
```

After each command's output (after `uptime`, after `free -m`, etc.) to create clear visual boundaries between sections. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Save and exit:** `Esc` → `:wq`

**Connection to flow:** Output is now structured and readable. Next, we make the script's source code readable too.

***

## Step 8 — Add Comments for Script Readability

**What we are doing:** Adding comments so the script's purpose and structure are clear to anyone reading the code later.

```bash
vim firstscript.sh
```

**Add comments using `#`:**

```bash
#!/bin/bash

### This script prints System info ###

echo "Welcome"
echo

# Checking system uptime
echo "The uptime of the system is"
uptime
echo "############"
echo

# Memory utilization
echo "Memory utilization"
free -m
echo "############"
echo

# Disk utilization
echo "Disk utilization"
df -h
```

**Key points during editing:**

* The title comment (`### This script prints System info ###`) uses triple hashes on both sides as a visual title block — all of it is still a comment, the interpreter ignores it [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)
* Section comments (`# Checking system uptime`, `# Memory utilization`) describe what each block does
* The video emphasizes making commenting a **habit** even for simple scripts — future-you reading this after a month should understand it without reading every command [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**Save and exit:** `Esc` → `:wq`

***

## Step 9 — Execute with Absolute Path

**What we are doing:** Running the script using its full filesystem path to demonstrate the alternative execution method.

```bash
/opt/scripts/firstscript.sh
```

**Breakdown:**

* `/opt/scripts/firstscript.sh` — the complete path from the filesystem root

**Expected result:** Identical output to `./firstscript.sh`. The script runs the same way regardless of how you specify its path. [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

**When to use which:**

* **Relative** (`./firstscript.sh`) — convenient when you're already in the script's directory
* **Absolute** (`/opt/scripts/firstscript.sh`) — required when calling the script from a different directory, from another script, or from a cron job

**Connection to flow:** You now know both execution methods. The script is complete — readable code, readable output, proper permissions, and proper structure.

***

## Final Script State

For reference, the complete final version of the script: [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)

```bash
#!/bin/bash

### This script prints System info ###

echo "Welcome"
echo

# Checking system uptime
echo "The uptime of the system is"
uptime
echo "############"
echo

# Memory utilization
echo "Memory utilization"
free -m
echo "############"
echo

# Disk utilization
echo "Disk utilization"
df -h
```

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ Core Identity

```
Shell Script = Text file + Bash commands + Shebang + Execute permission
             = Reusable, automated command execution
```

## 🔑 Shebang — The Interpreter Directive

```
Line 1 MUST be:  #!/bin/bash
                  ─┬──┬───────
                   │   └── Path to interpreter
                   └── Shebang (kernel-level, NOT a comment)

#! = "Use this interpreter"  ← KERNEL reads this
#  = "Ignore this line"      ← INTERPRETER reads this

Python: #!/usr/bin/python
Ruby:   #!/usr/bin/ruby
Bash:   #!/bin/bash
```

## 📋 Script Anatomy

```
#!/bin/bash                          ← 1. Shebang (mandatory, line 1)
### Title comment ###                ← 2. Script purpose (comment)
# Section description                ← 3. Block comment
echo "Label"                         ← 4. Output formatting
command                              ← 5. Actual work
echo "############"                  ← 6. Visual separator
echo                                 ← 7. Blank line spacer
```

## 🔒 Permission Gate

```
New file created → rw-r--r-- (NO execute)
                       │
Attempt ./script.sh  → ❌ Permission denied
                       │
chmod +x script.sh   → rwxr-xr-x (execute ADDED)
                       │
Attempt ./script.sh  → ✅ Runs successfully

One-time operation. Permission persists after granted.
```

## 🛤️ Execution Path Options

```
RELATIVE:  ./firstscript.sh              ← Works only from script's directory
ABSOLUTE:  /opt/scripts/firstscript.sh   ← Works from anywhere

Both execute identically. Choose by context.
```

## 📐 Dual Readability Principle

```
SCRIPT READABILITY (for developer):
  └── Comments (#) → Title block + Section descriptions
      "Understand the script without reading every command"

OUTPUT READABILITY (for operator):
  └── echo statements → Labels + Blank lines + Separator lines (####)
      "Understand the output without knowing the script"
```

## 🔄 Complete Operational Flow

```
mkdir /opt/scripts → cd into it
     │
Install vim (not default on CentOS)
     │
vim firstscript.sh → Write shebang + commands + save (:wq)
     │
./firstscript.sh → ❌ Permission denied
     │
chmod +x ./firstscript.sh
     │
./firstscript.sh → ✅ Output (unformatted)
     │
vim → Add echo spacers + separators → save
     │
./firstscript.sh → ✅ Output (formatted, readable)
     │
vim → Add comments (# title, # sections) → save
     │
/opt/scripts/firstscript.sh → ✅ Same output via absolute path
```

## 🧰 Commands Used

```
SYSTEM INFO:          uptime | free -m | df -h
FILE/PERMISSION:      vim | chmod +x | ls -l
EXECUTION:            ./script.sh | /full/path/script.sh
OUTPUT FORMATTING:    echo "text" | echo (blank) | echo "####..."
PACKAGE INSTALL:      yum install vim -y
```

## 🔁 Reusable Engineering Patterns

| Pattern                              | Manifestation                                                                                       |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- |
| **Interpreter directive**            | Shebang decouples script content from execution engine — same pattern across bash/python/ruby       |
| **Explicit permission gating**       | Linux requires deliberate `chmod +x` — security-by-default, no accidental execution                 |
| **Dual-audience documentation**      | Comments serve code readers; echo formatting serves output readers — separate concerns              |
| **Convention ≠ enforcement**         | `.sh` extension is convention only; actual behavior is controlled by shebang + permissions          |
| **Incremental refinement**           | Write → test → improve formatting → test → add comments → test (iterative development cycle)        |
| **Absolute vs. relative addressing** | Same resource, two access paths — relative for proximity convenience, absolute for universal access |

## ⚡ Key Gotchas for Fast Recall

```
❌ Forgetting chmod +x         → "Permission denied" every time
✅ chmod +x once               → Permanent for that file

❌ Confusing # with #!         → # = comment (ignored) | #! = shebang (executed by kernel)
✅ #! ONLY on line 1           → Anywhere else it's just a comment

❌ Typing script name without ./ → "command not found" (not in $PATH)
✅ Use ./script.sh or full path  → Explicit path always works

❌ No comments in scripts       → Unreadable after weeks
✅ Title + section comments     → Instantly understandable later
```

***

This completes the full reconstruction of the first shell scripting video. Want me to generate Anki flashcards (CSV) from this material, or shall I process the next caption file? [\[87-first-script \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/87-first-script.txt)
