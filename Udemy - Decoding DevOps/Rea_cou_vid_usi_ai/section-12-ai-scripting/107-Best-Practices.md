# 🎓 Applying Best Practices to Bash Scripts with GitHub Copilot — Deep Learning Material

**Source:** Video caption file — *Apply Best Practices (GitHub Copilot-Assisted Bash Refactoring)* [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Core Idea: Scripts That Work vs. Scripts That Work *Properly*

The lecture starts with an existing, functional web setup script (`websetup.sh`) that downloads an artifact from a URL and sets up a website. It works. But the instructor immediately asks the critical engineering question: **"Can it be better? Of course it can."** This frames the entire lecture — the goal is not to add new features but to **refactor existing working code into production-quality code** using developmental best practices. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

The tool used to drive the refactoring is **GitHub Copilot**, an AI coding assistant integrated into VS Code. But the lecture is not about blindly accepting AI suggestions — the instructor accepts suggestions, then **carefully explains each change**, using Copilot's own `/explain` feature to understand *why* each improvement matters. The learning model is: AI suggests → you understand → you decide. This dual benefit is explicitly noted: "We have improved our code and we have also seen how to ask the Copilot, the AI tool, for the explanation."

***

## 1.2 — Defensive Shell Initialization: `set -euo pipefail`

The single most important improvement Copilot suggests is adding a defensive initialization line at the top of the script. This line is described as a **"common best practice in Bash scripting"** and consists of three options that fundamentally change how the shell handles errors. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### `set -e` — Exit on Any Command Failure

Without `-e`, when a command in your script fails (returns non-zero exit code), Bash **silently continues** to the next line. The script keeps running as if nothing happened. This is dangerous — a failed `yum install` followed by a `systemctl start` will try to start a service that was never installed, producing confusing cascading failures.

With `-e`, the script **immediately exits** if any command returns a non-zero exit status. The failure is caught at the point it occurs, not three commands later. This connects directly to the exit code concept from earlier lectures — recall that exit code `0` means success and non-zero means failure. `set -e` automates the act of checking `$?` after every single command. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### `set -u` — Exit on Undefined Variables

Without `-u`, if you reference a variable that was never assigned a value (e.g., a typo like `$PAKAGE` instead of `$PACKAGE`), Bash silently expands it to an **empty string**. Your commands then execute with missing values, producing "weird results" — the instructor's exact words. A command like `yum install $PAKAGE` becomes `yum install ` (nothing), which either does nothing or installs something unexpected. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

With `-u`, the script **immediately exits** when any undefined variable is referenced. This catches typos, missing variable assignments, and — critically — situations where **user input is expected but not provided**. The instructor explicitly connects this to the user input scenario: "If the user is not entering the value, then the variable is not defined. You don't want your commands to get executed with non-defined variables." [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### `set -o pipefail` — Exit on Pipeline Failure

Without `pipefail`, in a pipeline like `command1 | command2 | command3`, Bash reports only the **exit code of the last command** in the chain. If `command1` fails catastrophically but `command3` succeeds, Bash considers the entire pipeline successful. The failure is **silently swallowed**.

With `pipefail`, if **any command** in a pipeline fails, the entire pipeline's exit code is non-zero. Combined with `-e`, this means the script exits. You don't want to continue processing data from a broken pipeline. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

> 🔍 **Deep Dive:** These three options work together as a **defense-in-depth system** for script reliability. `-e` catches command failures. `-u` catches variable errors. `-o pipefail` catches hidden pipeline failures. Together, they transform Bash from a "keep going no matter what" environment into a "fail fast, fail loud" environment. This is the same philosophy behind strict mode in programming languages, defensive coding in production systems, and the "fail-fast" principle in distributed systems design. Every automation tool that generates Bash scripts (Ansible, Chef, etc.) uses this pattern in generated scripts.

> ⚠️ **Expert Note:** `set -e` has edge cases — it doesn't trigger on failures inside `if` conditions, command substitutions with `||`, or functions called in conditional contexts. This is by design (you need to be able to test for failure without exiting). But it means `-e` is not a complete safety net — it's a baseline that should be combined with explicit error checking for critical operations.

***

## 1.3 — Functions: Reusable Code Blocks in Bash

The second major improvement is **restructuring the script's logic into functions**. A function is a named block of reusable code — instead of writing the same lines of code repeatedly, you write them once inside a function definition and **call** that function whenever you need it. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### Function Definition Syntax

```bash
function_name() {
    # code goes here
}
```

The function name is followed by `()`, and the code body is enclosed in `{ }` curly braces. The video demonstrates this with a `log` function. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### Function Arguments — `$1`, `$2`, etc.

Functions accept arguments using the **same positional parameter system** as scripts themselves. When you call `log "Installing packages"`, the text `"Installing packages"` becomes `$1` inside the `log` function. `$2` would be the second argument, and so on. This is the exact same mechanism as script-level `$1`–`$9` (from the system variables lecture), but scoped to the function. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### The `log` Function Example

The video shows a `log` function that takes a message as `$1` and prints it with decorative hash lines above and below — creating formatted, visible output in the terminal. Every time the script needs to announce what it's doing, it calls `log "message"` instead of writing three `echo` statements. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### Functions Calling Functions

After Copilot adds more functions, the script shows a deeper architectural pattern: **functions calling other functions**. For example, an `install_packages` function might call the `log` function internally to announce what it's doing before executing the installation. This creates a **layered execution model** — high-level functions orchestrate lower-level functions. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### The Main Execution Block

After all functions are defined, the script has a **main execution section** at the bottom where functions are called in order:

```bash
# Main script execution
install_dependencies
install_packages
deploy_artifact
start_service
```

This separation — **definitions at the top, execution at the bottom** — is a fundamental code organization pattern. The function definitions describe *what each piece does*. The main block describes *the order of operations*. Someone reading the main block immediately understands the script's flow without reading implementation details. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

> 🔍 **Deep Dive:** The instructor notes that functions will be explored more deeply in **Python scripting** later in the course. In Bash, functions are relatively simple — they're essentially named groups of commands. In Python, functions gain additional capabilities (return values, default arguments, scope management, etc.). But the core principle is identical: **encapsulate reusable logic, call it by name, pass data via arguments.** Understanding Bash functions provides the mental model that transfers directly to every programming language.

***

## 1.4 — Using GitHub Copilot as a Learning and Refactoring Tool

The video demonstrates two distinct ways of interacting with GitHub Copilot in VS Code, both valuable for learning:

### Inline Chat for Code Improvement

Select code → press `Ctrl+I` (Windows) or `Cmd+I` (Mac) → type a prompt like **"improve the code according to developmental best practices"** → Copilot suggests refactored code. You can accept or reject the suggestions. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### Inline Chat with Slash Commands for Explanation

Select code → press `Ctrl+I` → type **`/explain`** → Copilot explains what the selected code does. If the explanation is too small in the inline view, click **"View in Chat"** to see it in the full chat panel. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

The workflow the instructor models is: **improve → understand → accept**. Never accept AI suggestions blindly. Use the explanation feature to learn *why* each change was made, then make an informed decision.

***

## 1.5 — Testing Scripts via Vagrant Sync Folder

The video briefly covers the mechanics of testing scripts. There are two approaches: **copy the script to the VM manually**, or use the **Vagrant sync folder**. The sync folder maps a directory on your host machine to `/vagrant` inside the VM. When you edit scripts in VS Code on your host, they appear automatically in `/vagrant` on the VM. The instructor reminds: **always save your file** (`Ctrl+S`) in VS Code before testing — unsaved edits won't appear in the sync folder. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We're taking an existing, working Bash web setup script and **refactoring it into production-quality code** using GitHub Copilot's AI suggestions. The final outcome: the same script with defensive error handling (`set -euo pipefail`), organized into reusable functions, with clean logging and a readable main execution flow. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

## Step 1: Open the Script in VS Code and Review It

### What We're Doing

Opening `websetup.sh` in VS Code and reading through it to refresh our understanding before refactoring.

### The Action

Open `websetup.sh` in VS Code. The script is a simple web setup: downloads an artifact from `twoplay.com` and sets up the website. Read it top to bottom. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### Connection to Larger Flow

You need to understand the existing code before you can evaluate whether Copilot's improvements are correct and valuable. Never refactor code you don't understand.

***

## Step 2: Ask Copilot to Improve the Code

### What We're Doing

Selecting the entire script and using Copilot's inline chat to request best-practice improvements.

### The Steps

1. **Select all code** in `websetup.sh` (Ctrl+A or manually select).
2. **Open inline chat**: Press `Ctrl+I` (Windows) or `Cmd+I` (Mac). [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)
3. **Type the prompt:**

```
improve the code according to developmental best practices
```

4. **Press Enter.** Copilot generates a refactored version of the script.
5. **Review the suggestions** — don't blindly accept.
6. **Accept** the suggestions if they look correct. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### What Copilot Adds

The primary additions:

* `set -euo pipefail` at the top of the script (defensive initialization)
* A `log` function for formatted output
* Restructured code into multiple functions
* A main execution block at the bottom calling functions in order

### Common Mistakes

* **Accepting without reviewing** — Copilot suggestions are usually good but not always perfect. Always read the diff.
* **Forgetting to save** — Press `Ctrl+S` after accepting changes. Unsaved changes won't be reflected in the VM sync folder.

***

## Step 3: Understand `set -euo pipefail` Using Copilot's Explain Feature

### What We're Doing

Selecting the `set -euo pipefail` line and asking Copilot to explain it, so we understand what was added and why.

### The Steps

1. **Select the line** `set -euo pipefail`.
2. **Open inline chat**: `Ctrl+I` / `Cmd+I`.
3. **Type:** `/explain`
4. **Press Enter.** [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)
5. If the explanation appears too small in the inline popup, click **"View in Chat"** to see the full explanation in the chat panel.

### What Copilot Explains

* **`-e`** → Exit immediately if any command returns non-zero (failure). Recall from the exit code lecture: `$? = 0` means success, non-zero means failure. `-e` automates checking this after every command. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)
* **`-u`** → Exit if any undefined variable is referenced. Prevents commands from running with empty/missing values. Especially important when scripts accept user input. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)
* **`-o pipefail`** → If any command in a pipeline fails, the entire pipeline is considered failed. Without this, only the last command's exit code is reported. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### How to Verify Understanding

