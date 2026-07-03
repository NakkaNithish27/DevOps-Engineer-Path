# 🎓 Deep Learning Material: Deploying a Microservice Application (EMart) with Docker Compose

*Reconstructed from video lecture captions and supporting configuration files*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Is a Microservice Application and Why Does It Matter Here?

The entire lecture revolves around deploying an application called **EMart** — an e-commerce application comparable to Amazon or Flipkart. The critical teaching point is that EMart is designed using **microservice architecture**, which is fundamentally different from the **monolithic architecture** seen in the earlier vProfile project. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

In a monolithic application (like vProfile), the entire application is a single deployable unit — one codebase, one build artifact, one running process that contains all functionality. If you need to change one feature, you redeploy the entire application. In a microservice application, the system is decomposed into **independent services**, each responsible for a specific business capability, each potentially written in a different programming language, each with its own database, and each deployable independently. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

EMart demonstrates this concretely: the frontend is written in **Angular**, one API service is written in **NodeJS**, another API service is written in **Java**, and there are two separate databases — **MongoDB** and **MySQL** — each owned by a different service. These are not arbitrary technology choices; they reflect the microservice principle that each team or service picks the technology best suited for its job. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

The instructor explicitly states that this architecture is **highly scalable from a developer point of view** — you can keep adding more microservices (videos, payment gateway, cart) as independent units without touching existing services. This is the core advantage: independent scalability, independent deployment, and technology heterogeneity. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

