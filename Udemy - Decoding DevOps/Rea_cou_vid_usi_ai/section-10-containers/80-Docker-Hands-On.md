# 🎓 Deep Learning Material: Docker Hands-On — Containers, Images, Port Mapping & Image Building

*Reconstructed from video captions — [80-hands-on-docker-containers.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt?EntityRepresentationId=04b4c8c3-3480-47a8-a72c-c68892293d5c), with supporting resource files: [80.Vagrantfile.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.Vagrantfile.txt?EntityRepresentationId=e783192f-b9d6-4b99-8e8f-d5b4f3b91b6d), [80.dockerInstallOnUbuntu.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.dockerInstallOnUbuntu.txt?EntityRepresentationId=3c62a0a6-1cf3-40a8-8e0b-d8e2ac4218f3), [80.docker\_hands\_on\_commands.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt?EntityRepresentationId=900a042d-fb19-49e6-86fb-3a767cd18308)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Lab Environment Architecture: Vagrant → VM → Docker Engine

The hands-on environment follows a **layered infrastructure pattern**. You are not installing Docker directly on your host machine. Instead, you use **Vagrant** to create an **Ubuntu 20 virtual machine** inside VirtualBox, and Docker Engine is installed **inside that VM** via Vagrant's provisioning mechanism. This means your working architecture is: **Host OS → VirtualBox → Ubuntu VM → Docker Engine → Containers**. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt), [\[80.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.Vagrantfile.txt)

The Vagrantfile serves a dual purpose. First, it defines the VM itself — based on the `ubuntu/focal64` box, with a private network IP of `192.168.56.82` and a public (bridged) network interface. Second, its `provision "shell"` block contains the complete Docker Engine installation commands. This means when you run `vagrant up`, the VM is created **and** Docker is automatically installed in one operation — you don't need to manually install Docker after the VM is ready. [\[80.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.Vagrantfile.txt)

