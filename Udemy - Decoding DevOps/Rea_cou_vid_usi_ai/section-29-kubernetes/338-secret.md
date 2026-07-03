# 🧠 Kubernetes Secrets — Encoded Data Storage, Pod Injection & Private Registry Authentication

**Source:** *338. Secret* — Kubernetes Series (Video Caption Reconstruction + Command Reference)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: ConfigMaps Store Everything in Clear Text

In the previous lecture, ConfigMaps were introduced as a way to inject variables and configuration files into pods. ConfigMaps work well for non-sensitive data, but they have a critical limitation: everything is stored in **clear text**. If you store a database password in a ConfigMap, that password sits in plain text inside the ConfigMap definition file. Since definition files are stored in **git repositories**, anyone with access to the repository can read those passwords directly. The instructor frames this directly: *"Who has access to that git repository can see the passwords in clear text, which is very bad."*

**Secrets** solve this problem. A Secret is a Kubernetes object that stores sensitive data — passwords, tokens, keys, credentials — in an **encoded** format rather than clear text. You can then inject Secrets into pods just like ConfigMaps, but the sensitive values are not exposed in plain text in your definition files or repository.

***

## 1.2 Encoding vs. Encryption — The Critical Distinction

The instructor is very deliberate about terminology: Secrets use **encoding**, not encryption. The encoding method is **base64** — a standard encoding scheme that converts binary data to ASCII text. Base64 is **not a security mechanism**. Anyone who has the encoded value can decode it trivially.

The instructor demonstrates this explicitly: encoding `secretpass` with `echo -n "secretpass" | base64` produces an encoded string, and decoding it with `echo '<encoded-string>' | base64 -d` returns the original text immediately. There's no key, no password, no cryptographic protection.

So why use it if it's not secure? The instructor explains: *"This is more of a best practice to avoid accidental exposure."* The purpose is **not** to make data unreadable to determined attackers — it's to prevent casual, accidental exposure. When someone glances at a YAML file or a `kubectl get` output, they see encoded gibberish instead of raw passwords. This prevents the most common exposure vector: someone accidentally seeing credentials they shouldn't have seen.

The Secret is stored in the **Kubernetes control plane** (etcd). If someone has access to the control plane, they can retrieve and decode the values. For true security, the instructor notes: *"If you really want to encrypt, there is a way — you need to use encryption keys and you can encrypt this data as well."* Kubernetes supports **encryption at rest** for Secrets using encryption keys, but that's beyond the scope of this lecture.

> 🔍 **Deep Dive:** The security model of Secrets has three layers: (1) **Base64 encoding** — prevents accidental visual exposure (what this lecture covers). (2) **RBAC** — Kubernetes role-based access control limits who can read Secrets via the API. (3) **Encryption at rest** — encrypts Secret data in etcd using encryption keys (mentioned but out of scope). In production, all three layers should be active. Base64 alone is necessary but not sufficient.

***

## 1.3 Secret Types — Different Purposes for Different Data

Kubernetes Secrets come in multiple **types**, each designed for a specific kind of sensitive data. The instructor walks through the documentation to highlight the key types:

### Opaque (Generic)

The most basic and commonly used type. Stores arbitrary key-value pairs with base64-encoded values. This is what you use for passwords, API keys, tokens, and any general-purpose sensitive data. The instructor uses this type throughout the hands-on exercise.

### docker-registry (Docker Configuration)

This type stores **Docker registry credentials** — the username, password, email, and server URL needed to pull images from a **private Docker registry**. The instructor describes this as a *"very popular use case"* and dedicates significant attention to it.

In all previous lectures, container images were pulled from **public** Docker Hub repositories. But in real projects, application images are stored in **private registries** — Docker Hub private repos, AWS ECR, Google Container Registry, or self-hosted registries. Kubernetes needs credentials to authenticate and pull from these private registries. The `docker-registry` Secret type provides these credentials.

### Other Types (Mentioned)

* **Service account token** — Used for authentication within the cluster
* **SSH auth** — Stores SSH credentials
* **TLS** — Stores TLS certificates and keys

