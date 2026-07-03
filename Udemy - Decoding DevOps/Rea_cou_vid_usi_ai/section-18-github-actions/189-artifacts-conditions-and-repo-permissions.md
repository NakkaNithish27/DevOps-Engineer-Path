# 📘 Deep Learning Material — Lecture 189: Artifact Storage, Repository Permissions & Conditions in GitHub Actions Workflows

***

## 🧠 OUTPUT SECTION 1: THEORY (DEEP LEARNING MODE)

***

### 1.1 Repository Permissions and the `GITHUB_TOKEN`

When a GitHub Actions workflow executes, GitHub automatically generates a special token called `GITHUB_TOKEN`. This token is the identity that your workflow uses to interact with the GitHub repository it runs in — it's how the workflow reads code, writes commits, pushes tags, creates releases, or performs any repository operation. By default, this token has **both read and write** permissions on the repository. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

This default is dangerous in certain contexts. Consider a workflow running on the `main` branch — the production branch. If the workflow has write permission, any step (including third-party actions you reference) could accidentally or maliciously commit changes, push code, or modify the repository content on your production branch. This is an unacceptable risk in real engineering. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

To solve this, GitHub Actions provides the `permissions` key at the workflow level. By placing `permissions:` right below the triggers (the `on:` block) and setting `contents: read`, you restrict the `GITHUB_TOKEN` to **read-only** access on repository contents. The workflow can still check out code, read files, and pull information — but it cannot write, commit, or push anything back to the repository. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189.%20workflow-main-3.yaml)

The `contents` keyword specifically controls access to repository contents (code, commits, branches). There are other permission scopes too (like `issues`, `pull-requests`, `packages`), but in this context, restricting `contents` to `read` is the critical security hardening step for production branch workflows.

> 🔍 **Deep Dive**
>
> The `permissions` key operates at the workflow level (applies to all jobs) or can be set at the job level for granular control. When set at the workflow level as shown here, every job in the workflow inherits this restriction. This follows the **principle of least privilege** — grant only the minimum access needed. The `GITHUB_TOKEN` is scoped per workflow run and expires after the run completes, so its permissions window is already limited in time, but restricting the scope adds a second layer of defense. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

> ⚠️ **Expert Note**
>
> In production environments, always restrict `permissions` to `read` on the main branch. Third-party actions you reference (via `uses:`) also inherit this token. A compromised or poorly written action with write access could push malicious code to your main branch. Explicit read-only permissions close this attack vector. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### 1.2 Artifacts in GitHub Actions

