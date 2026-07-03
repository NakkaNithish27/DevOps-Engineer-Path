# 🎓 Deep Learning Material: Course Summary — Self-Assigned Tasks, Cleanup Procedure, and the Complete GitOps Maturity Path

**Source:** Video lecture on final summary, tasks, and cleanup (from [377-summary.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt?EntityRepresentationId=dca4f77b-6bd2-4b67-865e-b87d36c20f4e) caption file) [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Video Context:** This is the **absolute final lecture** of the entire course. The instructor does three things: **(1)** assigns three self-study tasks that extend the pipeline to production-grade maturity (PR-based Helm updates instead of direct commits, a Terraform CI/CD pipeline with manual apply approval, and Slack notifications for all pipelines), **(2)** walks through the complete cleanup procedure in reverse dependency order (ingress deletion → load balancer removal → IAM service account deletion → Terraform destroy), and **(3)** provides learning advice — repeat the project multiple times, create your own documentation, use AI code assistants for troubleshooting, and only declare the course complete when comfortable with every step. This lecture bridges the gap between "course project" and "production-ready system" by clearly articulating what's missing and assigning the learner to close those gaps.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Syncing Local and Remote Repositories Before Starting

The instructor begins with a practical but conceptually important step: ensuring local repositories match the remote state. Since the CI pipeline merged changes to `main` on GitHub (remote), the local clone may be behind. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

```bash
git pull
```

The instructor runs this on both `vprofile-app` and `vprofile-helm` repositories. If there are conflicts (local changes conflicting with remote changes), the instructor recommends the simplest approach: *"Just delete the repository and clone it once again."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

This reflects a pragmatic DevOps principle: when the authoritative source is the remote repository and local state is disposable, re-cloning is faster and safer than resolving merge conflicts in a learning environment.

***

## 1.2 — Task 1: PR-Based Helm Updates (Production Approval Flow)

The current pipeline directly updates `values.yaml` in the Helm repository and commits. In production, this is too dangerous — any merge to `main` in the app repo automatically triggers a deployment with no human approval. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

The instructor explains the production-grade approach: *"Instead of updating the image tag directly in the values.yaml file, you raise a pull request from here to update the values.yaml file. So not a direct change, a pull request."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Current flow:** Pipeline → direct commit to Helm repo → ArgoCD auto-deploys
**Target flow:** Pipeline → creates PR in Helm repo → human reviews and approves PR → ArgoCD deploys after merge

This adds a **human approval gate** between CI (build/test/push) and CD (deploy). The pipeline still automates everything up to the PR creation, but the actual deployment requires a human to approve the PR in the Helm repository. The instructor states: *"This should happen with an approval. The Argo should pull the changes based on the approval."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

The task requires modifying the `update-helm` job in the `ci.yml` pipeline to create a PR instead of directly committing. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## 1.3 — Task 2: Terraform CI/CD Pipeline (Infrastructure as Code Pipeline)

The second task extends the CI/CD pattern to **infrastructure code** — the `vprofile-infra` Terraform repository needs its own GitHub Actions pipeline with a specific behavior: [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**On new branch creation:** `terraform validate` + `terraform plan` (check syntax and preview changes)

**On pull request:** `terraform validate` + `terraform plan` (same — verify before merge)

**On merge to main:** **Do NOT auto-apply.** Instead, show a **manual approval button**. Only when clicked, `terraform apply` runs and modifies the EKS cluster. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

The instructor is explicit about the manual gate: *"It should not apply automatically. There should be a manual button where you click on apply and then you should apply the changes to EKS cluster. That means Terraform apply will run only when you click a button manually."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Drift detection (advanced, optional):** The pipeline should also periodically check the actual EKS cluster state against the Terraform code. If there's drift (someone changed something manually), the pipeline should notify and offer the apply button. *"It should also keep checking your code against the EKS cluster. If there is any changes, then it should give you again the apply button."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## 1.4 — Task 3: Slack Notifications for All Pipelines

Both the app pipeline and the Terraform pipeline should send Slack notifications for every change. The `SLACK_WEBHOOK` secret was already created in previous lectures. The task is to integrate Slack notification steps into both pipelines. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## 1.5 — The AI-Assisted Development Approach

The instructor explicitly directs learners to use AI code assistants for these tasks: *"You have to achieve all this by using prompt on GitHub Copilot, Amazon Q or whatever code assistance you are using. You create the prompt. As I'm speaking you speak to the GitHub Copilot or any code assistance and make sure it is fulfilled. And troubleshoot, when you get the issue, that's how you are going to learn."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

This is a deliberate pedagogical choice — the instructor doesn't provide the solution code. The learning comes from **prompting, testing, failing, debugging, and iterating** with AI assistance. This mirrors real-world DevOps work where engineers use AI tools to generate pipeline code and then validate and fix it.

***

## 1.6 — Cleanup: Reverse Dependency Order

The cleanup must follow a specific order to avoid orphaned resources and failed deletions. The instructor explains the reasoning behind each step: [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Why delete ingress before the cluster:** The ingress controller creates AWS load balancers. If you destroy the cluster (via Terraform) without deleting the ingress first, the load balancers become orphaned — they still exist in AWS, costing money, but nothing manages them. Worse, Terraform destroy may fail because it can't clean up resources it doesn't know about. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Why delete the IAM service account:** The AWS Load Balancer Controller uses an IAM service account created with `eksctl`. This must be explicitly deleted before the cluster is destroyed. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Why Terraform destroy is last:** Terraform manages the EKS cluster and its foundational infrastructure. Everything running on the cluster (pods, services, ingress) must be cleaned first, then Terraform can safely destroy the underlying infrastructure. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## 1.7 — The Rapid Rebuild Pattern

The instructor reveals a powerful operational insight for practicing: you don't need to repeat the entire setup process each time. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

*"You just need to run terraform apply. You don't need to go through the whole process of generating the prompt and generating the code EKS et cetera. We don't need to do all those things. You can run terraform apply, and from there you can start following. You can continue from this step, eksctl create... So you don't need to do anything, just terraform apply and then start following steps from here till the end and you get the same setup."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Rebuild shortcut:** `terraform apply` → creates EKS cluster → then follow from the `eksctl create iamserviceaccount` step onward. The IAM policy already exists from the first run, so it doesn't need to be recreated. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing and Why

We are performing the **complete project cleanup** — removing all Kubernetes resources, AWS load balancers, IAM service accounts, and the EKS cluster via Terraform destroy. The final outcome: a clean AWS account with no running resources and no ongoing costs, with the knowledge that everything can be rebuilt with `terraform apply` and a few follow-on commands.

***

## Step 0: Sync Local Repositories

```bash
cd vprofile-app
git pull

cd ../vprofile-helm
git pull
```

If conflicts appear: delete the local repo and `git clone` again. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## Step 1: Delete DNS Records

Remove entries from your domain registrar (GoDaddy or equivalent) for: [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

* ArgoCD domain record
* vProfile application domain record

***

## Step 2: Handle the SonarQube Server

**Recommended:** Stop (don't delete) the SonarQube EC2 instance — it's quick to restart for future practice. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

*"If you have no plan of repeating this again, you can delete the SonarQube server, but I recommend you just stop it and keep it."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## Step 3: Delete the vProfile Ingress

**First, verify the load balancers:**
Check AWS Console → EC2 → Load Balancers in your region. You should see **two load balancers** — one for vProfile, one for ArgoCD. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Delete vProfile ingress:**

```bash
kubectl delete ingress vpro-ingress -n vprofile
```

* `delete ingress` — removes the ingress resource
* `vpro-ingress` — the ingress name (default from the project)
* `-n vprofile` — the namespace [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**What happens:** Deleting the ingress triggers the ingress controller to remove the associated AWS load balancer. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## Step 4: Delete the ArgoCD Ingress

```bash
kubectl delete ingress argocd-ingress -n argocd
```

* `argocd-ingress` — the ArgoCD ingress name
* `-n argocd` — the ArgoCD namespace [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Fallback:** If for some reason the ingress deletion doesn't remove the load balancer, delete the load balancer manually from the AWS Console. *"Just make sure you delete the load balancer manually from the AWS console, but you have to delete it, otherwise Terraform destroy will also fail."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## Step 5: Delete the IAM Service Account

The AWS Load Balancer Controller's IAM service account was created with `eksctl create iamserviceaccount`. Delete it with the corresponding delete command: [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

```bash
eksctl delete iamserviceaccount --cluster=<cluster-name> --namespace=kube-system --name=aws-load-balancer-controller
```

* `delete iamserviceaccount` — removes the IAM service account (replaces `create` from the setup)
* `--cluster` — your EKS cluster name
* `--namespace=kube-system` — the namespace where the controller runs
* `--name=aws-load-balancer-controller` — the service account name [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**Important:** Do NOT include `--attach-policy-arn` in the delete command — only the cluster, namespace, and name are needed. The instructor catches this mistake: *"I think I should remove this attached policy also. This is wrong. Yeah, only this much."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**This takes some time.** [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## Step 6: (Optional) Delete the IAM Policy

The IAM policy created for the load balancer controller can be deleted from the AWS Console or CLI. The instructor notes it's not critical: *"Policy is not going to create any harm."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## Step 7: Destroy the EKS Cluster with Terraform

```bash
cd vprofile-infra
terraform init
terraform destroy
```

* `terraform init` — reinitializes the Terraform state (the instructor runs this as a precaution after making code changes)
* `terraform destroy` — destroys all infrastructure managed by Terraform (EKS cluster, VPC, subnets, security groups, node groups, etc.) [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

Confirm with `yes` when prompted. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

**This takes a significant amount of time** — Terraform must delete the EKS cluster, all node groups, networking, and IAM resources. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

## Rapid Rebuild Path (For Practice Repetition)

When you want to practice again, you don't need to regenerate the Terraform code or repeat the full setup: [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

```bash
cd vprofile-infra
terraform apply          # recreates EKS cluster
```

Then continue from the `eksctl create iamserviceaccount` step onward. The IAM policy already exists from the first run. Follow all subsequent steps (load balancer controller, ArgoCD, app deployment) to get the complete setup running again. [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

*"Every time it'll work. I have tested it multiple times."* [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Three Self-Assigned Tasks

```
TASK 1: PR-Based Helm Updates
  CURRENT: pipeline → direct commit to Helm repo → auto-deploy
  TARGET:  pipeline → create PR in Helm repo → human approves → deploy
  WHY:     production needs approval gate before deployment
  MODIFY:  update-helm job in ci.yml → create PR instead of commit

TASK 2: Terraform CI/CD Pipeline
  NEW BRANCH:      validate + plan
  PULL REQUEST:    validate + plan
  MERGE TO MAIN:   manual apply button (NOT auto-apply)
  ADVANCED:        drift detection (check cluster vs code)
  REPO:            vprofile-infra

TASK 3: Slack Notifications
  ADD TO:  both app pipeline and Terraform pipeline
  USE:     existing SLACK_WEBHOOK secret
```

***

## 🔷 Cleanup Sequence (MUST Follow This Order)

```
1. Remove DNS records (domain registrar)
2. Stop SonarQube EC2 (don't delete, keep for reuse)
3. kubectl delete ingress vpro-ingress -n vprofile
     → removes vProfile load balancer
4. kubectl delete ingress argocd-ingress -n argocd
     → removes ArgoCD load balancer
5. Verify: both LBs gone from AWS Console
     → if not, delete manually
6. eksctl delete iamserviceaccount \
     --cluster=<name> --namespace=kube-system \
     --name=aws-load-balancer-controller
7. (Optional) Delete IAM policy from console
8. cd vprofile-infra && terraform init && terraform destroy
     → removes EKS cluster + all infrastructure

ORDER RATIONALE:
  Ingress BEFORE cluster → prevent orphaned load balancers
  Service account BEFORE cluster → clean IAM associations
  Terraform destroy LAST → it manages the base infrastructure
```

***

## 🔷 Rapid Rebuild Path

```
FULL SETUP (first time):
  Generate Terraform code → terraform apply → eksctl create → 
  install LB controller → install ArgoCD → deploy app → configure pipeline

RAPID REBUILD (practice repetition):
  terraform apply → start from "eksctl create iamserviceaccount" → 
  follow all steps → complete setup

  IAM policy: already exists (skip creation)
  Terraform code: already exists (skip generation)
  Secrets/Variables: already configured (skip if repo not deleted)

"You just need to run terraform apply...
 and then start following steps from here till the end"
```

***

## 🔷 Production vs. Course Pipeline

```
FEATURE              COURSE PIPELINE           PRODUCTION PIPELINE
────────             ──────────────            ───────────────────
Helm update          Direct commit             Pull request + approval
Terraform apply      Manual CLI                Pipeline with manual button
Drift detection      Not implemented           Automated periodic check
Slack notifications  Partially set up          All pipelines notify
Approval gates       Quality gate only         Quality gate + deploy approval
```

***

## 🔷 eksctl Delete vs. Create

```bash
# CREATE (setup):
eksctl create iamserviceaccount \
  --cluster=<name> --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=<arn>

# DELETE (cleanup):
eksctl delete iamserviceaccount \
  --cluster=<name> --namespace=kube-system \
  --name=aws-load-balancer-controller

⚠️ DELETE does NOT include --attach-policy-arn
   Only: cluster + namespace + name
```

***

## 🔷 Learning Advice (Instructor's Recommendations)

```
1. REPEAT the project multiple times (2-3x minimum)
2. CREATE your own documentation (not just use provided)
3. USE AI assistants (Copilot, Amazon Q) for the tasks
4. TROUBLESHOOT failures yourself → that's where learning happens
5. IDENTIFY basics gaps (Linux, YAML, K8s, Helm) and fix them
6. ONLY declare course complete when comfortable with everything

"This is a pure gold mine, trust me."
"You will sound professional and confident after this."

INTERVIEW PREP:
  → Draw architecture diagrams
  → Explain the complete flow
  → Discuss trade-offs (auto-deploy vs approval)
  → Demonstrate understanding of each component's role
```

***

## 🔷 Complete Project Architecture (Final Course View)

```
DEVELOPER
  │
  ├── push feature branch → nothing
  ├── PR to main → quality gate (SonarQube)
  └── merge to main → build + push to ECR + update Helm repo
                                                    │
                                                    ▼
                                              ARGOCD (watches Helm repo)
                                                    │
                                                    ▼
                                              EKS CLUSTER
                                                    │
                                    ┌───────────────┼───────────────┐
                                    │               │               │
                                vProfile App    Backend Services   Ingress
                                (Tomcat pods)   (DB, Cache, MQ)    (ALB)
                                    │               │               │
                                    └───────────────┼───────────────┘
                                                    │
                                              USERS (via domain)

INFRASTRUCTURE:
  Terraform (vprofile-infra) → EKS cluster + VPC + networking
  
SUPPORTING SERVICES:
  SonarQube (EC2) → code quality
  ECR (AWS) → Docker image registry
  Slack → notifications
  GitHub Secrets → credentials
  Route 53 → DNS
```

***

## 🔷 Reusable Engineering Pattern: Maturity Levels of CI/CD

```
LEVEL 1 (Course Default):
  Code → auto-build → auto-push → auto-deploy
  Fast, simple, NO approval gates
  RISK: bad code reaches production automatically

LEVEL 2 (Task 1 — Helm PR):
  Code → auto-build → auto-push → PR for deploy → human approves
  Adds deployment approval gate
  RISK: infrastructure changes still manual

LEVEL 3 (Task 2 — Terraform Pipeline):
  Infrastructure changes → validate → plan → manual apply
  Adds infrastructure change control
  RISK: no drift detection

LEVEL 4 (Task 2 Advanced — Drift Detection):
  Pipeline periodically checks cluster vs code
  Detects manual changes → alerts → offers apply
  RISK: minimal — full automation with human gates

LEVEL 5 (Full Production):
  All pipelines + Slack notifications + approval gates
  + drift detection + RBAC + audit trails
  = Complete GitOps maturity

EACH LEVEL ADDS:
  More safety gates
  More automation
  More visibility
  Less human error risk

The course teaches Level 1.
The tasks push you to Level 3-4.
Production requires Level 5.
```

This final lecture's core message: the course gave you a working system, but a **production-ready** system requires additional safety layers — approval gates for deployments, controlled infrastructure changes, drift detection, and comprehensive notifications. The three assigned tasks are the bridge between "it works" and "it's production-grade." [\[377-summary \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/377-summary.txt)
