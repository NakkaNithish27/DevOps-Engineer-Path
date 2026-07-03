# 🧠 Kubernetes vProfile Project Architecture — Deployments, Services, Persistent Storage & Ingress

**Source:** *348. Architecture* — Kubernetes vProfile Project Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What We Are Building — The Complete Application on Kubernetes

This lecture maps the entire vProfile application — previously containerized with Docker images — onto Kubernetes. Every component that ran as a Docker container now runs as a Kubernetes-managed workload, with Kubernetes handling networking, storage, secret management, and external access. The instructor emphasizes the prerequisite: *"It's highly important for you to do the Containerization project before you do this project."* The Docker images created in that project (Tomcat, MySQL) and the official images used (RabbitMQ, Memcached) are the foundation — Kubernetes orchestrates them.

The lecture is a pure architecture lecture — no commands are run. Its purpose is to establish the **complete mental map** of what resources need to be created, why each exists, and how they connect. Every subsequent lecture writes one or more definition files (manifests) for the resources introduced here.

***

## 1.2 Pods and Deployments — The Compute Layer

The application has four components, each running in its own **pod**: a Tomcat pod (the application), a MySQL pod (the database), a Memcached pod (caching), and a RabbitMQ pod (message queue).

However, the instructor immediately clarifies a critical architectural decision: *"Here I'm showing pod, but we are not going to directly run the pod. We will be having deployment."* Pods are ephemeral — if a pod dies, it's gone. A **Deployment** is a higher-level Kubernetes object that manages pods: it ensures the desired number of pod replicas are running, replaces failed pods automatically, and enables rolling updates. You write a **deployment manifest** where you specify the pod template (which includes the container information — image name, ports, environment variables), and the Deployment controller handles the lifecycle.

Four deployments will be created:

* **Tomcat Deployment** — Uses the custom Docker image from the Containerization project
* **MySQL Deployment** — Uses the custom Docker image from the Containerization project
* **Memcached Deployment** — Uses the official Docker Hub image
* **RabbitMQ Deployment** — Uses the official Docker Hub image

The deployment manifest is a single file that contains both the deployment-level configuration (replicas, update strategy) and the pod-level configuration (container image, ports, volume mounts, environment variables). Writing the deployment manifest implicitly defines the pod.

***

## 1.3 Services (ClusterIP) — The Internal Networking Layer

In Kubernetes, pods do **not** communicate directly with each other by IP. Pod IPs are ephemeral — they change when pods restart or are rescheduled. Instead, Kubernetes uses **Services** as stable network endpoints that route traffic to the correct pods.

For the backend services — MySQL, Memcached, RabbitMQ — the instructor specifies **ClusterIP** type services. A ClusterIP service provides a **stable internal IP and DNS name** that other pods within the cluster can use to connect. It acts as an **internal load balancer**: it receives requests and routes them to the backing pods. The instructor explains: *"If the Tomcat pod or the container running inside the Tomcat pod needs to connect to the database, it is going to connect to the database service, which acts like a load balancer. That service is going to route the request to the database pod."*

ClusterIP is strictly **internal** — it has no public IP and cannot be accessed from outside the cluster. This is appropriate for backend services that should never be directly exposed to the internet.

Three ClusterIP services are needed for the backend: one for MySQL, one for Memcached, one for RabbitMQ. The Tomcat application also gets a ClusterIP service — it's internal too, because external access is handled by a different mechanism (Ingress, covered below).

> 🔍 **Deep Dive:** The Service object decouples the consumer from the producer. The Tomcat application connects to `db-service` (a DNS name), not to a specific pod IP. If the database pod crashes and is recreated with a new IP, the Service automatically updates its endpoint mapping. The Tomcat pod never needs to change — it keeps connecting to the same service name. This is Kubernetes's implementation of the **service discovery** pattern.

***

## 1.4 Stateful Data and the Storage Problem