Ask yourself: "What would happen without each flag?" If you can answer that for all three, you understand the improvement.

***

## Step 4: Understand the `log` Function

### What We're Doing

Examining the function Copilot created for formatted logging output.

### The Code

```bash
log() {
    echo "######################################"
    echo "$1"
    echo "######################################"
}
```

**Breakdown:**

* `log()` — Defines a function named `log`
* `{ }` — Curly braces contain the function body
* `echo "####..."` — Prints a decorative separator line
* `echo "$1"` — Prints the **first argument** passed to the function. When called as `log "Installing packages"`, `$1` becomes `"Installing packages"`. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)
* The function prints: separator → message → separator

### How It's Called

```bash
log "Installing packages"
```

This calls the `log` function and passes `"Installing packages"` as `$1`. The output:

```
######################################
Installing packages
######################################
```

### Connection to Larger Flow

The `log` function replaces scattered `echo` statements throughout the script. Every major step now has consistent, visible, formatted output — making it easy to track script progress during execution.

***

## Step 5: Ask Copilot to Add More Functions

### What We're Doing

Requesting Copilot to further decompose the script into more granular functions.

### The Steps

1. **Select the entire code.**
2. **Open inline chat**: `Ctrl+I` / `Cmd+I`.
3. **Type a prompt** asking to add more functions.
4. **Accept** the suggestions. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### What Copilot Produces

