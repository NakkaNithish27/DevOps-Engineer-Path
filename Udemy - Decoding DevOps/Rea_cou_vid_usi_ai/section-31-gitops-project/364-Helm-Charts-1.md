# 🧠 Helm Charts Part 1 — Generating Helm Charts from Kubernetes Manifests with AI Assistance

**Source:** *364. Helm Charts Part 1* — GitOps / Kubernetes Helm Series (Video Caption Reconstruction + Step Reference)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why Convert Plain Manifests to Helm Charts?

In the previous Kubernetes project (§348–§358), the vProfile application was deployed using **plain Kubernetes definition files** (manifests) — raw YAML files for deployments, services, secrets, PVC, and ingress. These work, but they have a significant limitation: every value is **hardcoded**. If you want to change the image tag, replica count, storage size, or domain name, you must edit the YAML files directly. In a GitOps pipeline with multiple environments (dev/staging/prod), this means maintaining multiple copies of nearly identical files — or manually editing values for each deployment.

**Helm charts** solve this by converting static manifests into **templates with variables**. Instead of hardcoding `image: myapp:v1`, the template says `image: {{ .Values.app.image }}:{{ .Values.app.tag }}`, and the actual values come from a separate `values.yaml` file. Different environments get different `values.yaml` files — same templates, different configurations. This is the Kubernetes equivalent of parameterized infrastructure.

The instructor positions this lecture within a larger GitOps project: *"This project is not about writing every line of code — this project is all about designing, architecting. Once you understand the entire flow of the GitOps pipeline, you can work on any GitOps project."* The Helm chart is one component of a three-repository GitOps architecture (Helm charts, Terraform infrastructure code, application code).

***

## 1.2 The Three-Repository GitOps Architecture

The step reference file reveals the broader project structure — three separate GitHub repositories:

| Repository         | Purpose                 | Content                                      |
| ------------------ | ----------------------- | -------------------------------------------- |
| **vprofile-helm**  | Helm charts             | Kubernetes deployment templates + values     |
| **vprofile-infra** | Infrastructure code     | Terraform code for AWS EKS, networking, etc. |
| **vprofile-app**   | Application source code | Application code, Dockerfiles, CI pipeline   |

This separation is a deliberate architectural decision. Each repository has a distinct lifecycle: application code changes frequently (feature development), infrastructure changes occasionally (scaling, new services), and Helm chart structure changes rarely (only when adding new Kubernetes resources or changing deployment patterns). Separating them allows independent version control, independent CI/CD pipelines, and clear ownership boundaries.

***

## 1.3 Using AI Assistance for Code Generation — The Deliberate Approach

The instructor makes an explicit and deliberate choice to use **GitHub Copilot** (AI assistant) to generate the Helm charts from the existing Kubernetes manifests. The reasoning is stated directly: *"Most of the time we will be using AI assistance to generate our code."* And: *"There's also one more reason we are not writing anything in this project — that is because we have already done this manually and through AI as well in previous lectures."*

This isn't laziness — it's a **workflow evolution**. The manual Helm chart creation was learned in a previous section. Now the focus shifts to the **architectural design** — knowing what to ask for, how to structure the chart, what variables to parameterize, and what annotations to include. The AI generates the boilerplate; the engineer provides the design decisions.

The prompt given to GitHub Copilot (detailed in the step reference) is itself a form of **engineering specification**. It defines:

* Chart name and folder structure
* How to split resources into template files
* How to organize `values.yaml` into sections
* Which variables to parameterize
* Default values for image tags
* Cloud-specific configurations (AWS EBS, AWS ALB)
* Conditional rendering logic (feature flags)

The quality of the generated Helm chart depends entirely on the quality of this prompt — which depends on the engineer's understanding of Kubernetes, Helm, and the target infrastructure.

