# 📄 YAML & JSON — Data Structures for DevOps — Deep Learning Material

**Source:** *YAML and JSON* (Video Lecture Caption File) [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Problem — Why XML Lost and JSON/YAML Won

The lecture opens by referencing `pom.xml` from the Maven and Jenkins sessions. XML, with its verbose opening/closing tag syntax (`<version>v2</version>`), is **difficult to read and difficult to write**. Every piece of data requires a tag pair, nested tags become deeply indented, and the visual noise of angle brackets and slashes overwhelms the actual data content. The instructor's verdict is sharp: "In today's time if I see any tool using XML format, I'll be really worried." [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

The industry has moved to two better data structures: **JSON** and **YAML**. Both solve the same problem — representing structured data (key-value pairs, lists, nested structures) — but with dramatically less syntax overhead than XML. Understanding these two formats is essential because virtually every modern DevOps tool uses one or both: Ansible playbooks are YAML, Ansible module output is JSON, Terraform can use JSON, Kubernetes manifests are YAML, Docker Compose is YAML, API responses are JSON, and so on.

***

## 1.2 The Foundation — Python Dictionary as the Mental Model

The instructor builds understanding by starting from something already familiar: the **Python dictionary**. If you understand Python dictionaries, you already understand the core data model that both JSON and YAML represent. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

A Python dictionary is a collection of **key-value pairs**. The instructor uses this example with three keys:

* **`DevOps`** — its value is a **list** (e.g., `["Jenkins", "Ansible", "Docker"]`)
* **`development`** — its value is also a **list** (e.g., `["Python", "Java"]`)
* **`ansible_facts`** — its value is a **dictionary** (another set of key-value pairs nested inside)

This example is intentionally designed to show three critical data relationships: a key whose value is a list, another key whose value is a list, and a key whose value is a nested dictionary. These three patterns — **scalar values, lists, and nested dictionaries** — are the building blocks of all structured data in JSON and YAML. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

The instructor emphasizes: "When you're learning Python, it's very important for you to understand Python data types. If you understand that, you will very easily understand JSON and then you'll very easily understand YAML." The learning chain is: **Python dictionary → JSON → YAML**. Each format represents the same underlying data structure, just with different syntax. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

***

## 1.3 JSON — The Vertical Python Dictionary

The transformation from Python dictionary to JSON is remarkably simple. The instructor takes the horizontal, single-line Python dictionary and reformats it **vertically** — placing each key-value pair on its own line with proper indentation. That vertical representation **is** JSON. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

```json
{
  "DevOps": ["Jenkins", "Ansible", "Docker"],
  "development": ["Python", "Java"],
  "ansible_facts": {
    "discovered_python_interpreter": "/usr/bin/python3"
  }
}
```

The structural rules of JSON:

* Data is enclosed in **curly braces `{}`** for dictionaries/objects
* Lists use **square brackets `[]`**
* Keys must be in **double quotes**
* Values can be strings (double-quoted), numbers, booleans, lists, or nested dictionaries
* Key-value pairs are separated by **colons `:`**
* Multiple pairs are separated by **commas `,`**

The instructor notes that PyCharm (or any smart editor) automatically formats JSON properly when you structure it vertically. JSON is now the dominant data interchange format — used in API responses, configuration files, Terraform state files, and virtually every modern tool's output. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

***

## 1.4 YAML — JSON Without the Noise

YAML takes JSON's data model and strips away almost all syntactic ceremony. The instructor converts JSON to YAML by removing:

* **Curly braces** `{}` — replaced by indentation (like Python)
* **Square brackets** `[]` — replaced by hyphen-prefixed list items
* **Double quotes** — optional (only needed for special characters)
* **Commas** — eliminated entirely [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

The same data in YAML:

```yaml
DevOps:
  - Jenkins
  - Ansible
  - Docker
development:
  - Python
  - Java
ansible_facts:
  discovered_python_interpreter: /usr/bin/python3
```

**YAML's core rules:**

**Indentation is structure.** Just like Python, YAML uses whitespace indentation to define nesting. A child element is indented relative to its parent. There are no braces or brackets to delineate scope — indentation is the only mechanism. This means **incorrect indentation breaks the data structure**. Two spaces, three spaces — the specific amount doesn't matter as long as it's consistent, but the instructor demonstrates using consistent spacing. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Lists use hyphens.** Each list item is on its own line, prefixed with a hyphen `-` followed by a **mandatory space** before the element value. The instructor specifically calls out: "after that hyphen, there should be a space." Missing the space is a syntax error. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Key-value pairs use colons.** A key is followed by a colon and a space, then the value. The space after the colon is also mandatory. If the value is a scalar (string, number, boolean), it goes on the same line. If the value is a list or dictionary, the children go on the next lines with increased indentation. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Double quotes are optional.** Unlike JSON where keys and string values must be quoted, YAML doesn't require quotes. You only need them if your value contains special characters that might be misinterpreted. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**The `---` marker.** Three hyphens at the beginning of a file indicate the start of a YAML document. The instructor notes this is **optional** — it just signals "this is where the YAML content begins." The Ansible documentation shows this convention. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

The instructor's reaction captures the universal sentiment: "I know which one you liked. That's everyone's choice. YAML." YAML is the preferred format for human-authored configuration because it's the most readable and the least cluttered. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

🔍 **Deep Dive:**
YAML is technically a superset of JSON — any valid JSON is also valid YAML. But in practice, they're used differently: JSON for machine-generated output and API communication (where strictness and parseability matter), YAML for human-authored configuration files (where readability matters). Ansible uses both: you write playbooks in YAML, but module output is returned in JSON. Understanding both is non-negotiable.

***

## 1.5 Data Types in Context — Scalars, Lists, Dictionaries, and Nesting

The instructor walks through several data type combinations to build fluency: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Scalar values:** A key whose value is a simple string, number, or boolean. Example: `version: 2` (integer), `changed: false` (boolean), `ping: pong` (string). The instructor points out that `changed` is a string key and `false` is a boolean value — understanding the type distinction matters when tools evaluate these values programmatically. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**List of dictionaries:** The Ansible documentation example shows a structure where a list contains two dictionary elements (Martin and Kabita), each with nested key-value pairs. Inside one dictionary, the `skills` key has a list as its value. This demonstrates arbitrary nesting: a list can contain dictionaries, and those dictionaries can contain lists. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

The instructor emphasizes that this nesting can go as deep as needed. The three fundamental types (scalar, list, dictionary) compose together in any combination. Once you internalize these three types and their composition rules, you can read any JSON or YAML file, no matter how complex.

***

## 1.6 Ansible's Use of JSON and YAML — Practical Context

The instructor connects the data format concepts to Ansible specifically: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Ansible playbooks** are written in **YAML** format. This is the configuration you author — the tasks, roles, variables, and handlers that define your automation.

**Ansible module output** is returned in **JSON** format. When you execute an Ansible module (like `ping`), the result comes back as a JSON dictionary. The instructor shows a real output with keys like `ansible_facts`, `changed`, and `ping`. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**The `changed` key** appears in every Ansible module's output. It's a boolean that tells you whether the task execution **modified anything** on the target system. For the `ping` module, `changed` is always `false` because ping is a "soft touch" module — it logs in and comes back without making any changes. But if you install a package or push a configuration file, `changed` will be `true` on the first run (when the change is applied) and `false` on subsequent runs (if the system is already in the desired state). This is Ansible's way of reporting idempotency — the same concept practiced in the Python OS automation lecture. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

⚠️ **Expert Note:**
The `changed` key is operationally important in Ansible because you can use **handlers** — tasks that only run when `changed` is `true`. For example: a handler that restarts a service only triggers when the configuration file task reports `changed: true`. If the config hasn't changed, the restart doesn't happen. This is why understanding the JSON output structure matters — it's not just informational, it drives conditional execution logic.

***

## 1.7 The Learning Chain — Python → JSON → YAML

The instructor explicitly states the pedagogical dependency: understanding Python data types (dictionaries, lists, nesting) is the prerequisite for understanding JSON, and understanding JSON is the prerequisite for understanding YAML. The three formats represent the same underlying data model with decreasing syntactic overhead: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

* **Python dictionary:** Most syntax (braces, brackets, quotes, commas, colons)
* **JSON:** Same structure, formatted vertically for readability
* **YAML:** Least syntax (indentation replaces braces, hyphens replace brackets, quotes optional)

This is why the Python sessions came first in the course — they built the data structure intuition that makes JSON and YAML instantly understandable.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Learning

We are learning to read, write, and mentally convert between three data representation formats: Python dictionaries, JSON, and YAML. There are no infrastructure commands or deployments — this is a conceptual-practical exercise done in a code editor (PyCharm). The outcome is fluency in reading any JSON or YAML file and understanding its data structure at a glance, which is prerequisite for writing Ansible playbooks and reading Ansible output. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

***

## Step 1: Start with a Python Dictionary (Horizontal)

In PyCharm (or any Python-capable editor), write a Python dictionary on a single line: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

```python
{"DevOps": ["Jenkins", "Ansible", "Docker"], "development": ["Python", "Java"], "ansible_facts": {"discovered_python_interpreter": "/usr/bin/python3"}}
```

**What to observe:** This is hard to read. All the data is compressed into one line. You can see the structure if you look carefully — three keys, two with list values, one with a dictionary value — but the horizontal format makes it difficult to parse visually. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Common mistake:** Missing a comma between key-value pairs or mismatching braces. PyCharm highlights these errors, but in a single line, they're easy to miss.

***

## Step 2: Convert to JSON (Vertical Formatting)

Copy the same dictionary and reformat it **vertically** — each key-value pair on its own line, with indentation showing nesting: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

```json
{
  "DevOps": [
    "Jenkins",
    "Ansible",
    "Docker"
  ],
  "development": [
    "Python",
    "Java"
  ],
  "ansible_facts": {
    "discovered_python_interpreter": "/usr/bin/python3"
  }
}
```

**What to observe:** This is the same data. Nothing changed except formatting. PyCharm auto-formats it properly — smart editors understand JSON structure and indent accordingly. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Key syntax elements to verify:**

* All keys in double quotes ✓
* All string values in double quotes ✓
* Lists in `[]` ✓
* Nested dictionary in `{}` ✓
* Commas after each element except the last in a block ✓
* Colons separating keys from values ✓

**The instructor notes:** "And this my friend is JSON." The vertical Python dictionary **is** JSON. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

***

## Step 3: Convert JSON to YAML

Copy the JSON and strip away the syntactic elements: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Remove** curly braces `{}`, square brackets `[]`, double quotes `""`, and commas `,`.

**Replace** list brackets with hyphen-prefixed items. **Maintain** indentation to show nesting.

```yaml
DevOps:
  - Jenkins
  - Ansible
  - Docker
development:
  - Python
  - Java
ansible_facts:
  discovered_python_interpreter: /usr/bin/python3
```

**Syntax verification checklist:**

* No braces, no brackets, no commas ✓
* Keys followed by colon + space ✓
* List items prefixed with `- ` (hyphen + space) ✓
* Nested dictionary content indented under its parent key ✓
* No double quotes (none needed here — no special characters) ✓

**Critical formatting rules:**

* **Space after hyphen:** `- Jenkins` is correct. `-Jenkins` (no space) is a syntax error. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)
* **Space after colon:** `DevOps: value` is correct. `DevOps:value` (no space) may cause parsing issues.
* **Consistent indentation:** All items at the same nesting level must have the same indentation.

**Adding a scalar value:** The instructor adds an integer value to the `ansible_facts` dictionary: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

```yaml
ansible_facts:
  discovered_python_interpreter: /usr/bin/python3
  version: 2
```

`version: 2` — the key is `version`, the value is the integer `2` (no quotes needed for numbers).

***

## Step 4: Read Ansible Module Output (JSON)

The instructor shows real Ansible `ping` module output: [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

```json
{
  "ansible_facts": {
    "discovered_python_interpreter": "/usr/bin/python3"
  },
  "changed": false,
  "ping": "pong"
}
```

**How to read this:**

* `ansible_facts` — key, value is a nested dictionary containing the Python interpreter path discovered on the target machine
* `changed` — key (string), value is `false` (boolean). Indicates the ping module made no changes to the target system. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)
* `ping` — key (string), value is `"pong"` (string). The ping module's response — it successfully reached the target and got a response.

**The `changed` key behavior:**

* **Ping module:** Always `false` — ping is read-only, it makes no modifications. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)
* **Package install (first run):** `true` — the package was installed (a change was made).
* **Package install (second run, same state):** `false` — the package already exists, no change needed.

