# 📘 Variables & Python Data Structures — Deep Learning Material

**Source:** Caption file covering Bash/Shell variables and core Python data structures (string, integer, list, tuple, dictionary), including indexing, slicing, and access patterns. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Is a Variable?

A variable is a **temporary storage of data in memory (RAM)**. It lives only inside the program or session that created it. When you open a shell like Git Bash and create a variable, that variable exists only for the life of that shell session. The moment you close Git Bash, the variable — and the data it held — is gone. This is the fundamental nature of runtime variables: they are **ephemeral, session-scoped containers**. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

Every variable has two parts: a **name** (the label you choose) and a **value** (the data it stores). The name is how you refer to the storage location later; the value is what occupies that location. The act of assigning a value is called **storing**, and reading it back is called **retrieving**. This store-then-retrieve cycle is the most basic operation in any programming or scripting environment. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

> 🔍 **Deep Dive**
> Variables in both Bash and Python are abstractions over memory addresses. You never deal with the address directly — the language runtime handles that. In Bash, variables are untyped at the shell level (everything is essentially a string unless the context forces arithmetic). In Python, variables are dynamically typed — the interpreter infers the type from the assigned value at runtime. This means the same variable name can hold a string now and an integer later (though doing so is generally poor practice). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.2 Shell (Bash) Variables — Syntax & Behavior

In Bash (or any POSIX-compatible shell), you create a variable with the pattern `NAME=VALUE` — **no spaces around the equals sign**. This is a critical syntax rule. If you write `skill = DevOps` with spaces, Bash interprets `skill` as a command and `=` and `DevOps` as its arguments, resulting in an error. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

