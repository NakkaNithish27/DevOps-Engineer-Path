# 🎓 Kubernetes Persistent Volume Claims (PVC) for Database Storage — Deep Learning Material

**Source:** Video caption file — *Persistent Volume for DB — PVC* [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Where Does Database Data Live in Kubernetes?

In Docker Compose, when you need persistent data for a database, you create a **named volume** (e.g., `vprodbdata`) in the volumes section. Docker creates a folder on the Docker engine's host machine and maps it to the container's data directory (e.g., `/var/lib/mysql`). If the container restarts, the data survives because it's stored in the named volume on the host — not inside the container. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

Kubernetes also has a volume concept, but there's a critical problem: a basic Kubernetes volume stores data on the **local worker node's filesystem**. The instructor states clearly: "In Kubernetes, it'll be storing it in the worker node, which is not at all recommended." [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

Why is local node storage bad for databases?

* If the **pod is rescheduled to a different node** (due to scaling, node failure, or rolling update), the data is on the old node — the new pod on the new node starts with empty storage.
* If the **node itself fails**, the data is lost with it.
* You can't **decouple** the data from the specific node — the data and the pod are tied to one machine.

For **stateful applications** — applications that store and retrieve data (databases, caches with persistence, message queues with durable storage) — the data must be **safe, decoupled from any specific pod or node, reconnectable to new pods, and independently managed**. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 1.2 — Persistent Volumes (PV): External, Managed Storage

Kubernetes solves the local-storage problem with **Persistent Volumes (PV)**. A Persistent Volume is a piece of **external storage** — not on the worker node's local disk, but on a separate storage system (EBS volumes on AWS, EFS, NFS, cloud disks, SAN, etc.). This external storage exists independently of any pod or node. If a pod is deleted and recreated, the PV remains. If a node fails, the PV survives because it's on separate infrastructure. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

The instructor emphasizes that managing Persistent Volumes is a **Kubernetes administrator's responsibility**: "In persistent volumes, you need to manage all the storage by yourself. Like this will be the job of the Kubernetes administrator, definitely, to make sure the volumes are available, scalable, its backup was taken regularly, all those things. It is definitely a job of the administrator. And there's a lot of work that goes behind the scenes — a complete storage management." [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

This is the same **stateful storage management burden** seen throughout the course — from EBS volume management in AWS (partitioning, formatting, mounting, snapshotting) to database-on-separate-volume patterns. The challenge is universal; only the abstraction layer changes.

***

## 1.3 — Storage Classes: Automated Storage Provisioning

Manually creating Persistent Volumes (pre-provisioning storage before pods need it) is operationally heavy. **Storage Classes** are Kubernetes's answer to automating this. A Storage Class defines **how storage should be provisioned** — what type of storage, what performance tier, what parameters. When a pod requests storage, the Storage Class automatically provisions it. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

The instructor notes: "Kubernetes gives us something called Storage Classes, where these kind of things are kind of automated. Again, you will need an administrator for this one also, because whenever data comes, you need regular backups, maintenance, scalability, all those things." [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

### kOps and the Default Storage Class

When you create a Kubernetes cluster with **kOps** on AWS, kOps automatically creates a **default Storage Class** that provisions **EBS volumes**. There's also a storage class available for **EFS**. You don't need to write Storage Class definitions or manage the storage provisioning yourself — kOps sets it up. You just write the **claim** (how much storage you need), and the Storage Class handles creating the actual EBS volume. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

This is the critical simplification: "So you don't need to write definitions like this and create a storage class and manage it. You can just write the persistent volume claims." The administrator sets up the Storage Class once; consumers (developers, pod definitions) just make claims against it. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

> 🔍 **Deep Dive:** The three-tier storage model in Kubernetes maps to familiar concepts:
>
> * **Persistent Volume (PV)** = The actual storage resource (like an EBS volume). Administrator creates or Storage Class auto-provisions.
> * **Storage Class** = The provisioner/template (like an EBS volume type definition — gp3, io1, etc.). Defines HOW to create PVs.
> * **Persistent Volume Claim (PVC)** = The consumer's request ("I need 3GB"). Binds to a matching PV.
>
> The relationship: PVC requests storage → Storage Class provisions a PV → PV is bound to the PVC → Pod mounts the PVC. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 1.4 — Persistent Volume Claim (PVC): The Consumer's Request

A **Persistent Volume Claim (PVC)** is a **request for storage** — written from the perspective of the application/pod, not the administrator. It says: "I need X amount of storage, with Y access mode, from Z storage class." The PVC doesn't know or care about the underlying storage technology — it just makes a claim. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

The instructor's analogy: "Like a consumer, right? I need 3GB of volume, like 30GB or 200GB of volume, and the storage class will take care of it." [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

### PVC Definition Structure

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-pv-claim
  labels:
    app: vprodb
spec:
  storageClassName: default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

Key fields:

* **`name: db-pv-claim`** — The PVC's name. This is what the pod definition references when mounting the volume.
* **`labels: app: vprodb`** — Labels for filtering and identification (same labeling pattern used throughout Kubernetes).
* **`storageClassName: default`** — Which Storage Class to request from. The `default` class on a kOps cluster provisions EBS volumes.
* **`accessModes: ReadWriteOnce`** — The volume can be mounted as read-write by a **single node**. This is the standard mode for database volumes (only one pod should write to the database storage at a time).
* **`storage: 3Gi`** — The amount of storage requested (3 GiB).

***

## 1.5 — How PVC Connects to the Pod

The PVC is created as a separate Kubernetes resource. Then, in the **pod definition** (or deployment definition), you reference the PVC by name and specify the **mount path** inside the container. The instructor previews this connection: "In the pod definition, we'll say connect this volume to `/var/lib/mysql`." [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

The full chain when everything is applied:

1. **PVC** is created → requests 3GB from the `default` Storage Class
2. **Storage Class** provisions an EBS volume (3GB) → creates a **PV** → binds the PV to the PVC
3. **Pod definition** references `db-pv-claim` and mounts it at `/var/lib/mysql`
4. **Pod starts** → MySQL writes data to `/var/lib/mysql` → data goes to the EBS volume
5. **Pod deleted/recreated** → new pod mounts the same PVC → same EBS volume → data intact [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 1.6 — Docker Compose Volumes vs. Kubernetes PVC: The Translation

The lecture explicitly maps the Docker Compose volume concept to Kubernetes PVC — continuing the pattern of translating the same application requirements across different technologies: [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

| Docker Compose                                      | Kubernetes                                              |
| --------------------------------------------------- | ------------------------------------------------------- |
| `volumes: vprodbdata:` (top-level)                  | PersistentVolumeClaim definition (separate YAML)        |
| `volumes: - vprodbdata:/var/lib/mysql` (in service) | `volumeMounts` in pod spec referencing PVC              |
| Data stored in Docker engine folder on host         | Data stored in external storage (EBS via Storage Class) |
| Tied to the Docker host machine                     | Decoupled from any specific node                        |

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We're creating a **Persistent Volume Claim** for the V-Profile database pod (MySQL/MariaDB). This PVC will request 3GB of storage from the cluster's default Storage Class (which provisions EBS volumes on AWS via kOps). In the next lecture, the PVC will be connected to the DB deployment, ensuring database data survives pod restarts and rescheduling. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## Step 1: Review the Docker Compose Volume (Understanding the Requirement)

### What We're Doing

Looking at the Docker Compose file to understand what volume the database needs — this is the **information gathering** step before writing the Kubernetes equivalent.

### What to Look For

In `docker-compose.yml`:

* **Top-level `volumes:` section** — defines a named volume `vprodbdata`
* **In the `db` service** — `volumes: - vprodbdata:/var/lib/mysql` — maps the named volume to MySQL's data directory [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

### The Kubernetes Translation

We need a PVC that provides the equivalent of `vprodbdata` and will be mounted at `/var/lib/mysql` in the database pod. The PVC definition is created now; the mount happens in the next lecture's deployment definition.

***

## Step 2: Generate the PVC Definition

### The Action

The instructor uses a generative AI tool to get the PVC template: "I just did 'Kubernetes persistent volume claim' and its generative AI is giving me this PVC example." [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

Copy the generated PVC template. Create the file:

```bash
vim kubedefs/dbpvc.yaml
```

***

## Step 3: Write the PVC Definition

### The Complete YAML

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-pv-claim
  labels:
    app: vprodb
spec:
  storageClassName: default
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

### Line-by-Line Breakdown

**`apiVersion: v1`** — PVCs are part of the core Kubernetes API (v1).

**`kind: PersistentVolumeClaim`** — The resource type. This tells Kubernetes we're creating a storage claim, not a pod, deployment, or service.

**`metadata.name: db-pv-claim`** — The name of this PVC. This exact name will be referenced in the database pod/deployment definition when mounting the volume.

**`metadata.labels.app: vprodb`** — Label for identification and filtering. Follows the project's labeling convention. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

**`spec.storageClassName: default`** — Specifies which Storage Class to request storage from. The instructor explains: "By default, there is a storage class called default. When we create the Kubernetes cluster \[with kOps]... that is basically going to give us the EBS." This is the critical link — the `default` Storage Class on a kOps/AWS cluster provisions EBS volumes automatically. [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

**`spec.accessModes: ReadWriteOnce`** — The volume can be mounted as read-write by **one node at a time**. This is correct for database storage — only one MySQL pod should write to the data directory.

**`spec.resources.requests.storage: 3Gi`** — Request 3 GiB of storage. The Storage Class will provision an EBS volume of this size.

### Save the File

Save and quit (`:wq`).

***

## Step 4: Understand What Happens When Applied (Preview)

### The Execution Chain (Not Applied Yet — Next Lecture)

When `kubectl apply -f dbpvc.yaml` is executed:

1. Kubernetes reads the PVC definition
2. Finds the `default` Storage Class
3. The Storage Class's provisioner (EBS CSI driver on kOps) **creates a 3GB EBS volume** on AWS
4. A **Persistent Volume (PV)** object is created automatically representing that EBS volume
5. The PV is **bound** to the PVC (`db-pv-claim`)
6. Status changes to **Bound** [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

### How It Will Connect to the Pod (Next Lecture)

In the DB deployment definition:

```yaml
volumes:
  - name: db-storage
    persistentVolumeClaim:
      claimName: db-pv-claim    # ← references this PVC
containers:
  - name: mysql
    volumeMounts:
      - mountPath: /var/lib/mysql    # ← mounts at MySQL data dir
        name: db-storage
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

### Verification Commands (For Next Lecture)

```bash
kubectl get pvc                    # Check PVC status (should be Bound)
kubectl get pv                     # Check auto-provisioned PV
kubectl get storageclass           # Verify default storage class exists
```

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ The Storage Problem in Kubernetes

```
DOCKER COMPOSE:
  volumes: vprodbdata  → folder on Docker host → data persists across container restarts
  PROBLEM: Tied to ONE host machine

KUBERNETES (basic volume):
  volume → stored on WORKER NODE filesystem
  PROBLEM: Pod rescheduled to different node → data LOST
           Node fails → data LOST
           "Not at all recommended"

KUBERNETES (Persistent Volume):
  PVC → Storage Class → provisions EXTERNAL storage (EBS)
  → Data survives pod deletion, node failure, rescheduling
  → Decoupled from any specific node
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 📐 Three-Tier Storage Architecture

```
PVC (Consumer request)
  "I need 3GB, ReadWriteOnce"
       │
       ▼
STORAGE CLASS (Provisioner/template)
  "default" on kOps = EBS provisioner
  Automatically provisions storage
       │
       ▼
PV (Actual storage resource)
  Auto-created EBS volume (3GB)
  Bound to the PVC
       │
       ▼
POD (Application)
  volumeMounts: /var/lib/mysql → PVC → PV → EBS
  MySQL writes here → data on EBS → safe

WHO MANAGES WHAT:
  Storage Class setup    → Administrator (done once, kOps does it)
  PVC definition         → Developer/DevOps (per-application)
  PV provisioning        → Automatic (Storage Class handles it)
  Backups, scaling, etc. → Administrator (ongoing)
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 🔗 Docker Compose → Kubernetes Translation

```
DOCKER COMPOSE                      KUBERNETES
──────────────                      ──────────
volumes:                            PersistentVolumeClaim (separate YAML)
  vprodbdata:                         name: db-pv-claim
                                      storageClassName: default
                                      storage: 3Gi

services.db.volumes:                Pod spec.volumes + volumeMounts:
  - vprodbdata:/var/lib/mysql         claimName: db-pv-claim
                                      mountPath: /var/lib/mysql

Storage location:                   Storage location:
  Docker host folder (local)          EBS volume (external, cloud)
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 📦 PVC Definition (Complete)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: db-pv-claim              # Referenced by pod definition
  labels:
    app: vprodb                  # For filtering
spec:
  storageClassName: default      # kOps default = EBS provisioner
  accessModes:
    - ReadWriteOnce              # One node at a time (correct for DB)
  resources:
    requests:
      storage: 3Gi               # Size of EBS volume to provision
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## ⚡ Execution Chain (When Applied)

```
kubectl apply -f dbpvc.yaml
       │
       ▼
K8s reads PVC → finds storageClassName: default
       │
       ▼
default Storage Class → EBS CSI provisioner
       │
       ▼
AWS API → creates 3GB EBS volume
       │
       ▼
PV object auto-created → bound to PVC
       │
       ▼
PVC status: Bound ✅
       │
       ▼
DB Deployment references PVC (claimName: db-pv-claim)
       │
       ▼
Pod mounts PVC at /var/lib/mysql
       │
       ▼
MySQL writes → /var/lib/mysql → PVC → PV → EBS volume
       │
       ▼
Pod deleted → data SAFE on EBS
Pod recreated → remounts same PVC → same data ✅
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 📊 Access Modes

```
ReadWriteOnce (RWO):  One node can mount read-write  → DB volumes (this lecture)
ReadOnlyMany (ROX):   Many nodes can mount read-only → Shared config/assets
ReadWriteMany (RWX):  Many nodes can mount read-write → Shared storage (like EFS)

DATABASE = ReadWriteOnce (only one MySQL pod writes at a time)
```

***

## 🔄 Storage Evolution Across the Course

```
EBS LECTURE:
  Manual: Create EBS → attach → partition → format → mount → fstab
  Problem: Manual, tied to one instance

EBS SNAPSHOTS:
  Backup → Restore → Change type/size/zone
  Problem: Still manual lifecycle management

EFS:
  Shared file storage across instances (NFS)
  Problem: Need NFS client, fstab, manual setup

RDS:
  Managed database storage (AWS handles it)
  Problem: AWS-specific, not portable

DOCKER VOLUMES:
  Named volumes on Docker host
  Problem: Tied to one host machine

KUBERNETES PVC: ◄── THIS LECTURE
  PVC → Storage Class → auto-provisions EBS
  → Decoupled, portable, auto-provisioned, declarative
  → SAME EBS underneath, but fully automated + declarative
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: CONSUMER/PROVIDER STORAGE MODEL
  Consumer (PVC): "I need 3GB"
  Provider (Storage Class): "Here's an EBS volume"
  → Consumer doesn't know/care about the backend technology
  → Same as: Cloud storage APIs, S3 client (doesn't know which disk),
    database connection string (doesn't know the server hardware)
  → PRINCIPLE: Decouple storage request from storage implementation

PATTERN 2: DECLARATIVE STORAGE PROVISIONING
  Declare WHAT you need (size, mode) → system provisions HOW
  → Same as: Terraform (declare infra → provider creates),
    docker-compose volumes (declare → Docker creates),
    AWS CloudFormation (declare → AWS provisions)
  → PRINCIPLE: Declare intent, not implementation

PATTERN 3: STATEFUL DATA DECOUPLING
  Data lives OUTSIDE the compute unit (pod/container/VM)
  Compute can be destroyed/recreated → data survives
  → Same as: EBS separate from EC2, Docker named volumes,
    RDS (managed, independent of app instances),
    database-on-separate-volume pattern (EBS Snapshots lecture)
  → PRINCIPLE: Stateless compute + externalized state = resilient systems

PATTERN 4: ADMINISTRATOR/DEVELOPER SEPARATION
  Admin sets up Storage Class (once)
  Developer writes PVC (per application)
  → Same as: Admin creates VPC/subnets, dev deploys into them
    Admin configures IAM, dev uses roles
    Platform team sets up infra, app team consumes it
  → PRINCIPLE: Platform provides, applications consume
```

 [\[351-persis...for-db-pvc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/351-persistent-volume-for-db-pvc.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → K8s Extras (Taints, Limits, Jobs, DaemonSets)
THIS      → Persistent Volume Claim for DB (storage decoupling)
NEXT      → DB Deployment definition (connects PVC to pod at /var/lib/mysql)

KEY RELATIONSHIP:
  This PVC → referenced in next lecture's Deployment → mounted in MySQL pod
  PVC is CREATED FIRST, CONSUMED LATER (dependency ordering)

STORAGE KNOWLEDGE ARC:
  EBS (manual) → EBS Snapshots (backup) → EFS (shared) → RDS (managed)
  → Docker volumes (host-local) → K8s PVC (declarative, auto-provisioned)
  Each step adds more abstraction and automation
```

***

Your Kubernetes PVC deep learning material is fully reconstructed — covering the storage problem, the three-tier PV/StorageClass/PVC architecture, the Docker-to-Kubernetes translation, and the complete execution chain from PVC creation to EBS provisioning. Ready for the next lecture (DB Deployment connecting the PVC) or want me to generate **AnkiDeck flashcards (.csv)** from this or the full series? 🃏
