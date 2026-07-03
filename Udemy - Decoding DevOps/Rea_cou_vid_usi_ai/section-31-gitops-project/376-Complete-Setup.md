# 🎓 Deep Learning Material: Completing the Whole Setup — End-to-End GitOps CI/CD Pipeline Validation

**Source:** [376-completing-the-whole-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt?EntityRepresentationId=b2bc3b34-123c-48a0-8b03-73d0c252c0ae) — Video lecture covering the complete end-to-end validation of the GitOps CI/CD pipeline: configuring DNS for the Ingress endpoint, verifying the vProfile application (DB, RabbitMQ, Memcache), then triggering the full pipeline flow — code commit on feature branch → pull request → SonarQube code analysis → quality gate → merge to main → Docker image build + push to ECR → Helm values.yaml tag update → Argo CD detects change → rolling update of the app Pod with the new image. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Complete GitOps CI/CD Flow — The Big Picture

This lecture demonstrates the **entire automated pipeline** working end-to-end. Every component built across previous lectures — the EKS cluster, Helm charts, Argo CD, GitHub Actions, SonarQube, ECR, DNS — is now connected and functioning as a single system. The flow is: [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Developer makes a code change** (feature branch) → **pushes to GitHub** → **creates a Pull Request to main** → **GitHub Actions pipeline triggers** → **SonarQube analyzes code quality** → **quality gate passes** → **developer merges PR to main** → **merge triggers the build pipeline** → **Docker image is built and pushed to Amazon ECR** → **pipeline updates the image tag in the Helm repository's `values.yaml`** → **Argo CD detects the change in the Helm repo** → **Argo CD fetches the latest Helm chart** → **Argo CD deploys the new version on the Kubernetes cluster** → **rolling update: new Pod created, old Pod deleted**. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

This is a **two-repository GitOps model**: one repository for application code (`vprofile-app`), one for Helm charts (`vprofile-helm`). The CI pipeline (GitHub Actions) bridges them — it builds the image from the app repo and updates the tag in the helm repo. Argo CD watches only the helm repo. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## 1.2 The Two-Phase Pipeline — PR Phase vs Merge Phase

The pipeline has **two distinct trigger points** with different behaviors: [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

### Pull Request Phase (Code Quality Gate)

When a **pull request is created** targeting the `main` branch, GitHub Actions triggers the **code analysis** stage. SonarQube scans the code and evaluates it against the quality gate. If the quality gate passes, the PR is marked as successful. If it fails, the merge should be blocked. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

This phase does NOT build a Docker image. It only validates code quality. This is intentional — you don't want to build and push images for every PR. You want to verify quality first, then build only after the code is approved and merged. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

### Merge/Push Phase (Build + Deploy)

When the PR is **merged** (which is a push to `main`), GitHub Actions triggers the **build pipeline**: build the Docker image, push it to Amazon ECR, then update the `values.yaml` in the Helm repository with the new image tag. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

This separation ensures: only code that passes quality analysis and is approved by a reviewer gets built into a deployable image. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## 1.3 The Image Tag as the Deployment Trigger

The key mechanism connecting CI to CD is the **image tag in `values.yaml`**. The CI pipeline (GitHub Actions) updates this tag after building and pushing the new image. Argo CD watches the Helm repository. When it detects the tag change, it re-renders the Helm templates with the new values and applies the changes to the cluster. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

The instructor demonstrates this explicitly: before the merge, they note the current tag in the app Pod (`kubectl describe pod` shows the container image and tag). After the pipeline completes, they check the Helm repository — the tag has been updated. Then Argo CD picks it up and deploys. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

The rolling update behavior is visible in Argo CD's UI: a new Pod is created with the new image tag, and once it's healthy, the old Pod is deleted. This is Kubernetes' default rolling update strategy — zero-downtime deployment. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## 1.4 Argo CD Sync — Automatic vs Manual

Argo CD periodically polls the Helm repository for changes. If it detects a difference between the desired state (in Git) and the actual state (on the cluster), it can either **auto-sync** or wait for **manual sync**. In the video, the instructor clicks **Sync → Synchronize** in the Argo CD UI to trigger an immediate deployment rather than waiting for the polling interval. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

After syncing, the Argo CD dashboard shows the `vproapp` deployment being updated ("two seconds ago"), a new Pod being created, the new Pod becoming healthy, and then the old Pod being deleted. The instructor then verifies the new tag is present in the newly created Pod. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## 1.5 Feature Branch Strategy — Safe Commits

The instructor works on a **feature branch** (`feature-x`), not directly on `main`. Commits to the feature branch do **not** trigger the pipeline — "when I make any commit over here and push it to GitHub, it's not going to run the pipeline." The pipeline is designed to trigger only on: (1) pull requests to `main`, and (2) pushes to `main` (merges). [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

This is standard branch protection: developers work on feature branches, make as many commits as they want, and only trigger CI/CD when they create a PR or when the PR is merged. This prevents unnecessary builds and ensures only reviewed code reaches production. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## 1.6 SonarQube Server URL — Runtime Configuration

Before triggering the pipeline, the instructor updates the **SonarQube server URL** in GitHub repository settings. The SonarQube server runs on an EC2 instance with a changing public IP (each time the instance is stopped and started, it gets a new IP). The URL is stored in GitHub Actions **variables** (Settings → Secrets and Variables → Actions → Variables → `SONAR_HOST_URL`). This must be updated to the current public IP before running the pipeline. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

⚠️ **Expert Note**
In production, the SonarQube server would have a stable DNS name or an Elastic IP, eliminating this manual step. For the learning environment, updating the variable before each pipeline run is a necessary operational step. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## 1.7 Application Verification — The Deployment Is Working

Before testing the pipeline, the instructor verifies the existing deployment by accessing the application through the browser:

* **HTTPS access** via `https://vprofile.<domain>` → login page loads → Ingress + ALB + DNS working.
* **Login** with `admin_vp`/`admin_vp` → success → DB Pod + PVC + EBS verified.
* **RabbitMQ test** → "RabbitMQ is also working."
* **Memcache test** → "All Users" → click user → "data inserted in cache" → click again → "data is coming from the caching." [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

The instructor confirms: "Vprofile application is deployed by Argo CD. It has fetched all the details from the repository, the helm charts on the repository, and deployed on our Kubernetes cluster." [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## 1.8 The Clone-Fresh Strategy

Instead of dealing with Git conflicts from local changes, the instructor deletes the local repository and clones it fresh. The clone uses an SSH endpoint with a custom SSH config alias: `github.com-devOpsForSure` (matching the SSH config file entry for the correct SSH key). This is a practical technique for avoiding merge conflicts in demo/learning environments. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing

We are executing and validating the complete GitOps CI/CD pipeline: configuring DNS for the deployed application, verifying all components work, then making a code change that flows through the entire pipeline — from Git commit to running Pod update — proving the automation is fully functional. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 1: Get the Ingress Endpoint and Configure DNS

**1a. Get the Ingress endpoint:**

```bash
kubectl get ingress -n vprofile
```

 [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

| Part          | Meaning                     |
| ------------- | --------------------------- |
| `get ingress` | List Ingress objects        |
| `-n vprofile` | In the `vprofile` namespace |

Note the **ADDRESS** field — this is the ALB endpoint. You can also copy it from the Argo CD UI (the hostname shown on the Ingress resource). [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**1b. Create DNS CNAME record:**

Go to GoDaddy (or your domain registrar) → DNS Records → Add New Record:

| Field | Value            |
| ----- | ---------------- |
| Type  | CNAME            |
| Host  | `vprofile`       |
| Value | `<ALB endpoint>` |

Save. Wait 5-10 minutes for DNS propagation. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 2: Verify the Application

**2a. Access via browser:**

```
https://vprofile.<your-domain>
```

The vProfile login page should load (HTTPS via ALB certificate). [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**2b. Login:** `admin_vp` / `admin_vp` → verifies DB Pod + PVC + EBS.

**2c. RabbitMQ test:** Click RabbitMQ link → should show "working."

**2d. Memcache test:** All Users → click user → "data inserted in cache" → click again → "data from cache." [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 3: Note the Current App Image Tag

```bash
kubectl describe pod <vproapp-pod-name> -n vprofile
```

Find the **Container Image** field — note the current image name and **tag**. This tag should change after the pipeline runs. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

Keep this tab open or write down the tag for comparison later.

***

## Step 4: Prepare the App Repository

**4a. Clone fresh (recommended to avoid conflicts):**

```bash
cd ~/Desktop/gitops
rm -rf vprofile-app
git clone git@github.com-devOpsForSure:<account>/vprofile-app.git
cd vprofile-app
```

 [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

The SSH endpoint uses the alias from the SSH config file (`github.com-devOpsForSure`) to select the correct SSH key. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**4b. Switch to the feature branch:**

```bash
git checkout feature-x
```

**4c. Open in VS Code:**

```bash
code .
```

 [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 5: Update the SonarQube Server URL

Go to GitHub → `vprofile-app` repository → **Settings** → **Secrets and Variables** → **Actions** → **Variables**. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

Find `SONAR_HOST_URL`. Click **Edit**. Update the public IP to the current SonarQube server IP. Save (requires GitHub password re-entry). [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

⚠️ If you skip this, the code analysis stage will fail because it can't reach the SonarQube server.

***

## Step 6: Make a Code Change and Push

**6a. Make a trivial change:**

Edit `README.md` — add a comment, a hash, anything. Save (`Ctrl+S`). [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**6b. Commit and push to the feature branch:**

```bash
git add .
git commit -m "test pipeline 99"
git push origin feature-x
```

 [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Expected:** Nothing happens in GitHub Actions yet. The pipeline only triggers on PRs to `main` or pushes to `main`. A push to `feature-x` alone does not trigger anything. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 7: Create a Pull Request

Go to GitHub → `vprofile-app` repository. GitHub may show a banner: "Compare & pull request." [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

Otherwise: **Pull Requests** → **New Pull Request** → base: `main`, compare: `feature-x` → **Create Pull Request**. Add a title and description. Click **Create Pull Request**. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Expected:** The PR triggers the GitHub Actions pipeline — specifically the **code analysis** stage. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Verify:** Go to **Actions** tab. You should see the pipeline running. It will execute SonarQube code analysis. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Wait** for the pipeline to complete. Expected result: "Code analysis completed successfully. Quality gate is good." [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 8: Merge the Pull Request

Go to the open Pull Request. Click **Merge Pull Request** → **Confirm Merge**. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

The instructor notes: "Some authorized party is going to look at the pull request. If everything checks out fine, he or she's going to confirm the merge." [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Expected:** The merge (push to `main`) triggers the **build pipeline**:

1. Build Docker image.
2. Push to Amazon ECR.
3. Update the image tag in `vprofile-helm` repository's `values.yaml`. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Verify:** Go to **Actions** tab. You should see the merge-triggered pipeline running. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 9: Verify the Helm Repository Update

While the pipeline runs, open the `vprofile-helm` repository on GitHub. Check `values.yaml` — note the current `app.tag` value. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

After the pipeline completes, **refresh** the `vprofile-helm` page. The `app.tag` should now show a **new tag** (matching the newly built image). [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 10: Sync Argo CD

Open the Argo CD dashboard. The current deployment may still show the old tag. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

Click **Sync** → **Synchronize** to trigger an immediate deployment (instead of waiting for the polling interval). [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

**Expected behavior in Argo CD UI:**

1. `vproapp` deployment shows update ("two seconds ago").
2. A **new Pod** is created with the new image tag.
3. Once the new Pod is healthy, the **old Pod is deleted**.
4. Rolling update complete — zero downtime. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

***

## Step 11: Verify the New Tag in the Pod

```bash
kubectl describe pod <new-vproapp-pod-name> -n vprofile
```

The **Container Image** field should now show the **new tag** — matching what was pushed to ECR and updated in `values.yaml`. [\[376-comple...hole-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/376-completing-the-whole-setup.txt)

Compare with the tag you noted in Step 3. They should be different — confirming the entire pipeline worked end-to-end.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Complete CI/CD Pipeline Flow

```
DEVELOPER
  │
  │  feature-x branch: edit README → git add/commit/push
  │  (nothing triggers)
  │
  ▼
PULL REQUEST (feature-x → main)
  │
  │  TRIGGERS: GitHub Actions → SonarQube code analysis
  │  Quality gate: pass/fail
  │  (NO image build yet)
  │
  ▼
MERGE PR (push to main)
  │
  │  TRIGGERS: GitHub Actions → build pipeline
  │    1. Build Docker image
  │    2. Push to Amazon ECR
  │    3. Update app.tag in vprofile-helm/values.yaml
  │
  ▼
HELM REPO CHANGE DETECTED
  │
  │  Argo CD polls (or manual Sync)
  │  Fetches latest Helm chart
  │  Renders templates with new values
  │
  ▼
KUBERNETES CLUSTER
  │
  │  Rolling update:
  │    New Pod (new tag) created → healthy → old Pod deleted
  │
  ▼
APPLICATION UPDATED (zero downtime)
```

***

## Two-Phase Pipeline

```
PHASE 1: Pull Request → Code Analysis
  Trigger:  PR to main
  Action:   SonarQube scan → quality gate
  Output:   pass/fail (no image built)
  Purpose:  validate before merge

PHASE 2: Merge → Build + Deploy
  Trigger:  push to main (merge)
  Action:   Docker build → ECR push → Helm tag update
  Output:   new image in ECR + updated values.yaml
  Purpose:  build and trigger deployment
```

***

## Two-Repository GitOps Model

```
vprofile-app (application code)
  │
  │  GitHub Actions (CI)
  │    builds image → pushes to ECR
  │    updates tag in ↓
  │
  ▼
vprofile-helm (Helm charts)
  │
  │  Argo CD watches (CD)
  │    detects values.yaml change
  │    deploys to K8s cluster
  │
  ▼
EKS Cluster (running application)

CI pipeline BRIDGES the two repos:
  reads from app repo → writes to helm repo
```

***

## Image Tag as Deployment Trigger

```
BEFORE pipeline:  app.tag = "old-tag-abc"
AFTER pipeline:   app.tag = "new-tag-xyz"

values.yaml change → Argo CD detects → sync → rolling update
The tag is the SINGLE value that triggers the entire deployment
```

***

## Rolling Update in Argo CD

```
Sync triggered
  → Deployment spec updated (new image tag)
    → K8s creates NEW Pod (new image)
      → Health check passes → Pod healthy
        → K8s deletes OLD Pod
          → Zero-downtime update complete

Visible in Argo CD UI:
  vproapp "2 seconds ago" → new pod creating → old pod terminating
```

***

## Branch Protection Strategy

```
feature-x branch:
  commit + push → NOTHING triggers (safe to experiment)

Pull Request (feature-x → main):
  → code analysis ONLY (no build)

Merge to main:
  → build + push + helm update (full pipeline)

Only REVIEWED + QUALITY-CHECKED code reaches production
```

***

## Pre-Pipeline Checklist

```
✓ SonarQube server running (EC2 instance up)
✓ SONAR_HOST_URL updated in GitHub → Settings → Variables
✓ Ingress endpoint has DNS CNAME record
✓ Argo CD dashboard accessible
✓ Note current app Pod image tag (for comparison)
```

***

## Application Verification Chain

```
https://vprofile.<domain>     → Ingress + ALB + DNS + cert
Login admin_vp/admin_vp       → DB Pod + PVC + EBS
RabbitMQ link                 → MQ Pod + Service
All Users → click user ×2     → Memcache Pod + caching

All verified by Argo CD deployment of Helm charts
```

***

## DNS Configuration

```
kubectl get ingress -n vprofile → copy ADDRESS (ALB endpoint)
GoDaddy → DNS → Add CNAME:
  Host: vprofile
  Value: <ALB endpoint>
Wait 5-10 min for propagation
```

***

## Clone-Fresh Strategy

```bash
rm -rf vprofile-app
git clone git@github.com-devOpsForSure:<account>/vprofile-app.git
cd vprofile-app
git checkout feature-x
code .

SSH alias: github.com-devOpsForSure (from ~/.ssh/config)
Why: avoids merge conflicts in demo/learning environment
```

***

## Command Sequence (Pipeline Test)

```bash
# 1. Make change
vim README.md                    # trivial edit
git add .
git commit -m "test pipeline 99"
git push origin feature-x       # nothing triggers yet

# 2. GitHub UI
# Create PR: feature-x → main   → triggers code analysis
# Wait for quality gate pass
# Merge PR                       → triggers build pipeline

# 3. Verify
# Check vprofile-helm values.yaml → tag updated
# Argo CD → Sync → Synchronize   → rolling update starts
kubectl describe pod <new-pod> -n vprofile  → verify new tag
```

***

## What Gets Updated Where

```
ECR:              new Docker image pushed (with new tag)
vprofile-helm:    values.yaml → app.tag updated to new tag
EKS cluster:     vproapp Deployment → new Pod with new image
Argo CD:         synced state matches Git state
```

***

## Key Engineering Patterns

| Pattern                          | Manifestation                                                                                 |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| **Two-repo GitOps**              | App code and deployment config in separate repos — CI bridges them, CD watches only config    |
| **Tag as deployment trigger**    | Single value change (image tag) cascades through: Git → Argo CD → K8s → Pod update            |
| **PR-gated quality**             | Code analysis on PR, build on merge — quality gate before production artifact creation        |
| **Rolling update**               | New Pod up + healthy → old Pod down — zero-downtime deployment as default K8s behavior        |
| **Manual sync option**           | Argo CD auto-polls but also supports manual sync for immediate deployment                     |
| **Clone-fresh for clean state**  | Delete and re-clone instead of resolving conflicts — practical for learning/demo environments |
| **Variable-based server config** | SonarQube URL as GitHub Actions variable — runtime infrastructure configuration               |

***

## Project Continuity

```
BEFORE: Helm charts generated (365), Argo CD configured, GitHub Actions pipeline built
THIS:   Complete end-to-end pipeline validation — commit to deployment
NEXT:   Do's and don'ts in real-time pipeline management
        Terraform pipeline through GitHub Actions
```

***

This completes the full reconstruction. **Theory** explains the two-phase pipeline, the two-repository GitOps model, and how the image tag cascades through the system. **Practical** walks through every step from DNS setup through the commit-PR-merge-sync cycle with exact commands and verification. The **Compression Map** gives you the complete pipeline flow diagram, the branch protection strategy, and the command sequence for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
