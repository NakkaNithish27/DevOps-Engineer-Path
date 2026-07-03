# 🎓 Deep Learning Material: Kubernetes Source Code Overview — vProfile Project Manifests

**Source:** [349-source-code-overview.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt?EntityRepresentationId=82743e1f-a652-4344-9c01-9b392f665d65) — Video lecture providing a guided walkthrough of the vProfile Kubernetes project's source code repository on GitHub, examining the complete set of manifest files (secrets, PVC, four deployments, four ClusterIP services, and ingress), showing how to clone and set up the project in VS Code, and mapping every manifest to the architecture diagram before writing them from scratch in subsequent lectures. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Repository Structure and Branch Strategy

The vProfile project source code lives on GitHub at `github.com/hkhcoder/vprofile-project`. The repository uses **branches** to separate different deployment methods. The branch relevant to this Kubernetes section is **`kubeapp`** — which contains the fully written Kubernetes manifests as a reference. There is also a branch called **`skelkube`** (skeleton Kubernetes) — an exact replica of `kubeapp` but with all manifest files **empty**. The upcoming lectures use `skelkube` as the starting point, writing every manifest from scratch. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

The `kubeapp` branch is created **from the Docker branch** (the containers branch from the containerization section). This means it inherits all Dockerfiles and the docker-compose file. The Kubernetes manifests are added on top in a dedicated folder called **`kubedefs`**. This demonstrates a real-world pattern: Kubernetes deployment definitions live alongside the application source code and Docker build files in the same repository. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## 1.2 The Complete Manifest Inventory