***

## 1.4 Creating Secrets — Imperative vs. Declarative

Like most Kubernetes objects, Secrets can be created two ways:

### Imperative (Command Line)

```bash
kubectl create secret generic <secret-name> --from-literal=<key>=<value>
```

The instructor notes: *"You will think, hey, it's same as ConfigMap. Well, almost."* The command structure is nearly identical to ConfigMap creation. The difference is what Kubernetes does with the value: it **encodes** it automatically. When you inspect the secret with `kubectl get secret`, the values appear as encoded strings, not the original clear text.

### Declarative (YAML Definition File)

When creating a Secret declaratively, **you** must encode the values first (using `echo -n "<text>" | base64`) and put the encoded values in the YAML file. The YAML file specifies `kind: Secret`, `type: Opaque`, and a `data:` section with base64-encoded key-value pairs.

The instructor emphasizes: *"You would have already encoded it, otherwise there's no point."* If you put clear text in the `data:` field of a Secret YAML, it will fail or be double-encoded.

***

## 1.5 Injecting Secrets into Pods — Two Methods

Once a Secret exists in the cluster, pods need to read its values. The injection mechanisms parallel ConfigMap injection:

### Method 1: All Keys at Once (`envFrom`)

```yaml
envFrom:
  - secretRef:
      name: mysecret
```

This exports **all** key-value pairs from the Secret as environment variables in the container. Every key becomes a variable name, every decoded value becomes the variable value.

### Method 2: Selective Keys (`valueFrom`)

```yaml
env:
  - name: SECRET_USERNAME
    valueFrom:
      secretKeyRef:
        name: mysecret
        key: username
        optional: false
```

This selectively maps **specific keys** from the Secret to specific environment variable names in the container. The `name` field defines what the environment variable is called inside the container (e.g., `SECRET_USERNAME`), and `secretKeyRef` specifies which Secret and which key to read.

The `optional: false` field means the Secret and the specified key **must exist** — if they don't, the pod won't start. This is a safety mechanism: it prevents pods from running with missing credentials, which would cause runtime failures.

> 🔍 **Deep Dive:** When a Secret value is injected into a pod as an environment variable, Kubernetes **automatically decodes** the base64 value. The container receives the **original clear text** — not the encoded version. The instructor demonstrates this: after exec-ing into the pod and running `echo $SECRET_USERNAME`, the output is `admin` (the original text), not `YWRtaW4=` (the encoded text). The encoding exists only in the storage and definition layer, not inside the running container.

***

## 1.6 Docker Registry Secret — Pulling from Private Registries

The `docker-registry` Secret type is a specialized use case that the instructor identifies as *"very popular."* The workflow:

**Step 1: Create the registry Secret** — Either imperatively (passing username, password, email, server URL directly in the command) or from a Docker config JSON file. The secret stores all authentication details for the private registry.

**Step 2: Reference the Secret in the pod** — In the pod spec, use `imagePullSecrets` to tell Kubernetes which Secret contains the registry credentials:

```yaml
spec:
  containers:
    - name: myapp
      image: private-registry.example.com/myapp:v1
  imagePullSecrets:
    - name: regcred
```

When Kubernetes needs to pull the image, it reads the Secret, uses the credentials to authenticate with the private registry, and pulls the image. Without this Secret, pulling from a private registry fails with an authentication error.

The instructor notes you can specify a custom registry URL and port — not just Docker Hub. Many companies run their own registries, and the Secret's server field accommodates this.

***

## 1.7 Secrets and ConfigMaps — The Relationship

The instructor positions Secrets and ConfigMaps as **complementary tools** that together handle all data injection into pods:

| Aspect               | ConfigMap                                         | Secret                                     |
| -------------------- | ------------------------------------------------- | ------------------------------------------ |
| **Data type**        | Non-sensitive (config files, feature flags, URLs) | Sensitive (passwords, tokens, keys, certs) |
| **Storage format**   | Clear text                                        | Base64 encoded                             |
| **Injection method** | `configMapRef` / `configMapKeyRef`                | `secretRef` / `secretKeyRef`               |
| **Image pulling**    | N/A                                               | `imagePullSecrets` for private registries  |

