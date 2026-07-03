# 🎓 Deep Learning Material: CI/CD Pipeline Setup — GitHub Actions, SonarQube, ECR, Helm GitOps, and Branch Protection for a Complete Continuous Integration Flow

**Source:** Video lecture on CI pipeline overview (from [366-ci-pipeline-overview.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt?EntityRepresentationId=e58f072d-7136-44d0-ad95-df18d07db6e3) caption file) with detailed setup reference from [366.CICDPipelineSetup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt?EntityRepresentationId=6334adb4-4a81-4700-bafd-1ca1950e3de4) [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

**Video Context:** This lecture lays out the **complete CI/CD pipeline architecture** for the vProfile Java application, connecting multiple systems into one automated flow. The pipeline uses **GitHub Actions** as the CI engine, **SonarQube** (self-hosted on EC2) for code quality scanning, **Amazon ECR** for Docker image storage, a **separate Helm repository** for GitOps-based deployment manifests, and **Slack** for notifications. The lecture explains the full setup — from initializing the app repo to configuring secrets, creating the pipeline YAML, enforcing branch protection with quality gates, and establishing a feature-branch workflow. This is the integration lecture where code quality, containerization, and deployment automation all converge into one automated pipeline triggered by git operations.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Two-Repository Architecture: App Code and Helm Charts

The pipeline spans **two separate Git repositories**: [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt)

**Repository 1: `vprofile-java-app`** — Contains the application source code (`src/`), Maven build configuration (`pom.xml`), Dockerfiles (`Docker-files/`), the SonarQube properties file (`sonar-project.properties`), and the GitHub Actions pipeline definition (`.github/workflows/ci.yml`). This is where developers push code changes.

**Repository 2: `vprofile-helm`** — Contains the Helm charts created in the previous lecture, including `values.yaml` which specifies the Docker image name and tag. This is the **GitOps deployment source** — ArgoCD (set up later) watches this repository and deploys whatever image version is specified in `values.yaml`.

The CI pipeline's **final action** is to update the image name and tag in the Helm repository's `values.yaml`. This is the bridge between CI (build and test) and CD (deploy). The instructor explains: *"The end of this pipeline will be updating the latest image name and tag in the helm charts that we have created in the previous lecture."* [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt)

> 🔍 **Deep Dive**
>
> This two-repository separation is a core **GitOps pattern**. Application code and deployment configuration live in different repos because they have different lifecycles, different access controls, and different audiences. Developers push to the app repo; the CI pipeline pushes to the Helm repo; ArgoCD deploys from the Helm repo. No human directly modifies deployment configuration — the pipeline is the only writer. This ensures traceability: every deployment is traceable to a specific commit in the app repo through the image tag (commit SHA). [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## 1.2 — Pipeline Flow: Three Jobs, Two Triggers

The pipeline has **three distinct jobs** triggered by **two different git events**: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

### Trigger 1: Pull Request to `main`

When a developer opens a PR targeting the `main` branch, **only the first job runs**:

**Job 1: `build-and-sonar`** — Runs Maven build, unit tests, Checkstyle (code style checking), SonarQube code scan, and SonarQube quality gate check. If the quality gate fails (code quality doesn't meet the threshold), the PR is **blocked from merging** by branch protection rules. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

### Trigger 2: Push to `main` (merge)

When the PR is approved and merged into `main`, **jobs 2 and 3 run**:

**Job 2: `docker-build-push`** — Builds the Docker image using the multi-stage Dockerfile, tags it with the **commit SHA** and `latest`, and pushes it to **Amazon ECR**. It outputs the image tag and ECR registry URL for the next job. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

**Job 3: `update-helm`** — Clones the Helm repository, updates `values.yaml` with the new image URI and SHA tag using `yq`, commits and pushes the change. This triggers ArgoCD to deploy the new version. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

The instructor emphasizes the separation: *"feature branch push → no pipeline runs"* — pushing to a feature branch does nothing. The pipeline only activates on PRs (for quality checks) and on merges to main (for build and deploy). [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## 1.3 — SonarQube: Code Quality Scanning

**SonarQube** is a self-hosted code quality and security scanning platform. It analyzes source code for bugs, vulnerabilities, code smells, and test coverage. In this pipeline, it runs during PR checks to ensure code quality **before** merging. [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt)

SonarQube runs on an **AWS EC2 instance** (Ubuntu 22.04, t3.medium minimum — SonarQube needs 2GB RAM). It's set up using a userdata script that automates installation. After setup, you access the web UI on port 80, generate an authentication token, and store it as a GitHub secret (`SONAR_TOKEN`). [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

The `sonar-project.properties` file in the app repo configures what SonarQube scans: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

```properties
sonar.projectKey=vprofile-java99
sonar.projectName=vprofile-java99
sonar.projectVersion=1.0
sonar.sources=src/
sonar.java.binaries=target/classes
sonar.junit.reportsPath=target/surefire-reports/
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.java.checkstyle.reportPaths=target/checkstyle-result.xml
```

This tells SonarQube: the project name, where the source code is, where compiled classes are (for deeper analysis), where test reports are, where coverage reports are, and where Checkstyle reports are. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

The **quality gate** is a pass/fail threshold on SonarQube. If the code doesn't meet the defined quality standards (coverage, bug count, etc.), the quality gate fails, and the PR check fails, blocking the merge. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## 1.4 — Amazon ECR: Private Docker Image Registry

**Amazon ECR (Elastic Container Registry)** is AWS's managed Docker image registry. The pipeline builds the Docker image and pushes it to a **private** ECR repository named `vproappimg`. The image is tagged with two tags: the **commit SHA** (for precise version identification) and `latest` (for convenience). [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

ECR URI format: `<account-id>.dkr.ecr.<region>.amazonaws.com/vproappimg` [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

For the pipeline to push images to ECR, it needs AWS credentials. An **IAM user** (`github-actions-user`) is created with `AmazonEC2ContainerRegistryFullAccess` policy, and its access key and secret key are stored as GitHub secrets. [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## 1.5 — GitHub Secrets and Variables: Secure Configuration for Pipelines

The pipeline needs to authenticate with multiple external systems. **GitHub Secrets** store sensitive credentials that are encrypted and never visible in logs: [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

| Secret                  | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| `SONAR_TOKEN`           | Authenticate with SonarQube server                |
| `AWS_ACCESS_KEY_ID`     | IAM user for ECR push                             |
| `AWS_SECRET_ACCESS_KEY` | IAM user for ECR push                             |
| `HELM_REPO_USER`        | GitHub username for Helm repo access              |
| `GITOPS_PAT`            | GitHub Personal Access Token for cross-repo write |
| `SLACK_WEBHOOK`         | Slack notification endpoint                       |

**GitHub Variables** store non-sensitive configuration: [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

| Variable         | Value           |
| ---------------- | --------------- |
| `AWS_REGION`     | `us-east-1`     |
| `ECR_REPOSITORY` | `vproappimg`    |
| `HELM_REPO_NAME` | `vprofile-helm` |

The instructor distinguishes: *"These are the secrets which nobody can see. These are variables."* [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt)

***

## 1.6 — Cross-Repository Authentication: GitHub PAT

The pipeline running in the app repo needs to **push commits** to the Helm repo (to update `values.yaml`). This requires cross-repository write access. A **GitHub Personal Access Token (PAT)** is created with **fine-grained permissions**: scoped to only the `vprofile-helm` repository, with `Contents: Read and write` permission. This token is stored as `GITOPS_PAT`. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## 1.7 — Branch Protection: Enforcing Quality Gates

The branch protection rule on `main` ensures no code reaches production without passing quality checks: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

* **Require a pull request before merging** — no direct pushes to main
* **Require status checks to pass** — the `build-and-sonar` job must succeed before merge is allowed
* **Block force pushes** — prevents bypassing the protection

This creates an **automated quality gate**: developer pushes feature branch → opens PR → pipeline runs tests and SonarQube scan → if quality gate passes, merge is allowed → merge triggers build and deploy. If quality gate fails, the merge button is blocked. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## 1.8 — Slack Notifications

A **Slack app** with an incoming webhook is set up to notify a channel (e.g., `#deployments`) about pipeline events. The webhook URL is stored as `SLACK_WEBHOOK` in GitHub secrets. [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## 1.9 — The Feature Branch Workflow

The enforced development workflow: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

1. **Create a feature branch:** `git checkout -b feature-your-name`
2. **Make changes and push:** `git push -u origin feature-your-name` — no pipeline runs
3. **Open a PR targeting main** — pipeline runs `build-and-sonar`
4. **Quality gate passes** — merge is allowed
5. **Merge the PR** — pipeline runs `docker-build-push` → `update-helm`
6. **ArgoCD detects change in Helm repo** → deploys the new image

*"Always work on a feature branch, never directly on main."* [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are setting up the **complete CI pipeline infrastructure** — SonarQube server, ECR repository, IAM credentials, Slack webhook, GitHub secrets/variables, branch protection, and the pipeline YAML — so that every code change automatically goes through quality scanning, Docker image building, ECR publishing, and Helm chart updating. The final outcome: a fully automated pipeline where pushing code to a feature branch and merging a PR triggers the entire build-test-containerize-deploy flow without any manual intervention.

***

## Step 1: Initialize the App Repository

Copy these files into the root of your `vprofile-java-app` GitHub repo: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

* `src/` — Java application source code
* `pom.xml` — Maven build configuration
* `Docker-files/` — Dockerfiles for app, db, and web

```bash
git add .
git commit -m "initial commit"
git push -u origin main
```

 [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## Step 2: Set Up SonarQube on EC2

**Launch EC2 instance:** [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

* AMI: **Ubuntu 22.04**
* Instance type: **t3.medium** (minimum — SonarQube needs 2GB RAM)
* Security group: Port 22 from your IP (SSH), Port 80 from anywhere (SonarQube UI)
* User data: use the setup script from `https://github.com/hkhcoder/vprofile-project/blob/electron/userdata/sonar-setup.sh` [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

**Generate SonarQube token:** [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

1. Open `http://<ec2-ip>` in browser
2. Login: `admin` / `admin` → set new password
3. Go to **My Account → Security → Generate Token**
4. Name: `github-actions`, Type: **Global Analysis Token**
5. **Copy the token** — store as `SONAR_TOKEN` in Step 6

**Create `sonar-project.properties`** in the app repo root: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

```properties
sonar.projectKey=vprofile-java99
sonar.projectName=vprofile-java99
sonar.projectVersion=1.0
sonar.sources=src/
sonar.java.binaries=target/classes
sonar.junit.reportsPath=target/surefire-reports/
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.java.checkstyle.reportPaths=target/checkstyle-result.xml
```

 [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

## Step 3: Create ECR Repository

AWS Console → **ECR** → **Create repository**: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

* Name: `vproappimg`
* Visibility: **Private**
* Note the ECR URI: `<account-id>.dkr.ecr.<region>.amazonaws.com/vproappimg`

***

## Step 4: Create IAM User for GitHub Actions

AWS Console → **IAM** → **Users** → **Create user**: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

* Name: `github-actions-user`
* Attach policies: **AmazonEC2ContainerRegistryFullAccess** (+ **AmazonEKSClusterPolicy** if deploying to EKS)
* **Security credentials** → **Create access key** → select "Application running outside AWS"
* **Copy Access Key ID and Secret Access Key**

***

## Step 5: Set Up Slack Notifications

1. Go to `api.slack.com/apps` → **Create New App → From scratch** [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)
2. Name: `GitHub Actions`, select your workspace
3. **Incoming Webhooks** → **Activate** → **Add New Webhook to Workspace**
4. Select channel (e.g., `#deployments`)
5. **Copy webhook URL** (format: `https://hooks.slack.com/services/xxx/yyy/zzz`)

***

## Step 6: Create GitHub Secrets and Variables

### 6a: Create GitHub PAT (for cross-repo Helm access)

GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens**: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

* Token name: `helm-pipeline`
* Repository access: **Only select repositories** → select `vprofile-helm`
* Permissions → Contents: **Read and write**
* **Copy the token**

### 6b: Create Secrets

Go to `vprofile-java-app` repo → **Settings → Secrets and variables → Actions → Secrets**: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

| Secret Name             | Value                           |
| ----------------------- | ------------------------------- |
| `SONAR_TOKEN`           | SonarQube token from Step 2     |
| `AWS_ACCESS_KEY_ID`     | IAM user access key from Step 4 |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key from Step 4 |
| `HELM_REPO_USER`        | Your GitHub username            |
| `GITOPS_PAT`            | GitHub PAT from Step 6a         |
| `SLACK_WEBHOOK`         | Slack webhook URL from Step 5   |

### 6c: Create Variables

Go to **Settings → Secrets and variables → Actions → Variables**: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

| Variable Name    | Value           |
| ---------------- | --------------- |
| `AWS_REGION`     | `us-east-1`     |
| `ECR_REPOSITORY` | `vproappimg`    |
| `HELM_REPO_NAME` | `vprofile-helm` |

***

## Step 7: Create the GitHub Actions Pipeline

Create a feature branch:

```bash
git checkout -b feature-x
```

Create `.github/workflows/ci.yml` using the detailed prompt provided in the setup document. The prompt specifies: Java 21, Maven, WAR packaging, self-hosted SonarQube, multi-stage Dockerfile at `Docker-files/app/multistage/Dockerfile`, ECR push with commit SHA tag, Helm `values.yaml` update using `yq`, job outputs for passing data between jobs, and caching for Maven and SonarQube dependencies. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

**Pipeline structure:** [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

```yaml
trigger:
  push → main          # docker + helm jobs only
  pull_request → main  # sonar job only

jobs:
  build-and-sonar:       # runs on PR only
  docker-build-push:     # runs on push to main, outputs image_tag + ecr_registry
  update-helm:           # runs on push to main, needs docker-build-push
```

***

## Step 8: Set Up Branch Protection

Go to repo → **Settings → Branches → Add branch ruleset**: [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

* Target: `main`
* Enable:
  * **Require a pull request before merging**
  * **Require status checks to pass** → add `build-and-sonar`
  * **Block force pushes**

***

## Step 9: Execute the Workflow

```bash
# On feature branch
git add .
git commit -m "add CI pipeline"
git push -u origin feature-x
```

Open a PR on GitHub targeting `main` → pipeline runs `build-and-sonar` → if quality gate passes → merge → pipeline runs `docker-build-push` → `update-helm` → Slack notification → ArgoCD picks up the change. [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Complete Pipeline Architecture

```
DEVELOPER
  │
  ├── push to feature branch → NOTHING HAPPENS
  │
  ├── open PR to main → TRIGGERS:
  │     └── JOB 1: build-and-sonar
  │           ├── Maven build + unit tests
  │           ├── Checkstyle analysis
  │           ├── SonarQube scan → EC2 SonarQube server
  │           └── Quality gate check
  │                 ├── PASS → merge allowed
  │                 └── FAIL → merge BLOCKED
  │
  └── merge PR to main → TRIGGERS:
        ├── JOB 2: docker-build-push
        │     ├── Build Docker image (multi-stage)
        │     ├── Tag: commit SHA + latest
        │     └── Push to Amazon ECR
        │
        └── JOB 3: update-helm (needs JOB 2)
              ├── Clone vprofile-helm repo
              ├── Update values.yaml (image + tag via yq)
              ├── Commit + push
              └── Slack notification
                    │
                    ▼
              ARGOCD (watches Helm repo) → deploys new version
```

***

## 🔷 Two Repositories

```
vprofile-java-app (APP REPO):
  ├── src/                          ← Java source code
  ├── pom.xml                       ← Maven config
  ├── Docker-files/app/multistage/  ← Dockerfile
  ├── sonar-project.properties      ← SonarQube config
  └── .github/workflows/ci.yml      ← Pipeline definition

vprofile-helm (HELM REPO):
  └── helm/vprofile/values.yaml     ← Updated by pipeline
        app:
          image: <ECR-URI>          ← written by JOB 3
          tag: <commit-SHA>         ← written by JOB 3
```

***

## 🔷 GitHub Secrets Map

```
SECRET                  AUTHENTICATES WITH        PURPOSE
────────────────        ────────────────────      ──────────────
SONAR_TOKEN             SonarQube EC2 server      Code quality scan
AWS_ACCESS_KEY_ID       AWS IAM                   ECR image push
AWS_SECRET_ACCESS_KEY   AWS IAM                   ECR image push
HELM_REPO_USER          GitHub                    Helm repo identity
GITOPS_PAT              GitHub (cross-repo)       Write to Helm repo
SLACK_WEBHOOK           Slack API                 Notifications

VARIABLES (non-secret):
  AWS_REGION        = us-east-1
  ECR_REPOSITORY    = vproappimg
  HELM_REPO_NAME    = vprofile-helm
```

***

## 🔷 Infrastructure Components

```
COMPONENT           PLATFORM        PURPOSE
──────────          ──────────      ────────────────────────
SonarQube           EC2 (Ubuntu)    Code quality + quality gate
ECR                 AWS             Private Docker image registry
IAM User            AWS             Pipeline auth to ECR
Slack App           Slack           Pipeline notifications
GitHub PAT          GitHub          Cross-repo write access
Branch Protection   GitHub          Enforce PR + quality gate
```

***

## 🔷 SonarQube Setup (Compressed)

```
EC2: Ubuntu 22.04, t3.medium (2GB RAM minimum)
SG:  22 (SSH, my IP) + 80 (SonarQube UI, anywhere)
Setup: userdata script (automated)
Login: admin/admin → set new password
Token: My Account → Security → Generate Token → Global Analysis Token
Config: sonar-project.properties in app repo root
```

***

## 🔷 Pipeline Job Dependencies

```
build-and-sonar ──── runs on: pull_request to main
                     no dependencies

docker-build-push ── runs on: push to main
                     no dependencies
                     OUTPUTS: image_tag, ecr_registry

update-helm ──────── runs on: push to main
                     NEEDS: docker-build-push (uses its outputs)
```

***

## 🔷 Branch Protection = Automated Quality Gate

```
RULE                              EFFECT
──────────────────────            ──────────────────────────────
Require PR before merging         No direct push to main
Require status checks to pass     build-and-sonar must succeed
Block force pushes                Cannot bypass protections

RESULT:
  Code with quality issues → quality gate fails → merge blocked
  Code passing quality gate → merge allowed → triggers build + deploy
```

***

## 🔷 Feature Branch Workflow

```bash
git checkout -b feature-x          # create branch
# make changes
git push -u origin feature-x       # push (no pipeline)
# open PR to main                  # triggers build-and-sonar
# quality gate passes              # merge allowed
# merge PR                         # triggers docker-build-push + update-helm
```

***

## 🔷 Image Tagging Strategy

```
TAG 1: commit SHA (e.g., a1b2c3d)
  → Precise version identification
  → Traceable to exact code commit
  → Used in values.yaml for deployment

TAG 2: latest
  → Convenience tag
  → Always points to most recent build
  → NOT used for production deployments (ambiguous)
```

***

## 🔷 values.yaml Update (Bridge Between CI and CD)

```yaml
# BEFORE pipeline:
app:
  image: <old-ecr-uri>
  tag: <old-sha>

# AFTER pipeline (JOB 3 uses yq to update):
app:
  image: <account>.dkr.ecr.us-east-1.amazonaws.com/vproappimg
  tag: a1b2c3d    # new commit SHA

# ArgoCD watches this file → detects change → deploys new version
```

***

## 🔷 Reusable Engineering Pattern: GitOps CI/CD Pipeline

```
PATTERN: Code Change → Quality Gate → Build → Registry → GitOps Update → Deploy

1. CODE CHANGE:     Developer pushes to feature branch
2. QUALITY GATE:    PR triggers scan (SonarQube) → blocks if fails
3. BUILD:           Merge triggers Docker build (multi-stage)
4. REGISTRY:        Image pushed to ECR with commit SHA tag
5. GITOPS UPDATE:   Pipeline updates Helm values.yaml in separate repo
6. DEPLOY:          ArgoCD detects change → deploys automatically

SEPARATION OF CONCERNS:
  App repo = WHAT to build (source code + Dockerfile)
  Helm repo = HOW to deploy (Kubernetes manifests + values)
  Pipeline = WHEN and HOW to build (CI logic)
  ArgoCD = WHEN to deploy (CD logic, watches Helm repo)

NO HUMAN touches deployment config directly.
Pipeline is the ONLY writer to the Helm repo.
Every deployment is traceable to a commit SHA.

This pattern applies to ANY application:
  Replace SonarQube with any code scanner
  Replace ECR with any registry (DockerHub, GCR, ACR)
  Replace Helm with Kustomize or raw manifests
  Replace ArgoCD with FluxCD or any GitOps tool
  The PATTERN is constant; the TOOLS are interchangeable.
```

This lecture is architecturally the most complex in the course — it connects **six external systems** (GitHub, SonarQube, AWS ECR, AWS IAM, Slack, Helm repo) into one automated pipeline. The key insight is that the pipeline's final output is not a running application — it's a **commit to the Helm repository**. The deployment itself is handled by a completely separate system (ArgoCD), creating clean separation between CI and CD. [\[366-ci-pip...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366-ci-pipeline-overview.txt), [\[366.CICDPi...elineSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/366.CICDPipelineSetup.txt)
