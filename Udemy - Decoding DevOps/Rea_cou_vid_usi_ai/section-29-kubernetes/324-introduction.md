# 🎓 Deep Learning Material: Kubernetes Introduction — Architecture, Orchestration & Core Concepts

*Reconstructed from video lecture captions (324-introduction.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: Why a Single Docker Engine Is Not Enough

The lecture begins from a practical reality: all the containers run so far in the course have been running on **a single Docker Engine**. The instructor poses the critical question: *"What if that Docker Engine fails? Obviously all the containers running inside that will be down and users will not be able to access them."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

A single Docker Engine is a **single point of failure**. If that machine crashes, loses power, runs out of disk, or has a kernel panic — every container on it dies simultaneously. For learning and development, this is acceptable. For production, it is catastrophic.

The natural engineering response is **high availability through clustering** — running multiple Docker Engines across multiple machines. But a cluster of independent Docker nodes creates a new problem: who decides which containers run where? Who detects a failed node and redistributes its containers? Who balances the workload? You need a **controller** — a master node that **orchestrates** the cluster. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The instructor describes the scenario: *"Not just one single docker node, multiple docker nodes, but we will also need a master node that is going to control all these docker nodes. The master node will give instruction to the docker node about containers to run. It's going to distribute containers across your docker nodes."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

When a worker node fails, the containers that were on it need to migrate to healthy nodes — either manually or, ideally, **automatically**. The instructor describes: *"Containers on the third node failed. The node itself failed. The containers migrated to the healthy node."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

This entire pattern — a master node controlling a cluster of worker nodes, distributing containers, handling failures, and maintaining desired state — is called **container orchestration**. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.2 Container Orchestration Tools Landscape

The instructor identifies several orchestration tools, establishing Kubernetes's position among them: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

* **Docker Swarm** — From Docker directly; simpler but less feature-rich
* **Kubernetes** — The most famous; open source, originally from Google
* **Mesosphere Marathon** — From Apache (you can run Kubernetes on it)
* **AWS ECS** — Cloud-based, AWS-proprietary
* **AWS EKS** — Elastic Kubernetes Service (managed Kubernetes on AWS)
* **Azure Container Service** — Microsoft's offering
* **Google Container Engine (GKE)** — Google's managed Kubernetes
* **CoreOS Fleet, OpenShift** — Other platforms

The critical insight: *"Among all this, Kubernetes is the most famous one, and other technologies like EKS is actually Kubernetes."*  Most cloud-based orchestration services are Kubernetes underneath. Learning Kubernetes gives you transferable knowledge across all major cloud platforms. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.3 Kubernetes Origin: From Google's Borg to Open Source

The instructor provides historical context that explains Kubernetes's credibility. In **2014**, Google announced that *"everything in Google — Gmail or everything — runs on Linux containers. And each week we launch more than 2 billion containers."*  The instructor's reaction: *"Jaw dropping — not because of containers, but because of the number of containers, 2 billion containers."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The reasoning behind such numbers: **containers are disposable**. Any change requires replacing containers, and across Google's global data centers, billions of replacements happen weekly. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The technology behind this was an internal Google tool called **Borg**, which managed Linux containers (LXC — there was no Docker back then). In **mid-2014**, Google introduced **Kubernetes** as an open-source version of Borg. In **mid-2015**, Kubernetes v1.0 (stable) was released, and Google partnered with **CNCF (Cloud Native Computing Foundation)**, which now manages the project. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

Key milestones: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

* **2016:** Kubernetes goes mainstream; tools like Kops and Minikube are developed; Pokémon Go case study boosts production confidence
* **2017:** Enterprise adoption — GitHub runs on Kubernetes, Oracle joins CNCF, Istio (ingress controller) announced

The instructor emphasizes the maturity argument: *"Google was using it for decades now."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.4 Kubernetes's Relationship to Docker

A crucial clarification: *"Kubernetes is really not a replacement for Docker Engine. Kubernetes manages the cluster of Docker Engine."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

Kubernetes sits **above** the container runtime. Docker Engine (or any other container runtime) still runs the containers. Kubernetes tells the runtime **which** containers to run, **where** to run them, and **what to do** when something fails. The relationship is: Kubernetes = orchestrator/manager, Docker Engine = executor/worker. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

Furthermore, Kubernetes can manage clusters of **different container runtimes** — not just Docker. It supports Docker, containerd, Rocket (rkt), and Kubernetes CRI (Container Runtime Interface). The instructor contrasts: *"If you go with Docker Swarm, then you can only use Docker Engine. But with Kubernetes you can use other runtime environments also."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.5 Kubernetes Key Features

The instructor highlights several features that make Kubernetes powerful: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Service Discovery & Load Balancing:** When you create a container (Pod), it gets **automatically discovered** by the load balancer and registered — no manual configuration needed. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Storage Orchestration:** Kubernetes integrates with many storage systems — SAN, NAS, EBS volumes, Ceph storage. This gave people confidence to run **stateful containers** (databases, file stores). [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Automated Rollout & Rollback:** Easy to deploy a new image version and roll back if it doesn't work — *"just like we do in Beanstalk, but faster than that."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Automatic Bin Packing:** Kubernetes places containers on the node where they get the right resources based on requirements, **optimizing resource utilization** across the cluster. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Self-Healing:** If a node goes down, containers are brought to life on healthy nodes. Containers themselves are monitored — similar to Auto Scaling Group replacing failed instances, but *"the self-healing capability is much faster than Auto Scaling Group."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Configuration & Secrets Management:** Configuration stored as variables, volumes, and **secrets** (encoded values). [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.6 Kubernetes Architecture: The Control Plane (Master Node)

The Kubernetes cluster has two main components: the **master node** (also called the **control plane**) and **worker nodes**. The master manages; workers execute. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

An important operational model: *"You don't log into the worker node and run the containers. You tell it to the master node. You don't even log into master node. You connect by using some client."*   You interact with the cluster through a client tool (`kubectl`), which communicates with the master's API server. The master then orchestrates everything. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The control plane has **four primary services**: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### 1.6.1 Kube API Server

The **main hero** of Kubernetes. It handles **all incoming and outgoing communication**. Every instruction to the cluster goes through the API server. It receives requests, passes information to other services (Scheduler, etcd), and communicates with worker nodes. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The API server **exposes the Kubernetes API** — a standard interface that third-party tools (monitoring agents, logging agents, web dashboards) can integrate with. It is the **front end** of the entire cluster. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

Administrators connect to the API server using **kubectl** (kube control) — the command-line interface. The instructor emphasizes: *"You really need to master the art of kubectl if you're managing Kubernetes cluster."* There's also a web dashboard available as an integration. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

🔍 **Deep Dive:**
The instructor warns against confusing **kubectl** and **kubelet**: *"Don't get confused between kubelet and kubectl. It's quite easy to confuse between them. kubectl is our tool to connect, and kubelet is an agent running in the worker node."*   kubectl = external client tool (on your machine); kubelet = internal agent (on every worker node). [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### 1.6.2 etcd

A **key-value store** that stores **all runtime information** about the Kubernetes cluster — what Pods are running, where they're running, current state of everything. The API server reads from and writes to etcd. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The instructor emphasizes a critical operational concern: *"It should be backed up regularly. Because if this fails, you lose the current data. You will not know what Pod is running where. The containers will be still running, but you'll lose the information."*   etcd is the cluster's **memory** — lose it and you lose awareness of the cluster's state, even though workloads may still be running. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### 1.6.3 Scheduler

The Scheduler watches for new container requests and **decides which worker node should run them**. It evaluates multiple factors: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

* **Resource requirements** (CPU, memory)
* **Hardware/software constraints**
* **Policies** you've defined
* **Affinity rules** — "I want to run my container on this particular node"
* **Anti-affinity rules** — "I don't want to run my container on this particular node"
* **Data locality**

Mostly, the Scheduler decides automatically, but you can influence its decisions through affinity/anti-affinity policies. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### 1.6.4 Controller Manager

Actually a **group of multiple controllers** bundled into one process to reduce complexity: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

* **Node Controller** — Monitors worker nodes; takes action if one goes down
* **Replication Controller** — Monitors Pods; if one dies, triggers self-healing (auto-healing)
* **Endpoint Controller** — Populates endpoint objects (connects Services to Pods)
* **Service Account & Token Controller** — Manages authentication and authorization

***

## 1.7 Kubernetes Architecture: Worker Node Components

Each worker node runs three key services: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### 1.7.1 Kubelet

The **agent** running on every worker node. It listens to the master's instructions. When the Scheduler decides a particular worker should run a container, it assigns the task to that node's kubelet. The kubelet then **fetches the image and runs the container** — it does the heavy lifting that you'd otherwise do manually with `docker run -p -v ...`. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### 1.7.2 Kube-proxy

A **network proxy** running on every node. It enables network communication and can enforce **network rules** (similar to security group rules — allow/deny traffic). Its most important function: if you want to **expose a Pod to the outside world**, kube-proxy handles that routing. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### 1.7.3 Container Runtime

The actual engine that runs containers. Kubernetes supports multiple runtimes: Docker, containerd, Rocket, Kubernetes CRI. This flexibility is a key differentiator from Docker Swarm. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Optional Add-ons:** DNS, web UI, resource monitoring, cluster-level logging — often provided by third-party tools with specialization in those areas. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.8 Pods: The Abstraction Layer Between Kubernetes and Containers

A **Pod** is the smallest deployable unit in Kubernetes — it wraps one or more containers and provides them with resources (network, storage, IP address). [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The instructor provides an analogy: *"The relation between Pod and container is the same relation a VM has with the process running inside it. The VM provides all the resource to the process — network, RAM, CPU, storage — and the process just uses it. Similarly, Pod provides all the resource to a container."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Why Pods exist — the abstraction argument:** Kubernetes can use different container runtimes (Docker, Rocket, CRI). Without Pods, Kubernetes would need runtime-specific commands and configurations for each. Pods provide a **standard abstraction** — *"a standard set of commands, standard set of configuration that we do, it doesn't matter what technology we are using behind the scene."* You give instructions to the Pod, and the Pod handles the container regardless of the underlying runtime. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Pod networking:** The Pod gets the **IP address**, not the container. To access a Tomcat container running on port 8080 inside a Pod, you use the Pod's IP address + the container's port number. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

### Pod Container Patterns

The instructor identifies three patterns: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

1. **Single container Pod** — One Pod, one container. This is the **ideal and most common** pattern.
2. **Pod with volume** — One container with attached storage.
3. **Multi-container Pod** — One main container plus helper containers:
   * **Init container** — Short-lived; starts first, executes setup commands, then dies. Only after it completes does the main container start.
   * **Sidecar container** — Runs alongside the main container, helping it (e.g., log streaming agent, monitoring agent).

The critical rule: *"At any given point of time, you should have one main container only running in the Pod. The other containers will be helper containers."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The anti-pattern: *"If you have Tomcat and MySQL, you are not going to run both in the same Pod. You'll run it on different Pods."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.9 Overlay Network: How Pods Communicate Across Nodes

Pods are distributed across multiple worker nodes. A Pod on Node 1 (e.g., Tomcat) may need to communicate with a Pod on Node 3 (e.g., MySQL). This is enabled by an **overlay network** — a virtual network spanning all nodes. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The instructor uses a networking analogy to explain the architecture: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

* Each node has a **private network** (like a local area network/subnet)
* Inside each node, **bridge0** acts like a **switch** — all Pods on the same node communicate through it
* When a Pod needs to reach a Pod on another node, bridge0 forwards the request to **veth0 (or wg0)**, which acts like a **router**
* The router forwards traffic to the correct node's router, which passes it to that node's bridge, which delivers it to the target Pod

*"All your Pods, doesn't matter in what node it is, will be in that network. Every node will have a small private network. And all these private networks will be connected in one bigger network. This is overlay network."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The instructor draws a parallel to AWS VPC: the overlay network is like a VPC connecting subnets across availability zones. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## 1.10 Kubernetes Cluster Setup Tools

The instructor identifies three tools for setting up Kubernetes clusters, each for a different use case: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Minikube** — For **testing and learning only**. Creates a single-node Kubernetes cluster (master + worker on one VM) using VirtualBox on your local machine. Not suitable for production. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**kubeadm** — A popular tool for **production multi-node clusters**. Requires you to provision the machines yourself (physical, virtual, EC2, etc.), then log into each node and run setup commands. Involves many manual steps but works on any platform. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Kops** — The instructor considers this *"the most stable way of running Kubernetes cluster for production."* Originally AWS-only, now supports Google Cloud, Digital Ocean, and OpenStack. Automates more of the infrastructure provisioning compared to kubeadm. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The course will cover both Minikube and Kops. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Learning

This is a **pure theory/architecture lecture** — there are no hands-on commands to execute. The practical value lies in understanding the **operational architecture** so that when we set up clusters in subsequent lectures, every component's role and every configuration decision is already understood. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The following sections organize the operational knowledge for practical use.

***

## Operational Understanding 1: How You Interact with Kubernetes

The interaction model is fundamentally different from directly running Docker commands: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

```
[You] → kubectl → [API Server (master)] → [Scheduler] → [Kubelet (worker)] → [Container Runtime] → [Container in Pod]
```

You never SSH into worker nodes to run containers. You never directly interact with the container runtime. You send declarative instructions through `kubectl` to the API server, and the cluster's internal machinery (Scheduler, kubelet) handles execution. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

**Tool to install on your machine:** `kubectl` (the CLI client). This is the primary operational tool — the instructor says mastering it is essential. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## Operational Understanding 2: The Component Responsibility Map

When troubleshooting or understanding cluster behavior, know which component is responsible for what: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

| Symptom/Need                              | Responsible Component                                                |
| ----------------------------------------- | -------------------------------------------------------------------- |
| Can't connect to cluster                  | API Server (is it running? is kubectl configured?)                   |
| Cluster "forgot" its state                | etcd (was it backed up? did it crash?)                               |
| Container placed on wrong node            | Scheduler (check affinity/anti-affinity rules)                       |
| Node went down, containers not recovering | Controller Manager → Node Controller                                 |
| Pod died, no replacement started          | Controller Manager → Replication Controller                          |
| Container not starting on worker          | Kubelet (is it running? can it pull the image?)                      |
| Pod can't be reached from outside         | Kube-proxy (network rules, service exposure)                         |
| Container runtime errors                  | Container Runtime (Docker/containerd — is it installed and running?) |

***

## Operational Understanding 3: etcd Backup Imperative

The instructor issues a direct operational warning about etcd: *"It should be backed up regularly."* [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

If etcd fails without a backup:

* Containers **keep running** (they're processes on worker nodes — they don't know etcd exists)
* But the cluster **loses awareness** of what's running and where
* You cannot manage, scale, or recover the cluster

**Operational rule:** In any production Kubernetes setup, etcd backup is a non-negotiable operational requirement. [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## Operational Understanding 4: Cluster Setup Tool Selection

| Requirement                     | Tool         | Key Characteristics                                |
| ------------------------------- | ------------ | -------------------------------------------------- |
| Learning/testing on laptop      | **Minikube** | Single-node, VirtualBox VM, not production         |
| Production on any platform      | **kubeadm**  | Multi-node, manual setup, works anywhere           |
| Production on AWS (most stable) | **Kops**     | Automated infra provisioning, AWS/GCP/DO/OpenStack |

 [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

The course covers Minikube (for learning) and Kops (for production-grade AWS clusters). [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

***

## Operational Understanding 5: Pod Design Rules

When designing your application's Pod structure: [\[324-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/324-introduction.txt)

* **One main container per Pod** — always
* **Helper containers** (sidecar, init) are allowed alongside the main container
* **Never co-locate independent services** (Tomcat + MySQL) in the same Pod — separate Pods
* Pod gets the IP → access container via Pod IP + container port
* Init containers run first and must complete before the main container starts
* Sidecar containers run alongside the main container for the Pod's entire lifetime

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Why Kubernetes Exists

```
Single Docker Engine = single point of failure
  → Need multiple Docker nodes (cluster)
  → Need a master to control the cluster
  → Need automatic failure recovery
  = Container Orchestration

Kubernetes = the dominant orchestration tool
  Origin: Google's Borg (internal, managing 2B+ containers/week)
  Open-sourced 2014 → CNCF manages it since 2015
  Most cloud K8s services (EKS, GKE, AKS) = Kubernetes underneath
```

***

## Kubernetes ≠ Docker Replacement

```
Kubernetes MANAGES clusters of container runtimes
Docker Engine RUNS containers

Kubernetes sits ABOVE Docker (or containerd, Rocket, CRI)
  K8s = orchestrator/manager
  Docker = executor/worker

Docker Swarm → Docker only
Kubernetes → Docker, containerd, Rocket, CRI (flexible)
```

***

## Architecture: Two-Component Model

```
KUBERNETES CLUSTER
  ├── Control Plane (Master Node)
  │     ├── API Server    → ALL communication gateway (front end)
  │     ├── etcd          → Key-value store (cluster state/memory)
  │     ├── Scheduler     → Decides WHICH node runs WHICH Pod
  │     └── Controller Manager
  │           ├── Node Controller        → monitors worker nodes
  │           ├── Replication Controller  → monitors Pods (self-healing)
  │           ├── Endpoint Controller     → connects Services to Pods
  │           └── SA & Token Controller   → auth/authz
  │
  └── Worker Nodes (1..N)
        ├── Kubelet          → Agent; receives instructions, runs containers
        ├── Kube-proxy       → Network proxy; exposes Pods, enforces rules
        └── Container Runtime → Docker / containerd / Rocket / CRI
```

***

## Communication Flow

```
[You] ──kubectl──→ [API Server]
                       ├──→ [etcd] (store/retrieve state)
                       ├──→ [Scheduler] (decide placement)
                       │       └──→ [Kubelet on chosen node]
                       │               └──→ [Container Runtime]
                       │                       └──→ [Container in Pod]
                       └──→ [Controller Manager] (monitor & heal)
```

***

## kubectl vs. kubelet (CRITICAL DISTINCTION)

```
kubectl  = YOUR tool (CLI client, on YOUR machine) → connects to API server
kubelet  = AGENT (on every WORKER node) → receives instructions, runs containers

kubectl → external, client-side
kubelet → internal, server-side
```

***

## Pod Concept

```
Pod = smallest deployable unit in K8s
  ├── Wraps 1+ containers
  ├── Provides resources: IP, network, storage
  ├── Pod gets IP address (not the container)
  └── Access: Pod_IP:Container_Port

WHY Pods exist:
  K8s supports multiple runtimes (Docker, Rocket, CRI)
  Pod = ABSTRACTION layer
  Standard commands/config regardless of runtime underneath
  
  Pod : Container :: VM : Process
  (Pod provides resources, container uses them)
```

***

## Pod Patterns

```
PATTERN 1: One Pod, one container (IDEAL, most common)
PATTERN 2: One Pod, one container + volume
PATTERN 3: Multi-container Pod:
  ├── Main container (always exactly ONE)
  ├── Init container (short-lived, runs first, dies before main starts)
  └── Sidecar container (helper, runs alongside main: logging, monitoring)

ANTI-PATTERN: Tomcat + MySQL in same Pod → NEVER
  → Separate Pods for independent services
```

***

## Overlay Network

```
All Pods across all nodes → one virtual network (like VPC)

Node 1                          Node 3
┌─────────────────┐             ┌─────────────────┐
│ Pod1  Pod2  Pod3 │             │ Pod6  Pod7      │
│   └──┬──┘       │             │   └──┬──┘       │
│   bridge0        │             │   bridge0        │
│   (switch)       │             │   (switch)       │
│      │           │             │      │           │
│   veth0/wg0      │             │   veth0/wg0      │
│   (router)       │             │   (router)       │
└──────┤───────────┘             └──────┤───────────┘
       └──────── overlay network ───────┘

Same-node: Pod → bridge0 → Pod (local switch)
Cross-node: Pod → bridge0 → router → overlay → router → bridge0 → Pod
```

***

## etcd: The Cluster's Memory

```
etcd = key-value store of ALL cluster state
  API Server reads/writes etcd

etcd alive + healthy → cluster knows its state
etcd fails (no backup) →
  ├── Containers KEEP RUNNING (they're just processes)
  └── Cluster LOSES AWARENESS (can't manage, scale, recover)

OPERATIONAL RULE: Back up etcd regularly (non-negotiable)
```

***

## Key Features

```
Service Discovery + LB  → Pods auto-registered with load balancer
Storage Orchestration    → SAN, NAS, EBS, Ceph integration → stateful containers
Automated Rollout/Back   → Deploy new version, rollback if broken (faster than Beanstalk)
Bin Packing              → Place Pods on optimal nodes → maximize resource utilization
Self-Healing             → Node dies → Pods restart on healthy nodes (faster than ASG)
Config & Secrets         → Variables, volumes, encoded secrets
```

***

## Scheduler Decision Factors

```
Scheduler picks worker node based on:
  ├── Resource requirements (CPU, memory)
  ├── Hardware/software constraints
  ├── Policies
  ├── Affinity: "run on THIS node"
  ├── Anti-affinity: "DON'T run on THIS node"
  └── Data locality

Mostly automatic → override with affinity/anti-affinity rules
```

***

## Cluster Setup Tools

```
minikube  → Learning/testing → single-node → VirtualBox VM → not production
kubeadm   → Production → multi-node → manual steps → any platform
kops      → Production → most stable → automated infra → AWS/GCP/DO/OpenStack

Course covers: minikube (learning) + kops (production AWS)
```

***

## Orchestration Tools Landscape

```
Docker Swarm        → Simple, Docker-only runtime
Kubernetes          → Dominant, multi-runtime, most features
Mesosphere Marathon → Apache, can run K8s on it
AWS ECS             → Proprietary AWS
AWS EKS             → Managed Kubernetes on AWS
Azure AKS           → Managed Kubernetes on Azure
Google GKE          → Managed Kubernetes on GCP
OpenShift           → Red Hat's Kubernetes distribution

Key insight: EKS, GKE, AKS = Kubernetes underneath
  → Learn K8s = transferable to all platforms
```

***

## Reusable Engineering Patterns

| Pattern                              | Manifestation                                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| **Master/worker architecture**       | Control plane orchestrates; workers execute (same as Ansible controller/nodes, Jenkins master/agents) |
| **Single point of communication**    | API Server = sole gateway (like a load balancer front-ending backend services)                        |
| **Declarative state management**     | You declare desired state → K8s continuously reconciles actual state toward it                        |
| **Abstraction layer (Pod)**          | Decouples orchestration from runtime implementation (same principle as interfaces in programming)     |
| **Self-healing through monitoring**  | Controller Manager watches → detects failure → takes corrective action (feedback loop)                |
| **Overlay network**                  | Virtual network spanning physical boundaries (same concept as VPC spanning AZs)                       |
| **Separation of state from compute** | etcd (state) separate from workers (compute) — state must be backed up independently                  |
| **Init → Main → Sidecar pattern**    | Setup first (init), then primary work (main), with ongoing support (sidecar)                          |

***

## Core Mental Model

```
Kubernetes = Master that manages a fleet of container workers

You → kubectl → API Server (gateway)
  API Server → etcd (memory: "what should exist")
  API Server → Scheduler (brain: "where to place it")
  API Server → Controller Manager (immune system: "keep it healthy")
  Scheduler → Kubelet (hands: "run this container")
  Kubelet → Container Runtime (muscle: "execute")
  Container → Pod (skin: "abstraction wrapper")
  Pod ↔ Overlay Network ↔ Pod (nervous system: "communication")

Everything flows through API Server.
Everything is stored in etcd.
Everything runs inside Pods.
Everything communicates through overlay network.
```

***

This material captures every concept, architectural component, Pod pattern, networking model, historical context, and tool comparison from the lecture — structured for deep understanding (Theory), operational clarity (Practical), and rapid future recall (Compression Map). 🚀