The Docker installation commands inside the Vagrantfile come directly from Docker's official documentation (docs.docker.com → Get Docker → Linux → Ubuntu). They follow a specific sequence: update the package index, install prerequisite packages (`ca-certificates`, `curl`, `gnupg`), set up Docker's official GPG key for package verification, add Docker's APT repository to the system's sources list, update the package index again (now including Docker's repo), and finally install the Docker engine packages (`docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`, `docker-compose-plugin`). [\[80.dockerI...llOnUbuntu \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.dockerInstallOnUbuntu.txt)

> 🔍 **Deep Dive:** The GPG key step (`curl -fsSL ... | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`) is a **trust verification mechanism**. When you add a third-party repository (Docker's), your system needs a way to verify that the packages it downloads are genuinely from Docker and haven't been tampered with. The GPG key is Docker's cryptographic signature. The `dearmor` converts it from ASCII-armored format to binary format that APT can use. The `chmod a+r` ensures all users can read the keyring file. Without this step, APT would refuse to install packages from Docker's repository because it can't verify their authenticity. [\[80.dockerI...llOnUbuntu \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.dockerInstallOnUbuntu.txt)

***

## 1.2 Docker Engine as a Service

Once the VM is provisioned, Docker Engine runs as a **systemd service** — a background daemon managed by the operating system's init system. This is not a one-time program you launch; it is a persistent service that starts at boot and continuously listens for commands. You verify this with `systemctl status docker`, which reports the service state. The service is described as "Docker Application Container Engine" — this name reveals its nature: it is an **engine** (a runtime that executes work) for **application containers** (isolated process environments). [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

The Docker Engine is the **control plane** for everything container-related on this machine. Every `docker` command you type in the terminal is actually a **client request** sent to this engine daemon. The engine receives the request, executes it (pull an image, create a container, stop a container, etc.), and returns the result. If this service is not running, no Docker command will work. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

## 1.3 Images and Containers — The Core Relationship

This is the most fundamental concept in Docker. An **image** is a read-only template — a packaged filesystem plus metadata that defines what a container will contain and how it will behave. A **container** is a running (or stopped) instance created from an image. The relationship is analogous to a **class and an object** in programming: the image is the blueprint, the container is the live instance. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

When you run `docker run hello-world`, the word `hello-world` is the **image name**. Docker first checks if this image exists **locally** on the Docker Engine. If it does not, Docker automatically **pulls** it from **Docker Hub** — a public registry of images. The video explicitly shows the message "unable to find image locally" followed by "pull complete", demonstrating this pull-on-demand behavior. The image is downloaded once and cached locally; subsequent runs use the local copy. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

The `hello-world` image is an extremely minimal image. It contains a single binary whose only job is to print a test message and exit. This is important conceptually: **a container only lives as long as its main process runs.** The hello-world container starts, prints its message, the process completes, and the container immediately enters the **Exited** state. It is not deleted — it still exists as a stopped container — but it is no longer running. This is visible in `docker ps -a` (shows all containers, including exited ones) but not in `docker ps` (shows only running containers). [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

> 🔍 **Deep Dive:** Every container gets an auto-generated **container ID** (a unique hash) and an auto-generated **name** (like `relaxed_sammet`). Docker assigns these random human-readable names automatically unless you explicitly specify a name with the `--name` flag. The container ID is the authoritative identifier; the name is a convenience alias. Both can be used in commands to reference the container. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

## 1.4 Container Networking and Port Mapping

Containers run inside Docker's **internal network**. They get their own private IP addresses (from the `172.17.0.x` range by default on the bridge network) that are **not accessible from outside the Docker host**. This is a critical architectural fact: if you run a web server in a container, nobody outside the VM can reach it by default — not your host machine, not your browser, not the internet. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Port mapping** is the mechanism that solves this isolation problem. It creates a bridge between a port on the **host** (the VM) and a port on the **container**. The syntax is `-p HOST_PORT:CONTAINER_PORT`. When traffic arrives at the host's IP on the host port, Docker **routes** (forwards) that traffic to the container on the container port. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

The video demonstrates this with `-p 9080:80` on an Nginx container. Port 80 is Nginx's default port **inside the container**. Port 9080 is an arbitrarily chosen port on the **host VM**. The result: accessing `VM_IP:9080` from a browser sends the request to the VM, which Docker intercepts and forwards to the Nginx container on port 80. The response travels back through the same path. From the outside, it looks like the VM is serving web content on port 9080; in reality, the container is doing the work on port 80. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

There are two ways to access a containerized service:

1. **Internally** (from within the Docker host): Use the container's private IP + container port. Discovered via `docker inspect`. Example: `curl http://172.17.0.2:80`. This works because you're already inside the Docker host's network. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)
2. **Externally** (from outside the Docker host — your browser, another machine): Use the host VM's IP + host port. Example: `http://192.168.56.82:9080`. This requires port mapping to be configured. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

> ⚠️ **Expert Note:** The distinction between `-p` (lowercase) and `-P` (uppercase) is significant. Lowercase `-p` lets you **explicitly specify** both the host port and container port (`-p 9080:80`). Uppercase `-P` tells Docker to **automatically assign a random high-numbered host port** and map it to every port that the image's Dockerfile declares via `EXPOSE`. The video demonstrates both: `-p 9080:80` for the Nginx container and `-P` for the custom-built image (which auto-assigned port 49154). Uppercase `-P` is convenient for quick testing but gives you no control over which host port is used. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

## 1.5 Building Custom Images — The Dockerfile

While you can pull pre-built images from Docker Hub, real-world usage requires building **custom images** that contain your own application. This is done through a **Dockerfile** — a text file containing a sequence of instructions that Docker executes in order to assemble an image. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

The Dockerfile demonstrated in the video uses a **multi-stage build** pattern and several key instructions: [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**`FROM ubuntu:latest AS BUILD_IMAGE`** — This declares the **base image**. Every custom Docker image is built **on top of** an existing image. The base image is usually an official image from Docker Hub (like `ubuntu`, `alpine`, `nginx`). The `AS BUILD_IMAGE` part names this stage for a multi-stage build — this first stage is a temporary build environment, not the final image. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**`RUN`** — Executes commands inside the image during build time. The first stage uses `RUN` to install `wget` and `unzip`, download a website template from tooplate.com, unzip it, and compress it into a `.tgz` archive. Each `RUN` instruction creates a new layer in the image. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**`FROM ubuntu:latest`** (second occurrence) — This starts the **second stage** of the multi-stage build. It begins fresh from a clean Ubuntu image. The build artifacts from stage one are not automatically included — only what you explicitly copy over survives. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**`COPY --from=BUILD_IMAGE /root/tween.tgz /var/www/html/`** — This is the multi-stage bridge. It copies the compressed website archive from the first stage (`BUILD_IMAGE`) into the second stage's filesystem. The benefit: the final image does not contain `wget`, `unzip`, or any build-time tools — only the final artifact. This keeps the image **small and clean**. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**`LABEL`, `ENV`, `CMD`, `VOLUME`, `WORKDIR`, `EXPOSE`** — Additional instructions that set metadata (`LABEL "project"="Marketing"`), environment variables (`ENV DEBIAN_FRONTEND=noninteractive` to suppress interactive prompts), the default command to run when a container starts (`CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]`), declare a volume mount point (`VOLUME /var/log/apache2`), set the working directory (`WORKDIR /var/www/html/`), and declare which port the container listens on (`EXPOSE 80`). [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

> 🔍 **Deep Dive:** The `CMD` instruction is particularly important. It defines the **main process** of the container. When this process exits, the container stops. The `"-D", "FOREGROUND"` flag for Apache is critical — without it, Apache would start as a background daemon and immediately return control, causing the container to think its main process has completed and exit. Running in the foreground keeps the process alive, which keeps the container alive. This foreground requirement is a universal Docker pattern: the main process **must** run in the foreground. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

The `docker build -t tesimg .` command triggers the build. The `-t` flag assigns a **tag** (name) to the resulting image. The `.` (dot) tells Docker where to find the Dockerfile — the current working directory. Docker reads the Dockerfile, executes each instruction sequentially, creates layers, and produces a final image. If you've already built the image before, Docker uses **cached layers** for unchanged steps, making rebuilds much faster. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

## 1.6 Container Lifecycle and Cleanup

Containers and images persist on disk until explicitly removed. Stopped containers remain in the `Exited` state indefinitely. Unused images remain cached. Over time, this accumulates disk usage and clutter. The video emphasizes cleanup as an operational discipline — especially important when preparing for subsequent labs that need a **clean environment**. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

The lifecycle operations are: **stop** (gracefully halt a running container), **rm** (remove a stopped container entirely), and **rmi** (remove an image). The order matters: you cannot remove a running container without stopping it first, and you cannot remove an image if containers (even stopped ones) still reference it. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up a Docker Engine inside a Vagrant-managed Ubuntu VM, then performing three core Docker operations: running a pre-built test container (`hello-world`), running and accessing a production-grade web server container (`nginx`) with port mapping, and building a custom Docker image from a Dockerfile containing a website. The final outcome: you can build, run, access, and clean up Docker containers end-to-end. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

## Phase 1: Environment Setup

### Step 1 — Prepare the Working Directory and Vagrantfile

**What we are doing:** Creating a project directory on your host machine and placing the Vagrantfile in it.

Open Git Bash or your terminal. Create a directory anywhere on your system (the video uses `F:\container`). Download the Vagrantfile from the course resource section and place it inside this directory. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

```bash
mkdir container
cd container
# Place Vagrantfile here (downloaded from course resources)
```

**Why:** Vagrant expects a `Vagrantfile` in the working directory. All `vagrant` commands operate relative to this file's location. The Vagrantfile defines both the VM configuration and the Docker installation provisioning script. [\[80.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.Vagrantfile.txt)

**Connection to flow:** This directory becomes your project root for all subsequent Vagrant and Docker operations.

***

### Step 2 — Bring Up the VM

**What we are doing:** Creating and provisioning the Ubuntu VM with Docker pre-installed.

```bash
vagrant up
```

**What each part does:**

* `vagrant` — the Vagrant CLI tool
* `up` — the command to create, configure, and provision the VM as defined in the Vagrantfile

**What happens internally:** Vagrant downloads the `ubuntu/focal64` box (if not already cached), creates a VirtualBox VM, configures networking (private IP `192.168.56.82` + bridged public network), boots the VM, and then executes the shell provisioning block — which runs the entire Docker installation sequence. This takes time on first run. [\[80.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.Vagrantfile.txt), [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Expected result:** The VM is running with Docker Engine installed and active.

**Common mistake:** Running `vagrant up` from the wrong directory (one without a Vagrantfile). Always ensure you're in the directory containing the Vagrantfile.

***

### Step 3 — Log Into the VM and Become Root

```bash
vagrant ssh
sudo -i
```

**Breakdown:**

* `vagrant ssh` — opens an SSH session into the running VM
* `sudo -i` — switches to the **root user** with a login shell. Docker commands typically require root privileges (unless your user is added to the `docker` group). [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

### Step 4 — Verify Docker Engine Is Running

```bash
systemctl status docker
```

**Breakdown:**

* `systemctl` — the systemd service manager command
* `status` — show current state of a service
* `docker` — the service name

**Expected output:** Active (running), described as "Docker Application Container Engine." [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Failure scenario:** If the status shows `inactive` or `failed`, the provisioning may have encountered errors. Re-run `vagrant provision` to retry the installation, or manually run the Docker installation commands from [80.dockerInstallOnUbuntu.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.dockerInstallOnUbuntu.txt?EntityRepresentationId=3c62a0a6-1cf3-40a8-8e0b-d8e2ac4218f3). [\[80.dockerI...llOnUbuntu \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.dockerInstallOnUbuntu.txt)

**Connection to flow:** All subsequent Docker commands depend on this service running. This is always your first verification step.

***

## Phase 2: Running Pre-Built Containers

### Step 5 — Run the Hello-World Test Container

```bash
docker run hello-world
```

**Breakdown:**

* `docker` — the Docker CLI client
* `run` — create and start a new container
* `hello-world` — the image name (from Docker Hub)

**What happens internally:**

1. Docker checks local image cache → image not found
2. Docker pulls `hello-world` image from Docker Hub → "Unable to find image locally... pull complete"
3. Docker creates a container from this image
4. The container's main process executes (prints a test message)
5. The process exits → container enters `Exited` state [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Verification:**

```bash
docker images
```

Shows all locally cached images. You should see `hello-world` listed. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

```bash
docker ps
```

Shows running containers. **Empty** — because the hello-world container already exited. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

```bash
docker ps -a
```

Shows **all** containers including stopped ones. You'll see the hello-world container with status `Exited`, its auto-generated container ID, the command it ran (`/hello`), and its auto-assigned name (e.g., `relaxed_sammet`). [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Connection to flow:** This confirms Docker Engine works end-to-end — pull, create, run, exit. Now we move to persistent, accessible containers.

***

### Step 6 — Run an Nginx Container with Port Mapping

```bash
docker run --name web01 -d -p 9080:80 nginx
```

**Breakdown of every part:**

* `docker run` — create and start a new container
* `--name web01` — assign the explicit name `web01` to this container (instead of a random name)
* `-d` — **detached mode**: run the container in the background, not attached to your terminal. Without this, Nginx's output would flood your terminal and you'd lose your shell prompt
* `-p 9080:80` — **port mapping**: map host port `9080` to container port `80`. Traffic hitting the VM on port 9080 is forwarded to the container's port 80
* `nginx` — the image name. Nginx is a web server; its official image is on Docker Hub [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**What happens internally:**

1. Docker checks for `nginx` image locally → not found on first run
2. Docker pulls `nginx` from Docker Hub
3. Docker creates a container named `web01`
4. Docker starts Nginx inside the container (listening on port 80 internally)
5. Docker configures the port mapping rule: `host:9080 → container:80`
6. The container runs in the background [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Verification:**

```bash
docker ps
```

Now shows `web01` as a running container, with the image `nginx`, and the port mapping `0.0.0.0:9080->80/tcp`. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

### Step 7 — Access the Container Internally

**What we are doing:** Accessing the Nginx web server from inside the Docker host using the container's private IP.

First, discover the container's internal IP:

```bash
docker inspect web01
```

**Breakdown:**

* `docker inspect` — returns detailed JSON metadata about a container
* `web01` — the container name (or you can use the container ID)

Look for the `IPAddress` field in the output. It will be something like `172.17.0.2`. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

Now access it:

```bash
curl http://172.17.0.2:80
```

**Breakdown:**

* `curl` — command-line HTTP client
* `http://172.17.0.2:80` — the container's internal IP and port

**Expected result:** Raw HTML output of Nginx's default welcome page. The terminal cannot render HTML, so you see the raw markup — this is normal and confirms the web server is responding. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Connection to flow:** This proves the container is serving content. Next, we make it accessible externally.

***

### Step 8 — Access the Container Externally (From Browser)

**What we are doing:** Accessing the Nginx container from your host machine's browser via port mapping.

First, find the VM's IP address:

```bash
ip addr show
```

Look for the **bridge** or **private network** IP (the `192.168.56.82` we configured, or the bridged network IP). [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

Now, in your **host machine's browser**, enter:

```
http://<VM_IP>:9080
```

**Expected result:** The Nginx default welcome page renders properly in the browser. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**What's happening in the full chain:**

```
Browser → VM_IP:9080 → Docker port mapping → Container web01:80 → Nginx response → back through the chain
```

**Common mistake:** Using the container's internal IP (`172.17.0.2`) in the browser. This won't work — that IP is only reachable from inside the Docker host. From outside, you must use the VM's IP + the mapped host port.

**Connection to flow:** You've now proven the complete external access path. This is how containerized applications are exposed to users in practice.

***

## Phase 3: Building a Custom Image

### Step 9 — Create the Dockerfile

```bash
mkdir images
cd images/
vim Dockerfile
```

**Breakdown:**

* `mkdir images` — create a working directory for the image build
* `cd images/` — enter it
* `vim Dockerfile` — create the Dockerfile. **The `D` must be capital** — Docker looks for this exact filename by default [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Paste the following Dockerfile content:** [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

```dockerfile
FROM ubuntu:latest AS BUILD_IMAGE
RUN apt update && apt install wget unzip -y
RUN wget https://www.tooplate.com/zip-templates/2128_tween_agency.zip
RUN unzip 2128_tween_agency.zip && cd 2128_tween_agency && tar -czf tween.tgz * && mv tween.tgz /root/tween.tgz

FROM ubuntu:latest
LABEL "project"="Marketing"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install apache2 git wget -y
COPY --from=BUILD_IMAGE /root/tween.tgz /var/www/html/
RUN cd /var/www/html/ && tar xzf tween.tgz
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
VOLUME /var/log/apache2
WORKDIR /var/www/html/
EXPOSE 80
```

**What this Dockerfile does conceptually:** It builds a web application image in two stages. Stage 1 downloads and packages a website template. Stage 2 creates a clean Apache web server image, copies only the packaged website from Stage 1, and configures Apache to serve it. The video notes this is essentially the same exercise as hosting a website on a VM — but now done inside a container. Detailed Dockerfile instruction explanations are deferred to Section 20 of the course. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

Save and exit vim (`:wq`).

***

### Step 10 — Build the Image

```bash
docker build -t tesimg .
```

**Breakdown:**

* `docker build` — the image build command
* `-t tesimg` — **tag** the resulting image with the name `tesimg`. You can choose any name
* `.` — the **build context path**. This tells Docker where to find the Dockerfile. The dot means "current directory" [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**What happens internally:** Docker reads the Dockerfile, executes each instruction sequentially (pulling base images, running commands, copying files), creates image layers, and produces a final tagged image. First builds take longer because nothing is cached. Subsequent builds reuse cached layers for unchanged steps. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Verification:**

```bash
docker images
```

You should see `tesimg` listed among the images, along with the base `ubuntu` images and any previously pulled images. [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**Common note:** The video mentions the build was fast because the image was already built previously (cached layers). For a first-time build, expect it to take significantly longer due to package downloads and installations.

***

### Step 11 — Run a Container from the Custom Image

```bash
docker run -P -d tesimg
```

**Breakdown:**

* `docker run` — create and start a container
* `-P` — **uppercase P**: automatically map a random host port to every `EXPOSE`d port in the image (port 80 in this case). Docker assigns a high-numbered port like `49154`
* `-d` — detached/background mode
* `tesimg` — the custom image we just built [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Verification:**

```bash
docker ps
```

Shows the running container with an auto-assigned port mapping (e.g., `0.0.0.0:49154->80/tcp`). [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

```bash
ip addr show
```

Note the VM's IP address again.

**In your browser:**

```
http://<VM_IP>:49154
```

(Replace `49154` with whatever port `docker ps` shows.)

**Expected result:** The Tooplate website template renders in the browser, served from inside the container. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

**Connection to flow:** You've now completed the full image-building lifecycle — from Dockerfile to running, accessible container serving your own application.

***

## Phase 4: Cleanup

### Step 12 — Stop All Running Containers

```bash
docker ps
docker stop web01 heuristic_hugle
```

**Breakdown:**

* `docker stop` — sends a graceful stop signal to running containers
* `web01 heuristic_hugle` — you can specify multiple container names/IDs in a single command [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt), [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

***

### Step 13 — Remove All Stopped Containers

```bash
docker rm heuristic_hugle web01 competent_gates elastic_ramanujan relaxed_sammet
```

**Breakdown:**

* `docker rm` — removes stopped containers entirely (deletes their filesystem)
* List all container names/IDs to remove. This includes containers from the hello-world run and any other stopped containers [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**Common mistake:** Trying to `docker rm` a running container. You must `docker stop` it first.

***

### Step 14 — Remove All Images

```bash
docker images
docker rmi a54ee9c44b3b 6130c26b5558 057d51c0049c 825d55fb6340 12766a6745ee feb5d9fea6a5
```

**Breakdown:**

* `docker rmi` — remove images by ID or name
* List all image IDs to remove. Use `docker images` first to get the IDs [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt)

**Common mistake:** Trying to remove an image while a container (even a stopped one) still references it. Remove all containers first, then remove images.

**Expected result:** `docker images` returns empty. `docker ps -a` returns empty. Clean slate. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

> ⚠️ **Expert Note:** The video explicitly emphasizes cleaning up before the next lecture. This is an operational discipline: Docker labs often depend on a known starting state. Leftover containers or images from previous exercises can cause port conflicts, name conflicts, or unexpected behavior. Always clean up between lab sessions unless instructed otherwise. [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ Environment Architecture Stack

```
Host OS (Windows/Mac)
  └── VirtualBox
       └── Ubuntu 20 VM (Vagrant-managed)
            ├── IP: 192.168.56.82 (private) + bridged (public)
            ├── Docker Engine (systemd service)
            │    └── Internal Network: 172.17.0.x
            │         ├── Container A (own IP, own ports)
            │         ├── Container B (own IP, own ports)
            │         └── ...
            └── Vagrantfile provisioning = auto-installs Docker
```

## 🔑 Core Object Relationship

```
Image (read-only template, stored in Docker Hub or local cache)
  │
  ├── docker pull ← fetches from Docker Hub if not local
  │
  └── docker run ← creates →  Container (live instance)
                                  ├── Running (docker ps)
                                  ├── Exited  (docker ps -a)
                                  ├── docker stop → Exited
                                  ├── docker rm   → Deleted
                                  └── Main process exits → Container exits
```

## 🌐 Port Mapping — Access Chain

```
INTERNAL ACCESS (inside Docker host):
  curl http://CONTAINER_IP:CONTAINER_PORT
  Example: curl http://172.17.0.2:80
  Discovery: docker inspect <container>

EXTERNAL ACCESS (browser / outside):
  http://HOST_VM_IP:HOST_PORT
  Example: http://192.168.56.82:9080
  Requires: -p HOST_PORT:CONTAINER_PORT at docker run time

MAPPING MODES:
  -p 9080:80   → explicit: you choose host port
  -P           → automatic: Docker assigns random high port to all EXPOSEd ports
```

## 🐳 Image Build Flow (Dockerfile → Image → Container)

```
Dockerfile (text instructions)
  │
  docker build -t NAME .
  │
  ├── Stage 1 (BUILD_IMAGE): FROM ubuntu → install tools → download → package artifact
  │
  ├── Stage 2 (Final):       FROM ubuntu → install runtime → COPY --from=Stage1 artifact
  │                           → CMD (foreground process) → EXPOSE → VOLUME → WORKDIR
  │
  └── Output: Tagged Image (NAME)
       │
       docker run -P -d NAME → Running Container → accessible via HOST_IP:AUTO_PORT
```

## 📋 Command Quick-Reference Chain

```
VERIFY:     systemctl status docker
IMAGES:     docker images
RUNNING:    docker ps
ALL:        docker ps -a
INSPECT:    docker inspect <name|id>
HOST IP:    ip addr show

RUN:        docker run [--name X] [-d] [-p H:C | -P] IMAGE
BUILD:      docker build -t NAME .
STOP:       docker stop <name|id> [name2...]
REMOVE:     docker rm <name|id> [name2...]
REMOVE IMG: docker rmi <id|name> [id2...]
```

## 🔄 Container Lifecycle State Machine

```
Image ──docker run──→ [Running] ──process exits──→ [Exited]
                          │                            │
                     docker stop ──→ [Exited]          │
                                        │              │
                                   docker rm ──→ [Deleted]
                                   
Image ──docker rmi──→ [Deleted]  (only if no containers reference it)
```

## 🧩 Cleanup Dependency Order

```
MUST follow this sequence:
  1. docker stop  (running → exited)
  2. docker rm    (exited → deleted)
  3. docker rmi   (image → deleted)

Violation: rm running container → ERROR
Violation: rmi image with existing container → ERROR
```

## 🔁 Reusable Engineering Patterns

| Pattern                                   | Manifestation                                                               |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| **Layered infrastructure**                | Host → VM → Engine → Container (each layer isolates the next)               |
| **Provisioning as code**                  | Vagrantfile shell block = reproducible Docker installation                  |
| **Pull-on-demand**                        | Image fetched from registry only when not locally cached                    |
| **Process = lifecycle**                   | Container lives only while main process runs; foreground required           |
| **Multi-stage build**                     | Build tools in Stage 1, copy only artifacts to Stage 2 → small clean image  |
| **Port mapping as access bridge**         | Internal network isolation + explicit port forwarding = controlled exposure |
| **Explicit vs. automatic mapping**        | `-p` = control, `-P` = convenience (trade-off: predictability vs. speed)    |
| **Immutable template → mutable instance** | Image (frozen) → Container (live, stateful, disposable)                     |
| **Clean state discipline**                | Cleanup between operations to prevent conflicts and ensure reproducibility  |

## ⚡ Key Gotchas for Fast Recall

```
❌ Container IP in browser          → Won't work from outside host
✅ Host IP + mapped port in browser → Correct external access

❌ Dockerfile with lowercase 'd'    → Docker won't find it by default
✅ Dockerfile with capital 'D'      → Correct

❌ CMD runs background daemon        → Container exits immediately
✅ CMD runs foreground process        → Container stays alive

❌ docker rm on running container    → Error
✅ docker stop first, then rm        → Correct sequence
```

***

This completes the full reconstruction of the Docker Hands-On video. All content is grounded exclusively in the caption and resource files.  Want me to generate Anki flashcards (CSV) from this material, or dive deeper into any specific section? [\[80-hands-o...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80-hands-on-docker-containers.txt), [\[80.docker_...n_commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.docker_hands_on_commands.txt), [\[80.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.Vagrantfile.txt), [\[80.dockerI...llOnUbuntu \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/80.dockerInstallOnUbuntu.txt)
