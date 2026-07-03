# 🧠 Python Exception Handling — try, except, else & Defensive Programming

**Source:** *216. Exception Handling* — Python Programming Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Core Problem: Programs Crash When Unexpected Things Happen

Consider a simple program: it takes a number from the user and divides 10 by that number. If the user types `2`, the result is `5.0` — the program runs perfectly. But what if the user types `abc`? Or `0`? The program **crashes**. It terminates abruptly, throws a cryptic error message to the screen, and any code that was supposed to run after the failing line never executes.

This is the problem exception handling exists to solve. In real programs — especially **automation scripts** — things will fail. A network request times out, a file doesn't exist, a user provides invalid input, an API returns an unexpected format. The instructor emphasizes this directly: *"Things can fail, it will fail, and you should know a way to handle those."* Exception handling gives you a structured mechanism to **intercept failures**, respond to them gracefully, and keep the program running (or terminate it on your terms, with a meaningful message).

***

## 1.2 What Is an Exception?

An exception is Python's way of signaling that something went wrong during execution. When Python encounters an operation it cannot complete — dividing by zero, converting a string to an integer when the string isn't numeric, accessing a variable that doesn't exist — it **raises an exception**. If nothing in the code handles that exception, Python's default behavior is to **terminate the program** and print a traceback showing the error type and where it occurred.

The video demonstrates two specific exceptions:

**`ValueError`** — Raised when a function receives an argument of the right type but an inappropriate value. In the video's case: `int("abc")` tries to convert the string `"abc"` into an integer, which is impossible. Python raises `ValueError: invalid literal for int()` and the program dies.

**`ZeroDivisionError`** — Raised when dividing any number by zero. `10 / 0` is mathematically undefined, so Python raises `ZeroDivisionError: division by zero`.

Both exceptions, if unhandled, produce the same result: **abrupt program termination**. The user sees an ugly traceback instead of a helpful message, and any remaining program logic never executes.

***

## 1.3 The try/except Structure — Intercepting Failures

The fundamental construct for exception handling in Python is the **`try`/`except`** block. The conceptual model is straightforward:

**`try:`** — "Attempt to execute this code. If it works, great. If it raises an exception, don't crash — instead, jump to the matching `except` block."

**`except <ExceptionType>:`** — "If the specific exception type was raised in the `try` block, execute this code instead of crashing."

The flow is:

1. Python enters the `try` block and begins executing code line by line.
2. If all lines execute without error → the `except` block is **skipped entirely**, and execution continues after it.
3. If any line raises an exception → Python **immediately stops** executing the `try` block (remaining lines in `try` are skipped), looks for a matching `except` block, and executes its code.

This is the core mechanism: `try` defines the "risky" code, and `except` defines the "recovery" code for specific failure modes.

***

## 1.4 Typed Exceptions — Catching Specific Errors

When writing an `except` block, you can specify **which exception type** to catch:

```python
except ValueError:
    print("Invalid input! Enter a valid number.")
```

This catches **only** `ValueError`. If a different exception occurs (like `ZeroDivisionError`), this `except` block won't match, and the program will still crash for that unhandled exception type.

You can chain **multiple `except` blocks** to handle different exception types differently:

```python
except ValueError:
    print("Invalid input!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

Each `except` block is like a specialized handler for a specific failure mode. Python checks them in order — when an exception is raised, it matches against the first compatible `except` block and executes that one.

> 🔍 **Deep Dive:** This typed exception system allows you to provide **contextually appropriate responses** to different failures. A `ValueError` (bad input) might prompt the user to re-enter data. A `ZeroDivisionError` might skip the calculation and use a default value. A `ConnectionError` in an automation script might trigger a retry. Each failure mode can have its own recovery strategy — which is far more useful than a generic "something went wrong" for every case.

***

## 1.5 The Generic Exception Catch — Safety Net for the Unexpected

After handling the specific exceptions you can anticipate, you can add a **catch-all** handler using the base `Exception` class:

```python
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

`Exception` is the parent class of (almost) all Python exceptions. Using `except Exception` catches **any** exception that wasn't already caught by a more specific `except` block above it. The `as e` syntax captures the exception object into the variable `e`, which contains the error message. You can then print it, log it, or use it for debugging.