> ⚠️ **Expert Note:** The instructor's approach models the real production workflow: engineers with deep understanding use AI to accelerate code generation, then **review and correct** the output. The step reference includes corrections after generation: *"Make sure ingress is enabled"*, *"Correct the domain name in values.yaml file"*, *"Add ingress annotation to use cert and 443."* AI-generated code is a starting point, not a finished product.

***

## 1.4 Helm Chart Structure — What Gets Generated

The prompt specifies a precise folder structure and file organization:

```
helm/vprofile/
├── Chart.yaml              # Chart metadata (name, version)
├── values.yaml             # All configurable values
└── templates/
    ├── app-deployment.yaml      # Tomcat deployment template
    ├── db-deployment.yaml       # MySQL deployment template
    ├── mc-deployment.yaml       # Memcached deployment template
    ├── rmq-deployment.yaml      # RabbitMQ deployment template
    ├── services.yaml            # All ClusterIP services
    ├── ingress.yaml             # Ingress rule (conditional)
    ├── secret.yaml              # Application secrets
    ├── pvc.yaml                 # PersistentVolumeClaim
    └── dockerregistry-secret.yaml  # Docker registry credentials (conditional)
```

Each template file corresponds to a resource type from the original plain manifests (§348). The separation into individual files per deployment (rather than one giant template) is a best practice — it makes the chart readable, debuggable, and maintainable.

***

## 1.5 values.yaml Design — Parameterization Strategy

The `values.yaml` file is organized into **separate variable sections** for each component, with **one level of nesting only** (keeping it simple):

```yaml
app:
  image: <tomcat-image>
  tag: latest
  replicas: 1
  containerPort: 8080
  servicePort: 8080

db:
  image: <mysql-image>
  tag: latest
  storageClass: gp2
  storageSize: 10Gi

memcached:
  image: memcached
  tag: latest

rabbitmq:
  image: rabbitmq
  tag: latest

ingress:
  enabled: true
  host: vprofile.example.com

dockerregistry:
  enabled: false

secrets:
  ...
```

**Key design decisions specified in the prompt:**

* **All image tags default to `latest`** — No empty tag values allowed (empty tags cause pull errors).
* **Image name and tag are separate variables** — Enables changing the tag without modifying the image name (common in CI/CD: same image, new tag per build).
* **`db.storageClass` defaults to `gp2`** — AWS EBS volumes use the `gp2` storage class. This is cloud-specific but necessary for the EKS deployment target.
* **Ingress and docker registry secret are conditionally rendered** — Controlled by `enabled` flags. If `ingress.enabled: false`, the ingress template is not rendered at all. If `dockerregistry.enabled: false`, no registry secret is created and no `imagePullSecrets` are added to deployments.
* **`imagePullSecrets` only in app and db deployments** — Only the custom images (Tomcat, MySQL) might be in a private registry. Memcached and RabbitMQ use official public images — they never need pull secrets.

***

## 1.6 AWS ALB Ingress Controller Annotations — Cloud-Specific Configuration

The ingress template includes AWS-specific annotations for the **AWS ALB (Application Load Balancer) Ingress Controller**:

```yaml
annotations:
  kubernetes.io/ingress.class: alb
  alb.ingress.kubernetes.io/scheme: internet-facing
  alb.ingress.kubernetes.io/target-type: ip
  alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:...
  alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
  alb.ingress.kubernetes.io/ssl-redirect: '443'
  alb.ingress.kubernetes.io/backend-protocol: HTTP
```

Each annotation configures the ALB's behavior:

* **`ingress.class: alb`** — Tells Kubernetes to use the AWS ALB controller (not NGINX or another controller)
* **`scheme: internet-facing`** — Creates a public ALB (accessible from the internet)
* **`target-type: ip`** — Routes traffic directly to pod IPs (instead of node ports)
* **`certificate-arn`** — References an SSL certificate from AWS Certificate Manager (ACM) for HTTPS
* **`listen-ports`** — ALB listens on both HTTP (80) and HTTPS (443)
* **`ssl-redirect: '443'`** — Automatically redirects HTTP traffic to HTTPS
* **`backend-protocol: HTTP`** — Communication between ALB and pods uses HTTP (SSL terminates at the ALB)

