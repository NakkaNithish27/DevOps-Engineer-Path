# 🐍 Python Print Functions & String Formatting — Deep Learning Material

**Source:** *Print Format* (Python Video Lecture Caption File) [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Core Problem — Embedding Variables Inside Printed Text

When you write a `print()` statement in Python, you often need to combine **static text** (strings you write directly) with **dynamic values** (stored in variables). The fundamental challenge is: how do you insert a variable's value into the middle of a sentence? If you write `print("The name of virus is name")`, Python treats the word `name` as literal text — it has no idea you're referring to a variable. It prints the word "name" as a string, not the value stored in the variable `name`. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

Python provides **four distinct methods** to solve this problem, each with different syntax, flexibility, and version requirements. Understanding all four matters because you'll encounter all of them in real codebases, and each has situations where it's the most appropriate choice.

***

## 1.2 Method 1 — Comma Separation in print()

The simplest approach: you pass the string and the variable as **separate arguments** to `print()`, separated by a comma. Python's `print()` function accepts multiple arguments and outputs them separated by a space.

```python
print("The name of virus is", name)
```

The string `"The name of virus is"` is one argument. The variable `name` is a second argument. Python evaluates `name`, gets its value, and prints both pieces with a space between them. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**Limitation:** The variable can only appear **at the end** of the print statement (or between other comma-separated pieces). If you need the variable embedded in the middle of a sentence — say, "**sars\_cov\_2** is the name of the virus" — comma separation becomes awkward because you'd need to split your sentence into multiple fragments. This limitation is what motivates the other methods.

***

## 1.3 Method 2 — The .format() Method

The `.format()` method solves the positional limitation. You write your entire string as a template, placing **curly braces `{}`** wherever you want a variable's value to appear. After the closing quote of the string, you chain `.format()` and pass the variables inside its parentheses. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

```python
print("The name of virus is {} and it causes {}".format(name, disease))
```

Python processes this by **replacing each `{}` placeholder with the corresponding variable from `.format()`**, in order. The first `{}` gets the first argument (`name`), the second `{}` gets the second argument (`disease`), and so on. This means you can place variables **anywhere** in the sentence — beginning, middle, end, or multiple locations — and have as many variables as you need. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

The key engineering insight: `.format()` separates the **template** (the string with placeholders) from the **data** (the variables). The template defines the structure; `.format()` fills in the values. This separation is useful but means you must mentally track which `{}` maps to which variable by counting positions.

***

## 1.4 Method 3 — f-strings (Formatted String Literals)

f-strings are the instructor's preferred method and the most modern approach. You prefix the string with the letter `f`, and then place variables **directly inside the curly braces** within the string itself. No `.format()` call, no external variable list — the variable name goes right where its value should appear. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

```python
print(f"{name} is the name of the virus and it causes {disease}")
```

Python evaluates the expressions inside `{}` at runtime and substitutes their values directly. This is the most readable approach because you see exactly what goes where — there's no positional counting, no external mapping. The template and the data are unified in one place. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**Critical version constraint:** f-strings work **only in Python 3.6 and higher**. If you're running Python 3.5 or earlier, this syntax does not exist and will produce a syntax error. The instructor explicitly warns about this. In real-world scenarios, most modern environments run Python 3.6+, but if you encounter legacy systems or older Docker images with Python 3.5, you must fall back to `.format()` or comma separation. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

***

## 1.5 Method 4 — String Concatenation with the `+` Operator

Concatenation uses the **arithmetic `+` operator** repurposed for strings. When `+` is applied between two strings, it **joins** them into a single string — no space added, no separator, just raw joining. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

```python
print("The name of virus is" + " " + name)
```

Here, three strings are concatenated: `"The name of virus is"`, `" "` (an explicit space), and the variable `name`. The `+` operator combines them left to right into one continuous string.

**Important detail:** Because `+` does not add spaces automatically (unlike comma separation in `print()`), you must manually include spaces as separate string fragments. If you forget the `" "` in the example above, the output would be `"The name of virus issars_cov_2"` — the words run together. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

⚠️ **Expert Note:**
Concatenation with `+` only works when **all operands are strings**. If `name` were an integer, `print("Value is " + name)` would raise a `TypeError`. You'd need `print("Value is " + str(name))`. The other three methods (comma, `.format()`, f-strings) handle type conversion automatically. This is a common source of bugs when using concatenation with mixed types.

***

## 1.6 Comparing the Four Methods — When to Use Which

The instructor demonstrates all four methods and positions them on a spectrum of flexibility and readability: [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

| Method              | Variable Placement     | Multiple Variables | Readability                        | Version Requirement |
| ------------------- | ---------------------- | ------------------ | ---------------------------------- | ------------------- |
| Comma separation    | End only (practically) | Awkward            | Simple but limited                 | All Python versions |
| `.format()`         | Anywhere (`{}`)        | Clean, ordered     | Good — template/data separated     | Python 2.6+         |
| f-string            | Anywhere (`{var}`)     | Clean, inline      | Best — variable visible in context | Python 3.6+         |
| Concatenation (`+`) | Anywhere               | Manual, verbose    | Lowest for complex strings         | All Python versions |

The instructor's stated preference: **f-strings** ("I frankly like this new way, which is much easier"). The recommendation is: if you're on Python 3.6+, use f-strings. They're the most readable, the most concise, and the least error-prone for multi-variable scenarios. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating a Python script that demonstrates all four methods of printing variables within strings. The script uses two variables (`name` and `disease`) and prints them using comma separation, `.format()`, f-strings, and concatenation. After this, you'll be able to choose the appropriate method for any situation and understand existing code that uses any of these patterns. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

***

## Step 1: Create the Script and Define Variables

Create a new Python script file:

```
printing.py
```

Define two variables at the top:

```python
name = "sars_cov_2"
disease = "covid-19"
```

These are the dynamic values we'll embed into printed text using each method. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

***

## Step 2: Comma Separation

```python
print("The name of virus is", name)
```

* `"The name of virus is"` — a string literal (first argument to `print()`)
* `,` — separates arguments; `print()` outputs them with a space between
* `name` — the variable (second argument); Python substitutes its value

**Expected output:** `The name of virus is sars_cov_2`

**What to notice:** The space between "is" and "sars\_cov\_2" is automatically inserted by `print()` because comma-separated arguments are joined with spaces by default. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**Limitation to observe:** The variable is at the end. If you wanted the variable at the beginning of the sentence, you'd need to restructure the arguments.

***

## Step 3: .format() — Single Variable

```python
print("The name of virus is {}".format(name))
```

* `"The name of virus is {}"` — string template with one placeholder (`{}`)
* `.format(name)` — chained method call; replaces `{}` with the value of `name`

**Expected output:** `The name of virus is sars_cov_2` [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**Now demonstrate variable placement flexibility:**

```python
print("{} is the name of the virus".format(name))
```

The `{}` is at the beginning of the sentence. `.format()` replaces it regardless of position.

**Expected output:** `sars_cov_2 is the name of the virus` [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

***

## Step 4: .format() — Multiple Variables

```python
print("The name of virus is {} and it causes {}".format(name, disease))
```

* First `{}` → replaced by `name` (first argument in `.format()`)
* Second `{}` → replaced by `disease` (second argument in `.format()`)

**Expected output:** `The name of virus is sars_cov_2 and it causes covid-19` [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**Common mistake:** Getting the variable order wrong in `.format()`. The replacement is strictly **positional** — first `{}` maps to first argument, second to second, etc. If you swap `name` and `disease` in the `.format()` call, the output reverses.

***

## Step 5: f-string — The Preferred Method

```python
print(f"{name} is the name of the virus and it causes {disease}")
```

* `f` — prefix before the opening quote, marking this as a formatted string literal
* `{name}` — variable name directly inside curly braces; Python evaluates and substitutes at runtime
* `{disease}` — second variable, also inline

**Expected output:** `sars_cov_2 is the name of the virus and it causes covid-19` [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**What to verify:** This produces the same output as the `.format()` version. Both methods are functionally equivalent — f-strings are just syntactically cleaner.

**Version check:** If this produces a `SyntaxError`, your Python version is below 3.6. Check with `python --version` or `python3 --version`. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

***

## Step 6: String Concatenation with +

```python
print("The name of virus is" + " " + name)
```

* `"The name of virus is"` — first string
* `+` — concatenation operator (joins strings)
* `" "` — explicit space (concatenation does NOT auto-add spaces)
* `+` — second concatenation
* `name` — variable whose value is joined to the end

**Expected output:** `The name of virus is sars_cov_2` [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**Common mistake:** Forgetting the explicit space `" "`. Without it:

```python
print("The name of virus is" + name)
```

**Output:** `The name of virus issars_cov_2` — no space between "is" and the variable value.

**Another common mistake:** Trying to concatenate a non-string variable (e.g., an integer) — this raises a `TypeError`. Use `str()` to convert first, or switch to a different method.

***

## Step 7: Run the Complete Script

Save `printing.py` and run it:

```bash
python printing.py
```

(or `python3 printing.py` depending on your system)

All print statements execute in order. Compare the outputs — they should all correctly embed the variable values into the text, just using different syntax. [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)

**The instructor's closing advice:** "Find your own variables, write your own print statement and get hold of this." Practice is essential — create your own variables and try all four methods to internalize the syntax differences.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## The Core Problem

```
Variable inside a string → Python treats variable name as literal text
Need: mechanism to EVALUATE variable and INSERT its value into text
Four solutions → increasing flexibility and readability
```

## Four Methods — Quick Reference

```
1. COMMA SEPARATION
   print("text", variable)
   Space auto-added | Variable at end only | All Python versions

2. .format()
   print("text {} more {}".format(var1, var2))
   {} = placeholder | Positional mapping | Variable anywhere | Python 2.6+

3. f-STRING ⭐ (preferred)
   print(f"text {var1} more {var2}")
   Variable inline in {} | Most readable | Python 3.6+ ONLY

4. CONCATENATION (+)
   print("text" + " " + variable)
   Manual space required | Strings only (TypeError on int) | All versions
```

## Method Selection Decision

```
Python 3.6+?
  ├─ YES → use f-string (cleanest, most readable)
  └─ NO  → use .format() (flexible, works on older versions)

Simple single variable at end?
  → comma separation is fine

Need to join raw strings?
  → concatenation (but watch for missing spaces and type errors)
```

## .format() Mechanics

```
"A {} B {} C".format(x, y)
     ↑          ↑
     1st {}  →  x (1st arg)
     2nd {}  →  y (2nd arg)

Positional: order of {} matches order of .format() arguments
```

## f-string Mechanics

```
f"A {x} B {y} C"
     ↑      ↑
     evaluates x    evaluates y
     inline          inline

No external mapping — variable name IS the placeholder
```

## Concatenation Gotchas

```
"text" + variable     → works ONLY if variable is string
"text" + int_variable → TypeError (must use str(int_variable))
"text" + variable     → NO auto-space (must add " " manually)
```

## Version Constraint

```
f-strings: Python 3.6+ ONLY
  < 3.6 → SyntaxError
  Fix: fall back to .format()
```

## Variables Used in Demo

```
name = "sars_cov_2"
disease = "covid-19"
Script file: printing.py
```

## Reusable Pattern

**Template vs. Inline Data Injection**

```
.format() = template + external data
  → template: "text {} text {}"
  → data: .format(var1, var2)
  → separation of structure and values

f-string = inline data injection
  → f"text {var1} text {var2}"
  → structure and values unified

Same pattern in other systems:
  SQL prepared statements (template + params)
  Jinja2 templates (template + variables)
  String interpolation in Bash ($variable), Ruby (#{variable})
```

***

*This completes the full reconstruction. Theory explains why each method exists and when to use it. Practical walks through every syntax variant with exact code. The Compression Map enables instant recall of all four methods, their constraints, and the decision logic for choosing between them.* [\[204-print-format \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/204-print-format.txt)