🔍 **Deep Dive:**
The comparison between vProfile (monolithic) and EMart (microservice) is architecturally significant. In the vProfile Docker Compose file, all services (MySQL, Memcached, RabbitMQ, Tomcat app, Nginx web) form a single application stack where the Tomcat app is the monolithic core that handles everything.  In EMart, there is no single "core" — each service is an independent unit behind a gateway. The deployment method is identical (Docker Compose), but the **architectural intent** is fundamentally different. This teaches a crucial lesson: Docker Compose is tool-agnostic to architecture — it orchestrates containers regardless of whether the system is monolithic or microservice. [\[83.docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.docker-compose.txt)

***

## 1.2 The EMart Application Architecture

The EMart architecture has a clear layered structure with an **API Gateway pattern** at its core. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Nginx** acts as the **API Gateway** — it is the single entry point for all external traffic. It listens on **three endpoints**: [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

* **`/` (root)** → Routes to the **Angular** client application (the frontend/UI)
* **`/api`** → Routes to **Mart API**, a NodeJS application, which connects to a **MongoDB** database
* **`/webapi`** → Routes to **Books API**, a Java application, which connects to a **MySQL** database

This is a textbook API Gateway pattern. The user never directly contacts any backend service. Every request goes through Nginx, which decides where to route it based on the URL path. This provides a single, unified interface to a collection of heterogeneous services behind it. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

The six containers that run in the final system are: [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

1. **Nginx** — API Gateway / reverse proxy
2. **Angular client** — Frontend application (served through root `/`)
3. **NodeJS Mart API** — Backend service for the main marketplace
4. **MongoDB** — Database for the NodeJS Mart API
5. **Java Books API** — Backend service for the book section
6. **MySQL (emartdb)** — Database for the Java Books API

Each service-database pair is **independent** — the NodeJS service knows nothing about MySQL, and the Java service knows nothing about MongoDB. They are connected only through the gateway layer.

🔍 **Deep Dive:**
The instructor mentions that MongoDB is deployed as a container here, but emphasizes it **could be an independent service running from a server or any other endpoint**.  This is an important architectural insight: in microservice deployments, the database doesn't have to be co-located with its service. In production, databases are often managed services (AWS RDS, MongoDB Atlas) while application containers run on orchestration platforms. The Docker Compose setup here is a development/demo convenience, not a production prescription. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

⚠️ **Expert Note:**
The three-endpoint routing (`/`, `/api`, `/webapi`) is simple here, but in real production API gateways (Kong, AWS API Gateway, Envoy), you'd also handle authentication, rate limiting, load balancing, circuit breaking, and request transformation at this layer. Nginx here is acting as a lightweight gateway — sufficient for demo, but production gateways carry much more responsibility.

***

## 1.3 Docker Compose: Build vs. Pull — Two Modes of Container Creation

The instructor highlights a critical conceptual difference between the vProfile Docker Compose file and the EMart Docker Compose file. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

In the **vProfile compose file**, every service specifies an `image:` directive — it pulls pre-built images from Docker Hub (e.g., `vprocontainers/vprofiledb`, `memcached`, `rabbitmq`, `vprocontainers/vprofileapp`, `vprocontainers/vprofileweb`).  This is the **pull-and-run** model: images already exist in a registry; Docker just downloads and runs them. [\[83.docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.docker-compose.txt)

In the **EMart compose file**, there is an additional `build:` directive.  This tells Docker Compose to **build images locally from Dockerfiles** present in the source code, and then run containers from those freshly built images. This is the **build-and-run** model. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

Docker Compose supports both modes:

* **`image:`** → Fetch from registry, run
* **`build:`** → Build from Dockerfile in source code, run

And it can do both in a single compose file — some services can be pulled, others can be built. This is why the instructor says: *"Docker compose can do this also, can build image, and then run containers from that. Or you can mention the image path."* [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

This is why the EMart deployment requires **cloning the full source code** — the Dockerfiles and application source are needed to build the images locally. The vProfile project didn't need source code because all images were pre-built and available on Docker Hub. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

🔍 **Deep Dive:**
When Docker Compose encounters a `build:` directive, it internally runs `docker build` using the Dockerfile at the specified path. The build process reads the Dockerfile instructions (FROM, COPY, RUN, etc.), creates intermediate layers, and produces a final image. This is computationally expensive — especially for NodeJS images where `npm install` downloads and compiles many dependencies, which is why the instructor warns that *"this is going to take a very long time because it's going to build the images and there are NodeJS images over here and that takes long time to build."* [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

***

## 1.4 The Restart Policy: Self-Healing Container Behavior

The instructor makes an important observation about container failure handling: *"Sometimes for some reason the container will get exit into exit state. And don't worry, this composed file will handle it automatically — if any container goes into exit state, it is going to restart those containers and make sure they run."* [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

This refers to the **restart policy** in Docker Compose. When a service definition includes a restart policy (such as `restart: always` or `restart: on-failure`), Docker's daemon monitors the container and automatically restarts it if it exits. This is a form of **self-healing** — the system recovers from transient failures without human intervention. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

This is operationally significant in microservice deployments because with six interdependent containers, startup order matters. If the NodeJS API container starts before MongoDB is ready to accept connections, the API might crash. With a restart policy, it will simply restart and retry until MongoDB becomes available. This is a common pattern: **retry through restart** instead of complex dependency orchestration.

⚠️ **Expert Note:**
In production, restart policies are a basic safety net but not a substitute for proper health checks, readiness probes, and dependency management. Kubernetes provides liveness probes and readiness probes for much more sophisticated self-healing. Docker Compose restart policies are effective for development and simple deployments but can mask underlying problems if a container keeps crash-looping.

***

## 1.5 The Infrastructure Layer: Vagrant as the VM Provider

The entire deployment happens inside a **Vagrant-managed virtual machine** running **Ubuntu Focal 64-bit** (20.04 LTS). [\[83.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.Vagrantfile.txt)

The Vagrantfile serves two purposes:

**1. VM provisioning:** It creates a VirtualBox VM with a private network IP (`192.168.56.82`) and a public (bridged) network interface. The private network allows the host machine to access the VM at a predictable IP address, which is how the instructor accesses the EMart application from a browser. [\[83.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.Vagrantfile.txt)

**2. Automated Docker installation:** The shell provisioner in the Vagrantfile automatically installs Docker Engine, Docker CLI, containerd, the Docker Buildx plugin, and the Docker Compose plugin during `vagrant up`. It also installs the standalone `docker-compose` binary (v2.1.1) separately. [\[83.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.Vagrantfile.txt)

This means every time you destroy and recreate the VM, you get a **clean, reproducible environment** with Docker pre-installed. The Vagrantfile is the **infrastructure-as-code** layer beneath the container orchestration layer.

🔍 **Deep Dive:**
The Vagrantfile installs Docker in two ways: the Docker Compose **plugin** (via `docker-compose-plugin` apt package, invoked as `docker compose` — two words) and the standalone **binary** (via direct download to `/usr/local/bin/docker-compose`, invoked as `docker-compose` — hyphenated).   This dual installation ensures compatibility — some older tutorials and scripts use the hyphenated form, while the modern approach uses the plugin form. The instructor uses `docker compose` (plugin form) in the actual commands. [\[83.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.Vagrantfile.txt) [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

***

## 1.6 Microservice Scalability: The Extensibility Principle

The instructor explicitly states that the EMart application *"can start like this and you can keep adding more microservices — like maybe another URL for videos, another URL for payment gateway, another URL for cart."* [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

This is the core extensibility principle of microservice architecture: **new capabilities are added as new services behind the gateway, not by modifying existing services**. The gateway (Nginx) simply gets a new route (e.g., `/videos`, `/payment`, `/cart`), and a new independent service handles that route. Existing services remain untouched.

This is architecturally powerful because:

* New teams can work on new services independently
* New services can use any technology stack
* Deployment of new services doesn't require redeploying existing ones
* Failure of a new service doesn't crash existing services

This contrasts sharply with monolithic architecture where adding a new feature means modifying the same codebase, redeploying the same artifact, and risking regression in existing features.

***

## 1.7 Docker Compose as the Unifying Deployment Tool

A subtle but important teaching point in this lecture is that **Docker Compose is the same tool for both monolithic and microservice deployments**.  The instructor explicitly draws the parallel: *"It'll be similar how we have seen for vProfile Project. vProfile was monolithic, this is microservice. But from implementing point of view, we'll have a similar thing — we'll have Docker and we'll have Docker Compose."* [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

The tool doesn't change. The `docker compose up -d` command is identical. The `docker compose down` command is identical. What changes is:

* The **compose file content** (services, build directives, networking)
* The **architectural intent** (single app stack vs. independent services)
* The **source code requirement** (pre-built images vs. local builds)

This teaches a transferable mental model: **the deployment tool is an orchestration layer that is agnostic to the application architecture**. Whether you're deploying one monolithic app with supporting services, or six independent microservices, the orchestration primitive is the same — define services, define their relationships, bring them up.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are deploying the **EMart microservice e-commerce application** on a local virtual machine using Docker Compose. The final outcome is a fully running web application accessible from a browser, consisting of six containers: Nginx (gateway), Angular (frontend), NodeJS API, MongoDB, Java Books API, and MySQL. The entire process — from VM creation to application access to cleanup — is covered. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

***

## Step 1: Prepare the Virtual Machine Environment

Before any Docker work, we need a running VM with Docker installed.

The Vagrantfile from the previous lecture is reused. It lives in a directory (the instructor's path: `F/container/intro/`). If you don't have this Vagrantfile, download it from the course resources and place it in your working folder. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

### 1a. Clean Up Stale Vagrant State

```bash
vagrant global-status --prune
```

**Breakdown:**

* `vagrant global-status` — Lists all Vagrant-managed VMs across your system, regardless of which directory you're in
* `--prune` — Removes entries for VMs that no longer exist on disk (stale/orphaned entries)

**Why:** Before bringing up a VM, ensure no conflicting VMs are running. The instructor checks that all other VMs from previous lectures are powered off to avoid resource contention (CPU, memory, network conflicts). [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Verification:** The output shows a table of VMs with their state. All non-relevant VMs should show `poweroff` or not appear at all.

### 1b. Bring Up the VM

```bash
vagrant up
```

**What happens internally:** Vagrant reads the Vagrantfile, creates (or starts) the VirtualBox VM with Ubuntu Focal 64, assigns the private network IP `192.168.56.82`, and runs the shell provisioner that installs Docker Engine, Docker CLI, containerd, Docker Buildx plugin, Docker Compose plugin, and the standalone docker-compose binary. [\[83.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.Vagrantfile.txt)

**Verification:** The command completes without errors. The provisioner output shows successful `apt-get install` operations.

**Common failure:** If the VM was already created but halted, `vagrant up` simply starts it without re-provisioning. If Docker is missing, you may need `vagrant provision` to re-run the provisioner.

### 1c. Log In and Switch to Root

```bash
vagrant ssh
```

Then inside the VM:

```bash
sudo -i
```

**Breakdown:**

* `vagrant ssh` — Opens an SSH session into the running VM
* `sudo -i` — Switches to the root user with a login shell (sets root's environment variables)

**Why root:** Docker commands require root privileges unless the user is added to the `docker` group. The instructor uses root throughout for simplicity. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

***

## Step 2: Clone the EMart Application Source Code

```bash
git clone https://github.com/devopshydclub/emartapp.git
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**Breakdown:**

* `git clone` — Downloads the complete repository (all files, history, branches) from the remote URL
* `https://github.com/devopshydclub/emartapp.git` — The GitHub repository URL for the EMart application

**Why we need the source code:** Unlike the vProfile project where pre-built images were pulled from Docker Hub, the EMart Docker Compose file uses `build:` directives that reference **Dockerfiles in the source code**. Without the source code, Docker Compose cannot build the images.  (See Theory Section 1.3 for the conceptual explanation.) [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Verification:**

```bash
ls
```

You should see an `emartapp` folder. [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

### 2a. Navigate Into the Project

```bash
cd emartapp/
ls
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**Expected contents:** You'll see the `docker-compose.yaml` file along with directories for each microservice (containing their respective Dockerfiles and source code).

***

## Step 3: Examine the Docker Compose File

```bash
vim docker-compose.yaml
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**Why examine it:** Before running any deployment, you should understand what it will do. The instructor opens the file to show the key difference from the vProfile compose file — the presence of `build:` directives alongside service definitions. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**What you'll see inside:**

* Services defined: `client` (Angular), `api` (NodeJS Mart API), `webapi` (Java Books API), `nginx`, `emongo` (MongoDB), `emartdb` (MySQL)
* `build:` directives pointing to subdirectories containing Dockerfiles
* Port mappings (notably Nginx on port `80`)
* The Nginx container is the only one exposed externally on port 80

**Connection to architecture:** The six services in the compose file directly map to the six components in the architecture diagram discussed in Theory Section 1.2.

Exit vim with `:q` after inspection.

### 3a. Verify Clean State

```bash
docker images
docker ps -a
```

**Why:** The instructor confirms there are no existing images or containers from previous work. This was achieved by the cleanup done at the end of the previous lecture. Starting from a clean state ensures no conflicts or stale artifacts. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Expected output:** Empty lists for both commands.

***

## Step 4: Build and Run All Containers

```bash
docker compose up -d
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**Breakdown:**

* `docker compose` — Invokes the Docker Compose plugin
* `up` — Creates and starts all services defined in the `docker-compose.yaml` file in the current directory
* `-d` — Detached mode: containers run in the background, freeing the terminal

**What happens internally:** Docker Compose reads the YAML file, sees `build:` directives, executes `docker build` for each service that needs building (using Dockerfiles from the cloned source), creates images, creates a Docker network for inter-container communication, and starts all six containers. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Time expectation:** This takes a **very long time** because it's building images from scratch. NodeJS images in particular are slow due to `npm install` downloading and compiling dependencies. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Alternative if the single command fails:**

```bash
docker compose build
```

Run the build step separately first. Once all images are built successfully:

```bash
docker compose up -d
```

Then bring up the containers from the already-built images. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Why this alternative exists:** If a build fails midway (network issues, dependency failures), separating build from run lets you retry the build without affecting container state. It also provides clearer error output since build logs and runtime logs are not interleaved.

**Verification:** Wait for the command to complete. All six images should be built and all six containers should start.

***

## Step 5: Verify Container Status

```bash
docker compose ps
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**What this shows:** Lists all containers managed by the current Docker Compose project, their state (running/exited), and port mappings.

**Expected output:** Six containers, all in `running` state.

**Additional verification:**

```bash
docker ps -a
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**Why `-a`:** This shows ALL containers, including those in `exited` state. If any container has exited, it will appear here. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**If a container is in exited state:** Don't panic. The compose file's restart policy will automatically restart exited containers. Check again after a few seconds. If it persists, check logs with `docker compose logs <service_name>`. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

***

## Step 6: Get the VM's IP Address

```bash
ip addr show
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**Why:** You need the VM's IP address to access the application from your host machine's browser. The Vagrantfile assigns `192.168.56.82` as the private network IP. [\[83.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.Vagrantfile.txt)

**What to look for:** Find the network interface with the `192.168.56.x` IP address. Copy this IP.

***

## Step 7: Access the Application in the Browser

Open a browser on your host machine and navigate to:

```
http://<VM_IP>:80
```

Or simply `http://<VM_IP>` since port 80 is the default HTTP port. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**What you see:** The EMart e-commerce application frontend (Angular app served through Nginx).

**What's happening behind the scenes:**

1. Your browser sends a request to Nginx (port 80)
2. Nginx routes `/` to the Angular client app
3. The Angular app renders in your browser
4. The frontend makes API calls to `/api` (NodeJS Mart API) for product data
5. Nginx routes `/api` calls to the NodeJS container, which queries MongoDB

### 7a. Test Registration Flow

The instructor demonstrates the full data flow by registering a user: [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

1. Click **Register**
2. Enter email, password
3. Enter ID number, first name, city (e.g., "New Delhi")
4. Click Register

**Data flow:** Registration data goes through Nginx → NodeJS API (or Java API depending on the endpoint) → MySQL database. The instructor confirms: *"this information is going in the MySQL database."* [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

### 7b. Test Login Flow

Log in with the registered credentials. The application greets the user by name (e.g., "Hi Imran"), displays the product list, and shows the **Booksmart** section which connects to the Java Books API. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

**Verification:** If you can register, log in, see products, and access the books section, all six containers are working correctly and communicating through the Nginx gateway.

***

## Step 8: Cleanup

### 8a. Stop and Remove All Containers

Ensure you're in the `emartapp` directory:

```bash
docker compose down
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**What it does:** Stops all running containers defined in the compose file, removes them, and removes the Docker network created for the project. Images are **not** removed by this command.

### 8b. Remove All Unused Docker Artifacts

```bash
docker system prune -a
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**Breakdown:**

* `docker system prune` — Removes all stopped containers, unused networks, dangling images, and build cache
* `-a` — Also removes all images not associated with a running container (not just dangling ones)

**Why:** This returns the VM to a clean state with no leftover images, containers, or cache consuming disk space. [\[83-microse...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83-microservice-project.txt)

### 8c. Exit the VM and Halt It

```bash
exit       # Exit root shell
exit       # Exit vagrant SSH session
vagrant halt
```

 [\[83.emart_d...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/83.emart_docker-compose.txt)

**What `vagrant halt` does:** Gracefully shuts down the VM (sends ACPI shutdown signal). The VM is stopped but not destroyed — you can `vagrant up` again later to restart it.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
EMart = Microservice e-commerce app (like Amazon/Flipkart)
6 containers, 3 languages, 2 databases, 1 gateway
Deployed via Docker Compose on a Vagrant-managed Ubuntu VM
```

***

## Architecture Map

```
[Browser] 
    │
    ▼ (port 80)
[Nginx — API Gateway]
    ├── /         → [Angular Client]  (Frontend/UI)
    ├── /api      → [NodeJS Mart API] → [MongoDB]
    └── /webapi   → [Java Books API]  → [MySQL]
```

**Key relationship:** Every external request enters through Nginx. No direct access to backend services.

***

## Monolithic vs. Microservice (vProfile vs. EMart)

```
vProfile (Monolithic)          │  EMart (Microservice)
───────────────────────────────┼────────────────────────────────
Single core app (Tomcat)       │  Multiple independent services
All services support one app   │  Each service = independent unit
image: (pull from registry)    │  build: (build from Dockerfile)
No source code needed          │  Full source code required
One tech stack dominates       │  Heterogeneous: Angular/Node/Java
Same deployment tool: docker compose up -d
```

***

## Docker Compose: Two Modes

```
image: <registry_path>  → Pull pre-built image → Run
build: <dockerfile_path> → Build image locally  → Run

Both can coexist in same compose file.
```

***

## Container Self-Healing

```
Container exits → Restart policy detects → Auto-restart
Handles: startup ordering issues, transient failures
Pattern: Retry-through-restart (not dependency orchestration)
```

***

## Infrastructure Stack

```
Host OS (Windows/Mac/Linux)
  └── VirtualBox
       └── Vagrant VM (Ubuntu Focal 64, IP: 192.168.56.82)
            └── Docker Engine + Docker Compose
                 └── 6 Containers (EMart microservices)
```

***

## Operational Flow (Complete Sequence)

```
vagrant global-status --prune     → Verify clean state
vagrant up                        → Create/start VM + install Docker
vagrant ssh → sudo -i             → Enter VM as root
git clone <emartapp_repo>         → Get source code (needed for build:)
cd emartapp/
vim docker-compose.yaml           → Inspect (build: directives present)
docker compose up -d              → Build images + run 6 containers
  └── (alt: docker compose build → docker compose up -d)
docker compose ps                 → Verify 6 containers running
docker ps -a                      → Check for exited containers
ip addr show                      → Get VM IP for browser access
Browser: http://<VM_IP>:80        → Access EMart app
── CLEANUP ──
docker compose down               → Stop + remove containers + network
docker system prune -a            → Remove all images + cache
exit → exit → vagrant halt        → Leave VM + shut down
```

***

## Scalability Model

```
New feature needed?
  → Create new service (any language)
  → Add new route in Nginx (/videos, /payment, /cart)
  → Add service to docker-compose.yaml
  → Existing services: UNTOUCHED
```

***

## Reusable Engineering Patterns

| Pattern                         | Manifestation in EMart                              |
| ------------------------------- | --------------------------------------------------- |
| **API Gateway**                 | Nginx routes all traffic; backends are hidden       |
| **Database-per-service**        | NodeJS→MongoDB, Java→MySQL; no shared DB            |
| **Infrastructure-as-code**      | Vagrantfile automates VM + Docker setup             |
| **Build-and-run orchestration** | Docker Compose `build:` + `up` in one tool          |
| **Self-healing containers**     | Restart policy handles transient exits              |
| **Clean state principle**       | `prune -a` + `compose down` before/after            |
| **Tool-agnostic orchestration** | Same `docker compose` for monolithic & microservice |

***

## Key Cause → Effect Chains

```
build: directive present → Source code required → git clone needed
NodeJS images → npm install → Long build time
Container exits → Restart policy → Auto-recovery
Nginx on port 80 → Default HTTP → No port needed in browser URL
docker compose down → Containers + network removed → Images persist
docker system prune -a → Everything unused removed → Clean slate
```

***

## Core Mental Model

```
Docker Compose = Universal container orchestrator
  ├── Architecture-agnostic (monolithic OR microservice)
  ├── Dual-mode (pull images OR build images)
  └── Single command deployment (docker compose up -d)

Microservice = Independent services + Gateway routing + Per-service DB
  ├── Scale by adding services, not modifying existing
  ├── Each service = own language, own DB, own lifecycle
  └── Gateway = single entry point, URL-based routing
```

***

This material covers every concept, command, decision, and architectural relationship present in the lecture. Each section serves its distinct purpose — Theory for understanding, Practical for execution, Compression Map for rapid recall — with minimal overlap between them. 🚀
