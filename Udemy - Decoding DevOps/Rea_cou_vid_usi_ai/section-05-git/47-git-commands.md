# 🎓 Complete Deep Learning Material — Advanced Git Commands: Diff, Revert, Reset, Restore, SSH Authentication, and the Pre-Git Backup Anti-Pattern

**Source:** [47-Git-Commands.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/47-Git-Commands.txt?EntityRepresentationId=a164cf96-20f8-4a75-ad5f-a89ce7e9fc22) — A command history log capturing an instructor's full Git session, demonstrating the manual backup anti-pattern (pre-Git workflow), discarding local changes (`git checkout <file>`), staged vs. unstaged diff (`git diff` / `git diff --cached`), unstaging files (`git restore --staged`), compact log viewing (`git log --oneline`), comparing commits (`git diff <hash>..<hash>`), undoing commits safely (`git revert HEAD`), destructive history rewriting (`git reset --hard`), and setting up SSH-based GitHub authentication (`ssh-keygen`, SSH clone URL). <cite>turn6search6</cite>

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Manual Backup Anti-Pattern: Why Git Exists

The command history opens with a sequence that is **not Git at all** — it's the old, pre-Git way of managing file versions. The instructor manually creates backup copies of a script file (`remotexecmulti.sh`) by copying it with timestamped filenames: <cite>turn6search6</cite>

```
cp remotexecmulti.sh remotexecmulti.sh_13123030_1040.bakup
cp remotexecmulti.sh remotexecmulti.sh_14123030_1040.bakup
cp remotexecmulti.sh remotexecmulti.sh_12113030_1040.bakup
cp remotexecmulti.sh remotexecmulti.sh_12103030_1150.bakup
cp remotexecmulti.sh remotexecmulti.sh_05103030_1150.bakup
```

Then archives all backups into a tar file (`tar czvf remotexecmulti.Bakup *.bakup`) and deletes the individual backup files (`rm -rf *.bakup`). <cite>turn6search6</cite>

This sequence exists in the history **as a contrast** — it shows what version control looked like before Git. Multiple timestamped copies clutter the directory, filenames become unreadable, there's no way to see *what* changed between versions, no way to compare versions meaningfully, no branching, no collaboration, and no undo mechanism beyond manually restoring a backup. The entire rest of the session then demonstrates how Git solves every one of these problems elegantly.

> 🔍 **Deep Dive:** This anti-pattern is still common in environments where engineers haven't adopted version control — you see it with configuration files, scripts, database dumps, and documents. The filename becomes the "version label" (dates, initials, "FINAL", "FINAL\_v2"). It scales terribly: 5 backup copies are manageable, 50 are a nightmare, and there's no way to know what actually changed in each version. Git replaces all of this with commits that have messages, diffs, timestamps, and authors — structured version metadata instead of filename chaos.

***

## 1.2 — Discarding Uncommitted Changes: `git checkout <file>`

One of the most valuable recovery operations in Git is the ability to **discard local changes** to a file and restore it to its last committed state. If you edit a file, realize the changes are wrong, and want to go back to how it was — `git checkout <filename>` does exactly that. <cite>turn6search6</cite>

The command history shows: the instructor edits `jupiter1.rb` with vim, views the modified content with `cat`, then runs `git checkout jupiter1.rb`, and views it again — the file is back to its original committed state. The local edits are **permanently discarded**. <cite>turn6search6</cite>

This is a **working-directory-level undo**. It operates on files that have been modified but **not yet staged** (not yet `git add`-ed). It replaces the file in your working directory with the version from the last commit.

> ⚠️ **Expert Note:** `git checkout <file>` permanently destroys uncommitted changes — there is no recovery. This is analogous to `rm -rf` in its irreversibility. Always be certain you want to discard changes before running it. In newer Git versions, the equivalent command is `git restore <file>`, which is more intuitive (since `checkout` is overloaded — it both switches branches and restores files).

***

## 1.3 — Git Diff: Understanding the Three Comparison Contexts

`git diff` is Git's tool for showing **exactly what changed** — line by line, word by word. But it operates differently depending on **where** the changes are in Git's three-tree architecture (working directory → staging area → repository). The command history demonstrates all three contexts: <cite>turn6search6</cite>