The `ingressClassName: alb` field is also set, which is the newer Kubernetes method for specifying the ingress controller (complementing the annotation).

> 🔍 **Deep Dive:** The shift from the NGINX Ingress Controller (used in the kOps project, §348) to the **AWS ALB Controller** reflects a platform change: the GitOps project targets **AWS EKS** (managed Kubernetes), where the ALB controller is the native, recommended ingress solution. ALB is a managed AWS service — it handles TLS termination, auto-scaling, and health checks at the cloud infrastructure level, removing that responsibility from the Kubernetes cluster itself.

***

## 1.7 SSH-Based GitHub Authentication — Repository Access Setup

The step reference describes setting up **SSH key-based authentication** for GitHub, which is the production method for cloning and pushing to private repositories:

1. **Generate SSH keys** locally: `ssh-keygen` in `~/.ssh/`
2. **Create an SSH config file** (`~/.ssh/config`) that maps a host alias to GitHub with a specific identity file
3. **Add the public key** to the GitHub account
4. **Clone repositories** using the SSH URL

The SSH config uses a **host alias** (`github.com-devops4sure`) with a specific `IdentityFile` — this allows using different SSH keys for different GitHub accounts on the same machine. `IdentitiesOnly yes` ensures only the specified key is used, preventing SSH from trying other keys.

***

## 1.8 The Source Manifests — What Gets Converted

The instructor downloads the existing Kubernetes manifests from the `kube-app` branch of the `hkhcoder/vprofile-project` repository. These are the same manifests from the Kubernetes project (§348–§358):

* Secret file (DB + RMQ passwords)
* Tomcat deployment + service
* DB deployment + service + PVC
* Memcached deployment + service
* RabbitMQ deployment + service
* Ingress definition

These plain manifests are placed into the Helm repository, and the AI generates Helm chart templates from them — replacing hardcoded values with `{{ .Values.xxx }}` template references.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are converting the **plain Kubernetes manifests** from the vProfile project into a **Helm chart** using GitHub Copilot. This Helm chart will be stored in the `vprofile-helm` repository as part of a three-repo GitOps architecture. The chart parameterizes all configuration values, supports conditional rendering of ingress and docker registry secrets, and includes AWS ALB-specific annotations for EKS deployment.

**Final outcome:** A complete Helm chart (`helm/vprofile/`) in the `vprofile-helm` repository, with templates for all Kubernetes resources and a `values.yaml` with organized, sensible defaults — ready for deployment via a GitOps pipeline.

***

## Step 1: Create the Three GitHub Repositories

Create three repositories on GitHub:

| Repository       | Purpose                                         |
| ---------------- | ----------------------------------------------- |
| `vprofile-helm`  | Helm charts for Kubernetes deployment           |
| `vprofile-infra` | Terraform infrastructure code (future lectures) |
| `vprofile-app`   | Application source code (future lectures)       |

Only `vprofile-helm` is used in this lecture. The other two are created now for the overall GitOps project.

***

## Step 2: Set Up SSH Key Authentication for GitHub

Generate SSH keys:

```bash
cd ~/.ssh
ssh-keygen
```

Follow the prompts — the instructor uses a key named `devops4sure`.

Create the SSH config file:

```bash
vim ~/.ssh/config
```

**Contents:**

```
Host github.com-devops4sure
  HostName github.com
  User git
  IdentityFile ~/.ssh/devops4sure
  IdentitiesOnly yes
```

**What this does:** Creates a host alias (`github.com-devops4sure`) that uses a specific SSH key when connecting to GitHub. This is useful when managing multiple GitHub accounts.

Copy the **public key** (`~/.ssh/devops4sure.pub`) and add it to your GitHub account under **Settings → SSH and GPG Keys → New SSH Key**.

***

## Step 3: Clone All Three Repositories Locally

