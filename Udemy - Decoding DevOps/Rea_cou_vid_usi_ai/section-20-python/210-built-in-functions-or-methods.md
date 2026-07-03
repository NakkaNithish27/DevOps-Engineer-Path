# 🎓 Deep Learning Material: Python Built-in Functions & Methods

**Source:** [210-built-in-functions-or-methods.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt?EntityRepresentationId=c8ff37ef-eaa1-4db6-95c2-64bfe098e3be) — Video lecture covering Python's built-in functions and data-type-specific methods for strings, lists, tuples, and dictionaries, including method discovery via `dir()` and PyCharm, string immutability, list mutability, and practical DevOps use cases for string processing. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Built-in Functions vs. Methods — The Core Distinction

Python comes with a set of **built-in functions** — these are globally available functions that work across different data types without needing to import anything. Examples the video references include `print()`, `type()`, `str()`, `input()`, and `len()`. These are **standalone functions** — you call them directly and pass data to them as arguments: `print(x)`, `type(x)`, `len(x)`. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

But the focus of this video is something different: **methods**. Methods are functions that are **attached to a specific data type**. You access them using **dot notation** — you take a variable, put a dot after it, and then call the method. For example, `message.capitalize()` calls the `capitalize` method on the string stored in `message`. The critical distinction is: built-in functions are universal (they exist independently), while methods belong to a specific data type (strings have string methods, lists have list methods, dictionaries have dictionary methods). You cannot call `message.len()` — `len` is a built-in function, not a string method. And you cannot call `capitalize("hello")` as a standalone function — `capitalize` is a string method that must be called on a string object. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

The video organizes these methods by data type: strings, lists, tuples, and dictionaries. Each data type has its own set of available methods, and the set of methods available directly reflects the **nature** of that data type — particularly whether it is mutable or immutable. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## 1.2 Discovering Available Methods — `dir()` and PyCharm

Before diving into individual methods, the video teaches two ways to discover what methods are available for any data type.

**Method 1: The `dir()` function.** `dir()` is itself a built-in function. When you pass a variable to it — `dir(message)` where `message` is a string — it returns a **list** of all available methods and attributes for that data type. The output is a list of strings, each being a method name (like `'capitalize'`, `'count'`, `'center'`, `'find'`, etc.). This works for any data type: pass a string, you get string methods; pass a list, you get list methods; pass a dictionary, you get dictionary methods. You must wrap `dir()` in `print()` to see the output: `print(dir(message))`. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**Method 2: PyCharm (or any Python IDE).** When you type a variable name followed by a dot in PyCharm, the IDE automatically pops up a list of all available methods for that variable's data type. This is essentially a visual, interactive version of `dir()`. The video explicitly recommends PyCharm for this reason — it provides immediate discovery of available methods as you code. The same autocomplete feature exists in other Python IDEs. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**Method 3: W3Schools documentation.** The video references W3Schools as a useful external documentation source, which lists all Python built-in functions, string methods, list methods, and dictionary methods with examples. The instructor notes that while you can get all this information from the interpreter itself, the documentation provides "a better view." [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## 1.3 String Methods and String Immutability

Strings are **immutable** in Python. This is a foundational concept the video emphasizes with a direct demonstration. When you call `message.capitalize()`, it does **not** modify the original string. It returns a **new** string with the first character capitalized. If you then print `message` again, the original value is unchanged. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

This has a practical consequence: if you want to keep the modified version, you must **store the return value** in a variable. You can either reassign it to the same variable (`message = message.capitalize()`) or store it in a new variable (`Message = message.capitalize()`). The video demonstrates the second approach — storing the capitalized version in a differently-named variable to show that the original remains untouched. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

This immutability rule applies to **every** string method. `upper()`, `lower()`, `find()`, `join()` — none of them change the original string. They all return new values. If you don't capture the return value, the result is lost. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### String Methods Covered