This maps directly to the idempotency pattern from the Python OS automation lecture: check state → act only if needed → report whether a change occurred.

***

## Step 5: Explore the Ansible YAML Documentation

Google: `ansible YAML syntax`

Find the Ansible documentation page on YAML syntax. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

**Key examples from the documentation:**

**List of fruits:**

```yaml
- Apple
- Orange
- Banana
```

**Dictionary (key-value pairs):**

```yaml
martin:
  name: Martin D'vloper
  job: Developer
  skill: Elite
```

**List of dictionaries:**

```yaml
- martin:
    name: Martin D'vloper
    job: Developer
    skills:
      - python
      - perl
- tabitha:
    name: Tabitha Bitumen
    job: Developer
    skills:
      - lisp
      - fortran
```

**How to read the list of dictionaries:** The top-level structure is a list (two items, each starting with `-`). Each list item is a dictionary. Inside each dictionary, the `skills` key has a list as its value. This is the deepest nesting shown: list → dictionary → key with list value. [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)

The instructor notes: the documentation page is a reference — bookmark it and return to it when you need to verify YAML syntax.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## The Evolution Chain

```
XML (verbose, hard to read/write)
  → JSON (structured, vertical, machine-friendly)
    → YAML (minimal syntax, human-friendly)

Same data model → decreasing syntactic overhead
```

