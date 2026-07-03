# Minikube for Kubernetes Cluster Setup — Local Single-Node K8s Environment

**Source:** Video caption file — *"Minikube for K8s Setup"* (from a Kubernetes / DevOps course) [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is Minikube and Why It Exists

Minikube is a tool that creates a **single-node Kubernetes cluster** on your local machine for testing and learning purposes. A real Kubernetes cluster has multiple nodes — master nodes for control and worker nodes for running applications. Setting up a real multi-node cluster requires cloud infrastructure, networking, and significant configuration. Minikube simplifies all of this: it launches **one single VM** that acts as both master and worker, giving you a fully functional Kubernetes environment to practice on without any cloud cost or complex setup. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

The video positions Minikube as one of two cluster setup methods covered in this section — the other being **kops** (Kubernetes Operations), which creates production-grade multi-node clusters on AWS. Minikube is for local testing; kops is for real cloud deployments. This lecture focuses entirely on the Minikube path. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

The underlying mechanism: when you run `minikube start`, Minikube downloads a VM image and launches it on **Oracle VM VirtualBox** (which must already be installed on your system). This VM contains a complete Kubernetes installation — the API server, scheduler, controller manager, etcd, kubelet, and container runtime — all running on a single node. From the outside, it behaves like a real Kubernetes cluster; you interact with it using the same `kubectl` commands you'd use on a production cluster. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## 1.2 — kubectl: The Kubernetes CLI

`kubectl` (Kubernetes CLI) is the **command-line tool** used to interact with any Kubernetes cluster — whether it's a local Minikube cluster, a cloud-based kops cluster, an EKS cluster, or any other Kubernetes environment. It's the universal client for Kubernetes. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

In this setup, `kubectl` is installed alongside Minikube via Chocolatey using the package name `kubernetes-cli`. After installation, `kubectl` connects to the Minikube cluster automatically because Minikube configures the connection details during `minikube start`. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## 1.3 — The kubeconfig File: How kubectl Knows Which Cluster to Access

This is one of the most important conceptual topics in the lecture. When you run `kubectl get nodes` or any other kubectl command, how does kubectl know **which cluster to connect to**, **which user credentials to use**, and **where the API server is**? The answer is the **kubeconfig file**. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

The kubeconfig file is located at `~/.kube/config` (in your home directory). It is a YAML file that contains three critical sections: [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

### Clusters

This section contains the **cluster details** — the API server URL/address and the cluster name. For Minikube, it stores the address of the VM's API server and names the cluster `minikube`. In a multi-cluster setup, you could have entries for dev, staging, and production clusters all in the same kubeconfig file.

### Users

This section contains the **authentication credentials** — the client certificate and client key that prove your identity to the cluster. For Minikube, the user is named `minikube` and the credentials are the certificate and key generated during cluster setup. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

### Contexts

This is the section that **marries a user with a cluster**. The video explicitly explains: "Context marries the user with the cluster." A context entry says: "When using this context, connect to *this cluster* as *this user*." For Minikube, the context maps the `minikube` user to the `minikube` cluster. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

When you run `kubectl get nodes`, kubectl reads the kubeconfig file, finds the active context, resolves which cluster and user that context refers to, and uses those details to connect and authenticate. This is why kubectl works seamlessly after `minikube start` — Minikube automatically writes the cluster details, user credentials, and context into the kubeconfig file. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

🔍 **Deep Dive:**
The kubeconfig architecture is designed for **multi-cluster management**. In real DevOps work, you'll have multiple clusters (dev, staging, production, different regions). Each cluster gets an entry in the `clusters` section, each set of credentials gets an entry in `users`, and each combination gets a `context`. You switch between clusters by changing the active context (`kubectl config use-context <name>`) — you never need to modify kubectl itself or re-install anything. The kubeconfig file is the single routing layer between kubectl and all your clusters. This is the same **config-based routing** pattern seen with SSH config files mapping hosts to keys, and Ansible config files mapping settings to environments. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## 1.4 — Kubernetes Core Objects: Deployment, Pod, Service

The video tests the Minikube cluster by creating three fundamental Kubernetes objects. Understanding what they are conceptually is essential. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

### Deployment

A **Deployment** is a Kubernetes object that manages a set of identical pods. You tell the Deployment which container image to run and how many replicas you want, and it ensures that many pods are always running. If a pod dies, the Deployment automatically creates a replacement. The video creates a deployment named `hello-minikube` that fetches an image from Google Container Registry. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

### Pod

A **Pod** is the smallest deployable unit in Kubernetes — it's one or more containers running together on a single node. In this example, the Deployment creates one Pod, and that Pod runs the container from the `hello-minikube` image. The relationship: **Deployment manages Pods**. When you delete a Deployment, its Pods are also deleted. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

### Service

A **Service** is a Kubernetes object that exposes Pods to network traffic. Pods have dynamic internal IPs that can change — a Service provides a **stable endpoint** to access them. The video creates a Service of type **NodePort**, which exposes the application on a port on the node's IP address, making it accessible from outside the cluster. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

The relationship chain: **Deployment → creates/manages → Pod(s) → exposed by → Service → accessible via URL**. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## 1.5 — kops Setup Prerequisites (Brief Overview)

The video briefly outlines the kops setup that will be covered separately. The prerequisites listed provide a useful architectural overview of what a production Kubernetes cluster requires: [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

* **A domain name** — for Kubernetes DNS records (the video uses one purchased from GoDaddy).
* **A VM** with tools installed — kops, kubectl, SSH keys, AWS CLI.
* **AWS resources** — S3 bucket (to store kops cluster state), IAM user (for CLI access), Route 53 hosted zones (for DNS management). [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

This contrast highlights why Minikube exists — it eliminates all of this complexity for local testing. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## 1.6 — The Source Code Repository and Branch Strategy

The video uses the `vprofile-project` repository, specifically the `kubernetes-setup` branch. This branch contains directories for different setup methods (minikube, kops) with documentation and configuration files. The video instructs: if you've already cloned the repository, do a `git pull` to get the latest changes; if not, clone it fresh. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a local single-node Kubernetes cluster using Minikube on Windows, verifying it works by deploying a test application, and then performing a clean teardown. The final outcome: a working Kubernetes environment where you can create deployments, pods, and services — confirming readiness for the upcoming project where a Java application will be hosted on Kubernetes. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Execution Flow Overview

```
Phase 1: Install tools (Chocolatey → Minikube + kubectl)
Phase 2: Start cluster (minikube start)
Phase 3: Verify cluster (kubectl get nodes + kubeconfig)
Phase 4: Test with deployment + pod + service
Phase 5: Cleanup (delete resources → stop → delete cluster)
```

***

### Step 1: Clone or Update the Source Code Repository

**What we are doing:** Getting the project repository with the Kubernetes setup documentation.

**If not yet cloned:**

```bash
git clone <vprofile-project-url>
```

**If already cloned:**

```bash
cd vprofile-project
git pull
```

This ensures you have the latest changes including the Kubernetes setup branch content. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Switch to the setup branch:**

```bash
git checkout kubernetes-setup
```

Navigate into the `minikube` directory — it contains a documentation file with all the setup steps. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

### Step 2: Install Chocolatey (If Not Already Installed)

**What we are doing:** Installing the Windows package manager that will install Minikube and kubectl.

1. Open **PowerShell as Administrator** (right-click → Run as Administrator).
2. Run the Chocolatey installation command (available from chocolatey.org or the project documentation). [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Failure scenario:** If you get a "restricted" or "not allowed" error, **temporarily turn off your antivirus**, run the command, then re-enable antivirus. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Expected output:** Chocolatey version confirmation message.

3. **Close PowerShell and reopen as Administrator** — this ensures the `choco` command is available in the new session.

***

### Step 3: Install Minikube and kubectl via Chocolatey

**What we are doing:** Installing both the Minikube cluster tool and the Kubernetes CLI in one step.

```bash
choco install minikube kubernetes-cli
```

**Breakdown:**

* `choco install` — Chocolatey's install command.
* `minikube` — the Minikube tool (creates and manages the local K8s cluster).
* `kubernetes-cli` — kubectl (the command-line client for interacting with any Kubernetes cluster). [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Expected output:** Installation progress for both packages, ending with version confirmations.

**After installation:** Close PowerShell. You can now switch to **Git Bash** which the video describes as "much more convenient." [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Verify Minikube is available:**

```bash
minikube
```

If the command is not found, close and reopen Git Bash. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Pre-requisite check:** Oracle VM VirtualBox must already be installed on your system. Minikube will launch its VM on VirtualBox.

***

### Step 4: Start the Minikube Cluster

**What we are doing:** Creating and starting the single-node Kubernetes cluster.

```bash
minikube start
```

**What happens internally:**

1. Minikube downloads a VM image (first time only).
2. It creates a VM on Oracle VM VirtualBox.
3. Inside the VM, it installs and configures all Kubernetes components (API server, scheduler, controller manager, etcd, kubelet).
4. It writes cluster connection details to `~/.kube/config` (kubeconfig file). [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**This takes time** — the download and VM provisioning can take several minutes on first run.

**Expected output:** "Done. The Kubernetes cluster is up." [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**How to verify visually:** Open Oracle VM VirtualBox — you should see a new VM created by Minikube.

***

### Step 5: Verify the Cluster

**What we are doing:** Confirming the cluster is running and kubectl can connect to it.

```bash
kubectl get nodes
```

**Expected output:** One node listed with status `Ready` — this is the master node (which also serves as a worker in Minikube's single-node architecture). [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Examine the kubeconfig file:**

```bash
cat ~/.kube/config
```

**What to look for:**

* **Cluster section:** Server URL and cluster name (`minikube`).
* **User section:** User name (`minikube`) with client certificate and client key paths.
* **Context section:** Context mapping `minikube` user to `minikube` cluster. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Connection to flow:** This kubeconfig file is what makes `kubectl get nodes` work — kubectl reads it to know where the cluster is and how to authenticate.

***

### Step 6: Test — Create a Deployment

**What we are doing:** Creating a test Deployment to verify the cluster can run workloads.

```bash
kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4
```

**Breakdown:**

* `kubectl create deployment` — creates a Deployment object.
* `hello-minikube` — the name of the Deployment.
* `--image=k8s.gcr.io/echoserver:1.4` — the container image to run (a simple echo server from Google Container Registry). [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Verify the Deployment:**

```bash
kubectl get deploy
```

**Expected output:** The `hello-minikube` deployment listed with 1/1 ready. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Verify the Pod:**

```bash
kubectl get pod
```

**Expected output:** One pod running, created by the deployment. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Relationship confirmed:** The Deployment created and manages the Pod.

***

### Step 7: Test — Expose the Deployment as a Service

**What we are doing:** Creating a Service to make the application accessible from outside the cluster.

```bash
kubectl expose deployment hello-minikube --type=NodePort --port=8080
```

**Breakdown:**

* `kubectl expose deployment` — creates a Service for the specified Deployment.
* `hello-minikube` — the Deployment to expose.
* `--type=NodePort` — the Service type. NodePort exposes the service on a port on the node's IP, making it accessible externally.
* `--port=8080` — the port the application listens on inside the container. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Get the URL to access the service:**

```bash
minikube service hello-minikube --url
```

**Expected output:** A URL (like `http://192.168.99.100:31234`) that you can open in a browser. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Verify in browser:** Open the URL — you should see a response from the echo server, confirming the entire chain works: Deployment → Pod → Service → accessible externally.

***

### Step 8: Cleanup — Delete Resources and Cluster

**What we are doing:** Removing all test resources and tearing down the cluster to free system resources.

**Check services:**

```bash
kubectl get svc
```

**Delete the service:**

```bash
kubectl delete svc hello-minikube
```

**Delete the deployment (which also deletes its pods):**

```bash
kubectl delete deploy hello-minikube
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Stop the cluster:**

```bash
minikube stop
```

This shuts down the VM but preserves it — you can `minikube start` later to bring it back. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**Delete the cluster entirely:**

```bash
minikube delete
```

This removes the VM completely from VirtualBox. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

**How to verify:** Open Oracle VM VirtualBox — the Minikube VM should be gone.

**Connection to flow:** Minikube setup is complete. The next project will use a Kubernetes cluster (either Minikube or kops) to host the vProfile Java application. [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Minikube — Local Kubernetes Cluster Setup
PURPOSE:  Single-node K8s cluster for testing/learning on local machine
CONTEXT:  Setup lecture before hosting Java app on Kubernetes
SCOPE:    Minikube only (kops covered separately)
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Minikube Architecture

```
LOCAL MACHINE (Windows)
  │
  ├── Chocolatey (package manager)
  │     ├── minikube (cluster tool)
  │     └── kubernetes-cli (kubectl)
  │
  ├── Oracle VM VirtualBox (hypervisor)
  │     └── Minikube VM (single node)
  │           ├── Master components (API server, scheduler, controller, etcd)
  │           └── Worker components (kubelet, container runtime)
  │
  └── ~/.kube/config (kubeconfig file)
        ├── clusters: [minikube → server URL]
        ├── users: [minikube → cert + key]
        └── contexts: [minikube → cluster:minikube + user:minikube]

kubectl → reads kubeconfig → connects to Minikube VM API server
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## kubeconfig File Structure (Critical)

```
~/.kube/config

clusters:                    ← WHERE to connect
  - name: minikube
    server: https://<vm-ip>:<port>

users:                       ← WHO you are
  - name: minikube
    client-certificate: ...
    client-key: ...

contexts:                    ← MARRIES user + cluster
  - name: minikube
    cluster: minikube
    user: minikube

"Context marries the user with the cluster"

kubectl get nodes → reads kubeconfig → uses active context → connects
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Kubernetes Object Hierarchy (Test Flow)

```
Deployment (hello-minikube)
    │ creates/manages
    ▼
Pod (container running echoserver:1.4)
    │ exposed by
    ▼
Service (NodePort on port 8080)
    │ accessible via
    ▼
URL (minikube service --url)
    │
    ▼
Browser → sees response ✅

DELETE ORDER (reverse):
  1. kubectl delete svc hello-minikube
  2. kubectl delete deploy hello-minikube  ← also deletes pods
  3. minikube stop                         ← stops VM
  4. minikube delete                       ← removes VM entirely
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Installation Sequence

```
1. PowerShell (Admin) → install Chocolatey
   └── Error? Turn off antivirus temporarily
2. Close PowerShell → Reopen as Admin
3. choco install minikube kubernetes-cli
4. Close PowerShell → Switch to Git Bash
5. minikube start  ← downloads image + creates VM + configures K8s
   └── Requires: Oracle VM VirtualBox pre-installed
6. kubectl get nodes  ← verify cluster is up (1 node, Ready)
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Key Commands Quick Reference

```
COMMAND                                      PURPOSE
───────                                      ───────
choco install minikube kubernetes-cli         Install tools
minikube start                               Create + start cluster
minikube stop                                Stop cluster (preserves VM)
minikube delete                              Delete cluster (removes VM)
kubectl get nodes                            List cluster nodes
kubectl create deployment <name> --image=<>  Create deployment
kubectl get deploy                           List deployments
kubectl get pod                              List pods
kubectl expose deployment <name> --type=NodePort --port=<>  Create service
kubectl get svc                              List services
minikube service <name> --url                Get external URL for service
kubectl delete svc <name>                    Delete service
kubectl delete deploy <name>                 Delete deployment + its pods
cat ~/.kube/config                           View cluster connection config
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Minikube vs kops

```
ASPECT          MINIKUBE                     KOPS
──────          ────────                     ────
Nodes           1 (single VM)                Multiple (master + workers)
Location        Local machine (VirtualBox)   AWS (EC2 instances)
Purpose         Testing / learning           Production / real deployment
Prerequisites   Chocolatey + VirtualBox      Domain, S3, IAM, Route53, AWS CLI
Cost            Free (local)                 AWS charges
Setup Time      Minutes                      Longer (cloud provisioning)
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## kops Prerequisites (Mentioned, Not Executed)

```
REQUIREMENT                PURPOSE
───────────                ───────
Domain name (GoDaddy)      Kubernetes DNS records
VM with tools              kops, kubectl, SSH keys, AWS CLI
S3 bucket                  Store kops cluster state
IAM user                   AWS CLI authentication
Route 53 hosted zones      DNS management for cluster
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Source Code Setup

```
git clone <vprofile-project>     ← if new
git pull                         ← if already cloned (get latest)
git checkout kubernetes-setup    ← branch with K8s setup docs

STRUCTURE:
  vprofile-project/
    └── kubernetes-setup/
          ├── minikube/          ← this lecture
          └── kops/              ← next lecture
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Lifecycle States

```
minikube start   → VM created → cluster running → kubeconfig written
minikube stop    → VM stopped → cluster paused → kubeconfig preserved
minikube start   → VM restarted → cluster resumes
minikube delete  → VM removed → cluster gone → VirtualBox clean
```

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## Reusable Engineering Patterns

| Pattern                                   | Manifestation                                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Config-Based Connection Routing**       | kubeconfig maps kubectl → cluster via context (same pattern as SSH config, Ansible config)      |
| **Context = User + Cluster Marriage**     | Contexts decouple "who" from "where" — switch clusters by switching context, not credentials    |
| **Single-Node for Testing**               | Minikube collapses master + worker into one VM — full API compatibility, minimal resources      |
| **Object Hierarchy Management**           | Deployment → Pod → Service = layered abstraction; delete parent cascades to children            |
| **Tool Installation via Package Manager** | Chocolatey installs both minikube and kubectl — reproducible, version-managed setup             |
| **Verify-Before-Use**                     | `kubectl get nodes` after start, `minikube service --url` after expose — validate each layer    |
| **Clean Teardown Discipline**             | Delete resources → stop cluster → delete cluster — orderly reverse of creation                  |
| **Branch-Based Project Organization**     | `kubernetes-setup` branch contains all K8s setup docs — isolated from application code branches |

 [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

## One-Line System Reconstruction

> **Minikube creates a single-node Kubernetes cluster as a VirtualBox VM (`minikube start`), auto-configures `~/.kube/config` (kubeconfig) with cluster address, user credentials, and context that "marries user with cluster" — enabling `kubectl` to manage the cluster identically to production, tested by creating a Deployment (manages Pods) exposed via a NodePort Service (accessible by URL), and cleaned up via `kubectl delete` → `minikube stop` → `minikube delete` — installed on Windows through Chocolatey (`choco install minikube kubernetes-cli`) with VirtualBox as the prerequisite hypervisor.** [\[325-miniku...-k8s-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/325-minikube-for-k8s-setup.txt)

***

This completes the full reconstruction of the Minikube for Kubernetes Setup lecture. It establishes the local Kubernetes environment and the fundamental kubectl/kubeconfig concepts needed for the upcoming project where the vProfile Java application will be deployed on a Kubernetes cluster. The kops setup for production-grade AWS clusters will be covered in a separate lecture. Let me know if you'd like any section expanded or adjusted! 🚀