### `git diff` (no flags) — Working Directory vs. Staging Area

Shows changes that exist in your **working directory** but have **not yet been staged** (`git add`). If you modify a file and run `git diff`, you see those modifications. After you `git add .`, running `git diff` shows **nothing** — because the changes have moved from the working directory into the staging area, and there's no longer a difference between the two. <cite>turn6search6</cite>

The command history confirms this: after `git add .` (line 539), `git diff` (line 541) produces no output.

### `git diff --cached` — Staging Area vs. Last Commit

Shows changes that have been **staged** (`git add`-ed) but **not yet committed**. This is what will go into the next commit. After staging but before committing, `git diff` is empty but `git diff --cached` shows the staged changes. <cite>turn6search6</cite>

The command history confirms: after `git add .`, `git diff` is empty (line 541), but `git diff --cached` (line 542) shows the staged content.

### `git diff <hash1>..<hash2>` — Between Two Specific Commits

Shows the difference between **any two commits** in history. You provide two commit hashes (or short hashes), separated by `..`, and Git shows every change between them. The history shows: `git diff 358d7f8..a886cb6`. <cite>turn6search6</cite>

> 🔍 **Deep Dive:** The three `git diff` modes map directly to Git's three-tree architecture:
>
> ```
> Working Dir ←─ git diff ─→ Staging Area ←─ git diff --cached ─→ Last Commit
>                                                                    ↕
>                                              git diff hash1..hash2 (any two commits)
> ```
>
> Understanding which "gap" each diff command inspects is essential. The most common mistake is running `git diff` after staging and seeing nothing — the changes aren't gone, they're just in the staging area now, visible only through `git diff --cached`.

***

## 1.4 — Unstaging Files: `git restore --staged`

After staging a file with `git add`, you may realize you don't want it in the next commit — but you don't want to lose the changes either. You just want to **move it back from the staging area to the working directory**. <cite>turn6search6</cite>

