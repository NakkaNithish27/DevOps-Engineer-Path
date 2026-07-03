# 🧠 ArgoCD Application Sync — GitOps Deployment, Repository Registration & Automated Reconciliation

**Source:** *375. Argo App Sync* — GitOps / ArgoCD Series (Video Caption Reconstruction + Setup Reference)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Where We Are in the GitOps Pipeline — ArgoCD as the Deployment Engine

At this point in the GitOps project, three foundational pieces are already in place: the **EKS cluster** (provisioned by Terraform from the `vprofile-infra` repo), the **Helm charts** (in the `vprofile-helm` repo), and the **application container image** (built by the CI pipeline and stored in **Amazon ECR**). ArgoCD has been installed on the EKS cluster. What remains is connecting ArgoCD to the Helm repository and telling it what to deploy — this lecture accomplishes exactly that.

The instructor opens with the architectural flow: *"We have an ArgoCD controller that is going to fetch the Helm charts from this Helm repository. And then when it runs our application pod, the Tomcat vProfile application pod, which is stored in Amazon ECR. So the EKS cluster will be fetching — that docker pull command will get executed."*

Two connectivity requirements emerge from this architecture:

1. **ArgoCD → Git repository** — ArgoCD needs to read the Helm charts from the `vprofile-helm` GitHub repository. This requires SSH-based repository registration.
2. **EKS nodes → Amazon ECR** — When pods start, Kubernetes pulls the container image from ECR. The EKS worker nodes need **IAM permissions** to access ECR.

***

## 1.2 ArgoCD Repository Registration — Connecting to the Helm Source

ArgoCD needs to know where to find the Helm charts. You register a Git repository with ArgoCD, providing the repository URL and the authentication credentials (SSH private key). Once registered, ArgoCD can clone the repository, read the Helm chart, and watch for changes.

The registration can be done two ways:

**Command line:** `argocd repo add git@github.com:<account>/vprofile-helm.git --ssh-private-key-path ~/.ssh/<key-name>` — This uses the same SSH key that was set up during the three-repository creation (§364). The `argocd` CLI tool communicates with the ArgoCD server to store the repository information.

**UI:** Settings → Repositories → Connect Repository → provide URL and paste the private key content. The instructor shows both methods and notes that the UI is an alternative if the CLI has issues.

Before adding the repository, you must log into ArgoCD from the command line: `argocd login <argocd-endpoint> --username admin`. This authenticates your CLI session with the ArgoCD server so subsequent commands are authorized.

The instructor encounters a transient error during repo registration: *"I was trying to troubleshoot, I couldn't find any problem, then I tried that command once again and it just worked."* This is an operational reality — transient failures happen, and retrying is often the first debugging step.

After successful registration, the repository shows as **"Successful connection"** in the ArgoCD UI.

***

## 1.3 EKS Node IAM Policy for ECR Access — The Pull Permission Problem

When a Kubernetes pod starts and specifies an image from Amazon ECR, the kubelet on the worker node needs to authenticate with ECR and pull the image. EKS worker nodes use **IAM roles** for AWS API access. If the node's IAM role doesn't have ECR permissions, image pulls fail with authentication errors.

The solution is to **attach an ECR access policy** to the IAM role that's associated with the EKS node group. The process:

1. **Find the node group name** — Either via `aws eks list-nodegroups` or from the EKS console
2. **Find the IAM role** attached to the node group — Via `aws eks describe-nodegroup` or from the EKS console (Compute → Node Group → Node IAM Role)
3. **Attach the policy** — `aws iam attach-role-policy` with the `AmazonEC2ContainerRegistryFullAccess` (or `ReadOnly`) policy ARN

This is a one-time infrastructure setup step — once the policy is attached, all pods on that node group can pull from ECR.

> 🔍 **Deep Dive:** The IAM role attached to the node group is assumed by every EC2 instance (worker node) in that group. When kubelet needs to pull an image, it uses the instance's IAM credentials (from the instance metadata service) to authenticate with ECR. The `AmazonEC2ContainerRegistryFullAccess` policy grants permissions for `ecr:GetAuthorizationToken`, `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer`, and other operations needed for image pulls. In production, `ReadOnly` is sufficient for pull-only access; `FullAccess` also allows pushing images.

