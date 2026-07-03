# 🧠 GitLab CI/CD Variables — Definition, Access, Secrets & Predefined Variables

**Source:** *196. Variables and More* — GitLab CI/CD Pipeline Series (Video Caption Reconstruction + Pipeline YAML)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why Variables Exist in CI/CD Pipelines

In any CI/CD pipeline, certain values appear repeatedly — project names, memory settings, branch names, connection strings. Hardcoding these values in every script line creates a maintenance problem: if a value changes, you'd have to find and update every occurrence. Variables solve this by letting you **define a value once and reference it everywhere**. But beyond simple reuse, variables in GitLab CI/CD serve a deeper purpose — they are the mechanism through which **configuration, secrets, and runtime context** flow into the pipeline execution environment.

The video teaches three distinct categories of variables, each with a different origin, visibility model, and purpose: **pipeline-defined variables**, **UI-defined variables** (including secrets), and **predefined CI/CD variables**. Understanding where each type lives, who can see it, and how it gets injected into the pipeline is the core conceptual framework of this lecture.

***

## 1.2 Pipeline-Defined Variables — Inline Configuration

The simplest form of variable is defined directly in the `.gitlab-ci.yml` pipeline file using the `variables:` keyword at the top level. You give a name and a value:

```yaml
variables:
  PROJECT_NAME: vprofile
```

These variables are **plain and simple**. Their purpose is to define keywords or values that you want to use multiple times across stages and jobs without repeating them. The instructor frames the use case clearly: *"We just want to use a keyword multiple times in our pipeline. So we define it at this level."*

The critical characteristic of pipeline-defined variables is **full visibility**. The values are written directly in the YAML file, which lives in the Git repository. Anyone with access to the project repository can see them. The instructor explicitly states: *"We don't mind people in the project to see the value of these variables."* This makes them suitable for non-sensitive configuration — project names, paths, version identifiers — but completely unsuitable for secrets like passwords or tokens.

***

## 1.3 UI-Defined Variables — Project-Level Configuration with Controls

The second type of variable is defined through the **GitLab web interface**: Project → Settings → CI/CD → Variables. These variables are stored outside the repository, in GitLab's project configuration layer.

Both pipeline-defined and UI-defined variables *"serve almost the same purpose"* — they inject values into the pipeline execution. The choice between them is **based on your requirement**, specifically around visibility, security, and scope control. UI-defined variables provide several capabilities that pipeline-defined variables cannot:

### Variable Type: Variable vs. File

When adding a UI variable, you can choose the type as **Variable** (default) or **File**. The default "Variable" type stores a simple key-value pair. The "File" type writes the value to a temporary file and exposes the file path as the variable's value — useful for certificates or configuration files, though this lecture focuses on the standard variable type.

### Environment Scope

UI variables can be **scoped to specific environments** — production, test, staging. If your pipeline uses environment designations, you can make a variable available only in a specific environment. By default, the scope is **all environments** — the variable is available everywhere. This allows you to have different database connection strings for production vs. staging, stored under the same variable name but scoped to different environments.

### Visibility Levels — The Three Tiers

This is the most important conceptual distinction in UI variables. GitLab offers three visibility levels, each with different security implications:

**Visible** — The variable value can be seen in the GitLab Settings UI **and** in the job logs. No protection at all. This is essentially the same as a pipeline-defined variable, just stored in the UI instead of the YAML file.

**Masked** — The variable value is **masked in job logs** (replaced with `[MASKED]`), but **you can still see it** in the Settings UI. This prevents accidental exposure in logs but doesn't fully protect the value from anyone with project settings access.

**Masked and Hidden** — This is a **secret**. Once saved, **you cannot see the value** in the Settings UI anymore. It's also masked in job logs. You can **edit** it (replace the value) and **delete** it, but you can **never view** the saved value again. The instructor emphasizes: *"The secret variables are not exposed. You cannot see them."*

The instructor's guidance on when to use secrets: *"Things like database password, access keys on your AWS account, tokens, or any other things that you do not want to reveal in the pipeline, or also even in the settings."*

> 🔍 **Deep Dive:** The three visibility tiers represent a progressive security model. Visible = no protection. Masked = log protection only (someone with settings access can still read the value). Masked+Hidden = full protection (no one can read the value after creation — not even the person who created it). The practical implication: if you need to verify the current value of a masked+hidden secret, you cannot. You can only delete and recreate it. This is a deliberate security design — it prevents secrets from being exfiltrated through the UI.

