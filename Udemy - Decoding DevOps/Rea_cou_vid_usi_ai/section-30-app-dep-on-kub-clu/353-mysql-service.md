# ☸️ Kubernetes MySQL Service Definition — Vprofile Project — Deep Learning Material

**Source:** Video caption file — [353-mysql-service.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt?EntityRepresentationId=661dcd48-80f4-4a83-91f8-5752094fc269) [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**Video Context:** The instructor creates the Kubernetes Service definition for the MySQL database pod in the Vprofile project. The lecture explains why pods cannot be connected directly (volatile IPs), how a ClusterIP Service acts as an internal load balancer, the critical relationship between the service name and the application.properties configuration file, label-based selector mechanics connecting the service to the pod, and the named port vs. numeric port pattern. This completes the database layer (Deployment + PVC + Service), with Memcache, RabbitMQ, and Tomcat remaining for subsequent lectures.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why Pods Cannot Be Connected Directly — The Volatility Problem

The instructor opens with a fundamental Kubernetes networking principle: "The deployment definition creates the pod, and that pod needs to be connected by Tomcat service and also Memcache service. So in Kubernetes, we do not connect pods like this directly. We don't give the pod IP because pods are volatile — they get deleted, recreated through deployment — so we cannot rely on the pod IP." [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

This is the core problem. In a traditional server environment, you'd configure one application to connect to another using the target server's IP address. But in Kubernetes, pods are managed by controllers (Deployments, ReplicaSets) that routinely destroy and recreate them — during scaling, updates, node failures, or health check failures. Every time a pod is recreated, it receives a **new IP address**. Any application hardcoded to the old pod IP would immediately break.

The MySQL pod running the Vprofile database will be accessed by the Tomcat pod (the web application) and the Memcache pod (the caching layer). If the MySQL pod crashes and gets recreated with a new IP, Tomcat and Memcache would lose their database connection. Hardcoding pod IPs is fundamentally incompatible with Kubernetes' dynamic pod lifecycle.

***

## 1.2 Kubernetes Service — The Stable Abstraction Layer

The solution is a **Service**. The instructor describes it precisely: "We create a service for them, like a load balancer, internal load balancer." [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

A Kubernetes Service is a stable networking endpoint that sits **in front of** one or more pods. It has a **fixed IP address** (ClusterIP) and a **DNS name** that never changes, regardless of what happens to the pods behind it. When a client (like the Tomcat pod) connects to the Service, the Service routes the traffic to whichever pod(s) are currently alive and matching the selector labels.

The Service acts as an abstraction layer: clients talk to the Service (which is stable), and the Service forwards to pods (which are volatile). Pods can be created, destroyed, moved across nodes, and scaled — the Service absorbs all this churn and presents a single, unchanging endpoint to consumers.

***

## 1.3 ClusterIP — The Internal Load Balancer Type

The instructor specifies the service type: "An internal load balancer in Kubernetes is called a service of type ClusterIP." [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

ClusterIP is the **default** service type. It creates a virtual IP address that is only accessible **within the Kubernetes cluster**. No external traffic can reach a ClusterIP service directly — it's purely for inter-pod communication. This is exactly what's needed for a database: the MySQL service should be reachable by Tomcat and Memcache pods within the cluster, but never exposed to the public internet.

The naming is intentional: "Cluster IP" — an IP that exists only within the cluster's internal network. It's the Kubernetes equivalent of an AWS internal load balancer.

***

## 1.4 Service Name = DNS Name = Application Configuration

This is the most operationally critical concept in the lecture. The instructor names the service `vprodb` and immediately explains why: "This is very important. Reason I'll tell you." [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

He navigates to the Vprofile source code: `source/main/resources/application.properties`. This file configures the Vprofile Java application, and it specifies the database hostname as `vprodb` with port `3306`. The instructor explains: "Our Vprofile application is going to look for a DB that is with this name `vprodb` and port number 3306." [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

When you create a Kubernetes Service named `vprodb`, Kubernetes automatically creates a **DNS entry** for it: `vprodb` resolves to the Service's ClusterIP within the cluster. When the Tomcat pod's application.properties says `db.host=vprodb`, the JVM does a DNS lookup for `vprodb`, gets the Service's ClusterIP, and connects. The Service then routes the connection to the actual MySQL pod.

This means the **service name must exactly match** the hostname expected by the application. If the application.properties says `vprodb`, the service must be named `vprodb`. A mismatch means the DNS lookup fails, and the application cannot find the database.

The instructor explicitly connects this to the broader Vprofile project: "We already discussed that, or we already seen multiple times in this project setup." This naming convention (`vprodb` for DB, and similar names for Memcache and RabbitMQ) is a pattern that runs through the entire multi-service Vprofile deployment — each backend service's Kubernetes Service name must match what the application code expects. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

🔍 **Deep Dive:** Kubernetes DNS resolution works within namespaces. If the Tomcat pod and the MySQL Service are in the same namespace, `vprodb` alone resolves correctly. If they're in different namespaces, the full DNS name would be `vprodb.<namespace>.svc.cluster.local`. The Vprofile project uses the default namespace, so the short name `vprodb` is sufficient.

***

## 1.5 Label-Based Selector — How the Service Finds Its Pod

The Service definition includes a **selector** section with a label: `app: vprodb`. The instructor explains: "Find a pod that has so-and-so label. So our DB pod has this label: `app: vprodb`. That's how we connect the service to the pod." [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

This is the same label-selector mechanism from the ReplicaSet lecture (see lecture 333), applied to Service→Pod routing. The Service doesn't know the pod's IP or name — it knows a **label**. Any pod with the label `app: vprodb` receives traffic from this Service. If the pod is recreated with a new IP but the same label, the Service automatically routes to the new pod.

The label must match exactly between the Service's `selector` and the Pod's `metadata.labels` (defined in the Deployment template). A mismatch means the Service has no endpoints — it exists but routes to nothing, causing connection failures.

***

## 1.6 Port vs. targetPort — Named Ports

The Service definition specifies port configuration, and the instructor introduces an important pattern: **named ports**. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

The Service has two port-related fields:

* **`port`:** The port the Service **listens on** — `3306`. This is the "front end" port that clients connect to.
* **`targetPort`:** The port on the **pod** where traffic is forwarded to. This can be a number (3306) or a **name**.

The instructor uses a named targetPort: `vprodb-port`. He explains: "In the DB deployment definition, if we see containerPort 3306, we have given this name." The Deployment's container spec defines `containerPort: 3306` with `name: vprodb-port`. The Service references this name instead of the number. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

The benefit: "If you wish to change the port number of your service, you don't need to make changes in the service. Here you don't need to make any change. You can keep the name as it is. In the backend, you can keep changing the port number." The name creates a level of **indirection** — the Service says "send traffic to whatever port is named `vprodb-port`" instead of "send traffic to port 3306." If the database port changes from 3306 to 3307, you only update the Deployment (where the containerPort number lives), and the Service automatically follows via the name. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

The instructor also notes you can simply use the number `3306` directly for targetPort: "We can give here the port number 3306." Named ports are a best practice, not a requirement.

⚠️ **Expert Note:** Named ports become especially valuable in environments where port numbers might change between versions, or when multiple containers in a pod expose different ports. The name provides semantic meaning (`vprodb-port` clearly indicates "database port") rather than just a number that requires documentation to understand.

***

## 1.7 What's Complete and What Remains

The instructor closes by taking stock of the database layer's completion: "We have the service, we have the DB deployment manifest, and we have the PVC — so database is all set." [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

The three components form a complete database stack:

* **PVC** — provides persistent storage (EBS volume via StorageClass)
* **Deployment** — runs the MySQL pod with the PVC mounted
* **Service** — exposes the MySQL pod with a stable DNS name (`vprodb`) and ClusterIP

Remaining services for the Vprofile project: **Memcache** (caching layer), **RabbitMQ** (message queue), and **Tomcat** (the web application itself). Each will follow the same pattern: Deployment + Service, with the Service name matching what the application.properties expects.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating the **Kubernetes Service definition** for the MySQL database pod in the Vprofile project. The final outcome: a ClusterIP Service named `vprodb` that provides a stable internal endpoint (DNS name + fixed IP) for the Tomcat and Memcache pods to connect to the MySQL database on port 3306. Combined with the already-created Deployment and PVC, this completes the database layer. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

***

## Step 1: Create the Service Definition File

The instructor generates a ClusterIP Service template (via search/generative text) and pastes it into the definition file, then modifies it. The resulting Service definition: [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vprodb
spec:
  selector:
    app: vprodb
  ports:
    - port: 3306
      targetPort: vprodb-port
  type: ClusterIP
```

### Breakdown of each field:

**`apiVersion: v1`** — Services are core Kubernetes objects, so they use the base `v1` API (not `apps/v1` like Deployments and ReplicaSets). [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**`kind: Service`** — Declares this as a Service object.

**`metadata.name: vprodb`** — The service name. **This is critical** — it must exactly match the hostname in the application.properties file (`db.host=vprodb`). Kubernetes creates a DNS entry `vprodb` that resolves to this Service's ClusterIP. If the Tomcat application looks for `vprodb`, this DNS entry is what it finds. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**`spec.selector.app: vprodb`** — The label selector. The Service routes traffic to any pod that has the label `app: vprodb`. This must match the label defined in the MySQL Deployment's pod template (`metadata.labels.app: vprodb`). [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**`spec.ports.port: 3306`** — The port the Service listens on. Clients connect to `vprodb:3306`. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**`spec.ports.targetPort: vprodb-port`** — The port on the pod to forward traffic to. Instead of the number 3306, a **named port** is used. This name must match the `name` field in the Deployment's `containerPort` definition. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**Alternative — numeric targetPort:**

```yaml
    - port: 3306
      targetPort: 3306
```

This works identically but doesn't benefit from named port indirection.

**`spec.type: ClusterIP`** — Internal-only service. Accessible only from within the cluster. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

***

## Step 2: Verify the Label Connection

Before applying, confirm the selector label matches the Deployment's pod labels.

**In the MySQL Deployment definition file**, check the pod template:

```yaml
spec:
  template:
    metadata:
      labels:
        app: vprodb      # ← must match Service selector
    spec:
      containers:
        - name: vprodb
          image: mysql:8.0
          ports:
            - containerPort: 3306
              name: vprodb-port   # ← must match Service targetPort (if using named port)
```

 [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**Verification checklist:**

* ✅ Service `selector.app` = Deployment `template.metadata.labels.app` = `vprodb`
* ✅ Service `targetPort` name = Deployment `containerPort` name = `vprodb-port`
* ✅ Service `name` = application.properties `db.host` = `vprodb`

**Common mistakes:**

* Mismatched labels: Service selector says `app: vprodb` but pod has `app: mysql` → Service has no endpoints → connection refused
* Wrong service name: Service named `mysql-service` but application.properties expects `vprodb` → DNS lookup fails → application can't find database
* Wrong port number: Service port is 3306 but application connects on 3307 → connection refused

***

## Step 3: Verify the Application Configuration

Open the Vprofile source code: `src/main/resources/application.properties`. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

Confirm the database connection settings reference:

* **Hostname:** `vprodb` (matches Service name)
* **Port:** `3306` (matches Service port)

The Tomcat image used for the Vprofile Deployment contains this same application.properties baked in. When the Tomcat container starts, it reads this config, does a DNS lookup for `vprodb`, gets the Service ClusterIP, and connects on port 3306. The Service forwards to the MySQL pod. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

***

## Step 4: Save and Note the Completed Database Layer

Save the Service definition file. [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

**Database layer status — COMPLETE:**

* ✅ **PVC** — persistent storage request (StorageClass → EBS volume)
* ✅ **Deployment** — MySQL 8.0 pod with PVC mounted at `/var/lib/mysql`
* ✅ **Service** — ClusterIP `vprodb:3306` routing to MySQL pod

**Remaining services (next lectures):**

* Memcache — Deployment + Service
* RabbitMQ — Deployment + Service
* Tomcat — Deployment + Service (+ possibly Ingress for external access) [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)

Each follows the same pattern: the Service name must match what the application.properties expects for that backend service.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ The Core Problem → Solution

```
PROBLEM:
  Tomcat pod needs to connect to MySQL pod
  Pod IPs are VOLATILE (change on recreate)
  → Cannot hardcode pod IP in application config

SOLUTION:
  Service = STABLE abstraction (fixed ClusterIP + DNS name)
  Tomcat connects to Service name "vprodb"
  Service routes to whatever MySQL pod currently exists

  Pod IP changes → Service absorbs the change → clients unaffected
```

***

## ⚡ Service Definition — Structure Map

```yaml
apiVersion: v1                    # core object (not apps/v1)
kind: Service
metadata:
  name: vprodb                    # ← DNS name (MUST match app config)
spec:
  selector:
    app: vprodb                   # ← MUST match pod label
  ports:
    - port: 3306                  # ← Service listens on (front-end)
      targetPort: vprodb-port     # ← Pod port (by name or number)
  type: ClusterIP                 # ← internal only
```

***

## 🔗 The Three-Way Name Contract

```
APPLICATION.PROPERTIES:
  db.host = vprodb          ← app expects this hostname
       ↕ MUST MATCH
SERVICE DEFINITION:
  metadata.name: vprodb     ← creates DNS entry "vprodb"
       ↕ MUST MATCH (via selector)
POD LABELS:
  app: vprodb               ← Service routes to pods with this label

BREAK ANY LINK → connection fails:
  Wrong service name → DNS lookup fails
  Wrong selector     → Service has no endpoints
  Wrong pod label    → Service can't find pod
```

***

## 📦 Port Mapping — Two Approaches

```
NUMERIC (simple):
  port: 3306           ← Service listens on 3306
  targetPort: 3306     ← forwards to pod port 3306

NAMED (recommended):
  port: 3306           ← Service listens on 3306
  targetPort: vprodb-port  ← forwards to pod port NAMED "vprodb-port"

  In Deployment:
    containerPort: 3306
    name: vprodb-port   ← name defined here

BENEFIT OF NAMED:
  Change pod port number → only edit Deployment
  Service stays unchanged (references name, not number)
  Indirection = fewer files to edit on port change
```

***

## 🔄 Service Types — Quick Recall

```
ClusterIP (this lecture):
  ├── Internal only (within cluster)
  ├── Fixed virtual IP + DNS name
  ├── Default type
  └── Use for: inter-pod communication (DB, cache, queue)

LoadBalancer:
  ├── External (creates cloud LB)
  └── Use for: exposing to internet (or use Ingress instead)

NodePort:
  ├── Exposes on each node's IP at a static port
  └── Use for: development/testing
```

***

## 🏗️ Database Layer — Complete Stack

```
PVC (mysql-pvc)
  └── StorageClass "default" → AWS EBS volume
      └── Mounted at /var/lib/mysql in pod

DEPLOYMENT (mysql)
  └── Pod: mysql:8.0
      ├── env: credentials from Secret
      ├── volumeMount: PVC → /var/lib/mysql
      ├── containerPort: 3306 (name: vprodb-port)
      └── label: app=vprodb

SERVICE (vprodb)
  └── ClusterIP, port 3306
      ├── selector: app=vprodb → routes to MySQL pod
      ├── DNS: "vprodb" resolves to ClusterIP
      └── targetPort: vprodb-port (named)

CLIENT (Tomcat pod):
  application.properties → db.host=vprodb:3306
  → DNS lookup "vprodb" → ClusterIP → MySQL pod
```

***

## 🔄 Traffic Flow — End to End

```
Tomcat container
  │ reads application.properties: db.host=vprodb, port=3306
  │ DNS lookup: "vprodb"
  ▼
Kubernetes DNS
  │ resolves: vprodb → 10.x.x.x (Service ClusterIP)
  ▼
Service "vprodb" (ClusterIP: 10.x.x.x, port: 3306)
  │ selector: app=vprodb → finds matching pod(s)
  │ forwards to targetPort: vprodb-port (=3306)
  ▼
MySQL Pod (label: app=vprodb, containerPort: 3306)
  │ processes SQL query
  ▼
Response flows back through the same chain
```

***

## 📋 Vprofile Service Naming Pattern (Across All Services)

```
SERVICE          K8S SERVICE NAME    PORT    APP CONFIG REFERENCE
MySQL DB         vprodb              3306    db.host=vprodb
Memcache         (next lecture)      11211   mc.host=<name>
RabbitMQ         (next lecture)      5672    rmq.host=<name>
Tomcat           (next lecture)      8080    (exposed via Ingress)

PATTERN: Service name = what application.properties expects
         EVERY backend service follows this rule
```

***

## ⚠️ Common Failure Modes

```
SYMPTOM: Application says "connection refused" or "host not found"
CHECK 1: Service name matches app config? (vprodb = vprodb?)
CHECK 2: Service selector matches pod label? (app:vprodb = app:vprodb?)
CHECK 3: Pod is running? (kubectl get pod)
CHECK 4: Service has endpoints? (kubectl get endpoints vprodb)
         → empty endpoints = selector mismatch or no matching pod

SYMPTOM: Service exists but no endpoints
CAUSE:   Label mismatch between selector and pod
FIX:     Align labels exactly

SYMPTOM: DNS lookup fails inside pod
CAUSE:   Service name typo or wrong namespace
FIX:     Verify service name (kubectl get svc)
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Stable Abstraction Over Volatile Resources**
Pods are ephemeral — they come and go. Services provide a **stable identity** (fixed IP + DNS name) that absorbs the volatility of the underlying pods. Clients never talk to pods directly; they talk to the abstraction. This is the same pattern as: AWS ELB in front of auto-scaled instances, DNS names over changing IPs, database connection pools over individual connections, and any proxy/gateway pattern. The principle: **never depend on something volatile; always interpose a stable layer**.

**Pattern 2: Name-as-Contract**
The service name (`vprodb`) isn't just a label — it's a **contract** between the infrastructure (Kubernetes Service) and the application (application.properties). Breaking this contract (renaming the service, changing the expected hostname) breaks the application. In multi-service architectures, these name contracts are the glue that holds services together. They must be documented, versioned, and protected from accidental changes.

**Pattern 3: Named Indirection for Decoupling**
Named ports (`vprodb-port` instead of `3306`) add a level of indirection that decouples the Service from the pod's port number. Changes to port numbers propagate through the name without touching the Service definition. This same principle — using names/labels/references instead of hardcoded values — appears throughout Kubernetes (label selectors, ConfigMap references, Secret references) and software engineering broadly (dependency injection, interface programming, environment variables).

***

## 🎯 One-Line System Summary

> **A Kubernetes ClusterIP Service named `vprodb` provides a stable internal DNS endpoint for the volatile MySQL pod, with the service name contractually matching the application.properties hostname, the label selector (`app: vprodb`) connecting the service to the correct pod, and named targetPorts (`vprodb-port`) decoupling port numbers from service configuration — completing the database layer (PVC + Deployment + Service) with Memcache, RabbitMQ, and Tomcat remaining.** [\[353-mysql-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/353-mysql-service.txt)
