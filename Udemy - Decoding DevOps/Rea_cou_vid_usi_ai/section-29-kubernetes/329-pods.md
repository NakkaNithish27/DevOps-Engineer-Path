# 🎓 Deep Learning Material: Kubernetes Pods — The Smallest Deployable Unit

**Source:** [329-pods.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt?EntityRepresentationId=85876059-982f-4a32-ad01-cea53a0d4557) — Video lecture covering what a Kubernetes Pod is, the relationship between pods and containers, single-container vs multi-container pods (sidecar/init patterns), pod definition files (YAML structure with apiVersion/kind/metadata/spec), creating/describing/editing/deleting pods with `kubectl`, the scheduling flow (scheduler → kubelet → pull → start), and the distinction between container port exposure and port mapping (handled by Services). [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What a Pod Is — The Wrapper Abstraction

A Pod is the **most basic and smallest unit** in Kubernetes. It is not a container — it is a **wrapper** around one or more containers. When you want to run something in Kubernetes, you don't create a container directly — you create a Pod, and the container runs inside it. A Pod represents **a single process** running in your cluster. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

This is a fundamental architectural decision: **Kubernetes manages Pods, not containers directly**. All commands, scaling operations, scheduling decisions, and lifecycle management happen at the Pod level. The container is inside the Pod, but you interact with the Pod. This abstraction layer is what separates Kubernetes from plain Docker — with Docker you manage containers directly (`docker run`, `docker stop`); with Kubernetes you manage Pods (`kubectl create`, `kubectl delete`), and the containers inside them are handled automatically. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## 1.2 Single-Container vs Multi-Container Pods

The **most common use case** is running **one container per Pod**. One Tomcat Pod, one MySQL Pod, one RabbitMQ Pod, one Nginx Pod — each running a single container. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

If you need **multi-container Pods**, the additional containers must be **helper containers** — not independent application components. These helper containers are called **sidecar containers** or **init containers** (or both). The key rule: containers within the same Pod are **tightly coupled**. They share the same network namespace (same IP address, same localhost), same storage volumes, and the same lifecycle. One main container runs the application; the helper containers provide supporting functionality (logging, monitoring, configuration loading, etc.). [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

A critical misconception: **scaling does NOT mean adding more containers to a Pod**. If you need high availability for Tomcat, you create **multiple Tomcat Pods** — horizontally scaled. You do not put multiple Tomcat containers inside one Pod. The instructor emphasizes this: "if you want high availability, you need to have multiple pods horizontally scaled, not multiple container in a pod, but multiple pods." [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## 1.3 The Pod Definition File — YAML Structure

Just as Docker Compose uses a YAML file to define containers declaratively, Kubernetes uses **definition files** (also called manifests) to define Pods and other objects declaratively. The instructor draws the same progression seen throughout the course: imperative commands (`docker run` / direct `kubectl` commands) → declarative files (Docker Compose / Kubernetes definition files). Definition files are preferred because they provide **infrastructure as code** — version controlled, reproducible, no long shell commands. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

Every Kubernetes definition file has **four top-level entries**: [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

### `apiVersion`

Specifies the **API version** for the Kubernetes object. For Pods, it is `v1` — the stable version. Different object types use different API versions: Services use `v1`, Deployments use `apps/v1`. New objects may start with beta versions and eventually reach `v1` stable releases. You check the documentation for the correct version of each object type. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

### `kind`

Specifies the **type of object** being created. For a Pod, it is `Pod` (capital P). Other kinds include `Service`, `Deployment`, `Ingress`, etc. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

### `metadata`

Contains **data about the object** — information that identifies it. Its value is a dictionary containing:

* **`name`** — the name of the Pod. This is how you reference it in `kubectl` commands.
* **`labels`** — key-value pairs, similar to AWS tags. Labels are used for grouping, selecting, and organizing objects. They become critically important when Services need to find Pods (covered in the next lecture). [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

### `spec`

Contains the **technical specification** — what actually runs inside the Pod. For a Pod definition file, `spec` contains:

* **`containers`** — a **list** (because you can have multiple containers in a Pod). Each container entry is a dictionary with:
  * `name` — the name of the container.
  * `image` — the Docker image to run (e.g., `imranvisualpath/freshtomapp:V7`). You specify your own image that you built during containerization.
  * `ports` — a list of ports the container exposes. Each port entry has `name` (a label for the port) and `containerPort` (the port number — capital P). [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

🔍 **Deep Dive**
The YAML structure maps directly to Python/Ansible data types that were covered in earlier lectures. `apiVersion` and `kind` are strings. `metadata` is a dictionary (key-value pairs). `spec.containers` is a list (indicated by the `-` prefix). Within each list item, the values are again dictionaries. The instructor explicitly connects this: "String dictionaries. So apiVersion value is a string, v1. Metadata value is a dictionary." Understanding the YAML data types prevents indentation and formatting errors, which are the most common cause of definition file failures. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## 1.4 Container Port vs Port Mapping — A Critical Distinction

The `containerPort` in the Pod definition file is **not port mapping**. It specifies which port the container **exposes** — the same port that would be in the `EXPOSE` directive of a Dockerfile. It tells Kubernetes what port the application inside the container listens on. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

**Port mapping** — making the container accessible from outside the cluster (equivalent to `docker run -p 8080:8080`) — is done through a completely different Kubernetes object: the **Service**. The instructor explicitly states: "This is not port mapping, this is the port number of the container that is exposed. Port mapping is done very different. It's done through service." Services, load balancers, and external access are covered in the next lecture. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## 1.5 The Pod Scheduling Flow

When you create a Pod, Kubernetes orchestrates a sequence of internal actions visible in the `describe` output's Events section:

1. **`default-scheduler`** assigns the Pod to a specific worker node. The scheduler evaluates which node has available resources and is the best fit. The output shows exactly which node the Pod is assigned to.
2. **`kubelet`** on the assigned worker node takes over. It pulls the container image from the registry (Docker Hub in this case).
3. **`kubelet`** starts the container once the image is pulled.

This flow — scheduler → kubelet → pull → start — is the standard Pod creation lifecycle. The Events section at the bottom of `kubectl describe` output shows each step with timestamps, making it the primary tool for **troubleshooting**. If something goes wrong (image not found, node out of resources, crash loop), the Events section shows exactly where the process failed. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## 1.6 The `1/1` Ready Status

When you run `kubectl get pod`, the READY column shows a fraction like `1/1`. The numerator is the number of containers **currently running**. The denominator is the number of containers **specified** in the Pod definition. `1/1` means one container was specified and one is running — the Pod is fully healthy. If you had a multi-container Pod with 2 containers and one failed, you would see `1/2`. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a Kubernetes Pod running the vProfile application (Tomcat container) from a custom Docker Hub image, using a YAML definition file. The final outcome: a running Pod in the cluster that we can inspect, describe, and manage with `kubectl` commands. This Pod is not yet accessible from outside — port mapping via Services comes in the next lecture. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## Step 1: Create a Working Directory

```bash
mkdir definitions
cd definitions
```

This directory will hold all Kubernetes definition files. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## Step 2: Write the Pod Definition File

```bash
vim vproapppod.yaml
```

Content:

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: vproapp
  labels:
    app: vproapp
spec:
  containers:
    - name: appcontainer
      image: imranvisualpath/freshtomapp:V7
      ports:
        - name: vproapp-port
          containerPort: 8080
```

 [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

**Line-by-line breakdown:**

| Line                                    | Meaning                                              |
| --------------------------------------- | ---------------------------------------------------- |
| `---`                                   | YAML document start marker                           |
| `apiVersion: v1`                        | Pod API version (stable)                             |
| `kind: Pod`                             | Object type — Pod (capital P)                        |
| `metadata:`                             | Object identification section                        |
| `name: vproapp`                         | Pod name — used in all `kubectl` commands            |
| `labels:`                               | Key-value tags for selection/organization            |
| `app: vproapp`                          | Label `app=vproapp` — will be used by Services later |
| `spec:`                                 | Technical specification                              |
| `containers:`                           | List of containers in this Pod                       |
| `- name: appcontainer`                  | Container name (the `-` makes it a list item)        |
| `image: imranvisualpath/freshtomapp:V7` | Docker Hub image (account/image:tag)                 |
| `ports:`                                | List of exposed ports                                |
| `- name: vproapp-port`                  | Port label                                           |
| `containerPort: 8080`                   | The port Tomcat listens on (NOT port mapping)        |

**Use your own image:** Replace `imranvisualpath/freshtomapp:V7` with the image you built and pushed to Docker Hub during the containerization lectures. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

⚠️ **Indentation is critical.** The instructor warns: "The only thing you need to worry about here is the indentation." Misaligned YAML causes parse errors. `metadata` and `spec` are at the same level. `containers` is indented under `spec`. Each container's properties are indented under the list item marker `-`.

Save and quit (`:wq`). [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## Step 3: Create the Pod

```bash
kubectl create -f vproapppod.yaml
```

 [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

| Part              | Meaning                      |
| ----------------- | ---------------------------- |
| `kubectl`         | Kubernetes command-line tool |
| `create`          | Create a new object          |
| `-f`              | From a file                  |
| `vproapppod.yaml` | The definition file          |

**Expected output:** `pod/vproapp created`

***

## Step 4: Check Pod Status

```bash
kubectl get pod
```

 [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

**Expected output progression:**

| NAME    | READY | STATUS            | First run          |
| ------- | ----- | ----------------- | ------------------ |
| vproapp | 0/1   | ContainerCreating | Image being pulled |

After a few seconds, run again:

| NAME    | READY | STATUS  | After image pull  |
| ------- | ----- | ------- | ----------------- |
| vproapp | 1/1   | Running | Container started |

`1/1` confirms: 1 container specified, 1 running. `ContainerCreating` → `Running` is the normal transition. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## Step 5: Describe the Pod (Detailed Inspection)

```bash
kubectl describe pod vproapp
```

 [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

| Part       | Meaning                                           |
| ---------- | ------------------------------------------------- |
| `describe` | Show detailed information (like `docker inspect`) |
| `pod`      | Object type                                       |
| `vproapp`  | Pod name                                          |

**Key information in the output:**

| Section          | What to Look For                        |
| ---------------- | --------------------------------------- |
| **IP**           | The Pod's internal IP address           |
| **Container ID** | The container running inside the Pod    |
| **Port**         | The container port (8080)               |
| **Node**         | Which worker node the Pod is running on |
| **Events**       | The scheduling/startup sequence         |

**Events section (bottom) — the troubleshooting goldmine:**

```
Type     Reason     Message
Normal   Scheduled  Successfully assigned to <node-name>
Normal   Pulling    Pulling image "imranvisualpath/freshtomapp:V7"
Normal   Pulled     Successfully pulled image
Normal   Created    Created container appcontainer
Normal   Started    Started container appcontainer
```

 [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

The Events section shows the exact sequence: **scheduler** assigns the Pod to a node → **kubelet** on that node pulls the image → creates the container → starts it. If anything fails, the error appears here with the exact reason. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## Step 6: Get Pod Output in YAML Format

```bash
kubectl get pod vproapp -o yaml
```

 [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

| Part      | Meaning               |
| --------- | --------------------- |
| `-o yaml` | Output in YAML format |

Returns the **full Pod specification** as Kubernetes sees it — including all default values, status information, and system-generated fields that you didn't specify in your definition file. This is much more detailed than your original YAML. You can redirect this to a file:

```bash
kubectl get pod vproapp -o yaml > pod-full.yaml
```

***

## Step 7: Edit a Pod (Limited)

```bash
kubectl edit pod vproapp
```

Opens the Pod specification in your default editor. **Most fields are NOT editable** on a running Pod. You can change a few things (like labels), but core settings (image, ports, resource limits) cannot be changed. For those changes, you use a **Deployment** object (covered in later lectures) which manages Pod recreation. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

## Step 8: Delete the Pod

```bash
kubectl delete pod vproapp
```

 [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

| Part      | Meaning           |
| --------- | ----------------- |
| `delete`  | Remove the object |
| `pod`     | Object type       |
| `vproapp` | Pod name          |

The Pod and its container are destroyed. Unlike Docker Compose's `down`, there is no "stop" concept for Pods — you delete them, and if managed by a Deployment, a new one is automatically created.

**Connection to larger flow:** The Pod is now running but not accessible from outside the cluster. The next lecture introduces **Services** — the Kubernetes object that handles port mapping, load balancing, and external access. [\[329-pods \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/329-pods.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Pod = Wrapper Around Containers

```
Kubernetes manages: PODS (not containers)
Pod manages:        CONTAINERS (one or more)

Docker:       docker run → container
Kubernetes:   kubectl create → pod → container(s) inside

Pod is to Kubernetes what Container is to Docker
```

***

## Single vs Multi-Container Pod

```
COMMON (99%):  1 Pod = 1 container (one app per pod)
MULTI:         1 Pod = 1 main + helper containers (sidecar/init)
               Tightly coupled, shared network + storage

SCALING:       ✓ Multiple PODS (horizontal scaling)
               ✗ Multiple containers in one pod (WRONG)

Tomcat × 3 = 3 Pods, each with 1 Tomcat container
             NOT 1 Pod with 3 Tomcat containers
```

***

## Pod Definition File Structure

```yaml
apiVersion: v1           # ← API version (string)
kind: Pod                # ← object type (string, capital P)
metadata:                # ← identification (dictionary)
  name: vproapp          #    pod name
  labels:                #    key-value tags (like AWS tags)
    app: vproapp
spec:                    # ← technical details (dictionary)
  containers:            #    LIST of containers
    - name: appcontainer #    container name
      image: account/img:tag  # Docker image
      ports:             #    LIST of ports
        - name: port-name
          containerPort: 8080  # exposed port (NOT mapping!)
```

***

## Four Top-Level Keys (All Definition Files)

```
apiVersion  → which API version (v1, apps/v1, etc.)
kind        → what object (Pod, Service, Deployment, Ingress)
metadata    → identity (name, labels)
spec        → technical specification (containers, ports, volumes)

API versions by kind:
  Pod:        v1
  Service:    v1
  Deployment: apps/v1
  New objects: beta → v1 (stable)
```

***

## containerPort vs Port Mapping

```
containerPort: 8080     ← which port the container LISTENS on
                           (equivalent to EXPOSE in Dockerfile)
                           NOT accessible from outside cluster

Port Mapping            ← done through SERVICE object (next lecture)
                           (equivalent to docker run -p)
```

***

## `kubectl` Command Reference

```bash
kubectl create -f file.yaml     # create from definition file
kubectl get pod                  # list pods (NAME, READY, STATUS)
kubectl describe pod <name>      # detailed info + events (troubleshooting)
kubectl get pod <name> -o yaml   # full YAML output
kubectl edit pod <name>          # edit (limited fields only)
kubectl delete pod <name>        # destroy the pod
```

***

## Pod Creation Flow (Internal)

```
kubectl create -f pod.yaml
  │
  ▼
API Server receives request
  │
  ▼
default-scheduler assigns Pod to a Node
  │  (Events: "Successfully assigned to <node>")
  ▼
kubelet on that Node:
  1. Pulls image from registry
     (Events: "Pulling image...")
  2. Creates container
     (Events: "Created container")
  3. Starts container
     (Events: "Started container")
  │
  ▼
Pod status: ContainerCreating → Running
READY: 0/1 → 1/1
```

***

## Pod Status Progression

```
ContainerCreating → Running      (normal)
ImagePullBackOff  → Error        (image not found / auth issue)
CrashLoopBackOff  → Error        (container starts then crashes)
Pending           → (waiting)    (no node available / scheduling issue)

Check Events section of describe for exact failure reason
```

***

## READY Column

```
1/1  → 1 container specified, 1 running (healthy)
0/1  → 1 container specified, 0 running (starting or failed)
2/3  → 3 containers specified, 2 running (1 failed)
```

***

## Describe Output Key Sections

```
kubectl describe pod <name>

  IP:            Pod's internal IP
  Node:          which worker node it runs on
  Containers:    container ID, image, port, state
  Events:        chronological scheduling + startup log
                 ← PRIMARY TROUBLESHOOTING TOOL
```

***

## Imperative vs Declarative Progression

```
Docker:       docker run (imperative) → Docker Compose (declarative)
Kubernetes:   kubectl run (imperative) → Definition files (declarative)

Definition files = Infrastructure as Code
  → version controlled
  → reproducible
  → no long shell commands
```

***

## Definition File for This Lecture

```
File: vproapppod.yaml

Pod name:       vproapp
Container name: appcontainer
Image:          imranvisualpath/freshtomapp:V7
                (replace with YOUR Docker Hub image)
Port:           8080 (Tomcat)
Labels:         app=vproapp
```

***

## Key Engineering Patterns

| Pattern                           | Manifestation                                                                           |
| --------------------------------- | --------------------------------------------------------------------------------------- |
| **Abstraction layer**             | Kubernetes manages Pods, not containers — adds scheduling, lifecycle, networking on top |
| **One process per unit**          | One main container per Pod — mirrors microservice architecture                          |
| **Horizontal scaling**            | Scale by adding Pods, not containers within a Pod                                       |
| **Declarative definition**        | YAML file with 4 standard keys → infrastructure as code                                 |
| **Events as audit trail**         | Every scheduling/startup step logged → primary troubleshooting mechanism                |
| **Separation of concerns**        | Pod defines WHAT runs; Service defines HOW it's accessed (next lecture)                 |
| **Container port ≠ port mapping** | Pod exposes port; Service maps it — two different objects, two different concerns       |

***

## Project Continuity

```
BEFORE: Docker Compose (multi-container), containerization of vProfile
THIS:   Kubernetes Pods — definition files, create/describe/delete
NEXT:   Services — port mapping, load balancing, external access
THEN:   Deployments — managed Pod scaling, rolling updates
```

***

This completes the full reconstruction. **Theory** explains Pods as the wrapper abstraction, single vs multi-container patterns, and the YAML structure with its four top-level keys. **Practical** walks through writing the definition file, creating the Pod, and using every `kubectl` command with expected outputs. The **Compression Map** gives you the definition file template, the creation flow, and the status/READY interpretation for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
