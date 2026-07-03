# Terraform for Amazon EKS Cluster Setup — Deep Learning Material

**Source:** [346-terraform-for-eks-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt?EntityRepresentationId=85ee97ff-5392-44cc-b517-3eac049734db) (VTT Caption File) [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Amazon EKS — Managed Kubernetes Service

Amazon EKS (Elastic Kubernetes Service) is a **managed Kubernetes service** from AWS. The core concept is best understood by contrasting it with the self-managed approach already learned. With Kops or Kubeadm, **you** create the Kubernetes cluster and **you** manage it — the VPC, the instances, the networking, the upgrades, the scaling, the security patches — all of it becomes your system administration responsibility. EKS shifts that burden to AWS. You provide a few simple configuration details (cluster name, node groups, instance types), and AWS creates the cluster, manages the control plane, handles upgrades, and takes care of the underlying infrastructure. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

The instructor draws a direct analogy to databases: just as you can install and manage MySQL manually **or** use RDS (a managed database service), you can set up Kubernetes yourself with Kops/Kubeadm **or** use EKS. The trade-off is the same: managed services cost more money but eliminate operational overhead. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

A critical architectural distinction in EKS: the **control plane (master node) is invisible**. Unlike a Kops cluster where you can see the master node as an EC2 instance, in EKS the control plane is fully managed by AWS and hidden from you. What you see and manage are only the **worker nodes** (node groups). The control plane is what AWS calls "the EKS cluster" — you interact with it only through its **public endpoint URL** (equivalent to the `api.kubevpro...` URL in Kops, but managed by AWS). [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

Once the cluster is created, the experience is **identical** to any other Kubernetes cluster. You get a kubeconfig file, you use `kubectl`, and you deploy containerized applications. The instructor emphasizes: *"Once it is created, it's same Kubernetes."* [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

### EKS Pricing Model

EKS has **two separate charges**: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

* **EKS cluster pricing** — a flat fee for the managed control plane (the master node equivalent).
* **Worker node pricing** — standard EC2 pricing for the instances in your node groups.

Both are required, and together they make EKS **expensive**. The instructor warns about this repeatedly and recommends creating and destroying the cluster within an hour to minimize costs.

> ⚠️ **Expert Note**
> Never delete an EKS cluster created by Terraform through the AWS Console. The instructor explicitly warns: *"Don't try to delete the cluster from there. You have to do it only from Terraform."* Deleting via the console would leave Terraform's state file out of sync, causing state drift and making future operations unpredictable. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## 1.2 Terraform Modules — Reusable Infrastructure Code

Terraform modules are **pre-written, reusable packages of Terraform code** that create and manage a set of related resources. The instructor's definition: *"Modules are containers for multiple resources that are used together."* The word "container" here is not Docker — it means a logical grouping of `.tf` files that someone has written and published for others to use. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

Modules eliminate the need to write Terraform code from scratch. Instead of writing hundreds of lines of HCL to define a VPC with subnets, NAT gateways, route tables, and internet gateways, you use the **VPC module** — pass in a few variables (CIDR, subnet CIDRs, AZs), and the module creates everything. The same applies to EKS. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

Modules are published on the **Terraform Registry** (registry.terraform.io). The two modules used in this lecture are both **official AWS modules**: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

* **`terraform-aws-modules/vpc/aws`** — Creates and manages a complete VPC with public/private subnets, NAT gateways, route tables, DNS settings, and tagging.
* **`terraform-aws-modules/eks/aws`** — Creates and manages an EKS cluster with node groups, auto-scaling, IAM roles, and endpoint configuration.

### How Modules Work — Variables as the Interface

Every module exposes a set of **input variables** that you use to customize its behavior. You don't modify the module's internal code — you only set variable values. The module documentation lists all available variables with their types (string, list, map, bool) and default values. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

For the VPC module, key variables include: `name`, `cidr`, `azs`, `private_subnets`, `public_subnets`, `enable_nat_gateway`, `single_nat_gateway`, `enable_dns_hostnames`, and various tag variables. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

For the EKS module, key variables include: `cluster_name`, `vpc_id`, `subnet_ids`, `cluster_endpoint_public_access`, and `eks_managed_node_groups`. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

The instructor emphasizes a practical learning approach: *"You don't need to know all this by heart. When you keep using it, then you'll slowly become master of it."* The documentation is the reference; you consult it as needed for your specific project requirements. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

### Module Output Variables — Cross-Module Data Flow

When a module creates resources, it produces **output variables** that other modules or resources can reference. This creates a **data dependency chain**: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

* The VPC module creates a VPC and outputs `vpc_id` and `private_subnets`.
* The EKS module consumes these: `vpc_id = module.vpc.vpc_id` and `subnet_ids = module.vpc.private_subnets`.
* The EKS module in turn outputs `cluster_endpoint` and `cluster_certificate_authority_data`.
* The Kubernetes provider consumes these for authentication.

This cross-module variable flow is the core mechanism that ties independent modules into a coherent infrastructure stack. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## 1.3 Code Architecture — The Four Files

The Terraform code is organized into four files, each with a distinct responsibility: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

### `terraform.tf` — Dependencies and Backend

This file declares:

* **Required providers** — `aws` (core cloud provider), `random` (for encryption key generation), `tls` (for certificates), `cloudinit` (for instance initialization), and `kubernetes` (for Kubernetes resource management).
* **Backend configuration** — An S3 bucket for storing Terraform state. The state file is stored at `state/terraform.tfstate` inside the bucket. The bucket and the cluster **must be in the same region** (not strictly mandatory, but the instructor keeps them together). [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

### `variables.tf` — Input Variables

Two simple variables: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

* `region` — The AWS region for the cluster (default: `us-east-1`).
* `cluster_name` — The name of the EKS cluster (e.g., `vprofile-eks`).

### `main.tf` — Providers, Data Sources, VPC Module

This file contains: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Kubernetes provider** — Configured with the EKS cluster endpoint and certificate. The `host` value comes from `module.eks.cluster_endpoint`, and the certificate is `base64decode`-d from `module.eks.cluster_certificate_authority_data`. These values are not known until the EKS module creates the cluster — Terraform resolves this dependency automatically.

**AWS provider** — Configured with `var.region`.

**Data source: `aws_availability_zones`** — Fetches the list of all availability zones in the selected region dynamically. This avoids hardcoding zone names. The result is used in the VPC module via the `slice()` function: `slice(data.aws_availability_zones.available.names, 0, 3)` extracts the first three AZs (index 0, 1, 2) as a list (e.g., `["us-east-1a", "us-east-1b", "us-east-1c"]`). [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**VPC module** — Uses the `terraform-aws-modules/vpc/aws` module with:

* 3 private subnets and 3 public subnets (matching the 3 AZs)
* NAT gateway enabled, but with `single_nat_gateway = true` (one NAT gateway instead of three, to save costs)
* DNS hostnames enabled
* **EKS-required tags** on subnets: `kubernetes.io/cluster/<cluster-name> = shared`. These tags are mandated by AWS documentation so that EKS can identify which subnets belong to the cluster.

> 🔍 **Deep Dive**
> The `slice()` function is a Terraform built-in that extracts a sub-list from a list. `slice(list, start, end)` returns elements from index `start` up to (but not including) `end`. If you want only 2 AZs instead of 3, change to `slice(..., 0, 2)` — but then also reduce the private and public subnet lists to match. The AZ count, subnet count, and slice range must always be consistent. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

### `eks.tf` (part of main configuration) — EKS Module

The EKS module creates: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

* The **EKS cluster** (managed control plane) with `cluster_endpoint_public_access = true`.
* **Two node groups** using `eks_managed_node_groups`:
  * **Node group 1**: `instance_types = ["t3.small"]`, min=1, max=3, desired=2.
  * **Node group 2**: `instance_types = ["t3.small"]`, min=1, max=3, desired=1.
  * Total initial worker nodes: **3** (2 + 1).
* Each node group has an **AMI type** specified (e.g., AL2\_x86\_64).
* Each node group is backed by an **auto-scaling group** — Kubernetes/EKS can scale nodes up to `max_size` based on load.

***

## 1.4 State Management — S3 Backend

Terraform stores its state file in an **S3 bucket** configured as the backend. The state file (`terraform.tfstate`) tracks every resource Terraform has created, enabling it to know what exists, what has changed, and what needs to be destroyed. This is why cluster deletion **must** happen through `terraform destroy` — Terraform reads the state to identify all 53+ resources it created and deletes them systematically. Deleting via the AWS Console bypasses the state file and creates orphaned state entries. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## 1.5 Kubeconfig Generation — The Bridge to kubectl

After the EKS cluster is created, you need a **kubeconfig file** to use `kubectl`. Unlike Kops (which generates the kubeconfig automatically), EKS requires you to run an explicit AWS CLI command: [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

```
aws eks update-kubeconfig --name <cluster-name> --region <region>
```

This command uses your configured IAM credentials (from `aws configure`) to generate the kubeconfig file at `~/.kube/config`. Once generated, `kubectl get nodes` works exactly as with any other Kubernetes cluster. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are provisioning an **Amazon EKS cluster** with a complete VPC using **Terraform modules**. The final outcome: a working Kubernetes cluster with 3 worker nodes (across 2 node groups), accessible via `kubectl` from our local machine. After verification, the cluster is immediately destroyed to minimize costs. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Cost warning:** EKS is expensive. The instructor recommends completing the entire exercise (create → verify → destroy) within one hour. If you prefer not to spend money, watching the lecture and reviewing the code is a valid alternative.

***

## Step 1: Clone the Repository and Switch Branch

Open **VS Code → Source Control → Clone Repository**.

Paste the repository URL:

```
https://github.com/hkhcoder/vprofile-project
```

Select a destination folder (e.g., create `terraform-eks/`). After cloning, **switch to the branch `terraform-eks`**. You should see the Terraform files: `terraform.tf`, `variables.tf`, `main.tf`, and the EKS configuration. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Step 2: Create the S3 Bucket for Terraform State

Navigate to **AWS Console → S3 → Create Bucket**.

| Field      | Value                                                             |
| ---------- | ----------------------------------------------------------------- |
| **Name**   | `terraform-eks23` (must be globally unique — use your own suffix) |
| **Region** | `us-east-1` (same region as the cluster)                          |

Click **Create Bucket**. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Step 3: Modify the Code — Required Changes

### 3a: `terraform.tf` — Update the Backend Bucket Name

Find the `backend "s3"` block and update:

```hcl
backend "s3" {
  bucket = "terraform-eks23"   # ← YOUR bucket name
  key    = "state/terraform.tfstate"
  region = "us-east-1"
}
```

The `key` defines the path inside the bucket where the state file will be stored. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

### 3b: `variables.tf` — Update the Cluster Name

```hcl
variable "cluster_name" {
  default = "vprofile-eks"   # ← change to YOUR unique name
}
```

The instructor changes this value during the lecture (trying various names). Pick a unique, simple name. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Save all modified files** (Ctrl+S). [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Step 4: Install Prerequisites on Your Local Machine

### 4a: Install Terraform

**Windows (PowerShell as Administrator):**

```powershell
choco install terraform
```

**macOS:**

```bash
brew install terraform
```

**Verify:**

```bash
terraform --version
```

If you have an older version, uninstall first (`choco uninstall terraform`) and reinstall. The instructor does this during the lecture because an older version was installed from previous experiments. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

### 4b: Install kubectl

**Windows (PowerShell as Administrator):**

```powershell
choco install kubernetes-cli
```

**macOS:**

```bash
brew install kubernetes-cli
```

### 4c: Create IAM User and Configure AWS CLI

Create an IAM user with **AdministratorAccess** policy (same as the Kops lecture). Generate an access key. Then:

```bash
aws configure
```

| Prompt            | Value                  |
| ----------------- | ---------------------- |
| Access Key ID     | From CSV / IAM console |
| Secret Access Key | From CSV / IAM console |
| Region            | `us-east-1`            |
| Output format     | `json`                 |

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Step 5: Initialize Terraform

Open **Git Bash** (Windows) or **Terminal** (macOS). Navigate to the cloned repository:

```bash
cd /path/to/terraform-eks/vprofile-project
```

If a `.terraform` folder exists from previous experiments, remove it:

```bash
rm -rf .terraform
```

Initialize:

```bash
terraform init
```

| Part             | Meaning                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `terraform init` | Downloads provider plugins, initializes the S3 backend, and downloads the VPC and EKS modules from the Terraform Registry |

**Expected output:** "Terraform has been successfully initialized!" [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Common failures:** Wrong bucket name or region in `terraform.tf` → backend initialization fails. Fix the values and re-run `terraform init`.

***

## Step 6: Plan the Infrastructure

```bash
terraform plan
```

**Expected output:** A long, detailed list of all resources Terraform will create. The plan shows **53 resources to add** — this includes the VPC, subnets, NAT gateways, route tables, the EKS cluster, node groups, auto-scaling groups, launch templates, security groups, IAM roles, and more. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Decision point:** Read through the plan. If you do not want to incur charges, **stop here**. If you want to proceed, continue to Step 7.

***

## Step 7: Apply the Infrastructure

```bash
terraform apply
```

Terraform will show the plan again and prompt for confirmation. Type **`yes`** and press Enter. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**What happens:** Terraform begins creating all 53+ resources in AWS. This takes a **very long time** (15–25 minutes typically for EKS). The EKS cluster creation itself is the longest step. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Expected result:** After completion, Terraform outputs the **cluster endpoint URL**. This is the API server address for the EKS cluster.

**Verification in AWS Console:** Navigate to **EKS** in the us-east-1 region:

* The cluster should be visible with its endpoint.
* **Node Groups tab:** Two node groups — one with 2 nodes, one with 1 node.
* **Networking tab:** The VPC with 3 public + 3 private subnets (6 total).
* **VPC Console:** The dedicated VPC with all subnets visible. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Step 8: Generate the Kubeconfig File

```bash
aws eks update-kubeconfig --name vprofile-eks --region us-east-1
```

| Part                        | Meaning                                                          |
| --------------------------- | ---------------------------------------------------------------- |
| `aws eks update-kubeconfig` | AWS CLI command that generates/updates the kubeconfig file       |
| `--name vprofile-eks`       | The EKS cluster name (must match what you set in `variables.tf`) |
| `--region us-east-1`        | The AWS region where the cluster was created                     |

**Expected output:** "Added new context ... to \~/.kube/config" [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Verify the kubeconfig:**

```bash
cat ~/.kube/config
```

You should see the cluster endpoint, certificate data, and authentication details. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**Common mistake:** The instructor types `ua-east-1` instead of `us-east-1` and has to cancel and re-run. Double-check the region code.

***

## Step 9: Verify kubectl Access

```bash
kubectl get nodes
```

**Expected output:** Three nodes in `Ready` state — two from node group 1, one from node group 2. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

From this point, the cluster behaves identically to any Kubernetes cluster. You can deploy applications, create services, manage pods — the same kubectl commands apply. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Step 10: Destroy the Cluster (CRITICAL — Do Not Skip)

```bash
terraform destroy
```

Terraform shows everything it will delete. Type **`yes`** to confirm. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

**What gets deleted:** All 53+ resources — VPC, subnets, NAT gateways, EKS cluster, node groups, ASGs, IAM roles, security groups — everything Terraform created.

**How long:** Destruction takes a long time (10–20 minutes). **Wait for complete deletion.** Do not interrupt the process.

**Critical rules:**

* Never delete EKS resources from the AWS Console — always use `terraform destroy`.
* Do not keep the cluster running longer than necessary — the billing meter runs on EKS cluster + NAT gateways + EC2 instances continuously. [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
EKS = Managed Kubernetes (AWS runs the control plane)
Kops/Kubeadm = Self-managed Kubernetes (you run everything)

EKS analogy: MySQL (manual) → RDS (managed)
             Kops (manual K8s) → EKS (managed K8s)

After creation → same kubectl, same kubeconfig, same Kubernetes
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## EKS Architecture

```
EKS Cluster (control plane)
  └── INVISIBLE — managed by AWS
  └── Accessed via public endpoint URL
  └── You pay for this separately

Node Groups (worker nodes)
  ├── Group 1: t3.small × 2 (min=1, max=3, desired=2)
  └── Group 2: t3.small × 1 (min=1, max=3, desired=1)
  └── Backed by Auto Scaling Groups
  └── You pay standard EC2 pricing

VPC (created by Terraform VPC module)
  ├── 3 public subnets
  ├── 3 private subnets
  ├── 1 NAT gateway (single_nat_gateway=true for cost)
  └── Tagged for EKS: kubernetes.io/cluster/<name>=shared
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Terraform Module Architecture

```
terraform-aws-modules/vpc/aws          terraform-aws-modules/eks/aws
──────────────────────────────         ──────────────────────────────
INPUT:                                 INPUT:
  name, cidr, azs                        cluster_name
  private_subnets, public_subnets        vpc_id ← module.vpc.vpc_id
  enable_nat_gateway, tags               subnet_ids ← module.vpc.private_subnets
                                         node_groups config
OUTPUT:                                OUTPUT:
  vpc_id ─────────────────────────►      cluster_endpoint ──────► Kubernetes provider
  private_subnets ────────────────►      cluster_ca_data ───────► Kubernetes provider

Cross-module data flow: VPC outputs → EKS inputs → K8s provider inputs
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## File Structure

```
terraform.tf    → providers (aws, random, tls, cloudinit, kubernetes)
                → backend s3 (bucket name, key, region)

variables.tf    → region (us-east-1)
                → cluster_name (vprofile-eks)

main.tf         → Kubernetes provider (host, cert from EKS module outputs)
                → AWS provider (var.region)
                → data source: aws_availability_zones → slice(0,3)
                → module "vpc" (source, cidr, subnets, NAT, tags)

eks config      → module "eks" (cluster_name, vpc_id, subnet_ids, node_groups)
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Data Flow: AZ Discovery

```
data.aws_availability_zones.available.names
  → ["us-east-1a", "us-east-1b", "us-east-1c", "us-east-1d", ...]
    → slice(0, 3) → ["us-east-1a", "us-east-1b", "us-east-1c"]
      → fed into VPC module azs variable

Change to 2 AZs: slice(0, 2) + reduce subnet lists to 2 entries each
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Required Changes Before Apply

```
terraform.tf  → backend bucket name (YOUR unique bucket)
variables.tf  → cluster_name (YOUR unique name)
aws configure → access key, secret key, region, json
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Command Sequence

```
1. git clone + switch to branch terraform-eks
2. Create S3 bucket (same region as cluster)
3. Edit: terraform.tf (bucket), variables.tf (cluster name)
4. Install: terraform, kubectl, aws configure
5. cd to repo directory
6. terraform init          → downloads providers + modules + initializes backend
7. terraform plan          → shows 53 resources to create (review / stop point)
8. terraform apply → yes  → creates everything (~20 min)
9. aws eks update-kubeconfig --name <name> --region <region>
10. kubectl get nodes      → 3 nodes Ready ✓
11. terraform destroy → yes → deletes everything (~15 min) ← DO NOT SKIP
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Kubeconfig Generation (EKS vs Kops)

```
Kops: kubeconfig auto-generated at ~/.kube/config during cluster creation
EKS:  must run explicit command:
      aws eks update-kubeconfig --name <name> --region <region>
      → generates ~/.kube/config
      → requires IAM user configured (aws configure)
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Cost Awareness

```
Charges:
  EKS cluster (control plane)  → flat hourly rate
  Worker nodes (EC2)           → t3.small × 3
  NAT gateway                  → hourly + data transfer
  
Strategy: create → verify → destroy within 1 hour
Never leave running unattended

CRITICAL: delete ONLY via terraform destroy (never via AWS Console)
  Console delete → Terraform state drift → broken future operations
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## EKS-Required Subnet Tags

```
Tag on subnets:
  Key:   kubernetes.io/cluster/<cluster-name>
  Value: shared

Source: AWS documentation (Google: "AWS EKS VPC tags")
Without these tags: EKS cannot identify its subnets → cluster creation fails
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Deletion Rule (CRITICAL)

```
Created by Terraform → MUST be deleted by Terraform
  terraform destroy → reads state → deletes all 53+ resources systematically
  
  AWS Console delete → state file doesn't know → orphaned entries
                     → future terraform plan/apply/destroy BROKEN
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## 53 Resources Created (Categories)

```
VPC layer:     VPC, 6 subnets (3 public + 3 private), route tables,
               IGW, NAT gateway, elastic IP
EKS layer:     EKS cluster, 2 node groups, ASGs, launch templates,
               IAM roles/policies, security groups
Supporting:    CloudWatch log groups, KMS keys, certificates
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

## Reusable Engineering Patterns

**Module Composition Pattern**

```
Complex infrastructure = composition of reusable modules
  Module A (VPC) outputs → Module B (EKS) inputs
  Each module: black box with variables in, resources + outputs out
  You customize via variables, never modify internal code
  
  Recurrence: Ansible roles, Helm charts, CloudFormation nested stacks
  Principle: don't write from scratch → compose from tested building blocks
```

**Plan-Then-Apply Pattern (Repeated)**

```
terraform plan  → preview (no side effects)
terraform apply → execute (creates infrastructure)
terraform destroy → reverse (removes infrastructure)

Same pattern: Kops create/update, K8s dry-run/apply
  Benefit: review before commit, reversible, reproducible
```

**State-Backed Lifecycle Management**

```
State file (S3) = single source of truth for what exists
  Create: state records what was created
  Destroy: state tells what to delete
  
  Delete outside state → state drift → system breaks
  Rule: whatever creates it must destroy it
  
  Recurrence: Terraform state, Kops S3 state, CloudFormation stacks
```

**Managed vs Self-Managed Trade-Off Pattern**

```
Self-managed: full control + full responsibility + lower cost
Managed: less control + less responsibility + higher cost

Decision axis: operational maturity × team size × budget
  Small team + limited ops experience → managed (EKS, RDS)
  Large team + deep ops skills → self-managed (Kops, manual MySQL)
```

 [\[346-terraf...-eks-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/346-terraform-for-eks-setup.txt)

***

This completes the full reconstruction of the Terraform EKS lecture. **Theory** explains EKS concepts, Terraform modules, and the code architecture. **Practical** walks through every step from cloning to destruction with full command breakdowns. The **Compression Map** enables rapid recall of the architecture, module data flow, command sequence, and critical operational rules. Let me know if you'd like any section refined! 🚀
