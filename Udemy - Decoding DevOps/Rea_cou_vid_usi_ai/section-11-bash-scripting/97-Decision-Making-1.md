# 🐚 Bash Scripting — Decision Making Part 1: The `if` and `if-else` Statement

**Source:** Bash Scripting Session — Decision Making Part 1 (Caption File) [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

This video introduces **decision making in bash scripts** — the ability for a script to evaluate a condition and choose different execution paths based on whether that condition is true or false. The instructor starts by framing the problem (scripts so far are just linear command sequences with no intelligence), introduces the `if` statement structure, demonstrates it with a number comparison script, then extends it with an `else` block. Two scripts are built: one with `if` only (`8if1.sh`), and one with `if-else` (`9_if2.sh`). [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. The Problem — Scripts That Cannot Think

Up to this point in the course, every script written has been a **linear series of commands** — command 1 runs, then command 2, then command 3, all the way to the end. The script has no ability to react to what's happening. If a command fails, the script doesn't know. If a variable holds an unexpected value, the script doesn't care. It blindly executes everything in sequence. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

The instructor frames this as a fundamental limitation: **"our script cannot make any decision."** But real automation needs intelligence. You want a script that can say: "if something fails, do something else" or "if the value of this variable is X, do this; otherwise, do that." This is what transforms a script from a dumb command list into a **smart automation tool**. Decision making is the mechanism that provides this intelligence. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

## 2. The `if` Statement — Structure and Mechanism

The `if` statement is bash's primary decision-making construct. Its core mechanism works on a simple principle: **evaluate a condition → if true, execute a block of commands → if false, skip that block**. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

The full conceptual structure the instructor presents (including extensions covered later) is:

```
if  CONDITION → then execute block
else if  CONDITION → then execute block    (can have multiple else-if's)
else if  CONDITION → then execute block
else → execute fallback block              (when everything above is false)
```

The instructor explicitly mentions you can have **multiple `else if` conditions** and a final `else` as a fallback when everything fails. In this lecture, only `if` and `if-else` are demonstrated; `else if` comes in a later part. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

The opening keyword is `if`. The closing keyword is `fi` (which is `if` spelled backwards). Everything between `then` and `fi` (or between `then` and `else`) is the **conditional block** — it only executes if the condition evaluates to true. This `if`/`fi` pairing is a syntactic requirement — every `if` must have a matching `fi` to close it, just as every opened block must be closed. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

## 3. Conditions — The Test Case Mechanism

The condition inside an `if` statement is what the instructor calls a **"test case"** — it **compares something with something**. The condition lives inside **square brackets `[ ]`** and follows a strict syntax pattern. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

The anatomy of a condition:

```
[ OPERAND1  OPERATOR  OPERAND2 ]
```

There are **two operands** (the values being compared) and one **operator** (the comparison type). In the video's example, the operands are the variable `$NUM` (user's input) and the literal value `100`, and the operator is `-gt` (greater than). [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

**Critical syntax rule: spaces are mandatory.** There must be a space after the opening `[`, a space before the closing `]`, and spaces between the operand and the operator. The instructor explicitly walks through this: "square bracket, a space, variable, space, operator, space, the other operand, space and the square bracket." Missing any of these spaces will cause a syntax error. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

The `-gt` operator means **"greater than"** and is used for numeric comparison. The instructor only demonstrates this one operator in this lecture, but the pattern (two operands separated by an operator inside spaced square brackets) is the universal syntax for all bash conditions.

<details>
<summary>🔍 Deep Dive</summary>

The square bracket `[` is actually a command in bash (an alias for the `test` command). That's why spaces are required — bash parses `[` as a command name, and the operands/operator as arguments to that command. Writing `[$NUM -gt 100]` without spaces is like writing `lscommand` instead of `ls command` — bash can't parse it. This also explains why `]` needs a space before it — it's the final argument to the `[` command, signaling the end of the test expression. Understanding `[` as a command (not just syntax decoration) makes the spacing rules logical rather than arbitrary.

</details>

***

## 4. True vs False Execution Paths

When the condition inside `[ ]` evaluates to **true**, bash executes everything between `then` and `fi` (or between `then` and `else`, if an else block exists). When the condition evaluates to **false**, bash **skips the entire `if` block** and jumps to either the `else` block (if one exists) or directly to the code after `fi`. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

In the `if`-only version (no `else`):

* **True →** execute the `if` block, then continue with code after `fi`.
* **False →** skip the `if` block entirely, continue with code after `fi`.

In the `if-else` version:

* **True →** execute the `if` block, skip the `else` block, continue after `fi`.
* **False →** skip the `if` block, execute the `else` block, continue after `fi`.

The code **after `fi`** always executes regardless of whether the condition was true or false. The instructor demonstrates this with an `echo "execution completed"` statement placed after `fi` — it prints in both cases. This is the **unconditional code** that runs no matter what the decision was. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

## 5. The `read` Command — Taking User Input

The instructor uses the `read` command to take input from the user at runtime. `read NUM` pauses script execution, waits for the user to type something and press Enter, and stores whatever they typed into the variable `NUM`. This value is then used in the condition (`$NUM -gt 100`). [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

This connects to the broader scripting progression: first scripts had hardcoded values, then command line arguments (`$1`, `$2`) allowed runtime input, and now `read` provides **interactive runtime input** — the script asks and the user answers during execution.

***

## 6. The `sleep` Command — Execution Pause

Inside the `if` block, the instructor uses `sleep 3`, which **pauses execution for 3 seconds** before continuing. This is used here as a demonstration tool to make the execution flow visible — you can see the script pause inside the `if` block, confirming it entered that path. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

## 7. Indentation — Optional but Valuable

The instructor deliberately indents the code inside the `if` block (the commands between `then` and `fi`) with spaces. He explicitly notes: **"you really don't need to give any space, but it really looks better if you give some space."** He also draws a contrast with Python, where **indentation is mandatory** (it defines the block structure). In bash, indentation is purely cosmetic — bash doesn't care — but it makes the script significantly more readable, especially as conditions become nested or complex. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are building two scripts that demonstrate bash decision making: [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

1. **`8if1.sh`** — Takes a number from the user, checks if it's greater than 100, and prints a message only if true.
2. **`9_if2.sh`** — Same logic, but adds an `else` block that prints a different message when the number is NOT greater than 100.

**Why it matters:** This is the transition from linear scripts to intelligent scripts — scripts that can evaluate conditions and branch their execution.

**Final outcome:** A script that responds differently based on user input, demonstrating both the `if`-only and `if-else` patterns.

***

## Step 1: Create the `if`-Only Script (`8if1.sh`)

**What we are doing:** Writing a script that takes a number from the user and checks if it's greater than 100.

**Create the file:**

```bash
vim 8if1.sh
```

**Script content:** [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

```bash
read NUM
if [ $NUM -gt 100 ]
then
    echo "We have entered the IF block"
    sleep 3
    echo "Your number is greater than 100"
    echo
    date
fi
echo "Execution completed"
```

**Line-by-line breakdown:**

* `read NUM` — Pauses execution, waits for user input, stores it in variable `NUM`.
* `if [ $NUM -gt 100 ]` — Opens the `if` statement. The condition checks: is the value in `$NUM` greater than (`-gt`) `100`?
  * `[` — Opens the test expression (must have space after).
  * `$NUM` — First operand (the user's number).
  * `-gt` — Operator: "greater than" (numeric comparison).
  * `100` — Second operand (the comparison value).
  * `]` — Closes the test expression (must have space before).
* `then` — Marks the start of the conditional block. Everything after this until `fi` executes only if the condition is true.
* `echo "We have entered the IF block"` — Confirmation message that the true path is executing.
* `sleep 3` — Pauses for 3 seconds (makes execution flow visible).
* `echo "Your number is greater than 100"` — The meaningful output message.
* `echo` — Prints an empty line (formatting).
* `date` — Prints the current date and time (demonstrates that any command can go inside an `if` block, not just `echo`).
* `fi` — Closes the `if` block.
* `echo "Execution completed"` — Runs unconditionally, regardless of whether the `if` block executed. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

**Make executable:**

```bash
chmod +x 8if1.sh
```

**Connection to flow:** The script is ready to test with both true and false conditions.

***

## Step 2: Test with a Value Greater Than 100 (True Path)

```bash
./8if1.sh
```

The script prompts for input. Enter: `120` [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

**Expected output:**

```
We have entered the IF block
(3-second pause)
Your number is greater than 100

Thu Jun 12 ...
Execution completed
```

* The condition `[ 120 -gt 100 ]` is **true** → the entire `if` block executes.
* `sleep 3` causes a visible pause.
* `date` prints the current timestamp.
* `"Execution completed"` prints after `fi` — it always runs.

**Verification:** The messages "We have entered the IF block" and "Your number is greater than 100" confirm the true path was taken. The 3-second pause confirms execution went through `sleep`. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

## Step 3: Test with a Value Less Than 100 (False Path)

```bash
./8if1.sh
```

Enter: `50` [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

**Expected output:**

```
Execution completed
```

* The condition `[ 50 -gt 100 ]` is **false** → the entire `if` block is **skipped**.
* None of the `echo`, `sleep`, or `date` commands inside the block execute.
* Only `"Execution completed"` (which is after `fi`) prints.

**Operational insight:** The script didn't crash, didn't give an error — it simply skipped the conditional block and continued. This is the designed behavior: false condition = silent skip.

**Common mistake:** Expecting bash to tell you the condition was false. It won't. If you need feedback on the false path, you must add an `else` block (next step). [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

## Step 4: Create the `if-else` Script (`9_if2.sh`)

**What we are doing:** Copying the first script and adding an `else` block so the script provides output on both true AND false paths. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

**Copy the base script:**

```bash
cp 8if1.sh 9_if2.sh
```

**Edit the script:**

```bash
vim 9_if2.sh
```

**Modification:** Add an `else` block just before `fi`:

```bash
read NUM
if [ $NUM -gt 100 ]
then
    echo "We have entered the IF block"
    sleep 3
    echo "Your number is greater than 100"
    echo
    date
else
    echo "Your number is less than 100"
fi
echo "Execution completed"
```

* `else` — Placed between the end of the `if` block's commands and `fi`. No condition needed — `else` catches **everything that didn't match the `if` condition**.
* `echo "Your number is less than 100"` — This only executes when the `if` condition is false.

**Connection to flow:** The script now has two distinct execution paths — one for true, one for false. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

***

## Step 5: Test the `if-else` Script — Both Paths

**Test with false condition (60):** [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

```bash
./9_if2.sh
```

Enter: `60`

**Expected output:**

```
Your number is less than 100
Execution completed
```

* `[ 60 -gt 100 ]` is **false** → `if` block skipped → `else` block executes.
* The user now gets meaningful feedback on the false path.

**Test with true condition (>100):**

```bash
./9_if2.sh
```

Enter a number greater than 100.

**Expected output:** Same as Step 2 — the `if` block executes, the `else` block is skipped, and "Execution completed" prints at the end. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

**Verification:** Running the script with values on both sides of 100 confirms both paths work correctly.

**Common mistake:** Placing `else` after `fi` instead of before it. The `else` must be inside the `if`/`fi` structure — it's part of the same decision block.

<details>
<summary>⚠️ Expert Note</summary>

The instructor's message "your number is less than 100" is technically imprecise — if the user enters exactly 100, `-gt` (greater than) returns false, so the `else` block runs and says "less than 100" even though the number equals 100. This is a common logical edge case in comparisons. In production scripts, you'd either use `-ge` (greater than or equal) if 100 should go to the `if` block, or handle the "equal to" case explicitly with `else if` (covered in Part 2).

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   Bash Decision Making — Part 1 (if / if-else)
CONTEXT: Bash scripting section → transition from linear execution → conditional branching
PURPOSE: Scripts that can evaluate conditions and choose execution paths
```

***

## The Problem → Solution

```
BEFORE:  Script = linear series of commands → no intelligence → runs everything blindly
AFTER:   Script = evaluates conditions → branches execution → "smart" automation
MECHANISM: if statement
```

***

## `if` Statement Structure

```
if [ CONDITION ]        ← test (spaces mandatory inside brackets)
then
    commands            ← executes ONLY if condition = TRUE
fi                      ← closes the if block (if backwards)

code after fi           ← ALWAYS executes (unconditional)
```

***

## `if-else` Structure

```
if [ CONDITION ]
then
    commands-A          ← TRUE path
else
    commands-B          ← FALSE path (catches everything else)
fi

code after fi           ← ALWAYS executes
```

***

## Full Decision Hierarchy (Previewed, not all demo'd yet)

```
if CONDITION → then block
else if CONDITION → then block      ← multiple allowed
else if CONDITION → then block
else → fallback block               ← when ALL above are false
fi
```

***

## Condition Syntax — The Spacing Contract

```
[ $VAR -gt 100 ]
↑ ↑     ↑    ↑  ↑
│ │     │    │  └─ space before ]
│ │     │    └──── operand 2
│ │     └───────── operator (-gt = greater than)
│ └─────────────── operand 1 (variable)
└───────────────── space after [

ALL SPACES MANDATORY — missing any = syntax error
```

***

## Execution Flow Map

```
                    ┌──────────┐
                    │ read NUM │
                    └────┬─────┘
                         ▼
              ┌─────────────────────┐
              │ [ $NUM -gt 100 ] ?  │
              └──────┬────────┬─────┘
                TRUE ▼        ▼ FALSE
          ┌──────────────┐  ┌──────────────┐
          │  if block     │  │  else block   │
          │  (echo,sleep, │  │  (echo msg)   │
          │   date, etc.) │  │               │
          └──────┬───────┘  └──────┬────────┘
                 ▼                  ▼
          ┌──────────────────────────────┐
          │  "Execution completed"       │
          │  (always runs — after fi)    │
          └──────────────────────────────┘
```

***

## Key Commands Used

```
read NUM          → pause, take user input, store in $NUM
sleep 3           → pause execution for 3 seconds
-gt               → "greater than" (numeric comparison operator)
fi                → closes if block (if spelled backwards)
chmod +x file.sh  → make script executable
cp old.sh new.sh  → copy script to iterate on it
```

***

## Indentation Rule

```
Bash:   indentation = OPTIONAL (cosmetic, improves readability)
Python: indentation = MANDATORY (defines block structure)
Instructor advice: always indent for clarity
```

***

## Operational Patterns

```
Script evolution in this course:
  Hardcoded values → Variables → Command line args ($1-$9) → read (interactive input) → if/else (decisions)
  
  Each step adds MORE INTELLIGENCE to the script
```

***

## Reusable Engineering Patterns Extracted

```
1. CONDITIONAL BRANCHING     → Evaluate condition → branch execution path
                               (universal in all programming: if/else = the basic decision unit)

2. COPY-THEN-EXTEND          → cp 8if1.sh 9_if2.sh → add else block
                               Don't rewrite — evolve working code incrementally

3. UNCONDITIONAL TAIL         → Code after fi ALWAYS runs → use for cleanup, final messages,
                               guaranteed operations regardless of branch taken

4. SILENT FALSE               → Bash doesn't notify you when a condition is false
                               If you need false-path behavior → you must explicitly build it (else)

5. MANDATORY SYNTAX SPACING   → [ ] requires internal spaces — not aesthetic, structural
                               ([ is a command; args need whitespace separation)
```

***

## Rapid Recall Triggers

```
"How to make a script decide?"      → if [ condition ]; then ... fi
"What is fi?"                       → Closes if block (if backwards)
"Spaces in [ ] — required?"         → YES, all mandatory ([ is a command, args need spaces)
"-gt means?"                        → Greater than (numeric comparison)
"What if condition is false, no else?" → if block silently skipped → code after fi runs
"What runs after fi?"               → ALWAYS runs, regardless of true/false
"read does what?"                   → Pauses, takes user input, stores in variable
"sleep 3?"                          → Pause execution for 3 seconds
"Indentation in bash?"              → Optional (cosmetic) — mandatory in Python
"Script evolution so far?"          → Hardcoded → vars → $1-$9 → read → if/else
```

***

This completes the full reconstruction of Decision Making Part 1. The **Theory** builds the conceptual model of conditional branching and the syntax rules, the **Practical** walks through every command and both test scenarios exactly as the instructor demonstrated, and the **Mental Compression Map** compresses the flow, syntax, and patterns for rapid future recall. [\[97-decisio...king-part1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/97-decision-making-part1.txt)

Ready for Part 2 of Decision Making, or shall I generate an **AnkiDroid CSV** covering this lecture? 🚀
