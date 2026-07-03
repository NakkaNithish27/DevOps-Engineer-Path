# ☸️ Kubernetes ReplicaSet — Deep Learning Material

**Source:** Video caption file — [333-replica-set.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt?EntityRepresentationId=a02d293c-daac-4cf5-8503-8a96ab772b9f), with supporting command reference — [333.replicaSet.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333.replicaSet.txt?EntityRepresentationId=51186ff5-542a-4f51-933d-aaac05df9407) [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt), [\[333.replicaSet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333.replicaSet.txt)

**Video Context:** The instructor teaches the Kubernetes ReplicaSet object — what it is, why it exists, how it maintains pod replicas, the YAML definition file structure (with label-selector mechanics), creating a ReplicaSet, observing self-healing behavior when pods are deleted, three different ways to scale (declarative YAML, imperative CLI, kubectl edit), and cleanup. The instructor uses the official Kubernetes documentation's ReplicaSet example and runs all commands on a Kops-managed cluster.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Core Problem — Pods Alone Are Fragile

The instructor opens with a vivid scenario: "You have a pod running on a node and users are accessing it. The pod is running some web application. And for some reason the pod goes down — the users won't be able to access the service. And that's it, end of the story. Someone needs to login, delete the pod, recreate it, fix the problem." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

A bare pod (created directly with `kubectl create`) has **no self-healing capability**. If the pod crashes, it stays dead. If the node it runs on crashes, the pod is gone permanently. There is no mechanism watching over it, no controller to detect the failure and recreate it. The pod is an ephemeral, unmanaged process — exactly like a standalone Linux process that dies and nobody restarts it.

This is the fundamental problem ReplicaSet solves: **automated pod lifecycle management** — maintaining a specified number of pod replicas at all times, recreating pods that fail, and enabling scaling up and down.

***

## 1.2 What a ReplicaSet Is

"ReplicaSet maintains a Replica of your pod." The instructor defines it clearly: a ReplicaSet is a Kubernetes **controller object** that ensures a specified number of identical pods are running at all times. You tell it "I want 3 replicas of this pod" and the ReplicaSet guarantees that exactly 3 pods exist. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The official documentation quote the instructor reads: "Purpose is to maintain a stable set of replica pods running at any given time. It is often used to guarantee the availability of a specified number of identical pods." The word **guarantee** is emphasized — "You said three replicas. It's going to give you three. If something goes wrong with one or two, it will recreate. It will always maintain those three replicas." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## 1.3 Self-Healing — Automatic Pod Recreation

This is the most important behavior of a ReplicaSet. If any pod managed by the ReplicaSet crashes, is deleted, or becomes unavailable, the ReplicaSet **automatically creates a replacement pod** to maintain the desired replica count. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The instructor demonstrates this dramatically: he deletes two pods simultaneously, and new pods appear within **4 seconds** — "How that was so fast. You know, these are two new pods. Look at their age — 4 seconds. How quickly they got created. Because it's just a process time." The ReplicaSet controller constantly watches its pod count, detects the discrepancy (desired: 3, current: 1), and immediately schedules new pods to restore the count. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

This extends to **node failures**: "The best part is — if you have pods running on a node without ReplicaSet, just you created a pod and that node goes down, pod goes down. That's it, end of the story. But if it is created with a ReplicaSet, it will recreate that pod for you." When a node crashes, the scheduler redistributes pods from the failed node to healthy worker nodes. Without a ReplicaSet, there's no controller to trigger this redistribution. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## 1.4 Why Use ReplicaSet with Just One Replica?

The instructor addresses a natural question: "If I have to mention one, why will I use ReplicaSet? Well, for the health checks. If your pod goes down, you don't need to manually recreate it. ReplicaSet will do it for you automatically." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

Even with `replicas: 1`, the ReplicaSet provides self-healing. A bare pod with no ReplicaSet that crashes stays dead until someone manually recreates it. A pod managed by a ReplicaSet with `replicas: 1` that crashes is automatically replaced. The value isn't in having multiple copies — it's in having a **controller** that watches and restores.

***

## 1.5 Scaling — Adding and Removing Pods

The ReplicaSet enables both **scale-out** (adding pods) and **scale-in** (removing pods). The instructor states: "You can add more pods into the ReplicaSet. You can remove pods from the ReplicaSet." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

When you scale up, the scheduler distributes new pods across available worker nodes. "The best part is you're mentioning more replicas — scheduler will distribute your pods across multiple worker nodes." This provides both capacity (more pods to handle traffic) and resilience (pods spread across nodes, so a single node failure doesn't take down all replicas). [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## 1.6 The YAML Definition File — Structure and Label Mechanics

The instructor takes the ReplicaSet definition directly from the official Kubernetes documentation and breaks it down: [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: guestbook
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
```

### API Version: `apps/v1`

The instructor notes: "Not just v1 — this is new style of API versioning for the newer objects. Older objects like pod will have `v1`, but newer objects like ReplicaSet, deployments, ingress will have API versioning in this format: `apps/v1`." This is a Kubernetes API group distinction — core objects use `v1`, while application-level controllers use `apps/v1`. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

### Kind: `ReplicaSet`

Tells Kubernetes what type of object to create.

### Metadata

The name (`frontend`) and labels (key-value pairs like `app: guestbook`, `tier: frontend`). "You can give as many labels as you want. We use labels for filtering, inspection." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

### Spec → replicas

"Replicas: 3. You can mention the number of replicas." This is the desired state — how many pods the ReplicaSet should maintain. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

### Spec → selector → matchLabels

This is the **most important conceptual mechanism** in the file. The `matchLabels` defines how the ReplicaSet identifies which pods belong to it. The instructor explains: [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

### Spec → template

"In template, you have all the pod information — from metadata till the end." The template section is essentially a **pod definition embedded inside the ReplicaSet definition**. It has its own `metadata` (with labels) and `spec` (with containers).

### The Label-Selector Connection

The template's pod labels (`tier: frontend`) must **match** the selector's `matchLabels` (`tier: frontend`). The instructor explains this relationship precisely: "This label is matching exactly the same matchLabel here. So this simply means that any pod that has this label — that is in this ReplicaSet." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The critical implication: "If you have an existing pod with the same label, you mentioned replica 3, you already have one pod with the same label — then this ReplicaSet will create just two pods. Because one already exists with this label." The ReplicaSet doesn't just create pods — it first **counts existing pods** that match the selector labels, then creates only the difference to reach the desired replica count. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

🔍 **Deep Dive:** The label-selector mechanism is how Kubernetes implements **loose coupling** between controllers and pods. The ReplicaSet doesn't track pods by name or ID — it tracks them by label. Any pod with matching labels is considered part of the ReplicaSet, regardless of who created it. This means you could accidentally "adopt" existing pods into a ReplicaSet if their labels match, or a ReplicaSet might not create all expected pods because existing pods already satisfy the count. Understanding this prevents subtle bugs where pod counts don't match expectations.

***

## 1.7 Pod Status — Desired, Current, and Ready

When running `kubectl get rs`, the output shows three counts: [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

* **Desired** — what you specified in `replicas` (3)
* **Current** — how many pods actually exist (3)
* **Ready** — how many pods are fully operational and passing health checks (3)

The instructor explains the difference: "Your pod may have some problem. So you may have current as three and ready as maybe two. Maybe one pod is still getting created. Or maybe having some problem, not getting created. It doesn't have resources. There could be many problems." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The goal is **desired = current = ready**. Any discrepancy indicates a problem: current < desired means pods are failing to be created; ready < current means pods exist but aren't healthy.

***

## 1.8 Container Count per Pod — The `1/1` Notation

In `kubectl get pod` output, the instructor points out: "One by one — out of one container, one is running. If you have multiple containers, you can have three containers maybe in a pod. And you can see out of three, one is running." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The `READY` column shows `1/1` — meaning 1 container out of 1 total is ready. A pod with 3 containers would show `3/3` when all are healthy, or `2/3` if one container is failing. This provides per-pod, per-container health visibility. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## 1.9 Three Ways to Scale — Declarative vs. Imperative

The instructor demonstrates three methods to change the replica count, with a clear recommendation: [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**Method 1 — Declarative (RECOMMENDED):** Edit the YAML file, change the `replicas` value, then `kubectl apply -f replset.yaml`. The instructor changes replicas from 3 to 5, applies, and sees 5 pods. "The best way is always declarative. Better always make the change in the definition file." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**Method 2 — Imperative CLI:** `kubectl scale --replicas=1 rs/frontend`. This directly tells Kubernetes to change the replica count without modifying any file. Quick but the YAML file now doesn't match the running state. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**Method 3 — kubectl edit:** `kubectl edit rs frontend`. This opens the live ReplicaSet definition in a text editor (like vi). You change the `replicas` value, save, and quit. Kubernetes applies the change immediately. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The instructor explicitly warns: "These last two methods — this one and this one — is not at all recommended in production. Always be going to do it through definition files, through manifest, and we apply the changes." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The reasoning: imperative commands and live edits change the running state but **don't update the source YAML file**. This creates **configuration drift** — what's running doesn't match what's defined. If someone later applies the original YAML file, the replica count reverts to the old value. Declarative management through files ensures the source of truth (the YAML file) always matches the running state.

***

## 1.10 The kubectl Cheat Sheet

The instructor addresses a common learner concern: "If you're thinking, 'Hey, where did this command come from? Do I need to remember it?' Well, I did it so many times, so I remember it. But trust me, you don't need to remember it." He navigates to the **kubectl Cheat Sheet** in the official Kubernetes documentation. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

The cheat sheet contains commonly used commands organized by category (scaling resources, viewing resources, etc.). The instructor finds the `scale` command under "Scaling Resources" and recommends: "You should really bookmark this. I use this a lot." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## 1.11 Cleanup — Deleting the ReplicaSet (Not the Pods)

The instructor makes a critical operational point: "You cannot really delete pods here — they will get created again. So you just need to delete the ReplicaSet, and that in turn will delete the pods." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

If you try to delete individual pods managed by a ReplicaSet, the self-healing mechanism immediately creates replacements — you're fighting the controller. To actually remove the pods, you must delete the controller (ReplicaSet) itself. When the ReplicaSet is deleted, it takes all its managed pods with it.

`kubectl delete rs frontend` — deletes the ReplicaSet AND all pods it manages. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a Kubernetes **ReplicaSet** that maintains 3 replicas of a pod, demonstrating self-healing (pod auto-recreation), scaling (up and down via three methods), and proper cleanup. The final outcome: understanding how to define, create, scale, and delete ReplicaSets — the foundational controller for pod availability in Kubernetes. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## Step 1: Create the ReplicaSet YAML File

```bash
vim replset.yaml
```

Paste the ReplicaSet definition from the official Kubernetes documentation: [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: guestbook
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
```

Save and exit (`:wq`).

**Key points to verify in the file:**

* `selector.matchLabels.tier: frontend` **matches** `template.metadata.labels.tier: frontend` — this is mandatory
* `replicas: 3` — the desired pod count
* The `template` section defines what each pod looks like (container name, image) [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**You can change names** (ReplicaSet name, container name) if you want, but the instructor uses the defaults from the documentation.

***

## Step 2: Create the ReplicaSet

```bash
kubectl create -f replset.yaml
```

**Breakdown:**

* `kubectl create` — create a Kubernetes resource
* `-f replset.yaml` — from the specified file [\[333.replicaSet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333.replicaSet.txt)

**Alternatively:** `kubectl apply -f replset.yaml` works the same for initial creation and also supports updates later.

***

## Step 3: Verify the ReplicaSet

```bash
kubectl get rs
```

**Breakdown:**

* `kubectl get rs` — list ReplicaSets (`rs` is the short form for `replicaset`) [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**Expected output:**

```
NAME       DESIRED   CURRENT   READY
frontend   3         3         3
```

**Interpretation:** Desired=3 (what you asked for), Current=3 (how many exist), Ready=3 (how many are healthy). All three matching means the ReplicaSet is fully operational. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

### Verify pods:

```bash
kubectl get pod
```

**Expected output:** Three pods with names like `frontend-xxxxx` (ReplicaSet name + random suffix). Each showing `1/1` READY and `Running` status. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## Step 4: Demonstrate Self-Healing — Delete Pods

```bash
kubectl delete pod frontend-qmxml frontend-s4kbp
```

Delete two of the three pods simultaneously (use the actual pod names from your `kubectl get pod` output). [\[333.replicaSet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333.replicaSet.txt)

**Immediately run:**

```bash
kubectl get pod
```

**Expected result:** You'll still see **three pods** — but two of them are brand new (age: a few seconds). The ReplicaSet detected the count dropped from 3 to 1 and instantly created 2 replacements. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**The point:** "How quickly they got created — 4 seconds. Because it's just a process time." The ReplicaSet controller is constantly reconciling desired state vs. actual state. Any discrepancy is corrected immediately.

**Connection to flow:** This proves that deleting pods directly is futile when a ReplicaSet manages them — the controller always restores the desired count.

***

## Step 5: Scale Up — Declarative Method (RECOMMENDED)

```bash
vim replset.yaml
```

Change `replicas: 3` to `replicas: 5`. Save and exit. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

```bash
kubectl apply -f replset.yaml
```

**Breakdown:**

* `kubectl apply` — apply the configuration changes from the file. Since the ReplicaSet already exists, it updates it.

```bash
kubectl get pod
```

**Expected result:** Five pods now running. Two new pods were created to go from 3 → 5. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**Why this method is best:** The YAML file is the source of truth. After applying, the file and the running state match. Version control can track changes. Team members can see what changed and why.

***

## Step 6: Scale Down — Imperative CLI Method (NOT recommended for production)

```bash
kubectl scale --replicas=1 rs/frontend
```

**Breakdown:**

* `kubectl scale` — the scaling command
* `--replicas=1` — set the desired count to 1
* `rs/frontend` — target the ReplicaSet named `frontend` [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

```bash
kubectl get pod
```

**Expected result:** Only 1 pod remains. Four pods were terminated.

⚠️ **Warning:** The YAML file still says `replicas: 5`. The running state (1) now disagrees with the file (5). If someone runs `kubectl apply -f replset.yaml`, it jumps back to 5. This is **configuration drift** — the reason imperative commands are discouraged in production. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

***

## Step 7: Scale Up — kubectl edit Method (NOT recommended for production)

```bash
kubectl edit rs frontend
```

**What happens:** Opens the live ReplicaSet definition in your default editor (usually `vi`). [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**Alternate syntax:** `kubectl edit rs/frontend` (both forms work — `rs frontend` or `rs/frontend`).

Find the `replicas` field (currently 1), change it to `2`. Save and exit (`:wq`).

```bash
kubectl get pod
```

**Expected result:** Two pods now running. [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

⚠️ **Same warning as Step 6:** This edits the live state, not the file. Configuration drift occurs.

***

## Step 8: Finding Commands — The kubectl Cheat Sheet

If you forget the `scale` command syntax:

Navigate to: **Kubernetes official documentation → kubectl Cheat Sheet** [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

Search for "Scaling Resources" — you'll find the `kubectl scale` command and its options.

**Instructor's advice:** "You should really bookmark this. I use this a lot." You don't need to memorize every command — use the cheat sheet as a reference.

***

## Step 9: Cleanup — Delete the ReplicaSet

```bash
kubectl delete rs frontend
```

**Breakdown:**

* `kubectl delete rs frontend` — delete the ReplicaSet named `frontend` [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**What happens:** The ReplicaSet is deleted, AND all pods it manages are automatically terminated.

```bash
kubectl get pod
```

**Expected result:** No pods — "gone." [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)

**Critical point:** You MUST delete the ReplicaSet to remove the pods. If you try `kubectl delete pod <name>`, the ReplicaSet immediately recreates it. The only way to stop the pods is to remove the controller that's managing them.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ ReplicaSet — Core Concept

```
WITHOUT ReplicaSet:
  Pod crashes → stays dead → manual intervention required
  Node crashes → pod gone forever → "end of the story"

WITH ReplicaSet:
  Pod crashes → ReplicaSet detects → new pod created (seconds)
  Node crashes → pods rescheduled to healthy nodes automatically
  
ReplicaSet = CONTROLLER that maintains desired pod count
  replicas: N → always N pods running (self-healing guarantee)
  Even replicas: 1 → still valuable (auto-restart on failure)
```

***

## ⚡ YAML Structure — Component Map

```yaml
apiVersion: apps/v1          ← apps group (not core v1)
kind: ReplicaSet
metadata:
  name: frontend             ← ReplicaSet name
  labels: ...                ← RS labels (for filtering RS itself)
spec:
  replicas: 3                ← DESIRED pod count
  selector:
    matchLabels:
      tier: frontend         ← HOW RS finds its pods
  template:                  ← EMBEDDED POD DEFINITION
    metadata:
      labels:
        tier: frontend       ← MUST MATCH selector.matchLabels
    spec:
      containers:
      - name: php-redis
        image: gcr.io/...
```

***

## 🔗 Label-Selector Mechanism

```
selector.matchLabels: tier=frontend
    ↕ MUST MATCH
template.metadata.labels: tier=frontend

HOW IT WORKS:
  RS counts pods with label tier=frontend
  If count < desired → create more pods
  If count > desired → terminate excess pods
  If count = desired → do nothing (reconciled)

⚠️ GOTCHA: Existing pods with matching labels get "adopted"
  You say replicas: 3, 1 pod already has tier=frontend
  → RS creates only 2 more (not 3)
```

***

## 📊 `kubectl get rs` Output Fields

```
DESIRED  = what you specified in replicas
CURRENT  = how many pods exist right now
READY    = how many pods are healthy and serving

GOAL: desired = current = ready
  current < desired → pods failing to create (resource issues?)
  ready < current   → pods exist but unhealthy
```

***

## 🔄 Three Scaling Methods

```
1. DECLARATIVE (✅ RECOMMENDED):
   Edit YAML → change replicas → kubectl apply -f file.yaml
   ✅ File = source of truth, matches running state
   ✅ Version-controllable, team-visible

2. IMPERATIVE CLI (❌ NOT for production):
   kubectl scale --replicas=N rs/frontend
   ❌ File not updated → configuration drift

3. KUBECTL EDIT (❌ NOT for production):
   kubectl edit rs frontend → change replicas → save
   ❌ File not updated → configuration drift

DRIFT: running state ≠ file state
  → someone applies file later → state reverts unexpectedly
```

***

## 🔄 Self-Healing Flow

```
DESIRED: 3 pods

EVENT: 2 pods deleted (crash / node failure / manual delete)
    ↓
RS CONTROLLER detects: current=1, desired=3
    ↓
RS creates 2 new pods (within seconds)
    ↓
RESULT: 3 pods running again (2 new, 1 original)

SPEED: ~4 seconds (just process scheduling time)
```

***

## 🧹 Cleanup Logic

```
DELETE PODS DIRECTLY?
  kubectl delete pod frontend-xxx → RS recreates immediately → FUTILE
  
DELETE REPLICASET:
  kubectl delete rs frontend → RS deleted → all managed pods terminated
  
RULE: To remove pods, remove the CONTROLLER managing them
      (applies to ReplicaSet, Deployment, DaemonSet, etc.)
```

***

## 📦 API Versioning Pattern

```
OLDER objects (Pod, Service, ConfigMap):
  apiVersion: v1

NEWER objects (ReplicaSet, Deployment, Ingress):
  apiVersion: apps/v1
  
FORMAT: <group>/<version>
  apps/v1 → application-level controllers
  v1      → core objects (implicit core group)
```

***

## 🔗 Pod Naming Convention

```
ReplicaSet name: frontend
Pod names:       frontend-xxxxx (RS name + random hash)

Container readiness: 1/1 = 1 container ready out of 1 total
                     2/3 = 2 containers ready out of 3 total
```

***

## ⚡ Command Quick Reference

```
CREATE:     kubectl create -f replset.yaml
            kubectl apply -f replset.yaml

VIEW:       kubectl get rs              ← list ReplicaSets
            kubectl get pod             ← list pods

SCALE:      vim replset.yaml → edit replicas → kubectl apply -f replset.yaml  ✅
            kubectl scale --replicas=N rs/frontend                            ❌
            kubectl edit rs frontend                                          ❌

DELETE:     kubectl delete rs frontend  ← deletes RS + all pods

HELP:       kubectl cheat sheet (official docs, bookmark it)
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Controller-Managed Desired State**
You declare what you want (3 replicas). A controller continuously reconciles actual state with desired state. You never manage individual instances — you manage the controller's configuration. This is the fundamental Kubernetes pattern and appears identically in AWS Auto Scaling Groups (desired capacity), Docker Swarm (service replicas), and any declarative orchestration system. The mental model: **manage the spec, not the instances**.

**Pattern 2: Label-Based Loose Coupling**
Controllers don't track pods by name or creation order — they track by labels. This creates a flexible, decoupled system where pods can be created, destroyed, and recreated freely as long as the label contract is maintained. But it also means labels must be managed carefully — accidental label matches cause unexpected adoption or exclusion.

**Pattern 3: Declarative > Imperative for State Management**
Imperative commands (`kubectl scale`, `kubectl edit`) change running state but leave the source definition file out of sync. Declarative changes (edit YAML → `kubectl apply`) keep the file and running state aligned. In production, the YAML file is the source of truth — it's version-controlled, reviewable, and reproducible. Imperative commands are for quick experiments only.

***

## 🎯 One-Line System Summary

> **A Kubernetes ReplicaSet is a controller that maintains a specified number of pod replicas by continuously reconciling desired state (YAML `replicas` field) with actual state (pods matching the `selector.matchLabels`), automatically recreating pods within seconds when they fail, distributing pods across nodes for resilience, scaling via declarative YAML changes (recommended) or imperative commands (not recommended), and requiring deletion of the ReplicaSet itself (not individual pods) for cleanup since the controller will always restore its desired count.** [\[333-replica-set \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/333-replica-set.txt)
