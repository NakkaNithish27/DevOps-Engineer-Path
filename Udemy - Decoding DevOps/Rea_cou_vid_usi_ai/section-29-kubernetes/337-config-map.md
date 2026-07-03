# ☸️ Kubernetes ConfigMaps — Injecting Variables & Configuration into Pods — Deep Learning Material

**Source:** *Config Map* (Video Lecture Caption File) + Supporting Hands-On Command History File [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt), [\[337.configMap \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337.configMap.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Problem — Pods Are Disposable, But Configuration Persists

Pods are disposable. If you want to make a change, you delete the pod and create a new one with a new container image. The image contains the application binary and its static dependencies. But what about the **dynamic** parts — the variables and configuration files that differ between environments (dev, staging, production) or change over time? You can't bake those into the image because that would require rebuilding the image for every configuration change. [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

Kubernetes solves this with two mechanisms: **environment variables** (set directly in the pod definition) and **ConfigMaps** (externalized collections of configuration data that can be injected into any pod). Both allow you to inject data into a running pod without modifying the container image.

***

## 1.2 Environment Variables — The Simplest Injection

The simplest way to inject data into a pod is through **environment variables** defined directly in the pod definition file. Under the container spec, you add an `env` section with name-value pairs: [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

```yaml
env:
  - name: MYSQL_DATABASE
    value: accounts
  - name: MYSQL_ROOT_PASSWORD
    value: vprodbpass
```

When this pod runs, the container will have these two variables available in its environment. You can verify with `echo $MYSQL_DATABASE` inside the container, and it returns `accounts`. This is functionally identical to Docker's `-e` flag or the `ENV` instruction in Dockerfiles — the variable is exported into the container's environment.

This approach works for simple cases but doesn't scale. When you're running a full application stack, you'll have **many variables and configurations that change over time**. Hardcoding them in every pod definition creates duplication, makes updates error-prone, and tightly couples pod definitions to specific values. [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

***

## 1.3 ConfigMaps — Centralized Variable and Configuration Storage

A **ConfigMap** is a Kubernetes object that stores a **collection of key-value pairs**. Instead of scattering variables across individual pod definitions, you store them all in one ConfigMap, and then inject them into whatever pods need them. The instructor describes it as: "collection of variables, and you can inject those variables in the pod." [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

ConfigMaps solve three problems simultaneously:

1. **Centralization** — all configuration in one place, not duplicated across pod definitions
2. **Decoupling** — pod definitions reference ConfigMap names, not hardcoded values; changing a value means updating the ConfigMap, not every pod definition
3. **Reusability** — the same ConfigMap can be injected into multiple pods

This is the same logic/data separation pattern seen throughout the course: Ansible `group_vars/` separate variables from playbooks, Terraform `.tfvars` separate values from resource definitions, Docker Compose `.env` files separate configuration from service definitions. ConfigMaps are Kubernetes's version of this universal pattern. [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

***

## 1.4 ConfigMap Structure — Keys and Values

A ConfigMap has a `data` section (not `spec` — this is different from most other Kubernetes objects). Inside `data`, each entry is a **key** with a **value**. The instructor demonstrates a ConfigMap called `game-demo` with four keys: [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

**Simple keys (scalar values):**

* `player_initial_lives: "3"` — a key with a simple string value
* `ui_properties_file_name: "user-interface.properties"` — another simple key-value

**Multi-line keys (configuration file content):**

* `game.properties` — a key whose value is multi-line content (multiple lines of configuration data, like a properties file)
* `user-interface.properties` — another key with multi-line content

This distinction is important: simple keys behave like environment variables (a name and a single value). Multi-line keys behave like **configuration file content** — they contain the entire content of a configuration file, and can be mounted as actual files inside the container. [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

***

## 1.5 Four Ways to Use ConfigMap Data in a Container

The instructor references the Kubernetes documentation which lists four ways to use ConfigMap data: [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

**Way 1: As command line arguments** — pass ConfigMap values as arguments to the container's command.

**Way 2: As environment variables for the entire ConfigMap (`envFrom`)** — inject ALL keys from a ConfigMap as environment variables in one statement:

```yaml
envFrom:
  - configMapRef:
      name: db-config
```

If the ConfigMap has 10 keys, all 10 become environment variables in the container. Simple, but no selectivity — everything gets injected. [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

**Way 3: As selective environment variables (`env` with `configMapKeyRef`)** — pick specific keys from a ConfigMap and assign them to specific variable names:

```yaml
env:
  - name: PLAYER_INITIAL_LIVES
    valueFrom:
      configMapKeyRef:
        name: game-demo
        key: player_initial_lives
```

Here, `PLAYER_INITIAL_LIVES` is the variable name inside the container, and `player_initial_lives` is the key in the ConfigMap. The instructor notes: "the name of the variable and name of the key are same. Usually I do this to avoid confusion, but here this is the variable and here this is the key in the ConfigMap." They can be different — the variable name in the container doesn't have to match the key name in the ConfigMap. [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

**Way 4: As configuration files in a volume** — mount ConfigMap keys as **files** inside the container. This is the most powerful mechanism and the one the instructor spends the most time on, saying: "This is used a lot — injecting configuration as a volume."

The mechanism works in two parts: [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

**Part 1: Define a volume of type `configMap`** at the pod level:

```yaml
volumes:
  - name: config
    configMap:
      name: game-demo
      items:
        - key: "game.properties"
          path: "game.properties"
        - key: "user-interface.properties"
          path: "user-interface.properties"
```

This creates a volume backed by the ConfigMap. Each `item` maps a ConfigMap key to a filename. The `path` is the filename that will be created — it can be different from the key name, but is typically kept the same.

**Part 2: Mount the volume into the container:**

```yaml
volumeMounts:
  - name: config
    mountPath: "/config"
    readOnly: true
```

The volume named `config` is mounted at `/config` inside the container. The result: two files are created — `/config/game.properties` and `/config/user-interface.properties` — each containing the multi-line content from the corresponding ConfigMap key. [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

🔍 **Deep Dive:**
The volume type here is `configMap` — this is different from the `hostPath` volume type seen in the previous lecture. Kubernetes supports many volume types, and `configMap` is one of them. When a volume is of type `configMap`, Kubernetes populates the volume's filesystem with files derived from the ConfigMap's keys. The `items` field is optional — if omitted, ALL keys in the ConfigMap become files. The `items` field lets you select which keys to materialize as files and what filenames to use.

***

## 1.6 envFrom vs. env — The Critical Distinction

The instructor carefully distinguishes two very similar-looking but functionally different mechanisms: [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

**`envFrom`** (with "From") — injects the **entire ConfigMap** as environment variables. Every key becomes a variable. No selectivity.

**`env`** (without "From") — defines **individual variables**, each with its own `valueFrom: configMapKeyRef` pointing to a specific key. Full selectivity — you choose which keys to import and what to name the variables.

The instructor explicitly highlights this: "envFrom — do you see the difference? envFrom here, env there." The naming difference is subtle but the behavior is completely different.

***

## 1.7 Imperative vs. Declarative ConfigMap Creation

**Imperative (command line):**

```bash
kubectl create configmap db-config --from-literal=MYSQL_DATABASE=accounts --from-literal=MYSQL_ROOT_PASSWORD=vprodbpass
```

Each `--from-literal` adds one key-value pair. The instructor notes: "imperative, command line, which you should avoid but you should anyways know how to do this." [\[337-config-map \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/337-config-map.txt)

**Declarative (YAML file):**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-config
data:
  MYSQL_DATABASE: accounts
  MYSQL_ROOT_PASSWORD: vprodbpass
```

Apply with `kubectl apply -f <file>`. Declarative is preferred for production — it's version-controllable, reviewable, and repeatable.

***

## 1.8 Viewing ConfigMap Contents

**List all ConfigMaps:**

```bash
kubectl get cm
```

**View full content in YAML:**

```bash
kubectl get cm game-demo -o yaml
```

This shows all keys and their values. Multi-line content appears with `\n` newline characters in the YAML output. <cite>turn20search24</cite>

**Describe (human-readable):**

```bash
kubectl describe cm game-demo
```

Shows the content in a readable format.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating a Kubernetes ConfigMap containing both simple variables and multi-line configuration file content, then creating a Pod that consumes the ConfigMap in two ways simultaneously: specific keys as environment variables, and multi-line keys as files mounted in a volume. We then exec into the container to verify both the variables and the files exist with the correct values. <cite>turn20search24</cite><cite>turn20search25</cite>

***

## Step 1: Create the ConfigMap from Documentation Example

Create the ConfigMap definition file:

```bash
vim samplecm.yaml
```

Paste the ConfigMap definition from the Kubernetes documentation: <cite>turn20search24</cite>

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  player_initial_lives: "3"
  ui_properties_file_name: "user-interface.properties"
  game.properties: |
    enemy.types=aliens,monsters
    player.maximum-lives=5
  user-interface.properties: |
    color.good=purple
    color.bad=yellow
    allow.textmode=true
```

**Structure breakdown:**

* `kind: ConfigMap` — the object type
* `metadata.name: game-demo` — the ConfigMap's name (used when referencing it from pods)
* `data:` — not `spec:` (ConfigMaps use `data`, not `spec`)
* Four keys: two simple (scalar values), two multi-line (configuration file content, using the `|` YAML block scalar indicator)

Save and apply: <cite>turn20search25</cite>

```bash
kubectl apply -f samplecm.yaml
```

**Expected output:** `configmap/game-demo created` (or a warning if it already exists from a previous creation).

**Verify:**

```bash
kubectl get cm
```

Should list `game-demo` among the ConfigMaps.

**View full content:**

```bash
kubectl get cm game-demo -o yaml
```

You should see all four keys with their values. Multi-line content will show `\n` characters representing newlines. <cite>turn20search24</cite>

***

## Step 2: Create the Pod That Consumes the ConfigMap

Create the pod definition file:

```bash
vim readcmpod.yaml
```

Paste the pod definition from the documentation — this pod uses the ConfigMap in two ways: <cite>turn20search25</cite><cite>turn20search24</cite>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-demo-pod
spec:
  containers:
    - name: demo
      image: alpine
      command: ["sleep", "3600"]
      env:
        - name: PLAYER_INITIAL_LIVES
          valueFrom:
            configMapKeyRef:
              name: game-demo
              key: player_initial_lives
        - name: UI_PROPERTIES_FILE_NAME
          valueFrom:
            configMapKeyRef:
              name: game-demo
              key: ui_properties_file_name
      volumeMounts:
        - name: config
          mountPath: "/config"
          readOnly: true
  volumes:
    - name: config
      configMap:
        name: game-demo
        items:
          - key: "game.properties"
            path: "game.properties"
          - key: "user-interface.properties"
            path: "user-interface.properties"
```

**What this pod does:** <cite>turn20search24</cite>

1. Runs an Alpine container with `sleep 3600` (keeps the container alive for 1 hour so we can exec into it)
2. **Two environment variables** (`PLAYER_INITIAL_LIVES`, `UI_PROPERTIES_FILE_NAME`) — values pulled from specific ConfigMap keys using `configMapKeyRef`
3. **Two files** (`/config/game.properties`, `/config/user-interface.properties`) — created from ConfigMap keys mounted as a volume

**Apply:**

```bash
kubectl apply -f readcmpod.yaml
```

**Verify:**

```bash
kubectl get pod
```

Should show `configmap-demo-pod` in `Running` state. <cite>turn20search25</cite>

**Common mistake:** If the ConfigMap doesn't exist when the pod starts, the pod will fail to start (status: `CreateContainerConfigError`). Always create the ConfigMap **before** the pod that references it.

***

## Step 3: Exec into the Container and Verify

**Open a shell inside the container:**

```bash
kubectl exec --stdin --tty configmap-demo-pod -- /bin/sh
```

* `kubectl exec` — executes a command inside a running container
* `--stdin` — keeps stdin open (allows typing)
* `--tty` — allocates a pseudo-TTY (gives you a terminal)
* `configmap-demo-pod` — the pod name
* `--` — separates kubectl flags from the command to execute
* `/bin/sh` — the shell to run

**Why `/bin/sh` and not `/bin/bash`?** The container uses the Alpine image, which is minimal and does not include Bash. It only has the basic `sh` shell. The instructor notes: "Alpine image does not have bash shell. It has just sh shell." <cite>turn20search24</cite>

***

## Step 4: Verify the Volume-Mounted Files

Inside the container shell: <cite>turn20search24</cite>

```sh
ls /config
```

**Expected output:** Two files — `game.properties` and `user-interface.properties`.

**View file contents:**

```sh
cat /config/game.properties
```

**Expected:**

```
enemy.types=aliens,monsters
player.maximum-lives=5
```

```sh
cat /config/user-interface.properties
```

**Expected:**

```
color.good=purple
color.bad=yellow
allow.textmode=true
```

These files contain the multi-line content from the ConfigMap keys. The ConfigMap key became the filename, and the key's value became the file content. <cite>turn20search24</cite>

***

## Step 5: Verify the Environment Variables

Still inside the container shell: <cite>turn20search24</cite>

```sh
echo $PLAYER_INITIAL_LIVES
```

**Expected:** `3`

```sh
echo $UI_PROPERTIES_FILE_NAME
```

**Expected:** `user-interface.properties`

These values come from the ConfigMap keys `player_initial_lives` and `ui_properties_file_name`, injected as environment variables via `configMapKeyRef`. <cite>turn20search24</cite>

**Exit the container:**

```sh
exit
```

**Both injection mechanisms are verified:** environment variables work (echo shows the values) and volume-mounted files work (cat shows the content). The ConfigMap is the single source of truth for all four pieces of data, and the pod consumes them through two different mechanisms depending on the data type (simple values as variables, multi-line content as files).

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## ConfigMap = Centralized Configuration Store

```
ConfigMap = collection of key-value pairs
  Simple keys → inject as environment variables
  Multi-line keys → inject as files via volumes

Same pattern as:
  Ansible group_vars/    → variables separate from playbooks
  Terraform .tfvars      → values separate from resource definitions
  Docker Compose .env    → config separate from service definitions
```

## ConfigMap Structure

```yaml
apiVersion: v1
kind: ConfigMap       ← object type
metadata:
  name: game-demo     ← referenced by pods
data:                 ← NOT spec (unique to ConfigMap)
  simple_key: "value"              ← scalar (→ env var)
  config.file: |                   ← multi-line (→ file)
    key1=value1
    key2=value2
```

## Four Ways to Consume ConfigMap Data

```
1. envFrom (entire ConfigMap → all keys become env vars)
   envFrom:
     - configMapRef:
         name: db-config

2. env + configMapKeyRef (selective keys → specific env vars)
   env:
     - name: VAR_NAME
       valueFrom:
         configMapKeyRef:
           name: configmap-name
           key: key-name

3. Volume mount (keys → files in a directory)
   volumes:
     - name: vol
       configMap:
         name: configmap-name
         items:
           - key: "file.properties"
             path: "file.properties"
   volumeMounts:
     - name: vol
       mountPath: "/config"

4. Command line arguments (keys → args to container command)
```

## envFrom vs. env — Critical Difference

```
envFrom:                         env:
  injects ALL keys               injects SELECTED keys
  no renaming                    can rename (variable ≠ key)
  one statement                  one statement per variable

envFrom → bulk import            env → selective import
```

## Volume Mount Mechanism

```
Pod level:
  volumes:
    - name: config              ← volume name
      configMap:
        name: game-demo         ← which ConfigMap
        items:                  ← which keys → which files
          - key: "game.properties"
            path: "game.properties"

Container level:
  volumeMounts:
    - name: config              ← same volume name
      mountPath: "/config"      ← directory in container

Result: /config/game.properties exists with ConfigMap key's content
```

## ConfigMap Creation

```
IMPERATIVE (quick, avoid in production):
  kubectl create configmap db-config \
    --from-literal=MYSQL_DATABASE=accounts \
    --from-literal=MYSQL_ROOT_PASSWORD=vprodbpass

DECLARATIVE (preferred):
  vim configmap.yaml → kubectl apply -f configmap.yaml
```

## ConfigMap Inspection

```
kubectl get cm                          ← list all
kubectl get cm game-demo -o yaml        ← full content (YAML)
kubectl describe cm game-demo           ← human-readable
```

## Exec Into Container

```
kubectl exec --stdin --tty <pod-name> -- /bin/sh

Alpine image → /bin/sh only (no /bin/bash)
Ubuntu image → /bin/bash available

--stdin = keep input open
--tty = terminal mode
-- = separator between kubectl flags and command
```

## Verification Sequence

```
1. kubectl get cm              → ConfigMap exists ✓
2. kubectl get cm -o yaml      → keys and values correct ✓
3. kubectl apply -f pod.yaml   → pod created
4. kubectl get pod             → Running ✓
5. kubectl exec ... -- /bin/sh → inside container
6. ls /config                  → files exist ✓
7. cat /config/game.properties → content matches ConfigMap ✓
8. echo $PLAYER_INITIAL_LIVES  → variable value correct ✓
```

## Pod Definition — Both Injection Methods Combined

```
spec:
  containers:
    - name: demo
      image: alpine
      command: ["sleep", "3600"]     ← keep alive for exec
      env:                           ← METHOD 1: selective env vars
        - name: PLAYER_INITIAL_LIVES
          valueFrom:
            configMapKeyRef:
              name: game-demo
              key: player_initial_lives
      volumeMounts:                  ← METHOD 2: files from volume
        - name: config
          mountPath: "/config"
  volumes:                           ← volume definition (pod level)
    - name: config
      configMap:
        name: game-demo
        items:
          - key: "game.properties"
            path: "game.properties"
```

## Dependency Order

```
ConfigMap MUST exist BEFORE pod that references it
  Pod references non-existent ConfigMap → CreateContainerConfigError

CREATE ORDER:
  1. kubectl apply -f configmap.yaml
  2. kubectl apply -f pod.yaml

Same as: Ansible variables must be defined before tasks use them
```

## Data Types in ConfigMap

```
Simple key:      player_initial_lives: "3"
                 → best consumed as: environment variable

Multi-line key:  game.properties: |
                   enemy.types=aliens,monsters
                   player.maximum-lives=5
                 → best consumed as: file via volume mount
```

## Volume Type: configMap (vs. hostPath)

```
Previous lecture:  volumes type = hostPath (host filesystem)
This lecture:      volumes type = configMap (ConfigMap data)

configMap volume: Kubernetes creates files from ConfigMap keys
  items field: select which keys → which filenames
  items omitted: ALL keys become files
```

## Reusable Engineering Patterns

**1. Centralized Configuration, Distributed Consumption**

```
ONE ConfigMap → injected into MANY pods
Change ConfigMap → all pods get updated config (on restart)

Same pattern:
  Ansible group_vars/all → all hosts get same variables
  Terraform variables → all modules reference same values
  Docker Compose .env → all services read same file
```

**2. Two Injection Channels for Two Data Types**

```
Scalar data (simple values) → environment variables
  → consumed via: $VARIABLE_NAME in application code

Structured data (multi-line config) → mounted files
  → consumed via: file path in application config reader

Match injection method to data shape
Same principle: Docker ENV for scalars, COPY for config files
```

**3. Documentation-Driven Development (Kubernetes Pattern)**

```
"We'll go to documentation and find out"
"Let's take it, let's copy that, let's create it"

Workflow: docs → copy example → modify for your use case → apply
Not: memorize everything → write from scratch

ConfigMap, Deployment, Service → all follow same workflow
```

***

*This completes the full reconstruction. Theory explains the four ConfigMap consumption methods and the critical envFrom vs. env distinction. Practical walks through creating a ConfigMap, creating a pod that uses both environment variables and volume-mounted files, and verifying both inside the container. The Compression Map enables instant recall of the four injection methods, the volume mount mechanism, the dependency order, and the data-type-to-injection-method matching principle.* <cite>turn20search24</cite><cite>turn20search25</cite>
