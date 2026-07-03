# 🎓 Kubernetes Extras: Taints & Tolerations, Resource Limits, Jobs, CronJobs, and DaemonSets — Deep Learning Material

**Source:** Video caption file — *Extras (Kubernetes Administration Concepts)* [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Taints and Tolerations: Controlling Where Pods Can Run

Kubernetes schedules pods onto nodes automatically. But what if you want to **restrict which pods can run on a specific node**? This is where **Taints and Tolerations** come in — a two-part mechanism that gives you fine-grained control over pod-to-node placement. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### Taints — "Painting" a Node

A **taint** is applied to a **node**. The instructor's mental model: "Think of it like painting a node with some information." When you taint a node, you're saying: **"This node is special — don't put just any pod here."** A taint consists of three parts: a **key**, a **value**, and an **effect**. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

The most common effect is **`NoSchedule`** — meaning no pod will be scheduled onto this node unless the pod explicitly declares it can tolerate the taint. The taint acts as a **gatekeeper**: it repels pods by default.

```bash
kubectl taint node <node-name> key=value:NoSchedule
```

After this command, the node is "painted" with this key-value pair and the NoSchedule effect. Any new pod that doesn't have a matching toleration will **not** be scheduled onto this node. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### Tolerations — Pods That Can Handle the Paint

A **toleration** is declared in the **pod definition**. It says: "I can tolerate this taint — I'm allowed to run on nodes painted with this information." A toleration matches a taint by specifying the same key, value (or just key existence), and effect. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

In the pod YAML:

```yaml
tolerations:
- key: "key-name"
  operator: "Equal"
  value: "value"
  effect: "NoSchedule"
```

This says: if a node has a taint with this key equal to this value and the effect is NoSchedule, then this pod **can** run on that node. The `operator` can also be `Exists` — meaning "if this key exists on the node, regardless of its value, I can tolerate it." [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### The Master Node Taint — A Built-In Example

The most important real-world example of taints is the **master node**. By default, Kubernetes master nodes are **tainted with `NoSchedule`** — meaning no regular workload pods will be scheduled onto them. Master nodes run control plane components (API server, scheduler, etc.) and should not compete with application workloads for resources. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

If you want a pod to run on the master node (e.g., a monitoring agent that should run on every node including the master), you must add a toleration in the pod definition that matches the master node's taint. The instructor demonstrates this explicitly with the fluentd DaemonSet example: the toleration allows the logging pod to run on the master node. Without that toleration, it would only run on worker nodes. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

> 🔍 **Deep Dive:** The taint-toleration model is a **repulsion-based scheduling system**. Unlike node affinity (which *attracts* pods to nodes), taints *repel* pods from nodes, and tolerations *exempt* specific pods from that repulsion. Both can coexist — you might taint a GPU node to repel non-GPU workloads, then use tolerations on GPU-hungry pods to allow them through, and additionally use node affinity to actively attract them.

***

## 1.2 — Resource Requests and Limits: Reserving and Restricting

When a pod runs on a node, how much CPU and memory should it get? Without any specification, a pod might consume **unlimited resources**, starving other pods on the same node. Kubernetes provides two controls: **Requests** and **Limits**. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### Requests — Reserving Resources

A **request** tells the Kubernetes scheduler: "This pod needs **at least** this much memory and CPU to run." The scheduler uses this information to decide which node has enough available resources to host the pod. If no node has enough unreserved resources to satisfy the request, the pod stays in **Pending** state — it won't be scheduled anywhere. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
```

### Limits — Restricting Maximum Usage

A **limit** tells the container runtime: "This pod can use **at most** this much memory and CPU." Even if the node has more available resources, the pod is capped at the limit. If the pod tries to exceed its memory limit, it gets **OOMKilled** (Out Of Memory killed). [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

```yaml
resources:
  limits:
    memory: "128Mi"
    cpu: "500m"
```

The instructor summarizes the distinction concisely: **"Request is reserving. Limit is restricting."** [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

If you don't specify limits, the pod may use unlimited resources (or up to whatever limit is set at the namespace level). This is dangerous in production — one misbehaving pod can consume all node resources and crash other pods.

> ⚠️ **Expert Note:** The instructor demonstrates this concept in the context of monitoring/logging DaemonSets: "When you run monitoring logging solution, you don't want it to take up all your resources because other workloads may be critical, more critical than this. So usually it's limited and it will also have requests because it may need some amount of resource to collect your logs or metrics." This is the standard practice — always set both requests and limits for infrastructure pods (logging, monitoring) to prevent them from competing with application workloads. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 1.3 — Jobs: Run-to-Completion Workloads

Not every workload runs continuously. An Nginx web server runs forever — it starts and stays running. But what about a **batch processing task**, a **data migration script**, or a **report generation command**? These need to **run once, complete their work, and exit**. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

A **Job** is a Kubernetes resource with `Kind: Job` that runs a container, waits for it to complete, and records the result. Unlike a regular pod (which Kubernetes tries to keep running indefinitely), a Job's pod is **expected to terminate**. When it completes successfully, the Job is marked as complete. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

```yaml
kind: Job
spec:
  template:
    spec:
      containers:
      - name: worker
        image: busybox
        command: ["echo", "batch processing done"]
```

The instructor's distinction: "This is similar to Pod, except Pod will run continuously and Job will run for a specific period of time." A Pod with `Kind: Pod` is meant to run forever. A `Kind: Job` is meant to finish. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 1.4 — CronJobs: Scheduled Jobs (Kubernetes Cron)

A **CronJob** extends the Job concept by adding **scheduling**. Instead of running once when you apply it, a CronJob runs **at specific intervals or times** — exactly like the Linux `crontab` system. The instructor draws the direct parallel: "This is similar to Cron Job of Linux. Scheduled tasks." [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

```yaml
kind: CronJob
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scheduled-task
            image: busybox
            command: ["echo", "running scheduled task"]
```

The `schedule` field uses **cron format** — the same five-field format from Linux and from the EventBridge lecture:

```
* * * * *
│ │ │ │ │
│ │ │ │ └── Day of week (0-6, Sun-Sat)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

`* * * * *` means **every minute**. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

The instructor's distinction between Job and CronJob: "Job just runs when you run it and just completes, returns the information. CronJob runs at a specific interval, specific time, like an alarm." [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 1.5 — DaemonSets: One Pod Per Node, Automatically

A **DaemonSet** is a controller that ensures **every node (or a subset of nodes) runs exactly one copy of a pod**. If you have 4 worker nodes and create a DaemonSet, you get 4 pods — one on each worker. If you add a 5th worker node to the cluster, the DaemonSet **automatically** creates a 5th pod on that new node. If you remove a node, the DaemonSet's pod on that node is gone. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

The instructor explains: "A DaemonSet ensures that all or some nodes run a copy of a Pod. As nodes are added to the cluster, pods are added to them."

### DaemonSet vs. Deployment

DaemonSet sounds similar to a Deployment — both run pods. But the **replica model** is fundamentally different:

* **Deployment**: You specify an explicit replica count (e.g., `replicas: 3`). The scheduler places pods wherever there's room. Multiple replicas might land on the same node.
* **DaemonSet**: The replica count **equals the number of nodes**. Exactly one pod per node. Pods are **distributed across all nodes** by definition. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### Use Cases — Logging and Monitoring

The instructor is direct about the use case: "DaemonSet — we use usually to collect logs or do monitoring of your worker nodes or even master node. And frankly, I have not seen any other use case for DaemonSet." [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

Tools like **Prometheus** (monitoring), **Grafana** (dashboards), and **Fluentd** (log collection) run as DaemonSets. They need an agent on every node to collect node-level metrics and logs. You don't manually deploy these — "You will have some readymade manifest definition file. You just run them, they run as a DaemonSet." [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### DaemonSet Self-Healing

Like Deployments, DaemonSets are **self-healing controllers**. If you delete a DaemonSet's pod, the DaemonSet controller **recreates it on that same node**. The only way a DaemonSet pod disappears is if the node itself is removed from the cluster. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### DaemonSet + Tolerations (Master Node)

The instructor ties DaemonSet back to Taints and Tolerations with a practical example: the **fluentd-elasticsearch** DaemonSet. The documentation sample includes a toleration for the master node's taint:

```yaml
tolerations:
- key: node-role.kubernetes.io/master
  operator: Exists
  effect: NoSchedule
```

This says: "If the master node has the `node-role.kubernetes.io/master` key tainted with NoSchedule, I can tolerate it — run on the master too." Without this toleration, the DaemonSet only runs on worker nodes. With it, it runs on **all nodes including the master** — which is exactly what you want for cluster-wide logging/monitoring. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

The instructor verifies this in the cluster: the DaemonSet runs 3 pods — 2 on worker nodes and 1 on the master node — because of the toleration.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Covering

We're exploring four Kubernetes features through documentation examples and live cluster verification: Taints & Tolerations, Resource Requests/Limits, Jobs/CronJobs, and DaemonSets. The focus is understanding each feature's purpose and seeing it operate in a real cluster. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## Part 1: Taints and Tolerations

### Taint a Node

```bash
kubectl taint node <node-name> key=value:NoSchedule
```

**Breakdown:**

* `kubectl taint` — Apply a taint to a node
* `node <node-name>` — Target node
* `key=value` — The key-value pair that "paints" the node
* `:NoSchedule` — The effect: no pod without matching toleration will be scheduled here [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### Add Toleration to a Pod

In the pod YAML:

```yaml
tolerations:
- key: "key"
  operator: "Equal"
  value: "value"
  effect: "NoSchedule"
```

Or using `Exists` operator (matches if the key exists regardless of value):

```yaml
tolerations:
- key: "key"
  operator: "Exists"
  effect: "NoSchedule"
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### How to Verify

If a pod without the matching toleration tries to schedule on a tainted node, it will remain **Pending** or be placed on a different node. Use `kubectl describe pod <name>` to see scheduling events.

***

## Part 2: Resource Requests and Limits

### Pod YAML with Resources

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

**Breakdown:**

* `requests.memory: "64Mi"` — Reserve 64 MiB of memory (scheduler won't place on nodes with less available)
* `requests.cpu: "250m"` — Reserve 250 millicores (0.25 CPU cores)
* `limits.memory: "128Mi"` — Maximum 128 MiB (OOMKilled if exceeded)
* `limits.cpu: "500m"` — Maximum 0.5 CPU cores (throttled if exceeded)

### What Happens Without Limits

The pod may consume unlimited resources on the node, potentially starving other workloads. In production, always set both requests and limits. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## Part 3: Jobs and CronJobs

### Job YAML Structure

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-task
spec:
  template:
    spec:
      containers:
      - name: worker
        image: busybox
        command: ["echo", "processing complete"]
      restartPolicy: Never
```

**Key difference from Pod:** `Kind: Job` runs to completion and stops. `Kind: Pod` runs indefinitely. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### CronJob YAML Structure

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scheduled-task
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: task
            image: busybox
            command: ["echo", "scheduled run"]
```

**`schedule: "* * * * *"`** — Cron format. This example runs every minute. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## Part 4: DaemonSet — Live Cluster Exercise

### Step 1: Check Existing DaemonSets

```bash
kubectl get ds -A
```

**Breakdown:**

* `kubectl get ds` — List DaemonSets (`ds` is the abbreviation)
* `-A` — Across **all namespaces** [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

**Expected output:** You should see existing DaemonSets in the `kube-system` namespace (e.g., `ebs-csi-node` with 3 desired/ready — matching the total number of nodes).

***

### Step 2: Deploy the Fluentd DaemonSet from Documentation

Copy the sample DaemonSet YAML from the Kubernetes documentation (the fluentd-elasticsearch example).

```bash
vim daemonset.yaml
```

Paste the YAML content. Key elements to notice in the definition:

**Tolerations section:**

```yaml
tolerations:
- key: node-role.kubernetes.io/master
  operator: Exists
  effect: NoSchedule
```

This toleration allows the DaemonSet pods to run on master nodes (which are tainted by default). [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

**Resources section:**

```yaml
resources:
  requests:
    memory: "..."
    cpu: "..."
  limits:
    memory: "..."
    cpu: "..."
```

Requests and limits prevent the logging agent from consuming excessive resources. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

Save and quit (`:wq`).

***

### Step 3: Apply the DaemonSet

```bash
kubectl apply -f daemonset.yaml
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

### Step 4: Verify the DaemonSet

```bash
kubectl get ds -A
```

**Expected:** The new DaemonSet shows **DESIRED: 3, CURRENT: 3, READY: 3** — one pod on each of the three nodes (2 workers + 1 master). [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

```bash
kubectl get pod -n kube-system
```

**Expected:** Three fluentd pods, each running on a different node. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### Why 3 Pods (Not Just 2)?

Because the toleration allows the DaemonSet to schedule on the master node. Without the toleration, it would only be 2 pods (worker nodes only). The instructor explicitly confirms: "Since we have given Toleration, that's why it's also running on master node. Otherwise, it won't run on master node." [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

### Self-Healing Test

If you delete one of the DaemonSet's pods, the DaemonSet controller will **immediately recreate** it on the same node — just like a Deployment recreates pods. The only way to remove a DaemonSet pod permanently is to remove the node from the cluster. [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🎨 Taints & Tolerations

```
TAINT (on NODE):
  kubectl taint node <node> key=value:NoSchedule
  → "Paints" the node → REPELS all pods without matching toleration

TOLERATION (on POD):
  tolerations:
  - key: "key"
    operator: Equal/Exists
    value: "value"
    effect: NoSchedule
  → "I can tolerate that paint" → ALLOWED to schedule on tainted node

INTERACTION:
  Node has taint + Pod has NO toleration → Pod CANNOT run on that node
  Node has taint + Pod HAS toleration    → Pod CAN run on that node
  Node has NO taint                      → Any pod can run (default)

KEY EXAMPLE: Master node
  Master is tainted: NoSchedule (by default)
  → No workload pods run on master
  → Monitoring/logging DaemonSets add toleration → run on master too
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 📊 Resource Requests & Limits

```
resources:
  requests:                    limits:
    memory: "64Mi"               memory: "128Mi"
    cpu: "250m"                  cpu: "500m"
    │                            │
    └── RESERVING                └── RESTRICTING
        (scheduler uses          (runtime enforces
         to place pod)            maximum usage)

NO REQUEST → may not get scheduled efficiently
NO LIMIT   → pod may consume UNLIMITED resources → danger

  Request < actual usage < Limit  → normal operation
  actual usage > Limit (memory)   → OOMKilled
  actual usage > Limit (CPU)      → throttled
  No node meets Request           → pod stays Pending
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## ⏱️ Jobs & CronJobs

```
POD:       Runs FOREVER (nginx, mysql, tomcat — continuous services)
JOB:       Runs ONCE → completes → exits (batch processing, migrations)
CRONJOB:   Runs on SCHEDULE → repeats at intervals (like Linux crontab)

JOB:
  Kind: Job
  → Container runs command → completes → Job marked done

CRONJOB:
  Kind: CronJob
  schedule: "* * * * *"  ← cron format (same as Linux cron, EventBridge)
  → Creates a Job at each scheduled time
  → Each Job runs → completes → next Job at next interval

DISTINCTION:
  Job = "run this task NOW"
  CronJob = "run this task EVERY [interval]"  (like an alarm)
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 🔄 DaemonSets

```
DAEMONSET:
  → Ensures EXACTLY ONE pod per node
  → 4 worker nodes = 4 pods (automatically)
  → Add 5th node  = 5th pod (automatically)
  → Remove a node = that pod gone (automatically)

DAEMONSET vs DEPLOYMENT:
  Deployment: replicas: 3 → 3 pods, scheduler decides WHERE (may overlap nodes)
  DaemonSet:  replicas = number of nodes → 1 pod PER node (distributed by design)

USE CASES:
  → Log collection (Fluentd, Filebeat)
  → Monitoring (Prometheus node exporter)
  → "Frankly, I have not seen any other use case"

SELF-HEALING:
  Delete a DaemonSet pod → DaemonSet recreates it on SAME node
  Only disappears if NODE is removed from cluster

MASTER NODE INCLUSION:
  Default: DaemonSet does NOT run on master (master is tainted)
  With toleration for master taint → runs on master TOO
  → 2 workers + 1 master = 3 pods (with toleration)
  → 2 workers + 1 master = 2 pods (without toleration)
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 🔗 How All Four Concepts Connect (DaemonSet Example)

```
FLUENTD DAEMONSET (log collector):
  │
  ├── KIND: DaemonSet
  │     → One pod per node (distributed logging)
  │
  ├── TOLERATION:
  │     key: node-role.kubernetes.io/master
  │     operator: Exists
  │     effect: NoSchedule
  │     → Allows running on master node (tainted by default)
  │
  ├── RESOURCES:
  │     requests: memory + cpu (reserve minimum for log collection)
  │     limits: memory + cpu (prevent log agent from starving workloads)
  │
  └── RESULT: 3 pods (2 workers + 1 master), resource-constrained,
              self-healing, auto-scaling with node count
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## ⚡ Commands Quick Reference

```bash
# TAINTS
kubectl taint node <node> key=value:NoSchedule     # Apply taint
kubectl taint node <node> key=value:NoSchedule-     # Remove taint (note the -)

# DAEMONSETS
kubectl get ds -A                                   # List all DaemonSets
kubectl get pod -n kube-system                      # See DaemonSet pods
kubectl apply -f daemonset.yaml                     # Deploy DaemonSet

# JOBS
kubectl apply -f job.yaml                           # Run a Job
kubectl get jobs                                    # List Jobs

# CRONJOBS
kubectl apply -f cronjob.yaml                       # Create CronJob
kubectl get cronjobs                                # List CronJobs
```

***

## 📐 Kubernetes Resource Kind Spectrum

```
KIND              LIFECYCLE          REPLICAS              USE CASE
────              ─────────          ────────              ────────
Pod               Forever            1 (manual)            Basic unit (rarely used alone)
Deployment        Forever            N (you specify)       Stateless apps (web, API)
DaemonSet         Forever            = number of nodes     Logging, monitoring (1 per node)
Job               Run-to-completion  1 (or parallel)       Batch tasks, migrations
CronJob           Scheduled          1 per schedule        Periodic tasks (cleanup, reports)

CONTROLLERS (manage pods):
  Deployment  → manages ReplicaSet → manages Pods
  DaemonSet   → manages Pods (1 per node)
  Job         → manages Pod (run to completion)
  CronJob     → manages Jobs (on schedule)
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: REPULSION-BASED SCHEDULING (Taints & Tolerations)
  Default: DENY all → Selectively ALLOW with tolerations
  → Same as: Firewall deny-all + allow rules (Security Groups)
    Default-deny network policies, RBAC deny-by-default
  → PRINCIPLE: Secure by default, permit explicitly

PATTERN 2: RESOURCE BUDGETING (Requests & Limits)
  Reserve minimum (request) + Cap maximum (limit)
  → Same as: AWS instance types (min resources guaranteed),
    Linux cgroups, Docker resource constraints,
    Database connection pool min/max
  → PRINCIPLE: Guarantee minimum, prevent monopolization

PATTERN 3: ONE-PER-NODE DISTRIBUTION (DaemonSet)
  Sidecar/agent on every node, auto-scales with fleet
  → Same as: SSM Agent on every EC2, node_exporter everywhere,
    antivirus on every workstation, log forwarder per host
  → PRINCIPLE: Infrastructure agents must be everywhere

PATTERN 4: RUN-TO-COMPLETION vs. RUN-FOREVER (Job vs. Pod)
  Some workloads have a natural end; don't force them into forever-running containers
  → Same as: Lambda functions (run and done), batch jobs,
    cron tasks, one-time migration scripts
  → PRINCIPLE: Match the workload lifecycle to the right abstraction
```

 [\[341-extras \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/341-extras.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → Pods, Deployments, Services, debugging (kubectl get/describe/logs)
THIS      → EXTRAS (administration concepts):
              Taints & Tolerations (node scheduling control)
              Requests & Limits (resource management)
              Jobs & CronJobs (finite workloads)
              DaemonSets (one-per-node agents)
NEXT      → Further Kubernetes topics or projects

INSTRUCTOR: "These are mostly administration things.
             They are really very simple things
             and I thought you should know them."
```

***

Your Kubernetes Extras deep learning material is fully reconstructed — covering the four administration concepts with their interconnections (especially how Taints, Tolerations, Resources, and DaemonSets combine in the fluentd example). Ready for the next lecture or want me to generate **AnkiDeck flashcards (.csv)** from this or the full lecture series? 🃏
