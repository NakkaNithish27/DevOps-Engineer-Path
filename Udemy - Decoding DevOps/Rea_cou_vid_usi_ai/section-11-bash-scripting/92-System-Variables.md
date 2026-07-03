# 🎓 Bash System Variables — Deep Learning Material

**Source:** Video caption file — *System Variables in Bash Scripting* [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What System Variables Are and Why They Exist

In Bash scripting, **system variables** (also called special variables or built-in variables) are pre-defined variables that the shell automatically populates with useful information. You don't create them — the shell creates and maintains them for you. They exist because scripts need to interact with their own execution context: they need to know what arguments were passed to them, whether the last command succeeded or failed, who is running the script, what machine it's running on, and so on. Without system variables, scripts would be blind to their own environment and execution state. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

These variables are accessed using the `$` prefix followed by a specific symbol or number. Each one has a precise, fixed meaning defined by the shell.

***

## 1.2 — Script Identity and Argument Variables

### `$0` — The Script's Own Name

`$0` holds the **name of the script** that is currently executing. When you run `./myscript.sh`, inside that script `$0` evaluates to `./myscript.sh`. This is the script's **self-identity** — it knows what it's called. This is useful for error messages, usage instructions, and logging where you want the script to refer to itself by name. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### `$1` through `$9` — Command-Line Arguments (Positional Parameters)

When you run a script with arguments (e.g., `./myscript.sh arg1 arg2 arg3`), each argument is captured in a numbered variable: `$1` gets the first argument, `$2` gets the second, and so on up to `$9`. These are called **positional parameters** because their value depends on the position of the argument on the command line. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

This is how scripts accept input from the user at runtime. Instead of hardcoding values, you write scripts that operate on whatever arguments are passed to them — making scripts reusable and flexible.

### `$#` — The Argument Count

`$#` tells you **how many arguments** were passed to the script. If you run `./myscript.sh a b c`, then `$#` equals `3`. This is essential for **input validation** — before a script processes arguments, it should check whether the correct number of arguments was provided. Without this check, scripts can fail in confusing ways when required arguments are missing. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### `$@` — All Arguments as a List

`$@` expands to **all the arguments** passed to the script, preserving each argument as a separate entity. This is useful when you need to iterate over all arguments (e.g., in a loop) or pass all arguments to another command. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

> 🔍 **Deep Dive:** The distinction between `$@` and a similar variable `$*` (not covered in this video) is subtle but important in advanced scripting. `$@` preserves the boundaries between arguments when quoted (`"$@"` gives you `"arg1" "arg2" "arg3"` as separate words), while `$*` merges them into a single string. For most practical use, `$@` is the safer choice. This is an *implicit concept* — the video mentions only `$@` but doesn't contrast it with `$*`.

***

## 1.3 — The Exit Status Variable: `$?` (The Most Important System Variable)

The video places special emphasis on `$?`, calling it **"interesting"** and noting **"we are going to use this a lot later."** This emphasis is well-deserved — `$?` is the foundation of all error handling and conditional logic in Bash scripting. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### What It Is

`$?` holds the **exit status (exit code) of the last command that was executed**. Every command in Linux, when it finishes running, returns a numeric exit code back to the shell. This code is a single number that tells you whether the command **succeeded** or **failed**. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### The Universal Rule

* **Exit code `0`** = the last command **succeeded**.
* **Any non-zero exit code** = the last command **failed**.

This is a binary success/failure signal, but the non-zero values can carry additional meaning — different non-zero codes can indicate different types of failure. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### How It Works — Demonstrated Through Examples

**Success case:** You run `free -m` (a valid command that displays memory usage). It executes successfully. Immediately after, you check `echo $?` and get `0`. The command worked, so the exit code is zero. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

**Failure case 1 — Command not found:** You intentionally type a wrong command (too many 'e's in `free`, making it an unrecognized command). The shell responds with "command not found." Checking `echo $?` gives `127`. This is non-zero, confirming failure. The specific code `127` is the shell's standard code for "command not found." [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

**Failure case 2 — Command exists but fails:** You run a valid command with wrong arguments, causing it to fail for a different reason. Checking `echo $?` gives `1`. This is a general failure code — the command was found and attempted, but it couldn't complete its task. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### The Critical Behavioral Detail

`$?` is **volatile** — it gets overwritten after **every single command**. When you run command A, `$?` holds A's exit code. The moment you run command B, `$?` is replaced with B's exit code. A's exit code is gone forever. This means if you need to use the exit code of a specific command, you must capture it immediately — either by checking it right away or by storing it in a variable (e.g., `result=$?`) before running anything else.

> 🔍 **Deep Dive:** The exit code mechanism is how **all automation and conditional logic** in Bash works. `if` statements, `&&` (run next command only if previous succeeded), `||` (run next command only if previous failed) — all of these operate on exit codes under the hood. When you write `if command; then ... fi`, Bash is really checking whether `command`'s exit code was `0`. Understanding `$?` is understanding the engine behind all Bash decision-making. The video's emphasis that "we are going to use this a lot later" points directly to this — `$?` will be the basis for error handling, conditional execution, and script flow control in future lectures. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

> ⚠️ **Expert Note:** Common exit codes have conventional meanings across Linux: `0` = success, `1` = general error, `2` = misuse of shell command, `126` = command found but not executable, `127` = command not found, `128+N` = killed by signal N. However, individual programs can define their own non-zero codes. The video demonstrates `0`, `1`, and `127` — the three most frequently encountered codes in practice.

***

## 1.4 — Environment Information Variables

Beyond script arguments and exit codes, Bash provides variables that give you information about the **execution environment** itself.

### `$USER` — The Current Username

`$USER` contains the **username of the user running the script**. If you're logged in as `root`, `$USER` is `root`. If you're logged in as `vagrant`, `$USER` is `vagrant`. This is useful for permission checks, logging, conditional behavior based on who's running the script, and audit trails. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### `$HOSTNAME` — The Machine's Hostname

`$HOSTNAME` contains the **hostname of the machine** where the script is executing. This ties directly back to the hostname configuration done during VM setup (as covered in the previous lecture on VM setup). When scripts run across multiple machines, `$HOSTNAME` lets the script know **which machine it's currently running on** — essential for multi-server automation where the same script might need to behave differently depending on the host. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### `$RANDOM` — A Random Number

`$RANDOM` generates a **random number** each time it's accessed. This is useful for generating temporary file names, introducing randomness in test data, creating unique identifiers, or adding jitter to scheduled tasks. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Learning to Do

We're learning to **use and interrogate Bash system variables** at the command line. This is hands-on exploration of how the shell communicates execution context to you. The outcome: you'll be able to check argument counts, read arguments, detect command success/failure via exit codes, and query environment information — all skills that will be used heavily in future scripting. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

***

## Step 1: Understanding `$?` Through Live Command Execution

This is the primary hands-on exercise in the video — testing `$?` with successful and failing commands.

### Step 1a: Run a Successful Command and Check Exit Code

**The Commands:**

```bash
free -m
echo $?
```

**Breakdown:**

* `free -m` — Displays system memory usage in megabytes. This is a valid command that will succeed on any Linux system.
* `echo $?` — Prints the exit code of the **immediately preceding command** (`free -m` in this case). [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

**Expected Output of `echo $?`:**

```
0
```

**What This Confirms:** The `free -m` command executed successfully. Exit code `0` = success.

**Critical Operational Rule:** You must run `echo $?` **immediately** after the command you want to check. If you run any other command in between — even a simple `echo "hello"` — `$?` will reflect that intermediate command's exit code, not the one you intended to check.

***

### Step 1b: Run an Invalid Command (Command Not Found) and Check Exit Code

**The Commands:**

```bash
freeeee -m
echo $?
```

**Breakdown:**

* `freeeee -m` — An intentionally misspelled command. This does not exist on the system. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)
* `echo $?` — Checks the exit code of the failed command attempt.

**Expected Output:**

```
bash: freeeee: command not found
```

Then `echo $?` outputs:

```
127
```

**What This Confirms:** Exit code `127` specifically means "command not found" — the shell couldn't locate any executable matching `freeeee`. This is non-zero, confirming failure. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

***

### Step 1c: Run a Valid Command with Bad Arguments and Check Exit Code

**The Commands:**

```bash
free blahblahblah
echo $?
```

**Breakdown:**

* `free blahblahblah` — The command `free` exists, but `blahblahblah` is not a valid argument. The command is found but fails during execution. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)
* `echo $?` — Checks the exit code.

