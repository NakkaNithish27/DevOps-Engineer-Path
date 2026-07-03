# GitOps Pipeline — Introduction to the Final VProfile Project

**Source:** Video caption file — *"Introduction"* (GitOps Pipeline section, final project of the DevOps course) [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is GitOps and Why It Is the Modern DevOps Standard

GitOps is a practice where the **Git repository becomes the single source of truth for all operational changes** — infrastructure, application configuration, deployment manifests, and platform settings. The video opens with a strong positioning statement: "In today's time, a modern DevOps means a GitOps Pipeline." This is not a peripheral concept — it is the culmination of everything taught in the course. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

The core principle is deceptively simple: **everything is stored in Git, and the actual running systems are kept in sync with what's in Git**. If you want to change infrastructure — change the code in Git. If you want to deploy a new application version — change the manifest in Git. If you want to update configuration — change the config in Git. The running systems are then automatically (or semi-automatically) reconciled to match. No manual changes are allowed on the live systems — "any manual changes will be absolutely denied." [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

The video explains this is "the final project in this course, and it also consolidates everything we have learned so far." GitOps is not a new isolated tool — it's an **architectural pattern** that integrates source control (Git), CI/CD pipelines (Jenkins/GitHub Actions), infrastructure as code (Terraform), container orchestration (Kubernetes), Helm charts, and continuous delivery (Argo CD) into a unified, automated, auditable system. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## 1.2 — The Problems GitOps Solves

The video systematically identifies the problems that exist without GitOps, establishing why this approach emerged: [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

**Manual deployment is time-consuming and error-prone.** When humans execute deployment steps manually, they make mistakes — wrong configurations, missed steps, inconsistent environments.

**Hard to audit and track.** If both automated pipelines and manual changes are happening on the same infrastructure, it becomes impossible to know who did what: "If I made any change with my automation pipeline or with my automation code and someone is also making manual changes, then it becomes difficult to track who did what." [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

**Not scalable.** Manual processes don't scale with team size. As teams grow, coordination overhead increases, and manual processes become bottlenecks.

**Environment inconsistency.** Without GitOps, it's difficult to replicate one environment into another. Dev might differ from staging, which might differ from production — configuration drift accumulates over time. With GitOps, "you can have dev environment as same as the production environment, at least in terms of configuration. In terms of infrastructure size, it will be definitely different." This is a crucial distinction — GitOps ensures **configuration parity**, not necessarily **scale parity**. Dev doesn't need the same number of servers as production, but it should have the same configuration structure. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## 1.3 — The Four Properties of a GitOps Platform

The video identifies four key properties that define a GitOps platform: [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

**Automated** — Everything is automated. No manual intervention for deployments, configuration changes, or infrastructure modifications. Pipelines detect changes in Git and apply them.

**Auditable** — Everything is in Git, so every change has a commit — who made it, when, what was changed, and why (via commit messages). Git history becomes the complete audit trail for all operational changes.

**Reproducible** — Because everything is defined as code (infrastructure as code, application manifests, Helm charts), any environment can be reproduced from scratch by applying the code. Disaster recovery, environment cloning, and scaling become deterministic operations.

**Kubernetes native** — GitOps is "mostly Kubernetes native." While the principles can apply to any infrastructure, the ecosystem (Argo CD, Helm, Kubernetes manifests) is designed around Kubernetes as the runtime platform. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## 1.4 — The Three Layers of GitOps Management

The video describes GitOps as operating across three distinct layers, each with its own scope, tooling, and Git repository: [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

### Layer 1: Cloud Infrastructure

The foundational layer — your cloud account configuration. This includes users, permissions, IAM policies, organizations, networking, and the Kubernetes cluster itself. All of this is managed through **infrastructure as code** (specifically Terraform in this project) stored in a Git repository. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

The sync mechanism: Terraform code in Git is applied to the cloud infrastructure via a CI/CD pipeline (e.g., GitHub Actions or Jenkins). The pipeline runs `terraform plan` to detect drift — comparing the actual cloud state with the desired state defined in code. If differences exist, `terraform apply` reconciles them. This can include a manual approval trigger for safety. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

The result: "Your Kubernetes cluster configuration stays in sync with the Git repository source code." [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

### Layer 2: Kubernetes Cluster Configuration

On top of the cloud infrastructure sits the Kubernetes cluster. The cluster's internal configuration — namespaces, RBAC, networking policies, storage classes — is also managed through code in Git. Changes to the cluster go through Git, not through manual `kubectl` commands. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

### Layer 3: Application Deployment

On top of the Kubernetes cluster sits the application — in this case, the vProfile application with its ingress, servers, deployments, volumes, and services. This layer is managed by **Argo CD**, which reads Kubernetes manifests (or Helm charts) from a Git repository and ensures the application running in the cluster matches what's defined in Git. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

Argo CD's job: "It will always try to keep this in sync." If someone manually changes something in the cluster (e.g., edits a deployment directly with `kubectl`), Argo CD detects the drift and reverts it to match the Git-defined state. This enforcement is what makes Git the **single source of truth** — not just a suggestion, but an enforced reality. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## 1.5 — Argo CD: The Application Sync Controller

Argo CD is the component that manages the **application layer** of GitOps. It watches a Git repository containing Helm charts or Kubernetes manifests. When changes are detected in the repository, Argo CD applies those changes to the Kubernetes cluster. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

The video describes the workflow: the CI pipeline (which handles source code testing, building, Docker image creation, and registry push) updates the **Helm values file** in the Git repository — specifically, it changes the Docker image tag to the newly built version. Argo CD detects this change in the Helm repository and applies it to the cluster, deploying the new version. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

This is the critical handoff point between **Continuous Integration** (CI) and **Continuous Delivery** (CD): [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

* **CI pipeline** (Jenkins/GitHub Actions): Takes developer source code → tests → builds → creates Docker image → pushes to registry → **updates Helm values file in Git with the new image tag**.
* **Argo CD** (CD controller): Detects the Helm values change in Git → applies the updated Helm chart to Kubernetes → new version is deployed.

The Git repository acts as the **contract boundary** between CI and CD. The CI pipeline never directly touches the cluster — it only modifies Git. Argo CD never builds code — it only reads Git and syncs the cluster. This separation is clean, auditable, and scalable. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

🔍 **Deep Dive:**
This CI-to-CD handoff via Git repository update is architecturally significant. In traditional CI/CD, the pipeline directly deploys to the cluster (e.g., `kubectl apply` at the end of Jenkins pipeline). In GitOps, the pipeline's final step is a **Git commit** — not a deployment action. The deployment is triggered by Argo CD observing the Git change. This means the cluster state is always derivable from Git — you can look at the Git history and know exactly what version was deployed when, by whom, and why. Direct `kubectl` deployments leave no such audit trail. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## 1.6 — The Three-Repository Architecture

The video establishes a standard practice for GitOps project organization: **three separate Git repositories**, each serving a distinct purpose: [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

**Repository 1: Application Source Code** — Contains the developer-written application code (Java source, build files, tests). This is where the CI pipeline reads from. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

**Repository 2: Helm / Argo CD Repository** — Contains Helm charts, Helm values files, and Argo CD application definition files. This is the repository Argo CD watches. The CI pipeline writes to this repository (updating image tags), and Argo CD reads from it (deploying changes). [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

**Repository 3: Infrastructure Repository** — Contains Terraform code and all infrastructure-related configuration. This is where infrastructure CI/CD pipelines read from to manage the cloud account and Kubernetes cluster. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

The video notes: "This is a standard practice. You don't need to put everything in one Git repository." Separation provides clear ownership, independent versioning, independent access control, and clean pipeline boundaries. "It will be more also based on microservice architecture. But for one service, let's say for one Tomcat application, you will have one application source code, one Helm source code, and one infrastructure source code." [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

⚠️ **Expert Note:**
In microservice architectures, the number of repositories multiplies — each microservice may have its own application repo and its own Helm chart, while potentially sharing an infrastructure repo. The three-repository pattern is the minimum unit per service. Organizations with dozens of microservices may have dozens of application repos, a shared or per-service Helm repo, and one or more infrastructure repos. Repository strategy is an architectural decision that affects team workflow, access control, and pipeline design. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## 1.7 — The Technology Stack

The video maps specific tools to each layer of the GitOps architecture for this project: [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

* **Cloud platform:** AWS
* **Kubernetes:** Amazon EKS (managed Kubernetes)
* **Infrastructure as Code:** Terraform
* **CI/CD pipeline:** GitHub Actions (or Jenkins/GitLab — any CI/CD tool works)
* **Container registry:** Docker registry (for built images)
* **Application delivery:** Argo CD
* **Application packaging:** Helm charts
* **Source control:** Git (GitHub)
* **Application:** vProfile (Tomcat-based Java app) [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

This is an **introductory/conceptual lecture** — no commands are executed. The lecture establishes the architectural understanding needed before building the GitOps pipeline in subsequent lectures. The practical value lies in understanding what will be built, why each component exists, and how they connect. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

The final operational outcome of the entire GitOps project (across upcoming lectures):

1. **Infrastructure layer:** Terraform code in a Git repo → CI/CD pipeline → provisions and manages EKS cluster on AWS.
2. **Application CI:** Developer pushes code to application Git repo → CI pipeline tests, builds, creates Docker image, pushes to registry → updates Helm values file in the Helm Git repo with the new image tag.
3. **Application CD:** Argo CD watches the Helm Git repo → detects the image tag change → deploys the new version to the EKS cluster.
4. **Enforcement:** Any manual change to the cluster is detected and reverted by Argo CD to match Git state.
5. **Audit:** Every change to infrastructure, configuration, and application is traceable through Git commit history. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Practical Preparation: Understanding the Repository Structure

Before the next lectures begin hands-on work, understand the three repositories you'll need: [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

| Repository                                                                                                                                                                             | Contains                                           | Used By                      | Written To By                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ---------------------------- | ------------------------------- |
| Application Source Code                                                                                                                                                                | Java source, build files, tests                    | CI pipeline (reads)          | Developers (commit)             |
| Helm / Argo CD                                                                                                                                                                         | Helm charts, values files, Argo CD app definitions | Argo CD (reads)              | CI pipeline (updates image tag) |
| Infrastructure                                                                                                                                                                         | Terraform code, infra config                       | Infra CI/CD pipeline (reads) | DevOps/Platform team (commit)   |
|  [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt) |                                                    |                              |                                 |

***

## Practical Preparation: Understanding the Pipeline Flow

The end-to-end flow that will be built:

```
Developer commits code → Application Repo
    │
    ▼
CI Pipeline (GitHub Actions/Jenkins):
    ├── Fetch source code
    ├── Run tests
    ├── Build application
    ├── Create Docker image
    ├── Push to container registry
    └── Update Helm values file in Helm Repo (new image tag)
            │
            ▼
        Helm/Argo CD Repo (Git commit with new tag)
            │
            ▼
        Argo CD detects change
            │
            ▼
        Argo CD applies updated Helm chart to EKS cluster
            │
            ▼
        New application version running ✅
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

**Separately (infrastructure):**

```
DevOps engineer commits Terraform code → Infrastructure Repo
    │
    ▼
Infra CI/CD Pipeline:
    ├── Terraform plan (detect drift)
    ├── Compare actual cloud state vs. code
    ├── Manual approval (optional)
    └── Terraform apply (reconcile)
            │
            ▼
        EKS cluster + AWS infra in sync with Git ✅
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

⚠️ **Expert Note:**
The architecture diagram and detailed implementation will be covered in the next lecture. This lecture establishes the conceptual framework. Understanding the "why" before the "how" prevents mechanical step-following and builds the engineering reasoning needed to troubleshoot, adapt, and extend the pipeline in real projects. [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    GitOps Pipeline — Introduction
PURPOSE:  Final project consolidating all course learning
CONTEXT:  Conceptual lecture before architecture diagram and implementation
CORE IDEA: "Git repository will be the single source of truth
            for any operational changes"
CLAIM:    "In today's time, a modern DevOps means a GitOps Pipeline"
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## GitOps Definition (One Sentence)

```
Everything (infra + config + app) stored in Git
  + controllers/pipelines keep running systems in sync with Git
  + manual changes denied
  = Git is the single source of truth
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Problems GitOps Solves

```
WITHOUT GITOPS:                     WITH GITOPS:
──────────────                      ────────────
Manual deployment (slow, errors)    Automated
Hard to audit (who did what?)       Auditable (Git commit history)
Not scalable (team growth)          Scalable (code-driven)
Environment drift (dev ≠ prod)      Reproducible (same code = same config)
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Four Properties of GitOps

```
1. Automated     — no manual deployment steps
2. Auditable     — Git history = complete audit trail
3. Reproducible  — code → environment (deterministic)
4. K8s Native    — ecosystem built around Kubernetes
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Three Layers of GitOps Management

```
LAYER 3: APPLICATION
  ├── vProfile app (ingress, deployments, services, volumes)
  ├── Managed by: Argo CD
  ├── Defined in: Helm charts / K8s manifests
  └── Stored in: Helm/Argo CD Git repo

LAYER 2: KUBERNETES CLUSTER
  ├── EKS cluster configuration
  ├── Managed by: Terraform + CI/CD pipeline
  └── Stored in: Infrastructure Git repo

LAYER 1: CLOUD INFRASTRUCTURE
  ├── AWS account (users, IAM, policies, networking)
  ├── Managed by: Terraform + CI/CD pipeline
  └── Stored in: Infrastructure Git repo
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Three-Repository Architecture

```
REPO 1: Application Source Code
  ├── Contains: Java source, build files, tests
  ├── Written by: Developers
  └── Read by: CI pipeline

REPO 2: Helm / Argo CD
  ├── Contains: Helm charts, values files, Argo CD app definitions
  ├── Written by: CI pipeline (image tag updates)
  └── Read by: Argo CD (watches for changes)

REPO 3: Infrastructure
  ├── Contains: Terraform code, infra config
  ├── Written by: DevOps/Platform team
  └── Read by: Infra CI/CD pipeline

"This is a standard practice.
 You don't need to put everything in one Git repository."
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## CI → CD Handoff via Git (Critical Pattern)

```
TRADITIONAL CI/CD:
  CI pipeline → builds → deploys directly to cluster (kubectl apply)
  Problem: No audit trail for deployments

GITOPS CI/CD:
  CI pipeline → builds → commits new image tag to Helm repo (Git commit)
  Argo CD → detects Git change → deploys to cluster
  Benefit: Every deployment is a Git commit (auditable, reversible)

BOUNDARY: CI pipeline NEVER touches cluster directly
          CI pipeline ONLY writes to Git
          Argo CD ONLY reads from Git and syncs cluster
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## End-to-End Pipeline Flow

```
DEVELOPER → commits code → APP REPO
                              │
                              ▼
                        CI PIPELINE
                        ├── Test
                        ├── Build
                        ├── Docker image → REGISTRY
                        └── Update image tag → HELM REPO
                                                  │
                                                  ▼
                                             ARGO CD
                                             ├── Detect change
                                             └── Apply to cluster
                                                  │
                                                  ▼
                                          EKS CLUSTER
                                          └── New version deployed ✅

INFRASTRUCTURE:
  DEVOPS → commits Terraform → INFRA REPO
                                   │
                                   ▼
                             INFRA PIPELINE
                             ├── terraform plan (detect drift)
                             ├── Manual approval (optional)
                             └── terraform apply
                                   │
                                   ▼
                             AWS + EKS in sync ✅
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Technology Stack

```
LAYER              TOOL                    ROLE
─────              ────                    ────
Cloud              AWS                     Infrastructure platform
Kubernetes         Amazon EKS              Container orchestration (managed)
IaC                Terraform               Infrastructure as code
CI/CD              GitHub Actions/Jenkins  Pipeline automation
Registry           Docker registry         Container image storage
App Delivery       Argo CD                 K8s sync controller (CD)
App Packaging      Helm                    K8s manifest templating
Source Control     Git (GitHub)            Single source of truth
Application        vProfile (Tomcat/Java)  The workload being deployed
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Argo CD Role

```
WHAT:    Kubernetes-native continuous delivery controller
WATCHES: Helm/Argo CD Git repository
DETECTS: Changes to Helm charts / values files / manifests
ACTION:  Applies changes to Kubernetes cluster
ENFORCES: Cluster state = Git state (reverts manual changes)
SCOPE:   Application layer only (not infrastructure)

"It will be the job of Argo CD to make sure
 your Helm charts or your Kubernetes manifest
 are in sync with the application that is in the cluster.
 Any manual changes will be absolutely denied."
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Drift Detection Pattern

```
INFRASTRUCTURE DRIFT:
  Terraform plan → compares code vs. actual cloud state
  Drift detected → terraform apply (with optional manual approval)
  Result: Cloud matches Git

APPLICATION DRIFT:
  Argo CD → compares Helm/manifests vs. actual cluster state
  Drift detected → Argo CD auto-applies Git state
  Result: Cluster matches Git

BOTH USE: Desired state (Git) vs. Actual state (running system) comparison
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Environment Parity

```
WITH GITOPS:
  Dev config  = same code  → same configuration
  Prod config = same code  → same configuration
  
  Dev SCALE  ≠ Prod SCALE  → different infrastructure size (OK)
  Dev CONFIG = Prod CONFIG  → same structure and settings (GOAL)

"You can have dev environment as same as the production environment,
 at least in terms of configuration.
 In terms of infrastructure size, it will be definitely different."
```

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## Reusable Engineering Patterns

| Pattern                                     | Manifestation                                                                                          |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Single Source of Truth**                  | Git repository defines desired state — running systems must match it                                   |
| **Desired State Reconciliation**            | Controllers (Argo CD, Terraform) continuously compare desired vs. actual and correct drift             |
| **Git as Contract Boundary**                | CI writes to Git, CD reads from Git — they never interact directly; Git is the handoff point           |
| **Separation of Concerns via Repositories** | App code / Helm charts / Infrastructure code in separate repos — independent ownership and versioning  |
| **No Manual Changes Enforcement**           | Argo CD reverts manual cluster changes — Git authority is enforced, not just suggested                 |
| **Audit Trail by Design**                   | Every change is a Git commit — who, what, when, why are automatically recorded                         |
| **Configuration Parity, Not Scale Parity**  | Same config code for all environments; different sizing parameters                                     |
| **Layered Management**                      | Cloud infra → K8s cluster → Application — each layer managed by appropriate tool with its own Git repo |

 [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

## One-Line System Reconstruction

> **GitOps makes Git the single source of truth by storing infrastructure (Terraform), cluster config, and application manifests (Helm charts) in three separate Git repositories — where CI pipelines handle code→test→build→Docker image→registry→update Helm values in Git (never touching the cluster directly), Argo CD watches the Helm repo and syncs the Kubernetes cluster to match (denying manual changes), Terraform pipelines detect and reconcile infrastructure drift, and every operational change is a Git commit — making the entire system automated, auditable, reproducible, and Kubernetes-native.** [\[361-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/361-introduction.txt)

***

This completes the full reconstruction of the GitOps Pipeline Introduction lecture. It establishes the architectural vision and conceptual framework for the final project — the next lecture will present the detailed architecture diagram showing exactly how all components connect, followed by hands-on implementation of each layer. Let me know if you'd like any section expanded or adjusted! 🚀
