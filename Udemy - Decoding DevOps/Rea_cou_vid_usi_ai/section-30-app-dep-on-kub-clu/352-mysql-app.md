# ☸️ Kubernetes MySQL Deployment — Deployment Definition, Secret Integration, PVC Volume Mounting, and Init Containers

**Source:** Kubernetes Section — MySQL App Deployment (Caption File) [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

This is a **hands-on Kubernetes definition writing lecture** where the instructor builds a complete MySQL Deployment manifest from scratch. The lecture covers why Deployments are used instead of bare Pods, how to inject secrets as environment variables (preventing accidental password exposure), how to connect a Persistent Volume Claim (PVC) to the MySQL data directory, and — most critically — how to solve the **EBS lost+found problem** using an **init container** that cleans the volume before MySQL starts. This is one of the most operationally rich lectures in the Kubernetes section, combining multiple K8s concepts into a single real-world definition file. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. Why Deployment, Not Pod — The Recurring Principle

The instructor opens by addressing a pattern he's been using throughout the section: **"I'm again and again saying pod, DB pod, Tomcat pod... but we are not actually going to write the pod definition file. We need deployment definition."** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

The reasons are the same as established in the Deployment lecture:

* **Self-healing:** If the DB pod fails, the Deployment controller **recreates it automatically**.
* **Rolling updates:** When you need a newer version of the container image, you update the Deployment's image tag, and it **replaces the old container with a new one** — deleting the old, creating the new.

The instructor reinforces: **"If the DB pod fails or whatever pod is managing, if it fails, it's going to recreate that. You want to update a newer version of your image... deployment will replace it."** This is why, in practice, you almost never write bare Pod definitions — Deployments wrap pods with lifecycle management. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## 2. Replica Count for Databases — A Conceptual Boundary

When setting `replicas`, the instructor explicitly states: **"We just need one single — we cannot have replica for database. That's a whole different concept that can be managed by StatefulSet."** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

This is an important architectural insight. Databases cannot be simply replicated by increasing the Deployment replica count because multiple database instances writing to the same data create **data conflicts and corruption**. Database replication requires special coordination — leader/follower relationships, replication protocols, consensus mechanisms — which is what **StatefulSets** handle in Kubernetes. A Deployment with `replicas: 1` is appropriate for a single database instance; scaling databases is a separate, more complex topic. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## 3. Labels — The Glue Between Deployment, Pod, and Service

The instructor sets the same label (`app: vprodb`) in three places within the Deployment definition, and explains why each matters: [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

1. **Deployment metadata labels** — Identifies the Deployment object itself.
2. **Selector matchLabels** — Tells the Deployment which pods it manages: **"Any pod that has this label is going to be part of this deployment definition."**
3. **Pod template labels** — Labels applied to the pods that the Deployment creates.

The connection to Services (from the previous lecture): **"When we create the service for DB, we're going to say find a pod that has so and so label... label is going to connect that service to this pod."** Labels are the universal binding mechanism in Kubernetes — they connect Services to Pods and Deployments to Pods through label selectors. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## 4. Secret Injection via Environment Variables — Preventing Accidental Exposure

The MySQL container requires a `MYSQL_ROOT_PASSWORD` environment variable to start. In the Docker Compose lecture (containerization section), this was set as a plain text value directly in the compose file. In Kubernetes, the instructor uses a **Secret** object instead. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

The mechanism: instead of `value: "mypassword"` in the environment variable definition, you use `valueFrom: secretKeyRef:` — which tells Kubernetes to **fetch the value from a Secret object**. The Secret was created in a previous lecture with the name `app-secret` containing a key `db-pass`. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**How it works internally:** Kubernetes takes the encoded value from the Secret, **decodes it**, and injects it into the container as an environment variable. The instructor explains: **"It's going to take its value, which is encoded, decoded, and then inject it into this container."** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**Why this matters:** **"If someone sees this deployment definition file, they won't be able to see the password. So that's the idea. Preventing accidental exposure."** The Deployment YAML file can be committed to Git, shared with team members, or stored in a repository — and the password is never visible in it. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**The instructor's security caveat:** Base64 encoding in Kubernetes Secrets is **not encryption** — it's just encoding. The instructor explicitly warns: **"That is the only way, only reason that you should use encoding and decoding. Otherwise you should do encryption by using keys. In AWS you can use AWS KMS keys."** For real security, Secrets should be encrypted at rest (using KMS or similar) and access should be controlled via RBAC. Base64 encoding prevents *accidental* exposure, not *deliberate* access. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## 5. Persistent Volume Claim (PVC) Mounting — Connecting Storage to the Pod

The MySQL container needs persistent storage at `/var/lib/mysql` — this is where MySQL stores all its database files. Without persistent storage, if the pod restarts, all database data is lost (the container's filesystem is ephemeral). [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

The PVC (`db-pv-claim`) was created in a previous lecture with 3 GB of storage. Connecting it to the pod requires **two steps** in the Deployment definition: [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**Step 1 — Define the volume** (at the pod level, under `volumes:`): Create a named volume that references the PVC. This makes the PVC's storage available to the pod as a named volume.

**Step 2 — Mount the volume** (at the container level, under `volumeMounts:`): Mount the named volume to a specific directory path inside the container (`/var/lib/mysql`).

The instructor explains the flow: **"This PVC... is going to create 3 GB of volume for us... it runs the container, in our case MySQL service, and it has a folder /var/lib/mysql that it'll connect it with this volume, which basically is the PVC. It gives it 3 GB of volume. So this 3 GB of volume gets connected to /var/lib/mysql."** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

The two-step process (define volume → mount volume) is the same pattern from the EBS lecture — you can't use a disk until it's both recognized (defined) and mounted to a directory.

***

## 6. The EBS Lost+Found Problem — Why Init Containers Are Needed

This is the **most operationally valuable concept** in the entire lecture. The instructor identifies a **known issue** specific to EBS-backed persistent volumes: [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**The problem:** When Kubernetes provisions an EBS volume and formats it, the Linux filesystem creates a directory called `lost+found` in the root of the volume. This is standard Linux behavior — every newly formatted ext filesystem partition gets a `lost+found` directory (as covered in the EBS lecture earlier in the course).

When this volume is mounted to `/var/lib/mysql`, the MySQL service expects that directory to be **completely empty** on first startup. But it's not empty — it contains the `lost+found` folder. MySQL detects this existing data and **refuses to start**: **"The MySQL service will say there is already some data in that. So it's not going to start the service."** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**The solution: Init Containers.** An init container is a container that runs **before the main container** in the same pod. It executes a task, completes, and then terminates. Only after all init containers complete successfully does the main container start. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

The instructor creates an init container using the **BusyBox** image (described as **"a very basic Linux image"**) that:

1. Mounts the same PVC volume.
2. Runs `rm -rf /var/lib/mysql/lost+found` to remove the problematic directory.
3. Terminates (the container dies after executing the command).

Then the main MySQL container starts, mounts the now-clean volume, and initializes successfully. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**The execution flow:** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

1. Pod starts → init container (BusyBox) runs first.
2. Init container mounts the EBS volume → deletes `lost+found` → dies.
3. Main container (MySQL) starts → mounts the same volume → `/var/lib/mysql` is empty → MySQL initializes successfully.

The instructor notes that the mount path in the init container doesn't technically need to be `/var/lib/mysql` — it can be any path, because the goal is just to remove the `lost+found` directory from the volume. But he uses the same path for clarity: **"Make sure the mount path and this path is same here."** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

<details>
<summary>🔍 Deep Dive</summary>

Init containers are a general-purpose Kubernetes mechanism, not specific to the lost+found problem. They can be used for any pre-startup task: waiting for a dependency service to be ready, downloading configuration files, running database migrations, populating a shared volume with data, or performing security checks. The pattern is: **run a task before the main application starts, using a separate container image that has the tools needed for that task.** The main container image stays clean (no extra tools), and the init container is disposable (runs once and dies).

</details>

***

## 7. Command Syntax in Container Definitions

The instructor shows how to run a command inside a container using the `args` field with a **list format**: [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

```yaml
args: ["rm", "-rf", "/var/lib/mysql/lost+found"]
```

The instructor compares this to a **Python list**: **"Same like Python list... make sure everything is in the double code and separated by comma."** Each element of the command is a separate string in the list — the command (`rm`), the flags (`-rf`), and the path — all separated, all quoted. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## 8. Using Pre-Built vs Custom Images

The instructor uses the image `vprocontainer/vprofiledb` — a custom image built during the containerization lecture. He gives learners the choice: **"You can use the same image or if you have built your own image... give your image, that will be better. If you don't want to take any risk, you can give my image — that's a public image, it'll fetch it and run it."** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

He also notes that the complete definition files are available in the **kube-app folder** for those who don't want to write them from scratch: **"If you don't intend to write all this definition file, you can just copy it from the kube app folder. Just make sure you understand all the options that we are using here."** Understanding is prioritized over typing. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are writing a complete **Kubernetes Deployment definition** for the MySQL database pod of the Vprofile application. This single YAML file integrates four Kubernetes concepts: Deployment (pod management), Secret (password injection), PVC (persistent storage), and Init Container (volume preparation). [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**Why it matters:** This is the pattern for deploying any stateful service on Kubernetes — database, message queue, cache — anything that needs persistent storage and sensitive credentials.

**Final outcome:** A Deployment definition file that, when applied with `kubectl create`, launches a MySQL pod that: pulls its password from a Secret, stores data on a persistent EBS volume, and uses an init container to clean the volume before MySQL starts.

***

## Step 1: Start with a Deployment Skeleton

**What we are doing:** Getting a basic Deployment YAML template to work from. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

The instructor searches for **"Kubernetes deployment YAML"** and copies a skeleton template. You can get this from:

* Kubernetes documentation
* Any generative AI (ChatGPT, Copilot)
* Previous lecture examples

Paste the skeleton into your editor and modify it.

**Connection to flow:** Skeleton provides the structure; we'll fill in MySQL-specific details.

***

## Step 2: Set Metadata, Labels, and Replica

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vprodb
  labels:
    app: vprodb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vprodb
  template:
    metadata:
      labels:
        app: vprodb
```

**Key decisions:** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

* **Name:** `vprodb` — identifies this as the Vprofile database Deployment.
* **Labels:** `app: vprodb` — set consistently in metadata, selector, and pod template. The upcoming Service will use this label to find the pod.
* **Replicas:** `1` — databases cannot be horizontally scaled via Deployment replicas (requires StatefulSet).

**Common mistake:** Using different labels in the selector vs the pod template → Deployment creates pods but can't manage them.

***

## Step 3: Define the Container with Image and Ports

```yaml
    spec:
      containers:
        - name: vprodb
          image: vprocontainer/vprofiledb
          ports:
            - name: vprodb-port
              containerPort: 3306
```

* `name: vprodb` — Container name. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)
* `image: vprocontainer/vprofiledb` — The custom MySQL image built in the containerization lecture. Use your own image if you built one, or use the instructor's public image.
* `containerPort: 3306` — MySQL's standard port.
* `name: vprodb-port` — Named port. The Service can reference this name instead of the port number (as covered in the Service lecture).

**Connection to flow:** Container defined. Now inject the password.

***

## Step 4: Inject MySQL Root Password from Secret

```yaml
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secret
                  key: db-pass
```

* `env:` — At the same indentation level as `ports:`. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)
* `name: MYSQL_ROOT_PASSWORD` — The environment variable MySQL requires to start.
* `valueFrom: secretKeyRef:` — Instead of a plain text `value:`, fetch from a Secret.
* `name: app-secret` — The Secret object's name (created in a previous lecture).
* `key: db-pass` — The specific key within the Secret that holds the password.

**What happens internally:** Kubernetes reads the Secret `app-secret`, finds the key `db-pass`, decodes the base64 value, and injects the decoded password as the `MYSQL_ROOT_PASSWORD` environment variable inside the container. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

**Verification:** After the pod is running, you can exec into it and echo the environment variable to confirm the password was injected correctly.

**Common mistake:** Wrong Secret name or wrong key name → Kubernetes can't find the value → pod fails to start with a `CreateContainerConfigError`.

**Security reminder:** Base64 encoding is NOT encryption. Use AWS KMS or similar for real encryption. Secrets prevent *accidental* exposure only. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## Step 5: Define the Volume from PVC

```yaml
      volumes:
        - name: vprodb-data
          persistentVolumeClaim:
            claimName: db-pv-claim
```

* `volumes:` — At the same indentation level as `containers:` (both under pod `spec:`). [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)
* `name: vprodb-data` — An arbitrary name for this volume within the pod. Used to reference it in `volumeMounts`.
* `claimName: db-pv-claim` — The name of the PVC created in a previous lecture (3 GB EBS volume).

**What happens internally:** Kubernetes provisions an EBS volume matching the PVC's requirements (3 GB, GP2/GP3), attaches it to the node where the pod is scheduled, and makes it available as the named volume `vprodb-data`.

**Connection to flow:** Volume defined. Now mount it to the container.

***

## Step 6: Mount the Volume to `/var/lib/mysql`

```yaml
          volumeMounts:
            - mountPath: /var/lib/mysql
              name: vprodb-data
```

* `volumeMounts:` — Under the container spec, at the same level as `image:`. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)
* `mountPath: /var/lib/mysql` — The directory inside the container where MySQL stores its data.
* `name: vprodb-data` — References the volume defined in Step 5.

**What happens internally:** The 3 GB EBS volume is mounted to `/var/lib/mysql` inside the container. All database files MySQL writes go to this persistent volume — surviving pod restarts, rescheduling, and upgrades.

**Connection to flow:** Volume mounted. But there's a problem — the lost+found directory. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## Step 7: Create the Init Container to Remove lost+found

```yaml
      initContainers:
        - name: busybox
          image: busybox:latest
          volumeMounts:
            - mountPath: /var/lib/mysql
              name: vprodb-data
          args: ["rm", "-rf", "/var/lib/mysql/lost+found"]
```

* `initContainers:` — At the same indentation level as `containers:` and `volumes:` (all under pod `spec:`). [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)
* `name: busybox` — Name of the init container.
* `image: busybox:latest` — A minimal Linux image. Only needs to run `rm`.
* `volumeMounts:` — Mounts the **same PVC volume** (`vprodb-data`) to `/var/lib/mysql`.
* `args: ["rm", "-rf", "/var/lib/mysql/lost+found"]` — The command to execute. Each element is a separate string in a list.

**Execution flow:** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

1. Pod starts → init container (BusyBox) starts first.
2. BusyBox mounts the EBS volume → runs `rm -rf /var/lib/mysql/lost+found`.
3. BusyBox command completes → init container terminates (dies).
4. Main container (MySQL) starts → mounts the same volume → `/var/lib/mysql` is empty → MySQL initializes successfully.

**Common mistakes:**

* Forgetting the init container → MySQL fails to start with "directory not empty" error.
* Mount path in init container doesn't match the `rm` command path → `lost+found` not removed.
* Wrong volume name in init container → mounts a different (or no) volume.

**Connection to flow:** Init container ensures clean volume. MySQL starts successfully. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

***

## Step 8: Save and Verify the Complete File

Save the file. The instructor notes that the complete definition files are available in the **kube-app folder** in the course resources.

**Before creating the Deployment, ensure prerequisites exist:** [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

* Secret `app-secret` with key `db-pass` (created in previous lecture).
* PVC `db-pv-claim` with 3 GB (created in previous lecture).

**Next lecture:** Create a **ClusterIP Service** for this MySQL Deployment so other pods (Tomcat) can connect to it internally.

<details>
<summary>⚠️ Expert Note</summary>

The lost+found issue is specific to EBS-backed volumes with ext3/ext4 filesystems. If you use a different storage class (e.g., NFS, GlusterFS) or a different filesystem (XFS), this issue may not occur. However, the init container pattern is still valuable as a general-purpose pre-startup mechanism — it's worth including even if you're unsure whether your storage backend creates lost+found, as the `rm -rf` on a non-existent directory simply does nothing (no harm).

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   Kubernetes MySQL Deployment — Complete Definition File
CONTEXT: Kubernetes section → Vprofile app → database pod deployment
PURPOSE: Build a Deployment integrating Secret + PVC + Init Container
```

***

## Why Deployment, Not Pod

```
Pods are mortal → no self-healing, no rolling updates
Deployment wraps pod → recreates on failure + replaces on image upgrade

DB replicas: 1 (NOT scalable via Deployment → use StatefulSet for DB replication)
```

***

## Complete Definition File Structure

```yaml
Deployment (vprodb)
├── metadata: labels: app: vprodb
├── spec:
│   ├── replicas: 1
│   ├── selector: matchLabels: app: vprodb
│   └── template (Pod):
│       ├── metadata: labels: app: vprodb
│       └── spec:
│           ├── initContainers:           ← runs BEFORE main container
│           │   └── busybox → rm lost+found
│           ├── containers:
│           │   └── vprodb (MySQL)
│           │       ├── image: vprocontainer/vprofiledb
│           │       ├── ports: 3306 (name: vprodb-port)
│           │       ├── env: MYSQL_ROOT_PASSWORD ← from Secret
│           │       └── volumeMounts: /var/lib/mysql ← from PVC
│           └── volumes:
│               └── vprodb-data ← from PVC (db-pv-claim, 3GB)
```

***

## Four Concepts Integrated in One File

```
DEPLOYMENT    → pod lifecycle management (self-heal + rolling update)
SECRET        → password injection (base64 encoded, NOT encrypted)
PVC           → persistent storage (3GB EBS → /var/lib/mysql)
INIT CONTAINER → pre-startup volume cleanup (rm lost+found)
```

***

## Secret Injection Flow

```
Secret (app-secret)
  └── key: db-pass → base64 encoded value
                      ↓ Kubernetes decodes
Container env:
  MYSQL_ROOT_PASSWORD ← decoded password injected

WHY? → Deployment YAML file shows NO password
     → prevents ACCIDENTAL exposure
     → NOT real security (base64 ≠ encryption)
     → real security: AWS KMS keys
```

***

## PVC Volume Connection (Two-Step)

```
STEP 1: Define volume (pod level)
  volumes:
    - name: vprodb-data
      persistentVolumeClaim:
        claimName: db-pv-claim         ← references existing PVC (3GB)

STEP 2: Mount volume (container level)
  volumeMounts:
    - mountPath: /var/lib/mysql        ← MySQL data directory
      name: vprodb-data                ← references Step 1 volume

Same pattern as EBS: define (recognize) → mount (connect to directory)
```

***

## The EBS Lost+Found Problem + Init Container Solution

```
PROBLEM:
  EBS volume formatted → creates lost+found directory (Linux default)
  Volume mounted to /var/lib/mysql → NOT empty
  MySQL first start → expects EMPTY directory → REFUSES to start

SOLUTION: Init Container
  1. Init container (busybox) starts FIRST
  2. Mounts same volume → runs: rm -rf /var/lib/mysql/lost+found
  3. Init container DIES (command complete)
  4. Main container (MySQL) starts → mounts clean volume → initializes OK

Init container = PRE-STARTUP TASK in separate disposable container
```

***

## Init Container Execution Order

```
Pod starts
  ↓
Init Container 1 (busybox) → mount volume → rm lost+found → EXIT
  ↓ (only after init completes)
Main Container (MySQL) → mount same volume → /var/lib/mysql is EMPTY → START OK
```

***

## Label Consistency Rule (Three Places)

```
Deployment metadata:     labels: app: vprodb
Deployment selector:     matchLabels: app: vprodb
Pod template:            labels: app: vprodb

ALL THREE must match
Service (next lecture) will use selector: app: vprodb → finds this pod
```

***

## YAML Indentation Rules (Critical)

```
Under pod spec (same level):
  ├── initContainers:
  ├── containers:
  └── volumes:

Under container (same level):
  ├── image:
  ├── ports:
  ├── env:
  └── volumeMounts:

env: at SAME level as ports: (not nested inside)
volumes: at SAME level as containers: (not nested inside)
```

***

## Command Syntax in Containers

```
args: ["rm", "-rf", "/var/lib/mysql/lost+found"]
       ↑cmd    ↑flags   ↑path

Format: list of strings, each element separated
Same as Python list: ["element1", "element2", "element3"]
```

***

## Dependencies (Prerequisites)

```
BEFORE creating this Deployment:
  ✅ Secret: app-secret (with key: db-pass) → created in previous lecture
  ✅ PVC: db-pv-claim (3GB) → created in previous lecture

AFTER this Deployment:
  → Create ClusterIP Service for MySQL (next lecture)
  → So Tomcat pod can connect to MySQL via stable endpoint
```

***

## Reusable Engineering Patterns

```
1. INIT CONTAINER = PRE-STARTUP HOOK  → Run setup tasks before main app starts
                                         Clean volumes, wait for dependencies, download configs
                                         Disposable: runs once → dies → main container starts
                                         (same pattern: Docker entrypoint scripts, systemd ExecStartPre)

2. SECRET REFERENCE, NOT VALUE        → Never hardcode passwords in definition files
                                         Reference a Secret object → K8s injects at runtime
                                         Files can be committed to Git safely
                                         (same pattern: env vars from vault, parameter store references)

3. TWO-STEP VOLUME BINDING            → Define volume (pod level) + Mount volume (container level)
                                         Decouples "what storage" from "where it appears"
                                         Same volume mountable to multiple containers in same pod

4. KNOWN ISSUE AWARENESS              → EBS lost+found is a KNOWN issue → plan for it
                                         Production = knowing the edge cases, not just the happy path
                                         (same pattern: checking for known issues in any infrastructure)

5. SKELETON + MODIFY                  → Start from template (docs/AI/previous files) → customize
                                         Don't write from memory → start from structure → fill in specifics
                                         (same pattern: helm create, cookiecutter, project templates)
```

***

## Rapid Recall Triggers

```
"Why Deployment not Pod?"              → Self-healing + rolling updates (pods are mortal)
"DB replicas in Deployment?"           → 1 only — DB scaling needs StatefulSet
"How password injected?"               → env: valueFrom: secretKeyRef → K8s decodes + injects
"Is base64 Secret encrypted?"          → NO — encoding only, prevents accidental exposure, use KMS for real security
"PVC mounting steps?"                  → 1) Define volume (pod level) 2) Mount volume (container level)
"MySQL data directory?"                → /var/lib/mysql
"What is the lost+found problem?"      → EBS format creates lost+found → MySQL expects empty dir → won't start
"How to fix lost+found?"              → Init container (busybox) → rm -rf lost+found → dies → MySQL starts clean
"What is an init container?"           → Container that runs BEFORE main container, completes task, then dies
"Init container image used?"           → busybox:latest (minimal Linux — just needs rm command)
"args format?"                         → List of strings: ["rm", "-rf", "/path"]
"Labels needed in how many places?"    → Three: deployment metadata, selector, pod template (all must match)
"env: indentation level?"              → Same level as ports: (both under container)
"volumes: indentation level?"          → Same level as containers: (both under pod spec)
"Where are complete files?"            → kube-app folder in course resources
"Next lecture?"                        → ClusterIP Service for MySQL → internal pod-to-pod connectivity
```

***

This completes the full reconstruction of the Kubernetes MySQL Deployment lecture. **Theory** builds the conceptual model of Deployment-over-Pod reasoning, Secret injection mechanics, PVC two-step binding, and the critical EBS lost+found problem with the init container solution; **Practical** walks through every YAML field with exact indentation, dependency prerequisites, and execution flow; and the **Mental Compression Map** compresses the four-concept integration (Deployment + Secret + PVC + Init Container), the execution order, and the YAML structure into rapid-recall structures. [\[352-mysql-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/352-mysql-app.txt)

Ready for the next lecture (ClusterIP Service for MySQL), or shall I generate an **AnkiDeck CSV** covering this lecture or the full course series? 🚀