**`capitalize()`** — Converts the first character of the string to uppercase, returns the result. The video starts with a sentence where the first character `c` is already capital, then demonstrates `capitalize()` to show the behavior. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`upper()`** — Converts the entire string to uppercase. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`lower()`** — Converts the entire string to lowercase. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`islower()`** — Returns a boolean (`True`/`False`). Returns `True` if all characters are lowercase. This is a **validation method** — it doesn't transform the string, it checks a property of it. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`isupper()`** — Returns `True` if all characters are uppercase, `False` otherwise. The video demonstrates calling `isupper()` on a lowercase string, getting `False`. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`isalnum()`** (alpha-numeric check) — The video mentions this along with `isalpha()`, `isascii()`, `isdecimal()`, `isdigit()` as examples of boolean validation methods. These are described as "good for data validation" — checking whether input meets certain criteria before processing it further. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`find()`** — Searches for a substring within the string and returns the **index** (position) where the substring starts. Index counting begins at zero. The video demonstrates finding `"ready"` in a string — it returns `18`, meaning the `r` of `"ready"` is at position 18. If the substring is **not found**, `find()` returns **-1**. The video explains this: the method traverses the entire string, reaches the end without finding a match, and returns -1 to indicate failure. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

The video then demonstrates **combining `find()` with string slicing**: once you know the starting index (18) and the length of the substring (5 characters for "ready"), you can slice the string with `message[18:23]` (or `18:24` depending on boundary — the video adjusts this live) to extract just that substring. This is presented as a practical pattern: find the position, then slice. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`join()`** — This method works differently from the others. It is called on the **separator string** (not on the data), and takes a sequence (tuple, list) as its argument. The video demonstrates:

```python
sequence1 = ("192", "168", "1", "14")
print(".".join(sequence1))
```

This joins all elements of the tuple with `"."` between them, producing `"192.168.1.14"` — an IP address. The video also shows joining with `"/"` and `"-"` to create date-like patterns. The instructor explicitly connects this to **DevOps use cases**: when doing cloud automation, you often receive data as separate pieces and need to combine them into formatted strings like IP addresses, paths, or dates. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

🔍 **Deep Dive**
The `join()` method requires all elements in the sequence to be strings. If any element is an integer, it will raise a `TypeError`. This is an implicit constraint — the video uses a tuple of strings without explicitly calling this out, but the data type choice (string elements in the tuple) is deliberate. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## 1.4 List Methods and List Mutability

Lists are **mutable** — unlike strings, you can modify them directly. The video states this explicitly: "I told you one thing about list is they are mutable. You can change it, but how do you change it? That I did not tell you. So you can edit a list through the built-in functions." This is the core reason lists have methods like `append`, `insert`, `pop` — they **modify the list in place** rather than returning new copies. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### List Methods Covered