When a workflow runs, it operates inside an ephemeral runner (a temporary virtual machine). Everything that the workflow produces — compiled binaries, `.war` files, test reports, build outputs inside `target/` — exists only during that workflow run. **Once the workflow terminates, all data on that runner is destroyed.** [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

This is a fundamental problem: you spend compute time building an artifact (e.g., `vprofile-v2.war`), but if you don't explicitly save it somewhere, it vanishes. You can't download it, deploy it, or pass it to another job.

GitHub Actions solves this with the **upload-artifact** action (`actions/upload-artifact@v4`). This action takes files from the runner's filesystem and uploads them to GitHub's artifact storage, associated with that specific workflow run. After the workflow completes (even if it fails), you get a downloadable link on the workflow run page. Clicking it gives you a **zip file** containing all the artifacts matching the path you specified. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

The action requires two key input parameters passed via the `with:` block:

*   **`name`** — A human-readable label for the artifact bundle (e.g., `vprofile-app`). This is the name that appears on the download link in the GitHub UI.
*   **`path`** — The file path (or glob pattern) specifying what to upload. For example, `target/*.war` uploads every `.war` file inside the `target/` directory. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

The `target/` folder is created by `mvn install` — it's where Maven places compiled output. The glob `*.war` matches any file ending in `.war`. Your project might produce `.jar`, `.ear`, or other files — the path pattern adapts accordingly. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

> 🔍 **Deep Dive**
>
> Artifacts serve two key purposes: (1) **Persistence** — surviving beyond the ephemeral runner lifecycle, and (2) **Inter-job data transfer** — one job uploads an artifact, another job in the same workflow can download it using the companion `actions/download-artifact` action. This is essential because jobs in GitHub Actions run on separate runners and do not share filesystems. Artifacts bridge this gap. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

> ⚠️ **Expert Note**
>
> GitHub artifact storage has retention limits (default 90 days, configurable). In production CI/CD, artifacts are often also pushed to dedicated artifact repositories (Nexus, JFrog Artifactory, S3) for long-term storage and deployment pipelines. The `upload-artifact` action is excellent for short-term workflow-scoped persistence, but not a replacement for a proper artifact management system. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### 1.3 Conditions (`if`) and Status Check Functions

GitHub Actions provides an `if` keyword that controls whether a step executes. The `if` field accepts an expression that must evaluate to `true` or `false`. If `true`, the step runs; if `false`, it is skipped entirely. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

This is critical because real workflows aren't linear success paths. Steps fail, branches differ, and you need the workflow to **make decisions** — send a notification on failure, skip tests on non-main branches, or always execute cleanup regardless of prior outcomes.

#### 1.3.1 Status Check Functions

GitHub provides three built-in **status check functions** that evaluate the outcome of previous steps/jobs: [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

| Function    | Returns `true` when...                    | Use case                                              |
| ----------- | ----------------------------------------- | ----------------------------------------------------- |
| `success()` | All previous steps succeeded              | Default behavior (implicit if no `if` is specified)   |
| `failure()` | Any previous step failed                  | Sending failure notifications, alerts, tickets        |
| `always()`  | Always — regardless of success or failure | Cleanup steps, mandatory reporting, resource teardown |

**`success()`** is the **default**. Even when you don't write an `if` condition, GitHub Actions implicitly applies `if: success()`. This means every step by default only runs if all prior steps succeeded. This is why a failing step causes all subsequent steps to be skipped — the implicit `success()` condition evaluates to `false`. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**`failure()`** inverts this — the step runs **only if** a previous step failed. This is the mechanism for failure-handling logic: sending an email notification, a Slack alert, or raising an incident ticket. In the lecture, the example prints a message (`echo "the build job failed. Please check logs"`), but in production this would be a notification or ticket-creation step. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**`always()`** overrides both — the step executes no matter what happened before. This is for mandatory operations that must occur regardless of workflow outcome (e.g., releasing a lock, tearing down infrastructure, reporting metrics). [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

> 🔍 **Deep Dive**
>
> These functions inspect the **aggregate status** of all prior steps in the job. `failure()` returns `true` if *any* previous step failed — not just the immediately preceding one. This means a failure early in the job still triggers a `failure()` condition on a step much later in the sequence. The evaluation is cumulative, not step-to-step. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### 1.4 Branch-Based Conditions Using `github.ref`

Beyond status check functions, the `if` keyword can evaluate **context variables** — runtime metadata about the workflow execution environment. The most important one introduced here is `github.ref`. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

`github.ref` holds the **full Git reference** of the branch (or tag) that triggered the workflow. Its value is NOT just the branch name — it's in the full ref format: `refs/heads/<branch-name>`. So for the `main` branch, `github.ref` equals `refs/heads/main`. For a `bugfix` branch, it equals `refs/heads/bugfix`. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

This enables branch-conditional logic. In the lecture, the instructor uses this to:

1.  **Run `mvn test` and `mvn checkstyle:checkstyle` only on the `main` branch** — using `if: github.ref == 'refs/heads/main'`. If the workflow is triggered on any other branch (e.g., `develop`, `bugfix`), these steps are skipped. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

2.  **Print a skip notification on non-main branches** — using `if: github.ref != 'refs/heads/main'`. The `!=` operator (not equal) makes this step execute only when the branch is NOT `main`. The message printed is: "Skipping unit test and code analysis." [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

This is a powerful pattern: you can have a single workflow file that behaves differently depending on which branch triggered it. Main branch gets full testing; feature/bugfix branches get lighter treatment. This reduces workflow duplication and centralizes CI logic. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

> 🔍 **Deep Dive**
>
> The comparison uses `==` (double equals) for equality and `!=` for inequality. String values must be enclosed in single quotes. The `github` context object contains many other useful fields (`github.event_name`, `github.actor`, `github.repository`, etc.) that can all be used in `if` conditions for fine-grained workflow control. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### 1.5 YAML Syntax Sensitivity and Debugging Workflow Failures

The lecture also demonstrates an important operational reality: **YAML is extremely sensitive to syntax errors.** The instructor accidentally types an extra character in the workflow file, and the entire workflow fails immediately — not with a step failure, but with a **YAML parsing error** before any job even starts. GitHub reports the exact line number of the error (e.g., "error in YAML syntax on line 63"). [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

This teaches a critical lesson: workflow failures aren't always logic failures or command failures — they can be structural failures in the YAML itself. The debugging approach is: check the error message, identify the line number, fix the syntax, commit, and push again. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

> ⚠️ **Expert Note**
>
> In production, use a YAML linter (locally or as a pre-commit hook) to catch syntax errors before pushing. The GitHub Actions workflow validator also catches these, but the feedback loop (push → wait for runner → see error) is slow. Catching YAML errors locally saves significant time. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

***

## ⚙️ OUTPUT SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

### What We Are Building

We are enhancing an existing GitHub Actions CI/CD workflow (`Vprofile CICD Workflow`) with three new capabilities: (1) restricting repository write access for security, (2) saving build artifacts beyond workflow lifetime, and (3) adding conditional execution logic based on step outcomes and branch identity. The final outcome is a workflow that is safer, preserves its outputs, and makes intelligent decisions about what to execute. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189.%20workflow-main-3.yaml)

***

### Step 1: Add Repository Permissions (Read-Only)

**What we are doing:** Restricting the `GITHUB_TOKEN` to read-only access on repository contents.

**Why:** To prevent the workflow from accidentally writing to the repository (especially critical on the `main` branch, as discussed in Theory §1.1).

**Location in the file:** Directly below the trigger block (`on:` block), in the first column (no indentation).

**The configuration:**

```yaml
permissions:
  contents: read
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189.%20workflow-main-3.yaml), [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Breakdown:**

*   `permissions:` — Top-level workflow key that overrides the default token permissions.
*   `contents: read` — Sets the `contents` scope (repository code, commits, branches) to read-only. The token can no longer push, commit, or write to the repo.

**Verification:** After adding this and pushing, if any step in the workflow attempts a write operation (e.g., `git push`), it will fail with a permissions error. The workflow should run normally for read operations like checkout.

**Common mistake:** Placing `permissions:` inside a job block instead of at the workflow level. At the workflow level, it applies globally. Indentation matters — it must be at the root level (same column as `on:` and `jobs:`). [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### Step 2: Store Build Artifacts Using `upload-artifact`

**What we are doing:** Adding a step to the Build job that saves the compiled `.war` file(s) as downloadable artifacts.

**Why:** The runner is ephemeral — without this step, the build output (`target/vprofile-v2.war`) disappears when the workflow ends (see Theory §1.2).

**The step configuration:**

```yaml
- name: Upload Artifact
  uses: actions/upload-artifact@v4
  with:
    name: vprofile-app
    path: target/*.war
```

 [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Breakdown:**

*   `- name: Upload Artifact` — Human-readable step name (choose any descriptive name).
*   `uses: actions/upload-artifact@v4` — References the official GitHub upload-artifact action, version 4. This is a pre-built, ready-made action maintained by GitHub.
*   `with:` — Begins the input parameters block for this action.
*   `name: vprofile-app` — The label for the artifact bundle. This name appears in the GitHub UI as the downloadable link.
*   `path: target/*.war` — A glob pattern specifying which files to upload. `target/` is the Maven output directory. `*.war` matches any WAR file in that directory.

**What happens internally:** After `mvn install` completes and produces `target/vprofile-v2.war`, this step scans the `target/` directory for `*.war` files, compresses them into a zip archive, and uploads the zip to GitHub's artifact storage tied to this workflow run. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Expected result:** On the workflow run page in GitHub (under Actions), you will see a downloadable artifact link labeled `vprofile-app`. Clicking it downloads a zip file containing the `.war` file(s).

**Verification:** Navigate to the workflow run in the GitHub Actions tab → scroll to the "Artifacts" section at the bottom → confirm `vprofile-app` appears and is downloadable. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Common mistake:** Specifying the wrong `path`. If `mvn install` hasn't run yet (step ordering issue) or the path pattern doesn't match any files, the upload step will fail or upload nothing. Ensure this step comes **after** the Maven build step.

**Adapting for your project:** If your project produces `.jar` files instead of `.war`, change the path to `target/*.jar`. For multiple file types, you can use multiple path entries or a broader glob. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### Step 3: Add a Failure Notification Condition

**What we are doing:** Adding a conditional step that runs only if a previous step fails, printing a failure message.

**Why:** In real pipelines, you need failure-aware steps — notifications, alerts, or ticket creation. This step demonstrates the mechanism using the `failure()` status check function (see Theory §1.3).

**The step configuration:**

```yaml
- name: Notify if build fails
  if: failure()
  run: echo "the build job failed. Please check logs"
```

 [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Breakdown:**

*   `- name: Notify if build fails` — Descriptive step name.
*   `if: failure()` — The condition. `failure()` is a built-in status check function that returns `true` if any previous step in this job has failed. If all previous steps succeeded, this evaluates to `false` and the step is skipped.
*   `run: echo "the build job failed. Please check logs"` — The command to execute. Here it's a simple `echo`, but in production this would be replaced with a notification action (Slack, email, PagerDuty, etc.).

**What happens internally:** GitHub evaluates the `if` expression before deciding whether to execute the step. If the expression is `false`, the step shows as "skipped" in the workflow log (not failed, not succeeded — skipped). [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Verification:** If the build succeeds, this step will appear as skipped in the logs. To test it, you could intentionally break the Maven build (e.g., introduce a compilation error) and verify this step executes and prints the message.

**Other status check functions you can use in the same pattern:**

*   `if: success()` — Run only if all prior steps succeeded (this is the default even without an `if`).
*   `if: always()` — Run regardless of prior outcomes. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### Step 4: Add Branch-Based Conditions Using `github.ref`

**What we are doing:** Making the `mvn test` and `mvn checkstyle:checkstyle` steps run only on the `main` branch, and adding a notification step that prints a skip message on non-main branches.

**Why:** Not all branches need the same level of testing. Main branch (production) gets full tests; feature/bugfix branches can skip heavy analysis to save time and resources (see Theory §1.4).

**Condition on `mvn test` step:**

```yaml
- name: Maven Test
  if: github.ref == 'refs/heads/main'
  run: mvn test
```

 [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Breakdown:**

*   `if: github.ref == 'refs/heads/main'` — Evaluates whether the current branch is `main`. `github.ref` contains the full Git ref (e.g., `refs/heads/main`). The `==` operator compares strings. The branch name is in the format `refs/heads/<branch>`.

**Same condition applied to the checkstyle step:**

```yaml
- name: Checkstyle
  if: github.ref == 'refs/heads/main'
  run: mvn checkstyle:checkstyle
```

 [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Skip notification step (non-main branches):**

```yaml
- name: Skipping message
  if: github.ref != 'refs/heads/main'
  run: echo "Skipping unit test and code analysis"
```

 [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Breakdown:**

*   `if: github.ref != 'refs/heads/main'` — The `!=` operator means "not equal to." This step runs only when the branch is NOT `main` — e.g., `develop`, `bugfix`, `feature/xyz`.

**Expected behavior on `main` branch:** `mvn test` runs ✅, `mvn checkstyle:checkstyle` runs ✅, skip message is skipped ⏭️.

**Expected behavior on any other branch (e.g., `bugfix`):** `mvn test` skipped ⏭️, `mvn checkstyle:checkstyle` skipped ⏭️, skip message prints ✅ "Skipping unit test and code analysis." [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Common mistake:** Writing just `'main'` instead of `'refs/heads/main'`. The `github.ref` value always uses the full ref format — the short name won't match.

***

### Step 5: Commit, Push, and Handle YAML Errors

**What we are doing:** Committing and pushing all changes to trigger the workflow, and debugging any YAML syntax errors.

**The commit message used:** `"read permissions artifacts and conditions"` [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Process:** In VS Code → Source Control → Stage changes → Write commit message → Commit and Push.

**YAML error scenario:** The instructor accidentally introduced an extra character in the YAML file. The workflow failed immediately with the error: `"You have an error in the YAML syntax on line 63"`. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

**Debugging approach:**

1.  Read the error message — it gives the exact line number.
2.  Open the workflow file, navigate to that line.
3.  Identify and remove the erroneous character.
4.  Save, commit, and push again.

**Verification:** After the fix, the workflow triggers again and runs successfully. Check the Actions tab to confirm all jobs and steps execute (or skip) as expected based on the conditions. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

> ⚠️ **Expert Note**
>
> YAML errors halt the entire workflow before any job starts — they're not step-level failures. Always validate YAML locally before pushing. Tools like `yamllint` or VS Code YAML extensions with schema validation for GitHub Actions catch these errors instantly. [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

***

## 🧠 OUTPUT SECTION 3: MENTAL COMPRESSION MAP

***

### 🏗️ System Architecture

    Workflow: Vprofile CICD Workflow
    ├── Triggers: push (main, develop) | pull_request (main, develop) | manual | cron (weekdays 2:10 PM)
    ├── Permissions: contents → read-only (restricts GITHUB_TOKEN)
    ├── Job: Build
    │   ├── Checkout code
    │   ├── mvn install → produces target/*.war
    │   ├── upload-artifact@v4 → persists .war as "vprofile-app"
    │   ├── [if: failure()] → notify: "build job failed"
    │   └── Runner dies → artifact survives in GitHub storage
    └── Job: Testing (needs: Build)
        ├── Checkout code
        ├── [if: github.ref == refs/heads/main] → mvn test
        ├── [if: github.ref == refs/heads/main] → mvn checkstyle:checkstyle
        └── [if: github.ref != refs/heads/main] → echo "Skipping..."

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189.%20workflow-main-3.yaml), [\[189-artif-...d-repo-per \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/189-artif-con-and-repo-per.txt)

***

### 🔑 Core Concepts — Rapid Recall

| Concept                       | Key Point                                                                          |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| `GITHUB_TOKEN`                | Auto-generated per workflow run; default = read+write; restrict with `permissions` |
| `permissions: contents: read` | Workflow-level; prevents accidental writes to repo; security hardening             |
| Artifact problem              | Runner is ephemeral → build output dies with it                                    |
| `upload-artifact@v4`          | `name` = label, `path` = glob pattern; output = downloadable zip on workflow page  |
| `if:` keyword                 | Accepts expression → `true` = execute, `false` = skip                              |
| `failure()`                   | Returns `true` if ANY prior step failed                                            |
| `success()`                   | Default (implicit); `true` only if ALL prior steps succeeded                       |
| `always()`                    | Always returns `true`; overrides failure; for mandatory steps                      |
| `github.ref`                  | Full ref format: `refs/heads/<branch>`; NOT short name                             |
| `==` / `!=`                   | String comparison operators in `if` expressions; values in single quotes           |

***

### 🔄 Decision Flow — Conditions

    Step execution decision:
      ├── No `if` specified → implicit success() → runs only if all prior steps OK
      ├── if: failure() → runs only if something failed above
      ├── if: always() → runs no matter what
      ├── if: github.ref == 'refs/heads/main' → main branch only
      └── if: github.ref != 'refs/heads/main' → non-main branches only

***

### 🔗 Dependency & Interaction Chain

    mvn install → target/*.war → upload-artifact (path: target/*.war) → GitHub artifact storage → download zip
                                         ↑                                        ↓
                                  Ephemeral runner dies                  Artifact persists (90 days default)

    permissions: contents: read ──► GITHUB_TOKEN scoped to read ──► blocks any git push/write from workflow

    github.ref ──► evaluated at runtime ──► drives branch-conditional step execution

***

### ⚡ Reusable Engineering Patterns

| Pattern                                    | Instance in This Lecture                                                                |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Least Privilege**                        | `permissions: contents: read` — grant minimum access needed                             |
| **Ephemeral Compute + Persistent Storage** | Runner dies, artifact persists via explicit upload                                      |
| **Failure-Aware Pipelines**                | `if: failure()` → react to failures instead of silently continuing                      |
| **Branch-Conditional Behavior**            | Single workflow, different behavior per branch via `github.ref`                         |
| **Fail-Fast with Override**                | Default `success()` stops pipeline on failure; `always()` overrides for mandatory steps |
| **Declarative Control Flow**               | `if` conditions as declarative guards — not imperative if/else blocks                   |

***

### 🧩 Error Pattern

    YAML syntax error → entire workflow fails before any job starts
      → Error message gives exact line number
      → Fix: locate line → remove bad character → re-commit → re-push
      → Prevention: local YAML linting / VS Code schema validation

***

### 🗜️ One-Line Mental Models

*   **Permissions** = "Lock the door before running the factory."
*   **Artifacts** = "Save the product before demolishing the factory."
*   **`failure()`** = "Fire alarm — only activates when something goes wrong."
*   **`always()`** = "Security camera — runs no matter what."
*   **`github.ref` conditions** = "Different assembly lines for different product types, same factory."

***

This covers all content from the lecture. Would you like me to save this as a downloadable markdown file? 📄