## Learning Dependency Chain

```
Python dictionary → JSON → YAML
  ↑                  ↑       ↑
  understand         same    same data,
  data types         data,   least syntax
  first              vertical
```

## Three Formats — Same Data

```
PYTHON (horizontal):
{"DevOps": ["Jenkins"], "ansible_facts": {"key": "val"}}

JSON (vertical):
{
  "DevOps": ["Jenkins"],
  "ansible_facts": {"key": "val"}
}

YAML:
DevOps:
  - Jenkins
ansible_facts:
  key: val
```

## Syntax Comparison

```
Feature        | Python Dict | JSON          | YAML
─────────────────────────────────────────────────────
Braces {}      | required    | required      | NONE (indentation)
Brackets []    | required    | required      | NONE (- hyphen)
Quotes ""      | required    | required      | optional
Commas ,       | required    | required      | NONE
Colons :       | required    | required      | required (+ space)
```

## Three Fundamental Data Types

```
SCALAR:     key: value          (string, int, bool)
LIST:       key:                (ordered collection)
              - item1
              - item2
DICTIONARY: key:                (nested key-value pairs)
              subkey1: val1
              subkey2: val2

These three compose arbitrarily:
  list of dictionaries
  dictionary with list values
  dictionary with dictionary values
  any depth of nesting
```

