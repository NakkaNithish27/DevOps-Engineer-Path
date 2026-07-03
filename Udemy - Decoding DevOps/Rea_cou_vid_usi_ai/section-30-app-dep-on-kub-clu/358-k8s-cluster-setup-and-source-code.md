# 🧠 Kubernetes Cluster Setup & Source Code — kOps Cluster Creation, GitHub Repository & Project File Structure

**Source:** *358. K8s Cluster Setup and Source Code* — Kubernetes vProfile Project Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Purpose of This Lecture — Bridging Architecture to Execution

This lecture is the operational bridge between the architecture lecture (§348, where the blueprint was established — 11 manifests, deployments, services, PVC, secret, ingress) and the actual manifest creation. Two things happen here: the Kubernetes cluster is brought up (or re-created) using kOps, and the project's source code — specifically the Kubernetes definition files — is pushed to a GitHub repository and cloned onto the kOps instance where `kubectl` commands will be run.

No new Kubernetes concepts are introduced. The lecture is about **operational setup** — getting the infrastructure and the code in place so the manifest-by-manifest deployment can begin.

***

## 1.2 Three Entry Points for Learners

The instructor identifies three possible starting states for learners, and provides a path for each:

**State 1: Cluster never created.** Go back to the kOps setup lectures, follow the full prerequisite chain (AWS access keys, Route 53 hosted zone, S3 bucket, kOps EC2 instance), and create the cluster from scratch.

**State 2: Cluster previously created and deleted, but prerequisites exist.** The kOps EC2 instance is still there, the hosted zone is configured, the S3 bucket exists. Simply power on the kOps instance, SSH in, and re-run the `kops create cluster` and `kops update cluster` commands to bring the cluster back up.

**State 3: Just watching.** If you don't want to set up a cluster, you can follow along by watching. The definition files and their execution are the same regardless.

The instructor follows **State 2** — the prerequisites exist, the cluster was previously deleted, and it's being recreated.

***

## 1.3 kOps Prerequisites — What Must Already Exist

The instructor lists the prerequisites that must be in place before running the kOps cluster creation command. These were set up in earlier lectures and are referenced here as a checklist:

* **AWS Access Key** stored on the kOps EC2 instance (so kOps can call AWS APIs)
* **Route 53 Hosted Zone** created (the DNS zone where kOps registers the cluster's API server DNS record)
* **DNS name records** stored (the cluster name corresponds to a subdomain of the hosted zone)
* **S3 Bucket** for kOps state storage (kOps stores the cluster configuration in S3, which is how it knows what the cluster should look like)
* **kOps EC2 Instance** running (the machine from which cluster operations are performed)
* **kubectl** installed on the kOps instance (or on the laptop with the kubeconfig, as covered in §328)

These prerequisites are not re-explained — the instructor assumes they were done previously. The only action needed is to verify they exist and power on the kOps instance.

***

## 1.4 What the Project Needs on the kOps Instance — Only the kubedefs Folder

A critical insight emerges during the file upload process: **the Kubernetes project does not need the application source code**. The instructor states: *"Frankly, that's all we need for this project setup. It's going to fetch all the images from Docker Hub. We really don't need the source code. We are not doing any build or anything over here."*

This is an important architectural understanding. In the Containerization project, Docker images were built from source code. Those images were pushed to Docker Hub (or a registry). The Kubernetes project **consumes those pre-built images** — it doesn't build anything. The manifests (definition files) reference image names on Docker Hub, and Kubernetes pulls them at pod creation time.

Therefore, the only files needed on the kOps instance are:

* **`kubedefs/`** — The folder containing all Kubernetes definition files (manifests). This is the primary requirement.
* **Docker-related files** (Dockerfiles, docker-compose.yml) — Optional, uploaded for reference only. Not needed for the Kubernetes deployment.
* **`src/`** (source code) — Not needed at all. The instructor doesn't upload it successfully (GitHub's file limit blocks it) and confirms it's unnecessary.

This separation — images are built elsewhere, Kubernetes only deploys pre-built images — is the standard production pattern. The build pipeline (CI) produces images. The deployment pipeline (CD) applies Kubernetes manifests. They are decoupled.

***

## 1.5 GitHub as the Repository — Why and How