### Protected Variable Flag

UI variables have a **Protect variable** flag. When enabled, the variable is **only accessible in protected branches** (like `main`). If a pipeline runs on a non-protected branch (a feature branch, bugfix branch, etc.), the protected variable will not be injected — it won't be available at all.

The instructor explains the reasoning: protected branches like `main` are branches *"where you don't want anybody to commit."* Code goes through merge requests to reach `main`. Making a variable protected ensures that sensitive values (like production credentials) are only available in pipelines running on the controlled, protected branch — not in any random feature branch someone creates.

> ⚠️ **Expert Note:** If you save a variable as protected and your pipeline runs on a non-protected branch, the variable will be empty or undefined. This can cause confusing failures where the pipeline works on `main` but breaks on feature branches. Always consider branch protection status when deciding whether to protect a variable.

***

## 1.4 Accessing Variables — Two Syntax Forms

Variables are accessed in pipeline scripts using the **dollar sign** prefix, with two syntax options:

**Form 1: `$VARIABLE_NAME`** — Simple, direct reference. Works for standalone variable access.

**Form 2: `${VARIABLE_NAME}`** — Curly-brace syntax. Functionally equivalent for simple access, but provides additional capabilities: **concatenation** with other text, **default values**, and **error handling**.

The instructor demonstrates concatenation: `${PROJECT_NAME}-test` produces `vprofile-test`. With the simple `$` form, the shell might not correctly determine where the variable name ends and the literal text begins (especially when the variable is immediately followed by alphanumeric characters). The curly-brace form explicitly delimits the variable name.

Both forms work in `echo` commands, `script:` blocks, and anywhere shell variable expansion is supported.

***

## 1.5 Bridging UI Variables into Pipeline Variables

A powerful pattern demonstrated in the video: you can **reference a UI-defined variable inside a pipeline-defined variable**. The YAML shows:

```yaml
variables:
  JAVA_OPTS: ${JAVA_OPTIONS}
```

Here, `JAVA_OPTIONS` is defined in the GitLab UI (with the value containing Maven memory settings like `-Xms512m -Xmx1024m`). In the pipeline, `JAVA_OPTS` is defined as a pipeline variable whose value is the *resolved* content of `JAVA_OPTIONS`. This creates an alias — a pipeline-level variable name that's meaningful for the build tool (Maven uses `JAVA_OPTS`), populated from a UI-level variable that's managed through the settings interface.

This pattern separates **where values are managed** (UI, with visibility controls and protection) from **what names the pipeline uses** (YAML, with tool-meaningful names).

***

## 1.6 Predefined CI/CD Variables — Runtime Context Injection

GitLab automatically injects a large set of **predefined variables** into every pipeline run. These variables provide runtime context about the commit, branch, pipeline, and trigger event. The instructor introduces four key predefined variables:

**`CI_COMMIT_BRANCH`** — The name of the branch on which the commit was made and the pipeline is running. Example value: `main`. Use case: conditional logic — run certain stages only on specific branches.

**`CI_COMMIT_MESSAGE`** — The text of the commit message that triggered the pipeline.

**`CI_COMMIT_SHA`** — The full SHA hash of the commit. The instructor notes this is *"very useful in tagging, versioning your artifact like Docker images"* — you can tag a Docker image with the commit SHA to create a direct, traceable link between an image and the exact code it was built from.

**`CI_PIPELINE_SOURCE`** — How the pipeline was triggered. Possible values include `push` (a code commit), `merge_request_event` (a pull/merge request), `schedule` (a scheduled trigger), and others. Use case: conditional pipeline behavior based on trigger type.

The instructor emphasizes these predefined variables will be used for **conditions** in the next lecture. In this lecture, they are simply printed to demonstrate their existence and values. The practical output showed: `CI_PIPELINE_SOURCE` = `push` and `CI_COMMIT_BRANCH` = `main`, confirming the pipeline was triggered by a push to the main branch.

> 🔍 **Deep Dive:** Predefined variables transform a pipeline from a static script into a **context-aware execution system**. Without them, the pipeline would be blind to its own trigger, branch, commit, and environment. With them, you can build conditional logic: deploy only on `main`, skip tests on documentation-only commits, tag artifacts with commit SHAs for traceability, behave differently when triggered by a schedule vs. a push. They are the pipeline's **self-awareness mechanism**.