```bash
cd
mkdir ~/Desktop/gitops
cd ~/Desktop/gitops
git clone <vprofile-helm-ssh-url>
git clone <vprofile-infra-ssh-url>
git clone <vprofile-app-ssh-url>
```

**Verification:** Three directories created under `~/Desktop/gitops/`.

***

## Step 4: Download the Kubernetes Manifests

Navigate to: **github.com/hkhcoder/vprofile-project** → switch to the **`kube-app`** branch.

The `kubedefs/` folder contains all the Kubernetes definition files from the previous project.

Click **Code → Download ZIP**. Extract the ZIP file. Locate the `kubedefs/` folder in the extracted content.

**Copy the `kubedefs/` folder** into the `vprofile-helm` repository directory.

Open the `vprofile-helm` directory in **VS Code**. Verify you can see the `kubedefs/` folder with all manifest files.

***

## Step 5: Install and Sign In to GitHub Copilot

In VS Code:

1. Go to **Extensions** → search for **GitHub Copilot** → click **Install** (if not already installed)
2. Sign in: click the account icon in the bottom-right → **Sign in to use AI features** → **Continue with GitHub**
3. Authorize in the browser → return to VS Code

**Verification:** GitHub Copilot is active (icon visible in the status bar).

***

## Step 6: Generate the Helm Chart Using the AI Prompt

Open the **Copilot Chat** panel in VS Code. Use the following prompt (from the step reference):

> *Create a Helm chart from the Kubernetes manifests in the kubedefs folder.*
>
> Requirements:
>
> * Chart name: vprofile
> * Folder structure: helm/vprofile
> * Separate each resource type into individual template files (app-deployment.yaml, db-deployment.yaml, mc-deployment.yaml, rmq-deployment.yaml, services.yaml, ingress.yaml, secret.yaml, pvc.yaml, dockerregistry-secret.yaml)
> * Use separate variable sections for app, db, memcached, rabbitmq, initcontainers, ingress, secrets, dockerregistry in values.yaml
> * One level nesting only in values.yaml
> * Variables: Common variables: image, tag, replicas, containerPort, servicePort, storageClass, storageSize, defaultUser
> * All image tags must default to latest — no empty tag values
> * image name and tag should be separate variables
> * db.storageClass must be set to gp2 for AWS EKS EBS volumes
> * Ingress must use AWS ALB controller with annotations kubernetes.io/ingress.class: alb, alb.ingress.kubernetes.io/scheme: internet-facing, alb.ingress.kubernetes.io/target-type: ip and ingressClassName: alb
> * Ingress and docker registry secret must be conditionally rendered with an enabled flag
> * dockerregistry.enabled defaults to false
> * Include imagePullSecrets in app and db deployments only when dockerregistry.enabled is true
> * initContainers use command not args
> * Keep it simple and minimal

**What Copilot generates:** A complete Helm chart structure under `helm/vprofile/` with:

* `Chart.yaml` — Chart metadata
* `values.yaml` — All parameterized values organized by component
* `templates/` — Template files for each resource

**Review the generated output carefully.** AI-generated code requires validation.

***

## Step 7: Post-Generation Corrections

The step reference identifies three corrections needed after generation:

### 7a: Ensure Ingress is Enabled

In `values.yaml`, verify:

```yaml
ingress:
  enabled: true
```

If Copilot defaulted to `false`, change it to `true`.

### 7b: Correct the Domain Name

In `values.yaml`, verify the `ingress.host` value matches your actual domain name (e.g., `vprofile.yourdomain.com`).

### 7c: Add SSL/HTTPS Annotations to Ingress

Add or verify these annotations in the ingress template or `values.yaml`:

```yaml
alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:<account-id>:certificate/<cert-id>
alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
alb.ingress.kubernetes.io/ssl-redirect: '443'
alb.ingress.kubernetes.io/backend-protocol: HTTP
```

The `certificate-arn` must reference your actual ACM certificate ARN from your AWS account.

***

## Step 8: Generate README.md

