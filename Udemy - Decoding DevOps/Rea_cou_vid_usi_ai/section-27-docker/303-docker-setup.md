# 🐳 Docker Engine Setup on EC2 — Deep Learning Material

**Source:** Video caption file — [303-docker-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt?EntityRepresentationId=df5e1f96-7c96-4032-af7b-e35a6bc6c190) [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**Video Context:** The instructor launches an EC2 instance (Ubuntu 18), installs Docker Engine following official documentation, handles user permissions for non-root Docker access, validates the installation with the `hello-world` test image, and explains the fundamental concepts that emerge from this first interaction with Docker: the daemon, images, containers, Docker Hub, container lifecycle (short-lived vs. continuously running), and auto-naming.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Docker Engine — What It Is and Where It Runs

Docker Engine is the core software that enables you to build, run, and manage containers. It can run on any platform — the instructor says "Feel free to use your own platform. You can use virtual machines or whatever. VM, cloud, anything." For this exercise, he uses an Ubuntu 18 EC2 instance on AWS, but the concepts and installation process apply anywhere Docker can run. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

Docker Engine comes in two editions: **Docker CE (Community Edition)** and **Docker EE (Enterprise Edition)**. The instructor installs **Docker CE** — the free, open-source version suitable for development and most production use cases. Enterprise Edition adds additional security, management, and support features for large organizations. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

***

## 1.2 The Docker Daemon — The Background Service

After installation, Docker runs as a **daemon** (background service) on the host machine. The instructor verifies this: "Let's check the docker service. There should be a service running with the name docker. That's your docker daemon." [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

The daemon is the engine itself — it's the process that manages images, creates containers, handles networking, and manages storage. You interact with the daemon through the **Docker CLI** (command-line interface). When you type `docker images` or `docker run`, the CLI sends requests to the daemon, and the daemon executes them.

This is a **client-server architecture**: the CLI is the client, the daemon is the server. They communicate through a Unix socket (`/var/run/docker.sock`). This socket is the access point — whoever can communicate with this socket can control Docker.

***

## 1.3 Root-Only Access by Default — The Docker Group Permission Model

A critical security and operational concept emerges immediately. The instructor demonstrates: as root user, `docker images` works. As the regular `ubuntu` user, `docker images` throws **"Permission denied."** [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

The instructor explains: "By default, only root user can connect to the docker daemon by CLI. If you want any other user to run docker commands, then you need to add that user in the docker group. There is a group called as docker group." [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

When Docker is installed, it creates a Linux group called `docker`. The Docker socket (`/var/run/docker.sock`) is owned by this group. Only users in the `docker` group (or root) can communicate with the daemon. This is a deliberate security gate — Docker commands can do powerful things (mount host filesystems, access host networking, run privileged processes), so access shouldn't be open to everyone by default.

The fix is adding the user to the docker group using `usermod -G docker ubuntu`. After adding the user, you must **log out and log back in** for the group membership to take effect. The instructor demonstrates this: after re-logging, `docker images` works as the `ubuntu` user. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

🔍 **Deep Dive:** You can verify the group membership by checking `/etc/group` — the docker group line should show the added username. The `-G` flag in `usermod` adds the user to a supplementary group. Be careful with `-G` vs. `-aG`: `-G` alone replaces all supplementary groups with just the one specified, while `-aG` appends to existing groups. For safety, `-aG` is preferred in general, though in this case the instructor uses `-G` directly. Since the ubuntu user may have other groups, `-aG` would be safer in production.

***

## 1.4 Docker Images — The Template Layer

The instructor runs `docker images` to "list all the images which is in your local machine." Initially, there are none: "There is nothing now." [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

An image is a **read-only template** from which containers are created. It contains the application, its dependencies, libraries, configuration files, and the filesystem structure needed to run. Images are not running processes — they are static blueprints. You can have many images stored locally, and from each image, you can create one or many containers.

***

## 1.5 Docker Hub — The Image Registry

When the instructor runs `docker run hello-world`, Docker first checks if the `hello-world` image exists locally. It doesn't, so: "It says, I don't know where is this image. So it will go and find it at Docker Hub. There is a place, Docker Hub, where all these images are hosted." [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

Docker Hub is a **public registry** — a centralized repository where Docker images are stored, shared, and distributed. When you reference an image name in a Docker command and the image isn't available locally, Docker automatically **pulls** (downloads) it from Docker Hub. This is the default behavior — Docker Hub is the default registry.

The flow: `docker run hello-world` → image not found locally → pull from Docker Hub → download image → store locally → create container from image → run container. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

***

## 1.6 `docker run` — The Core Command

The instructor explains the fundamental Docker command: "`docker run` means actually 'create container for me from this image.'" [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

`docker run hello-world` does three things in sequence:

1. Checks for the `hello-world` image locally (not found)
2. Pulls it from Docker Hub (downloads)
3. Creates and starts a container from that image

The `hello-world` container runs a simple script (`/hello`) that prints a welcome message. After printing, the container's process completes and the container exits. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

***

## 1.7 Container Lifecycle — Short-Lived vs. Continuously Running

This is a foundational concept the instructor teaches through the `hello-world` example. After running the container, the instructor checks running containers: [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**`docker ps`** — shows **running** containers. The `hello-world` container doesn't appear because it already finished.

**`docker ps -a`** — shows **all** containers, including stopped/exited ones. The `hello-world` container appears with status **"Exited."**

The instructor identifies two categories of containers:

**Short-lived containers:** "This is a very short-lived container. Its job is to just run a script that prints a message — that's it, dead." The container starts, executes its task, and exits. Use cases: archiving logs, scheduled data processing, batch jobs, running a script. "You need to have a container that runs, does that work, and then it's dead." [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**Continuously running containers:** "Continuously running container like you're running Apache service or Tomcat service or MySQL service. It should be running continuously." These containers stay alive because the process inside them (a web server, database, etc.) is designed to run indefinitely. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

The distinction is not about Docker configuration — it's about the **process inside the container**. If the process finishes (like a script that prints "hello"), the container exits. If the process runs indefinitely (like an Apache daemon), the container stays running.

***

## 1.8 Container Details — ID, Image, Command, and Auto-Naming

From `docker ps -a`, the instructor points out the information visible for each container: [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

* **Container ID** — a unique identifier
* **Image** — which image the container was created from (`hello-world`)
* **Command** — what command the container executed (`/hello` — "That means it's some kind of script")
* **Created** — when it was created ("35 seconds ago")
* **Status** — current state (`Exited`)
* **Name** — `modest_query` — "If you don't name a container, it will give a name — adjective and celebrity name combined together." Docker auto-generates names by combining a random adjective with a famous scientist/hacker name. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

***

## 1.9 Docker on Ubuntu — Auto-Enable on Boot

The instructor mentions: "In Ubuntu anyways, if you install a service, it gets enabled automatically." This means the Docker daemon will start automatically on boot without needing to explicitly run `systemctl enable docker`. On other Linux distributions (CentOS, for example), you might need to enable it manually. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

***

## 1.10 The Installation Process — Following Official Documentation

The instructor follows Docker's official documentation (`docs.docker.com` → Get Started → Download and Install → Linux → Ubuntu). He highlights that the documentation has "improved a lot" and is "really amazing" now. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

The installation steps (from the docs) follow a standard pattern:

1. Remove any old/conflicting Docker packages (`docker`, `docker-engine`, `docker.io`)
2. Update the package index
3. Install prerequisite dependencies
4. Install Docker's GPG key
5. Add Docker's official APT repository
6. Install Docker CE

The instructor also mentions the post-installation steps in the documentation: managing Docker as a non-root user (which he already did), configuring Docker to start on boot, and troubleshooting steps for common issues. He recommends going through these "if you're getting into any issues while you're setting up Docker Engine on Linux machine." [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

***

## 1.11 Security Group Configuration for Docker

The instructor creates a security group with: SSH (port 22) from "My IP" and **all traffic from "My IP"**. The reason for all-traffic: "We'll be accessing Docker Engine on different different ports when we run the containers on them." [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

Each container can expose different ports (80 for web, 3306 for MySQL, 8080 for Tomcat, etc.). Rather than adding security group rules for each port individually, allowing all traffic from your own IP simplifies development access. This is a development convenience — not a production security practice.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a **Docker Engine on an EC2 instance** — installing Docker, configuring user permissions, and validating the installation. The final outcome: a working Docker environment where you can pull images, create containers, and run services — ready for all subsequent Docker lectures. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

***

## Step 1: Launch the EC2 Instance

Navigate to **EC2 Console → Launch Instance**. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**Settings:**

* **Name:** `docker-engine`
* **AMI:** Ubuntu 18 (the instructor uses this; any Ubuntu version works)
* **Instance type:** `t2.micro`
* **Security group:** Create new — name it `docker-sg` or similar:
  * **Rule 1:** SSH (port 22) from My IP
  * **Rule 2:** All Traffic from My IP — needed because containers will expose various ports during the course
* **Key pair:** Create a new key pair, download it
* **All other settings:** Defaults [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

Click **Launch**.

Wait for the instance to reach "running" state, then SSH in:

```bash
ssh -i <key.pem> ubuntu@<public-ip>
```

***

## Step 2: Follow Official Docker Documentation for Installation

Navigate to: **docs.docker.com → Get Started → Download and Install → Linux → Ubuntu** [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

The instructor follows the documentation step by step. Switch to root first:

```bash
sudo -i
```

### 2a. Remove old Docker versions (if any):

The docs recommend removing any pre-existing `docker`, `docker-engine`, or `docker.io` packages. On a fresh instance, there likely aren't any, but running the removal command ensures a clean state. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

### 2b. Update and install prerequisites:

```bash
apt-get update
apt-get install ca-certificates curl gnupg lsb-release -y
```

### 2c. Add Docker's GPG key:

Follow the exact command from the docs to install Docker's official GPG key.

### 2d. Add Docker's APT repository:

Follow the docs to add Docker's repository to your system's package sources.

### 2e. Install Docker CE:

```bash
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io -y
```

 [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**Expected result:** Installation completes without errors.

**Connection to flow:** Docker is now installed but we need to verify it's running and configure permissions.

***

## Step 3: Verify the Docker Service Is Running

```bash
systemctl status docker
```

**Expected output:** The Docker service should show as **active (running)**. This is the Docker daemon — the background service that manages everything. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**If not running:** `systemctl start docker` to start it.

**On Ubuntu:** The Docker service is auto-enabled on boot after installation. On other distros, you may need `systemctl enable docker`. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

### Quick test as root:

```bash
docker images
```

**Expected output:** An empty list (no images yet). This confirms the CLI can communicate with the daemon.

***

## Step 4: Configure Non-Root Docker Access

### Exit root and test as ubuntu user:

```bash
exit  # back to ubuntu user
whoami  # should show "ubuntu"
docker images
```

**Expected result:** **Permission denied.** This is normal — only root and members of the `docker` group can access the daemon. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

### Add ubuntu user to the docker group:

```bash
sudo usermod -G docker ubuntu
```

**Breakdown:**

* `sudo` — needs root to modify user groups
* `usermod` — modify user account
* `-G docker` — set supplementary group to `docker`
* `ubuntu` — the username to modify [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

### Verify group membership:

```bash
cat /etc/group | grep docker
```

**Expected output:** A line showing `docker:x:XXXX:ubuntu` — confirming `ubuntu` is in the `docker` group. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

### Log out and log back in:

```bash
exit  # exit SSH session
ssh -i <key.pem> ubuntu@<public-ip>  # reconnect
```

**Why logout/login:** Group membership changes only take effect in **new sessions**. The current shell session still has the old group list. You must start a fresh session for the `docker` group to be active. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

### Test again:

```bash
docker images
```

**Expected output:** Empty list — no errors. The `ubuntu` user can now run Docker commands without `sudo`.

**Common mistake:** Forgetting to log out and log back in after adding the user to the group. The `docker images` command will still fail with permission denied until you start a new session.

***

## Step 5: Validate with the `hello-world` Test Image

```bash
docker run hello-world
```

**Breakdown:**

* `docker run` — create and start a container
* `hello-world` — the image name [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**What happens internally:**

1. Docker checks locally for the `hello-world` image → not found
2. Docker pulls the image from Docker Hub (you'll see download progress)
3. Docker creates a container from the image
4. The container runs the `/hello` command (a script that prints a welcome message)
5. The script finishes → the container exits [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**Expected output:** A "Hello from Docker!" message with information about what just happened — confirming Docker is working correctly.

### Check running containers:

```bash
docker ps
```

**Expected output:** Empty — no running containers. The `hello-world` container already exited. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

### Check all containers (including stopped):

```bash
docker ps -a
```

**Breakdown:**

* `docker ps` — list containers
* `-a` — show **all** containers (running + stopped/exited)

**Expected output:** One container with:

* **Status:** `Exited (0)` — exit code 0 means success
* **Image:** `hello-world`
* **Command:** `/hello`
* **Name:** A random auto-generated name (e.g., `modest_query`) [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**Verification:** Seeing the exited container with status 0 confirms the complete Docker flow works: pull → create → run → exit.

### Check downloaded images:

```bash
docker images
```

**Expected output:** One image: `hello-world` — now stored locally. Future `docker run hello-world` commands won't need to download it again. [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)

**Connection to flow:** Docker Engine is fully operational. The next lecture covers Docker CLI commands in detail.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Docker Engine Architecture

```
HOST MACHINE (Ubuntu 18 EC2)
│
├── DOCKER DAEMON (background service)
│   ├── Manages: images, containers, networks, volumes
│   ├── Socket: /var/run/docker.sock
│   ├── Access: root user OR members of 'docker' group
│   └── Auto-starts on boot (Ubuntu)
│
├── DOCKER CLI (client)
│   ├── Commands: docker run, docker ps, docker images, ...
│   └── Communicates with daemon via Unix socket
│
├── LOCAL IMAGE STORE
│   └── (empty until first pull)
│
└── DOCKER HUB (remote registry)
    └── Public image repository
    └── Default pull source when image not found locally
```

***

## ⚡ Installation Flow

```
1. Launch EC2: Ubuntu 18, t2.micro, SG: SSH + All Traffic from My IP
2. SSH in → sudo -i (root)
3. Follow docs.docker.com → Linux → Ubuntu:
   apt update → install prereqs → add GPG key → add repo → install docker-ce
4. Verify: systemctl status docker → active (running)
5. Test as root: docker images → works (empty list)
6. Test as ubuntu: docker images → PERMISSION DENIED
7. Fix: sudo usermod -G docker ubuntu
8. Verify: cat /etc/group | grep docker → ubuntu listed
9. LOGOUT → LOGIN (mandatory for group change)
10. Test as ubuntu: docker images → works
11. Validate: docker run hello-world → pull + run + print + exit
```

***

## 🔒 Permission Model

```
DEFAULT: Only root can use Docker CLI
         (daemon socket owned by docker group)

FIX:
  sudo usermod -G docker <username>
  → logout → login (new session required)
  → docker commands work without sudo

VERIFY:
  cat /etc/group | grep docker → should show username
```

***

## 🔄 `docker run hello-world` — Complete Flow

```
docker run hello-world
    │
    ├── 1. Check local images → NOT FOUND
    ├── 2. Pull from Docker Hub → DOWNLOAD
    ├── 3. Store image locally
    ├── 4. Create container from image
    ├── 5. Run command: /hello (prints message)
    └── 6. Process completes → container EXITS

AFTER:
  docker ps     → EMPTY (container exited)
  docker ps -a  → shows exited container (status: Exited 0)
  docker images → shows hello-world image (stored locally)
```

***

## 📦 Container Lifecycle Types

```
SHORT-LIVED:
  Process runs → completes → container exits
  Examples: log archival, batch jobs, scripts, scheduled tasks
  hello-world: runs /hello → prints → dead

CONTINUOUSLY RUNNING:
  Process runs indefinitely → container stays alive
  Examples: Apache, Tomcat, MySQL, Nginx
  Stays in 'docker ps' output (not just 'docker ps -a')

WHAT DETERMINES IT: the nature of the PROCESS inside,
                    NOT a Docker configuration setting
```

***

## 📋 `docker ps -a` Output Fields

```
CONTAINER ID  │ unique identifier
IMAGE         │ source image (hello-world)
COMMAND       │ what the container executed (/hello)
CREATED       │ when it was created
STATUS        │ current state (Exited, Running, etc.)
NAME          │ auto-generated if not specified
              │ format: adjective_celebrity (e.g., modest_query)
```

***

## 🔗 Key Docker Concepts — Relationship Map

```
DOCKER HUB (remote)
    │ pull (download)
    ▼
IMAGE (local, read-only template)
    │ docker run (create + start)
    ▼
CONTAINER (running instance of image)
    │ process completes or keeps running
    ▼
EXITED or RUNNING state

IMAGE → many CONTAINERS (one image, many instances)
CONTAINER → one IMAGE (each container from exactly one image)
```

***

## 🛡️ Security Group — Why All Traffic

```
SSH (22): My IP        ← management access
All Traffic: My IP     ← containers expose various ports
                         (80, 8080, 3306, etc.)
                         easier than adding rules per port
⚠️ Development convenience only, not production practice
```

***

## ⚠️ Common Errors — Quick Fix

```
SYMPTOM: "Permission denied" on docker commands
  CAUSE: User not in docker group
  FIX:   sudo usermod -G docker <user> → logout → login

SYMPTOM: Still "Permission denied" after usermod
  CAUSE: Didn't logout/login (group change not active)
  FIX:   Exit SSH → reconnect

SYMPTOM: docker service not running
  FIX:   systemctl start docker

SYMPTOM: Old docker versions conflict
  FIX:   Remove docker, docker-engine, docker.io first (per docs)
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Client-Server with Socket-Based Access Control**
Docker uses a client (CLI) → server (daemon) architecture, with access controlled through Unix socket ownership. The `docker` group controls who can communicate with the daemon. This same pattern appears in many systems: database sockets, web server management interfaces, container orchestrators. The security boundary is the socket, not the command itself.

**Pattern 2: Pull-on-Demand from Registry**
When a resource (image) is requested locally and not found, the system automatically fetches it from a centralized registry (Docker Hub). This lazy-pull pattern minimizes local storage while ensuring any image is available on demand. The same pattern appears in package managers (`apt`, `yum`, `npm`), Maven repositories, and container registries.

**Pattern 3: Process Lifecycle = Container Lifecycle**
A container lives exactly as long as its main process. When the process exits, the container exits. When the process runs indefinitely, the container runs indefinitely. Understanding this eliminates confusion about "why did my container stop?" — the answer is always: "because its process finished."

***

## 🎯 One-Line System Summary

> **Docker Engine is installed on Ubuntu via official docs (add repo → install docker-ce), runs as a daemon accessible only to root/docker-group members, stores images locally (pulled on demand from Docker Hub), and creates containers whose lifecycle matches their internal process — short-lived for scripts, continuously running for services — validated by `docker run hello-world` which pulls, runs, prints, and exits.** [\[303-docker-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/303-docker-setup.txt)
