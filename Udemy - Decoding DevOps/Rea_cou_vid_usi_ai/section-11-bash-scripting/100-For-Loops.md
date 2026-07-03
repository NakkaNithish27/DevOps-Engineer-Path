# 🔁 Shell Scripting — Loops (For Loop) — Deep Learning Material

**Source:** Video caption file — [100-loops.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt?EntityRepresentationId=492a8080-1c48-4117-88d8-6d9706acf430) [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

**Video Context:** The instructor teaches loops in bash scripting — specifically the `for` loop — progressing from the concept of repeated execution, through the syntax and internal mechanics, to two practical scripts: one that loops through a hardcoded list of items, and another that creates multiple Linux users from a list stored in a variable.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Core Problem — Repetitive Execution

The instructor opens directly: "Loops — running something again and again and again." This frames the entire topic. In scripting, you frequently encounter situations where you need to run the **same command (or set of commands) multiple times**, with only a **small part changing** each time. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

The instructor gives two concrete examples to anchor this:

**Example 1:** You want to add 10 users. The command is `useradd`. The command itself is identical every time — the only thing that changes is the **username**. You could type `useradd` 10 separate times, manually changing the username each time. Or you could write a loop that runs `useradd` 10 times, automatically substituting a different username on each iteration.

**Example 2:** You have a list of servers where you need to log in and execute commands. Instead of manually SSH-ing into each server and running the task, a loop can iterate through the server list and execute the task on each one automatically.

The instructor emphasizes: "This really saves a lot of time." The value of loops isn't just convenience — it's the difference between manually executing N operations (slow, error-prone, tedious) and writing one loop that handles all N automatically (fast, consistent, scalable). As N grows, the value of the loop grows proportionally. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

***

## 1.2 Two Types of Loops in Bash

The instructor states there are "two kinds of loops in bash scripting: for loop and while loop. There are few other, but we are going to deal with that." This video focuses exclusively on the **for loop**. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

The key characteristic of a for loop: it "runs for a definitive number of times." It operates on a **sequence** — a list of items. The loop runs once for each item in the list, and when the list is exhausted, the loop stops. The number of iterations is determined by the number of items in the sequence. This contrasts conceptually with a while loop (not covered in this video), which runs as long as a condition remains true — potentially indefinitely.

***

## 1.3 For Loop Syntax and Internal Mechanics

The syntax of a bash for loop is: [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

```bash
for VARIABLE in item1 item2 item3 ...
do
    commands using $VARIABLE
done
```

The instructor explains the mechanics step by step:

**Step 1:** The first value in the sequence (`item1`) is stored into the variable (`VARIABLE`).

**Step 2:** The commands between `do` and `done` are executed. Inside these commands, `$VARIABLE` holds the current value.

**Step 3:** "It's a loop — it's going to come back." Execution returns to the top, the **next** value in the sequence is stored into the variable, and the commands execute again.

**Step 4:** This repeats — "then next, then next" — until the sequence is **exhausted** (all items have been processed). [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

The `done` keyword marks the end of the loop body. The instructor draws a parallel to the `if` statement: "Like in 'if' you have 'if' and 'fi' is for closing. Here, 'for' begins and 'done' is the closing." This establishes a consistent pattern in bash: control structures have explicit opening and closing keywords.

The number of iterations equals the number of items in the sequence. The instructor counts explicitly: "One, two, three, four, five — five times" for a five-item list. If the list has three items, the loop runs three times. This is deterministic and predictable. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

***

## 1.4 The Sequence — Inline Lists vs. Variable-Based Lists

The instructor demonstrates two ways to provide the sequence to a for loop:

**Inline list:** The items are written directly in the `for` statement:

```bash
for VAR1 in java .net python ruby php
```

The list is `java .net python ruby php` — five space-separated items written directly in the code. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

**Variable-based list:** The items are stored in a variable first, and the variable is referenced in the `for` statement:

```bash
MYUSERS="Alpha Beta Gamma"
for usr in $MYUSERS
```

The list is stored in `MYUSERS`, and `$MYUSERS` expands to `Alpha Beta Gamma` when the loop begins. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

The variable-based approach is more flexible and more common in real scripts because the list can be populated dynamically — from a file, from command substitution (covered in the previous lecture), from user input, or from any data source. The loop structure remains the same regardless of where the list comes from.

🔍 **Deep Dive:** When bash encounters `$MYUSERS` in the `for` statement, it performs **word splitting** — it takes the variable's value and splits it into separate items by whitespace (spaces, tabs, newlines). Each resulting word becomes one iteration of the loop. This is why `MYUSERS="Alpha Beta Gamma"` produces three iterations: three space-separated words = three loop items. This word-splitting behavior is fundamental to how bash for loops consume lists.

***

## 1.5 The Loop Body — Commands Between `do` and `done`

Everything between `do` and `done` constitutes the **loop body** — the set of commands that execute on every iteration. The instructor states: "In the middle, whatever commands we give, it's going to run again and again until the sequence is exhausted." [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

The loop body can contain **any number of commands** — it's not limited to one. In the first example, the body contains an `echo` statement and a `sleep`. In the second example, it contains `echo`, `useradd`, `id`, and another `echo`. Every command in the body runs for every item in the sequence.

This means if you have 3 items and 4 commands in the body, the total command executions are 3 × 4 = 12. The loop doesn't just repeat one command — it repeats the **entire block**.

***

## 1.6 The `sleep` Command — Controlling Execution Speed

The instructor adds `sleep 1` inside the first loop and explains: "Because it is going to run really super fast, I'm just going to sleep one. So it runs little slow." [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

`sleep 1` pauses execution for 1 second. Without it, the loop would execute all iterations almost instantaneously, and the output would flash by too quickly to observe. This is a practical tool for **visibility during development and debugging** — slowing down execution so you can watch what the loop is doing iteration by iteration.

***

## 1.7 Print Statements and Separators in Loops — Operational Readability

In both scripts, the instructor adds `echo` statements that print messages like "adding user $usr" and separator lines (hashes `######`). The purpose is the same as in the sample script lecture (see previous video on sample scripts): making loop output readable for the operator watching the terminal. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

Without separators, the output of multiple iterations blends together into an unreadable stream. The echo with hashes visually separates each iteration's output, making it clear where one iteration ends and the next begins. The instructor explicitly adds this: "I can put one more echo here so you can see it all separated."

***

## 1.8 Real Use Case — Creating Users from a List

The second script (`14_for.sh`) demonstrates a real operational use case: creating multiple Linux users. The instructor stores usernames in a variable (`MYUSERS="Alpha Beta Gamma"`), loops through them, and for each username runs `useradd $usr` (to create the user) and `id $usr` (to verify the user was created by showing their UID/GID). [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

This directly fulfills the problem stated at the beginning of the lecture: "You want to add 10 users, and the command is useradd. The only thing that changes is the username." The for loop eliminates the repetition — you write the `useradd` command once, and the loop runs it for every username in the list.

The `id` command after `useradd` serves as **inline verification** — immediately after creating a user, the script checks that the user actually exists. This verification-inside-the-loop pattern ensures problems are caught at the specific iteration where they occur, not discovered later.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing two bash scripts that use `for` loops: the first iterates through a hardcoded list and prints each item (to learn the mechanics), and the second creates multiple Linux users from a variable-based list with verification. The final outcome: understanding how to write and execute for loops, and seeing a real-world automation use case. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

***

## Script 1: Basic For Loop — `13_for.sh`

### Step 1: Create the Script

```bash
vim 13_for.sh
```

Write the following: [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

```bash
#!/bin/bash

for VAR1 in java .net python ruby php
do
    echo "Looping..."
    echo "Value of VAR1 is $VAR1"
    sleep 1
    echo "###########################"
done
```

**Line-by-line breakdown:**

* `#!/bin/bash` — Shebang, declares the interpreter.
* `for VAR1 in java .net python ruby php` — Begins the loop. `VAR1` is the loop variable. `java .net python ruby php` is the sequence — five items. On each iteration, the next item is assigned to `VAR1`.
* `do` — Opens the loop body.
* `echo "Looping..."` — Prints a static message (same every iteration).
* `echo "Value of VAR1 is $VAR1"` — Prints the current value of `VAR1` (changes each iteration).
* `sleep 1` — Pauses for 1 second so you can watch the loop execute step by step.
* `echo "###########################"` — Visual separator between iterations.
* `done` — Closes the loop body. After `done`, bash checks if more items remain. If yes, loop back. If no, exit the loop. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

### Step 2: Make It Executable and Run

```bash
chmod +x 13_for.sh
./13_for.sh
```

**Expected output:** Five iterations, each showing "Looping...", then "Value of VAR1 is java" (then `.net`, then `python`, then `ruby`, then `php`), separated by hash lines, with a 1-second pause between iterations. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

**Verification:** Count the iterations — there should be exactly 5, matching the 5 items in the list. The final value printed should be `php` (the last item).

**Common mistakes:**

* Forgetting `done` — bash will show a syntax error or wait for more input
* Forgetting `do` — same result, syntax error
* Using `$VAR1` in the `for` line instead of `VAR1` — the `for` line declares the variable name (no `$`), while the body references its value (with `$`)

**Connection to flow:** This script proves the loop mechanics work. The next script applies the same pattern to a real task.

***

## Script 2: User Creation Loop — `14_for.sh`

### Step 1: Create the Script

```bash
vim 14_for.sh
```

Write the following: [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

```bash
#!/bin/bash

MYUSERS="Alpha Beta Gamma"

for usr in $MYUSERS
do
    echo "###########################"
    echo "Adding user $usr"
    useradd $usr
    id $usr
    echo "###########################"
done
```

**Line-by-line breakdown:**

* `MYUSERS="Alpha Beta Gamma"` — A variable holding the list of usernames. Three space-separated names = three loop iterations.
* `for usr in $MYUSERS` — `$MYUSERS` expands to `Alpha Beta Gamma`. The loop variable `usr` gets `Alpha` first, then `Beta`, then `Gamma`.
* `echo "Adding user $usr"` — Progress message showing which user is being created.
* `useradd $usr` — Creates the Linux user. On the first iteration, this runs `useradd Alpha`.
* `id $usr` — Immediately verifies the user was created by printing their UID, GID, and groups. If `useradd` failed, `id` will show an error — giving you instant per-iteration feedback.
* Hash-line echoes — Visual separators between iterations. [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

### Step 2: Make It Executable and Run

```bash
chmod +x 14_for.sh
sudo ./14_for.sh
```

**Note:** `useradd` requires root privileges. Either run the script with `sudo`, or run as root (`sudo -i` first).

**Expected output:** Three blocks (one per user), each showing "Adding user Alpha/Beta/Gamma", followed by the `id` output for that user (UID, GID, groups). [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)

**Verification:**

* `id` output should show valid UID/GID for each user — this confirms `useradd` succeeded
* Three iterations, matching the three names in `MYUSERS`

**Common mistakes:**

* Running without root/sudo — `useradd` will fail with "Permission denied"
* Running the script twice without deleting users first — `useradd` will fail with "user already exists" for each name

**Failure scenario:** If `useradd` fails for one user (e.g., user already exists), the loop **continues** to the next user — it does not stop. The `id` command for that iteration will still succeed (because the user exists from the previous run), which might mask the `useradd` error. Watch for `useradd: user 'Alpha' already exists` messages in the output.

⚠️ **Expert Note:** In production scripts, you'd typically add error checking after `useradd` — check the exit code (`$?`) and handle the failure (skip, log, or abort). The basic for loop doesn't have built-in error handling; it just runs every command in the body regardless of whether previous commands succeeded or failed.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ For Loop — Core Mechanism

```
SYNTAX:
  for VARIABLE in item1 item2 item3
  do
      commands using $VARIABLE
  done

EXECUTION FLOW:
  VARIABLE=item1 → execute body → loop back
  VARIABLE=item2 → execute body → loop back
  VARIABLE=item3 → execute body → loop back
  sequence exhausted → exit loop

ITERATION COUNT = number of items in sequence
```

***

## ⚡ Key Syntax Rules — Instant Recall

```
for line:    VARIABLE (no $)     ← declaring the name
body:        $VARIABLE (with $)  ← reading the value

Opening:     for ... in ...
             do
Closing:     done

Parallel:    if/fi    ←→    for/do/done

Sequence sources:
  Inline:    for x in a b c           ← hardcoded
  Variable:  LIST="a b c"; for x in $LIST  ← from variable
  (Future: command substitution, file content, etc.)
```

***

## 🔗 Two Scripts — Structure Map

```
13_for.sh (LEARNING)                14_for.sh (REAL USE CASE)
┌────────────────────────┐          ┌────────────────────────┐
│ for VAR1 in java .net  │          │ MYUSERS="Alpha Beta    │
│   python ruby php      │          │   Gamma"               │
│ do                     │          │ for usr in $MYUSERS    │
│   echo (message)       │          │ do                     │
│   echo $VAR1           │          │   echo (message)       │
│   sleep 1              │          │   useradd $usr         │
│   echo (separator)     │          │   id $usr  ← VERIFY   │
│ done                   │          │   echo (separator)     │
│                        │          │ done                   │
│ Iterations: 5          │          │ Iterations: 3          │
│ Purpose: observe loop  │          │ Purpose: create users  │
└────────────────────────┘          └────────────────────────┘
```

***

## 🔄 Loop Problem Pattern

```
PROBLEM: Same command, N times, only one part changes
  ↓
SOLUTION: for loop

  useradd Alpha    ┐
  useradd Beta     ├── repetitive, only name changes
  useradd Gamma    ┘
       ↓ becomes ↓
  for usr in Alpha Beta Gamma
  do
      useradd $usr       ← command written ONCE
  done                   ← runs N times automatically

SCALING: Change list size → loop auto-adjusts
  3 users → 3 iterations
  100 users → 100 iterations
  Same script, no code change needed
```

***

## 📦 Control Structure Keyword Pairs

```
if   ... fi          ← conditional
for  ... do ... done ← loop
(while ... do ... done ← mentioned, not covered)
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: List-Driven Automation**
Store items in a list (inline or variable) → loop iterates through list → same command(s) applied to each item. Scales by growing the list, not by duplicating code. This is the fundamental automation pattern for any "do X for each Y" task.

**Pattern 2: Inline Verification**
After the action command (`useradd`), immediately run a verification command (`id`) inside the same loop iteration. This catches failures at the point of occurrence rather than discovering them after all iterations complete.

**Pattern 3: Variable-as-Data-Source**
Separating the data (`MYUSERS="Alpha Beta Gamma"`) from the logic (`for usr in $MYUSERS`) makes the script configurable. To change which users are created, modify only the variable — not the loop structure. Data and logic are decoupled.

***

## 🎯 One-Line System Summary

> **A bash `for` loop takes a sequence of items (inline or from a variable), assigns each item to a loop variable one at a time, executes the entire command block between `do` and `done` for each item, and stops when the sequence is exhausted — transforming N repetitive manual commands into a single loop that scales by list size.** [\[100-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/100-loops.txt)