Use Copilot to generate a `README.md` file documenting the Helm chart — chart structure, values reference, usage instructions.

***

## Step 9: Commit and Push

```bash
cd ~/Desktop/gitops/vprofile-helm
git add .
git commit -m "Helm chart for vprofile application"
git push origin main
```

**Verification:** The `vprofile-helm` repository on GitHub contains the complete Helm chart under `helm/vprofile/`.

> ⚠️ **Expert Note:** Always review AI-generated Helm templates against the original manifests. Common issues: missing environment variable injections, incorrect secret key references, wrong port numbers, missing volume mounts. Run `helm template helm/vprofile/` locally to render the templates and compare against the original plain manifests.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Three-Repository GitOps Architecture

```
REPOSITORY              CONTENT                   LIFECYCLE
─────────────           ──────────                ─────────
vprofile-helm           Helm charts (K8s deploy)  Changes rarely
vprofile-infra          Terraform (AWS infra)     Changes occasionally
vprofile-app            App source + Dockerfiles  Changes frequently

SEPARATION PRINCIPLE:
  App code, infra code, deployment specs = independent version control
```

***

## Helm Chart Generation Flow

```
1. Download kubedefs/ from hkhcoder/vprofile-project (kube-app branch)
2. Copy kubedefs/ into vprofile-helm repo
3. Open in VS Code with GitHub Copilot
4. Feed structured prompt to Copilot Chat
5. Copilot generates: Chart.yaml + values.yaml + templates/
6. REVIEW + CORRECT:
     ✅ ingress.enabled = true
     ✅ correct domain name
     ✅ add SSL/HTTPS annotations (cert ARN, listen ports, redirect)
7. Generate README.md
8. Commit to main branch
```

***

## Generated Helm Chart Structure

```
helm/vprofile/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── app-deployment.yaml
    ├── db-deployment.yaml
    ├── mc-deployment.yaml
    ├── rmq-deployment.yaml
    ├── services.yaml
    ├── ingress.yaml            (conditional: ingress.enabled)
    ├── secret.yaml
    ├── pvc.yaml
    └── dockerregistry-secret.yaml  (conditional: dockerregistry.enabled)
```

***

## values.yaml Organization

```yaml
app:       { image, tag: latest, replicas, containerPort, servicePort }
db:        { image, tag: latest, storageClass: gp2, storageSize }
memcached: { image: memcached, tag: latest }
rabbitmq:  { image: rabbitmq, tag: latest }
ingress:   { enabled: true, host: <domain> }
dockerregistry: { enabled: false }   # conditional imagePullSecrets
secrets:   { ... }
initcontainers: { ... }

RULES:
  - All tags default to "latest" (never empty)
  - Image name and tag = separate variables
  - One level nesting only
  - db.storageClass = gp2 (AWS EBS)
```

***

## Conditional Rendering Logic

```
ingress.enabled: true
  → ingress.yaml template RENDERED
  → ALB created, domain routing active

ingress.enabled: false
  → ingress.yaml template SKIPPED
  → no external access

dockerregistry.enabled: true
  → dockerregistry-secret.yaml RENDERED
  → imagePullSecrets ADDED to app + db deployments

dockerregistry.enabled: false (default)
  → dockerregistry-secret.yaml SKIPPED
  → no imagePullSecrets (public images only)
```

***

## AWS ALB Ingress Annotations

```yaml
kubernetes.io/ingress.class: alb              # use ALB controller
alb.ingress.kubernetes.io/scheme: internet-facing   # public ALB
alb.ingress.kubernetes.io/target-type: ip           # route to pod IPs
alb.ingress.kubernetes.io/certificate-arn: <ACM-ARN>  # SSL cert
alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
alb.ingress.kubernetes.io/ssl-redirect: '443'       # force HTTPS
alb.ingress.kubernetes.io/backend-protocol: HTTP    # ALB→pod = HTTP
ingressClassName: alb                               # K8s native field
```

***