The instructor emphasizes the operational importance: *"When you run your pod, you will inject data into that. You will inject credentials, you will inject secret encoded variables or just normal variables or configuration files. And for that, ConfigMaps and Secrets are very useful."*

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a **Kubernetes Secret** with encoded username and password values, then creating a pod that reads those Secret values as environment variables. This demonstrates the complete Secret lifecycle: encode → create Secret → inject into pod → verify decoded values inside the container.

**Final outcome:** A running Redis pod that has `SECRET_USERNAME=admin` and `SECRET_PASSWORD=mysecretpass` as environment variables, injected from a Secret where these values are stored in base64-encoded form.

***

## Step 1: Encode the Username and Password

Before creating a declarative Secret, you must encode the values yourself:

```bash
echo -n "admin" | base64
```

**Command breakdown:**

* `echo -n "admin"` — Outputs the string `admin` without a trailing newline. The `-n` flag is critical — without it, the newline character gets encoded too, producing a different (incorrect) encoded value.
* `| base64` — Pipes the output to the `base64` encoder.

**Expected output:** `YWRtaW4=`

```bash
echo -n "mysecretpass" | base64
```

**Expected output:** `bXlzZWNyZXRwYXNz`

**Save both encoded values** — you'll need them in the next step.

**Common mistake:** Forgetting `-n` in `echo`. Without it, a newline is included in the encoding, and the decoded value inside the pod will have an unexpected trailing newline, which can break authentication logic.

***

## Step 2: Create the Secret Definition File

```bash
vim mysecret.yaml
```

**Contents:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
data:
  username: YWRtaW4=
  password: bXlzZWNyZXRwYXNz
type: Opaque
```

**Line-by-line breakdown:**

* `apiVersion: v1` — Secrets are a core API resource (v1).
* `kind: Secret` — Declares this as a Secret object.
* `metadata: name: mysecret` — The Secret's name. Referenced later by the pod.
* `data:` — The key-value pairs. **Values must be base64-encoded.** Two keys here: `username` and `password`.
* `type: Opaque` — The generic Secret type for arbitrary data.

**Save and quit** (`:wq`).

***

## Step 3: Create the Secret

```bash
kubectl create -f mysecret.yaml
```

**Expected output:** `secret/mysecret created`

**Verification:** The Secret now exists in the cluster with encoded values. If you `kubectl get secret mysecret -o yaml`, you'll see the base64 values — not the original text.

***

## Step 4: Create the Pod Definition File That Reads the Secret

```bash
vim readsecret.yaml
```

**Contents:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
    - name: mycontainer
      image: redis
      env:
        - name: SECRET_USERNAME
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: username
              optional: false
        - name: SECRET_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: password
              optional: false
  restartPolicy: Never
```

**Key sections breakdown:**

* `image: redis` — Uses the Redis image. The choice of image doesn't matter for this exercise — any image with a shell would work. The point is demonstrating Secret injection.
* `env:` — Defines environment variables for the container.
* `name: SECRET_USERNAME` — The environment variable name **inside** the container. This is what you use with `echo $SECRET_USERNAME`.
* `secretKeyRef:` — Tells Kubernetes to get the value from a Secret.
  * `name: mysecret` — The Secret name (must match Step 2).
  * `key: username` — The specific key within the Secret to read.
  * `optional: false` — The Secret and key **must** exist; if they don't, the pod won't start.
* `restartPolicy: Never` — The pod won't restart if the container exits.

**Source:** The instructor notes: *"I got all this from the Kubernetes documentation."* The pod definition is adapted from the official Secret documentation examples.

**Save and quit.**

***

## Step 5: Create the Pod

```bash
kubectl create -f readsecret.yaml
```

**Expected output:** `pod/secret-env-pod created`

**Verify the pod is running:**

```bash
kubectl get pod
```

**Expected:** `secret-env-pod` with status `Running`.

**If the pod isn't running:** Check if the Secret exists and has the correct key names. If `optional: false` and the Secret/key is missing, the pod will be in `CreateContainerConfigError` state.

