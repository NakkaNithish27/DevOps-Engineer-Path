# 📘 Deep Learning Material — Lecture 188: GitHub Actions Workflow Triggers & Action Inputs

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1.1 Action Inputs — Passing Parameters to Actions with `with`

GitHub Actions are reusable units of automation. Each action is published on the GitHub Marketplace and designed to perform a specific task — checking out code, logging into a container registry, building a Docker image, and so on. But many actions need **context-specific configuration** to behave correctly for *your* particular use case. This is where **inputs** come in. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

An input is a key-value parameter you pass to an action using the `with` keyword. It appears directly beneath the `uses` line in a workflow step. The structure is:

```yaml
steps:
  - name: Code checkout
    uses: actions/checkout@v4
    with:
      fetch-depth: 0
```

The `with` block is the **input delivery mechanism**. Every key inside it (like `fetch-depth`) corresponds to a named parameter that the action's author defined in the action's metadata (`action.yml`). The action reads these inputs at runtime and adjusts its behavior accordingly. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

**Why inputs exist:** Without inputs, every action would behave in exactly one way — its default. That would make actions rigid and useless for anything beyond the most generic scenario. Inputs make actions **parameterizable and reusable** across wildly different projects and requirements, turning each action into a configurable building block rather than a hardcoded script.

**The `fetch-depth` input — a concrete example:** The `actions/checkout@v4` action clones your repository's source code into the runner's workspace. By default, `fetch-depth` is `1`, meaning it performs a **shallow clone** — only the latest commit, no history. This is fast and sufficient for most build/test scenarios. However, when you set `fetch-depth: 0`, the action fetches **the entire commit history across all branches and tags**. This is necessary when your pipeline needs to compare commits, generate changelogs, compute semantic version tags from git history, or tag Docker images using commit metadata. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

In this course's workflow, `fetch-depth: 0` is used even though only the current commit ID is needed. The instructor includes it specifically to demonstrate how inputs work — showing that passing `fetch-depth: 0` changes the checkout behavior from a shallow clone to a full history clone. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Discovering available inputs:** Every action on the GitHub Marketplace has documentation listing all supported inputs, their descriptions, defaults, and whether they are required or optional. For `actions/checkout@v4`, you'll find inputs like `token` (for authentication), `ssh-key`, `submodules`, `fetch-depth`, and many more. You navigate to the Marketplace, search for the action (e.g., "checkout"), and read the documented `with` parameters. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

🔍 **Deep Dive**
The `with` keyword maps directly to the `inputs` section in an action's `action.yml` manifest. When GitHub's runner engine processes a step, it reads the `with` block, validates the keys against the action's declared inputs, applies defaults for any missing optional inputs, and passes all values as environment variables or direct arguments into the action's runtime. If you pass a key that doesn't exist in the action's manifest, it is typically ignored, but this varies by implementation. The key takeaway: `with` is the **interface contract** between your workflow and the action — you supply configuration, the action consumes it.

***

### 1.2 Workflow Triggers — The `on` Keyword

A GitHub Actions workflow is inert YAML until something **triggers** it. The `on` keyword at the top of the workflow file defines *when* the workflow should execute. Without `on`, the workflow has no activation condition and will never run. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

The trigger system is event-driven: GitHub monitors repository activity (pushes, pull requests, schedules, manual dispatches), and when a matching event occurs, the runner infrastructure picks up the workflow and begins execution. You can define **multiple triggers** simultaneously — the workflow activates when **any one** of the listed events fires. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

```yaml
on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]
  workflow_dispatch:
  schedule:
    - cron: "0 2 * * *"
```

This single `on` block registers four distinct triggers. The workflow will run on pushes, pull requests, manual dispatch, *or* on the cron schedule. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

***

### 1.3 The `push` Trigger

The `push` trigger fires whenever code is pushed (committed) to one of the specified branches. In the workflow file, it looks like:

```yaml
on:
  push:
    branches: [ "main", "develop" ]
```

