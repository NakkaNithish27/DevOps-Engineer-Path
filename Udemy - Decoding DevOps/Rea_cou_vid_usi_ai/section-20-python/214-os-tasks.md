# 🐍 Python for OS Automation — Executing System Commands & Automating Linux Tasks — Deep Learning Material

**Source:** *OS Tasks* (Video Lecture Caption File) + Supporting files: [214.check-file.py](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.check-file.py?EntityRepresentationId=07123819-e8cb-4bc2-9a99-8ccb82caccf2), [214.ostasks.py](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.ostasks.py?EntityRepresentationId=9f152639-89ef-4b9b-8796-a1df44364397), [214.Vagrantfile.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.Vagrantfile.txt?EntityRepresentationId=f54e424a-96cb-40d5-821b-efdcea9389f9) [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Why Python for OS Automation — And Why Not (The Honest Context)

The instructor opens with a critical disclaimer: **everything we're about to do with Python can be done much more easily and much better using Ansible** (which is covered later in the course). The purpose of these Python automation exercises is not to replace Ansible — it's to build **programming fundamentals** so that when you later use automation tools like Ansible, Terraform, or CloudFormation, you have the underlying programming intuition to use them effectively. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

This is an important mental model: Python scripting for OS tasks is a **learning vehicle**, not a production best practice. In real-world DevOps, you would use purpose-built tools (Ansible for configuration management, Terraform for infrastructure). But those tools are built on the same logical constructs — loops, conditions, variable substitution, exit codes, idempotency checks — that you learn by writing Python automation scripts. Mastering these constructs in Python first makes the specialized tools intuitive rather than magical.

That said, the instructor also notes: **you can use Python to do all kinds of automation.** Python isn't limited to what specialized tools do. You can automate AWS tasks, call Jenkins jobs from Python scripts, integrate with virtually any tool that has an API or CLI. The versatility of Python is the secondary reason for learning this. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## 1.2 The Roadmap — What This Section Covers

The instructor outlines the full trajectory of the Python automation section: [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

1. **Local OS command execution** (this lecture) — running Linux commands from Python, writing a script that adds users, groups, directories, checks conditions, and assigns permissions.
2. **Remote execution via SSH** (next lecture) — using the Python **Fabric** library to SSH into remote Linux machines and execute tasks remotely. A script will provision a web server using Python Fabric.
3. **Python Virtual Environments** — isolating Python dependencies per project.
4. **Integration modules/libraries** — connecting Python with tools like Jenkins and AWS for broader automation.

This lecture focuses exclusively on item 1 — local OS automation.

***

## 1.3 The os Module — Python's Bridge to the Operating System

Python, by default, cannot execute operating system commands. If you type `ls` in the Python interpreter, you get a `NameError: name 'ls' is not defined` — because `ls` is a Linux/bash command, not a Python command. Python and the operating system are separate execution environments. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

The **`os` module** is Python's built-in bridge to the operating system. When you `import os`, you gain access to a collection of functions (methods) that let Python interact with the OS: execute commands, navigate the filesystem, check file/directory existence, change permissions, and much more. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

The most important function for command execution is **`os.system()`**. You pass it a string containing any OS command, and Python hands that string to the operating system's shell for execution. The command runs exactly as if you typed it at the terminal. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

```python
import os
os.system("ls")
os.system("pwd")
os.system("whoami")
```

 [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## 1.4 Exit Codes — The Communication Channel Between OS and Python

When `os.system()` executes a command, it does two things: it displays the command's output on the screen, and it **returns the exit code**. The exit code is the OS's way of telling you whether the command succeeded or failed. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

* **Exit code 0** = command executed successfully
* **Non-zero exit code** = command failed

This is the critical mechanism that enables conditional automation. You run a command, capture its exit code, and make decisions based on whether it succeeded or failed. For example: run `id alpha` to check if user `alpha` exists. If exit code is 0, the user exists. If non-zero, the user doesn't exist — so create it. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

You capture the exit code by assigning the `os.system()` call to a variable:

```python
exitcode = os.system("id alpha")
```

The variable `exitcode` now holds the numeric exit code. The command's printed output still appears on screen but is **not** captured in the variable — only the exit code is. This is exactly what we need for decision-making: we don't care about the output text; we care about success/failure. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

🔍 **Deep Dive:**
The instructor demonstrates that a non-existent command (gibberish) returns a non-zero exit code (e.g., 256). The specific non-zero value can vary by command and error type, but for our automation purposes, the only distinction that matters is zero vs. non-zero. This is a universal Unix convention — exit code 0 means success, anything else means failure — and it's the same convention used by shell scripts, Ansible, Jenkins, and virtually every automation tool.

***

## 1.5 The os Module — Beyond os.system()

The `os` module contains far more than just `system()`. The instructor uses the **`dir()` function** to list all available functions within the module: `dir(os)` returns every method/function available. Many of these map directly to Linux commands you already know: [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

* `os.chdir()` — change directory (equivalent to `cd`)
* `os.getcwd()` — get current working directory (equivalent to `pwd`)
* `os.chmod()` — change file permissions
* `os.chown()` — change file ownership
* `os.getpid()` — get process ID
* `os.uname()` — get OS information
* `os.mkdir()` — create a directory
* `os.path.isdir()` — check if a path is a directory (returns `True`/`False`)
* `os.path.isfile()` — check if a path is a file (returns `True`/`False`)

The key distinction: `os.system()` is a **generic command executor** — you can pass any shell command as a string. The other functions are **specialized Python methods** that perform specific OS operations directly through Python's internal OS interface, not through the shell. Both approaches work; the specialized methods are more "Pythonic" and sometimes more reliable, while `os.system()` is more flexible (any command you can type at a terminal, you can pass to `os.system()`). [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

The instructor demonstrates both approaches when creating a directory: you can use `os.system("mkdir /opt/science_dir")` (generic shell command) or `os.mkdir("/opt/science_dir")` (specialized Python method). Both create the directory. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## 1.6 The Shebang Line — Telling the OS Which Interpreter to Use

When you write a Python script and execute it directly (like `./ostasks.py` instead of `python3 ostasks.py`), the operating system needs to know **which interpreter** to use. By default, the shell assumes the file contains shell commands. If it encounters Python syntax, it fails. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

The **shebang line** (first line of the script) solves this: `#!/usr/bin/python3` tells the OS: "use the Python 3 interpreter located at `/usr/bin/python3` to execute this file." [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

The instructor verifies the interpreter paths:

* Python 3: `/usr/bin/python3`
* Python 2: `/usr/bin/python2` (or `/usr/bin/python`)

If you write a Python 3 script, the shebang must point to the Python 3 interpreter. Using the wrong interpreter path (or omitting the shebang) causes the script to fail with syntax errors because the wrong interpreter tries to parse the code. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## 1.7 Idempotency Through Condition Checking — The Core Automation Pattern

The most important engineering concept in this lecture is **idempotency** — the idea that running a script multiple times should produce the same end state without errors or unwanted side effects. The instructor demonstrates this through a consistent pattern: **check before acting**. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

Before adding a user: check if the user exists (`id username` → check exit code). If the user exists, skip and print a message. If not, create the user.

Before adding a group: check if the group exists (`grep science /etc/group` → check exit code). If the group exists, skip. If not, create it.

Before creating a directory: check if the directory exists (`os.path.isdir()` → returns `True`/`False`). If it exists, skip. If not, create it. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

This check-before-act pattern ensures the script is **safe to run repeatedly**. The first run creates everything. Subsequent runs detect that everything already exists and skip the creation steps. Without these checks, the second run would fail with "user already exists" errors or create duplicate entries.

The instructor notes one exception: adding a user to a group with `usermod -G science username` does **not** require an existence check because the command is inherently idempotent — if the user is already in the group, it doesn't throw an error. The instructor explicitly says: "I'm not checking any condition over here, but because it really doesn't matter if the user already exists. It's not gonna throw any error if it already exists in the group." [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

🔍 **Deep Dive:**
This check-before-act pattern is exactly what Ansible calls "desired state" or "declarative configuration." In Ansible, every module internally performs this check — it examines the current state, compares it to the desired state, and only takes action if they differ. By writing these checks manually in Python, you're learning the fundamental logic that Ansible automates for you. This is why the instructor says Python automation makes you better at using Ansible.

***

## 1.8 String Formatting in os.system() — Injecting Variables into Commands

When constructing OS commands dynamically (e.g., `useradd alpha`, `useradd beta`), you need to inject Python variable values into command strings. The instructor uses the **`.format()` method** (covered in the print formatting lecture) to accomplish this: [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

```python
os.system("id {}".format(user))
os.system("useradd {}".format(user))
os.system("usermod -G science {}".format(user))
```

The `{}` placeholder in the command string is replaced by the value of the `user` variable. This is the same `.format()` mechanism used for print statements, now applied to command construction. The instructor demonstrates this in the interpreter first: showing that putting the variable name directly inside the double-quoted string treats it as literal text, not as a variable reference — hence the need for `.format()`. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## 1.9 The Lab Environment — Three VMs via Vagrant

The practical environment consists of **three virtual machines** defined in a Vagrantfile: [\[214.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.Vagrantfile.txt)

| VM        | OS                  | IP Address    | Purpose                                    |
| --------- | ------------------- | ------------- | ------------------------------------------ |
| scriptbox | Ubuntu 22 (jammy64) | 192.168.56.36 | Where we write and run Python scripts      |
| web01     | CentOS Stream 9     | 192.168.56.37 | Target for remote execution (next lecture) |
| web02     | CentOS Stream 9     | 192.168.56.38 | Target for remote execution (next lecture) |

`web01` has custom resources: 1024MB memory and 2 CPUs. The other VMs use defaults. Only `scriptbox` is used in this lecture; `web01` and `web02` are for the SSH/Fabric lecture that follows. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt), [\[214.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.Vagrantfile.txt)

***

## 1.10 Python 2 vs. Python 3 — Both Exist in the Real World

Ubuntu 22 ships with **Python 3** by default. Python 2 is not installed by default but can be added (`apt install python2`). The instructor installs both to make the point: many machines in production still use Python 2, and you should know how to work with both interpreters. The commands to invoke them are different: `python3` for Python 3, `python2` for Python 2. The shebang line in your script determines which one executes when you run the script directly. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up a Python scripting environment on an Ubuntu VM, then writing two scripts: a simple file/directory existence checker (`check-file.py`) and a comprehensive OS automation script (`ostasks.py`) that creates users, a group, adds users to the group, creates a directory, and assigns ownership and permissions — all with idempotency checks. After this, the `ostasks.py` script can be run repeatedly without errors, always producing the correct end state. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## Step 1: Set Up the Virtual Machine Environment

Download the `pyvms.zip` file from the lecture resources. Extract it. Choose the correct Vagrantfile based on your OS:

* **Windows / macOS Intel** → use the Windows folder's Vagrantfile
* **macOS M1/M2/M3** → use the Mac ARM folder's Vagrantfile [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

Create a working folder and copy the Vagrantfile into it:

```bash
# Example: create folder on F drive
mkdir /f/pyvms
# Copy Vagrantfile into /f/pyvms/
```

Navigate to the folder in Git Bash or Terminal:

```bash
cd /f/pyvms
```

**Examine the Vagrantfile** to understand what will be created:

```bash
cat Vagrantfile
```

Three VMs: `scriptbox` (Ubuntu), `web01` (CentOS), `web02` (CentOS) — each with a private network IP. [\[214.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.Vagrantfile.txt)

**Check for existing VMs** to avoid resource conflicts:

```bash
vagrant global-status
```

If other VMs are running, navigate to their folders and power them off (`vagrant halt`) or destroy them (`vagrant destroy`). [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Bring up the VMs:**

```bash
vagrant up
```

Open **VirtualBox** to monitor. If any VM takes a long time, double-click it in VirtualBox to see its console output. **Do not close** the console window — that powers off the VM. Minimize instead. Wait for all VMs to finish provisioning. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## Step 2: Log Into scriptbox and Verify Python

```bash
vagrant ssh scriptbox
```

Switch to root (scripts will need root privileges for user/group management):

```bash
sudo -i
```

**Verify the OS:**

```bash
cat /etc/os-release
```

Should show Ubuntu 22. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Verify Python 3:**

```bash
python3
```

This opens the Python 3 interactive interpreter. Type `exit()` to leave.

**Install Python 2 (optional, for awareness):**

```bash
apt update && apt install python2 -y
```

After installation, `python2` opens the Python 2 interpreter. We will use Python 3 for all scripts. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## Step 3: Explore os.system() in the Interpreter

Enter the Python 3 interpreter:

```bash
python3
```

**Demonstrate that Linux commands don't work natively:**

```python
ls
```

Result: `NameError: name 'ls' is not defined` — Python doesn't know Linux commands. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Import the os module and execute commands:**

```python
import os
os.system("ls")
os.system("pwd")
os.system("whoami")
```

Each command executes and prints output, then returns exit code `0` (success). [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Demonstrate a failed command:**

```python
os.system("some_gibberish_command")
```

Returns a non-zero exit code (e.g., 127 or 256) because the command doesn't exist.

**Capture exit code into a variable:**

```python
user = "alpha"
ec = os.system("id {}".format(user))
print(ec)
```

Since user `alpha` doesn't exist yet, `id alpha` fails and `ec` holds a non-zero value (256). The `id` command's error output prints to screen, but only the exit code is stored in `ec`. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Explore available os functions:**

```python
dir(os)
```

Returns a list of all functions in the `os` module. Exit the interpreter:

```python
exit()
```

***

## Step 4: Create the Scripts Directory

```bash
mkdir /opt/pyscripts
cd /opt/pyscripts
```

All scripts will be created here. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## Step 5: Write and Test check-file.py

Create the script:

```bash
vim check-file.py
```

Write the following content: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.check-file.py)

```python
#!/usr/bin/python3
import os

path = '/tmp/testfile.txt'

if os.path.isdir(path):
    print("It is a directory")
elif os.path.isfile(path):
    print("It is a file.")
else:
    print("file or dir does not exists.")
```

**Line-by-line breakdown:**

* `#!/usr/bin/python3` — shebang line; tells the OS to use the Python 3 interpreter. Verify this path exists: `which python3` should return `/usr/bin/python3`. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)
* `import os` — loads the os module for filesystem checks.
* `path = '/tmp/testfile.txt'` — variable holding the path to check.
* `os.path.isdir(path)` — returns `True` if the path is an existing directory.
* `os.path.isfile(path)` — returns `True` if the path is an existing file.
* The `else` branch catches the case where the path is neither a file nor a directory (i.e., doesn't exist).

**Make executable and run:**

```bash
chmod +x check-file.py
./check-file.py
```

**Expected output:** `file or dir does not exists.` — because `/tmp/testfile.txt` doesn't exist yet. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Create the file and run again:**

```bash
touch /tmp/testfile.txt
./check-file.py
```

**Expected output:** `It is a file.` — the `elif` branch matches. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Connection to the larger flow:** This small script validates the `os.path.isdir()` and `os.path.isfile()` patterns before using them in the larger `ostasks.py` script.

***

## Step 6: Write ostasks.py — The Full Automation Script

Create the script:

```bash
vim ostasks.py
```

Write the following content (the instructor builds this incrementally, testing after each section): [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.ostasks.py)

```python
#!/usr/bin/python3
import os

userlist = ["alpha", "beta", "gamma"]

print("Adding users to system")
print("##############################################################################")

## Loop to add users from userlist
for user in userlist:
    exitcode = os.system("id {}".format(user))
    if exitcode != 0:
        print("User {} does not exist. Adding it.".format(user))
        print("##############################################")
        print()
        os.system("useradd {}".format(user))
    else:
        print("User already exist, skipping it.")
        print("##############################################")
        print()

## Condition to check if group exists or not, add if not exist
exitcode = os.system("grep science /etc/group")
if exitcode != 0:
    print("Group science does not exist. Adding it.")
    print("##############################################")
    print()
    os.system("groupadd science")
else:
    print("Group already exist, skipping it.")
    print("##############################################")
    print()

## Add all users to the science group
for user in userlist:
    print("Adding user {} in the science group".format(user))
    print("##############################################")
    print()
    os.system("usermod -G science {}".format(user))

## Create directory
print("Adding directory")
print("##############################################")
print()

if os.path.isdir("/opt/science_dir"):
    print("Directory already exist, skipping it")
else:
    os.mkdir("/opt/science_dir")

## Assign permissions and ownership
print("Assigning permission and ownership to the directory.")
print("##############################################")
print()
os.system("chown :science /opt/science_dir")
os.system("chmod 770 /opt/science_dir")
```

**Make executable:**

```bash
chmod +x ostasks.py
```

 [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.ostasks.py)

***

## Step 7: Execute ostasks.py — First Run

```bash
./ostasks.py
```

**Expected behavior on first run:** [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

1. **User creation loop:** For each user (alpha, beta, gamma), `id username` returns non-zero (user doesn't exist) → prints "does not exist, adding" → runs `useradd username`.
2. **Group creation:** `grep science /etc/group` returns non-zero (group doesn't exist) → prints "does not exist, adding" → runs `groupadd science`.
3. **Group membership:** For each user, runs `usermod -G science username` — adds user to the science group. No condition check needed (inherently idempotent).
4. **Directory creation:** `os.path.isdir("/opt/science_dir")` returns `False` → runs `os.mkdir("/opt/science_dir")`.
5. **Ownership and permissions:** `chown :science /opt/science_dir` sets group ownership to `science`. `chmod 770 /opt/science_dir` sets permissions (owner=rwx, group=rwx, others=none).

***

## Step 8: Execute ostasks.py — Second Run (Idempotency Test)

```bash
./ostasks.py
```

**Expected behavior on second run:** [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

1. **User creation loop:** For each user, `id username` returns 0 (user exists) → prints "User already exist, skipping it."
2. **Group creation:** `grep science /etc/group` returns 0 (group exists) → prints "Group already exist, skipping it."
3. **Group membership:** Runs `usermod` commands again — no error because adding to a group that already contains the user is harmless.
4. **Directory creation:** `os.path.isdir()` returns `True` → prints "Directory already exist, skipping it."
5. **Ownership and permissions:** Re-applied (harmless to re-run).

**No errors. Same end state.** This is idempotency in action.

***

## Step 9: Verify the Final State

```bash
id alpha
```

Should show user `alpha` with group `science` in the group list. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

```bash
ls -ld /opt/science_dir
```

**Expected output:** `drwxrwx--- ... root science ... /opt/science_dir` — directory owned by group `science` with permission `770`. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

## Step 10: Debugging Common Issues

**Syntax errors (missing parentheses in print):** The instructor encounters this twice. Python 3 requires `print()` as a function call with parentheses. `print "text"` (Python 2 syntax) causes a `SyntaxError`. The error message includes the line number — go to that line and add parentheses. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

**Script fails with "permission denied":** Either the shebang line is missing/wrong, or the script isn't executable. Fix with `chmod +x scriptname.py`.

**Script fails with shell syntax errors:** The shebang line is missing, so the shell tries to interpret Python code as shell commands. Add `#!/usr/bin/python3` as the first line.

**VMs taking long to boot:** Double-click the VM in VirtualBox to see console output. Don't close the window — minimize it. Closing powers off the VM. [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Lecture Context

```
Python for OS automation = LEARNING VEHICLE
Real production: use Ansible, Terraform, CloudFormation
BUT: Python teaches the LOGIC underneath those tools
  → loops, conditions, exit codes, idempotency
  → master Python automation → master Ansible faster
```

## Section Roadmap

```
1. Local OS commands via Python ← THIS LECTURE
2. Remote SSH execution via Fabric (next lecture)
3. Python Virtual Environments
4. Integration: Jenkins API, AWS SDK from Python
```

## Lab Environment

```
scriptbox (Ubuntu 22)   → 192.168.56.36 → write & run scripts HERE
web01     (CentOS 9)    → 192.168.56.37 → remote target (next lecture)
web02     (CentOS 9)    → 192.168.56.38 → remote target (next lecture)

web01: 1024MB RAM, 2 CPUs (custom)
Others: default resources
```

## Core Mechanism: os.system()

```
import os
os.system("any_linux_command")
  → executes command via shell
  → prints output to screen
  → RETURNS exit code (0 = success, non-zero = failure)

exitcode = os.system("id alpha")
  → stores ONLY exit code in variable
  → output still prints to screen (not captured)
```

## os Module — Key Functions Used

```
os.system("cmd")       → execute any shell command, return exit code
os.mkdir("/path")       → create directory (Python-native, no shell)
os.path.isdir("/path")  → True if directory exists
os.path.isfile("/path") → True if file exists
dir(os)                 → list ALL available os functions
```

## Shebang Line

```
#!/usr/bin/python3  → first line of script
  → tells OS: use Python 3 interpreter
  → without it: shell tries to parse Python as bash → fails

Verify paths:
  /usr/bin/python3 → Python 3
  /usr/bin/python2 → Python 2
```

## ostasks.py — Full Task Flow

```
PHASE 1: Add Users (loop + condition)
  for user in ["alpha", "beta", "gamma"]:
    id {user} → exitcode
    ├─ non-zero → user doesn't exist → useradd {user}
    └─ zero → user exists → skip

PHASE 2: Add Group (condition)
  grep science /etc/group → exitcode
    ├─ non-zero → group doesn't exist → groupadd science
    └─ zero → group exists → skip

PHASE 3: Add Users to Group (loop, NO condition)
  for user in userlist:
    usermod -G science {user}
    (inherently idempotent — no error if already member)

PHASE 4: Create Directory (condition)
  os.path.isdir("/opt/science_dir")
    ├─ True → skip
    └─ False → os.mkdir("/opt/science_dir")

PHASE 5: Set Ownership & Permissions (always runs)
  chown :science /opt/science_dir
  chmod 770 /opt/science_dir
```

## Idempotency Pattern

```
FIRST RUN:  check → doesn't exist → CREATE
SECOND RUN: check → exists → SKIP

Pattern: os.system("check_cmd") → exitcode → if/else → act or skip
         os.path.isdir/isfile()  → True/False → if/else → act or skip

Exception: some commands are inherently idempotent
  → usermod -G (no error if already in group)
  → chown, chmod (re-applying same state = no harm)
```

## String Formatting in Commands

```
user = "alpha"
os.system("id {}".format(user))       → executes: id alpha
os.system("useradd {}".format(user))   → executes: useradd alpha
os.system("usermod -G science {}".format(user))

{} = placeholder → replaced by .format() argument
Same mechanism as print formatting (Lecture 204)
```

## Exit Code Decision Logic

```
exitcode = os.system("command")

exitcode == 0    → command SUCCEEDED → resource EXISTS
exitcode != 0    → command FAILED → resource DOES NOT EXIST

Used for: id (user check), grep (group check)
Universal Unix convention: 0 = success, non-zero = failure
```

## Two Ways to Create a Directory

```
os.system("mkdir /opt/science_dir")  → shell command (generic)
os.mkdir("/opt/science_dir")          → Python-native method (specific)

Both work. os.mkdir is more "Pythonic".
os.system is more flexible (any command).
```

## check-file.py Logic

```
path = '/tmp/testfile.txt'

os.path.isdir(path)?
  ├─ True → "It is a directory"
  └─ False →
     os.path.isfile(path)?
       ├─ True → "It is a file"
       └─ False → "file or dir does not exists"
```

## Verification Commands

```
id alpha              → shows user info + groups
ls -ld /opt/science_dir → shows permissions + ownership
grep science /etc/group → shows group exists
```

## Debugging Quick Reference

```
SyntaxError at line N → missing parentheses in print()
  Python 3: print("text")  ✓
  Python 2: print "text"   ✗ in Python 3

Permission denied → chmod +x script.py

Shell syntax errors → missing shebang (#!/usr/bin/python3)

VM won't boot → double-click in VirtualBox → watch console
  DO NOT close console window (powers off VM) → minimize instead
```

## Reusable Engineering Patterns

**1. Check-Before-Act (Idempotency)**

```
Before creating resource:
  → Check if it already exists
  → Exists? Skip. Doesn't exist? Create.

This IS Ansible's internal logic, manually implemented.
Same pattern: Terraform state check, K8s desired state reconciliation.
```

**2. Exit Code as Decision Signal**

```
Run a probe command → capture exit code → branch on 0 vs non-zero
  → 0: resource exists / command succeeded
  → non-zero: resource missing / command failed

Universal across: shell scripts, Python, Jenkins pipelines, CI/CD
```

**3. Loop + Condition for Batch Operations**

```
Define a list of items (users, servers, files)
  → for item in list:
       check if item exists
       create if missing, skip if present

Scales linearly: add more items to list → same logic handles them
Same pattern: Ansible playbooks with loops, Terraform for_each
```

**4. Learning Vehicle → Production Tool Progression**

```
Manual Python scripting → teaches: loops, conditions, exit codes, idempotency
  → prepares you for: Ansible (same logic, declarative syntax)
  → prepares you for: Terraform (same state-checking pattern)

"You can master these automation tools if you have
 some hands-on programming, especially using Python"
```

***

*This completes the full reconstruction of the lecture and all supporting files. Theory explains the os module, exit codes, and the idempotency pattern. Practical walks through every command in both scripts with debugging guidance. The Compression Map enables rapid recall of the task flow, decision logic, and the foundational automation patterns that transfer directly to Ansible and other tools.* [\[214-os-tasks \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214-os-tasks.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.check-file.py), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.ostasks.py), [\[214.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/214.Vagrantfile.txt)
