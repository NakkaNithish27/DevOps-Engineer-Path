# 🎓 Deep Learning Material: Exporting Variables in Bash — Scope, Persistence, and System-Wide Configuration

**Source:** Video lecture on exporting variables in bash shell (from [95-exporting-variables.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt?EntityRepresentationId=e44b42b7-a57d-44a1-bccd-eb8bc809d8eb) caption file) [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Video Context:** This is a hands-on lecture that builds on prior scripting knowledge (the learner has already used variables in scripts). The instructor now addresses the critical gap: variables created in a shell session are **temporary and local** — they die with the shell process. This lecture teaches the complete lifecycle of variable scope: from local → exported (child-shell accessible) → permanent for a user → permanent for all users, using live terminal demonstrations that show each failure and fix in sequence.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Variable Scope in Bash: The Default Is Temporary and Local

Every variable you create in a bash shell has a **scope** — a boundary that defines where that variable is visible and accessible. By default, when you create a variable like `SEASON=Monsoon`, that variable exists **only in the current shell process** and **only for as long as that process is alive**. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

This is the starting point the instructor establishes: *"the scope of those variables are very local. If you log out, if you close the shell, the variables will be gone."* The word "local" here doesn't mean local in the programming-language sense (like inside a function) — it means local to **the specific shell process** you're currently running in. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

To understand why, you need to understand what a shell actually is at the operating system level. When you open a terminal or SSH into a system, the OS starts a **bash process**. This process has its own memory space. Variables you create are stored in that process's memory. When you type `exit`, that process terminates, and its memory is reclaimed by the OS. The variable doesn't "go somewhere" — it simply ceases to exist because the process that held it is dead. The instructor captures this precisely: *"variables are temporary in the process. The process is dead. So Bash Shell was the process that's dead. So variable is gone."* [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

This is the fundamental concept everything else in this lecture builds on: **a variable's lifetime is tied to the lifetime of the shell process that created it.**

***

## 1.2 — Parent Shell and Child Shell: The Inheritance Boundary

When you run a bash script from your current shell, the system does **not** execute that script in your current shell process. Instead, it creates a **new bash process** — a **child shell** — to execute the script. This child shell is spawned by your current shell (the **parent shell**). [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The critical rule is: **variables defined in a parent shell are NOT automatically available in child shells.** The instructor demonstrates this by creating a variable `SEASON=Monsoon` in the parent shell, then running a script (`testvars.sh`) that tries to use `$SEASON`. The script runs in a child shell, and the variable is empty there — it doesn't exist in the child's process memory. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The mechanism behind script execution ties back to the shebang line (`#!/bin/bash`). The instructor reminds: *"what this bin bash is doing here — we know it invokes the interpreter and then executes."* When you run a script, the OS reads the shebang, launches a **new** `/bin/bash` process (the child shell), and that child process executes the script's commands. This new process starts with its own clean environment — it does not automatically inherit the parent's regular variables. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

This is where many beginners get confused. They set a variable, write a script that uses it, and the script can't see it. The variable exists — but in a different process. The child shell is a separate world.

> 🔍 **Deep Dive**
>
> The parent-child shell relationship is a direct consequence of how Unix process creation works. When a script is executed, the parent shell calls `fork()` to create a child process, then `exec()` to replace that child with the script's interpreter. Regular (non-exported) variables live only in the parent process's memory and are **not** copied to the child during `fork()`. Only **environment variables** (exported variables) are copied into the child's environment. This is the OS-level mechanism that the `export` command leverages.

***

## 1.3 — The `export` Command: Making Variables Visible to Child Shells

The `export` command solves the parent-to-child visibility problem. When you run `export SEASON`, you are telling the shell: *"take this variable from my local process memory and place it into my **environment**."* The environment is a special area of process memory that **is** inherited by child processes. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

After exporting, any child shell spawned from the current parent shell will have access to `SEASON`. The instructor demonstrates this: after `export SEASON`, running the `testvars.sh` script successfully prints the variable's value. *"Exporting a variable will make the variable global for all the other child shell."* [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

However — and this is the critical limitation — **exporting does NOT make the variable permanent**. The exported variable still lives in the current shell process's environment. When you `exit` that shell, the process dies, the environment dies, and the exported variable dies with it. The instructor explicitly demonstrates this: after exporting, he logs out, logs back in, and the variable is gone. *"This is still temporary if I log out."* [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

So `export` solves the **scope problem** (parent → child visibility) but does **not** solve the **persistence problem** (surviving across sessions). These are two separate problems, and understanding the distinction is essential.

***

## 1.4 — Making Variables Permanent: The File-Based Persistence Mechanism

Since variables die with their process, the only way to make them "permanent" is to ensure they are **re-created automatically every time a new shell process starts**. Bash provides exactly this mechanism through **startup files** — files that are automatically **sourced** (read and executed) when a user logs in or opens a new shell. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The instructor introduces two levels of persistence:

### Per-User Persistence: `~/.bashrc`

Every user's home directory contains a hidden file called `.bashrc`. When a user logs in (or opens a new interactive shell), bash automatically **sources** this file — meaning it reads the file line by line and executes each line as if you typed it in the shell. If you place `export SEASON=Monsoon` inside `~/.bashrc`, then every time that user logs in, the variable will be automatically created and exported. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The instructor demonstrates this with the root user: he edits root's `.bashrc`, adds `export SEASON=Monsoon`, saves, and then shows that the variable is **not immediately available** — because the file hasn't been sourced yet in the current session. But after logging out and logging back in, the variable is there. *"It's available because the .bashrc file was sourced when the user logged in."* [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The key insight: `.bashrc` is **per-user**. Each user has their own copy. The root user's `.bashrc` only affects root. The vagrant user's `.bashrc` only affects vagrant. The instructor makes this explicit: *"every user will have its own bashrc file"* and *"if I want to make this variable permanent for vagrant user, then I need to edit bashrc file of vagrant user."* [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The instructor also mentions `~/.bash_profile` (and `~/.profile`) as additional per-user startup files that serve a similar purpose. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

### System-Wide Persistence: `/etc/profile`

If you want a variable available to **every user** on the system, editing each user's `.bashrc` individually would be impractical. Instead, you edit `/etc/profile` — a **global** startup file that is sourced for **all users** when they log in. The instructor demonstrates adding `export SEASON=Winter` to `/etc/profile`. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

***

## 1.5 — Sourcing Order and Override Behavior: Who Wins?

This is the most architecturally important concept in the lecture. When a user logs in, **multiple startup files are sourced in a specific order**:

1. **`/etc/profile`** is sourced **first** (system-wide, affects all users)
2. **`~/.bashrc`** is sourced **second** (per-user, affects only that user) [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

Because `.bashrc` is sourced *after* `/etc/profile`, if both files define the same variable with different values, **`.bashrc` wins** — it overrides the value set by `/etc/profile`. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The instructor sets up a brilliant demonstration to prove this: he sets `SEASON=Winter` in `/etc/profile` (global) and `SEASON=Monsoon` in root's `.bashrc` (per-user). Then he tests:

* **Vagrant user** (has no `SEASON` in their `.bashrc`): `echo $SEASON` → `Winter` — the value comes from `/etc/profile` because there's no per-user override. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)
* **Root user** (has `SEASON=Monsoon` in their `.bashrc`): `echo $SEASON` → `Monsoon` — the `.bashrc` value overrides the `/etc/profile` value. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The instructor summarizes the rule: *"/etc/profile file will be sourced and then the bashrc file will be sourced"* — so `.bashrc` always gets the last word for that user. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

> 🔍 **Deep Dive**
>
> This sourcing order creates a **layered configuration system** — a pattern seen throughout Linux and systems engineering. The global layer (`/etc/profile`) establishes defaults. The user layer (`~/.bashrc`) provides overrides. This is the same pattern as global config → user config in tools like Git (`.gitconfig`), SSH (`/etc/ssh/ssh_config` → `~/.ssh/config`), and many others. The general principle is: **system-wide defaults are set globally; individual customization happens at the user level; user-level always overrides system-level.** Understanding this as a pattern (not just a bash feature) gives you transferable architectural knowledge.

***

## 1.6 — Summary of the Variable Persistence Hierarchy

The instructor closes with a clear summary of the options: [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

| Goal                                  | Where to Put `export VAR=value`                  |
| ------------------------------------- | ------------------------------------------------ |
| Available to child shells (temporary) | `export` command in current shell                |
| Permanent for one user                | `~/.bashrc` or `~/.bash_profile` or `~/.profile` |
| Permanent for all users               | `/etc/profile`                                   |

The underlying logic: you cannot make a variable truly "permanent" — you can only ensure it is **automatically re-created** every time a new shell starts, by placing the creation command in a file that bash sources on startup.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing and Why

We are learning to control **where and how long** bash variables exist. The operational outcome: you will know how to create variables that survive across shell sessions, propagate into scripts (child shells), and persist either for a specific user or for all users on the system. This is essential for any environment configuration, scripting infrastructure, or system administration task.

***

## Step 1: Create a Variable and Observe Its Local Scope

**What we're doing:** Creating a variable in the current shell and confirming it exists.

```bash
SEASON=Monsoon
```

* `SEASON` — the variable name (convention: uppercase for environment-style variables)
* `=` — assignment operator (**no spaces** around `=` — spaces would break this)
* `Monsoon` — the value stored

**Access the variable:**

```bash
echo $SEASON
```

* `$` — the variable expansion operator; tells bash to replace `$SEASON` with its stored value
* **Expected output:** `Monsoon` [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

The instructor initially forgets the `$` prefix and catches himself: *"Oops! I have to use $."* This is a common mistake — without `$`, bash treats `SEASON` as a literal string, not a variable reference. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Connection to system flow:** The variable now exists in this shell process's memory. It is not exported, not persistent, and not visible to any other process.

***

## Step 2: Demonstrate Variable Loss on Logout

**What we're doing:** Proving that variables die when the shell process ends.

```bash
exit
```

* `exit` — terminates the current shell process. The instructor explains: *"what exit does is it closes the current shell."* [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

In the video, the instructor is logged in as root (via `sudo -i` from vagrant). Running `exit` closes the root shell and drops back to the vagrant user's shell.

**Log back in as root:**

```bash
sudo -i
```

* `sudo -i` — switches to root user by opening a **new shell** (this is a fresh process with fresh memory) [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Try to access the variable:**

```bash
echo $SEASON
```

* **Expected output:** *(empty/blank)* — the variable no longer exists [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Why it's empty:** The previous root shell process is dead. This is a new process. The variable was stored only in the old process's memory.

**Common mistake:** Assuming variables "save" somewhere automatically. They don't — they live only in RAM, tied to the process.

***

## Step 3: Create a Script That Uses the Variable (Demonstrating Child Shell Isolation)

**What we're doing:** Writing a script that references `$SEASON` and showing it can't see the parent shell's variable.

```bash
vi testvars.sh
```

**Script content:**

```bash
#!/bin/bash
echo "The $SEASON is longer this time."
echo "$SEASON is more than expected this time."
```

* `#!/bin/bash` — shebang line; tells the OS to execute this script in a **new bash process** (child shell)
* `$SEASON` — references the variable; will be empty if the variable isn't in the child shell's environment [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Make the script executable:**

```bash
chmod +x testvars.sh
```

**Set the variable in the parent shell, then run the script:**

```bash
SEASON=Monsoon
echo $SEASON          # Works — parent shell has it
./testvars.sh         # Fails — child shell does NOT have it
```

* **Expected output of `echo $SEASON`:** `Monsoon` ✅
* **Expected output of `./testvars.sh`:** Lines print with blank spaces where `$SEASON` should be ❌ [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Why:** The script runs in a child shell (new process). Regular variables are not inherited by child processes.

***

## Step 4: Export the Variable to Child Shells

**What we're doing:** Using `export` to push the variable into the environment so child shells can see it.

```bash
export SEASON
```

* `export` — copies the variable from local shell memory into the **process environment** (which IS inherited by child processes)
* `SEASON` — the variable to export (it must already exist, or you can combine: `export SEASON=Monsoon`) [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Verify by running the script again:**

```bash
./testvars.sh
```

* **Expected output:** Lines now correctly include "Monsoon" ✅ [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Connection to system flow:** The variable is now in the environment. Any child shell spawned from this parent will inherit it. But it's still temporary — it dies when this parent shell dies.

***

## Step 5: Prove That Export Is Still Temporary

**What we're doing:** Logging out and back in to show the exported variable doesn't survive.

```bash
exit            # Kill the current shell
sudo -i         # Open a new root shell
echo $SEASON    # Empty — the export died with the old shell
```

* **Expected output:** *(empty)* [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**This confirms:** `export` solves scope (parent → child), NOT persistence (across sessions).

***

## Step 6: Make the Variable Permanent for a Specific User via `~/.bashrc`

**What we're doing:** Editing the root user's `.bashrc` file so the variable is automatically created every time root logs in.

```bash
vi ~/.bashrc
```

**Add at the end of the file:**

```bash
export SEASON=Monsoon
```

* `export` — creates and exports the variable in one command
* This line will execute automatically every time root's shell starts [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Save and exit** (`:wq` in vi).

**Test immediately:**

```bash
echo $SEASON
```

* **Expected output:** *(empty)* — the file hasn't been sourced yet in this session [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

This is a common point of confusion. Editing `.bashrc` doesn't retroactively affect the current shell. The file is only sourced when a **new** shell starts.

**Log out and log back in:**

```bash
exit
sudo -i
echo $SEASON
```

* **Expected output:** `Monsoon` ✅ — `.bashrc` was sourced on login [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Verification:** The variable now survives across sessions for root. Every time root logs in, `.bashrc` re-creates it.

> ⚠️ **Expert Note**
>
> If you need the variable available immediately without logging out/in, you can manually source the file: `source ~/.bashrc` or `. ~/.bashrc`. But understand that this runs the entire file in your current shell, which may have side effects if `.bashrc` contains other initialization logic.

***

## Step 7: Make the Variable Permanent for ALL Users via `/etc/profile`

**What we're doing:** Setting a system-wide default by editing the global profile file.

```bash
vi /etc/profile
```

**Add at the end of the file:**

```bash
export SEASON=Winter
```

The instructor intentionally uses a **different value** (`Winter` instead of `Monsoon`) to demonstrate the override behavior between global and per-user files. [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Save and exit.**

***

## Step 8: Observe the Override Behavior (Sourcing Order in Action)

**What we're doing:** Testing which value each user sees, proving the sourcing order.

**Log out completely and log back in:**

```bash
exit                        # Exit root shell
exit                        # Exit vagrant shell
vagrant ssh scriptbox       # Fresh login as vagrant
```

**Test as vagrant user:**

```bash
echo $SEASON
```

* **Expected output:** `Winter` — vagrant has no `SEASON` in their `.bashrc`, so only `/etc/profile`'s value applies [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Switch to root and test:**

```bash
sudo -i
echo $SEASON
```

* **Expected output:** `Monsoon` — root's `.bashrc` (sourced second) overrides `/etc/profile`'s `Winter` value [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**The operational rule proven here:**

1. `/etc/profile` runs first → sets `SEASON=Winter` for everyone
2. `~/.bashrc` runs second → root's `.bashrc` overrides to `SEASON=Monsoon`
3. Vagrant has no override → keeps `Winter` from `/etc/profile` [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)

**Common mistake:** Expecting `/etc/profile` to always win because it's "global." It doesn't — per-user files execute later and override it.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Variable Lifecycle (The Complete Chain)

```
SEASON=Monsoon
  │
  Scope: current shell process ONLY
  Lifetime: dies with shell (exit / logout)
  Child shells: CANNOT see it
  │
  ▼
export SEASON
  │
  Scope: current shell + ALL child shells
  Lifetime: STILL dies with shell (exit / logout)
  │
  ▼
~/.bashrc → export SEASON=Monsoon
  │
  Scope: auto-created on every login for THIS user
  Lifetime: permanent for this user
  Child shells: yes (exported)
  │
  ▼
/etc/profile → export SEASON=Winter
  │
  Scope: auto-created on every login for ALL users
  Lifetime: permanent for everyone
  Child shells: yes (exported)
```

***

## 🔷 Scope vs. Persistence (Two Separate Problems)

```
PROBLEM 1: SCOPE (who can see it?)
  ├── Local variable    → only current shell
  └── Exported variable → current shell + child shells
  Solution: export

PROBLEM 2: PERSISTENCE (how long does it live?)
  ├── In-memory only    → dies on exit
  └── In startup file   → re-created on every login
  Solution: place export in startup file
```

***

## 🔷 Sourcing Order & Override Rule

```
LOGIN EVENT
  │
  ├─ 1st: /etc/profile  (GLOBAL — all users)
  │       sets defaults
  │
  └─ 2nd: ~/.bashrc     (PER-USER — specific user)
          overrides globals
          
∴ Same variable in both → .bashrc WINS (last-write-wins)

EXAMPLE:
  /etc/profile:  SEASON=Winter
  root/.bashrc:  SEASON=Monsoon
  
  vagrant sees: Winter   (no .bashrc override)
  root sees:    Monsoon  (.bashrc overrides)
```

***

## 🔷 File Map

```
/etc/profile          → system-wide, all users, sourced FIRST
~/.bashrc             → per-user, sourced SECOND (overrides /etc/profile)
~/.bash_profile       → per-user (alternative/complementary to .bashrc)
~/.profile            → per-user (alternative/complementary to .bashrc)
```

***

## 🔷 Parent Shell ↔ Child Shell Interaction

```
PARENT SHELL (your terminal)
  │
  ├── local var: SEASON=Monsoon     → NOT copied to child
  │
  ├── export SEASON                 → COPIED to child via environment
  │
  └── runs: ./testvars.sh
        │
        └── CHILD SHELL (#!/bin/bash → new process)
              │
              ├── Can see exported vars ✅
              └── Cannot see local vars ❌
```

***

## 🔷 Key Commands (Quick Reference)

```
SEASON=Monsoon              → create local variable
echo $SEASON                → read variable ($ = expand)
export SEASON               → push existing var to environment
export SEASON=Monsoon       → create + export in one step
exit                        → kill current shell (vars die)
sudo -i                     → open new root shell (new process)
vi ~/.bashrc                → edit per-user startup file
vi /etc/profile             → edit global startup file
source ~/.bashrc            → reload file without logout (implied)
```

***

## 🔷 Cause → Effect Chain (Failure Diagnosis)

```
Variable empty in script?
  → Not exported. Fix: export VAR

Variable gone after logout?
  → Not in startup file. Fix: add to ~/.bashrc

Variable wrong value for specific user?
  → Check ~/.bashrc (overrides /etc/profile)

Variable not available after editing .bashrc?
  → File not sourced yet. Fix: logout/login or source ~/.bashrc

Variable not available for all users?
  → Not in /etc/profile. Fix: add export to /etc/profile
```

***

## 🔷 Reusable Engineering Pattern: Layered Configuration with Override

```
PATTERN: Global Default → Per-Entity Override (last-write-wins)

In this lecture:
  /etc/profile (global) → ~/.bashrc (per-user)

Same pattern everywhere in Linux/DevOps:
  /etc/gitconfig      → ~/.gitconfig       (Git)
  /etc/ssh/ssh_config → ~/.ssh/config      (SSH)
  system defaults     → user customization (universal)

Rule: specific overrides general. Later overrides earlier.
```

***

## 🔷 Core Mental Model (One-Line Reconstruction)

> **Variables live in processes. Processes die. To survive death, variables must be written into files that are auto-executed on rebirth (login).**

That single sentence reconstructs the entire lecture. Everything else is implementation detail of *where* to write (`.bashrc` vs `/etc/profile`) and *who* it affects (one user vs all users). [\[95-exporti...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/95-exporting-variables.txt)
