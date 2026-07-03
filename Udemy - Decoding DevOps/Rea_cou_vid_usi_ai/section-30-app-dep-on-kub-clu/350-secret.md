# 🎓 Deep Learning Material: Kubernetes Secrets — Encoding Sensitive Data and Injecting It Into Pods

**Source:** Video lecture on Kubernetes Secrets (from [350-secret.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt?EntityRepresentationId=01568e08-2d4c-4b6c-b51d-617e16d82c85) caption file) [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**Video Context:** This lecture introduces Kubernetes **Secrets** — objects designed to store sensitive data (passwords, tokens, keys) separately from application code and pod definitions. The instructor creates a Secret manifest to store two passwords (MySQL database password and RabbitMQ password) that were previously hardcoded in the Docker Compose file. The lecture carefully distinguishes between **encoding** (base64, which this lecture uses — prevents accidental exposure only) and **encryption** (which uses keys and is truly secure). The instructor encodes passwords using the `echo -n | base64` command and writes them into a Secret manifest of type `Opaque`. These values will be injected into pod definitions in subsequent lectures.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Passwords in Source Code

The lecture starts by examining the Docker Compose file from the containerization project. The MySQL container required a mandatory environment variable `MYSQL_ROOT_PASSWORD` with the database password set directly as a plain-text value. The instructor identifies the fundamental problem: *"this is the database password. We cannot directly put this database password like this for productions. Also in test and staging also you should never put, but in the source code, you should never have the database password."* [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

But the application needs the password to connect to the database — it's referenced in the `application.properties` file as `vprodbpass`. Similarly, RabbitMQ has a password (`guest`). These values must be supplied to the containers at runtime, but they shouldn't be visible in the manifest files or source code repositories. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

The engineering tension: the system **needs** the password, but it should **never appear** in readable form in any file that might be committed to version control, shared with unauthorized users, or displayed in logs.

***

## 1.2 — The Solution Spectrum: Encoding vs. Encryption

The instructor carefully distinguishes between two approaches to protecting sensitive data: [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**Encryption** — Uses cryptographic keys to transform data into ciphertext that cannot be read without the corresponding decryption key. The encryption key is stored separately. *"Whenever you have such kind of things, then usually you encrypt it. And the encryption key will be somewhere else. So even if someone looks at it, they will see this gibberish values, which they will not be able to decrypt."* This is the production-grade approach. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**Encoding (base64)** — Transforms data into a different representation using a publicly known algorithm (base64). There is no key. Anyone who sees the encoded value can decode it trivially. *"Encoding-decoding is actually not safe and not recommended for production. It is just to prevent accidental exposure, that's all. If someone sees the encoded key, they can very easily decode it."* [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

The instructor is transparent that this lecture uses **encoding, not encryption**: *"the idea in this lecture is not to encrypt, but to prevent the accidental exposure of our password."* Kubernetes Secrets of type Opaque use base64 encoding — they provide a layer of obscurity (a glance at the manifest won't reveal the password) but not true security. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

> ⚠️ **Expert Note**
>
> In production Kubernetes environments, base64-encoded Secrets are considered **not secure** by themselves. To truly protect Secrets: (1) enable **encryption at rest** in etcd (Kubernetes stores Secrets in etcd, and by default they're stored as base64, not encrypted), (2) use external secret management tools like HashiCorp Vault, AWS Secrets Manager, or sealed-secrets, and (3) use RBAC to restrict who can read Secret objects. The instructor explicitly acknowledges this limitation: *"encoding-decoding is actually not safe and not recommended for production."* [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

## 1.3 — Kubernetes Secret Object: What It Is

A **Secret** is a Kubernetes API object specifically designed to hold sensitive information — passwords, OAuth tokens, SSH keys, TLS certificates. It's stored separately from pod definitions and can be **injected** into pods as environment variables or mounted as files. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

The instructor explains: *"In Kubernetes, we can use a secret object, which can secretly store our information. And that information can be injected in the pod."* [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

### Types of Secrets

The instructor lists four types: [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

| Type                 | Purpose                                  | Used in This Lecture |
| -------------------- | ---------------------------------------- | -------------------- |
| **Opaque**           | Generic key-value pairs (base64 encoded) | ✅ Yes                |
| **TLS**              | TLS certificates and keys (encrypted)    | No                   |
| **Token**            | Authentication tokens                    | No                   |
| **dockerconfigjson** | Docker Hub authentication credentials    | No                   |
| **SSH**              | SSH authentication keys                  | No                   |

*"Opaque, this is what we will be using. This is just encoding and decoding with base64, nothing so serious. But you can use encryptions with TLS and tokens."* [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

## 1.4 — Base64 Encoding: How It Works

Base64 is a **reversible encoding scheme** — not a hash, not encryption. It converts binary/text data into a string of ASCII characters using a 64-character alphabet. The transformation is deterministic and publicly known. Anyone can decode a base64 string using the `base64 --decode` command or any online tool. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

The encoding command: `echo -n "password" | base64` [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

* `echo -n` — prints the password without a trailing newline (the `-n` flag is critical — without it, the newline character gets encoded as part of the password, producing a different base64 value that won't match the actual password)
* `| base64` — pipes the output through the base64 encoder

The instructor demonstrates encoding both passwords: `vprodbpass` and `guest`. The encoded values look like random strings — this is the "accidental exposure prevention" aspect. A casual glance at the manifest won't reveal the passwords. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

## 1.5 — Secret Manifest Structure

The Secret manifest follows the standard Kubernetes YAML structure: [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  db-pass: <base64-encoded-value>
  rmq-pass: <base64-encoded-value>
```

**Key fields:**

* `kind: Secret` — the resource type (capital S)
* `type: Opaque` — indicates base64-encoded key-value pairs
* `data:` — contains the key-value pairs where **values must be base64-encoded**
* `db-pass` and `rmq-pass` — user-defined variable names that will be referenced when injecting into pods [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

The `data` section's keys (`db-pass`, `rmq-pass`) are the names you'll use to reference these values in pod definitions. The instructor notes: *"this is what we'll inject in our pod definitions."* [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

## 1.6 — Where the Passwords Come From

The instructor traces the actual password values from the source code: [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**Database password:** Found in `src/main/resources/application.properties` — the value is `vprodbpass`. This is the same file used in the Docker image built during the containerization project. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**RabbitMQ password:** The value is `guest` (the default RabbitMQ password). [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

Both values are encoded with base64 and stored in the Secret manifest. When pods need these passwords, they reference the Secret by name (`app-secret`) and key (`db-pass` or `rmq-pass`), and Kubernetes automatically **decodes** the base64 value and injects the plain-text password into the container. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a Kubernetes **Secret manifest** that stores two base64-encoded passwords (MySQL database and RabbitMQ). These passwords were previously hardcoded in Docker Compose files. In Kubernetes, they'll be stored as a Secret object and injected into pods — separating sensitive data from application code. The final outcome: a `secret.yaml` file ready to be applied, with encoded passwords that will be referenced by pod definitions in subsequent lectures.

***

## Step 1: Identify the Passwords to Encode

**Database password:** [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

Navigate to the source code:

```
src/main/resources/application.properties
```

The database password is: `vprodbpass` [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**RabbitMQ password:** `guest` [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

## Step 2: Encode the Passwords with Base64

Open **Git Bash** (Windows) or **Terminal** (macOS/Linux).

**Encode the database password:**

```bash
echo -n "vprodbpass" | base64
```

* `echo` — prints the string
* `-n` — **critical flag** — suppresses the trailing newline character. Without this, the encoded value includes a newline, producing a different (incorrect) base64 string
* `"vprodbpass"` — the plain-text password
* `| base64` — pipes through the base64 encoder [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**Copy the output** — this is the encoded value for `db-pass`.

**Encode the RabbitMQ password:**

```bash
echo -n "guest" | base64
```

**Copy the output** — this is the encoded value for `rmq-pass`. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

> 🔍 **Deep Dive**
>
> To verify or decode a base64 value, use: `echo "<encoded-value>" | base64 --decode`. This demonstrates exactly what the instructor means by "if someone sees the encoded key, they can very easily decode it." Base64 provides zero cryptographic security — it's a format transformation, not a protection mechanism. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

## Step 3: Write the Secret Manifest

Open or create `secret.yaml` in the `kubedefs` directory: [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  db-pass: dnByb2RicGFzcw==
  rmq-pass: Z3Vlc3Q=
```

 [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**Field-by-field breakdown:**

| Field           | Value        | Explanation                                             |
| --------------- | ------------ | ------------------------------------------------------- |
| `apiVersion`    | `v1`         | Secrets are part of the core API group                  |
| `kind`          | `Secret`     | Resource type (capital S)                               |
| `metadata.name` | `app-secret` | Name used to reference this Secret from pod definitions |
| `type`          | `Opaque`     | Generic base64-encoded key-value store                  |
| `data.db-pass`  | `<base64>`   | Encoded database password (`vprodbpass`)                |
| `data.rmq-pass` | `<base64>`   | Encoded RabbitMQ password (`guest`)                     |

<cite>turn28search10</cite>

**Save the file** (Ctrl+S in VS Code, `:wq` in vim). [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

**Common mistakes:**

* Forgetting `-n` in `echo -n` → encoded value includes a newline → password mismatch at runtime
* Using `stringData` instead of `data` (stringData accepts plain text, data requires base64 — they're different fields)
* Typos in the key names (`db-pass`, `rmq-pass`) → pod definitions referencing wrong keys → injection fails

**Connection to system flow:** This Secret will be applied to the cluster with `kubectl apply -f secret.yaml`. Pod definitions will reference `app-secret` by name and pull specific keys (`db-pass`, `rmq-pass`) as environment variables. Kubernetes will auto-decode the base64 values and inject the plain-text passwords into the containers. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept (One-Line Reconstruction)

> **Kubernetes Secrets store sensitive data (base64-encoded for Opaque type) as a separate object, injected into pods at runtime — preventing passwords from appearing in manifests or source code.**

***

## 🔷 The Problem → Solution Chain

```
PROBLEM:
  Docker Compose: MYSQL_ROOT_PASSWORD=vprodbpass (plain text in file)
  → Password visible in source code, version control, logs
  → Security risk

SOLUTION:
  Kubernetes Secret: stores encoded password as separate object
  → Pod references Secret by name + key
  → Kubernetes decodes and injects at runtime
  → Password never appears in pod definition
```

***

## 🔷 Encoding vs. Encryption

```
ENCODING (base64) — THIS LECTURE:
  → Reversible by anyone (no key needed)
  → Prevents ACCIDENTAL exposure only
  → echo -n "password" | base64
  → echo "encoded" | base64 --decode
  → NOT production-secure

ENCRYPTION — PRODUCTION:
  → Requires encryption key to decrypt
  → Key stored separately
  → Truly secure
  → Tools: Vault, AWS Secrets Manager, sealed-secrets
  → Enable encryption at rest in etcd
```

***

## 🔷 Secret Manifest Template

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret          # referenced by pod definitions
type: Opaque                 # base64 encoded key-value
data:
  db-pass: <base64-value>    # echo -n "vprodbpass" | base64
  rmq-pass: <base64-value>   # echo -n "guest" | base64
```

***

## 🔷 Base64 Encoding Commands

```bash
# ENCODE:
echo -n "vprodbpass" | base64
#        ^^^ -n is CRITICAL (no trailing newline)

# DECODE (verification):
echo "dnByb2RicGFzcw==" | base64 --decode
```

***

## 🔷 Secret Types

```
TYPE                USE CASE                        THIS LECTURE
──────────          ────────────────────            ────────────
Opaque              Generic passwords/keys          ✅ Used
TLS                 TLS certificates + keys         No
Token               Auth tokens                     No
dockerconfigjson    Docker Hub credentials          No
SSH                 SSH authentication keys          No
```

***

## 🔷 Data Flow: Secret → Pod

```
SECRET OBJECT (app-secret):
  data:
    db-pass: dnByb2RicGFzcw==     (base64 of "vprodbpass")
    rmq-pass: Z3Vlc3Q=            (base64 of "guest")

            │
            ▼ (referenced by pod definition)

POD DEFINITION:
  env:
    - name: MYSQL_ROOT_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secret        ← Secret name
          key: db-pass            ← key within the Secret

            │
            ▼ (Kubernetes auto-decodes base64)

CONTAINER RUNTIME:
  MYSQL_ROOT_PASSWORD = "vprodbpass"   (plain text, in memory only)
```

***

## 🔷 Password Sources (This Project)

```
PASSWORD         PLAIN TEXT       SOURCE FILE                      SECRET KEY
────────         ──────────       ──────────────────────           ──────────
MySQL DB         vprodbpass       application.properties           db-pass
RabbitMQ         guest            default RabbitMQ password        rmq-pass
```

***

## 🔷 Key Warnings

```
⚠️ echo WITHOUT -n:
   echo "password" | base64  → encodes "password\n" (WITH newline)
   echo -n "password" | base64 → encodes "password" (correct)
   WRONG encoding = password mismatch at runtime = connection failures

⚠️ Opaque Secrets are NOT encrypted:
   "encoding-decoding is actually not safe
    and not recommended for production"
   → base64 = obscurity, NOT security
   → anyone can decode: echo "value" | base64 --decode

⚠️ Never commit plain-text passwords:
   "in the source code, you should never have the database password"
   → even Secret manifests with base64 should be handled carefully
   → consider using sealed-secrets or external vault for git-committed manifests
```

***

## 🔷 Reusable Engineering Pattern: Sensitive Data Separation

```
PATTERN: Separate Sensitive Data from Configuration

ANTI-PATTERN (what we're fixing):
  docker-compose.yml:
    MYSQL_ROOT_PASSWORD: vprodbpass     ← password IN the config file
  
  → committed to git → visible to everyone → security violation

CORRECT PATTERN:
  secret.yaml:
    db-pass: <encoded>                  ← password in SEPARATE object
  
  pod.yaml:
    secretKeyRef: app-secret / db-pass  ← REFERENCE, not value

  → pod definition has NO password
  → Secret object managed separately
  → Access controlled via RBAC

THIS PATTERN APPLIES TO:
  Kubernetes:  Secret object → injected via env/volume
  Docker:      Docker secrets → mounted in /run/secrets
  AWS:         Secrets Manager → accessed via SDK/IAM
  Azure:       Key Vault → accessed via managed identity
  Terraform:   sensitive variables → never in state output
  CI/CD:       pipeline secrets → injected as env vars

PRINCIPLE:
  Configuration = WHAT to connect to (hostname, port)     → can be in code
  Credentials = HOW to authenticate (password, token)     → must be separate
```

This separation is the foundational security pattern the lecture teaches: sensitive data and application configuration must live in different places, connected only by references. The Secret object is Kubernetes' native implementation of this principle. [\[350-secret \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/350-secret.txt)
