# 🎓 Deep Learning Material: Python Conditions — if/elif/else Decision Making and Data Structure Membership Checks

**Source:** Video lecture on Python conditions and decision making (from [207-conditions.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt?EntityRepresentationId=f162933d-eade-462d-9a5e-2cc7c4755790) caption file) [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Video Context:** This lecture introduces Python's conditional logic (`if`, `elif`, `else`) — drawing a direct parallel to Bash scripting conditions the learner already knows. The instructor starts with simple integer comparisons to establish syntax, then builds toward a comprehensive interactive program that combines **all previously learned data types** (lists, tuples, dictionaries) with **membership operators** and **logical operators** inside conditional blocks. The second program is the lecture's real payload — it's a synthesis exercise that tests whether the learner can integrate conditions with data structures, user input, and operators into a working program.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Conditional Logic in Python: The Same Concept, Different Syntax

The instructor frames Python conditions against prior knowledge: *"It's similar as what you see in the Bash scripting conditions. If this is true, then execute the code. Else execute something else. Or we can have elseif also."* The logic is identical to Bash — the only difference is syntax. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

In Bash, you write `if [ condition ]; then ... elif [ condition ]; then ... else ... fi`. In Python, you write `if condition:` followed by an indented block, `elif condition:` for additional checks, and `else:` for the fallback. The structural elements map one-to-one; the syntax is cleaner in Python.

***

## 1.2 — The `if` Statement: Syntax and Indentation

The most basic conditional structure in Python is the `if` statement. You write the keyword `if`, followed by a **condition expression** (e.g., `x < 30`), followed by a **colon** (`:`). The code that should execute when the condition is true goes on the **next line, indented**. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

The instructor emphasizes the colon: *"make sure you give that colon there at the end."* The colon is mandatory — it signals the start of the conditional block. Without it, Python raises a syntax error.

**Indentation** is not optional in Python — it's how Python knows which lines belong to the `if` block. The instructor notes that PyCharm (the IDE) automatically provides the indentation: *"If you're using PyCharm, it should automatically give you the space."* If using another editor, you manually indent (typically 4 spaces or 1 tab). [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

When the condition is **true**, all indented lines under the `if` execute. When the condition is **false**, the indented block is skipped entirely, and execution continues with the **next non-indented line** — what the instructor calls *"the rest of the code."* The instructor demonstrates this by changing `x` from `21` (condition true → both prints execute) to `31` (condition false → block skipped, only the non-indented print runs). [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 1.3 — The `if-else` Statement: Two-Path Decision

When you want to execute one block if the condition is true and a **different block** if the condition is false, you add `else:` after the `if` block. The `else` has its own colon and its own indented block. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

```python
x = 31
if x < 30:
    print("x is less than 30")
else:
    print("x is NOT less than 30")
```

The instructor sets `x = 31` and the condition `x < 30` is false, so the `else` block executes. This is straightforward two-path branching. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 1.4 — The `if-elif-else` Statement: Multi-Path Decision and the Gap Problem

When you have more than two possible outcomes, `if-else` is insufficient. The instructor demonstrates this with a value of `x = 40` and conditions checking `x > 40` and `x < 40`. Both are false when `x` equals exactly 40. With only `if-else`, the code incorrectly falls into the `else` block and prints `"x is less than 40"` — which is logically wrong. The instructor catches this: *"code is syntactically right, but logically it's wrong. It is saying X is less than 40. That's not true. X is equal to 40."* [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

The fix is `elif` (else-if), which adds an additional condition check between `if` and `else`:

```python
x = 40
if x > 40:
    print("x is greater than 40")
elif x == 40:
    print("x is equal to 40")
else:
    print("x is less than 40")
```

Now all three cases are covered: greater than, equal to, and less than. The `elif` provides the missing middle path. You can chain as many `elif` blocks as needed. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

This demonstrates an important engineering principle: **syntactically correct code can be logically wrong**. The program runs without errors but produces incorrect output. The instructor deliberately shows the bug first, then fixes it — reinforcing that testing with edge cases (boundary values like `40` when comparing against `40`) is essential.

***

## 1.5 — PyCharm Style Guidance: PEP 8 Standards

The instructor briefly encounters a PyCharm style warning about **redundant parentheses** around print arguments. PyCharm highlights this in a yellow/off-white color (not red, which would indicate an error). Right-clicking and selecting "Show context actions" reveals the suggestion: *"remove redundant parenthesis."* This follows **PEP 8** — Python's official style guide. The instructor explains: *"the best practice is the standards in Python eight standards."* [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

The key distinction: yellow/off-white warnings are **style suggestions** (code works but could be cleaner); red highlights are **errors** (code will fail). Both should be addressed, but errors are blocking while style warnings are advisory.

***

## 1.6 — The Synthesis Program: Conditions + Data Structures + Membership Operators + User Input

The second half of the lecture builds a comprehensive interactive program that combines **everything learned so far** — conditions, lists, tuples, dictionaries, membership operators (`in`), logical operators (`or`), the `input()` function, and string formatting. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**The program's architecture:**

The instructor creates an "IT organization skill database" using three data types: [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

* **List** (`DevOps`) — contains strings: `"Jenkins"`, `"Ansible"`, `"Bash"`, etc.
* **Tuple** (`development`) — contains strings: `"NodeJS"`, `"AngularJS"`, `"Java"`, `".Net"`, `"Python"`
* **Two Dictionaries** (`contract_employee` entries) — each with key-value pairs for `skill` and `employee code`

The program takes **user input** via the `input()` function, which displays a prompt and stores the user's typed response into a variable (`user_skill`). [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

The program then uses a **chain of `if-elif-else`** conditions with **membership operators** to check whether the entered skill exists in any of the data structures:

1. `if user_skill in DevOps:` — checks if the skill exists in the list
2. `elif user_skill in development:` — checks if the skill exists in the tuple
3. `elif user_skill in contract_dict1.values() or user_skill in contract_dict2.values():` — checks if the skill exists in either dictionary's values
4. `else:` — skill not found anywhere [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 1.7 — Membership Operators with Different Data Types

The `in` operator works directly on **lists and tuples** — it checks if a value exists in the sequence. The instructor uses it straightforwardly: `user_skill in DevOps` (list) and `user_skill in development` (tuple). [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

For **dictionaries**, `in` by default checks **keys**, not values. But the instructor needs to check values (the skill names are stored as values, not keys). The solution is the `.values()` method: `contract_dict.values()` returns a **view of all values** in the dictionary, which the `in` operator can then search. *"Directly we don't do membership operators to dictionary. So dictionary.values() — that is going to return me list of values."* [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 1.8 — Logical Operators Inside Conditions: Combining Checks

When checking two dictionaries, instead of writing two separate `elif` blocks, the instructor uses the **`or` logical operator** to combine both checks into a single condition:

```python
elif user_skill in contract1.values() or user_skill in contract2.values():
```

*"So I don't need to write two elif. I can just write one elif, right? In that I can just use my logical operator and do the comparison."* [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

The `or` operator returns `True` if **either** operand is `True`. Only if both are `False` does it return `False`. This is a cleaner, more concise way to check multiple data sources in a single condition. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 1.9 — The `input()` Function: Interactive User Input

The `input()` function is Python's built-in mechanism for reading user input from the terminal. You pass a **prompt string** as an argument — this string is displayed to the user. Whatever the user types and confirms with Enter is returned as a **string** and stored in the variable. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

```python
user_skill = input("Enter your desired skill: ")
```

The instructor demonstrates: when the program runs, it pauses at this line, displays the prompt, waits for input, and then continues with the entered value stored in `user_skill`. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 1.10 — Case Sensitivity: A Deliberate Limitation

The program uses **capitalized** skill names in the data structures (`"Jenkins"`, `"Ansible"`, `"Java"`, etc.) and instructs the user to enter values in capitalized form. The instructor acknowledges this is a limitation: *"Sure, this program is not foolproof but it's a good practice for you."* If the user enters `"jenkins"` (lowercase), the membership check fails because Python string comparison is **case-sensitive**. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

The `else` block handles this gracefully by printing: *"Please check if you have entered the value in capitalized."* This is a practical UX consideration — the program tells the user what went wrong rather than silently failing. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 1.11 — String Formatting with `.format()`

The instructor uses the `.format()` method for dynamic output messages:

```python
print("We have {} in DevOps team".format(user_skill))
```

The `{}` is a **placeholder** that gets replaced with the value of `user_skill` at runtime. This produces clean, dynamic output like `"We have Jenkins in DevOps team"` when the user enters `"Jenkins"`. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are building two Python programs. **Program 1** (`conditions.py`) teaches basic `if`, `if-else`, and `if-elif-else` syntax with simple integer comparisons. **Program 2** (`conditions_variables.py`) is a comprehensive interactive program that combines conditions with lists, tuples, dictionaries, membership operators, logical operators, user input, and string formatting — synthesizing all previously learned Python concepts. The final outcome: you can write conditional logic that queries different data structures and provides meaningful responses to user input.

***

## Program 1: Basic Conditions (`conditions.py`)

### Step 1: Simple `if` Statement

**Create a new file** called `conditions.py`.

```python
x = 21
if x < 30:
    print("I am inside if block")
    print("Yes, x is less than 30")
print("This is the rest of the code")
```

 [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

* `x = 21` — assigns the value
* `if x < 30:` — condition + colon (mandatory colon)
* Indented lines — execute ONLY if condition is true
* Non-indented line — executes regardless (after the `if` block)

**Run it:**

* **Expected output (x=21):** All three print statements execute (condition is true) [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Change `x = 31` and run again:**

* **Expected output (x=31):** Only `"This is the rest of the code"` prints (condition false, `if` block skipped) [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Common mistake:** Forgetting the colon after the condition → `SyntaxError`. Incorrect indentation → `IndentationError`.

***

### Step 2: `if-else` Statement

```python
x = 31
if x < 30:
    print("x is less than 30")
else:
    print("x is NOT less than 30")
```

 [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Run it (x=31):** Condition is false → `else` block executes → prints `"x is NOT less than 30"` [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

### Step 3: `if-elif-else` Statement (The Bug-First Approach)

**First, write the buggy version (without `elif`):**

```python
x = 40
if x > 40:
    print("x is greater than 40")
else:
    print("x is less than 40")
```

**Run it (x=40):** Prints `"x is less than 40"` — **WRONG**. x equals 40, it's not less than 40. The code is syntactically valid but logically incorrect. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Fix with `elif`:**

```python
x = 40
if x > 40:
    print("x is greater than 40")
elif x == 40:
    print("x is equal to 40")
else:
    print("x is less than 40")
```

**Run it (x=40):** Prints `"x is equal to 40"` — **CORRECT**. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Key learning:** Always test with boundary values (the exact threshold value) to catch logic gaps.

***

## Program 2: Interactive Skill Checker (`conditions_variables.py`)

### Step 4: Set Up the Data Structures

**Create a new file** called `conditions_variables.py`.

```python
print("IT organization has various skill sets")
print("Find out your match")
print("Enter the value in CAPITALIZED")
```

 [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Define the data structures:**

```python
# List
DevOps = ["Jenkins", "Ansible", "Bash", ...]

# Tuple
development = ("NodeJS", "AngularJS", "Java", ".Net", "Python")

# Dictionaries
contract1 = {"skill": "Rocky_skill", "code": "employee_code"}
contract2 = {"skill": "AI", "code": "employee_code"}
```

 [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

* **List** for DevOps skills — mutable, ordered
* **Tuple** for development skills — immutable, ordered
* **Dictionaries** for contract employees — key-value pairs (skill + employee code)

***

### Step 5: Take User Input

```python
user_skill = input("Enter your desired skill: ")
```

* `input()` — pauses execution, displays the prompt string, waits for user to type and press Enter
* The entered text is stored as a **string** in `user_skill` [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Test:** Run the program → it prompts → type anything → it stores the value. Add `print(user_skill)` temporarily to verify. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

### Step 6: Build the Conditional Check Chain

```python
# Check in the database
if user_skill in DevOps:
    print("We have {} in DevOps team".format(user_skill))
elif user_skill in development:
    print("We have {} in Development team".format(user_skill))
elif user_skill in contract1.values() or user_skill in contract2.values():
    print("We have contract employee with {} skill".format(user_skill))
else:
    print("Skill not found")
    print("Please check if you have entered the value in CAPITALIZED")
```

 [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Breakdown of each condition:**

| Condition                                                    | Data Type         | Operator          | What It Checks                              |
| ------------------------------------------------------------ | ----------------- | ----------------- | ------------------------------------------- |
| `user_skill in DevOps`                                       | List              | `in` (membership) | Is the skill in the DevOps list?            |
| `user_skill in development`                                  | Tuple             | `in` (membership) | Is the skill in the development tuple?      |
| `user_skill in contract1.values() or ... contract2.values()` | Dictionary values | `in` + `or`       | Is the skill in either dictionary's values? |
| `else`                                                       | —                 | —                 | None of the above matched                   |

**Why `.values()` on dictionaries:** The `in` operator checks **keys** by default on dictionaries. To check values, you must call `.values()` to get a view of all values, then apply `in` to that view. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Why `or` instead of two `elif`s:** Both dictionary checks are combined with the logical `or` operator — if either returns `True`, the entire condition is `True`. This avoids redundant `elif` blocks. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

### Step 7: Test with Multiple Inputs

**Run the program multiple times with different inputs:** [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

| Input     | Expected Result                             | Why                            |
| --------- | ------------------------------------------- | ------------------------------ |
| `Jenkins` | "We have Jenkins in DevOps team"            | Found in the DevOps list       |
| `Python`  | "We have Python in Development team"        | Found in the development tuple |
| `Java`    | "We have Java in Development team"          | Found in the development tuple |
| `AI`      | "We have contract employee with AI skill"   | Found in dictionary values     |
| `IoT`     | "Skill not found" + capitalization reminder | Not in any data structure      |

 [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

**Note on `Python`:** The instructor observes that Python exists in both the development tuple and potentially could exist elsewhere. The `if-elif` chain stops at the **first match** — since `development` is checked in the second `elif` (after `DevOps`), that's where it matches. The order of conditions matters. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

> ⚠️ **Expert Note**
>
> The program is case-sensitive — entering `"jenkins"` instead of `"Jenkins"` results in "Skill not found." The instructor acknowledges this: *"this program is not foolproof."* In a production version, you would normalize the input with `.upper()` or `.lower()` and store all data in a consistent case. The instructor intentionally leaves this as a learning limitation rather than adding complexity. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Python Conditional Syntax (Complete)

```python
if condition:               # colon mandatory
    # indented block        # runs if true
elif condition:             # optional, multiple allowed
    # indented block        # runs if previous false, this true
else:                       # optional, one only, must be last
    # indented block        # runs if ALL above are false

# non-indented code         # runs regardless (after conditional)
```

***

## 🔷 Bash → Python Mapping

```
BASH                                PYTHON
────────────────────                ────────────────────
if [ condition ]; then              if condition:
elif [ condition ]; then            elif condition:
else                                else:
fi                                  (indentation ends the block)
[ $x -lt 30 ]                      x < 30
== (string)                         == (universal)
```

***

## 🔷 Evaluation Flow

```
if cond1:       ──TRUE──► execute block 1 → SKIP rest → continue after
    │
    FALSE
    ▼
elif cond2:     ──TRUE──► execute block 2 → SKIP rest → continue after
    │
    FALSE
    ▼
elif cond3:     ──TRUE──► execute block 3 → SKIP rest → continue after
    │
    FALSE
    ▼
else:           ────────► execute else block → continue after

FIRST MATCH WINS. Order of conditions matters.
```

***

## 🔷 The Bug-First Teaching Sequence

```
x = 40, conditions: >40 and <40 (no ==40)

if x > 40:   → FALSE
else:         → prints "x < 40" → WRONG (x is 40, not < 40)

FIX: add elif x == 40

LESSON: Syntactically correct ≠ logically correct
        Always test boundary values (threshold == test value)
```

***

## 🔷 Program 2 Architecture (Skill Checker)

```
DATA STRUCTURES:
  DevOps (list)          → ["Jenkins", "Ansible", "Bash", ...]
  development (tuple)    → ("NodeJS", "Java", "Python", ...)
  contract1 (dict)       → {"skill": "...", "code": "..."}
  contract2 (dict)       → {"skill": "AI", "code": "..."}

INPUT:
  user_skill = input("prompt")    → string from user

CHECK CHAIN:
  if user_skill in DevOps          → membership on LIST
  elif user_skill in development   → membership on TUPLE
  elif user_skill in dict.values() → membership on DICT VALUES (.values())
       or ... in dict2.values()    → logical OR combines two dict checks
  else → "not found" + case warning

OUTPUT:
  "We have {skill} in {team}".format(user_skill)
```

***

## 🔷 Membership Operator (`in`) by Data Type

```
DATA TYPE       USAGE                           CHECKS
─────────       ──────────────────────          ────────────
List            value in my_list                items directly
Tuple           value in my_tuple               items directly
Dictionary      value in my_dict                KEYS (default)
Dict values     value in my_dict.values()       VALUES (explicit)
Dict keys       value in my_dict.keys()         KEYS (explicit)
```

***

## 🔷 Key Syntax Rules

```
COLON (:)         → mandatory after if, elif, else
INDENTATION       → defines block membership (4 spaces or 1 tab)
                    wrong indent = IndentationError
PARENTHESES       → NOT needed around conditions (PEP 8: remove if redundant)
input()           → returns STRING always
.format()         → {} placeholder replaced by .format(value)
.values()         → returns dict value view for membership checking
or                → logical OR: True if EITHER operand is True
```

***

## 🔷 Test Results (Quick Reference)

```
INPUT        FOUND IN          RESULT
─────────    ────────────      ──────────────────────
"Jenkins"    DevOps (list)     "We have Jenkins in DevOps team"
"Python"     development (tuple) "We have Python in Development team"
"Java"       development (tuple) "We have Java in Development team"
"AI"         contract dict     "We have contract employee with AI"
"IoT"        NOWHERE           "Skill not found" + case warning
"jenkins"    NOWHERE           "Skill not found" (case-sensitive!)
```

***

## 🔷 Multiline Comments (Used to Disable Code)

```python
"""
This is a multiline comment.
Used to temporarily disable code blocks during testing.
"""
```

The instructor uses this to comment out earlier code while testing new code in the same file. [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)

***

## 🔷 PyCharm Style Warnings

```
RED highlight       → ERROR (code won't run)
YELLOW/off-white    → STYLE WARNING (PEP 8 suggestion, code runs fine)
  → Right-click → Show context actions → apply fix

Example: "Remove redundant parenthesis"
```

***

## 🔷 Reusable Engineering Pattern: Search Across Heterogeneous Data Stores

```
PATTERN: Sequential Search with Early Exit

User input → check store 1 (list)
           → check store 2 (tuple)
           → check store 3+4 (dicts, combined with OR)
           → else: not found

KEY PROPERTIES:
  - First match wins (order defines priority)
  - Different stores may need different access methods
    (direct for list/tuple, .values() for dict)
  - Logical operators combine checks on same-type stores
  - else handles the "not found anywhere" case

This pattern appears in:
  - Configuration resolution (check env var → check config file → check default)
  - Service discovery (check local cache → check DNS → check registry)
  - Authentication (check session → check token → check credentials)
  
The underlying model: ordered fallback search across heterogeneous sources.
```

***

## 🔷 Core Concept Anchor (One-Line Reconstruction)

> **Python conditions use `if/elif/else` with colons and indentation to branch execution, and the `in` operator with `.values()` enables membership checking across lists, tuples, and dictionaries in a unified conditional chain.** [\[207-conditions \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/207-conditions.txt)
