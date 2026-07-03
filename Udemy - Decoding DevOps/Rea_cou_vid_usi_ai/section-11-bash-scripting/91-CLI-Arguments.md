# 🐚 Bash Scripting — Command Line Arguments: Making Scripts Reusable

**Source:** Bash Scripting Session — Command Line Arguments (Caption File) [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

This video teaches **command line arguments in bash scripts** — how to pass external values into a script at execution time instead of hardcoding them. The instructor starts with a conceptual bridge from commands you already use (like `ls`, `cp`, `mv` that take arguments), builds understanding with a simple demo script, demonstrates the behavior of undefined variables, and then applies arguments to a **real web deployment script** — transforming a hardcoded script into a **reusable tool** that can deploy any website by simply changing the arguments passed to it. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. The Conceptual Bridge — You Already Use Arguments Every Day

Before the instructor introduces anything new, he anchors the concept in something you already know. Every time you run a Linux command, you often give it **arguments**. When you type `ls /path/to/directory`, the path is an argument to `ls`. When you type `cp source destination`, both the source and destination are arguments to the `cp` command. When you type `mv file1 file2`, those are arguments to `mv`. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

This is the foundational insight: **arguments are values passed to a command at execution time that tell it what to operate on**. You've been using them all along with built-in Linux commands. The question this lecture answers is: **how can your own scripts accept arguments the same way?** How can you write a script that behaves like `ls` or `cp` — where the user provides values at runtime instead of the script having them hardcoded inside?

***

## 2. The Problem — Hardcoded Variables Limit Reusability

In previous sessions (referenced as `3_vars_websetup.sh`), the instructor built a web deployment script that used **variables declared inside the script** to store the URL and artifact name. This worked, but it had a limitation: every time you wanted to deploy a **different** website, you had to **open the script and edit the variable values**. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

This is a real engineering problem. A script that requires manual editing before each use is not truly automated — it's semi-automated. The user must understand the script's internals, find the right lines, change the values correctly, save, and then run. This is error-prone and defeats the purpose of scripting as a hands-off automation tool. Command line arguments solve this by moving the variable values **outside the script** — the user provides them at execution time, and the script receives them dynamically. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

***

## 3. How Command Line Arguments Work in Bash — The `$0` through `$9` System

When you execute a bash script and pass values after the script name, bash automatically stores those values in **special numbered variables**: `$1`, `$2`, `$3`, ... up to `$9`. These are called **positional parameters**. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

The mapping is purely **positional** — the first argument after the script name goes into `$1`, the second into `$2`, the third into `$3`, and so on. You do not declare these variables anywhere in your script. You do not assign values to them. Bash does it automatically based on what the user types on the command line.

**`$0` is special and reserved** — it always contains the **name of the script itself** (or the path used to invoke it). You cannot use `$0` as a user argument. It is always occupied by the script identity. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

So the full mapping when you run `./myscript.sh Linux AWS Docker` is:

| Variable | Value                              |
| -------- | ---------------------------------- |
| `$0`     | `./myscript.sh` (script name/path) |
| `$1`     | `Linux` (first argument)           |
| `$2`     | `AWS` (second argument)            |
| `$3`     | `Docker` (third argument)          |

The instructor explicitly states the usable range: **`$1` to `$9`** for user-supplied arguments, with `$0` reserved for the script name. You can pass more than 9 arguments, but accessing them requires different syntax (not covered in this video). [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

<details>
<summary>🔍 Deep Dive</summary>

The reason bash auto-populates these variables is that the shell performs **argument parsing before script execution begins**. When you type `./script.sh arg1 arg2`, bash splits the command line by whitespace, assigns position 0 to the command itself and positions 1+ to each subsequent token, then starts executing the script with those variables already in scope. This is why you never see a declaration like `$1="something"` inside a script — by the time the script runs, the values are already there. This is the same mechanism the kernel uses when launching any process: the argument vector (`argv`) is populated before `main()` runs in C programs. Bash's `$1`-`$9` is the shell-scripting interface to that same OS-level mechanism.

</details>

***

## 4. Behavior of Undefined or Missing Variables — The Empty Value Principle

The instructor demonstrates a critical behavior before showing arguments: **if you access a variable that has never been declared or assigned a value, bash does not throw an error — it returns an empty string (nothing)**. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

He demonstrates this on the command line: he accesses `$y` (a variable never defined), and bash simply prints nothing. No error, no warning, just blank output. This behavior is the same for positional parameters: if your script uses `$1` and `$2`, but the user only passes one argument, `$2` will be **empty** — not undefined, not an error, just empty.

This is both a feature and a danger. It's a feature because scripts don't crash on missing optional arguments. It's a danger because **if an argument is required and the user forgets it, the script won't warn them** — it will proceed with an empty value, which often causes a confusing failure later in the execution. The instructor explicitly highlights this: if the user doesn't pass the URL argument, the `wget` command will receive an empty URL, "which will throw error at us." The error comes from `wget` failing on empty input, not from bash telling you an argument was missing. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

<details>
<summary>⚠️ Expert Note</summary>

This is why production bash scripts include argument validation at the top — checking if `$1` is empty and printing a usage message if it is (e.g., `if [ -z "$1" ]; then echo "Usage: $0 <url> <artifact>"; exit 1; fi`). The instructor does not add validation in this video (it's a learning exercise), but the implicit lesson is clear: the script "definitely needs" the user to pass the arguments, and there's no built-in safety net. You must build your own.

</details>

***

## 5. From Hardcoded Variables to Command Line Arguments — The Reusability Transformation

The instructor takes an existing web deployment script (`3_vars_websetup.sh`) that had the URL and artifact name stored as **hardcoded variables inside the script**, copies it to a new file (`5_args.sh`), and transforms it by: [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

1. **Commenting out** the hardcoded variable declarations (the lines that defined URL and artifact name)
2. **Replacing** every reference to those variables with `$1` (for URL) and `$2` (for artifact name)

That's it. The script's logic is unchanged. The commands are unchanged. The only difference is **where the values come from** — they now come from the command line instead of from inside the script.

The instructor calls the result **"reusable code"** — and this is the key conceptual payoff of the entire lecture. With hardcoded variables, the script could deploy exactly one website. With command line arguments, the **same script can deploy any website** — just pass a different URL and artifact name. The instructor demonstrates this by deploying a completely different website ("Ziggy" from tooplate.com) without changing a single line of the script. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

This transformation — from hardcoded to parameterized — is one of the most important engineering patterns in scripting and software design. The instructor frames it explicitly: **"this is now a reusable code, I can use it to deploy any website I want. And that is some intelligent work there."** [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

***

## 6. The Dollar Sign (`$`) as the Value Extraction Operator

The instructor reinforces a concept from earlier sessions: the `$` symbol in bash is the **value extraction operator**. When you write `$x`, you are saying "give me the value stored in variable `x`." When you write `$1`, you are saying "give me the value stored in positional parameter 1." When you write `$0`, you are saying "give me the value stored in positional parameter 0 (the script name)." [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

The `$` does not create a variable or assign a value — it only **reads** the current value. If no value exists, it reads empty (as demonstrated with the undefined variable `$y`).

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are building two things in this session: first, a **simple demonstration script** (`4_args.sh`) that shows how command line arguments map to numbered variables; second, a **real web deployment script** (`5_args.sh`) that accepts a URL and artifact name as arguments, making it reusable for deploying any website. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Why it matters:** This transforms a single-purpose script into a **general-purpose tool** — the same script deploys any website by simply changing the arguments at runtime.

**Final outcome:** A working web deployment script that the user invokes with a URL and artifact name on the command line, and the script downloads, extracts, and deploys the website automatically.

***

## Step 1: Understanding Undefined Variable Behavior (Command Line Demo)

Before writing any script, the instructor demonstrates variable behavior directly on the command line. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Declare a variable and print it:**

```bash
X=123
echo $X
```

* `X=123` — assigns the value `123` to variable `X`. No spaces around `=` (bash requirement).
* `echo $X` — prints the value of `X`. Output: `123`.

**Access an undefined variable:**

```bash
echo $y
```

* `$y` — variable `y` was never declared. Bash returns **empty** (blank output). No error.

**Why this matters operationally:** This establishes that missing arguments in your script won't cause bash to stop — they'll silently become empty strings, which can cause downstream command failures (like `wget` receiving an empty URL). You must anticipate this.

***

## Step 2: Create the Demonstration Script (`4_args.sh`)

**What we are doing:** Writing a script that prints the values of `$0`, `$1`, `$2`, and `$3` to show how command line arguments are mapped. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Create and edit the script:**

```bash
vim 4_args.sh
```

**Script content:**

```bash
echo "Value of 0 is $0"
echo "Value of 1 is $1"
echo "Value of 2 is $2"
echo "Value of 3 is $3"
```

* Each `echo` statement prints a label and the value of a positional parameter.
* `$0` — will contain the script name.
* `$1`, `$2`, `$3` — will contain whatever the user passes as arguments.
* These variables are **not declared** anywhere in the script. Bash populates them automatically from the command line.

**Make the script executable:**

```bash
chmod +x 4_args.sh
```

* `chmod` — change file permissions.
* `+x` — add execute permission.
* Without this, running `./4_args.sh` would give a "permission denied" error.

**Connection to flow:** The script is now ready to test with and without arguments.

***

## Step 3: Execute Without Arguments — Observe Empty Behavior

```bash
./4_args.sh
```

**Expected output:** [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

```
Value of 0 is ./4_args.sh
Value of 1 is
Value of 2 is
Value of 3 is
```

* `$0` prints `./4_args.sh` — the script name/path (always populated).
* `$1`, `$2`, `$3` are **empty** — no arguments were passed, so bash has nothing to put in them.

**Operational insight:** This confirms the undefined variable behavior from Step 1 — no errors, just empty values. The script ran to completion even though it "expected" arguments.

***

## Step 4: Execute With Arguments — Observe Positional Mapping

```bash
./4_args.sh Linux AWS Docker
```

**Expected output:** [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

```
Value of 0 is ./4_args.sh
Value of 1 is Linux
Value of 2 is AWS
Value of 3 is Docker
```

* `$0` — still the script name.
* `$1` — `Linux` (first argument).
* `$2` — `AWS` (second argument).
* `$3` — `Docker` (third argument).

**Operational insight:** Arguments are mapped purely by **position** — the order you type them determines which variable they land in. The instructor also notes you can pass more arguments than the script uses, but extra ones are simply ignored if the script doesn't reference them.

**Verification:** The output directly shows the mapping. If any value appears in the wrong position, you know the argument order was wrong.

**Connection to flow:** Now that the mapping mechanism is clear, the next step applies it to a real-world script.

***

## Step 5: Create the Reusable Web Deployment Script (`5_args.sh`)

**What we are doing:** Copying the existing web deployment script and replacing hardcoded variables with command line arguments. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Copy the base script:**

```bash
cp 3_vars_websetup.sh 5_args.sh
```

* `cp` — copy command.
* `3_vars_websetup.sh` — the source script (has hardcoded URL and artifact name variables).
* `5_args.sh` — the new script we'll modify.

**Edit the new script:**

```bash
vim 5_args.sh
```

**Modifications made:**

1. **Comment out** the hardcoded variable declarations for URL and artifact name (add `#` in front of those lines).
2. **Replace** every occurrence of the URL variable with `$1`.
3. **Replace** every occurrence of the artifact name variable with `$2`.

**What this means operationally:** The script no longer contains any website-specific information. The URL and artifact name will come entirely from what the user types on the command line. The `wget` command that was `wget $URL` now becomes `wget $1`. The extraction/deployment logic that referenced `$ART_NAME` now references `$2`. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Connection to flow:** The script is now parameterized — ready to accept any website URL and artifact name.

***

## Step 6: Obtain the URL and Artifact Name for a New Website

**What we are doing:** Getting the download URL for a different website to prove the script is truly reusable. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

The instructor goes to **tooplate.com**, selects a template called **"Ziggy"**, and obtains the download URL using **browser developer tools**:

1. Open the website (tooplate.com).
2. Choose a template (Ziggy).
3. Press **F12** to open Developer Tools.
4. Go to the **Network** tab.
5. Click the **Download** button on the website.
6. The network tab captures the request — the download URL is visible there.

The instructor also identifies the **artifact name** (the zip file name) from the same network request.

**Operational reasoning:** The URL and artifact name are the two inputs the script needs. Getting them from the browser's network tab is a reliable way to find the exact download URL for any web template. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Connection to flow:** These two values become `$1` and `$2` when running the script.

***

## Step 7: Dismantle the Previous Deployment and Run the New One

**What we are doing:** Cleaning up the previous website deployment (referenced as "dismantling everything") and running the reusable script with the new website's URL and artifact name. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Execute the script:**

```bash
./5_args.sh <URL> <artifact_name>
```

* `./5_args.sh` — run the script (`$0`).
* First argument (the URL) → stored in `$1` → used by `wget` to download.
* Second argument (the artifact name) → stored in `$2` → used to extract and deploy.

**What happens internally:** The script executes the same sequence as the hardcoded version — downloads the artifact with `wget`, extracts it, copies files to the web server directory — but using the values passed from the command line instead of internal variables. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

**Verification:**

1. The script output should show successful download and extraction (the instructor says "looks fine").
2. **Get the server's IP address** and paste it into a browser.
3. The browser should display the new website — "Welcome to Zigi" confirms success.

**Common mistakes:**

* Forgetting to pass an argument → `wget` receives empty URL → download fails.
* Swapping argument order → URL goes into `$2` and artifact name into `$1` → both commands fail.
* Passing the wrong URL (not the direct download link) → `wget` downloads an HTML page instead of the artifact.

**Connection to flow:** The successful deployment of a completely different website **without editing the script** proves the reusability transformation is complete. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

<details>
<summary>⚠️ Expert Note</summary>

In production, this script would need: (1) argument validation at the top to check that `$1` and `$2` are non-empty, (2) a usage message showing the expected format if arguments are missing, (3) error handling after `wget` and extraction steps to stop execution if any step fails, and (4) potentially a `set -e` at the top to auto-exit on any command failure. The instructor's version is intentionally lean for learning, but the gap between this and production-ready is precisely these four additions.

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   Bash Command Line Arguments
CONTEXT: Bash scripting section → evolving from hardcoded vars → parameterized reusable scripts
PURPOSE: Make scripts accept external input at runtime → reusability
```

***

## The Core Mechanism

```
USER TYPES:     ./script.sh  arg1   arg2   arg3
                    ↓          ↓      ↓      ↓
BASH MAPS TO:     $0         $1     $2     $3

$0 = RESERVED (always = script name/path)
$1–$9 = user-supplied arguments (positional, order matters)
No declaration needed — bash auto-populates before script executes
```

***

## The Empty Variable Rule

```
Variable never declared/assigned?
  → Bash returns EMPTY STRING (not error, not null, not warning)
  → Script continues executing
  → Downstream commands receive empty input → THEY fail

IMPLICATION: Missing arguments = silent empty → late, confusing failure
DEFENSE:     Validate arguments at script start (not shown in video, but implied as necessary)
```

***

## The Reusability Transformation

```
BEFORE (hardcoded):
  Script contains:  URL="https://specific-site.com/file.zip"
                    ART_NAME="file.zip"
  Usage:            ./script.sh                    (no args needed)
  Limitation:       Deploy ONLY that one website → must edit script to change

AFTER (parameterized):
  Script contains:  $1 (where URL was)
                    $2 (where ART_NAME was)
  Usage:            ./script.sh <any_url> <any_artifact>
  Capability:       Deploy ANY website → zero script editing

TRANSFORMATION:  Comment out hardcoded vars → replace var references with $1, $2
```

***

## The `$` Operator

```
$ = VALUE EXTRACTION (read-only access to variable content)
$X    → value of variable X
$1    → value of first positional parameter
$0    → value of script name
$y    → empty (if y undefined) — NO ERROR
```

***

## Operational Flow — Web Deployment with Arguments

```
1. Get URL + artifact name (browser DevTools → Network tab → capture download URL)
2. Run: ./5_args.sh <URL> <artifact_name>
       $1 = URL    → wget $1 (download)
       $2 = artifact → extract/deploy $2
3. Verify: get server IP → open in browser → website loads
```

***

## Argument Discovery Method (from video)

```
tooplate.com → pick template → F12 (DevTools) → Network tab → click Download → capture URL
URL      = first argument ($1)
Filename = second argument ($2)
```

***

## Failure Modes

```
Missing argument    → $N = empty → command gets empty input → cryptic failure (not "missing arg" error)
Swapped order       → $1 gets artifact name, $2 gets URL → both commands fail on wrong input
Wrong URL           → wget downloads HTML page → extraction fails
Not executable      → "permission denied" → fix: chmod +x script.sh
```

***

## Reusable Engineering Patterns Extracted

```
1. PARAMETERIZATION          → Move variable values from INSIDE code to OUTSIDE (runtime input)
                               Hardcoded → parameterized = single-use → reusable
2. POSITIONAL INTERFACE      → Order-based contract: caller must know position = meaning
                               ($1=URL, $2=artifact — no labels, pure position)
3. SILENT EMPTY FAILURE      → System doesn't fail at input stage → fails at consumption stage
                               Design defense: validate inputs before using them
4. COPY-THEN-MODIFY          → Don't rewrite from scratch → copy working script → replace only
                               what changes (cp 3_vars → 5_args → swap vars for $1/$2)
5. SAME LOGIC, DIFFERENT DATA→ Script logic is stable; only data varies → separate them
                               (the essence of parameterization)
```

***

## Rapid Recall Triggers

```
"What are command line args?"   → Values passed after script name → auto-stored in $1–$9
"What is $0?"                   → Always the script name/path (reserved, not user input)
"What if arg is missing?"       → $N = empty string, no error, downstream command fails
"Range of positional params?"   → $0 (script name) + $1 to $9 (user arguments)
"How to make script reusable?"  → Replace hardcoded vars with $1, $2... → user passes values at runtime
"How to get download URL?"      → Browser → F12 → Network tab → click download → copy URL
"$ means what in bash?"         → Extract/read the value of the variable that follows
```

***

This completes the full reconstruction of the Command Line Arguments lecture. **Theory** explains the mechanism and engineering reasoning behind parameterization, **Practical** walks through every command and decision in the exact order of the video, and the **Mental Compression Map** compresses everything into fast-recall structures. [\[91-command...-arguments \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/91-command-line-arguments.txt)

Ready for the next caption file, or shall I generate an **AnkiDroid CSV** covering this lecture's key concepts? 🚀
