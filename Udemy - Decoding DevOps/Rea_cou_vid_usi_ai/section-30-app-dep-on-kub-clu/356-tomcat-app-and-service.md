# Kubernetes Tomcat Deployment & Service with Init Containers — Deep Learning Material

**Source:** [356-tomcat-app-and-service.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt?EntityRepresentationId=79904c14-7078-4b2a-9bf8-e579e675b1da) (VTT Caption File) [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Application Architecture Context

This lecture deploys the **final service** in a Kubernetes-based vprofile application stack. The vprofile application runs inside **Tomcat**, and a Docker image for it (`vprocontainers/vproapp`) was already built and pushed to Docker Hub during a previous containerization project. The backend services — MySQL (vprodb), Memcached (vprocache01), and RabbitMQ (vpromq01) — are already deployed as Kubernetes Deployments and Services in the cluster. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

This lecture creates two Kubernetes resources for the Tomcat frontend:

1. A **Deployment** — to run the Tomcat Pod with the vprofile application.
2. A **Service** (ClusterIP) — to expose the Tomcat Pod internally within the cluster.

The external-facing connectivity (connecting a load balancer to this service) will be handled by an **Ingress** resource in the next lecture. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## 1.2 Init Containers — Ordered Startup Dependencies

Init containers are the most significant concept introduced in this lecture. The core problem they solve is **startup ordering**: the Tomcat frontend application depends on backend services (database, cache, message queue). If the Tomcat Pod starts before the backends are ready, the application may fail to connect, throw errors, or crash. The instructor wants to guarantee that all backend services are **up and running** before the Tomcat container starts. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

An **init container** is a special container defined within a Pod that runs **before** the main application container. The lifecycle is strict and sequential: [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

1. The init container starts first.
2. It executes its assigned task.
3. When the task completes successfully (exit code 0), the init container **dies**.
4. Only **then** does the main container start.

If there are multiple init containers, they run **in sequence** — each must complete before the next starts. In this lecture, three init containers are defined (one each for vprodb, vprocache01, and vpromq01), each checking whether its corresponding backend service is reachable. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

The init containers use the **BusyBox** image — a minimal Linux image that provides basic utilities like `nslookup` and shell scripting, perfect for lightweight probe tasks. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

> 🔍 **Deep Dive**
> The instructor notes: *"There are other ways from Kubernetes also. There are other ways to create a link like that."* Init containers are one approach to startup dependencies. Kubernetes also offers readiness probes, liveness probes, and startup probes on the main containers themselves. However, init containers provide the most explicit guarantee: the main container literally **cannot start** until all init containers have completed. This is the strongest form of startup ordering available in a Pod definition. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

> ⚠️ **Expert Note**
> The instructor explicitly states that this init container setup is *"not really mandatory"* for the vprofile application specifically — it will come up without problems. But he includes it because many real applications **do** require backends to be up first. The pattern is demonstrated for transferable learning, not because this specific app demands it. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## 1.3 The nslookup Probe — How Init Containers Check Backend Readiness

Each init container runs a **Bash `until` loop** that repeatedly attempts to resolve the Kubernetes service name of a backend service using `nslookup`. The logic is: [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

* `nslookup` takes a hostname and tries to resolve it to an IP address.
* If the backend **Service** exists and has backend Pods running, `nslookup` succeeds — it resolves the service name to the backend Pod IPs. The exit code is **0** (success in Linux).
* If the backend Service doesn't exist yet or has no ready Pods, `nslookup` fails — exit code is **non-zero**.
* The `until` loop continues running until `nslookup` returns exit code 0.
* Between each attempt, the loop sleeps for **2 seconds**, then retries.
* While waiting, it prints a message: *"waiting for mydb"* (or equivalent).

Once `nslookup` succeeds, the until loop completes, the init container's command finishes, the container dies, and the next init container (or the main container) starts. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

### Fully Qualified Service Name Resolution

The `nslookup` command does not use just the bare service name (e.g., `vprodb`). It uses the **fully qualified domain name (FQDN)** within the Kubernetes cluster DNS: [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

```
vprodb.<namespace>.svc.cluster.local
```

In the command, the namespace is dynamically injected using **command substitution** — a shell construct that retrieves the current namespace at runtime. This makes the init container portable: it automatically adapts to whatever namespace the Pod is deployed in, rather than hardcoding a namespace. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

The FQDN structure breaks down as:

* `vprodb` — the Kubernetes Service name
* `<namespace>` — the namespace where the service lives (injected dynamically)
* `svc` — indicates this is a Service resource
* `cluster.local` — the default Kubernetes cluster DNS domain

The instructor explains: *"Just the service name will not resolve to the complete name"* — you need the full path for reliable DNS resolution within init containers. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## 1.4 Kubernetes Service (ClusterIP) for Tomcat

The Tomcat Service is of type **ClusterIP** — it is accessible only **internally** within the cluster. External users cannot reach it directly. This is intentional: external access will be handled by an **Ingress** resource (created in the next lecture) that connects an external load balancer to this ClusterIP service. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

The Service configuration uses:

* **Port (frontend):** 8080 — the port the service listens on within the cluster.
* **TargetPort (backend):** 8080 — the port on the container where Tomcat actually runs. Alternatively, the **container port name** (defined in the Deployment as `vproapp-port`) could be used instead of the numeric value.
* **Selector:** `app: vproapp` — matches the label on the Tomcat Pods, telling the Service which Pods to route traffic to.

The Service name (`vproapp-service`) is important because the **Ingress** resource in the next lecture will reference this exact name to know where to route incoming external requests. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## 1.5 Workflow Pattern — Copy, Modify, Apply

The instructor demonstrates a practical workflow pattern used throughout the Kubernetes deployment process: rather than writing manifests from scratch, he **copies an existing manifest** (in this case, the Memcached deployment and service YAML files) and **modifies** the relevant fields — names, labels, image, ports, and container-specific configuration. This is a common operational pattern because Kubernetes manifests share a consistent structure across resource types. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a **Kubernetes Deployment** for the Tomcat-based vprofile application and a **ClusterIP Service** to expose it internally. The Deployment includes **init containers** that wait for backend services (MySQL, Memcached, RabbitMQ) to become available before starting the Tomcat container. After this lecture, external access via Ingress will be configured in the next lecture. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Step 1: Create the Deployment Manifest — `appdeploy.yaml`

Copy the content from the existing Memcached deployment manifest (`mcdep.yaml`) into a new file called `appdeploy.yaml`, then modify the following fields: [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

### Modified Fields:

| Field                                       | Value                    | Reason                                                             |
| ------------------------------------------- | ------------------------ | ------------------------------------------------------------------ |
| `metadata.name`                             | `vproapp`                | Identifies the Deployment                                          |
| `spec.containers[0].name`                   | `vproapp`                | Container name within the Pod                                      |
| `spec.containers[0].image`                  | `vprocontainers/vproapp` | The Docker Hub image built during the containerization project     |
| `spec.containers[0].ports[0].name`          | `vproapp-port`           | Named port for reference in Services                               |
| `spec.containers[0].ports[0].containerPort` | `8080`                   | Tomcat runs on port 8080 (known from the containerization project) |

**Verification checkpoint:** Cross-check the image name, port number, and port name against the `kube-app` branch to ensure consistency. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Step 2: Add Init Containers to the Deployment

Below the main `containers` section (at the same level), add an `initContainers` section. Three init containers are defined, one for each backend service: [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

```yaml
initContainers:
  - name: init-db
    image: busybox
    command: ['sh', '-c', 'until nslookup vprodb.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for mydb; sleep 2; done']
  - name: init-cache
    image: busybox
    command: ['sh', '-c', 'until nslookup vprocache01.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for mycache; sleep 2; done']
  - name: init-mq
    image: busybox
    command: ['sh', '-c', 'until nslookup vpromq01.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for mymq; sleep 2; done']
```

**Command breakdown (using the DB init container as example):**

| Part                                    | Meaning                                                                                                               |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `image: busybox`                        | Minimal Linux image providing `nslookup` and shell utilities                                                          |
| `command: ['sh', '-c', '...']`          | Runs the string as a shell command                                                                                    |
| `until ... ; do ... ; done`             | Bash `until` loop — repeats until the condition succeeds (exit code 0)                                                |
| `nslookup vprodb.$(...)...`             | Tries to DNS-resolve the backend service FQDN                                                                         |
| `$(cat /var/run/secrets/.../namespace)` | Command substitution — reads the current namespace from the Pod's service account mount (makes it namespace-portable) |
| `.svc.cluster.local`                    | Completes the Kubernetes internal DNS FQDN                                                                            |
| `echo waiting for mydb`                 | Prints a status message while waiting                                                                                 |
| `sleep 2`                               | Waits 2 seconds between retry attempts                                                                                |

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

**How to find this pattern:** The instructor notes this comes directly from the **Kubernetes documentation**. Search for *"Kubernetes init containers"* — the official docs have an example using the same `nslookup` + `until` loop pattern. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

**Execution flow:**

1. Pod is scheduled → init-db starts → loops `nslookup vprodb...` every 2 seconds.
2. When vprodb Service resolves → init-db completes → init-db container dies.
3. init-cache starts → loops `nslookup vprocache01...`.
4. When vprocache01 resolves → init-cache completes → dies.
5. init-mq starts → loops `nslookup vpromq01...`.
6. When vpromq01 resolves → init-mq completes → dies.
7. **Main container** (`vproapp` / Tomcat) starts.

**Service names used must match** the actual Kubernetes Service names of the backend deployments:

* `vprodb` — MySQL service
* `vprocache01` — Memcached service
* `vpromq01` — RabbitMQ service

If these names do not match, the `nslookup` will never resolve and the init containers will loop forever — the main container will never start. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Step 3: Create the Service Manifest — `appservice.yaml`

Copy the content from the existing Memcached service manifest (`mcservice.yaml`) into a new file called `appservice.yaml`, then modify: [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vproapp-service
spec:
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  selector:
    app: vproapp
  type: ClusterIP
```

**Field-by-field breakdown:**

| Field                      | Value             | Meaning                                                                                                       |
| -------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------- |
| `metadata.name`            | `vproapp-service` | Service name — referenced by Ingress in the next lecture                                                      |
| `spec.ports[0].port`       | `8080`            | The port the Service listens on inside the cluster                                                            |
| `spec.ports[0].targetPort` | `8080`            | The port on the container to forward to (Tomcat's port). Could alternatively use the port name `vproapp-port` |
| `spec.selector.app`        | `vproapp`         | Matches the Pod label from the Deployment — this is how the Service knows which Pods to route traffic to      |
| `spec.type`                | `ClusterIP`       | Internal-only access. External access will come via Ingress (next lecture)                                    |

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

**Why ClusterIP:** The Tomcat service does not need to be directly exposed to the internet. An Ingress resource (next lecture) will create a load balancer that routes external traffic to this ClusterIP service. The service name `vproapp-service` is the reference the Ingress will use. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Step 4: Save Both Files

Save `appdeploy.yaml` and `appservice.yaml`. These will be applied along with the Ingress configuration in the next lecture when the full stack is brought up. [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

**Pre-application checklist:**

* Image name matches Docker Hub: `vprocontainers/vproapp` ✓
* Container port: `8080` ✓
* Init container service names match backend Service names: `vprodb`, `vprocache01`, `vpromq01` ✓
* Service selector matches Deployment label: `app: vproapp` ✓
* Service type is ClusterIP ✓

***

## Looking Ahead

The architecture after this lecture: [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

```
[Internet] → [Load Balancer] → [Ingress (next lecture)]
                                    ↓
                              vproapp-service (ClusterIP :8080)
                                    ↓
                              vproapp Pod (Tomcat :8080)
                                    ↓ (connects to)
                     vprodb / vprocache01 / vpromq01 Services
                                    ↓
                     MySQL / Memcached / RabbitMQ Pods
```

The Ingress will connect the external load balancer to `vproapp-service`, completing the end-to-end traffic flow.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
This lecture = final service in K8s vprofile stack
  Tomcat Deployment + ClusterIP Service
  Image: vprocontainers/vproapp (pre-built, on Docker Hub)
  Port: 8080 (Tomcat)
  Key feature: init containers for startup ordering
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Init Container Mechanism

```
Pod startup sequence:
  init-db ──► init-cache ──► init-mq ──► MAIN CONTAINER (Tomcat)
    │              │              │
    ▼              ▼              ▼
  nslookup       nslookup       nslookup
  vprodb         vprocache01    vpromq01
    │              │              │
  resolves?      resolves?      resolves?
  yes → die      yes → die      yes → die → Tomcat starts
  no → sleep 2   no → sleep 2   no → sleep 2
       retry          retry          retry

All init containers use BusyBox image
Each runs independently, sequentially
Main container CANNOT start until ALL init containers complete
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## nslookup Probe Command

```
until nslookup <service>.<namespace>.svc.cluster.local; do
  echo waiting for <name>;
  sleep 2;
done

Namespace injection: $(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
  → reads namespace from Pod's service account mount
  → makes the probe namespace-portable

Exit code: 0 = resolved (service up) → loop exits → container dies
           non-zero = failed → loop continues → retry in 2s
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## FQDN Structure

```
vprodb.default.svc.cluster.local
  │       │      │      │
  │       │      │      └── cluster DNS domain
  │       │      └── resource type (Service)
  │       └── namespace (dynamic)
  └── service name (must match backend K8s Service)
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Deployment Manifest Key Fields

```
Deployment: vproapp
  containers:
    - name: vproapp
      image: vprocontainers/vproapp    ← Docker Hub
      containerPort: 8080              ← Tomcat
      portName: vproapp-port
  initContainers:
    - init-db    → nslookup vprodb
    - init-cache → nslookup vprocache01
    - init-mq    → nslookup vpromq01
    All use: busybox image + until loop + sleep 2
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Service Manifest Key Fields

```
Service: vproapp-service
  type: ClusterIP (internal only)
  port: 8080 → targetPort: 8080
  selector: app=vproapp (matches Deployment Pod label)
  
  Referenced by: Ingress (next lecture) → routes external LB traffic here
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Label-Selector Linkage

```
Deployment Pod template:
  labels:
    app: vproapp  ──────────────┐
                                │ MUST MATCH
Service:                        │
  selector:                     │
    app: vproapp  ──────────────┘

Mismatch → Service finds no Pods → traffic goes nowhere
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Traffic Flow (Full Stack After Ingress)

```
Internet → Load Balancer → Ingress
              ↓
        vproapp-service (ClusterIP :8080)
              ↓
        vproapp Pod (Tomcat :8080)
              ↓ connects to
    ┌─────────┼─────────┐
    ▼         ▼         ▼
  vprodb   vprocache01  vpromq01
  (MySQL)  (Memcached)  (RabbitMQ)
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Workflow Pattern: Copy → Modify → Apply

```
Source: existing working manifest (mcdep.yaml / mcservice.yaml)
  → Copy to new file (appdeploy.yaml / appservice.yaml)
  → Change: name, image, ports, labels, selectors
  → Add: init containers (new for this deployment)
  → Verify: cross-check against branch / Docker Hub
  → Save → apply in upcoming lecture
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Init Container Service Name Dependencies

```
init-db    → must match Service name: vprodb
init-cache → must match Service name: vprocache01
init-mq    → must match Service name: vpromq01

Wrong name → nslookup never resolves → init loops forever → main container NEVER starts
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

## Reusable Engineering Patterns

**Startup Dependency Ordering Pattern (Init Containers)**

```
Problem: Frontend starts before backends → connection failures
Solution: Init containers probe backend readiness before main container starts

Mechanism:
  Init container runs probe (nslookup/curl/nc)
  Success → init dies → next init or main starts
  Failure → retry loop → blocks main container

Recurrence: Docker healthcheck + depends_on, systemd After/Requires,
            any system with ordered service startup
```

**DNS-Based Service Discovery Pattern**

```
Components find each other by NAME, not IP
  nslookup <service-name> → resolves to Pod IPs via Kubernetes DNS
  
  Service exists + Pods ready → resolves ✓
  Service missing / Pods not ready → fails ✗
  
  DNS resolution = proxy for "is this service alive?"
  
Recurrence: Cloud DNS private zones, Consul, service meshes,
            any system where DNS = service health indicator
```

**ClusterIP + Ingress Layering Pattern**

```
Internal service (ClusterIP) → not directly exposed
External access (Ingress) → connects LB to internal service by name

Separation: internal routing ≠ external exposure
  Change external access without touching internal service
  Change internal service without touching external routing
  
Recurrence: reverse proxy → backend, API gateway → microservice
```

 [\[356-tomcat...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/356-tomcat-app-and-service.txt)

***

This completes the full reconstruction of the Tomcat Deployment & Service lecture. **Theory** explains init containers, DNS probing, and ClusterIP architecture. **Practical** walks through every manifest field and the init container command. The **Compression Map** enables rapid recall of the startup sequence, FQDN structure, and traffic flow. Let me know if you'd like any section refined! 🚀
