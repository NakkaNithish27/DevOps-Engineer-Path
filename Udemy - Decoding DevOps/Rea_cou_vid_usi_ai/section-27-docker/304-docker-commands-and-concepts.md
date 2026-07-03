# 🎓 Deep Learning Material: Docker Hub, Images, Containers & Core Commands

*Reconstructed from video lecture captions (304-docker-commands-and-concepts.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Docker Hub: The Registry That Powers Docker

Docker Hub (`hub.docker.com`) is the **default registry** for Docker images — the instructor calls it *"really the backbone of Docker."*   A registry is a centralized storage and distribution system for container images. When you run `docker pull nginx`, Docker goes to Docker Hub by default to download the image. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

Docker Hub hosts two categories of images: **official images** and **non-official images**. Official images come directly from the vendor — the Nginx image is maintained by the Nginx team, the Ubuntu image by Canonical, etc. The instructor lists examples: Mongo, Postgres, Node, Redis, Ubuntu, MariaDB, Alpine, Nginx, Memcached, httpd, RabbitMQ, Python, Hello World. You can also create your own account and **upload your own customized images**. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

Docker Hub is not the only registry. The instructor identifies several alternatives: [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

* **GCR** (Google Container Registry)
* **Amazon ECR** (Elastic Container Registry)
* **Nexus 3** — can serve as a Docker registry
* **JFrog Artifactory**
* **DTR** (Docker Trusted Registry) — a container-based registry whose own image is available on Docker Hub (the instructor notes the humor: *"That's kind of funny"*)

In registry terminology, an image is called a **repository**. The instructor clarifies: *"In Docker Hub, if you see Tomcat, that's a repository. Tomcat repository in Docker Hub registry."* [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## 1.2 Docker Images: What They Are at a Fundamental Level

A Docker image is **a stopped container which is archived**. The instructor uses this definition deliberately. It is not an entire operating system. It is not a VM disk. It is a lightweight, layered filesystem snapshot from which containers run. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

The instructor draws and then carefully limits a comparison to VM images: *"Just like you have VM image from where you can create VMs, or like AMI, but cannot directly compare that. Virtual machine images, we are talking specifically about container images."*  The comparison helps understand the concept (a template from which you create running instances), but the internal mechanics are fundamentally different. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

### The Layer Architecture

An image consists of **multiple layers**. Each layer represents a change to the filesystem — installing a package creates a layer, creating a directory creates a layer, copying a file creates a layer. The instructor explains: *"When you're building your own image, let's say you have installed a package, apt install git, that will create a layer. After that you created a directory, that will create another layer."* [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

All image layers are **read-only**. Once an image is built, its layers never change. This is a critical architectural property — images are immutable.

### Image Size vs. VM Size

The instructor demonstrates the size difference concretely: the Nginx image is **133 MB**. He contrasts this with an AWS AMI for Linux, which is minimum **8 GB**. *"Compare that with 133 MB. What is it? Nothing."*  This dramatic size difference exists because container images don't include a kernel, device drivers, or most OS utilities — they contain only the application and its direct dependencies, layered on top of a minimal base filesystem. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## 1.3 The Image-Container Relationship: The Most Important Concept

This is the single most important conceptual understanding in the lecture, and the instructor returns to it repeatedly with multiple proofs. **Containers run directly from images. They are connected to the image. They do not clone the image.** [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

The instructor distinguishes this from VMs: *"Unlike VMs, when you create VMs from an image like we create from Vagrant box, the box and VM are separate then. The VM will be a complete clone of the image. But containers are not like that. They are running from the images. Like directly."* [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

A container is a **thin read/write layer** sitting on top of the image's read-only layers. When you access a file inside a container — say, the Nginx default webpage — you are actually reading data from the image layers beneath. The container itself stores almost nothing. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

The instructor proves this with two demonstrations:

**Proof 1 — Container directory size:** He navigates to `/var/lib/docker/containers/<container_id>/` on the host and runs `du -sh`. The result is **40 KB** — just some configuration files (resolv.conf, hostname). The actual web content, the Nginx binary, the libraries — all of that lives in the image directory (`/var/lib/docker/image/overlay2/`). [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Proof 2 — Deletion dependency:** You **cannot remove an image if a container is using it** — even a stopped container. The instructor demonstrates: `docker rmi nginx` fails with *"container with so and so ID is using its referenced image."*  This proves the container depends on the image at a filesystem level. To remove the image, you must first remove all containers derived from it. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

🔍 **Deep Dive:**
The filesystem mechanism that makes this possible is called **overlay filesystem** (specifically `overlay2` on modern Docker). The image layers are stacked as read-only filesystem layers, and the container adds a single writable layer on top. When a container writes data (like installing a package with `apt install`), the data goes into the container's writable layer — the image layers remain unchanged. When a container reads a file, the overlay filesystem serves it from the appropriate image layer. This "union mount" approach is how multiple containers can share the same image without duplicating data.

***

## 1.4 Image Tags: Versioning Mechanism

Every image has **tags** — labels used primarily for versioning. When you pull `nginx`, you get the `latest` tag by default. But you can pull a specific version by specifying the tag: `docker pull nginx:mainline-alpine-perl`. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

The instructor makes an important clarification about the `latest` tag: *"Latest — it's just a name. It really doesn't mean, it's not a guarantee that it's the latest image, but majorly for official images, latest will really mean the latest image."*  The `latest` tag is a convention, not an automated mechanism. For non-official images, `latest` might not actually point to the newest version. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

When you list images with `docker images`, the same image name can appear multiple times with different tags. Each tag can point to the same or different image content (identified by the Image ID). [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## 1.5 Container Networking: Port Mapping

A container runs inside a **private network** on the host machine. It is not directly accessible from outside. The instructor uses an analogy: *"Think of this like the private subnet instance. Running in a private subnet. You cannot access it like that."* [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

To access a service running inside a container from outside the host, you must **map a host port to a container port**. This is called **port mapping** or **port forwarding**. The syntax is `-p <host_port>:<container_port>`. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

For example, `-p 7090:80` means: when traffic arrives at the host machine on port 7090, route it to the container on port 80 (where Nginx is listening). The host port must be free (not used by another process or container). The container port is determined by what process runs inside the container — for Nginx, it's 80 by default. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

The instructor also notes that to access the container from outside (e.g., from your browser), the **host machine's security group** (EC2 in this case) must allow traffic on the host port. He adds a rule allowing all traffic from his IP, noting: *"We are going to run many, many containers here."* [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## 1.6 Container as a Process: The Host-Level View

The instructor proves that a container is literally **a process running on the host machine**, not a virtual machine. He runs `ps -ef` on the host and shows the Nginx container processes: *"That's the process ID of your container. That's actually your container."* Two processes are visible — the master Nginx process and a worker. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

He then proves the container is **a process running from a directory** by navigating to `/var/lib/docker/containers/`. Each container has a directory named with its full container ID. Inside: configuration files, hostname, resolv.conf — but the actual data (web content, binaries) comes from the image directory. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

This "container = process + directory" mental model is the most operationally useful understanding of what a container actually is at the system level.

***

## 1.7 Attaching to a Container: exec, -it, and the PID 1 Concept

You cannot SSH into a container — there is no SSH server running inside. The instructor asks: *"How can you really log into a process?"*   The answer is you don't "log in" — you **attach** to the container by running a new process inside it. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

The mechanism is `docker exec`. You can run a single command (`docker exec <container> ls /`) or start an interactive shell. For an interactive shell, you use `docker exec -it <container> /bin/bash`: <cite>turn11search3</cite>

* `-i` — Interactive mode (keeps STDIN open)
* `-t` — Allocates a TTY (terminal)
* `/bin/bash` — The command to run (a Bash shell)

Together, `-it` means: "Run this command in the container and attach me to it so I can interact with it." [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

Inside the container, running `ps -ef` reveals the process hierarchy. **PID 1** is always the container's main process — for Nginx, it's the Nginx master process; for Ubuntu, it's the Bash shell. The `bash` session you started via `exec` appears as a separate process. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**The critical rule:** If PID 1 dies, the container dies. The instructor demonstrates this with the Ubuntu container. When he types `exit`, it kills the Bash shell (which is PID 1 for that container), and the container immediately enters the exited state. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

For the Nginx container, typing `exit` in an `exec` session only kills the secondary bash process — not PID 1 (Nginx). So the container keeps running. The difference: your `exec` session is PID 34, not PID 1. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

🔍 **Deep Dive:**
This explains why `docker run ubuntu` immediately exits. The Ubuntu image's default command is `/bin/bash`. When run without `-it`, there's no terminal attached to the bash process, so bash has nothing to do and exits immediately. Since bash is PID 1, the container exits too. You must run `docker run -it ubuntu /bin/bash` to keep the shell alive by attaching your terminal to it. The Nginx image, in contrast, has its default command as the Nginx daemon, which runs continuously in the background — it doesn't need terminal interaction to stay alive. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## 1.8 Container Lifecycle and Cleanup: The Dependency Chain

The instructor demonstrates a strict **dependency chain** for cleanup: [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

1. A **running container** cannot be removed → must be **stopped** first
2. A **stopped container** cannot have its image removed → must be **removed** first
3. Only after all containers (running and stopped) are removed can the **image** be removed

The chain is: **Stop → Remove container → Remove image**. Attempting to skip any step produces an error. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

The instructor also notes that containers can store data (stateful containers), but if you want data to persist beyond the container's lifecycle, you must use **volumes** — a topic deferred to the next lecture. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are pulling images from Docker Hub, running containers from them, exploring container internals (networking, filesystem, processes), attaching to containers, and performing lifecycle management (start, stop, remove). The final outcome: operational comfort with Docker's core commands and a concrete understanding of how containers work at the system level. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## Phase 1: Pull and Inspect Images

### Step 1: Pull the Nginx Image

```bash
docker pull nginx
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**What happens:** Docker contacts Docker Hub (default registry), downloads the `nginx` image with the `latest` tag, and stores it locally. Multiple layers are downloaded.

### Step 2: List Local Images

```bash
docker images
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Expected output:** A table showing repository name, tag, image ID, creation time, and size. You should see `nginx` (latest, \~133MB) and `hello-world` (from previous lectures).

### Step 3: Pull an Image with a Specific Tag

```bash
docker pull nginx:mainline-alpine-perl
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**What happens:** Downloads a different variant of the Nginx image identified by this specific tag.

**Verification:** Run `docker images` again — you should see `nginx` listed twice: once with `latest` and once with `mainline-alpine-perl`. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## Phase 2: Run a Container with Port Mapping

### Step 4: Run Nginx in Detached Mode with Port Mapping

```bash
docker run --name my-web -d -p 7090:80 nginx
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Breakdown:**

* `docker run` — Create and start a container from an image
* `--name my-web` — Assign the name `my-web` to this container (easier to reference than IDs)
* `-d` — **Detached mode**: run in background, don't capture the terminal
* `-p 7090:80` — **Port mapping**: host port 7090 → container port 80 (Nginx)
* `nginx` — The image to use (defaults to `latest` tag)

**Expected output:** A long hexadecimal string — the full container ID. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Why `-d`:** Without it, Nginx would run in the foreground, capturing your shell. Since Nginx is a continuously running process (unlike hello-world which prints and exits), you need detached mode. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

### Step 5: Verify the Container is Running

```bash
docker ps
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Expected output:** A table showing the container ID (short form), image name, command, status (Up), and port mapping (`0.0.0.0:7090->80/tcp`).

### Step 6: Add Security Group Rule (EC2-Specific)

If running on an EC2 instance, add an inbound rule to the security group allowing traffic from your IP. The instructor adds **all traffic from my IP** to avoid repeated rule additions for different container ports. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

### Step 7: Access from Browser

Navigate to `http://<EC2_PUBLIC_IP>:7090` in your browser. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Expected result:** The default Nginx welcome page. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**What this proves:** Traffic flows: Browser → EC2 port 7090 → Docker port mapping → Container port 80 → Nginx process serves the page.

***

## Phase 3: Container Lifecycle Operations

### Step 8: Stop the Container

```bash
docker stop my-web
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Verification:** `docker ps` shows nothing. `docker ps -a` shows the container in **Exited** status.

### Step 9: Start the Container Again

```bash
docker start my-web
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Verification:** `docker ps` shows the container running again.

***

## Phase 4: Investigate Container Internals on the Host

### Step 10: View Container Processes on the Host

```bash
ps -ef
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**What to look for:** Nginx processes running on the host — these ARE the container. The instructor identifies two processes (master and worker). [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

### Step 11: Explore the Container Directory

```bash
sudo -i
cd /var/lib/docker/containers/
ls
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Expected:** Directories named with full container IDs. Match them to your running containers. Enter a container's directory to see configuration files (resolv.conf, hostname).

### Step 12: Verify Container Size

```bash
du -sh /var/lib/docker/containers/<container_id>/
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Expected:** \~**40 KB**. This proves the container stores almost nothing — all data comes from the image layers.

### Step 13: View Image Data Location

```bash
ls /var/lib/docker/image/
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Expected:** An `overlay2` directory with the distributed image layer data. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## Phase 5: Attach to a Container

### Step 14: Run a Command Inside the Container

```bash
docker exec my-web ls /
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**What happens:** Executes `ls /` inside the container and displays the output. You see a Linux directory structure (bin, etc, usr, var, etc.). The command runs and you stay on the host.

### Step 15: Attach an Interactive Shell

```bash
docker exec -it my-web /bin/bash
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**What happens:** A Bash shell starts inside the container and your terminal is attached to it. Your prompt changes — you are now "inside" the container.

**Inside the container:**

```bash
apt update
apt install procps -y
ps -ef
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Expected ps output:**

* **PID 1:** The Nginx master process (the container's main process)
* **PID 34 (or similar):** `/bin/bash` — your exec session

**Exit the container:**

```bash
exit
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**What happens:** The bash process (PID 34) is killed. You return to the host. The container **keeps running** because PID 1 (Nginx) is still alive.

**Important note:** Packages installed inside the container (like `procps`) are stored in the container's writable layer. This is **not recommended** for production — the data is ephemeral and lost when the container is removed. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

## Phase 6: Ubuntu Container — PID 1 Behavior

### Step 16: Run Ubuntu Without Flags

```bash
docker run ubuntu
docker ps
docker ps -a
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Result:** The container appears in `docker ps -a` in **Exited** state. It started and immediately died because the default command (bash) had no terminal attached and exited. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

### Step 17: Run Ubuntu Interactively

```bash
docker run -it ubuntu /bin/bash
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Result:** You're inside the Ubuntu container. Run `ps -ef` — PID 1 is `/bin/bash`.

Type `exit` → the bash process (PID 1) dies → the container exits immediately. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Key lesson:** For Ubuntu, bash IS the container's main process. Killing it kills the container. For Nginx, the Nginx daemon is PID 1 — exec'd bash sessions are secondary processes.

***

## Phase 7: Cleanup

### Step 18: Attempt Image Removal (Demonstrates Dependency)

```bash
docker rmi nginx:mainline-alpine-perl
```

**Result:** Succeeds (no container uses this specific tag). [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

```bash
docker rmi nginx
```

**Result:** **Fails** — a container (running or stopped) is using this image. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

### Step 19: Full Cleanup Chain

```bash
docker stop my-web
docker rm my-web
docker rm <ubuntu_container_names>
docker rmi nginx ubuntu hello-world
```

 [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

**Verification:**

```bash
docker ps -a
docker images
```

Both should return empty. Clean slate. [\[304-docker...d-concepts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/304-docker-commands-and-concepts.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Docker Hub / Registry

```
Docker Hub = Default registry (hub.docker.com)
  ├── Official images (from vendors: nginx, ubuntu, postgres...)
  ├── User images (your account, custom images)
  └── Image = "Repository" in registry terminology

Other registries: GCR, ECR, Nexus 3, JFrog, DTR
docker pull → goes to Docker Hub by default
```

***

## Image Architecture

```
Image = stopped container, archived, immutable
  ├── Multiple LAYERS (each layer = a filesystem change)
  ├── All layers = READ-ONLY
  ├── Has tags (versioning): nginx:latest, nginx:alpine
  ├── "latest" = convention, not guarantee
  └── Size: ~133MB (vs. VM AMI ~8GB minimum)

Image ≠ VM image
  VM image → cloned into independent VM
  Container image → container runs FROM it (connected, not cloned)
```

***

## Container-Image Relationship (CORE CONCEPT)

```
Container = thin read/write layer ON TOP of image layers

IMAGE LAYERS (read-only):
  ├── Layer 1: base OS files
  ├── Layer 2: installed packages
  └── Layer 3: application files

CONTAINER LAYER (read/write):
  └── ~40KB config files (resolv.conf, hostname)
      All visible data = actually from image layers

PROOF 1: Container dir (/var/lib/docker/containers/<id>/) = 40KB
PROOF 2: Cannot delete image while container exists (dependency)
PROOF 3: Image data lives in /var/lib/docker/image/overlay2/
```

***

## Container = Process + Directory

```
Host view:
  ps -ef → container processes visible as regular host processes
  /var/lib/docker/containers/<id>/ → container's config directory
  /var/lib/docker/image/overlay2/ → image data (shared by containers)

Container is NOT a VM — it's a process with an isolated filesystem view
```

***

## Port Mapping

```
Container = private network (like private subnet)
  Cannot access directly from outside

Port mapping: -p <host_port>:<container_port>
  -p 7090:80 → host:7090 routes to container:80

Requirements:
  ├── Host port must be FREE
  ├── Container port must match the process (nginx=80, tomcat=8080)
  └── Host security group must allow traffic on host port
```

***

## Container Modes

```
Foreground (default):    docker run nginx         → captures terminal
Detached (-d):           docker run -d nginx      → runs in background

Continuously running:    nginx, tomcat, mongo     → need -d
Run-and-exit:            hello-world, scripts     → no -d needed
```

***

## Attaching to Containers

```
docker exec <name> <command>           → run single command, stay on host
docker exec -it <name> /bin/bash       → attach interactive shell
  -i = interactive (STDIN open)
  -t = TTY (terminal allocation)

Inside container:
  Stripped-down OS (many commands missing)
  apt update / apt install = adds to writable layer (ephemeral)
  exit → kills YOUR process, not necessarily the container

No SSH in containers → exec is the access mechanism
If /bin/bash missing → try /bin/sh
```

***

## PID 1 Rule

```
PID 1 = container's main process
  PID 1 alive → container runs
  PID 1 dead  → container exits

nginx container:  PID 1 = nginx daemon    → exec bash = PID 34 → exit kills 34, not 1 → container lives
ubuntu container: PID 1 = /bin/bash       → exit kills PID 1 → container dies

docker run ubuntu → bash starts without terminal → exits immediately → container dead
docker run -it ubuntu /bin/bash → bash has terminal → stays alive → exit kills it → container dead
```

***

## Cleanup Dependency Chain

```
Running container → CANNOT remove
  └── docker stop <name>
Stopped container → CANNOT remove its image
  └── docker rm <name>
No containers → CAN remove image
  └── docker rmi <image>

MUST follow: STOP → REMOVE CONTAINER → REMOVE IMAGE
```

***

## Core Commands Summary

```
docker pull <image>              → download image from registry
docker images                    → list local images
docker run [flags] <image>       → create + start container
docker ps                        → list running containers
docker ps -a                     → list ALL containers (including exited)
docker stop <name|id>            → stop container
docker start <name|id>           → start stopped container
docker exec <name> <cmd>         → run command in container
docker exec -it <name> /bin/bash → attach shell to container
docker rm <name|id>              → remove stopped container
docker rmi <image>               → remove image (no containers using it)
```

***

## Operational Flow

```
── PULL ──
docker pull nginx → image downloaded (layers)
docker images → verify

── RUN ──
docker run --name my-web -d -p 7090:80 nginx
  → detached, port-mapped, named
docker ps → verify running
Browser: http://<HOST_IP>:7090 → Nginx welcome page

── INVESTIGATE ──
ps -ef (host) → container = host process
/var/lib/docker/containers/<id>/ → 40KB (config only)
/var/lib/docker/image/overlay2/ → actual data

── ATTACH ──
docker exec -it my-web /bin/bash → inside container
ps -ef → PID 1 = nginx, PID 34 = bash
exit → bash dies, container lives (PID 1 still nginx)

── UBUNTU EXPERIMENT ──
docker run ubuntu → exits immediately (bash has no terminal)
docker run -it ubuntu /bin/bash → stays alive
exit → PID 1 (bash) dies → container dies

── CLEANUP ──
docker stop → docker rm → docker rmi
Dependency: stop → remove container → remove image
```

***

## Reusable Engineering Patterns

| Pattern                            | Manifestation                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| **Layered immutable filesystem**   | Image layers (read-only) + container layer (read/write) = space efficiency    |
| **Process-not-VM mental model**    | Container = process on host + isolated filesystem view, not a virtual machine |
| **Port forwarding for isolation**  | Private network container → mapped host port → external access                |
| **PID 1 lifecycle binding**        | Main process lifecycle = container lifecycle                                  |
| **Dependency chain for cleanup**   | Must respect: stop → remove container → remove image                          |
| **Registry as distribution layer** | Docker Hub = centralized image distribution, multiple registries possible     |
| **Tag-based versioning**           | Same image name, different tags = different versions, "latest" is convention  |

***

## Core Mental Model

```
Image = Immutable layered filesystem template (read-only, archived)
Container = Process running from that template (thin r/w layer on top)

They are CONNECTED, not cloned:
  Container reads data FROM image layers
  Container stores ~nothing itself (40KB config)
  Removing image requires removing container first

Container on host = just a process + a directory
  Visible in ps -ef, stored in /var/lib/docker/
  
PID 1 = the container's soul
  PID 1 alive → container alive
  PID 1 dead → container dead

Access: exec -it (not SSH)
Network: port mapping (private → mapped host port)
Registry: Docker Hub (default), many alternatives exist
```

***

This material captures every concept, command, proof demonstration, filesystem investigation, PID 1 behavior, and lifecycle rule from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