To **retrieve** (access) the stored value, you prefix the variable name with a **dollar sign (`$`)**. So `echo $skill` prints the value `DevOps`. Without the dollar sign, `echo skill` simply prints the literal text `skill` — Bash has no idea you meant a variable. The dollar sign is the **dereference operator** in shell: it tells the interpreter "go look up the value stored under this name." [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

### String Interpolation and Quoting Rules

You can embed a variable inside a string using double quotes: `echo "I am learning $skill"` outputs `I am learning DevOps`. The dollar sign retains its special meaning inside double quotes. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

However, **single quotes strip all special meaning**. If you write `echo 'I am learning $skill'`, the output is literally `I am learning $skill`. The dollar sign becomes plain text. This is a fundamental Bash quoting rule: **double quotes allow variable expansion; single quotes prevent it entirely.** [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

> ⚠️ **Expert Note**
> This single-quote vs. double-quote distinction is specific to shell scripting and does **not** apply to Python or most other programming languages. In Python, single and double quotes are functionally interchangeable for defining strings. Confusing these rules across languages is a common beginner mistake. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.3 Data Types — String vs. Integer (Conceptual Foundation)

A **string** is textual data — any sequence of characters enclosed in quotes. `"DevOps"` is a string. A string can contain letters, numbers, symbols, or even be empty (`""`). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

An **integer** is a whole number with no quotes around it. `num=123` in Bash or `number = 123` in Python creates an integer variable. The absence of quotes is what signals to the interpreter that this is a numeric value, not text. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

This distinction matters because the type determines what operations are valid. You can perform arithmetic on integers but not on strings. You can concatenate strings but not integers (without conversion). Understanding that the **value's format determines the type** is the first mental model of dynamic typing. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.4 Transition to Python — Environment & Print

The video transitions from Bash to Python using an **online editor** (Programiz is demonstrated, but any Python editor or IDE works). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

In Python, the equivalent of Bash's `echo` is the **`print()` function**. The syntax is `print("text")` — parentheses are mandatory (it's a function call), and the text goes inside quotes within those parentheses. `print("")` with an empty string outputs a blank line, which can serve as a visual separator in output. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.5 Comments in Python (and Bash)

A **comment** is a line (or portion of a line) that the interpreter ignores entirely. In both Python and Bash, comments begin with the **hash symbol (`#`)**. Anything after `#` on that line is not executed. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

Comments exist for humans, not machines. They let you annotate your code with explanations, reminders, or temporary disabling of code lines (a technique used throughout this video to isolate sections during demonstration). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.6 Python Variables — String and Integer

In Python, variable assignment uses the same `name = value` pattern, but **spaces around `=` are allowed** (and conventional for readability), unlike Bash. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

For strings: `skill = "DevOps"` — the value is enclosed in double or single quotes. Both work identically in Python (unlike Bash). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

For integers: `number = 123` — no quotes. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

To retrieve and display a variable, you pass it to `print()` **without quotes**: `print(skill)` outputs `DevOps`. If you write `print("skill")`, Python prints the literal text `skill` — it treats the quoted content as a string, not a variable reference. This is the Python equivalent of Bash's dollar-sign rule: **quotes make it literal; no quotes make it a variable reference** (inside `print()`). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.7 Lists — Ordered, Mutable Collections

A **list** is a collection of multiple values stored under a single variable name. It is defined using **square brackets `[]`**, with elements separated by **commas**. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

```python
tools = ["Jenkins", "Docker", "k8s", "Terraform", 90]
```

Key characteristics of lists: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

* **Ordered**: Elements maintain the sequence in which you define them.
* **Mixed types**: A single list can hold strings, integers, and even other lists (nested lists).
* **Mutable** (implied): You can change, add, or remove elements after creation (the video does not explicitly demonstrate mutation but references further Python sections).

When you `print(tools)`, Python outputs the entire list in its square-bracket notation: `['Jenkins', 'Docker', 'k8s', 'Terraform', 90]`. The visual signature of a list is **square brackets with comma-separated elements** — this same notation is used in JSON, making lists a bridge concept between Python and data serialization formats. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.8 Tuples — Ordered, Immutable Collections

A **tuple** looks almost identical to a list, but is defined using **parentheses `()`** instead of square brackets. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

```python
tools = ("Jenkins", "Docker", "k8s", "Terraform", 90)
```

The video emphasizes that the parenthesis-vs-bracket distinction is the **visible difference**. The **actual difference** (which the video defers to the Python section) is that tuples are **immutable** — once created, their elements cannot be changed, added, or removed. Lists are mutable; tuples are not. This makes tuples useful for data that should remain constant. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

Accessing elements works identically for both lists and tuples — using square-bracket indexing (covered next). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.9 Indexing — Accessing Individual Elements

Both lists and tuples support **index-based access**. The syntax is `variable[index]`. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

Python uses **zero-based indexing**: the first element is at position `0`, the second at `1`, and so on. For the list `["Jenkins", "Docker", "k8s", "Terraform", 90]`: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

| Index | 0       | 1      | 2   | 3         | 4  |
| ----- | ------- | ------ | --- | --------- | -- |
| Value | Jenkins | Docker | k8s | Terraform | 90 |

`tools[0]` → `Jenkins`, `tools[1]` → `Docker`, and so on.

Python also supports **negative indexing**: `-1` is the last element, `-2` is the second-to-last, and so on. `tools[-1]` → `90`. This is a powerful shortcut when you need the end of a collection without knowing its length. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

> 🔍 **Deep Dive**
> Negative indexing is syntactic sugar. Internally, `tools[-1]` is equivalent to `tools[len(tools) - 1]`. The interpreter calculates the actual position by adding the negative index to the length. This works for lists, tuples, and strings alike — any sequence type in Python. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.10 Slicing — Extracting Sub-sequences

Slicing extends indexing to extract a **range** of elements. The syntax is `variable[start:end]`, where: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

* `start` is the index of the first element to include (inclusive).
* `end` is the index to stop at (**exclusive** — the element at this index is NOT included).

For `tools = ["Jenkins", "Docker", "k8s", "Terraform", 90]`: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

`tools[1:4]` → `["Docker", "k8s", "Terraform"]`

This returns elements at indices 1, 2, and 3 — **not** 4. The "end is exclusive" rule is one of the most common sources of off-by-one errors for beginners. The mental model: **the end index is a boundary wall, not an element selector**. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

### Nested/Chained Slicing

Slicing can be **chained**. The result of a slice is itself a sequence, so you can index or slice it further. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

```python
tools[1:4][1]  # → "k8s"
```

Here, `tools[1:4]` produces `["Docker", "k8s", "Terraform"]`, and then `[1]` picks the second element of that result: `"k8s"`. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

Since strings are also sequences, you can further slice into a string element:

```python
tools[1:4][1][0]  # → "k"
```

`"k8s"[0]` → `"k"`. This demonstrates a core Python principle: **every sequence type supports the same indexing and slicing protocol**. Strings, lists, and tuples all share this interface. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

> ⚠️ **Expert Note**
> The video explicitly stops at this level of nested slicing and notes that deeper slicing mechanics are covered in the dedicated Python section. For this stage, the goal is to understand the **pattern** (sequence → index/slice → sequence → index/slice) rather than memorize complex nested expressions. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.11 Dictionaries — Key-Value Storage

A **dictionary** is a collection where data is stored as **key-value pairs**, enclosed in **curly braces `{}`**. Each pair uses a **colon** to separate the key from the value, and pairs are separated by **commas**. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

```python
DevOps = {
    "skill": "DevOps",
    "year": 2023,
    "tech": ["Docker", "k8s", "Terraform"],
    "GitOps": ""
}
```

The analogy is a real-world dictionary: the **key** is the word, and the **value** is its definition. You look things up by key, not by position number. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

### Heterogeneous Values

A dictionary's values can be of **any type** — and different keys can hold different types within the same dictionary: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

| Key        | Value                            | Type         |
| ---------- | -------------------------------- | ------------ |
| `"skill"`  | `"DevOps"`                       | string       |
| `"year"`   | `2023`                           | integer      |
| `"tech"`   | `["Docker", "k8s", "Terraform"]` | list         |
| `"GitOps"` | `""`                             | empty string |

This makes dictionaries extremely flexible. They can model complex, structured data — which is exactly why JSON (a data format built on key-value pairs) maps directly to Python dictionaries. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

### Accessing Dictionary Values

Unlike lists (which use numeric indices), dictionaries use **key names** for access: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

```python
print(DevOps["skill"])  # → "DevOps"
```

The syntax is `dictionary_name["key_name"]` — square brackets with the key as a string. This is structurally similar to list indexing (`list[0]`), but instead of a positional number, you provide a meaningful name. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

Once you retrieve a value, you can **further slice it** if the value itself is a sliceable type. Since `DevOps["skill"]` returns the string `"DevOps"`, you can do: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

```python
print(DevOps["skill"][0])  # → "D"
```

This is the same chained-access pattern seen with lists: **access → get a sequence → access again**. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.12 The Unified Access Pattern (Key Conceptual Insight)

Across all data structures covered, a single access pattern emerges: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

| Structure  | Access Syntax   | Accessor Type      |
| ---------- | --------------- | ------------------ |
| List       | `list[index]`   | Integer (position) |
| Tuple      | `tuple[index]`  | Integer (position) |
| String     | `string[index]` | Integer (position) |
| Dictionary | `dict["key"]`   | String (key name)  |

And all of them support **chaining**: you access an element, and if that element is itself a sequence or dictionary, you can access deeper. This recursive access pattern is the foundation for navigating complex nested data structures — which is exactly what JSON and YAML files are. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 1.13 The Syntax Signature Map (Visual Type Identification)

The video implicitly teaches a critical skill: **identifying data types by their visual delimiters**: [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

| Delimiter          | Data Structure |
| ------------------ | -------------- |
| `" "` or `' '`     | String         |
| `[ ]`              | List           |
| `( )`              | Tuple          |
| `{ }`              | Dictionary     |
| No quotes, numeric | Integer        |

When you see output or code, the brackets/braces immediately tell you what type of data you're looking at. This visual recognition skill becomes essential when reading JSON, YAML, API responses, and configuration files. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning to **create, store, and retrieve data** using Bash shell variables and Python's core data structures (string, integer, list, tuple, dictionary). We are also learning to **access specific elements** within collections using indexing, slicing, and key-based access. The final operational outcome is the ability to define structured data in Python and extract any piece of information from it — a prerequisite for working with JSON and YAML. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## Step 1: Set Up the Shell Environment

**What we're doing:** Opening the correct terminal to practice Bash variables.

* **Windows users:** Open **Git Bash** (not PowerShell, not Command Prompt).
* **macOS users:** Open the default **Terminal**.

Git Bash is required on Windows because it provides a POSIX-compatible shell (Bash), which supports the `$variable` syntax. PowerShell and CMD use different variable conventions. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## Step 2: Create and Retrieve a Bash String Variable

**What we're doing:** Storing a string value and printing it.

```bash
skill="DevOps"
```

**Breakdown:** `skill` is the variable name. `=` is the assignment operator. `"DevOps"` is the string value. **No spaces** around `=`. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Retrieve it:**

```bash
echo $skill
```

**Breakdown:** `echo` is the print command. `$skill` dereferences the variable — the `$` tells Bash to look up the value stored under `skill`. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Expected output:** `DevOps`

**Common mistake:** Omitting the `$`. Running `echo skill` outputs the text `skill`, not the variable's value. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Embedding in a string:**

```bash
echo "I am learning $skill"
```

**Expected output:** `I am learning DevOps` [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Verification of quoting behavior:**

```bash
echo 'I am learning $skill'
```

**Expected output:** `I am learning $skill` (literal — single quotes suppress variable expansion). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Connection to larger flow:** This establishes the store → retrieve pattern that all subsequent structures follow.

***

## Step 3: Create and Retrieve a Bash Integer Variable

```bash
num=123
echo $num
```

**Expected output:** `123`

Same pattern as strings. No quotes around the number when assigning. Retrieval syntax is identical — `$` prefix. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## Step 4: Set Up the Python Environment

**What we're doing:** Opening an online Python editor to practice Python data structures.

1. Open **Brave Browser** (recommended to block ads on online editors — or use any browser). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)
2. Google search: `Python editors online`.
3. Open **Programiz** online Python editor (or use VS Code, or any Python environment you prefer). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Connection to larger flow:** We are switching from Bash to Python because the data structures (list, tuple, dictionary) we need for JSON/YAML understanding are Python constructs.

***

## Step 5: Python Print Statement and Comments

**What we're doing:** Learning the basic output command and comment syntax.

```python
print("Hello")
```

**Breakdown:** `print` is the function. `()` encloses the argument. `"Hello"` is the string to display. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Empty print (separator):**

```python
print("")
```

Outputs a blank line. Useful as a visual separator between outputs. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Comments:**

```python
# This is a comment
print("This runs")
# hello — this is ignored
```

The `#` tells Python to ignore everything after it on that line. Use it to annotate code or temporarily disable lines. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## Step 6: Python String Variable — Store and Retrieve

```python
skill = "DevOps"
print(skill)
```

**Breakdown:** `skill` is the variable name. `=` assigns. `"DevOps"` is the string value. `print(skill)` — note: **no quotes** around `skill` inside print. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Expected output:** `DevOps`

**Common mistake:**

```python
print("skill")
```

**Output:** `skill` (literal text). Quotes make Python treat it as a string, not a variable reference. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## Step 7: Python Integer Variable — Store and Retrieve

```python
number = 123
print(number)
```

**Expected output:** `123`

No quotes around `123` — this makes it an integer, not a string. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## Step 8: Python List — Create, Print, and Access

**What we're doing:** Creating an ordered collection with mixed types.

```python
tools = ["Jenkins", "Docker", "k8s", "Terraform", 90]
print(tools)
```

**Breakdown:** Square brackets `[]` define a list. Elements are comma-separated. Mix of strings and an integer (`90`). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Expected output:** `['Jenkins', 'Docker', 'k8s', 'Terraform', 90]`

**Accessing a specific element by index:**

```python
print(tools[0])    # → Jenkins (first element)
print(tools[1])    # → Docker
print(tools[-1])   # → 90 (last element, negative index)
```

**How indexing works:** Position counting starts at `0`. Negative indices count backward from the end (`-1` = last, `-2` = second-to-last). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Connection to larger flow:** List indexing syntax (`variable[index]`) is the same pattern used for dictionary access and string slicing.

***

## Step 9: Python Tuple — Create, Print, and Access

```python
tools = ("Jenkins", "Docker", "k8s", "Terraform", 90)
print(tools)
```

**Only visible change from list:** Parentheses `()` instead of square brackets `[]`. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Accessing elements:** Identical to list — uses square brackets with index numbers.

```python
print(tools[0])    # → Jenkins
print(tools[-1])   # → 90
```

**Connection to larger flow:** The video focuses on lists going forward, as they are more commonly used and directly relevant to JSON. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## Step 10: List Slicing — Extracting Ranges

**What we're doing:** Getting a subset of elements from a list.

```python
tools = ["Jenkins", "Docker", "k8s", "Terraform", 90]
print(tools[1:4])
```

**Breakdown:** `1` is the start index (inclusive). `4` is the end index (**exclusive**). This extracts elements at indices 1, 2, 3. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Expected output:** `['Docker', 'k8s', 'Terraform']`

**Common mistake:** Expecting the element at the end index to be included. `tools[1:4]` does **not** include `tools[4]` (which is `90`). [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Chained slicing:**

```python
print(tools[1:4][1])    # → k8s
```

`tools[1:4]` returns `['Docker', 'k8s', 'Terraform']`, then `[1]` picks `k8s` from that result. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Further chaining into a string:**

```python
print(tools[1:4][1][0])  # → k (not shown explicitly but follows same logic)
```

Since `k8s` is a string, `[0]` gets its first character. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Connection to larger flow:** This chained access pattern is how you navigate deeply nested JSON/YAML structures.

***

## Step 11: Python Dictionary — Create, Print, and Access

**What we're doing:** Creating a key-value data structure with mixed value types.

```python
DevOps = {
    "skill": "DevOps",
    "year": 2023,
    "tech": ["Docker", "k8s", "Terraform"],
    "GitOps": ""
}
print(DevOps)
```

**Breakdown:** [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

* `{}` — curly braces define a dictionary.
* `"skill": "DevOps"` — key `"skill"`, value `"DevOps"` (string → string).
* `"year": 2023` — key `"year"`, value `2023` (string → integer).
* `"tech": ["Docker", "k8s", "Terraform"]` — key `"tech"`, value is a **list** (string → list).
* `"GitOps": ""` — key `"GitOps"`, value is an **empty string**.
* Pairs separated by commas.

**Accessing a value by key:**

```python
print(DevOps["skill"])    # → DevOps
```

**Breakdown:** `DevOps` is the dictionary variable. `["skill"]` accesses the value associated with the key `"skill"`. Unlike lists (which use integer indices), dictionaries use **key names** as strings. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Chained access — slicing a string value:**

```python
print(DevOps["skill"][0])  # → D
```

`DevOps["skill"]` returns `"DevOps"` (a string), then `[0]` gets the first character. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

**Connection to larger flow:** This dictionary structure is exactly how JSON data is organized. The next lecture builds more complex dictionaries to bridge into JSON and YAML formats.

> ⚠️ **Expert Note**
> The video advises: focus on the **syntax details** — commas, colons, double quotes, bracket types. These punctuation rules are identical in JSON. Mistakes like a missing comma or a misplaced colon will cause parse errors in both Python and JSON. Mastery comes through hands-on repetition: store different types, print them, access their elements. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗂️ Core Architecture

```
VARIABLE (name = value)
├── Bash: NAME=VALUE (no spaces), retrieve with $NAME
└── Python: name = value (spaces OK), retrieve with print(name)
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 🔤 Type Signature Map (Instant Visual Recognition)

```
" " or ' '  →  String
[ ]         →  List
( )         →  Tuple
{ : }       →  Dictionary
No quotes   →  Integer (if numeric)
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 🔗 Bash Quoting Rule (Single vs Double)

```
Double quotes "..."  →  $variable EXPANDS  →  value printed
Single quotes '...'  →  $variable LITERAL  →  $variable printed
⚠️ This rule is BASH-ONLY. Python: single = double (no difference).
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 📦 Python Data Structures — Hierarchy

```
Data Structures
├── String    →  "text"         →  Immutable sequence of characters
├── Integer   →  123            →  Whole number, no quotes
├── List      →  [a, b, c]     →  Ordered, mutable, mixed types
├── Tuple     →  (a, b, c)     →  Ordered, IMMUTABLE, mixed types
└── Dictionary → {key: value}  →  Unordered key-value pairs, mixed value types
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 🎯 Unified Access Pattern

```
SEQUENCE TYPES (list, tuple, string):
  variable[index]        →  Single element (zero-based)
  variable[-1]           →  Last element
  variable[start:end]    →  Slice (start inclusive, end EXCLUSIVE)

DICTIONARY:
  variable["key"]        →  Value for that key

CHAINING (universal):
  container[accessor1][accessor2][accessor3]...
  → Each access returns a value → next accessor operates on THAT value
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 🔢 Indexing Mental Model

```
List: ["Jenkins", "Docker", "k8s", "Terraform", 90]
       ↑0         ↑1        ↑2      ↑3          ↑4
       ↑-5        ↑-4       ↑-3     ↑-2         ↑-1

Slice [1:4] → elements at 1, 2, 3 → ["Docker", "k8s", "Terraform"]
              (start inclusive, end EXCLUSIVE — end is a wall, not a selector)
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 📖 Dictionary Internal Structure

```
DevOps = {
  "skill"  : "DevOps"                      ← str → str
  "year"   : 2023                           ← str → int
  "tech"   : ["Docker","k8s","Terraform"]   ← str → list
  "GitOps" : ""                             ← str → empty str
}

Access:  DevOps["skill"]     → "DevOps"
Chain:   DevOps["skill"][0]  → "D"
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 🔄 Operational Flow (Store → Retrieve → Slice)

```
1. DEFINE    →  variable = value
2. STORE     →  interpreter saves in memory
3. RETRIEVE  →  print(variable) / echo $variable
4. ACCESS    →  variable[index] or variable["key"]
5. SLICE     →  variable[start:end]
6. CHAIN     →  variable[a][b][c] (recursive access into nested structures)
```

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 🔁 Reusable Engineering Patterns

| Pattern                            | Instance in This Content                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| **Uniform Interface**              | All sequence types (list, tuple, string) share `[index]` and `[start:end]` syntax    |
| **Key-Based Lookup**               | Dictionary replaces positional index with semantic key name                          |
| **Recursive Composition**          | Lists inside dictionaries, strings inside lists — access by chaining                 |
| **Visual Delimiter = Type Signal** | `[]` = list, `()` = tuple, `{}` = dict — instant type recognition                    |
| **Ephemeral State**                | Shell variables die with the session — data must be persisted externally             |
| **Literal vs. Reference**          | Quotes make it literal text; no quotes (or `$` in Bash) make it a variable reference |

 [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

## 🧭 Bridge to Next Lecture

```
This Lecture                          Next Lecture
─────────────                         ─────────────
Simple dictionary  ──────────────→   Complex/nested dictionary
Python syntax      ──────────────→   JSON format (same structure, different syntax)
Python syntax      ──────────────→   YAML format (same structure, human-readable)
```

The dictionary structure you learned here **is** JSON. The next step is building more complex nested dictionaries and seeing how they map 1:1 to JSON and YAML. [\[60-variabl...-python-ds \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/60-variables-and-python-ds.txt)

***

This material covers every concept, command, and relationship from the video. Practice by creating your own variables of each type, accessing elements at various indices, and building dictionaries with mixed value types — that hands-on repetition is what converts this knowledge into operational fluency. 🚀