**`append(item)`** — Adds a single item to the **end** of the list. The video appends `"mount oregon"` to a list of mountains. After appending, printing the list shows the new item at the end. Unlike string methods, `append()` modifies the original list directly — you do not need to capture a return value. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`extend(another_list)`** — Combines two lists by adding all elements from the given list to the end of the original list. The video extends the mountains list with a new list of additional mountains. The key difference from `append`: `append` adds its argument as a **single element** (even if it's a list — it would add the whole list as one nested item), while `extend` **unpacks** the argument list and adds each element individually. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`insert(index, item)`** — Inserts an item at a **specific position** in the list. The video inserts `"mount abu"` at index 2 (the third position, since indexing starts at 0). This pushes all subsequent elements one position forward. Unlike `append` (which only adds at the end), `insert` gives you positional control. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`pop()`** — Removes and returns the **last element** of the list when called with no arguments. The video demonstrates calling `pop()` on the mountains list, which removes `"satpuda"` (the last item). The video also notes: "If I run it many times, that many times it's going to pop" — each execution removes the current last element. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`pop(index)`** — When called with an index argument, removes the element at that specific position. The video demonstrates `pop(5)` to remove `"k2"` from position 5 (counting from 0). [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

🔍 **Deep Dive**
The video makes an important operational note about script re-execution: "when I'm hitting run, it's executing everything again. So mountains will be executed again. The variable again, it's going to store the value and then it's going to append. So all the operations are doing again whenever I'm running it." This means each run starts fresh — the list is re-initialized from its definition, then all operations are applied in order. The list does not "remember" modifications from previous runs. This is a common source of confusion for beginners who think running the script multiple times accumulates changes. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## 1.5 Tuple — Immutability Means Almost No Methods

The video handles tuples very briefly and deliberately: "There are not many because tuple is immutable. So you can't make many, can't make any change to it." Since tuples cannot be modified after creation, they lack modification methods like `append`, `insert`, `pop`, `extend`, or `clear`. The video skips directly from tuples to dictionaries because there is little to demonstrate. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## 1.6 Dictionary Methods

Dictionaries are mutable and have their own set of methods. The video demonstrates several and mentions others.

**`keys()`** — Returns all the **keys** of the dictionary. The video shows a dictionary with keys `name`, `skill`, `code` and calls `.keys()` to get them. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`values()`** — Returns all the **values** of the dictionary. The video demonstrates this as the complement to `keys()`. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**`clear()`** — Removes **all** key-value pairs from the dictionary, leaving it empty. The video demonstrates this: after calling `clear()`, printing the dictionary shows `{}` — an empty dictionary. This is an **in-place** modification (like list methods), not a copy. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

The video also mentions (via the PyCharm dot-autocomplete list) additional dictionary methods without demonstrating them in detail: `pop`, `remove`, `copy`, `get`, `items`, `popitem`. These are listed as "few nice methods, useful" — acknowledged but not explored in this lecture. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## 1.7 The DevOps Context for These Operations

The instructor explicitly connects string and data processing methods to DevOps work: "These are some commonly used built-in functions by us. I mean to say DevOps. When we get some data, we're doing some cloud automation, something. We get some data, we find that data and we process it. And then based on that data, we do more operations. So in such cases, data validation, finding your string, combining them — these operations will be very helpful." [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

This frames the methods not as abstract programming concepts but as **operational tools**: `find()` locates data in strings returned by API calls or command outputs; `join()` assembles IP addresses, paths, or formatted identifiers; `islower()`/`isalnum()` validate input before acting on it; `append()`/`extend()` build up collections of resources or results during automation scripts. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning to use Python's built-in methods to manipulate strings, lists, and dictionaries — and to discover what methods are available for any data type. The final outcome: you can transform, search, validate, and restructure data using dot-notation methods on any Python object, discover available methods without memorizing them, and apply these operations in automation scripts. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 1: Set Up the Environment

Open **PyCharm** (recommended) or any Python IDE. Create a new Python script file. PyCharm is specifically recommended because typing a variable followed by `.` will auto-display all available methods for that variable's data type. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 2: Discover Available Methods with `dir()`

Before using methods, learn to discover them. Define any variable and pass it to `dir()`:

```python
message = "some string here"
print(dir(message))
```

| Part           | Purpose                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------- |
| `dir(message)` | Returns a list of all method names available for the data type of `message` (string in this case) |
| `print(...)`   | Required to see the output — `dir()` returns a list, it doesn't print it automatically            |

**Expected output:** A list of strings like `['capitalize', 'center', 'count', 'encode', 'find', ...]`. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

You can replace `message` with any variable of any type — a list, a tuple, a dictionary — and `dir()` will return the methods specific to that type. This is how you explore without documentation.

**In PyCharm:** Simply type the variable name, then `.` — the IDE shows the same list interactively with descriptions. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 3: String Methods — Transformation

### 3a. `capitalize()`

```python
message = "cloud computing is evolving fast"
print(message.capitalize())
```

**Expected output:** `Cloud computing is evolving fast` — first character uppercased.

**Critical behavior:** The original `message` is **unchanged**. Print it again to confirm:

```python
print(message)  # still "cloud computing is evolving fast"
```

To keep the result, store it:

```python
Message = message.capitalize()
print(Message)  # "Cloud computing is evolving fast"
```

 [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

This immutability rule applies to **all** string methods below. None modify the original.

### 3b. `upper()` and `lower()`

```python
print(message.upper())   # entire string → UPPERCASE
print(message.lower())   # entire string → lowercase
```

 [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 4: String Methods — Boolean Validation

```python
print(message.islower())   # True — all characters are lowercase
print(message.isupper())   # False — not all uppercase
print(message.isalnum())   # checks if alphanumeric (no spaces/special chars)
```

 [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

These return `True` or `False`. Use them for **data validation** — checking properties of input before acting on it. Other validation methods mentioned: `isalpha()`, `isascii()`, `isdecimal()`, `isdigit()`.

***

## Step 5: String Methods — `find()` and String Slicing

### 5a. Find a substring

```python
message = "most of them are more than ready to go"
print(message.find("ready"))
```

**Expected output:** `18` — the index where `"ready"` starts (counting from 0). [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### 5b. Extract the found substring using slicing

```python
start = message.find("ready")      # 18
length = len("ready")              # 5
print(message[start:start+length]) # "ready"
```

Pattern: **find the position → calculate the range → slice**. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### 5c. Handle "not found"

```python
print(message.find("not"))  # returns -1 if substring doesn't exist
```

`-1` means: the method traversed the entire string without finding a match. Always check for `-1` before slicing. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 6: String Methods — `join()`

```python
sequence1 = ("192", "168", "1", "14")
print(".".join(sequence1))
```

| Part               | Purpose                                                   |
| ------------------ | --------------------------------------------------------- |
| `"."`              | The separator string — placed between each element        |
| `.join(sequence1)` | Takes the sequence, joins all elements with the separator |

**Expected output:** `192.168.1.14` [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

Note: `join()` is called on the **separator**, not on the sequence. The sequence is passed as the argument.

Other separator examples:

```python
print("/".join(sequence1))   # 192/168/1/14
print("-".join(sequence1))   # 192-168-1-14
```

 [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**DevOps use case:** Assembling IP addresses, file paths, date strings, or any formatted identifier from component parts received during cloud automation. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 7: List Methods — Modification

### 7a. Define a list

```python
mountains = ["everest", "k2", "kangchenjunga", "lhotse", "makalu", "satpuda"]
print(mountains)
```

 [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### 7b. `append()` — Add to end

```python
mountains.append("mount oregon")
print(mountains)
```

**Expected:** `"mount oregon"` appears at the end of the list. Unlike string methods, this **modifies the list in place** — no need to capture a return value. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### 7c. `extend()` — Merge another list

```python
mountains.extend(["mount fuji", "mount kilimanjaro"])
print(mountains)
```

All elements from the second list are added individually to the end. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### 7d. `insert()` — Add at specific position

```python
mountains.insert(2, "mount abu")
print(mountains)
```

| Argument      | Meaning                               |
| ------------- | ------------------------------------- |
| `2`           | Index position to insert at (0-based) |
| `"mount abu"` | The item to insert                    |

Elements at position 2 and beyond shift right by one. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### 7e. `pop()` — Remove from end or by index

```python
mountains.pop()      # removes last element
mountains.pop(5)     # removes element at index 5
print(mountains)
```

 [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

⚠️ **Expert Note**
Every time you run the script, the list is **re-initialized** from its definition line. Previous `append`/`pop` operations do not persist between runs. All operations execute fresh each time. This is not a bug — it's how script execution works. Each run is a clean slate. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 8: Dictionary Methods

### 8a. Define a dictionary

```python
devops = {"name": "Nithish", "skill": "DevOps", "code": "Python"}
```

### 8b. `keys()` and `values()`

```python
print(devops.keys())    # dict_keys(['name', 'skill', 'code'])
print(devops.values())  # dict_values(['Nithish', 'DevOps', 'Python'])
```

 [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

### 8c. `clear()` — Empty the dictionary

```python
devops.clear()
print(devops)   # {}
```

Removes all key-value pairs. The dictionary object still exists but is empty. This is an **in-place** operation. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

**Other methods available** (shown via PyCharm dot-autocomplete, not demonstrated in detail): `pop`, `copy`, `get`, `items`, `popitem`. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

## Step 9: Tuples — Why There's Almost Nothing Here

```python
my_tuple = (1, 2, 3)
# No append, insert, pop, clear — tuples are immutable
```

Tuples have very few methods because they cannot be modified after creation. The video skips them deliberately. [\[210-built-...or-methods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/210-built-in-functions-or-methods.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Taxonomy

```
Python Built-in Functions (standalone)     │  Data Type Methods (dot-notation)
  print(), type(), str(), input(),         │  Called on variable: variable.method()
  len(), dir()                             │  Specific to each data type
                                           │
  Called as: function(argument)             │  String methods → return NEW value (immutable)
                                           │  List methods   → modify IN PLACE (mutable)
                                           │  Dict methods   → modify IN PLACE (mutable)
                                           │  Tuple methods  → almost none (immutable)
```

***

## Mutability → Method Behavior

```
IMMUTABLE (string, tuple):
  method() → returns NEW object
  original unchanged
  MUST capture return value: var = var.method()

MUTABLE (list, dict):
  method() → modifies object IN PLACE
  original IS changed
  No need to capture: var.method() is sufficient
```

***

## Method Discovery

```
Option 1: print(dir(variable))     → list of all method names (any data type)
Option 2: variable. (in PyCharm)   → autocomplete popup with methods
Option 3: W3Schools docs           → methods + examples by data type
```

***

## String Methods Map

```
TRANSFORMATION          VALIDATION (→ bool)        SEARCH              ASSEMBLY
─────────────           ───────────────────        ──────              ────────
.capitalize()           .islower()                 .find("sub")        "sep".join(seq)
.upper()                .isupper()                   → index (0-based)    → joins elements
.lower()                .isalnum()                   → -1 if not found    with separator
                        .isalpha()
                        .isascii()                 find + slice:
                        .isdecimal()               start = .find("x")
                        .isdigit()                 result = s[start:start+len("x")]

⚠️ ALL return new values — original string NEVER modified
```

***

## List Methods Map

```
ADD                          REMOVE
───                          ──────
.append(item)     → end      .pop()        → remove last
.extend([list])   → end      .pop(index)   → remove at position
.insert(idx,item) → position

append vs extend:
  .append([a,b])  → adds [a,b] as ONE element (nested list)
  .extend([a,b])  → adds a and b as SEPARATE elements

⚠️ ALL modify list IN PLACE — original list IS changed
⚠️ Script re-run = list re-initialized from definition (no persistence)
```

***

## Dictionary Methods Map

```
READ                    MODIFY
────                    ──────
.keys()   → all keys   .clear()    → empty entire dict
.values() → all values  .pop(key)   → remove by key
                        .copy()     → shallow copy
Also: .get(), .items(), .popitem()
```

***

## `find()` + Slice Pattern (DevOps Operational)

```
string = "...some data from API..."

index = string.find("target")
  ├── index >= 0 → found at position
  │     └── slice: string[index : index + len("target")]
  └── index == -1 → not found (traversed entire string, no match)
```

***

## `join()` Pattern (DevOps Operational)

```
parts = ("192", "168", "1", "14")

".".join(parts)   → "192.168.1.14"    (IP address)
"/".join(parts)   → "192/168/1/14"    (path-like)
"-".join(parts)   → "192-168-1-14"    (identifier)

Called on SEPARATOR, not on data
Sequence elements MUST be strings
```

***

## DevOps Use Case Flow

```
Cloud automation / API call / Command output
    │
    ▼
Receive raw data (string)
    │
    ├── Validate: .islower(), .isalnum(), .isdigit()  → proceed or reject
    ├── Search:   .find("pattern")                    → locate within data
    ├── Extract:  string[start:end]                   → slice out needed part
    ├── Transform: .upper(), .lower(), .capitalize()  → normalize format
    └── Assemble: "sep".join(parts)                   → build formatted output
    │
    ▼
Use processed data for further operations
```

***

## Data Type → Available Methods (Mental Index)

```
String:  capitalize, upper, lower, islower, isupper, isalnum, find, join, + many more
List:    append, extend, insert, pop, + more
Tuple:   (almost nothing — immutable)
Dict:    keys, values, clear, pop, copy, get, items, popitem
```

***

## Key Conceptual Anchors

| Concept                      | Rule                                                                     |
| ---------------------------- | ------------------------------------------------------------------------ |
| Immutable types (str, tuple) | Methods return new objects; originals untouched                          |
| Mutable types (list, dict)   | Methods modify in place; originals changed                               |
| `dir()`                      | Universal method discovery for any data type                             |
| `find()` returns -1          | -1 = not found (reached end of string without match)                     |
| `join()` syntax              | Called on separator: `"sep".join(sequence)` — NOT `sequence.join("sep")` |
| Script re-execution          | Variables re-initialize every run; mutations don't persist               |

***

## Project Continuity

```
BEFORE: Learned data types — string, list, tuple, dictionary (structure + access)
THIS:   Learned methods to MANIPULATE each data type (transform, search, validate, modify)
NEXT:   Writing custom functions (user-defined functions)
```

***

This completes the full reconstruction. **Theory** builds understanding of mutability, method vs. function, and data-type-specific behavior. **Practical** gives you every method call with exact syntax and expected outputs. The **Compression Map** lets you rapidly look up any method, recall the mutability rule, or reconstruct the DevOps data-processing pattern. Let me know if you'd like Anki flashcards or want any section expanded! 🚀