***

## 1.4 ArgoCD Project — Defining Boundaries

ArgoCD organizes applications into **Projects**. A Project defines the **boundaries** for applications within it: which source repositories are allowed, which destination clusters and namespaces are permitted, and which Kubernetes resource types can be created.

The instructor explains the purpose: *"Creating application in ArgoCD is always through project. If you do not define a project, then it is going to use the default project. But if you create your own project, then you can set boundaries."*

The Project manifest (`vprofile-project.yaml`) is a **custom resource** of ArgoCD (not a native Kubernetes resource). It defines:

* **`sourceRepos`** — Which Git repositories this project can pull from (the Helm repository URL)
* **`destinations`** — Which Kubernetes cluster and namespace the applications can deploy to. `https://kubernetes.default.svc` means the **local cluster** — the same cluster where ArgoCD is running. If ArgoCD managed a remote cluster, that cluster's endpoint would go here instead.
* **`clusterResourceWhitelist`** — Which cluster-scoped resources (like Namespaces) can be created
* **`namespaceResourceWhitelist`** — Which namespace-scoped resources can be created (using wildcards `*` allows all types)

The Project is created in the `argocd` namespace — all ArgoCD custom resources live there.

***

## 1.5 ArgoCD Application — The Deployment Definition

The **Application** is the core ArgoCD resource that defines **what to deploy, where to get it, and how to keep it synchronized**. The Application manifest (`vprofile-app.yaml`) specifies:

### Source Configuration

```yaml
source:
  repoURL: git@github.com:<account>/vprofile-helm.git
  targetRevision: main
  path: helm/vprofile
  helm:
    valueFiles:
      - values.yaml
```

* **`repoURL`** — The Git repository containing the Helm chart
* **`targetRevision: main`** — Which branch to track (ArgoCD watches this branch for changes)
* **`path: helm/vprofile`** — The path within the repository where the Helm chart lives. The instructor catches a path error during the lecture: *"The path is wrong. It's helm/vprofile, -chart is not there."* Getting this path exactly right is critical — if it doesn't match the actual folder structure in the repository, ArgoCD can't find the chart.
* **`helm.valueFiles`** — Which `values.yaml` file to use. The instructor highlights the multi-environment implication: *"If you have multiple environments like dev, staging, production, you can define different values.yaml files, and then you can mention the path here. But the charts should be the same — same chart, but values will be different, like more replicas, more resources, more CPU, more RAM, better, faster storage."*

### Destination Configuration

```yaml
destination:
  server: https://kubernetes.default.svc
  namespace: vprofile
```

* **`server`** — The target Kubernetes cluster. `https://kubernetes.default.svc` is the **local cluster** — ArgoCD deploys to the same cluster it runs on. For remote clusters, you'd provide that cluster's API endpoint.
* **`namespace: vprofile`** — The namespace where all resources will be created.

### Sync Policy — The Automation Engine

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
    - CreateNamespace=true
    - ServerSideApply=true
```

This is the most important section — it defines ArgoCD's **automated reconciliation behavior**:

**`prune: true`** — If a resource is **removed** from the Git repository (Helm chart), ArgoCD will **delete** it from the Kubernetes cluster. The instructor explains: *"If anyone deletes a resource from the repository, then it'll delete that resource in the Kubernetes cluster also."* Without pruning, deleted manifests would leave orphaned resources in the cluster.

**`selfHeal: true`** — If someone **manually changes** a resource in the Kubernetes cluster (e.g., editing a deployment directly with `kubectl edit`), ArgoCD detects the drift and **reverts it** to match what's defined in the Git repository. The instructor explains: *"If someone changes something in your application, any resource, then it is going to check that and match it, what is defined in the repository. If it doesn't match, then it is going to apply whatever is mentioned in the repository."* This is the essence of GitOps: **Git is the single source of truth**, and the cluster is always reconciled to match it.

**`CreateNamespace=true`** — If the target namespace (`vprofile`) doesn't exist in the cluster, ArgoCD creates it automatically.

**`ServerSideApply=true`** — Uses Kubernetes server-side apply for resource management (better conflict resolution).

### Finalizers

```yaml
finalizers:
  - resources-finalizer.argocd.argoproj.io