The definition files are pushed to a **GitHub repository** so they can be:

1. **Version-controlled** — Track changes to manifests over time
2. **Cloned onto the kOps instance** — Pull the files where `kubectl` will be run
3. **Shared and portable** — Anyone with the repo URL can clone and use them

The instructor creates a **public repository** (named `vprokube`) and uploads files via the GitHub web interface (drag and drop) rather than using SSH-based git push. This is a convenience choice for the lecture — in production, you'd use `git push` from a local clone.

GitHub has a **file upload limit** — fewer than 100 files at a time. When the instructor tries to upload everything (including `src/` which has many files), it's rejected. This naturally leads to the realization that only the `kubedefs/` folder is needed.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are setting up two things: (1) recreating the **Kubernetes cluster** using kOps, and (2) getting the **Kubernetes definition files** onto the kOps instance via a GitHub repository. By the end, the cluster is running and the manifests are ready to be applied one by one in subsequent lectures.

**Final outcome:** A running Kubernetes cluster (master + worker nodes) accessible via `kubectl` from the kOps instance, with the `kubedefs/` folder cloned locally containing all 11+ manifest files needed for the vProfile deployment.

***

## Step 1: Power On and Log Into the kOps Instance

The kOps EC2 instance should already exist from earlier lectures. Power it on in the AWS console if it was stopped.

Copy the **public IP** from the EC2 console (remember: the IP changes every time you stop/start the instance — see §253).

```bash
ssh -i <key-path> ubuntu@<kops-public-ip>
```

Switch to root:

```bash
sudo -i
```

Clear the screen:

```bash
clear
```

**Verification:** You should be logged into the kOps instance as root.

***

## Step 2: Verify Prerequisites Exist

Before creating the cluster, confirm the prerequisites are in place:

* **AWS access key:** Should already be configured (`~/.aws/credentials` or environment variables). kOps needs this to call AWS APIs.
* **Route 53 hosted zone:** Should exist in the AWS console with the correct domain.
* **S3 bucket:** Should exist (kOps stores cluster state here).
* **DNS records:** The cluster name should match a subdomain of the hosted zone.

If any of these are missing, refer back to the kOps setup lectures. The instructor assumes they're already configured.

***

## Step 3: Create the Kubernetes Cluster

Run the kOps cluster creation command:

```bash
kops create cluster <cluster-creation-options>
```

The exact flags (cluster name, zones, node count, node size, master size, DNS zone, state store) were specified in the kOps setup lecture. The instructor runs this command without re-explaining each flag — it's the same command used previously.

Then apply the cluster configuration to actually provision the infrastructure:

```bash
kops update cluster <cluster-name> --state=s3://<bucket-name> --yes --admin
```

**Command breakdown:**

* `kops update cluster` — Applies the cluster configuration, creating actual AWS resources (EC2 instances for master and worker nodes, security groups, auto scaling groups, etc.)
* `<cluster-name>` — The full DNS name of the cluster (e.g., `kubevpro.groophy.in`)
* `--state=s3://<bucket-name>` — Points to the S3 bucket where kOps stores cluster state
* `--yes` — Confirms the changes (without this flag, kOps only shows what it *would* do — a dry run)
* `--admin` — Generates admin kubeconfig credentials with full cluster access

**What happens internally:** kOps calls AWS APIs to create EC2 instances (master node, worker nodes), configure networking, set up security groups, create the API server DNS record in Route 53, and store all configuration in the S3 bucket. This takes several minutes.

**While the cluster is being created**, the instructor proceeds to set up the GitHub repository and source code — parallelizing the work.

**Verification (after cluster is ready):**

```bash
kubectl get nodes
```

**Expected:** Master and worker nodes listed with status `Ready`. If nodes show `NotReady`, wait a few more minutes for the cluster to fully initialize.

***

## Step 4: Create the GitHub Repository

Go to **github.com** → ensure you're logged in → click **New Repository**.

| Field          | Value                                    |
| -------------- | ---------------------------------------- |
| **Name**       | `vprokube`                               |
| **Visibility** | Public                                   |
| **Initialize** | Don't add README, .gitignore, or license |

Click **Create Repository**.

**Expected:** An empty repository page with instructions for pushing code.

***

## Step 5: Upload the Kubernetes Definition Files