## SSH Config for Multi-Account GitHub

```
~/.ssh/config:
  Host github.com-devops4sure
    HostName github.com
    User git
    IdentityFile ~/.ssh/devops4sure
    IdentitiesOnly yes

PURPOSE: use specific SSH key per GitHub account
CLONE: git clone git@github.com-devops4sure:user/repo.git
```

***

## Plain Manifests → Helm Chart Transformation

```
BEFORE (plain manifest):
  image: myapp:v1                    ← hardcoded
  replicas: 2                        ← hardcoded
  storageClassName: gp2              ← hardcoded

AFTER (Helm template):
  image: {{ .Values.app.image }}:{{ .Values.app.tag }}    ← parameterized
  replicas: {{ .Values.app.replicas }}                     ← parameterized
  storageClassName: {{ .Values.db.storageClass }}           ← parameterized

VALUES.YAML:
  app:
    image: myapp
    tag: latest
    replicas: 2
  db:
    storageClass: gp2

BENEFIT: same templates, different values per environment (dev/staging/prod)
```

***

## AI-Assisted Code Generation Workflow

```
PREREQUISITE: engineer already understands the technology manually

WORKFLOW:
  1. DESIGN: define chart structure, variable organization, conditions
  2. SPECIFY: write detailed prompt with all requirements
  3. GENERATE: AI produces code from prompt
  4. REVIEW: validate against original manifests
  5. CORRECT: fix domain names, enable flags, add annotations
  6. TEST: helm template to render and verify

"This project is all about designing, architecting"
→ AI handles boilerplate
→ Engineer handles design decisions and corrections
```

***

## Post-Generation Correction Checklist

```
✅ ingress.enabled = true (not false)
✅ Domain name correct in values.yaml
✅ certificate-arn matches YOUR ACM cert
✅ listen-ports includes both HTTP:80 and HTTPS:443
✅ ssl-redirect set to '443'
✅ backend-protocol set to HTTP
✅ All image tags default to "latest" (no empty values)
✅ imagePullSecrets conditional on dockerregistry.enabled
✅ initContainers use "command" not "args"
```

***

## Reusable Engineering Pattern: Structured AI Prompt as Engineering Specification

```
PATTERN:
  Instead of writing code manually:
    1. Define ARCHITECTURE (chart structure, file layout)
    2. Define PARAMETERIZATION (which values are variable)
    3. Define CONSTRAINTS (defaults, cloud-specific settings, conditions)
    4. Define CONVENTIONS (naming, nesting depth, file separation)
    5. Feed as STRUCTURED PROMPT to AI
    6. REVIEW + CORRECT output

WHY:
  - Architecture understanding > code writing speed
  - Prompt quality = output quality
  - Engineer focuses on DESIGN DECISIONS
  - AI handles BOILERPLATE TRANSLATION

PREREQUISITE:
  Must have done it manually first
  "We have already done this manually in previous lectures"
  → understanding enables effective prompting
  → without understanding, can't review or correct output

WHERE ELSE:
  • Terraform module generation from architecture requirements
  • CI/CD pipeline YAML generation from workflow description
  • Dockerfile generation from deployment requirements
  • Any infrastructure-as-code generation task
```

***

## One-Line Mental Reload Trigger

> *"Download kubedefs/ from vprofile-project kube-app branch → copy to vprofile-helm repo → Copilot prompt generates helm/vprofile/ chart (templates per resource, values.yaml by component, one-level nesting, tags=latest, gp2 storageClass, ALB ingress with cert+SSL annotations, conditional ingress+dockerregistry) → review, correct domain/enabled/cert-arn → commit to main — three repos: helm, infra, app."*

This single sentence reconstructs the source of manifests, the generation workflow, every key design decision in the prompt, the post-generation corrections, and the three-repository GitOps structure. [\[364-helm-c...rts-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/364-helm-charts-part-1.txt), [\[364.Helm_Repo_Steps \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/364.Helm_Repo_Steps.txt)
