# 🎓 Deep Learning Material: Python on Linux — Versions, Execution, and Indentation

**Source:** [201-python-on-linux-versions-and-indentation.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt?EntityRepresentationId=7b178763-e6e5-4e33-9384-3782531ee8ae) — Video caption reconstruction covering how to write and execute Python scripts on Linux machines, Python 2 vs Python 3 version differences, the shebang interpreter path, script execution methods, and Python's indentation-based syntax compared to Bash. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Python Is Already Installed on Linux

Linux machines come with Python pre-installed. This is not optional software you need to seek out — it is part of the base operating system. The reason is that many core system tools, package managers, and automation utilities in Linux are written in Python. The OS itself depends on Python to function. When you type `python` on a Linux terminal and hit Enter, it opens the **Python interpreter** — an interactive environment where you can type Python statements and see results immediately. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

The critical distinction is **which version** is installed by default, and this depends on the Linux distribution and its version.

***

## 1.2 Python 2 vs Python 3: The Version Split

On **Red Hat-based machines up to Enterprise Linux 7** (which includes CentOS 7, the system used in this video), the default `python` command invokes **Python 2.7**. This means typing `python` gives you a Python 2 interpreter. On **Ubuntu 20.04 (focal) and higher versions**, the default is **Python 3**. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

This matters because Python 2 and Python 3 are **not the same language** in terms of syntax. Code written for one version may not work on the other. The most visible example in this video is the `print` statement:

* **Python 2:** `print "hello"` — `print` is a **statement**. No parentheses required.
* **Python 3:** `print("hello")` — `print` is a **function**. Parentheses are mandatory.

If you write Python 2 `print` syntax and execute it with a Python 3 interpreter, you get a **syntax error**. The video demonstrates this directly — copying a Python 2 script, changing the interpreter to Python 3, and watching it fail until the `print` statements are corrected to function syntax. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

The video explicitly states: **Python 2 support has stopped.** You should use Python 3 going forward. However, Python 2 is not dead in practice — some tools still depend on it. The specific example given is **Ansible**, which uses Python 2, and certain Linux system automation tools and libraries that are more stable or more established under Python 2. So the operational reality is: learn and write Python 3, but be aware that Python 2 exists and you may encounter it when certain tools require it. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

## 1.3 The Shebang Line: Telling Linux Which Interpreter to Use

When you write a Python script file (with the `.py` extension by convention), you need a way to tell the Linux operating system **which program should interpret this file**. This is done with the **shebang line** — the very first line of the script, starting with `#!` followed by the path to the interpreter.

