# 🎓 Deep Learning Material: Memcached Pod & Service Setup in Kubernetes — Pattern Replication for Multi-Service Applications

*Reconstructed from video lecture captions (354-memcache-app-and-service.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Where Memcached Fits in the Application Architecture

This lecture is part of a larger project where the vprofile application's backend services (database, cache, message queue) are being deployed as separate Kubernetes Pods with their own Services. The **Memcached** component is the caching layer — it stores frequently accessed data in memory so the application doesn't hit the database for every request. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

The instructor frames Memcached as the simplest service to set up: *"Memcached is pretty easy, we just need to fetch an official Docker image for Memcached and run it in the Pod."*  Unlike databases that need volumes, passwords, and initialization, Memcached is a stateless in-memory cache that requires only an image and a port. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

***

## 1.2 The Copy-Paste-Modify Pattern: Replicating Service Setups

The most important conceptual takeaway from this lecture is not about Memcached specifically — it's about the **reusable pattern** for deploying any service in Kubernetes. The instructor states this explicitly: *"If you know how to set up one complete service — the database, the Pod, Deployment, Service, everything, volumes — if you know to do set up one complete service, then other service is similar. Just copy, paste, make the changes."* [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

The workflow is:

1. Take an existing, working Deployment YAML (in this case, from the database service)
2. Copy its structure into a new file
3. Change the **name**, **labels**, **image**, and **port** to match the new service
4. Do the same for the Service YAML
5. Ensure the **label matching** between Deployment and Service is correct

This is a deliberate engineering practice: don't write every definition from scratch — use a known-working structure as a template and modify the service-specific values. The structure (apiVersion, kind, spec hierarchy, selector mechanism) stays the same; only the identity and configuration values change. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

***

## 1.3 The Three Things That Change Between Services

When replicating a Deployment+Service setup from one component to another, three categories of information must be updated: [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

**1. Identity (Names and Labels):** The Deployment name, Pod labels, container name, and Service name all change. For Memcached, the instructor uses `vpromc` (short for vprofile Memcached) consistently across the Deployment's metadata, labels, selectors, and container name. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

**2. Image:** The Docker image changes to `memcached` — the official Memcached image from Docker Hub. This is a direct pull with no custom build needed. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

**3. Port:** The port changes to `11211` — Memcached's default port. This port must be consistent across three places: the container's `containerPort` in the Deployment, the Service's `port` (frontend), and the Service's `targetPort` (routing destination). [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

***

## 1.4 Label Matching: The Critical Connection Mechanism

The instructor emphasizes the label matching requirement twice: *"This label and this label should definitely match. Then only this Pod will be part of this Deployment."* [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

In the Deployment YAML, there are three places where labels appear:

1. **`metadata.labels`** — The Deployment's own labels (identifies the Deployment itself)
2. **`spec.selector.matchLabels`** — What the Deployment looks for to find its Pods
3. **`spec.template.metadata.labels`** — The labels assigned to the Pods

Items **2 and 3 MUST match** — the selector must match the Pod template labels. If they don't, the Deployment cannot find its Pods, and Kubernetes will reject the definition or the Deployment will report zero ready replicas. Item 1 (the Deployment's own label) can technically differ, but the instructor keeps all three consistent for clarity. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

The Service also uses a **selector** to find the Pods it should route traffic to. This selector must match the Pod labels from the Deployment template. This creates the full chain: Service selector → matches Pod labels → Pod belongs to Deployment via matchLabels. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

***

## 1.5 Service Name: Driven by Application Configuration

The Service name is not arbitrary — it's determined by the **application configuration**. The instructor opens the `application.properties` file and shows: *"Memcached, the name is vprochace01. The same name we have to give to the service so it can find it."* [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

The vprofile application is configured to look for its Memcached cache server at hostname `vprochace01` on port `11211`. In Kubernetes, a **Service name becomes a DNS entry** within the cluster. When the application Pod tries to connect to `vprochace01:11211`, Kubernetes DNS resolves `vprochace01` to the Service's ClusterIP, and the Service routes the request to the Memcached Pod. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

This means the Service name is a **contract** between the application and the infrastructure. Change the Service name without changing the application config, and the application can't find its cache server. The instructor makes this relationship explicit by keeping the `application.properties` file open while editing the Service definition. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

🔍 **Deep Dive:**
This is the same pattern used for the database service in a previous lecture — the database Service name matched what the application expected. The Service name acts as a **service discovery mechanism** in Kubernetes: the application doesn't need to know Pod IPs (which change), it just needs to know the Service name (which is stable). This is Kubernetes' built-in service discovery through DNS.

***

## 1.6 Port Name and Target Port Linking

The instructor introduces a port-naming pattern. In the Deployment, the container port is given a **name** (e.g., `vpromc-port`). In the Service definition, the `targetPort` field references this **name** instead of a raw port number. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

The instructor explains: *"We've given the name to this port — that will give it in the service definition of this file. So for service definition for this port, we need the port name and we need the label for the selector."* [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

This creates an indirect reference: Service → `targetPort: vpromc-port` → resolves to container port 11211. The benefit is decoupling — if the container port number changes, you only update the Deployment; the Service still references the port by name and automatically resolves to the new number.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a **Memcached Deployment** (one Pod running the official `memcached` image on port 11211) and a **Memcached Service** (exposing the Pod within the cluster as `vprochace01` on port 11211). The final outcome: the vprofile application can reach its cache layer via the DNS name `vprochace01:11211`. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

***

## Phase 1: Create the Memcached Deployment

### Step 1: Copy the Base Structure

Copy the content of an existing, working Deployment YAML file (the instructor uses the database deployment as a template) into a new file named `mcdeployment.yaml` (or similar Memcached deployment file). [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

### Step 2: Modify the Deployment Definition

Edit the file and change the following values: [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vpromc
  labels:
    app: vpromc
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vpromc
  template:
    metadata:
      labels:
        app: vpromc
    spec:
      containers:
      - name: vpromc
        image: memcached
        ports:
        - name: vpromc-port
          containerPort: 11211
```

**Key changes from the copied template:** [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

| Field                                | Value         | Reasoning                                                                     |
| ------------------------------------ | ------------- | ----------------------------------------------------------------------------- |
| `metadata.name`                      | `vpromc`      | Identifies this Deployment                                                    |
| All `labels` / `matchLabels`         | `app: vpromc` | Must match across selector and template — instructor emphasizes this twice    |
| `replicas`                           | `1`           | *"We don't need extra"* — cache doesn't need multiple replicas for this setup |
| `containers[].name`                  | `vpromc`      | Container name                                                                |
| `containers[].image`                 | `memcached`   | Official Docker Hub image — no tag means `latest`                             |
| `containers[].ports[].containerPort` | `11211`       | Memcached's default port                                                      |
| `containers[].ports[].name`          | `vpromc-port` | Named port — referenced by the Service's targetPort                           |

**Critical verification:** Ensure `spec.selector.matchLabels.app` and `spec.template.metadata.labels.app` are **identical** (`vpromc`). If they don't match, the Deployment can't manage its Pods. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

**Common mistake:** Forgetting to change a label or name from the copied template (e.g., leaving `db` or database-related values). The instructor warns: *"That's why you see DB DB here. Make sure you don't edit the dbservice file. This is the mcservice file you need to edit."* [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

***

## Phase 2: Create the Memcached Service

### Step 3: Copy the Base Service Structure

Copy the content of the database service file (`dbservice.yaml`) into a new file for the Memcached service (`mcservice.yaml`). [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

### Step 4: Modify the Service Definition

Edit with values from the **application.properties** file: [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vprochace01
spec:
  selector:
    app: vpromc
  ports:
  - port: 11211
    targetPort: vpromc-port
    protocol: TCP
```

**Key changes:** [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

| Field                | Value         | Source of Value                                                             |
| -------------------- | ------------- | --------------------------------------------------------------------------- |
| `metadata.name`      | `vprochace01` | From `application.properties` — the hostname the app uses to find Memcached |
| `spec.selector.app`  | `vpromc`      | Must match the Pod label from the Deployment                                |
| `ports[].port`       | `11211`       | Frontend port — what clients connect to                                     |
| `ports[].targetPort` | `vpromc-port` | Routes to the named port in the Deployment's container spec                 |

**Critical verification points:** [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

1. **Service name** (`vprochace01`) matches what's in `application.properties` — this is the DNS name the application uses
2. **Selector** (`app: vpromc`) matches the Pod labels in the Deployment template
3. **targetPort** (`vpromc-port`) matches the port name defined in the Deployment's container spec
4. **Frontend port** (`11211`) matches what the application expects to connect on

**Common mistake:** Editing the wrong file — the instructor warns about accidentally modifying the database service file instead of the Memcached service file, since the content was copied from there. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

### Step 5: Save and Cross-Reference

Save both files (`Ctrl+S`). [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

**Final verification:** Cross-check your files against the **kube-app branch** of the source code repository to ensure correctness: *"You can anytime check the kube-app branch to see the code and match it with your code."* [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

**Connection to flow:** The Memcached Deployment and Service are now defined. In the next lecture, the same pattern will be applied to RabbitMQ (Deployment + Service). Once all backend services (database, cache, message queue) are defined, the full application stack can be deployed. [\[354-memcac...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/354-memcache-app-and-service.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Memcached in the Application Stack

```
vprofile application connects to:
  ├── Database   → Service: vprodb       (port 3306)   [previous lecture]
  ├── Cache      → Service: vprochace01  (port 11211)  [THIS lecture]
  └── MQ         → Service: vprorabbit   (port ?)      [next lecture]

App finds services via DNS: hostname = Service name
  application.properties: memcached.host = vprochace01
  → K8s DNS resolves vprochace01 → Service ClusterIP → Pod
```

***

## Memcached Deployment

```
Deployment: vpromc
  replicas: 1
  image: memcached (official, Docker Hub)
  containerPort: 11211 (named: vpromc-port)
  
Labels (ALL must match):
  metadata.labels.app:                  vpromc
  spec.selector.matchLabels.app:        vpromc  ← MUST MATCH ↓
  spec.template.metadata.labels.app:    vpromc  ← MUST MATCH ↑
```

***

## Memcached Service

```
Service: vprochace01 (name from application.properties)
  selector.app: vpromc          → finds Pods with label app=vpromc
  port: 11211                   → frontend (what clients connect to)
  targetPort: vpromc-port       → routes to named port in container spec
```

***

## Connection Chain

```
[App Pod] → DNS lookup "vprochace01" → [Service: vprochace01]
  → selector matches app=vpromc → [Pod: vpromc]
    → targetPort: vpromc-port → containerPort: 11211 → Memcached process
```

***

## The Copy-Paste-Modify Pattern

```
For EACH new service in the application:

1. COPY existing working Deployment YAML → new file
2. CHANGE: name, labels, image, port
3. COPY existing working Service YAML → new file  
4. CHANGE: name (from app config), selector, port, targetPort

Three things change between services:
  ├── Identity:  names + labels (e.g., vpromc)
  ├── Image:     container image (e.g., memcached)
  └── Port:      service port (e.g., 11211)

Structure stays IDENTICAL — only values change

"If you know how to set up one complete service,
 then other service is similar. Just copy, paste, make the changes."
```

***

## Label Matching Rules

```
Deployment:
  selector.matchLabels.app  ══MUST MATCH══  template.metadata.labels.app
  (Deployment finds its Pods)

Service:
  selector.app  ══MUST MATCH══  Pod labels (from Deployment template)
  (Service routes traffic to correct Pods)

MISMATCH → Deployment reports 0 ready | Service routes to nothing
```

***

## Service Name = Application Contract

```
application.properties defines: memcached.host = vprochace01
  ↓
Service name MUST be: vprochace01
  ↓
K8s DNS creates: vprochace01 → ClusterIP
  ↓
App connects to: vprochace01:11211 → works

Change Service name without changing app config → app can't find cache → failure
```

***

## Named Port Linking

```
Deployment:
  containerPort: 11211
  name: vpromc-port         ← defines a named port

Service:
  targetPort: vpromc-port   ← references by NAME, not number

Benefit: If port number changes, update only Deployment
  Service still references by name → auto-resolves
```

***

## Common Mistakes

```
├── Forgot to change label from copied template (left "db" values)
├── Edited wrong file (dbservice instead of mcservice)
├── selector.matchLabels ≠ template.labels (Deployment broken)
├── Service name ≠ what app expects (DNS resolution fails)
└── targetPort name doesn't match Deployment port name
```

***

## Operational Flow

```
── CREATE DEPLOYMENT ──
Copy DB deployment YAML → mcdeployment.yaml
Change: name=vpromc, labels=vpromc, image=memcached, port=11211
Verify: matchLabels == template labels

── CREATE SERVICE ──  
Copy DB service YAML → mcservice.yaml
Open application.properties → find cache hostname (vprochace01)
Change: name=vprochace01, selector=vpromc, port=11211, targetPort=vpromc-port

── VERIFY ──
Cross-check against kube-app branch in source code repo
Ensure no leftover DB values from copy-paste

── NEXT: Same pattern for RabbitMQ (Deployment + Service)
```

***

## Reusable Engineering Patterns

| Pattern                         | Manifestation                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| **Template replication**        | Copy working YAML → modify values → new service (structure identical, values differ) |
| **Label-based binding**         | Deployment→Pod and Service→Pod connections via label matching                        |
| **DNS-based service discovery** | Service name = DNS hostname; app connects by name, not IP                            |
| **Named port indirection**      | targetPort references port name, not number → decoupled from port changes            |
| **Config-driven naming**        | Service names derived from application.properties, not invented                      |
| **Proportional complexity**     | Simple service (Memcached) = simple setup (image + port, no volumes/secrets)         |

***

## Core Mental Model

```
Every Kubernetes backend service follows the same pattern:

  [Deployment]                    [Service]
  ├── name: <service-id>         ├── name: <from-app-config>
  ├── labels: app=<service-id>   ├── selector: app=<service-id>
  ├── image: <docker-image>      ├── port: <service-port>
  └── containerPort: <port>      └── targetPort: <named-port>

Labels connect Deployment to Pods.
Selector connects Service to Pods.
Service name connects Application to Service (via DNS).

Know ONE service setup → replicate for ALL services.
Only identity, image, and port change.
```

***

This material captures every concept, naming convention, label matching rule, copy-paste workflow, and service discovery relationship from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