***

## 1.7 The Variable Hierarchy — Three Sources, One Pipeline

Pulling all the concepts together, GitLab CI/CD has three distinct variable sources that all feed into the same pipeline execution:

1. **Pipeline-defined** (YAML `variables:`) — visible to everyone, simple reuse, lives in the repository
2. **UI-defined** (Settings → CI/CD → Variables) — controllable visibility, environment scoping, branch protection, secret capability, lives outside the repository
3. **Predefined** (GitLab-injected) — automatically available, provides runtime context about the pipeline, commit, and trigger

All three are accessed with the same `$` or `${}` syntax. The pipeline execution environment merges them all, and any script line can reference any of them seamlessly.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are configuring and testing **three types of variables** in a GitLab CI/CD pipeline: inline pipeline variables, UI-managed variables (including a secret), and predefined variables. The goal is to see each type injected into a running pipeline, verify their values in job logs, and observe how masking/hiding behaves in practice.

**Final outcome:** A pipeline that echoes all three variable types, demonstrating normal variable display, secret masking in logs, variable concatenation, and predefined runtime context — all verified through job log inspection.

***

## Step 1: Define Pipeline Variables in `.gitlab-ci.yml`

Open your pipeline YAML file in **VSCode**. Under the top-level `variables:` block, define:

```yaml
variables:
  PROJECT_NAME: vprofile
  JAVA_OPTS: ${JAVA_OPTIONS}
```

**Breakdown:**

* `PROJECT_NAME: vprofile` — A plain pipeline variable. Value `vprofile` is directly set and visible to anyone reading the YAML.
* `JAVA_OPTS: ${JAVA_OPTIONS}` — A pipeline variable whose value comes from a **UI-defined variable** called `JAVA_OPTIONS`. This bridges the UI variable into the pipeline namespace under a name meaningful for Maven builds.

**Connection to flow:** These variables will be accessed in the `script:` blocks of jobs.

***

## Step 2: Add a Normal Variable in GitLab UI

Navigate to your GitLab project → **Settings** → **CI/CD**. You'll see sections for pipeline customization, Auto DevOps, Runners, Artifacts, and **Variables**. Click **Expand** on the Variables section. Scroll down and click **Add variable**.

**Configuration for the normal variable:**

| Field                | Value                       | Reasoning                                                        |
| -------------------- | --------------------------- | ---------------------------------------------------------------- |
| **Type**             | Variable (default)          | Standard key-value pair                                          |
| **Environment**      | All (default)               | Available in all environments                                    |
| **Visibility**       | Visible                     | Normal variable — no need to hide                                |
| **Protect variable** | ⚠️ **Uncheck**              | We want this accessible on all branches, not just protected ones |
| **Key**              | `JAVA_OPTIONS`              | The name used to reference this variable                         |
| **Value**            | `"-Xms512m -Xmx1024m"`      | Maven JVM memory settings: 512 MB minimum, 1024 MB maximum       |
| **Description**      | (optional descriptive text) | Helps identify purpose later                                     |

Click **Add variable**.

**Verification:** The variable appears in the list. Click **Edit** — you should be able to **see the value**, confirming it's a visible (non-secret) variable.

***

## Step 3: Add a Secret Variable (Masked and Hidden) in GitLab UI

Click **Add variable** again.

**Configuration for the secret variable:**

| Field                | Value                           | Reasoning                                       |
| -------------------- | ------------------------------- | ----------------------------------------------- |
| **Type**             | Variable                        | Standard key-value pair                         |
| **Visibility**       | **Masked and Hidden**           | This makes it a secret — invisible after saving |
| **Protect variable** | Checked (protected branch only) | Demonstrates the protection flag                |
| **Key**              | `MY_SECRET`                     | The name used to reference this variable        |
| **Value**            | `I am the ninja`                | Example secret value                            |
| **Description**      | (optional)                      |                                                 |

Click **Add variable**.

**Verification:** The variable appears in the list showing labels: **protected**, **masked**, **hidden**. Click **Edit** and scroll down — you will see that **you cannot see the value**. You can only delete or replace it. This confirms the masked+hidden behavior.

**Connection to flow:** This variable will be referenced in the pipeline to demonstrate log masking.

***

