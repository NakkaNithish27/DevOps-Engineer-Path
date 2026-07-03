# 🎓 Deep Learning Material: While Loops in Bash — Condition-Driven Iteration, Infinite Loops, and Termination Control

**Source:** Video lecture on while loops in bash scripting (from [101-while-loops.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt?EntityRepresentationId=e4239923-d96b-418d-8a65-7d75dfdc5902) caption file) [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Video Context:** This lecture builds on prior knowledge of `for` loops and `if` conditions. The instructor introduces the `while` loop as a **condition-driven** iteration mechanism (contrasted with `for` loops which are sequence-driven). The teaching unfolds through live terminal experimentation — the instructor deliberately creates an infinite loop first, lets it run, kills it, then fixes it — building understanding through observable failure before showing the correct pattern. The lecture covers finite loops with counter increment, intentional infinite loops using `true`, arithmetic operations inside loops, and closes with a critical operational warning about uncontrolled loops in production.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — While Loop vs. For Loop: Two Different Drivers of Iteration

Bash provides two fundamental loop types, and they are driven by **different engines**. A `for` loop iterates over a **sequence** — a predefined list of items. It knows in advance how many times it will run because the list has a finite number of elements. A `while` loop, by contrast, iterates based on a **condition**. It does not know in advance how many times it will run. It checks a condition before each iteration, and **as long as that condition evaluates to true, it keeps executing the code block**. It stops only when the condition becomes false. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

The instructor frames this distinction immediately: *"a for loop runs for a sequence, a while loop runs for a condition."* This is the foundational mental model. The `for` loop asks "what items do I iterate over?" The `while` loop asks "should I keep going?" These are fundamentally different questions, and they make each loop suited for different kinds of tasks. You use `for` when you have a known collection to process. You use `while` when you need to repeat something until a state changes.

***

## 1.2 — The Structure of a While Loop: Condition → Do → Done

A `while` loop in bash has a specific syntactic structure. You write the keyword `while`, followed by a **condition expression** (using the same syntax as `if` conditions — square brackets with a test expression inside), followed by the keyword `do`, then the body of the loop (the commands to execute each iteration), and finally the keyword `done` to close the loop. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

The condition is evaluated **before** each iteration, including the very first one. If the condition is false from the start, the loop body never executes at all. If the condition is true, the body executes, and then control returns to the condition check. This cycle repeats until the condition evaluates to false.

The instructor explicitly connects this to prior knowledge: *"I have to give a condition like the give condition in the 'if'. Here also, we give the condition."* This means everything you know about writing conditions for `if` statements — comparison operators, string tests, numeric tests — applies directly to `while` loop conditions. The condition syntax is not a new concept; it's the same mechanism reused in a loop context.

***

## 1.3 — The Infinite Loop Problem: What Happens When the Condition Never Becomes False

This is the most important conceptual lesson in the entire lecture, and the instructor teaches it by **deliberately creating the problem first**.

He sets up a counter variable initialized to `0`, writes a `while` loop that checks `$counter -lt 5` (counter less than 5), and inside the loop body, prints the counter value — but **does not change the counter**. The result: the counter stays at `0` forever. Every time the loop checks "is 0 less than 5?", the answer is `true`. The loop never terminates. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

The instructor explains the mechanics precisely: *"the value of counter is 0 first, it's going to check if zero is less than five. That is true. It is less than five. So it will execute the code and then again come back and again check it... Yes, zero because it's been zero. Every time the loop runs, it will be zero. Each and every iteration, because we are not changing the value of counter. So this is going to run for infinity."* [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

This is the fundamental rule of while loops: **the loop body MUST contain logic that eventually makes the condition false.** If nothing inside the loop changes the variables that the condition depends on, the condition's truth value can never change, and the loop runs forever.

The only way to stop an accidental infinite loop is to **externally kill the process** using `Ctrl+C`. The instructor demonstrates this and notes that *"sometimes you have to press multiple times"* — because the loop may be executing a command when you press `Ctrl+C`, and the signal may be caught by the child process rather than the loop itself. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

> 🔍 **Deep Dive**
>
> `Ctrl+C` sends a `SIGINT` (Signal Interrupt) to the foreground process. In a tight loop with no `sleep`, the shell is rapidly cycling between condition check and body execution. The signal gets delivered between instructions, but if the loop body involves a command that traps or handles signals, you may need to press `Ctrl+C` multiple times. The instructor's observation about pressing multiple times reflects real terminal behavior — it's not a glitch, it's signal delivery timing.

***

## 1.4 — Counter Increment: The Mechanism That Makes Loops Finite

The fix for the infinite loop is to **modify the counter inside the loop body** so that it progresses toward the termination condition. The instructor adds the line `counter=$(($counter + 1))` inside the loop. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

Let's break down this arithmetic expression. The outer `$( )` is command substitution syntax — but here, the inner `(( ))` is bash **arithmetic evaluation**. Inside `(( ))`, bash evaluates mathematical expressions. `$counter + 1` takes the current value of `counter` and adds `1`. The result is assigned back to `counter`. So each iteration, the counter increases by one: 0 → 1 → 2 → 3 → 4 → 5. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

When the counter reaches `5`, the condition `$counter -lt 5` (is 5 less than 5?) evaluates to **false**. The loop terminates, and execution continues with whatever comes after the `done` keyword. The instructor places `echo "out of the loop"` after the loop to visually confirm that execution has exited the loop block. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

The instructor also adds `sleep 1` inside the loop body. This pauses execution for one second between iterations, making the output human-readable rather than a rapid scroll. Without `sleep`, the loop runs as fast as the CPU allows, and the output flashes by too quickly to observe. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

> 🔍 **Deep Dive**
>
> The iteration count in this example is exactly **5** (counter values 0, 1, 2, 3, 4). This is because the condition uses **less than** (`-lt`), not **less than or equal to** (`-le`). The instructor initially considers "less than or equal to" but then settles on "less than." This distinction matters: `-lt 5` gives 5 iterations (0–4); `-le 5` would give 6 iterations (0–5). Off-by-one errors in loop conditions are one of the most common bugs in programming. Always mentally trace the boundary value (here: what happens when counter equals exactly 5?) to verify your loop count.

***

## 1.5 — Intentional Infinite Loops: The `while true` Pattern

Not all infinite loops are bugs. Sometimes you **want** a loop that runs forever — a monitoring daemon, a service listener, a continuous data processor. Bash provides a clean way to express this: `while true`. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

`true` is a **bash built-in command** that does nothing except return a success exit code (exit status 0). In bash, an exit status of 0 means "true" in conditional contexts. So `while true` means "while the condition is true" — and since `true` always returns success, the condition is always true. The loop runs forever by design. The instructor describes it as: *"That's a boolean expression. True means true. It's going to be true forever."* [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

The instructor demonstrates this by creating a copy of the script (`16_while.sh`), replacing the numeric condition with `true`, and changing the arithmetic from addition to multiplication: `counter=$(($counter * 2))`, starting the counter at `2`. This produces the sequence 2, 4, 8, 16, 32, 64... — powers of 2, doubling every iteration. The loop never terminates because there is no condition to become false; the only way to stop it is `Ctrl+C`. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

***

## 1.6 — The Operational Warning: Uncontrolled Loops in Production

The instructor closes with a critical real-world warning that elevates this from a scripting lesson to an operational safety lesson: *"make sure whenever you're using while loop, you know how to terminate, that condition needs to become false at some point of time, otherwise it will run for infinity. And imagine that running in the background as a cron job. That will put some load on your system if you're doing some heavy operation."* [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

This is the production-thinking dimension. An infinite loop running interactively in a terminal is annoying but easily killed with `Ctrl+C`. The same infinite loop **scheduled as a cron job** is dangerous — it runs in the background with no terminal attached, no human watching, and no `Ctrl+C` available. Each cron trigger spawns a new instance. If the loop does CPU-intensive or I/O-intensive work, it will consume system resources indefinitely. Multiple cron triggers can stack up, each running its own infinite loop, compounding the load until the system becomes unresponsive. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

> ⚠️ **Expert Note**
>
> In production environments, scripts with while loops should always have **explicit termination safeguards**: a maximum iteration count, a timeout mechanism, or a conditional break triggered by an external signal or file. Relying solely on the loop condition to eventually become false is risky — if the data or state that the condition depends on behaves unexpectedly, the loop becomes infinite. Defensive scripting means planning for the case where your termination condition never fires.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are writing bash scripts that use `while` loops to repeatedly execute code based on a condition. The operational progression is: **(1)** create an infinite loop (to understand the danger), **(2)** fix it with a counter increment (to understand termination), **(3)** build an intentional infinite loop with `while true` (to understand deliberate infinite iteration). The final outcome is operational confidence in writing, controlling, and terminating while loops.

***

## Step 1: Create the Initial Script with a While Loop (Infinite — By Design of the Lesson)

**What we're doing:** Writing a while loop that checks a counter but doesn't change it — deliberately creating an infinite loop to observe the behavior.

**Set the counter variable:**

```bash
counter=0
```

* `counter` — variable name
* `=0` — initial value (no spaces around `=`) [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Write the while loop structure:**

```bash
while [ $counter -lt 5 ]
do
    echo "looping"
    echo "value of counter is $counter"
done
```

* `while` — begins the loop
* `[ $counter -lt 5 ]` — condition: is the value of `counter` less than 5? (`-lt` = less than)
* `do` — marks the start of the loop body
* `echo "looping"` — prints a static message each iteration
* `echo "value of counter is $counter"` — prints the current counter value
* `done` — marks the end of the loop body; control returns to the `while` condition check [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Make the script executable:**

```bash
chmod +x <scriptname>.sh
```

**Run it:**

```bash
./<scriptname>.sh
```

**Expected behavior:** The script prints "looping" and "value of counter is 0" endlessly. The counter never changes, so the condition `0 < 5` is always true. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**How to stop it:**

```bash
Ctrl+C
```

Press `Ctrl+C` to send SIGINT to the process. You may need to press it **multiple times** if the signal doesn't register immediately. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Connection to system flow:** This step proves that a while loop without state change in the loop body = infinite execution. This is the failure case you must always guard against.

***

## Step 2: Fix the Infinite Loop — Add Counter Increment

**What we're doing:** Adding a line inside the loop body that changes the counter value each iteration, ensuring the condition eventually becomes false.

**Open the script and add the counter increment:**

```bash
counter=$(($counter + 1))
```

* `$(( ))` — bash arithmetic evaluation; computes the math expression inside
* `$counter + 1` — takes current counter value, adds 1
* `counter=` — assigns the result back to `counter` [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Add a post-loop confirmation message:**

```bash
echo "out of the loop"
```

This line is placed **after** `done`. It only executes when the loop terminates — confirming that we've exited the loop cleanly. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Add a sleep for readable output:**

```bash
sleep 1
```

* `sleep 1` — pauses execution for 1 second; placed inside the loop body so each iteration pauses before the next
* Without this, the loop runs at full CPU speed and output scrolls too fast to observe [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**The complete fixed script:**

```bash
#!/bin/bash
counter=0
while [ $counter -lt 5 ]
do
    echo "looping"
    echo "value of counter is $counter"
    counter=$(($counter + 1))
    sleep 1
done
echo "out of the loop"
```

**Run it:**

```bash
./<scriptname>.sh
```

**Expected output:**

```
looping
value of counter is 0
looping
value of counter is 1
looping
value of counter is 2
looping
value of counter is 3
looping
value of counter is 4
out of the loop
```

The loop runs exactly **5 times** (counter values 0, 1, 2, 3, 4). When counter reaches 5, the condition `5 -lt 5` is false → loop exits → "out of the loop" prints. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**How to verify success:** Count the iterations in the output — should be exactly 5. Confirm "out of the loop" appears at the end. If the loop doesn't stop, the increment line is missing or incorrect.

**Common mistakes:**

* Forgetting the `$` in `$counter` inside `$(( ))` — without `$`, bash doesn't expand the variable
* Putting spaces around `=` in the assignment (`counter = $((...))`) — bash interprets this as a command, not an assignment
* Using `-lt` vs `-le` confusion — off-by-one error in iteration count

***

## Step 3: Create an Intentional Infinite Loop with `while true`

**What we're doing:** Copying the script and modifying it to run forever on purpose, using `true` as the condition and multiplication instead of addition.

**Copy the script:**

```bash
cp <original>.sh 16_while.sh
```

* `cp` — copy command; creates `16_while.sh` as a duplicate to modify without losing the original [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Edit `16_while.sh` — change the condition and arithmetic:**

```bash
#!/bin/bash
counter=2
while true
do
    echo "looping"
    echo "value of counter is $counter"
    counter=$(($counter * 2))
    sleep 1
done
echo "out of the loop"
```

Key changes from the previous version:

* **`counter=2`** — starting value changed to 2 (multiplying 0 by 2 would always stay 0; starting at 2 gives meaningful progression) [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)
* **`while true`** — replaces the numeric condition; `true` is a bash builtin that always returns exit code 0 (success = true); the loop never terminates on its own [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)
* **`$(($counter * 2))`** — multiplication instead of addition; `*` is the multiplication operator inside `(( ))`; the counter doubles each iteration: 2 → 4 → 8 → 16 → 32 → ... [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Run it:**

```bash
./16_while.sh
```

**Expected output:**

```
looping
value of counter is 2
looping
value of counter is 4
looping
value of counter is 8
looping
value of counter is 16
...
(continues forever)
```

**How to stop:** `Ctrl+C` — this is the **only** way to stop a `while true` loop (from the terminal). [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**What happens without `sleep`:** The instructor notes that removing `sleep` makes the loop *"run super fast"* — output floods the terminal instantly. The `sleep` is not a functional requirement; it's an observability aid. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

**Connection to system flow:** This demonstrates the `while true` pattern used in real-world scripts for daemons, watchers, and continuous processes. The key operational difference from the accidental infinite loop in Step 1: here, infinity is **intentional and controlled** — you chose it, you know `Ctrl+C` stops it, and you understand the resource implications.

> ⚠️ **Expert Note**
>
> The instructor's warning about cron jobs applies directly here. If you schedule a `while true` script as a cron job, every cron trigger starts a **new** infinite loop instance. Within hours, you could have dozens of processes all running infinite loops, each consuming CPU and memory. In production, `while true` scripts should either: (a) never be cron-scheduled (run them as managed services instead), or (b) include a self-termination mechanism (max iterations, timeout, or pidfile-based duplicate detection). [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept Anchor

```
for loop  → iterates over a SEQUENCE (list of items)
while loop → iterates on a CONDITION (boolean check each cycle)
```

***

## 🔷 While Loop Execution Cycle

```
      ┌─────────────────────┐
      │  Evaluate CONDITION  │ ◄──────────────────┐
      └─────────┬───────────┘                     │
                │                                  │
          TRUE  │   FALSE                          │
                │     │                            │
                ▼     ▼                            │
           [EXECUTE  [EXIT LOOP                    │
            BODY]     → continue after "done"]     │
                │                                  │
                └──────────────────────────────────┘
```

***

## 🔷 The Infinite Loop Rule

```
CONDITION depends on VARIABLE(S)
  │
  BODY changes variable(s)? 
    │
    YES → condition eventually becomes false → LOOP TERMINATES
    │
    NO  → condition is ALWAYS TRUE → INFINITE LOOP → Ctrl+C to kill
```

**One-line rule:** If nothing in the body moves the condition toward false, the loop runs forever.

***

## 🔷 Syntax Structure

```bash
variable=INITIAL_VALUE
while [ $variable OPERATOR THRESHOLD ]
do
    # loop body
    variable=$(($variable ARITHMETIC))    # ← MUST progress toward termination
    sleep N                                # ← optional: observability
done
echo "post-loop code"                      # ← executes only after loop exits
```

***

## 🔷 Arithmetic Inside Loops

```
counter=$(($counter + 1))    → increment by 1 (linear growth: 0,1,2,3,4...)
counter=$(($counter * 2))    → multiply by 2 (exponential growth: 2,4,8,16...)

Syntax: $(( expression ))    → bash arithmetic evaluation
        $variable            → current value expansion inside (( ))
```

***

## 🔷 Two Kinds of Infinite Loops

```
ACCIDENTAL                              INTENTIONAL
──────────────────────                  ──────────────────────
Cause: forgot to change variable        Pattern: while true
Result: unexpected infinite execution   Result: designed infinite execution
Fix: add counter increment in body      Stop: Ctrl+C or external signal
Danger: HIGH (silent resource drain)    Danger: CONTROLLED (if you know it's there)
```

***

## 🔷 `while true` Pattern

```
while true        ← "true" = builtin command, always returns exit code 0
do                ← condition is ALWAYS true by definition
    ...           ← loop body runs forever
done              ← never reached unless body contains "break"
```

Use case: daemons, watchers, continuous processors

***

## 🔷 Operational Danger Chain

```
while loop + no termination path
  │
  ▼
Runs in terminal → annoying but Ctrl+C kills it
  │
  ▼
Runs as CRON JOB → background, no terminal, no Ctrl+C
  │
  ▼
Each cron trigger = NEW infinite loop instance
  │
  ▼
Multiple instances stacking → CPU/memory exhaustion → SYSTEM OVERLOAD
```

***

## 🔷 Key Commands (Quick Reference)

```
counter=0                         → initialize variable
while [ $counter -lt 5 ]          → condition: counter < 5
do ... done                       → loop body delimiters
counter=$(($counter + 1))         → increment counter
counter=$(($counter * 2))         → double counter
echo "out of the loop"            → post-loop confirmation
sleep 1                           → 1-second pause per iteration
Ctrl+C                            → SIGINT → kill foreground process
while true                        → intentional infinite loop
cp script.sh 16_while.sh          → copy script to new file
chmod +x script.sh                → make executable
```

***

## 🔷 Cause → Effect Diagnosis

```
Loop never stops?
  → Check: does the body change the condition variable?
  → Fix: add increment/decrement inside loop body

Loop runs wrong number of times?
  → Check: -lt vs -le (off-by-one)
  → Check: initial value of counter

Counter not changing?
  → Check: $ before variable name in $(( ))
  → Check: no spaces around = in assignment

Need to stop a runaway loop?
  → Interactive: Ctrl+C (may need multiple presses)
  → Background: find PID with ps, then kill <PID>
```

***

## 🔷 Reusable Engineering Pattern: Condition-Guard Loop

```
PATTERN: Initialize State → Check Condition → Execute → Mutate State → Recheck

    state = initial
    while (state meets condition):
        execute work
        state = transform(state)     ← MANDATORY for termination
    post-loop

RULE: The transform MUST move state toward condition failure.
      Without transform → infinite loop.
      
This pattern appears in:
  - Retry loops (counter tracks attempts)
  - Polling loops (check until resource ready)
  - Processing loops (consume until queue empty)
  - Convergence loops (iterate until error < threshold)
```

***

## 🔷 Video Teaching Sequence (Flow Reconstruction)

```
1. Create loop WITHOUT increment → observe infinite loop
2. Kill with Ctrl+C → learn emergency termination
3. Add counter increment → observe controlled termination
4. Add sleep → observe paced execution
5. Add post-loop echo → confirm clean exit
6. Copy script → create while true variant
7. Replace condition with true → intentional infinite loop
8. Replace + with * → observe exponential growth
9. Warning: cron + infinite loop = system overload
```

This deliberate **fail-first, fix-second** teaching sequence is itself a reusable pattern: understanding failure before understanding correctness produces deeper retention. [\[101-while-loops \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/101-while-loops.txt)
