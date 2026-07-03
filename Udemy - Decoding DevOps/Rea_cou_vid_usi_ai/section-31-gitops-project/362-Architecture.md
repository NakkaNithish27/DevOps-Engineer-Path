# GitOps Pipeline Architecture — Deep Learning Material

**Source:** [362-architecture.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt?EntityRepresentationId=2927636c-e215-47d8-9bf3-cbca2375e358) (VTT Caption File) and [362.GitOpsFInal-DDCCourse.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf?EntityRepresentationId=eaae431a-9b91-49de-b0eb-1c3eac1ac06a) (Architecture Diagram) [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What This System Is — The Big Picture

This lecture presents the **complete GitOps pipeline architecture** for the vprofile project. It is the architectural blueprint that governs how infrastructure is provisioned, how application code is tested and containerized, and how deployments are kept in sync with the desired state defined in Git. The instructor frames it clearly: this is both the **project-specific flow** and a **general GitOps flow** — the same architecture applies regardless of whether you use GitHub or GitLab, AWS or Azure or GCP. The platforms are interchangeable; the pattern is universal. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

The architecture is divided into **two sides**: the **left side is GitHub** (the source of truth — code, configuration, and pipeline definitions), and the **right side is AWS** (the execution environment — where infrastructure runs and applications are deployed). Everything on the left drives everything on the right. This is the fundamental GitOps principle: **Git is the single source of truth**, and the live environment must always reflect what Git says. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

## 1.2 Three Git Repositories — The Structural Foundation

The entire system is organized into **three separate Git repositories**, each with a distinct responsibility. This separation is not arbitrary — it reflects a core architectural decision about what changes independently and what should trigger different workflows. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

### 1.2.1 `vprofile-infra` — Infrastructure as Code (Terraform)

This repository contains the **Terraform source code** that defines the AWS infrastructure — specifically the EKS (Elastic Kubernetes Service) cluster. The infrastructure pipeline (managed by GitHub Actions) ensures that changes to this Terraform code are validated, planned, applied, and monitored for drift on the live AWS environment. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

The GitHub Actions pipeline for this repository has the following stages (visible in the architecture diagram): **Validate → Plan → Apply → Drift Detection → Notify (Slack) → Destroy**. This is a full infrastructure lifecycle pipeline: it validates the Terraform syntax, plans the changes, applies them to create/modify the EKS cluster, periodically detects whether the live infrastructure has drifted from the desired Terraform state, notifies the team via Slack if drift is detected, and provides a destroy capability for teardown. [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

### 1.2.2 `vprofile-app` — Application Source Code (Java)

This repository contains the **vprofile application Java source code**. It has its own GitHub Actions pipeline that handles both **Continuous Integration** (testing, code analysis) and **Continuous Delivery** (building Docker images and pushing them to Amazon ECR). [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

This pipeline is the most complex in terms of stages, and the instructor explains it in the most detail (covered in §1.3 below).

### 1.2.3 `vprofile-helm` — Helm Charts and Argo CD Manifests

This repository contains **Helm charts** (Kubernetes deployment configuration) and **Argo CD manifests** (the Argo CD project/application definitions). Critically, this repository has **no pipeline**. It is a pure configuration repository. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

The repository structure includes: a `charts/` folder containing a `vprofile/` subfolder, which contains a `values.yaml` file. The `values.yaml` file holds the **Docker image name and tag** that define which version of the application is currently deployed. When the application pipeline builds a new Docker image, it updates this `values.yaml` file with the new image tag. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

Argo CD (running inside the EKS cluster) **continuously watches** this repository. When it detects a change (e.g., an updated image tag in `values.yaml`), it automatically applies the difference to the Kubernetes cluster — updating deployments, services, or whatever Kubernetes resources the Helm chart defines. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

> 🔍 **Deep Dive**
> The three-repository separation encodes a principle of **change isolation**: infrastructure changes (Terraform) are independent of application code changes (Java), which are independent of deployment configuration changes (Helm). Each can evolve at its own pace, be reviewed by different teams, and trigger different workflows. A change to the Java code should not accidentally modify infrastructure; a Helm chart update should not require rebuilding the application. This separation also enables different access controls — infrastructure repos might be restricted to platform engineers, while app repos are open to all developers. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## 1.3 The Application Pipeline — CI/CD Flow in Detail

The `vprofile-app` pipeline is the most detailed flow described in the lecture. It operates in **two distinct phases**, triggered by different Git events: [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

### Phase 1: Pull Request → Continuous Integration

When a developer creates a **feature branch**, writes new code, and commits it, **nothing happens** — no pipeline is triggered by a commit to a feature branch. The pipeline activates only when a **Pull Request (PR)** is created to merge the feature branch into the **main branch**. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

The PR triggers the CI pipeline, which executes these stages sequentially:

1. **Build & Unit Test** — Compiles the source code and runs unit tests (Maven).
2. **Checkstyle Code Analysis** — Runs static code style analysis (Maven Checkstyle).
3. **Code Analysis with SonarQube** — Performs deep code quality analysis.
4. **Upload Results to SonarQube Server** — Sends analysis results to a SonarQube server running on an **EC2 instance** in AWS.
5. **Quality Check** — SonarQube evaluates the results against quality gates. The response (pass/fail) is sent back to the pipeline.

If the quality check passes, the **CI pipeline stops**. The PR is now eligible for approval. If the quality check fails, the PR cannot proceed — the code does not meet quality standards. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

### Phase 2: Merge to Main → Continuous Delivery

When the PR is **approved and merged** into the main branch (which only happens after passing the quality check), the second phase triggers: [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

1. **Build Docker Image** — The application source code is built into a Docker image.
2. **Push to Amazon ECR** — The Docker image is pushed to Amazon Elastic Container Registry with a **new tag**.
3. **Update Image Tag in Helm Repository** — The pipeline updates the `values.yaml` file in the `vprofile-helm` repository with the new image name and tag.

This final step is the **bridge between the application pipeline and the deployment pipeline**. By updating the Helm repository, the application pipeline signals to Argo CD that a new version is available. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

> 🔍 **Deep Dive**
> The two-phase trigger design is significant. **Commits to feature branches** are completely silent — no resources are consumed, no pipelines run. **Pull Requests** trigger CI (testing and quality analysis only — no artifacts are produced). **Merges to main** trigger CD (image build, push, and Helm update). This ensures that only code that has passed review and quality gates ever produces a deployable artifact. The pipeline enforces a quality funnel: code must pass automated checks AND human review before it can reach production. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## 1.4 Argo CD — GitOps Continuous Deployment

Argo CD is a **Kubernetes-native continuous deployment controller** that runs inside the EKS cluster. Its role is conceptually simple but architecturally powerful: it **continuously watches the `vprofile-helm` Git repository** and compares the desired state (defined in the Helm charts) with the actual state of the Kubernetes cluster. If there is any difference, Argo CD automatically applies the changes to bring the cluster in sync with Git. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

The Kubernetes resources managed by Argo CD include (visible in the architecture diagram): **Deployment, Service, PersistentVolumeClaim, Ingress, and Secret**. These are the components of the vprofile application running on EKS. [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

The Argo CD manifests (which define the Argo CD project and application configuration) are stored in the same `vprofile-helm` repository. These manifests tell Argo CD what to watch and where to apply changes. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

The key insight is that **no pipeline pushes changes to the cluster**. Instead, Argo CD **pulls** changes from Git. This is the "pull-based" deployment model that defines GitOps — the cluster actively synchronizes itself with the desired state in Git, rather than a CI/CD pipeline pushing deployments into the cluster. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## 1.5 The Infrastructure Pipeline — Terraform Lifecycle

The `vprofile-infra` pipeline (managed by GitHub Actions) handles the **full Terraform lifecycle** for the EKS cluster: [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

| Stage               | Purpose                                                                    |
| ------------------- | -------------------------------------------------------------------------- |
| **Validate**        | Checks Terraform syntax and configuration validity                         |
| **Plan**            | Generates an execution plan showing what changes will be made              |
| **Apply**           | Executes the plan to create/modify AWS infrastructure                      |
| **Drift Detection** | Periodically checks if the live infrastructure matches the Terraform state |
| **Notify (Slack)**  | Sends notifications (e.g., drift alerts) to a Slack channel                |
| **Destroy**         | Tears down all infrastructure (used for cleanup)                           |

The instructor notes that the Terraform source code and pipeline will be written **at the end of the course**, after the application pipeline and Helm charts are set up. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## 1.6 The End-to-End Flow — From Developer Commit to Live Deployment

Combining all components, the complete flow from a developer's code change to a live deployment is: [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

1. **Developer** commits code to a feature branch in `vprofile-app`.
2. Developer creates a **Pull Request** to merge into main.
3. **GitHub Actions CI pipeline** triggers: build → test → checkstyle → SonarQube analysis → quality check.
4. Quality check passes → PR is eligible for review.
5. PR is **approved and merged** to main.
6. **GitHub Actions CD pipeline** triggers: build Docker image → push to **Amazon ECR** → update `values.yaml` in `vprofile-helm` with new image tag.
7. **Argo CD** (running in EKS) detects the change in `vprofile-helm`.
8. Argo CD applies the change to the Kubernetes cluster — updates the **Deployment** with the new image tag.
9. Kubernetes performs a rolling update — new Pods with the new image replace old Pods.
10. The application is live with the new code.

No human manually deploys anything. The entire flow is automated, quality-gated, and Git-driven. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## 1.7 Implementation Order — The Course Roadmap

The instructor outlines the **order in which the system will be built** across the upcoming lectures: [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

1. **Create the three Git repositories** and sync them to local.
2. **Set up the Helm charts** in `vprofile-helm` (values.yaml, chart structure, Argo manifests).
3. **Build the vprofile-app pipeline** (CI: test/analyze, CD: Docker build/push/Helm update).
4. **Write the Terraform source code** in `vprofile-infra` and create the EKS cluster.
5. **Deploy Argo CD manifests** to the cluster.
6. Everything connects — Argo CD watches the Helm repo, the app pipeline updates the Helm repo, infrastructure is managed by Terraform.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

This lecture is an **architecture overview** — no commands are executed. The practical content here focuses on understanding the **operational structure** that will be built in subsequent lectures: three Git repositories, two GitHub Actions pipelines, Argo CD deployment, and Terraform infrastructure management. The final operational outcome is a fully automated GitOps pipeline where a developer's code commit flows through quality gates, becomes a Docker image, and is automatically deployed to a Kubernetes cluster via Argo CD — with zero manual deployment steps. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## Operational Structure — What Will Be Created

### Three Git Repositories

| Repository       | Content                         | Pipeline?            | Trigger                              |
| ---------------- | ------------------------------- | -------------------- | ------------------------------------ |
| `vprofile-infra` | Terraform source code           | Yes (GitHub Actions) | Changes to Terraform code            |
| `vprofile-app`   | Java application source code    | Yes (GitHub Actions) | PR to main (CI) / Merge to main (CD) |
| `vprofile-helm`  | Helm charts + Argo CD manifests | **No pipeline**      | Watched by Argo CD (pull-based)      |

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

### Two Pipelines

**Pipeline 1: `vprofile-app` (Application CI/CD)**

```
[PR to main] ──► Build & Unit Test → Checkstyle → SonarQube Analysis
                  → Upload to SonarQube Server (EC2) → Quality Check
                  → STOP (CI complete, await approval)

[Merge to main] ──► Build Docker Image → Push to Amazon ECR
                    → Update image tag in vprofile-helm/charts/vprofile/values.yaml
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

**Pipeline 2: `vprofile-infra` (Infrastructure Terraform)**

```
Validate → Plan → Apply → Drift Detection → Notify (Slack) → Destroy
```

 [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

### Argo CD (No Pipeline — Pull-Based)

```
Argo CD (inside EKS) ──watches──► vprofile-helm Git repo
  └── Detects change in Helm charts / values.yaml
      └── Applies diff to Kubernetes cluster
          └── Updates: Deployment, Service, PVC, Ingress, Secret
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

## Key Operational Details to Note

### Helm Repository Structure

```
vprofile-helm/
├── charts/
│   └── vprofile/
│       └── values.yaml    ← image name + tag updated by app pipeline
└── argo-manifests/        ← Argo CD project/application definitions
```

The `values.yaml` file is the **synchronization point** between the application pipeline and Argo CD. The app pipeline writes to it; Argo CD reads from it. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

### Pipeline Trigger Rules

| Git Event                    | What Triggers                                       |
| ---------------------------- | --------------------------------------------------- |
| Commit to feature branch     | **Nothing** — no pipeline runs                      |
| Pull Request to main         | CI pipeline only (test + analysis + quality check)  |
| PR approved + merged to main | CD pipeline (Docker build + ECR push + Helm update) |

This trigger structure ensures only quality-gated, reviewed code produces deployable artifacts. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

### AWS Components

| Component           | Purpose                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| **Amazon EKS**      | Kubernetes cluster (created by Terraform from `vprofile-infra`)         |
| **Amazon ECR**      | Docker image registry (stores built application images)                 |
| **EC2 (SonarQube)** | Hosts the SonarQube server for code quality analysis                    |
| **Slack**           | Receives notifications (drift detection alerts from Terraform pipeline) |

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

### Kubernetes Resources Managed by Argo CD

The architecture diagram shows these Kubernetes resources inside the EKS cluster under Argo CD management: **Deployment, Service, PersistentVolumeClaim, Ingress, Secret**. [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

## Implementation Order (Course Roadmap)

| Step | Action                                                                      |
| ---- | --------------------------------------------------------------------------- |
| 1    | Create three Git repositories + sync to local machine                       |
| 2    | Set up Helm charts in `vprofile-helm` (charts, values.yaml, Argo manifests) |
| 3    | Build `vprofile-app` GitHub Actions pipeline (CI + CD stages)               |
| 4    | Write Terraform code in `vprofile-infra` + create EKS cluster               |
| 5    | Deploy Argo CD manifests to EKS                                             |
| 6    | End-to-end integration — all components connected                           |

The next immediate lecture creates the three Git repositories and syncs them locally. [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
GitOps Pipeline = Git is the single source of truth for EVERYTHING
  Infrastructure (Terraform) → defined in Git → applied to AWS
  Application (Java)         → built in Git   → pushed to ECR
  Deployment config (Helm)   → stored in Git  → synced by Argo CD to K8s

Left side: GitHub (source of truth)
Right side: AWS (execution environment)
GitHub drives AWS. Never the reverse.
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## Three Repositories — Separation of Concerns

```
vprofile-infra                vprofile-app                vprofile-helm
──────────────                ────────────                ─────────────
Terraform code                Java source code            Helm charts + Argo manifests
HAS pipeline (GH Actions)    HAS pipeline (GH Actions)   NO pipeline
Manages: EKS cluster          Manages: Docker images      Managed BY: Argo CD (pull)
                                                          
Pipeline stages:              Pipeline stages:            Watched by Argo CD
Validate→Plan→Apply           PR: Build→Test→Checkstyle   on change → sync to K8s
→Drift Detection→Notify       →SonarQube→Quality Check
→Destroy                      Merge: Docker Build→ECR Push
                              →Update values.yaml in helm repo
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

## Application Pipeline — Two-Phase Trigger

```
Feature branch commit ──► NOTHING (silent)

Pull Request to main ──► CI PIPELINE:
  Build & Unit Test
  → Checkstyle
  → SonarQube Analysis
  → Upload to SonarQube Server (EC2)
  → Quality Check (pass/fail)
  → STOP

PR approved + merged to main ──► CD PIPELINE:
  Build Docker Image
  → Push to Amazon ECR (new tag)
  → Update image tag in vprofile-helm/charts/vprofile/values.yaml
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## Argo CD — Pull-Based Deployment

```
Argo CD (runs INSIDE EKS cluster)
  │
  ├── Watches: vprofile-helm Git repo (continuously)
  ├── Compares: Git desired state vs K8s actual state
  ├── On difference: applies changes automatically
  │
  └── Manages K8s resources:
        Deployment | Service | PVC | Ingress | Secret
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

## Bridge: App Pipeline → Argo CD

```
App Pipeline (last step):
  updates values.yaml in vprofile-helm
    └── image name + new tag written
         │
Argo CD detects change:
  └── new image tag in values.yaml
       └── updates Deployment → rolling update → new Pods
            └── app live with new code
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## End-to-End Flow (Developer → Live App)

```
Developer
  └── commit to feature branch (nothing happens)
       └── PR to main
            └── CI: test → analyze → quality gate
                 └── PASS → PR approved → merge to main
                      └── CD: Docker build → ECR push
                           └── Update values.yaml in helm repo
                                └── Argo CD detects change
                                     └── Syncs K8s cluster
                                          └── App live ✓
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## Infrastructure Pipeline (Terraform)

```
vprofile-infra repo (GitHub Actions):

  Validate → Plan → Apply ──────────────► EKS Cluster (AWS)
                              │
                    Drift Detection (periodic)
                              │
                    Mismatch? → Notify (Slack)
                              │
                    Destroy (teardown)
```

 [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

## Helm Repository Structure

```
vprofile-helm/
  ├── charts/
  │     └── vprofile/
  │           └── values.yaml   ← image: name + tag
  │                               ← WRITTEN BY app pipeline
  │                               ← READ BY Argo CD
  └── argo-manifests/
        └── Argo CD project/app definitions
            ← tells Argo CD WHAT to watch and WHERE to apply
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## AWS Components

```
EKS ← created by Terraform (vprofile-infra)
  └── Argo CD (controller inside cluster)
  └── K8s resources: Deployment, Service, PVC, Ingress, Secret

ECR ← Docker images pushed by app pipeline
EC2 ← SonarQube server (quality analysis)
Slack ← drift detection notifications
```

 [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

## Platform Interchangeability

```
GitHub ↔ GitLab ↔ Any Git hosting
AWS    ↔ GCP    ↔ Azure ↔ Any cloud

Pattern is platform-agnostic:
  Git repos (source of truth) + CI/CD pipeline + GitOps controller + Cloud infra
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## Implementation Order

```
1. Create 3 Git repos + local sync
2. Helm charts in vprofile-helm (values.yaml, Argo manifests)
3. App pipeline in vprofile-app (CI + CD)
4. Terraform code in vprofile-infra → create EKS
5. Deploy Argo CD to EKS
6. Full integration ✓
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt)

***

## Reusable Engineering Patterns

**GitOps Pattern (Pull-Based Deployment)**

```
Git = single source of truth for desired state
Controller (Argo CD) continuously watches Git
  Detects drift between Git state and live state
  Auto-applies diff → live state = Git state

Push model: pipeline pushes TO cluster (traditional CI/CD)
Pull model: controller pulls FROM Git (GitOps)
  Benefit: cluster self-heals, Git is auditable, no direct cluster access needed
```

**Repository-Per-Concern Separation Pattern**

```
Infrastructure repo (Terraform) ← changes independently
Application repo (Java)         ← changes independently  
Config/Deployment repo (Helm)   ← changes independently

Each repo: own lifecycle, own pipeline (or none), own access controls
Bridge: app pipeline writes to config repo → triggers deployment

Recurrence: microservices (repo per service), monorepo vs polyrepo debates,
            platform engineering (infra repo vs app repo)
```

**Quality Gate Funnel Pattern**

```
Feature branch → silent (no pipeline)
PR → CI only (test + analyze)
Merge → CD only (build + deliver)

Each stage is a gate:
  Code must pass automated quality → eligible for review
  Code must pass human review → eligible for merge
  Merge triggers delivery → only quality-proven code reaches production

Recurrence: trunk-based development, branch protection rules,
            any mature CI/CD pipeline
```

**Drift Detection Pattern**

```
Desired state (Terraform code / Helm charts) vs actual state (live infra / K8s)
  Periodic comparison → detect drift → notify → remediate

Two implementations in this architecture:
  Terraform pipeline: Drift Detection → Slack notification
  Argo CD: continuous Git watch → auto-sync on difference

Recurrence: Config management (Ansible --check), compliance scanning,
            infrastructure auditing
```

 [\[362-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362-architecture.txt), [\[362.GitOps...-DDCCourse \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/362.GitOpsFInal-DDCCourse.pdf)

***

This completes the full reconstruction of the GitOps Pipeline Architecture lecture. **Theory** explains the three-repository model, the two-phase application pipeline, and Argo CD's pull-based deployment. **Practical** maps the operational structure, trigger rules, and implementation order. The **Compression Map** enables rapid recall of the end-to-end flow, component relationships, and transferable GitOps patterns. Let me know if you'd like any section refined! 🚀