## Step 4: Add Echo Statements to Access All Variable Types

In the `build-job` section of your YAML, add echo statements to the `script:` block:

```yaml
build-job:
  stage: build
  image: maven:3.9.9-eclipse-temurin-17
  only:
    - main
  script:
    - echo "Building the project ${PROJECT_NAME}-test."
    - echo "Java Options are $JAVA_OPTS"
    - echo "My Secret is that $MY_SECRET"
    - echo "The source of the pipeline trigger is $CI_PIPELINE_SOURCE for branch $CI_COMMIT_BRANCH"
    - mvn install
```

**Breakdown of each echo:**

**Line 1:** `echo "Building the project ${PROJECT_NAME}-test."`

* `${PROJECT_NAME}` — References the pipeline variable, using curly braces for **concatenation** with `-test`. Result: `Building the project vprofile-test.`

**Line 2:** `echo "Java Options are $JAVA_OPTS"`

* `$JAVA_OPTS` — References the pipeline variable that resolves from `${JAVA_OPTIONS}` (UI variable). Shows the Maven memory settings in the log.

**Line 3:** `echo "My Secret is that $MY_SECRET"`

* `$MY_SECRET` — References the masked+hidden UI variable. The actual value will **not** appear in logs — it will show as `[MASKED]`.

**Line 4:** `echo "The source of the pipeline trigger is $CI_PIPELINE_SOURCE for branch $CI_COMMIT_BRANCH"`

* `$CI_PIPELINE_SOURCE` — Predefined variable: how the pipeline was triggered.
* `$CI_COMMIT_BRANCH` — Predefined variable: which branch triggered the pipeline.
* Note: This line uses `$` without curly braces. Both forms work — the instructor deliberately uses both to demonstrate equivalence.

***

## Step 5: Commit, Push, and Observe the Pipeline

Save the file in VSCode. Commit with a meaningful message:

```
learning variables
```

Push to the remote (commit and push).

Navigate to GitLab → **Build** → **Pipelines**. You should see a new pipeline running.

Click into the pipeline → click the **build-job** → click **Open full log** (or Full log viewer).

***

## Step 6: Verify Variable Output in Job Logs

**Expected log output and what to verify:**

| Echo Statement                           | Expected Output                               | What It Proves                                                                        |
| ---------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------- |
| Building the project...                  | `Building the project vprofile-test.`         | Pipeline variable works; `${}` concatenation works                                    |
| Java Options are...                      | Shows `-Xms512m -Xmx1024m` (the actual value) | UI variable → pipeline variable bridging works; visible variable shows in logs        |
| My Secret is that...                     | `My Secret is that [MASKED]`                  | Masked+hidden variable value is **not visible** in logs — replaced with `[MASKED]`    |
| The source of the pipeline trigger is... | `...is push for branch main`                  | Predefined variables correctly injected; pipeline was triggered by a `push` on `main` |

**Key observations:**

* The normal variable (`JAVA_OPTIONS`) shows its actual value in logs because it was saved as **Visible**.
* The secret variable (`MY_SECRET`) shows `[MASKED]` because it was saved as **Masked and Hidden**. The instructor's joke: *"Ninja is masked, right? Jokes apart, but that's what it means — it is not visible in the job logs if it's masked."*
* The predefined variables resolve to their runtime values automatically — no manual configuration needed.

**Common mistakes:**

| Mistake                                                     | Symptom                                         | Fix                                                                     |
| ----------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------- |
| Protected variable + non-protected branch                   | Variable is empty/undefined in pipeline         | Either uncheck "Protect variable" or run pipeline on a protected branch |
| Typo in variable name (`$MY_SECRE` instead of `$MY_SECRET`) | Empty output — no error, just blank             | Variable names are case-sensitive; double-check spelling                |
| Using `$PROJECT_NAME-test` without curly braces             | Shell may misinterpret where variable name ends | Use `${PROJECT_NAME}-test` for concatenation                            |
| Forgetting to expand Variables section in Settings          | Can't find where to add variables               | Settings → CI/CD → scroll to Variables → click **Expand**               |

***

## Step 7: Test Stage (Additional Verification)

The `test-job` also references `${PROJECT_NAME}`:

```yaml
test-job:
  stage: test
  image: maven:3.9.9-eclipse-temurin-17
  only:
    - main
  script:
    - echo "Running Unit Tests in the ${PROJECT_NAME}-test."
    - mvn test
    - mvn checkstyle:checkstyle
```

