# 🐳 Vprofile Project on Containers — Deep Learning Material

**Source:** Video caption file — [81-vprofile-project-on-containers.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt?EntityRepresentationId=75420937-a17a-49e3-93d9-8256e45a02d1), with supporting files: [81.Vagrantfile.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt?EntityRepresentationId=baa8ff80-cfe6-4a2b-a5f8-5a2fa8d30146), [81.docker-compose.yml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml?EntityRepresentationId=434bd2a8-42c9-4be3-a7c8-950d01285196), [81.vprofile\_docker-compose.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.vprofile_docker-compose.txt?EntityRepresentationId=1c3a0e7f-cdbe-4855-8da1-e4cfd99a4e3b) [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt), [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml), [\[81.vprofil...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.vprofile_docker-compose.txt)

**Video Context:** The instructor demonstrates how to run the entire Vprofile multi-tier application (Nginx, Tomcat, RabbitMQ, Memcached, MySQL) — previously deployed on separate VMs — as containers on a single VM using Docker Compose. This is positioned as a "trailer" for the full Docker section; everything here is ready-made. The detailed building-from-scratch happens later.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Core Idea — From Multiple VMs to Containers on a Single VM

In the earlier Vprofile project setup, the application stack was deployed across **separate virtual machines** — one VM for Nginx, one for Tomcat, one for RabbitMQ, one for Memcached, and one for MySQL. Each VM ran a full operating system, consumed significant RAM, CPU, and disk, and took considerable time to provision and configure individually. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

This lecture demonstrates the **container-based alternative**: all five services run as **containers** on a **single virtual machine**. Instead of five separate OS instances, you have one VM running a Docker engine, and each service runs as a lightweight, isolated process (a container) sharing the host VM's kernel. The instructor explicitly states this is "one of a very big reason the world is shifting towards the container" — the ease and speed of deploying complex multi-service applications. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

The conceptual shift is fundamental: **VMs virtualize hardware** (each VM gets its own kernel, OS, and full resource allocation). **Containers virtualize the operating system** (each container shares the host kernel but gets its own isolated filesystem, processes, and network). This means containers start in seconds, consume far less memory, and allow you to run many more services on the same hardware.

🔍 **Deep Dive:** The instructor's Vagrantfile allocates the VM with a default VirtualBox memory configuration. He explicitly warns to **shut down all other VMs** before bringing this one up, to avoid running out of resources. This highlights a practical reality: even though containers are lightweight, the host VM still needs sufficient resources to run the Docker engine plus all container workloads. The constraint moved from "one VM per service" to "one VM total, but it must be adequately resourced." [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

***

## 1.2 The Vprofile Application Architecture — Five Services, One Stack

The Vprofile application is a multi-tier web application with five distinct services, each handling a specific responsibility: [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**Nginx (vproweb)** — The front-end web server. It listens on port 80 and acts as a reverse proxy, routing incoming HTTP requests to the Tomcat application server. Users never talk to Tomcat directly; Nginx is the entry point. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

**Tomcat (vproapp)** — The Java application server. It runs the actual Vprofile web application, serves the login page, handles user authentication, and processes business logic. It listens on port 8080. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

**MySQL/MariaDB (vprodb)** — The relational database. It stores user data and application data. Tomcat connects to it for authentication and data retrieval. It listens on port 3306. The root password is set via an environment variable (`MYSQL_ROOT_PASSWORD=vprodbpass`). [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

**Memcached (vprocache01)** — The caching layer. When user data is retrieved from the database, it gets cached in Memcached. Subsequent requests for the same data are served from cache instead of hitting the database again. It listens on port 11211. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

**RabbitMQ (vpromq01)** — The message queue. It handles asynchronous messaging between application components. It listens on port 15672 (management interface). Default credentials are `guest/guest`. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

The **request flow** through the stack: User browser → Nginx (:80) → Tomcat (:8080) → MySQL (:3306) for authentication/data → Memcached (:11211) for caching → RabbitMQ (:15672) for messaging. The instructor validates this exact chain during the demonstration. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

🔍 **Deep Dive:** Looking at the docker-compose.yml, two services have **persistent volumes**: `vprodb` mounts `vprodbdata:/var/lib/mysql` (the MySQL data directory) and `vproapp` mounts `vproappdata:/usr/local/tomcat/webapps` (the Tomcat application deployment directory). This means the database data and the deployed application survive container restarts. Memcached, RabbitMQ, and Nginx have no persistent volumes — Memcached is inherently ephemeral (it's a cache), RabbitMQ queues are transient in this setup, and Nginx's configuration is baked into the image. This volume design reflects the nature of each service: **stateful services get volumes, stateless/ephemeral services don't.** [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

***

## 1.3 Docker Compose — Orchestrating Multi-Container Applications

When you need to run **multiple containers that work together as a single application**, managing each container individually (starting, stopping, networking, configuring) becomes tedious and error-prone. **Docker Compose** solves this problem. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

Docker Compose is a tool that reads a declarative configuration file — `docker-compose.yml` — and from that single file, creates, starts, networks, and manages all the containers defined in it. Instead of running five separate `docker run` commands with complex flags, you write one YAML file describing your entire stack and run one command: `docker compose up`. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

The `docker compose` command provides several operations: `up` (create and start all containers), `down` (stop and remove all containers), `ps` (list running containers in the composition), `stop` (stop without removing). The instructor notes these will be covered in detail later — for now, the key operations are `up -d` (start in background) and `down` (clean teardown). [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

The docker-compose.yml file structure follows a declarative pattern: you define **services** (each service = one container type), and for each service you specify the **image** to use, **ports** to expose, **volumes** for persistence, and **environment variables** for configuration. Docker Compose handles the rest — pulling images, creating containers, connecting them to a shared network, and starting them in the right order. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

⚠️ **Expert Note:** The instructor explicitly says "don't need to understand this entire docker compose file now" — this lecture is intentionally a preview. The compose file, image building, and detailed Docker concepts are covered in the dedicated Docker section. The pedagogical pattern here is: **see the result first, understand the mechanism later.** This gives the learner a mental anchor for where the Docker section is heading. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

***

## 1.4 Container Images — Pre-built and Ready-Made

Every container runs from an **image** — a read-only template containing the application, its dependencies, and its configuration. In this lecture, all images are **pre-built** and stored on **Docker Hub** under the account `vprocontainers`. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

Three images are custom-built for the Vprofile project:

* `vprocontainers/vprofiledb` — MySQL with Vprofile schema and data pre-loaded
* `vprocontainers/vprofileapp` — Tomcat with the Vprofile application deployed
* `vprocontainers/vprofileweb` — Nginx configured as a reverse proxy for the Vprofile Tomcat backend

Two images are **official/community images** used as-is:

* `memcached` — the standard Memcached image
* `rabbitmq` — the standard RabbitMQ image

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

The instructor navigates to Docker Hub, searches for `vprocontainers`, and shows the three custom images stored there. The key concept: Docker Hub is a **registry** — a centralized repository where images are stored and pulled from. When `docker compose up` runs, it checks if the required images exist locally; if not, it **pulls** them from Docker Hub automatically. The first run takes significant time because all five images must be downloaded. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

***

## 1.5 The Vagrantfile — Infrastructure as Code for the Host VM

The VM itself is provisioned using Vagrant with a specific Vagrantfile that does two things: creates an Ubuntu VM and **automatically installs the entire Docker toolchain** inside it via a shell provisioner. [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt)

The Vagrantfile specifies:

* **Base box:** `ubuntu/focal64` (Ubuntu 20.04 LTS)
* **Private network:** IP `192.168.56.82` — this is how you access the VM from the host browser
* **Public network:** bridged networking — the VM also gets an IP on the physical network
* **Shell provisioner:** A sequence of commands that installs Docker's GPG key, adds Docker's official APT repository, and installs `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`, and `docker-compose-plugin`. It also downloads the standalone `docker-compose` binary (v2.1.1). [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt)

The engineering reasoning: by embedding Docker installation into the Vagrantfile, the entire setup is **reproducible**. Anyone with the Vagrantfile can run `vagrant up` and get a Docker-ready VM without any manual installation steps. This is a practical example of **Infrastructure as Code** — the VM's desired state (Ubuntu + Docker installed) is codified in a file, and provisioning is automated.

🔍 **Deep Dive:** The provisioner installs Docker using the **official Docker repository** method (not the Ubuntu default `docker.io` package). This ensures the latest Docker CE version. It adds the GPG key, configures the repository with architecture detection (`dpkg --print-architecture`) and Ubuntu version detection (`. /etc/os-release && echo "$VERSION_CODENAME"`), and then installs the full Docker stack. This is the recommended installation method for production-grade Docker setups. [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt)

***

## 1.6 The Source Repository — Branch-Based Organization

The Vprofile project source code is hosted on GitHub under the `devopshydclub/vprofile-project` repository. The docker-compose.yml file lives in a specific **branch** called `docker`, inside a `compose/` folder. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

The instructor demonstrates: navigate to the repository, click the branch dropdown, switch to the `docker` branch, then navigate to `compose/docker-compose.yml`. To download the file directly to the VM, click the **Raw** button to get a direct URL, then use `wget` to download it. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

The instructor encounters a download failure and attributes it to **GitHub restrictions in India**. The fallback: download the compose file from the course's resource section (a zip file), open it with a text editor, copy the content, and manually create the file using `vim docker-compose.yml` on the VM. This fallback pattern — always having an alternative source — is a practical operational habit. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

***

## 1.7 Validation — Proving the Entire Stack Works

After all containers are running, the instructor performs a systematic validation by accessing the application through the browser and exercising the entire request chain: [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

1. **Nginx validation** — Accessing `VM_IP:80` in the browser reaches the Nginx container, which routes to Tomcat.
2. **Tomcat validation** — The Vprofile login page appears, served by the Tomcat container.
3. **MySQL validation** — Logging in with `admin_vp` / `admin_vp` succeeds, proving Tomcat successfully authenticated against the database.
4. **RabbitMQ validation** — Checking RabbitMQ shows a queue was generated, confirming the messaging service is operational.
5. **Memcached validation** — Clicking "All Users" and selecting a user shows data served from cache, confirming the caching layer is active.

This validation sequence is deliberate — it traces the entire data flow through every component, proving not just that containers are running, but that they are **communicating correctly with each other**. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

***

## 1.8 Cleanup — `docker compose down` and `docker system prune -a`

Two cleanup commands are demonstrated: [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**`docker compose down`** stops all running containers in the composition and **removes** them. The containers cease to exist, but the images remain on disk (available for faster future `docker compose up`).

**`docker system prune -a`** goes further: it removes all stopped containers **and** all unused images. After this command, the system is completely clean — no containers, no images. The next `docker compose up` would need to pull all images again from Docker Hub.

The instructor shows these as a two-step cleanup: `down` for the containers, `prune -a` for a full reset. This distinction matters: `down` is for "I'm done for now but might come back" while `prune -a` is for "I want a completely clean slate."

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are deploying the entire Vprofile multi-tier application — Nginx, Tomcat, RabbitMQ, Memcached, MySQL — as **five Docker containers on a single VM**, using Docker Compose. The final outcome: a fully functional web application accessible from the host browser at `VM_IP:80`, with all five services communicating seamlessly. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

***

## Step 1: Prepare the Working Directory and Vagrantfile

Create a folder on your host machine for this project. The instructor creates `containerIntro`. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

Download the Vagrantfile from the course resource section (provided as a zip file). Extract it and identify the correct Vagrantfile for your platform:

* **Windows / MacOS Intel** — one Vagrantfile
* **MacOS M1 chip** — a separate Vagrantfile

Copy the correct Vagrantfile into your project folder. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**Verification:** You should have a single file named `Vagrantfile` (no extension) in your project folder.

**Common mistake:** Using the wrong Vagrantfile for your platform. M1 Macs need the ARM-specific file.

**Connection to larger flow:** This Vagrantfile is special — it not only creates the VM but also installs the entire Docker toolchain automatically (see Theory §1.5). [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt)

***

## Step 2: Clean Up Existing VMs and Bring Up the Docker VM

### Check existing VMs:

```bash
vagrant global-status --prune
```

**Breakdown:**

* `vagrant global-status` — lists all Vagrant VMs across your entire system, regardless of which directory you're in
* `--prune` — removes stale/invalid entries from the list (VMs that were manually deleted or whose directories no longer exist) [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**What to do:** If any VMs show as `running` or `powerup`, navigate to their respective directories and shut them down:

```bash
vagrant halt
```

Or delete them entirely. The instructor emphasizes: **make sure you shut down all other VMs** to avoid running out of resources (RAM, CPU). [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

### Bring up the Docker VM:

```bash
vagrant up
```

**What happens internally:** Vagrant reads the Vagrantfile, creates an Ubuntu 20.04 VM in VirtualBox, configures networking (private IP `192.168.56.82` + bridged public network), and then runs the shell provisioner. The provisioner executes a sequence of `apt-get` commands to install Docker CE, Docker CLI, containerd, Docker Buildx, Docker Compose plugin, and the standalone docker-compose binary. This takes significant time on the first run. [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt)

**Expected result:** After completion, the VM is running with Docker fully installed and ready.

**Failure scenarios:**

* If you don't have enough RAM, the VM may fail to start or be very slow. Shut down other VMs.
* If the Docker installation fails (network issues during apt-get), you may need to `vagrant destroy` and try again, or `vagrant ssh` in and manually re-run the provisioner commands.

***

## Step 3: Log Into the VM and Switch to Root

```bash
vagrant ssh
```

**Breakdown:** Opens an SSH session into the running VM.

```bash
sudo -i
```

**Breakdown:** Switches to the root user. Docker commands require root privileges (or the user being in the `docker` group). [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

```bash
clear
```

Clears the terminal for a clean working area.

***

## Step 4: Verify Docker Compose Is Available

```bash
docker compose
```

**What this does:** Running `docker compose` without a subcommand displays the help/options screen. This is a quick verification that Docker Compose is installed and functional. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**Expected output:** A list of available subcommands — `up`, `down`, `ps`, `stop`, etc.

**If this fails:** Docker Compose wasn't installed correctly during provisioning. Check if `docker` itself works (`docker --version`). If Docker is missing, the provisioner failed — re-run provisioning or install manually.

***

## Step 5: Create the Compose Directory and Get the docker-compose.yml File

### Create and enter the working directory:

```bash
mkdir compose
cd compose/
```

 [\[81.vprofil...er-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.vprofile_docker-compose.txt)

### Method A — Download from GitHub (may fail in some regions):

Navigate to the GitHub repository `devopshydclub/vprofile-project`, switch to the **`docker`** branch, go to the `compose/` folder, click on `docker-compose.yml`, click the **Raw** button, and copy the URL. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

```bash
wget https://raw.githubusercontent.com/devopshydclub/vprofile-project/docker/compose/docker-compose.yml
```

**Breakdown:**

* `wget` — command-line download tool
* The URL — the raw content URL of the docker-compose.yml file from the `docker` branch

**If this fails** (as it did for the instructor due to GitHub access restrictions in India): use Method B. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

### Method B — Manual creation from resource section:

Download the resources zip from the course, extract it, find the `compose/` folder, open `docker-compose.yml` in a text editor, and copy its contents. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

On the VM:

```bash
vim docker-compose.yml
```

Press `i` for insert mode, paste the content (in Git Bash: `Shift+Insert`), press `Esc`, type `:wq` to save and quit.

### Verify the file:

```bash
ls
vim docker-compose.yml
```

Confirm the file exists and its content matches the expected compose structure (five services: vprodb, vprocache01, vpromq01, vproapp, vproweb). [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)

**Common mistakes:**

* Spelling `docker-compose.yml` incorrectly (the instructor explicitly warns about this)
* Pasting with wrong indentation (YAML is indentation-sensitive)
* Being in the wrong directory

**Connection to larger flow:** This YAML file is the single source of truth for the entire multi-container deployment. Everything from here depends on this file being correct.

***

## Step 6: Bring Up All Containers

```bash
docker compose up -d
```

**Breakdown:**

* `docker compose` — the orchestration command
* `up` — create and start all services defined in docker-compose.yml
* `-d` — detached mode (run in the background; returns control to the terminal) [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**What happens internally:**

1. Docker Compose reads `docker-compose.yml`
2. For each service, it checks if the required image exists locally
3. If not, it **pulls** the image from Docker Hub (this is what takes time on first run)
4. After all images are available, it creates containers for each service
5. It creates a shared network for inter-container communication
6. It starts all five containers

**Expected output:** Progress messages showing images being pulled, then containers being created and started. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**First run vs. subsequent runs:** The first `docker compose up` is slow because all five images must be downloaded. Subsequent runs are fast because images are cached locally (unless you ran `docker system prune -a`).

***

## Step 7: Verify All Containers Are Running

```bash
docker compose ps
```

**What this does:** Lists all containers managed by the current docker-compose.yml, showing their names, status, and port mappings. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**Expected output:** Five containers, all showing status as `Up` or `running`:

* vprodb (:3306)
* vprocache01 (:11211)
* vpromq01 (:15672)
* vproapp (:8080)
* vproweb (:80)

### Also verify images:

```bash
docker images
```

Should show five images from which the containers were created. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**If a container is not running:** It may have crashed on startup. Use `docker compose logs <service_name>` to check logs (not shown in the video, but implied debugging approach).

***

## Step 8: Find the VM's IP Address

```bash
ip addr show
```

**What to look for:** An IP address on the `192.168.x.x` range. The Vagrantfile assigns `192.168.56.82` as the private network IP. The VM may also have a bridged network IP (also in the `192.168.x.x` range). **Do NOT use** the `10.0.2.x` address — that's VirtualBox's internal NAT. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt), [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt)

The instructor identifies the interface `enp0s9` and uses a `192.168.x.x` IP address.

**Common mistake:** Copying the wrong IP (the NAT one). Always use a `192.168.x.x` address.

***

## Step 9: Validate the Application in the Browser

Open a browser on your **host machine** and navigate to:

```
http://<VM_IP>:80
```

### Validation sequence: [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

**9a. Nginx + Tomcat:** The page loads → Nginx on port 80 received the request and routed it to the Tomcat container. You see the Vprofile login page.

**9b. MySQL/Database:** Enter username `admin_vp` and password `admin_vp`, click Login. Successful login = Tomcat authenticated against the MySQL database container.

**9c. RabbitMQ:** After login, check the RabbitMQ section — it should show a generated queue. This confirms the RabbitMQ container is operational and communicating with the application.

**9d. Memcached:** Click "All Users," select any user. The data should indicate it's being served from cache. This confirms the Memcached container is active and caching is working.

**If login fails:** Database container might not be running or the schema isn't loaded. Check `docker compose ps` and container logs.

**Connection to larger flow:** This validation proves end-to-end functionality — not just "containers are running" but "the entire distributed application works as an integrated system."

***

## Step 10: Cleanup

### Stop and remove containers:

```bash
docker compose down
```

**What it does:** Stops all running containers in the composition and removes them. Images remain on disk. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

### Full system cleanup (optional):

```bash
docker system prune -a
```

**What it does:** Removes ALL stopped containers AND all unused images. After this, the system is completely clean — no containers, no images. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

⚠️ **Expert Note:** Only run `docker system prune -a` if you want a full reset. If you plan to run `docker compose up` again soon, skip this — keeping the images locally means the next startup is instant instead of requiring a full re-download.

### Exit and power off:

```bash
exit       # exit root shell
exit       # exit vagrant ssh
vagrant halt   # power off the VM
```

**To resume later:** `vagrant up` in the same folder → `vagrant ssh` → `sudo -i` → `cd compose/` → `docker compose up -d`. [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Architecture — VMs vs. Containers

```
BEFORE (VM-based Vprofile):
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ VM:Nginx │ │VM:Tomcat │ │VM:RabbitMQ│ │VM:Memcache│ │VM:MySQL  │
│ Full OS  │ │ Full OS  │ │ Full OS  │ │ Full OS  │ │ Full OS  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
   5 VMs × Full OS each = heavy resource usage

AFTER (Container-based Vprofile):
┌──────────────────────────────────────────────────────┐
│                  Single VM (Ubuntu)                   │
│  ┌─────────┐┌────────┐┌─────────┐┌────────┐┌──────┐ │
│  │ Nginx   ││Tomcat  ││RabbitMQ ││Memcache││MySQL │ │
│  │ :80     ││ :8080  ││ :15672  ││ :11211 ││:3306 │ │
│  └─────────┘└────────┘└─────────┘└────────┘└──────┘ │
│              Docker Engine + Compose                  │
└──────────────────────────────────────────────────────┘
   1 VM, shared kernel, 5 lightweight containers
```

***

## 🔗 Request Flow Chain

```
Browser → Nginx(:80) → Tomcat(:8080) → MySQL(:3306) → [auth OK]
                                      → Memcached(:11211) → [cache hit]
                                      → RabbitMQ(:15672) → [queue generated]
```

***

## 📦 Docker Compose File — Service Map

```
docker-compose.yml (v3.8)
│
├── vprodb
│   ├── image: vprocontainers/vprofiledb
│   ├── port: 3306:3306
│   ├── volume: vprodbdata:/var/lib/mysql  ← STATEFUL
│   └── env: MYSQL_ROOT_PASSWORD=vprodbpass
│
├── vprocache01
│   ├── image: memcached (official)
│   └── port: 11211:11211                 ← STATELESS
│
├── vpromq01
│   ├── image: rabbitmq (official)
│   ├── port: 15672:15672
│   └── env: guest/guest                  ← STATELESS
│
├── vproapp
│   ├── image: vprocontainers/vprofileapp
│   ├── port: 8080:8080
│   └── volume: vproappdata:/usr/local/tomcat/webapps ← STATEFUL
│
└── vproweb
    ├── image: vprocontainers/vprofileweb
    └── port: 80:80                        ← STATELESS (config in image)
```

***

## ⚡ Operational Command Sequence

```
SETUP:
  mkdir containerIntro → copy Vagrantfile
  vagrant global-status --prune       ← clean stale entries
  (halt other VMs)
  vagrant up                          ← creates VM + installs Docker

RUN:
  vagrant ssh → sudo -i → clear
  docker compose                      ← verify compose works
  mkdir compose → cd compose/
  wget <raw-github-url>               ← get docker-compose.yml
    OR vim docker-compose.yml         ← manual paste (fallback)
  docker compose up -d                ← start all 5 containers (background)
  docker compose ps                   ← verify: 5 containers running
  docker images                       ← verify: 5 images present
  ip addr show                        ← find 192.168.x.x IP

VALIDATE:
  Browser → VM_IP:80                  ← Nginx responds
  Login: admin_vp / admin_vp          ← MySQL validates
  Check RabbitMQ → queue generated    ← MQ works
  All Users → select user → from cache ← Memcached works

CLEANUP:
  docker compose down                 ← stop + remove containers
  docker system prune -a              ← remove ALL images + containers
  exit → exit → vagrant halt          ← power off VM

RESUME:
  vagrant up → vagrant ssh → sudo -i → cd compose/ → docker compose up -d
```

***

## 🏗️ Image Sourcing Map

```
Docker Hub
├── vprocontainers/ (custom account)
│   ├── vprofiledb     ← MySQL + Vprofile schema
│   ├── vprofileapp    ← Tomcat + Vprofile app
│   └── vprofileweb    ← Nginx + reverse proxy config
│
└── Official images
    ├── memcached      ← used as-is
    └── rabbitmq       ← used as-is

Source: GitHub → devopshydclub/vprofile-project → branch:docker → compose/
Fallback: Course resource section (zip download)
```

***

## 🧱 Infrastructure Provisioning Chain

```
Vagrantfile
├── Box: ubuntu/focal64
├── Network: private 192.168.56.82 + public (bridged)
└── Shell Provisioner:
    ├── apt-get update
    ├── Install prerequisites (ca-certificates, curl, gnupg)
    ├── Add Docker GPG key → /etc/apt/keyrings/docker.gpg
    ├── Add Docker apt repo (arch-aware, version-aware)
    ├── apt-get update (with new repo)
    ├── Install: docker-ce, docker-ce-cli, containerd.io,
    │            docker-buildx-plugin, docker-compose-plugin
    └── Download standalone docker-compose v2.1.1
```

***

## 🔁 Reusable Engineering Patterns

**Pattern 1: Declarative Orchestration**
One YAML file defines the entire multi-service stack → one command deploys it → one command tears it down. State is declared, not imperatively built. (docker-compose.yml → `docker compose up` → `docker compose down`)

**Pattern 2: Stateful vs. Stateless Service Design**
Services that hold persistent data (MySQL, Tomcat apps) get volumes. Services that are inherently ephemeral or reconstructable (Memcached, RabbitMQ, Nginx) don't. Volume assignment follows data lifecycle.

**Pattern 3: Infrastructure as Code Layering**
Vagrantfile automates VM + Docker installation → docker-compose.yml automates container deployment. Two layers of IaC: infrastructure layer (Vagrantfile) and application layer (Compose). Neither requires manual intervention.

**Pattern 4: Fallback Source Strategy**
Primary source (GitHub wget) → Fallback (course resource zip + manual copy). Always have an alternative acquisition path for critical files. The instructor demonstrated this live when the download failed.

**Pattern 5: End-to-End Validation Chain**
Don't just check "are containers running" — trace the full request path through every component (Nginx → Tomcat → DB → Cache → MQ) to prove integration, not just individual health.

***

## 🎯 One-Line System Summary

> **A Vagrantfile provisions a Docker-ready VM, a docker-compose.yml declaratively defines five services (Nginx → Tomcat → MySQL + Memcached + RabbitMQ), `docker compose up -d` pulls images and starts all containers, and end-to-end validation through the browser confirms the entire Vprofile stack works as an integrated system on a single machine.** [\[81-vprofil...containers \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81-vprofile-project-on-containers.txt), [\[81.Vagrantfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.Vagrantfile.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/81.docker-compose.yml)