The instructor uses the **GitHub web interface** for simplicity (drag-and-drop upload) instead of SSH-based git push.

Click **"uploading an existing file"** on the empty repository page.

### What to upload:

**Required:** The `kubedefs/` folder — contains all Kubernetes manifest files (deployments, services, secret, PVC, ingress). This is the only folder needed for the Kubernetes project.

**Optional (for reference):** Dockerfiles and `docker-compose.yml` from the Containerization project. Not needed for Kubernetes execution, but useful to have in the same repo for reference.

**Not needed:** The `src/` folder (application source code). The instructor confirms: *"It's going to fetch all the images from Docker Hub. We really don't need the source code."*

### Upload process:

1. Navigate to the files on your local machine (the instructor uses VS Code / File Explorer, files are in `F:/kubeapp/vprofile-project/`)
2. Drag and drop the `kubedefs/` folder into the GitHub upload area
3. Optionally add Dockerfiles and docker-compose
4. Write a commit message: e.g., `kube defs upload`
5. Click **Commit changes**

**GitHub file limit:** If you try to upload more than 100 files at once, GitHub rejects it. Upload in batches — one folder at a time.

**After commit:** Copy the **HTTPS repository URL** from the repository page.

***

## Step 6: Clone the Repository onto the kOps Instance

Back on the kOps instance (SSH session from Step 1):

```bash
git clone <repository-HTTPS-URL>
```

**Example:**

```bash
git clone https://github.com/<username>/vprokube.git
```

**What happens:** Git downloads the repository contents to the current directory on the kOps instance. The `kubedefs/` folder is now locally available.

**Verification:**

```bash
cd vprokube/
ls
```

**Expected:** You should see the `kubedefs/` folder (and optionally Docker-related files).

```bash
ls kubedefs/
```

**Expected:** All the manifest YAML files — secret, PVC, deployment files, service files, ingress definition.

**Connection to flow:** The cluster is running (Step 3) and the manifests are on the machine (Step 6). Everything is ready for the next lectures, where each manifest is applied with `kubectl create -f` or `kubectl apply -f`.