Multiple functions, each handling one logical step of the deployment:

* Installing dependencies
* Installing packages
* Deploying the artifact
* Starting the service

Functions call other functions internally (e.g., each function calls `log` to announce what it's doing). [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### The Main Execution Block

At the bottom of the script, all functions are called in sequence:

```bash
# Main script execution
install_dependencies
install_packages
deploy_artifact
start_service
```

**Why This Matters:** Someone reading this block instantly understands the **entire deployment flow** without reading any implementation details. The function names describe what each step does. The order of calls describes the operational sequence. This is **self-documenting code**. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

### How to Verify

```bash
cat websetup.sh
```

Confirm: function definitions at the top, main execution calls at the bottom, functions called in the correct operational order.

***

## Step 6: Save and Test the Refactored Script

### What We're Doing

Saving the refactored script and testing it on the VM.

### The Steps

1. **Save in VS Code**: `Ctrl+S`. The instructor explicitly warns about this — unsaved changes won't appear in the VM. [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)
2. **Access the script in the VM**: Either copy it to the VM, or use the Vagrant sync folder (`/vagrant` directory inside the VM).

```bash
cd /vagrant
ls    # should see your scripts including websetup.sh
bash websetup.sh
```

### How to Verify Success

* The script should produce clean, formatted output with `log` messages marking each phase.
* If any command fails, the script should **immediately exit** (thanks to `set -e`) rather than continuing with broken state.
* No "weird results" from undefined variables (thanks to `set -u`).

### Common Mistakes

* **Not saving in VS Code before testing** — The sync folder reflects the last saved state, not the current editor state.
* **Running from the wrong directory** — Make sure you're in `/vagrant` or wherever the script was copied.

> ⚠️ **Expert Note:** After refactoring, always test the **failure paths** too, not just the success path. Temporarily introduce a bad command or unset a variable to confirm that `set -euo pipefail` actually catches and exits as expected. A safety net you never test is a safety net you can't trust.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ What This Lecture Does

```
BEFORE: Working but fragile script (no error handling, flat structure, scattered echo)
AFTER:  Production-quality script (defensive init, functions, structured flow, logging)
TOOL:   GitHub Copilot (suggest improvements + explain changes)
```

 [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

## 🛡️ `set -euo pipefail` — Defensive Initialization

```
set -e           → Exit on ANY command failure ($? ≠ 0)
                   ├── Without: script silently continues after failures
                   └── With:    script stops at the point of failure

set -u           → Exit on ANY undefined variable reference
                   ├── Without: undefined vars expand to "" → weird results
                   └── With:    typos and missing inputs caught immediately
                   └── Critical for: user input, variable typos, missing assignments

set -o pipefail  → Exit if ANY command in a pipeline fails
                   ├── Without: only last command's exit code matters
                   └── With:    hidden mid-pipeline failures caught

COMBINED: "Fail fast, fail loud" — Bash strict mode
```

 [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

## 📦 Function Architecture

```
DEFINITION SYNTAX:
  function_name() {
      # code
      # $1 = first argument, $2 = second, etc.
  }

CALLING:
  function_name "arg1" "arg2"

EXAMPLE — log function:
  log() {
      echo "######################################"
      echo "$1"                                      ← argument becomes $1
      echo "######################################"
  }
  
  log "Installing packages"    ← call with message

FUNCTION COMPOSITION:
  install_packages() {
      log "Installing packages"     ← function calls function
      yum install $PACKAGE -y
  }
```

 [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

## 📐 Refactored Script Structure

```
#!/bin/bash
set -euo pipefail                    ◄── DEFENSIVE INIT (fail fast)

# ─── FUNCTION DEFINITIONS ───
log() { ... }                        ◄── Logging utility
install_dependencies() { ... }       ◄── Step 1 logic
install_packages() { ... }           ◄── Step 2 logic
deploy_artifact() { ... }            ◄── Step 3 logic
start_service() { ... }              ◄── Step 4 logic

# ─── MAIN EXECUTION ───
install_dependencies                 ◄── Call step 1
install_packages                     ◄── Call step 2
deploy_artifact                      ◄── Call step 3
start_service                        ◄── Call step 4

PRINCIPLE: Definitions at top, execution at bottom
           Main block = readable operational flow
           Function names = self-documenting
```

***

## 🤖 GitHub Copilot Workflow

```
IMPROVE:  Select code → Ctrl+I → "improve according to best practices" → Accept
EXPLAIN:  Select code → Ctrl+I → /explain → View in Chat (if too small)
ADD:      Select code → Ctrl+I → "add more functions" → Accept

WORKFLOW: Suggest → Understand → Accept (never blind acceptance)
```

 [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

## 🔄 Script Testing via Vagrant Sync Folder

```
HOST (VS Code)                         VM (/vagrant)
  │                                      │
  ├── Edit websetup.sh                   │
  ├── Ctrl+S (MUST SAVE!)   ──sync──►    ├── /vagrant/websetup.sh (updated)
  │                                      ├── bash /vagrant/websetup.sh (test)
  │                                      └── Verify output + behavior
  
  ALTERNATIVE: scp script to VM manually
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: FAIL-FAST INITIALIZATION (set -euo pipefail)
  Set strict error handling BEFORE any logic runs
  → Same as: strict mode in JavaScript, -Wall -Werror in C,
    raise on error in Python, fail-fast in microservices
  → PRINCIPLE: Catch errors at the source, not downstream

PATTERN 2: FUNCTION DECOMPOSITION
  Flat script → named functions → main execution block
  → Same as: Refactoring monolith into services,
    extracting methods in OOP, modular Terraform,
    Ansible roles, Helm chart templates
  → BENEFIT: Readability, reusability, testability

PATTERN 3: FUNCTION ARGUMENTS = SCRIPT ARGUMENTS ($1, $2)
  Same positional parameter system at function scope
  → Transferable to: Python *args, function parameters in any language
  → Bash functions and scripts share the same argument interface

PATTERN 4: DEFINITION/EXECUTION SEPARATION
  Define all functions first, call them at the bottom
  → Same as: class definitions → main() in Python/Java/Go,
    Terraform modules → root module calls,
    Library imports → application logic
  → BENEFIT: Main block becomes self-documenting flow

PATTERN 5: AI-ASSISTED LEARNING LOOP
  AI suggests → Human explains/understands → Human decides
  → Not blind automation — augmented learning
  → Copilot as teacher AND tool simultaneously
```

 [\[107-apply-...-practices \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/107-apply-best-practices.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS lectures → Wrote working scripts (variables, conditions, loops, remote exec, multi-OS)
THIS lecture       → REFACTOR: apply best practices to existing working scripts
                    ├── Defensive error handling (set -euo pipefail)
                    ├── Functions (reusable, composable, self-documenting)
                    └── AI-assisted refactoring workflow (Copilot)
NEXT              → Python scripting (functions explored in greater depth)
```

***

Your best-practices refactoring material is fully reconstructed. Want me to generate **AnkiDroid flashcards (.csv)** from this lecture or across all lectures we've covered? 🃏
