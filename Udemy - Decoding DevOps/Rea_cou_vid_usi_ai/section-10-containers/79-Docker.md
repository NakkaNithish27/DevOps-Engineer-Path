# 🎓 Docker Overview — Deep Learning Material

**Source:** Video caption file — *Docker Overview* [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Docker Is and What Problem It Solves

Docker is an **open platform for developing, shipping, and running applications**. But the word "application" in Docker's world has a very specific meaning — it really means **containers that have your process in it**. So when Docker says "develop, ship, and run applications," what it actually means is: you can create a container that holds your process, package it, transfer it anywhere, and run it on any machine that has the Docker Daemon installed. The "wherever you want" portability is the foundational promise. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

The core problem Docker solves is **separation of applications from infrastructure**. Before Docker, your application was deeply entangled with the host machine — its OS version, installed libraries, configurations, other running services. Changing the infrastructure could break the application; running multiple applications could create conflicts. Docker breaks this entanglement through **isolation**. Your application runs inside a container, and the container provides a boundary that separates it from the underlying infrastructure and from other containers. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

This isolation has a direct business consequence: **you can deliver software quickly**. Because the application is decoupled from the host, you don't spend time debugging environment-specific issues or worrying about what else is running on the machine. You build it once in a container, and it runs the same way everywhere.

***

## 1.2 — What a Container Actually Is

A container is a **loosely isolated environment** in which you package and run an application. The key engineering characteristics:

**Isolation + Security:** Because containers are isolated, you can run **many containers simultaneously on a single host**. You don't need multiple physical or virtual computers to achieve separation — one computer can host many containers, each running independently. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

**Lightweight — The "Miniature OS" Concept:** Containers are lightweight because they are essentially a **miniature operating system**. But "miniature" is critical here — a container doesn't carry a full OS with all its utilities, services, and libraries. It contains **only the files needed to run that particular process**. The video gives a concrete example: an Nginx container needs only Nginx files. Not the full Ubuntu installation, not development tools, not a desktop environment — just what Nginx needs to operate. This is why containers are small, start fast, and consume minimal resources compared to full virtual machines. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

> 🔍 **Deep Dive:** The phrase "loosely isolated" is deliberately chosen in Docker's documentation. It's not *fully* isolated like a virtual machine (which has its own complete kernel). Containers share the host's kernel but have isolated user spaces (file system, processes, network). This shared-kernel architecture is precisely what makes them lightweight — they don't duplicate the entire OS, only the user-space components their process needs. This is an *implicit concept* — the video refers to "miniature OS" and "isolation" without explicitly explaining the shared-kernel mechanism, but the lightweight nature directly follows from it.

***

## 1.3 — Docker Architecture: The Three-Component System

The Docker architecture consists of three interacting components: **Docker Host**, **Docker Daemon**, and **Docker Client**. Plus an external component: the **Registry**. Understanding how these relate is essential.

### Docker Host

A Docker Host is simply **a computer** — nothing more. It's the machine on which Docker is installed and containers run. In the video's practical setup, this host is a **virtual machine** that they create and install Docker engine on. But it could be any computer — a physical server, a cloud VM, your laptop. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Docker Daemon

The Docker Daemon is the **Docker service** — the background process that actually does the work of managing containers and images on the host. When you "install Docker engine" on a machine, you're installing this daemon. It listens for commands, manages the lifecycle of containers (creating, starting, stopping, deleting them), handles images, and interacts with registries. The daemon is the engine that powers everything. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Docker Client

The Docker Client is the tool you use to **send commands to the Docker Daemon**. It's the interface through which you interact with Docker. An important architectural detail: the client **can be on the same machine as the daemon, or on a different machine**. In the video's setup, both client and daemon are on the same virtual machine, which is the most common development setup. But in production environments, you might have a client on your local workstation sending commands to a daemon running on a remote server. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Registry (Docker Hub)

Images have to come from somewhere. A **Registry** is a storage and distribution system for Docker images. The primary public registry is **hub.docker.com** (Docker Hub). When you go to Docker Hub and click "Explore," you see **ready-made official images**: Python, Postgres, Ubuntu (a miniature Ubuntu), Traefik, Redis, Node, Mongo, OpenJDK, MySQL, Golang, Nginx — and the list goes on extensively. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

These are the same container images that containers are built from. The official images are maintained by the respective projects or Docker, but **you can also create your own images and store them on Docker Hub**. So Docker Hub serves both as a public library of pre-built images and as a private/public repository for your custom images. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

> ⚠️ **Expert Note:** The distinction between "official" and "unofficial" images on Docker Hub matters operationally. Official images are curated, regularly updated, and security-scanned. Unofficial images are community-contributed and may vary in quality, security, and maintenance. The video explicitly mentions you can pull "official or unofficial images" — in production, you'd want to carefully evaluate unofficial images before trusting them.

***

## 1.4 — The Image → Container Relationship

This is a critical conceptual relationship: **containers run from images**. An image is a static, read-only template that contains everything needed to run a process — the miniature OS files, the application binaries, configurations. A container is a **running instance** of an image. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

Think of it this way: the image is the blueprint, the container is the live, running thing built from that blueprint. You can run multiple containers from the same image, each operating independently. This is how you get many isolated instances of the same application running on one host.

The flow is: **Registry → Image → Container**. Images are stored in the registry. You pull them to your host. You run containers from them. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

***

## 1.5 — Three Core Docker Commands (Conceptual Understanding)

Three commands map directly to the three core operations in Docker's workflow:

**`docker build`** — Creates your own custom image. When the pre-built images from Docker Hub don't match your exact needs, you build your own. This is how you package your application into an image. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

**`docker pull`** — Downloads an image from a registry (Docker Hub) to your local Docker Host. This is how you get official images (or anyone else's images) onto your machine so you can run containers from them. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

**`docker run`** — Creates and starts a container from an image. This is the command that brings an image to life as a running, isolated process on your host. "Run the container from the image" — that's the exact mental model. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

These three commands represent the complete operational lifecycle: **build** (create images) → **pull** (get images) → **run** (start containers).

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building and Why

We're setting up a Docker environment from scratch and learning the operational flow of getting containers running. The setup involves: creating a **virtual machine**, installing **Docker Engine** on it (which gives us both the Docker Daemon and Docker Client), and then using Docker commands to pull images from Docker Hub and run containers. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

This matters because it's the foundational operational workflow for every Docker-based project — whether you're running a local development environment, a CI/CD pipeline, or production infrastructure.

The final outcome: a running Docker host where you can pull any image from Docker Hub and run it as a container, and where you can build your own custom images.

***

## Step 1: Set Up the Docker Host (Create a Virtual Machine)

### What We're Doing

Creating a virtual machine that will serve as our Docker Host — the computer on which Docker runs. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Why We're Doing It

Docker Daemon needs a host machine to run on. Using a VM gives us a clean, isolated environment for Docker without affecting our main operating system. This mirrors how Docker is typically deployed in real environments (on dedicated servers or cloud VMs).

### What to Expect

After this step, you have a running virtual machine — an empty computer ready for Docker installation. No Docker functionality exists yet.

### Connection to Larger Flow

This VM becomes the **Docker Host** from the architecture diagram. Everything that follows — daemon, client, containers, images — lives on or interacts with this machine.

***

## Step 2: Install Docker Engine

### What We're Doing

Installing Docker Engine on the virtual machine. This single installation gives us both the **Docker Daemon** (the background service) and the **Docker Client** (the command-line tool). [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Why We're Doing It

Without Docker Engine installed, the machine is just a regular computer. Docker Engine is what transforms it into a Docker Host capable of building, pulling, and running containers.

### What Happens Internally

The installation places the Docker Daemon as a service on the machine (it runs in the background, listening for commands) and installs the `docker` CLI binary (the client). After installation, the client and daemon are on the **same machine**, which is the standard development setup. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### How to Verify Success

After installation, you should be able to run Docker commands from the terminal. If the daemon is running and the client can communicate with it, your Docker Host is operational.

### Common Mistakes

* Forgetting to start the Docker Daemon service after installation.
* Permission issues — on Linux, you may need to add your user to the `docker` group or use `sudo`.

### Connection to Larger Flow

You now have a functional Docker Host with both client and daemon. The next steps use the client to interact with the daemon to manage images and containers.

***

## Step 3: Pull an Image from Docker Hub (`docker pull`)

### What We're Doing

Downloading a pre-built image from the Docker Hub registry to our local Docker Host. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### The Command

```
docker pull <image_name>
```

**Breakdown:**

* `docker` — Invokes the Docker Client CLI.
* `pull` — The subcommand that tells Docker to download an image.
* `<image_name>` — The name of the image on Docker Hub (e.g., `nginx`, `python`, `mysql`, `ubuntu`).

### What Happens Internally

The Docker Client sends a `pull` request to the Docker Daemon. The daemon contacts the Docker Hub registry (hub.docker.com), locates the specified image, and downloads it to the local image store on the Docker Host. After this, the image exists locally and is ready to be used. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Where to Find Available Images

Go to **hub.docker.com**, click **Explore**. You'll see official images: Python, Postgres, Ubuntu, Traefik, Redis, Node, Mongo, OpenJDK, MySQL, Golang, Nginx, and many more. You can also search for unofficial community images. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Expected Result

The image is downloaded and stored locally. You can now run containers from it.

### Common Mistakes

* Pulling unofficial images without checking their quality/security.
* Not specifying a tag (version) — Docker defaults to `:latest`, which may not always be what you want.

### Connection to Larger Flow

This step completes the **Registry → Image** part of the flow. The image now exists on your Docker Host, ready for `docker run`.

***

## Step 4: Run a Container from an Image (`docker run`)

### What We're Doing

Creating and starting a live, running container from a locally available image. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### The Command

```
docker run <image_name>
```

**Breakdown:**

* `docker` — Invokes the Docker Client CLI.
* `run` — The subcommand that tells Docker to create and start a container.
* `<image_name>` — The image to instantiate as a running container.

### What Happens Internally

The Docker Client sends the `run` command to the Docker Daemon. The daemon takes the specified image, creates a new container instance from it (with its own isolated filesystem, process space, and network), and starts the main process defined in the image. The container is now a live, running, isolated environment on your Docker Host. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### Expected Result

A running container. The specific process inside the container (e.g., Nginx serving web traffic, Python running a script, MySQL listening for database connections) is now active and isolated from everything else on the host.

### Connection to Larger Flow

This completes the full **Registry → Image → Container** pipeline. You've gone from a registry of available software to a running, isolated instance on your machine.

***

## Step 5: Build Your Own Image (`docker build`)

### What We're Doing

Creating a custom Docker image when the official images don't meet your specific needs. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### The Command

```
docker build <options>
```

**Breakdown:**

* `docker` — Invokes the Docker Client CLI.
* `build` — The subcommand that tells Docker to create a new image from a set of instructions (typically a Dockerfile).

### Why We're Doing It

Official images provide base functionality (e.g., a clean Python environment, a clean Nginx server). But your application has custom code, custom configurations, custom dependencies. `docker build` lets you package all of that into your own image, which you can then run as containers or push to Docker Hub for others to use. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

### What Happens Internally

The Docker Client sends the build context and instructions to the Docker Daemon. The daemon executes the build instructions layer by layer, creating a new image. This custom image can then be used with `docker run` just like any official image.

### Connection to Larger Flow

This is the **creation side** of the Docker workflow. While `pull` gets existing images, `build` creates new ones. Custom images can be stored back on Docker Hub, completing the full lifecycle: build → push to registry → pull from registry → run.

> 🔍 **Deep Dive:** The video mentions that building custom images and storing them on Docker Hub will be covered in detail in **Section 20** of the course. The current lecture establishes the conceptual and architectural framework; the hands-on image-building practice comes later. [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Docker Core Identity

```
Docker = Open platform for DEVELOPING, SHIPPING, and RUNNING containers
         └─ "Application" in Docker = Container with your process in it
         └─ Core value: Separate application from infrastructure → fast delivery
```

 [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

***

## 📦 What a Container Is

```
Container = Loosely isolated environment running a single process
  ├─ Miniature OS (only files needed for THAT process)
  │    └─ Example: Nginx container = only Nginx files
  ├─ Lightweight → fast start, low resource usage
  ├─ Many containers can run simultaneously on ONE host
  └─ Isolation + Security without needing multiple computers
```

***

## 🔗 Docker Architecture — Component Map

```
┌─────────────────────────────────────────────────┐
│                  DOCKER HOST (a computer / VM)   │
│                                                   │
│   ┌──────────────┐       ┌──────────────────┐    │
│   │ Docker Client │──────▶│  Docker Daemon    │    │
│   │ (CLI tool)    │ cmds  │  (background svc) │    │
│   └──────────────┘       └────────┬─────────┘    │
│                                    │ manages      │
│                          ┌────────┴────────┐     │
│                          │  Images  │ Containers │ │
│                          └────────┬────────┘     │
└───────────────────────────────────┼──────────────┘
                                    │ pull/push
                          ┌─────────▼──────────┐
                          │     REGISTRY        │
                          │  (hub.docker.com)   │
                          │  Official: nginx,   │
                          │  python, mysql,     │
                          │  ubuntu, redis...   │
                          │  + Custom images    │
                          └────────────────────┘
```

 [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

***

## ⚙️ Component Roles — One-Line Each

```
Docker Host    =  The computer (physical/VM) where Docker runs
Docker Daemon  =  The service that manages images + containers (the engine)
Docker Client  =  CLI that sends commands to daemon (same or remote machine)
Registry       =  Image storage + distribution (Docker Hub = default public registry)
Image          =  Static read-only template (blueprint)
Container      =  Running instance of an image (live isolated process)
```

***

## 🔄 Core Operational Flow

```
REGISTRY  ──pull──▶  IMAGE (local)  ──run──▶  CONTAINER (live)
                        ▲
                        │ build
                   YOUR CODE + Dockerfile
                        │
                        ▼
                   CUSTOM IMAGE  ──push──▶  REGISTRY
```

***

## 🛠️ Three Commands = Three Operations

```
docker pull   →  Registry → Local Image Store     (GET existing images)
docker build  →  Code/Dockerfile → Custom Image    (CREATE new images)
docker run    →  Image → Running Container         (START isolated process)
```

***

## 🔑 Key Relationships to Remember

```
Image : Container  =  Blueprint : Running Instance  (1 image → N containers)
Client : Daemon    =  Remote/CLI : Engine            (can be same or different machine)
Registry : Image   =  Library : Book                 (centralized storage, pull on demand)
Container : Host   =  Isolated process : Shared kernel (lightweight, not full VM)
```

***

## 🧩 Reusable Engineering Patterns Extracted

```
PATTERN 1: BLUEPRINT → INSTANCE
  Image → Container = static template → live running thing
  Applies to: VM images/snapshots, class/object in OOP, AMIs in AWS, Helm charts → deployments

PATTERN 2: CLIENT-SERVER ON SAME OR REMOTE HOST
  Docker Client ↔ Docker Daemon can be co-located or separated
  Applies to: database CLI/server, kubectl/API server, any CLI/daemon architecture

PATTERN 3: CENTRALIZED REGISTRY + LOCAL CACHE
  Pull from central registry → store locally → run from local cache
  Applies to: Maven/npm/pip registries, Git repos, package managers, artifact stores

PATTERN 4: ISOLATION WITHOUT DUPLICATION
  Containers share host kernel but isolate user space → lightweight isolation
  Applies to: namespaces, cgroups, chroot jails, multi-tenancy patterns

PATTERN 5: MINIMAL FOOTPRINT BY DESIGN
  Include ONLY what the process needs, nothing more
  Applies to: microservices, single-responsibility principle, minimal base images, 
              Lambda functions, sidecar containers
```

 [\[79-what-is-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/79-what-is-docker.txt)

***

## 🧭 Course Navigation Context

```
Previous lecture  →  Container concepts + isolation theory (referenced but not included here)
THIS lecture      →  Docker architecture overview (Host, Daemon, Client, Registry, Image, Container)
Next lecture       →  Hands-on: install Docker, pull images, run containers
Section 20        →  Build custom images, push to Docker Hub
```

***

This gives you a solid conceptual and operational foundation for Docker's architecture before diving into hands-on work. Want me to generate **AnkiDroid flashcards (.csv)** from this material for spaced repetition? 🃏