The instructor positions this as a safety net: *"We don't know what to expect."* Even after handling the exceptions you anticipate, there might be others you haven't thought of. The generic catch prevents the program from crashing due to unforeseen errors.

> ⚠️ **Expert Note:** In real automation scripts, the generic `except Exception as e` block is where you'd typically **log the error** (not just print it), potentially **send an alert**, and decide whether to continue, retry, or exit gracefully. Simply printing a message is fine for learning, but production code needs the error information preserved for debugging.

***

## 1.6 The else Block — Code That Runs Only on Success

The `try`/`except` structure has a subtle but important gap: where do you put code that should **only execute if the `try` block succeeded**? You can't put it inside the `try` block after the risky code, because if an exception occurs, everything in `try` after the failure point is skipped. You can't put it after the `except` block, because that code runs **regardless** of whether an exception occurred.

The `else` block solves this:

```python
try:
    # risky code
except ValueError:
    # handle error
else:
    # runs ONLY if try succeeded (no exception)
```

The flow with `else`:

1. `try` block executes.
2. If exception → `except` runs, `else` is **skipped**.
3. If no exception → `except` is **skipped**, `else` runs.
4. Code after all blocks runs regardless.

The video demonstrates this precisely. Without `else`, the instructor puts `print(f"The result is {result}")` after the `try`/`except` blocks. When the user enters a string, the `try` block fails (so `result` is never assigned), the `except` block runs, but then the `print(result)` line executes and crashes with `NameError: name 'result' is not defined` — because `result` was never created. Moving this print into an `else` block ensures it only executes when `result` was actually computed successfully.

> 🔍 **Deep Dive:** The `else` block is conceptually important because it separates **risky code** (in `try`) from **success-dependent code** (in `else`). This makes the code's intent clearer: everything in `try` is "the operation that might fail," and everything in `else` is "what to do with the result if it worked." It also prevents accidentally catching exceptions from the success-path code — if `print(result)` itself raised an exception, you wouldn't want your `ValueError` handler catching it, because that would be a different, unrelated bug.

***

## 1.7 The Exception Type Ecosystem

Python has a rich hierarchy of built-in exception types. The instructor checks a list and highlights several categories:

* **`ValueError`** — Wrong value for the expected type
* **`ZeroDivisionError`** — Division by zero (subclass of `ArithmeticError`)
* **`ArithmeticError`** — Parent of math-related errors
* **`FloatingPointError`** — Floating-point operation failure
* **`KeyError`** — Accessing a dictionary key that doesn't exist
* **`KeyboardInterrupt`** — User presses Ctrl+C
* **`MemoryError`** — System runs out of memory
* **`NameError`** — Using a variable that hasn't been defined
* **`ImportError`** — Failed to import a module/library
* **`Exception`** — The base class that catches (almost) everything

The instructor's practical advice on learning exception types: *"In my real-time experience, I have learned this exception by not executing, failing in the code, and then looking at the message. That's how I used to do it."* This is the natural learning path — you encounter exceptions through actual failures, read the error message, and then add the appropriate handler. You don't need to memorize the full list upfront.

***

## 1.8 Exception Handling in the Context of Automation

The instructor connects exception handling to its most critical use case: **automation**. When you write Python scripts that automate cloud infrastructure, deployments, or system administration tasks, the scripts run unattended. There's no human watching the terminal to see a crash and intervene. If a script crashes silently, an entire automation pipeline breaks.

Exception handling transforms fragile scripts into resilient ones. Instead of crashing when an AWS API call fails, the script catches the exception, logs the error, and either retries or escalates. The instructor frames this as the bridge to the next lecture: *"We are also going to try cloud automation by using Python."* Exception handling is the prerequisite skill for writing reliable automation code.

The instructor also hints at a deeper pattern: in the `except` block, *"Maybe we need to do something else, execute some other code, or execute some other function if things fail."* This means exception handlers aren't limited to printing messages — they can trigger alternative workflows, retry logic, cleanup operations, or fallback strategies.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are building a series of **four progressively more robust Python programs** that handle user input and division, each iteration adding a new layer of exception handling. The progression demonstrates: unhandled crash → single exception handler → else block for success-only code → multiple exception handlers with a generic catch-all.

