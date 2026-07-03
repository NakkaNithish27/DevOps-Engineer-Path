# 🎓 Security Scan — Trivy in GitHub Actions (Lecture 190)

**Video Title:** Security Scan
**Resource File:** [190. workflow-main-4.yaml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml?EntityRepresentationId=54d48d8b-3595-463b-8e5b-1c210a0ac06e) (Updated Workflow YAML)
**Context:** This lecture adds a **security scanning job** to the existing GitHub Actions workflow. The pipeline already has Build and Testing jobs from previous lectures. Now we introduce **Trivy**, an open-source vulnerability scanner by Aqua Security, to scan the source code for security vulnerabilities. This is the entry point into **DevSecOps** — integrating security checks directly into the CI/CD pipeline. The scan results are stored as downloadable artifacts. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

***

## 🧠 SECTION 1: THEORY — Deep Learning Mode

***

### 1. Security Scanning in CI/CD — The DevSecOps Layer

The instructor frames this job alongside existing pipeline activities: **"Like we conduct unit testing — `mvn test` — or code analysis like Checkstyle, like that, security scanning is also very much used in DevSecOps pipelines."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

This positions security scanning as a **parallel concern** to functional testing and code quality — not a replacement for either, but an additional dimension of validation. In a DevSecOps pipeline, every code change is automatically checked for known vulnerabilities before it can progress to deployment. The pipeline doesn't just ask "Does the code work?" and "Is the code clean?" — it also asks "Is the code safe?"

The instructor explains what happens when vulnerabilities are found: **"If there are any issues, it highlights the vulnerabilities, and then you can decide whether you want to promote that build or you want to stop it."** This reveals a key design decision in security scanning — the scan produces **information**, and the pipeline designer decides the **policy**: should a vulnerable build be blocked (fail the pipeline) or merely flagged (continue but report)?

***

### 2. Trivy by Aqua Security — What It Is

