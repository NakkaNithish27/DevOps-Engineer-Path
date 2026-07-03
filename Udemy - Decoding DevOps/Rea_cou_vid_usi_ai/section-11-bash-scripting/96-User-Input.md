# 🎓 Deep Learning Material: Bash User Input with the `read` Command

*Reconstructed from video lecture captions (96-user-input.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What User Input Is and What Problem It Solves

Up to this point in the course, scripts have been **non-interactive** — every value is either hardcoded or stored in a variable declared inside the script itself. The script runs from start to finish without ever pausing to ask the operator anything. This lecture introduces the opposite model: **interactive scripting**, where the script pauses execution, waits for the user to type something, captures that input, stores it in a variable, and then continues execution using that value. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

The command that makes this possible is `read`. When Bash encounters a `read` statement during script execution, it **halts and waits**. Execution does not proceed until the user types something and presses Enter. Whatever the user types gets stored into the variable name specified after `read`. From that point forward, the variable can be used exactly like any other variable — with `$VARIABLE_NAME` to retrieve the stored value. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

The core mechanism is simple: `read VARIABLE_NAME` creates a **pause point** in the script, captures keyboard input from the user, and assigns it to the named variable in the Bash process memory. This is the same variable storage concept covered in the variables lecture (see previous material) — the only difference is **who supplies the value**: in variable declaration, the script author supplies it at write time; with `read`, the user supplies it at run time. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

***

## 1.2 The `read` Command: Core Mechanics

The simplest form of `read` is:

```bash
read SKILL
```

When Bash hits this line, it does three things in sequence: [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

1. **Pauses execution** — the script stops and a blinking cursor appears
2. **Waits for user input** — the user types a value and presses Enter
3. **Stores the input** — whatever the user typed is assigned to the variable `SKILL`

After this, `$SKILL` contains the user's input and can be used in any subsequent command, exactly like a pre-declared variable.

The important detail is that `read` by itself provides **no visual prompt** — the cursor just blinks on an empty line. The user has no idea what they're supposed to type unless the script explicitly prints a message before the `read` statement. This is why the instructor first uses `echo` to print a message like "Enter your skills" before the `read` line. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

***

## 1.3 The `-p` Option: Inline Prompting

The pattern of "print a message, then read" is so common that `read` has a built-in option to combine both into one line: the **`-p` (prompt) option**. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

```bash
read -p "Enter your username: " USERNAME
```

With `-p`, `read` prints the prompt string ("Enter your username: ") and then waits for input on the **same line**. The user sees the prompt text, types their value immediately after it, and presses Enter. The typed value is stored in `USERNAME`. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

This is functionally equivalent to writing two separate lines (`echo "Enter your username: "` followed by `read USERNAME`), but `-p` is cleaner — it keeps the prompt and the input on the same line, producing a more professional-looking interaction.

***

## 1.4 The `-s` Option: Suppressed (Silent) Input

The `-s` option makes `read` **suppress the display of what the user types**. When the user types characters, nothing appears on screen — no letters, no asterisks, nothing. The input is still captured and stored in the variable, but it is invisible during entry. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

```bash
read -s -p "Enter your password: " PASS
```

The instructor explicitly explains the use case: **passwords and secrets**. When a user enters a password, you don't want it visible on screen because someone might be looking over their shoulder, or the terminal output might be logged. The `-s` flag solves this by making the input invisible. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

The instructor demonstrates this live: *"I'm typing, typing, typing, but it's really not printing anything. That's because we used -s option to suppress the input."* [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

A critical complementary warning follows: **never print the password variable in your script's output**. The instructor says: *"Don't you dare print pass variable, because if you print that, then what's the point of using -s?"*  The `-s` flag protects the input during entry. But if you then `echo $PASS` in the script output, you've defeated the entire purpose — the secret is now displayed in plain text in the terminal. The protection must extend from input through to usage: capture silently, use internally, never echo. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

🔍 **Deep Dive:**
The `-p` and `-s` flags can be combined in a single `read` call: `read -s -p "Enter password: " PASS`. The order of flags doesn't matter. When combined, `-p` provides the visible prompt text, and `-s` suppresses only the user's typed response. This gives the user clear instruction about what to type while keeping their actual input hidden. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

***

## 1.5 Why Interactive Scripts Are NOT Recommended in DevOps

This is the most important conceptual takeaway of the entire lecture, and the instructor is very deliberate about it. After teaching how `read` works, he immediately adds a strong caveat: *"It's really not recommended in DevOps, at least, to make the script interactive because we run scripts from background, from some other tools. And we really don't want the user to interact with the system. Because user interaction is always error prone."* [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

This warning contains three layers of reasoning:

**Layer 1: Background execution.** In DevOps, scripts are frequently executed by automation tools (Jenkins, Ansible, cron jobs, CI/CD pipelines) — not by a human sitting at a terminal. When a script runs in the background or inside an automation pipeline, there is **no user present** to type input. If the script hits a `read` statement, it will hang indefinitely, waiting for input that will never come. This blocks the pipeline, wastes resources, and can cause cascading failures in automated workflows. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

**Layer 2: Tool-driven execution.** DevOps scripts are often called by other tools — Ansible runs shell scripts on remote hosts, Jenkins executes build scripts, Terraform runs provisioning scripts. These tools send commands programmatically. They cannot respond to interactive prompts. A `read` statement inside a script called by such tools creates an **incompatibility between the script's expectations and its execution environment**. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

**Layer 3: Human error.** Even when a human is present, interactive input is **error-prone**. Users can mistype values, enter values in the wrong format, skip prompts, or provide inconsistent input across runs. Every `read` statement is a potential point of failure introduced by human unpredictability. The DevOps philosophy prefers **deterministic, repeatable execution** — scripts should produce the same result every time with the same inputs, and those inputs should come from variables, configuration files, or command-line arguments, not from real-time human typing. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

The instructor's conclusion is balanced: *"In any case, if you need input from the user, you can use read."*   He doesn't say never use it — he says understand when it's appropriate (one-off interactive scripts, local utilities, learning exercises) and when it's inappropriate (automation, pipelines, production operations). [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

⚠️ **Expert Note:**
This anti-pattern warning is a fundamental DevOps principle. In production, the alternatives to `read` for providing runtime values are: command-line arguments (`$1`, `$2`), environment variables (`$ENV_VAR`), configuration files, and secrets managers (Vault, AWS Secrets Manager). Each of these allows the script to receive input **without pausing for human interaction**, making the script compatible with automation and repeatable across environments. The `read` command is a learning tool and a local convenience — it should almost never appear in production automation scripts.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building two small interactive Bash scripts to learn how the `read` command works. The first script takes a simple text input (a skill name) and prints it. The second script takes a username (visible input) and a password (hidden input) to demonstrate `-p` and `-s` options. The final understanding is knowing how to use `read` **and** knowing why to avoid it in DevOps automation. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

***

## Step 1: Write the Simple Input Script

Create a script that asks for a skill and prints it.

The script content: [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

```bash
#!/bin/bash
echo "Enter your skill:"
read SKILL
echo "Your skill is $SKILL"
```

**Line-by-line breakdown:**

* `echo "Enter your skill:"` — Prints a message telling the user what to type. Without this, the script would just show a blank cursor and the user wouldn't know what's expected.
* `read SKILL` — Halts execution, waits for the user to type something and press Enter, stores the input in the variable `SKILL`.
* `echo "Your skill is $SKILL"` — Prints the captured value using standard variable interpolation (`$SKILL` → stored value).

**Connection to flow:** This demonstrates the basic `read` mechanism — print a prompt with `echo`, capture input with `read`, use the value with `$`.

***

## Step 2: Write the Prompt and Secret Input Script

Create a second script that demonstrates `-p` (inline prompt) and `-s` (suppressed input): [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

```bash
#!/bin/bash
read -p "Enter your username: " USERNAME
read -s -p "Enter your password: " PASS
echo
echo "Your username is $USERNAME"
```

**Line-by-line breakdown:**

* `read -p "Enter your username: " USERNAME` — The `-p` flag combines the prompt message and the `read` into a single line. It prints "Enter your username: " and waits for input on the same line. The typed value is stored in `USERNAME`.
* `read -s -p "Enter your password: " PASS` — Two flags combined: `-s` suppresses the display of typed characters (nothing appears on screen as the user types), and `-p` provides the prompt text. The typed value is stored in `PASS` despite being invisible.
* `echo` — Prints an empty line. This is necessary because `-s` suppresses the newline that normally appears when the user presses Enter, so without this `echo`, the next output would appear on the same line as the password prompt.
* `echo "Your username is $USERNAME"` — Prints the username. **Notice: the password variable `$PASS` is intentionally NOT printed.** The instructor explicitly warns against printing secret values — doing so defeats the purpose of `-s`. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

**Common mistake:** Printing `$PASS` in the output. If you suppress input with `-s` to protect a secret but then `echo` it, the secret is exposed in the terminal output. The protection must be end-to-end.

***

## Step 3: Make the Script Executable

```bash
chmod +x <script_name>.sh
```

 [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

**Breakdown:**

* `chmod` — Change file permissions
* `+x` — Add execute permission
* `<script_name>.sh` — The script file

**Why:** Bash scripts are text files by default. Without execute permission, the OS will not allow you to run them directly with `./<script_name>.sh`. Adding `+x` tells the OS this file can be executed as a program.

***

## Step 4: Execute and Test the Simple Input Script

```bash
./<script_name>.sh
```

 [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

**What happens:**

1. The script prints "Enter your skill:"
2. The cursor waits — execution is paused at the `read` line
3. You type a value (the instructor types "cloud computing") and press Enter
4. The script prints "Your skill is cloud computing"

**Verification:** The printed output should contain exactly what you typed. If it prints an empty string, the variable name in the `read` statement doesn't match the variable name in the `echo` statement (a typo). [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

***

## Step 5: Execute and Test the Prompt/Secret Script

Run the second script: [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

**What happens:**

1. "Enter your username: " appears — you type a username, it appears on screen as you type, you press Enter
2. "Enter your password: " appears — you type, but **nothing appears on screen**. The instructor confirms: *"I'm typing, typing, typing, but it's really not printing anything."* You press Enter.
3. The script prints the username but NOT the password

**Verification:** The username should display correctly. The password prompt should show no visible characters during typing. If characters are visible during password entry, the `-s` flag was not included or was misspelled. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

**Failure scenario:** If you accidentally include `echo $PASS` in the script, the password will be printed in plain text — the `-s` protection is only during input capture, not during output.

***

## Step 6: Understand When NOT to Use This

After successful testing, internalize the operational constraint from Theory Section 1.5: `read` makes scripts interactive, which is incompatible with background execution, automation tools, and CI/CD pipelines. In real DevOps work, prefer command-line arguments, environment variables, or configuration files over `read`. Use `read` only for local, one-off, human-operated scripts. [\[96-user-input \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/96-user-input.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Concept Identity

```
read = Pause script execution → Wait for keyboard input → Store in variable
Same variable mechanics as declaration (SKILL=value) but value comes from USER at runtime
```

***

## `read` Command Options

```
read VARIABLE          → bare read, no prompt, cursor blinks on empty line
read -p "text" VAR     → inline prompt ("text" printed, input on same line)
read -s VAR            → suppressed input (nothing visible while typing)
read -s -p "text" VAR  → combined: prompt shown, input hidden

-p = prompt (UX convenience)
-s = silent/suppress (security)
```

***

## Execution Flow

```
Script hits `read SKILL`
  → Execution HALTS
  → Cursor waits
  → User types + Enter
  → Input → stored in $SKILL
  → Execution resumes
  → $SKILL usable like any variable
```

***

## Security Rule

```
-s suppresses INPUT DISPLAY only
  ├── Protects during typing (nothing visible on screen)
  └── Does NOT protect during output

RULE: Never echo/print a variable captured with -s
  read -s -p "Password: " PASS   ← input hidden ✓
  echo $PASS                      ← secret exposed ✗ (NEVER DO THIS)

Protection must be end-to-end: capture silently → use internally → never display
```

***

## Two Patterns: Prompt Before vs. Inline Prompt

```
PATTERN A (two lines):          PATTERN B (one line):
  echo "Enter skill:"             read -p "Enter skill: " SKILL
  read SKILL

Both functionally equivalent
-p is cleaner (prompt + input on same line)
```

***

## ⚠️ The Anti-Pattern: Why NOT to Use `read` in DevOps

```
DevOps scripts run from:
  ├── Background processes (cron, systemd)
  ├── Automation tools (Jenkins, Ansible)
  └── CI/CD pipelines

`read` → HALTS execution → waits for human input
  └── No human present → script HANGS FOREVER → pipeline blocked

Additional: Human input = error-prone, non-repeatable, non-deterministic

ALTERNATIVES (for production):
  ├── Command-line arguments ($1, $2)
  ├── Environment variables ($ENV_VAR)
  ├── Configuration files
  └── Secrets managers (Vault, etc.)

read = learning tool / local convenience
read ≠ production automation
```

***

## Operational Flow

```
Write script with echo + read (or read -p)
  → chmod +x script.sh
  → ./script.sh
  → Script pauses at read → type input → Enter
  → Script continues with stored value
  → Verify: output matches input
```

***

## Reusable Engineering Pattern

| Pattern                      | Manifestation                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Input-source separation**  | Value comes from user (read) vs. author (declaration) vs. system (env var) — same variable, different source |
| **Security layering**        | `-s` protects input; discipline protects output; both needed                                                 |
| **Automation compatibility** | Interactive ≠ automatable; production scripts must run without human presence                                |
| **UX in CLI tools**          | `-p` for clear prompts; `-s` for secrets; `echo` for line breaks after silent input                          |

***

## Core Mental Model

```
read = runtime variable assignment (by the user, not the author)

Three input sources for variables (progression):
  1. Hardcoded:   SKILL=DevOps          (author decides at write time)
  2. Interactive:  read SKILL            (user decides at run time)
  3. Automated:    SKILL=$1 / SKILL=$ENV (system provides at run time)

DevOps trajectory: 1 → 2 (for learning) → 3 (for production)
```

***

This material captures every concept, command, option, warning, and anti-pattern from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
