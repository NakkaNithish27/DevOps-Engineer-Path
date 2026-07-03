# EKS Cluster Prerequisites — Deep Learning Material

**Source:** [372-eks-prereqs.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt?EntityRepresentationId=5d2afd34-ee1b-455b-8d9f-87a01a5050f4) (VTT Caption File) and [372.IntallTools.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt?EntityRepresentationId=cac37b43-50d1-469c-8ba7-7b847560577d) (Tool Installation Reference) [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt), [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What This Lecture Covers — Context and Purpose

This lecture completes the **prerequisites** needed before writing Terraform code to spin up an EKS cluster with Argo CD. It is a setup lecture — no infrastructure is created, no Terraform code is written. The goal is to ensure that the local machine has all required tools installed, AWS credentials are configured, and the `vprofile-infra` repository is open and ready for the next lecture where Terraform code will be written using GitHub Copilot. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

This fits into the broader GitOps pipeline architecture (covered in the previous lecture): the `vprofile-infra` repository holds Terraform code, and the immediate plan is to execute that Terraform code **from the local machine** first. The Terraform pipeline via GitHub Actions will be configured at the end of the project — the local execution comes first for initial cluster setup. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## 1.2 Domain and Public Certificate — HTTPS Access

The first prerequisite is a **domain name**. The vprofile application and Argo CD will both be accessed through **secure HTTPS URLs** — not raw IP addresses or insecure HTTP. This requires: [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

1. **A domain** — The instructor uses `hkhinfoteck.xyz` purchased from GoDaddy. Any registrar works. The course prerequisites section explains how to purchase a cheap domain.

2. **An AWS public certificate** for this domain — This is a **free** TLS/SSL certificate issued by AWS Certificate Manager (ACM). It enables HTTPS access for services deployed on AWS infrastructure.

If you do not have a domain and do not wish to purchase one, the instructor explicitly says it is fine to **watch from here** — the lecture can be followed without a domain, but the HTTPS URL access for the application and Argo CD will not work without one. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## 1.3 IAM User — Terraform Execution Credentials

An **IAM user** with the **AdministratorAccess** policy is required. This user provides the credentials (access key + secret key) that Terraform uses to interact with AWS services when creating the EKS cluster and all associated resources (VPC, subnets, node groups, IAM roles, etc.). [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

The credentials are configured on the local machine using `aws configure`, which stores the access key, secret key, default region, and output format in the AWS CLI configuration files. Terraform reads these credentials automatically when executing. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

The instructor gives a strong security warning: *"You need to be extremely careful with this access key, it has administrator privileges."* The recommended practice is: [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

* Download the key only to your machine.
* Keep it safe.
* **Delete the key and the user** once you are done with the project.

> ⚠️ **Expert Note**
> Administrator access is used here for simplicity — Terraform touches many AWS services during EKS creation. In production, you would create a scoped IAM policy with only the permissions Terraform actually needs (VPC, EKS, EC2, IAM, S3, etc.) following the principle of least privilege. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## 1.4 Required Tools — The Five Binaries

Five CLI tools must be installed on the local machine. Each serves a distinct purpose in the EKS + Argo CD workflow: [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt), [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

| Tool                         | Purpose                                                                                               |
| ---------------------------- | ----------------------------------------------------------------------------------------------------- |
| **awscli**                   | AWS Command Line Interface — communicates with AWS services, stores credentials, generates kubeconfig |
| **terraform**                | Infrastructure as Code tool — creates the EKS cluster and all supporting AWS resources                |
| **kubernetes-cli** (kubectl) | Kubernetes command-line tool — interacts with the EKS cluster after creation                          |
| **kubernetes-helm** (helm)   | Kubernetes package manager — manages Helm charts for application deployment                           |
| **eksctl**                   | AWS-specific CLI for EKS — simplifies EKS cluster operations and configuration                        |

These five tools together provide full control over the infrastructure lifecycle: Terraform creates the cluster, awscli configures credentials and generates kubeconfig, kubectl interacts with Kubernetes, Helm manages application deployment packages, and eksctl handles EKS-specific operations. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

### Installation Methods — OS-Specific

The installation approach differs by operating system, using platform-specific package managers: [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

**Windows** uses **two** package managers:

* **Chocolatey (choco)** — installs awscli, terraform, kubernetes-cli, and kubernetes-helm.
* **Scoop** — installs eksctl. Scoop must be set up first by running a PowerShell execution policy change and the Scoop installer script.

**macOS** uses **one** package manager:

* **Homebrew (brew)** — installs all five tools in a single command.

The reason for the dual package manager on Windows is that eksctl is not available in Chocolatey's repository but is available in Scoop's. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt), [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

***

## 1.5 Execution Strategy — Local First, Pipeline Later

The instructor clarifies an important sequencing decision: even though the `vprofile-infra` repository will eventually have a GitHub Actions pipeline (Validate → Plan → Apply → Drift Detection → Notify → Destroy), the **initial cluster creation** is done by running Terraform **locally** from the developer's machine. The pipeline is configured at the end of the project. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

This is a common real-world pattern: you bootstrap infrastructure manually (or from a local machine) first, then wrap the same Terraform code in a CI/CD pipeline for ongoing management. The pipeline automates what was initially done manually. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## 1.6 The vprofile-infra Repository

The lecture ends by opening the `vprofile-infra` Git repository (created in a previous lecture) in **VS Code** using the `code .` command. This repository is where the Terraform code will be written in the next lecture, using **GitHub Copilot** to assist with code generation. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing

We are completing the **prerequisites** for EKS cluster creation: installing five CLI tools on the local machine, creating an IAM user with admin access, configuring AWS credentials, and opening the `vprofile-infra` repository in VS Code. After this, the environment is fully ready to write and execute Terraform code. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Step 1: Install Required Tools

### Windows (PowerShell as Administrator)

Open **PowerShell as Administrator**. Run the following commands in sequence:

**Install four tools via Chocolatey:**

```powershell
choco install awscli terraform kubernetes-cli kubernetes-helm -y
```

| Part              | Meaning                                                |
| ----------------- | ------------------------------------------------------ |
| `choco install`   | Installs packages using the Chocolatey package manager |
| `awscli`          | AWS CLI                                                |
| `terraform`       | Terraform                                              |
| `kubernetes-cli`  | kubectl                                                |
| `kubernetes-helm` | Helm                                                   |
| `-y`              | Auto-confirms all installation prompts                 |

This takes some time to download and install all four tools. [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

**Install Scoop (required for eksctl):**

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

| Part                                                  | Meaning                                                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` | Allows PowerShell to run scripts downloaded from the internet (required for Scoop)                |
| `irm get.scoop.sh \| iex`                             | Downloads and executes the Scoop installer (`irm` = Invoke-RestMethod, `iex` = Invoke-Expression) |

**Install eksctl via Scoop:**

```powershell
scoop install eksctl
```

 [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

### macOS (Terminal)

Open **Terminal**. Run a single command:

```bash
brew install awscli terraform kubernetes-cli helm eksctl
```

All five tools are installed in one Homebrew command. [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

**Verification:** After installation, verify each tool is accessible:

```bash
aws --version
terraform --version
kubectl version --client
helm version
eksctl version
```

Each command should return version information without errors.

**Pause point:** The instructor says to pause the lecture and complete the installation before continuing. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Step 2: Create the IAM User

Navigate to **AWS Console → IAM → Users → Create User**.

| Field           | Value                                            |
| --------------- | ------------------------------------------------ |
| **Name**        | Any name (e.g., `terraform-admin`)               |
| **Permissions** | Attach policies directly → `AdministratorAccess` |

After creation, generate the access key: [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

1. Click on the user → **Security Credentials** tab.
2. Click **Create access key**.
3. Select **CLI** as the use case.
4. Confirm ("I understand").
5. Click **Next** → **Create access key**.
6. **Download the CSV file** or note the access key ID and secret access key.

**Security warning:** This key has **full administrator privileges**. Keep it only on your machine. Delete the key and user after the project is complete. Never share, commit to Git, or expose these credentials. [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Step 3: Configure AWS CLI

Open **Git Bash** (Windows) or **Terminal** (macOS):

```bash
aws configure
```

You will be prompted for four values:

| Prompt                | Value                                  |
| --------------------- | -------------------------------------- |
| AWS Access Key ID     | From the CSV file / IAM console        |
| AWS Secret Access Key | From the CSV file / IAM console        |
| Default region name   | `us-east-1` (or your preferred region) |
| Default output format | `json`                                 |

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

**Verification:**

```bash
aws sts get-caller-identity
```

This should return your IAM user ARN, confirming the credentials are correctly configured.

**Connection to larger flow:** Terraform will automatically use these credentials when executing. No additional Terraform-specific credential configuration is needed — it reads from the same AWS CLI configuration files.

***

## Step 4: Open the vprofile-infra Repository in VS Code

Navigate to the directory where you cloned the `vprofile-infra` repository:

```bash
cd /path/to/vprofile-infra
code .
```

| Part                         | Meaning                                |
| ---------------------------- | -------------------------------------- |
| `cd /path/to/vprofile-infra` | Navigate to the repository directory   |
| `code .`                     | Opens the current directory in VS Code |

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

**Expected result:** VS Code opens with the `vprofile-infra` repository loaded. This is where Terraform code will be written in the next lecture using GitHub Copilot.

***

## Prerequisites Checklist (Before Next Lecture)

| Prerequisite                                           | Status               |
| ------------------------------------------------------ | -------------------- |
| Domain purchased (e.g., from GoDaddy)                  | ✓ (or watching only) |
| AWS public certificate for domain (via ACM)            | ✓ (or watching only) |
| awscli installed                                       | ✓                    |
| terraform installed                                    | ✓                    |
| kubectl installed                                      | ✓                    |
| helm installed                                         | ✓                    |
| eksctl installed                                       | ✓                    |
| IAM user with AdministratorAccess created              | ✓                    |
| `aws configure` completed with access key + secret key | ✓                    |
| `vprofile-infra` repo open in VS Code                  | ✓                    |

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt), [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
This lecture = prerequisites for EKS + Argo CD setup via Terraform
  No infrastructure created
  No Terraform code written
  Pure environment preparation
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Prerequisites List

```
1. Domain (GoDaddy / any registrar)
     └── + AWS public certificate (ACM, free)
     └── Purpose: HTTPS URLs for vprofile app + Argo CD
     └── Optional: can watch without domain

2. IAM User → AdministratorAccess → access key + secret key
     └── aws configure (key, secret, region, json)
     └── ⚠️ Delete after project — admin privileges = high risk

3. Five CLI Tools:
     awscli     → AWS communication + credential storage
     terraform  → infrastructure creation (EKS)
     kubectl    → Kubernetes cluster interaction
     helm       → Helm chart management
     eksctl     → EKS-specific operations

4. vprofile-infra repo → open in VS Code
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt), [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

***

## Tool Installation Commands

```
WINDOWS (PowerShell as Admin):
  choco install awscli terraform kubernetes-cli kubernetes-helm -y
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  irm get.scoop.sh | iex
  scoop install eksctl

macOS (Terminal):
  brew install awscli terraform kubernetes-cli helm eksctl

Windows: 2 package managers (choco + scoop)
macOS:   1 package manager (brew)
Reason:  eksctl not in choco → use scoop
```

 [\[372.IntallTools \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372.IntallTools.txt)

***

## IAM User Flow

```
IAM → Create User → attach AdministratorAccess
  → Security Credentials → Create access key → CLI
    → Download CSV
      → aws configure (key, secret, us-east-1, json)
        → Terraform reads these automatically

⚠️ After project: delete key → delete user
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Execution Strategy

```
NOW:   Execute Terraform from LOCAL MACHINE (this lecture's setup)
LATER: Wrap same Terraform code in GitHub Actions pipeline

Bootstrap locally first → automate via pipeline later
  Common real-world pattern for infrastructure setup
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## What Each Tool Does in the Pipeline

```
aws configure → stores credentials → Terraform reads them
terraform     → creates EKS cluster + VPC + all AWS resources
kubectl       → interacts with K8s cluster post-creation
helm          → manages vprofile Helm charts + Argo CD Helm install
eksctl        → EKS-specific cluster configuration
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Domain + Certificate Chain

```
Domain (GoDaddy) → AWS ACM public certificate (free)
  → HTTPS URL for vprofile app
  → HTTPS URL for Argo CD dashboard
  
No domain → no HTTPS → can still watch/learn but not access via URL
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Next Step

```
This lecture: prerequisites complete ✓
Next lecture: write Terraform code in vprofile-infra using GitHub Copilot
  → Terraform creates EKS cluster
  → Then: deploy Argo CD, connect pipelines, full GitOps flow
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

## Reusable Engineering Patterns

**Bootstrap-Then-Automate Pattern**

```
Phase 1: Execute infrastructure code MANUALLY (local machine)
  → Verify it works → cluster created → tested

Phase 2: Wrap same code in CI/CD pipeline (GitHub Actions)
  → Automates ongoing management (plan, apply, drift, destroy)

You never build the pipeline first without knowing the code works
  Manual validation → then automation

Recurrence: Terraform local → Terraform Cloud/pipeline,
            Ansible manual run → AWX/Tower automation,
            any IaC bootstrapping workflow
```

**Credential Lifecycle Pattern**

```
Create IAM user → generate access key → use → DELETE when done
  Minimize exposure window for high-privilege credentials
  Never leave admin keys active after project completion

Recurrence: any cloud project with temporary admin access,
            service account key rotation, CI/CD secret management
```

 [\[372-eks-prereqs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/372-eks-prereqs.txt)

***

This completes the full reconstruction of the EKS Prerequisites lecture. **Theory** explains the purpose of each prerequisite and security considerations. **Practical** provides exact installation commands and configuration steps. The **Compression Map** enables rapid recall of the tool list, installation methods, and execution strategy. Let me know if you'd like any section refined! 🚀