```

This ensures that when the ArgoCD Application is deleted, all the Kubernetes resources it manages are also cleaned up. Without the finalizer, deleting the Application would leave the deployed resources running.

> ⚠️ **Expert Note:** The combination of `prune: true` and `selfHeal: true` makes the Git repository the **absolute authority** over the cluster state. This is powerful but requires discipline: all changes must go through Git, never through `kubectl` directly. Any manual `kubectl` change will be automatically reverted by ArgoCD. This is by design — it enforces the GitOps principle that the desired state lives in Git, and the cluster is just a reflection of it.

***

## 1.6 The CI Pipeline's Effect on the Helm Repository

The instructor mentions a detail that reveals the CI/CD integration: *"Our pipeline has updated the app image name and tag — that happened in the GitHub repository. So we need to fetch the changes to the main branch."* Before creating the ArgoCD manifests, a `git pull` is needed in the Helm repository because the **CI pipeline** (from the `vprofile-app` repo) has already pushed an updated image tag to `values.yaml` in the Helm repo.

This is the GitOps feedback loop: the CI pipeline builds a new image → pushes the image to ECR → updates the image tag in the Helm repository's `values.yaml` → ArgoCD detects the change → ArgoCD syncs the cluster to the new state (deploying the new image).

***

## 1.7 Committing Terraform Code — Infrastructure Repository Hygiene

Before moving to the Helm/ArgoCD work, the instructor commits the Terraform code to the `vprofile-infra` repository. This includes generating a `.gitignore` file (excluding the `.terraform/` directory and log files) and a `README.md` file using GitHub Copilot. The `.terraform/` directory contains downloaded provider plugins and is large — it should never be committed to Git (it's regenerated by `terraform init`).

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are connecting **ArgoCD to the Helm repository** and creating the ArgoCD **Project** and **Application** resources that trigger the automated deployment of the vProfile application on the EKS cluster. We also grant the EKS nodes permission to pull images from Amazon ECR. By the end, ArgoCD is actively syncing the Helm chart to the cluster, and all vProfile resources (deployments, services, PVC, secrets, ingress) are running.

**Final outcome:** ArgoCD Application showing **Healthy** status in the UI, with all vProfile Kubernetes resources created and running in the `vprofile` namespace — automatically synchronized with the Helm repository.

***

## Step 1: Log Into ArgoCD from the Command Line

```bash
argocd login argocd.hkhinfotek.xyz --username admin
```

**Command breakdown:**

* `argocd login` — Authenticates the ArgoCD CLI
* `argocd.hkhinfotek.xyz` — The ArgoCD server endpoint (use **your** endpoint, not the instructor's)
* `--username admin` — The admin user

**Expected:** Prompted for password. Enter the ArgoCD admin password set during installation.

**Expected output:** `'admin:login' logged in successfully`

**Common mistake:** Using the instructor's endpoint instead of your own. The instructor warns: *"Just make sure you are using your endpoint and not mine."*

***

## Step 2: Register the Helm Git Repository with ArgoCD

```bash
argocd repo add git@github.com:<your-account>/vprofile-helm.git --ssh-private-key-path ~/.ssh/<your-key>
```

**Command breakdown:**

* `argocd repo add` — Registers a new Git repository with ArgoCD
* `git@github.com:<account>/vprofile-helm.git` — The SSH URL of the Helm repository
* `--ssh-private-key-path ~/.ssh/<key>` — Path to the SSH private key (the same key used when setting up the three repositories in §364)

**Expected output:** Repository registered successfully.

**If it fails:** The instructor encountered a transient error and resolved it by retrying the same command. If persistent, verify:

* The SSH key is correct and matches the public key on GitHub
* The repository URL is correct (check for typos)
* ArgoCD can reach GitHub (network connectivity)

**Alternative (UI method):** ArgoCD UI → Settings → Repositories → Connect Repository → provide URL + paste private key content.

**Verification:** ArgoCD UI → Settings → Repositories → should show the repository with **"Successful"** connection status.

***

## Step 3: Attach ECR Access Policy to EKS Node Group

### 3a: Find the node group name

```bash
aws eks list-nodegroups --cluster-name vprofile-eks-cluster --region us-east-1
```

**Or:** EKS Console → Cluster → Compute → Node Groups → note the name (e.g., `vprofile-eks-cluster-ng`).

### 3b: Find the IAM role attached to the node group

```bash
aws eks describe-nodegroup \
  --cluster-name vprofile-eks-cluster \
  --nodegroup-name vprofile-eks-cluster-ng \
  --region us-east-1 \
  --query "nodegroup.nodeRole" \
  --output text
