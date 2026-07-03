# Git Rollback — Undoing Changes at Every Stage

### `git checkout`, `git restore`, `git revert`, and `git reset` — Complete Rollback System

*Reconstructed from video lecture captions* [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Why Rollback Exists

In any version control workflow, you will inevitably make changes that you need to undo — a wrong edit, a broken feature, an accidental commit. But "undoing" in Git is not a single action because Git has **multiple stages** where your changes can exist at any given moment. A change sitting in your working directory is fundamentally different from a change that has been staged, and both are different from a change that has been committed. Each stage requires its **own rollback mechanism**. Understanding rollback in Git means understanding that there is no single "undo button" — there is a **rollback system** with stage-specific tools. [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

The video repeatedly emphasizes: "when you're doing versioning you need to be absolutely sure what you're doing." Rollback operations, especially destructive ones, affect shared history that other DevOps engineers and developers depend on. Confidence comes from understanding which tool operates at which stage and what it does to your data and history. [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

***

## 1.2 — The Three Stages of Change: The Rollback Landscape

To understand rollback, you must first have a clear mental model of the three places a change can live in Git: [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

### Stage 1: Working Directory (Unstaged Changes)

When you edit a file, the change exists only in your **working directory** — the actual files on disk. Git knows something changed (visible via `git status` as "modified"), but the change has not been recorded anywhere in Git's tracking system yet. At this point, the change is at its most fragile and easiest to undo. [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

### Stage 2: Staging Area (Indexed Changes)

When you run `git add`, the change moves from the working directory into the **staging area** (also called the index). The staging area is a holding zone — it's where you prepare changes that will be included in your next commit. The change is now tracked by Git but not yet permanently recorded. [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

### Stage 3: Committed (Permanent History)

When you run `git commit`, the staged changes become a **permanent commit** in the repository's history. The commit gets a unique ID, it's linked to the previous commit, and it becomes part of the project's historical record. Rolling back from here is more consequential because you're modifying recorded history. [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

```
Change Lifecycle:

  Edit file → [Working Directory] → git add → [Staging Area] → git commit → [Commit History]
                    │                              │                              │
              git checkout file             git restore --staged           git revert / git reset
                (rollback ←)                    (rollback ←)                  (rollback ←)
```

The core insight: **each stage has its own rollback command**. Using the wrong command at the wrong stage either won't work or will have unintended consequences. [\[43-rollback \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/43-rollback.txt)

***

## 1.3 — `git checkout <file>` — Rolling Back Unstaged Changes

When you've modified a file but have NOT yet run `git add`, the change exists only in the working directory. To discard this change and restore the file to its last committed state, you use `git checkout` followed by the filename. <cite>turn5search5</cite>

This is the simplest rollback. It replaces the modified file in your working directory with the version from the latest commit. The change is **permanently lost** — there is no undo for this undo. The video demonstrates this clearly: after editing a file and adding content, running `git checkout <filename>` makes it "all went back to how it was." <cite>turn5search5</cite>

A conceptual note: `git checkout` is primarily known as a branch-switching command ("we know git checkout switches between branches"), but the video explicitly highlights this **second use case** — when given a filename instead of a branch name, it restores that specific file to its last committed state. <cite>turn5search5</cite>

> ⚠️ **Expert Note**
> `git checkout <file>` is a destructive operation — the working directory changes are gone with no recovery path. Always use `git diff` to review what you're about to discard before running this command.

***

## 1.4 — `git diff` — The Inspection Tool Before Any Rollback

`git diff` is not a rollback command itself, but it is **essential to the rollback workflow**. It shows you exactly what has changed, allowing you to make an informed decision about whether to keep or discard changes. The video positions `git diff` as a decision-support tool used at every stage: "make sure you use git diff command to really check what are the differences." <cite>turn5search5</cite>

`git diff` behaves differently depending on where the changes are:

* **`git diff`** (no flags) — shows the difference between the **working directory** and the **staging area**. If a file has been modified but not staged, this shows what changed. However, once you run `git add`, plain `git diff` shows nothing — because the working directory and staging area are now in sync. <cite>turn5search5</cite>

* **`git diff --cached`** — shows the difference between the **staging area** and the **last commit**. This is what you use after `git add` to see what will be included in the next commit. The video explicitly demonstrates this behavioral shift: "just git diff command is not going to work now. You have to give an option, git diff --cached." <cite>turn5search5</cite>

* **`git diff <commit_id>..<commit_id>`** — shows the difference between **two specific commits**. Used after committing to compare the current commit against a previous one. The two commit IDs are separated by `..` (two dots). <cite>turn5search5</cite>

The video presents a practical workflow: check `git status` to see WHAT changed, then `git diff` (or `git diff --cached`) to see HOW it changed, then decide whether to proceed or rollback. <cite>turn5search5</cite>

> 🔍 **Deep Dive**
> The reason `git diff` stops showing changes after `git add` is that `git diff` compares the working directory against the index (staging area). After `git add`, the working directory and staging area contain the same version of the file, so there's no difference. The difference now exists between the staging area and the last commit — which is what `--cached` reveals. This is not a bug or limitation; it's a direct consequence of Git's three-stage architecture. Understanding why `git diff` "stops working" after staging is understanding the stage model itself.

***

## 1.5 — `git restore --staged <file>` — Unstaging Without Losing Changes

When you've run `git add` and a change is in the staging area, but you decide you don't want to include it in the next commit, `git restore --staged <filename>` moves the change **back to the working directory**. The change is NOT lost — it's simply moved from "staged" back to "modified." After this, `git status` will show the file as "modified" (not staged), and `git diff` (without `--cached`) will work again to show the changes. <cite>turn5search5</cite>

This is a **non-destructive** unstaging operation. The file in your working directory still contains your edits — only the staging state is reversed. This is the key difference from `git checkout <file>`, which discards the changes entirely. <cite>turn5search5</cite>

***

## 1.6 — `git revert HEAD` — Soft Rollback After Commit (History-Preserving)

Once changes are committed, you need a different approach. `git revert HEAD` creates a **new commit** that is the exact opposite of the current commit (HEAD). If the last commit added 5 lines, the revert commit removes those 5 lines. The result is that the code returns to the state before the problematic commit, but **the history of both the original commit and the revert commit are preserved**. <cite>turn5search5</cite>

The video illustrates this with a clear mental model: "we are here, we made some changes, we came at this place, then we wanted to roll back over here, but it created a new commit." The commit history after a revert looks like: original state → bad commit → revert commit. The code at the revert commit matches the original state, but you can see the full journey in the log. <cite>turn5search5</cite>

When you run `git revert HEAD`, Git opens an editor asking for a **commit message** for the revert (just like a regular commit, because it IS a regular commit — one that happens to undo another). You can also specify a specific commit ID instead of HEAD: `git revert <commit_id>`. <cite>turn5search5</cite>

The word **"softer"** is how the video characterizes revert: "Git revert is a softer way where you are storing the history also." This is important for collaborative work — other developers can see what happened and why. <cite>turn5search5</cite>

***

## 1.7 — `git reset --hard <commit_id>` — Hard Rollback (History-Destroying)

`git reset --hard <commit_id>` is the most aggressive rollback command. It moves the branch pointer **back to the specified commit**, and **deletes all commits that came after it** from the history. The data and all commit history after the specified commit ID are removed. The repository looks as if those commits never happened. <cite>turn5search5</cite>

The video is explicit about the consequences: "all the commit ID after that, all the commit history after that is removed. The data and all the history is removed." This is described as "a more direct way of a rollback." <cite>turn5search5</cite>

The fundamental decision between revert and reset is: **do you want to preserve the history of the mistake, or erase it entirely?** <cite>turn5search5</cite>

|               | `git revert`                         | `git reset --hard`                       |
| ------------- | ------------------------------------ | ---------------------------------------- |
| History       | Preserved (new commit added)         | Destroyed (commits removed)              |
| Safety        | Safer for shared/collaborative repos | Dangerous if commits were already pushed |
| Visibility    | Everyone can see what was undone     | Looks like nothing ever happened         |
| Reversibility | Can revert the revert                | Gone unless you have reflog              |

The video also mentions `git reset` (without `--hard`): "you can use git reset, you can use git reset --hard." The plain `git reset` unstages changes (similar to `git restore --staged`), while `--hard` is the destructive variant that resets everything — working directory, staging area, and commit history — back to the specified commit. <cite>turn5search5</cite>

> ⚠️ **Expert Note**
> The video stresses: "when you're doing versioning you need to be absolutely sure what you're doing. You have to, because you have to push it and share it with your fellow DevOps engineers and developers as well." Using `git reset --hard` on commits that have already been pushed to a shared remote is extremely dangerous — it rewrites shared history. `git revert` is the safe choice for anything already pushed. `git reset --hard` should be reserved for local, unpushed commits.

***

## 1.8 — Using ChatGPT as a Command Confirmation Tool

The video introduces an operational practice that is not about Git itself but about **how to work safely with Git**: using ChatGPT (or similar AI tools) to confirm commands before running them. The instructor demonstrates asking ChatGPT "explain git reset --hard with an example" and getting back a visual explanation with commit history (A, B, C, D). <cite>turn5search5</cite>

The reasoning is practical: "anytime you feel that you're not doing it right, just check with ChatGPT. Is your command correct or not?" and "sure we can roll back whatever mistakes we do, but I think ChatGPT is a really very good tool to confirm the commands." This is positioned as a safety net — not a learning replacement, but a real-time verification tool when working with consequential operations. <cite>turn5search5</cite>

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are walking through the complete Git rollback system — learning how to undo changes at every stage of the Git workflow: before staging, after staging, and after committing. By the end, you'll be able to confidently inspect changes with `git diff`, discard working directory edits with `git checkout`, unstage with `git restore --staged`, undo commits softly with `git revert`, and undo commits destructively with `git reset --hard`. <cite>turn5search5</cite>

***

## Level 1: Rolling Back Unstaged Changes

### Step 1.1 — Edit a File

Open any tracked file in your repository and add some content. The video edits `jupiter1.rb` and adds several lines from an existing playbook. <cite>turn5search5</cite>

### Step 1.2 — Check What Changed

```bash
git status
```

**Expected output:** The file appears as **modified** (red, not staged). Git knows the file changed but the change is not in the staging area. <cite>turn5search5</cite>

### Step 1.3 — View the Exact Differences

```bash
git diff
```

* `git diff` — compares working directory against the staging area (which currently matches the last commit since nothing has been staged)

**Expected output:** Shows the added/removed lines with `+` and `-` prefixes. The video shows the added lines prefixed with `+` signs in `jupiter1.rb`. <cite>turn5search5</cite>

This is your **decision point**: review the diff, decide if you want to keep or discard the changes.

### Step 1.4 — Discard the Changes (Rollback)

```bash
git checkout jupiter1.rb
```

* `git checkout` — when given a **filename** (not a branch name), it restores that file to its last committed state
* `jupiter1.rb` — the specific file to restore <cite>turn5search5</cite>

**What happens internally:** Git replaces the file in your working directory with the version from the latest commit. Your edits are permanently gone.

**Verification:** <cite>turn5search5</cite>

```bash
git status
```

**Expected output:** Clean working directory — no modified files. The file is back to how it was. <cite>turn5search5</cite>

**Common mistake:** Using this command when you actually wanted to keep some of the changes. Always run `git diff` first to review what you're discarding.

**Connection to flow:** This is the simplest rollback — changes never left the working directory. Next we'll see what happens when changes have already been staged.

***

## Level 2: Rolling Back Staged Changes

### Step 2.1 — Edit and Stage a File

Edit the file again (add content), then stage it: <cite>turn5search5</cite>

```bash
git add jupiter1.rb
```

### Step 2.2 — Verify the Staging

```bash
git status
```

**Expected output:** The file appears as **staged** (green, ready to commit). <cite>turn5search5</cite>

### Step 2.3 — Try `git diff` (It Shows Nothing Now)

```bash
git diff
```

**Expected output:** Nothing. No output. This is because `git diff` compares working directory vs. staging area, and they are now identical (the working directory change was moved into staging). <cite>turn5search5</cite>

**Common confusion:** "git diff is broken" — it's not. The change moved to a different stage. Use `--cached` instead.

### Step 2.4 — View Staged Differences

```bash
git diff --cached
```

* `--cached` — compares the **staging area** against the **last commit** <cite>turn5search5</cite>

**Expected output:** Shows the same diff you saw before staging — the lines you added. This confirms what will be included in the next commit. <cite>turn5search5</cite>

This is your **decision point** for staged changes.

### Step 2.5 — Unstage the Changes (Rollback from Staging)

```bash
git restore --staged jupiter1.rb
```

* `git restore` — the restore command
* `--staged` — specifies you want to restore FROM the staging area (move back to working directory)
* `jupiter1.rb` — the file to unstage <cite>turn5search5</cite>

**What happens internally:** The change is removed from the staging area and placed back in the working directory. The file content is **NOT changed** — your edits still exist in the file. Only the staging state is reversed. <cite>turn5search5</cite>

**Verification:** <cite>turn5search5</cite>

```bash
git status
```

**Expected output:** The file appears as **modified** (red, unstaged) — back to the Level 1 state.

```bash
git diff
```

**Expected output:** Shows the changes again (they're back in working directory territory). <cite>turn5search5</cite>

**Connection to flow:** The change has been moved backward one stage — from staging to working directory. From here, you could use `git checkout <file>` to discard it entirely, or re-stage it with `git add` if you change your mind. <cite>turn5search5</cite>

***

## Level 3: Rolling Back Committed Changes

### Step 3.1 — Stage and Commit

```bash
git add jupiter1.rb
git commit -m "some commit message"
```

### Step 3.2 — Verify the Commit

```bash
git status
```

**Expected output:** Clean working directory — nothing to commit. <cite>turn5search5</cite>

```bash
git diff
```

**Expected output:** Nothing.

```bash
git diff --cached
```

**Expected output:** Nothing. All three checks return empty because the change is now permanently committed. <cite>turn5search5</cite>

### Step 3.3 — View Commit History

```bash
git log --oneline
```

* `git log` — shows commit history
* `--oneline` — compact format, one commit per line (commit ID + message)

**Expected output:** Your latest commit appears at the top with its commit ID. Note this commit ID and the previous commit's ID. <cite>turn5search5</cite>

### Step 3.4 — Compare Two Commits

```bash
git diff <previous_commit_id>..<current_commit_id>
```

* `<previous_commit_id>` — the commit ID before your change
* `..` — range operator (two dots)
* `<current_commit_id>` — the commit you just made <cite>turn5search5</cite>

**Expected output:** Shows the differences between the two commits — what your commit actually changed. <cite>turn5search5</cite>

### Step 3.5 — Option A: Soft Rollback with `git revert`

```bash
git revert HEAD
```

* `git revert` — creates a new commit that undoes a previous commit
* `HEAD` — pointer to the current (latest) commit <cite>turn5search5</cite>

**What happens:** Git opens an editor for the revert commit message (like a normal commit). Save and exit. Git creates a **new commit** that reverses the changes from the HEAD commit. <cite>turn5search5</cite>

**Verification:**

```bash
cat jupiter1.rb
```

**Expected output:** The file content is back to the state before the reverted commit — "see there is nothing." <cite>turn5search5</cite>

```bash
git log --oneline
```

**Expected output:** You see a **new commit** (the revert) on top of the original commit. Both are visible in history. The video emphasizes: "you should actually see a new commit. That is for revert." <cite>turn5search5</cite>

**Connection to flow:** The code is rolled back, but history is preserved. Everyone can see the original commit AND the revert commit. This is the **safe** approach for shared repositories.

### Step 3.6 — Option B: Hard Rollback with `git reset`

```bash
git reset --hard <commit_id>
```

* `git reset` — moves the branch pointer to a different commit
* `--hard` — also resets the working directory and staging area to match
* `<commit_id>` — the specific commit to go back to <cite>turn5search5</cite>

**What happens internally:** The branch pointer moves backward to the specified commit. All commits after that commit ID are **deleted from history**. The working directory and staging area are reset to match the target commit. <cite>turn5search5</cite>

**Verification:**

```bash
git log --oneline
```

**Expected output:** The commits that existed after the target commit ID are gone. History reads as if they never happened. <cite>turn5search5</cite>

**Critical difference from revert:** No new commit is created. The unwanted commits simply disappear.

> ⚠️ **Expert Note**
> Use `git revert` for commits that have already been pushed to a shared remote. Use `git reset --hard` only for local, unpushed commits. If you reset commits that others have already pulled, you will create divergent histories and significant collaboration problems.

***

## Summary: Which Command at Which Stage

| Change is in...                | Rollback Command               | Effect                                                   |
| ------------------------------ | ------------------------------ | -------------------------------------------------------- |
| Working directory (unstaged)   | `git checkout <file>`          | Discards edits, restores last commit version             |
| Staging area (after `git add`) | `git restore --staged <file>`  | Moves change back to working directory (edits preserved) |
| Committed (soft undo)          | `git revert HEAD`              | Creates new inverse commit (history preserved)           |
| Committed (hard undo)          | `git reset --hard <commit_id>` | Deletes commits after target (history destroyed)         |

<cite>turn5search5</cite>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## The Three-Stage Rollback Architecture

```
┌──────────────┐   git add   ┌──────────────┐  git commit  ┌──────────────┐
│   WORKING    │ ──────────→ │   STAGING    │ ──────────→  │  COMMITTED   │
│  DIRECTORY   │             │    AREA      │              │   HISTORY    │
│              │ ←────────── │              │ ←──────────  │              │
│  (modified)  │ git checkout│  (staged)    │ git restore  │ (permanent)  │
│              │  <file>     │              │  --staged    │              │
│              │  [DESTROYS] │              │  <file>      │ git revert   │
│              │             │              │  [PRESERVES] │  [SOFT]      │
│              │             │              │              │ git reset    │
│              │             │              │              │  --hard      │
│              │             │              │              │  [HARD]      │
└──────────────┘             └──────────────┘              └──────────────┘
```

***

## `git diff` Behavior by Stage

```
UNSTAGED changes:
  git diff            → shows working dir vs staging area  ✅ works
  git diff --cached   → shows staging vs last commit       (nothing)

STAGED changes (after git add):
  git diff            → (nothing) ← working dir = staging now
  git diff --cached   → shows staging vs last commit       ✅ works

COMMITTED changes:
  git diff            → (nothing)
  git diff --cached   → (nothing)
  git diff A..B       → shows diff between commit A and B  ✅ works
```

***

## Rollback Decision Tree

```
Want to undo changes?
│
├── Changes NOT staged yet?
│   └── git checkout <file>        ← discards edits permanently
│
├── Changes STAGED (git add done)?
│   └── git restore --staged <file> ← moves back to working dir
│       └── Then optionally: git checkout <file> to discard
│
└── Changes COMMITTED?
    ├── Want to PRESERVE history?
    │   └── git revert HEAD         ← new commit undoing the change
    │
    └── Want to ERASE history?
        └── git reset --hard <id>   ← commits after <id> deleted
```

***

## Revert vs. Reset

```
git revert HEAD:
  Commit A → Commit B (bad) → Commit C (revert of B)
  Code at C = Code at A
  History: A, B, C all visible
  SAFE for shared repos

git reset --hard <A>:
  Commit A → Commit B (bad)  ← B deleted
  Code at A
  History: only A visible
  DANGEROUS for shared repos
```

***

## Inspection Commands (Pre-Rollback)

```
git status              → WHAT changed (which files, which stage)
git diff                → HOW it changed (unstaged: working vs staging)
git diff --cached       → HOW it changed (staged: staging vs last commit)
git diff <id1>..<id2>   → HOW it changed (committed: between two commits)
git log --oneline       → commit IDs + messages (compact)
```

***

## Command Quick-Reference

```
ROLLBACK:
  git checkout <file>           → discard unstaged edits
  git restore --staged <file>   → unstage (keep edits)
  git revert HEAD               → undo last commit (new commit, history kept)
  git revert <commit_id>        → undo specific commit
  git reset --hard <commit_id>  → erase all commits after <id>

INSPECT:
  git status                    → see file states
  git diff                      → see unstaged changes
  git diff --cached             → see staged changes
  git diff <id>..<id>           → compare two commits
  git log --oneline             → list commits compactly
```

***

## Operational Safety Pattern

```
BEFORE any rollback:
  1. git status         → identify what's changed
  2. git diff / --cached → review the exact changes
  3. Decide: keep or discard?
  4. (Optional) Confirm command with ChatGPT if unsure
  5. Execute rollback command

RULE: Always inspect before you rollback.
      Rollback commands can be destructive.
      git checkout <file> and git reset --hard are IRREVERSIBLE.
```

***

## Key Failure Points

```
❌ git diff shows nothing after staging   → use git diff --cached
❌ git checkout discarded wanted changes  → no recovery (should have used git diff first)
❌ git reset --hard on pushed commits     → breaks shared history for all collaborators
❌ Confused revert vs reset               → revert = safe + new commit; reset = destructive + erase
❌ Forgot commit ID for reset             → use git log --oneline to find it
```

***

## Reusable Engineering Patterns

**1. Stage-Specific Undo Pattern:** Each stage of a pipeline has its own undo mechanism. You cannot use a single "undo" across all stages — you must know where the change currently lives and apply the appropriate rollback for that specific stage. *Transferable to:* CI/CD pipeline rollbacks (build stage vs. deploy stage vs. production), database migration rollbacks (pending vs. applied), infrastructure state management (planned vs. applied in Terraform).

**2. Soft vs. Hard Rollback Pattern:** Two philosophies of undoing: **soft** (preserve the history of the mistake and its correction, creating an audit trail) vs. **hard** (erase all evidence, clean slate). The choice depends on whether the context is collaborative/shared or local/private. *Transferable to:* database rollback strategies (compensating transactions vs. point-in-time recovery), deployment rollback (blue-green switch vs. redeploy previous version), document version history (track changes vs. discard draft).

**3. Inspect-Before-Act Pattern:** Every rollback in the video is preceded by an inspection step (`git status` → `git diff`). Never execute a destructive operation without first confirming what you're about to destroy. *Transferable to:* `terraform plan` before `terraform apply`, `--dry-run` flags, pre-flight checks in deployment pipelines, `SELECT` before `DELETE` in databases. <cite>turn5search5</cite>

***

*This completes the full reconstruction of the Git rollback lecture. Theory builds the three-stage mental model and the conceptual difference between each rollback tool. Practical walks through exact commands at each stage with verification. Mental Compression Map provides rapid-recall decision trees and command references for future retrieval.*
