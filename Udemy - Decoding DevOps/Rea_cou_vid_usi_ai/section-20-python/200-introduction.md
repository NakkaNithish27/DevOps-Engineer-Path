# 🎓 Deep Learning Material: Python for DevOps — Introduction, Installation & Development Environment Setup

**Source:** [200-introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt?EntityRepresentationId=31f055b9-dec8-4750-9b5f-98c79d001457) — Video caption reconstruction covering why Python is essential for DevOps engineers, installation on Windows and macOS, Anaconda Navigator, Jupyter Notebook, PyCharm IDE, Python interpreter, and first Python code execution across all three environments. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

*(Supplementary reference: [200.Anaconda+installation+on+Ubuntu+20.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf?EntityRepresentationId=d84e2d11-9321-40e6-a712-c09199fc6a30) — Ubuntu-specific Anaconda installation steps, referenced where relevant.)* [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why Python Is Essential for DevOps Engineers

The video opens with a clear position: any DevOps engineer should learn Python. The reasoning is layered across three distinct arguments. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**First — programming literacy as a foundation for automation tools.** The modern DevOps ecosystem runs on automation tools: Jenkins, Terraform, Ansible, Argo CD, and many others. These tools are not black boxes you simply click through — they derive their power from programming concepts and logic. Pipeline definitions, infrastructure-as-code templates, playbooks, and deployment manifests all use conditional logic, loops, variables, data structures, and abstraction. If you don't understand programming fundamentals, you can use these tools superficially but you cannot master them. You'll copy configurations without understanding why they work, and you'll be helpless when they break in unexpected ways. Python teaches you these foundational concepts — variables, functions, control flow, data manipulation — which transfer directly into understanding every major automation tool. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Second — customized automation when tools fall short.** Automation tools cover the common cases well, but real projects inevitably produce tasks that no existing tool handles cleanly. Maybe you need to parse a custom log format, interact with an API that has no Terraform provider, orchestrate a sequence of operations across multiple systems in a specific order, or transform data between two incompatible formats. In these situations, you write a Python script. Python becomes the glue between the things your automation tools can do and the things your project specifically needs. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Third — Python's ecosystem extends its reach indefinitely.** Python's power is amplified by its library ecosystem. If you need to interact with AWS, there's `boto3`. Google Cloud has its own Python SDK. Jenkins has Python bindings. Beyond DevOps, Python covers web development, data science, machine learning, and AI. The video emphasizes this breadth: "Python is used almost everywhere." For a DevOps engineer, this means the investment in learning Python pays off across virtually every domain you might encounter. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

***

## 1.2 Python as a Language — Key Characteristics

The video identifies Python as an **interpreted and interactive** language, placing it in the same category as Perl and PHP. This distinction matters operationally. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

With a **compiled** language (like C or Java), you write code, then run a separate compilation step that transforms your source code into machine code or bytecode, and only then can you execute it. With an **interpreted** language like Python, there is no separate compilation step. You write Python code and run it directly — the Python **interpreter** reads your code line by line and executes it on the spot. This means faster development cycles: write, run, see result, fix, repeat. There's no waiting for compilation. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

The **interactive** nature means you can also use Python in a live shell (the interpreter), typing statements one at a time and seeing results immediately — much like a Bash shell, but for Python code instead of system commands. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

The video also positions Python as "definitely a beginner's language" — easy to read, easy to write. It notes that while C used to be the traditional starting point for learning programming, Python has replaced it in modern times. This is relevant because the course assumes no prior programming experience. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

***

## 1.3 The Three Execution Environments — And Why Three Exist

The video introduces three distinct ways to write and run Python code. Understanding *why* each exists prevents confusion about which to use. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Jupyter Notebook** is a browser-based Python environment. You write code in "cells," execute individual cells, and see output inline. It is ideal for learning, experimentation, and short programs. You write a small piece of code, run it, see what happens, modify it, run again. This tight feedback loop makes it the best starting environment for beginners. Jupyter is launched from Anaconda Navigator. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**PyCharm Community Edition** is a full IDE (Integrated Development Environment). An IDE is designed for professional, sustained development — writing larger scripts, organizing code into projects, navigating complex file structures, using debugging tools, and managing dependencies. PyCharm automatically creates a **virtual environment** for each project (the video shows a path like `venv/scripts/python.exe`), meaning it uses an isolated Python installation rather than the system Python. This virtual environment concept is mentioned but deferred to later lectures. The key point now: PyCharm uses its own Python, not the one installed on your system. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**The Python Interpreter (shell)** is the raw, command-line interface to Python. On Windows, you open Git Bash; on macOS, you open Terminal. You type `python`, hit Enter, and you're inside the interpreter. You can type Python statements directly and see results. It is the most minimal environment — no file management, no project structure, no browser. It's useful for quick tests and verifying that Python is installed and working. The video explicitly notes: the Python interpreter only accepts Python statements — Linux commands and Windows commands will not work inside it. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

🔍 **Deep Dive**
The relationship between these three is hierarchical in terms of capability. The interpreter is the engine that runs Python code — it exists at the bottom of the stack. Jupyter Notebook is a user-friendly wrapper that sends code to the interpreter behind the scenes and displays results in a browser. PyCharm is a full development platform that also sends code to an interpreter (specifically, the one inside the virtual environment it creates). All three ultimately rely on the same core mechanism: the Python interpreter executing statements. They differ in the interface and tooling wrapped around it. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

***

## 1.4 Anaconda — What It Is and Why It's Used

Anaconda is not Python itself. It is a **distribution and environment manager** that bundles Python together with a large collection of libraries and tools. The video describes it as making it "easier to manage Python environment and launch application from it." Anaconda is widely used in data science, machine learning, and scientific computing because it pre-packages hundreds of commonly needed libraries. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

In this course, Anaconda's role is simpler: it provides **Anaconda Navigator**, a graphical launcher from which you can open Jupyter Notebook, PyCharm, VS Code, and other tools in a unified way. Instead of hunting for each tool separately, you open Navigator and launch what you need. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

For Ubuntu/Linux users specifically, the supplementary PDF ([200.Anaconda+installation+on+Ubuntu+20.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf?EntityRepresentationId=d84e2d11-9321-40e6-a712-c09199fc6a30)) describes a different installation path: downloading the Anaconda installer from the website, verifying it with `sha256sum`, running it with `bash`, and then activating it via `source ~/.bashrc` and `conda init`. The `conda config --set auto_activate_base True/False` commands control whether the Anaconda base environment activates automatically every time you open a terminal. [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

***

## 1.5 The `print()` Function — First Python Concept

The first actual Python code demonstrated is the `print()` function. The video teaches several things through this simple example: [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

`print()` is Python's equivalent of `echo` in Bash — it outputs text to the screen. In Python 3, `print` is a **function**. A function has a name followed by parentheses, and you pass **arguments** inside the parentheses. The argument to `print()` is the text you want to display, wrapped in double quotes. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

The video demonstrates a critical syntax rule: **do not put spaces before the statement.** Writing `print(...)` starting from the first column is correct. Adding a leading space causes an `IndentationError`. Python uses indentation as part of its syntax (unlike most other languages where indentation is cosmetic). The video flags this as something that will be explained in the next lecture but establishes the rule immediately: start all statements from the first column unless you have a specific structural reason not to. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

***

## 1.6 Course Scope — What Will Be Covered

The video outlines the course trajectory: Python fundamentals → simple automation scripts → cloud computing automation with Python → leveraging AI to expand Python knowledge. This is a DevOps-oriented Python course — the goal is not to become a Python software developer but to gain enough programming skill to write automation, interact with cloud APIs, and understand the logic behind DevOps tools. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a complete Python development environment on our local machine — installing Python, Anaconda, and PyCharm — and then verifying that all three execution methods (Jupyter Notebook, PyCharm IDE, and the Python interpreter) work correctly by running our first Python code. The final outcome: you have three working ways to write and execute Python, you understand when to use each, and you've confirmed everything functions by printing output. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

***

## Step 1: Install Python

Python comes pre-installed on Linux and macOS. On Windows, you need to install it manually. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Windows** — Open **PowerShell as Administrator**:

```powershell
choco install python -y
```

| Part             | Meaning                                                        |
| ---------------- | -------------------------------------------------------------- |
| `choco`          | Chocolatey — a Windows package manager (must be pre-installed) |
| `install python` | Installs the latest Python distribution                        |
| `-y`             | Auto-confirms the installation prompt                          |

 [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**macOS** — Open **Terminal**:

```bash
brew install python
```

| Part             | Meaning                              |
| ---------------- | ------------------------------------ |
| `brew`           | Homebrew — the macOS package manager |
| `install python` | Installs or upgrades Python          |

 [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Connection to larger flow:** Python is the core runtime. Everything else (Anaconda, Jupyter, PyCharm) depends on Python being installed.

***

## Step 2: Install Anaconda

**Windows:**

```powershell
choco install anaconda3
```

**macOS:**

```bash
brew install --cask anaconda
```

| Part       | Meaning                                                            |
| ---------- | ------------------------------------------------------------------ |
| `--cask`   | Tells Homebrew this is a GUI application (not a command-line tool) |
| `anaconda` | The Anaconda distribution                                          |

 [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Ubuntu/Linux** (from the supplementary PDF):

1. Download the installer from `https://www.anaconda.com/products/individual#linux`

2. Verify the download:
   ```bash
   sha256sum /path/filename
   ```
   This computes a checksum to confirm the file wasn't corrupted or tampered with. [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

3. Run the installer:
   ```bash
   bash ~/Downloads/Anaconda3-2020.02-Linux-x86_64.sh
   ```
   * Press **Enter** repeatedly through the license text.
   * Type **yes** to accept the license.
   * Press **Enter** to confirm the installation path.
   * Wait for unpacking.
   * Type **yes** when asked to initialize conda. [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

4. Activate Anaconda:
   ```bash
   source ~/.bashrc
   conda config --set auto_activate_base True
   conda init
   ```
   These commands reload your shell configuration and enable the Anaconda base environment. [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

**Connection to larger flow:** Anaconda provides Anaconda Navigator, which is the launcher for Jupyter Notebook and can also launch PyCharm and VS Code.

***

## Step 3: Install PyCharm

**Windows:**

```powershell
choco install pycharm-community
```

**macOS:**

```bash
brew install --cask pycharm-ce
```

 [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Ubuntu/Linux** (from the supplementary PDF):
Go to the **Software Installer** (Ubuntu Software Center) in the menu bar, search for "PyCharm," select **PyCharm Community**, and click **Install**. [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

**After all installations — reboot your computer once.** This ensures all paths, environment variables, and shell configurations are properly loaded. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

***

## Step 4: Launch Jupyter Notebook and Write First Code

**4a. Open Anaconda Navigator:**

On Windows, open the Start Menu and search for **Anaconda Navigator**. On macOS, find it in Applications. On Linux, open a terminal and run `jupyter notebook` directly (after activating conda). [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**4b. Launch Jupyter Notebook:**

In Anaconda Navigator, find **Jupyter Notebook** and click **Launch**. This opens your default web browser with a URL showing your folder structure. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**4c. Create a working folder:**

Click the **New** dropdown → **Folder**. Rename it to something like `python-practice`. This folder is created in your home directory. Navigate into it. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**4d. Create a new notebook:**

Click **New** → **Python 3**. This opens a new notebook with an empty cell. Rename the notebook (click on "Untitled" at the top) to something like `first-python-notebook`. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**4e. Write and execute code:**

In the first cell, type:

```python
print("Welcome to Python")
```

Click the **Run** button (or press Shift+Enter). The output `Welcome to Python` appears directly below the cell. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Critical rule:** Do **not** put any spaces before `print`. This code is wrong:

```python
 print("Welcome to Python")
```

This will produce an `IndentationError`. All statements must start from the first column. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**4f. Save the notebook:**

Click **Save**. The notebook file (`.ipynb`) is saved in the folder you created. You can close the tab, navigate back to the folder, and double-click the notebook to reopen it in a new tab. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Connection to larger flow:** Jupyter Notebook is confirmed working. You now have a browser-based environment for learning and quick experimentation.

***

## Step 5: Launch PyCharm and Write First Code

**5a. Launch PyCharm:**

From Anaconda Navigator, find **PyCharm Community** and click **Launch**. (Or open it from your system's application menu.) [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

On first launch, you may get a prompt to import settings from VS Code or other editors. Click **Skip**. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**5b. Create a new project:**

Click **New Project**. Give it a name (e.g., `my-python-scripts`). Note the path where it will be saved. Click **Create**. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

The editor opens showing the project folder structure on the left side. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**5c. Create a Python file:**

Right-click on the project folder → **New** → **Python File**. Type a name (e.g., `first_script`) — do **not** add `.py`, PyCharm adds the extension automatically. Press Enter. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**5d. Write code:**

Type the same `print()` statements in the editor. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**5e. Run the script:**

Right-click inside the editor → **Run 'first\_script'**. The output appears in the bottom panel. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

Notice the execution path shown in the output panel — something like `venv/scripts/python.exe`. This means PyCharm created a **virtual environment** and is using the Python interpreter from that environment, not the system-wide Python. This is normal and expected behavior; virtual environments are covered in later lectures. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Connection to larger flow:** PyCharm is confirmed working. You now have a professional IDE for writing larger scripts and managing projects.

***

## Step 6: Verify the Python Interpreter (Command Line)

**6a. Open a terminal:**

* **Windows:** Open **Git Bash**
* **macOS:** Open **Terminal**

 [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**6b. Enter the Python interpreter:**

```bash
python
```

Hit Enter. You should see the Python version number and a `>>>` prompt. This is the Python interpreter — a live, interactive shell where you type Python statements and see results immediately. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**6c. Run a statement:**

```python
print("Welcome to Python")
```

The output prints immediately. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**6d. Understand the boundary:**

This interpreter **only** accepts Python statements. If you type a Linux command like `ls` or a Windows command like `dir`, it will not work. The Python interpreter is not a system shell — it is a Python-only environment. [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**6e. Exit the interpreter:**

Type `exit()` or press `Ctrl+D` (macOS/Linux) / `Ctrl+Z` then Enter (Windows). [\[200-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200-introduction.txt)

**Connection to larger flow:** All three execution methods are verified. You can now choose the appropriate one depending on the task — Jupyter for learning/experimentation, PyCharm for project development, interpreter for quick one-off tests.

***

## Ubuntu/Linux: Controlling Anaconda Base Environment Activation

After installing Anaconda on Ubuntu, the base environment may activate automatically every time you open a terminal (you'll see `(base)` in your prompt). To control this: [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

**To stop auto-activation:**

```bash
conda config --set auto_activate_base False
source ~/.bashrc
```

**To re-enable and launch Jupyter:**

```bash
conda config --set auto_activate_base True
source ~/.bashrc
jupyter notebook
```

`source ~/.bashrc` reloads the shell configuration so the change takes effect immediately. [\[200.Anacon...+Ubuntu+20 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/200.Anaconda+installation+on+Ubuntu+20.pdf)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Why Python for DevOps — Three-Layer Argument

```
1. Foundation:    Programming concepts → required to master automation tools
                  (Jenkins, Terraform, Ansible, Argo CD all use programming logic)

2. Gap-filler:    Automation tools can't cover everything → Python fills custom gaps

3. Ecosystem:     Libraries extend Python into AWS/GCP/Azure, ML, web dev, data science
```

***

## Python Language Identity

```
Type:        Interpreted (no compilation step) + Interactive (live shell)
Comparison:  Like Perl, PHP — write and run directly
Positioning: Beginner-friendly, replaced C as first language
```

***

## Three Execution Environments

```
┌──────────────────────┬─────────────────────┬──────────────────────┐
│   Jupyter Notebook   │   PyCharm IDE       │  Python Interpreter  │
├──────────────────────┼─────────────────────┼──────────────────────┤
│ Browser-based        │ Full IDE            │ CLI / terminal       │
│ Cell-by-cell exec    │ Project-based       │ Statement-by-stmt    │
│ Best for: learning,  │ Best for: real      │ Best for: quick      │
│   short programs,    │   scripts, larger   │   tests, verifying   │
│   experimentation    │   codebases         │   Python works       │
├──────────────────────┼─────────────────────┼──────────────────────┤
│ Launched from:       │ Launched from:      │ Launched from:       │
│ Anaconda Navigator   │ Navigator / menu    │ Git Bash / Terminal  │
│                      │                     │ Command: python      │
├──────────────────────┼─────────────────────┼──────────────────────┤
│ Saves: .ipynb files  │ Saves: .py files    │ No file persistence  │
│ in home directory    │ in project dir      │                      │
└──────────────────────┴─────────────────────┴──────────────────────┘

All three → Python interpreter underneath
```

***

## Installation Commands — Quick Reference

```
               Windows (PowerShell Admin)          macOS (Terminal)
─────────────────────────────────────────────────────────────────────
Python         choco install python -y              brew install python
Anaconda       choco install anaconda3              brew install --cask anaconda
PyCharm        choco install pycharm-community      brew install --cask pycharm-ce

Linux/Ubuntu:  Python → pre-installed
               Anaconda → download .sh from website → sha256sum → bash installer
               PyCharm → Ubuntu Software Center → search → install

⚠️ Reboot after all installations
```

***

## Ubuntu Anaconda Activation Control

```
Deactivate base:   conda config --set auto_activate_base False → source ~/.bashrc
Reactivate base:   conda config --set auto_activate_base True  → source ~/.bashrc
Launch Jupyter:     jupyter notebook
Initialize:         conda init
```

***

## Anaconda's Role

```
Anaconda ≠ Python
Anaconda = Python distribution + library bundle + environment manager

Anaconda Navigator = graphical launcher
    ├── Jupyter Notebook
    ├── PyCharm Community
    └── VS Code
```

***

## First Python Concept: `print()`

```
print("text")
  │      │
  │      └── argument (the text to output), in quotes
  └── function name, followed by parentheses = function call

Equivalent of: echo in Bash

⚠️ CRITICAL RULE: No leading spaces before statements
   print("ok")    ← correct (starts at column 1)
    print("ok")   ← IndentationError (space before print)
```

***

## PyCharm Virtual Environment (Implicit)

```
PyCharm auto-creates: venv/ inside project directory
Uses:                 venv/scripts/python.exe (NOT system Python)
Why:                  Isolation — project dependencies don't clash with system
Detail:               Deferred to later lectures
```

***

## Course Trajectory

```
Python fundamentals → automation scripts → cloud computing automation → AI-powered expansion
                                            (AWS, GCP, Azure)
```

***

## Key Engineering Patterns

| Pattern                             | Manifestation                                                                                                              |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Layered tooling**                 | Three environments at different abstraction levels, all using the same interpreter underneath                              |
| **Environment isolation**           | PyCharm auto-creates venv; Anaconda manages environments — never pollute system Python                                     |
| **Verify-before-proceeding**        | Install → reboot → launch each tool → run test code → confirm output                                                       |
| **Interpreter as universal engine** | Jupyter, PyCharm, CLI all delegate to the same Python interpreter — the tool changes, the engine doesn't                   |
| **Skill transferability**           | Programming fundamentals learned in Python transfer to understanding Jenkins pipelines, Terraform logic, Ansible playbooks |

***

## Validation Sequence

```
1. Install Python + Anaconda + PyCharm → Reboot
2. Open Anaconda Navigator → Launch Jupyter → create folder → create notebook → print() → output ✓
3. Navigator → Launch PyCharm → new project → new .py file → print() → run → output ✓
4. Git Bash / Terminal → python → print() → output ✓
→ All three environments confirmed working
```

***

This completes the full reconstruction of the Python introduction lecture. **Theory** explains the reasoning behind every tool and concept, **Practical** walks through every installation and first-run step, and the **Compression Map** gives you instant reload capability for future revision. Let me know if you'd like Anki flashcard export or any section refined! 🚀