## YAML Syntax Rules

```
Indentation = structure (like Python)
Hyphen + space = list item (- item)
Colon + space = key-value separator (key: value)
Quotes = optional (use only for special characters)
--- = optional YAML document start marker
```

## YAML Syntax Traps

```
WRONG: -Jenkins     → missing space after hyphen
RIGHT: - Jenkins    → space after hyphen required

WRONG: key:value    → missing space after colon
RIGHT: key: value   → space after colon required

WRONG: inconsistent indentation → structure breaks
RIGHT: consistent spaces at each nesting level
```

## Ansible Format Usage

```
WRITE in YAML:    playbooks, roles, variables, inventory
READ in JSON:     module output, API responses, facts

Playbook (YAML) → executes on target → returns output (JSON)
```

## Ansible `changed` Key

```
Present in EVERY module output

changed: false → module made NO modifications
changed: true  → module MADE a modification

Behavior by run:
  1st run (state differs):  changed: true
  2nd run (state matches):  changed: false

ping module: always false (read-only, "soft touch")
install pkg: true on first, false if already installed

Same concept as: idempotency check-before-act pattern (Python OS lecture)
```

## Ansible Output Structure

```
{
  "ansible_facts": { ... },     ← discovered system info
  "changed": true/false,         ← did this task modify anything?
  "module_specific_key": "value" ← varies by module (e.g., ping: pong)
}
```

## Documentation Reference

```
Google: "ansible YAML syntax"
→ Ansible docs YAML syntax page
→ Lists, dictionaries, list of dictionaries examples
→ Bookmark for syntax reference
```

## Reusable Engineering Patterns

**1. Data Format Evolution = Syntax Reduction**

```
XML → JSON → YAML
Each generation removes syntactic overhead
Same expressiveness, less visual noise
Pattern: as formats mature, they optimize for human readability

Same progression in other domains:
  Makefiles → Jenkinsfiles → GitHub Actions YAML
  XML configs → JSON configs → YAML configs
```

**2. Three-Type Composition Model**

```
ALL structured data = combinations of:
  Scalar (single value)
  List (ordered collection)
  Dictionary (key-value map)

Master these three → read ANY config file in ANY format
JSON, YAML, TOML, HCL — all express these same three types
```

**3. Write-Format ≠ Read-Format**

```
Ansible: write YAML (human-friendly) → read JSON (machine-friendly)
APIs: send JSON → receive JSON
Terraform: write HCL → state in JSON

Pattern: authoring format optimizes for humans
         output/interchange format optimizes for machines
```

***

*This completes the full reconstruction. Theory explains the data model shared by all three formats and Ansible's usage of both JSON and YAML. Practical walks through the conversion process and reading real Ansible output. The Compression Map enables instant recall of syntax rules, the three-type composition model, and the relationship between YAML authoring and JSON output in Ansible.* [\[235-yaml-and-json \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/235-yaml-and-json.txt)