This confirms that top-level pipeline variables are accessible across **all jobs and stages** — not just the job where they were first used.

> ⚠️ **Expert Note:** In the next lecture, predefined variables like `CI_PIPELINE_SOURCE` and `CI_COMMIT_BRANCH` will be used for **conditional logic** — controlling which stages run based on how the pipeline was triggered or which branch it's running on. This lecture establishes the foundation; the next lecture applies it for real decision-making.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Variable Source Hierarchy

```
┌─────────────────────────────────────────────────────┐
│              GitLab CI/CD Pipeline Runtime           │
│                                                     │
│  ┌─────────────────────────────────────────┐        │
│  │  1. PIPELINE-DEFINED (YAML)             │        │
│  │     variables:                          │        │
│  │       PROJECT_NAME: vprofile            │        │
│  │       JAVA_OPTS: ${JAVA_OPTIONS} ──────────┐    │
│  └─────────────────────────────────────────┘  │    │
│                                                │    │
│  ┌─────────────────────────────────────────┐  │    │
│  │  2. UI-DEFINED (Settings → CI/CD)       │◄─┘    │
│  │     JAVA_OPTIONS = "-Xms512m -Xmx1024m" │       │
│  │       [visible, unprotected]            │        │
│  │     MY_SECRET = "I am the ninja"        │        │
│  │       [masked+hidden, protected]        │        │
│  └─────────────────────────────────────────┘        │
│                                                     │
│  ┌─────────────────────────────────────────┐        │
│  │  3. PREDEFINED (GitLab-injected)        │        │
│  │     CI_COMMIT_BRANCH    → main          │        │
│  │     CI_COMMIT_MESSAGE   → (commit msg)  │        │
│  │     CI_COMMIT_SHA       → (full SHA)    │        │
│  │     CI_PIPELINE_SOURCE  → push          │        │
│  └─────────────────────────────────────────┘        │
│                                                     │
│  ALL accessed via: $VAR or ${VAR}                   │
└─────────────────────────────────────────────────────┘
```

***

## Variable Access Syntax

```
$VARIABLE_NAME       → simple access
${VARIABLE_NAME}     → explicit delimited access
                        enables: concatenation, defaults, error handling

Example: ${PROJECT_NAME}-test  →  "vprofile-test"
```

***

## UI Variable Visibility Tiers

```
VISIBLE
  ├── Seen in: Settings UI ✅  Job Logs ✅
  └── Use for: non-sensitive config

MASKED
  ├── Seen in: Settings UI ✅  Job Logs ❌ → [MASKED]
  └── Use for: semi-sensitive values

MASKED + HIDDEN (SECRET)
  ├── Seen in: Settings UI ❌  Job Logs ❌ → [MASKED]
  ├── After save: can EDIT, can DELETE, CANNOT VIEW
  └── Use for: passwords, tokens, AWS keys, DB credentials
```

***

## UI Variable Protection Logic

```
Protect Variable = CHECKED
  ├── Protected branch (main)     → variable ACCESSIBLE ✅
  └── Non-protected branch (feat) → variable NOT ACCESSIBLE ❌
                                      (empty/undefined → pipeline may fail)

Protect Variable = UNCHECKED
  └── ALL branches → variable ACCESSIBLE ✅
```

***

## UI Variable Scoping

```
Environment scope:
  ALL (default)    → available in every environment
  production       → only in production pipelines
  staging          → only in staging pipelines
```

***

## Pipeline Variable ↔ UI Variable Bridging Pattern

```
GitLab UI:
  JAVA_OPTIONS = "-Xms512m -Xmx1024m"

Pipeline YAML:
  variables:
    JAVA_OPTS: ${JAVA_OPTIONS}

EFFECT:
  UI manages the VALUE (with visibility/protection controls)
  Pipeline defines the NAME (tool-meaningful: JAVA_OPTS for Maven)
  → Separation of value management from pipeline usage
```

***

## Predefined Variables — Key Four

```
CI_COMMIT_BRANCH     → branch name (e.g., "main")
                        USE: conditional stage execution by branch

CI_COMMIT_MESSAGE    → commit message text
                        USE: decision-making based on commit content

CI_COMMIT_SHA        → full commit hash
                        USE: artifact tagging/versioning (Docker images)

CI_PIPELINE_SOURCE   → trigger method ("push", "merge_request_event", "schedule")
                        USE: conditional behavior based on trigger type
```

