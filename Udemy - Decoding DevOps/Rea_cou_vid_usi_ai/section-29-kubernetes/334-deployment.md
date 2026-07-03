# 🎓 Deep Learning Material: Kubernetes Deployments — Rolling Updates, Rollbacks & ReplicaSet Management

*Reconstructed from video lecture captions (334-deployment.txt) and command reference (334.deployment.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What a Deployment Is and Why It's the Most Important Object for DevOps

A Deployment is a Kubernetes object that manages the **lifecycle of your application Pods** — creating them, updating them, rolling back changes, and scaling them. The instructor calls it *"one of the most used objects by us"* (DevOps engineers) and explains why: *"Most of the DevOps work is involved around deployments, making changes, making regular changes to the application, to the code."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

The Deployment's core value proposition: you **declare a desired state** (which image, how many replicas, which configuration), and the Deployment Controller **continuously works to make the actual state match** that desired state. If you change the desired state (new image tag), the controller **transitions the actual state** to match — gracefully, in a rolling fashion, one Pod at a time. If something goes wrong, you can **roll back** to a previous state. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

The instructor frames this precisely: *"You can define the desired state — I want this particular image tag, these many replicas. And when you apply, this Deployment Controller will change the actual state, which could be an older image tag, to the desired state, which could be a new image tag, at a controlled rate."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

***

## 1.2 The Three-Layer Hierarchy: Deployment → ReplicaSet → Pods

This is the architectural relationship that makes Deployments powerful. A Deployment does **not** directly manage Pods. Instead, it creates and manages **ReplicaSets**, and the ReplicaSets manage the Pods. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

```
Deployment
  └── ReplicaSet (created and managed by Deployment)
        └── Pods (created and managed by ReplicaSet)
```

The instructor states: *"Deployment uses ReplicaSet. You give a definition of Deployment. This in turn creates ReplicaSet. And ReplicaSet will maintain your Pod."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

This layering is not just organizational — it's the **mechanism** that enables rolling updates and rollbacks (explained in Section 1.4).

***

## 1.3 The Deployment Definition File

The Deployment definition (YAML) is structurally almost identical to a ReplicaSet definition. The instructor explicitly asks learners to compare them and spot the differences. The key structural elements: [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt), [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

The instructor breaks this down: [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

* **`apiVersion: apps/v1`** — Same as ReplicaSet
* **`kind: Deployment`** — This is what makes it a Deployment (vs. `ReplicaSet` or `ReplicationController`)
* **`metadata`** — Name and labels for the Deployment itself
* **`spec.replicas: 3`** — *"This information is for the ReplicaSet"* — how many Pod replicas to maintain
* **`spec.selector.matchLabels`** — One difference from older ReplicationController: uses `matchLabels` under `selector` (ReplicationController used selector directly with the label name)
* **`spec.template`** — Everything from `template` onward is **Pod information**: the Pod's labels, container name, container image (with tag), and port

The instructor identifies the boundary: *"From metadata till here, it's all Pod information."* The Deployment wraps the Pod template and adds replica count and selector logic around it. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

***

## 1.4 Rolling Updates: How Deployments Change Pods

When you change a Deployment's desired state (e.g., update the image tag from `1.14.2` to `1.16.1`), the Deployment Controller performs a **rolling update**. This is the core operational mechanism. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

The instructor explains: *"If you have three replicas of the Pod, it's going to do it one at a time. Changes on the Pod will always happen by deleting the existing Pod and creating a new Pod. So that delete and recreation will be in a controlled rate, one by one."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

**What happens internally with ReplicaSets:**

When you update the image tag, the Deployment does NOT modify the existing ReplicaSet. Instead, it **creates a new ReplicaSet** with the new image tag. Then: [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

1. The new ReplicaSet starts scaling **up** (creating Pods with the new image)
2. The old ReplicaSet starts scaling **down** (terminating Pods with the old image)
3. This happens gradually — one Pod at a time — ensuring the application stays available throughout

The instructor demonstrates this with `kubectl get rs` after an update: *"You see two ReplicaSets here. This is the older one — three minutes and 28 seconds old. When we created the Deployment, it created this ReplicaSet. Now when I made a change, it created a new ReplicaSet. So it will slowly make this to zero. And slowly it will increase the number over here."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

The instructor draws a parallel to AWS: *"If you remember Auto Scaling from AWS, it does it similarly."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

🔍 **Deep Dive:**
The old ReplicaSet is **not deleted** after the rollout completes — it stays with zero replicas. This is the key to rollback capability. Kubernetes keeps the old ReplicaSet as a historical record. When you roll back, it simply scales the old ReplicaSet back up and the current one down. No new objects need to be created — the history already exists in the form of preserved ReplicaSets.

***

## 1.5 Rollback: Returning to a Previous State

If an update causes problems, you can roll back to the previous version. The mechanism is elegant because of the ReplicaSet preservation described above. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

The instructor demonstrates with `kubectl rollout undo deployment/nginx-deployment`. After execution: *"Now the new ReplicaSet has gone to zero. The old ReplicaSet got new Pods."*  The old ReplicaSet (with the previous image tag) scales back up, and the newer one scales down. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

**Rollback to a specific revision:** Kubernetes maintains a **revision history** of all Deployment changes. You can view it with `kubectl rollout history deployment/nginx-deployment`, which shows revision numbers (e.g., revision 2, revision 3). To roll back to a specific revision: `kubectl rollout undo deployment/nginx-deployment --to-revision=<number>`. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

The instructor notes: *"You may have 10, 15 different versions, revision numbers. And you can roll back to any of the revision number you want."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

Each rollback creates yet another ReplicaSet (or reactivates an existing one), and the history continues growing. This gives you a full audit trail and the ability to jump to any previous state.

***

## 1.6 Imperative vs. Declarative: The Instructor's Repeated Warning

The instructor demonstrates the image update using an **imperative command** (`kubectl set image ...`) but immediately warns: *"I know this is imperative, and I told you not to do imperative, but you can still test it. The best way is just change your definition file and apply it."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

He repeats this at the end of the lecture with emphasis: *"I keep repeating myself, but it's very important. You should do everything through definition files, manifest. Imperative is for learning, testing purpose. But in real time, especially in productions, do it through definition files."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

The reason: definition files are **versionable** (stored in Git), **reviewable** (code review), **reproducible** (apply the same file anywhere), and **auditable** (you can see what was defined). Imperative commands leave no trace and cannot be replicated.

***

## 1.7 Scaling via Deployment

Deployments also support scaling — changing the number of replicas. The instructor mentions: *"You can scale by using the scale command... same way here we say deployment and the deployment name, replicas and the number of replicas."* [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

This works the same as scaling a ReplicaSet, but through the Deployment object. The Deployment updates the underlying ReplicaSet's replica count.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a Kubernetes **Deployment** with 3 replicas of an Nginx Pod, performing a **rolling image update** (from `nginx:1.14.2` to `nginx:1.16.1`), executing a **rollback** to the previous version, inspecting the ReplicaSet mechanism that powers it all, and then cleaning up. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt), [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

***

## Phase 1: Create the Deployment

### Step 1: Write the Definition File

```bash
vim deployment.yaml
```

Paste the following content: [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

Save and exit (`:wq`).

**Prerequisite:** If you have existing Pods with the same names/labels from previous exercises, delete them first to avoid conflicts. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

### Step 2: Apply the Deployment

```bash
kubectl apply -f deployment.yaml
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Breakdown:**

* `kubectl apply` — Declaratively apply a configuration
* `-f deployment.yaml` — From this file

**Expected output:** `deployment.apps/nginx-deployment created`

### Step 3: Verify the Three-Layer Hierarchy

**Check the Deployment:**

```bash
kubectl get deploy
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** One deployment `nginx-deployment` with READY 3/3.

**Check the ReplicaSet:**

```bash
kubectl get rs
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** One ReplicaSet with a name like `nginx-deployment-9456bbbf9` — this was auto-created by the Deployment. Shows DESIRED: 3, CURRENT: 3, READY: 3.

**Check the Pods:**

```bash
kubectl get pod
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** Three Pods with names like `nginx-deployment-9456bbbf9-xxxxx` — created by the ReplicaSet.

### Step 4: Verify the Image Tag

```bash
kubectl describe pod nginx-deployment-9456bbbf9-dx5s5
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**What to look for:** In the output, find the `Image:` field — it should show `nginx:1.14.2`. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

**Connection to flow:** Deployment created → ReplicaSet created → 3 Pods created with image `nginx:1.14.2`. The baseline is established.

***

## Phase 2: Perform a Rolling Update

### Step 5: Update the Image Tag (Imperative Method)

```bash
kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.16.1
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Breakdown:**

* `kubectl set image` — Change the image of a resource
* `deployment.v1.apps/nginx-deployment` — The resource type and name
* `nginx=nginx:1.16.1` — `<container_name>=<new_image:tag>`. The container name is `nginx` (from the YAML definition, not the Pod name)

**Critical distinction:** `nginx` here is the **container name** (defined in `spec.containers[].name`), not the Pod name or Deployment name. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

**Reminder:** The declarative (recommended) approach is to edit `deployment.yaml`, change the image tag, and `kubectl apply -f deployment.yaml`. The imperative command is used here for learning. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

### Step 6: Observe the Rolling Update

Immediately run:

```bash
kubectl get deploy
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** Shows the update progressing — you may catch it mid-rollout with different READY/UP-TO-DATE counts.

```bash
kubectl get pod
```

**Expected:** If you run this fast enough, you'll see Pods in various states — some Terminating (old), some ContainerCreating (new), some Running. The ages will be very recent (9 seconds, 15 seconds, 21 seconds as the instructor observes). [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

### Step 7: Verify the New Image on Updated Pods

```bash
kubectl describe pod nginx-deployment-ff6655784-2bn9t
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Important:** Use a **new Pod name** (from the latest `kubectl get pod` output). The old Pod names are gone — those Pods were deleted and replaced. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

**What to look for:** `Image: nginx:1.16.1` — confirming the tag is updated.

### Step 8: Inspect the ReplicaSet Mechanism

```bash
kubectl get rs
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** **Two ReplicaSets** now exist: [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

| ReplicaSet                         | DESIRED | CURRENT | AGE   |
| ---------------------------------- | ------- | ------- | ----- |
| `nginx-deployment-9456bbbf9` (old) | 0       | 0       | \~3m  |
| `nginx-deployment-ff6655784` (new) | 3       | 3       | \~30s |

The old ReplicaSet has been scaled to zero. The new one runs 3 Pods. **The old ReplicaSet is preserved** — this is the rollback mechanism.

***

## Phase 3: Rollback

### Step 9: Roll Back to Previous Version

```bash
kubectl rollout undo deployment/nginx-deployment
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**What happens internally:** The old ReplicaSet (with `nginx:1.14.2`) scales back up to 3. The current ReplicaSet (with `nginx:1.16.1`) scales down to 0. Rolling fashion, one Pod at a time. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

### Step 10: Verify Rollback

```bash
kubectl get rs
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** The old ReplicaSet now shows DESIRED: 3 again. The newer one shows DESIRED: 0. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

```bash
kubectl get pod
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** Three new Pods (freshly created by the old ReplicaSet).

### Step 11: Confirm the Image Tag Reverted

```bash
kubectl describe pod nginx-deployment-9456bbbf9-8xhw6 | grep Image
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** `Image: nginx:1.14.2` — the original tag is back. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

### Step 12: View Revision History

```bash
kubectl rollout history deployment/nginx-deployment
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**Expected:** A list of revisions (e.g., revision 2, revision 3). Each revision corresponds to a state change. [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

**To roll back to a specific revision:**

```bash
kubectl rollout undo deployment/nginx-deployment --to-revision=2
```

 [\[334-deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334-deployment.txt)

This jumps directly to revision 2, regardless of how many changes have happened since.

***

## Phase 4: Cleanup

### Step 13: Delete the Deployment

```bash
kubectl get deploy
kubectl delete deploy nginx-deployment
```

 [\[334.deployment \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/334.deployment.txt)

**What happens:** Deleting the Deployment also deletes its ReplicaSets and all their Pods. The entire hierarchy is cleaned up.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Deployment Identity

```
Deployment = THE primary DevOps object in Kubernetes
  Purpose: Manage Pod lifecycle — create, update, rollback, scale
  Mechanism: Declarative desired state → controller reconciles actual state
  "Most of the DevOps work is involved around deployments"
```

***

## Three-Layer Hierarchy

```
Deployment (you create this)
  └── ReplicaSet (auto-created by Deployment)
        └── Pods (auto-created by ReplicaSet)

You define Deployment → it creates ReplicaSet → RS creates Pods
You NEVER directly create ReplicaSets when using Deployments
```

***

## Definition File Structure

```yaml
apiVersion: apps/v1           # same as ReplicaSet
kind: Deployment               # ← THIS makes it a Deployment
metadata:
  name: nginx-deployment       # Deployment name
  labels:
    app: nginx                 # Deployment label
spec:
  replicas: 3                  # → passed to ReplicaSet
  selector:
    matchLabels:               # ← uses matchLabels (vs. RC's direct selector)
      app: nginx
  template:                    # ── everything below = Pod definition ──
    metadata:
      labels:
        app: nginx             # Pod label (must match selector)
    spec:
      containers:
      - name: nginx            # CONTAINER name (used in set image command)
        image: nginx:1.14.2    # Image:tag (this is what you update)
        ports:
        - containerPort: 80
```

***

## Rolling Update Mechanism

```
BEFORE update:
  Deployment → RS-old (replicas: 3) → [Pod1-old, Pod2-old, Pod3-old]

DURING update (image tag change):
  Deployment → RS-old (scaling DOWN: 3→2→1→0)
             → RS-new (scaling UP: 0→1→2→3)
  
  Controlled rate: one Pod at a time
  Delete old Pod → create new Pod → repeat

AFTER update:
  Deployment → RS-old (replicas: 0, PRESERVED for rollback)
             → RS-new (replicas: 3) → [Pod1-new, Pod2-new, Pod3-new]

KEY: Old RS kept at 0 replicas = rollback capability
```

***

## Rollback Mechanism

```
kubectl rollout undo deployment/nginx-deployment
  → RS-new scales DOWN to 0
  → RS-old scales UP to 3
  → Old Pods recreated with old image tag

No new ReplicaSet created for undo — reuses existing RS

Revision history:
  kubectl rollout history deployment/nginx-deployment
  → Shows revision numbers (2, 3, 4...)
  
  kubectl rollout undo deployment/nginx-deployment --to-revision=2
  → Jump to any specific revision
```

***

## Core Commands

```
── CREATE ──
kubectl apply -f deployment.yaml       → create/update Deployment from file

── INSPECT ──
kubectl get deploy                      → list Deployments
kubectl get rs                          → list ReplicaSets (see old + new)
kubectl get pod                         → list Pods
kubectl describe pod <name>             → full Pod details (check Image:)
kubectl describe pod <name> | grep Image → quick image tag check

── UPDATE (imperative — learning only) ──
kubectl set image deployment.v1.apps/<deploy-name> <container-name>=<image:tag>

── ROLLBACK ──
kubectl rollout undo deployment/<name>                    → previous revision
kubectl rollout undo deployment/<name> --to-revision=<N>  → specific revision
kubectl rollout history deployment/<name>                 → list all revisions

── SCALE ──
kubectl scale deployment <name> --replicas=<N>

── DELETE ──
kubectl delete deploy <name>            → removes Deployment + RS + Pods
```

***

## Imperative vs. Declarative

```
IMPERATIVE (kubectl set image ...):
  ├── Quick for testing/learning
  ├── No audit trail in files
  └── NOT for production

DECLARATIVE (edit YAML → kubectl apply -f):
  ├── Versionable (Git)
  ├── Reviewable (code review)
  ├── Reproducible (apply anywhere)
  └── ALWAYS for production

"You should do everything through definition files.
 Imperative is for learning, testing purpose."
```

***

## ReplicaSet Accumulation Pattern

```
Initial deploy:     RS-1 (replicas: 3)
After update 1:     RS-1 (0), RS-2 (3)
After update 2:     RS-1 (0), RS-2 (0), RS-3 (3)
After rollback:     RS-1 (0), RS-2 (3), RS-3 (0)  ← reactivated RS-2

Each RS = a snapshot of a Deployment state
Old RS preserved at 0 replicas = instant rollback targets
History grows with each change → revision numbers track them
```

***

## Operational Flow

```
── CREATE ──
vim deployment.yaml → paste definition → :wq
kubectl apply -f deployment.yaml
kubectl get deploy → READY 3/3 ✓
kubectl get rs → one RS created ✓
kubectl get pod → three Pods ✓
kubectl describe pod <name> → Image: nginx:1.14.2 ✓

── UPDATE ──
kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.16.1
kubectl get deploy → update in progress/complete
kubectl get pod → new Pods (old ones deleted)
kubectl describe pod <new-name> → Image: nginx:1.16.1 ✓
kubectl get rs → TWO ReplicaSets (old=0, new=3)

── ROLLBACK ──
kubectl rollout undo deployment/nginx-deployment
kubectl get rs → old RS back to 3, new RS to 0
kubectl get pod → fresh Pods from old RS
kubectl describe pod <name> | grep Image → nginx:1.14.2 ✓
kubectl rollout history deployment/nginx-deployment → revision list

── CLEANUP ──
kubectl delete deploy nginx-deployment → all gone
```

***

## Key Gotchas

```
Container name ≠ Pod name:
  kubectl set image ... nginx=nginx:1.16.1
                        ↑ THIS is the CONTAINER name from spec.containers[].name

Old Pods are DELETED after update:
  Old Pod names no longer exist → use new Pod names for describe

kubectl get rs shows history:
  Multiple RS with different ages = visual proof of update history
  RS at 0 replicas = rollback targets, NOT garbage
```

***

## Reusable Engineering Patterns

| Pattern                                                 | Manifestation                                                   |
| ------------------------------------------------------- | --------------------------------------------------------------- |
| **Declarative state management**                        | Define desired state → controller reconciles actual state       |
| **Rolling update (zero-downtime)**                      | Replace Pods one-at-a-time → service stays available            |
| **Preserved history for rollback**                      | Old ReplicaSets kept at 0 replicas = instant rollback           |
| **Layered object hierarchy**                            | Deployment → ReplicaSet → Pod (each layer adds capability)      |
| **Delete-and-recreate (immutability)**                  | Pods are never modified in-place — always destroyed and rebuilt |
| **Revision tracking**                                   | Numbered revisions → jump to any historical state               |
| **Imperative for learning, declarative for production** | Two modes of interaction with clear usage boundaries            |

***

## Core Mental Model

```
Deployment = "Git for your running application"

Each apply = a commit (creates/reuses a ReplicaSet)
Each ReplicaSet = a snapshot of that state
rollout undo = git revert (go back to previous commit)
rollout undo --to-revision=N = git checkout <specific-commit>
rollout history = git log

The mechanism:
  You declare → Deployment Controller acts
  Update = new RS scales up, old RS scales down (rolling)
  Rollback = old RS scales up, current RS scales down
  Old RS never deleted = history always available

Pod changes = ALWAYS delete + recreate (never in-place edit)
  Controlled rate, one at a time, zero downtime
```

***

This material captures every concept, command, YAML structure, rolling update mechanism, rollback technique, and operational pattern from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
