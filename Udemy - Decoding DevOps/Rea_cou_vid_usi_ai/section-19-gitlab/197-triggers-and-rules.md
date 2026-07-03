# 🎓 Deep Learning Material: GitLab CI/CD Rules — Controlling When Pipeline Jobs Execute with Triggers and Conditions

**Source:** Video lecture on GitLab CI/CD pipeline rules and triggers (from [197-triggers-and-rules.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt?EntityRepresentationId=e323dc4a-12cb-4e68-96d3-d3c7310aec3e) caption file), with pipeline YAML reference from [197.Rules.yml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197.Rules.yml?EntityRepresentationId=04aca470-9889-42f2-ac23-2f639bfc2e12) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197.Rules.yml)

**Video Context:** This lecture replaces the older, limited `only` keyword with the modern **`rules`** keyword for controlling when GitLab CI/CD jobs run. The instructor defines rules based on four trigger types (push to specific branches, merge requests, manual/web triggers, and scheduled pipelines), demonstrates them by pushing to `main` (triggers), pushing to a feature branch (doesn't trigger), and creating a merge request (triggers). The lecture also covers the complete merge request workflow — branch creation, commit, merge request, pipeline validation, merge, and branch cleanup — making it both a rules tutorial and a practical introduction to the GitLab merge request lifecycle.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Why Rules Exist: Controlling Job Execution in Pipelines

In a CI/CD pipeline, not every job should run on every event. A build triggered by a push to a feature branch may not need the same jobs as a push to `main`. A scheduled nightly pipeline might need different behavior than a merge request pipeline. Without control mechanisms, every defined job runs on every trigger — wasteful, potentially dangerous (deploying from a feature branch), and noisy. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

GitLab provides **`rules`** as the modern mechanism to define **conditions** under which a job should or should not execute. The instructor explicitly replaces the older `only: main` keyword: *"This is the old way to decide whether the pipeline runs and it's very limited. The best way is always with the rules."* The `only`/`except` keywords are limited to simple branch filtering. Rules offer full conditional logic using predefined variables, allowing you to express complex conditions like "run on pushes to main OR develop, OR on merge requests, OR on manual triggers, but never otherwise." [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## 1.2 — Rules Syntax and Evaluation Logic

Rules are defined as a **list of conditions** under the `rules:` keyword in a job definition, placed after `image:` and before `script:`. Each rule is a list item (prefixed with `-`) that specifies a condition. GitLab evaluates rules **top to bottom** — the first matching rule determines the job's behavior. If no rule matches and no `when: never` catch-all exists, the default behavior applies. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

A rule can use: [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

* **`if:`** — evaluates a condition expression against CI/CD predefined variables
* **`when:`** — specifies what happens when a condition matches (e.g., `never`, `manual`, `always`)
* **`allow_failure:`** — if true, the job's failure doesn't block subsequent jobs
* Other keywords like `changes`, `exists`, `needs`, `variables`, `interruptible`

The instructor focuses on `if` and `when` as the primary mechanisms, with a brief mention of `allow_failure` and `manual`.

***

## 1.3 — Predefined CI/CD Variables: The Data That Rules Evaluate

Rules don't operate on arbitrary data — they evaluate **predefined CI/CD variables** that GitLab automatically sets based on the context of the pipeline trigger. The two most important variables in this lecture are: [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**`CI_COMMIT_BRANCH`** — Contains the name of the branch that was pushed to. If you push to `main`, this variable's value is `"main"`. If you push to `develop`, its value is `"develop"`. If you push to `feature-91`, its value is `"feature-91"`. This variable is how you filter by branch name. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**`CI_PIPELINE_SOURCE`** — Contains the **trigger type** that started the pipeline. Its value tells you *how* the pipeline was initiated: [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

| Trigger Event                     | `CI_PIPELINE_SOURCE` Value |
| --------------------------------- | -------------------------- |
| Code pushed to a branch           | `"push"`                   |
| Merge request created/updated     | `"merge_request_event"`    |
| Manually triggered from GitLab UI | `"web"`                    |
| Triggered by a scheduled pipeline | `"schedule"`               |

The instructor explains: *"That means what triggers the pipeline. If the merge request triggers the pipeline then this variable value will be merge\_request\_event. But if it's triggered by a push then its value will be push."* [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## 1.4 — Building the Rule Set: The Four Trigger Conditions

The instructor builds a comprehensive rule set that covers the four most common trigger scenarios. Each is expressed as a separate `if:` condition: [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### Rule 1: Push to `main` or `develop`

```yaml
- if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"'
```

This checks: is the branch that received the push either `main` or `develop`? The `||` is the **OR operator**. The entire condition is wrapped in **single quotes**, and the branch names (`main`, `develop`) are in **double quotes** to match the exact string value. If either condition is true, the job runs. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

The instructor carefully points out the quoting: *"Single quotes starts over here and ends over there. So this all condition is in single quote. And this double quote is only for the keyword to match it with this variable value."* [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### Rule 2: Merge Request Event

```yaml
- if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

This triggers the job when a merge request is created or updated — regardless of which branches are involved. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### Rule 3: Manual Trigger (Web UI)

```yaml
- if: '$CI_PIPELINE_SOURCE == "web"'
```

This triggers when someone manually runs the pipeline from the GitLab web interface. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### Rule 4: Scheduled Pipeline

```yaml
- if: '$CI_PIPELINE_SOURCE == "schedule"'
```

This triggers when the pipeline runs on a configured schedule (e.g., nightly at 9 PM). [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### Catch-All: Never

```yaml
- when: never
```

This is the **safety net** at the end of the rules list. If none of the above conditions match, the job **does not run**. The instructor explains: *"only any of this condition matches, then only the job will run. Otherwise never."* He also notes: *"this is just to make sure that this job or this stage never runs if this conditions are not matched. So just to be sure, we can put this. Otherwise it's really not mandatory to put when never."* — meaning it's defensive but not strictly required, since unmatched rules default to not running anyway. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## 1.5 — Advanced Rule Evaluation: `when: manual` and `allow_failure`

The instructor briefly introduces more advanced rule behaviors from the GitLab documentation example: [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**`when: manual`** — Instead of running automatically when the condition matches, the job appears in the pipeline but requires a **manual click** to execute. *"That means it's not going to run automatically. You need to click on the button and decide whether to run it or not."* [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**`allow_failure: true`** — If the job fails, the pipeline continues to the next job instead of stopping. *"Even if this job fails, still go to the next job."* [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

The instructor also mentions that a bare variable reference in a condition (just `$SOME_VARIABLE` without a comparison) evaluates as **boolean**: if the variable exists and is non-empty, it's true; if it's unset or empty, it's false. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## 1.6 — The Merge Request Lifecycle: Branches, Pipelines, and Merging

The second half of the lecture demonstrates the complete merge request workflow, which is both a practical demonstration of rule triggers and an introduction to a fundamental GitLab/DevOps workflow: [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**The workflow:** A developer creates a **feature branch** from `main`, makes changes in that branch, and then creates a **merge request** to merge those changes back into `main`. The merge request triggers a pipeline (because of the `merge_request_event` rule). If the pipeline passes, the code can be merged. After merging, the feature branch is deleted. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

The instructor elevates the importance of merge requests significantly: *"Do not take this merge request lightly. In fact, in GitOps project setup, everything revolves around this merge request... Any change goes through the merge request only."* [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

The merge request serves multiple purposes: code review (assigning reviewers), automated validation (triggering pipelines), and controlled integration (merging only after tests pass). This is the foundation of **trunk-based development** and **GitOps** workflows.

> 🔍 **Deep Dive**
>
> The instructor demonstrates a critical behavioral difference: pushing to `main` triggers the pipeline (matches Rule 1), but pushing to `feature-91` does **not** trigger any pipeline (doesn't match any rule — `feature-91` is not `main` or `develop`, and it's not a merge request, web trigger, or schedule). This proves the rules work as intended — they act as a **whitelist** of conditions. Only explicitly matched conditions trigger execution. The feature branch commit only triggers a pipeline later, when a merge request is created from it. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## 1.7 — Branch Cleanup: Local and Remote Synchronization

After a merge request is merged with the "delete source branch" option checked, the feature branch is removed from GitLab (remote). But the local machine (VS Code) still has a reference to that branch. The instructor teaches the cleanup process: switch to `main`, delete the local branch, prune stale remote-tracking references, and sync. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

This is operationally important: stale branch references cause confusion in branch listings and can lead to accidentally working on a deleted branch. The instructor states this cleanup is **mandatory before the next lecture**. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are adding **`rules`** to a GitLab CI/CD pipeline to control exactly when each job runs — replacing the older `only` keyword. We then validate the rules by testing three scenarios: push to `main` (triggers), push to a feature branch (doesn't trigger), and creating a merge request (triggers). The final outcome: a pipeline that intelligently responds only to specific events, plus a clean branch state ready for the next lecture.

***

## Step 1: Remove the Old `only` Keyword and Add Rules

**What we're doing:** Replacing the limited `only: main` with the modern `rules:` block in both jobs.

Open the `.gitlab-ci.yml` file in VS Code. Remove the `only: main` line from both jobs. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Add rules to the build job** (below `image:`, before `script:`):

```yaml
rules:
  # Trigger on pushes to main or develop
  - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"'
  # Trigger on merge requests
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  # Trigger when started manually
  - if: '$CI_PIPELINE_SOURCE == "web"'
  # Trigger on scheduled pipelines
  - if: '$CI_PIPELINE_SOURCE == "schedule"'
  # Otherwise never run
  - when: never
```

 [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197.Rules.yml)

**Breakdown of the YAML structure:**

* `rules:` — begins the rules block (replaces `only:`)
* Each `- if:` — a condition to evaluate; the value is a string expression in single quotes
* `$CI_COMMIT_BRANCH` — predefined variable: the branch name that received the push
* `==` — equality comparison
* `||` — logical OR operator
* `"main"`, `"develop"` — exact branch name strings in double quotes (inside the single-quoted expression)
* `$CI_PIPELINE_SOURCE` — predefined variable: how the pipeline was triggered
* `"merge_request_event"`, `"web"`, `"schedule"` — trigger type values
* `- when: never` — catch-all: if no condition above matched, don't run

**Copy the same rules block to the test job** — paste it in the same position (below `image:`, before `script:`). [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

The complete pipeline YAML now has both stages (`build`, `test`), global variables, and identical rules on both jobs: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197.Rules.yml)

```yaml
stages:
  - build
  - test

variables:
  PROJECT_NAME: "Vprofile-App"
  TEST_REPORT_DIR: "target/surefire-reports"
  JAVA_OPTS: "-Xms512m -Xmx1024m"

build-job:
  stage: build
  image: maven:3.9.9-eclipse-temurin-17
  rules:
    - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
    - when: never
  script:
    - pwd
    - ls -la
    - echo "Building project => $PROJECT_NAME"
    - mvn clean package -DskipTests

test-job:
  stage: test
  image: maven:3.9.9-eclipse-temurin-17
  needs: [build-job]
  rules:
    - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
    - when: never
  script:
    - echo "Running tests for $PROJECT_NAME with Java options => $JAVA_OPTS"
    - mvn test
    - mvn checkstyle:checkstyle
    - echo "Saving test reports in $TEST_REPORT_DIR"
  artifacts:
    paths:
      - $TEST_REPORT_DIR
    when: always
```

***

## Step 2: Commit and Push to Main — Validate Trigger

**What we're doing:** Pushing the updated pipeline to `main` to verify that the "push to main" rule triggers the pipeline.

1. In VS Code → Source Control → commit with message: `testing some triggers` [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
2. Push to `main`

**Go to GitLab → Build → Pipelines**

**Expected result:** A pipeline has been triggered. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Why it triggered:** The first rule matched — `$CI_COMMIT_BRANCH == "main"` is true because we pushed to `main`. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Wait for pipeline completion.** Both jobs should pass successfully. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## Step 3: Create a Feature Branch and Push — Validate NO Trigger

**What we're doing:** Proving that pushing to a branch that isn't `main` or `develop` does NOT trigger the pipeline.

### 3a: Create the branch in GitLab

1. Go to **Repository** → click the branch dropdown (showing `main`) → **New branch** [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
2. Branch name: `feature-91`
3. Create from: `main` → creates the branch with all content from `main` [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### 3b: Fetch and switch in VS Code

1. Source Control → three dots menu → **Fetch** (syncs remote branch info) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
2. Click the branch name in the bottom-left → select **feature-91** to switch to it [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### 3c: Make a change and push

1. Open `README.md` → make a small change (e.g., add text, remove a `#`) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
2. Commit with message: `updated Readme file`
3. Push (this pushes to `feature-91`, NOT `main`) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### 3d: Check GitLab pipelines

**Go to GitLab → Build → Pipelines**

**Expected result:** **No new pipeline triggered.** [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Why:** The branch is `feature-91`. The first rule checks `$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"` — both false. `CI_PIPELINE_SOURCE` is `"push"`, which doesn't match `"merge_request_event"`, `"web"`, or `"schedule"`. No rule matches → `when: never` applies → jobs don't run. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**This proves the rules are working correctly as a whitelist.**

***

## Step 4: Create a Merge Request — Validate Merge Request Trigger

**What we're doing:** Creating a merge request from `feature-91` to `main` and proving the merge request event triggers the pipeline.

### 4a: Create the merge request

1. In GitLab → **Merge Requests** → **Create merge request** [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
2. Source branch: `feature-91` → Target branch: `main`
3. Click **Compare branches and continue**
4. Title: keep default (or customize) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
5. **Assignee:** assign to yourself (in a real team, assign to a reviewer/admin) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
6. **Reviewer:** can assign a reviewer (instructor keeps it to their own user since only one user exists) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
7. Check **"Delete source branch when merge request is accepted"** [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
8. Click **Create merge request** [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

### 4b: Verify the pipeline triggered

**Expected result:** A pipeline appears with label **"merge request pipeline"**. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Why:** `$CI_PIPELINE_SOURCE == "merge_request_event"` matched — the second rule triggered both jobs. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Wait for both jobs to complete successfully.** [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## Step 5: Merge the Code

**What we're doing:** Merging the feature branch into `main` after the pipeline passes.

1. In the merge request page → click **Merge** [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
2. This merges the changes into `main` and **deletes** the `feature-91` branch on GitLab [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Verify:** Go to Repository → branch dropdown → only `main` should be visible. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

## Step 6: Clean Up the Local Branch (Mandatory)

**What we're doing:** Removing the now-deleted feature branch from the local machine to stay in sync with GitLab.

**Switch to main:**

```bash
git checkout main
```

**Delete the local branch:**

```bash
git branch -D feature-91
```

* `-D` — force delete (uppercase D forces deletion even if not fully merged locally) [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Check branches (will still show stale remote reference):**

```bash
git branch -a
```

* You'll still see `remotes/origin/feature-91` — this is a stale tracking reference [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Prune stale remote references:**

```bash
git fetch --prune
```

* `--prune` — removes remote-tracking references that no longer exist on the remote [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Verify clean state:**

```bash
git branch -a
```

* Should show only `main` and `remotes/origin/main` [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**Sync changes:** Click the sync button in VS Code or run `git pull`. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

**If anything goes wrong:** The instructor provides a nuclear option: *"close VS Code, delete the branch in GitLab and clone the repository once again. You can remove this folder and you can clone a new repository from GitLab. That will be a fresh repository."* [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

> ⚠️ **Expert Note**
>
> The instructor emphasizes this cleanup is **mandatory before the next lecture**: *"This is mandatory to do before we go to the next lecture."* Stale branches in the local environment can cause confusion when creating new branches or switching contexts. In team environments, developers should make branch cleanup a habit after every merged MR. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Rules: What They Replace and Why

```
OLD: only: main                  → limited to branch filtering only
NEW: rules:                      → full conditional logic with variables

Rules = whitelist of conditions. Job runs ONLY if a rule matches.
```

***

## 🔷 The Complete Rules Block

```yaml
rules:
  - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"'   # push to main/develop
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'                     # merge request
  - if: '$CI_PIPELINE_SOURCE == "web"'                                     # manual from UI
  - if: '$CI_PIPELINE_SOURCE == "schedule"'                                # scheduled run
  - when: never                                                            # catch-all safety
```

***

## 🔷 Key Predefined Variables

```
$CI_COMMIT_BRANCH      → branch name that received the push
                          "main", "develop", "feature-91", etc.

$CI_PIPELINE_SOURCE    → HOW the pipeline was triggered
                          "push"                → code pushed
                          "merge_request_event" → MR created/updated
                          "web"                 → manually from GitLab UI
                          "schedule"            → scheduled pipeline
```

***

## 🔷 Rule Evaluation Flow

```
Rules evaluated TOP → BOTTOM (first match wins)

Rule 1: branch == main OR develop?  ──YES──► RUN JOB
                                    ──NO───▼
Rule 2: source == merge_request?    ──YES──► RUN JOB
                                    ──NO───▼
Rule 3: source == web (manual)?     ──YES──► RUN JOB
                                    ──NO───▼
Rule 4: source == schedule?         ──YES──► RUN JOB
                                    ──NO───▼
Catch-all: when: never              ────────► SKIP JOB
```

***

## 🔷 Three Test Scenarios and Results

```
SCENARIO                           TRIGGER?   WHY
──────────────────────────         ────────   ─────────────────────────
Push to main                       ✅ YES     Rule 1: CI_COMMIT_BRANCH == "main"
Push to feature-91                 ❌ NO      No rule matches (not main/develop, not MR/web/schedule)
Create merge request (feature→main) ✅ YES    Rule 2: CI_PIPELINE_SOURCE == "merge_request_event"
```

***

## 🔷 Merge Request Lifecycle

```
1. Create feature branch (from main)
2. Make changes in feature branch
3. Push to feature branch → NO pipeline (rules filter it out)
4. Create Merge Request (feature → main)
   → Pipeline TRIGGERS (merge_request_event rule)
   → Assign reviewer, set options
5. Pipeline passes → click MERGE
   → Code merged to main
   → Source branch deleted (if option checked)
6. Cleanup local branch:
   git checkout main
   git branch -D feature-91
   git fetch --prune
   git branch -a  (verify clean)
```

***

## 🔷 YAML Structure (Where Rules Go)

```yaml
job-name:
  stage: <stage>
  image: <docker-image>
  rules:                    ← AFTER image, BEFORE script
    - if: '<condition>'
    - if: '<condition>'
    - when: never
  script:
    - <commands>
```

***

## 🔷 Additional Rule Keywords (Mentioned)

```
when: manual       → job exists but requires manual click to run
allow_failure: true → job failure doesn't block subsequent jobs
$VARIABLE          → bare variable as boolean (exists/non-empty = true)
```

***

## 🔷 Branch Cleanup Commands

```bash
git checkout main              # switch to main
git branch -D <branch>         # delete local branch
git branch -a                  # list all (shows stale remote ref)
git fetch --prune              # remove stale remote-tracking refs
git branch -a                  # verify: only main remains
```

**Nuclear option:** Delete local folder → re-clone from GitLab

***

## 🔷 Quoting Rules in YAML Conditions

```
OUTER: single quotes → wraps entire condition expression
INNER: double quotes → wraps string values being compared

Example:
  '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"'
   ^                    ^    ^                         ^          ^
   single quote start   double quotes for values       single quote end
```

***

## 🔷 Pipeline YAML Reference (Complete from .yml file)

```yaml
stages: [build, test]

variables:
  PROJECT_NAME: "Vprofile-App"
  TEST_REPORT_DIR: "target/surefire-reports"
  JAVA_OPTS: "-Xms512m -Xmx1024m"

build-job:                              test-job:
  stage: build                            stage: test
  image: maven:3.9.9-eclipse-temurin-17   image: maven:3.9.9-eclipse-temurin-17
  rules: [same 4 rules + never]           needs: [build-job]
  script:                                 rules: [same 4 rules + never]
    - mvn clean package -DskipTests       script:
                                            - mvn test
                                            - mvn checkstyle:checkstyle
                                          artifacts:
                                            paths: [$TEST_REPORT_DIR]
                                            when: always
```

***

## 🔷 Reusable Engineering Pattern: Event-Driven Conditional Execution

```
PATTERN: Whitelist-Based Trigger Filtering

EVENTS HAPPEN (push, MR, schedule, manual)
  │
  ▼
RULES EVALUATE (ordered conditions against event metadata)
  │
  ├── Match found → EXECUTE job
  │
  └── No match → SKIP job (when: never)

Key principle:
  - Default is DENY (when: never at the end)
  - Only explicitly matched conditions execute
  - Same rules applied to ALL jobs ensures consistent trigger behavior

This pattern appears in:
  - Firewall rules (allow specific traffic, deny all else)
  - IAM policies (allow specific actions, deny by default)
  - Event-driven architectures (process specific events, ignore others)
  - Kubernetes admission controllers (allow specific resources, deny rest)

The underlying model: explicit whitelist + implicit deny = controlled execution.
```

***

## 🔷 Merge Request Importance (Instructor's Emphasis)

```
"Do not take this merge request lightly."
"In GitOps project setup, everything revolves around this merge request."
"Any change goes through the merge request only."

MR = code review + automated validation + controlled integration
   = the GATE through which all changes flow
```

This single concept — that merge requests are the central control point for all code changes — is the foundational idea behind GitOps, and it's enabled precisely by the rules system taught in this lecture. The pipeline validates the code *before* it's merged, not after. [\[197-trigge...-and-rules \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/197-triggers-and-rules.txt)