***

## Step 6: Verify Decoded Secret Values Inside the Pod

Exec into the running pod:

```bash
kubectl exec --stdin --tty secret-env-pod -- /bin/bash
```

**Command breakdown:**

* `kubectl exec` — Execute a command in a running container.
* `--stdin --tty` — Allocate an interactive terminal (like SSH).
* `secret-env-pod` — The pod name.
* `-- /bin/bash` — The command to run inside the container (bash shell).

**Inside the container, print the Secret values:**

```bash
echo $SECRET_USERNAME
```

**Expected output:** `admin`

```bash
echo $SECRET_PASSWORD
```

**Expected output:** `mysecretpass`

**Key observation:** The values are **decoded** — you see the original text (`admin`, `mysecretpass`), not the base64-encoded versions (`YWRtaW4=`, `bXlzZWNyZXRwYXNz`). Kubernetes automatically decodes Secret values when injecting them into pods.

**Common mistake:** Using the wrong variable name. The variable name is `SECRET_USERNAME` (defined in the pod YAML `env.name` field), not `username` (the key in the Secret). These are different — the pod definition maps Secret keys to container environment variable names.

**Exit the container:** `exit`

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Secret vs. ConfigMap — Core Distinction

```
ConfigMap                          Secret
─────────                          ──────
Non-sensitive data                 Sensitive data (passwords, tokens, keys)
Stored in CLEAR TEXT               Stored BASE64 ENCODED
configMapRef / configMapKeyRef     secretRef / secretKeyRef
No image pull support              imagePullSecrets for private registries

BOTH: inject data into pods as env vars or files
```

***

## Encoding ≠ Encryption

```
BASE64 ENCODING:
  echo -n "admin" | base64           →  YWRtaW4=
  echo 'YWRtaW4=' | base64 -d       →  admin

  ANYONE can decode → NOT a security mechanism
  PURPOSE: prevent ACCIDENTAL visual exposure

ENCRYPTION (out of scope):
  Requires encryption keys
  Kubernetes supports encryption at rest for Secrets
  Stored encrypted in etcd → only decryptable with the key
  
SECURITY LAYERS:
  1. Base64 encoding (accidental exposure prevention)
  2. RBAC (API access control — who can read Secrets)
  3. Encryption at rest (true cryptographic protection)
```

***

## Secret Creation Flow

```
DECLARATIVE:
  1. Encode values:  echo -n "text" | base64
  2. Write YAML:     kind: Secret, type: Opaque, data: {key: encoded-value}
  3. Create:         kubectl create -f mysecret.yaml

IMPERATIVE:
  kubectl create secret generic <name> --from-literal=<key>=<value>
  → Kubernetes encodes automatically
```

***

## Secret YAML Structure

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
data:
  username: YWRtaW4=          # base64 of "admin"
  password: bXlzZWNyZXRwYXNz  # base64 of "mysecretpass"
type: Opaque
```

***

## Pod Injection — Two Methods

```
METHOD 1: ALL keys (envFrom)
  envFrom:
    - secretRef:
        name: mysecret
  → exports ALL keys as env vars

METHOD 2: SELECTIVE keys (valueFrom)
  env:
    - name: SECRET_USERNAME        ← env var name in container
      valueFrom:
        secretKeyRef:
          name: mysecret           ← Secret name
          key: username            ← specific key in Secret
          optional: false          ← must exist or pod fails

AUTO-DECODE: Kubernetes decodes base64 → container gets CLEAR TEXT
  Storage: YWRtaW4=
  Container: admin
```

***

## Secret Types

```
Opaque (generic)         → arbitrary key-value pairs (passwords, tokens)
docker-registry          → private registry credentials (username, password, server)
service-account-token    → cluster authentication
ssh-auth                 → SSH credentials
tls                      → TLS certificates and keys
```

***

## Private Registry Pull Pattern

```
STEP 1: Create docker-registry Secret
  kubectl create secret docker-registry regcred \
    --docker-username=<user> \
    --docker-password=<pass> \
    --docker-email=<email> \
    --docker-server=<registry-url>