When someone pushes a commit to `main` or `develop`, the workflow executes. Pushes to any other branch (e.g., `feature-xyz`) will **not** trigger this workflow. The `branches` filter is the scoping mechanism — it ensures the workflow only runs for branches that matter (typically protected or release-critical branches). [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

This trigger was already covered in a previous lecture, so the instructor moves quickly past it, but its structural importance is foundational: **push is the most common CI trigger** because every code change starts with a push.

***

### 1.4 The `pull_request` Trigger

The `pull_request` trigger fires when a pull request is **opened, synchronized (updated), or reopened** targeting one of the specified branches. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

```yaml
on:
  pull_request:
    branches: [ "main", "develop" ]
```

**Why this trigger matters:** In professional development workflows, developers do not push directly to the main branch. The main branch is typically **protected** — direct pushes are blocked. Instead, developers create **feature or bugfix branches**, make their changes there, and then raise a **pull request** (PR) to merge those changes into main. The PR is a formal request: "I want my code reviewed and merged into the target branch." [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

When a PR is raised targeting `main`, the `pull_request` trigger fires and the workflow executes. This allows the team to **validate the proposed changes before they are merged** — running tests, linting, security scans, etc. If the pipeline passes, the PR can be safely merged. If it fails, the merge is blocked or flagged.

**Branch filtering syntax — two equivalent formats:**

Format 1 — inline list:

```yaml
branches: [ "main", "feature" ]
```

Format 2 — YAML list:

```yaml
branches:
  - main
  - feature
```

Both are functionally identical. The instructor uses the inline bracket format (`[ "main" ]`) for compactness. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

🔍 **Deep Dive**
The `pull_request` trigger specifically activates when a PR targets the listed branch, not when it originates from it. So `branches: ["main"]` means "run this workflow when someone opens a PR *into* main," regardless of which branch the PR comes *from*. This is a common misunderstanding. The trigger is about the **destination**, not the source.

***

### 1.5 The `workflow_dispatch` Trigger — Manual Execution

```yaml
on:
  workflow_dispatch:
```

This trigger enables a **manual "Run workflow" button** in the GitHub Actions UI. No event needs to occur — a human clicks the button, and the workflow executes. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Why it exists:** Not every workflow is tied to code changes. Some workflows run infrastructure tasks, database migrations, cleanup scripts, or operational commands that should only execute on demand. Even for CI/CD workflows, `workflow_dispatch` is valuable during **initial development and testing** — you can trigger the pipeline without needing to push a commit. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

The keyword alone, with no additional configuration, is sufficient. Simply declaring `workflow_dispatch:` under `on` activates the manual trigger.

⚠️ **Expert Note**
`workflow_dispatch` also supports custom input fields (text boxes, dropdowns, booleans) that the user fills in when manually triggering. This makes it powerful for parameterized operational workflows — e.g., "deploy to which environment?" with a dropdown of `staging` / `production`. This capability is not covered in the lecture but is a natural extension of the concept.

***

### 1.6 The `schedule` Trigger — Cron-Based Automation

```yaml
on:
  schedule:
    - cron: "0 2 * * *"
```

The `schedule` trigger runs the workflow at **fixed time intervals** defined by a cron expression, regardless of whether any push, PR, or manual event occurred. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

**Why it exists:** Some workflows must run periodically — nightly builds, daily security scans, scheduled dependency updates, periodic health checks, or recurring reports. The `schedule` trigger decouples workflow execution from code activity entirely, turning GitHub Actions into a **time-based task scheduler**.

**Cron expression format (standard Linux cron):**

    ┌───────────── minute (0–59)
    │ ┌───────────── hour (0–23)
    │ │ ┌───────────── day of month (1–31)
    │ │ │ ┌───────────── month (1–12)
    │ │ │ │ ┌───────────── day of week (0–6, Sunday=0)
    │ │ │ │ │
    * * * * *

Examples from the lecture: [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

| Cron Expression | Meaning                             |
| --------------- | ----------------------------------- |
| `0 2 * * *`     | Every day at 2:00 AM UTC            |
| `10 14 * * *`   | Every day at 2:10 PM UTC            |
| `10 14 * * 1-5` | Weekdays (Mon–Fri) at 2:10 PM UTC   |
| `0 2 * 1 *`     | Every day in January at 2:00 AM UTC |

The `*` wildcard means "every" — every minute, every day, every month, etc. Ranges use hyphens: `1-5` means Monday (1) through Friday (5). [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

🔍 **Deep Dive**
GitHub Actions cron schedules use **UTC time exclusively**. There is no timezone override. Also, scheduled workflows run on the **default branch** (usually `main`), regardless of where the workflow file exists. GitHub does not guarantee exact-to-the-second timing for scheduled runs — there can be delays of several minutes during periods of high platform load. For time-critical operations, external schedulers with webhook triggers may be more reliable.

***

### 1.7 Branch Lifecycle in a PR Workflow — Conceptual Model

The lecture walks through a full pull request cycle, which implicitly teaches the **branching model** that underpins professional development workflows. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

The core concept: **the main branch is sacred**. Developers never commit directly to it. Instead:

1.  A **feature or bugfix branch** is created *from* main (e.g., `bugfix-901`). At creation, both branches have identical code.
2.  The developer makes changes only on the bugfix branch, keeping main untouched.
3.  When changes are complete, the developer **pushes the bugfix branch** to the remote and raises a **pull request** targeting main.
4.  The PR triggers the CI workflow, which validates the proposed changes.
5.  If validation passes, the PR is **merged** — the bugfix branch's changes flow into main.
6.  The bugfix branch, having served its purpose, is **deleted** both remotely (on GitHub) and locally.

This is the **feature branch workflow** — one of the most common Git branching strategies. It ensures main always contains validated, stable code. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

⚠️ **Expert Note**
In production environments, branch protection rules enforce this model: direct pushes to main are blocked, PRs require approvals and passing status checks (from the CI workflow), and force-pushes are disabled. The `pull_request` trigger is the CI enforcement point within this protection model.

***

### 1.8 Trigger Coexistence and Combinability

A single workflow file can declare **multiple triggers simultaneously**. The workflow from this lecture combines `push`, `pull_request`, `workflow_dispatch`, and `schedule` under the same `on` block. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

These triggers are **independent and additive** — each one can independently activate the workflow. A push fires it. A PR fires it. A manual click fires it. The cron schedule fires it. They do not conflict, interfere, or depend on each other. This combinability means a single workflow can serve multiple activation scenarios without duplication.

The instructor demonstrates this by **commenting out the push trigger** temporarily while testing the pull\_request trigger, confirming that commenting out one trigger disables only that specific activation path while others remain functional. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building

We are extending the `vprofile-action` GitHub Actions workflow (in file `workflow-main-2.yaml`) to:

1.  **Pass inputs to the checkout action** using `with` and `fetch-depth: 0`
2.  **Add multiple triggers**: `push`, `pull_request`, `workflow_dispatch`, and `schedule`
3.  **Execute a full pull request cycle** — create a branch, make changes, raise a PR, observe the trigger, merge, and clean up

The final outcome: a workflow file with four triggers and parameterized actions, validated through a complete branch-PR-merge cycle. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml), [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

***

### Step 1: Add Inputs to the Checkout Action

**What we are doing:** Adding the `fetch-depth: 0` input to the `actions/checkout@v4` step in both the `Build` and `Testing` jobs.

**Why:** To demonstrate how the `with` keyword passes parameters to actions, and to ensure a full git history clone (needed for commit-based operations in real pipelines).

**The configuration:**

```yaml
steps:
  - name: Code checkout
    uses: actions/checkout@v4
    with:
      fetch-depth: 0
```

**Breakdown:** [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml), [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

| Element                     | Purpose                                                             |
| --------------------------- | ------------------------------------------------------------------- |
| `uses: actions/checkout@v4` | Specifies the action to run (checkout action, version 4)            |
| `with:`                     | Opens the input parameter block                                     |
| `fetch-depth: 0`            | Input name `fetch-depth`, value `0` — fetches entire commit history |

**Apply to both jobs:** The workflow has two jobs — `Build` and `Testing`. Both need the source code, so both get the checkout step with `fetch-depth: 0`. The `Testing` job has `needs: Build`, so it runs sequentially after Build completes.

**Verification:** After committing, check the workflow run logs. In the "Code checkout" step, you should see git fetching the full history rather than a shallow clone.

**How to discover other inputs:** Go to <https://github.com/marketplace>, search for "checkout" (or any action), and read the documented inputs. For `actions/checkout@v4`, you'll find parameters like `token`, `ssh-key`, `submodules`, `fetch-depth`, etc. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

***

### Step 2: Configure the `push` Trigger with Branch Filtering

**What we are doing:** Setting the `push` trigger to fire only for the `main` and `develop` branches.

```yaml
on:
  push:
    branches: [ "main", "develop" ]
```

**Why:** We want the CI pipeline to run whenever code is pushed to these critical branches, but not for every random feature branch push. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

**Branch list format options:**

Inline (used in this workflow):

```yaml
branches: [ "main", "develop" ]
```

Multi-line:

```yaml
branches:
  - main
  - develop
```

Both are equivalent YAML representations. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Verification:** Push a commit to main → the workflow should trigger. Push to an unlisted branch → the workflow should NOT trigger.

***

### Step 3: Add the `pull_request` Trigger

**What we are doing:** Adding a `pull_request` trigger so the workflow fires when a PR is raised targeting the specified branches.

```yaml
on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]
```

**Why:** In professional workflows, code enters main via pull requests. The CI pipeline must validate the proposed changes before merge. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Alignment note:** `push` and `pull_request` must be at the **same indentation level** under `on:`. They are sibling triggers. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Testing the PR trigger (full walkthrough follows in Steps 5–10):** The instructor temporarily **comments out the push trigger** to isolate the PR trigger for testing. This is done by adding `#` before the push-related lines:

```yaml
on:
  # push:
  #   branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main" ]
```

Committing this change to main does NOT trigger the workflow (because the push trigger is commented out), confirming that only active triggers fire. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

***

### Step 4: Add `workflow_dispatch` and `schedule` Triggers

**What we are doing:** Adding manual and time-based triggers.

```yaml
on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]
  workflow_dispatch:
  schedule:
    - cron: "0 2 * * *"
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

**`workflow_dispatch:`** — No additional configuration needed. Just the keyword. This adds a "Run workflow" button in the Actions tab on GitHub. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**`schedule:`** — Uses cron syntax. `"0 2 * * *"` means every day at 2:00 AM UTC.

**Cron field reference:**

    minute  hour  day-of-month  month  day-of-week
      0       2       *           *        *

*   `0` → at minute 0
*   `2` → at hour 2 (2 AM UTC)
*   `*` → every day of month
*   `*` → every month
*   `*` → every day of week

**Instructor's additional examples:** [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

*   `10 14 * * 1-5` → Weekdays at 2:10 PM UTC (0=Sunday, 1=Monday, 5=Friday)

**Verification for `workflow_dispatch`:** Go to the Actions tab → select the workflow → click "Run workflow" dropdown → click "Run workflow." The pipeline should execute.

**Verification for `schedule`:** Wait for the scheduled time, then check the Actions tab for an automatically triggered run.

***

### Step 5: Create a Bugfix Branch on GitHub

**What we are doing:** Creating a new branch from main on GitHub's web interface to simulate a developer branching workflow. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Why:** To test the `pull_request` trigger, we need a separate branch to merge into main.

**Steps:**

1.  Go to your repository on GitHub.
2.  Click the branch dropdown (showing "main").
3.  Type a new branch name: `bugfix-901`.
4.  Click "Create branch: bugfix-901 from main."

**Result:** The new branch `bugfix-901` is created with an exact copy of main's code. Both branches are identical at this point. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

***

### Step 6: Pull the New Branch Locally and Switch to It

**What we are doing:** Fetching the newly created remote branch into our local machine and switching to it.

**Commands:**

```bash
git fetch origin
```

**Breakdown:** `git fetch origin` contacts the remote repository (`origin`) and downloads all new references (branches, tags) without modifying your working directory. After this, your local Git knows about `bugfix-901`. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

```bash
git checkout bugfix-901
```

**Breakdown:** `git checkout bugfix-901` switches your working directory to the `bugfix-901` branch. Your VS Code branch indicator (bottom-left) should now show `bugfix-901`.

**Alternative:** You can also click the branch indicator in VS Code's bottom-left corner and select the branch from the dropdown. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

***

### Step 7: Make Changes on the Bugfix Branch

**What we are doing:** Simulating a developer fixing a bug — deleting unnecessary files and editing content. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Changes made:**

1.  **Delete** the `Jenkinsfile` (right-click → Delete in VS Code)
2.  **Delete** the `vagrant` folder
3.  **Edit** `README.md` — modify content (e.g., ensure it says "JDK 21")

**Why:** These are arbitrary changes to simulate real development work. The specific changes don't matter for the trigger demonstration — what matters is that the bugfix branch diverges from main.

***

### Step 8: Commit and Push the Bugfix Branch

**Commands:**

```bash
git add .
```

**Breakdown:** Stages **all** changes in the current directory (deletions, modifications, new files) for commit. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

```bash
git commit -m "Fixed bug 901"
```

**Breakdown:** Creates a commit with the message "Fixed bug 901." The `-m` flag allows the message inline.

```bash
git push origin bugfix-901
```

**Breakdown:** Pushes the local `bugfix-901` branch to the remote (`origin`). After this, GitHub has the updated bugfix branch with your changes. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Result:** The bugfix branch is now **ahead of main** on GitHub — it has commits that main doesn't have.

**Common mistake:** The instructor initially made a typo in the branch name during push. Always double-check the branch name matches exactly.

***

### Step 9: Raise a Pull Request and Observe the Trigger

**What we are doing:** Creating a PR to merge `bugfix-901` into `main`, which triggers the `pull_request` workflow. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Steps:**

1.  Go to the repository on GitHub.
2.  You may see a banner: "bugfix-901 had recent pushes — Compare & pull request." You can click that, or:
3.  Go to **Pull requests** tab → **New pull request**.
4.  Set **base**: `main` (target) and **compare**: `bugfix-901` (source).
5.  Review the changes shown.
6.  Click **Create pull request**.
7.  Add a title and description → Click **Create pull request**.

**What happens immediately:** The workflow triggers automatically. You can see this:

*   Directly on the PR page — a status check appears showing the pipeline running.
*   On the **Actions** tab — a new workflow run appears. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**This confirms the `pull_request` trigger works.** The workflow ran because a PR was raised targeting `main`, and our trigger is configured for `pull_request: branches: ["main"]`.

***

### Step 10: Merge the Pull Request and Clean Up

**Merging:**

1.  After the workflow completes successfully, click **Merge pull request** on the PR page.
2.  Click **Confirm merge**.
3.  Click **Delete branch** to remove `bugfix-901` from GitHub. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

**Result:** The bugfix branch's changes are now in main. The remote bugfix branch is deleted.

**Local cleanup — important step often forgotten:**

Switch to main first:

```bash
git checkout main
```

Delete the local bugfix branch:

```bash
git branch -d bugfix-901
```

**Breakdown:** `git branch -d` deletes the specified local branch. The lowercase `-d` is the "safe delete" — it refuses if the branch has unmerged changes.

**If `-d` fails** (e.g., Git thinks changes aren't merged):

```bash
git branch -D bugfix-901
```

Capital `-D` **force-deletes** the branch regardless of merge status. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

Prune stale remote-tracking references:

```bash
git fetch --prune
```

**Breakdown:** `--prune` removes local references to remote branches that no longer exist (like the deleted `bugfix-901` on GitHub). Without this, your local Git still "remembers" the remote branch even though it's gone.

Verify branch state:

```bash
git branch -a
```

**Breakdown:** Lists **all** branches — local and remote-tracking. You should see only `main` (and `remotes/origin/main`). [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

Pull latest changes:

```bash
git pull
```

**Breakdown:** Fetches and merges the latest main branch content (which now includes the merged bugfix changes) into your local main. [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt)

***

### Step 11: Final Commit of All Triggers

**What we are doing:** Uncommenting the push trigger, ensuring all four triggers are active, and committing the final workflow file.

**Final `on` block:**

```yaml
on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]
  workflow_dispatch:
  schedule:
    - cron: "0 2 * * *"
```

**Save** (`Ctrl+S`), **commit**, and **push** to main. This push itself triggers the workflow (via the push trigger). [\[188-trigge...and-inputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188-triggers-and-inputs.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/188.%20workflow-main-2.yaml)

**Verification:** Go to Actions tab → confirm a new workflow run has been triggered by the push event.

⚠️ **Expert Note**
When multiple triggers are active simultaneously, be aware that certain events can cause **double runs**. For example, merging a PR into main fires both the `pull_request` (closed/merged) event *and* a `push` event (because code was pushed to main via the merge). This results in two workflow runs for the same code change. In production, you may want to use conditional logic (`if:` expressions) or separate workflows to avoid redundant runs and wasted runner minutes.

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### System Architecture — Single Workflow, Multiple Activation Paths

    GitHub Repository
      └── .github/workflows/workflow-main-2.yaml
            │
            ├── on:                          ← TRIGGER LAYER (4 independent paths)
            │     ├── push → branches filter
            │     ├── pull_request → branches filter
            │     ├── workflow_dispatch → (no config needed)
            │     └── schedule → cron expression
            │
            └── jobs:                        ← EXECUTION LAYER
                  ├── Build  (ubuntu-latest)
                  │     └── checkout@v4 + with: fetch-depth: 0
                  └── Testing (ubuntu-latest, needs: Build)
                        └── checkout@v4 + with: fetch-depth: 0

***

### Trigger Decision Map

    When does the workflow run?
      ├── Code pushed to main/develop?       → YES → push trigger fires
      ├── PR opened targeting main/develop?  → YES → pull_request trigger fires
      ├── Manual button clicked?             → YES → workflow_dispatch fires
      └── Cron time reached?                 → YES → schedule fires

    All triggers are INDEPENDENT. Any one fires → workflow runs.
    Commenting out a trigger = disabling only that path.

***

### Action Input Model

    Action (e.g., actions/checkout@v4)
      ├── Default behavior: shallow clone (fetch-depth: 1)
      ├── with:                      ← INPUT INTERFACE
      │     └── fetch-depth: 0       → full history clone
      └── Discovery: GitHub Marketplace → action docs → list of inputs

**Key relationship:** `with` = interface contract between workflow and action.

***

### Branch List Syntax — Two Equivalent Forms

    Inline:     branches: [ "main", "develop" ]
    Multi-line: branches:
                  - main
                  - develop

Identical behavior. Style choice only.

***

### PR Workflow Lifecycle — Operational Sequence

    1. Create branch from main          → git branch on GitHub UI
    2. Fetch + checkout locally          → git fetch origin → git checkout <branch>
    3. Make changes                      → edit/delete files
    4. Stage + commit + push             → git add . → git commit -m "msg" → git push origin <branch>
    5. Raise PR (branch → main)         → GitHub UI → New Pull Request
    6. Workflow auto-triggers            → pull_request trigger fires
    7. Pipeline passes → Merge PR       → Merge pull request → Confirm
    8. Delete remote branch              → Delete branch button
    9. Local cleanup:
         git checkout main
         git branch -d <branch>          (or -D to force)
         git fetch --prune
         git branch -a                   (verify: only main remains)
         git pull                        (sync local main)

***

### Cron Expression Quick-Reference

    Position:   1       2       3            4       5
    Field:    minute   hour   day-of-month  month   day-of-week
    Range:    0-59    0-23    1-31         1-12     0-6 (Sun=0)
    Wildcard: *  = every
    Range:    1-5 = Mon through Fri

***

### Key Cause → Effect Chains

    push to main              → push trigger → workflow runs
    PR opened targeting main  → pull_request trigger → workflow runs
    push trigger commented    → push to main → NO workflow run
    PR merged into main       → push event + PR event → potential DOUBLE run
    workflow_dispatch declared → "Run workflow" button appears in UI
    schedule declared         → GitHub cron scheduler activates → runs at UTC time
    fetch-depth: 0            → full history cloned (all branches, all tags)
    fetch-depth: 1 (default)  → shallow clone (latest commit only)

***

### Git Cleanup Command Chain (Post-Merge)

    git checkout main         → ensure on main
    git branch -d <branch>    → safe delete (fails if unmerged)
    git branch -D <branch>    → force delete (always works)
    git fetch --prune         → remove stale remote refs
    git branch -a             → verify only main remains
    git pull                  → sync local with remote main

***

### Reusable Engineering Patterns Extracted

| Pattern                              | Instance in This Lecture                                               |
| ------------------------------------ | ---------------------------------------------------------------------- |
| **Parameterizable Component**        | Actions accept `with` inputs → configurable behavior                   |
| **Event-Driven Activation**          | `on:` block = event subscription model                                 |
| **Multiple Independent Triggers**    | Four triggers coexist, any one activates the pipeline                  |
| **Branch Protection Model**          | Main is sacred → changes enter only via validated PRs                  |
| **Validation Gate**                  | PR trigger = CI runs before merge is allowed                           |
| **Temporal Decoupling**              | `schedule` trigger = execution independent of human activity           |
| **Manual Override**                  | `workflow_dispatch` = human-initiated bypass of event dependency       |
| **Interface Contract**               | `with` block = defined parameter interface between workflow and action |
| **Create → Use → Destroy Lifecycle** | Branch created → used for changes → merged → deleted                   |

***

This material covers everything conveyed in the lecture. You can save this as a `.md` file for your learning library — want me to generate a downloadable markdown file? 📄
