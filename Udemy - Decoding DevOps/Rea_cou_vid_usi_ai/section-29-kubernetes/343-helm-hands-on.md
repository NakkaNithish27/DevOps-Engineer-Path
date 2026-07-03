# ⎈ Helm Hands-On — WordPress on Kubernetes with Helm Charts — Deep Learning Material

**Source:** Video caption file — [343-helm-hands-on.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt?EntityRepresentationId=483dde15-8557-4eb1-aa5b-d271a80ed858) [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**Video Context:** The instructor builds a WordPress + MySQL application on Kubernetes, progressing through three layers: first, understanding the raw Kubernetes definition files (generated via Amazon Q Developer); second, understanding the Helm chart structure (created with `helm create`); third, manually converting Kubernetes files into Helm templates with variables. The lecture bridges from "I have Kubernetes YAML files" to "I understand what Helm charts are and how they templatize Kubernetes definitions." Full Helm chart creation with AI assistance is deferred to the next lecture.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Setup Chain — Prerequisites Before Helm

The instructor establishes the prerequisites: a running Kubernetes cluster (created with Kops on AWS) and an Nginx Ingress Controller installed (from a previous ingress exercise). Additionally, the kubeconfig file must be accessible from the local machine — the instructor copies the kubeconfig from the Kops instance to the local `~/.kube/config` file so that `kubectl` commands from the local terminal and VS Code can reach the cluster. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

This is an operational chain: **Kops creates cluster → Ingress controller installed → kubeconfig copied locally → kubectl works locally → VS Code can interact with cluster → Helm can deploy to cluster**.

***

## 1.2 The WordPress Application — What We're Deploying

The application consists of two main components: **WordPress** (the web application) and **MySQL** (the database). Each requires multiple Kubernetes objects: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**For MySQL:** A Deployment (running the MySQL 8.0 container), a Service (exposing port 3306 internally), a PVC (Persistent Volume Claim for database storage), and database credentials stored in a Secret.

**For WordPress:** A Deployment (running the WordPress container), a Service (exposing the application), a PVC (for WordPress content storage), and database connection variables (referencing the Secret).

**Connecting them:** An Ingress resource (Nginx type) that routes external traffic to the WordPress service via a hostname/domain.

The instructor finds the official Kubernetes documentation for deploying WordPress + MySQL, examines the definition files, and notes the key elements: MySQL environment variables (`MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`) sourced from Secrets, PVCs mapped as volumes to container mount points (`/var/lib/mysql` for MySQL, `/var/www/html` for WordPress), and the WordPress service originally defined as type LoadBalancer (which the instructor replaces with Ingress). [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

***

## 1.3 Persistent Volume Claims (PVC) and StorageClass — How Storage Works

This is one of the most important conceptual explanations in the lecture. The instructor explains the complete chain from PVC to actual storage: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

A **StorageClass** is a Kubernetes object that defines *how* storage is provisioned. The instructor runs `kubectl get sc` (sc = storageclass) and shows a default StorageClass named `default` with provisioner `aws-ebs`. This StorageClass was automatically created when the Kubernetes cluster was set up with Kops on AWS. It tells Kubernetes: "When someone requests storage, create an AWS EBS volume."

A **Persistent Volume Claim (PVC)** is a *request* for storage. The PVC definition file specifies: a name (e.g., `mysql-pvc`), access mode (`ReadWriteOnce`), storage class name (`default`), and the requested size (e.g., `1Gi`). [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

When you submit a PVC to Kubernetes: "It's going to go and talk to this StorageClass, which in turn will create an EBS volume of 1 GB size." The StorageClass acts as the **provisioner** — it knows how to create actual storage on the underlying infrastructure. The PVC is the abstract request; the StorageClass translates it into real infrastructure.

The volume is then **mounted** into the pod through two steps in the Deployment definition:

1. **`volumes`** section: declares a volume name and references the PVC by name (`persistentVolumeClaim: claimName: mysql-pvc`)
2. **`volumeMounts`** section: mounts that volume name to a specific path inside the container (`mountPath: /var/lib/mysql`)

The chain: **PVC (request) → StorageClass (provisioner) → EBS Volume (actual storage) → Volume (K8s abstraction) → VolumeMount (container mount point)**. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

🔍 **Deep Dive:** The `ReadWriteOnce` access mode means the volume can be mounted as read-write by a **single node**. This is important for database workloads — you don't want two MySQL pods writing to the same disk simultaneously. Other modes include `ReadOnlyMany` (multiple nodes can read) and `ReadWriteMany` (multiple nodes can read-write, requires special storage like EFS/NFS).

***

## 1.4 Using AI Code Assistants for Kubernetes Files — Amazon Q Developer

The instructor demonstrates using **Amazon Q Developer** (VS Code extension) to generate all the Kubernetes definition files instead of manually copying from documentation. The prompt is detailed and specific: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

*"WordPress setup Kubernetes definition files. Separate files for WordPress app, MySQL app, service, DB service, PVC and ingress. PVC should use storage class default. Secret file should contain all db users and db password for MySQL and WordPress both. Ingress will be nginx with hostname \[domain]."*

The instructor emphasizes that **this prompt didn't come from the first attempt**: "The reason this prompt is so long is because I tried other things. Few attempts to get the right prompt. First it was giving everything in one single file. The storage class was not default, something else, and the secret file was also a little scrambled. So slowly I got to this prompt." [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

He also notes the need to **verify and correct** AI output — the generated MySQL image version was wrong ("There is no 5.0. It's going to throw error. Make sure you change that. Or better put this in the prompt itself"). This reinforces the same AI collaboration principle from the bash scripting section: skills + AI = effective output; AI alone = potential errors. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

The instructor tested multiple AI tools: "I tried GitHub Copilot, different other generative AI, ChatGPT, many other things... Amazon Q was the one that got everything correct" for Helm/K8s work. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

***

## 1.5 Helm — Why It Exists and What Problem It Solves

The instructor doesn't give a formal Helm introduction (it was covered in a previous theory lecture), but the practical motivation is clear from context: the WordPress application requires **7+ separate YAML files** (MySQL deployment, MySQL service, MySQL PVC, WordPress deployment, WordPress service, WordPress PVC, Secret, Ingress). Each file has hardcoded values (image names, tags, replica counts, storage sizes, database names, passwords, hostnames). [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

If you want to deploy this application to a different environment (different domain, different storage size, different database credentials), you'd need to manually edit values across multiple files. Helm solves this by **templatizing** the YAML files — replacing hardcoded values with variables that are defined in a single `values.yaml` file. Change the values in one place, and all templates pick up the changes.

***

## 1.6 The `helm create` Command — Scaffold Structure

The instructor runs `helm create wp-chart`, which generates a complete Helm chart scaffold. The generated structure: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

```
wp-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── serviceaccount.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── NOTES.txt
│   └── tests/
│       └── test-connection.yaml
```

The instructor examines three key components:

### `Chart.yaml` — Chart Identity and Versioning

Contains the chart's name, description, type, and **two version fields**: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**`version`** — the **chart version**. "This version number should be incremented each time you make changes to the chart and its templates." This tracks changes to the Helm chart itself — the templates, the structure, the variable definitions.

**`appVersion`** — the **application version**. "This is different. This is the chart version. This is your application version." For WordPress, this would be the WordPress version. For a custom app, it would be the release version from CI/CD. Chart version and app version evolve independently — you can update the chart (change a template) without changing the app version, or deploy a new app version without changing the chart structure.

### `values.yaml` — The Variable Store

Contains all configurable values as YAML variables. The instructor shows examples: `replicaCount: 1`, `image.repository`, `image.tag`, `autoscaling.enabled: false`. These values are referenced from templates using `{{ .Values.variableName }}` syntax. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### `templates/` — Templatized Kubernetes Definitions

Contains Kubernetes YAML files with **Go template syntax** instead of hardcoded values. The instructor examines `deployment.yaml` and breaks down the templating: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

***

## 1.7 Helm Template Syntax — How Variables Work

The core mechanism: **double curly braces `{{ }}` contain expressions** that are evaluated when the chart is rendered. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**`{{ include "wp-chart.fullname" . }}`** — the `include` function imports a named template (defined in `_helpers.tpl`). `wp-chart.fullname` generates the full name of the chart, used as the Deployment name. This ensures consistent naming across all resources.

**`{{ .Values.replicaCount }}`** — references the `replicaCount` variable from `values.yaml`. "When it says `values`, it's going to check the `values.yaml` file. And that's going to look for a variable called `replicaCount`." The dot notation traverses the YAML hierarchy. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**Conditional logic:** The instructor shows a condition in the scaffold's deployment template:

```yaml
{{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
{{- end }}
```

This reads: "If `autoscaling.enabled` is not true, then set replicas to `replicaCount`." The instructor traces it: "So `values.autoscaling.enabled` — once again we go to `values.yaml` file, we look for the variable `autoscaling`, in that you have another variable `enabled`. Its value is `false`." Since it's false, `not false` = true, so the replicas line is included. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

***

## 1.8 Converting Kubernetes Files to Helm Templates — The Manual Process

The instructor demonstrates the manual conversion process: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**Step 1:** Delete all the default scaffold templates (they're examples, not needed for the WordPress chart). Also delete the tests folder. Clear the `values.yaml` file content.

**Step 2:** Copy the actual Kubernetes definition files (MySQL deployment, WordPress deployment, services, PVCs, secret, ingress) into the `templates/` folder.

**Step 3:** In each template file, replace hardcoded values with template expressions. The instructor demonstrates two types of replacements:

**Using built-in chart helpers** for names:

```yaml
# Before:
name: mysql-deployment
# After:
name: {{ include "wp-chart.fullname" . }}-app
```

**Using custom variables** for configurable values:

```yaml
# Before:
image: mysql:8.0
# After:
image: {{ .Values.mysql.image.repository }}:{{ .Values.mysql.image.tag }}
```

**Step 4:** Define the corresponding variables in `values.yaml`:

```yaml
mysql:
  image:
    repository: mysql
    tag: "8.0"
```

The instructor notes that VS Code (with Amazon Q) even suggests the template syntax as he types — "it's already code suggested me." [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

The key teaching point: "I wanted you to understand the structure of Helm chart. So when you develop Helm charts by using any code assistant, and if things don't work as you expected, you know what to change, where." Understanding the manual process enables effective use of AI tools — you can debug and fix what AI generates. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

***

## 1.9 DNS Configuration — The Ingress Hostname

The Ingress definition uses a hostname (the instructor's purchased domain). He notes: "Make sure you change this with the domain that you have. You have created a hosted zone. The domain that you purchased. Make sure that domain is there because we're going to also need to edit those DNS records." He mentions using GoDaddy for DNS and adding a WordPress entry. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a **WordPress + MySQL application on Kubernetes**, first as raw definition files (generated via AI), then understanding the **Helm chart structure** by scaffolding with `helm create`, and finally beginning the manual conversion of Kubernetes files into Helm templates. The final outcome of this lecture: understanding Helm chart architecture well enough to use AI assistants effectively in the next lecture for full chart creation. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

***

## Phase A: Environment Setup

### Step A1: Ensure Kubernetes Cluster and Ingress Controller

Your cluster must be running (Kops) and the Nginx Ingress Controller must be installed (from the previous ingress exercise). [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step A2: Copy Kubeconfig to Local Machine

On the Kops instance, view the kubeconfig:

```bash
cat ~/.kube/config
```

Copy the **entire content**. On your local machine: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

```bash
mkdir -p ~/.kube
vim ~/.kube/config
# Paste the content, save and exit
```

If you already have a kubeconfig, replace the existing content.

### Verify local kubectl access:

```bash
kubectl get nodes
```

**Expected result:** Your cluster nodes listed. This confirms local kubectl can reach the remote cluster. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step A3: Install Helm

**Mac:**

```bash
brew install helm
```

**Windows (Chocolatey as administrator):**

```bash
choco install kubernetes-helm
```

 [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step A4: Install Amazon Q Extension in VS Code

Go to **Extensions** → search for **Amazon Q** → install. Click the Amazon Q icon in the sidebar → **Use for Free → Continue**. Sign in with your AWS account email, complete verification, and allow VS Code access. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**If login gets stuck:** Sign out, close VS Code, reopen, and try signing in again.

***

## Phase B: Generate Kubernetes Definition Files

### Step B1: Create the Project Folder

Create a folder named `wordpress-k8s` (or similar) anywhere on your system. Open it in VS Code (**File → Open Folder**). [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step B2: Check the StorageClass

```bash
kubectl get sc
```

**Expected output:** A StorageClass named `default` with provisioner `aws-ebs`. This is auto-created by Kops on AWS. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**Why this matters:** Your PVC definitions must reference this exact StorageClass name (`default`). If the name is different, update accordingly.

### Step B3: Generate Files with Amazon Q

Open the Amazon Q chat in VS Code. Enter the prompt (adapt the domain to yours): [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

```
WordPress setup Kubernetes definition files. Separate files for WordPress app, 
MySQL app, service, DB service, PVC and ingress. PVC should use storage class 
default. Secret file should contain all db users and db password for MySQL and 
WordPress both. Ingress will be nginx with hostname wordpress.<your-domain>.
```

**Wait** for Amazon Q to generate all files (it takes longer than other assistants but produces better K8s results per the instructor's experience). [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step B4: Review and Fix Generated Files

Click the insert/accept button for each generated file. Then verify: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**Critical fix:** Check the MySQL image version. If it says `mysql:5.0`, change it to `mysql:8.0` — "There is no 5.0. It's going to throw error." [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**PVC sizes:** The instructor reduces MySQL PVC to `1Gi` and WordPress PVC to `2-3Gi` (from the generated defaults of 10Gi/5Gi) to minimize EBS costs. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**Review all files for:** correct image names/tags, correct StorageClass name (`default`), correct port numbers (3306 for MySQL, 80 for WordPress), Secret references matching across files, Ingress hostname matching your domain.

**The instructor provides these files in the lecture resources** as an alternative to generating them yourself. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step B5: Understand the PVC-to-Deployment Connection

In `mysql-pvc.yaml`:

```yaml
metadata:
  name: mysql-pvc
spec:
  storageClassName: default
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 1Gi
```

In `mysql-deployment.yaml`:

```yaml
volumes:
  - name: mysql-storage           # volume name (internal reference)
    persistentVolumeClaim:
      claimName: mysql-pvc        # must match PVC name above
volumeMounts:
  - name: mysql-storage           # must match volume name above
    mountPath: /var/lib/mysql     # where data is stored inside container
```

 [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**The chain:** PVC name → referenced in volumes.persistentVolumeClaim.claimName → volume declared with a name → volumeMounts references that volume name → mounted at a container path.

**Pause here** — the instructor asks students to review all generated files before continuing to Helm.

***

## Phase C: Create and Understand the Helm Chart Structure

### Step C1: Scaffold a Helm Chart

In the VS Code terminal (make sure you're in the project folder):

```bash
helm create wp-chart
```

**What this creates:** A complete Helm chart scaffold directory (`wp-chart/`) with `Chart.yaml`, `values.yaml`, `templates/`, and example templates. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step C2: Examine Chart.yaml

Open `wp-chart/Chart.yaml`. Note the two version fields: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

* **`version`:** Chart version — increment when you change chart templates/structure
* **`appVersion`:** Application version — the version of WordPress (or your app) being deployed

These are independent. A chart template fix bumps `version`. A new WordPress release bumps `appVersion`.

### Step C3: Examine values.yaml

Open `wp-chart/values.yaml`. This is where all configurable values live. Variables here are accessed in templates via `{{ .Values.variableName }}`. Nested YAML creates dot-notation paths: `image.repository` in values.yaml → `{{ .Values.image.repository }}` in templates. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step C4: Examine a Template (deployment.yaml)

Open `wp-chart/templates/deployment.yaml`. Observe: [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

* `{{ include "wp-chart.fullname" . }}` — imports the chart's full name
* `{{ .Values.replicaCount }}` — references values.yaml
* `{{- if not .Values.autoscaling.enabled }}` — conditional logic
* The template is a **standard Kubernetes Deployment** with variables replacing hardcoded values

***

## Phase D: Begin Manual Conversion to Helm Chart

### Step D1: Clean the Scaffold

Delete all default template files from `wp-chart/templates/` (deployment.yaml, service.yaml, ingress.yaml, serviceaccount.yaml, hpa.yaml, NOTES.txt, `_helpers.tpl`). Delete the `tests/` folder. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

Clear the contents of `wp-chart/values.yaml` (select all → delete → save).

### Step D2: Copy Kubernetes Files into Templates

Copy your Kubernetes definition files (from Phase B) into `wp-chart/templates/`. [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step D3: Replace Hardcoded Values with Template Variables

**Example — Deployment name:**

```yaml
# Before:
name: mysql-deployment
# After:
name: {{ include "wp-chart.fullname" . }}-app
```

**Example — Image:**

```yaml
# Before:
image: mysql:8.0
# After:
image: {{ .Values.mysql.image.repository }}:{{ .Values.mysql.image.tag }}
```

 [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

### Step D4: Define Variables in values.yaml

```yaml
mysql:
  image:
    repository: mysql
    tag: "8.0"
```

 [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)

**Repeat** for all hardcoded values you want to make configurable (WordPress image, PVC sizes, database names, hostnames, etc.).

**Connection to flow:** The full Helm chart conversion will be completed in the next lecture using Amazon Q Developer. This manual exercise ensures you understand the structure well enough to debug AI-generated charts.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ WordPress Application — Kubernetes Object Map

```
KUBERNETES OBJECTS NEEDED:
├── SECRET                    ← DB credentials (root pass, user, pass, db name)
├── MYSQL
│   ├── PVC (mysql-pvc)       ← 1Gi, StorageClass: default → creates EBS
│   ├── Deployment            ← mysql:8.0, env from Secret, volume → /var/lib/mysql
│   └── Service               ← port 3306, selector → MySQL pods
├── WORDPRESS
│   ├── PVC (wordpress-pvc)   ← 2-3Gi, StorageClass: default → creates EBS
│   ├── Deployment            ← wordpress:latest, env from Secret, volume → /var/www/html
│   └── Service               ← port 80, selector → WordPress pods
└── INGRESS                   ← Nginx type, hostname → WordPress service
```

***

## ⚡ PVC → Storage Chain

```
PVC definition (name, size, storageClass, accessMode)
    │ submitted to K8s
    ▼
StorageClass "default" (provisioner: aws-ebs)
    │ creates
    ▼
AWS EBS Volume (actual disk, size from PVC)
    │ referenced by
    ▼
Deployment volumes: (claimName: mysql-pvc → volume name: mysql-storage)
    │ mounted by
    ▼
Container volumeMounts: (name: mysql-storage → mountPath: /var/lib/mysql)

VERIFY StorageClass: kubectl get sc → name "default", provisioner "aws-ebs"
```

***

## 📦 Helm Chart Structure

```
wp-chart/
├── Chart.yaml          ← identity: name, description, version, appVersion
│   ├── version:        chart version (increment on template changes)
│   └── appVersion:     application version (WordPress version)
│
├── values.yaml         ← ALL configurable variables
│   └── accessed via {{ .Values.variable.path }}
│
└── templates/          ← K8s YAML files with {{ }} template expressions
    ├── deployment.yaml
    ├── service.yaml
    ├── pvc.yaml
    ├── secret.yaml
    ├── ingress.yaml
    └── _helpers.tpl    ← reusable named templates (fullname, labels, etc.)
```

***

## 🔗 Helm Template Syntax — Quick Reference

```
VARIABLE:     {{ .Values.replicaCount }}
              → looks up replicaCount in values.yaml

NESTED:       {{ .Values.mysql.image.repository }}
              → mysql.image.repository in values.yaml

INCLUDE:      {{ include "wp-chart.fullname" . }}
              → imports named template from _helpers.tpl

CONDITION:    {{- if not .Values.autoscaling.enabled }}
                replicas: {{ .Values.replicaCount }}
              {{- end }}

CONCATENATE:  image: {{ .Values.mysql.image.repository }}:{{ .Values.mysql.image.tag }}
              → mysql:8.0
```

***

## 🔄 Conversion Process — K8s YAML → Helm Template

```
RAW K8S FILE:
  name: mysql-deployment
  image: mysql:8.0
  replicas: 3

HELM TEMPLATE:
  name: {{ include "wp-chart.fullname" . }}-app
  image: {{ .Values.mysql.image.repository }}:{{ .Values.mysql.image.tag }}
  replicas: {{ .Values.replicaCount }}

VALUES.YAML:
  replicaCount: 3
  mysql:
    image:
      repository: mysql
      tag: "8.0"

PROCESS:
  1. Delete scaffold defaults from templates/
  2. Clear values.yaml
  3. Copy K8s files into templates/
  4. Replace hardcoded values with {{ .Values.xxx }}
  5. Define variables in values.yaml
```

***

## 🤖 AI-Assisted Workflow

```
PROMPT ENGINEERING for K8s files:
  Be SPECIFIC: separate files, storage class name, secret contents, ingress type
  ITERATE: first attempt rarely perfect → refine prompt → retry
  VERIFY: check image versions, StorageClass names, port numbers
  FIX: mysql:5.0 → mysql:8.0 (AI got version wrong)

TOOLS TESTED:
  GitHub Copilot → struggled with K8s/Helm
  ChatGPT → required many edits
  Amazon Q Developer → best for DevOps/K8s (instructor's opinion)
  
PRINCIPLE: "Understand the structure → use AI effectively → debug when AI is wrong"
```

***

## 🧱 Two Versions in Chart.yaml

```
version: 1.0.0        ← CHART version (template/structure changes)
appVersion: "6.4"     ← APP version (WordPress/your app release)

INDEPENDENT:
  Chart template fix → bump version only
  New WordPress release → bump appVersion only
  Both changed → bump both
```

***

## 🔄 `helm create` → What Gets Generated

```
helm create wp-chart
    │
    ├── Chart.yaml (identity + versions)
    ├── values.yaml (sample variables: replicaCount, image, service, ingress, autoscaling...)
    ├── templates/
    │   ├── deployment.yaml (templatized)
    │   ├── service.yaml
    │   ├── ingress.yaml
    │   ├── serviceaccount.yaml
    │   ├── hpa.yaml
    │   ├── _helpers.tpl (name generators, label generators)
    │   ├── NOTES.txt (post-install message)
    │   └── tests/test-connection.yaml
    │
    └── FOR CUSTOM CHART: delete defaults → copy your K8s files → templatize
```

***

## 🛡️ Environment Prerequisites

```
□ Kubernetes cluster running (Kops)
□ Nginx Ingress Controller installed
□ kubeconfig copied to ~/.kube/config on local machine
□ kubectl works locally (kubectl get nodes)
□ Helm installed (brew/choco)
□ VS Code + Amazon Q extension (optional but recommended)
□ StorageClass verified: kubectl get sc → "default" + aws-ebs
□ Domain name available for Ingress hostname
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Template-Variable Separation**
Hardcoded values in configuration files create rigidity — every environment needs manual edits across multiple files. Separating the template (structure) from the values (configuration) lets you deploy the same application to different environments by swapping only the values file. This pattern appears in Helm (values.yaml), Terraform (variables.tf), Ansible (group\_vars), and any configuration management system. The universal principle: **structure stays stable, values change per environment**.

**Pattern 2: Scaffold-Then-Customize**
`helm create` generates a complete, working scaffold. You then delete what you don't need and replace the rest with your actual content. This is faster than building from scratch because the scaffold provides the correct directory structure, naming conventions, and helper templates. The same pattern appears in `create-react-app`, `django-admin startproject`, `dotnet new`, and any framework scaffolding tool.

**Pattern 3: Understand-Then-Automate**
The instructor deliberately teaches manual Helm chart conversion before using AI to generate charts. "I wanted you to understand the structure... so when you develop Helm charts by using any code assistant, and if things don't work as you expected, you know what to change, where." Automation without understanding produces fragile workflows — you can't debug what you don't understand. Understanding the manual process makes AI assistance a force multiplier rather than a black box.

***

## 🎯 One-Line System Summary

> **Helm charts templatize Kubernetes YAML files by replacing hardcoded values with `{{ .Values.xxx }}` expressions sourced from a central `values.yaml`, scaffolded via `helm create`, with `Chart.yaml` tracking independent chart and app versions — enabling a WordPress+MySQL stack (Deployments, Services, PVCs via StorageClass→EBS, Secrets, Ingress) to be deployed consistently across environments by changing only the values file, with AI assistants (Amazon Q) generating the initial files but requiring human verification and structural understanding to debug.** [\[343-helm-hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/343-helm-hands-on.txt)