MySQL is a **stateful application** — it stores and retrieves data that must persist across pod restarts. The instructor defines stateful clearly: *"Stateful means which stores and retrieves the data, which needs to access the data in the runtime."* MySQL stores its data at `/var/lib/mysql` by default.

The problem: if the MySQL pod is deleted or recreated (which Kubernetes does routinely — during updates, node failures, rescheduling), **all data stored inside the pod's filesystem is lost**. The new pod starts fresh with no data. The instructor warns: *"If the pod gets deleted or recreated, all the data will be gone, and when it gets created again, there will be new data. We don't want that to happen."*

The solution is to attach **persistent external storage** to the pod — storage that exists independently of the pod's lifecycle. When the pod is recreated, it reconnects to the same storage and finds all its data intact. This is implemented through three Kubernetes components working together:

***

## 1.5 StorageClass — The Storage Driver

A **StorageClass** is a Kubernetes object that represents a **storage provisioner** — it knows how to create and manage a specific type of storage. The instructor uses an analogy: *"You can understand StorageClass like a driver."*

When the Kubernetes cluster was created with kOps on AWS, kOps automatically created a StorageClass for **Amazon EBS (Elastic Block Store)**. This StorageClass knows how to talk to the AWS API, create EBS volumes, and make them available to pods. Without the StorageClass, Kubernetes has no idea how to interact with EBS or any other external storage system.

The instructor emphasizes the abstraction: *"Pod does not understand, and Kubernetes does not understand, the EBS or any other external volumes. So StorageClass, in essence, makes that external storage available."* StorageClass is the **adapter** between Kubernetes's storage model and the cloud provider's actual storage infrastructure.

Since the StorageClass was created automatically by kOps, no manifest needs to be written for it — it already exists in the cluster.

***

## 1.6 PersistentVolumeClaim (PVC) — Requesting Storage

A **PersistentVolumeClaim** is a request for storage. You write a manifest that says: "I need X GB of storage." The PVC doesn't know or care about the underlying storage technology — it just states what it needs.

The PVC talks to the StorageClass: *"PersistentVolumeClaim is going to talk to StorageClass and say, 'I need this 5GB of volume.' It's the responsibility of the StorageClass to talk to the external storage, create the storage, and give it to the claim."* The StorageClass creates the actual EBS volume, and the PVC represents the claim on that volume.

Once the PVC has successfully claimed storage, it's mapped to the pod. In the database deployment manifest, you specify: store `/var/lib/mysql` on this PersistentVolumeClaim. Behind the scenes, Kubernetes mounts the EBS volume at that path inside the container. If the pod is destroyed and recreated, it reattaches to the same PVC and the same underlying EBS volume — data persists.

The interaction chain is: **Pod → PVC → StorageClass → EBS volume**. The pod knows only about the PVC. The PVC knows only about the StorageClass. The StorageClass handles the AWS-specific details. This layered abstraction means the same pod definition could work on any cloud — only the StorageClass changes.

***

## 1.7 Secrets — Credential Management

The application needs two passwords: one for the **MySQL database** and one for the **RabbitMQ user**. These are stored in a Kubernetes **Secret** object (covered conceptually in the previous Secret lecture, §338). The Secret stores the passwords in base64-encoded format, and they're injected into the relevant pods as environment variables.

One Secret manifest stores both passwords. This Secret is referenced by the database and RabbitMQ deployment manifests, which read the appropriate keys as environment variables.

***

## 1.8 Ingress Controller and Ingress — External Access

All the ClusterIP services are internal — none of them have public IPs. But the Tomcat application (vProfile) needs to be accessible from the internet. This is handled by two components:

### NGINX Ingress Controller

An **Ingress Controller** is a Kubernetes component that manages **external access** to services in the cluster. The instructor specifies an **NGINX Ingress Controller**. When deployed, it automatically creates an **AWS Application Load Balancer (ALB)** — a cloud load balancer with a public endpoint. The Ingress Controller watches for Ingress rules (defined below) and configures the load balancer accordingly.

