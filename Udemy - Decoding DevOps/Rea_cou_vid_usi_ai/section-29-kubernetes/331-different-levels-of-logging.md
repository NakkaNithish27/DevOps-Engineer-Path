# 🎓 Kubernetes: Finding and Fixing Faulty Pods — Debugging & Diagnostic Workflow Deep Learning Material

**Source:** Video caption file — *Different Levels of Logging / Fix Faulty Pods* + Accompanying command reference file [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt), [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Reality: Mistakes Happen

The lecture begins with a candid operational truth: "We try to create or manage everything perfectly, but mistakes happen. And when it does, first thing you have to do is find out your mistake and second you fix it." This frames the entire lecture as a **debugging methodology** — not just specific fixes, but a **systematic approach** to diagnosing pod failures in Kubernetes. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

The instructor shares a personal best practice for minimizing mistakes: **test locally first**. "Whenever I'm working in any project, I will have a local environment set up. I test things in local environment, then in the test or dev environment, and then finally in production environment." This is the same **staged validation pattern** (local → dev → prod) seen throughout the course — from Bash scripting (test locally before remote deployment) to AWS (test before production) to Docker (test before push). [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

> ⚠️ **Expert Note:** The instructor adds an important caveat: "Just make sure it's allowed in your project to do a local setup." Some projects have restrictions on local environments due to data sensitivity, licensing, or compliance requirements.

***

## 1.2 — Pod Status Indicators: Reading the First Signal

When you run `kubectl get pod`, each pod shows a **STATUS** field. This status is the **first diagnostic signal** — it tells you the category of problem before you investigate further. The lecture demonstrates two specific failure statuses: [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

### `ImagePullBackOff` / `ErrImagePull`

This status means Kubernetes **could not pull the container image** from the registry. The most common causes:

* **Wrong image name** — A typo in the image name (e.g., `nginox` instead of `nginx`). This is exactly what the instructor demonstrates. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)
* **Private registry without credentials** — The image exists in a private registry but the pod doesn't have the authentication credentials to pull it. The instructor mentions: "If it's in a private registry and if you have not given your credentials, the same error may come. We will talk about how you can supply credentials for private registry in the secrets lecture." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)
* **Repository doesn't exist** — The image name points to a repository that doesn't exist on Docker Hub or the configured registry.

### `CrashLoopBackOff`

This status means the container **starts, runs, crashes, and Kubernetes keeps trying to restart it** — in a loop. Each restart attempt is counted (visible in the `RESTARTS` column). The instructor shows a pod that restarted 8 times. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

CrashLoopBackOff indicates that the **image was pulled successfully** (the image name is correct), but something inside the container is failing — a bad command, a missing configuration, a process that exits immediately, a startup script error. The problem is **inside the container's execution**, not in pulling the image.

> 🔍 **Deep Dive:** Kubernetes has a **back-off restart policy** for CrashLoopBackOff. It doesn't restart immediately every time — it waits with exponentially increasing delays (10s, 20s, 40s, etc., up to 5 minutes). This prevents a crashing container from consuming all system resources with rapid restart cycles. The "BackOff" in the name refers to this exponential back-off timer. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## 1.3 — The Diagnostic Drill-Down: Four Levels of Investigation

The lecture teaches a **progressive diagnostic methodology** — a systematic way to investigate pod failures, starting from the least detailed view and drilling down to the most detailed. The instructor explicitly models this: "I'm showing you how you can drill down to the problem." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

### Level 1: `kubectl get pod`

The basic listing. Shows pod name, status, restarts, and age. Gives you the **first signal** — which pod is failing and what category of failure it is (ImagePullBackOff vs. CrashLoopBackOff vs. Error, etc.).

### Level 2: `kubectl get pod -o wide`

Adds more columns: the node the pod is running on, the IP address, and the **image name**. This can sometimes immediately reveal the problem — for example, you might spot a typo in the image name directly. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

### Level 3: `kubectl get pod <name> -o yaml` (or `-o json`)

Outputs the **complete pod specification and status** in YAML or JSON format. This includes every detail Kubernetes knows about the pod: the image being pulled, the container status, the reason for failure, restart counts, conditions, and more. The instructor demonstrates catching the wrong image name (`ngnox`) by reading the YAML output: "Pulling image ngnox — I have given the wrong name there. So you see, we caught it here." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

### Level 4: `kubectl describe pod <name>`

The most detailed diagnostic view. Produces a human-readable report of the pod including **Events** at the bottom — a chronological log of everything that happened to the pod. The instructor emphasizes: "In the events, as I told you, in the events you can find out mistakes." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

Events show messages like:

* "Pulling image..."
* "Failed to pull image..."
* "Failed to resolve..."
* "Repository does not exist or may require authorization"
* "Back-off restarting failed container" [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

### Level 5: `kubectl logs <pod-name>` — The Last Resort

When `get`, `-o yaml`, and `describe` don't reveal the problem (especially for CrashLoopBackOff where the image is correct but the container crashes), **logs** is the final and most powerful diagnostic tool. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

The instructor explains what logs actually shows: "Pod is running a container and container will execute commands. Those commands could be a script, it could be a command that runs the process, like the NGINX process. So whatever process runs in the container, the output of that process you can see by using logs." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

Logs shows the **stdout/stderr output** of the container's main process. If the process crashes, the error message explaining why is typically in the logs. The instructor's CrashLoopBackOff case was caused by an erroneous extra argument (`test47`) passed to the container — the logs showed: "exec... test47... command not found." This immediately identified the root cause. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

The instructor's summary of the methodology: "Most of the time you will catch the problem somewhere here \[in these five levels]." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## 1.4 — The Two Failure Scenarios Demonstrated

### Scenario 1: Wrong Image Name (ImagePullBackOff)

A pod is created with `image: nginox:1.14.2` — a typo (`nginox` instead of `nginx`). Kubernetes tries to pull this image from Docker Hub, fails because the repository doesn't exist, and enters `ImagePullBackOff` state. [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

**Diagnosis path:** `get pod` (see ImagePullBackOff) → `-o wide` (didn't reveal it clearly) → `-o yaml` (saw "Pulling image ngnox") → `describe` (Events show "Failed to pull image... repository does not exist") → **Root cause found: typo in image name.** [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

**Fix:** Delete the pod, fix the image name in the YAML file, re-apply.

### Scenario 2: Bad Command Argument (CrashLoopBackOff)

A pod is created with `kubectl run web2 --image=nginx test47`. The `test47` at the end is interpreted as a **command to execute inside the container** — overriding the default Nginx startup command. Since `test47` is not a valid command, it fails immediately with "command not found," the container exits, Kubernetes restarts it, it fails again — CrashLoopBackOff. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt), [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

**Diagnosis path:** `get pod` (see CrashLoopBackOff, restarts: 8) → `-o wide` (image is correct) → `-o yaml` (just shows "back off... restarting failed container") → `describe` (Events show correct image pull, but container keeps failing) → **`logs`** (shows "exec: test47: command not found") → **Root cause found: invalid command argument.** [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

**Fix:** Delete the pod, re-run without the extra argument.

> 🔍 **Deep Dive:** When you run `kubectl run web2 --image=nginx test47`, the `test47` becomes the container's **command** (overriding the image's default `CMD`). In Kubernetes, the command specified after the image in `kubectl run` maps to the container's `command` field in the pod spec, which overrides the Docker image's `CMD` instruction. This is equivalent to `docker run nginx test47` — it replaces the default startup command with `test47`. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## 1.5 — Why We Don't Edit Pods Directly

The instructor preempts a natural question: "Now you will say, why don't we edit the pod?" The answer: **in production, you don't edit pods directly**. Pods are managed by higher-level controllers — **Deployments**, **DaemonSets**, **ReplicaSets**. You edit the Deployment, and the Deployment controller automatically deletes the old pod and creates a new one with the corrected specification. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

What was done manually in this lecture (delete pod → fix YAML → re-apply) is what Deployments do automatically when you update them. "Basically, it's going to delete and recreate — what we did manually." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

This is an *implicit concept* about Kubernetes architecture: pods are **ephemeral** and **replaceable**. The correct unit to manage is the controller (Deployment/DaemonSet), not the individual pod.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Doing

We're deliberately creating **two faulty pods** with different types of errors, then systematically diagnosing and fixing each one using the Kubernetes diagnostic drill-down methodology. The final outcome: all pods running successfully, and a mastered debugging workflow applicable to any future pod failure. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## Exercise 1: Wrong Image Name (ImagePullBackOff)

### Step 1: Create the Faulty Pod

Create a pod YAML file with an intentionally wrong image name:

```bash
vim pod2.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx12
spec:
  containers:
  - name: nginx
    image: nginox:1.14.2
    ports:
    - containerPort: 80
```

Note the typo: `nginox` instead of `nginx`. [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

Apply it:

```bash
kubectl apply -f pod2.yaml
```

***

### Step 2: Diagnose — Level 1 (`get pod`)

```bash
kubectl get pod
```

**Expected output:** `nginx12` shows status **`ImagePullBackOff`** (or `ErrImagePull`). [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

This tells you: the image could not be pulled. The problem is with the image reference.

***

### Step 3: Diagnose — Level 2 (`-o wide`)

```bash
kubectl get pod -o wide
```

Shows additional columns including the image name. In this case, the instructor notes: "Still we are not finding anything" — the wide output didn't immediately make the typo obvious. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

### Step 4: Diagnose — Level 3 (`-o yaml`)

```bash
kubectl get pod nginx12 -o yaml
```

In the output, look for the image pull status. You'll find: **"Pulling image nginox"** — the typo is now visible. "I have given the wrong name there. So you see, we caught it here." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

### Step 5: Diagnose — Level 4 (`describe`)

```bash
kubectl describe pod nginx12
```

Scroll to the **Events** section at the bottom. You'll see:

```
Failed to pull image "nginox:1.14.2"
Failed to resolve reference... repository does not exist or may require authorization
```

 [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

The Events section provides the clearest human-readable explanation of the failure.

***

### Step 6: Fix the Problem

Delete the faulty pod:

```bash
kubectl delete pod nginx12
```

Edit the YAML file and fix the image name:

```bash
vim pod2.yaml
```

Change `nginox` → `nginx`:

```yaml
image: nginx:1.14.2
```

Re-apply:

```bash
kubectl apply -f pod2.yaml
```

 [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

### Verify

```bash
kubectl get pod
```

**Expected:** `nginx12` status is now **`Running`**. ✅ [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## Exercise 2: Bad Command Argument (CrashLoopBackOff)

### Step 1: Create the Faulty Pod

```bash
kubectl run web2 --image=nginx test47
```

**Breakdown:**

* `kubectl run web2` — Create a pod named `web2`
* `--image=nginx` — Use the correct `nginx` image
* `test47` — This is interpreted as a **command to run inside the container**, overriding the default Nginx startup command [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt), [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

***

### Step 2: Diagnose — Level 1 (`get pod`)

```bash
kubectl get pod
```

**Expected:** `web2` shows status **`CrashLoopBackOff`** with increasing restart count (e.g., `RESTARTS: 8`). [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

This tells you: the container starts, crashes, and keeps restarting.

***

### Step 3: Diagnose — Level 2 (`-o wide`)

```bash
kubectl get pod web2 -o wide
```

Image shows `nginx` — correct. The problem is not the image name. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

### Step 4: Diagnose — Level 3 (`-o yaml`)

```bash
kubectl get pod web2 -o yaml
```

Shows "back off... restarting failed container" but **doesn't reveal the root cause**. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

### Step 5: Diagnose — Level 4 (`describe`)

```bash
kubectl describe pod web2
```

Events show the image was pulled successfully. Container keeps failing but Events don't explain why. **Still no root cause.** [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

### Step 6: Diagnose — Level 5 (`logs`) — The Last Resort

```bash
kubectl logs web2
```

**Output:** `exec: "test47": executable file not found` (or similar "command not found" message). [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

**Root cause identified:** The `test47` argument was interpreted as a command to execute inside the container. Since `test47` is not a valid executable, the container exits immediately with an error. Kubernetes restarts it, same error, restart again → CrashLoopBackOff.

***

### Step 7: Fix the Problem

Delete the faulty pod:

```bash
kubectl delete pod web2
```

Re-create without the extra argument:

```bash
kubectl run web2 --image=nginx
```

 [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

### Verify

```bash
kubectl get pod
```

**Expected:** `web2` status is now **`Running`**. ✅ [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## Summary of the Diagnostic Methodology

The instructor explicitly recaps the drill-down: "I first checked the status, there was an error. I tried to do wide, I describe, I can see it in `-o yaml` format, and still we don't catch anything. We look at the logs and trust me, most of the time you will catch the problem somewhere here." [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

### The Instructor's Recommendation

"Run this command, break things, break pods and fix them." Practice by deliberately creating errors and diagnosing them. The debugging skill is more important than the ability to create perfect pods. [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔍 The 5-Level Diagnostic Drill-Down

```
LEVEL 1: kubectl get pod
  └── STATUS field = first signal
      ├── ImagePullBackOff → image name/registry problem
      ├── CrashLoopBackOff → container starts then crashes
      ├── Running → healthy
      ├── Pending → scheduling issue
      └── RESTARTS column → how many restart attempts

LEVEL 2: kubectl get pod -o wide
  └── Shows: Node, IP, IMAGE NAME
      → Quick image name verification

LEVEL 3: kubectl get pod <name> -o yaml (or -o json)
  └── Complete pod spec + status in structured format
      → Image pull details, container state, conditions
      → "Pulling image nginox" → caught typo HERE

LEVEL 4: kubectl describe pod <name>
  └── Human-readable report + EVENTS (chronological log)
      → "Failed to pull image..."
      → "Repository does not exist or may require authorization"
      → Events = most readable diagnostic output

LEVEL 5: kubectl logs <name>   ◄── LAST RESORT, MOST POWERFUL
  └── stdout/stderr of the container's MAIN PROCESS
      → "exec: test47: command not found"
      → Shows WHY the process inside the container failed
      → USE WHEN: image pulled OK, but container keeps crashing
```

 [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## ⚡ Two Failure Scenarios

```
SCENARIO 1: ImagePullBackOff (wrong image name)
  CAUSE:    image: nginox:1.14.2  (typo: nginox ≠ nginx)
  STATUS:   ImagePullBackOff
  CAUGHT:   Level 3 (-o yaml) or Level 4 (describe → Events)
  FIX:      Delete pod → fix YAML → re-apply
  
  kubectl delete pod nginx12
  vim pod2.yaml → fix image name
  kubectl apply -f pod2.yaml

SCENARIO 2: CrashLoopBackOff (bad command argument)
  CAUSE:    kubectl run web2 --image=nginx test47
            → "test47" overrides default CMD → command not found
  STATUS:   CrashLoopBackOff (RESTARTS: 8)
  CAUGHT:   Level 5 (logs) ← only logs revealed the root cause
  FIX:      Delete pod → re-create without extra argument
  
  kubectl delete pod web2
  kubectl run web2 --image=nginx
```

 [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt), [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

***

## 📐 Status → Root Cause Mapping

```
STATUS                  LIKELY ROOT CAUSE                 PRIMARY DIAGNOSTIC TOOL
──────────────          ─────────────────                 ──────────────────────
ImagePullBackOff        Wrong image name                  describe (Events)
                        Private registry, no credentials  describe (Events)
                        Repository doesn't exist          describe (Events)

CrashLoopBackOff        Bad command/argument              logs
                        Missing config/env vars           logs
                        App startup failure               logs
                        Script error                      logs

Pending                 No available node / resources     describe (Events)
                        Scheduling constraints            describe (Events)

Error                   Container exited with error       logs
```

***

## 🔗 Pod Fix Strategy

```
IN THIS LECTURE (learning):
  Delete pod → Fix YAML/command → Re-create pod
  (Manual delete + recreate)

IN PRODUCTION (real):
  Edit the DEPLOYMENT (not the pod)
  → Deployment controller auto-deletes old pod
  → Deployment controller auto-creates new pod
  → "Basically it's going to delete and recreate — what we did manually"

RULE: Never edit pods directly in production
      Edit: Deployment / DaemonSet / ReplicaSet
      Pod = ephemeral, replaceable
```

 [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## 🛡️ Prevention Strategy

```
INSTRUCTOR'S PRACTICE:
  1. Local environment (test locally first)
  2. Dev/test environment (verify in shared env)
  3. Production environment (deploy with confidence)

  "Even though you took care of everything, still mistakes happen"
  → Prevention reduces mistakes, debugging handles the rest
```

 [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## ⚡ All Commands Used (Quick Reference)

```bash
# DIAGNOSE
kubectl get pod                        # Level 1: status overview
kubectl get pod -o wide                # Level 2: + node, IP, image
kubectl get pod <name> -o yaml         # Level 3: full spec + status
kubectl describe pod <name>            # Level 4: events + details
kubectl logs <name>                    # Level 5: container process output

# FIX (YAML-based pod)
kubectl delete pod <name>              # Remove faulty pod
vim pod2.yaml                          # Fix the YAML
kubectl apply -f pod2.yaml             # Re-create from fixed YAML

# FIX (imperative pod)
kubectl delete pod <name>              # Remove faulty pod
kubectl run <name> --image=<correct>   # Re-create with correct args
```

 [\[331.FixFaultyPod \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331.FixFaultyPod.txt)

***

## 🔄 `kubectl logs` — What It Actually Shows

```
POD
  └── Container
        └── Main Process (e.g., nginx, java, python script)
              └── stdout + stderr
                    └── kubectl logs <pod-name> SHOWS THIS

LOGS = output of the container's main process
       NOT Kubernetes events (that's describe)
       NOT pod spec (that's -o yaml)
       → The PROCESS output: startup messages, errors, crashes
```

 [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: PROGRESSIVE DIAGNOSTIC DRILL-DOWN
  Start broad (status) → narrow progressively → until root cause found
  Level 1 → 2 → 3 → 4 → 5
  → Same as: EC2 debugging (process → port → firewall → external)
    Network debugging (ping → traceroute → tcpdump)
    Application debugging (logs → stack trace → debugger)
  → PRINCIPLE: Each level adds detail. Stop when root cause found.

PATTERN 2: STATUS AS FAILURE CATEGORY INDICATOR
  ImagePullBackOff = image/registry problem (Level 3-4 catches it)
  CrashLoopBackOff = runtime/process problem (Level 5 catches it)
  → Status tells you WHERE to look, not WHAT happened
  → Same as: HTTP status codes (4xx = client, 5xx = server)

PATTERN 3: EPHEMERAL UNITS MANAGED BY CONTROLLERS
  Pod = ephemeral (delete + recreate, don't edit)
  Deployment = persistent controller (edit this instead)
  → Same as: Docker containers (don't fix, rebuild from image)
    EC2 instances in ASG (terminate, ASG replaces)
    MIG instances in GCP (delete, MIG recreates)
  → PRINCIPLE: Fix the TEMPLATE/CONTROLLER, not the INSTANCE

PATTERN 4: STAGED VALIDATION (Local → Dev → Prod)
  Test locally first → test in dev → deploy to prod
  → Same across entire course:
    Bash scripts (local → remote)
    Docker (build → test → push)
    Cloud infra (CLI one-at-a-time → verify → automate)
```

 [\[331-differ...of-logging \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/331-different-levels-of-logging.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → Kubernetes basics: creating pods (kubectl run, apply)
THIS      → DEBUGGING: 5-level diagnostic drill-down for faulty pods
NEXT      → Deployments, DaemonSets, ReplicaSets (controllers that manage pods)
            Secrets (for private registry credentials — mentioned in this lecture)

KEY INSIGHT:
  "Most of the time you will catch the problem somewhere here"
  (within the 5 diagnostic levels)
  
  "Run this command, break things, break pods and fix them."
  (Practice debugging > practice creating)
```

***

Your Kubernetes pod debugging deep learning material is fully reconstructed — covering the complete 5-level diagnostic drill-down, both failure scenarios (ImagePullBackOff and CrashLoopBackOff), the fix methodology, and the production principle of editing controllers instead of pods. Ready for the next lecture or **AnkiDeck flashcards (.csv)** across the series? 🃏