**Expected Output of `echo $?`:**

```
1
```

**What This Confirms:** Exit code `1` is a general failure — the command was found and attempted, but it couldn't complete its operation due to invalid input. This is different from `127` (command not found). The command **existed** but **failed**. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### Key Takeaway from All Three Cases

```
$? = 0    →  SUCCESS (command ran and completed its job)
$? = 127  →  COMMAND NOT FOUND (shell couldn't find the executable)
$? = 1    →  GENERAL FAILURE (command found, but execution failed)
$? ≠ 0    →  ALWAYS means failure (the specific number indicates the type)
```

### Common Mistakes

* **Checking `$?` too late:** Running another command between the target command and `echo $?` overwrites the exit code. Always check immediately.
* **Assuming all non-zero codes are `1`:** Different failure types produce different codes (1, 2, 126, 127, etc.). Don't treat all failures as identical.

***

## Step 2: Querying Environment Variables

### Checking the Current User

```bash
echo $USER
```

**What It Does:** Prints the username of the currently logged-in user (e.g., `root` if you ran `sudo -i`, or `vagrant` if you're the default Vagrant user). [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### Checking the Hostname

```bash
echo $HOSTNAME
```

**What It Does:** Prints the hostname of the machine (e.g., `scriptbox` if you configured it in the previous VM setup session). [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### Generating a Random Number

```bash
echo $RANDOM
```

**What It Does:** Prints a random integer. Each invocation produces a different number. [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

### Connection to Larger Flow

These variables will be used inside scripts for conditional logic (e.g., "if running as root, do X"), logging (e.g., "script ran on $HOSTNAME at this time"), and utility purposes (e.g., `$RANDOM` for temp file names). The video encourages you to **try these yourself** before moving on.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 📐 Complete System Variable Reference

```
VARIABLE    MEANING                          CATEGORY
────────────────────────────────────────────────────────
$0          Name of the script               Script Identity
$1–$9       Positional arguments (1st–9th)   Script Input
$#          Number of arguments passed       Input Validation
$@          All arguments (as separate list)  Input Iteration
$?          Exit code of last command         Execution State
$USER       Current username                 Environment
$HOSTNAME   Machine hostname                 Environment
$RANDOM     Random number                    Utility
```

 [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

***

## 🔑 The Exit Code System (`$?`)

```
COMMAND EXECUTES
       │
       ▼
  ┌─────────┐
  │ Exit Code│ ← automatically set by every command
  └────┬────┘
       │
       ├── = 0    → SUCCESS ✅
       │
       └── ≠ 0    → FAILURE ❌
             ├── 1    = General error (command found, execution failed)
             ├── 127  = Command not found
             └── other = Specific failure type
       
  ⚠️ VOLATILE: Overwritten by EVERY subsequent command
     → Capture immediately: result=$?
```

 [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

***

## 🔄 Exit Code Demo Flow (from video)

```
free -m          → runs OK     → $? = 0    (success)
freeeee -m       → not found   → $? = 127  (command not found)
free blahblah    → bad args    → $? = 1    (general failure)

RULE: 0 = success | non-zero = failure | check IMMEDIATELY
```

***

## 🗂️ Variable Grouping by Purpose

```
SCRIPT CONTEXT          EXECUTION STATE         ENVIRONMENT INFO
──────────────          ───────────────         ────────────────
$0  → script name       $? → last exit code     $USER     → who
$1–$9 → args                                    $HOSTNAME → where
$#  → arg count                                 $RANDOM   → utility
$@  → all args
```

***

## 🔗 Dependency Chain: How Variables Connect to Scripting

```
$1–$9 + $# + $@  →  INPUT HANDLING (accept & validate arguments)
         │
         ▼
   Script runs commands
         │
         ▼
       $?  →  ERROR HANDLING (check success/failure after each command)
         │
         ▼
  $USER + $HOSTNAME  →  CONTEXT AWARENESS (who/where for logging & conditionals)
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: EXIT CODE AS UNIVERSAL STATUS SIGNAL
  Every command returns a numeric status → 0 = success, non-zero = failure
  → Same pattern as: HTTP status codes (200 = OK, 4xx/5xx = error)
                      Process return codes in any language
                      API response status fields
                      Health check pass/fail

PATTERN 2: VOLATILE STATE — CAPTURE OR LOSE
  $? is overwritten by every command → must capture immediately
  → Same pattern as: Last-error registers in hardware
                      errno in C (overwritten by next syscall)
                      Any "last status" variable in event-driven systems

PATTERN 3: POSITIONAL INTERFACE CONTRACT
  $1–$9 define a script's input interface by position
  → Same pattern as: Function arguments in any language
                      CLI tool argument parsing
                      API endpoint path parameters
```

***

## 🧭 Course Flow Context

```
PREVIOUS lectures → $0, $1–$9, $#, $@ introduced (referenced as "already seen")
THIS lecture       → Deep focus on $? (exit codes) + environment variables ($USER, $HOSTNAME, $RANDOM)
UPCOMING scripts   → $? used heavily for error handling and conditional execution
```

 [\[92-system-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/92-system-variables.txt)

***

You now have the full system variable toolkit mapped. Want me to generate **AnkiDroid flashcards (.csv)** from this material, or proceed to another caption file? 🃏