***

## Job Log Output Verification

```
echo "${PROJECT_NAME}-test"     → "vprofile-test"         (pipeline var + concat)
echo "$JAVA_OPTS"               → "-Xms512m -Xmx1024m"   (UI visible var)
echo "$MY_SECRET"               → "[MASKED]"              (UI secret var)
echo "$CI_PIPELINE_SOURCE"      → "push"                  (predefined)
echo "$CI_COMMIT_BRANCH"        → "main"                  (predefined)
```

***

## Pipeline YAML Structure (This Lecture)

```yaml
stages: [build, test]

variables:
  PROJECT_NAME: vprofile          # plain inline
  JAVA_OPTS: ${JAVA_OPTIONS}      # bridges UI variable

build-job:                        # uses all 3 variable types
  stage: build
  image: maven:3.9.9-eclipse-temurin-17
  only: [main]
  script:
    - echo "${PROJECT_NAME}-test"           # pipeline var
    - echo "$JAVA_OPTS"                     # UI → pipeline var
    - echo "$MY_SECRET"                     # UI secret (masked)
    - echo "$CI_PIPELINE_SOURCE ... $CI_COMMIT_BRANCH"  # predefined
    - mvn install

test-job:                         # also accesses top-level vars
  stage: test
  image: maven:3.9.9-eclipse-temurin-17
  only: [main]
  script:
    - echo "${PROJECT_NAME}-test"
    - mvn test
    - mvn checkstyle:checkstyle
```

***

## Decision Map

| Decision                             | Choice                                      | Reason                                             |
| ------------------------------------ | ------------------------------------------- | -------------------------------------------------- |
| Where to store non-sensitive values  | Pipeline YAML `variables:`                  | Simple, visible, version-controlled                |
| Where to store sensitive values      | UI → Masked+Hidden                          | Cannot be viewed after creation; masked in logs    |
| Variable access syntax               | `${}` for concatenation, `$` for standalone | `${}` explicitly delimits variable name boundaries |
| Protection flag on secret            | Enabled                                     | Restricts to protected branches only               |
| Protection flag on normal var        | Disabled                                    | Needed on all branches                             |
| Predefined vars usage (this lecture) | Print only                                  | Conditions taught in next lecture                  |

***

## Reusable Engineering Pattern: Three-Tier Configuration Injection

```
PATTERN:
  Tier 1: CODE-LEVEL CONFIG      (pipeline YAML — visible, version-controlled)
  Tier 2: MANAGED CONFIG          (UI settings — visibility controls, scoping, protection)
  Tier 3: RUNTIME CONTEXT         (predefined — auto-injected, reflects execution state)

  All tiers merge into a single execution namespace
  All accessed with identical syntax ($VAR / ${VAR})

WHY:
  Different values have different sensitivity → different storage
  Different values have different lifecycle → different management
  Runtime context can't be pre-defined → auto-injection

WHERE ELSE:
  • Kubernetes: ConfigMaps (Tier 1) + Secrets (Tier 2) + Downward API (Tier 3)
  • Docker: ENV in Dockerfile + docker run --env + built-in vars
  • Jenkins: Jenkinsfile params + Credentials plugin + env vars
  • Any CI/CD system with config/secret/context separation
```

***

## Failure Signature Index

```
Variable value empty in logs         → typo in name OR protected var on non-protected branch
[MASKED] in logs                     → working correctly (variable is masked)
Concatenation produces wrong output  → used $VAR instead of ${VAR} before adjacent text
Can't see variable value in UI       → masked+hidden (by design — not a bug)
Variable works on main, fails on feature branch → protected variable flag enabled
UI variable not reaching pipeline    → key name mismatch between UI and YAML reference
```

***

## One-Line Mental Reload Trigger

> *"Three variable sources — YAML (plain), UI (visible/masked/hidden + protected + scoped), predefined (branch, SHA, source) — all accessed with $VAR or ${VAR}, secrets show \[MASKED] in logs, ${} enables concatenation."*

This single sentence reconstructs the entire variable system, all three sources, visibility tiers, access syntax, and the key behavioral difference between normal and secret variables. [\[196-variab...s-and-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/196-variables-and-more.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/196.Variables.yml)
