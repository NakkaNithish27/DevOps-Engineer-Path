# 🔄 Shell Scripting — Command Substitution — Deep Learning Material

**Source:** Video caption file — [94-command-substitution.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt?EntityRepresentationId=d2e62281-432f-4173-b1f2-d7d9f4fe4925) [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**Video Context:** The instructor teaches command substitution — the mechanism that captures the output of a command and stores it into a variable — then builds progressively from raw commands, through filtering with `grep` and `awk`, to a complete system health information script that uses command substitution throughout.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Command Substitution Is and Why It Matters

The instructor opens with a clear statement: "What command substitution does — it takes the output of a command and stores it into a variable." He emphasizes: "You will really need this if you really want to write some intelligent script." [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

Without command substitution, a script can only execute commands and display their output to the terminal. The script can *do* things, but it cannot *capture and reason about* what it did. Command substitution changes this fundamentally — it lets a script take the output that a command would normally print to the screen, capture it as a string, and store it in a variable. Once stored in a variable, that data can be filtered, combined with other data, used in messages, tested in conditions, or passed to other commands.

This is what separates a "dumb" script (a linear sequence of commands) from an "intelligent" script (one that captures system state, processes it, and makes decisions or reports based on it). Every script that monitors system health, generates reports, or adapts its behavior based on runtime conditions depends on command substitution.

***

## 1.2 The Two Syntaxes — Backticks and `$()`

Command substitution can be written in two ways: [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**Backticks:** `` VARIABLE=`command` ``

**Dollar-parentheses:** `VARIABLE=$(command)`

Both do exactly the same thing — the instructor explicitly states "both does the same thing." The command inside the backticks or `$()` is executed, its stdout output is captured, and that output is assigned to the variable.

The instructor demonstrates both: `` UP=`uptime` `` and `CURRENT_USERS=$(who)`.

🔍 **Deep Dive:** While functionally identical for simple cases, `$()` is the modern, preferred syntax for several reasons that become apparent in more complex scripts. `$()` nests cleanly — you can write `$(command1 $(command2))` — while backticks require awkward escaping for nesting (`` `command1 \`command2\`` ``). `$()` is also visually clearer: the opening `$(` and closing `)` are distinct characters, while backticks `` ` `` can be confused with single quotes `'\` at a glance. The instructor uses both interchangeably throughout the video, showing that you should recognize and be comfortable with both forms.

***

## 1.3 The Critical Mistake — Quotes vs. Backticks

The instructor deliberately demonstrates a common mistake: "If I put this into double quotes or single quotes or without quotes, what happens is it just stores the name of the command. That's it." [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

This is the most important conceptual distinction in this topic:

* `UP="uptime"` → the variable `UP` contains the **string** `"uptime"` (the literal word)
* `UP='uptime'` → same result — the string `"uptime"`
* `UP=uptime` → same — just the word `"uptime"` as a value
* `` UP=`uptime` `` → the variable `UP` contains the **output** of running the `uptime` command (e.g., `"12:05:02 up 3 days, 2 users, load average: 0.01, 0.02, 0.05"`)

The difference is between **storing a name** and **storing a result**. Quotes (single or double) and bare assignment all treat the right side as literal text. Only backticks or `$()` trigger execution of the command and capture of its output. This is the entire point of command substitution — it's the mechanism that says "run this, give me the output."

⚠️ **Expert Note:** This is one of the most frequent beginner mistakes in shell scripting. When a script doesn't produce the expected output and a variable contains a command name instead of command output, the first thing to check is whether command substitution syntax (backticks or `$()`) was actually used in the assignment.

***

## 1.4 Filtering Command Output — `grep` + `awk` Pipeline Inside Substitution

Raw command output is often too verbose or structured in a way that doesn't give you the single value you need. The instructor demonstrates the solution: **pipe-based filtering inside command substitution**. [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

The example: extracting the free RAM value from the `free` command's output. The `free` command outputs a multi-line table. The instructor builds a filter pipeline:

1. `free` → produces the full memory table
2. `| grep Mem` → filters to only the line starting with "Mem" (the physical memory row)
3. `| awk '{print $4}'` → from that line, extracts the 4th field (the "free" column value)

The instructor manually counts the columns — "one, two, three, four — 4th field" — to determine which `$` field number corresponds to the "free" value. This counting step is critical: `awk` splits lines into fields by whitespace, and you must count from the actual output to know which field position holds your target data. [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

The entire pipeline is then wrapped in command substitution:

```bash
FREE_RAM=$(free | grep Mem | awk '{print $4}')
```

This single line does three things: runs a command, filters its output through two stages, and stores the final extracted value in a variable. The instructor then uses it: `echo "Free RAM is $FREE_RAM mb"`.

The conceptual takeaway: command substitution doesn't just capture raw output — it captures the output of **any pipeline**, no matter how complex. You can chain as many pipes, greps, awks, seds, or cuts as you need inside `$()`, and the final output of the entire pipeline becomes the variable's value.

***

## 1.5 System Variables — `$USER` and `$HOSTNAME`

The instructor's system health script uses `$USER` and `$HOSTNAME` without defining them: `"Welcome $USER on $HOSTNAME"`. These are **system-defined environment variables** — they are pre-set by the shell when you log in. `$USER` contains the current username (e.g., `root`), and `$HOSTNAME` contains the machine's hostname (e.g., `scriptbox`). [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

The distinction from command substitution variables: system variables are **already available** — you don't need to capture them. Command substitution variables (like `$FREE_RAM`, `$LOAD`) must be **explicitly created** by running a command and storing its output. The health script uses both types together: system variables for identity information, command substitution variables for dynamic system state.

***

## 1.6 The System Health Script — Combining Everything

The instructor builds a complete script that prints system health information. It combines multiple concepts into one working system: [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

* **System variables** (`$USER`, `$HOSTNAME`) for identity context
* **Command substitution with filtering** for `FREE_RAM` — extracted from `free` output via `grep` + `awk`
* **Command substitution with filtering** for `LOAD` — extracted from `uptime` output via filtering
* **Command substitution with filtering** for root partition free space — extracted from disk usage commands

Each variable captures one specific metric by running a command, filtering the output to the exact value, and storing it. Then the script prints a formatted message using all these variables together.

The instructor's output: `"Welcome root on scriptbox, available free ram is 590 mb, current load average is [value] and free root partition is [value]."` [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

The engineering idea: each `$()` expression is a **sensor** — it queries one aspect of the system and returns a single data point. The script assembles multiple sensors into a dashboard. This pattern scales: add more command substitution variables to monitor more metrics.

The instructor also mentions a forward-looking use case: "Imagine you have a script like this that prints system information whenever you login to your system, and I'll show you how we are going to execute the script when we really log into the system." This refers to login-triggered script execution (covered in a future lecture). [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning to capture command output into variables using command substitution, then building a **system health information script** that extracts free RAM, load average, and free root partition space — and prints a formatted status message. The final outcome: running the script produces a clean, human-readable system health report. [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

***

## Step 1: Understand the Problem — Command Output Goes to Screen, Not to Variables

### Run a command normally:

```bash
uptime
```

**Expected output:** Something like `12:05:02 up 3 days, 2 users, load average: 0.01, 0.02, 0.05`

This output appears on screen and is immediately gone — no variable holds it, no script can use it. [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

### Try storing it with quotes (THE WRONG WAY):

```bash
UP="uptime"
echo $UP
```

**Output:** `uptime` — just the literal word. Not the command's output.

Same result with single quotes (`UP='uptime'`) or no quotes (`UP=uptime`). All three store the **string**, not the **result**. [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**This is the mistake to internalize:** quotes/no-quotes = literal text assignment. You need a different syntax to trigger execution.

***

## Step 2: Use Command Substitution — Backticks

```bash
UP=`uptime`
echo $UP
```

**Breakdown:**

* `` ` `` (backtick) — **not** a single quote `'`. Located on the tilde key (`~`) on most keyboards
* `uptime` — the command to execute
* The backticks tell bash: "Run this command, capture its stdout, and assign the output to `UP`" [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**Expected output of `echo $UP`:** The full uptime string (e.g., `12:05:02 up 3 days, 2 users, load average: 0.01, 0.02, 0.05`)

**Common mistake:** Using single quotes instead of backticks. They look similar but behave completely differently. Single quote `'` = literal string. Backtick `` ` `` = execute and capture.

***

## Step 3: Use Command Substitution — `$()` Syntax

```bash
CURRENT_USERS=$(who)
echo $CURRENT_USERS
```

**Breakdown:**

* `$()` — the modern command substitution syntax
* `who` — the command (shows logged-in users)
* The output of `who` is captured and stored in `CURRENT_USERS` [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**Expected output:** List of currently logged-in users, as `who` would normally print.

**Both syntaxes are equivalent.** Use whichever you prefer; `$()` is generally recommended for clarity and nestability.

***

## Step 4: Filter Command Output Before Storing — The `free` + `grep` + `awk` Pipeline

### First, examine the raw output:

```bash
free
```

This prints a multi-line table with columns for total, used, free, shared, buffers, available memory.

### Filter to the memory line:

```bash
free | grep Mem
```

This returns only the line starting with `Mem` — the physical memory row. [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

### Extract the specific field:

```bash
free | grep Mem | awk '{print $4}'
```

**Breakdown of `awk '{print $4}'`:**

* `awk` — a text-processing tool that splits each line into fields by whitespace
* `'{print $4}'` — print the 4th field
* The instructor manually counts: "one, two, three, four — 4th field" — this is the "free" column value [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**How to determine the field number:** Look at the `grep Mem` output and count the columns from left to right. The first field (`$1`) is `Mem:`, the second is total, the third is used, the fourth is free. Always count from the actual output — don't guess.

### Store the result:

```bash
FREE_RAM=$(free | grep Mem | awk '{print $4}')
echo "Free RAM is $FREE_RAM mb"
```

**Expected output:** `Free RAM is 590 mb` (or whatever the current free memory value is). [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**What happened:** The entire pipeline ran inside `$()`, the final output (a single number) was captured, and stored in `FREE_RAM`. The variable now holds just the extracted value, not the full `free` output.

**Connection to larger flow:** This is the core technique used in the health script — every metric is extracted using this same pattern: `command | filter | extract → variable`.

***

## Step 5: Build the System Health Script

The instructor has a pre-created script. Based on the video, it follows this structure: [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

```bash
#!/bin/bash

# System health monitoring script

# Using system variables for identity
echo "Welcome $USER on $HOSTNAME"

# Command substitution: Free RAM
FREE_RAM=$(free | grep Mem | awk '{print $4}')

# Command substitution: Load average
LOAD=$(uptime | awk -F'load average:' '{print $2}' )

# Command substitution: Free root partition
ROOT_FREE=$(df -h / | awk 'NR==2 {print $4}')

# Print system health
echo "Available free RAM is $FREE_RAM mb"
echo "Current load average is $LOAD"
echo "Free root partition is $ROOT_FREE"
```

**Variable breakdown:**

* `$USER` — system variable, no substitution needed — contains current username (e.g., `root`)
* `$HOSTNAME` — system variable — contains machine name (e.g., `scriptbox`)
* `$FREE_RAM` — command substitution — free memory extracted from `free` via `grep` + `awk`
* `$LOAD` — command substitution — load average extracted from `uptime` via filtering
* `$ROOT_FREE` — command substitution — root partition free space from disk usage command via filtering [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**Each command substitution is a sensor:** it queries one aspect of system state, filters to the exact value, and stores it. The script assembles all sensors into a readable report.

***

## Step 6: Execute the Script

```bash
chmod +x <scriptname>.sh
./<scriptname>.sh
```

**Expected output:**

```
Welcome root on scriptbox
Available free RAM is 590 mb
Current load average is 0.01, 0.02, 0.05
Free root partition is 15G
```

 [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

**Verification:** Each line should show a real, dynamic value — not a command name or empty string. If you see the command name instead of its output, the command substitution syntax is wrong (likely used quotes instead of backticks/`$()`).

**Connection to future lectures:** The instructor mentions this script will be reused later, specifically for **automatic execution on login** — configuring the system so this health report appears every time you SSH into the machine. [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Command Substitution — Core Mechanism

```
PURPOSE: Capture command OUTPUT → store in VARIABLE

TWO SYNTAXES (identical behavior):
  VAR=`command`          ← backticks (older)
  VAR=$(command)         ← dollar-parens (modern, preferred)

CRITICAL DISTINCTION:
  VAR="command"          → stores the WORD "command" (literal string)
  VAR=$(command)         → stores the OUTPUT of running command

PIPELINE SUPPORT:
  VAR=$(cmd1 | cmd2 | cmd3)  → entire pipeline runs, final output captured
```

***

## ⚡ Filtering Pattern — Extract One Value from Verbose Output

```
raw command → grep (select line) → awk (select field) → $() (capture)

Example:
  free                           → full memory table
  free | grep Mem                → only the Mem: line
  free | grep Mem | awk '{print $4}'  → only the 4th field (free value)
  FREE_RAM=$(free | grep Mem | awk '{print $4}')  → stored in variable

HOW TO COUNT awk FIELDS:
  Look at grep output → count words left-to-right
  $1=first word, $2=second, ... $N=Nth field
  ⚠️ Always count from actual output, never guess
```

***

## 📦 Variable Types in the Script

```
SYSTEM VARIABLES (pre-defined, always available):
  $USER      → current logged-in username
  $HOSTNAME  → machine's hostname

COMMAND SUBSTITUTION VARIABLES (you create these):
  $FREE_RAM  → $(free | grep Mem | awk '{print $4}')
  $LOAD      → $(uptime | <filtering>)
  $ROOT_FREE → $(df | <filtering>)
```

***

## 🔗 System Health Script — Architecture

```
┌─────────────────────────────────────────────┐
│           System Health Script               │
│                                              │
│  IDENTITY LAYER (system vars):               │
│    $USER ──────────────┐                     │
│    $HOSTNAME ──────────┤                     │
│                        ▼                     │
│              "Welcome $USER on $HOSTNAME"    │
│                                              │
│  SENSOR LAYER (command substitution):        │
│    free | grep | awk ──→ $FREE_RAM           │
│    uptime | filter ────→ $LOAD               │
│    df | filter ────────→ $ROOT_FREE          │
│                        ▼                     │
│              "Free RAM: $FREE_RAM mb"        │
│              "Load: $LOAD"                   │
│              "Root free: $ROOT_FREE"         │
│                                              │
│  FUTURE: auto-execute on SSH login           │
└─────────────────────────────────────────────┘
```

***

## 🔄 Mistake → Fix Recall

```
SYMPTOM: Variable prints the command name, not its output
  CAUSE: Used quotes or bare assignment instead of $() or backticks
  FIX:   Change VAR="cmd" → VAR=$(cmd)

SYMPTOM: Variable has too much data (whole table instead of one value)
  CAUSE: No filtering pipeline
  FIX:   Add grep (select line) + awk (select field) inside $()

SYMPTOM: awk prints wrong field
  CAUSE: Counted field position incorrectly
  FIX:   Re-examine grep output, recount columns from $1
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Sensor-Variable-Report**
`$(command | filter)` = a sensor. Each sensor captures one metric. Multiple sensors → assembled into a dashboard/report. This pattern scales to any number of metrics — CPU, disk, network, processes — by adding more command substitution variables.

**Pattern 2: Pipeline-Inside-Substitution**
Command substitution isn't limited to single commands. Any arbitrary pipeline (`cmd | grep | awk | sed | cut`) can live inside `$()`. The final stdout of the entire chain becomes the variable's value. This makes `$()` a universal "capture the result of any data transformation" tool.

**Pattern 3: Identity + State Separation**
System variables (`$USER`, `$HOSTNAME`) provide static identity context. Command substitution variables provide dynamic runtime state. Clean scripts separate these two layers — who/where am I (identity) vs. what's happening right now (state).

***

## 🎯 One-Line System Summary

> **Command substitution (`$(command)` or `` `command` ``) captures the stdout of any command or pipeline into a variable, enabling scripts to sense system state, filter it to exact values via `grep`+`awk`, and assemble dynamic reports — transforming passive command execution into intelligent data-driven scripting.** [\[94-command...bstitution \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/94-command-substitution.txt)
