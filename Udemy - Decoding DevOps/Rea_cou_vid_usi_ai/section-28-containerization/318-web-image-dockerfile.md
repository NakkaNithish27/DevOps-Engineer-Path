# 🧠 Docker Web Image Dockerfile — Nginx Custom Image, Official Image Reuse & Configuration Injection Patterns

**Source:** *318. Web Image Dockerfile* — Docker / Containerization Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: Nginx Needs Custom Configuration

In the vProfile containerization project, Nginx serves as the **reverse proxy** — it receives HTTP requests on port 80 and routes them to the Tomcat application container on port 8080. In a previous lecture, this was set up manually: install Nginx, replace the default configuration file with a custom one that defines the routing rule. Now, this manual process must be captured in a **Dockerfile** so the Nginx setup becomes a reproducible, portable Docker image.

The core challenge is simple but architecturally instructive: the official Nginx Docker image from Docker Hub already has Nginx installed and running. The only thing that needs to change is the **configuration file** — specifically, replacing the default Nginx config with a custom one that says "route port 80 traffic to the Tomcat backend on port 8080." Understanding how to make this single change reveals important Docker image design patterns.

***

## 1.2 Two Strategies for Configuration Injection — Build-Time vs. Runtime

The instructor identifies two fundamentally different approaches to getting custom configuration into a Docker container, and this distinction is one of the most important architectural decisions in Docker image design:

### Strategy 1: Build-Time Injection (Bake Into the Image)

Copy the configuration file into the image during the `docker build` process using the `COPY` instruction. The resulting image **contains** the configuration permanently. Every container launched from this image has the same configuration baked in.

**When to use:** When the configuration is **stable and doesn't change frequently**. The instructor's reasoning for choosing this approach: *"Our configuration is straightforward, just route the request to the Tomcat container, and we don't have any other changes in that. So it's better we put the configuration and build the image directly and keep it in our repository."*

### Strategy 2: Runtime Injection (Volume Mount)

Use the default official image without modification. When running the container, mount the configuration file as a **volume** at the correct path inside the container, overriding the default configuration at runtime.

**When to use:** When the configuration **changes regularly**. The instructor notes: *"This is required when you regularly change the configuration."* With volume mounting, you can change the configuration file on the host and restart the container — no image rebuild needed.

The instructor explicitly states both approaches exist: *"There are always two ways. You can either have an image with the configuration loaded in that, or you can take the default Nginx image from Docker Hub and when you run the container, at that time in the runtime, you can inject the configuration."*

For this project, **Strategy 1 (build-time)** is chosen because the configuration is static.

> 🔍 **Deep Dive:** This build-time vs. runtime decision is a fundamental pattern in container engineering. Build-time injection produces **immutable images** — every instance is identical, which is great for reproducibility and deployment confidence. Runtime injection produces **flexible containers** — the same image can behave differently based on what's mounted, which is great for environment-specific configuration (dev/staging/prod using the same image with different configs). In production, both patterns are commonly combined: application code is baked in (build-time), while environment-specific secrets and configs are injected at runtime (via volumes or environment variables).

***

## 1.3 The Nginx Dockerfile — Three Instructions

The Dockerfile for the Nginx web image is remarkably simple — only three meaningful instructions beyond the base image:

```dockerfile
FROM nginx
LABEL ...
LABEL ...
RUN rm -rf /etc/nginx/conf.d/default.conf
COPY nginxvproapp.conf /etc/nginx/conf.d/vproapp.conf
```

### `FROM nginx`

Uses the **official Nginx image** from Docker Hub as the base. No tag is specified, so Docker uses the **`:latest`** tag by default. The instructor acknowledges this: *"I don't mention any tags, so it is going to take the latest. It's going to use the latest tag, and that is fine."*

### `RUN rm -rf /etc/nginx/conf.d/default.conf`