**Final outcome:** A Python script that gracefully handles invalid string input, zero division, and any unexpected error — never crashing, always providing meaningful feedback, and executing all remaining program logic.

***

## Step 1: Set Up the Project Structure

In your IDE (the instructor uses PyCharm/IntelliJ), create a **new directory** for this exercise:

Go to **New → Directory**, name it `exceptions`.

Inside this directory, create the first Python file: **New → Python file** → name it `tr_one.py`.

***

## Step 2: Write the Base Program (No Exception Handling) — `tr_one.py`

```python
number = int(input("Enter a number: "))
result = 10 / number
print(f"The result is {result}")
print("Program ends here")
print("Happy coding")
```

**Line-by-line breakdown:**

* `input("Enter a number: ")` — Displays the prompt and waits for user input. Returns whatever the user types as a **string**.
* `int(...)` — Wraps the input, converting the string to an **integer**. This is where `ValueError` can occur if the input isn't a valid number.
* `number = ...` — Assigns the converted integer to the variable `number`.
* `result = 10 / number` — Divides 10 by the user's number. This is where `ZeroDivisionError` can occur if `number` is 0.
* `print(f"The result is {result}")` — f-string formatting: inserts the value of `result` into the output string.
* The last two `print` statements represent "the rest of the program" — code that should always run.

**Test run 1 — Happy path:**

```
Enter a number: 2
The result is 5.0
Program ends here
Happy coding
```

✅ Works perfectly. All lines execute.

**Test run 2 — String input:**

```
Enter a number: abc
ValueError: invalid literal for int() with base 10: 'abc'
```

❌ Program crashes. "Program ends here" and "Happy coding" **never print**.

**Test run 3 — Zero input:**

```
Enter a number: 0
ZeroDivisionError: division by zero
```

❌ Program crashes again.

**Connection to flow:** This demonstrates the problem. The next files progressively add exception handling.

***

## Step 3: Add Basic Exception Handling — `tr_two.py`

Copy `tr_one.py` → paste into the `exceptions` folder → rename to `tr_two.py`.

Restructure the code:

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"The result is {result}")
except ValueError:
    print("Invalid input! Enter a valid number.")

print("Program ends here")
print("Happy coding")
```

**What changed:**

* The risky code (input, conversion, division, result printing) is now inside a `try:` block.
* An `except ValueError:` block handles the specific case of non-integer input.
* The two closing `print` statements remain **outside** both blocks — they always execute.

⚠️ **Indentation is critical.** Everything inside `try:` must be indented one level. The `except` keyword must be at the same indentation level as `try`.

**Test run 1 — Normal input (`2`):**

```
Enter a number: 2
The result is 5.0
Program ends here
Happy coding
```

✅ `try` succeeds → `except` skipped → closing prints execute.

**Test run 2 — String input (`abc`):**

```
Enter a number: abc
Invalid input! Enter a valid number.
Program ends here
Happy coding
```

✅ `try` fails with ValueError → `except ValueError` catches it → prints friendly message → closing prints execute. **No crash.**

**But there's still a problem.** If you enter `0`, the program still crashes with `ZeroDivisionError` — because we only catch `ValueError`, not `ZeroDivisionError`.

***

## Step 4: Add the else Block — `tr_three.py`

Copy `tr_two.py` → paste → rename to `tr_three.py`.

The problem with `tr_two.py`: the `print(f"The result is {result}")` is inside the `try` block. If the `try` fails, `result` is never defined. If we move the print **outside** the try/except, it runs even after a failure and crashes with `NameError` because `result` doesn't exist.

Solution: use the **`else` block** — code that runs **only when `try` succeeds**:

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
except ValueError:
    print("Invalid input! Enter a valid number.")
else:
    print(f"The result is {result}")

print("Program ends here")
print("Happy coding")
```

**Execution flow:**

* If `try` succeeds → `except` skipped → `else` runs (prints result) → closing prints run.
* If `try` fails (ValueError) → `except` runs → `else` skipped → closing prints run.

**Test run — Input `4`:**