STEP 2: Reference in pod spec
  spec:
    containers:
      - name: myapp
        image: private-registry.example.com/myapp:v1
    imagePullSecrets:
      - name: regcred

FLOW:
  Pod needs image → reads imagePullSecrets → gets regcred Secret
  → authenticates with private registry → pulls image

WITHOUT Secret: pull from private registry → authentication error
```

***

## Complete Exercise Flow

```
1. echo -n "admin" | base64                    → YWRtaW4=
2. echo -n "mysecretpass" | base64             → bXlzZWNyZXRwYXNz
3. vim mysecret.yaml (kind: Secret, data: encoded values)
4. kubectl create -f mysecret.yaml             → secret created
5. vim readsecret.yaml (pod with secretKeyRef)
6. kubectl create -f readsecret.yaml           → pod created
7. kubectl get pod                             → Running
8. kubectl exec --stdin --tty secret-env-pod -- /bin/bash
9. echo $SECRET_USERNAME                       → admin (decoded!)
10. echo $SECRET_PASSWORD                      → mysecretpass (decoded!)
```

***

## Variable Name Mapping

```
Secret key:      username            (in mysecret.yaml data:)
Pod env name:    SECRET_USERNAME     (in readsecret.yaml env.name:)
Container var:   $SECRET_USERNAME    (what you echo inside pod)

⚠️ Secret key ≠ Container variable name
   Pod definition MAPS between them
```

***

## Common Pitfalls

```
echo without -n                → newline encoded → wrong value in Secret
Clear text in data: field      → fails or double-encoded
Wrong Secret name in pod       → pod won't start (optional: false)
Wrong key name in secretKeyRef → pod won't start (optional: false)
Using Secret key as var name   → echo $username fails; use echo $SECRET_USERNAME
Treating base64 as encryption  → false security; anyone can decode
```

***

## Commands Reference

```bash
# Encode
echo -n "text" | base64

# Decode
echo 'encoded' | base64 -d

# Create Secret (declarative)
kubectl create -f mysecret.yaml

# Create Secret (imperative, generic)
kubectl create secret generic <name> --from-literal=key=value

# Create Secret (docker-registry)
kubectl create secret docker-registry <name> \
  --docker-username=<u> --docker-password=<p> --docker-email=<e> --docker-server=<s>

# Create pod
kubectl create -f readsecret.yaml

# Exec into pod
kubectl exec --stdin --tty <pod-name> -- /bin/bash
```

***

## Reusable Engineering Pattern: Layered Sensitive Data Management

```
PATTERN:
  1. ENCODE/ENCRYPT sensitive data before storing
  2. STORE in a dedicated secret management object (not alongside code)
  3. INJECT into the runtime environment (env vars / files)
  4. AUTO-DECODE at injection point (consumer gets clear text)

LAYERS:
  Definition layer:  encoded/encrypted (safe in git repos)
  Storage layer:     control plane / etcd (access-controlled)
  Runtime layer:     decoded clear text (available to application)

WHERE ELSE:
  • AWS Secrets Manager → inject into ECS/EKS pods
  • HashiCorp Vault → inject into any application
  • Azure Key Vault → inject into AKS pods
  • Docker Secrets → inject into Swarm services
  • .env files + encryption → inject via CI/CD pipeline

PRINCIPLE:
  Sensitive data must be encoded/encrypted at rest
  Decoded/decrypted only at the point of use (runtime)
  Never stored in clear text in version control
```

***

## One-Line Mental Reload Trigger

> *"Secrets store base64-encoded (not encrypted) sensitive data — encode with echo -n | base64, create kind: Secret type: Opaque with encoded values, inject into pods via secretKeyRef (auto-decoded to clear text), docker-registry type for private image pulls via imagePullSecrets — prevents accidental exposure, not true encryption without encryption keys."*

This single sentence reconstructs the encoding mechanism and its limitation, the creation workflow, the injection method with auto-decode behavior, the private registry use case, and the security boundary. <cite>turn19search23</cite><cite>turn19search22</cite>