`git restore --staged <filename>` does exactly this. The command history shows: after staging `jupiter1.rb`, the instructor runs `git restore --staged jupiter1.rb` (line 543). After this, `git status` shows the file as modified but **unstaged**, and `git diff` shows the changes again (because they're back in the working directory). <cite>turn6search6</cite>

This is a **non-destructive** operation — the file contents are not changed. Only the file's location in Git's staging model moves (from staged → unstaged).

The conceptual flow: `git add` moves changes from working directory → staging area. `git restore --staged` reverses that, moving changes from staging area → back to working directory. These are inverse operations.

***

## 1.5 — Compact Log Viewing: `git log --oneline`

`git log` shows the full commit history, but it's verbose — each commit takes multiple lines (hash, author, date, message). `git log --oneline` compresses each commit to a **single line**: the short hash and the commit message. <cite>turn6search6</cite>

The command history shows this being used multiple times (lines 552, 556, 558, 560) to quickly check the state of history before and after revert and reset operations. It's the operational tool for **quickly inspecting where you are** in the commit timeline.

***

## 1.6 — Safe Undo: `git revert HEAD`

`git revert HEAD` creates a **new commit** that undoes the changes made in the most recent commit. The key word is "new commit" — it does **not** delete or erase the original commit from history. Instead, it adds a reversal on top. <cite>turn6search6</cite>

The command history shows: after committing "playbook" (line 547), the instructor runs `git revert HEAD` (line 554), then verifies with `cat jupiter1.rb` that the file content has been restored, and `git log --oneline` (line 556) shows **both** the original commit and the revert commit in history.

This is the **safe** undo mechanism. History is preserved — you can see what was done, and what was undone. This is important for collaboration: if you've already pushed commits to a shared repository, `revert` is the correct approach because it doesn't rewrite history that other people may have already pulled.

***

## 1.7 — Destructive Undo: `git reset --hard <hash>`

`git reset --hard <commit_hash>` moves the branch pointer **back to a specific commit** and **discards all commits after it**. Unlike `revert`, this **erases history**. Commits after the target hash are gone (from the branch's perspective). The working directory and staging area are also reset to match that commit — all uncommitted changes are destroyed. <cite>turn6search6</cite>

The command history shows: `git reset --hard 358d7f8` (line 559). After this, `git log --oneline` (line 560) shows only history up to that commit — the "playbook" commit and the revert commit are both gone.

The critical distinction between `revert` and `reset --hard`:

| Aspect    | `git revert HEAD`           | `git reset --hard <hash>`         |
| --------- | --------------------------- | --------------------------------- |
| History   | Preserved (adds new commit) | Erased (removes commits)          |
| Safety    | Safe for shared repos       | Dangerous for shared repos        |
| Mechanism | Creates inverse commit      | Moves branch pointer backward     |
| Data loss | None                        | Discards all changes after target |

> ⚠️ **Expert Note:** `git reset --hard` is the Git equivalent of `rm -rf` — irreversible and dangerous. If you've already pushed the commits you're resetting, you'll need `git push --force` to overwrite the remote, which **rewrites shared history** and can cause serious problems for collaborators. Use `reset --hard` only on local, unpushed commits. For pushed commits, always use `revert`.

***

## 1.8 — SSH Authentication for GitHub

The final section of the command history transitions from HTTPS-based GitHub authentication to **SSH-based authentication**. <cite>turn6search6</cite>

### Viewing Git Configuration

`cat .git/config` (line 563) shows the repository's configuration file, which includes the remote URL (currently HTTPS). <cite>turn6search6</cite>

### Generating SSH Keys

The sequence `rm -rf .ssh/*` → `ssh-keygen.exe` (lines 565-566) generates a new SSH key pair. `ssh-keygen` creates two files in `~/.ssh/`: <cite>turn6search6</cite>

* **`id_rsa`** — the private key (never share this)
* **`id_rsa.pub`** — the public key (this gets uploaded to GitHub)

The instructor views the public key with `cat .ssh/id_rsa.pub` (line 569), which is then copied and added to the GitHub account settings (implied — the actual GitHub UI step isn't in the command history).

### Cloning via SSH

Instead of the HTTPS URL (`https://github.com/...`), the SSH clone URL uses a different format: `git@github.com:imranvisualpath/titanwork.git` (line 571). After adding the public key to GitHub, cloning via SSH authenticates using the key pair instead of username/password. <cite>turn6search6</cite>

> 🔍 **Deep Dive:** HTTPS authentication requires entering credentials (or using a credential manager/token) for each push/pull operation. SSH authentication uses the key pair: your local machine proves its identity with the private key, and GitHub verifies it against the stored public key. Once set up, SSH never prompts for credentials — it's seamless. The trade-off: initial setup is more complex, but ongoing usage is frictionless. In team environments, SSH is the standard for developers who push frequently.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning **advanced Git operations** for day-to-day version control: inspecting changes before committing (diff), undoing mistakes at various levels (checkout, restore, revert, reset), viewing compact history, and setting up SSH authentication for seamless GitHub access. The final outcome is the ability to **confidently manage, inspect, undo, and recover** from any state in a Git repository. <cite>turn6search6</cite>

***

## Step 1 — Clone the Repository (Starting Point)

```bash
git clone https://github.com/imranvisualpath/titanwork.git
cd titanwork/
ls
```

* **`git clone <URL>`** — downloads the full repository from GitHub
* **`cd titanwork/`** — enter the cloned repository directory <cite>turn6search6</cite>

**Verification:** `ls` shows all repository files.

***

## Step 2 — Edit a File, Then Discard Changes with `git checkout`

### Edit a file:

```bash
vim jupiter1.rb
```

Make some changes to the file content. <cite>turn6search6</cite>

### View the modified content:

```bash
cat jupiter1.rb
```

Confirms your edits are in the file.

### Discard all changes and restore to last commit:

```bash
git checkout jupiter1.rb
```

**Breakdown:**

* **`git checkout`** — when given a filename (not a branch name), it restores the file to its last committed state
* **`jupiter1.rb`** — the specific file to restore <cite>turn6search6</cite>

**What happens:** Your edits are permanently discarded. The file reverts to exactly how it was in the last commit.

**Verification:**

```bash
cat jupiter1.rb
```

File content matches the last committed version — your edits are gone. <cite>turn6search6</cite>

**Common mistake:** Confusing `git checkout <branch>` (switches branches) with `git checkout <file>` (restores file). Same command, very different operations depending on whether the argument is a branch name or a filename.

***

## Step 3 — Make Changes and Observe `git diff` (Unstaged)

### Edit the file again:

```bash
vim jupiter1.rb
```

<cite>turn6search6</cite>

### Check what changed (unstaged diff):

```bash
git diff
```

**What it shows:** Line-by-line differences between the **working directory** and the **staging area** (which currently matches the last commit since nothing is staged). You see your edits highlighted. <cite>turn6search6</cite>

### Check status:

```bash
git status
```

Shows `jupiter1.rb` as modified but not staged.

***

## Step 4 — Stage Changes and Observe `git diff` Behavior Shift

### Stage all changes:

```bash
git add .
```

<cite>turn6search6</cite>

### Check unstaged diff:

```bash
git diff
```

**Result:** Empty — no output. The changes have moved from working directory to staging area, so there's no difference between them anymore. <cite>turn6search6</cite>

### Check staged diff:

```bash
git diff --cached
```

**Breakdown:**

* **`--cached`** — compare the staging area against the last commit (instead of working directory vs. staging area) <cite>turn6search6</cite>

**Result:** Shows the staged changes — this is what will be included in the next commit.

**Key takeaway:** After `git add`, use `git diff --cached` (not `git diff`) to see what you're about to commit.

***

## Step 5 — Unstage a File with `git restore --staged`

```bash
git restore --staged jupiter1.rb
```

**Breakdown:**

* **`git restore`** — file restoration command
* **`--staged`** — operate on the staging area (move file FROM staged BACK to unstaged)
* **`jupiter1.rb`** — the file to unstage <cite>turn6search6</cite>

**What happens:** The file is removed from the staging area but **changes are preserved** in the working directory. The file goes from "staged" to "modified but unstaged."

**Verification:**

```bash
git status
```

Shows `jupiter1.rb` as modified (unstaged). <cite>turn6search6</cite>

```bash
git diff
```

Shows the changes again (since they're back in the working directory). <cite>turn6search6</cite>

**Connection to flow:** This is the inverse of `git add`. Use it when you accidentally staged something you didn't want in the next commit.

***

## Step 6 — Re-stage, Commit, and View Log

### Stage and commit:

```bash
git add .
git commit -m "playbook"
```

<cite>turn6search6</cite>

### Verify clean state:

```bash
git status
git diff
git diff --cached
```

All three should show nothing — everything is committed. <cite>turn6search6</cite>

### View compact commit history:

```bash
git log --oneline
```

**Breakdown:**

* **`git log`** — show commit history
* **`--oneline`** — compress each commit to one line (short hash + message) <cite>turn6search6</cite>

**Expected output:** A list of commits, most recent at top. Note the short hash of the "playbook" commit and the commit before it — you'll need them for the next steps.

***

## Step 7 — Compare Two Specific Commits

```bash
git diff 358d7f8..a886cb6
```

**Breakdown:**

* **`git diff`** — comparison command
* **`358d7f8`** — short hash of the first (older) commit
* **`..`** — range separator
* **`a886cb6`** — short hash of the second (newer) commit <cite>turn6search6</cite>

**What it shows:** Every change that occurred between these two commits. Useful for reviewing what happened over a range of history.

**Where to get the hashes:** From `git log --oneline` output (Step 6).

***

## Step 8 — Safely Undo a Commit with `git revert`

```bash
git revert HEAD
```

**Breakdown:**

* **`git revert`** — create a new commit that undoes a specified commit
* **`HEAD`** — refers to the most recent commit <cite>turn6search6</cite>

**What happens:** Git creates a **new commit** whose changes are the exact inverse of the "playbook" commit. The original commit remains in history.

**Verification:**

```bash
cat jupiter1.rb
```

File content is back to pre-"playbook" state. <cite>turn6search6</cite>

```bash
git log --oneline
```

Shows THREE entries: the original commit, the "playbook" commit, AND the revert commit. History is fully preserved. <cite>turn6search6</cite>

**Connection to flow:** This is the **safe undo** — use for pushed/shared commits.

***

## Step 9 — Destructively Undo with `git reset --hard`

```bash
git reset --hard 358d7f8
```

**Breakdown:**

* **`git reset`** — move the branch pointer to a different commit
* **`--hard`** — also reset the staging area AND working directory to match that commit (discard everything)
* **`358d7f8`** — the target commit hash to reset to <cite>turn6search6</cite>

**What happens:** The branch pointer moves back to `358d7f8`. All commits after it (including "playbook" and the revert) are **erased from history**. Working directory and staging area are reset to match. <cite>turn6search6</cite>

**Verification:**

```bash
git log --oneline
```

Only shows commits up to `358d7f8`. The "playbook" and revert commits are gone. <cite>turn6search6</cite>

**⚠️ CRITICAL WARNING:** This is irreversible for the erased commits. If these commits were already pushed, you'd need `git push --force` to update the remote, which rewrites shared history and can break collaborators' repositories. **Use only on local, unpushed work.**

***

## Step 10 — Set Up SSH Authentication for GitHub

### View current Git config:

```bash
cat .git/config
```

Shows the remote URL (currently HTTPS). <cite>turn6search6</cite>

### Generate a new SSH key pair:

```bash
cd ~
rm -rf .ssh/*
ssh-keygen.exe
```

* **`rm -rf .ssh/*`** — clears any existing SSH keys
* **`ssh-keygen.exe`** — generates a new key pair (follow the prompts; press Enter for defaults) <cite>turn6search6</cite>

**Verification:**

```bash
ls .ssh/
```

Should show `id_rsa` (private key) and `id_rsa.pub` (public key). <cite>turn6search6</cite>

### Copy the public key:

```bash
cat .ssh/id_rsa.pub
```

Copy the entire output. Go to **GitHub → Settings → SSH and GPG keys → New SSH key** and paste it there (implied UI step). <cite>turn6search6</cite>

### Clone using SSH URL:

```bash
git clone git@github.com:imranvisualpath/titanwork.git
```

**Breakdown:**

* **`git@github.com:`** — SSH protocol prefix for GitHub
* **`imranvisualpath/titanwork.git`** — repository path <cite>turn6search6</cite>

**What happens:** Git authenticates using your private key (matched against the public key on GitHub). No password prompt. <cite>turn6search6</cite>

**Connection to flow:** Once SSH is set up, all future push/pull operations to this remote are passwordless and seamless.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Git's Three-Tree Architecture (Diff Context Map)

```
WORKING DIRECTORY ←── git diff ──→ STAGING AREA ←── git diff --cached ──→ REPOSITORY
       │                                │                                     │
       │          git add .             │         git commit                  │
       │ ──────────────────────→        │ ──────────────────────→             │
       │                                │                                     │
       │     git restore --staged       │                                     │
       │ ←──────────────────────        │                                     │
       │                                                                      │
       │              git checkout <file>                                      │
       │ ←────────────────────────────────────────────────────────────────────│

                     git diff hash1..hash2 = compare ANY two commits
```

<cite>turn6search6</cite>

***

## 🔄 Undo Operations Hierarchy

```
LEVEL 1 — Discard working directory changes (NOT staged):
  git checkout <file>          → restore file to last commit (DESTRUCTIVE)
  git restore <file>           → modern equivalent

LEVEL 2 — Unstage (staged but NOT committed):
  git restore --staged <file>  → move back: staging → working dir (NON-DESTRUCTIVE)

LEVEL 3 — Undo a commit (SAFE, preserves history):
  git revert HEAD              → creates inverse commit on top
  └── History: A → B → revert-B (all visible)
  └── Safe for pushed/shared commits

LEVEL 4 — Erase commits (DESTRUCTIVE, rewrites history):
  git reset --hard <hash>      → moves branch pointer back, erases later commits
  └── History: A → B → C becomes A (B,C gone)
  └── DANGEROUS for pushed commits (needs --force push)
```

<cite>turn6search6</cite>

***

## 🔍 Diff Command Matrix

```
git diff                    → unstaged changes (working dir vs staging)
git diff --cached           → staged changes (staging vs last commit)
git diff hash1..hash2       → between any two commits

AFTER git add:
  git diff        → EMPTY (nothing unstaged)
  git diff --cached → SHOWS changes (staged, waiting for commit)

AFTER git commit:
  git diff        → EMPTY
  git diff --cached → EMPTY
  git log --oneline → SHOWS commit in history
```

<cite>turn6search6</cite>

***

## 🔐 Authentication: HTTPS vs SSH

```
HTTPS:
  URL:  https://github.com/user/repo.git
  Auth: username + password/token (each push/pull)

SSH:
  URL:  git@github.com:user/repo.git
  Auth: key pair (automatic, no prompts)

  SETUP:
    ssh-keygen → creates ~/.ssh/id_rsa (private) + id_rsa.pub (public)
    cat id_rsa.pub → copy to GitHub Settings → SSH keys
    git clone git@github.com:user/repo.git → passwordless access
```

<cite>turn6search6</cite>

***

## 📜 Anti-Pattern vs Git

```
WITHOUT GIT (manual backups):
  cp file file_DATE_TIME.bakup     → filename = version label
  cp file file_DATE2_TIME2.bakup   → clutter accumulates
  tar czvf archive *.bakup         → archive to manage clutter
  rm -rf *.bakup                   → cleanup
  ❌ No diff, no history, no branching, no collaboration, no undo

WITH GIT:
  git add . → git commit -m "msg"  → structured version with message
  git diff                         → see exactly what changed
  git log --oneline                → clean version history
  git revert / git reset           → undo at any level
  ✅ Full history, diffs, branches, collaboration, recovery
```

<cite>turn6search6</cite>

***

## ⚡ Key Command Reference (Compact)

```
INSPECT:
  git diff                → unstaged changes
  git diff --cached       → staged changes
  git diff h1..h2         → between commits
  git log --oneline       → compact history
  git status              → overall state

STAGE/UNSTAGE:
  git add .               → stage all
  git restore --staged F  → unstage file F

UNDO (escalating severity):
  git checkout <file>     → discard local edits (irreversible)
  git restore --staged F  → unstage (non-destructive)
  git revert HEAD         → undo last commit (safe, adds commit)
  git reset --hard <hash> → erase commits (dangerous, rewrites history)

AUTH:
  ssh-keygen              → generate key pair
  cat ~/.ssh/id_rsa.pub   → get public key for GitHub
  git clone git@...       → SSH clone (passwordless)
```

<cite>turn6search6</cite>

***

## 🧩 Reusable Patterns

| Pattern                             | Instance                                                                                                                                                          |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Escalating Undo Severity**        | checkout (discard edits) → restore --staged (unstage) → revert (safe undo commit) → reset --hard (erase history) — each level is more powerful and more dangerous |
| **Safe vs. Destructive Operations** | `revert` preserves history (additive); `reset --hard` erases history (destructive) — same dichotomy as `mv` (recoverable) vs `rm -rf` (permanent)                 |
| **Layer-Aware Inspection**          | `git diff` inspects the working↔staging gap; `git diff --cached` inspects staging↔repo gap — knowing which layer you're inspecting prevents misdiagnosis          |
| **Anti-Pattern as Motivation**      | Manual timestamp-based backups → Git commits; seeing the broken approach clarifies why the tool exists                                                            |
| **Credential Delegation**           | SSH key pair replaces interactive credentials — private key proves identity, public key verifies it; same pattern as certificate-based auth everywhere            |
| **Preview before Action**           | `git log --oneline` before reset/revert; `git diff` before commit — inspect state before executing irreversible operations                                        |

<cite>turn6search6</cite>

***

## 🧭 One-Line Mental Reload

> **`git diff` shows unstaged changes, `git diff --cached` shows staged changes, `git diff h1..h2` compares commits; undo escalates from `checkout <file>` (discard edits) → `restore --staged` (unstage) → `revert HEAD` (safe commit undo, preserves history) → `reset --hard <hash>` (erase commits, dangerous); `git log --oneline` for quick history inspection; SSH setup: `ssh-keygen` → copy `id_rsa.pub` to GitHub → clone with `git@github.com:` URL for passwordless auth.** <cite>turn6search6</cite>