For a Bash script, you write `#!/bin/bash`. For a Python script, you write `#!/usr/bin/python` (for Python 2) or `#!/usr/bin/python3` (for Python 3). The shebang line tells the OS: "When this file is executed, use this specific program to interpret it." [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

On CentOS 7, the default Python interpreter is at `/usr/bin/python` (Python 2). If you install Python 3, it becomes available at `/usr/bin/python3`. The shebang path must match the version of Python your code is written for. If your script uses Python 3 syntax but the shebang points to `/usr/bin/python` (Python 2), it will fail with syntax errors. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

🔍 **Deep Dive**
The shebang mechanism is a Linux kernel feature, not a Python feature. When you execute a file that starts with `#!`, the kernel reads the path after `#!` and launches that program, feeding the script file to it as input. This is why the shebang line must be the **very first line** — the kernel checks the first two bytes of the file for `#!`. If the shebang is missing, the OS doesn't know which interpreter to use, and the file will either fail or be interpreted by the current shell (which won't understand Python syntax). [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

## 1.4 Script Execution: Three Methods

There are three ways to execute a Python script on Linux, each with different requirements:

**Method 1: Make the script executable and run it directly.**
You first set the executable permission using `chmod +x <script>`, then run it with `./script.py` (relative path) or the full absolute path. This method **requires** the shebang line — without it, the OS doesn't know which interpreter to use. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Method 2: Invoke the interpreter explicitly.**
You run `python script.py` or `python3 script.py`. In this case, you are telling the OS exactly which interpreter to use. The shebang line is not required (though it's still good practice to include it). Executable permission is also not required — the interpreter reads the file, it doesn't "execute" the file as a program. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Method 3: The interactive interpreter.**
You type `python` or `python3` to enter the interactive interpreter, then type commands line by line. This is for quick testing, not for writing persistent scripts. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

The video demonstrates Methods 1 and 2 explicitly, and Method 3 at the beginning when opening the Python interpreter. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

## 1.5 Python's Indentation Syntax: The Core Concept

This is the most important concept in the video, and the instructor emphasizes it repeatedly.

In most programming languages (and in Bash scripting), code blocks are defined by **explicit delimiters** — opening and closing markers. In Bash, an `if` block starts with `if ... then` and ends with `fi`. You can indent the code inside however you want (or not at all) — the indentation is cosmetic. The interpreter doesn't care about spaces. It knows where the block ends because it sees `fi`. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

Python works fundamentally differently. **Python has no closing delimiters.** There is no `fi`, no `end`, no closing brace. Instead, Python uses **indentation (spaces at the beginning of lines) as its syntax** to determine which statements belong to which block. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

Here is how it works concretely, using the example from the video:

```python
x = 0
print("something")
if x == 0:
  print("in the if block")
  print("value of x is 0")
else:
  print("in the else block")
  print("value of x is non-zero")
print("this statement is outside")
```

The `if` line ends with a **colon (`:`)** — this signals the start of a block. The two `print` statements under `if` are indented by **two spaces** — this tells Python they belong to the `if` block. The `else` line also ends with a colon, and its indented statements belong to the `else` block. The final `print` statement starts at **column zero** (no indentation) — this tells Python it is **outside** both the `if` and `else` blocks. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

The rules are strict:

* All statements in the same block **must** have the **same indentation level** (same number of spaces).
* If you mess up the indentation — give three spaces where two were expected, or put a statement at the wrong level — Python throws an **`IndentationError`**. The video demonstrates this: misaligning a `print` statement immediately produces `IndentationError: expected an indented block`. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)
* You can use 2 spaces, 3 spaces, 4 spaces, or even tabs — but **you must be consistent** within a block.

The video demonstrates the consequence of moving the last `print` statement under `else` by giving it two spaces of indentation: now it becomes **part of the else block** instead of being independent. The indentation directly changes the program's logical structure. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

🔍 **Deep Dive**
The comparison to Bash is instructive. In Bash:

```bash
x=0
if [ $x -eq 0 ]
then
  echo "zero"
else
  echo "non-zero"
fi
```

You can remove all indentation, collapse lines, or add random spacing — it still works because `then`, `else`, and `fi` explicitly mark block boundaries. In Python, **whitespace IS the syntax**. This is not a style preference — it is a language requirement enforced by the interpreter. A `print` statement nested under another `print` statement (without a valid block opener like `if`, `for`, `def`) is illegal and will error out. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

The instructor notes that if you are new to indentation-based syntax, you will initially make mistakes. But within a few days it becomes natural, and the habit carries over — you start giving proper indentation even in other languages and scripts. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

## 1.6 Bash Script vs Python Script: Structural Comparison

The video explicitly places a Bash script and a Python script side-by-side to highlight the syntactic differences. The logic is identical — a variable `x` is set, and an `if/else` checks whether `x` equals zero.

| Feature             | Bash                                   | Python                               |
| ------------------- | -------------------------------------- | ------------------------------------ |
| Variable assignment | `x=0` (no spaces around `=`)           | `x = 0` (spaces allowed)             |
| Condition syntax    | `if [ $x -eq 0 ]` with square brackets | `if x == 0:` with colon, no brackets |
| Block opening       | `then` keyword                         | Colon `:` + indentation              |
| Block closing       | `fi` keyword                           | Return to previous indentation level |
| Else syntax         | `else`                                 | `else:` (with colon)                 |
| Indentation role    | Cosmetic only                          | **Structural — defines code blocks** |

 [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

This comparison exists to help learners coming from Bash understand that Python's block structure mechanism is entirely different. The absence of `fi` or any closing marker is not a shortcut — it is replaced by indentation as a first-class syntactic element.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing

We are writing and executing Python scripts on a Linux machine (CentOS 7 VM), understanding how to work with both Python 2 and Python 3, and learning how Python's indentation syntax works through hands-on comparison with Bash. The final outcome: you can write a Python script on any Linux machine, set the correct interpreter, execute it using multiple methods, and understand how indentation controls program logic. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

## Step 1: Log into a Linux Machine and Verify Python

SSH into any Linux machine — a VM, an EC2 instance, any CentOS/Ubuntu system. The video uses a **CentOS 7** machine. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Check Python availability:**

```bash
python
```

This opens the **Python interactive interpreter**. On CentOS 7, you will see **Python 2.7.x**. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Test a quick print statement (Python 2 syntax):**

```python
print "hello"
```

This works in Python 2 because `print` is a statement, not a function. Press `Ctrl+D` or type `exit()` to close the interpreter. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Connection to larger flow:** You have confirmed Python is installed and identified which version is the default. This determines what syntax your scripts must use.

***

## Step 2: Write a Python 2 Script

**2a. Install Vim (if not present on CentOS 7):**

```bash
yum install vim -y
```

| Part          | Meaning                            |
| ------------- | ---------------------------------- |
| `yum`         | Package manager for Red Hat/CentOS |
| `install vim` | Install the Vim text editor        |
| `-y`          | Auto-confirm                       |

 [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**2b. Create the script file:**

```bash
vim first-python-code.py
```

The `.py` extension is the standard convention for Python scripts. It is not technically required by Linux, but it is universally expected for clarity. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**2c. Write the script contents:**

```python
#!/usr/bin/python
print "statement one"
print
print "statement three"
```

| Line                      | Meaning                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------ |
| `#!/usr/bin/python`       | **Shebang line** — tells the OS to use the Python 2 interpreter at `/usr/bin/python` |
| `print "statement one"`   | Python 2 print statement                                                             |
| `print`                   | Prints a blank line (Python 2 allows `print` with no arguments)                      |
| `print "statement three"` | Another print statement                                                              |

Save and quit (`:wq` in Vim). [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Connection to larger flow:** You now have a Python 2 script ready to execute.

***

## Step 3: Execute the Python 2 Script

**Method 1 — Make executable and run directly:**

```bash
chmod +x first-python-code.py
```

| Part                   | Meaning                   |
| ---------------------- | ------------------------- |
| `chmod`                | Change file permissions   |
| `+x`                   | Add executable permission |
| `first-python-code.py` | Target file               |

Now run it:

```bash
./first-python-code.py
```

Or use the absolute path (e.g., `/root/first-python-code.py` if you are in `/root`). The OS reads the shebang, invokes `/usr/bin/python`, and the script runs. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Method 2 — Invoke interpreter explicitly (no executable permission or shebang needed):**

```bash
python first-python-code.py
```

This directly tells the OS which interpreter to use, bypassing the shebang and permission requirements. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Expected result:** Both methods print the three lines (with one blank line in the middle). [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

## Step 4: Install Python 3 and Observe the Version Conflict

**4a. Search for available Python 3 packages:**

```bash
yum search python3
```

This shows many Python 3-related packages. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**4b. Install Python 3:**

```bash
yum install python3 -y
```

 [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**4c. Verify:**

```bash
python3
```

This opens the **Python 3 interpreter**. Note the command is `python3`, not `python` (which still points to Python 2 on CentOS 7). [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Connection to larger flow:** You now have both Python 2 (`python`) and Python 3 (`python3`) available on the same machine. Scripts must match the version they target.

***

## Step 5: Create a Python 3 Script and See the Syntax Difference

**5a. Copy the Python 2 script:**

```bash
cp first-python-code.py first-python3-code.py
```

 [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**5b. Edit the copy:**

```bash
vim first-python3-code.py
```

Change the shebang line from `/usr/bin/python` to `/usr/bin/python3`:

```python
#!/usr/bin/python3
```

 [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**5c. Attempt to execute WITHOUT changing the print syntax:**

```bash
chmod +x first-python3-code.py
./first-python3-code.py
```

**Expected result: SYNTAX ERROR.** Python 3 does not recognize `print "text"`. It requires `print("text")`. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**5d. Fix the print statements to Python 3 syntax:**

```python
#!/usr/bin/python3
print("statement one")
print()
print("statement three")
```

Save and execute again. Now it works. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Key takeaway demonstrated:** Changing the interpreter path without updating the code syntax causes failure. The shebang and the code must be in agreement.

***

## Step 6: Understand Indentation Through PyCharm Comparison

The video switches to the **PyCharm editor** (a Python IDE) to demonstrate indentation. This is a visual teaching exercise, not a Linux operational step.

**6a. The Bash version (for reference):**

```bash
#!/bin/bash
x=0
if [ $x -eq 0 ]
then
  echo "in the if block"
  echo "value of x is 0"
else
  echo "in the else block"
  echo "value of x is non-zero"
fi
echo "outside"
```

Indentation in Bash is cosmetic. You can remove all indentation and it still works because `then`, `else`, and `fi` mark block boundaries. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**6b. The Python 3 version (identical logic):**

```python
x = 0
print("something")
if x == 0:
  print("in the if block")
  print("value of x is 0")
else:
  print("in the else block")
  print("value of x is non-zero")
print("this statement is outside")
```

 [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**6c. Execute with `x = 0`:**

The `if` block runs. Both `print` statements under `if` execute. The final `print` (no indentation) also executes because it is outside the `if/else` entirely. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**6d. Change `x = 2` and re-run:**

Now the `else` block runs. The final `print` still runs because it is outside both blocks. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**6e. Demonstrate indentation errors:**

Move the last `print` statement inward by 2 spaces → it now falls **under `else`**. This changes program logic without changing the text of the statement — only the indentation changed. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

Now deliberately **misalign** indentation (e.g., give 3 spaces where 2 are expected, or indent a `print` under another `print` without a block opener):

**Expected result: `IndentationError: expected an indented block`** — Python tells you exactly which line has the problem. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

**Debugging approach for indentation errors:** The error message gives you the **line number**. Go to that line and check the spacing. Either the line has wrong spacing, or the line before it opened a block (with `:`) that expects indented content. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

⚠️ **Expert Note**
The instructor notes that indentation errors are the most common beginner mistake. The fix is always the same: check the spaces on the reported line and the lines around it. Within a few days of practice, correct indentation becomes instinctive. The habit transfers to other languages too — you start indenting Bash, YAML, and other code properly even when it's not syntactically required. [\[201-python...ndentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/201-python-on-linux-versions-and-indentation.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Python on Linux — Version Map

```
CentOS 7 / RHEL ≤ 7:
    python  → Python 2.7 (default)
    python3 → Python 3 (must install: yum install python3)

Ubuntu ≥ 20.04:
    python3 → Python 3 (default)

Status: Python 2 = EOL (support stopped)
        Python 3 = standard going forward
Exception: Ansible, some Linux system tools still use Python 2
```

***

## Script Execution — Three Methods

```
Method 1: Direct execution (requires shebang + chmod +x)
    chmod +x script.py → ./script.py

Method 2: Explicit interpreter (no shebang/permissions needed)
    python script.py   OR   python3 script.py

Method 3: Interactive interpreter (no file)
    python  → type commands → Ctrl+D to exit
```

***

## Shebang Line

```
#!/usr/bin/python    → Python 2
#!/usr/bin/python3   → Python 3

Rule: Shebang version MUST match code syntax
      Wrong shebang + right code = SyntaxError
```

***

## Python 2 vs Python 3 — Key Syntax Difference (from video)

```
Python 2:  print "hello"      ← statement (no parentheses)
Python 3:  print("hello")     ← function (parentheses required)

Python 2 code + Python 3 interpreter = SyntaxError
```

***

## Indentation — The Core Mental Model

```
Bash block structure:            Python block structure:
    if ... then                      if ...:
      (code)         ← cosmetic        (code)    ← STRUCTURAL
    fi               ← explicit end    (dedent)  ← implicit end

Bash: delimiters (then/fi) define blocks → indentation optional
Python: indentation defines blocks → no delimiters exist
```

***

## Indentation Rules

```
1. Block opener (if/else/for/def) ends with COLON (:)
2. All statements in same block = SAME number of leading spaces
3. Block ends when indentation returns to previous level
4. Mismatched indentation → IndentationError (with line number)
5. Consistency within block required (2 spaces, 3 spaces, 4 spaces — pick one, stick to it)
```

***

## Indentation Controls Logic (Visual)

```python
if x == 0:
  print("A")       # belongs to if
  print("B")       # belongs to if (same indent)
else:
  print("C")       # belongs to else
  print("D")       # belongs to else (same indent)
print("E")         # OUTSIDE both (no indent) — always runs
```

Move `print("E")` inward by 2 spaces → becomes part of `else` block.

```
Indentation change = Logic change (no text change needed)
```

***

## Debugging Indentation Errors

```
IndentationError: expected an indented block (line N)
    └─→ Go to line N
        └─→ Check: is the spacing consistent with the block it's in?
            └─→ Check: did the previous line open a block with `:` that expects indented content?
                └─→ Fix spacing → re-run
```

***

## Script Creation Flow (CentOS 7)

```
1. vim script.py
2. Add shebang: #!/usr/bin/python  OR  #!/usr/bin/python3
3. Write code (match syntax to version)
4. Save (:wq)
5. chmod +x script.py
6. Execute: ./script.py  OR  python3 script.py
```

***

## Engineering Patterns

| Pattern                              | Manifestation                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **Pre-installed dependency**         | Python ships with Linux because OS tools depend on it — you inherit it, not install it               |
| **Version coexistence**              | `python` and `python3` as separate binaries on same system — parallel version management             |
| **Interpreter dispatch via shebang** | OS uses `#!` to route script to correct runtime — declarative execution binding                      |
| **Syntax-version coupling**          | Code syntax must match interpreter version — version mismatch = immediate failure                    |
| **Whitespace-as-syntax**             | Python uses indentation instead of delimiters — structure IS formatting                              |
| **Fail-fast on structure errors**    | `IndentationError` fires before execution — prevents logic bugs from bad structure                   |
| **Graduated execution methods**      | Interactive → explicit interpreter → direct execution: increasing formality, increasing requirements |

***

## Project Context

```
BEFORE: Linux basics, Bash scripting fundamentals
THIS LECTURE: Python execution on Linux + version awareness + indentation syntax
AFTER: Python 3 syntax deep-dive, scripting for DevOps automation
Key rule: Default to Python 3, fall back to Python 2 only when specific tools require it
```

***

This completes the full reconstruction. **Theory** explains *why* Python versions, shebangs, and indentation work the way they do. **Practical** walks through every command and demonstration from the video. The **Compression Map** gives you a rapid-reload index for the entire session. Let me know if you'd like Anki flashcards or want any section expanded! 🚀
