# 🎓 Deep Learning Material: Kubernetes vProfile Project — Architecture Summary, Cleanup, and Complete System Reconstruction

**Source:** Video lecture on project summarization and cleanup (from [360-summarize.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt?EntityRepresentationId=d0ed4f2d-f8f6-472e-94ae-a05e85afea84) caption file) [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**Video Context:** This is the **final lecture** of the Kubernetes vProfile project. The instructor does three things: **(1)** walks through the complete architecture diagram one final time, tracing the entire request flow from user to backend and identifying every Kubernetes object involved, **(2)** performs a systematic cleanup of all resources (ingress controller, all manifests, EBS volumes, the kOps cluster, Route 53 hosted zone, and the kOps EC2 instance), and **(3)** provides learning advice — recommending students draw their own diagrams, re-do the project multiple times, and internalize the architecture for interviews and real project meetings. Despite being short, this lecture is architecturally the most valuable because it connects every concept from the entire project into one unified flow.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Complete Request Flow: User to Backend and Back

The instructor traces the full end-to-end architecture one final time, connecting every Kubernetes object in the request path. This is the unified system view that ties together every previous lecture's individual concepts: [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**The flow begins with the user accessing the load balancer.** The load balancer was automatically created by the ingress controller when the ingress resource was applied. The user's request arrives at this external load balancer. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**The ingress matches the request by host and path.** The ingress resource contains rules that map specific hostnames and URL paths to specific Kubernetes services. When the incoming request matches a rule (the "correct host path"), the ingress routes it to the **Tomcat service** (the vProfile application's ClusterIP service). [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**The service forwards the request to the pod.** The Tomcat service acts as an internal load balancer — it knows which pods belong to it (via label selectors) and forwards the request to one of the vProfile application pods. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**The application connects to backend services.** Inside the pod, the vProfile application has an `application.properties` file that contains the connection details for backend services. Critically, these connection details are **Kubernetes service names** — not IP addresses. The instructor emphasizes: *"In this case, literally the Kubernetes service information, like vproDB, port 3306."* The application uses the service name `vproDB` to connect to the database, and Kubernetes' internal DNS resolves that name to the database service's ClusterIP. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**The database service forwards to the database pod.** Just as the Tomcat service routes to app pods, the DB service routes to the MySQL pod. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**The database pod's data lives on an EBS volume.** The MySQL container stores its data on a **persistent volume** backed by an AWS EBS disk. This volume was provisioned through a **storage class** (which defines how to create EBS volumes) and claimed by a **persistent volume claim** (PVC) in the pod definition. If the pod restarts or moves to another node, the data persists on the EBS volume. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**The database container gets its password from a Secret.** The MySQL container requires the `MYSQL_ROOT_PASSWORD` environment variable. Instead of hardcoding this in the pod definition, it's stored in a **Kubernetes Secret** object and injected into the container at runtime. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

This single flow touches every major Kubernetes concept from the project: **Ingress** (external access + routing), **Services** (internal routing + DNS), **Pods** (application containers), **PVC/StorageClass** (persistent storage), **Secrets** (sensitive data injection), and the **application.properties** configuration pattern (using service names for service discovery). [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

***

## 1.2 — The "Everything as Code" Cleanup Pattern

The cleanup sequence reveals an important architectural insight: resources must be deleted in **reverse dependency order**. The ingress controller must be deleted first (because it created the load balancer), then the application resources (pods, services, secrets, PVCs), then the cluster itself, and finally the supporting infrastructure (Route 53, kOps EC2 instance). [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

The instructor uses `kubectl delete -f .` in the `kubedefs` directory — this reads every YAML file in the directory and deletes all the resources defined in them. This is the **mirror of `kubectl apply -f .`** — the same declarative approach works for both creation and destruction. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

A critical cascade behavior: *"when we delete the volume claim, it's going to also delete the EBS volume."* Deleting the PVC triggers the storage class's reclaim policy, which (if set to Delete) automatically removes the underlying EBS volume. This is an example of Kubernetes managing the full lifecycle of cloud resources through its abstraction layers. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

The instructor also reinforces the "everything from scratch" principle: *"You have the lecture, you have all the resources, whenever you want, you can create everything from scratch."* All resources are reproducible from code — the cleanup is safe because nothing is lost permanently. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

***

## 1.3 — Learning Advice: Internalization Through Repetition and Drawing

The instructor provides specific advice for deep learning: [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

*"I'll also recommend you draw yourself these diagrams and write your own information. It'll be easier for you when you sit in the project meetings, when you want to really containerize applications. And also very helpful when you're talking in the interview."*

And: *"if you do it few times and you make sure you know the architecture, you know the application... you can anytime do this."* [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

The implication: understanding Kubernetes is not about memorizing commands — it's about internalizing the **architecture** (how objects relate) and the **application** (what the actual software needs). The commands are mechanical; the architecture is what makes you effective.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing and Why

We are performing a **complete teardown** of the Kubernetes vProfile project — deleting all Kubernetes resources, the cluster itself, and supporting AWS infrastructure. The final outcome: a clean AWS account with no running resources, no ongoing costs, and the confidence that everything can be recreated from the code files at any time.

***

## Step 1: Delete the Ingress Controller

The ingress controller was created using `kubectl apply -f <url>`. To delete it, use the same URL with `delete` instead of `apply`: [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

```bash
kubectl delete -f <ingress-controller-url>
```

* `delete` — removes all resources defined in the manifest
* `-f <url>` — the same manifest URL used during creation [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**What happens internally:** [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

* The ingress controller deployment, service, and related objects are removed
* The AWS load balancer that was automatically created by the ingress controller is **also deleted**

**This takes some time** — the load balancer deletion involves AWS API calls and resource deprovisioning. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**Why delete this first:** The ingress controller manages the external load balancer. If you delete the cluster before deleting the ingress controller, the load balancer may become an orphaned AWS resource — still running and costing money, but no longer managed by anything. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

***

## Step 2: Delete All Application Resources

Navigate to the manifests directory:

```bash
cd kubedefs
kubectl delete -f .
```

* `delete -f .` — reads every YAML file in the current directory (`.`) and deletes all resources defined in them [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**What gets deleted:**

* All pods (app, db, cache, queue)
* All services (ClusterIP services for each component)
* All deployments/replicasets
* The Secret (`app-secret`)
* The PVC (persistent volume claim) [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**Cascade effect:** Deleting the PVC triggers deletion of the **EBS volume** in AWS (if the storage class reclaim policy is `Delete`). *"When we delete the volume claim, it's going to also delete the EBS volume."* [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

***

## Step 3: Delete the Kubernetes Cluster

```bash
kops delete cluster --name=<cluster-name> --yes
```

* `kops delete cluster` — destroys the entire Kubernetes cluster (master nodes, worker nodes, networking, security groups, IAM roles, etc.)
* `--name` — the cluster name (or use `kops validate cluster` to find it)
* `--yes` — confirms the deletion (without this, kops only shows what it would delete) [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**This takes a long time** — kops must delete EC2 instances, EBS volumes, security groups, load balancers, auto-scaling groups, IAM resources, and VPC components. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

***

## Step 4: Delete the Route 53 Hosted Zone

After the cluster is deleted, go to **AWS Console → Route 53** and delete the hosted zone that was created for the cluster's DNS. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

**Why:** The hosted zone incurs a small monthly cost and is no longer needed if the cluster is gone. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

***

## Step 5: Handle the kOps EC2 Instance

The instructor recommends: [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

* **If you plan to use it again soon:** Shut it down (stop) but keep it — it has many prerequisites installed (kubectl, kops, AWS CLI, SSH keys, etc.)
* **If you're done for a long time:** Delete it entirely — *"you have the lecture, you have all the resources, whenever you want, you can create everything from scratch."* [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Complete Architecture (Full Request Flow)

```
USER
  │
  ▼
LOAD BALANCER (AWS ELB, created by Ingress Controller)
  │
  ▼
INGRESS (matches host/path → routes to service)
  │
  ▼
TOMCAT SERVICE (ClusterIP) ──label selector──► VPROFILE APP POD
  │                                              │
  │                                              │ application.properties:
  │                                              │   db: vproDB:3306
  │                                              │   cache: vprocache:11211
  │                                              │   mq: vpromq:15672
  │                                              │
  │                                              ▼
  │                                     DB SERVICE (vproDB)
  │                                              │
  │                                              ▼
  │                                     DB POD (MySQL)
  │                                       │           │
  │                                       │           ▼
  │                                       │     SECRET (app-secret)
  │                                       │       → MYSQL_ROOT_PASSWORD
  │                                       ▼
  │                                     EBS VOLUME
  │                                       ↑ claimed by PVC
  │                                       ↑ provisioned by StorageClass
  │
  ├──► CACHE SERVICE (vprocache) → MEMCACHE POD
  └──► MQ SERVICE (vpromq) → RABBITMQ POD
```

***

## 🔷 Every Kubernetes Object in the Project

```
OBJECT              PURPOSE                          LAYER
──────────          ────────────────────             ──────
Ingress             External routing (host/path)     Access
Ingress Controller  Creates/manages AWS LB           Access
Service (ClusterIP) Internal routing + DNS            Networking
Pod                 Application containers            Compute
Deployment          Pod lifecycle management          Orchestration
Secret              Password storage (base64)         Security
PVC                 Volume claim                      Storage
StorageClass        EBS volume provisioner            Storage
Namespace           Resource isolation                Organization
```

***

## 🔷 Service Discovery Mechanism

```
application.properties:
  db.host = vproDB        ← Kubernetes Service name (NOT IP)
  db.port = 3306

RESOLUTION:
  App container → DNS query "vproDB" → Kubernetes DNS → ClusterIP of DB Service
  DB Service → label selector → DB Pod IP

WHY SERVICE NAMES:
  Pod IPs change (pods restart, reschedule)
  Service IPs are STABLE
  Service names are HUMAN-READABLE
```

***

## 🔷 Cleanup Sequence (Reverse Dependency Order)

```
1. kubectl delete -f <ingress-controller-url>
   → removes ingress controller + AWS load balancer

2. cd kubedefs && kubectl delete -f .
   → removes all app resources (pods, services, secrets, PVC)
   → PVC deletion → triggers EBS volume deletion

3. kops delete cluster --name=<name> --yes
   → removes entire cluster (EC2, networking, IAM, etc.)
   → TAKES A LONG TIME

4. Route 53 → delete hosted zone
   → removes DNS zone (stops monthly cost)

5. kOps EC2 instance → stop or terminate
   → stop if reusing soon, delete if done

ORDER MATTERS:
  Ingress controller BEFORE cluster (prevent orphaned LB)
  App resources BEFORE cluster (clean cascade of PVC → EBS)
  Cluster BEFORE Route 53 (cluster uses the DNS zone)
```

***

## 🔷 The Mirror Pattern: Apply ↔ Delete

```
CREATE:                              DESTROY:
kubectl apply -f <url>               kubectl delete -f <url>
kubectl apply -f .                   kubectl delete -f .
kops create cluster ... --yes        kops delete cluster ... --yes

Same manifests, same commands, opposite action.
Declarative infrastructure works in both directions.
```

***

## 🔷 Cascade Deletion Chain

```
kubectl delete -f . (in kubedefs/)
  │
  ├── deletes PVC
  │     └── triggers StorageClass reclaim policy
  │           └── deletes EBS volume in AWS
  │
  ├── deletes Deployments
  │     └── deletes ReplicaSets
  │           └── deletes Pods
  │
  ├── deletes Services
  ├── deletes Secrets
  └── deletes Ingress

kubectl delete -f <ingress-controller>
  │
  └── deletes Ingress Controller
        └── deletes AWS Load Balancer
```

***

## 🔷 AWS Resources Created by Kubernetes (Must Be Cleaned)

```
RESOURCE                  CREATED BY              DELETED BY
────────────────          ──────────────          ──────────────────
AWS ELB                   Ingress Controller      kubectl delete ingress controller
EBS Volumes               StorageClass/PVC        kubectl delete PVC
EC2 Instances (nodes)     kOps                    kops delete cluster
Security Groups           kOps                    kops delete cluster
IAM Roles                 kOps                    kops delete cluster
VPC + Subnets             kOps                    kops delete cluster
Route 53 Records          kOps                    kops delete cluster
Route 53 Hosted Zone      Manual                  Manual deletion
kOps EC2 Instance         Manual                  Manual deletion
```

***

## 🔷 Learning Advice (From the Instructor)

```
1. DRAW the architecture diagram yourself
2. WRITE your own notes
3. DO the project multiple times
4. KNOW the architecture (not just the commands)
5. KNOW the application (what it needs, how it connects)

"If you do it few times and you make sure you know
 the architecture, you know the application...
 you can anytime do this."

INTERVIEW VALUE:
  → Architecture understanding > command memorization
  → Drawing diagrams > reciting steps
  → Explaining WHY > explaining HOW

PROJECT MEETING VALUE:
  → Understanding the flow helps containerize any application
  → Same patterns apply: services, secrets, storage, ingress
```

***

## 🔷 Complete Project Object Map (Final Reference)

```
kubedefs/
  ├── secret.yaml        → Secret: app-secret (db-pass, rmq-pass)
  ├── db-deployment.yaml → Deployment + PVC + Service: vproDB
  ├── mc-deployment.yaml → Deployment + Service: vprocache
  ├── rmq-deployment.yaml→ Deployment + Service: vpromq
  ├── app-deployment.yaml→ Deployment + Service: vproapp
  └── ingress.yaml       → Ingress: host/path → vproapp service

External:
  └── ingress-controller → kubectl apply -f <url> (creates AWS LB)

Infrastructure:
  ├── kOps cluster       → EC2 nodes, VPC, SGs, IAM
  ├── Route 53 zone      → DNS for cluster
  ├── kOps EC2 instance  → management workstation
  └── StorageClass       → EBS volume provisioner (cluster-default)
```

***

## 🔷 Reusable Engineering Pattern: Architecture-First Kubernetes Deployment

```
PATTERN: Understand Application → Map to K8s Objects → Deploy → Verify → Clean

1. UNDERSTAND the application:
   What services does it have? (app, db, cache, queue)
   How do they connect? (hostnames, ports, credentials)
   What data needs persistence? (database)
   What's sensitive? (passwords)

2. MAP to Kubernetes objects:
   Service → K8s Service (ClusterIP)
   Container → Pod (in Deployment)
   Connection info → application.properties (use K8s service names)
   Passwords → Secret
   Persistent data → PVC + StorageClass
   External access → Ingress + Ingress Controller

3. WRITE manifests (kubedefs/ directory)

4. DEPLOY: kubectl apply -f .

5. VERIFY: access through ingress, test each backend

6. CLEAN: kubectl delete -f . → kops delete cluster

This pattern works for ANY application being containerized:
  → Identify components → map to K8s objects → deploy declaratively
  → "It'll be easier for you when you want to really
     containerize applications."
```

This final lecture's greatest value is not in any new concept — it's in the **unified view**. Every object, every connection, every data flow from the entire project is visible in one architecture diagram. Mastering this diagram means mastering the project. [\[360-summarize \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/360-summarize.txt)