```
Enter a number: 4
The result is 2.5
Program ends here
Happy coding
```

✅ `try` succeeds → `else` executes → result printed correctly.

**Test run — Input `0`:**

```
Enter a number: 0
ZeroDivisionError: division by zero
```

❌ Still crashes — `ZeroDivisionError` is not caught yet.

***

## Step 5: Add Multiple Exception Handlers + Generic Catch — `tr_four.py`

Copy `tr_three.py` → paste → rename to `tr_four.py`.

Add handlers for `ZeroDivisionError` and a generic `Exception` catch-all:

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
except ValueError:
    print("Invalid input! Enter a valid number.")
except ZeroDivisionError:
    print("Cannot divide a number by zero.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print(f"The result is {result}")

print("Program ends here")
print("Happy coding")
```

**What changed:**

* Added `except ZeroDivisionError:` — catches division by zero specifically.
* Added `except Exception as e:` — catches **any other** exception not already handled. The `as e` captures the exception object; `{e}` in the f-string prints the error message.
* The `else` block still only runs on success.

**Test run — Input `0`:**

```
Enter a number: 0
Cannot divide a number by zero.
Program ends here
Happy coding
```

✅ `ZeroDivisionError` caught → friendly message → program continues.

**Test run — Input `abc`:**

```
Enter a number: abc
Invalid input! Enter a valid number.
Program ends here
Happy coding
```

✅ `ValueError` caught.

**Test run — Input `5`:**

```
Enter a number: 5
The result is 2.0
Program ends here
Happy coding
```

✅ No exception → `else` executes.

**The generic `Exception as e` block:** The instructor notes that for this simple program, it's hard to trigger an exception that isn't `ValueError` or `ZeroDivisionError`. He suggests taking the code to ChatGPT and asking: *"What user input should I take so it enters into the `except Exception as e` block?"* — a useful exercise for exploring edge cases.

**Common mistakes:**

| Mistake                                            | Symptom                                                              | Fix                                                                                                                            |
| -------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Wrong indentation in `try` block                   | `IndentationError`                                                   | Use consistent tab/4-space indentation inside `try`                                                                            |
| Misspelling exception type (`ValueEror`)           | `NameError` at the `except` line itself                              | Check exact spelling of exception class names                                                                                  |
| Putting result-dependent code outside `else`       | `NameError: result is not defined` when exception occurs             | Move success-dependent code into `else` block                                                                                  |
| Using `accept` instead of `except`                 | `SyntaxError`                                                        | The keyword is `except` (the instructor humorously notes his own struggle: *"I always had this problem of accept and expect"*) |
| Ordering generic `Exception` before specific types | Generic catch intercepts everything; specific handlers never trigger | Always put specific exceptions **before** the generic `Exception` catch                                                        |

> ⚠️ **Expert Note:** The `except` blocks are checked **in order**. If you place `except Exception as e` before `except ValueError`, the generic handler catches the `ValueError` first, and the specific handler never executes. Always order from **most specific** to **most generic**.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Exception Handling Flow Architecture

```
            ┌───────────────┐
            │   try: block  │ ← risky code goes here
            └───────┬───────┘
                    │
            ┌───────▼───────┐
            │  Exception?   │
            └───┬───────┬───┘
                │       │
              NO │       │ YES
                │       │
                │       ▼
                │  ┌─────────────────┐
                │  │ except Handler  │ ← match specific type first
                │  │  ValueError?    │──→ handle
                │  │  ZeroDivError?  │──→ handle
                │  │  Exception?     │──→ catch-all
                │  └────────┬────────┘
                │           │
                ▼           │
          ┌──────────┐      │
          │  else:   │      │ (else is SKIPPED on exception)
          │ (success │      │
          │  only)   │      │
          └────┬─────┘      │
               │            │
               ▼            ▼
        ┌──────────────────────┐
        │ Code after all blocks │ ← ALWAYS executes
        └──────────────────────┘
```

***

## Progressive File Evolution

```
tr_one.py    →  NO handling          →  crashes on bad input
tr_two.py    →  try/except ValueError →  handles strings, still crashes on zero
tr_three.py  →  + else block          →  result printing only on success; zero still crashes
tr_four.py   →  + ZeroDivisionError   →  handles zero
             →  + Exception as e      →  catches anything unexpected
             →  FULLY ROBUST
```

***

## try/except/else Execution Logic

```
SUCCESS PATH:     try ✅ → except SKIPPED → else RUNS → post-block RUNS
EXCEPTION PATH:   try ❌ → except RUNS    → else SKIPPED → post-block RUNS

Key insight: post-block code ALWAYS runs (unless program exits)
```

***

## Exception Handler Ordering Rule

```
except ValueError:           ← most specific FIRST
except ZeroDivisionError:    ← specific
except Exception as e:       ← generic catch-all LAST

⚠️ WRONG ORDER: generic first → specific handlers never trigger
```

***

## Exception Types Encountered / Referenced

```
ValueError           →  int("abc") — invalid value for conversion
ZeroDivisionError    →  10 / 0 — division by zero
NameError            →  using undefined variable (result before assignment)
ArithmeticError      →  parent of math errors
ImportError          →  failed module import
KeyError             →  missing dictionary key
KeyboardInterrupt    →  user Ctrl+C
MemoryError          →  out of memory
FloatingPointError   →  float operation failure
Exception            →  base class — catches (almost) all
```

***

## `as e` Pattern — Capturing Error Details

```
except Exception as e:
    print(f"An unexpected error occurred: {e}")

"as e"  →  stores exception object in variable e
"{e}"   →  prints the error message string
USE:    →  logging, debugging, user feedback
```

***

## The Base Program Structure

```python
# THE PATTERN (tr_four.py — final form)
try:
    number = int(input("Enter a number: "))    # ← can raise ValueError
    result = 10 / number                        # ← can raise ZeroDivisionError
except ValueError:
    print("Invalid input! Enter a valid number.")
except ZeroDivisionError:
    print("Cannot divide a number by zero.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print(f"The result is {result}")            # ← only if try succeeded

print("Program ends here")                      # ← always runs
print("Happy coding")                           # ← always runs
```

***

## Why else Exists — The NameError Trap

```
WITHOUT else:
  try fails → result never assigned → print(result) outside try → NameError crash

WITH else:
  try fails → except runs → else SKIPPED → print(result) never attempted → no crash
  try succeeds → result exists → else runs print(result) → works correctly
```

***

## Common Pitfall Index

```
"accept" instead of "except"              →  SyntaxError (keyword is "except")
Generic Exception before specific types   →  specific handlers never trigger
Result-dependent code outside else        →  NameError when try fails
Unhandled exception type                  →  program still crashes for that type
Forgetting indentation inside try         →  IndentationError
```

***

## Reusable Engineering Pattern: Defensive Execution with Layered Recovery

```
PATTERN:
  1. ATTEMPT the risky operation              (try)
  2. Handle KNOWN failure modes specifically   (except Type1, except Type2)
  3. Handle UNKNOWN failures generically       (except Exception as e)
  4. Execute success-dependent logic safely    (else)
  5. Execute cleanup/continuation always       (code after blocks)

WHY:
  Programs must not crash silently in automation
  Different failures need different responses
  Unknown failures need graceful degradation, not termination

WHERE ELSE:
  • API calls with retry logic on timeout
  • File operations with fallback on permission denied
  • Cloud automation with rollback on provisioning failure
  • Database operations with transaction rollback on error
  • Any unattended script that must keep running
```

***

## Automation Context (Bridge to Next Lecture)

```
Exception handling → PREREQUISITE for reliable automation
  "Things can fail, it will fail" → must handle gracefully
  except blocks can: print messages, retry, call alternative functions,
                     log errors, trigger alerts, execute rollback

Next lecture: Cloud automation with Python → exception handling becomes operational
```

***

## One-Line Mental Reload Trigger

> *"try the risky code, except catches specific errors (ValueError, ZeroDivisionError) then generic Exception as e, else runs only on success, code after blocks always runs — order specific-to-generic, else prevents NameError on unassigned result."*

This single sentence reconstructs the full block structure, ordering rule, the else rationale, and the key pitfall that motivated the progressive file evolution. [\[216-except...n-handling \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/216-exception-handling.txt)
