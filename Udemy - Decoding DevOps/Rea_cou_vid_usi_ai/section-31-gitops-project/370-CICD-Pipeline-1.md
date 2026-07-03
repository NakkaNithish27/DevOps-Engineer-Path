# 🎓 Deep Learning Material: GitHub Actions CI/CD Pipeline Part 1 — Build, Scan, Docker Push & Helm Update for GitOps

*Reconstructed from video lecture captions (370-cicd-pipeline-part-1.txt), prompt specification (370.CICDPrompt.txt), and pipeline structure (370.ci.yml)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What This Pipeline Does and Where It Fits in the GitOps Architecture

This lecture creates the **GitHub Actions CI/CD pipeline** for the `vprofile-app` repository — the application source code repository in the three-repository GitOps architecture established in previous lectures (`vprofile-app`, `vprofile-helm`, `vprofile-infra`). [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

The pipeline automates the entire path from code change to deployment readiness. The instructor frames it clearly: *"This is nothing new, except here we are going to at the end update the values.yaml file in a different repository."*  Everything before the Helm update (building, testing, scanning, Docker image creation) has been done before in previous CI/CD lectures. The new element is the **cross-repository update** — after building and pushing a Docker image, the pipeline automatically updates the Helm chart's `values.yaml` in the separate `vprofile-helm` repository with the new image tag. This is the bridge between CI (continuous integration) and CD (continuous deployment) in a GitOps model. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

***

## 1.2 The Pipeline's Branching Strategy and Event-Based Triggering

The pipeline implements a precise **branching strategy** where different pipeline stages run based on different Git events. The instructor explains the complete flow: [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt), [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt)

**Feature branch push → Nothing happens.** No pipeline runs when developers push to their feature branches. This prevents wasting CI resources on incomplete work.

**Pull Request to main → Quality checks only.** When a PR is raised against main, the pipeline runs: Maven build, unit tests, Checkstyle analysis, SonarQube scan, and SonarQube quality gate check. If the quality gate fails, the merge is blocked. This is the **gate** that ensures only quality-verified code reaches main.

**Merge/Push to main → Build and deploy artifacts.** When code is merged (which is a push event to main), the pipeline builds a Docker image, pushes it to Amazon ECR with two tags (commit SHA + `latest`), and then updates the Helm values file in the separate Helm repository.

This is implemented using GitHub Actions' `if` conditions on each job: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
```

The `build-and-sonar` job checks `if: github.event_name == 'pull_request'`. The `docker-build-push` and `update-helm` jobs check `if: github.event_name == 'push'`. Same trigger definition, different job-level conditions. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

🔍 **Deep Dive:**
The instructor explains why this separation matters: you don't want to build and push Docker images on every PR — that would create unnecessary images for code that hasn't been approved yet. The Docker build only happens after the code has passed quality checks AND been merged to main. The quality checks only run on PRs because merged code has already been validated. This prevents both waste (unnecessary Docker builds) and risk (deploying unchecked code).

***

## 1.3 The Three Jobs: Separation of Concerns

The pipeline has three jobs, each with a clear responsibility and execution condition: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml), [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt)

### Job 1: `build-and-sonar` (PR only)

**Condition:** `github.event_name == 'pull_request'`

Steps: Checkout source → Set up JDK 21 → Cache Maven and SonarQube dependencies → Build + unit tests + Checkstyle → SonarQube scan → Quality gate check.

The **caching** of Maven and SonarQube dependencies is explicitly included in the prompt and pipeline: *"Add Maven and SonarQube dependency caching to speed up PR builds."*  Without caching, every PR build would re-download all Maven dependencies from the internet, adding minutes to each run. Caching stores these between runs so subsequent builds are faster. [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt) [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

The **Maven command** the instructor cleans up to: `mvn verify checkstyle:checkstyle -B`. The `-B` flag is **batch mode** — the instructor explains: *"This option -B is batch mode. This prevents it from putting too much extra information like downloading this, downloading that."*  It suppresses interactive output and download progress bars, making CI logs cleaner. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

The **SonarQube** setup uses two specific GitHub Actions: [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt)

* `sonarsource/sonarqube-scan-action@v2` — Scans the source code and sends results to the SonarQube server
* `sonarsource/sonarqube-quality-gate-action@v1.1.0` — Polls the SonarQube server for the quality gate result

The instructor explains the self-hosted SonarQube choice: *"There is a reason we are not using SonarCloud — because there are too many restrictions on free account. We cannot operate it properly for our project test cases. So we are using EC2 instance."* [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

The quality gate has a **polling timeout** of 600 seconds — the action waits up to 10 minutes for SonarQube to process the scan and return the quality gate result. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

### Job 2: `docker-build-push` (Push to main only)

**Condition:** `github.event_name == 'push'`

Steps: Checkout source → Configure AWS credentials → (Optionally verify/create ECR repository) → Build Docker image → Tag with commit SHA and `latest` → Login to ECR → Push both tags → Output registry and tag information.

The Docker image is built from a specific Dockerfile: `Docker-files/app/multistage/Dockerfile` — a multi-stage Dockerfile that builds the application and creates a minimal runtime image. [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt)

**Dual tagging** is critical: each image gets both a **commit SHA tag** (unique, immutable identifier) and a **`latest` tag** (mutable pointer to the newest image). The commit SHA provides traceability — you can always map a running container back to the exact commit that produced it. The `latest` tag provides convenience for development environments. [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt)

This job produces **outputs** that are consumed by the next job: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

```yaml
outputs:
  ecr_registry: ${{ steps.set-outputs.outputs.ecr_registry }}
  ecr_image: ${{ steps.set-outputs.outputs.ecr_image }}
  image_tag: ${{ steps.set-outputs.outputs.image_tag }}
```

### Job 3: `update-helm` (Push to main, depends on Job 2)

**Condition:** `github.event_name == 'push'` AND `needs: docker-build-push`

Steps: Checkout → Install yq → Clone the Helm repository → Use yq to update `app.image` and `app.tag` in `values.yaml` → Git commit and push changes.

The `needs: docker-build-push` creates a **dependency chain** — this job only runs after Job 2 completes successfully. It consumes the outputs (ECR registry, image tag) from Job 2. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

The instructor explains **yq**: *"There's one way you can use sed Linux command — that is too complicated. yq is a YAML editor for search and replace."*  yq understands YAML structure, so it can reliably update specific fields (`app.image`, `app.tag`) without breaking the file format. Using `sed` for YAML manipulation is fragile because YAML is indentation-sensitive. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

The instructor identifies a **problem** with the AI-generated yq commands: the initial generation hardcodes the current image value in the search pattern, meaning it would only work once (when the current value matches). The instructor flags this: *"The app.image value could be anything, not just this one. Take care of this."*  The yq command needs to update the field regardless of its current value. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

⚠️ **Expert Note:**
The cross-repository update requires authentication to the Helm repository. This is handled via `GITOPS_PAT` (a GitHub Personal Access Token) and `HELM_REPO_USER` — stored as GitHub secrets. The pipeline clones the Helm repo using these credentials, makes changes, commits, and pushes. This is the GitOps bridge — the CI pipeline in one repo automatically updates the deployment definition in another repo.

***

## 1.4 Secrets vs. Variables: The Two Configuration Layers

The prompt and pipeline distinguish between **secrets** (sensitive, encrypted) and **variables** (non-sensitive, visible): [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt)

**Secrets (encrypted, hidden in logs):**

* `SONAR_TOKEN` — Authentication token for SonarQube server
* `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` — AWS credentials for ECR access
* `HELM_REPO_USER` — GitHub username for Helm repo access
* `GITOPS_PAT` — GitHub Personal Access Token for pushing to Helm repo
* `SLACK_WEBHOOK` — Slack notification endpoint

**Variables (visible, non-sensitive):**

* `AWS_REGION` — AWS region (e.g., us-east-1)
* `ECR_REPOSITORY` — ECR repository name (vprofileappimg)
* `SONAR_HOST_URL` — SonarQube server URL
* `HELM_REPO_NAME` — Helm repository name (vprofile-helm)

The pipeline references them differently: secrets use `${{ secrets.NAME }}`, variables use `${{ vars.NAME }}`. Variables are defined at the pipeline level as `env:` for convenience. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

***

## 1.5 The AI-Assisted Pipeline Development Workflow

The instructor uses GitHub Copilot to generate the pipeline from the detailed prompt, but emphasizes that the AI output requires **human review and correction**. He identifies several issues: [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

1. **Unnecessary role assumption** — Copilot added AWS role-based authentication that wasn't needed; the instructor removes it
2. **Redundant variable declarations** — Variables already defined in GitHub were re-declared inline
3. **Overly complex Maven command** — Simplified to `mvn verify checkstyle:checkstyle -B`
4. **ECR repository creation step** — Not needed (repository already exists), but left because it has an OR condition that skips creation if the repo exists
5. **Hardcoded yq values** — The search pattern was hardcoded to the current image value instead of being dynamic
6. **Missing Slack notification** — Noted for later addition

The instructor's meta-workflow: *"When I get started, I do one at a time. I come to a point where I like the pipeline. This is a working pipeline. Then I ask it to give me a prompt which I can use later to generate the same pipeline."* [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

He also sets expectations: *"Every time it will make one or the other mistake, which is fine, expected. It cannot literally get inside our brain and look at all the configuration."* [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

***

## 1.6 The Branch Discipline: Never Work on Main Directly

The instructor emphasizes a development practice: *"We have to do it the right way. We have to make all the changes in a different branch, not the main branch."* [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

He creates a feature branch (`feature-x`), makes all pipeline changes there, and will raise a PR to main in the next lecture. This mirrors real-world practice — main is protected, all changes go through PR review, and the pipeline itself validates changes before they reach main.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a **GitHub Actions CI/CD pipeline** (`ci.yml`) for the `vprofile-app` repository that: on PRs → runs quality checks (build, test, Checkstyle, SonarQube); on merge to main → builds a Docker image, pushes to ECR, and updates the Helm chart in a separate repository. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

***

## Phase 1: Set Up the Working Branch

### Step 1: Navigate to the App Repository

```bash
cd ~/Desktop/gitops/vprofile-app
```

 [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

Verify you're on the main branch.

### Step 2: Create and Switch to a Feature Branch

```bash
git branch -c feature-x
git checkout feature-x
```

 [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

**Breakdown:**

* `git branch -c feature-x` — Creates a new branch named `feature-x` (copied from current branch)
* `git checkout feature-x` — Switches to the new branch

**Why:** All changes are made on a feature branch, never directly on main. This is the branching practice the pipeline itself enforces. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

Open VS Code and verify you're on the `feature-x` branch (visible in the bottom-left status bar).

***

## Phase 2: Generate the Pipeline with AI

### Step 3: Prepare and Submit the Prompt

Open GitHub Copilot Chat in VS Code. Paste the detailed prompt (from the prompt reference file). [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

The prompt specifies:

* Java 21, Maven, WAR packaging
* PR → build + test + Checkstyle + SonarQube scan + quality gate
* Push to main → Docker build → ECR push (commit SHA + latest tags) → Helm values update
* Specific actions to use (sonarqube-scan-action\@v2, quality-gate-action\@v1.1.0)
* Dockerfile path: `Docker-files/app/multistage/Dockerfile`
* ECR repo: `vprofileappimg`, region: `us-east-1`
* Helm values path: `helm/vprofile/values.yaml`
* Values structure (app.image, app.tag)
* Update tool: yq
* All secrets and variables listed
* Job structure: 3 jobs with conditions

Copilot may ask questions (e.g., to check the SonarQube action from GitHub). Allow it to proceed. Wait for generation to complete. Click **Keep** to accept the generated file. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

***

## Phase 3: Review and Fix the Generated Pipeline

### Step 4: Verify the Trigger Configuration

Check the top of `ci.yml`: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

```yaml
name: CI/CD Pipeline
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
```

**Verify:** Both `pull_request` and `push` triggers target only `main`. Feature branch pushes should NOT trigger the pipeline.

### Step 5: Verify Environment Variables

```yaml
env:
  AWS_REGION: ${{ vars.AWS_REGION }}
  ECR_REPOSITORY: ${{ vars.ECR_REPOSITORY }}
  HELM_REPO_NAME: ${{ vars.HELM_REPO_NAME }}
  SONAR_HOST_URL: ${{ vars.SONAR_HOST_URL }}
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

**Note:** These reference GitHub repository **variables** (not secrets). The instructor notes that inline redeclaration of variables is unnecessary if they're already defined at the `env` level, but it doesn't cause harm. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

### Step 6: Review and Clean Job 1 — build-and-sonar

**Verify condition:** `if: github.event_name == 'pull_request'` [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

**Steps to verify:**

1. Checkout with `fetch-depth: 0` (full history needed for SonarQube)
2. JDK 21 setup
3. Maven cache step (speeds up builds)
4. SonarQube cache step (speeds up scans)

**Clean the Maven command** — remove unnecessary flags, keep it simple: [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

```bash
mvn verify checkstyle:checkstyle -B
```

* `verify` — Runs compilation, unit tests, and packaging
* `checkstyle:checkstyle` — Generates Checkstyle report
* `-B` — Batch mode (clean logs, no interactive prompts)

**Verify SonarQube steps:** [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

* Scan action: `sonarsource/sonarqube-scan-action@v2` with `SONAR_TOKEN` and `SONAR_HOST_URL`
* Quality gate action: `sonarsource/sonarqube-quality-gate-action@v1.1.0` with polling timeout of 600 seconds

### Step 7: Review Job 2 — docker-build-push

**Verify condition:** `if: github.event_name == 'push'` [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

**Verify outputs are defined:** [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

```yaml
outputs:
  ecr_registry: ${{ steps.set-outputs.outputs.ecr_registry }}
  ecr_image: ${{ steps.set-outputs.outputs.ecr_image }}
  image_tag: ${{ steps.set-outputs.outputs.image_tag }}
```

**Remove unnecessary steps:** [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

* Remove AWS role assumption if present (using access keys instead)
* The ECR repository creation step can stay — it has an OR condition that skips creation if the repo already exists

**Verify the build-and-push logic:** [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

1. Sets ECR registry variable and image tag (GitHub SHA)
2. `docker build` with Dockerfile at `Docker-files/app/multistage/Dockerfile`
3. Tags with both `$IMAGE_TAG` (commit SHA) and `latest`
4. `aws ecr get-login-password` → Docker login to ECR
5. Pushes both tags
6. Echoes the image information

### Step 8: Review and Fix Job 3 — update-helm

**Verify condition:** `if: github.event_name == 'push'` AND `needs: docker-build-push` [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.ci.yml)

**Verify steps:**

1. Checkout source
2. Install yq
3. Clone Helm repository (using `GITOPS_PAT` and `HELM_REPO_USER`)
4. Use yq to update `app.image` and `app.tag` in `values.yaml`
5. Git add, commit, push to Helm repo

**Fix the yq commands:** The AI may hardcode the current image value in the yq search pattern. The yq command must update the field **regardless of its current value** — use yq's direct field assignment, not search-and-replace. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

**Verify git operations:** [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

* `git config user.name` and `user.email` are set
* `git add .` stages changes
* `git commit` with a descriptive message
* `git push` to the Helm repository

### Step 9: Save the Pipeline File

Save `ci.yml` (should be at `.github/workflows/ci.yml`). [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

**Note:** Slack notification was missed in the initial generation. The instructor notes: *"Slack we have missed. Let's add it later."* [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

**Connection to flow:** The pipeline file is saved on the `feature-x` branch. In the next lecture, this branch will be committed, a PR raised to main, and the pipeline tested. [\[370-cicd-p...ine-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370-cicd-pipeline-part-1.txt)

***

## Pre-Pipeline Checklist (Before Running)

Before the pipeline can execute, these must be configured in the GitHub repository settings: [\[370.CICDPrompt \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/370.CICDPrompt.txt)

| Type     | Name                    | Value/Purpose                       |
| -------- | ----------------------- | ----------------------------------- |
| Secret   | `SONAR_TOKEN`           | SonarQube authentication            |
| Secret   | `AWS_ACCESS_KEY_ID`     | AWS ECR access                      |
| Secret   | `AWS_SECRET_ACCESS_KEY` | AWS ECR access                      |
| Secret   | `HELM_REPO_USER`        | GitHub username for Helm repo       |
| Secret   | `GITOPS_PAT`            | GitHub PAT for pushing to Helm repo |
| Secret   | `SLACK_WEBHOOK`         | Slack notification URL              |
| Variable | `AWS_REGION`            | e.g., `us-east-1`                   |
| Variable | `ECR_REPOSITORY`        | e.g., `vprofileappimg`              |
| Variable | `HELM_REPO_NAME`        | e.g., `vprofile-helm`               |
| Variable | `SONAR_HOST_URL`        | SonarQube server URL (EC2)          |

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Pipeline Identity

```
Pipeline: GitHub Actions CI/CD for vprofile-app
File: .github/workflows/ci.yml
Purpose: Quality gate → Docker build → Helm update (GitOps bridge)
```

***

## Event-to-Job Mapping

```
feature branch push → NOTHING (no trigger)

PR to main → build-and-sonar job ONLY
  Build → Test → Checkstyle → SonarQube scan → Quality gate
  Gate fails → merge blocked

Push/merge to main → docker-build-push → update-helm
  Build Docker image → push to ECR (SHA + latest tags)
  → Clone Helm repo → yq update values.yaml → git push
```

***

## Pipeline Architecture

```
on:
  pull_request → main
  push → main

┌─────────────────────────────────────────────────┐
│ JOB 1: build-and-sonar                          │
│ Condition: event == pull_request                 │
│                                                  │
│ Checkout → JDK 21 → Cache (Maven+Sonar)         │
│ → mvn verify checkstyle:checkstyle -B            │
│ → SonarQube scan → Quality gate check            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ JOB 2: docker-build-push                        │
│ Condition: event == push                         │
│ OUTPUTS: ecr_registry, ecr_image, image_tag      │
│                                                  │
│ Checkout → AWS credentials → Docker build        │
│ → Tag: commit-SHA + latest                       │
│ → ECR login → Push both tags                     │
└──────────────────────┬──────────────────────────┘
                       │ needs
┌──────────────────────▼──────────────────────────┐
│ JOB 3: update-helm                              │
│ Condition: event == push + needs docker-build    │
│                                                  │
│ Checkout → Install yq → Clone Helm repo          │
│ → yq update app.image + app.tag in values.yaml   │
│ → git add → git commit → git push (to Helm repo) │
└─────────────────────────────────────────────────┘
```

***

## Cross-Repository Update Flow

```
vprofile-app repo (CI pipeline runs here)
  │
  │ Job 2: Builds image → pushes to ECR
  │   Output: ecr_registry, image_tag (commit SHA)
  │
  │ Job 3: Clones vprofile-helm repo
  │   Uses: GITOPS_PAT + HELM_REPO_USER for auth
  │   Updates: helm/vprofile/values.yaml
  │     app.image: <ecr_registry>/<ecr_repo>
  │     app.tag: <commit_sha>
  │   Commits + pushes to vprofile-helm
  │
  ▼
vprofile-helm repo (updated automatically)
  → GitOps operator detects change → deploys to EKS
```

***

## Dual Image Tagging

```
Docker image pushed with TWO tags:
  1. Commit SHA (e.g., a1b2c3d)  → immutable, traceable to exact commit
  2. "latest"                     → mutable, always points to newest

ECR: <registry>/<repo>:<sha>
ECR: <registry>/<repo>:latest

Helm values updated with SHA tag (immutable reference)
```

***

## Secrets vs. Variables

```
SECRETS (encrypted, hidden in logs):
  SONAR_TOKEN          → SonarQube auth
  AWS_ACCESS_KEY_ID    → ECR access
  AWS_SECRET_ACCESS_KEY → ECR access
  HELM_REPO_USER       → GitHub username
  GITOPS_PAT           → GitHub token (push to Helm repo)
  SLACK_WEBHOOK        → notifications

VARIABLES (visible, non-sensitive):
  AWS_REGION           → us-east-1
  ECR_REPOSITORY       → vprofileappimg
  HELM_REPO_NAME       → vprofile-helm
  SONAR_HOST_URL       → SonarQube server URL

Reference: secrets.$NAME vs. vars.$NAME
```

***

## Key Tools and Actions

```
Maven:          mvn verify checkstyle:checkstyle -B
SonarQube scan: sonarsource/sonarqube-scan-action@v2
Quality gate:   sonarsource/sonarqube-quality-gate-action@v1.1.0
Docker:         docker build -f Docker-files/app/multistage/Dockerfile
ECR login:      aws ecr get-login-password | docker login
YAML update:    yq (NOT sed — yq understands YAML structure)
Checkout:       actions/checkout@v6
```

***

## yq Gotcha

```
AI-generated yq may HARDCODE current image value in search pattern
  → Works once, breaks on second run (value changed)
  
FIX: Use direct field assignment, not search-and-replace
  yq -i '.app.image = "NEW_VALUE"' values.yaml
  yq -i '.app.tag = "NEW_TAG"' values.yaml
  
"The app.image value could be anything, not just this one"
```

***

## AI Corrections Made

```
REMOVED: AWS role assumption (using access keys)
REMOVED: Redundant inline variable declarations
SIMPLIFIED: Maven command → mvn verify checkstyle:checkstyle -B
KEPT: ECR repo creation (has OR condition, harmless)
FLAGGED: yq hardcoded values (needs dynamic update)
NOTED: Slack notification missing (add later)
```

***

## Branch Discipline

```
"We have to do it the right way.
 We have to make all the changes in a different branch."

git branch -c feature-x → git checkout feature-x
  → Make pipeline changes on feature-x
  → Raise PR to main (triggers quality checks)
  → Merge (triggers Docker + Helm jobs)

Main branch = PROTECTED, all changes via PR
```

***

## AI Prompt-to-Pipeline Workflow

```
APPROACH:
  1. Start with detailed prompt (full specification)
  2. AI generates pipeline
  3. Human reviews → identifies errors → fixes
  4. Iterate until working
  5. Ask AI to generate reproducible prompt from working pipeline

EXPECTATION:
  "Every time it will make one or the other mistake,
   which is fine, expected."
  
  "Use the pipeline in the lecture resource
   to get a working CICD flow quickly."
```

***

## Job Dependency Chain

```
PR event:
  build-and-sonar (standalone) → pass/fail → allow/block merge

Push event:
  docker-build-push (standalone)
       │
       │ needs (waits for completion)
       ▼
  update-helm (consumes outputs from docker-build-push)
```

***

## Operational Flow

```
── SETUP ──
cd vprofile-app → git branch -c feature-x → git checkout feature-x
Open VS Code → verify feature-x branch

── GENERATE ──
Open Copilot Chat → paste detailed prompt → wait → Keep

── REVIEW + FIX ──
Check triggers: PR + push on main only
Clean Maven command: mvn verify checkstyle:checkstyle -B
Remove: role assumption, redundant vars
Fix: yq hardcoded values → dynamic field assignment
Note: Slack missing → add later

── VERIFY STRUCTURE ──
Job 1: build-and-sonar (if: pull_request)
Job 2: docker-build-push (if: push, outputs defined)
Job 3: update-helm (if: push, needs: docker-build-push)

── SAVE ──
.github/workflows/ci.yml → Ctrl+S

── NEXT LECTURE ──
Commit → push feature-x → raise PR → test pipeline
```

***

## Reusable Engineering Patterns

| Pattern                            | Manifestation                                                |
| ---------------------------------- | ------------------------------------------------------------ |
| **Event-conditional jobs**         | Same pipeline, different jobs execute based on PR vs. push   |
| **Quality gate as merge blocker**  | SonarQube pass/fail controls whether code can reach main     |
| **Cross-repository GitOps bridge** | CI in app repo → updates Helm repo → triggers CD             |
| **Job output passing**             | docker-build-push outputs → consumed by update-helm          |
| **Dependency chain (needs)**       | update-helm waits for docker-build-push completion           |
| **Dual tagging (SHA + latest)**    | Immutable traceability + mutable convenience                 |
| **Structured YAML editing (yq)**   | Use YAML-aware tools, not text manipulation (sed)            |
| **Dependency caching**             | Maven + SonarQube caches → faster PR builds                  |
| **Secrets/Variables separation**   | Sensitive in secrets (encrypted), non-sensitive in variables |
| **AI-generate → human-fix cycle**  | Detailed prompt → AI output → review → correct → iterate     |

***

## Core Mental Model

```
GitHub Actions CI/CD = Event-driven pipeline with conditional jobs

PR to main = QUALITY GATE
  Build → Test → Scan → Gate check
  Pass → allow merge | Fail → block merge

Push to main = ARTIFACT + DEPLOY BRIDGE
  Docker build → ECR push (SHA + latest)
  → Clone Helm repo → yq update values.yaml → git push

The pipeline CONNECTS two repos:
  vprofile-app (source) ──CI──→ ECR (artifact) ──bridge──→ vprofile-helm (deployment)

Job 3 (update-helm) is the GitOps bridge:
  It transforms a code change into a deployment definition change
  From this point, a GitOps operator can detect the Helm change
  and deploy automatically to the cluster

Three repos, one pipeline, zero manual deployment steps.
```

***

This material captures every concept, event-based triggering logic, job structure, cross-repository update mechanism, AI correction detail, and operational pattern from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
