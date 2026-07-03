# 🎓 Deep Learning Material: kubectl CLI Tips, Tricks, and Cheat Sheet — Efficient Kubernetes Operations and Manifest Generation

**Source:** Video lecture on kubectl CLI tricks and the official cheat sheet (from [340-kubectl-cli-and-cheatsheet.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt?EntityRepresentationId=e537605b-91ae-4835-94ab-4487272fe9c1) caption file) [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**Video Context:** This lecture is a **tooling and efficiency** lecture — the instructor walks through the official Kubernetes kubectl cheat sheet, demonstrating key commands and revealing a critically important workflow trick: using `--dry-run=client -o yaml` to **auto-generate YAML manifest files** from imperative commands. This eliminates the need to write manifests from scratch or copy them from documentation. The lecture also covers kubeconfig management for multi-cluster environments, resource patching, node maintenance operations (cordon/drain/uncordon), multi-container log access, and many other operational commands. The instructor repeatedly emphasizes that these commands shouldn't be memorized but practiced until they become automatic — and that the cheat sheet itself is the reference document for daily work.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Cheat Sheet Philosophy: Practice Over Memorization

The instructor opens with a practical reality: *"no matter how many tips and tricks we have, it's difficult to remember all of them. So Kubernetes has created an amazing document for that, cheat sheet."* The official kubectl cheat sheet (searchable as "kubectl cheat sheet") is a curated collection of regularly used commands for daily Kubernetes operations. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

The instructor's advice on using it: *"do not by-heart. This is already available. But if you keep running this regularly it will be automatically by-hearted."* This reflects the practical reality of DevOps tooling — fluency comes from repetition in real environments, not from studying command lists. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

***

## 1.2 — The Dry-Run Trick: Auto-Generating Manifests from Imperative Commands

This is the **most important concept** in the lecture — a workflow that bridges the imperative and declarative worlds. The instructor has established in earlier lectures that production Kubernetes should always use **declarative** manifests (YAML files). But writing manifests from scratch is tedious and error-prone. The solution: use an imperative command with `--dry-run=client -o yaml` to **generate the manifest without actually creating the resource**, then redirect the output to a file. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**For a Pod:**

```bash
kubectl run nginx-pod --image=nginx --dry-run=client -o yaml > ng-pod.yaml
```

**For a Deployment:**

```bash
kubectl create deployment ngdep --image=nginx --dry-run=client -o yaml > ngdep.yaml
```

The `--dry-run=client` flag tells kubectl: *"just show me how you're going to do, but don't do it."* The `-o yaml` flag formats the output as a YAML manifest. The `>` redirects that YAML to a file instead of the screen. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

The result is a **complete, valid manifest file** that you can then open, edit (add ports, volumes, remove unnecessary fields like `creationTimestamp`, `dnsPolicy`, `restartPolicy`, `status`, `resources`), and apply declaratively with `kubectl apply -f`. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

The instructor highlights the exam value: *"This is very helpful in Kubernetes exams, the certification exam where the time is very critical. You get documentation in the exam, but going there, copying pasting just avoids that time."* [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**Key distinction:** `kubectl run` generates **Pod** manifests. `kubectl create deployment` generates **Deployment** manifests. The `run` command is exclusively for pods; everything else uses `create`. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

***

## 1.3 — kubeconfig: Managing Multiple Clusters from One File

`kubectl config view` displays the kubeconfig file contents (hiding certificates for security). The kubeconfig file can contain **multiple contexts** — each context is a combination of a cluster, a user, and a namespace. When managing multiple Kubernetes clusters, you can have one kubeconfig file with information about all clusters and switch between them using contexts. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

Key commands: [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

* `kubectl config get-contexts` — list all available contexts
* `kubectl config current-context` — show which context is active
* `kubectl config use-context <name>` — switch to a different context

The instructor also demonstrates JSON path querying: `kubectl config view -o jsonpath='{.users[0].name}'` — this navigates the kubeconfig's JSON structure to extract specific values. The syntax is: `.users` (the users key) → `[0]` (first item in the list) → `.name` (the name field). [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

***

## 1.4 — kubectl apply with Multiple Sources

The `kubectl apply` command is more versatile than just single files: [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

* **Single file:** `kubectl apply -f manifest.yaml`
* **Multiple files:** `kubectl apply -f file1.yaml -f file2.yaml`
* **Entire directory:** `kubectl apply -f /path/to/dir/` — applies all manifests in the directory
* **URL:** `kubectl apply -f <url>` — applies a manifest hosted at a remote URL

This enables patterns like keeping all manifests for a project in one directory and applying them in a single command. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

***

## 1.5 — Node Maintenance Operations: Cordon, Drain, Uncordon

These three commands form the **node maintenance lifecycle** — used when a worker node needs to be taken down for updates, patches, or hardware maintenance: [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**`kubectl cordon <node>`** — Makes the node **unschedulable**. No new pods will be placed on this node. Existing pods continue running. *"Cordon basically means make this node unschedulable so no new pod will be running on this node."* [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**`kubectl drain <node>`** — Removes **all workload** from the node. Pods are evicted and rescheduled on other healthy worker nodes. This is the actual evacuation step. *"Then you drain it. So you remove all the workload from that, which migrates to healthy worker nodes."* [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**`kubectl uncordon <node>`** — Marks the node as **schedulable** again after maintenance. New pods can be placed on it. The instructor clarifies an important nuance: *"Uncordon doesn't really mean that it's going to bring back your previous workload. It is just going to open up to take the new workload."* The previously evicted pods don't automatically return — they stay wherever they were rescheduled. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

The operational sequence is always: **cordon → drain → \[perform maintenance] → uncordon**. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

***

## 1.6 — Multi-Container Pod Logging

When a pod has **multiple containers**, you need to specify which container's logs you want. The `-c` flag targets a specific container: [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

```bash
kubectl logs <pod-name> -c <container-name>
```

Without `-c`, kubectl shows logs from the default (first) container. With multiple containers, you must be explicit. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

***

## 1.7 — Interactive Pod Access

Two methods for getting a shell inside a running container: [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**Run and login immediately:**

```bash
kubectl run -i --tty <name> --image=<image> -- /bin/bash
```

Creates a new pod and opens an interactive shell inside it. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

**Exec into an existing pod:**

```bash
kubectl exec --stdin --tty <pod-name> -- /bin/bash
```

Opens a shell in an already-running pod. [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

***

## 1.8 — Other Operational Commands (From the Cheat Sheet)

The instructor walks through several categories of commands from the cheat sheet: [\[340-kubect...cheatsheet \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/340-kubectl-cli-and-cheatsheet.txt)

* **Updating resources:** `kubectl set image` (change container image in a deployment), `kubectl rollout` (history, undo, restart)
* **Exposing services:** `kubectl expose` (create a service imperatively)
* **Labels:** `kubectl label` (add/modify labels on resources)
* **Patching:** `kubectl patch` — change specific values in a resource using JSON patches. The instructor advises: *"try avoid this in productions in real time. Always go through definitions manifest."*
* **Scaling:** `kubectl scale` (scale in/out deployments)
* **Deleting:** `kubectl delete -f <file>` (delete everything defined in a manifest), delete by label
* **Port forwarding:** `kubectl port-forward` (access a pod or service without creating a full service)
* **Explaining resources:** `kubectl explain pods` (show the API spec for a resource type)
* **Copying files:** `kubectl cp` (copy files to/from containers)
* **Wide output:** `kubectl get pods -o wide` (shows additional columns like node name and IP) <cite>turn27search9</cite>

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are learning **kubectl efficiency techniques** — specifically the dry-run manifest generation trick, kubeconfig management, and the node maintenance workflow. The final outcome: the ability to quickly generate YAML manifests without writing them from scratch, manage multi-cluster environments, and perform safe node maintenance operations. These skills dramatically increase operational speed in daily Kubernetes work.

***

## Step 1: View kubeconfig

```bash
kubectl config view
```

Shows the kubeconfig file contents. Certificates are hidden (replaced with `DATA+OMITTED`). You can see clusters, users, and contexts. <cite>turn27search9</cite>

***

## Step 2: Generate a Pod Manifest (Dry-Run Trick)

**This is the most valuable practical skill in the lecture.**

```bash
kubectl run nginx-pod --image=nginx --dry-run=client -o yaml > ng-pod.yaml
```

* `run nginx-pod` — would create a pod named `nginx-pod`
* `--image=nginx` — using the nginx container image
* `--dry-run=client` — **don't actually create it** — just simulate and show the output
* `-o yaml` — format the output as YAML
* `> ng-pod.yaml` — redirect to a file instead of printing to screen <cite>turn27search9</cite>

**Verify the generated file:**

```bash
cat ng-pod.yaml
```

**Expected:** A complete Pod definition YAML file with all default fields populated. <cite>turn27search9</cite>

**Edit to clean up unnecessary fields:**

```bash
vim ng-pod.yaml
```

**Remove these auto-generated fields** (not needed for basic use): <cite>turn27search9</cite>

* `creationTimestamp`
* `dnsPolicy`
* `restartPolicy`
* `status`
* `resources`

**Add what you need:**

* Port numbers
* Volume mounts
* Environment variables
* Any other customization <cite>turn27search9</cite>

**Apply the manifest:**

```bash
kubectl apply -f ng-pod.yaml
```

<cite>turn27search9</cite>

**Connection to system flow:** You now have a declarative manifest created in seconds, without visiting the documentation or writing YAML from scratch.

***

## Step 3: Generate a Deployment Manifest (Dry-Run Trick)

```bash
kubectl create deployment ngdep --image=nginx --dry-run=client -o yaml > ngdep.yaml
```

* `create deployment ngdep` — would create a deployment named `ngdep`
* `--image=nginx` — container image
* `--dry-run=client -o yaml > ngdep.yaml` — same trick: generate, don't execute, save to file <cite>turn27search9</cite>

**Key distinction:** `run` = Pod only. `create deployment` = Deployment (which manages ReplicaSets which manage Pods). <cite>turn27search9</cite>

**Verify:**

```bash
cat ngdep.yaml
```

**Expected:** A Deployment definition with spec.template (pod template), spec.replicas, spec.selector, etc. <cite>turn27search9</cite>

Edit, customize, and apply as needed.

***

## Step 4: Node Maintenance Workflow

**Step 4a — Cordon (prevent new scheduling):**

```bash
kubectl cordon <node-name>
```

Existing pods keep running. No new pods get scheduled here. <cite>turn27search9</cite>

**Step 4b — Drain (evacuate all workload):**

```bash
kubectl drain <node-name>
```

All pods are evicted and rescheduled on other nodes. <cite>turn27search9</cite>

**Step 4c — \[Perform maintenance]** (OS patches, hardware work, etc.)

**Step 4d — Uncordon (reopen for scheduling):**

```bash
kubectl uncordon <node-name>
```

Node accepts new pod scheduling again. **Previous pods do NOT return automatically.** <cite>turn27search9</cite>

***

## Step 5: Multi-Container Logs

```bash
kubectl logs <pod-name> -c <container-name>
```

* `-c <container-name>` — targets a specific container within a multi-container pod <cite>turn27search9</cite>

Without `-c`: logs from the default (first) container.

***

## Step 6: Interactive Shell Access

**Into an existing pod:**

```bash
kubectl exec --stdin --tty <pod-name> -- /bin/bash
```

<cite>turn27search9</cite>

**Create and immediately enter a new pod:**

```bash
kubectl run -i --tty debug-pod --image=nginx -- /bin/bash
```

<cite>turn27search9</cite>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Trick (Highest Value in This Lecture)

```bash
# GENERATE POD MANIFEST:
kubectl run <name> --image=<img> --dry-run=client -o yaml > pod.yaml

# GENERATE DEPLOYMENT MANIFEST:
kubectl create deployment <name> --image=<img> --dry-run=client -o yaml > dep.yaml

WORKFLOW:
  1. Generate with --dry-run=client -o yaml > file.yaml
  2. vim file.yaml → remove junk fields, add customizations
  3. kubectl apply -f file.yaml

FIELDS TO REMOVE: creationTimestamp, dnsPolicy, restartPolicy, status, resources
FIELDS TO ADD:    ports, volumes, env, replicas, labels, namespace

"run" = Pod only
"create deployment" = Deployment
```

***

## 🔷 kubeconfig Commands

```bash
kubectl config view                    # show kubeconfig (certs hidden)
kubectl config get-contexts            # list all contexts
kubectl config current-context         # which context is active
kubectl config use-context <name>      # switch context

CONTEXT = cluster + user + namespace
MULTI-CLUSTER: one kubeconfig → multiple contexts → switch with use-context

JSON PATH:
  kubectl config view -o jsonpath='{.users[0].name}'
  .users = key → [0] = first item → .name = field
```

***

## 🔷 kubectl apply Sources

```bash
kubectl apply -f file.yaml              # single file
kubectl apply -f file1.yaml -f file2.yaml  # multiple files
kubectl apply -f /path/to/dir/          # all files in directory
kubectl apply -f <url>                  # remote manifest
```

***

## 🔷 Node Maintenance Lifecycle

```
CORDON → DRAIN → [MAINTENANCE] → UNCORDON

kubectl cordon <node>     # mark unschedulable (existing pods stay)
kubectl drain <node>      # evict all pods (reschedule elsewhere)
[perform maintenance]
kubectl uncordon <node>   # mark schedulable again

⚠️ uncordon ≠ restore previous pods
   uncordon = accept NEW pods only
   old pods stay where they were rescheduled
```

***

## 🔷 Command Categories (Cheat Sheet Map)

```
CATEGORY              KEY COMMANDS
──────────            ──────────────────────────────────────
Config                config view, get-contexts, use-context
Create (imperative)   run (pod), create deployment/job/service
Apply (declarative)   apply -f file/dir/url
Get info              get pods -o wide, describe, explain, logs
Update                set image, rollout restart/undo/history
Scale                 scale deployment --replicas=N
Labels                label pod <name> key=value
Patch                 patch deployment (JSON format)
Delete                delete -f file, delete by label, delete ns
Interact              exec --stdin --tty, run -i --tty, cp, port-forward
Logs                  logs <pod>, logs <pod> -c <container>
Node admin            cordon, drain, uncordon
```

***

## 🔷 Multi-Container Logs

```bash
kubectl logs <pod>                    # default container
kubectl logs <pod> -c <container>     # specific container

USE CASE: sidecar patterns, init containers, multi-container pods
```

***

## 🔷 Interactive Access

```bash
# Exec into EXISTING pod:
kubectl exec --stdin --tty <pod> -- /bin/bash

# Create NEW pod and login:
kubectl run -i --tty <name> --image=<img> -- /bin/bash
```

***

## 🔷 Imperative vs. Declarative Bridge

```
IMPERATIVE (quick, ad-hoc):
  kubectl run nginx --image=nginx
  kubectl create deployment dep --image=nginx
  → Creates resource immediately
  → No file, no version control, no reproducibility

DECLARATIVE (production, repeatable):
  kubectl apply -f manifest.yaml
  → File-based, version-controlled, auditable

BRIDGE (this lecture's key trick):
  kubectl run nginx --image=nginx --dry-run=client -o yaml > file.yaml
  → Imperative command GENERATES declarative manifest
  → Best of both worlds: speed + reproducibility
```

***

## 🔷 Patching (Use with Caution)

```bash
kubectl patch deployment <name> --type json -p '[{"op":"replace","path":"/spec/...","value":"..."}]'

"Try avoid this in productions in real time.
 Always go through definitions manifest."

USE: emergency fixes, quick tests
AVOID: production changes (use manifests instead)
```

***

## 🔷 Delete Patterns

```bash
kubectl delete -f manifest.yaml         # delete everything in the manifest
kubectl delete pod,svc -l key=value     # delete by label
kubectl delete ns <namespace>           # delete namespace + ALL contents
```

***

## 🔷 Reusable Engineering Pattern: Scaffold → Customize → Apply

```
PATTERN: Auto-Generate Template → Edit → Deploy

KUBERNETES:
  kubectl run/create --dry-run=client -o yaml > file.yaml
  vim file.yaml (customize)
  kubectl apply -f file.yaml

SAME PATTERN IN:
  Terraform:    terraform plan → review → terraform apply
  Ansible:      ansible-galaxy init role → edit → ansible-playbook
  Docker:       docker init → edit Dockerfile → docker build
  Helm:         helm create chart → edit templates → helm install
  Spring Boot:  spring init → edit code → mvn package

PRINCIPLE:
  Never write boilerplate from scratch.
  Let the tool generate the skeleton.
  You provide the customization.
  Apply the result declaratively.

"This is very helpful in Kubernetes exams...
 and also regular operation."
```

This is the lecture's central efficiency insight: the `--dry-run=client -o yaml` pattern converts any imperative kubectl command into a declarative manifest generator. It eliminates the two slowest parts of Kubernetes work — looking up manifest syntax in documentation and writing YAML from scratch. Master this one pattern and every Kubernetes resource creation becomes: generate → edit → apply. <cite>turn27search9</cite>