The instructor explains: *"The job of this Ingress Controller is to manage an external load balancer for us. So in this case, we are doing everything on AWS, so we'll have an Application Load Balancer."*

### Ingress Rule

An **Ingress** is a Kubernetes object (one more manifest) that defines **routing rules** for incoming traffic. The Ingress rule says: "If a user accesses `vprofile.hqinfotech.com`, route the request to the Tomcat ClusterIP service."

The complete external traffic flow:

1. User enters `vprofile.hqinfotech.com` in the browser
2. A **GoDaddy DNS record** maps this domain to the ALB's endpoint
3. The request hits the **ALB** (created by the Ingress Controller)
4. The ALB passes it to the **Ingress Controller** inside the cluster
5. The Ingress Controller checks the **Ingress rule** — the URL matches
6. The request is forwarded to the **Tomcat ClusterIP Service**
7. The Service routes it to the **Tomcat pod**
8. Tomcat processes the request, connecting to backend services (DB, Memcached, RabbitMQ) via their ClusterIP services

> ⚠️ **Expert Note:** The Ingress Controller is a separate deployment that must be installed in the cluster (it's not built-in). The instructor uses NGINX Ingress Controller, which is the most popular choice. When it's deployed on AWS, it automatically provisions an ALB through the AWS Load Balancer Controller integration. This is a powerful pattern: Kubernetes-native configuration (Ingress YAML) drives cloud-provider infrastructure creation (ALB provisioning).

***

## 1.9 The Complete Manifest Inventory

The instructor carefully counts all the definition files (manifests) needed:

| Manifest | Type                         | Purpose                                                    |
| -------- | ---------------------------- | ---------------------------------------------------------- |
| 1        | **Secret**                   | Stores MySQL and RabbitMQ passwords                        |
| 2        | **PersistentVolumeClaim**    | Claims EBS storage for MySQL data                          |
| 3        | **Deployment (MySQL)**       | Runs MySQL pod with custom image                           |
| 4        | **Deployment (Memcached)**   | Runs Memcached pod with official image                     |
| 5        | **Deployment (RabbitMQ)**    | Runs RabbitMQ pod with official image                      |
| 6        | **Deployment (Tomcat)**      | Runs Tomcat pod with custom image                          |
| 7        | **Service (MySQL)**          | ClusterIP for DB internal access                           |
| 8        | **Service (Memcached)**      | ClusterIP for cache internal access                        |
| 9        | **Service (RabbitMQ)**       | ClusterIP for MQ internal access                           |
| 10       | **Service (Tomcat)**         | ClusterIP for app internal access                          |
| 11       | **Ingress**                  | Routes external traffic to Tomcat service                  |
| —        | **NGINX Ingress Controller** | Creates ALB, manages external access (deployed separately) |
| —        | **StorageClass**             | Already exists (created by kOps)                           |

Total: **11 manifests to write** + Ingress Controller installation + StorageClass already present.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are designing the **complete Kubernetes architecture** for the vProfile application — mapping every component to Kubernetes resources. This lecture produces no commands or running infrastructure — it produces the **architectural blueprint** that drives all subsequent lectures, where each manifest is written and applied one by one.

**Final operational outcome (across the project):** A fully functional vProfile application running on Kubernetes with auto-managed pods (Deployments), stable internal networking (ClusterIP Services), persistent database storage (PVC → StorageClass → EBS), encoded credentials (Secrets), and internet-facing access (NGINX Ingress Controller → ALB → Ingress rule → Tomcat Service).

***

## Resource Creation Plan — Execution Order

The manifests will be created in a logical dependency order across upcoming lectures. Understanding this order now prevents confusion later:

### Phase 1: Foundation Objects

**Secret** — Must exist before deployments that reference it (MySQL, RabbitMQ pods need passwords at startup).

**PersistentVolumeClaim** — Must exist before the MySQL deployment mounts it. The PVC triggers the StorageClass to provision an EBS volume.

### Phase 2: Backend Deployments + Services

**MySQL Deployment + ClusterIP Service** — Database must be running before the application connects.

**Memcached Deployment + ClusterIP Service** — Cache service.

**RabbitMQ Deployment + ClusterIP Service** — Message queue service.

### Phase 3: Application Deployment + Service

**Tomcat Deployment + ClusterIP Service** — The application pod. Connects to all three backend services via their ClusterIP DNS names.

### Phase 4: External Access

**NGINX Ingress Controller** — Deployed to the cluster (often via Helm or a manifest from the NGINX project). Creates the ALB on AWS.

**Ingress Rule** — Routes `vprofile.hqinfotech.com` → Tomcat ClusterIP Service.

**GoDaddy DNS Record** — Maps the domain to the ALB endpoint (done outside Kubernetes, in the domain registrar).

***

## Verification Checklist (For Use During Implementation)

As each manifest is applied in subsequent lectures, verify:

| Resource           | Verification Method                 | Expected State                                 |
| ------------------ | ----------------------------------- | ---------------------------------------------- |
| Secret             | `kubectl get secret`                | Secret exists with correct keys                |
| PVC                | `kubectl get pvc`                   | Status: `Bound` (storage provisioned)          |
| Deployments        | `kubectl get deployment`            | All 4 show desired/available replicas matching |
| Pods               | `kubectl get pod`                   | All pods in `Running` state                    |
| Services           | `kubectl get svc`                   | 4 ClusterIP services with correct ports        |
| Ingress Controller | `kubectl get pods -n ingress-nginx` | Controller pod running                         |
| ALB                | AWS Console → EC2 → Load Balancers  | ALB exists, targets healthy                    |
| Ingress            | `kubectl get ingress`               | Rule shows correct host → service mapping      |
| End-to-end         | Browser → `vprofile.hqinfotech.com` | Application loads                              |

***

## Image Source Reference

| Component | Image Source         | Origin                            |
| --------- | -------------------- | --------------------------------- |
| Tomcat    | Custom image         | Built in Containerization project |
| MySQL     | Custom image         | Built in Containerization project |
| Memcached | Official `memcached` | Docker Hub                        |
| RabbitMQ  | Official `rabbitmq`  | Docker Hub                        |

> ⚠️ **Expert Note:** If the custom images from the Containerization project are in a **private registry**, you'll need a `docker-registry` Secret and `imagePullSecrets` in the deployment manifests (as covered in the Secrets lecture, §338). If they're in a public registry, no additional configuration is needed.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Complete Architecture Diagram

```
                        INTERNET
                           │
                     ┌─────┴──────┐
                     │  GoDaddy   │
                     │  DNS A rec │  vprofile.hqinfotech.com → ALB endpoint
                     └─────┬──────┘
                           │
                     ┌─────┴──────┐
                     │    ALB     │  (created by Ingress Controller)
                     └─────┬──────┘
                           │
              ┌────────────┴────────────┐
              │  NGINX Ingress          │
              │  Controller             │
              │  (watches Ingress rules)│
              └────────────┬────────────┘
                           │
              ┌────────────┴────────────┐
              │  Ingress Rule           │
              │  host: vprofile.*.com   │
              │  → Tomcat Service       │
              └────────────┬────────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    │          ┌───────────┴───────────┐           │
    │          │ Tomcat ClusterIP Svc  │           │
    │          └───────────┬───────────┘           │
    │                      │                      │
    │          ┌───────────┴───────────┐           │
    │          │ Tomcat Deployment     │           │
    │          │ (custom image)        │           │
    │          └──┬────────┬────────┬──┘           │
    │             │        │        │              │
    │   ┌─────────┴─┐  ┌──┴──────┐  ┌──┴────────┐ │
    │   │DB ClusterIP│  │MC ClIP  │  │RMQ ClIP   │ │
    │   │Service     │  │Service  │  │Service    │ │
    │   └─────┬──────┘  └───┬─────┘  └───┬───────┘ │
    │         │             │            │         │
    │   ┌─────┴──────┐ ┌───┴─────┐ ┌────┴────────┐│
    │   │DB Deploy   │ │MC Deploy│ │RMQ Deploy   ││
    │   │(custom img)│ │(official│ │(official    ││
    │   └─────┬──────┘ │ image)  │ │ image)      ││
    │         │        └─────────┘ └──────────────┘│
    │   ┌─────┴──────┐                             │
    │   │    PVC     │                             │
    │   └─────┬──────┘                             │
    │   ┌─────┴──────┐                             │
    │   │StorageClass│ (auto-created by kOps)      │
    │   └─────┬──────┘                             │
    │   ┌─────┴──────┐                             │
    │   │ AWS EBS    │                             │
    │   └────────────┘                             │
    │                                              │
    │          ┌───────────────┐                    │
    │          │    Secret     │                    │
    │          │ (DB + RMQ     │                    │
    │          │  passwords)   │                    │
    │          └───────────────┘                    │
    └──────────────────────────────────────────────┘
```

***

## Manifest Inventory

```
FOUNDATION:
  1. Secret               → DB password + RMQ password (base64 encoded)
  2. PersistentVolumeClaim → claims EBS storage for MySQL /var/lib/mysql

BACKEND DEPLOYMENTS:
  3. MySQL Deployment      → custom image + PVC mount + Secret injection
  4. Memcached Deployment  → official image
  5. RabbitMQ Deployment   → official image + Secret injection

BACKEND SERVICES (all ClusterIP = internal only):
  6. MySQL Service         → stable endpoint for DB access
  7. Memcached Service     → stable endpoint for cache access
  8. RabbitMQ Service      → stable endpoint for MQ access

APPLICATION:
  9. Tomcat Deployment     → custom image, connects to backend via service DNS
  10. Tomcat Service       → ClusterIP (internal, used by Ingress)

EXTERNAL ACCESS:
  11. Ingress Rule         → host-based routing to Tomcat Service
  [+] NGINX Ingress Controller (installed separately → creates ALB)
  [+] GoDaddy DNS record (outside K8s → maps domain to ALB)

ALREADY EXISTS:
  StorageClass (created by kOps → EBS provisioner)

TOTAL: 11 manifests to write
```

***

## Storage Chain (MySQL Persistence)

```
MySQL container writes to: /var/lib/mysql
    ↓ volume mount
Pod references: PersistentVolumeClaim
    ↓ claims storage from
PersistentVolumeClaim → StorageClass
    ↓ provisions
StorageClass → AWS EBS Volume (actual disk)

POD DIES → PVC + EBS survive → new pod reattaches → data intact

WITHOUT PVC: pod dies → data lost → new pod starts empty
```

***

## Service Type Decision

```
BACKEND (MySQL, Memcached, RabbitMQ, Tomcat):
  Service type: ClusterIP
  WHY: internal communication only, no public IP needed

EXTERNAL ACCESS:
  NOT a LoadBalancer service on Tomcat
  INSTEAD: Ingress Controller + Ingress Rule
  WHY: Ingress provides host-based routing, SSL, URL mapping
       → more flexible than raw LoadBalancer service
```

***

## External Traffic Flow

```
User → vprofile.hqinfotech.com
  → GoDaddy DNS → ALB endpoint
    → ALB (created by NGINX Ingress Controller)
      → Ingress Controller checks Ingress rules
        → URL matches → forward to Tomcat ClusterIP Service
          → Tomcat pod
            → connects to DB/MC/RMQ via their ClusterIP Services
```

***

## Pod Communication Pattern

```
Tomcat Pod ──→ MySQL ClusterIP Service ──→ MySQL Pod
Tomcat Pod ──→ Memcached ClusterIP Service ──→ Memcached Pod
Tomcat Pod ──→ RabbitMQ ClusterIP Service ──→ RabbitMQ Pod

NEVER: Pod ──→ Pod (direct IP)
ALWAYS: Pod ──→ Service ──→ Pod

WHY: Pod IPs are ephemeral; Service provides stable DNS + load balancing
```

***

## Stateful vs. Stateless Components

```
STATEFUL (needs PVC):
  MySQL       → stores data at /var/lib/mysql → PVC → EBS

STATELESS (no PVC needed):
  Tomcat      → application logic, no persistent data
  Memcached   → in-memory cache, runtime only
  RabbitMQ    → message queue (transient in this setup)
```

***

## Secret Injection Map

```
Secret (mysecret):
  ├── key: db-password     → injected into MySQL Deployment pod
  └── key: rmq-password    → injected into RabbitMQ Deployment pod

Tomcat reads these from: application config → connects using credentials
```

***

## Image Source Map

```
Tomcat     → custom image (Containerization project)
MySQL      → custom image (Containerization project)
Memcached  → official Docker Hub image
RabbitMQ   → official Docker Hub image
```

***

## Kubernetes Resource Hierarchy (This Project)

```
CLUSTER
├── Namespace (default)
│   ├── Secret
│   ├── PVC → StorageClass → EBS
│   ├── Deployment (MySQL) → Pod → Container (custom image)
│   ├── Deployment (Memcached) → Pod → Container (official)
│   ├── Deployment (RabbitMQ) → Pod → Container (official)
│   ├── Deployment (Tomcat) → Pod → Container (custom image)
│   ├── Service (MySQL) → ClusterIP
│   ├── Service (Memcached) → ClusterIP
│   ├── Service (RabbitMQ) → ClusterIP
│   ├── Service (Tomcat) → ClusterIP
│   └── Ingress (routing rule)
│
├── Namespace (ingress-nginx)
│   └── NGINX Ingress Controller → creates ALB
│
└── StorageClass (cluster-wide, created by kOps)
```

***

## Reusable Engineering Pattern: Layered Abstraction for Infrastructure Independence

```
PATTERN (observed in storage chain):
  Application layer:    Pod writes to /var/lib/mysql (knows nothing about storage)
  Claim layer:          PVC requests "10GB storage" (knows nothing about AWS)
  Driver layer:         StorageClass provisions EBS (knows AWS API)
  Infrastructure layer: AWS EBS volume (actual disk)

EACH LAYER:
  - Knows only about its immediate neighbor
  - Can be swapped without affecting other layers
  - PVC is portable across clouds (only StorageClass changes)

SAME PATTERN IN:
  Networking:    Pod → Service (ClusterIP) → Pod
                 (Pod doesn't know other pod's IP; Service abstracts it)
  
  External:      Ingress Rule → Ingress Controller → ALB
                 (Rule is K8s-native; Controller handles cloud-specific LB)

  Secrets:       Pod → Secret → encoded values
                 (Pod gets decoded values; doesn't manage encoding)

PRINCIPLE:
  Each layer abstracts the complexity of the layer below it
  Higher layers are portable; lower layers are provider-specific
  Kubernetes = abstraction machine for infrastructure
```

***

## One-Line Mental Reload Trigger

> *"4 Deployments (Tomcat/MySQL custom, MC/RMQ official) + 4 ClusterIP Services (internal) + Secret (DB+RMQ passwords) + PVC→StorageClass→EBS (MySQL persistence) + NGINX Ingress Controller→ALB + Ingress rule (host→Tomcat svc) + GoDaddy DNS — 11 manifests total, pods never talk directly, Service abstracts everything."*

This single sentence reconstructs all four deployments with their image sources, the service type and count, the secret contents, the complete storage chain, the external access architecture, the manifest count, and the core networking principle. [\[348-architecture \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/348-architecture.txt)
