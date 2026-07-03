# ☸️ Kubernetes Services — NodePort, ClusterIP, LoadBalancer: Exposing Pods, Label Selectors, and Service Discovery

**Source:** Kubernetes Section — Service (Caption File) [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

This is a **critical Kubernetes networking lecture** that teaches the **Service** resource — the mechanism for exposing pods as network endpoints. The instructor explains why services exist (pods are mortal with unstable IPs), introduces the three service types (**NodePort**, **ClusterIP**, **LoadBalancer**), walks through the port architecture (node port → service frontend port → backend/container port), demonstrates label-selector-based auto-discovery, and performs hands-on creation and testing of NodePort and LoadBalancer services on a real EKS cluster. The lecture establishes the networking foundation for all Kubernetes communication — between users and pods, and between pods themselves. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. Why Services Exist — The Problem of Mortal Pods

The starting point is a fundamental problem with pods: **pods are disposable**. The instructor connects this directly to the earlier Docker concept: **"I said containers are disposable. But yes, same is with the pod."** When you upgrade a container image, you don't modify the running pod — you **replace it** with a new pod. This means pods are constantly being created and destroyed. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

Pods have IP addresses, but because pods are mortal, **their IPs are not static**. A pod running MySQL today at IP `10.0.1.5` might be replaced tomorrow by a new pod at `10.0.2.9`. If your Tomcat pod is configured to connect to MySQL at `10.0.1.5`, it breaks when MySQL is replaced.

The solution: **you need something static — an endpoint that doesn't change even when the pods behind it are replaced.** This is exactly what a Kubernetes Service provides. The instructor draws a direct parallel to AWS: **"Service gives that endpoint like what ELB does — Elastic Load Balancer does to EC2 instances. It gives us static endpoints so we can access the elastic load balancer. Behind it, you can keep deleting and creating your EC2 instances."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

A Service is a stable network abstraction that sits in front of pods, provides a **static IP address** and **DNS name** that never changes (as long as the service exists), and forwards traffic to the appropriate pods behind it. The pods can come and go — the service endpoint remains constant.

***

## 2. The Three Service Types — When to Use Each

Kubernetes has three types of services, each designed for a different networking scenario: [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

### NodePort — External Access (Non-Production)

NodePort opens a **specific port on every node** in the cluster and maps it to the service. When you access any node's IP address on that port, the request reaches the service, which forwards it to the appropriate pod. The instructor compares it directly to **Docker port mapping**: **"Similar to port mapping. We have seen in Docker — a host port you pick up and you map it with the container port. It's exactly the same way."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

NodePort is for **non-production use cases** — development, testing, quick access. The instructor is explicit: **"Mostly it's for non-prod purpose, not for production, not for exposing the frontend to the production."** The reason is that NodePort requires knowing node IP addresses and uses high-numbered ports (30000-32767), which isn't user-friendly for production traffic.

### ClusterIP — Internal Communication Only

ClusterIP creates a service that is **only accessible from within the cluster** — no external port, no node port, no load balancer. It's for **internal communication between pods**: Tomcat connecting to MySQL, a frontend pod connecting to a backend pod. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

The instructor gives the example: **"Tomcat connecting to MySQL — for MySQL you need a static endpoint, so you can create a service of type ClusterIP."** MySQL doesn't need to be accessed from the internet; it only needs to be reachable by other pods inside the cluster.

### LoadBalancer — External Access (Production)

LoadBalancer creates an **actual cloud load balancer** (on AWS, it creates an Elastic Load Balancer) and maps it to the service. Users access the load balancer's DNS name/IP, and traffic flows to the pods. The instructor states this is **for production use cases**: **"We are running a Tomcat pod and I want users from the internet to access that. I will create the service of type LoadBalancer."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

The instructor emphasizes that on AWS, this **literally creates an ELB**: **"If you go to AWS console load balancer, you should even see that load balancer."** The integration is automatic — Kubernetes talks to the cloud provider's API and provisions the load balancer.

**Summary of when to use each:** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

* **Frontend (external users → pods):** LoadBalancer (production) or NodePort (non-production)
* **Backend (pods → pods):** ClusterIP (internal only)

***

## 3. The Port Architecture — Three Levels of Ports

Understanding the port architecture is essential. A service has up to **three port levels**, and the instructor walks through each carefully: [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Node Port (External Port)** — The port opened on the node itself. Range: 30000–32767. This is the entry point from the outside network. When you access `<node-IP>:30001`, you hit this port. Only relevant for NodePort and LoadBalancer types.

**Service Port (Internal Frontend Port)** — The port on the service's own ClusterIP. This is the internal frontend port. Other pods within the cluster use this port to access the service. The instructor clarifies: **"Port 80 means it's a frontend port, but internal frontend port. You cannot access it from the outside network."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Target Port (Backend/Container Port)** — The port on which the container inside the pod is actually listening. This **must match** the container's listening port. The instructor emphasizes: **"Backend port and the container port should be exactly same."**

The request flow for NodePort: `User → Node IP:NodePort → Service ClusterIP:Port → Pod IP:TargetPort → Container` [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

For LoadBalancer, the flow adds one more layer: `User → ELB:Port → Node:NodePort → Service → Pod:TargetPort → Container`

<details>
<summary>🔍 Deep Dive</summary>

The instructor reveals that a LoadBalancer service **automatically creates a NodePort** even if you don't specify one: "You'll be saying, hey, you said there is no node port. Of course there is a node port, but we have not mentioned it." When you create a LoadBalancer service without specifying a node port, Kubernetes picks a **random port from the 30000-32767 range** and assigns it. The ELB then routes traffic to the worker nodes on this auto-assigned node port. This means LoadBalancer is architecturally NodePort + an actual load balancer on top.

</details>

***

## 4. Label Selectors — How Services Find Their Pods

Services don't know specific pod IPs — they discover pods through **label selectors**. When you create a service, you define a `selector` with a label (e.g., `app: vproapp`). The service automatically finds **all pods that have this matching label** and routes traffic to them. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

The instructor highlights the power of this: **"If I run exactly a third pod, exactly same with same label, my third pod will be automatically included under the service — auto discovery."** You don't need to reconfigure the service when adding or removing pods. As long as a pod has the matching label, the service includes it.

**Two things are critical when creating a service:** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

1. **Label selector must match the pod's label** — mismatch means the service finds no pods.
2. **Target port must match the container's port** — mismatch means traffic reaches the pod but hits the wrong port.

The instructor also shows that the service's `endpoints` field automatically populates with the pod's IP: **"Automatically it has mapped it. We did not mention — we just mentioned the label selector. So automatically it's discovered and mapped."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

***

## 5. Service is Not a Pod — It's Proxy Rules

The instructor makes a critical architectural clarification: **"Service is across your cluster. It's not on a worker node. It's not a pod, it's not a container. It is rule or some rules, proxy rules."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

A service is not a running process — it's a set of **iptables/IPVS rules** distributed across all nodes (worker and master). Every node in the cluster has these rules, which is why you can access a NodePort service from **any node**, even if the pod is running on a different node. The instructor demonstrates this: **"It really doesn't matter which node our pod is running. We are going to access the service. And service is across all the node. Even at the master node."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

***

## 6. Target Port by Name — A Cleaner Alternative

The instructor shows that instead of specifying `targetPort: 8080` (a number), you can reference the **port name** defined in the pod's definition file. If the pod defines its container port with a name (e.g., `name: vproapp-port`), the service can use `targetPort: vproapp-port` instead of the number. The instructor prefers this: **"There's too many numbers. Name should be better here."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

This makes service definitions more readable and resilient to port number changes — if the container port number changes but the name stays the same, the service doesn't need updating.

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are creating Kubernetes Services to expose a Tomcat pod (running the Vprofile application) to external users. We'll create a **NodePort service** first (for understanding), then delete it and create a **LoadBalancer service** (for production-like access). Both use label selectors to discover the pod. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Why it matters:** Without services, pods are unreachable. Every application deployed on Kubernetes needs services for both external access and internal communication.

**Final outcome:** The Vprofile Tomcat application accessible via a browser — first through a node IP:port (NodePort), then through an AWS ELB URL (LoadBalancer).

***

## Step 1: Verify the Running Pod

**What we are doing:** Confirming we have a Tomcat pod running with the correct label and port.

The instructor has a pod already running from a previous lecture's definition file. Two pieces of information must be extracted from the pod for the service: [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

1. **Label** — the pod's label (e.g., `app: vproapp`). The service's selector must match this.
2. **Container port** — the port the container listens on (e.g., `8080`). The service's target port must match this.

**View the pod definition:**

```bash
kubectl get pod
```

Verify the pod is running. The instructor also prints/views the pod's YAML to confirm the label and port.

**Connection to flow:** Pod is running. Now create a service to expose it.

***

## Step 2: Write the NodePort Service Definition File

**File:** `vproapp-nodeport.yaml` [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vproapp-nodeport
spec:
  type: NodePort
  ports:
    - port: 80
      nodePort: 30001
      targetPort: vproapp-port
      protocol: TCP
  selector:
    app: vproapp
```

**Line-by-line breakdown:**

* `apiVersion: v1` — Services use API version v1.
* `kind: Service` — Resource type is Service (capital S).
* `metadata: name:` — Name of the service.
* `spec: type: NodePort` — Explicitly declares this as a NodePort service.
* `ports:` — List of port mappings (starts with `-` because it's a YAML list).
* `port: 80` — The **internal frontend port** (service's ClusterIP port). Other pods inside the cluster use this port.
* `nodePort: 30001` — The **external port** opened on every node. Must be in range 30000-32767.
* `targetPort: vproapp-port` — The **backend port** on the container. Here, using the port **name** defined in the pod spec instead of the number `8080`. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)
* `protocol: TCP` — Network protocol.
* `selector: app: vproapp` — Label selector. The service routes traffic to all pods with label `app: vproapp`.

**Key alignment rules:**

* `selector` must be at the **same indentation level** as `ports` and `type` (all under `spec`).
* The instructor encounters a YAML indentation error and fixes it: **"Selector is at the same level as the ports and as the type."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Common mistake:** YAML indentation errors — selector nested under ports instead of being a sibling. This causes the service to be created without a selector, meaning it discovers no pods.

***

## Step 3: Create the NodePort Service

```bash
kubectl create -f vproapp-nodeport.yaml
```

* `kubectl create` — Creates a resource.
* `-f` — From file.
* `vproapp-nodeport.yaml` — The definition file. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**The instructor encounters a syntax error on first attempt.** Fix: correct the YAML indentation so `selector` is at the same level as `ports` and `type`. After fixing, the service creates successfully.

**Verify:**

```bash
kubectl get svc
```

**Expected output:** Two services — the default `kubernetes` service (ignore) and `vproapp-nodeport` showing:

* **Type:** NodePort
* **ClusterIP:** An internal static IP
* **Ports:** `80:30001/TCP` (internal frontend port : external node port) [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Detailed verification:**

```bash
kubectl describe svc vproapp-nodeport
```

Shows the **Endpoints** field — the pod IP and port that the service has automatically discovered. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Confirm auto-discovery:**

```bash
kubectl describe pod <pod-name> | grep IP
```

The pod's IP matches the endpoint listed in the service. **"Automatically it has mapped it."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Connection to flow:** Service created and linked to the pod. Now access it from outside.

***

## Step 4: Access the Application via NodePort

**What we are doing:** Accessing the Tomcat application through a browser using the node's IP and the node port.

**Pre-requisite — Security Group:** The instructor updates the worker node's AWS security group to allow **all traffic from My IP**. This is because NodePort uses a non-standard port (30001) that isn't open by default. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Access URL:** `http://<any-node-IP>:30001`

The instructor emphasizes: **"It really doesn't matter which node our pod is running. We are going to access the service."** You can use **any node's IP** — worker node or even master node — because the service proxy rules exist on all nodes. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Expected result:** The Vprofile Tomcat application loads in the browser.

**The instructor confirms:** **"Voila. Our Tomcat application of Vprofile is running on Kubernetes cluster."** [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Connection to flow:** NodePort works. Now replace it with LoadBalancer for production-like access.

***

## Step 5: Delete the NodePort Service

```bash
kubectl delete svc vproapp-nodeport
```

**Why:** We're replacing it with a LoadBalancer service. Only one service is needed in front of the same pods. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

***

## Step 6: Create the LoadBalancer Service

**File:** `vproapp-loadbalancer.yaml` (copied from nodeport, modified) [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vproapp-loadbalancer
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: vproapp-port
      protocol: TCP
  selector:
    app: vproapp
```

**Key differences from NodePort:**

* `type: LoadBalancer` — instead of `NodePort`.
* **No `nodePort` field** — Kubernetes auto-assigns a random node port from the 30000-32767 range.
* `port: 80` — This becomes the **load balancer's frontend port**. Users access the ELB on port 80. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Create the service:**

```bash
kubectl create -f vproapp-loadbalancer.yaml
```

**Verify:**

```bash
kubectl get svc
```

Shows the service with type LoadBalancer and an **EXTERNAL-IP** — the ELB's DNS name/IP.

**Verify in AWS Console:** Go to **EC2 → Load Balancers** — an ELB has been automatically created. The instructor confirms: **"Yeah, that's a load balancer."** The ELB shows: [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

* Two worker nodes registered as instances.
* Frontend port: 80 (as defined in the service).
* Backend port: 32654 (the auto-assigned node port).

Wait for instances to become **healthy** (health checks pass).

**Access URL:** `http://<ELB-DNS-name>` (no port needed — it's port 80, the default HTTP port). [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**The instructor confirms:** **"And there you go."** The Vprofile application loads via the ELB.

**Connection to flow:** Production-like access via LoadBalancer established.

***

## Step 7: Clean Up

```bash
kubectl delete pod/<pod-name>
kubectl delete service/<service-name>
```

**Important:** When you delete a LoadBalancer service, **Kubernetes also deletes the AWS ELB**. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

**Verify cleanup:**

```bash
kubectl get all
```

Shows all resources in the current namespace. Confirm pods and services are deleted. [\[332-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/332-service.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   Kubernetes Service — Exposing Pods as Network Endpoints
CONTEXT: Kubernetes section → networking → pods need stable access points
PURPOSE: Provide static endpoints for mortal pods + route traffic
```

***

## Why Services Exist

```
PROBLEM:  Pods are MORTAL → IPs are NOT static → can't rely on pod IPs
SOLUTION: Service = STATIC endpoint in front of pods
          → same concept as ELB in front of EC2 instances
          → pods come and go, service endpoint stays constant
```

***

## Three Service Types

```
NODE PORT         → external access (non-production)
                    opens port on EVERY node (30000-32767)
                    = Docker port mapping equivalent
                    access: <any-node-IP>:<nodePort>

CLUSTER IP        → internal access ONLY
                    no external port, no node port
                    for pod-to-pod communication (Tomcat→MySQL)
                    access: <service-name>:<port> (within cluster)

LOAD BALANCER     → external access (PRODUCTION)
                    creates REAL cloud LB (AWS ELB)
                    auto-assigns random node port internally
                    access: <ELB-DNS>:<port>
```

***

## Port Architecture (Three Levels)

```
OUTSIDE NETWORK                    INSIDE CLUSTER
─────────────────                  ──────────────────
nodePort (30001)  ──→  port (80)  ──→  targetPort (8080)
external frontend      internal        container/backend
on every node          service port    on the pod

LoadBalancer adds:
ELB:port (80) ──→ node:nodePort (auto) ──→ service:port ──→ pod:targetPort
```

***

## Request Flow

```
NodePort:
  User → nodeIP:30001 → Service(ClusterIP:80) → Pod(IP:8080) → Container

LoadBalancer:
  User → ELB:80 → node:randomNodePort → Service → Pod:8080 → Container

ClusterIP:
  OtherPod → serviceName:80 → Pod:8080 → Container
  (internal only, no external path)
```

***

## Label Selector — Auto Discovery

```
SERVICE defines:  selector: { app: vproapp }
POD has:          labels:   { app: vproapp }
                            ↓ MATCH
Service AUTOMATICALLY discovers pod → adds to endpoints

Add new pod with SAME label → auto-included
Remove pod → auto-removed
No manual mapping needed

TWO CRITICAL THINGS for service creation:
  1. selector MUST match pod label
  2. targetPort MUST match container port
```

***

## Service Is Not a Pod

```
Service = PROXY RULES (iptables/IPVS) distributed across ALL nodes
  ├── exists on every worker node
  ├── exists on master node
  └── NOT a running container or pod

Result: access ANY node's IP → rules route to correct pod
        regardless of which node the pod runs on
```

***

## LoadBalancer = NodePort + Cloud LB

```
LoadBalancer service internally:
  1. Creates a ClusterIP (internal)
  2. Auto-assigns a NodePort (random from 30000-32767)
  3. Creates cloud load balancer (AWS ELB)
  4. ELB routes to nodes on the auto-assigned NodePort

On AWS: ELB appears in EC2 → Load Balancers console
Delete service → ELB auto-deleted
```

***

## Service Definition Template

```yaml
apiVersion: v1
kind: Service
metadata:
  name: <service-name>
spec:
  type: NodePort | ClusterIP | LoadBalancer
  ports:
    - port: <internal-frontend>
      targetPort: <container-port-or-name>
      nodePort: <30000-32767>           # NodePort only, optional for LB
      protocol: TCP
  selector:
    <label-key>: <label-value>          # MUST match pod label
```

**YAML indentation rule:** `selector`, `ports`, and `type` are ALL at the same level under `spec`.

***

## Target Port by Name

```
Pod definition:
  ports:
    - containerPort: 8080
      name: vproapp-port        ← define name

Service definition:
  targetPort: vproapp-port      ← reference name instead of 8080

Benefits: readable, resilient to port number changes
```

***

## Command Reference

```
kubectl create -f <file>.yaml       → create service from definition
kubectl get svc                     → list services (name, type, IP, ports)
kubectl describe svc <name>         → detailed info (endpoints, selector, ports)
kubectl delete svc <name>           → delete service (+ cloud LB if LoadBalancer type)
kubectl get all                     → all resources in current namespace
kubectl delete pod/<name>           → delete pod
kubectl delete service/<name>       → alternative delete syntax
```

***

## Frontend vs Backend Service Pattern

```
FRONTEND (user-facing):
  type: LoadBalancer (production) or NodePort (non-prod)
  
BACKEND (internal):
  type: ClusterIP
  
Architecture:
  [User] → LB Service → [Nginx Pod] → ClusterIP Service → [Tomcat Pod]
                                     → ClusterIP Service → [MySQL Pod]
                                     → ClusterIP Service → [RabbitMQ Pod]
```

***

## Security Group Consideration (AWS)

```
NodePort: must open nodePort (30001) in worker node SG
LoadBalancer: ELB handles external access → SG on ELB
              worker node SG needs ELB→node traffic allowed

Instructor: opens "all traffic from My IP" on worker node SG
```

***

## Reusable Engineering Patterns

```
1. STABLE ENDPOINT OVER MORTAL INSTANCES → Service = static front for disposable pods
                                            (same pattern: ELB→EC2, DNS→servers, VIP→backends)

2. LABEL-BASED DISCOVERY                 → Don't hardcode pod IPs → match labels
                                            Add/remove pods dynamically → auto-included/excluded
                                            (same pattern: AWS target groups, Consul service mesh)

3. PORT LAYERING                         → external port → service port → container port
                                            Each layer can transform/remap port numbers
                                            (same pattern: NAT, reverse proxy, Docker port mapping)

4. RULES, NOT PROCESSES                  → Service is distributed proxy rules, not a running process
                                            Exists on every node → accessible from anywhere in cluster
                                            (same pattern: iptables, security groups, routing tables)

5. CLOUD INTEGRATION                     → type: LoadBalancer → Kubernetes creates REAL cloud LB
                                            Infrastructure provisioned declaratively via YAML
                                            (same pattern: Terraform, CloudFormation — declare, cloud provides)

6. NON-PROD vs PROD EXPOSURE             → NodePort for dev/test, LoadBalancer for production
                                            Same pods, different service types → different access patterns
```

***

## Rapid Recall Triggers

```
"Why services exist?"                → Pods are mortal, IPs not static → need stable endpoint
"Three service types?"               → NodePort (external/non-prod), ClusterIP (internal), LoadBalancer (external/prod)
"NodePort range?"                    → 30000-32767
"NodePort like what in Docker?"      → Docker port mapping (-p host:container)
"ClusterIP used for?"                → Internal pod-to-pod communication (Tomcat→MySQL)
"LoadBalancer creates what on AWS?"  → Actual Elastic Load Balancer (visible in AWS console)
"How service finds pods?"            → Label selector matches pod labels → auto-discovery
"Two critical things for service?"   → Selector must match pod label + targetPort must match container port
"Service is a pod?"                  → NO — it's proxy rules distributed across ALL nodes
"Can access service from any node?"  → YES — rules exist on every node (worker + master)
"LoadBalancer internally?"           → ClusterIP + auto NodePort + cloud LB on top
"Delete LB service → what happens?" → AWS ELB also auto-deleted
"targetPort by name?"                → Reference port name from pod spec instead of number
"port vs targetPort vs nodePort?"    → port=internal service, targetPort=container, nodePort=external node
"YAML indentation for selector?"     → Same level as ports and type (under spec)
"Frontend service type?"             → LoadBalancer (prod) or NodePort (dev)
"Backend service type?"              → ClusterIP (internal only)
```

***

This completes the full reconstruction of the Kubernetes Service lecture. **Theory** builds the complete conceptual model from the mortal-pod problem through the three service types to the port architecture and label-based discovery; **Practical** walks through every YAML field, command, debugging step, and AWS verification for both NodePort and LoadBalancer; and the **Mental Compression Map** compresses the three-type decision model, request flow chains, port layering, and the stable-endpoint-over-mortal-instances pattern into rapid-recall structures. <cite>turn17search7</cite>

Ready for the next Kubernetes lecture (ReplicationController / high availability), or shall I generate an **AnkiDeck CSV** covering this lecture or the full course series? 🚀
