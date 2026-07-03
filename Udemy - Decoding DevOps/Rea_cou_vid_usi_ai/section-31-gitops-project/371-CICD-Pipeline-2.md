# GitOps CI Pipeline Part 2 — Running the Pipeline, Pull Requests, and Helm Values Update

**Source:** Video caption file — *"CI/CD Pipeline Part 2"* (GitOps final project section) [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Pull Request Workflow: Why the Pipeline Doesn't Run on Every Commit

The most important architectural concept in this lecture is the **branch protection and pull request trigger model**. The CI pipeline is configured to run **only** when a pull request is raised against the `main` branch or when code is pushed to `main` — never when commits happen on feature branches. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

The video demonstrates this explicitly: after committing and pushing code to the `feature-x` branch, the instructor checks the Actions tab and confirms — "you should not see any pipeline that got triggered. As long as you don't push it to the main branch, nothing will happen." Commits to `feature-x` are invisible to the pipeline. Only when a **pull request** is created to merge `feature-x` into `main` does the pipeline trigger. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

This is a deliberate design rooted in a fundamental development principle: **"Main branch will always be protected."** Developers cannot directly push to `main`. They create feature branches, make changes, and then request permission to merge into `main` via a pull request (also called a merge request in GitLab). This ensures that every change to `main` goes through a review and quality gate process. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

The video notes that in real teams, different parties handle different stages: "Here we are raising the pull request, we are approving it and we are only merging it. But in real time, there will be different parties that will be doing this." A developer raises the PR, a reviewer approves it, and an authorized party merges it — separation of concerns enforced through the Git workflow. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## 1.2 — The Two-Phase Pipeline Trigger Model

The pipeline has two distinct trigger points that correspond to two different phases of the CI process: [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

### Phase 1: Pull Request Opened → Code Quality Check

When a pull request is raised (merging `feature-x` into `main`), the pipeline triggers and runs: code build, test, code analysis, and **SonarQube quality gates check**. This phase answers the question: "Is this code good enough to merge into main?" [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

The quality gate is a **blocking check** — "You cannot merge this to the main branch without this SonarQube quality gates checks out." If the quality gate fails, the merge is blocked. The developer must fix the code quality issues and push again. Only when the quality gate passes can the authorized party merge the pull request. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

### Phase 2: Merge to Main → Build Docker Image + Update Helm

When the pull request is **merged** (code actually enters the `main` branch), the pipeline triggers again with the full CI flow: build the Docker image, push it to Amazon ECR, and update the `values.yaml` file in the Helm repository with the new image tag. This phase executes the actual artifact creation and delivery handoff. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

This two-phase model creates a **quality checkpoint** before any code reaches `main`, and then a **delivery automation** once code passes that checkpoint. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## 1.3 — GitHub Variables: Storing Dynamic Configuration

The SonarQube server has a public IP that changes every time it's powered on. Hardcoding this IP in the pipeline code would require a code change every time the server restarts. Instead, the pipeline uses a **GitHub repository variable** — `SONAR_HOST_URL` — that stores the SonarQube server URL. The pipeline references it as `vars.SONAR_HOST_URL`. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

This is stored in: **Repository → Settings → Secrets and Variables → Actions → Variables**. It's a repository-level variable (not a secret — it's a URL, not a credential). When the SonarQube server gets a new IP, you update the variable in GitHub settings without touching the pipeline code. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

The video specifies the value format: `http://<public-ip>:80`. SonarQube's Nginx proxy listens on port 80 (the default HTTP port), so `:80` is technically optional but explicitly mentioned for clarity. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## 1.4 — SonarQube Quality Gates: The Merge Guard

SonarQube quality gates define **code quality thresholds** that must be met for the pipeline to pass. The video uses the **default quality gates** for simplicity. If the quality gate fails for any reason, the video advises: "You can create your own quality gates, attach it to your project, set it as per your requirement so it passes, because our idea is to complete this project." [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

The distinction between learning and production is important: "In real time, there will be definitely rule set and the quality gates, and if our code is not as per the quality gates, it fails and the developer needs to make the code changes and make sure the quality of the code is good." In production, quality gates enforce real standards; in learning, they're a checkpoint you configure to pass so you can complete the pipeline flow. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## 1.5 — The CI Pipeline's Final Actions: ECR Push + Helm Values Update

After the merge to `main`, the pipeline executes two critical final steps that connect CI to CD: [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**Step 1: Build and push Docker image to Amazon ECR.** The image is tagged with the **commit ID** (ensuring every build is uniquely identifiable) and also tagged as `latest`. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**Step 2: Update the `values.yaml` file in the Helm repository.** The pipeline makes a **Git commit** to the separate Helm repository (`vProfile-Helm`), updating the image tag in `values.yaml` to match the newly pushed image. This is the **GitOps handoff point** — the CI pipeline's last action is a Git commit, not a deployment. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

The video verifies both: checking ECR for the new image with the commit ID tag, and checking the Helm repository's `values.yaml` for the updated image tag. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

🔍 **Deep Dive:**
This is the concrete implementation of the CI-to-CD contract described in the GitOps introduction lecture. The CI pipeline writes to two destinations: Docker image → ECR (artifact storage), image tag → Helm repo (deployment specification). The CI pipeline never touches the Kubernetes cluster. Argo CD (set up in the next lecture) will read the Helm repo, detect the tag change, and deploy the new version. The Git commit in the Helm repo is the **triggering event** for the CD side of the pipeline. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## 1.6 — The Working Pipeline File

The video acknowledges that building the pipeline iteratively can introduce errors: "I'm not sure whether this is going to be working. Most of things are correct as per my knowledge, but things might go wrong." The instructor provides a **known-working pipeline** file in the lecture resources: "You'll have this pipeline in this lecture resource, the working pipeline, which you should use in your project." [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

The practical advice: download the working pipeline file, copy it into `ci.yml`, and follow along. This avoids debugging syntax issues and lets you focus on understanding the pipeline flow. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are executing the full CI pipeline flow: committing pipeline code to a feature branch, configuring the SonarQube variable, raising a pull request to trigger the quality check, merging to main to trigger the Docker build + ECR push + Helm values update. The final outcome: a Docker image in Amazon ECR tagged with the commit ID, and an updated `values.yaml` in the Helm repository — ready for Argo CD to deploy in the next lecture. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

### Step 1: Commit Pipeline Code to Feature Branch

**What we are doing:** Pushing the `ci.yml` pipeline file to the `feature-x` branch.

**Pre-requisite:** Ensure you're on the `feature-x` branch in the `vProfile-app` repository. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

```bash
git add .
```

Stages all changes (including the `ci.yml` file).

```bash
git commit -m "Pipeline"
```

Commits with a descriptive message.

```bash
git push origin feature-x
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**⚠️ Critical:** Push to `feature-x`, **not** `main`. "Be careful, feature-x. You need to commit this in the feature branch." Pushing directly to `main` would bypass the pull request workflow.

**Expected result:** Code is pushed. **No pipeline triggers** — the pipeline only runs on pull requests to `main` or pushes to `main`.

**Verification:** Go to **Actions** tab in the GitHub repository — no pipeline should appear. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

### Step 2: Power On SonarQube Server and Get Its IP

**What we are doing:** Starting the SonarQube server (which was powered off to save costs) and retrieving its public IP.

1. Power on the SonarQube server (from your cloud console — AWS EC2).
2. **Wait at least 5 minutes** — "if you just powered on SonarQube server, it's going to take some time, at least five minutes to bring up all its services." [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)
3. Get the **public IP** of the SonarQube server.
4. Verify it's working by accessing `http://<public-ip>:80` in a browser.

***

### Step 3: Set the SonarQube URL as a GitHub Variable

**What we are doing:** Storing the SonarQube server URL as a repository variable so the pipeline can reference it dynamically.

1. Go to your `vProfile-app` repository on GitHub.
2. Navigate to **Settings → Secrets and Variables → Actions → Variables**.
3. Click **New repository variable**.
4. **Variable name:** `SONAR_HOST_URL` (must match exactly what the pipeline references as `vars.SONAR_HOST_URL`). [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)
5. **Value:** `http://<public-ip-of-sonarqube>:80`
   * Must include `http://` — it's a URL, not just an IP.
   * Port 80 is the default HTTP port (optional to include, but explicit is clearer).
   * If SonarQube runs on a non-standard port, you must include that port number. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)
6. Click **Update variable** (or Create).

**Connection to flow:** The pipeline reads this variable during the SonarQube analysis stage to know where to send the code analysis results.

***

### Step 4: Raise a Pull Request (Triggers Quality Check)

**What we are doing:** Creating a pull request to merge `feature-x` into `main`, which triggers the first phase of the pipeline.

1. Go to the repository on GitHub.
2. Navigate to **Pull Requests → New Pull Request**.
3. Set the merge direction: `feature-x` → `main`. "Look at the arrow. This is the branch that will get merged." [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)
4. Click **Create Pull Request**.
5. Optionally add a title and description.
6. Click **Create Pull Request** to confirm. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**What happens immediately:** The pipeline triggers and runs: build → test → code analysis → SonarQube quality gates check. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**How to monitor:** Click on the pipeline run in the PR page, or go to **Actions** tab. The commit message and "pull request opened by..." information appears. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**Wait for completion.** The video's run completed in 1 minute 52 seconds. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**Verify SonarQube results:** Go to the SonarQube server UI → your project (`vProfile-app`) should appear with quality gate results. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**If quality gate fails:** Create your own quality gate in SonarQube, attach it to the project, and configure thresholds that your code meets. This is a learning-environment adjustment; in production, you'd fix the code instead. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

### Step 5: Merge the Pull Request (Triggers Full CI Pipeline)

**What we are doing:** Merging the approved code into `main`, which triggers the second phase — Docker build, ECR push, and Helm values update.

1. Go to the **Pull Request** page.
2. Verify the quality gate check passed (green checkmark). [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)
3. Click **Merge Pull Request**.
4. Click **Confirm Merge**. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**What happens immediately:** The pipeline triggers again, this time executing the full flow including Docker image build, push to Amazon ECR, and Helm values file update. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**This takes time.** The video pauses the recording and resumes after completion. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

### Step 6: Verify — Docker Image in Amazon ECR

**What we are doing:** Confirming the Docker image was pushed to the container registry.

1. Go to **Amazon ECR** in the AWS console.
2. Find the `vProfile-app` image repository.
3. Check for the new image tag — it should show the **commit ID** as the tag, plus a `latest` tag. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**Expected result:** An image with a tag matching the Git commit hash, confirming the exact source code that produced this image.

***

### Step 7: Verify — Helm Values File Updated

**What we are doing:** Confirming the CI pipeline updated the Helm repository with the new image tag.

1. Go to your GitHub repositories.
2. Open the **`vProfile-Helm`** repository.
3. Open the **`values.yaml`** file.
4. Check the `image` section — the `tag` value should match the commit ID from the ECR image. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**Expected result:** The `values.yaml` shows the updated image tag, confirming the CI pipeline made a commit to this repository. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

**Connection to flow:** This is the GitOps handoff. The CI pipeline is done. From the next lecture, EKS cluster and Argo CD are set up. Argo CD will watch this Helm repository and deploy the application based on the values in `values.yaml`. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

### Handling the README Detour

During the lecture, the instructor encountered a pull request issue and resolved it by generating a new `README.md` file (using GitHub Copilot) and committing it to `feature-x` to create a fresh pull request. The process followed the exact same pattern: [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

```bash
git add .
git commit -m "Generated README file"
git push origin feature-x
```

Then: new pull request → pipeline runs → quality check passes → merge → full pipeline triggers. [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

This detour reinforces the workflow: any commit to `feature-x` alone does nothing; only a pull request to `main` triggers the pipeline.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    GitOps CI Pipeline Part 2 — Execution
PURPOSE:  Run the complete CI pipeline: PR → quality check → merge → Docker + ECR + Helm update
CONTEXT:  After pipeline code written (Part 1); before EKS + Argo CD setup
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Two-Phase Pipeline Trigger Model

```
PHASE 1: Pull Request Opened → QUALITY CHECK
  ├── Trigger: PR raised (feature-x → main)
  ├── Runs: Build → Test → SonarQube Analysis → Quality Gates
  ├── Purpose: "Is this code good enough to merge?"
  └── Gate: Merge BLOCKED if quality gate fails

PHASE 2: Merge to Main → FULL CI + DELIVERY HANDOFF
  ├── Trigger: PR merged (code enters main)
  ├── Runs: Build Docker image → Push to ECR → Update Helm values.yaml
  ├── Purpose: Create artifact + trigger CD handoff
  └── Output: Image in ECR + updated tag in Helm repo

NOTHING TRIGGERS on commits to feature-x alone
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## End-to-End Flow (This Lecture)

```
1. git push origin feature-x         ← code in feature branch (NO trigger)
2. Set SONAR_HOST_URL variable        ← GitHub Settings → Variables
3. Power on SonarQube, wait 5 min     ← services need startup time
4. New Pull Request (feature-x → main) ← TRIGGERS Phase 1
5. Pipeline: build → test → SonarQube → quality gate
6. Quality gate passes ✅
7. Merge Pull Request                 ← TRIGGERS Phase 2
8. Pipeline: Docker build → ECR push → Helm values.yaml update
9. VERIFY: ECR has image with commit ID tag
10. VERIFY: Helm repo values.yaml has updated tag

CI COMPLETE → next: EKS + Argo CD (CD side)
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Branch Protection Model

```
main branch: PROTECTED
  ├── No direct pushes allowed
  ├── Changes only via pull request
  ├── Quality gate must pass before merge
  └── Authorized party merges

feature-x branch: OPEN
  ├── Developers commit freely
  ├── No pipeline triggers
  └── Changes enter main only via PR

"Main branch will always be protected"
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## GitHub Variable Configuration

```
LOCATION: Repository → Settings → Secrets and Variables → Actions → Variables

VARIABLE:        SONAR_HOST_URL
VALUE:           http://<sonarqube-public-ip>:80
REFERENCED AS:   vars.SONAR_HOST_URL (in ci.yml)

WHY VARIABLE:    SonarQube IP changes on restart
                 Update variable → pipeline uses new IP
                 No pipeline code change needed
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## CI Pipeline Final Output

```
ARTIFACT 1: Docker Image → Amazon ECR
  ├── Tag: commit ID (unique per build)
  ├── Tag: latest
  └── Repository: vProfile-app

ARTIFACT 2: Git Commit → Helm Repository
  ├── File: values.yaml
  ├── Change: image.tag = <commit-id>
  └── Repository: vProfile-Helm

CI NEVER touches K8s cluster
CI ONLY writes to: ECR (image) + Git (Helm values)
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## GitOps Handoff Point

```
CI PIPELINE (this lecture)          CD (next lecture)
──────────────────────              ────────────────
Build + Test + Quality Gate
Docker image → ECR
Helm values.yaml → Git commit ──→  Argo CD detects change
                                   Argo CD deploys to EKS
                                   Cluster matches Git state

BOUNDARY: Git commit in Helm repo = handoff event
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Pull Request Lifecycle

```
DEVELOPER:
  1. Create feature branch
  2. Make changes + commit
  3. Push to feature branch
  4. Raise Pull Request (feature → main)

PIPELINE:
  5. Triggers quality check (build, test, SonarQube)
  6. Reports pass/fail on PR page

AUTHORIZED PARTY:
  7. Reviews quality gate results
  8. Merges PR if quality passes
  
PIPELINE (again):
  9. Triggers full CI (Docker + ECR + Helm update)

"In real time, there will be different parties doing this"
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## SonarQube Quality Gate

```
PURPOSE:    Block merge if code quality is below threshold
DEFAULT:    Uses default quality gates (learning)
PRODUCTION: Custom quality gates with strict rules

IF FAILS (learning):
  → Create custom quality gate in SonarQube
  → Attach to project
  → Set thresholds your code meets

IF FAILS (production):
  → Developer fixes code quality issues
  → Pushes fix → new PR → re-check
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## SonarQube Server Timing

```
POWER ON → wait 5+ minutes → services start → verify in browser
URL: http://<public-ip>:80 (Nginx proxy → SonarQube)
Port 80 = default HTTP (optional to specify, but explicit is clearer)
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Verification Checklist

```
CHECK                            WHERE                    EXPECTED
─────                            ─────                    ────────
No trigger on feature push       GitHub Actions           No pipeline runs
PR triggers quality check        GitHub Actions           Pipeline runs (Phase 1)
SonarQube results                SonarQube UI             Project appears, gate passes
Merge triggers full CI           GitHub Actions           Pipeline runs (Phase 2)
Docker image in ECR              AWS ECR console          Image with commit ID tag + latest
Helm values updated              vProfile-Helm repo       values.yaml image.tag = commit ID
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Key Commands

```
COMMAND                              PURPOSE
───────                              ───────
git add .                            Stage all changes
git commit -m "Pipeline"             Commit with message
git push origin feature-x            Push to feature branch (NOT main)
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Working Pipeline File Note

```
⚠️ LECTURE RESOURCE contains a KNOWN-WORKING pipeline file
   → Download from lecture resource
   → Copy into ci.yml
   → Use this instead of building from scratch

"You'll have this pipeline in this lecture resource,
 the working pipeline, which you should use in your project"
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Image Tagging Strategy

```
TAG 1: Commit ID (Git SHA)
  → Unique per build
  → Traceable to exact source code
  → Used in Helm values.yaml for deployment

TAG 2: latest
  → Always points to most recent build
  → Convenience tag

HELM VALUES: Uses commit ID tag (not latest) for deterministic deployments
```

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## Reusable Engineering Patterns

| Pattern                              | Manifestation                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **Protected Main Branch**            | No direct pushes to main — all changes via pull request with quality gates                           |
| **Two-Phase Pipeline Trigger**       | PR opened → quality check; PR merged → artifact creation + delivery handoff                          |
| **Quality Gate as Merge Guard**      | SonarQube check must pass before merge is allowed — blocking checkpoint                              |
| **Git Commit as Deployment Trigger** | CI's final action is a Git commit to Helm repo — not a direct deployment                             |
| **Externalized Configuration**       | SonarQube URL stored as GitHub variable — changes without code modification                          |
| **Commit ID as Image Tag**           | Unique, traceable, deterministic — every image maps to exact source code                             |
| **Separation of Roles**              | Developer raises PR, pipeline checks quality, authorized party merges — no single actor controls all |
| **Known-Good Reference File**        | Working pipeline provided in resources — debug from known-good, not from scratch                     |

 [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

## One-Line System Reconstruction

> **The GitOps CI pipeline triggers in two phases — Phase 1 on pull request (build→test→SonarQube quality gate must pass before merge is allowed), Phase 2 on merge to protected main branch (build Docker image→push to ECR with commit-ID tag→update `values.yaml` in Helm Git repo with new tag) — where the CI pipeline never touches the cluster directly, the SonarQube URL is stored as a GitHub repository variable (`SONAR_HOST_URL`), and the final Git commit to the Helm repository is the GitOps handoff point for Argo CD (next lecture) to detect and deploy.** [\[371-cicd-p...ine-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/371-cicd-pipeline-part-2.txt)

***

This completes the full reconstruction of the CI/CD Pipeline Part 2 lecture. The CI pipeline is now fully operational — code is quality-checked, Docker images are built and stored in ECR, and the Helm repository is updated with the new image tag. The next lectures set up the EKS cluster, Argo CD, and the infrastructure Terraform pipeline to complete the full GitOps system. Let me know if you'd like any section expanded or adjusted! 🚀