The `kubedefs` folder contains **all the Kubernetes definition files** needed to deploy the entire vProfile application on a Kubernetes cluster. The instructor walks through every file, mapping each to its role in the architecture. The complete inventory is: [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

### Secret (1 file)

A **Secret** stores sensitive data — specifically two variables: `db-pass` (the MySQL database password) and `rmq-pass` (the RabbitMQ password). In the Docker Compose approach, these were set as plain-text environment variables in the compose file. In Kubernetes, secrets provide a more secure mechanism — values are base64-encoded and can be mounted into Pods as environment variables or files without being visible in plain text in the definition files. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

### PersistentVolumeClaim (1 file)

A **PVC** claims a volume of **3GB** for persistent storage. This replaces the Docker Compose `volumes:` section where host volumes were declared with `{}`. In Kubernetes, PVCs are the standard way to request persistent storage — the cluster's storage provisioner automatically creates the actual volume (on EBS in AWS, persistent disk in GCP, etc.). The PVC has a name that will be referenced by the database deployment to persist MySQL data. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

### Deployments (4 files)

Four **Deployment** manifests — one for each application component:

| Deployment     | Component                 | Image Source              |
| -------------- | ------------------------- | ------------------------- |
| vproapp        | Tomcat application server | Custom Docker Hub image   |
| vprodb         | MySQL database            | Custom Docker Hub image   |
| vpromq         | RabbitMQ message broker   | Official Docker Hub image |
| vprocache (mc) | Memcached cache           | Official Docker Hub image |

 [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

These Deployments replace the `services:` entries in Docker Compose. Each Deployment manages one Pod (or multiple replicas for scaling). The Deployment object — not a bare Pod — is used because Deployments provide replica management, rolling updates, and self-healing. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

### Services (4 files)

Four **Service** manifests — one for each Deployment — all of type **ClusterIP**. ClusterIP means the service is **internal only** — accessible within the cluster but not from the internet. Each Service provides a stable DNS name and IP address for its corresponding Pods. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

The key architectural point: **all inter-service communication is internal**. The app Pod reaches the database Pod through its ClusterIP Service name. The app Pod reaches Memcached and RabbitMQ through their ClusterIP Service names. This mirrors how `container_name` worked in Docker Compose — but in Kubernetes, it's the Service name that provides the DNS resolution, not the Pod name. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

### Ingress (1 file)

One **Ingress** manifest handles **external access**. It defines the rule: if a user accesses a specific host URL, route the request through the NGINX Ingress Controller to the `vproapp-service` ClusterIP Service, which forwards to the Tomcat Pods. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

The flow as described by the instructor: user accesses URL → load balancer → NGINX Ingress Controller → checks Ingress rule → if URL matches, forward to `vproapp-service` → Service routes to the `vproapp` Pod. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## 1.3 The Architecture Pattern — Internal ClusterIP + External Ingress

The most important architectural concept in this lecture is the **separation between internal and external access**:

**Internal (ClusterIP):** All four services communicate internally through ClusterIP Services. No NodePort, no LoadBalancer type — purely internal. This is the most secure configuration: backend services (database, cache, message broker) are never exposed outside the cluster. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

**External (Ingress):** Only the frontend access point uses Ingress. A single Ingress rule routes external HTTP/HTTPS traffic to the application service. The Ingress Controller (with its NLB) is the only component exposed to the internet. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

This maps directly to the architecture diagram from the previous lecture and mirrors the GCP project architecture (private instances behind a load balancer, backend services accessible only internally). [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## 1.4 Mapping Docker Compose Concepts to Kubernetes Objects

The video implicitly establishes a concept mapping between Docker Compose (previous section) and Kubernetes:

| Docker Compose             | Kubernetes                    | Purpose                             |
| -------------------------- | ----------------------------- | ----------------------------------- |
| `services:` entries        | Deployment + Service          | Define and run containers           |
| `container_name:`          | Service name (DNS)            | Inter-container/pod name resolution |
| `environment:` (sensitive) | Secret                        | Store credentials                   |
| `volumes: {}`              | PersistentVolumeClaim         | Persistent storage                  |
| `ports:`                   | Service (ClusterIP) + Ingress | Internal + external access          |
| `docker-compose up`        | `kubectl apply -f`            | Declarative deployment              |
| `build:`                   | Pre-built image on Docker Hub | Image building is separate in K8s   |

 [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## 1.5 VS Code Setup for Kubernetes Development

The instructor demonstrates cloning the repository in VS Code using the Source Control panel (clone repository → paste HTTPS URL → select destination). After cloning, switching to the `kubeapp` branch reveals the complete manifests. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

A practical recommendation: install the **Kubernetes extension** in VS Code. Search for "Kubernetes" in the Extensions panel and install the first result. This extension provides syntax highlighting, auto-completion, and validation for Kubernetes YAML files. It may show an error about `kubectl` not being found — this can be ignored for now as the actual cluster commands are run on the kops VM, not locally. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing

We are examining the fully-written Kubernetes manifest files for the vProfile project to understand what needs to be built, then setting up the development environment (VS Code + repository clone) in preparation for writing every manifest from scratch in the next lectures. The final outcome: a clear mental picture of all 11 files we need to write and how they map to the architecture. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## Step 1: Access the Source Code Repository

Open your browser and navigate to:

```
https://github.com/hkhcoder/vprofile-project
```

Select the branch **`kubeapp`** from the branch dropdown. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

This branch contains the complete Kubernetes manifests alongside the existing Dockerfiles and docker-compose file.

***

## Step 2: Browse the Manifest Files

Navigate to the **`kubedefs`** folder. Inside, you'll find all the Kubernetes definition files: [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

| File           | Object Type           | Purpose                                   |
| -------------- | --------------------- | ----------------------------------------- |
| Secret YAML    | Secret                | Stores `db-pass` and `rmq-pass`           |
| PVC YAML       | PersistentVolumeClaim | Claims 3GB storage for MySQL              |
| App Deployment | Deployment            | Tomcat vProfile application               |
| DB Deployment  | Deployment            | MySQL database                            |
| MQ Deployment  | Deployment            | RabbitMQ message broker                   |
| MC Deployment  | Deployment            | Memcached cache                           |
| App Service    | Service (ClusterIP)   | Internal access to app pods               |
| DB Service     | Service (ClusterIP)   | Internal access to db pods                |
| MQ Service     | Service (ClusterIP)   | Internal access to mq pods                |
| MC Service     | Service (ClusterIP)   | Internal access to mc pods                |
| Ingress        | Ingress               | External HTTP access via NGINX controller |

Open each file and **match it with the architecture diagram** from the previous lecture. The instructor explicitly asks you to do this cross-referencing. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## Step 3: Clone the Repository in VS Code

**3a. Copy the clone URL:**

On GitHub, click the repository name → click the dropdown (Code button) → select **HTTPS** → click **Copy**. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

**3b. Clone in VS Code:**

Open VS Code → click the **Source Control** icon (left sidebar) → click **Clone Repository** → paste the URL → click the clone option → select a destination folder (e.g., `F:\kubeapp`) → click **Select as Repository Destination** → click **Open** when prompted. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

**3c. Switch to the `kubeapp` branch:**

Click the branch name in the bottom-left of VS Code → select `kubeapp` from the dropdown. The `kubedefs` folder should now be visible in the file explorer. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## Step 4: Install the Kubernetes VS Code Extension

Go to **Extensions** (left sidebar) → search for **Kubernetes** → install the first result. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

It will show an error about `kubectl` not being found. **Ignore this** — `kubectl` runs on your kops VM, not your local machine. The extension is useful for YAML syntax support and auto-completion while editing manifest files. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

***

## Step 5: Switch to the Skeleton Branch

Click the branch symbol in VS Code → switch to **`skelkube`**. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

This branch has the same folder structure and the same file names, but **all manifest files are empty**. This is your starting point for the next lectures — you will write every manifest from scratch. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

**Verify:** Open any file in `kubedefs` — it should have no content.

***

## Step 6: Study and Cross-Reference

Before proceeding to the next lecture:

1. Switch back to `kubeapp` branch.
2. Open each manifest file.
3. Match each file to its component in the architecture diagram.
4. Understand the flow: Ingress → `vproapp-service` → `vproapp` Deployment → Pod.
5. Note the internal connections: app Pod → `vprodb` Service, `vprocache` Service, `vpromq` Service.
6. Switch to `skelkube` branch — this is where you'll work. [\[349-source...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/349-source-code-overview.txt)

**Connection to larger flow:** The next lecture begins writing manifests starting with the Secret, then PVC, then Deployments, then Services, and finally Ingress — following the dependency order.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Complete Manifest Inventory

```
kubedefs/
├── Secret              (1)  → db-pass, rmq-pass
├── PVC                 (1)  → 3GB for MySQL data
├── Deployments         (4)  → vproapp, vprodb, vpromq, vprocache
├── Services (ClusterIP)(4)  → vproapp-service, vprodb-svc, vpromq-svc, vprocache-svc
└── Ingress             (1)  → external HTTP access via NGINX controller

Total: 11 manifests
```

***

## Architecture Mapping

```
EXTERNAL ACCESS:
  User → URL → NLB → NGINX Ingress Controller
    → Ingress Rule: host match? → vproapp-service (ClusterIP)
      → vproapp Pod (Tomcat:8080)

INTERNAL ACCESS (all ClusterIP):
  vproapp Pod → vprodb-service     → vprodb Pod (MySQL:3306)
  vproapp Pod → vprocache-service  → vprocache Pod (Memcached:11211)
  vproapp Pod → vpromq-service     → vpromq Pod (RabbitMQ:5672)

STORAGE:
  PVC (3GB) → mounted to vprodb Pod (/var/lib/mysql)

SECRETS:
  Secret → db-pass, rmq-pass → injected into Pods as env vars
```

***

## Docker Compose → Kubernetes Mapping

```
compose services:       → Deployment + Service (per component)
container_name:         → Service name (DNS resolution)
environment: (secrets)  → Secret object
volumes: {}             → PersistentVolumeClaim
ports: (external)       → Ingress
ports: (internal)       → Service type: ClusterIP
docker-compose up       → kubectl apply -f <files>
build:                  → pre-built images on Docker Hub (build is separate)
```

***

## Branch Strategy

```
kubeapp     → REFERENCE (fully written manifests)
              Purpose: study, compare, verify
              Contains: kubedefs/ with complete YAML content

skelkube    → WORKSPACE (empty manifests)
              Purpose: write from scratch in upcoming lectures
              Contains: kubedefs/ with empty files

Both branches: same Dockerfiles + docker-compose from containers branch
```

***

## Repository Setup

```
GitHub: github.com/hkhcoder/vprofile-project
  → Branch: kubeapp (reference)
  → Branch: skelkube (workspace)

Clone in VS Code:
  Source Control → Clone Repository → HTTPS URL → select destination
  Switch branch: bottom-left branch indicator

VS Code extension: "Kubernetes" (for YAML support)
  kubectl error → ignore (runs on kops VM, not local)
```

***

## Request Flow (Complete)

```
User → vprofile.domain.com
  → DNS → NLB (Ingress Controller's LoadBalancer Service)
    → NGINX Ingress Controller Pod
      → Ingress rule: host match → service: vproapp-service:8080
        → ClusterIP Service → vproapp Pod (Tomcat)
          → Secret (db-pass) → vprodb Service → MySQL Pod
          → Secret (rmq-pass) → vpromq Service → RabbitMQ Pod
          → vprocache Service → Memcached Pod
          → PVC → /var/lib/mysql (persistent storage)
```

***

## Object Count by Type

```
Deployment:              4  (app, db, mq, mc)
Service (ClusterIP):     4  (one per deployment)
Secret:                  1  (db-pass + rmq-pass)
PersistentVolumeClaim:   1  (3GB for MySQL)
Ingress:                 1  (external routing rule)
─────────────────────────
Total manifests:        11
```

***

## Writing Order (Dependency-Based)

```
1. Secret              ← credentials needed by deployments
2. PVC                 ← storage needed by db deployment
3. Deployments (×4)    ← depend on secret + PVC
4. Services (×4)       ← depend on deployments (label selectors)
5. Ingress             ← depends on app service existing

This is the order for the upcoming lectures
```

***

## Internal vs External Access Pattern

```
INTERNAL (ClusterIP):
  All 4 services → ClusterIP → never exposed externally
  Backend (db, mq, mc) → ONLY reachable within cluster
  App service → reachable within cluster + via Ingress

EXTERNAL (Ingress):
  Single entry point → NGINX controller → 1 rule → app service
  Only the app is accessible from outside
  All backends completely isolated
```

***

## Key Engineering Patterns

| Pattern                                        | Manifestation                                                                                                              |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Reference + skeleton branches**              | Study complete code first, then write from scratch — learn by examining, then by doing                                     |
| **Same repo, different deployment methods**    | Dockerfiles + docker-compose + kubedefs coexist — application code is deployment-method agnostic                           |
| **Internal-by-default, external-by-exception** | All services ClusterIP; only app exposed via single Ingress — minimal attack surface                                       |
| **Secret extraction**                          | Sensitive values moved from inline env vars (compose) to dedicated Secret object (K8s) — separation of config from secrets |
| **PVC replaces host volumes**                  | Docker `{}` volumes → Kubernetes PVC — storage becomes portable, cloud-provisioned, not host-dependent                     |
| **Architecture-first, code-second**            | Study diagram → map to manifests → then write — understanding before execution                                             |

***

## Project Continuity

```
BEFORE: Ingress (lecture 339), Pods, Services, Deployments concepts
THIS:   Source code overview — all 11 manifests identified and mapped
NEXT:   Write all manifests from scratch (skelkube branch)
        Order: Secret → PVC → Deployments → Services → Ingress
```

***

This completes the full reconstruction. **Theory** explains every manifest type and the internal-vs-external access architecture. **Practical** walks through repository cloning, branch switching, and VS Code setup. The **Compression Map** gives you the complete 11-manifest inventory, the request flow, and the writing order for the upcoming lectures. Let me know if you'd like Anki flashcards or any section expanded! 🚀