> ⚠️ **Expert Note:** In production, you would never manually drag-and-drop files to GitHub. The standard workflow: develop locally in VS Code → commit with git → push via SSH/HTTPS → clone on deployment machine (or better, use a CI/CD pipeline that automatically applies manifests when they're pushed). The instructor explicitly acknowledges this: *"We can do SSH-based authentication, push our code. But I'm just keeping it simple."*

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Lecture Purpose

```
GOAL: Get cluster running + get manifests on machine
NO new Kubernetes concepts — purely operational setup
BRIDGE: Architecture (§348) → This setup → Manifest execution (next lectures)
```

***

## Three Learner Entry Points

```
STATE 1: Never created cluster
  → go back to kOps setup lectures, do full prerequisite chain

STATE 2: Created + deleted cluster, prerequisites exist
  → power on kOps instance → run kops create + update → cluster up
  (THIS IS THE PATH FOLLOWED IN THE LECTURE)

STATE 3: Just watching
  → follow along without a cluster
```

***

## kOps Prerequisites Checklist

```
✅ AWS Access Key (on kOps instance)
✅ Route 53 Hosted Zone (DNS domain)
✅ S3 Bucket (kOps state store)
✅ DNS name records (cluster name = subdomain)
✅ kOps EC2 Instance (running)
✅ kubectl installed
```

***

## Cluster Creation Flow

```
1. SSH into kOps instance
     ssh -i <key> ubuntu@<ip> → sudo -i

2. kops create cluster <options>
     → defines cluster configuration

3. kops update cluster <name> --state=s3://<bucket> --yes --admin
     → provisions AWS resources (EC2 master/workers, SG, ASG, DNS)
     → generates kubeconfig (~/.kube/config)
     → takes several minutes

4. Verify: kubectl get nodes → all nodes Ready
```

***

## Source Code Setup Flow

```
1. github.com → create repo "vprokube" (public, empty)

2. Upload files (drag-and-drop via web UI):
     REQUIRED:  kubedefs/          ← all K8s manifest files
     OPTIONAL:  Dockerfiles, docker-compose.yml (reference only)
     NOT NEEDED: src/              ← no build happens in K8s project

3. Commit: "kube defs upload"

4. On kOps instance:
     git clone https://github.com/<user>/vprokube.git
     cd vprokube/kubedefs/
     → manifests ready for kubectl apply
```

***

## Key Architectural Insight: Build ≠ Deploy

```
CONTAINERIZATION PROJECT (previous):
  Source code → docker build → Docker image → push to Docker Hub
  (BUILD phase — images are created)

KUBERNETES PROJECT (this):
  Manifests → kubectl apply → Kubernetes pulls images from Docker Hub
  (DEPLOY phase — images are consumed, NOT built)

IMPLICATION:
  kOps instance needs: kubedefs/ (manifests)
  kOps instance does NOT need: src/ (source code)
  
  "It's going to fetch all the images from Docker Hub.
   We really don't need the source code."
```

***

## What's on the kOps Instance After This Lecture

```
~/vprokube/
  ├── kubedefs/
  │     ├── secret.yaml
  │     ├── pvc.yaml
  │     ├── db-deployment.yaml
  │     ├── mc-deployment.yaml
  │     ├── rmq-deployment.yaml
  │     ├── tomcat-deployment.yaml
  │     ├── db-service.yaml
  │     ├── mc-service.yaml
  │     ├── rmq-service.yaml
  │     ├── tomcat-service.yaml
  │     └── ingress.yaml
  │
  ├── Dockerfiles (optional, reference)
  └── docker-compose.yml (optional, reference)

~/.kube/config  ← kubeconfig (generated by kops update --admin)

CLUSTER: running (master + worker nodes, verified with kubectl get nodes)
```

***

## kops update cluster — Flag Reference

```
kops update cluster <cluster-name> \
  --state=s3://<bucket>    ← where kOps stores cluster config
  --yes                    ← actually apply (without = dry run)
  --admin                  ← generate admin kubeconfig
```

***

## GitHub Upload Constraint

```
GitHub web upload: < 100 files per upload
If > 100 files: upload folder by folder
Alternative: git push via SSH (production method)
```

***

## Project Readiness State After This Lecture

```
✅ Kubernetes cluster running (kOps)
✅ kubectl configured (kubeconfig from --admin)
✅ kubedefs/ manifests cloned to kOps instance
✅ Docker images available on Docker Hub (from Containerization project)

READY FOR: applying manifests one by one (next lectures)
  kubectl create -f secret.yaml
  kubectl create -f pvc.yaml
  kubectl create -f db-deployment.yaml
  ... (following architecture dependency order from §348)
```

***

## Reusable Engineering Pattern: Separate Build Artifact from Deployment Specification

```
PATTERN:
  BUILD PIPELINE produces ARTIFACTS (Docker images → registry)
  DEPLOY PIPELINE consumes ARTIFACTS via SPECIFICATIONS (K8s manifests → cluster)

  The deployment environment (kOps instance) needs:
    ✅ Deployment specifications (manifests / kubedefs)
    ✅ Access to artifact registry (Docker Hub / private registry)
    ❌ Source code (NOT needed — build already happened)

WHY:
  Decoupling build from deploy enables:
    - Different teams for dev (build) and ops (deploy)
    - Different schedules (build on commit, deploy on demand)
    - Different environments (build once, deploy to dev/staging/prod)
    - Rollback by re-deploying old manifest pointing to old image tag

WHERE ELSE:
  • CI/CD pipelines: Jenkins builds image → ArgoCD deploys manifest
  • Helm charts: chart defines deployment, values.yaml specifies image tag
  • Terraform: infra code deploys AMIs built by Packer
  • Any artifact-based deployment model
```

***

## One-Line Mental Reload Trigger

> *"Power on kOps instance → kops create + update cluster (--yes --admin) → create GitHub repo 'vprokube' → upload kubedefs/ folder (manifests only, no source code needed — K8s pulls pre-built images from Docker Hub) → git clone onto kOps instance → cluster running + manifests ready for kubectl apply."*

This single sentence reconstructs the full operational sequence, the cluster creation command with key flags, the repository setup, the critical insight about not needing source code, the image consumption model, and the final readiness state for manifest deployment. [\[358-k8s-cl...ource-code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/358-k8s-cluster-setup-and-source-code.txt)
