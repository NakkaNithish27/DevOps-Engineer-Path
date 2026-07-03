# ☸️ Kubernetes Objects & Documentation — Deep Learning Material

**Source:** *Objects and Documentation* (Video Lecture Caption File) + Supporting Hands-On Command History File [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt), [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What Are Kubernetes Objects — The Fundamental Abstraction

In Docker, the fundamental unit you work with is a **container**. The instructor frames this as: "Container is an object in Docker." Kubernetes extends this thinking — it has its own set of **objects**, and these objects are the building blocks you create, configure, and manage. You don't directly manage containers in Kubernetes. Instead, you manage Kubernetes objects, and those objects manage containers for you. [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

This is a critical abstraction shift from Docker to Kubernetes. In Docker, you `docker run` a container and interact with it directly. In Kubernetes, you never touch containers directly — you define objects (in YAML files), apply them to the cluster, and Kubernetes handles the container lifecycle internally. The objects are your interface; the containers are an implementation detail managed by the system beneath.

***

## 1.2 Pod — The Smallest Deployable Object

A **Pod** is the smallest object you can create in Kubernetes. A container lives **inside** a Pod. The instructor emphasizes: "We do not directly touch containers. We manage Pods, and Pod in turn will manage containers for us." [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

This is the foundational relationship in Kubernetes: **you → Pod → container**. You define a Pod, specifying which container image to run, and Kubernetes creates the Pod, which creates and manages the container inside it. If the container crashes, the Pod can restart it. If the Pod is deleted, the container goes with it. The Pod is the wrapper, the management boundary, the scheduling unit.

A Pod can contain one or more containers (multi-container pods exist for sidecar patterns), but the most common pattern is one container per Pod. The detailed mechanics of Pods are covered in a dedicated lecture later in the course. [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

***

## 1.3 Service — Static Endpoints for Dynamic Pods

A **Service** provides a **static endpoint** to access Pods. The instructor compares it directly to a load balancer: "To have a static endpoint to your pod, like a load balancer." [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

Why is this needed? Pods are ephemeral — they can be created, destroyed, and recreated at any time, each time potentially getting a different IP address. If another component needs to reach a Pod, it can't rely on the Pod's IP address because that IP changes. A Service solves this by providing a **stable, unchanging address** that routes traffic to the correct Pod(s), regardless of how many times those Pods are recreated or rescheduled. This is the same problem that load balancers solve for EC2 instances — instances come and go, but the load balancer's DNS name stays the same.

***

## 1.4 ReplicaSet — Creating a Cluster of Identical Pods

A **ReplicaSet** creates and maintains a specified number of **identical Pod replicas**. The instructor describes it as: "to create a cluster of pods or replica of same pod." [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

If you need three instances of your web server running simultaneously (for redundancy, load distribution, or high availability), you don't create three separate Pod definitions. You create a ReplicaSet that specifies the desired count (3), the Pod template (what image to run, what ports to expose), and Kubernetes ensures that exactly 3 Pods matching that template are always running. If one Pod dies, the ReplicaSet creates a replacement. If there are too many, it removes the excess.

***

## 1.5 Deployment — The Most Important Object for DevOps

A **Deployment** works similar to a ReplicaSet — it manages Pod replicas — but adds the ability to **deploy new image tags** (rolling updates, rollbacks). The instructor shares a strong practical endorsement: "In my own experience, deployment is the most used object as far as DevOps is concerned because we are involved in a lot of deployments. And deployment object will help us do that." [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

A Deployment wraps a ReplicaSet and adds deployment strategy management. When you update the container image tag (e.g., from `v1` to `v2`), the Deployment orchestrates a rolling update: creating new Pods with the new image, verifying they're healthy, then terminating old Pods. If the new version fails, you can roll back to the previous version. This is the Kubernetes mechanism for zero-downtime deployments — the same concept as Beanstalk's rolling updates or blue-green deployments, but managed declaratively through the Deployment object.

***

## 1.6 ConfigMap and Secret — Externalized Configuration

**ConfigMap** stores **variables and configuration** data. **Secret** stores the same kind of information but for data that should **not be in clear text** — passwords, API keys, certificates. [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

Both serve the same architectural purpose: separating configuration from the container image. Instead of baking environment-specific values into the image (which would require a different image per environment), you store them in ConfigMaps/Secrets and inject them into Pods at runtime. This is the same logic/data separation pattern seen throughout the course: Ansible variables in `group_vars/`, Terraform variables in `.tfvars`, Docker environment variables in Compose files.

***

## 1.7 Volumes — Persistent Storage for Pods

Just like EC2 instances can have **EBS volumes** attached for persistent storage, Pods can have **volumes** attached. The instructor draws the direct parallel: "Just like we have EBS volumes for EC2 instances, we can have different kinds of volumes attached to our pod." [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

Kubernetes supports many volume types (cloud provider disks, NFS, local storage, etc.). Volumes solve the ephemeral storage problem: when a Pod is deleted, any data written inside the container is lost. Volumes persist data beyond the Pod's lifecycle, similar to how Docker volumes persist data beyond a container's lifecycle.

***

## 1.8 Kubernetes Documentation — Your Daily Reference

The instructor makes a strong operational point about Kubernetes documentation: "Whenever you are lost in Kubernetes, you can always refer to documentation. And let me tell you, they are very, very good. I use Kubernetes documentation every day." [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

The key insight: **you are not expected to memorize everything in Kubernetes.** Objects you use regularly will become second nature — their configuration, creation, updating, and editing. But Kubernetes has so many objects, options, and configurations that memorizing everything is impractical. The documentation is the operational reference you use constantly. [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

The instructor demonstrates searching for "Pod" in the documentation — finding the Pod page, reading about what a Pod is, seeing example YAML configurations, and finding the `kubectl apply` commands. The same process works for Deployments and every other object.

The instructor specifically notes that the example configurations look "similar to Docker Compose because it is in YAML format." This connects to the YAML lecture: the same data format skills apply — keys, values, lists, dictionaries, indentation. [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

***

## 1.9 Object Definition Files — YAML Configuration

Kubernetes objects are defined in **YAML files** (also called manifests or definition files). These files describe the desired state of the object — what image to run, how many replicas, what ports to expose, what volumes to mount. You apply these files using `kubectl apply -f <filename>`. <cite>turn19search23</cite>

The instructor shows three ways to apply object definitions:

1. **Create your own file** and apply it: `kubectl apply -f pod1.yaml`
2. **Download a file** from a URL and apply it locally
3. **Give a URL directly** to `kubectl apply`: `kubectl apply -f <URL>` — Kubernetes downloads and applies the definition in one step

The instructor notes: "There are many objects that are created, or should I say these definition files are created by different providers and vendors. You can give the link and you can directly apply objects." This means the Kubernetes ecosystem has a rich library of pre-built definitions you can use directly. [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

***

## 1.10 The Kubernetes Cluster Setup — Context from the Hands-On File

The hands-on command history reveals the complete cluster setup process that precedes working with objects: [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Toolchain installation:** The cluster is managed from an EC2 instance where three tools are installed:

* **AWS CLI** — for AWS API interaction (configured with `aws configure`)
* **kubectl** — the Kubernetes command-line tool for managing clusters and objects (downloaded from the official Kubernetes release URL)
* **kops** — Kubernetes Operations, a tool for creating, upgrading, and managing Kubernetes clusters on AWS (downloaded from GitHub releases)

**Cluster creation:** The `kops create cluster` command creates the Kubernetes cluster with specific parameters:

* `--name=kubevpro.groophy.in` — cluster name (DNS-based)
* `--state=s3://vproile-kops-state` — S3 bucket for storing cluster state (similar to Terraform state)
* `--zones=us-west-2a,us-west-2b` — availability zones for high availability
* `--node-count=2` — two worker nodes
* `--node-size=t3.small` — worker node instance type
* `--master-size=t3.medium` — master node instance type
* `--dns-zone=kubevpro.groophy.in` — DNS zone for the cluster
* `--node-volume-size=8` and `--master-volume-size=8` — 8GB EBS volumes

The cluster is materialized with `kops update cluster ... --yes --admin`. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

***

## 1.11 kubectl — The Object Management Interface

The hands-on file demonstrates the core `kubectl` commands for working with objects: [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Viewing objects:**

* `kubectl get nodes` — lists all nodes in the cluster
* `kubectl get nodes -o wide` — lists nodes with additional details (IPs, OS, kernel)
* `kubectl get pod` — lists all pods
* `kubectl get pod -o wide` — lists pods with node assignment and IP

**Inspecting objects in detail:**

* `kubectl describe node <name>` — detailed human-readable information about a node
* `kubectl get pod nginx -o yaml` — outputs the pod's full YAML definition (the complete object state)
* `kubectl get pod nginx -o json` — same information in JSON format
* `kubectl describe pod nginx` — detailed human-readable pod information

**Creating objects:**

* `kubectl apply -f pod1.yaml` — creates (or updates) the object defined in the YAML file
* `kubectl run nginx1 --image=nginx` — creates a pod imperatively (quick, ad-hoc, not using a file)

**Modifying objects:**

* `kubectl edit pod nginx1` — opens the pod definition in an editor for live modification

**Deleting objects:**

* `kubectl delete pod nginx` — removes the pod

The `-o yaml` and `-o json` output formats are especially important: they show you the **complete state** of any object, including fields you didn't explicitly set (Kubernetes fills in defaults). This is invaluable for understanding what Kubernetes actually created and for debugging misconfigurations. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up a Kubernetes cluster on AWS using kops, installing the management tools (kubectl, kops, AWS CLI), and then creating, inspecting, modifying, and deleting our first Kubernetes object — a Pod. This establishes the foundational workflow for all subsequent Kubernetes operations. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt), [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt)

***

## Step 1: Prepare the Management Instance

SSH into the EC2 instance that will serve as the Kubernetes management machine. Switch to root:

```bash
sudo -i
```

Generate SSH keys (used by kops to configure SSH access to cluster nodes):

```bash
ssh-keygen
```

Accept all defaults (press Enter through all prompts). [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

***

## Step 2: Install AWS CLI

```bash
sudo apt update
sudo apt install awscli -y
```

Configure AWS credentials:

```bash
aws configure
```

Enter your AWS Access Key ID, Secret Access Key, default region, and output format. These credentials allow kops and kubectl to interact with AWS APIs (creating EC2 instances, S3 buckets, Route53 records, etc.). [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

***

## Step 3: Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

**Line 1:** Downloads the latest stable kubectl binary. The inner `curl` command fetches the latest version string, which is embedded into the download URL.
**Line 2:** Installs the binary to `/usr/local/bin/` with proper ownership (root:root) and permissions (0755 — executable). [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Verify:**

```bash
kubectl
```

Should display the kubectl help text.

***

## Step 4: Install kops

```bash
curl -Lo kops https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
chmod +x kops
sudo mv kops /usr/local/bin/kops
```

**Line 1:** Downloads the latest kops binary from GitHub. The inner `curl` + `grep` + `cut` chain extracts the latest release tag from the GitHub API.
**Line 2:** Makes the binary executable.
**Line 3:** Moves it to the system path. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Verify:**

```bash
kops
```

Should display the kops help text.

***

## Step 5: Create the Kubernetes Cluster

```bash
kops create cluster \
  --name=kubevpro.groophy.in \
  --state=s3://vproile-kops-state \
  --zones=us-west-2a,us-west-2b \
  --node-count=2 \
  --node-size=t3.small \
  --master-size=t3.medium \
  --dns-zone=kubevpro.groophy.in \
  --node-volume-size=8 \
  --master-volume-size=8
```

This creates the cluster **definition** (stored in the S3 bucket) but doesn't yet create the AWS infrastructure. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Apply the cluster definition:**

```bash
kops update cluster --name kubevpro.groophy.in --state=s3://vproile-kops-state --yes --admin
```

* `--yes` — confirms you want to apply the changes (without it, kops only shows what would be created)
* `--admin` — generates admin-level kubeconfig credentials

**Wait** for the cluster to be fully ready (several minutes — EC2 instances must launch, Kubernetes components must start). [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Verify:**

```bash
kubectl get nodes
```

Should show 3 nodes (1 master + 2 workers) in `Ready` state. If nodes show `NotReady`, wait longer.

***

## Step 6: Explore Nodes — Output Formats

**Wide output:**

```bash
kubectl get nodes -o wide
```

Shows additional columns: internal/external IPs, OS image, kernel version, container runtime. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Describe a node (human-readable detail):**

```bash
kubectl describe node <node-name>
```

Replace `<node-name>` with a node name from the `get nodes` output (e.g., `ip-172-20-86-99.us-west-2.compute.internal`). Shows labels, conditions, capacity, allocated resources, running pods, and events.

**YAML output (full object definition):**

```bash
kubectl get nodes <node-name> -o yaml
```

Outputs the complete node object in YAML format — every field, every default, every status. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**JSON output:**

```bash
kubectl get nodes <node-name> -o json
```

Same information in JSON format. Useful for piping to `jq` or processing programmatically.

***

## Step 7: Create a Pod from a YAML File

Create a Pod definition file:

```bash
vim pod1.yaml
```

Write a basic Pod definition (based on the documentation example): [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
```

**Apply the definition:**

```bash
kubectl apply -f pod1.yaml
```

* `kubectl apply` — creates the object if it doesn't exist, or updates it if it does
* `-f pod1.yaml` — specifies the file containing the object definition

**Expected output:** `pod/nginx created` [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Verify:**

```bash
kubectl get pod
```

Should show the `nginx` pod with status `Running`.

```bash
kubectl get pod -o wide
```

Shows which node the pod was scheduled on and its IP address.

***

## Step 8: Inspect the Pod

**Full YAML definition:**

```bash
kubectl get pod nginx -o yaml
```

Shows the complete pod specification including all defaults that Kubernetes filled in (restart policy, DNS policy, service account, tolerations, etc.). [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**JSON format:**

```bash
kubectl get pod nginx -o json
```

Same data in JSON.

**Human-readable description:**

```bash
kubectl describe pod nginx
```

Shows events (scheduling, pulling image, starting container), conditions, volumes, and more. Especially useful for debugging — if a pod won't start, the events section shows why.

***

## Step 9: Delete the Pod

```bash
kubectl delete pod nginx
```

Removes the pod. Since this is a standalone pod (not managed by a Deployment or ReplicaSet), it's gone permanently — no automatic recreation. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

***

## Step 10: Create a Pod Imperatively (Without a YAML File)

```bash
kubectl run nginx1 --image=nginx
```

* `kubectl run` — creates a pod directly from the command line
* `nginx1` — pod name
* `--image=nginx` — container image to run

This is the **imperative** approach (tell Kubernetes exactly what to do right now). The YAML file approach is the **declarative** approach (describe the desired state, let Kubernetes figure out how to achieve it). Declarative is preferred for production; imperative is useful for quick testing. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Edit the pod live:**

```bash
kubectl edit pod nginx1
```

Opens the pod's YAML definition in the default editor. You can modify fields and save — Kubernetes applies the changes. [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)

**Verify:**

```bash
kubectl get pod
```

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Kubernetes Objects — The Core Set

```
POD           smallest unit, wraps container(s)
SERVICE       static endpoint for dynamic pods (like load balancer)
REPLICASET    maintains N identical pod replicas
DEPLOYMENT    ReplicaSet + rolling updates/rollbacks (MOST USED by DevOps)
CONFIGMAP     stores variables/config (plain text)
SECRET        stores sensitive data (not clear text)
VOLUME        persistent storage for pods (like EBS for EC2)
```

## Abstraction Chain

```
YOU → define objects (YAML)
  → kubectl apply → Kubernetes API
    → Kubernetes manages Pods
      → Pods manage Containers

You NEVER touch containers directly
Objects are your interface
```

## Object ↔ AWS Analogy

```
Pod          ↔  EC2 instance (runtime unit)
Service      ↔  Load Balancer (stable endpoint)
ReplicaSet   ↔  Auto Scaling Group (replica count)
Deployment   ↔  ASG + rolling deployment strategy
ConfigMap    ↔  Parameter Store / environment variables
Secret       ↔  Secrets Manager / KMS
Volume       ↔  EBS Volume
```

## kubectl Command Patterns

```
CREATE:   kubectl apply -f file.yaml    (declarative)
          kubectl run name --image=img  (imperative, quick test)

READ:     kubectl get <type>            (list)
          kubectl get <type> -o wide    (list + details)
          kubectl get <type> <name> -o yaml  (full YAML definition)
          kubectl get <type> <name> -o json  (full JSON definition)
          kubectl describe <type> <name>     (human-readable detail)

UPDATE:   kubectl edit <type> <name>    (live edit in editor)
          kubectl set image ...         (update image tag)

DELETE:   kubectl delete <type> <name>
```

## Three Ways to Apply Definitions

```
1. kubectl apply -f pod1.yaml           ← local file
2. Download file → kubectl apply -f     ← downloaded file
3. kubectl apply -f <URL>               ← direct URL (download + apply)
```

## Output Formats

```
default:   name + status (minimal)
-o wide:   + IP, node, additional columns
-o yaml:   complete object definition (ALL fields + defaults)
-o json:   same as yaml, JSON format
describe:  human-readable + events (best for debugging)
```

## Cluster Setup Toolchain

```
EC2 instance (management machine)
  ├─ AWS CLI (aws configure → credentials)
  ├─ kubectl (Kubernetes CLI → manage objects)
  └─ kops (Kubernetes Operations → create/manage clusters)
```

## kops Cluster Creation

```
kops create cluster \
  --name=kubevpro.groophy.in \
  --state=s3://vproile-kops-state \    ← state in S3 (like Terraform state)
  --zones=us-west-2a,us-west-2b \     ← multi-AZ
  --node-count=2 \                      ← 2 workers
  --node-size=t3.small \                ← worker instance type
  --master-size=t3.medium \             ← master instance type
  --node-volume-size=8 \                ← 8GB disks
  --master-volume-size=8

kops update cluster ... --yes --admin   ← actually creates infrastructure
kubectl get nodes                       ← verify (wait for Ready state)
```

## Documentation Usage

```
"I use Kubernetes documentation every day"
"You don't need to remember all this"

Workflow:
  1. Go to kubernetes.io/docs
  2. Search for the object type (Pod, Deployment, etc.)
  3. Read the description + example YAML
  4. Copy/modify the example for your use case
  5. kubectl apply -f

BOOKMARK kubernetes.io/docs → daily reference
```

## Pod YAML — Minimal Structure

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
```

## Declarative vs. Imperative

```
DECLARATIVE (preferred for production):
  Write YAML file → kubectl apply -f file.yaml
  Repeatable, version-controllable, reviewable

IMPERATIVE (quick testing):
  kubectl run nginx1 --image=nginx
  Fast, ad-hoc, not tracked in version control
```

## Debugging Flow

```
kubectl get pod           → status (Running/Pending/Error?)
kubectl describe pod name → events section (why is it failing?)
kubectl get pod name -o yaml → full definition (what was actually created?)
kubectl logs pod-name     → container stdout/stderr
```

## Reusable Engineering Patterns

**1. Objects as Abstraction Layer**

```
Docker: you manage containers directly
Kubernetes: you manage objects → objects manage containers

Pattern: add an abstraction layer between user and runtime
  → enables: auto-healing, scaling, rolling updates, scheduling
Same in: Terraform resources abstract cloud API calls
         Ansible modules abstract shell commands
```

**2. Documentation as Operational Companion**

```
Complex systems → impossible to memorize everything
Documentation = daily operational tool, not learning-phase reference

Pattern: master the structure of the docs, not the content
  Know WHERE to find things > memorize the things
Same in: Terraform provider docs, AWS docs, Ansible module index
```

**3. State Storage in External Bucket**

```
kops: cluster state in S3 bucket (--state=s3://...)
Terraform: state in S3 bucket (backend "s3")

Pattern: operational state stored externally, not locally
  → enables: team collaboration, disaster recovery, auditability
  → loss of state = loss of management ability
```

***

*This completes the full reconstruction. Theory explains every Kubernetes object type and the documentation-first approach to working with Kubernetes. Practical walks through the full cluster setup and the complete lifecycle of a Pod (create, inspect, modify, delete) using both declarative and imperative methods. The Compression Map enables instant recall of all object types, the kubectl command patterns, the AWS analogies, and the cluster creation flow.* [\[327-object...umentation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327-objects-and-documentation.txt), [\[327.Handon...8s_objects \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/327.Handon_K8s_objects.txt)
