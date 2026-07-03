# 🎓 Deep Learning Material: Python Functions Part 2 — Variable Length Arguments (`*args` & `**kwargs`)

**Source:** [212-functions-part-2.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt?EntityRepresentationId=c14125e0-e927-4398-9808-0726596a6cd8) — Video caption reconstruction covering Python variable length arguments: `*args` (non-keyword, stored as tuple), `**kwargs` (keyword, stored as dictionary), iterating and processing both types, combining them in a single function, and using the `random` module (`randint`, `choice`) for practical processing logic. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: Fixed Argument Count Is Too Rigid

Up to this point, functions have been defined with a fixed number of parameters. If a function expects two arguments, you must pass exactly two — no more, no less. But many real-world operations don't have a predictable input count. If you're building a function that processes a food order, you don't know in advance whether the user will order one item or ten. If you're building a function that takes time values, you might get three numbers or thirty. You need a mechanism that allows a function to **accept any number of arguments** and then process however many it receives. Python provides two such mechanisms: `*args` for positional arguments and `**kwargs` for keyword arguments. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## 1.2 `*args` — Non-Keyword Variable Length Arguments

When you prefix a parameter name with a single star (`*`), Python collects all **extra positional arguments** passed to the function and packs them into a **tuple**. The conventional name is `args`, but the name itself doesn't matter — what matters is the single star prefix. You could write `*items` or `*values` and it would work identically. The star is the mechanism; the name is just convention. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

Consider the `order_food` function from the video. It starts with one required parameter (`minimum_order`) — the minimum order without which the function cannot proceed. Then `*args` captures everything else:

```python
def order_food(minimum_order, *args):
```

When you call `order_food("salad", "pizza", "biryani", "soup")`, the first argument `"salad"` goes into `minimum_order`. The remaining three — `"pizza"`, `"biryani"`, `"soup"` — are packed into the `args` tuple: `("pizza", "biryani", "soup")`. If you only pass one argument (`order_food("salad")`), `args` is simply an empty tuple `()`. The function works with any count. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

Because `args` is a **tuple**, you can iterate over it with a `for` loop. The video demonstrates this by looping through the ordered items and printing a message for each one:

```python
for item in args:
    print(f"You have ordered {item}")
```

This loop runs as many times as there are extra arguments. Three extra items → three iterations. One extra item → one iteration. Zero → the loop body never executes. The tuple nature of `*args` is not just a storage detail — it determines what operations are available: iteration, indexing, `len()`, unpacking, and any operation valid on tuples. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## 1.3 `**kwargs` — Keyword Variable Length Arguments

While `*args` captures unnamed positional values into a tuple, `**kwargs` (double star) captures **named key-value pairs** into a **dictionary**. Again, the name `kwargs` is convention — the double star is the mechanism. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

In the `time_activity` function, the call looks like this:

```python
time_activity(10, 20, 10, hobby="dance", sport="boxing", fun="driving", work="DevOps")
```

The positional values `10, 20, 10` go into `*args` as a tuple `(10, 20, 10)`. The keyword arguments `hobby="dance"`, `sport="boxing"`, `fun="driving"`, `work="DevOps"` go into `**kwargs` as a dictionary: `{"hobby": "dance", "sport": "boxing", "fun": "driving", "work": "DevOps"}`. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

Because `kwargs` is a dictionary, you access it using dictionary operations:

* `kwargs.keys()` returns all the keys (`hobby`, `sport`, `fun`, `work`).
* `kwargs[key]` returns the value associated with a specific key.
* You can iterate over it, check membership, etc. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

