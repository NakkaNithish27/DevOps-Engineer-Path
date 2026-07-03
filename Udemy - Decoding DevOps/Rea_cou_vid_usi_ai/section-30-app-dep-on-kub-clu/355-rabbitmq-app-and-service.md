# Kubernetes RabbitMQ Deployment and Service — Writing Definition Files for Message Queuing

**Source:** Video caption file — *"RabbitMQ App and Service"* (from a Kubernetes / DevOps course) [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What We Are Defining and Where It Fits

This lecture creates two Kubernetes definition files for the **RabbitMQ** component of the vProfile application stack: a **Deployment** (to run the RabbitMQ pod) and a **Service** (to expose it internally within the cluster). RabbitMQ is a message broker — it handles asynchronous message queuing between application components. In the vProfile architecture, it's a backend service alongside MySQL (database) and Memcached (cache), all of which the application server connects to. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

The video follows a pattern established in earlier lectures: the MySQL deployment and Memcached deployment/service files were already written, and this lecture creates the RabbitMQ equivalents. The approach is not to write from scratch but to **copy from an existing definition file** (the database deployment file `dbdeploy.yaml`) and modify it. This reflects a real engineering practice — similar resources share structural patterns, and copying-then-modifying is faster and less error-prone than writing from zero. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## 1.2 — The Deployment File: What Makes RabbitMQ Different from the Database

The RabbitMQ deployment is structurally similar to the database deployment, but with key differences that reveal the architectural characteristics of each service: [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**No volumes needed.** The database deployment required persistent volumes to store MySQL data — if the database pod restarts, the data must survive. RabbitMQ in this project does **not** need persistent storage. Messages in a development/learning setup are transient. The video explicitly removes the volume-related sections: "We don't need any initContainers and volumes" and "We don't need to mount the volume anywhere." This is a conscious design decision — RabbitMQ *can* use persistent storage in production, but for this project it's not required. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Secrets are still needed.** The RabbitMQ password is stored in a Kubernetes Secret (the same Secret resource used by other services). The password is not hardcoded in the deployment file — it's referenced via `valueFrom: secretKeyRef`, pointing to the key `rmq-pass` in the Secret. This follows the same credential management pattern used for the database. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Two environment variables are required.** The official RabbitMQ Docker image expects two environment variables for initialization:

* `RABBITMQ_DEFAULT_PASS` — the password for the default user. This comes **from the Secret** via `secretKeyRef`.
* `RABBITMQ_DEFAULT_USER` — the username for the default user. This is set **directly as a value** (`guest`) in the deployment file. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

The video references the Docker Compose file from earlier in the course to identify these variables: "If you remember the Docker Compose file, just open the Docker Compose file. For RabbitMQ, we need to set this — default user and default pass." This demonstrates the pattern of using Docker Compose files as a **reference specification** when translating to Kubernetes definitions — the same services, same environment variables, same configuration, different orchestration format. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**The image is the official RabbitMQ image.** Simply named `rabbitmq` — no custom image is needed. The official image with the right environment variables handles all RabbitMQ setup internally. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**The container port is 5672** — RabbitMQ's standard AMQP protocol port. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## 1.3 — The Service File: Name Matching Is Critical

The Service file for RabbitMQ follows the same pattern as the Memcached service (the video copies from `mcservice.yaml` and modifies). The Service is of type **ClusterIP** — internal-only communication. RabbitMQ doesn't need to be accessible from outside the cluster; only the application pods inside the cluster need to reach it. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

The most important concept in this lecture is the **naming and port matching contract** between three sources: [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

### 1. The `application.properties` File (Application Configuration)

The vProfile application's `application.properties` file contains the address and port for every backend service. For RabbitMQ, it specifies the hostname as `vpromq01` and port as `5672`. The application uses this hostname to connect to RabbitMQ. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

### 2. The Service Definition (Kubernetes Service)

The Kubernetes Service **name** must exactly match the hostname in `application.properties`. If `application.properties` says `vpromq01`, the Service must be named `vpromq01`. Kubernetes internal DNS resolves Service names to their ClusterIP addresses — when the application pod tries to connect to `vpromq01`, Kubernetes DNS resolves it to the RabbitMQ Service's ClusterIP, which routes traffic to the RabbitMQ pod. If the name doesn't match, DNS resolution fails and the application can't find RabbitMQ. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

### 3. The Deployment/Pod Definition

The pod's name and deployment name do **not** need to match anything in `application.properties`. The video explicitly clarifies: "This name is not referred anywhere outside except in the service. But application properties file, the name that is given, that is of the service name. So service name really matters." The pod can be named anything — `vprormq`, `rabbitmq-pod`, anything — because the application never addresses the pod directly. It addresses the Service, and the Service routes to the pod via label selectors. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## 1.4 — The Service's Dual-Facing Contract

The video articulates a powerful mental model for how a Kubernetes Service connects front-end consumers to back-end pods. A Service has two "faces": [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Front-end face (toward the application):**

* **Service name** → must match `application.properties` hostname.
* **Front-end port** → must match `application.properties` port number (5672). [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Back-end face (toward the pod):**

* **Selector** → must match the pod's label (so the Service knows which pod to route to).
* **Target port** → must match the container port defined in the Deployment (5672 for RabbitMQ). [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

The video states this rule explicitly: "In the service, the service name should match with the configuration file, its front-end port should match with the configuration file. Back-end information should match with the pod information — like the selector, the back-end port number, which will be the container port of the pod." [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

🔍 **Deep Dive:**
This dual-facing contract is the fundamental mechanism by which Kubernetes Services act as a **stable abstraction layer** between consumers and providers. The application doesn't know or care which pod is running RabbitMQ, where it's scheduled, or what its IP is. It only knows the Service name and port. The Service handles all the routing. This decoupling allows pods to be rescheduled, restarted, or scaled without the application needing any configuration changes — as long as the Service name and port remain constant. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## 1.5 — The Secret Reference Pattern: Direct Value vs. SecretKeyRef

The two environment variables in the RabbitMQ deployment demonstrate the two ways to provide values in Kubernetes: [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Direct value (`value:`)** — Used for `RABBITMQ_DEFAULT_USER`. The username `guest` is not sensitive, so it's written directly in the YAML. Simple, readable, no external dependency. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Secret reference (`valueFrom: secretKeyRef:`)** — Used for `RABBITMQ_DEFAULT_PASS`. The password is sensitive, so it's stored in a Kubernetes Secret and referenced by key name (`rmq-pass`). The actual password value never appears in the deployment file. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

This pattern — direct values for non-sensitive data, Secret references for sensitive data — is the standard Kubernetes credential management approach. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## 1.6 — Validation Discipline

The video closes with explicit validation instructions: check naming conventions, port numbers, and ensure no accidental edits were made to other files. "Make sure you did not make any change in the memcache service file or any other file. If I made such changes then revert it back." This reflects a real operational discipline — when copying between files and making edits, it's easy to accidentally modify the source file. Always verify that only the intended files were changed. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

The video also instructs comparing against the reference code in the `kube-app` branch of the source repository — "match it with the code in the kube-app branch, make sure it's same." This is a **reference-driven validation** pattern: always compare your work against a known-good reference before proceeding. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing two Kubernetes YAML definition files — `rmqdeploy.yaml` (Deployment for RabbitMQ pod) and `rmqservice.yaml` (ClusterIP Service for internal access) — by copying from existing database/memcached definitions and modifying them. The final outcome: ready-to-apply definition files that will deploy RabbitMQ with correct credentials (from Secret), correct ports (5672), and a Service name matching `application.properties` (`vpromq01`). No `kubectl apply` is executed in this lecture — that happens in a later lecture when all definitions are applied together. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## File 1: `rmqdeploy.yaml` — RabbitMQ Deployment

***

### Step 1: Copy the Base from `dbdeploy.yaml`

**What we are doing:** Using the database deployment as a structural template.

1. Open `rmqdeploy.yaml` for editing.
2. Open `dbdeploy.yaml` and **copy everything**. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)
3. Paste into `rmqdeploy.yaml`.

***

### Step 2: Remove Volume-Related Sections

**What we are doing:** RabbitMQ doesn't need persistent storage in this project.

**Remove the following sections entirely:** [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

* `initContainers` — not needed (no volume initialization).
* `volumes` — no volume definitions.
* `volumeMounts` — no volume mount references inside the container spec.

**Keep:** The `secret` reference section — we still need it for the RabbitMQ password.

***

### Step 3: Rename All Resource References

**What we are doing:** Changing all name references from the database naming to RabbitMQ naming.

Replace all instances of `vprodb` (or similar database names) with `vprormq`: [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

* Deployment `metadata.name` → `vprormq`
* Container `name` → `vprormq`
* Labels → `vprormq`
* All other name references → `vprormq`

**The video removes the `01` suffix** from some names: "I'll remove this 01. It's not really required. VPRORMQ." [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Important clarification:** The pod/deployment name does NOT need to match `application.properties`. Only the Service name matters for application connectivity (covered in the Service file). [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 4: Set the Image

**What we are doing:** Specifying the official RabbitMQ Docker image.

```yaml
image: rabbitmq
```

No custom image — the official `rabbitmq` image from Docker Hub. No tag specified (defaults to `latest`). [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 5: Set the Container Port

```yaml
ports:
- name: vprormq-port
  containerPort: 5672
```

**5672** is the standard AMQP port for RabbitMQ. The port name `vprormq-port` is referenced later by the Service's `targetPort`. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 6: Configure Environment Variables

**What we are doing:** Setting the two environment variables the RabbitMQ image requires.

**Variable 1 — Password (from Secret):**

```yaml
env:
- name: RABBITMQ_DEFAULT_PASS
  valueFrom:
    secretKeyRef:
      name: app-secret
      key: rmq-pass
```

**Breakdown:**

* `name: RABBITMQ_DEFAULT_PASS` — the environment variable name the RabbitMQ image expects.
* `secretKeyRef.name: app-secret` — the name of the Kubernetes Secret resource (same Secret used by other services).
* `secretKeyRef.key: rmq-pass` — the specific key within that Secret that holds the RabbitMQ password value. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Variable 2 — Username (direct value):**

```yaml
- name: RABBITMQ_DEFAULT_USER
  value: "guest"
```

**Breakdown:**

* `name: RABBITMQ_DEFAULT_USER` — the username variable.
* `value: "guest"` — set directly (not sensitive, no Secret needed). [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**How to verify which variables are needed:** Check the Docker Compose file from earlier in the course — it lists the same `RABBITMQ_DEFAULT_USER` and `RABBITMQ_DEFAULT_PASS` variables. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Save the file.** [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## File 2: `rmqservice.yaml` — RabbitMQ Service

***

### Step 7: Copy the Base from `mcservice.yaml`

**What we are doing:** Using the Memcached service as a template.

1. Open `rmqservice.yaml`.
2. Open `mcservice.yaml` (Memcached service), copy everything.
3. Paste into `rmqservice.yaml`. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 8: Set the Target Port

**What we are doing:** Pointing the Service to the correct container port name.

```yaml
targetPort: vprormq-port
```

This must match the `ports.name` defined in `rmqdeploy.yaml` (`vprormq-port`). [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 9: Set the Front-End Port

```yaml
port: 5672
```

This must match the port in `application.properties` (which specifies RabbitMQ on port 5672). [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 10: Set the Service Name (Critical)

**What we are doing:** Setting the Service name to match the hostname in `application.properties`.

```yaml
metadata:
  name: vpromq01
```

**This is the most critical naming decision.** The application connects to RabbitMQ using the hostname `vpromq01`. Kubernetes DNS resolves this Service name to its ClusterIP. If this name doesn't match `application.properties`, the application can't find RabbitMQ. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 11: Set the Selector

**What we are doing:** Linking the Service to the RabbitMQ pod via label matching.

```yaml
selector:
  app: vprormq
```

This must match the label defined on the pod in `rmqdeploy.yaml`. The Service uses this selector to discover which pod(s) to route traffic to. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 12: Set the Service Type

```yaml
type: ClusterIP
```

ClusterIP = internal only. RabbitMQ is accessed only by other pods within the cluster, never from outside. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

### Step 13: Validate and Save

**Validation checklist:** [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

1. **Service name** (`vpromq01`) matches `application.properties` hostname.
2. **Front-end port** (`5672`) matches `application.properties` port.
3. **Target port** (`vprormq-port`) matches the container port name in `rmqdeploy.yaml`.
4. **Selector** (`app: vprormq`) matches the pod label in `rmqdeploy.yaml`.
5. **No accidental edits** to other files (mcservice.yaml, dbdeploy.yaml, etc.).
6. **Compare** against the `kube-app` branch reference code. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

**Save the file.** Files are ready — `kubectl apply` will happen in a later lecture. [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    RabbitMQ Kubernetes Deployment + Service
PURPOSE:  Define message broker for vProfile app on K8s
CONTEXT:  After DB + Memcached definitions; before applying all definitions
METHOD:   Copy from existing definitions → modify (not write from scratch)
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Files Created

```
rmqdeploy.yaml     ← copied from dbdeploy.yaml, removed volumes
rmqservice.yaml    ← copied from mcservice.yaml, changed names/ports
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## RabbitMQ vs Database Deployment Differences

```
FEATURE            DATABASE (dbdeploy)        RABBITMQ (rmqdeploy)
───────            ───────────────            ────────────────────
initContainers     YES (volume init)          NO (removed)
volumes            YES (persistent data)      NO (removed)
volumeMounts       YES                        NO (removed)
Secret reference   YES (db password)          YES (rmq password)
Image              mysql                      rabbitmq
Port               3306                       5672
Env vars           MYSQL_ROOT_PASSWORD        RABBITMQ_DEFAULT_PASS (from Secret)
                                              RABBITMQ_DEFAULT_USER (direct: "guest")
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Service Dual-Facing Contract (Critical Pattern)

```
FRONT-END FACE (toward application):
  ├── Service name: vpromq01          ← MUST match application.properties hostname
  └── Front-end port: 5672           ← MUST match application.properties port

BACK-END FACE (toward pod):
  ├── Selector: app=vprormq          ← MUST match pod label in rmqdeploy.yaml
  └── Target port: vprormq-port      ← MUST match container port name in rmqdeploy.yaml

"Service name should match with the configuration file.
 Back-end information should match with the pod information."
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Name Matching Map

```
application.properties        rmqservice.yaml             rmqdeploy.yaml
──────────────────────        ───────────────             ──────────────
hostname: vpromq01     ←→    metadata.name: vpromq01      (doesn't matter)
port: 5672             ←→    port: 5672
                              targetPort: vprormq-port  ←→  ports.name: vprormq-port
                              selector: app=vprormq     ←→  labels: app=vprormq

POD NAME: "not referred anywhere outside except in the service"
SERVICE NAME: "really matters based on our application properties file"
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Environment Variable Patterns

```
SENSITIVE DATA (password):
  env:
  - name: RABBITMQ_DEFAULT_PASS
    valueFrom:
      secretKeyRef:
        name: app-secret          ← Secret resource name
        key: rmq-pass             ← key within the Secret

NON-SENSITIVE DATA (username):
  env:
  - name: RABBITMQ_DEFAULT_USER
    value: "guest"                ← direct value, no Secret

SOURCE FOR VARIABLE NAMES: Docker Compose file from earlier project
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## RabbitMQ Deployment Structure

```yaml
# rmqdeploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vprormq
spec:
  selector:
    matchLabels:
      app: vprormq
  template:
    metadata:
      labels:
        app: vprormq              ← Service selector matches THIS
    spec:
      containers:
      - name: vprormq
        image: rabbitmq           ← official image, no custom build
        ports:
        - name: vprormq-port      ← Service targetPort matches THIS
          containerPort: 5672
        env:
        - name: RABBITMQ_DEFAULT_PASS
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: rmq-pass
        - name: RABBITMQ_DEFAULT_USER
          value: "guest"
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## RabbitMQ Service Structure

```yaml
# rmqservice.yaml
apiVersion: v1
kind: Service
metadata:
  name: vpromq01                  ← MUST match application.properties
spec:
  type: ClusterIP                 ← internal only
  selector:
    app: vprormq                  ← matches pod label
  ports:
  - port: 5672                    ← front-end port (app connects here)
    targetPort: vprormq-port      ← back-end port (routes to container)
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Application Connection Chain

```
Application Pod
    │ connects to hostname: vpromq01, port: 5672
    ▼
K8s DNS → resolves vpromq01 → ClusterIP of Service
    │
    ▼
Service (vpromq01:5672, type: ClusterIP)
    │ selector: app=vprormq → finds matching pod
    │ targetPort: vprormq-port → routes to container port
    ▼
RabbitMQ Pod (container port 5672)
    │ authenticates with RABBITMQ_DEFAULT_USER/PASS
    ▼
RabbitMQ process running ✅
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Validation Checklist

```
CHECK                                    AGAINST
─────                                    ───────
Service name (vpromq01)                  application.properties hostname
Service port (5672)                      application.properties port
Service targetPort (vprormq-port)        Deployment container port name
Service selector (app=vprormq)           Deployment pod label
Secret key (rmq-pass)                    Secret resource definition
Env var names                            Docker Compose file reference
No accidental edits to other files       mcservice.yaml, dbdeploy.yaml unchanged
Final comparison                         kube-app branch reference code
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Copy-Modify Workflow

```
NEW FILE               COPIED FROM           MODIFICATIONS
────────               ───────────           ─────────────
rmqdeploy.yaml         dbdeploy.yaml         Remove volumes/initContainers/mounts
                                             Change names → vprormq
                                             Change image → rabbitmq
                                             Change port → 5672
                                             Change env vars → RABBITMQ_DEFAULT_*

rmqservice.yaml        mcservice.yaml        Change service name → vpromq01
                                             Change port → 5672
                                             Change targetPort → vprormq-port
                                             Change selector → app=vprormq
```

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## Reusable Engineering Patterns

| Pattern                                            | Manifestation                                                                               |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Copy-Modify from Existing Definitions**          | Don't write from scratch — copy similar resource, modify differences (dbdeploy → rmqdeploy) |
| **Service as Stable Abstraction Layer**            | Service name = DNS-resolvable hostname; pod name is irrelevant to consumers                 |
| **Dual-Facing Contract**                           | Service front-end matches app config; Service back-end matches pod spec                     |
| **Secret for Sensitive, Direct for Non-Sensitive** | `secretKeyRef` for password, `value:` for username — credential management pattern          |
| **Docker Compose as K8s Reference**                | Compose file lists required env vars → translate to K8s env spec                            |
| **Reference-Driven Validation**                    | Compare against kube-app branch code before proceeding                                      |
| **ClusterIP for Internal Services**                | Backend services (RabbitMQ, MySQL, Memcached) = ClusterIP; no external exposure needed      |
| **Accidental Edit Prevention**                     | Explicitly verify no unintended changes to other files after copy-paste operations          |

 [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

## One-Line System Reconstruction

> **RabbitMQ K8s definition files are created by copying from existing definitions (dbdeploy→rmqdeploy removing volumes, mcservice→rmqservice) — the Deployment uses the official `rabbitmq` image on port 5672 with `RABBITMQ_DEFAULT_PASS` from Secret (`secretKeyRef: rmq-pass`) and `RABBITMQ_DEFAULT_USER` as direct value (`guest`) — while the ClusterIP Service's name (`vpromq01`) MUST match `application.properties` hostname and its front-end port (5672) MUST match the config, with the back-end selector/targetPort matching the pod label/container port — because "service name really matters" while "the pod does not matter."** [\[355-rabbit...nd-service \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/355-rabbitmq-app-and-service.txt)

***

This completes the full reconstruction of the RabbitMQ Deployment and Service lecture. It follows the same patterns established in the MySQL and Memcached definition lectures, reinforcing the Service dual-facing contract and the critical distinction between Service names (must match application config) and pod names (can be anything). The next lecture will apply all definition files together to bring the complete vProfile stack up on Kubernetes. Let me know if you'd like any section expanded or adjusted! 🚀
