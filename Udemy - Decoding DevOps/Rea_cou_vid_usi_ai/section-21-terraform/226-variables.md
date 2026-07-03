# Terraform Variables — Deep Learning Material

**Source:** Terraform course lecture on Variables (caption file: [226-variables.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt?EntityRepresentationId=c879a401-82b3-484c-80f0-18493a0bfb0d)) [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Are Variables in Terraform and Why Do They Exist?

In Terraform, a **variable** is a named container that holds a value you want to keep separate from the core logic of your infrastructure code. The concept exists to solve three concrete problems that arise the moment you write real infrastructure scripts:

**Problem 1 — Hardcoded Confidential Data.** If you write your AWS access key or secret key directly inside your `.tf` files, anyone who reads your code (or your version control history) can see those credentials. Variables let you extract sensitive values out of the main script and manage them separately — or better yet, not put them in code at all.

**Problem 2 — Environment-Specific Values.** Infrastructure values change depending on *where* and *for what* you're deploying. The AWS region, the AMI ID, the availability zone, the instance type — all of these shift when you move from development to production, or from one AWS region to another. Without variables, you'd have to manually hunt through your code and change every hardcoded value each time.

**Problem 3 — Code Reusability.** If you want to reuse the same Terraform code across different projects or environments, hardcoded values make that impossible without heavy editing. Variables let you write the logic once and simply swap the values. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

The core engineering idea here is **separation of concerns**: the *logic* of what infrastructure to create stays in one place, while the *values* that drive that logic live in a separate, easily swappable layer.

***

## 1.2 — Variable Definition Syntax

A Terraform variable is declared using a specific block structure:

```hcl
variable "VARIABLE_NAME" {
  default = "value"
}
```

The keyword `variable` tells Terraform you are declaring an input variable. The name in quotes (`"VARIABLE_NAME"`) is how you'll reference this variable throughout your code. Inside the curly braces, `default` assigns the value that Terraform will use if no other value is explicitly provided at runtime.

For example:

```hcl
variable "REGION" {
  default = "us-east-1"
}
```

This declares a variable called `REGION` whose default value is `us-east-1`. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

> 🔍 **Deep Dive**
> The `default` value is what makes a variable *optional* during execution. If you omit `default`, Terraform will interactively prompt you for the value during `terraform plan` or `terraform apply`. In automated pipelines, a missing default with no supplied value will cause a failure — which is why defaults are common for non-sensitive values.

***

## 1.3 — Referencing Variables: The `var.` Prefix

Once a variable is declared, you reference it anywhere in your Terraform code using the syntax:

```
var.VARIABLE_NAME
```

For example, if you have `variable "REGION" { default = "us-east-1" }` in your `vars.tf`, then in `providers.tf` you write `region = var.REGION`. Terraform will resolve `var.REGION` to `"us-east-1"` at execution time. The `var.` prefix is Terraform's way of telling the engine: "this is not a literal string — go look up the value from the declared variables." [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

This referencing mechanism is what makes the entire variable system work. You declare once, reference many times, and change in one place.

***

## 1.4 — File Organization: Separating Concerns Across `.tf` Files

Terraform reads **all `.tf` files** in a directory as a single configuration. This means you can split your code across multiple files for organizational clarity without changing how Terraform processes it. The video establishes a clean file structure:

| File               | Responsibility                                                   |
| ------------------ | ---------------------------------------------------------------- |
| `providers.tf`     | Provider configuration (AWS region, authentication)              |
| `vars.tf`          | All variable declarations                                        |
| `instance.tf`      | Resource definitions (EC2 instances, etc.)                       |
| `terraform.tfvars` | Actual values for sensitive variables (access keys, secret keys) |

The key insight: **Terraform doesn't care about file names** — it merges everything in the directory. But humans care. Separating provider logic, variable declarations, and resource definitions into distinct files makes the codebase navigable, maintainable, and less error-prone. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

> ⚠️ **Expert Note**
> The video explicitly warns: **do not put your access key and secret key in your scripts or code.** The `terraform.tfvars` file is mentioned as an option, but the strong recommendation is to avoid embedding credentials entirely. In production, you'd use IAM roles, environment variables, or a credentials file managed outside of Terraform. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

***

## 1.5 — Variable Types: String, List, Map, Boolean

Terraform supports multiple variable types. The video mentions four:

**String** — The simplest type. Holds a single text value. This is the default when you write `default = "us-east-1"`. Most basic variables (region, zone, instance type) are strings.

**List** — An ordered collection of values. Declared as `list(string)` and populated with comma-separated values. Useful when you need multiple values of the same kind (e.g., a list of allowed availability zones).

**Map** — A dictionary / hash of key-value pairs. This is the most important non-trivial type covered in the video and gets its own dedicated section below. Maps let you do **value lookups** based on a key.

**Boolean** — A `true` / `false` value. Useful for feature flags or conditional behavior. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

***

## 1.6 — Map Variables: The Lookup Mechanism (Core Concept)

This is the most architecturally important variable concept in the video. A **map variable** stores multiple key-value pairs, and you retrieve a specific value by supplying the correct key.

**Why it exists:** AMI IDs are region-specific. The same Ubuntu image has a *different* AMI ID in `us-east-1` vs `us-east-2`. If you hardcode one AMI ID and later change your region, your deployment breaks. A map variable solves this by storing AMI IDs for *all* your target regions in one place, and then automatically selecting the correct one based on the current region.

**Declaration syntax:**

```hcl
variable "amiID" {
  type = map
  default = {
    us-east-1 = "ami-0abcdef1234567890"
    us-east-2 = "ami-0fedcba0987654321"
  }
}
```

The `type = map` tells Terraform this variable holds key-value pairs. Inside `default`, each line is a `key = value` pair. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

**Access syntax:**

```hcl
ami = var.amiID[var.REGION]
```

This is the critical line. Let's trace the resolution:

1. Terraform evaluates `var.REGION` → resolves to `"us-east-1"` (from the REGION variable's default).
2. The expression becomes `var.amiID["us-east-1"]`.
3. Terraform looks up key `"us-east-1"` inside the `amiID` map → finds the corresponding AMI ID.
4. That AMI ID is used for the EC2 instance.

If you later change `REGION` to `us-east-2`, the *same code* automatically picks the `us-east-2` AMI. No code changes needed — only the region variable changes. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

> 🔍 **Deep Dive**
> The video draws a direct analogy to **Python dictionaries**: the map variable *is* a dictionary, the variable name is the dictionary name, and the key inside square brackets selects the value. `var.amiID[var.REGION]` is equivalent to `amiID[region]` in Python. If you supply a key that doesn't exist in the map, Terraform will throw an error at plan time — it won't silently default to anything.

The engineering pattern here is powerful and reusable: **parameterized lookup**. Instead of writing conditional logic ("if region is X, use AMI Y"), you store the mapping data declaratively and let the lookup mechanism handle selection. This is cleaner, more scalable (just add more key-value pairs for new regions), and eliminates branching logic.

***

## 1.7 — Additional Variable Arguments

The video briefly references the official Terraform documentation, which lists several arguments you can attach to a variable declaration beyond `default`:

* **`type`** — Constrains the variable to a specific type (`string`, `list(string)`, `map`, `bool`, etc.). Terraform will reject values that don't match.
* **`description`** — A human-readable explanation of the variable's purpose. Shown during prompts and in documentation.
* **`sensitive`** — When set to `true`, Terraform suppresses the variable's value from CLI output. Use this for secrets or credentials you don't want printed during `plan` or `apply`.
* **`validation`** — Allows custom validation rules.

The video also mentions that during `terraform apply`, you can specify a **custom var-file location** using `-var-file=path/to/file.tfvars`. This is useful when your variable values file lives in a different directory or when you maintain separate `.tfvars` files for different environments (dev, staging, prod). [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

> ⚠️ **Expert Note**
> The `sensitive = true` flag only hides values from Terraform's *own* CLI output. It does **not** encrypt the value in the state file. In production, your state file still contains sensitive data in plaintext unless you use remote state with encryption (e.g., S3 backend with server-side encryption).

***

## 1.8 — Terraform Validate: Catching Variable Errors Early

`terraform validate` checks your configuration for syntax errors and internal consistency *without* contacting any cloud provider. This is where mismatched variable names get caught.

The video demonstrates a real error: the code referenced `var.zone`, but the declared variable was named `zone1`. Terraform's validate command caught this and even suggested the correct name:

```
An input variable with the name 'zone' has not been declared.
Did you mean 'zone1'?
```

This teaches an important operational principle: **variable names must match exactly between declaration and reference**. Terraform is case-sensitive and has no fuzzy matching at runtime — though `validate` will suggest close matches to help you debug. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are restructuring an existing Terraform project (Exercise2) to use **variables** instead of hardcoded values. By the end, we'll have a cleanly separated codebase where provider configuration, variable declarations, and resource definitions live in distinct files — and AMI selection is driven dynamically by a map variable tied to the region. The final outcome: a Terraform configuration that can be repointed to a different AWS region by changing a single variable value.

***

## Step 1 — Copy the Previous Exercise as a Starting Point

We begin by duplicating the existing Exercise2 directory to create Exercise3, preserving the working code while giving us a clean workspace for modifications.

**Action:** In your IDE (e.g., VS Code), right-click the `Exercise2` folder → **Copy**, then right-click in the file explorer → **Paste**, then right-click the pasted folder → **Rename** to `Exercise3`. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

At this point, Exercise3 contains the same `instance.tf` (and possibly `providers.tf`) from the previous exercise, with hardcoded values.

***

## Step 2 — Create `vars.tf` and Declare Initial Variables

**Action:** Right-click on the `Exercise3` folder → **New File** → name it `vars.tf`.

Start with two variables — `region` and `zone1`:

```hcl
variable "REGION" {
  default = "us-east-1"
}

variable "zone1" {
  default = "us-east-1a"
}
```

* `variable` — keyword to declare a Terraform input variable.
* `"REGION"` / `"zone1"` — the name you'll use to reference this variable via `var.REGION` or `var.zone1`.
* `default` — the value Terraform uses if none is supplied at runtime.

**Why two separate variables?** Region controls the AWS region for the provider. Zone controls the specific availability zone for the EC2 instance. They are related but serve different configuration points. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

***

## Step 3 — Replace Hardcoded Values with Variable References

### In `providers.tf`:

Replace the hardcoded region string with:

```hcl
region = var.REGION
```

### In `instance.tf`:

Replace the hardcoded availability zone with:

```hcl
availability_zone = var.zone1
```

**Save both files.** Terraform resolves `var.REGION` and `var.zone1` at execution time by looking up the declarations in `vars.tf`. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

**⚠️ Critical detail the video highlights:** The instructor initially wrote `var.zone` instead of `var.zone1` — a typo that caused a validation error. Variable reference names must **exactly match** the declared variable names.

***

## Step 4 — Format and Validate

Open terminal and navigate to the Exercise3 directory:

```bash
cd Exercise3
```

### 4a — Format

```bash
terraform fmt
```

* `terraform` — the CLI tool.
* `fmt` — the format subcommand. It automatically rewrites `.tf` files to canonical Terraform style (indentation, alignment, spacing).

The output will list any files it reformatted. In this case, `vars.tf` was corrected. **Save the reformatted file** if your IDE doesn't auto-reload. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

### 4b — Validate

```bash
terraform validate
```

* `validate` — checks configuration for internal consistency (correct syntax, matching variable names, valid references) **without** contacting AWS.

**First run — error scenario:**

```
Error: Reference to undeclared input variable
  on instance.tf line 6:
  An input variable with the name 'zone' has not been declared.
  Did you mean 'zone1'?
```

**Fix:** Change `var.zone` to `var.zone1` in `instance.tf`. Save. Re-run:

```bash
terraform validate
```

**Expected output:** `Success! The configuration is valid.` [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

**Operational lesson:** Always run `terraform validate` after any code change and before `terraform plan`. It catches naming mismatches, syntax errors, and type errors at zero cost (no API calls, no state changes).

***

## Step 5 — Plan (First Pass, String Variables Only)

```bash
terraform plan
```

* `plan` — Terraform compares the desired state (your `.tf` files) against the current state and shows what changes it would make.

Since the previous exercise deleted all resources, the plan shows **9 resources to add**. This confirms the variable references are resolving correctly — Terraform can build a valid execution plan.

**We do NOT apply yet.** The video holds off on `apply` to introduce the map variable first. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

***

## Step 6 — Create the Map Variable for AMI IDs

### 6a — Find Your AMI IDs from AWS Console

For each region you want to support:

1. Go to the **AWS Console**.
2. Switch to the target region (e.g., `us-east-1`).
3. Navigate to **EC2 → Launch Instance**.
4. Select **Ubuntu**.
5. Copy the **AMI ID** displayed.
6. Repeat for other regions (e.g., switch to `us-east-2`, find its Ubuntu AMI ID).

**Key observation from the video:** Both regions show the same Ubuntu version (e.g., Ubuntu Server 24.04 LTS HVM SSD Volume Type), but their **AMI IDs are different**. This is exactly why the map variable is needed. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

### 6b — Declare the Map Variable in `vars.tf`

Add to your `vars.tf`:

```hcl
variable "amiID" {
  type = map
  default = {
    us-east-1 = "ami-0abcdef1234567890"
    us-east-2 = "ami-0fedcba0987654321"
  }
}
```

* `type = map` — tells Terraform this variable holds key-value pairs, not a single string.
* `default = { ... }` — each line inside the braces is a `region = ami-id` pair.
* Replace the example AMI IDs above with the actual IDs you copied from the AWS console.

### 6c — Reference the Map Variable in `instance.tf`

Replace the AMI line with:

```hcl
ami = var.amiID[var.REGION]
```

**Command breakdown:**

* `var.amiID` — references the map variable.
* `[var.REGION]` — uses the current value of the REGION variable as the lookup key.
* At resolution time: `var.REGION` → `"us-east-1"` → `var.amiID["us-east-1"]` → the corresponding AMI ID. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

**Save all files.**

***

## Step 7 — Format, Validate, and Plan (Final Pass)

```bash
terraform fmt
```

Reformats any files changed during map variable addition.

```bash
terraform validate
```

**Expected:** `Success!` — confirms the map variable declaration and lookup syntax are correct. If a key referenced by `var.REGION` doesn't exist in the map, the error surfaces here.

```bash
terraform plan
```

The plan output confirms Terraform is fetching the correct AMI ID through the map lookup. The validate step already catches variable name mismatches, so if validation passes, the plan will correctly resolve variables. [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

**The video does not apply at this point** — the purpose was to demonstrate variable mechanics, not to provision infrastructure.

> 🔍 **Deep Dive**
> The `terraform plan` output will show the resolved AMI ID in the planned resource attributes. This is your verification point — check that the AMI ID shown matches what you expect for the configured region. If it shows the wrong AMI, either the REGION default is wrong or the map keys don't match.

> ⚠️ **Expert Note**
> The video mentions that the existing code was "smart enough to fetch the latest AMI ID" (likely using a `data` source with `most_recent = true`). The map variable approach is a deliberate trade-off: you lose automatic latest-AMI resolution but gain **explicit control** over which AMI is used in each region. In production, explicit AMI pinning is often preferred because it prevents unexpected OS changes from breaking deployments.

***

## Step 8 — Reference: External Documentation

For additional variable types and arguments, search **"variables in Terraform"** to find the official HashiCorp documentation page for Input Variables. Key things you can explore there:

* `list(string)` type with comma-separated defaults
* `sensitive = true` to suppress values in CLI output
* `description` for documentation
* `validation` blocks for custom constraints
* `-var-file` flag to specify an alternate `.tfvars` file location during apply [\[226-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/226-variables.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Architecture

```
Exercise3/
├── providers.tf    →  Provider config  →  references var.REGION
├── vars.tf         →  All variable declarations (REGION, zone1, amiID, etc.)
├── instance.tf     →  Resource definitions  →  references var.zone1, var.amiID[var.REGION]
└── terraform.tfvars → (Optional) Sensitive values — but DON'T put keys in code
```

***

## Core Variable Mechanics

```
DECLARE:    variable "NAME" { default = "value" }
REFERENCE:  var.NAME
RESOLVE:    Terraform replaces var.NAME → actual value at plan/apply time
```

***

## Variable Types

```
string  →  single value        →  default = "us-east-1"
list    →  ordered collection  →  default = ["a", "b", "c"]
map     →  key-value pairs     →  default = { key1 = "val1", key2 = "val2" }
boolean →  true / false        →  default = true
```

***

## Map Lookup — Resolution Chain

```
var.amiID[var.REGION]
        │         │
        │         └─→ resolves to "us-east-1"
        │
        └─→ var.amiID["us-east-1"] → "ami-0abcdef..."

CHANGE REGION → AUTOMATICALLY PICKS CORRECT AMI → zero code changes
```

**Pattern:** Parameterized lookup eliminates conditional branching. Store mappings declaratively, select via key.

***

## Execution Workflow

```
terraform fmt       →  Auto-format .tf files (cosmetic, no logic change)
         ↓
terraform validate  →  Syntax + internal consistency check (no API calls)
         ↓                catches: wrong variable names, type mismatches
terraform plan      →  Dry-run against provider (shows resolved values)
         ↓                verification point: check AMI ID in output
terraform apply     →  Execute (not done in this exercise)
```

***

## Variable Name Matching Rule

```
Declaration:  variable "zone1" { ... }
Reference:    var.zone1  ✅
              var.zone   ❌  → "Did you mean 'zone1'?"

EXACT MATCH REQUIRED — case-sensitive, no fuzzy resolution at runtime
validate catches mismatches before any cloud interaction
```

***

## Sensitive Data Flow

```
Access Key / Secret Key
  ├── Option: terraform.tfvars  (possible but NOT recommended)
  └── Best: IAM roles / env vars / external credential management
        → NEVER in .tf source code
```

***

## Variable Arguments (Quick Reference)

```
default      →  fallback value (makes variable optional)
type         →  enforce type constraint (string, map, list, bool)
description  →  human-readable purpose
sensitive    →  suppress value from CLI output (NOT encrypted in state)
validation   →  custom rules
```

***

## Reusable Engineering Pattern

```
SEPARATION OF CONCERNS:
  Logic (.tf files)  ←→  Values (variables / .tfvars)
  
  Change environment?  → Change vars only
  Change region?       → Change one variable → map auto-selects dependent values
  Reuse code?          → Same .tf files + different .tfvars per environment

PARAMETERIZED LOOKUP (map variable):
  Problem: Value depends on another value (AMI depends on region)
  Solution: Store all possibilities in map → lookup by key
  Scales: Add new regions by adding map entries, no logic changes
  Anti-pattern: if/else branching for value selection
```

***

## File Responsibility Boundaries

```
providers.tf   →  WHERE to deploy (region, auth)
vars.tf        →  WHAT can change (all variable declarations)
instance.tf    →  WHAT to deploy (resources, referencing vars)
terraform.tfvars → ACTUAL sensitive values (override defaults)
```

**Terraform merges all `.tf` files in a directory → file names are for humans, not for the engine.**

***

## Error → Fix → Verify Loop

```
Edit code → save → terraform fmt → terraform validate → fix errors → re-validate → terraform plan → verify resolved values
                                          ↑                    │
                                          └────────────────────┘
```

***

This concludes the full reconstruction. All three sections are designed to be complementary — Theory for understanding, Practical for execution, and the Compression Map for rapid future recall. Let me know if you'd like me to generate an AnkiDeck CSV from this material or dive deeper into any specific concept! 🚀