🔍 **Deep Dive**
The video demonstrates that `kwargs.keys()` returns a view object (the instructor says "returns a tuple" — it's actually a dict\_keys view, but for practical purposes it behaves like a sequence of keys). To use it with `random.choice()`, which requires a **list** (a sequence type), the instructor explicitly wraps it: `list(kwargs.keys())`. This conversion step is important — `random.choice()` operates on sequences with indexing support, and a `dict_keys` object does not support direct indexing. Converting to a list makes it compatible. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## 1.4 Combining `*args` and `**kwargs` in One Function

A single function can accept both `*args` and `**kwargs`. The parameter order must be: regular parameters first, then `*args`, then `**kwargs`. In the `time_activity` example:

```python
def time_activity(*args, **kwargs):
```

When called with `time_activity(10, 20, 10, hobby="dance", sport="boxing", fun="driving", work="DevOps")`, Python separates the inputs automatically: all bare positional values go into `args` (tuple), all `key=value` pairs go into `kwargs` (dictionary). The function then processes both collections independently — summing the numerical tuple and randomly selecting from the dictionary keys. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

This pattern allows a function to handle **arbitrarily complex input** — any number of unnamed values plus any number of named key-value pairs — all in a single function signature. It's the most flexible argument pattern Python offers. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## 1.5 The `random` Module — `randint()` and `choice()`

The video introduces the `random` module through practical use inside the `time_activity` function. Two methods are used:

**`random.randint(a, b)`** — Returns a random integer between `a` and `b` (inclusive on both ends). In the video: `random.randint(0, 60)` generates a random integer from 0 to 60. This value is added to the sum of all `*args` values to create a variable total. The instructor runs the function multiple times and gets different results each time (72, 44, 90) — demonstrating the randomness. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

**`random.choice(sequence)`** — Takes a list (or any sequence) and returns a single randomly selected element from it. In the video, the sequence is `list(kwargs.keys())` — the list of activity names. `random.choice()` picks one at random (e.g., `"hobby"`, `"sport"`, `"fun"`, or `"work"`), and that chosen key is then used to look up its value from `kwargs`. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

The module must be imported before use with `import random`. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## 1.6 The `sum()` Built-in Function

The video uses `sum(args)` to add up all the integer values in the `*args` tuple. `sum()` is a Python built-in that takes an iterable of numbers and returns their total. Since `args` is a tuple of integers `(10, 20, 10)`, `sum(args)` returns `40`. This is then combined with the random integer to produce the final minute value. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## 1.7 Dictionary Value Access via Variable Key

A subtle but important pattern appears in the final output message. The variable `choice` holds a randomly selected key (e.g., `"hobby"`). To get the **value** associated with that key, the instructor writes `kwargs[choice]`. If `choice` is `"hobby"`, then `kwargs[choice]` evaluates to `kwargs["hobby"]`, which returns `"dance"`. This is standard dictionary bracket-access, but the key is a variable, not a hardcoded string. This dynamic lookup is what makes the function's output different every run — a random key selects a random activity, and the associated value (the activity name) is displayed in the message. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building two Python functions that demonstrate variable length arguments. The first function (`order_food`) takes a minimum order plus any number of additional items using `*args`. The second function (`time_activity`) takes any number of time values via `*args` and any number of named activities via `**kwargs`, then uses the `random` module to produce a randomized output. The final outcome: understanding how to write, call, and process functions that accept flexible input counts. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## Example 1: `order_food` — Using `*args`

### Step 1: Define a Basic One-Argument Function

```python
def order_food(minimum_order):
    print(f"{minimum_order} will be delivered in 30 minutes. Enjoy the party!")
```

Call it:

```python
order_food("salad")
```

**Output:** `salad will be delivered in 30 minutes. Enjoy the party!` [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

This works, but only accepts exactly one argument. Passing more would cause an error.

***

### Step 2: Add `*args` for Additional Items

```python
def order_food(minimum_order, *args):
    print(f"{minimum_order} will be delivered in 30 minutes. Enjoy the party!")
    print(args)
```

Call with multiple arguments:

```python
order_food("salad", "pizza", "biryani", "soup")
```

**What happens internally:**

* `"salad"` → assigned to `minimum_order` (first positional parameter)
* `"pizza"`, `"biryani"`, `"soup"` → packed into `args` as a tuple: `("pizza", "biryani", "soup")`

**Output of `print(args)`:** `('pizza', 'biryani', 'soup')` — confirms it is a **tuple**. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

### Step 3: Iterate Over `*args`

Since `args` is a tuple, loop through it:

```python
def order_food(minimum_order, *args):
    for item in args:
        print(f"You have ordered {item}")
    print(f"{minimum_order} will be delivered in 30 minutes. Enjoy the party!")
```

```python
order_food("salad", "pizza", "biryani", "soup")
```

**Output:**

```
You have ordered pizza
You have ordered biryani
You have ordered soup
salad will be delivered in 30 minutes. Enjoy the party!
```

 [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

The loop runs three times — once for each item in `args`. The `minimum_order` is processed separately because it's a named parameter, not part of `*args`.

**Key point:** `*args` is called a **non-keyword variable length argument** because the extra values are passed by position (not by name). [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

## Example 2: `time_activity` — Using `*args` and `**kwargs` Together

### Step 1: Define the Function and Understand the Call

First, understand how the function will be called:

```python
time_activity(10, 20, 10, hobby="dance", sport="boxing", fun="driving", work="DevOps")
```

| Input                                                         | Goes Into  | Type                                                                              |
| ------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------- |
| `10, 20, 10`                                                  | `*args`    | Tuple: `(10, 20, 10)`                                                             |
| `hobby="dance", sport="boxing", fun="driving", work="DevOps"` | `**kwargs` | Dict: `{"hobby": "dance", "sport": "boxing", "fun": "driving", "work": "DevOps"}` |

 [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

### Step 2: Define the Function Skeleton and Print Inputs

```python
def time_activity(*args, **kwargs):
    print(args)
    print(kwargs)
```

**Output:**

```
(10, 20, 10)
{'hobby': 'dance', 'sport': 'boxing', 'fun': 'driving', 'work': 'DevOps'}
```

 [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

**Verification:** `args` is a tuple of integers. `kwargs` is a dictionary of string key-value pairs. This confirms the separation is working correctly.

**Common mistake:** Using a single star for kwargs (`*kwargs` instead of `**kwargs`). Single star captures positional values into a tuple. Double star captures keyword arguments into a dictionary. The star count is the mechanism. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

### Step 3: Import `random` and Process `*args`

```python
import random

def time_activity(*args, **kwargs):
    minute = sum(args) + random.randint(0, 60)
    print(minute)
```

| Part                    | Meaning                                                 |
| ----------------------- | ------------------------------------------------------- |
| `sum(args)`             | Adds all integers in the tuple: `10 + 20 + 10 = 40`     |
| `random.randint(0, 60)` | Generates a random integer between 0 and 60 (inclusive) |
| `+`                     | Adds the random value to the sum                        |
| `minute`                | Stores the total                                        |

**Output (varies each run):** `72`, `44`, `90`, etc. — because the random component changes. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

### Step 4: Randomly Pick an Activity from `**kwargs`

```python
choice = random.choice(list(kwargs.keys()))
print(choice)
```

| Part                 | Meaning                                                                     |
| -------------------- | --------------------------------------------------------------------------- |
| `kwargs.keys()`      | Returns the dictionary keys: `dict_keys(['hobby', 'sport', 'fun', 'work'])` |
| `list(...)`          | Converts to a list (required by `random.choice`)                            |
| `random.choice(...)` | Picks one element randomly from the list                                    |
| `choice`             | Stores the randomly selected key (e.g., `"sport"`)                          |

 [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

### Step 5: Build the Final Output Message

```python
import random

def time_activity(*args, **kwargs):
    minute = sum(args) + random.randint(0, 60)
    choice = random.choice(list(kwargs.keys()))
    print(f"You have to spend {minute} minutes for {kwargs[choice]}")

time_activity(10, 20, 10, hobby="dance", sport="boxing", fun="driving", work="DevOps")
```

| Part                                | Meaning                                                                                         |
| ----------------------------------- | ----------------------------------------------------------------------------------------------- |
| `kwargs[choice]`                    | Looks up the **value** for the randomly chosen key. If `choice` is `"hobby"`, returns `"dance"` |
| `f"...{minute}...{kwargs[choice]}"` | Constructs the final message with both random values                                            |

 [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

**Sample outputs across multiple runs:**

```
You have to spend 96 minutes for driving
You have to spend 92 minutes for driving
You have to spend 70 minutes for DevOps
You have to spend 52 minutes for dance
You have to spend 57 minutes for boxing
```

Both the number of minutes and the activity change on each run because both are randomly determined. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

**Connection to larger flow:** This is the complete demonstration of `*args` and `**kwargs` working together in a single function. The video concludes by stating that this covers functions, and the next topic is **modules**. [\[212-functions-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/212-functions-part-2.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Mechanism

```
*args   → single star  → captures EXTRA positional args → stored as TUPLE
**kwargs → double star → captures EXTRA keyword args    → stored as DICTIONARY

Star count = mechanism. Name = convention (args/kwargs).
```

***

## Argument Routing

```
def func(required, *args, **kwargs):

func("a", "b", "c", x=1, y=2)
      │     │    │    │    │
      ▼     └──┬─┘    └──┬─┘
  required   args       kwargs
   = "a"   = ("b","c")  = {"x":1, "y":2}

Order: required params → *args → **kwargs
```

***

## Data Type → Available Operations

```
*args (tuple):
  ├── iterate:    for item in args
  ├── sum:        sum(args)
  ├── index:      args[0]
  └── length:     len(args)

**kwargs (dictionary):
  ├── keys:       kwargs.keys()
  ├── values:     kwargs.values()
  ├── access:     kwargs[key]       ← key can be a variable
  └── iterate:    for k, v in kwargs.items()
```

***

## `random` Module — Two Methods Used

```
random.randint(a, b)     → random integer in [a, b] inclusive
random.choice(sequence)  → random element from a list
                            ⚠️ requires list, not dict_keys
                            fix: list(kwargs.keys())
```

***

## Example 1: `order_food` Flow

```
order_food("salad", "pizza", "biryani", "soup")
              │          │
        minimum_order    *args = ("pizza", "biryani", "soup")
              │                        │
        processed         for item in args → print each
        separately
```

***

## Example 2: `time_activity` Flow

```
time_activity(10, 20, 10, hobby="dance", sport="boxing", fun="driving", work="DevOps")
                │                              │
          *args = (10,20,10)             **kwargs = {hobby:dance, sport:boxing, ...}
                │                              │
        sum(args) = 40                  kwargs.keys() → list → random.choice → key
                │                              │
      + randint(0,60) = random_num      kwargs[key] → value (activity name)
                │                              │
          minute (total)                 choice (activity)
                │                              │
                └──────────┬───────────────────┘
                           ▼
              "You have to spend {minute} minutes for {activity}"
```

***

## Key Distinctions

```
Single star *    → tuple    → positional values   → non-keyword
Double star **   → dict     → key=value pairs     → keyword

sum()            → built-in → adds iterable of numbers
random.randint() → module   → random int in range
random.choice()  → module   → random pick from list
```

***

## `kwargs.keys()` → `list()` Requirement

```
kwargs.keys()  → dict_keys object (not directly indexable)
                      │
               random.choice() needs indexable sequence
                      │
               list(kwargs.keys()) → converts to list → works
```

***

## Dynamic Dictionary Access Pattern

```
choice = random.choice(list(kwargs.keys()))   ← random KEY
value  = kwargs[choice]                       ← VALUE for that key

key is a variable, not hardcoded string
→ different key each run → different value each run
```

***

## Engineering Patterns

| Pattern                             | Manifestation                                                                                   |
| ----------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Flexible input interface**        | `*args` + `**kwargs` = function accepts any number/type of inputs without signature change      |
| **Automatic type routing**          | Python separates positional vs keyword arguments into tuple vs dict — no manual parsing         |
| **Collection-then-process**         | Collect all inputs first (tuple/dict), then iterate/aggregate — decouples input from processing |
| **Convention over enforcement**     | `args`/`kwargs` names are convention; the star mechanism is what matters                        |
| **Type-driven operation selection** | Tuple → iterate/sum; Dict → key lookup/random select — data type determines processing strategy |

***

## Lecture Continuity

```
BEFORE: Functions basics — fixed arguments, return values
THIS:   Variable length arguments (*args, **kwargs), random module
NEXT:   Modules
```

***

This completes the full reconstruction. **Theory** explains *what* `*args` and `**kwargs` are, *why* they exist, and *how* Python routes arguments into tuples and dictionaries. **Practical** walks through both functions step-by-step with exact code and output. The **Compression Map** lets you reload the entire argument-routing mechanism, data-type operations, and processing flow in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀
