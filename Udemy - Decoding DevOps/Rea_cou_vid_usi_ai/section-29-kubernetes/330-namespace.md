# 🎓 Deep Learning Material: Kubernetes Namespaces — Isolating and Grouping Resources Within a Cluster

**Source:** Video lecture on Kubernetes namespaces (from [330-namespace.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt?EntityRepresentationId=bc32be97-1def-4efa-b4fc-500dcd002963) caption file), with command reference from [330.namespaces.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt?EntityRepresentationId=971f6a73-6687-4ab8-8642-9ceeed6f93e3) [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Video Context:** This is a focused lecture on Kubernetes namespaces — the mechanism for logically partitioning a single cluster into isolated groups of resources. The instructor covers what namespaces are, why they exist, default namespaces that come with a cluster, how to create custom namespaces, how to run pods in specific namespaces (both imperatively and via definition files), how to query resources across or within namespaces, and how deleting a namespace removes all its resources. The instructor also reveals that the Kubernetes control plane components (etcd, controller, scheduler, proxy) all run as pods inside the `kube-system` namespace — an important architectural insight. The lecture is short but dense with operational patterns.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Namespaces Are and What Problem They Solve

A Kubernetes cluster can run hundreds or thousands of resources — pods, services, deployments, replica sets. Without organization, all these resources exist in a flat space, making it difficult to manage, secure, and clean up. **Namespaces** provide a mechanism for **logically isolating groups of resources** within a single physical cluster. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

The instructor reads directly from the documentation: *"Namespaces provides a mechanism for isolating groups of resources within a single cluster."* [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

Think of namespaces as **folders in a filesystem**. Just as you organize files into directories, you organize Kubernetes resources into namespaces. Each namespace is its own logical boundary — resources within it are grouped together, and certain rules (like naming uniqueness) apply within that boundary.

***

## 1.2 — Name Uniqueness: Within, Not Across

A critical rule: *"Names of resources needs to be unique within a namespace, but not across namespaces."* [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

This means you can have a pod named `nginx1` in the `default` namespace AND a pod named `nginx1` in a `kubekart` namespace — no conflict. But you **cannot** have two pods named `nginx1` within the same namespace. The instructor demonstrates this: creating `nginx1` in `kubekart` succeeds, but trying to create it again in the same namespace fails with "already exists." Creating it in a different namespace works. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

This property is what enables namespaces to support multiple environments (dev, staging, prod) with identically-named resources — each environment gets its own namespace, and the same resource names can be reused.

***

## 1.3 — Default Namespaces: What Comes with a New Cluster

When you create a Kubernetes cluster, several namespaces are automatically created: [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

* **`default`** — where resources go if you don't specify a namespace. When you run `kubectl get all`, it shows resources in this namespace.
* **`kube-system`** — contains all **control plane components** and cluster-internal services. The instructor shows: *"in kube-system namespace, we have Replica Set, deployment, Daemon Set, service... etcd manager, that is also a pod, controller that is also pod, proxy is also pod, scheduler is also pod."* [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)
* **`kube-public`** — a namespace readable by all users (including unauthenticated ones), typically used for cluster-wide publicly readable resources.
* **`kube-node-lease`** — holds lease objects associated with each node (used for node heartbeats).

***

## 1.4 — Control Plane Components Run as Pods in `kube-system`

This is an important architectural insight the instructor reveals while exploring namespaces. The Kubernetes control plane components — **etcd**, **kube-controller-manager**, **kube-scheduler**, **kube-proxy** — all run as **pods** inside the `kube-system` namespace. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

*"In kube-system namespace you have all your control plane resources and they run as a pod."* [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

This means Kubernetes uses its own pod abstraction to run itself. The control plane is not external to the cluster — it's managed by the same mechanisms it provides. This is a self-hosting pattern: the orchestrator is orchestrated by itself.

***

## 1.5 — When to Use Multiple Namespaces

The instructor provides practical guidance from experience: [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

*"I have seen for small environments people don't even care about namespaces. They create most of the things in default namespace. But when you have many users and you have multiple projects or multiple environments you want to manage, it's better to create namespaces and group your resources."*

**Use cases for custom namespaces:**

* **Environment isolation:** separate namespaces for development, staging, production
* **Project isolation:** different projects within the same cluster get their own namespace
* **Team isolation:** different teams operate in different namespaces
* **Security and quotas:** namespaces are the boundary for resource quotas and RBAC policies [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

## 1.6 — Namespace Deletion: Powerful and Dangerous

The instructor shares a practical insight: *"When you create your own namespace, it's really easy to delete the entire namespace. I mean all the resources, you can just delete the namespace. It removes everything from that namespace just in one command. I know that's dangerous, but it's also usable or useful."* [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

`kubectl delete ns <name>` removes the namespace **and every resource inside it** — all pods, services, deployments, configmaps, everything. This is simultaneously a **powerful cleanup tool** (tear down an entire environment in one command) and a **dangerous operation** (accidentally deleting a production namespace destroys everything in it). [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

***

## 1.7 — Three Ways to Specify a Namespace

The instructor demonstrates three mechanisms for targeting a specific namespace: [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

**1. Command-line flag (`-n`):** Add `-n <namespace>` to any `kubectl` command to target a specific namespace. Without `-n`, commands default to the `default` namespace.

**2. Definition file (`metadata.namespace`):** In a YAML definition file, include `namespace: <name>` under the `metadata` section. When you `kubectl apply` this file, the resource is created in the specified namespace.

**3. kubeconfig context:** You can set a default namespace in the kubeconfig file. Then every `kubectl` command uses that namespace automatically without needing `-n`. The instructor mentions: *"you can specify namespace in kube config file, then every time you use kubectl command it's going to use that namespace if you do not specify."* [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a custom Kubernetes namespace, deploying pods into it both imperatively and declaratively, querying resources across namespaces, and then cleaning up by deleting the namespace. The final outcome: understanding how to organize, target, and clean up resources using namespaces in daily Kubernetes operations.

***

## Step 1: View Existing Namespaces

```bash
kubectl get ns
```

* `get ns` — lists all namespaces (`ns` is shorthand for `namespaces`) [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Expected output:** `default`, `kube-node-lease`, `kube-system`, `kube-public` — the four namespaces that come with a fresh cluster. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

## Step 2: View Resources in Default Namespace

```bash
kubectl get all
```

Shows all resources (pods, services, deployments, etc.) in the **default namespace** only. Without specifying `-n`, kubectl always targets `default`. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Expected output:** Any previously created pods/services in the default namespace (the instructor sees one pod and the default Kubernetes service). [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

## Step 3: View Resources Across ALL Namespaces

```bash
kubectl get all --all-namespaces
```

* `--all-namespaces` — shows resources from every namespace, not just default [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Expected output:** A large list showing resources from `default`, `kube-system`, and other namespaces. The `kube-system` namespace contains many pods — these are the control plane components (etcd, controller-manager, scheduler, proxy, CoreDNS, etc.) all running as pods. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

## Step 4: Query a Specific Namespace

```bash
kubectl get svc -n kube-system
```

* `get svc` — lists services
* `-n kube-system` — targets the `kube-system` namespace specifically [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Expected output:** Internal cluster services like CoreDNS. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

## Step 5: Create a Custom Namespace

```bash
kubectl create ns kubekart
```

* `create ns` — creates a new namespace
* `kubekart` — the name of the new namespace [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

***

## Step 6: Run a Pod in the Custom Namespace (Imperative)

```bash
kubectl run nginx1 --image=nginx -n kubekart
```

* `run nginx1` — creates a pod named `nginx1`
* `--image=nginx` — uses the nginx Docker image
* `-n kubekart` — creates the pod in the `kubekart` namespace, not default [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Demonstrate name uniqueness rule:**

```bash
kubectl run nginx1 --image=nginx -n kubekart
```

Running the same command again → **ERROR: "already exists"** — you can't have two pods with the same name in the same namespace. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

But running it in a **different namespace** would succeed — same name, different namespace, no conflict. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

## Step 7: Create a Pod via Definition File with Namespace

**Create the definition file:**

```bash
vim pod1.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx12
  namespace: kubekart
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```

 [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Key addition:** `namespace: kubekart` under `metadata` — this directs the pod to be created in the `kubekart` namespace regardless of what `-n` flag you use (the file takes precedence).

**Apply the definition:**

```bash
kubectl apply -f pod1.yaml
```

 [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

***

## Step 8: Verify Pods in the Namespace

```bash
kubectl get pod -n kubekart
```

 [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**Expected output:** Two pods running — `nginx1` (created imperatively in Step 6) and `nginx12` (created from the definition file in Step 7). [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

**Common mistake:** Running `kubectl get pod` without `-n kubekart` → shows pods in the `default` namespace → the `kubekart` pods are invisible. Always specify the namespace. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

## Step 9: Delete the Namespace (Cleanup)

```bash
kubectl delete ns kubekart
```

 [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt), [\[330.namespaces \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330.namespaces.txt)

**What happens:** The namespace AND **all resources inside it** (both pods, any services, configmaps, etc.) are deleted in one command. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

**Verify:**

```bash
kubectl get ns
```

`kubekart` is gone. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

> ⚠️ **Expert Note**
>
> This command is irreversible. In production, namespace deletion should be protected by RBAC policies that restrict who can delete namespaces. Never run `kubectl delete ns` on production namespaces without extreme caution and verification. The instructor acknowledges: *"I know that's dangerous, but it's also usable or useful."* [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept (One-Line Reconstruction)

> **Namespaces logically partition a Kubernetes cluster — resources are unique within a namespace, isolated between namespaces, and an entire namespace (with all contents) can be deleted in one command.**

***

## 🔷 Default Namespaces (Come with Every Cluster)

```
NAMESPACE           CONTENTS
──────────          ────────────────────────────────────────
default             User resources (when -n not specified)
kube-system         Control plane pods (etcd, controller, scheduler, proxy, CoreDNS)
kube-public         Publicly readable resources
kube-node-lease     Node heartbeat leases
```

***

## 🔷 Three Ways to Specify Namespace

```
1. COMMAND FLAG:
   kubectl get pod -n kubekart

2. DEFINITION FILE:
   metadata:
     namespace: kubekart

3. KUBECONFIG DEFAULT:
   Set default namespace in kubeconfig context
   → all kubectl commands use it without -n
```

***

## 🔷 Key Commands

```bash
kubectl get ns                         # list all namespaces
kubectl get all                        # resources in default namespace
kubectl get all --all-namespaces       # resources in ALL namespaces
kubectl get svc -n kube-system         # resources in specific namespace
kubectl create ns kubekart             # create namespace
kubectl run nginx1 --image=nginx -n kubekart  # pod in namespace
kubectl apply -f pod1.yaml            # create from file (namespace in metadata)
kubectl get pod -n kubekart            # list pods in namespace
kubectl delete ns kubekart             # DELETE namespace + ALL contents
```

***

## 🔷 Name Uniqueness Rule

```
WITHIN namespace:    names MUST be unique
                     nginx1 + nginx1 in kubekart → ERROR

ACROSS namespaces:   names CAN repeat
                     nginx1 in default + nginx1 in kubekart → OK
```

***

## 🔷 Namespace in YAML Definition

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx12
  namespace: kubekart      ← THIS LINE
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```

***

## 🔷 Control Plane = Pods in kube-system

```
kube-system namespace contains:
  ├── etcd (pod)                    ← cluster state store
  ├── kube-controller-manager (pod) ← reconciliation loops
  ├── kube-scheduler (pod)          ← pod placement decisions
  ├── kube-proxy (pod/daemonset)    ← network rules on each node
  └── CoreDNS (pod/deployment)      ← cluster DNS

"In kube-system namespace you have all your
 control plane resources and they run as a pod."
```

***

## 🔷 When to Use Custom Namespaces

```
SMALL ENV:  default namespace is fine (simple, few resources)

LARGE ENV:  create namespaces for:
  ├── Environments (dev / staging / prod)
  ├── Projects (project-a / project-b)
  ├── Teams (team-frontend / team-backend)
  └── Security boundaries (quotas + RBAC per namespace)
```

***

## 🔷 Namespace Deletion = Nuclear Cleanup

```
kubectl delete ns kubekart

DELETES:
  ├── The namespace itself
  ├── ALL pods in it
  ├── ALL services in it
  ├── ALL deployments in it
  ├── ALL configmaps, secrets, etc.
  └── EVERYTHING in that namespace

ONE COMMAND → ENTIRE ENVIRONMENT GONE

USEFUL: tear down dev/test environments instantly
DANGEROUS: accidentally targeting production
PROTECTION: RBAC policies restricting namespace deletion
```

***

## 🔷 Default Namespace Behavior

```
kubectl get pod                → default namespace
kubectl get pod -n kubekart    → kubekart namespace

WITHOUT -n: always targets "default"
  → resources in other namespaces are INVISIBLE

COMMON MISTAKE:
  "My pod disappeared!" → it's in a different namespace
  FIX: kubectl get pod --all-namespaces | grep <pod-name>
```

***

## 🔷 Reusable Engineering Pattern: Logical Partitioning Within a Shared System

```
PATTERN: Single Physical System → Multiple Logical Boundaries

KUBERNETES:
  1 cluster → N namespaces → isolated resource groups
  Mechanism: namespace
  Scope: name uniqueness, RBAC, quotas, network policies

SAME PATTERN IN:
  Linux:      1 kernel → N users/groups → isolated file permissions
  Databases:  1 server → N schemas/databases → isolated tables
  AWS:        1 account → N VPCs → isolated networks
  Docker:     1 host → N networks → isolated container groups
  Git:        1 repo → N branches → isolated code versions

Core principle:
  Physical sharing + Logical isolation
  = Cost efficiency + Operational separation

Namespaces provide the BOUNDARY without requiring
separate physical infrastructure per environment/project.
```

This is the fundamental value of namespaces: they enable **multi-tenancy within a single cluster** — multiple teams, environments, or projects share the same physical infrastructure while maintaining logical isolation, security boundaries, and independent lifecycle management. [\[330-namespace \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/330-namespace.txt)
