# ☸️ Kubernetes Project — Deploying vprofile Web Application on Kubernetes Cluster — Introduction — Deep Learning Material

**Source:** *Introduction* (Video Lecture Caption File) [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Situation — From Containerized to Production-Ready

At this point in the course, the vprofile web application has already been **containerized** (Docker images built and tested in previous projects). The containers work — you can run them, the application functions. But running containers for development/testing is fundamentally different from running them **for production**. The instructor opens with this exact distinction: "Running containers for production is a little different." [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

The gap between "containers work" and "containers are production-ready" is filled by a set of requirements that Docker alone cannot satisfy. Understanding these requirements explains why Kubernetes exists and why this project is necessary.

***

## 1.2 Production Container Requirements — The Seven Demands

The instructor lays out the specific requirements for running containers in production: [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

**1. High Availability (containers):** Containers should not go down. If one instance of the application stops, users shouldn't notice. There must be multiple replicas running simultaneously so that if one fails, others continue serving traffic.

**2. High Availability (compute nodes):** It's not just the containers that need redundancy — the underlying **compute nodes** (the machines running the containers) also need high availability. If a node goes down, the containers on it must be automatically rescheduled to other nodes.

**3. Fault Tolerance and Auto-Healing:** If containers stop responding (crash, hang, become unhealthy), the system should **automatically detect** the failure and **replace** the unhealthy containers without human intervention. This is auto-healing — the system repairs itself.

**4. Convenient Scaling:** It should be easy to scale containers up (add more replicas when demand increases) and down (remove replicas when demand decreases). Scaling the **compute resources** (the nodes) should also be convenient.

**5. Platform Independence:** The containers should be able to run on **local machines, cloud platforms, virtual machines, physical machines** — any compute environment. The same container images, the same orchestration definitions, regardless of where they run.

**6. Portability Across Environments:** The same container setup should work across **dev, QA, and production** environments. You don't rebuild or reconfigure for each environment — the definitions are portable, and environment-specific differences are handled through configuration (ConfigMaps, Secrets). [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

**7. Flexibility and Agility:** The overall system should be easy to update, modify, and evolve without complex procedures or downtime.

Docker alone provides containerization and portability of images. But it does **not** provide multi-node scheduling, auto-healing, declarative scaling, load balancing across replicas, or rolling updates across a fleet of containers. These are orchestration capabilities — and that's what Kubernetes provides.

***

## 1.3 Why Kubernetes — The Container Orchestration Answer

**Kubernetes** is the tool that satisfies all seven production requirements listed above. The instructor positions it definitively: "Kubernetes is today the best container orchestration tool in the market. It's very mature and a rock solid platform to run your containers for production." [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

The instructor backs this with industry statistics:

* **77% of containers** run on Kubernetes
* Including RedHat OpenShift and Rancher (both built on Kubernetes): **89%**
* **56% of organizations** planned to increase Kubernetes usage in the next 12 months
* Production Kubernetes cluster usage grew from **19% to 28%** (a significant jump indicating mainstream adoption)

The key insight from these statistics: Kubernetes isn't just one option among many — it has effectively won the container orchestration market. Learning Kubernetes is not optional for DevOps engineers; it's the standard. [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

***

## 1.4 The Project Architecture — What We Are Deploying

The project deploys the **vprofile multi-tier web application** on a Kubernetes cluster. This is the same application stack that has been deployed throughout the course on VMs (manually, with Ansible), on AWS (with Beanstalk), and in Docker containers (with Docker Compose). Now it's being deployed on Kubernetes — the production-grade orchestration platform. [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

The application is multi-tier, meaning it has multiple services (web server, application server, database, caching, messaging) each running in separate containers/pods. The containerized images were built in the previous Docker project.

***

## 1.5 Two Prerequisites — Cluster and Images

The project requires exactly two things to be ready before starting: [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

**1. A Kubernetes cluster** — created using **kops** (Kubernetes Operations). The instructor references a previous project where kops was used to set up a production-grade Kubernetes cluster on AWS. The cluster must be running and accessible via `kubectl`.

**2. Containerized application images** — the Docker images built in the containerization project (vprofile web app, MySQL database, etc.) must be available in a registry (Docker Hub or private registry). The instructor says: "take note of your images which you have created in the containerization project."

These two prerequisites represent the two layers of the system: the **infrastructure** (Kubernetes cluster) and the **application** (container images). Everything in this project connects these two layers using Kubernetes objects.

***

## 1.6 The Kubernetes Objects We Will Use

The instructor lists the specific Kubernetes objects that will be used in this project: [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

**Deployment** — manages Pod replicas with rolling update capability. This is how the application containers will be deployed (as covered in the Kubernetes objects lecture — "the most used object for DevOps").

**Service** — provides stable endpoints for accessing pods. This is how the tiers of the application will discover and communicate with each other (as covered in the Kubernetes objects lecture).

**Secret** — stores sensitive configuration data (passwords, credentials) in a non-clear-text format. This is the secure variant of ConfigMap (covered in the ConfigMap lecture — same concept but for sensitive data).

**Volume** — provides persistent storage for pods. Specifically needed for the MySQL database container, which must retain data across pod restarts and rescheduling. [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

***

## 1.7 The EBS Volume and Node Labeling Strategy — Zone Affinity

The most architecturally significant detail in this introduction is the **EBS volume strategy** for the database pod. The instructor explains a specific constraint and its solution: [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

**The constraint:** The MySQL container needs persistent storage. An **EBS volume** (Elastic Block Store) will be used to store the database data. But EBS volumes are **zone-specific** — an EBS volume created in `us-west-2a` can only be attached to an EC2 instance in `us-west-2a`. It cannot cross availability zone boundaries.

**The problem:** Kubernetes schedules pods to any available node. If the database pod gets scheduled to a node in `us-west-2b` but the EBS volume is in `us-west-2a`, the volume attachment fails — the pod can't start.

**The solution:** **Label the nodes with their availability zone names**, then use **node selectors** in the database pod definition to ensure the pod is scheduled only on nodes in the same zone as the EBS volume. The instructor describes this as: "We're going to label our nodes with zone names. So when we run our DB pod, we'll select node based on the zones." [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

This is a **zone affinity** pattern: tying a pod to a specific zone because its storage is zone-bound. It's a common pattern in cloud-native Kubernetes deployments where persistent storage has locality constraints.

🔍 **Deep Dive:**
This zone-affinity requirement reveals a fundamental tension in Kubernetes: the orchestrator wants to schedule pods anywhere for maximum flexibility and resilience, but certain resources (like EBS volumes) have physical locality constraints that restrict scheduling freedom. The solution — node labels + node selectors — is Kubernetes's mechanism for expressing "schedule this pod only on nodes that match these criteria." It's a constraint-based scheduling system where labels are the constraint language.

***

## 1.8 The Progression — Same Application, Different Platforms

This project represents the culmination of a progression that runs through the entire course: [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

1. **Manual on VMs** — install and configure each service by hand
2. **Automated on VMs** — use Ansible/Vagrant to automate the same setup
3. **AWS managed services** — use Beanstalk, RDS to offload infrastructure management
4. **Containerized** — package each service as a Docker image
5. **Kubernetes** — deploy the containerized application on a production-grade orchestration platform

Each step adds a layer of automation, abstraction, and production-readiness. Kubernetes is the final deployment target — where the application runs in production with all seven requirements (HA, fault tolerance, auto-healing, scaling, portability, platform independence, flexibility) satisfied.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are deploying the containerized vprofile multi-tier web application onto a production-grade Kubernetes cluster. The final outcome: the application runs on Kubernetes with persistent database storage (EBS volume), zone-aware pod scheduling (node labels), secure credential management (Secrets), stable service endpoints (Services), and managed pod lifecycles (Deployments). [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

This is an **introduction lecture** — no commands are executed here. The practical content consists of the **prerequisites to complete** and the **execution plan** to follow in subsequent lectures.

***

## Prerequisites — What Must Be Ready Before Starting

### Prerequisite 1: Kubernetes Cluster via kops

The cluster must already be running. If not, set it up using the kops setup project from earlier in the course: [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

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

kops update cluster --name kubevpro.groophy.in --state=s3://vproile-kops-state --yes --admin
```

**Verify the cluster is ready:**

```bash
kubectl get nodes
```

All nodes should show `Ready` status.

### Prerequisite 2: Container Images

Note the Docker images created in the containerization project. You'll need the full image names and tags (e.g., `kubeimran/vprofileapp:v1`, `kubeimran/vprofiledb:v1`, etc.) for the Kubernetes definition files. [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

These images must be accessible from the Kubernetes cluster — either in a public Docker Hub repository or a private registry that the cluster can authenticate to.

***

## Execution Plan — Steps That Will Follow

The instructor outlines the execution sequence for subsequent lectures: [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)

**Step 1: Create an EBS volume** for the MySQL database pod's persistent storage. This volume must be created in a specific availability zone (e.g., `us-west-2a`).

**Step 2: Label nodes with zone names.** Tag each Kubernetes worker node with its availability zone so that pod scheduling can be constrained by zone.

**Step 3: Write Kubernetes definition files** for all objects:

* **Deployments** — for each application tier (web, app, db, cache, messaging)
* **Services** — for inter-tier communication and external access
* **Secrets** — for database passwords and application credentials
* **Volumes** — for MySQL persistent data (referencing the EBS volume)

**Step 4: Apply the definitions** to the cluster with `kubectl apply -f`.

**Step 5: Verify** the application is running, all pods are healthy, services are reachable, and the database has persistent storage.

⚠️ **Expert Note:**
The EBS volume must be created in the **same region and zone** as the node where the database pod will run. If you create the volume in `us-west-2a`, the node label and pod node selector must ensure the pod runs on a node in `us-west-2a`. Mismatching zones = volume attachment failure = pod stuck in `Pending` state.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Project Context

```
vprofile application journey:
  Manual VMs → Automated VMs → AWS managed → Containerized → KUBERNETES
                                                                ↑
                                                          THIS PROJECT

Input:  containerized images (Docker Hub) + kops K8s cluster
Output: production-grade deployment with HA, auto-heal, scaling
```

## Seven Production Requirements → Kubernetes

```
1. Container HA          → multiple pod replicas (Deployment)
2. Compute node HA       → multi-node cluster (kops, multi-AZ)
3. Fault tolerance       → auto-heal (Deployment restarts failed pods)
4. Convenient scaling    → kubectl scale / HPA
5. Platform independent  → K8s runs anywhere (cloud, local, bare metal)
6. Portable across envs  → same definitions, different ConfigMaps/Secrets
7. Flexible & agile      → rolling updates, rollbacks (Deployment)

Docker provides: containerization + image portability
Kubernetes adds: orchestration + all 7 requirements above
```

## Kubernetes Market Dominance

```
77% of containers run on Kubernetes
89% including OpenShift + Rancher (built on K8s)
56% of orgs increasing K8s usage
19% → 28% growth in production K8s clusters
```

## Two Prerequisites

```
1. KUBERNETES CLUSTER (infrastructure layer)
   → created with kops on AWS
   → kubectl get nodes → all Ready

2. CONTAINER IMAGES (application layer)
   → built in containerization project
   → available in Docker Hub (or private registry)
   → note image names + tags
```

## Kubernetes Objects Used in This Project

```
DEPLOYMENT  → manage pod replicas + rolling updates
SERVICE     → stable endpoints for pod communication
SECRET      → secure credential storage (passwords)
VOLUME      → persistent storage for MySQL (EBS)
```

## EBS Volume + Zone Affinity Pattern

```
EBS volume created in: us-west-2a
  ↓
EBS is ZONE-SPECIFIC (can't cross AZ boundaries)
  ↓
Node labels: each node tagged with its zone
  ↓
Pod node selector: DB pod → select node in us-west-2a
  ↓
Pod scheduled on correct node → EBS attaches successfully

MISMATCH: pod in zone-2b + volume in zone-2a → FAILS
  Pod stuck in Pending → volume attachment error
```

## Execution Plan (Upcoming Lectures)

```
1. Create EBS volume (specific zone)
2. Label nodes with zone names
3. Write K8s definition files:
   ├─ Deployments (all tiers)
   ├─ Services (internal + external)
   ├─ Secrets (credentials)
   └─ Volumes (EBS for MySQL)
4. kubectl apply -f <definitions>
5. Verify: pods running, services reachable, data persists
```

## Multi-Tier Architecture on Kubernetes

```
[Internet]
  │
  ▼
[Service: LoadBalancer] → [Deployment: Web/Nginx pods]
                              │
                              ▼
                         [Service: ClusterIP] → [Deployment: App/Tomcat pods]
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
              [Service]  [Service]  [Service]
              DB/MySQL   Cache     Messaging
              [Deploy]   [Deploy]  [Deploy]
                 │
                 ▼
            [Volume: EBS]
            (persistent data)
```

## vprofile Deployment Evolution

```
Platform              Orchestration    Persistence     Scaling
─────────────────────────────────────────────────────────────
Manual VMs            none             local disk      manual
Automated VMs         Vagrant+Ansible  local disk      manual
AWS Beanstalk         Beanstalk        RDS             auto (ASG)
Docker Compose        Compose          Docker volumes  manual
Kubernetes         ★  K8s controller   EBS volumes     auto (replicas/HPA)
```

## Reusable Engineering Patterns

**1. Zone-Affinity Scheduling**

```
Storage resource is zone-locked (EBS, persistent disk)
  → label nodes with zone metadata
    → constrain pod scheduling to matching zone
      → storage attaches successfully

Pattern: when resources have locality constraints,
         use metadata (labels) + selectors to enforce co-location

Same in: GCP regional persistent disks, Azure availability zones
         any system where compute must be co-located with storage
```

**2. Progressive Deployment Maturity**

```
Manual → Automated → Managed Service → Containerized → Orchestrated

Each level:
  + more automation
  + more abstraction
  + more production-readiness
  - less manual control (by design)

The application stays the SAME
The deployment mechanism evolves
```

**3. Two-Layer Architecture: Infrastructure + Application**

```
Layer 1: Infrastructure (K8s cluster via kops)
  → nodes, networking, DNS, storage

Layer 2: Application (K8s objects via kubectl)
  → deployments, services, secrets, volumes

Both must be ready independently
Then connected through definition files

Same pattern:
  Terraform (infra) + Ansible (app config)
  CloudFormation (infra) + CodeDeploy (app)
```

***

*This completes the full reconstruction. This is an introduction lecture with no hands-on execution — it establishes the production requirements that justify Kubernetes, outlines the project architecture, identifies the two prerequisites, and previews the execution plan. Theory explains the seven production requirements and the zone-affinity strategy. Practical defines the prerequisites and execution sequence. The Compression Map enables instant recall of the full architecture, the EBS zone constraint, and the project's position in the course-long deployment evolution.* [\[347-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/347-introduction.txt)