```

**Or:** EKS Console → Compute → Node Group → **Node IAM Role** field (e.g., `vprofile-eks-cluster-node-role`).

### 3c: Attach the ECR policy

```bash
aws iam attach-role-policy \
  --role-name vprofile-eks-cluster-node-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
```

**Command breakdown:**

* `aws iam attach-role-policy` — Attaches a managed IAM policy to an IAM role
* `--role-name` — The IAM role name from Step 3b (use **your** role name)
* `--policy-arn` — The ARN of the `AmazonEC2ContainerRegistryFullAccess` policy

### 3d: Verify the policy is attached

```bash
aws iam list-attached-role-policies \
  --role-name vprofile-eks-cluster-node-role \
  --output table
```

**Expected:** The table includes `AmazonEC2ContainerRegistryFullAccess`.

**Connection to flow:** EKS nodes can now pull container images from ECR. Without this, pods referencing ECR images would fail with `ImagePullBackOff`.

***

## Step 4: Commit Terraform Code to Infrastructure Repository

```bash
cd ~/Desktop/gitops/vprofile-infra
git add .
git commit -m "terraform code"
git push origin main
```

Before committing, generate `.gitignore` and `README.md` using GitHub Copilot (to exclude `.terraform/` directory and log files).

***

## Step 5: Pull Latest Changes in the Helm Repository

```bash
cd ~/Desktop/gitops/vprofile-helm
git pull
```

**Why:** The CI pipeline has updated the image tag in `values.yaml`. You need the latest version before adding ArgoCD manifests.

**Alternative in VS Code:** Source Control → Sync Changes.

***

## Step 6: Create ArgoCD Project Manifest

Create the folder structure:

```bash
mkdir -p argocd/projects argocd/apps
```

Create the project file:

```bash
vim argocd/projects/vprofile-project.yaml
```

**Contents:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: vprofile
  namespace: argocd
spec:
  description: vProfile application project
  sourceRepos:
    - git@github.com:<your-account>/vprofile-helm.git
  destinations:
    - namespace: vprofile
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - group: ""
      kind: Namespace
  namespaceResourceWhitelist:
    - group: "*"
      kind: "*"
```

**Key fields to customize:** `sourceRepos` must contain **your** Helm repository SSH URL.

**`server: https://kubernetes.default.svc`** means the local cluster — ArgoCD deploys to the same cluster it runs on.

***

## Step 7: Create ArgoCD Application Manifest

```bash
vim argocd/apps/vprofile-app.yaml
```

**Contents:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: vprofile
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: vprofile
  source:
    repoURL: git@github.com:<your-account>/vprofile-helm.git
    targetRevision: main
    path: helm/vprofile
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: vprofile
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
```

**Critical field — `path`:** Must match the actual folder structure in the Helm repository. The instructor catches an error: the path was `helm/vprofile-chart` but the actual folder is `helm/vprofile`. Verify: `ls helm/` in the repo — inside you should see `Chart.yaml` and `values.yaml`.

**Fields to customize:** `repoURL` (your Helm repo SSH URL).

***

## Step 8: Apply the Project and Application

```bash
kubectl apply -f argocd/projects/vprofile-project.yaml
```

**Expected:** `appproject.argoproj.io/vprofile created`

```bash
kubectl apply -f argocd/apps/vprofile-app.yaml
```

**Expected:** `application.argoproj.io/vprofile created`

**Order matters:** Project must be created before the Application (the Application references the project by name).

***

## Step 9: Verify in ArgoCD UI

Navigate to the ArgoCD UI in the browser.

**Check Projects:** Settings → Projects → `vprofile` should be listed.

**Check Application:** Applications → `vprofile` should appear.

**Expected state progression:** `Progressing` → resources appearing (db-pv-claim, app-secret, deployments, services) → `Healthy` + `Synced`.

**If the path was wrong:** The application shows `Unknown` or error status. The instructor had to delete and recreate the Application after fixing the path:

```bash
kubectl delete -f argocd/apps/vprofile-app.yaml
# Fix the path in the YAML file, save
kubectl apply -f argocd/apps/vprofile-app.yaml
```

**Final expected state:** All resources visible in the ArgoCD UI — deployments, services, PVC, secrets, ingress — all **Healthy** and **Synced**.

> ⚠️ **Expert Note:** If pods show `ImagePullBackOff`, the ECR IAM policy (Step 3) may not have been attached correctly. Verify with `kubectl describe pod <pod-name>` — look for ECR authentication errors in the events. If the Helm chart path is wrong, ArgoCD shows a clear error in the Application status — always check the `path` field first.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Two Connectivity Requirements

```
1. ArgoCD → Git (Helm repo)
     Register repo: argocd repo add <SSH-URL> --ssh-private-key-path <key>
     ArgoCD clones repo → reads Helm charts → watches for changes