**Removes the default Nginx configuration file.** The official Nginx image ships with a default configuration that serves a welcome page. This default must be removed before the custom configuration is added; otherwise, both configurations would exist and could conflict. The path `/etc/nginx/conf.d/default.conf` is documented in the official Nginx Docker image documentation.

The `rm -rf` flags: `-r` for recursive (in case of directories), `-f` for force (don't prompt, don't error if file doesn't exist).

### `COPY nginxvproapp.conf /etc/nginx/conf.d/vproapp.conf`

**Copies the custom configuration file** from the build context into the image at the Nginx configuration directory. The custom configuration file (`nginxvproapp.conf`) contains the routing rule: requests arriving on port 80 are forwarded to the backend container named `vproapp` on port 8080.

The instructor explains the build process: *"When I build this image, it is going to run the container, remove this configuration file, copy your configuration file, and give us an image with this configuration in that."*

***

## 1.4 The Configuration File — Container Name Dependency

The custom Nginx configuration references the Tomcat backend by **container name**: `vproapp`. This means when the containers are actually run, the Tomcat container **must** be named `vproapp` — otherwise, Nginx won't be able to resolve the backend hostname and routing will fail.

The instructor flags this explicitly: *"It needs to be routed to the container with the name vproapp. So we need to make sure the Tomcat container, when we run in the runtime, its name should be vproapp."* This is a runtime contract that must be honored when running the containers (via Docker Compose in the next lecture).

> 🔍 **Deep Dive:** In Docker networking, containers on the same Docker network can reach each other by **container name** as a hostname. Docker's internal DNS resolves the container name to its IP address. This is why the Nginx config uses `vproapp` as the backend server name — it relies on Docker's built-in service discovery. If the Tomcat container has a different name, the DNS lookup fails and Nginx returns a 502 Bad Gateway error.

***

## 1.5 Official Images That Need No Customization — Memcached

Not every service needs a custom Dockerfile. **Memcached** is the first example of a service that can be used **directly from its official Docker Hub image** with zero modifications.

The instructor walks through the reasoning: *"How did we set up memcache? We just install memcache, we started the service. That's all."* There is no custom configuration needed, and there is no persistent data to manage — memcache stores everything in runtime memory. The official Memcached image already handles installation and startup.

The instructor verifies by examining the official Memcached Dockerfile on Docker Hub, noting: *"You see there is exposed 11211 port. That's what we need. Memcache runs on port 11211."* This matches the `application.properties` file of the vProfile project, which specifies Memcached on port 11211. Everything aligns — no custom Dockerfile needed.

***

## 1.6 Official Images That Need No Customization — RabbitMQ

**RabbitMQ** initially appears to need customization — in the manual setup, a custom user (`test`) was created with administrator privileges. However, the instructor discovers that the **application configuration** (`application.properties`) actually specifies the default credentials: username `guest`, password `guest`.

The official RabbitMQ Docker image uses `guest`/`guest` as default credentials. The instructor confirms: *"The RabbitMQ default user, you can mention the username. If you don't mention, it will be guest."* Since the application's source code configuration already expects `guest`/`guest`, the default RabbitMQ image works without any modification.

The instructor also notes that if you needed different credentials, you could set **environment variables** when running the container (`RABBITMQ_DEFAULT_USER`, `RABBITMQ_DEFAULT_PASS`) — another form of runtime configuration injection. But for this project, the defaults match the application requirements.

RabbitMQ runs on default port **5672**, which matches the application's configuration.

***

## 1.7 The Complete Image Inventory — What Needs Custom Dockerfiles vs. What Doesn't

The instructor summarizes the entire project's image strategy:

| Service          | Custom Dockerfile?        | Reason                                                             |
| ---------------- | ------------------------- | ------------------------------------------------------------------ |
| **App (Tomcat)** | ✅ Yes                     | Custom application deployment, build process                       |
| **DB (MySQL)**   | ✅ Yes                     | Custom schema, initial data                                        |
| **Web (Nginx)**  | ✅ Yes                     | Custom routing configuration                                       |
| **Memcached**    | ❌ No — use official image | No config changes, no data, port 11211 matches                     |
| **RabbitMQ**     | ❌ No — use official image | Default user `guest`/`guest` matches app config, port 5672 matches |

This creates a clear division: **three custom Dockerfiles** (app, db, web) and **two official images** (memcached, rabbitmq). The next lecture brings them all together in a **Docker Compose file** that builds the custom images and runs all five containers together.

> ⚠️ **Expert Note:** The decision to use official images directly versus creating custom Dockerfiles is a significant engineering judgment. The instructor's method is sound: check what the manual setup required, compare it against what the official image provides by default, verify that ports and credentials match the application's configuration, and only write a custom Dockerfile if there's an actual gap. This avoids unnecessary image maintenance and leverages the community's work on official images (security patches, updates, best practices).

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a **custom Nginx Docker image** that acts as a reverse proxy, routing HTTP requests on port 80 to the Tomcat application container (`vproapp`) on port 8080. We also evaluate the remaining services (Memcached, RabbitMQ) and determine they need no custom Dockerfiles. By the end, the complete image inventory for the vProfile containerization project is finalized.

**Final outcome:** A Dockerfile for the Nginx web image that produces a custom image with baked-in routing configuration, plus the confirmed decision to use official images for Memcached and RabbitMQ.

***

## Step 1: Review the Nginx Configuration File

Navigate to the Docker files folder → `web/` directory. Two files exist here:

* An empty Dockerfile (to be written)
* The Nginx configuration file (`nginxvproapp.conf`)

Examine the configuration:

```bash
cat nginxvproapp.conf
```

**Key content:** The configuration specifies that requests arriving on **port 80** should be routed to the backend server named **`vproapp`** on **port 8080**.

**Critical runtime dependency:** The Tomcat container must be named `vproapp` when running. This is handled in the Docker Compose file (next lecture), not here. For now, just note the requirement.

***

## Step 2: Write the Nginx Dockerfile

In the `web/` directory, create the Dockerfile:

```dockerfile
FROM nginx
LABEL project="vprofile"
LABEL maintainer="<your-info>"
RUN rm -rf /etc/nginx/conf.d/default.conf
COPY nginxvproapp.conf /etc/nginx/conf.d/vproapp.conf
```

**Line-by-line breakdown:**

**`FROM nginx`**

* Base image: official Nginx from Docker Hub.
* No tag specified → uses `:latest` by default.
* Provides Nginx fully installed and configured to start automatically.

**`LABEL project="vprofile"` / `LABEL maintainer="..."`**

* Metadata labels for identification. Same labels used across all project Dockerfiles for consistency.

**`RUN rm -rf /etc/nginx/conf.d/default.conf`**

* Removes the default Nginx site configuration.
* `rm` — remove command.
* `-r` — recursive (handles directories).
* `-f` — force (no confirmation prompt, no error if file doesn't exist).
* `/etc/nginx/conf.d/default.conf` — the default configuration file path (documented in the official Nginx Docker image).
* **Why:** The default config serves a welcome page. It must be removed to avoid conflicts with the custom configuration.

**`COPY nginxvproapp.conf /etc/nginx/conf.d/vproapp.conf`**

* Copies the custom configuration from the build context (local file) into the image.
* Source: `nginxvproapp.conf` (must exist in the same directory as the Dockerfile, or in the build context).
* Destination: `/etc/nginx/conf.d/vproapp.conf` — Nginx reads all `.conf` files in this directory.

**What happens during `docker build`:** Docker pulls the Nginx base image → creates a temporary container → executes `rm -rf` to delete the default config → executes `COPY` to place the custom config → commits the result as a new image layer.

**Save the Dockerfile.**

***

## Step 3: Verify Memcached — No Custom Dockerfile Needed

Check the official Memcached image on Docker Hub:

1. Search for `memcached` on Docker Hub.
2. Verify the exposed port: **11211** — matches the `application.properties` file.
3. Verify no configuration changes are needed for the vProfile project.
4. Verify no persistent data setup is needed (Memcached stores everything in memory at runtime).

**Decision:** Use the official `memcached` image directly. No Dockerfile required.

**How to find the official Dockerfile:** On the Docker Hub page, click on one of the tags — it links to the Dockerfile used to build that image. You can inspect the `EXPOSE 11211` instruction there.

***

## Step 4: Verify RabbitMQ — No Custom Dockerfile Needed

Check the official RabbitMQ image on Docker Hub:

1. Search for `rabbitmq` on Docker Hub.
2. Verify the default port: **5672** — matches the `application.properties` file.
3. Check default credentials: **username `guest`, password `guest`** — matches the application configuration.
4. Note: if different credentials were needed, environment variables could be set at runtime:
   * `RABBITMQ_DEFAULT_USER=<username>`
   * `RABBITMQ_DEFAULT_PASS=<password>`
     But for this project, the defaults match.

**Decision:** Use the official `rabbitmq` image directly. No Dockerfile required.

**Verification method:** Compare the values in the official image documentation against the values in the project's `application.properties` file. If they match → no customization needed.

***

## Step 5: Confirm the Complete Image Inventory

At this point, all image decisions are finalized:

| Service      | Image Source         | Dockerfile Location           |
| ------------ | -------------------- | ----------------------------- |
| App (Tomcat) | Custom build         | `Docker-files/app/Dockerfile` |
| DB (MySQL)   | Custom build         | `Docker-files/db/Dockerfile`  |
| Web (Nginx)  | Custom build         | `Docker-files/web/Dockerfile` |
| Memcached    | Official `memcached` | None needed                   |
| RabbitMQ     | Official `rabbitmq`  | None needed                   |

**Connection to flow:** The next lecture creates a **Docker Compose file** that:

* Builds the three custom images from their Dockerfiles
* Pulls the two official images from Docker Hub
* Runs all five containers together on the same network
* Ensures the Tomcat container is named `vproapp` (satisfying the Nginx config dependency)

> ⚠️ **Expert Note:** The decision process demonstrated here — check manual setup steps → compare against official image defaults → verify port and credential alignment with application config → decide custom vs. official — is the standard evaluation workflow for any containerization project. Always check the official image first before writing a custom Dockerfile.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Nginx Dockerfile — Complete Structure

```dockerfile
FROM nginx                                          # official base, :latest
LABEL project="vprofile"                            # metadata
LABEL maintainer="..."                              # metadata
RUN rm -rf /etc/nginx/conf.d/default.conf           # remove default config
COPY nginxvproapp.conf /etc/nginx/conf.d/vproapp.conf  # inject custom config
```

```
BUILD PROCESS:
  Pull nginx:latest → remove default.conf → copy custom conf → commit image
  
RESULT: Nginx image with routing rule:
  port 80 → backend container "vproapp" : port 8080
```

***

## Two Configuration Injection Strategies

```
STRATEGY 1: BUILD-TIME (chosen for this project)
  COPY config into image during docker build
  Image CONTAINS config permanently
  USE WHEN: config is STABLE, doesn't change frequently

STRATEGY 2: RUNTIME
  Mount config as VOLUME during docker run
  Image uses default, volume overrides at runtime
  USE WHEN: config CHANGES regularly, environment-specific configs

DECISION: vProfile Nginx config is static → build-time injection
```

***

## Container Name Dependency Chain

```
Nginx config file
  → routes to backend server: "vproapp"
    → Docker DNS resolves "vproapp" to container IP
      → Tomcat container MUST be named "vproapp" at runtime
        → enforced in Docker Compose file (next lecture)

IF name mismatch: Nginx DNS lookup fails → 502 Bad Gateway
```

***

## Image Decision Matrix (Complete Project)

```
SERVICE      CUSTOM?   WHY / WHY NOT
─────────    ───────   ────────────────────────────────────
App/Tomcat   ✅ YES    Custom app deployment, build process
DB/MySQL     ✅ YES    Custom schema, initial data
Web/Nginx    ✅ YES    Custom routing configuration
Memcached    ❌ NO     No config changes, no data, port 11211 matches
RabbitMQ     ❌ NO     Default guest/guest matches app config, port 5672 matches

TOTAL: 3 custom Dockerfiles + 2 official images = 5 services
```

***

## Official Image Evaluation Workflow

```
1. How was the service set up MANUALLY?
     → install, start, configure, data?

2. What does the OFFICIAL IMAGE provide?
     → check Docker Hub: ports, default config, default credentials

3. Does the app's configuration (application.properties) MATCH?
     → ports match? credentials match? paths match?

4. DECISION:
     ALL match → use official image directly
     GAP exists → write custom Dockerfile (or use env vars / volumes)
```

***

## Memcached Evaluation

```
Manual setup: install → start → DONE
Official image: memcached → port 11211 exposed → no config needed
App config: memcached port 11211 ✅
Data: runtime memory only (no persistence needed)
→ USE OFFICIAL IMAGE
```

***

## RabbitMQ Evaluation

```
Manual setup: install → start → create user "test" → admin tag
Official image: rabbitmq → port 5672 → default user guest/guest
App config: rabbitmq user=guest, password=guest ✅ (matches default)
Custom user needed? NO (app uses guest)
If needed: set env vars RABBITMQ_DEFAULT_USER / RABBITMQ_DEFAULT_PASS
→ USE OFFICIAL IMAGE
```

***

## Nginx Configuration Path Reference

```
Default config (to remove):  /etc/nginx/conf.d/default.conf
Custom config (to place):    /etc/nginx/conf.d/vproapp.conf

Source: documented in official Nginx Docker Hub page
```

***

## Project Progress — Image Layer Complete

```
✅ App Dockerfile (Tomcat + vProfile)
✅ DB Dockerfile (MySQL + schema + data)
✅ Web Dockerfile (Nginx + custom routing config)    ← THIS LECTURE
✅ Memcached → official image (no Dockerfile)
✅ RabbitMQ → official image (no Dockerfile)

NEXT: Docker Compose file
  → builds 3 custom images
  → pulls 2 official images
  → runs 5 containers on same network
  → names Tomcat container "vproapp" (Nginx dependency)
```

***

## Reusable Engineering Pattern: Evaluate Before Customize

```
PATTERN:
  Before writing ANY custom Dockerfile:
    1. Check if an official image exists
    2. Compare its defaults against your requirements
    3. Only customize what the official image doesn't provide

DECISION TREE:
  Official image exists?
    YES → ports/config/credentials match app requirements?
      YES → use official image directly (ZERO maintenance)
      PARTIALLY → inject via env vars or volumes at runtime
      NO → write custom Dockerfile extending official image
    NO → write Dockerfile from base OS image

WHY:
  Official images = maintained by community (security patches, updates)
  Custom Dockerfiles = YOUR maintenance burden
  Less custom code = less to maintain = fewer bugs

WHERE ELSE:
  • Helm charts: use official charts, override values.yaml
  • Ansible roles: use Galaxy roles, customize variables
  • Terraform modules: use registry modules, set input variables
  • Any tool ecosystem: prefer official + configure over build-from-scratch
```

***

## One-Line Mental Reload Trigger

> *"Nginx Dockerfile: FROM nginx, RUN rm default.conf, COPY custom config (routes to 'vproapp':8080) — Memcached and RabbitMQ use official images directly (ports and default credentials match app config) — always evaluate official image defaults before writing custom Dockerfiles."*

This single sentence reconstructs the complete Nginx Dockerfile structure, the configuration routing target and its container name dependency, both official image decisions with their justification, and the core engineering principle of the entire lecture. [\[318-web-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/318-web-image-dockerfile.txt), [\[135. DNS Route 53 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/135.%20DNS%20Route%2053.txt)
