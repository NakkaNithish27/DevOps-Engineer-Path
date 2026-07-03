# Python Variables and Data Types — Foundations for DevOps Automation

**Source:** Video caption file — *"Variables and Data Types"* (from a Python for DevOps course) [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is a Variable and How Does Assignment Work in Python?

A variable in Python is a name that points to a value stored in memory. You create a variable by **assigning** a value to it using the `=` operator. There is no separate declaration step — the moment you write `var1 = "Python"`, the variable `var1` exists and holds the string `"Python"`. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

Python is flexible about spacing around the `=` sign during assignment. All of these are valid:

```python
var1 = "Python"    # space on both sides
var2 =7575         # space only on left
var3= 3.5          # space only on right
```

However, the video explicitly asks: "What looks good?" and answers that **spaces on both sides** (`var1 = "Python"`) is the preferred, readable style. While all forms are syntactically valid, consistent spacing is a readability convention you should follow. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

A critical aspect of Python variables: **you do not declare the type**. You don't say "this is a string variable" or "this is an integer variable." Python automatically determines the type based on the value you assign. This is called **dynamic typing** — the type is inferred from the value, not declared by the programmer. `var1 = "Python"` makes `var1` a string because the value `"Python"` is a string. `var2 = 7575` makes `var2` an integer because `7575` is an integer. `var3 = 3.5` makes `var3` a float because `3.5` has a decimal point. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.2 — The Three Fundamental Scalar Types: String, Integer, Float

These are the basic building-block data types in Python. Every value you work with is one of these (or a more complex type built from them). [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**String** — Text data, enclosed in quotes. Python accepts multiple quoting styles: double quotes (`"text"`), single quotes (`'text'`), triple quotes (`'''text'''`), and triple double quotes (`"""text"""`). All produce strings. Strings hold characters — letters, words, sentences, any textual data.

**Integer** — Whole numbers without a decimal point. `7575`, `65`, `12` — these are all integers. Integers represent counts, quantities, or any numeric value that doesn't require fractional precision.

**Float** — Numbers with a decimal point. `3.5`, `5.4` — these are floats. Floats represent values that need fractional precision (weights, measurements, percentages). [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

The distinction between integer and float matters because they behave differently in calculations and because many systems (JSON, YAML, APIs, databases) treat them as different types. The video uses `type()` to confirm types — `type(var1)` returns `<class 'str'>`, `type(var2)` returns `<class 'int'>`, `type(var3)` returns `<class 'float'>`. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.3 — The `type()` Function: Asking Python What Type a Variable Is

Since Python doesn't require you to declare types, you sometimes need to check what type a variable actually is. The built-in `type()` function does this — you pass a variable into it, and it returns the type. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

```python
print(type(var1))   # <class 'str'>
print(type(var2))   # <class 'int'>
print(type(var3))   # <class 'float'>
```

This is not just a learning exercise — in real DevOps scripts, you frequently receive data from external sources (API responses, configuration files, command output) where the type isn't obvious. Using `type()` helps you verify that the data is what you expect before operating on it. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.4 — Multiple Assignment: Two Patterns

Python supports two forms of assigning multiple variables in a single line. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

### Pattern 1: Chain Assignment (Same Value)

```python
a = b = c = 65
```

The integer `65` is stored in `c`, the value of `c` is stored in `b`, and the value of `b` is stored in `a`. All three variables end up with the same value: `65`. The assignment flows **right to left** — the rightmost value is assigned first, then chained leftward. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

### Pattern 2: Comma-Separated Assignment (Different Values)

```python
x, y, z = "alpha", "beta", 12
```

Here, the comma acts as a **separator**. The first value (`"alpha"`) goes to the first variable (`x`), the second value (`"beta"`) goes to `y`, and the third value (`12`) goes to `z`. Each variable gets its own distinct value. The number of variables on the left must match the number of values on the right. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

Notice that the values can be of **different types** — `x` gets a string, `y` gets a string, `z` gets an integer. Python handles mixed-type multiple assignment without any issue because of dynamic typing.

***

## 1.5 — Printing Variables with Strings

The `print()` function can output both literal strings and variable values in the same statement by separating them with commas. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

```python
print("variable x value is", x)
```

This prints the literal string `"variable x value is"` followed by the current value of `x`. The comma between the string and the variable tells `print()` to output both, separated by a space. This is the simplest way to create labeled output — useful for debugging and verification in scripts. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.6 — List: Mutable Ordered Collection

A **list** is a collection that can hold multiple values of different types, enclosed in **square brackets** `[]`, with elements separated by commas. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

```python
first_list = [str1, "DevOps", num1, 3.5]
```

A list can contain strings, integers, floats, other variables, and even other lists — all mixed together in a single collection. Lists are **ordered** (elements maintain the position you put them in) and **indexed** (you can access elements by their position). [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

The most important characteristic of a list is that it is **mutable** — you can change, add, or remove elements after the list is created. Think of it like a **pen drive**: you can edit, add, or delete the content on a pen drive freely. This mutability is what makes lists the workhorse data structure for dynamic data in Python scripts. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.7 — Tuple: Immutable Ordered Collection

A **tuple** is visually and structurally almost identical to a list — it's an ordered collection of multiple values of different types. The syntax difference: tuples use **round brackets** `()` instead of square brackets. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

```python
my_first_tuple = (str1, "DevOps", num1, 3.5)
```

The critical difference is **immutability**. A tuple, once created, **cannot be edited**. You cannot add elements, remove elements, or change the value of an element at a specific position. You can overwrite the entire tuple variable with a new tuple, but you cannot modify the content of an existing tuple. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

The video uses a memorable analogy: a tuple is like a **CD** — you can't change the content on a CD. A list is like a **pen drive** — you can edit the content freely. "You will say I can overwrite a CD. Well, sure you can overwrite a tuple also, but you can't make the change in the content." [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

🔍 **Deep Dive:**
The distinction between mutability and immutability is not just a theoretical nicety — it has practical consequences. Tuples are used when you want to guarantee that data won't be accidentally modified (configuration constants, fixed coordinate pairs, database record keys). Lists are used when the data needs to change during program execution (accumulating results, building dynamic inventories, processing variable-length input). In Ansible and Terraform, understanding when data is meant to be fixed vs. changeable maps directly to this concept. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.8 — Dictionary: Key-Value Pair Collection

A **dictionary** is a collection of **key-value pairs**, enclosed in **curly braces** `{}`. Each element consists of a key and its associated value, separated by a colon (`:`). Elements are separated by commas. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

```python
first_dict = {"name": "Imran", "weight": 75, "exercises": ["boxing", "dancing", "jogging"]}
```

The analogy is straightforward: like a real dictionary where every word has a meaning, in a Python dictionary every **key** has a **value**. Data is always in pairs. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

Keys are typically strings (like `"name"`, `"weight"`, `"exercises"`), and values can be **any data type** — strings, integers, floats, lists, or even other dictionaries. The video explicitly demonstrates this: `"name"` maps to a string (`"Imran"`), `"weight"` maps to an integer (`75`), and `"exercises"` maps to a **list** (`["boxing", "dancing", "jogging"]`). This nesting — a list inside a dictionary — is extremely common in real-world data structures. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

⚠️ **Expert Note:**
Dictionaries are the single most important data type to master for DevOps work. The video explicitly states: "It's very important for you to understand all these data types because when we get into Ansible and when we see JSON format, YAML format, we'll be seeing strings, we'll be seeing list and we'll be seeing dictionaries there. And they'll have almost same syntax." JSON objects **are** dictionaries. YAML mappings **are** dictionaries. Ansible playbooks, CloudFormation templates, Kubernetes manifests, Terraform configurations — all of them are built on dictionaries (key-value pairs), lists, and strings. If you understand Python's data types deeply, JSON and YAML become immediately readable. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.9 — Boolean: True or False

The final data type covered is **Boolean** — a type that can only hold one of two values: `True` or `False`. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

```python
x = True
y = False
```

Important syntax detail: `True` and `False` must be capitalized (capital T, capital F). No quotes — if you put quotes around them, they become strings, not booleans. `type(x)` returns `<class 'bool'>`. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

Booleans are fundamental to **condition checking** — when you check a condition (is this value greater than that value? is this file present? did this command succeed?), the result is a boolean. Your program logic then branches based on whether the result is `True` or `False`. Every `if` statement, every loop condition, every error check ultimately evaluates to a boolean. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.10 — The Visual Bracket Rule: How to Identify Data Types by Sight

The video provides a powerful visual shortcut for instantly identifying collection types: [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

* **Square brackets** `[]` → List
* **Round brackets** `()` → Tuple
* **Curly braces** `{}` → Dictionary
* **Quotes** (`""`, `''`, `""" """`) → String
* **No quotes, no decimal** → Integer
* **No quotes, has decimal** → Float
* **`True` / `False`** (capitalized, no quotes) → Boolean

This visual identification rule is critical because you will constantly encounter these structures in JSON, YAML, Ansible playbooks, API responses, and configuration files. Being able to instantly recognize the data type by its enclosing syntax is a foundational skill. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## 1.11 — Why This Matters for DevOps: The JSON/YAML Connection

The video makes an explicit and important connection between Python data types and DevOps tooling. The instructor states: "Almost every automation tool today uses JSON or YAML." And then gives specific examples: [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

* **Ansible** playbooks are in YAML format. Ansible output is returned in JSON format.
* **CloudFormation** templates use JSON and YAML.
* New tools and configuration formats are also predominantly YAML-based.

The direct mapping: Python **dictionaries** = JSON **objects** = YAML **mappings**. Python **lists** = JSON **arrays** = YAML **sequences**. Python **strings/integers/floats/booleans** = JSON/YAML **scalar values**. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

"If you understand this, then I can very easily explain you JSON and YAML. And being the DevOps, you should be very good in reading and writing JSON and YAML." This is why the video emphasizes practicing with these data types — they are not just Python concepts, they are the **data structure vocabulary of the entire DevOps ecosystem**. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing Python scripts that demonstrate every fundamental variable type and data type. The final outcome: two scripts — `variables.py` (variable assignments, multiple assignments, type checking) and `data_types.py` (list, tuple, dictionary, boolean). These scripts serve as executable reference material and practice exercises for the data types that underpin all DevOps configuration formats. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## Script 1: `variables.py` — Variable Assignments and Types

***

### Step 1: Single Variable Assignment

**What we are doing:** Creating three variables of different types and printing them.

```python
var1 = "Python"
var2 = 7575
var3 = 3.5
print(var1, var2, var3)
```

**Breakdown:**

* `var1 = "Python"` — assigns the string `"Python"` to `var1`. The double quotes make it a string.
* `var2 = 7575` — assigns the integer `7575` to `var2`. No quotes, no decimal → integer.
* `var3 = 3.5` — assigns the float `3.5` to `var3`. Has a decimal point → float. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**Expected output:** `Python 7575 3.5`

**Spacing convention:** Use spaces on both sides of `=` for readability. Other spacing styles work but look inconsistent.

***

### Step 2: Chain Assignment (Same Value to Multiple Variables)

```python
a = b = c = 65
print(a, b, c)
```

**What happens:** `65` is assigned to `c`, then `c`'s value to `b`, then `b`'s value to `a`. All three hold `65`. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**Expected output:** `65 65 65`

***

### Step 3: Comma-Separated Assignment (Different Values)

```python
x, y, z = "alpha", "beta", 12
print("variable x value is", x)
print("variable y value is", y)
print("variable z value is", z)
```

**Breakdown:** Comma separates both variables and values. First value → first variable, second → second, third → third. Types can be mixed — `x` and `y` are strings, `z` is integer. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**Expected output:**

```
variable x value is alpha
variable y value is beta
variable z value is 12
```

**How the print works:** The comma inside `print()` concatenates the literal string and the variable value with a space between them.

***

### Step 4: Adding More Variables with Mixed Types

```python
w, x, y, z = "alpha", "beta", 12, 5.4
print(w, x, y, z)
```

**Types:** `w` = string, `x` = string, `y` = integer, `z` = float. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

### Step 5: Checking Types with `type()`

```python
print("variable w is", type(w))
print("variable x is", type(x))
print("variable y is", type(y))
print("variable z is", type(z))
```

**Expected output:**

```
variable w is <class 'str'>
variable x is <class 'str'>
variable y is <class 'int'>
variable z is <class 'float'>
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**How to verify:** The `type()` output confirms the type Python inferred from the assigned value. If the type doesn't match what you expect, check the value — a missing decimal makes it `int` instead of `float`; missing quotes make a word an undefined variable name instead of a string.

**Common mistake:** Forgetting quotes around strings. `var1 = Python` (without quotes) would cause a `NameError` because Python looks for a variable named `Python`, not a string.

***

## Script 2: `data_types.py` — Collection Types and Boolean

***

### Step 6: List (Mutable Collection)

```python
str1 = "alpha"
num1 = 123
first_list = [str1, "DevOps", num1, 3.5]
print(first_list)
```

**Breakdown:**

* Square brackets `[]` → this is a list.
* Elements separated by commas.
* Contains a string variable (`str1`), a literal string (`"DevOps"`), an integer variable (`num1`), and a literal float (`3.5`).
* When printed, variables are resolved to their values. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**Expected output:** `['alpha', 'DevOps', 123, 3.5]`

**Key point:** Lists are **mutable** — you can add, remove, or change elements after creation.

***

### Step 7: Tuple (Immutable Collection)

```python
my_first_tuple = (str1, "DevOps", num1, 3.5)
print(my_first_tuple)
```

**Breakdown:**

* Round brackets `()` → this is a tuple.
* Same elements as the list, just different brackets. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**Expected output:** `('alpha', 'DevOps', 123, 3.5)`

**Key difference from list:** Tuples are **immutable**. If you try to do `my_first_tuple[0] = "new_value"`, Python raises a `TypeError`. Lists allow this; tuples do not.

**Analogy:** List = pen drive (editable). Tuple = CD (read-only content). [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

### Step 8: Dictionary (Key-Value Pairs)

```python
first_dict = {
    "name": "Imran",
    "weight": 75,
    "exercises": ["boxing", "dancing", "jogging"]
}
print(first_dict)
```

**Breakdown:**

* Curly braces `{}` → this is a dictionary.
* Each element is a `key: value` pair.
* `"name": "Imran"` — key is string, value is string.
* `"weight": 75` — key is string, value is integer.
* `"exercises": ["boxing", "dancing", "jogging"]` — key is string, value is a **list**. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**Expected output:** `{'name': 'Imran', 'weight': 75, 'exercises': ['boxing', 'dancing', 'jogging']}`

**Critical observation:** Dictionary values can be **any data type**, including other collections. A list inside a dictionary is extremely common — this is exactly how Ansible variables, JSON API responses, and YAML configurations are structured. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

### Step 9: Checking Types of Collections

```python
print("variable first_list is", type(first_list))
print("variable my_first_tuple is", type(my_first_tuple))
print("variable first_dict is", type(first_dict))
```

**Expected output:**

```
variable first_list is <class 'list'>
variable my_first_tuple is <class 'tuple'>
variable first_dict is <class 'dict'>
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

### Step 10: Boolean

```python
x = True
y = False
print(x, y)
print(type(x), type(y))
```

**Critical syntax:** `True` and `False` — capital T, capital F. No quotes. If you write `"True"` with quotes, it becomes a string, not a boolean. [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

**Expected output:**

```
True False
<class 'bool'> <class 'bool'>
```

**Connection to larger system:** Booleans are the result of every condition check. When you write `if file_exists:` or `if deploy_success:`, those variables hold boolean values that control program flow.

***

## Practice Recommendation from the Video

The instructor explicitly recommends self-practice: "Stress yourself more. Assign your own key value pairs. Use your own dictionaries. Give your own list, tuples. Use your own values. Print them. Print their types. So you get very good hold of this." [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

This is not optional advice — fluency with these data types is prerequisite knowledge for Ansible, JSON, YAML, CloudFormation, and every automation tool in the DevOps ecosystem.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Python Variables and Data Types
PURPOSE:  Foundation for reading/writing JSON, YAML, Ansible, CloudFormation
CONTEXT:  Python for DevOps course — data type fluency enables automation fluency
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## Variable Assignment Patterns

```
SINGLE:
  var1 = "Python"          ← type inferred from value (dynamic typing)

CHAIN (same value):
  a = b = c = 65           ← right-to-left: 65 → c → b → a (all = 65)

COMMA-SEPARATED (different values):
  x, y, z = "alpha", "beta", 12   ← positional: 1st→1st, 2nd→2nd, 3rd→3rd
                                      types can be mixed
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## The Seven Data Types

```
TYPE        SYNTAX                   EXAMPLE              MUTABLE?
──────────  ───────────────────────  ───────────────────  ────────
String      quotes ("" '' """ """)   "Python"             Yes
Integer     no quotes, no decimal    7575                 N/A (scalar)
Float       no quotes, has decimal   3.5                  N/A (scalar)
Boolean     True / False (cap, no ") True                 N/A (scalar)
List        [ ]  square brackets     [1, "a", 3.5]        ✅ MUTABLE
Tuple       ( )  round brackets      (1, "a", 3.5)        ❌ IMMUTABLE
Dictionary  { }  curly braces        {"key": "value"}     ✅ MUTABLE
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## Visual Bracket Identification Rule

```
[ ... ]  →  List        (pen drive — editable)
( ... )  →  Tuple       (CD — read-only content)
{ k: v } →  Dictionary  (word: meaning pairs)
"..."    →  String
no quotes, no dot  →  Integer
no quotes, has dot →  Float
True/False (caps)  →  Boolean
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## Dictionary Nesting (Most Important Pattern)

```
{
  "name": "Imran",              ← string: string
  "weight": 75,                 ← string: integer
  "exercises": [                ← string: LIST
      "boxing",
      "dancing",
      "jogging"
  ]
}

VALUES can be ANY type: string, int, float, list, dict, bool
This is EXACTLY how JSON objects and YAML mappings work
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## List vs. Tuple: Mutability Decision

```
NEED TO MODIFY AFTER CREATION?
  ├── YES → List   [ ]   (add/remove/change elements)
  └── NO  → Tuple  ( )   (fixed content, overwrite only)

ANALOGY:
  List  = pen drive (read/write)
  Tuple = CD (read-only content, can overwrite entire disc)
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## Type Checking

```
type(variable) → returns <class 'TYPE'>

type("hello")  → <class 'str'>
type(42)       → <class 'int'>
type(3.14)     → <class 'float'>
type(True)     → <class 'bool'>
type([1,2])    → <class 'list'>
type((1,2))    → <class 'tuple'>
type({"a":1})  → <class 'dict'>
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## Python → DevOps Format Mapping (Critical)

```
PYTHON              JSON              YAML
──────              ────              ────
dict  { }     =     object { }   =    mapping (key: value)
list  [ ]     =     array  [ ]   =    sequence (- item)
str   "..."   =     string "..."  =   string
int   42      =     number 42    =    integer 42
float 3.5     =     number 3.5   =    float 3.5
bool  True    =     true         =    true / yes
None          =     null         =    null / ~

TOOLS THAT USE THIS:
  Ansible playbooks → YAML (dict + list + string)
  Ansible output    → JSON (dict + list + string)
  CloudFormation    → JSON or YAML
  Kubernetes        → YAML
  Terraform         → HCL (similar concepts)
  API responses     → JSON

"Almost every automation tool today uses JSON or YAML"
```

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## Reusable Engineering Patterns

| Pattern                            | Manifestation                                                                               |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| **Dynamic Typing**                 | Python infers type from value — no explicit declaration needed                              |
| **Universal Data Vocabulary**      | dict/list/string/int/float/bool = the building blocks of ALL config formats                 |
| **Nested Structures**              | Dictionaries containing lists containing dictionaries — the shape of real-world config data |
| **Mutability Contract**            | List (mutable) vs. Tuple (immutable) = explicit control over data changeability             |
| **Key-Value as Universal Pattern** | Dictionaries = JSON objects = YAML mappings = config files = API payloads                   |
| **Visual Syntax Identification**   | Bracket type instantly reveals data structure — transferable to JSON/YAML reading           |

 [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

## One-Line System Reconstruction

> **Python variables use dynamic typing (type inferred from value) across seven data types — string, int, float, bool (scalars) and list `[]` (mutable), tuple `()` (immutable), dict `{}` (key-value pairs, values can be any type including nested lists) — which map directly to JSON objects/arrays and YAML mappings/sequences, making Python data type fluency the foundation for reading and writing every DevOps automation format (Ansible, CloudFormation, Kubernetes, API responses).** [\[203-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/203-variables.txt)

***

This completes the full reconstruction of the Python Variables and Data Types lecture. It connects directly to every DevOps tool that uses JSON or YAML — which, as the video states, is essentially all of them. The next lecture covers different ways of printing in Python. Let me know if you'd like any section expanded or adjusted! 🚀
