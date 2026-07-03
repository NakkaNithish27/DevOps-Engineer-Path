# 🏗️ Build and Run Microservice App with Docker Compose — Deep Learning Material

**Source:** Video caption files — [323-build-and-run-microservice-app.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt?EntityRepresentationId=30a3c25a-7aaf-45cc-b518-2c1c7d1a7676) and [323.intDockerAndCompose.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323.intDockerAndCompose.txt?EntityRepresentationId=4ebbd66a-68d1-403d-a990-38851ef76e87) [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt), [\[323.intDoc...AndCompose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323.intDockerAndCompose.txt)

**Video Context:** The instructor takes a Docker Compose file (reviewed in the previous lecture in VS Code) and uses it to **build and run an entire microservice application** on an EC2 instance. The application has multiple services: an Angular front-end in Nginx, a Java Web API, a Node.js eMart API, MongoDB, MySQL, and an Nginx API gateway. The lecture covers instance sizing decisions, user data for Docker installation, the full build-and-run workflow, image layer caching for incremental builds, foreground vs. background execution, validation through the browser, and cleanup.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Docker Compose Build-and-Run Workflow — Two Distinct Phases

The instructor makes a clear architectural separation: "First we will build, and then after that we will run the container. Because build takes a very long time." Docker Compose can handle both phases, but they are conceptually and operationally distinct. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**`docker-compose build`** — reads the `build` instructions in the docker-compose.yml file (which reference Dockerfiles for each service), and builds Docker images from source code. This is the **compilation phase** — source code is transformed into runnable images. This phase is slow because it involves downloading dependencies, compiling code, and assembling filesystem layers.

**`docker-compose up`** — reads the `run` configuration in the docker-compose.yml (ports, networks, volumes, environment variables) and creates/starts containers from the built images. This is the **execution phase** — images are instantiated as running processes. For services that use pre-built images (like MongoDB, MySQL, Nginx), this phase pulls them from Docker Hub.

The instructor summarizes the compose file's dual role: "Docker Compose file has build step and how to run the container option also." One file describes both how to build the images and how to run the containers — the complete lifecycle definition. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## 1.2 The Microservice Application Architecture

The application consists of **six containers** working together: [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**Three custom-built images (built from source code via Dockerfiles):**

* **Client** — an Angular front-end application hosted in an Nginx container. This serves the UI that users interact with in the browser.
* **Web API** — a Java application hosted in a JDK container. This is one of the backend APIs.
* **eMart API** — a Node.js application running in a Node.js container. This handles the eMart business logic (login, registration, book smart features).

**Three pre-built images (pulled from Docker Hub):**

* **MongoDB** — NoSQL database (likely used by the Node.js eMart API)
* **MySQL** — relational database (likely used by the Java Web API)
* **Nginx** — the API gateway that routes incoming requests to the appropriate backend service

The traffic flow: **Browser → Nginx API gateway (:80) → routes to Client (Angular pages) or Web API (Java) or eMart API (Node.js) → which connect to MongoDB or MySQL for data.**

The instructor validates this after deployment: "These pages are coming from the Nginx Angular content, and the login — all that intelligent work coming through the API of Node. So all the services are working together." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## 1.3 Multi-Stage Build Images — The Unnamed Layers

After the build completes, the instructor runs `docker images` and observes: "You see some other containers — sorry, images — which does not have any name. These are the build images. So when you do multi-stage, you'll also see your build images." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

Multi-stage Docker builds use intermediate images for compilation (e.g., a full JDK image to compile Java code), then copy only the compiled output into a smaller runtime image (e.g., a JRE image). The intermediate build images remain in the local image store but are unnamed (shown as `<none>` in `docker images`). They consumed disk space but are not used to run containers — they were just build tools.

***

## 1.4 Image Layer Caching — Why Rebuilds Are Fast

The instructor demonstrates a critical Docker optimization: "If you're thinking if it takes that much longer every time — no, we already have the images. There's already image layers which are already cached, so only the changes will be built." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

He runs `docker-compose build` a second time (without any code changes) and shows it completes almost instantly: "You see, that was faster." Docker images are built in **layers** — each instruction in the Dockerfile creates a layer. Docker caches every layer. On subsequent builds, Docker checks if each layer has changed: if not, it uses the cached version. Only layers that changed (and all layers after them) are rebuilt.

This means incremental builds — where only a few lines of application code changed — rebuild only the affected layers, not the entire image. The instructor connects this to microservice development practice: "In microservices, it's always encouraged to make small, small changes multiple times, rather than making big and huge changes. So any small change, you build the image once again and you run the container and test it." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

The operational cycle is: **pull changes → docker-compose build (fast, only changed layers) → docker-compose up (test) → repeat**. And: "This all part can be automated by using a CI/CD pipeline." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## 1.5 Instance Sizing — Why t2.micro Won't Work

The instructor makes a deliberate infrastructure decision: "This instance cannot be t2.micro. It needs to be t3.medium." The reasons: [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

* **RAM:** t2.micro has 1 GB. Running multiple containers (Angular build, Java compilation, Node.js, MongoDB, MySQL, Nginx) simultaneously requires much more memory. t3.medium has **4 GB**.
* **CPU:** t2.micro has 1 vCPU. Building multiple images and running multiple containers benefits from **2 CPUs** (t3.medium).
* **Network:** "Internet speed will be also better on this one" — pulling images from Docker Hub and downloading dependencies is faster on a larger instance.
* **Disk:** The default 8 GB volume is insufficient. The instructor sets **20 GB** — "8 GB will not work. We will need minimum 15 GB." Source code, build dependencies, multiple images, and container layers all consume significant disk space.

The cost consideration: "Yes, there will be some charges and you just need it for less than an hour. So the charges will be very minute." This is a practical cloud usage pattern — use a larger instance temporarily for build-heavy work, then stop it to avoid ongoing charges. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## 1.6 User Data Script — Automated Docker + Compose Installation

The instructor uses EC2 **User Data** to automate the setup of the Docker engine on first boot. The script (`323.intDockerAndCompose.txt`) performs three steps: [\[323.intDoc...AndCompose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323.intDockerAndCompose.txt)

1. **Install Docker Engine** — follows the standard Docker CE installation process (add GPG key, add repository, install `docker-ce`, `docker-ce-cli`, `containerd.io`)
2. **Install Docker Compose** — downloads the standalone `docker-compose` binary (v1.29.2) from GitHub and makes it executable with `chmod +x`
3. **Add ubuntu user to the docker group** — so Docker commands work without `sudo`

The instructor notes a fallback: "For some reason, if this does not work, you login to this EC2 instance and execute the steps manually." This is defensive operational practice — always have a manual fallback for automated provisioning. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## 1.7 Foreground vs. Background Execution

The instructor demonstrates both modes of `docker-compose up`: [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**Without `-d` (foreground):** "If you want to run it in the foreground, don't use Hyphen D option. So you can see all the output of all the containers." The terminal shows live logs from all containers — Web API, eMart DB, all services. This is useful for watching startup behavior and debugging. But your terminal is locked — you can't type other commands. To stop, press **Ctrl+C**, which stops all containers.

**With `-d` (background/detached):** "Docker Compose up -d to run it in the background." Containers start and the terminal returns immediately. You can then use commands like `docker ps`, `docker logs <container>`, `docker-compose ps`, `docker-compose top` to inspect the running system.

The instructor shows the practical workflow: first run in foreground to watch everything start, verify it's working, then Ctrl+C to stop, then re-run with `-d` for normal operation. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## 1.8 Port Mapping — Accessing the Application

The instructor explains: "We already did port mapping — Nginx container port 80 mapped with port 80 of the host. So we just need to access our Docker engine, which is the EC2 instance, on port 80." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

The EC2 instance's public IP on port 80 reaches the Nginx API gateway container, which routes to the appropriate backend containers. The user never directly accesses the backend containers — all traffic flows through the Nginx gateway.

***

## 1.9 Application Validation — End-to-End Proof

The instructor validates the entire microservice stack through the browser: [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

1. Navigate to `http://<EC2-IP>` — the Angular front-end loads (served by the Nginx/Client container)
2. Click **Register** — fill in details (email, password, ID number) — the registration flow goes through the Node.js eMart API to MongoDB
3. **Log in** — authentication works, proving the API and database are connected
4. Click **Book Smart** — the books API responds, proving the Java Web API is functional

"It's a sample application, so it's not fully functional, but we see all the services are connected." The validation proves the **integration**, not the completeness of the application. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building and running a **complete microservice application** (Angular + Java + Node.js + MongoDB + MySQL + Nginx gateway) using Docker Compose on an EC2 instance. The final outcome: a working multi-container application accessible from a browser, demonstrating the full Docker Compose build-and-run lifecycle. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## Step 1: Launch the EC2 Instance

Navigate to **EC2 Console → Launch Instance**. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**Settings:**

* **Name:** `Docker engine`
* **AMI:** Ubuntu Server 20 (Ubuntu 20.04)
* **Instance type:** `t3.medium` (4 GB RAM, 2 vCPU) — t2.micro is insufficient for building and running multiple containers simultaneously
* **Key pair:** Create new — name it `docker-key`, type `.pem`. Download and save.
* **Security group:**
  * SSH (port 22) from **My IP**
  * HTTP (port 80) from **Anywhere** (0.0.0.0/0) — needed to access the Nginx API gateway from the browser
* **Storage:** Change volume size to **20 GB**, type GP2
* **Advanced Details → User Data:** Paste the contents of the Docker installation script (`323.intDockerAndCompose.txt`) [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt), [\[323.intDoc...AndCompose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323.intDockerAndCompose.txt)

The user data script installs Docker Engine, Docker Compose, and adds the `ubuntu` user to the `docker` group — all automatically on first boot.

Click **Launch Instance**.

**Wait 5-10 minutes** for the instance to launch and the user data script to complete. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**Cost note:** t3.medium incurs charges. You need it for less than an hour. Stop or terminate the instance when done. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## Step 2: SSH In and Verify Docker Installation

```bash
ssh -i downloads/docker-key.pem ubuntu@<public-ip>
```

### Verify Docker group membership:

```bash
id
```

**Expected output:** The output should include `docker` in the groups list. If you see the docker group, it confirms: Docker was installed successfully AND the ubuntu user was added to the docker group. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

### Verify Docker Compose:

```bash
docker-compose --version
```

**Expected output:** Docker Compose version (e.g., `1.29.2`). [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**If either fails:** The user data script didn't complete. Log in and execute the installation steps manually (install Docker, install docker-compose, `sudo usermod -aG docker ubuntu`, then logout/login).

***

## Step 3: Clone the Source Code Repository

```bash
git clone <repository-URL>
```

**Breakdown:**

* `git clone` — downloads the entire repository
* `<repository-URL>` — the GitHub URL for the microservice project (provided in the course) [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**Expected result:** A new directory containing the source code, Dockerfiles for each service, and the `docker-compose.yml` file.

**Verification:** `ls` should show the cloned repository directory. Navigate into it.

**Connection to flow:** This repository contains everything Docker Compose needs — the docker-compose.yml file references Dockerfiles within the repository for the build step, and the source code that those Dockerfiles compile.

***

## Step 4: Build All Images

```bash
docker-compose build
```

**What this does:** Reads the docker-compose.yml, finds all services with `build` directives, and builds Docker images for each one using their respective Dockerfiles. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**What happens internally:**

* For the **Client** (Angular): installs npm dependencies, builds the Angular app, copies the built static files into an Nginx image
* For the **Web API** (Java): compiles Java code with Maven/Gradle, packages it, copies the JAR into a JDK runtime image
* For the **eMart API** (Node.js): installs npm dependencies, copies the Node.js application into a Node.js runtime image

**This takes a long time** (first build). The instructor explicitly says: "Take your time. Or maybe if you want to take a break, take a break." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**Expected result after build:**

```bash
docker images
```

Should show: [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

* **client** — the Angular/Nginx image
* **webapi** — the Java/JDK image
* **emartapi** (or similar) — the Node.js image
* Several `<none>` images — these are **multi-stage build intermediates** (the compilation stages that are discarded after the final image is produced)

***

## Step 5: Run All Containers (Foreground First)

```bash
docker-compose up
```

**Without `-d`** — runs in foreground. You see live logs from all containers. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**What happens:**

1. For services using pre-built images (MongoDB, MySQL, Nginx) — Docker **pulls** them from Docker Hub
2. For services with locally built images (client, webapi, emartapi) — Docker creates containers directly from local images
3. All containers start and their logs stream to your terminal

**Expected output:** Log lines from Web API, eMart DB, and other services showing startup activity. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**When it stabilizes:** The log output slows down — all services have started.

***

## Step 6: Validate in the Browser

Open a browser and navigate to:

```
http://<EC2-public-IP>
```

Port 80 is the default HTTP port — no need to specify it explicitly. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

### Validation sequence:

**6a.** Page loads → **Angular front-end is working** (Nginx serving client container content)

**6b.** Click **Register** → fill in fake details (email, password, ID number) → click Register → **Node.js eMart API + MongoDB are working** (registration data flows through API to database) [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**6c.** **Log in** with the registered credentials → successful login → **authentication flow is working**

**6d.** Click **Book Smart** → books data loads → **Java Web API + MySQL are working** (book data flows from Java API to MySQL)

"All the services are working together." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**If the page doesn't load:** Check the security group allows HTTP (port 80) from your IP or anywhere. Check `docker-compose ps` to verify all containers are running.

***

## Step 7: Switch to Background Mode

In the foreground terminal, press **Ctrl+C** — this stops all containers. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

Then restart in background:

```bash
docker-compose up -d
```

**Breakdown:**

* `-d` — detached mode (runs in background, returns terminal control) [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

### Inspect running containers:

```bash
docker ps
```

Shows all running containers with their names, ports, and status. [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

### Check logs of a specific container:

```bash
docker logs <container-name>
```

### Other useful commands:

```bash
docker-compose ps     # show compose-managed containers
docker-compose top    # show processes in containers
```

 [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## Step 8: Demonstrate Incremental Build (Layer Caching)

```bash
docker-compose build
```

**Run build again** (without any code changes). [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

**Expected result:** Completes almost instantly. Docker detects that no layers have changed and uses cached versions for everything.

**The point:** Future builds after small code changes will only rebuild the affected layers. "In microservices, it's always encouraged to make small, small changes multiple times. Any small change, you build the image once again and you run the container and test it." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

***

## Step 9: Cleanup

### Stop and remove all containers:

```bash
docker-compose down
```

"Stopped and removed all the containers." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

### Optionally remove images:

```bash
docker image prune -a
```

Or remove specific images with `docker rmi <image-name>`.

### Stop the EC2 instance:

Navigate to EC2 Console → select the instance → **Actions → Instance State → Stop**.

"Because it's t3.medium. If it's in a stop state, there won't be any extra bills. Only when you run it, that time you will see charges." [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt)

If you're completely done, you can **Terminate** instead. Stopping preserves the instance for later reuse.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Microservice Application Architecture

```
BROWSER
    │ HTTP :80
    ▼
┌──────────────────────────────────────────────┐
│           EC2 Instance (t3.medium)            │
│           20 GB, Ubuntu 20, Docker + Compose  │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │        Nginx API Gateway (:80)          │  │
│  │        (pre-built, pulled from Hub)     │  │
│  └───┬──────────┬──────────┬───────────────┘  │
│      │          │          │                  │
│      ▼          ▼          ▼                  │
│  ┌────────┐ ┌────────┐ ┌────────┐             │
│  │ Client │ │Web API │ │eMart  │             │
│  │Angular │ │ Java   │ │API    │             │
│  │in Nginx│ │in JDK  │ │Node.js│             │
│  │BUILT   │ │BUILT   │ │BUILT  │             │
│  └────────┘ └───┬────┘ └───┬────┘             │
│                 │          │                  │
│                 ▼          ▼                  │
│           ┌────────┐ ┌────────┐               │
│           │ MySQL  │ │MongoDB │               │
│           │PULLED  │ │PULLED  │               │
│           └────────┘ └────────┘               │
│                                               │
│  BUILT = from source via Dockerfile           │
│  PULLED = pre-built from Docker Hub           │
└──────────────────────────────────────────────┘
```

***

## ⚡ Two-Phase Workflow

```
PHASE 1: BUILD
  docker-compose build
  ├── Reads docker-compose.yml → finds 'build' directives
  ├── Builds 3 custom images from Dockerfiles:
  │   ├── client (Angular → Nginx)
  │   ├── webapi (Java → JDK)
  │   └── emartapi (Node.js → Node)
  ├── SLOW on first run (dependencies, compilation)
  ├── FAST on subsequent runs (layer caching)
  └── Produces: named images + unnamed multi-stage intermediates (<none>)

PHASE 2: RUN
  docker-compose up [-d]
  ├── Pulls 3 pre-built images (MongoDB, MySQL, Nginx)
  ├── Creates 6 containers from all images
  ├── Starts all containers with networking/ports/volumes
  └── Application accessible at http://<host-IP>:80
```

***

## 🔗 Command Sequence — Full Operational Flow

```
1. LAUNCH:   EC2 t3.medium, Ubuntu 20, 20GB, User Data (Docker install)
2. WAIT:     5-10 min for user data script
3. SSH:      ssh -i docker-key.pem ubuntu@<IP>
4. VERIFY:   id (docker group?) + docker-compose --version
5. CLONE:    git clone <repo-URL>
6. BUILD:    docker-compose build          ← SLOW first time
7. VERIFY:   docker images                 ← 3 named + N unnamed
8. RUN FG:   docker-compose up             ← watch logs
9. TEST:     Browser → http://<IP> → register → login → book smart
10. STOP:    Ctrl+C                        ← stop foreground
11. RUN BG:  docker-compose up -d          ← background
12. INSPECT: docker ps / docker logs / docker-compose ps / top
13. REBUILD: docker-compose build          ← FAST (cached layers)
14. CLEANUP: docker-compose down           ← stop + remove containers
15. EC2:     Stop instance (avoid t3.medium charges)
```

***

## 📦 Image Layer Caching — Build Speed

```
FIRST BUILD:
  Download deps → compile → assemble layers → SLOW (minutes)

SUBSEQUENT BUILDS (no changes):
  All layers cached → INSTANT

SUBSEQUENT BUILDS (small code change):
  Unchanged layers → cached (instant)
  Changed layer + all after it → rebuilt (fast)

MICROSERVICE PATTERN:
  Small changes → frequent builds → fast due to caching
  "Small, small changes multiple times" → fast iteration cycle
  
  Automatable via CI/CD pipeline
```

***

## 🔄 Foreground vs. Background

```
docker-compose up        (foreground)
  ├── See all logs live
  ├── Terminal locked
  └── Ctrl+C stops all containers

docker-compose up -d     (background/detached)
  ├── Terminal returns immediately
  ├── Containers run silently
  └── Inspect with: docker ps, docker logs, docker-compose ps/top
```

***

## 💰 Instance Sizing — Why t3.medium

```
RESOURCE         t2.micro    t3.medium
RAM              1 GB        4 GB        ← need for 6 containers + builds
CPU              1 vCPU      2 vCPU      ← need for parallel builds
Network          slower      faster      ← pulling images + deps
Disk (default)   8 GB        8 GB        ← OVERRIDE to 20 GB
Cost             free tier   charges     ← use < 1 hour, then STOP

STOP instance when done → no charges in stopped state
TERMINATE if completely done
```

***

## 🛡️ User Data Script — Three Steps

```
323.intDockerAndCompose.txt:
  1. Install Docker Engine (apt repo + docker-ce)
  2. Install Docker Compose (download binary from GitHub)
  3. Add ubuntu user to docker group

FALLBACK: If user data fails → SSH in → execute manually
```

***

## ✅ Validation Chain

```
Browser → http://<IP>:80
  │
  ├── Page loads?         → Nginx gateway + Angular client ✅
  ├── Register works?     → eMart API (Node.js) + MongoDB ✅
  ├── Login works?        → Authentication flow ✅
  └── Book Smart works?   → Web API (Java) + MySQL ✅

"All the services are working together"
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Build Once, Run Many (Image as Artifact)**
`docker-compose build` transforms source code into images (the artifact). `docker-compose up` deploys those artifacts as running containers. The artifact (image) is stable and reproducible — you can run it anywhere Docker exists. This decouples building from running, just as compiling a binary decouples development from deployment.

**Pattern 2: Layer Caching for Incremental Builds**
Docker's layer cache means rebuilds are proportional to the size of the change, not the size of the project. This makes the small-change/frequent-build cycle practical for microservices. The same caching principle appears in build tools (Maven incremental compile, Webpack hot reload, Gradle build cache) — avoid redoing work that hasn't changed.

**Pattern 3: Right-Size Infrastructure for the Task**
Use a larger instance (t3.medium) temporarily for build-heavy work, then stop it. Don't try to squeeze builds onto free-tier instances where they'll fail or take forever. The cost of a larger instance for one hour is negligible compared to the time wasted fighting resource constraints. Match infrastructure to workload, not to budget defaults.

**Pattern 4: Compose as Single-File Full-Stack Definition**
One docker-compose.yml file defines everything: which services exist, how to build custom ones, which pre-built images to pull, how services connect, port mappings, volumes, and environment variables. The entire multi-service application is captured in a single declarative file that anyone can clone and run. This is the container-era equivalent of "infrastructure as code" at the application level.

***

## 🎯 One-Line System Summary

> **A Docker Compose file defines both the build (Dockerfiles for Angular/Java/Node.js custom images) and run (port mappings, pre-built MongoDB/MySQL/Nginx images) configuration for a complete microservice stack; `docker-compose build` compiles source into images with layer caching for fast incremental rebuilds; `docker-compose up -d` pulls missing images, creates all containers, and starts the entire application accessible through the Nginx API gateway on port 80; all on a right-sized EC2 instance (t3.medium, 20GB) provisioned with Docker via user data.** [\[323-build-...ervice-app \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323-build-and-run-microservice-app.txt), [\[323.intDoc...AndCompose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/323.intDockerAndCompose.txt)
