# Kops for Kubernetes Cluster Setup on AWS — Deep Learning Material

**Source:** [326-kops-for-k8s-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt?EntityRepresentationId=1d319e25-fda1-470f-a62d-9bb71b1a322d) (VTT Caption File) and [326.kopscreate.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt?EntityRepresentationId=b9b39087-a910-4c27-9ffd-dc78d46daa05) (Command Reference) [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt), [\[326.kopscreate \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Kops Is and What Problem It Solves

Kops (Kubernetes Operations) is a **command-line tool** that automates the creation, management, and deletion of production-grade Kubernetes clusters on cloud infrastructure. Without Kops, setting up a Kubernetes cluster manually would require provisioning VPCs, subnets, EC2 instances, configuring networking, installing Kubernetes components on each node, setting up DNS, configuring auto-scaling groups, creating security groups, and wiring everything together — a complex, error-prone process involving dozens of AWS services. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

Kops reduces all of this to essentially **two commands**: one to generate the cluster configuration, and another to apply it. Kops handles the entire infrastructure lifecycle — creation, validation, and deletion — by directly interacting with AWS services on your behalf.

***

## 1.2 Architecture — The Kops Base Machine

A critical architectural concept is the **separation between the Kops management machine and the Kubernetes cluster itself**. The EC2 instance from which you run Kops commands is **not part of the cluster**. It is a lightweight management workstation (t2.micro is sufficient) used solely to: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

* Install and run the `kops` binary
* Install and run `kubectl` (the Kubernetes CLI)
* Store SSH keys used by Kops to configure cluster nodes
* Run `aws cli` configured with credentials that have access to AWS services

The actual cluster consists of separate, larger EC2 instances (control plane and worker nodes) that Kops creates automatically. The Kops instance is the **control point** — you can shut it down when you are not managing the cluster, and power it on whenever you need to create, modify, or delete the cluster. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

> 🔍 **Deep Dive**
> The Kops instance could alternatively be a local Vagrant VM or any Linux machine. The instructor chooses EC2 for convenience, but the only requirements are: Linux OS, network access to AWS APIs, and the four tools installed (kops, kubectl, ssh-keygen, aws cli). The Kops instance never runs any Kubernetes workloads. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## 1.3 Prerequisites — The Four AWS Dependencies

Kops needs four things pre-configured in your AWS account before it can create a cluster:

### 1.3.1 IAM User with Administrator Access

Kops interacts with **many AWS services** during cluster creation — VPC, EC2, Auto Scaling Groups, S3, Route 53, EBS, Security Groups, Launch Templates, and more. Because the scope is so broad, the IAM user needs **administrator access** (the `AdministratorAccess` managed policy). An access key (access key ID + secret access key) is generated for this user and configured via `aws configure` on the Kops instance. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

### 1.3.2 S3 Bucket — Cluster State Store

Kops stores all cluster configuration and state in an **S3 bucket**. This is the single source of truth for the cluster's desired state. When you run `kops create cluster`, the configuration is written **only to this bucket** — no actual infrastructure is created yet. When you run `kops update cluster`, Kops reads from this bucket and creates the actual AWS resources. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

The bucket name must be **globally unique**. The instructor adds a number suffix (e.g., `kopsstate956`) to ensure uniqueness. Every subsequent Kops command must reference this bucket via the `--state` flag (or via an exported environment variable). [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

### 1.3.3 Route 53 Hosted Zone — DNS for Kubernetes

Kubernetes relies on DNS for internal and external communication. Kops uses a **Route 53 hosted zone** to create DNS records that map Kubernetes API endpoints to the actual IP addresses of cluster nodes. The hosted zone is a **subdomain** of a domain you already own. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

For example, if your domain is `hkhinfoteck.xyz` (on GoDaddy), you create a hosted zone in Route 53 for the subdomain `kubevpro.hkhinfoteck.xyz`. Kops will then automatically create records like `api.kubevpro.hkhinfoteck.xyz` pointing to the control plane node's public IP. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

### 1.3.4 Domain with DNS Delegation (NS Records)

This is the most conceptually complex prerequisite. You own a domain on an external registrar (GoDaddy in this case). You've created a subdomain hosted zone in Route 53. But there is a problem: **the internet doesn't know that your subdomain is managed by Route 53**. When someone (or kubectl) tries to resolve `api.kubevpro.hkhinfoteck.xyz`, the DNS resolver first goes to GoDaddy (because GoDaddy controls `hkhinfoteck.xyz`). GoDaddy has no record for `kubevpro`, so the resolution **fails immediately** — it never reaches Route 53. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

The solution is **DNS delegation**: you create **four NS (Name Server) records** in GoDaddy that tell the DNS system: *"For anything under `kubevpro.hkhinfoteck.xyz`, go ask these four Route 53 name servers."* The four NS server URLs are provided by Route 53 when you create the hosted zone. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

The resolution flow after delegation:

```
Client → "resolve api.kubevpro.hkhinfoteck.xyz"
  → GoDaddy (owns hkhinfoteck.xyz)
    → NS record for "kubevpro" → points to Route 53 name servers
      → Route 53 hosted zone
        → A record: api.kubevpro... → IP address of control plane
```

This delegation is a one-time setup. Once done, all DNS records that Kops creates in the Route 53 hosted zone are globally resolvable. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

> 🔍 **Deep Dive**
> The NS record delegation pattern is not Kops-specific — it is a general DNS architecture pattern. Whenever you want a subdomain managed by a different DNS provider than the parent domain, you create NS records in the parent domain pointing to the subdomain's name servers. This is how large organizations manage DNS across different teams or cloud providers. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## 1.4 The Two-Command Cluster Lifecycle

Kops uses a **plan-then-apply** model for cluster creation, directly analogous to Terraform's `plan` and `apply`:

**`kops create cluster`** — This command **only generates configuration**. It writes the cluster specification (node counts, instance sizes, zones, networking, DNS) to the S3 bucket. No AWS infrastructure is created. No EC2 instances are launched. No VPCs are provisioned. This is purely a configuration step. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**`kops update cluster --yes --admin`** — This command **reads the configuration from S3 and creates all the actual infrastructure**. It provisions the VPC, subnets, security groups, launch templates, auto-scaling groups, EC2 instances (control plane + worker nodes), EBS volumes, and DNS records. The `--yes` flag confirms that you want to apply (without it, Kops only shows what it would do — a dry run). The `--admin` flag generates admin-level kubeconfig credentials. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

This separation is powerful: you can review the configuration before committing resources. It also means cluster recreation is trivial — just re-run the two commands. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## 1.5 What Kops Creates Automatically

When `kops update cluster` executes, it creates a **complete infrastructure stack**: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

* **VPC** — A dedicated VPC for the Kubernetes cluster with all necessary subnets.
* **EC2 Instances** — One control plane (master) node and the specified number of worker nodes.
* **Auto Scaling Groups (ASGs)** — Three ASGs: one for the control plane, one for each worker node group. ASGs ensure nodes are replaced if they fail.
* **Launch Templates** — Define the instance configuration (AMI, instance type, volume, etc.) used by each ASG.
* **Security Groups** — Network firewall rules for all instances.
* **EBS Volumes** — Attached to each node with the specified size (12 GB in this lecture, but in production you should let Kops decide the appropriate size).
* **DNS Records in Route 53** — Automatically creates:
  * `api.kubevpro.hkhinfoteck.xyz` → public IP of the control plane (for external kubectl access)
  * `api.internal.kubevpro.hkhinfoteck.xyz` → private IP of the control plane (for internal cluster communication)

All of this infrastructure is **fully managed by Kops** — it creates it, and it can also **fully delete it** with a single command. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## 1.6 Kubeconfig — How kubectl Connects to the Cluster

When Kops creates the cluster, it also generates a **kubeconfig file** at `~/.kube/config` on the Kops instance. This file contains everything `kubectl` needs to communicate with the cluster: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

* **Server URL** — The API endpoint (e.g., `https://api.kubevpro.hkhinfoteck.xyz`). This is how kubectl knows where the control plane is.
* **Certificate information** — TLS certificates for secure communication.
* **Login credentials** — Authentication details for the admin user.

When you run `kubectl get nodes`, kubectl reads this config file, resolves the server URL via DNS (which goes through the GoDaddy → Route 53 delegation chain), connects to the control plane node, and retrieves the requested information. Without this file, kubectl has no idea where the cluster is or how to authenticate. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## 1.7 SSH Key Generation — Node Access

Kops requires an **SSH public key** to configure on the cluster nodes. This allows SSH access to the nodes if direct debugging is ever needed. The key is generated on the Kops instance using `ssh-keygen` and the public key path is provided to the `kops create cluster` command via the `--ssh-public-key` flag. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## 1.8 Cost Management — Create and Destroy Pattern

The instructor emphasizes cost awareness throughout. The cluster uses **t3.small** worker nodes and a **t3.medium** control plane — these are not free tier. The recommended workflow is: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

* **Create** the cluster when you need it (two commands).
* **Delete** the cluster when you are done (`kops delete cluster --yes`).
* **Shut down** the Kops EC2 instance after cluster deletion.
* **Power on** the Kops instance and re-create the cluster whenever needed.

The deletion command removes **everything** — instances, ASGs, VPC, DNS records, security groups — returning the AWS account to its pre-cluster state. The only thing that persists is the S3 bucket (state store) and the Route 53 hosted zone. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

> ⚠️ **Expert Note**
> The volume sizes are set to 12 GB explicitly to save costs. The instructor warns: *"In real time, don't give the size, let it create its own volume of its own size, which would be very much required for the production use case."* The 12 GB minimum is for learning only — production clusters need larger volumes for container images, logs, and etcd data. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a **Kubernetes cluster on AWS using Kops**. The final outcome: a working cluster with one control plane node and two worker nodes, accessible via `kubectl` from a dedicated Kops management EC2 instance. The cluster will have full DNS resolution, auto-scaling, and can be created and destroyed on demand. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Step 1: Launch the Kops EC2 Instance

Navigate to **AWS Console → EC2 → Launch Instance** (in the **us-east-1 / North Virginia** region).

| Field              | Value                                                 |
| ------------------ | ----------------------------------------------------- |
| **Name**           | `Kops`                                                |
| **AMI**            | Ubuntu 24 (free tier eligible)                        |
| **Instance type**  | `t2.micro`                                            |
| **Key pair**       | Create new: `Kops-key`, PEM format                    |
| **Security group** | Create new: `Kops-SG`, allow SSH (port 22) from My IP |

Click **Launch Instance**. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Why t2.micro:** This instance only runs CLI tools (kops, kubectl, aws cli). No heavy workloads. It is the management plane, not the data plane.

***

## Step 2: Create the IAM User

Navigate to **IAM → Users → Create User**.

| Field           | Value                                         |
| --------------- | --------------------------------------------- |
| **Name**        | `kops-admin`                                  |
| **Permissions** | Attach policy directly: `AdministratorAccess` |

After creation: click the user → **Security Credentials** → **Create access key** → select **CLI** → confirm → **Create access key**. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Keep this page open** or download the CSV — you will need the access key ID and secret access key in the next step.

***

## Step 3: SSH into Kops Instance and Install Tools

```bash
ssh -i <path-to-Kops-key.pem> ubuntu@<kops-public-ip>
```

Once connected, switch to root:

```bash
sudo -i
```

### 3a: Update Packages

```bash
apt update
```

### 3b: Install AWS CLI

```bash
snap install aws-cli --classic
```

| Part           | Meaning                                                   |
| -------------- | --------------------------------------------------------- |
| `snap install` | Installs a package using the Snap package manager         |
| `aws-cli`      | The AWS Command Line Interface                            |
| `--classic`    | Grants the snap full system access (required for aws-cli) |

### 3c: Configure AWS CLI

```bash
aws configure
```

You will be prompted for four values:

| Prompt                | Value                                                 |
| --------------------- | ----------------------------------------------------- |
| AWS Access Key ID     | Paste from IAM (Step 2)                               |
| AWS Secret Access Key | Paste from IAM (Step 2)                               |
| Default region name   | `us-east-1` (must match your intended cluster region) |
| Default output format | `json`                                                |

**Critical:** Verify the region matches where you want the cluster. The instructor emphasizes: *"Make sure you check the region name before you enter."* [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

### 3d: Generate SSH Keys

```bash
ssh-keygen
```

Press **Enter** three times (accept defaults — no passphrase). This creates: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

* Public key: `~/.ssh/id_ed25519.pub`
* Private key: `~/.ssh/id_ed25519`

**Verify the key name:**

```bash
ls ~/.ssh/
```

Note the exact public key filename — you will need it for the `kops create cluster` command. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

### 3e: Install Kops

Search "install kops" in your browser → follow the official documentation. Three commands: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

1. **Download the binary** (curl/wget command from documentation)
2. **Make it executable:** `chmod +x kops`
3. **Move to system path:** `mv kops /usr/local/bin/`

**Verify:**

```bash
kops
```

If installed correctly, you see the Kops help output with available commands. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

### 3f: Install kubectl

Search "install kubectl" → Kubernetes documentation → Install on Linux → use the **curl method**: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

1. **Download the binary** (curl command from documentation)
2. **Install (make executable + move to path):** use the `install` command from the documentation

**Verify:**

```bash
kubectl version --client
```

You should see the client version output. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Connection to larger flow:** The Kops instance now has all four required tools: aws-cli (configured), kops, kubectl, and SSH keys. The machine is ready to create the cluster.

***

## Step 4: Create the S3 Bucket (State Store)

Navigate to **AWS Console → S3 → Create bucket**.

| Field    | Value                                                          |
| -------- | -------------------------------------------------------------- |
| **Type** | General purpose                                                |
| **Name** | `kopsstate956` (must be globally unique — use your own suffix) |

Leave defaults. Click **Create bucket**. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Note down the bucket name** — it is required in every subsequent Kops command via the `--state` flag.

***

## Step 5: Create the Route 53 Hosted Zone

Navigate to **AWS Console → Route 53 → Create hosted zone**.

| Field           | Value                                                       |
| --------------- | ----------------------------------------------------------- |
| **Domain name** | `kubevpro.<your-domain>` (e.g., `kubevpro.hkhinfoteck.xyz`) |
| **Type**        | Public hosted zone                                          |

Click **Create hosted zone**. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**After creation:** Route 53 displays **four NS (Name Server) records** — these are the DNS servers that will hold all records for this subdomain. You need these values for the next step. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Important:** Use **your own domain name**, not the instructor's. The subdomain prefix (`kubevpro`) can be whatever you choose, but it must be consistent throughout all subsequent steps.

***

## Step 6: Create NS Records in GoDaddy (DNS Delegation)

Go to your domain registrar (GoDaddy in this case) → your domain → **DNS management**.

Add **four NS records**, all with the same name but different values: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

| Type | Name       | Value                      |
| ---- | ---------- | -------------------------- |
| NS   | `kubevpro` | 1st Route 53 NS server URL |
| NS   | `kubevpro` | 2nd Route 53 NS server URL |
| NS   | `kubevpro` | 3rd Route 53 NS server URL |
| NS   | `kubevpro` | 4th Route 53 NS server URL |

Copy each NS server URL from the Route 53 hosted zone (Step 5) and paste into the corresponding GoDaddy record. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Critical verification:** The `Name` field in GoDaddy must **exactly match** the subdomain prefix of your hosted zone. If your hosted zone is `kubevpro.yourdomain.com`, the name is `kubevpro`.

Click **Save all records**. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**What this achieves:** Any DNS query for `*.kubevpro.yourdomain.com` will now be directed from GoDaddy to Route 53's name servers, where the actual records (created automatically by Kops) will provide the answers.

***

## Step 7: Create the Cluster Configuration

Download the command file from the lecture resources (or use [326.kopscreate.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt?EntityRepresentationId=b9b39087-a910-4c27-9ffd-dc78d46daa05)) and modify the values for your setup. [\[326.kopscreate \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt)

Return to the Kops instance terminal (as root). Run:

```bash
kops create cluster \
  --name=kubevpro.hkhinfoteck.xyz \
  --state=s3://kopsstate956 \
  --zones=us-east-1a,us-east-1b \
  --node-count=2 \
  --node-size=t3.small \
  --control-plane-size=t3.medium \
  --dns-zone=kubevpro.hkhinfoteck.xyz \
  --node-volume-size=12 \
  --control-plane-volume-size=12 \
  --ssh-public-key ~/.ssh/id_ed25519.pub
```

**Flag-by-flag breakdown:**

| Flag                             | Meaning                                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| `--name`                         | The cluster name — must match your Route 53 hosted zone domain exactly                        |
| `--state`                        | S3 bucket where cluster config/state is stored (the bucket from Step 4)                       |
| `--zones`                        | AWS availability zones for the cluster (two zones for redundancy)                             |
| `--node-count=2`                 | Number of worker nodes to create                                                              |
| `--node-size=t3.small`           | Instance type for worker nodes                                                                |
| `--control-plane-size=t3.medium` | Instance type for the control plane (needs more resources — runs many Kubernetes services)    |
| `--dns-zone`                     | The Route 53 hosted zone domain (must match `--name`)                                         |
| `--node-volume-size=12`          | EBS volume size (GB) for worker nodes (12 GB minimum to save cost; omit in production)        |
| `--control-plane-volume-size=12` | EBS volume size (GB) for control plane (12 GB minimum; omit in production)                    |
| `--ssh-public-key`               | Path to the SSH public key generated in Step 3d (verify the exact filename with `ls ~/.ssh/`) |

 [\[326.kopscreate \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt), [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**What happens:** Configuration is written to the S3 bucket. **No infrastructure is created yet.** No EC2 instances, no VPC, nothing. This is a planning step only. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Step 8: Apply the Cluster Configuration (Create the Cluster)

```bash
kops update cluster \
  --name=kubevpro.hkhinfoteck.xyz \
  --state=s3://kopsstate956 \
  --yes --admin
```

| Flag      | Meaning                                                                                     |
| --------- | ------------------------------------------------------------------------------------------- |
| `--name`  | Cluster name (same as create command)                                                       |
| `--state` | S3 bucket path (required on every kops command)                                             |
| `--yes`   | Confirms you want to actually create infrastructure (without it, Kops only shows a dry run) |
| `--admin` | Generates admin-level kubeconfig credentials for kubectl access                             |

 [\[326.kopscreate \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt), [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**What happens:** Kops reads the configuration from S3 and begins creating all AWS resources — VPC, subnets, ASGs, launch templates, security groups, EC2 instances, EBS volumes, DNS records. **This takes approximately 15 minutes.** [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Important operational note:** Every Kops command requires the `--state` flag pointing to the S3 bucket. You can alternatively set an environment variable (`export KOPS_STATE_STORE=s3://kopsstate956`) to avoid repeating it, but the instructor does not do this since Kops commands are not run frequently. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Step 9: Validate the Cluster

Wait approximately **15 minutes** after the update command, then:

```bash
kops validate cluster \
  --name=kubevpro.hkhinfoteck.xyz \
  --state=s3://kopsstate956
```

**Expected output:** `Your cluster kubevpro.hkhinfoteck.xyz is ready` — followed by a list showing the control plane node and two worker nodes. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**If validation fails:** The cluster may still be provisioning. Wait a few more minutes and retry.

***

## Step 10: Verify kubectl Access

```bash
kubectl get nodes
```

**Expected output:** Three nodes listed — one control plane and two workers, all in `Ready` state. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**How this works internally:** kubectl reads `~/.kube/config` → finds the server URL (`https://api.kubevpro.hkhinfoteck.xyz`) → resolves via DNS (GoDaddy NS delegation → Route 53 → IP address of control plane) → connects to the control plane → retrieves node information. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Verify the kubeconfig file:**

```bash
ls -a ~ | grep .kube
cat ~/.kube/config
```

The config file contains the server URL, certificate data, and authentication credentials. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Step 11: Explore What Kops Created (Recommended)

Navigate through the AWS Console to see the infrastructure Kops built automatically: [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

| AWS Service                   | What to Look For                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| **EC2 → Instances**           | 1 control plane node + 2 worker nodes                                                      |
| **EC2 → Auto Scaling Groups** | 3 ASGs (1 master + 2 worker)                                                               |
| **EC2 → Launch Templates**    | Templates used by each ASG                                                                 |
| **EC2 → Security Groups**     | SGs attached to all cluster instances                                                      |
| **VPC**                       | A dedicated VPC for the Kubernetes cluster with subnets                                    |
| **Route 53 → Hosted Zone**    | `api.kubevpro...` → public IP of master; `api.internal.kubevpro...` → private IP of master |

**Verify DNS records match instance IPs:** Compare the public/private IPs of the control plane instance in EC2 with the IP addresses in the Route 53 records. They should match. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Step 12: Delete the Cluster (When Done)

```bash
kops delete cluster \
  --name=kubevpro.hkhinfoteck.xyz \
  --state=s3://kopsstate956 \
  --yes
```

| Flag      | Meaning                                                               |
| --------- | --------------------------------------------------------------------- |
| `--name`  | Cluster to delete                                                     |
| `--state` | S3 bucket with cluster state                                          |
| `--yes`   | Confirms deletion (without it, Kops only shows what would be deleted) |

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**What gets deleted:** EC2 instances, ASGs, launch templates, VPC, subnets, security groups, EBS volumes, DNS records. Everything Kops created is removed.

**What survives:** The S3 bucket and the Route 53 hosted zone remain (they were created manually, not by Kops).

**After deletion:** Shut down the Kops EC2 instance to save costs. Power it on whenever you need to re-create the cluster. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

**Timing:** Deletion takes several minutes — wait for completion before shutting down the Kops instance.

> ⚠️ **Expert Note**
> Always delete the cluster before shutting down the Kops instance. If you shut down the Kops instance first and later need to delete the cluster, you must power the instance back on — the kops binary, AWS credentials, and state bucket reference are all on that instance. Never leave the cluster running unattended — t3.small and t3.medium instances accumulate cost. [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
Kops = CLI tool that automates full Kubernetes cluster lifecycle on AWS
  Create → Validate → Use → Delete
  Two commands to create, one command to destroy
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Architecture Separation

```
Kops Instance (t2.micro)              Kubernetes Cluster
──────────────────────                ─────────────────────
NOT part of cluster                   Created BY Kops
Tools: kops, kubectl, aws-cli, ssh    Control plane (t3.medium) × 1
Purpose: management plane only        Workers (t3.small) × 2
Can shut down when cluster exists     Managed via ASGs
Can re-create cluster anytime         Full VPC + networking
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Four Prerequisites

```
1. IAM User → AdministratorAccess → access key → aws configure
2. S3 Bucket → cluster state store (globally unique name)
3. Route 53 Hosted Zone → subdomain (kubevpro.yourdomain.com) → public
4. DNS Delegation → 4 NS records in GoDaddy → point to Route 53 NS servers
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Tools on Kops Instance

```
apt update
snap install aws-cli --classic → aws configure (key, secret, region, json)
ssh-keygen → ~/.ssh/id_ed25519.pub
kops binary → download → chmod +x → mv /usr/local/bin/
kubectl binary → download → install → /usr/local/bin/
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## DNS Resolution Chain

```
kubectl get nodes
  → reads ~/.kube/config
    → server: https://api.kubevpro.hkhinfoteck.xyz
      → DNS resolver → GoDaddy (parent domain)
        → NS record "kubevpro" → Route 53 name servers
          → Route 53 hosted zone
            → A record: api.kubevpro... → control plane public IP
              → kubectl connects to control plane
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Two-Command Creation Model

```
kops create cluster [flags]     → writes config to S3 ONLY (no infra created)
                                     │
kops update cluster --yes --admin → reads S3 → creates ALL AWS infrastructure
                                     │
                              ~15 min wait
                                     │
kops validate cluster           → confirms: "cluster is ready"
```

 [\[326.kopscreate \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt), [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## What Kops Creates Automatically

```
kops update cluster --yes
  ├── VPC + subnets
  ├── Security Groups
  ├── Launch Templates
  ├── Auto Scaling Groups (×3: 1 master + 2 worker)
  ├── EC2 Instances (1 control plane + 2 workers)
  ├── EBS Volumes (attached to each node)
  ├── DNS Records in Route 53:
  │     ├── api.kubevpro...        → master PUBLIC IP
  │     └── api.internal.kubevpro... → master PRIVATE IP
  └── ~/.kube/config on Kops instance
        ├── server URL
        ├── certificates
        └── credentials
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## kops create cluster — Key Flags

```
--name          = cluster name = hosted zone domain (must match exactly)
--state         = s3://bucket  (required on EVERY kops command)
--zones         = AZs (us-east-1a,us-east-1b)
--node-count    = worker count (2)
--node-size     = worker instance type (t3.small)
--control-plane-size = master instance type (t3.medium)
--dns-zone      = Route 53 hosted zone domain (= --name)
--node-volume-size       = worker EBS GB (12 for learning; omit in prod)
--control-plane-volume-size = master EBS GB (12 for learning; omit in prod)
--ssh-public-key = path to pub key (~/.ssh/id_ed25519.pub — verify with ls)
```

 [\[326.kopscreate \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326.kopscreate.txt)

***

## Cluster Lifecycle Commands

```
CREATE:   kops create cluster [flags]
APPLY:    kops update cluster --name=... --state=s3://... --yes --admin
VALIDATE: kops validate cluster --name=... --state=s3://...
USE:      kubectl get nodes
DELETE:   kops delete cluster --name=... --state=s3://... --yes

Every kops command needs: --name + --state (or KOPS_STATE_STORE env var)
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## DNS Delegation Pattern (NS Records)

```
Parent domain (GoDaddy): hkhinfoteck.xyz
  └── NS record: "kubevpro" → 4 Route 53 NS server URLs

Subdomain (Route 53): kubevpro.hkhinfoteck.xyz
  └── A records auto-created by Kops

Effect: subdomain resolution delegated from GoDaddy → Route 53
One-time setup. Kops manages records within the zone automatically.
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Cost Management Pattern

```
NOT using cluster?
  1. kops delete cluster --yes  (removes ALL AWS resources)
  2. Stop Kops EC2 instance     (only AFTER deletion completes)

Need cluster again?
  1. Start Kops EC2 instance
  2. kops create cluster [flags]
  3. kops update cluster --yes --admin
  4. Wait ~15 min → kops validate cluster

Persists between cycles: S3 bucket, Route 53 hosted zone, GoDaddy NS records
Destroyed each cycle: VPC, instances, ASGs, SGs, volumes, DNS A records
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## kubeconfig Flow

```
kops update --admin
  └── generates ~/.kube/config
        └── kubectl reads it automatically
              ├── server: https://api.kubevpro... → DNS → control plane IP
              ├── certificate-authority-data → TLS
              └── credentials → authentication
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

## Reusable Engineering Patterns

**Plan-Then-Apply Pattern**

```
Step 1: Generate configuration (no side effects)
Step 2: Review / modify
Step 3: Apply configuration (creates infrastructure)

Kops:      create → update --yes
Terraform: plan   → apply
K8s:       dry-run → apply

Benefit: review before commit, reproducible, idempotent
```

**DNS Delegation Pattern**

```
Parent domain (registrar) → NS records → child DNS provider
  Decouples domain ownership from DNS management
  Enables cloud-native DNS (Route 53) with external domains
  Recurrence: any multi-provider DNS architecture
```

**Ephemeral Infrastructure Pattern**

```
Create when needed → use → destroy when done
  State externalized to S3 (survives destroy cycle)
  Infrastructure is disposable; state is permanent
  Recurrence: Kops, Terraform remote state, CodeBuild, spot instances
```

**Management Plane / Data Plane Separation**

```
Kops instance = management plane (lightweight, CLI tools, control point)
Cluster nodes = data plane (heavy, runs workloads, managed by ASGs)

Management plane can be powered off independently
Data plane lifecycle controlled from management plane
Recurrence: Ansible control node, Terraform workstation, CI/CD runners
```

 [\[326-kops-f...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/326-kops-for-k8s-setup.txt)

***

This completes the full reconstruction of the Kops Kubernetes setup lecture. **Theory** builds conceptual understanding of Kops architecture, DNS delegation, and the two-command model. **Practical** walks through every step from EC2 launch to cluster deletion with full command breakdowns. The **Compression Map** enables rapid recall of the architecture, resolution chain, lifecycle commands, and reusable patterns. Let me know if you'd like any section refined! 🚀
