# 🎓 Decision Making Part 2: `elif` — Deep Learning Material

**Source:** Video caption file — *Decision Making Part 2 (elif)* [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: What Happens When You Have More Than Two Outcomes?

In the previous lecture, the `if`/`else` structure was introduced. That structure handles **two-path** logic: a condition is either true (execute the `if` block) or false (execute the `else` block). But real-world scripting constantly encounters situations where there are **more than two possible outcomes**. You don't just need "yes or no" — you need "is it this? If not, is it that? If not that either, then do the fallback." [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

This is exactly the problem that **`elif`** (else-if) solves. It introduces **additional condition checks** between the initial `if` and the final `else`, creating a multi-branch decision chain. Each `elif` adds a new condition to evaluate, and only if all preceding conditions were false does the chain continue downward. The `else` at the bottom is the **final fallback** — it executes only when every `if` and `elif` condition above it has been false. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

## 1.2 — How `elif` Works: The Execution Flow

The structure follows a strict **top-down, first-match-wins** evaluation pattern:

1. The `if` condition is evaluated first.
2. If it's **true** → execute the `if` block → **skip everything else** → jump to `fi`. End of story.
3. If it's **false** → move to the first `elif` condition.
4. If the `elif` condition is **true** → execute its block → **skip everything below** → jump to `fi`.
5. If the `elif` condition is also **false** → move to the next `elif` (if any), or to `else`.
6. The `else` block executes **only if every condition above it was false**. It's the unconditional fallback.
7. `fi` closes the entire structure. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

The critical behavioral rule: **exactly one block executes**. Once a condition matches and its block runs, the entire structure terminates at `fi`. No further conditions are checked. This is the "first-match-wins" model — the order of conditions matters because the first true condition captures all execution. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

> 🔍 **Deep Dive:** You can chain **multiple `elif`** blocks — not just one. The structure is `if → elif → elif → elif → ... → else → fi`. Each `elif` is an additional checkpoint in the decision chain. The `else` remains optional but serves as a safety net for unexpected states. In this video, the structure is `if → elif → else → fi` (one `elif`), but the mechanism scales to any number of conditions. The video explicitly shows three distinct outcomes (exactly one adapter, more than one adapter, no active adapter) — requiring three branches, which is exactly what `if`/`elif`/`else` provides.

***

## 1.3 — The Real-World Problem: Counting Active Network Interfaces

The video teaches `elif` through a practical systems-administration problem: **counting how many active network interfaces exist on a machine** and printing a different message depending on the count. This is not a toy example — monitoring network interface status is a real operational task in infrastructure management. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

The problem has three possible outcomes:

* **Exactly 1** active interface → report single adapter
* **More than 1** active interface → report multiple adapters
* **Zero** active interfaces (after excluding loopback) → report no active interfaces

Two outcomes would be handled by `if`/`else`. Three outcomes require `if`/`elif`/`else`. This is the perfect demonstration of why `elif` exists. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

## 1.4 — The Data Pipeline: Building a Command to Count Interfaces

Before the script can make decisions, it needs **data** — specifically, a count of active network interfaces. The video constructs this data through a **command pipeline**, building it step by step. Understanding this pipeline is essential because it demonstrates how operational data is extracted, filtered, and quantified for use in script logic.

### Step 1: Get all network interface information

The starting command is `ip addr show`, which displays **all network interfaces** on the machine. The output shows three interfaces, but the first one is the **loopback** interface (`lo`). The loopback is a virtual interface that the machine uses to talk to itself — it's always present and always active, but it's not a "real" network adapter in the sense of connecting to external networks. So for the purpose of counting real active interfaces, loopback must be **excluded**. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### Step 2: Filter out the loopback line

The pipeline uses `grep -v` with text unique to the loopback line (the word "loopback") to **exclude** that line from the output. `grep -v` is an **inverse match** — it removes lines that match the pattern instead of keeping them. After this filter, only the non-loopback interface lines remain. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### Step 3: Count occurrences of a common marker

The video identifies that the text **"mtu"** appears in every interface line — it's a common marker across all interface entries. By counting how many times "mtu" appears in the filtered output (after loopback removal), you get the number of active non-loopback interfaces. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

The counting is done with `grep -ic "mtu"`:

* `-i` = **case-insensitive** match (ignore uppercase/lowercase differences)
* `-c` = **count** mode — instead of printing matching lines, just print the number of matches [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### The Complete Pipeline

```
ip addr show | grep -v loopback | grep -ic mtu
```

This produces a single number — the count of active non-loopback interfaces. In the video, this number is **2**. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

> 🔍 **Deep Dive:** This pipeline demonstrates a reusable data extraction pattern: **raw data → filter unwanted entries → count relevant markers**. The same three-stage pattern applies to counting running processes, active services, error log entries, connected users, etc. The specific commands change but the structural pattern is identical: produce raw output → pipe through exclusion filter → pipe through counter.

***

## 1.5 — Comparison Operators: `-eq` and `-gt`

The script uses two numeric comparison operators inside the condition brackets:

**`-eq`** = **equal to**. `$value -eq 1` tests whether the variable equals the number 1. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

**`-gt`** = **greater than**. `$value -gt 1` tests whether the variable is greater than 1. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

These are Bash's **numeric comparison operators** — they work on integer values. They are used inside `[ ]` test brackets in `if` and `elif` conditions.

***

## 1.6 — Command Substitution: Capturing Command Output into a Variable

The pipeline's output (the count number) needs to be stored in a variable so the script can use it in conditions. This is done through **command substitution** using backticks or `$(...)`. The video stores the entire pipeline result into a variable called `value`. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

This is the bridge between the **data-gathering phase** (running commands, filtering, counting) and the **decision-making phase** (using `if`/`elif`/`else` on the result). Without command substitution, you'd have a number printed to the screen but no way to use it in script logic.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We're writing a Bash script that **automatically detects how many active network interfaces** are on the machine (excluding loopback) and prints a context-appropriate message based on the count. The script demonstrates the `if`/`elif`/`else` decision structure in a real systems-monitoring scenario. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

The final outcome: a script that outputs one of three messages — "one active adapter," "multiple active adapters," or "no active adapters found" — based on live system state.

***

## Step 1: Explore the Raw Data Source

### What We're Doing

Running `ip addr show` to see all network interfaces and understand the raw data we'll work with.

### The Command

```bash
ip addr show
```

**Breakdown:**

* `ip` — The modern Linux networking utility
* `addr` — Subcommand for address-related operations
* `show` — Display the current interface information

### Expected Output

Three interface blocks are shown. The first is `lo` (loopback) — identified by the word "loopback" in its line. The other two are real network adapters. Each interface line contains the text "mtu" — this is the marker we'll count. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### Connection to Larger Flow

This raw output is what we'll filter and count in the next step. We've identified two things: loopback needs to be excluded, and "mtu" is the countable marker.

***

## Step 2: Build the Counting Pipeline

### What We're Doing

Constructing a command pipeline that filters out loopback and counts active interfaces.

### The Command

```bash
ip addr show | grep -v loopback | grep -ic mtu
```

**Breakdown:**

* `ip addr show` — Produces all interface data (as explored in Step 1)
* `|` — Pipe: sends the output of the left command as input to the right command
* `grep -v loopback` — **Inverse grep**: removes any line containing "loopback". This eliminates the loopback interface from our data.
  * `-v` = invert match (exclude matching lines)
  * `loopback` = the pattern unique to the loopback interface line
* `|` — Second pipe: sends the filtered output onward
* `grep -ic mtu` — Counts occurrences of "mtu" in the remaining output.
  * `-i` = case-insensitive matching
  * `-c` = count mode (output the number of matches, not the matching lines)
  * `mtu` = the text common to every interface line [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### Expected Output

```
2
```

This confirms two active non-loopback interfaces. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### How to Verify

Compare this number against the `ip addr show` output manually — count the non-loopback interfaces yourself and confirm the number matches.

### Common Mistakes

* **Forgetting `-v` on the first grep** — Without the invert flag, you'd be *keeping* only the loopback line instead of removing it.
* **Using a non-unique filter term** — If the text you grep -v isn't unique to loopback, you might accidentally remove real interface lines.

### Connection to Larger Flow

This pipeline output is the **input data** for our decision-making script. Next we store this number in a variable.

***

## Step 3: Write the Script

### What We're Doing

Creating a script file that stores the pipeline result and uses `if`/`elif`/`else` to act on it.

### The Command to Create the Script

```bash
vim 9_ifelif.sh
```

(Later renamed to a file with prefix `10` for proper numbering) [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### The Script Content

```bash
#!/bin/bash

value=$(ip addr show | grep -v loopback | grep -ic mtu)

if [ $value -eq 1 ]
then
    echo "1 active network interface found."
elif [ $value -gt 1 ]
then
    echo "Found multiple active interfaces: $value"
else
    echo "No active interface found."
fi
```

 [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### Line-by-Line Breakdown

**`value=$(ip addr show | grep -v loopback | grep -ic mtu)`**

* Runs the entire counting pipeline (from Step 2)
* `$(...)` = command substitution — captures the command output (the number `2`) and stores it in the variable `value`
* After this line, `$value` contains the integer count of active interfaces [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

**`if [ $value -eq 1 ]`**

* First condition check: is `value` **equal to** 1?
* `-eq` = numeric equality operator
* If true → executes the next `echo` → skips everything else → reaches `fi` [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

**`elif [ $value -gt 1 ]`**

* Second condition check (only reached if the `if` was false): is `value` **greater than** 1?
* `-gt` = numeric greater-than operator
* If true → executes the next `echo` → skips `else` → reaches `fi` [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

**`else`**

* Fallback: reached only if `value` is not 1 AND not greater than 1. The only remaining possibility is 0 (or a negative number, which shouldn't occur here).
* Prints "no active interface found" [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

**`fi`**

* Closes the entire `if`/`elif`/`else` structure. Every `if` block must end with `fi`. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### The Decision Logic Mapped to Outcomes

```
value == 1   → "1 active network interface found"
value  > 1   → "Found multiple active interfaces"
value == 0   → "No active interface found"
```

Since we already confirmed the pipeline returns `2`, the script will print the "multiple active interfaces" message. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

## Step 4: Execute the Script

### The Command

```bash
bash 9_ifelif.sh
```

(Or after renaming: the script with prefix `10`) [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### Expected Output

```
Found multiple active interfaces: 2
```

This matches our prediction — `value` is 2, which is greater than 1, so the `elif` branch executes. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

### How to Verify

* The output message matches the `elif` branch, confirming the correct branch was taken.
* You can add `echo $value` before the `if` block to see the raw count value during debugging.
* You can temporarily hardcode `value=1` or `value=0` to test the other branches.

### Common Mistakes

* **Forgetting spaces inside `[ ]`** — `[$value -eq 1]` fails. Bash requires spaces: `[ $value -eq 1 ]`. The brackets are actually a command (`test`), and the spaces are argument separators.
* **Missing `then` after `elif`** — Every `if` and `elif` condition must be followed by `then`. Omitting it causes a syntax error.
* **Forgetting `fi`** — The structure isn't closed without it. Bash will throw an unexpected-end-of-file error.
* **Using `=` instead of `-eq`** — For numeric comparison in `[ ]`, use `-eq`, `-gt`, `-lt`, etc. The `=` operator does string comparison, which may produce incorrect results with numbers.

***

## Step 5: Script Renaming (Housekeeping)

The video notes that the script name `9_ifelif.sh` conflicts with another similarly named file. It's renamed with a `10` prefix for proper sequencing in the script collection. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

```bash
mv 9_ifelif.sh 10_ifelif.sh
```

This is a minor housekeeping step but reflects a practical habit: **keep scripts numbered and organized** so you can find them later in your learning progression.

***

## What Comes Next

The video explicitly states that in the **next lecture**, this `if`/`elif`/`else` knowledge will be applied to **monitor a process and take action based on that information**. This means the decision-making structure will be combined with process monitoring commands to build a real operational monitoring script. [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 📐 `if` / `elif` / `else` Execution Structure

```
if [ condition_1 ]          ◄── Checked FIRST
then
    action_1                ◄── Executes ONLY if condition_1 = TRUE → jump to fi
elif [ condition_2 ]        ◄── Checked ONLY if condition_1 = FALSE
then
    action_2                ◄── Executes ONLY if condition_2 = TRUE → jump to fi
else                        ◄── Reached ONLY if ALL conditions = FALSE
    fallback_action
fi                          ◄── End of structure

RULE: Exactly ONE block executes. First true condition wins. Order matters.
```

 [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

## 🔄 Data Pipeline → Decision Chain (Script Architecture)

```
DATA GATHERING PHASE                    DECISION PHASE
─────────────────────                   ──────────────
ip addr show                            if [ $value -eq 1 ]
  │                                         → "1 active adapter"
  ├── grep -v loopback  (exclude)       elif [ $value -gt 1 ]
  │                                         → "multiple active adapters"
  └── grep -ic mtu      (count)        else
        │                                   → "no active adapter"
        ▼                               fi
  value=<count>  ──────────────────▶
```

 [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

## 🛠️ Pipeline Command Decomposition

```
ip addr show | grep -v loopback | grep -ic mtu
│              │                  │
│              │                  └── Count "mtu" occurrences (case-insensitive)
│              │                      -i = ignore case
│              │                      -c = count mode (output number, not lines)
│              │
│              └── Remove loopback line
│                  -v = invert match (exclude matching lines)
│
└── Show all network interfaces (raw data source)

OUTPUT: single integer = count of active non-loopback interfaces
```

***

## 🔑 Comparison Operators Used

```
-eq  →  equal to        (numeric)
-gt  →  greater than    (numeric)
```

***

## ⚡ Three-Outcome Decision Map (This Script)

```
value == 1  →  Single adapter message    (if branch)
value  > 1  →  Multiple adapter message  (elif branch)
value == 0  →  No adapter message        (else branch)

Video result: value = 2 → elif branch fires ✅
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: RAW DATA → FILTER → COUNT → DECIDE
  ip addr show → grep -v (exclude) → grep -ic (count) → if/elif/else
  → Same pattern as:
    ps aux → grep -v grep → grep -c process → decide if running
    cat log → grep -v noise → grep -c ERROR → decide severity
    df -h → filter mount → extract % → decide if disk full
  
  UNIVERSAL FORM: produce_data | exclude_noise | count_signal → branch on count

PATTERN 2: FIRST-MATCH-WINS EVALUATION CHAIN
  if/elif/elif/.../else = ordered priority chain
  → Same pattern as:
    Firewall rules (first matching rule applies)
    Route tables (most specific match wins)
    Switch/case in programming
    Load balancer health check cascades

PATTERN 3: COMMAND SUBSTITUTION AS DATA BRIDGE
  value=$(command_pipeline)
  → Bridges data-gathering phase to decision-making phase
  → Same pattern as: storing API response before processing,
    capturing metric before alerting, query result → conditional logic
```

 [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS lecture  →  if/else (two-branch decisions)
THIS lecture      →  elif (multi-branch decisions) + real pipeline example
NEXT lecture       →  Monitor a PROCESS and take ACTION based on status
                     (combines if/elif/else with process monitoring)
```

 [\[98-decisio...king-part2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/98-decision-making-part2.txt)

***

Your `elif` decision-making toolkit is now fully mapped. Ready for the next caption file, or want me to generate **AnkiDroid flashcards (.csv)** from any of the materials we've covered? 🃏
