# Python Modules — Creating and Using Custom Modules

**Source:** Video caption file — *"Modules"* (from a Python for DevOps course) [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is a Module?

A module in Python is simply a **Python script** (a `.py` file) or a **package** that contains functions (also called methods) that you can reuse. Instead of writing the same functions in every script where you need them, you write them once in a module and **import** them wherever they're needed. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

Python comes with many built-in modules. The video uses `random` as the example — `random` is a module that already exists in Python's standard library. When you write `import random`, you load that module into your script, and then you can call its methods like `random.randint()` (generates a random integer) or `random.choice()` (picks a random element from a collection). The pattern is always `module_name.method_name()` — the dot notation connects the module to the specific function you want to use. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## 1.2 — Why Create Your Own Modules?

The built-in modules solve common programming needs, but in real work you will have **your own functions that you use regularly** — functions specific to your project, your automation scripts, your infrastructure tooling. Writing these functions inside every script that needs them creates duplication, makes maintenance harder, and increases the chance of inconsistency. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

The solution is to put your reusable functions into a module — a separate Python file — and import them wherever needed. The video states this directly: "When you have some functions which you regularly use, it's better you put them into modules or a module and then whenever you need it, you can import those modules and call the methods." [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

This is the **separation of definition from execution** pattern: one file defines the functions (the module), another file calls them (the caller). The module becomes a reusable library that any script can import. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## 1.3 — The Structure of a Custom Module

Creating a custom module is remarkably simple — it is just a regular Python script file containing function definitions. There is no special syntax, no registration, no configuration. You create a `.py` file, write your functions in it, and that file **is** a module. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

In the video, the module file is named `modern.py`. It contains several functions that were written in previous lectures (like `order_food`, `vaccine_feedback`, and a variable-length argument function), plus an `import random` statement at the top (because one of the functions uses the `random` module internally). [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

The critical rule: the module file contains **only function definitions** — you do **not** call the functions from within the module file itself. The video explicitly demonstrates this: "I'm not calling the function from here itself. I'm going to call it from a different script, a different program." If you included function calls in the module file, those calls would execute every time any script imports the module — which is almost never what you want. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

🔍 **Deep Dive:**
The module file name becomes the module's import name, but **without the `.py` extension**. The file is `modern.py`, but you import it as `import modern` — not `import modern.py`. Python automatically looks for a file named `modern.py` in the same directory (and in other locations on the Python path). The file name must also follow Python naming rules: no hyphens (the video explicitly says "no hyphen, nothing, just the name"), no spaces, and it shouldn't conflict with existing Python module names. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## 1.4 — Two Import Styles and Their Behavioral Differences

Python provides two distinct ways to import from a module, and they affect how you call the functions. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

### Style 1: `import module_name`

```python
import modern
```

This loads the entire module. To call any function, you must use the **fully qualified name**: `modern.order_food(...)`, `modern.vaccine_feedback(...)`. The module name acts as a namespace — it prefixes every function call. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

### Style 2: `from module_name import ...`

```python
from modern import order_food     # import one specific function
from modern import *               # import ALL functions
```

With this style, the functions are loaded directly into the current script's namespace. You call them **directly by name**: `order_food(...)` — no module prefix needed. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

The `*` (star) variant imports everything from the module. The video states: "All your functions will be loaded in the memory." This is the most convenient for calling but loads all functions regardless of whether you need them all. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

The video summarizes both approaches: "Either you say import the module name, then you say dot and the function name. Or you can say from modern import a particular function or all the functions like star. Then calling becomes easy — you just give the name of the method." [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

⚠️ **Expert Note:**
In production scripts and larger projects, `import *` is generally discouraged because it makes it unclear where functions come from — if you import `*` from three different modules, and all three have a function called `process()`, you get silent name collisions. The explicit `import module_name` or `from module import specific_function` styles are preferred because they make dependencies clear and avoid namespace pollution. For small DevOps utility scripts, `import *` is often acceptable due to limited scope. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## 1.5 — The `dir()` Function: Discovering What's Inside a Module

When you import a module, you might not remember all the functions it contains. The `dir()` function solves this — pass a module to `dir()` and it returns a list of everything available in that module. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

```python
import modern
print(dir(modern))
```

The output includes both built-in attributes (like `__doc__`, `__file__`, `__name__`, `__package__`, `__spec__` — these are Python internal metadata about the module) and your custom functions (`order_food`, `time_activity`, `vaccine_feedback`). [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

The built-in attributes provide useful information: `__file__` returns the file path of the module, `__name__` returns the module name, `__doc__` returns the module's docstring if one exists. But for practical purposes, the custom functions are what you care about — `dir()` lets you discover them without opening the module file. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## 1.6 — Module as a Reusability and Organization Pattern

The module concept implements a fundamental software engineering principle: **write once, use everywhere**. Functions that embody reusable logic are centralized in module files. Any script that needs that logic imports the module rather than rewriting the functions. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

This pattern maps directly to real DevOps work:

* You might have a module of AWS utility functions (creating instances, tagging resources, checking statuses).
* You might have a module of notification functions (sending Slack messages, email alerts).
* You might have a module of parsing functions (reading config files, extracting values from JSON/YAML).

Each caller script imports only what it needs. If a function needs to be updated (bug fix, new feature), you change it in one place (the module), and every script that imports it gets the updated version. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a custom Python module containing reusable functions, then writing separate caller scripts that import and use those functions via two different import styles. The final outcome: a module file (`modern.py`) that serves as a reusable function library, and two caller scripts (`caller.py` and `call_modern_two.py`) that demonstrate both import patterns. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Execution Flow Overview

```
Step 1: Create the module file (modern.py) with function definitions
Step 2: Create caller script using "import module_name" style
Step 3: Discover module contents with dir()
Step 4: Call functions using module.function() syntax
Step 5: Create second caller script using "from module import *" style
Step 6: Call functions directly by name (no prefix)
```

***

### Step 1: Create the Module File — `modern.py`

**What we are doing:** Creating a Python file that will serve as our custom module.

**Execution:**

1. Create a new Python file. Name it `modern.py`.
   * **Important:** No hyphens in the filename. No spaces. Just the name. The filename (minus `.py`) becomes the import name. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

2. Move your reusable function definitions into this file. The video transfers functions written in previous lectures: `order_food`, `vaccine_feedback`, and a variable-length argument function.

3. If any of your functions depend on other modules (e.g., one function uses `random`), add the `import random` statement at the top of `modern.py`. The module must import its own dependencies. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

4. **Do NOT include any function calls in this file.** Only function definitions (`def function_name():` blocks). No `order_food("pizza")` at the bottom. The module file defines; the caller file executes. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**How to verify:** The file should contain only `import` statements and `def` blocks. No standalone function calls.

**Common mistake:** Including function calls in the module file. If you do, those calls execute every time any script does `import modern`, causing unintended side effects. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**Connection to flow:** This module is now ready to be imported by any script in the same directory.

***

### Step 2: Create Caller Script — `caller.py` (Import Style 1)

**What we are doing:** Writing a script that imports the entire module and calls its functions using the `module.function()` syntax.

**Execution:**

1. Create a new Python file named `caller.py` (or any name — the video notes "name it anything" but suggests avoiding names that conflict with existing modules). [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

2. At the top, import the module:

```python
import modern
```

**Breakdown:** `import` is the keyword. `modern` is the module name — this matches the filename `modern.py` **without** the `.py` extension. Never write `import modern.py`. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**What happens internally:** Python finds `modern.py` in the same directory, reads it, executes all the `import` statements and `def` blocks inside it (loading function definitions into memory), and makes them available under the namespace `modern`. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

### Step 3: Discover Module Contents with `dir()`

**What we are doing:** Listing all available functions and attributes in the imported module.

```python
print(dir(modern))
```

**Expected output:** A list containing built-in attributes (`__doc__`, `__file__`, `__name__`, `__package__`, `__spec__`) and your custom functions (`order_food`, `time_activity`, `vaccine_feedback`). [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**Why this matters:** When working with unfamiliar modules (your own or third-party), `dir()` is how you discover what's available without reading the source file.

**How to verify:** Your custom function names should appear in the list. If they don't, check that the module file is in the same directory and the function definitions have correct syntax.

***

### Step 4: Call Functions Using `module.function()` Syntax

**What we are doing:** Calling the module's functions by their fully qualified names.

```python
modern.order_food("pizza", "burger", 3)
modern.vaccine_feedback("Covaxin")
modern.time_activity()
```

**Breakdown:** `modern` is the module name (namespace). The dot `.` connects the module to the function. The function name follows, with arguments in parentheses. You pass the same arguments you would if the function were defined locally. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**Expected output:** The functions execute and produce their output — same as if they were defined in this file.

**How to verify:** Run the script and confirm each function produces the expected output.

**Common mistake:** Forgetting the module prefix — writing `order_food(...)` instead of `modern.order_food(...)`. With `import modern`, the prefix is mandatory. Python raises a `NameError` if you omit it. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**IDE hint:** After typing `modern.`, your IDE should show autocomplete suggestions listing all available functions. The video demonstrates this: "You can just type here modern, say dot. It should show you all the functions available in that." [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

### Step 5: Create Second Caller Script — `call_modern_two.py` (Import Style 2)

**What we are doing:** Writing a script that imports functions directly using the `from...import` syntax.

**Execution:**

1. Create a new file named `call_modern_two.py`. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

2. Import using the `from...import *` pattern:

```python
from modern import *
```

**Breakdown:**

* `from modern` — specifies which module to import from.
* `import *` — the asterisk means "import all functions from this module into the current namespace." [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**Alternative (import specific function):**

```python
from modern import order_food
```

This imports only `order_food` — useful when you only need one function and want to keep the namespace clean. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

### Step 6: Call Functions Directly by Name

**What we are doing:** Calling functions without the module prefix.

```python
order_food("pizza", "burger", 3)
```

**Breakdown:** No `modern.` prefix needed. The function was imported directly into this script's namespace by the `from...import` statement. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

**Expected output:** Same as Style 1 — the function executes identically regardless of how it was imported.

**How to verify:** Run the script and confirm the output matches expectations.

**When to use which style:**

* Use `import modern` when you want explicit namespacing and clarity about where each function comes from.
* Use `from modern import *` when you want convenience and the module is small/trusted.
* Use `from modern import specific_function` when you only need one or two functions. [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Python Modules
PURPOSE:  Reusable function organization — write once, import anywhere
CORE IDEA: A module is just a .py file with function definitions
```

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Module Architecture

```
modern.py (MODULE FILE)
  ├── import random            ← module's own dependencies
  ├── def order_food():        ← function definition only
  ├── def vaccine_feedback():  ← function definition only
  └── def time_activity():     ← function definition only
  ⚠️ NO function calls in this file

caller.py (CALLER FILE)
  ├── import modern            ← loads module
  └── modern.order_food(...)   ← calls via namespace

call_modern_two.py (CALLER FILE - Style 2)
  ├── from modern import *     ← loads all functions directly
  └── order_food(...)          ← calls without prefix
```

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Two Import Styles

```
STYLE 1: import module_name
  ├── Loads entire module as namespace
  ├── Call: module_name.function_name()
  ├── Prefix REQUIRED
  └── Clear origin of every function

STYLE 2: from module_name import ...
  ├── from modern import order_food    ← one function
  ├── from modern import *             ← all functions
  ├── Call: function_name()            ← direct, no prefix
  └── Convenient but less explicit

TRADEOFF:
  Style 1 = explicit + safe (clear namespace)
  Style 2 = convenient + concise (risk of name collision with *)
```

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Module Creation Rules

```
1. File name = module name (no .py in import)
   modern.py → import modern

2. No hyphens, no spaces in filename

3. Only function DEFINITIONS in module file
   ✅ def order_food(): ...
   ❌ order_food("pizza")     ← don't call functions in module

4. Module imports its own dependencies
   import random  ← inside modern.py, not in caller

5. Module file must be in same directory as caller
   (or on Python path)
```

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Discovery: `dir()`

```
import modern
print(dir(modern))

OUTPUT:
  Built-in: __doc__, __file__, __name__, __package__, __spec__
  Custom:   order_food, vaccine_feedback, time_activity

USE: Discover available functions without reading source
```

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Execution Flow

```
CALLER SCRIPT runs
    │
    ▼
import modern
    │
    ▼
Python finds modern.py in same directory
    │
    ▼
Reads modern.py:
  ├── Executes import statements (e.g., import random)
  ├── Registers function definitions (def blocks)
  └── Does NOT execute any standalone calls (there shouldn't be any)
    │
    ▼
Functions available via modern.function_name()
    │
    ▼
Caller invokes: modern.order_food("pizza", "burger", 3)
    │
    ▼
Function executes, returns result
```

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Built-in vs. Custom Modules

```
BUILT-IN (already exists):
  import random
  random.randint(1, 10)
  random.choice(["a", "b", "c"])

CUSTOM (you create):
  Create modern.py with def blocks
  import modern
  modern.order_food(...)

SAME PATTERN: import → namespace.method()
```

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## Reusable Engineering Patterns

| Pattern                                     | Manifestation                                                          |
| ------------------------------------------- | ---------------------------------------------------------------------- |
| **Separation of Definition from Execution** | Module file defines functions; caller file executes them               |
| **Write Once, Use Everywhere**              | Functions centralized in module → imported by any script               |
| **Namespace Isolation**                     | `import modern` keeps functions under `modern.` prefix — no collision  |
| **Single Update Point**                     | Fix a function in the module → all callers get the fix                 |
| **Dependency Encapsulation**                | Module imports its own dependencies (e.g., `import random`) internally |
| **Discovery Interface**                     | `dir(module)` reveals available functions without reading source       |

 [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

## One-Line System Reconstruction

> **A Python module is a `.py` file containing only function definitions (no calls), imported by caller scripts either as a namespace (`import modern` → `modern.func()`) or directly (`from modern import *` → `func()`), with `dir()` for discovery — implementing the write-once-use-everywhere pattern that centralizes reusable logic and maps to how DevOps teams organize utility functions across automation scripts.** [\[213-modules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/213-modules.txt)

***

This completes the full reconstruction of the Python Modules lecture. It builds on the functions knowledge from previous lectures and establishes the organizational pattern for scaling Python scripts from single-file utilities to multi-file projects — which is essential as DevOps automation scripts grow in complexity. Let me know if you'd like any section expanded or adjusted! 🚀