**"Aqua Security is a company that builds some open-source tools. One of them is Trivy."** The instructor finds it in the GitHub Marketplace by searching for "Aqua Security." [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

**Trivy** is an open-source vulnerability scanner that can scan multiple target types: source code filesystems, Docker container images, and other artifacts. In this lecture, it scans the **source code filesystem** — analyzing the project's dependency files (like `pom.xml` for Java) to identify known vulnerabilities in the libraries the project uses.

The instructor also mentions that Trivy's scope can be expanded: **"Later you can also expand it to the Docker image that we will be building later. And the artifacts also."** This tells us Trivy is not a one-trick tool — it's a versatile scanner that will reappear in later pipeline stages for different scan targets. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

The action's full reference name is `aqua-security/trivy-action@0.28.0`. The instructor notes: **"This is the version when I'm seeing it. So you can keep the same version, or you can give a different version. If you see a newer version later, you can use that also."** This is the standard versioning pattern for GitHub Actions — you pin to a specific version for reproducibility but can upgrade when needed. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### 3. Scan Configuration — The `with` Parameters

The Trivy action accepts several parameters through the `with` block. The instructor explains each one he uses: [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

**`scan-type: fs`** — Tells Trivy to perform a **filesystem scan** (`fs`). This means Trivy examines the source code files and their dependency manifests (e.g., `pom.xml`, `package.json`, `requirements.txt`) to find known vulnerabilities in declared dependencies. The alternative would be scanning a Docker image (which the instructor says will come later).

**`scan-ref: .`** — The **scan reference** — what to scan. The dot (`.`) means the **current working directory**, which, after `actions/checkout`, contains the entire cloned source code. The instructor explains: **"That means the current working directory that includes our source code, everything."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

**`format: json`** — The output format. The instructor chooses JSON and later explains the tradeoff: **"The JSON output is useful when you want to upload it somewhere on a dashboard. You want to do analysis on this. The more human-readable format is table... but mostly after generating the result, we do take some action based on the result. So that's why usually you should see the JSON format."** This reveals a practical engineering decision — JSON is for machine consumption and downstream processing; table is for human reading. In automated pipelines, JSON is the standard choice because results often feed into dashboards, alerting systems, or policy engines. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

**`exit-code: 0`** — This is the **most critical behavioral parameter**. The instructor explains: **"Exit code zero means continue with the next step. Do not fail it even if the vulnerabilities are found. But if you set it to one, then if vulnerabilities are found, this is going to fail your workflow."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

This maps to a fundamental CI/CD pattern: **informational scanning vs. gating scanning**. With `exit-code: 0`, the scan is informational — it reports vulnerabilities but the pipeline continues regardless. With `exit-code: 1`, the scan becomes a **gate** — any vulnerability fails the pipeline, blocking promotion of the build. The instructor sets it to `0` because: **"We're going to keep it zero because there are vulnerabilities. And we'll talk about what happens when there are vulnerabilities later."** This implies the project has known vulnerabilities, and failing the pipeline right now would block all progress. In a mature pipeline, you'd eventually set this to `1` to enforce security standards. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

**Vulnerability types:** The instructor mentions: **"Vulnerability types that you want to scan — like these two are the most famous one: OS and library, but there are a few other options."** OS vulnerabilities are in the operating system packages of a container image. Library vulnerabilities are in the application's third-party dependencies. For a filesystem scan of source code, library vulnerabilities are the primary concern. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

> 🔍 **Deep Dive (Optional):**
> The `exit-code` parameter leverages a universal Unix convention: a process exit code of `0` means success, and any non-zero value means failure. GitHub Actions interprets step exit codes to determine if a step succeeded or failed. By setting Trivy's exit code to `0` even when vulnerabilities are found, we're telling GitHub Actions "this step succeeded" regardless of scan results. Setting it to `1` when vulnerabilities exist makes GitHub Actions see the step as "failed," which stops the job (and potentially the entire workflow if downstream jobs depend on it).

***

### 4. Storing Scan Results as Artifacts — Why and How

The instructor identifies the problem: **"Once the workflow completes, the output will be also gone. So you want to store the output as the artifact."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

This is the **ephemeral runner** problem encountered in Lecture 186 — runners are destroyed after the workflow finishes, taking all generated files with them. Any output you want to keep (build artifacts, test reports, scan results) must be explicitly **uploaded** before the runner disappears.

The mechanism is the same `actions/upload-artifact` action used previously for the build artifact (`.war` file). The instructor reuses the same pattern: give the artifact a name, specify the file path to upload. The Trivy scan produces a JSON file, and this file is uploaded as an artifact named `trivy-scan-results`. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

After the workflow completes, artifacts are downloadable from the workflow run page in the Actions tab. The instructor demonstrates: **"If you scroll down over here, you can see here the vprofile app folder — we downloaded that, it downloads a zip file that will contain the artifact — and then we have the scan result."** Both artifacts appear as separate downloadable zip files. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### 5. Parallel Execution Topology — The Fan-Out Pattern

With three jobs in the workflow, the execution topology becomes more interesting. The instructor explains: **"Now if you see, you have Build, and after that these two jobs are going to run at the same time. Security scan and Testing."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

Both `Testing` and `Security_Scan` have `needs: Build`. This creates a **fan-out** pattern:

    Build → Testing      (parallel)
    Build → Security_Scan (parallel)

The instructor then explains how to create a **sequential chain** instead: **"If you want to run security scan after testing, then we need to give security scan `needs` as `testing`... First build job will run, then testing because that needs build, and then it is going to run security scan."** But he decides: **"We can run both the jobs parallelly. There's no problem. So let's keep it as it is."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

This reveals an important design principle: use parallel execution when jobs are **independent** (testing and security scanning don't depend on each other's results) and sequential execution only when there's a **data or logic dependency** between jobs.

> 🔍 **Deep Dive (Optional):**
> The `needs` keyword accepts both a single job name (string) and a list of job names (array). If `Security_Scan` needed both `Build` AND `Testing` to complete before starting, you'd write `needs: [Build, Testing]`. This enables complex DAG (Directed Acyclic Graph) topologies where jobs can fan out and fan in. The current topology is a simple fan-out from Build.

***

### 6. Workflow Evolution — Accumulated Triggers and Permissions

The resource file ([190. workflow-main-4.yaml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml?EntityRepresentationId=54d48d8b-3595-463b-8e5b-1c210a0ac06e)) shows the workflow has evolved significantly since Lecture 186. It now includes four triggers and a permissions block: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml)

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:
  schedule:
    - cron: "10 14 * * 1-5"
permissions:
  contents: read
```

The **schedule trigger** uses a cron expression: `"10 14 * * 1-5"` — meaning the workflow runs at 2:10 PM UTC, Monday through Friday. The **workflow\_dispatch** enables manual triggering from the GitHub UI. The **pull\_request** trigger fires when PRs target the `main` branch. The **permissions** block restricts the workflow to read-only access to repository contents — a security hardening measure. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml)

The checkout steps now also include `fetch-depth: 0`, which clones the **full Git history** instead of a shallow clone (the default). This is typically needed for tools that analyze Git history (like some code analysis or versioning tools). [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml)

These elements were likely added in lectures 187–189 (between the quickstart and this lecture). This caption focuses specifically on the **Security\_Scan job addition**.

***

***

## ⚙️ SECTION 2: PRACTICAL — Guided Execution Mode

***

### What We Are Building

We are adding a **third job** (`Security_Scan`) to the existing workflow. This job clones the source code, runs Trivy to scan for vulnerabilities, and uploads the scan results as a downloadable artifact. After this change, the workflow has three jobs: Build runs first, then Testing and Security\_Scan run in parallel.

**Final outcome:** A workflow run showing three jobs — Build (sequential first), then Testing and Security\_Scan (parallel) — with a downloadable JSON artifact containing the vulnerability scan results. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Step 1: Open VSCode and Verify Branch

Open VSCode with the repository. The instructor says: **"Make sure you are in the main branch, no other branch."** Verify in the bottom-left corner of VSCode that the active branch is `main`. All workflow changes should be committed to the branch that the trigger monitors. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Step 2: Add the Security\_Scan Job

In `main.yml`, at the **same indentation column** as `Build:` and `Testing:` (under `jobs:`), add a new job. The instructor starts by copying the Testing job's structure as a base: [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

```yaml
  Security_Scan:
    runs-on: ubuntu-latest
    needs: Build
    steps:
      - name: Code checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
```

**`Security_Scan:`** — The job name. Uses underscore (YAML-safe naming). Placed at the same column level as `Build:` and `Testing:`.

**`needs: Build`** — This job waits for Build to complete, just like Testing does. Since both Testing and Security\_Scan need Build (and neither needs the other), they will execute **in parallel** after Build finishes.

**`actions/checkout@v4` with `fetch-depth: 0`** — Clones the full source code into the fresh runner. Required because this is a separate runner with no shared state (as established in Lecture 186). [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml)

***

### Step 3: Add the Trivy Scan Step

After the checkout step, add the security scanning step: [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

```yaml
      - name: Run Trivy vulnerability scanner
        uses: aqua-security/trivy-action@0.28.0
        with:
          scan-type: fs
          scan-ref: .
          format: json
          exit-code: 0
          output: trivy-results.json
```

Breaking down every parameter:

| Parameter   | Value                               | Meaning                                                                         |
| ----------- | ----------------------------------- | ------------------------------------------------------------------------------- |
| `uses`      | `aqua-security/trivy-action@0.28.0` | The Trivy action from GitHub Marketplace, pinned to version 0.28.0              |
| `scan-type` | `fs`                                | Filesystem scan — analyzes source code and dependency files, not a Docker image |
| `scan-ref`  | `.`                                 | Scan the current working directory (the cloned repo root)                       |
| `format`    | `json`                              | Output in JSON format (machine-readable, suitable for dashboards/automation)    |
| `exit-code` | `0`                                 | Always succeed, even if vulnerabilities are found (informational mode)          |
| `output`    | `trivy-results.json`                | Write scan results to this file                                                 |

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

**Why `exit-code: 0`?** The project has known vulnerabilities. Setting this to `1` would fail the workflow immediately, blocking all pipeline progress. The instructor keeps it at `0` for now and notes this decision will be revisited later. In a production pipeline, you'd eventually set this to `1` to enforce security gates.

***

### Step 4: Add the Artifact Upload Step

After the scan step, add the artifact upload step. The instructor copies this from the existing build artifact upload pattern: [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

```yaml
      - name: Upload Trivy scan results as artifact
        uses: actions/upload-artifact@v4
        with:
          name: trivy-scan-results
          path: trivy-results.json
```

| Parameter | Value                | Meaning                                                                     |
| --------- | -------------------- | --------------------------------------------------------------------------- |
| `name`    | `trivy-scan-results` | The display name of the artifact in the GitHub UI                           |
| `path`    | `trivy-results.json` | The file path to upload — must match the `output` value from the Trivy step |

**Connection:** The Trivy step writes results to `trivy-results.json`. This step takes that file and uploads it to GitHub's artifact storage. After the workflow finishes (and the runner is destroyed), the artifact remains downloadable from the Actions tab. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Step 5: Save, Commit, and Push

Save the file (`Ctrl+S`). Go to VSCode's Source Control panel, commit with a descriptive message (e.g., `security scanning`), and push to the `main` branch. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

Because the workflow triggers on `push` to `main`, this commit immediately starts a new workflow run.

***

### Step 6: Observe the Parallel Execution

Go to the repository's **Actions** tab. Click on the new workflow run. You will see three jobs: [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

1.  **Build** — starts first (no dependencies).
2.  **Testing** and **Security\_Scan** — start simultaneously after Build completes.

The instructor confirms: **"Now if you see, you have Build, and after that these two jobs are going to run at the same time."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

If you wanted **sequential** execution (Build → Testing → Security\_Scan), you would change the Security\_Scan job's `needs` to `Testing` instead of `Build`. But the instructor decides parallel is fine since the two jobs are independent.

***

### Step 7: Download and Inspect the Scan Results

After the workflow completes, scroll down on the workflow run page. You will see **two artifacts** listed: [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

1.  **vprofile-app** — the build artifact (`.war` file from the Build job)
2.  **trivy-scan-results** — the security scan output

Click to download `trivy-scan-results`. It downloads as a **ZIP file**. Extract it to find the JSON file. Open it in VSCode or any text editor. [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

The JSON contains structured vulnerability data — CVE identifiers, severity levels, affected packages, and versions. The instructor notes that while JSON is less human-readable than a table format, it's the standard choice for automated pipelines: **"Mostly after generating the result, we do take some action based on the result. So that's why usually you should see the JSON format."** [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

**Alternative format:** If you change `format: json` to `format: table`, the output becomes a human-readable text table — easier to read visually but harder to parse programmatically.

> ⚠️ **Expert Note (Optional):**
> In production pipelines, the JSON scan results would typically be sent to a security dashboard (like DefectDojo, Snyk, or a custom solution) via an API call in a subsequent step. This enables centralized vulnerability tracking, trend analysis, and policy enforcement across all repositories and builds — not just manual inspection of downloaded files.

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### Job Topology After This Lecture

            ┌─── Testing ──────────┐
    Build ──┤                       ├──→ (workflow complete)
            └─── Security_Scan ────┘

    Build:         sequential first (no needs)
    Testing:       needs: Build     ── parallel with Security_Scan
    Security_Scan: needs: Build     ── parallel with Testing

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml)

***

### Trivy Action — Configuration Map

    aqua-security/trivy-action@0.28.0
      ├── scan-type: fs          ← filesystem (source code + deps)
      │   └── alternatives: image (Docker), repo, config...
      ├── scan-ref: .            ← current directory (cloned repo root)
      ├── format: json           ← machine-readable (dashboard/automation)
      │   └── alternative: table (human-readable)
      ├── exit-code: 0           ← ALWAYS PASS (informational)
      │   └── alternative: 1     ← FAIL if vulnerabilities found (gate)
      ├── output: trivy-results.json  ← file written to runner filesystem
      └── vulnerability types: OS, library (most common)

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Exit Code as Policy Switch

    exit-code: 0  →  INFORMATIONAL mode
      └── Vulnerabilities found? → Report but CONTINUE pipeline
      └── Use when: learning, legacy code, early adoption

    exit-code: 1  →  GATING mode
      └── Vulnerabilities found? → FAIL the step → FAIL the job → block pipeline
      └── Use when: mature pipeline, security compliance required

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Scan → Store Pattern (Two-Step)

    Step 1: SCAN    → produces file on runner filesystem (trivy-results.json)
    Step 2: UPLOAD  → actions/upload-artifact → persists file beyond runner lifetime

    CRITICAL: Runner is ephemeral → any file not uploaded is LOST
      └── Trivy output file lives only during workflow execution
      └── upload-artifact preserves it as downloadable artifact in GitHub UI

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Output Format Decision

    json   → for machines (dashboards, APIs, policy engines, downstream automation)
    table  → for humans (quick visual inspection, debugging)

    Pipeline default: json (because results feed automation, not just eyes)

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### `needs` Topology Control

    PARALLEL (current):
      Testing:       needs: Build
      Security_Scan: needs: Build
      → Both start simultaneously after Build

    SEQUENTIAL (alternative):
      Testing:       needs: Build
      Security_Scan: needs: Testing
      → Build → Testing → Security_Scan (chain)

    RULE: Use parallel when jobs are independent
          Use sequential when there's a data/logic dependency

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Full Workflow State (Lecture 190)

    TRIGGERS:
      push → main
      pull_request → main
      workflow_dispatch (manual)
      schedule: cron "10 14 * * 1-5" (2:10 PM UTC, Mon-Fri)

    PERMISSIONS: contents: read

    JOBS:
      Build [ubuntu-latest]
        ├── checkout@v5 (fetch-depth: 0)
        └── (build steps from previous lectures)

      Testing [ubuntu-latest] ← needs: Build
        ├── checkout@v4 (fetch-depth: 0)
        └── (test steps from previous lectures)

      Security_Scan [ubuntu-latest] ← needs: Build  ← NEW
        ├── checkout@v4 (fetch-depth: 0)
        ├── aqua-security/trivy-action@0.28.0
        │     scan-type: fs, scan-ref: ., format: json, exit-code: 0
        └── upload-artifact: trivy-scan-results

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190.%20workflow-main-4.yaml), [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Reusable Pattern: Scan → Report → Decide

    PATTERN: Security/Quality Gate Integration

      1. SCAN   — run automated analysis tool (Trivy, SonarQube, Checkstyle...)
      2. STORE  — persist results as artifact / upload to dashboard
      3. DECIDE — exit-code controls pipeline behavior:
                   0 = informational (continue)
                   1 = gating (block on failure)

    Applies to:
      - Security scanning (Trivy)
      - Code quality (SonarQube quality gate)
      - Compliance checks
      - License scanning
      - Dependency auditing

    The tool produces DATA. The exit-code enforces POLICY.
    Separate concerns: detection ≠ enforcement.

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### Artifact Download Location

    GitHub UI → Actions tab → Workflow run → scroll to bottom → Artifacts section
      ├── vprofile-app (build artifact)
      └── trivy-scan-results (scan output)
    Both download as .zip files

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

### What's Next (Foreshadowed)

    Next lecture: Build Docker image from source code → upload to Amazon ECR
    Trivy scope expansion: scan Docker images + artifacts (not just filesystem)

 [\[190-security-scan \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/190-security-scan.txt)

***

Would you like me to save this as a downloadable markdown file?