2. EKS Nodes → ECR (container images)
     Attach IAM policy: AmazonEC2ContainerRegistryFullAccess
     → to the IAM role of the EKS node group
     → enables docker pull from ECR
```

***

## ArgoCD Login + Repo Registration

```bash
# Login
argocd login <endpoint> --username admin   → enter password

# Add repo
argocd repo add git@github.com:<acct>/vprofile-helm.git \
  --ssh-private-key-path ~/.ssh/<key>

# Verify: ArgoCD UI → Settings → Repositories → "Successful"

# Alternative: UI → Settings → Repositories → Connect → paste URL + key
```

***

## ECR Access — IAM Policy Chain

```
EKS Cluster
  └── Node Group (vprofile-eks-cluster-ng)
        └── IAM Role (vprofile-eks-cluster-node-role)
              └── ATTACH: AmazonEC2ContainerRegistryFullAccess

COMMANDS:
  aws eks list-nodegroups --cluster-name <name> --region <region>
  aws eks describe-nodegroup ... --query "nodegroup.nodeRole"
  aws iam attach-role-policy --role-name <role> --policy-arn <ecr-policy>
  aws iam list-attached-role-policies --role-name <role>   ← verify
```

***

## ArgoCD Resource Hierarchy

```
AppProject (vprofile-project.yaml)
  ├── defines BOUNDARIES:
  │     ├── sourceRepos: [vprofile-helm.git]
  │     ├── destinations: [namespace: vprofile, server: local]
  │     ├── clusterResourceWhitelist: [Namespace]
  │     └── namespaceResourceWhitelist: [*/*]
  │
  └── Application (vprofile-app.yaml)
        ├── project: vprofile
        ├── source:
        │     ├── repoURL: vprofile-helm.git
        │     ├── targetRevision: main
        │     ├── path: helm/vprofile        ⚠️ MUST match actual folder
        │     └── helm.valueFiles: [values.yaml]
        ├── destination:
        │     ├── server: https://kubernetes.default.svc  (= local cluster)
        │     └── namespace: vprofile
        ├── syncPolicy:
        │     ├── automated:
        │     │     ├── prune: true     → delete removed resources
        │     │     └── selfHeal: true  → revert manual changes
        │     └── syncOptions:
        │           ├── CreateNamespace=true
        │           └── ServerSideApply=true
        └── finalizers: [resources-finalizer]  → cleanup on delete
```

***

## Sync Policy Behavior

```
prune: true
  Git removes resource → ArgoCD DELETES it from cluster
  Git is authoritative for what EXISTS

selfHeal: true
  kubectl edit changes resource → ArgoCD REVERTS to Git state
  Git is authoritative for what resources LOOK LIKE

CreateNamespace: true
  Namespace "vprofile" doesn't exist → ArgoCD CREATES it

COMBINED EFFECT:
  Git = single source of truth
  Cluster = always matches Git
  Manual changes = automatically reverted
```

***

## Multi-Environment Pattern (Mentioned)

```
SAME chart, DIFFERENT values:
  helm/vprofile/
    ├── Chart.yaml
    ├── templates/
    ├── values.yaml          ← dev defaults
    ├── values-staging.yaml  ← staging overrides
    └── values-prod.yaml     ← prod overrides

ArgoCD Application for each env:
  dev-app:  helm.valueFiles: [values.yaml]
  stg-app:  helm.valueFiles: [values-staging.yaml]
  prod-app: helm.valueFiles: [values-prod.yaml]

"Same chart, but values will be different —
 more replicas, more resources, more CPU, more RAM"
```

***

## Complete GitOps Data Flow

```
Developer pushes code → vprofile-app repo
  │
  ├── CI Pipeline triggers
  │     ├── Builds Docker image
  │     ├── Pushes to Amazon ECR
  │     └── Updates image tag in vprofile-helm repo (values.yaml)
  │
  ├── ArgoCD detects change in vprofile-helm (main branch)
  │     ├── Reads Helm chart from helm/vprofile/
  │     ├── Renders templates with values.yaml
  │     ├── Compares desired state vs. cluster state
  │     └── Syncs: applies changes to EKS cluster
  │
  └── EKS cluster pulls new image from ECR
        └── Pods start with new version
```

***

## Apply Order

```
1. kubectl apply -f argocd/projects/vprofile-project.yaml
     → creates Project (boundaries)

2. kubectl apply -f argocd/apps/vprofile-app.yaml
     → creates Application (deployment spec)
     → ArgoCD immediately starts syncing

ORDER MATTERS: Project must exist before Application references it
```

***

## Folder Structure in Helm Repo

```
vprofile-helm/
├── helm/
│   └── vprofile/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── app-deployment.yaml
│           ├── db-deployment.yaml
│           ├── ...
├── argocd/
│   ├── projects/
│   │   └── vprofile-project.yaml
│   └── apps/
│       └── vprofile-app.yaml
└── kubedefs/ (original plain manifests, reference only)
```

***

## Failure Signatures

```
Application status "Unknown"          → path field doesn't match actual folder
ImagePullBackOff on pods              → ECR IAM policy not attached to node role
Repo connection failed in ArgoCD      → wrong SSH key or URL; retry or use UI method
Application won't create              → Project doesn't exist yet; apply project first
Resources not pruning                 → prune: false or sync not automated
Manual kubectl changes persist        → selfHeal: false
Namespace doesn't exist error         → CreateNamespace not set to true
```

***

## Reusable Engineering Pattern: Declarative Desired-State Reconciliation

```
PATTERN:
  1. DECLARE desired state in a versioned repository (Git)
  2. CONTROLLER continuously compares desired state vs. actual state
  3. RECONCILE: automatically apply/revert/prune to match desired state

COMPONENTS:
  Source of truth:    Git repository (Helm charts)
  Controller:        ArgoCD Application controller
  Target system:     Kubernetes cluster
  Sync mechanism:    automated sync with prune + selfHeal

PROPERTIES:
  prune: true     → deletions in Git = deletions in cluster
  selfHeal: true  → manual drift = automatically corrected
  Boundary:       Project defines allowed repos, namespaces, resource types
  Multi-env:      Same chart + different values.yaml per environment

WHERE ELSE:
  • Terraform state reconciliation (plan + apply)
  • Flux CD (alternative GitOps controller, same pattern)
  • AWS CloudFormation drift detection
  • Ansible desired-state playbooks with --check
  • Any system where "declared intent" drives "actual state"

CORE PRINCIPLE:
  "Git is the single source of truth.
   The cluster is just a reflection of it."
```

***

## One-Line Mental Reload Trigger

> *"Login to ArgoCD CLI → register Helm repo with SSH key → attach ECR IAM policy to EKS node role → create AppProject (boundaries: repo + namespace + cluster) → create Application (source: helm/vprofile on main, destination: local cluster/vprofile namespace, syncPolicy: automated prune+selfHeal+CreateNamespace) → kubectl apply project then app → ArgoCD syncs all resources automatically, Git is single source of truth."*

This single sentence reconstructs both connectivity requirements, the two ArgoCD custom resources with their key fields, the apply order, the sync policy behavior, and the fundamental GitOps principle. [\[375-argo-app-sync \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/375-argo-app-sync.txt), [\[375.ArgoVp...leAppSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/375.ArgoVprofileAppSetup.txt)
