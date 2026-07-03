# 🎓 Deep Learning Material: Docker Compose Build and Run — Building Images, Running Multi-Container Applications, Pushing to Docker Hub, and Cleanup

**Source:** Video lecture on Docker Compose build and run workflow (from [320-build-and-run.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt?EntityRepresentationId=1f740e96-7319-4ef9-ba4e-44afae10ba0a) caption file) [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Video Context:** This is the execution lecture where all prior Docker work converges. The Dockerfiles (app, db, web) and the Docker Compose file were written in previous lectures. Now the instructor builds all images with a single command, runs the entire multi-container vProfile application stack (Nginx, Tomcat, MySQL, Memcache, RabbitMQ), verifies end-to-end functionality through the browser, fixes container naming, pushes images to Docker Hub for reuse in Kubernetes lectures, and performs complete cleanup. The lecture demonstrates the full lifecycle: **build → run → verify → publish → clean**. The most important conceptual takeaway is the "everything as code" principle — with Dockerfiles, Docker Compose, and Vagrantfile in version control, the entire infrastructure can be destroyed and recreated at will.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Docker Compose Build: One Command to Build All Images

In previous lectures, three Dockerfiles were created (for the app, database, and web/Nginx containers) and a Docker Compose file was written that references these Dockerfiles and defines how to run the containers. The Docker Compose file contains both the **build instructions** (where each Dockerfile is located) and the **run instructions** (port mappings, volumes, networks, container names, dependencies). [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

`docker compose build` reads the Compose file, finds every service that has a `build` directive (a path to a Dockerfile), and runs `docker build` for each one. The instructor explains: *"This command is going to read your Docker Compose file, find all the images that requires the build, and going to run the Docker build command to build the images."* [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

Not all services in the Compose file require building. The Memcache and RabbitMQ services use **official images** from Docker Hub — they have no Dockerfile and don't need building. They're pulled during `docker compose up`, not during `docker compose build`. The instructor clarifies: *"It will also pull two images for memcache and RabbitMQ. Now memcache and RabbitMQ image. Those are official images that we are taking. We're not building it."* [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

When no tag is specified in the Compose file, Docker assigns the **`latest`** tag by default. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## 1.2 — Docker Compose Up: Running the Full Stack

`docker compose up -d` starts all containers defined in the Compose file. The `-d` flag runs them in **detached mode** (background). Before starting containers, Compose checks whether the required images exist locally. If they don't, it either builds them (if a `build` directive exists) or pulls them from Docker Hub (if only an `image` directive exists). Since we already ran `docker compose build`, the three custom images exist; Compose only needs to pull the two official images (Memcache, RabbitMQ). [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

When Compose runs `up`, it also creates the **network** and **volumes** defined in the Compose file. The instructor observes: *"When it created a network, it created these two volumes that we mentioned."* This is automatic — Compose manages the full infrastructure lifecycle. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## 1.3 — Container Naming: The `container_name` Directive

By default, Docker Compose generates container names using the format `<project>-<service>-<number>`. But the vProfile application's `application.properties` file hardcodes specific hostnames for backend services (`vprodb`, `vprocache01`, `vpromq01`). The container names **must match** these hostnames because Docker's internal DNS resolves container names to IP addresses within the Compose network. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

The instructor notices the Memcache and RabbitMQ containers have incorrect names and fixes this by adding `container_name` directives to the Compose file: [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

```yaml
container_name: vpromq01      # for RabbitMQ
container_name: vprocache01   # for Memcache
```

The `vprodb` and `vproapp` containers already had `container_name` set from the original Compose file. After fixing the names, the instructor runs `docker compose down` (stops and removes all containers) then `docker compose up -d` again. This time all container names match what the application expects. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

> 🔍 **Deep Dive**
>
> This reveals a critical relationship: the application's configuration file (`application.properties`) contains hostnames like `vprodb`, `vprocache01`, `vpromq01`. Docker Compose creates a network where each container's name is registered as a DNS entry. When the Tomcat application tries to connect to `vprodb`, Docker's internal DNS resolves it to the MySQL container's IP address. If the container name doesn't match, DNS resolution fails and the application can't connect to its backends. This is why `container_name` is not cosmetic — it's a **service discovery mechanism**. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## 1.4 — Port Mapping and Request Routing: The Full Traffic Path

The instructor explains the complete request flow when accessing the application from a browser: [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

1. **Browser** accesses `http://192.168.56.16:80` (the Vagrant VM's IP on port 80)
2. **Host port 80** is mapped to **container port 80** (visible in `docker ps` output)
3. The request reaches the **Nginx container** (vproweb) on port 80
4. Nginx has a configuration that **proxies the request** to the **Tomcat container** (vproapp)
5. Tomcat processes the request using its `application.properties` file, which contains connection details for **vprodb**, **vprocache01**, and **vpromq01**
6. Tomcat connects to these backend containers via Docker's internal DNS

The instructor emphasizes the port mapping visibility: *"when you run Docker PS command, you can see the container port of Nginx is port 80 and the host port is 80. So when you access the host on port 80, it is going to route the request to container, the Nginx container on port 80."* [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## 1.5 — End-to-End Verification: Proving All Services Work

The instructor verifies each backend service through the application's UI: [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

* **MySQL (vprodb):** Login with `admin_vp` / `admin_vp` succeeds → *"This information is stored in the database. If you're able to log in, then it is able to also connect to the DB container."*
* **RabbitMQ (vpromq01):** Click on "RabbitMQ" in the app → shows "RabbitMQ initiated"
* **Memcache (vprocache01):** Click on "All users" → select a user → first click shows "Data is from DB and data is inserted in cache" → second click shows "data is coming from the cache"

This verification pattern tests the entire stack through the application's own functionality rather than individual container checks. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## 1.6 — Pushing Images to Docker Hub

After verifying the application works, the instructor pushes the three custom-built images to Docker Hub for future use (specifically in Kubernetes lectures). The process: [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

1. **Image naming convention:** Images must be prefixed with your Docker Hub account name (e.g., `vprocontainers/vprofileapp`). The instructor notes: *"first should be your account name and then the image name."*
2. **Login:** `docker login` → browser-based authentication with a one-time code
3. **Push:** `docker push <image-name>` for each of the three images, one by one [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## 1.7 — The "Everything as Code" Principle

The lecture's closing insight is the most architecturally significant. After cleanup, the instructor states: *"as long as we have the Docker Compose file and all the Docker files, we can anytime build and run these containers. And if you're done with this, you can really exit and stop this VM or even destroy this VM because we have everything in the code. We have the Vagrant file, we can bring up the VM, then we can run the Docker Compose file to build the images and run the containers. So everything we have as a code."* [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

The complete reproducibility chain: **Vagrantfile** (creates the VM with Docker installed) → **Dockerfiles** (build application images) → **Docker Compose file** (orchestrates multi-container deployment). All are text files in version control. The entire infrastructure — from VM to running application — can be destroyed and recreated from these files alone. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are building all Docker images, running the complete vProfile multi-container application (5 containers: Nginx, Tomcat, MySQL, Memcache, RabbitMQ), verifying end-to-end functionality, pushing images to Docker Hub, and performing cleanup. The final outcome: a verified, working multi-container application with images published to a registry for reuse in Kubernetes.

***

## Step 1: Start the Vagrant VM

Navigate to the folder where the Vagrant VM was created (with Docker Engine installed):

```bash
cd f/containerization/vprofile-project/vagrant/Windows
vagrant status
```

If the VM is powered off:

```bash
vagrant up
```

If already running:

```bash
vagrant reload
```

**Log in:**

```bash
vagrant ssh
```

**Switch to root (optional — vagrant user is in the Docker group):**

```bash
sudo -i
```

 [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## Step 2: Place Docker Files in the Vagrant Shared Directory

The `/vagrant` directory inside the VM is synced with the host folder where the Vagrantfile lives. All Docker files must be accessible here. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**On the host machine (VS Code / file manager):**

1. Copy the `Docker-files/` folder into the Vagrant project folder
2. Copy the `docker-compose.yml` file into the same location [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Inside the VM:**

```bash
cd /vagrant
ls
```

**Expected:** You should see the Docker Compose file and Docker-files directory. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## Step 3: Build All Images

```bash
docker compose build
```

* `docker compose` — the Compose CLI
* `build` — reads the Compose file, finds all services with `build` directives, runs `docker build` for each [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**This takes significant time** (Maven dependencies download, package installations, etc.). The instructor pauses recording and resumes after completion. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Verify the built images:**

```bash
docker images
```

**Expected output:** Three images — app, db, web — all tagged as `latest` (default when no tag specified). [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## Step 4: Run All Containers

```bash
docker compose up -d
```

* `up` — creates and starts all containers defined in the Compose file
* `-d` — detached mode (runs in background) [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**What happens internally:** [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

1. Checks that the three built images exist locally → found
2. **Pulls** Memcache and RabbitMQ official images from Docker Hub (not built locally)
3. Creates the Docker network defined in the Compose file
4. Creates the two volumes defined in the Compose file
5. Starts all five containers

***

## Step 5: Fix Container Names

```bash
docker ps
```

**Check the container names.** The instructor notices Memcache and RabbitMQ containers don't have the correct names (`vprocache01`, `vpromq01`). [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Edit the Docker Compose file:**

```bash
vim docker-compose.yml
```

Add `container_name` directives to the Memcache and RabbitMQ services: [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

```yaml
# Under RabbitMQ service:
container_name: vpromq01

# Under Memcache service:
container_name: vprocache01
```

Save and quit. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Recreate containers with correct names:**

```bash
docker compose down
docker compose up -d
```

* `down` — stops AND removes all containers (but keeps images and volumes)
* `up -d` — recreates containers with updated configuration [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Verify:**

```bash
docker ps
```

All five containers should show correct names: `vprodb`, `vproapp`, `vproweb`, `vprocache01`, `vpromq01`. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## Step 6: Verify the Application

**Get the VM's IP address:**

```bash
ip addr show
```

Find the IP on `enp0s8` interface (the host-only network) — e.g., `192.168.56.16`. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Access in browser:**

```
http://192.168.56.16:80
```

(Port 80 is default for HTTP; can be omitted.) [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Verification checklist:** [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

| Test                    | Action                        | Expected Result                         | Service Verified       |
| ----------------------- | ----------------------------- | --------------------------------------- | ---------------------- |
| Web page loads          | Navigate to URL               | vProfile login page appears             | Nginx → Tomcat         |
| Login works             | Enter `admin_vp` / `admin_vp` | Login succeeds                          | MySQL (vprodb)         |
| RabbitMQ                | Click "RabbitMQ" in app       | "RabbitMQ initiated"                    | RabbitMQ (vpromq01)    |
| Memcache (first click)  | All users → select user       | "Data is from DB and inserted in cache" | MySQL + Memcache       |
| Memcache (second click) | Click same user again         | "Data is coming from cache"             | Memcache (vprocache01) |

 [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## Step 7: Push Images to Docker Hub

**Log in to Docker Hub:**

```bash
docker login
```

Follow the browser-based authentication: copy the URL → open in browser → enter the one-time code shown in terminal → confirm. Terminal shows "login succeeded." [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Push each image:**

```bash
docker push <account-name>/vprofileapp
docker push <account-name>/vprofiledb
docker push <account-name>/vprofileweb
```

Replace `<account-name>` with your Docker Hub username. Push all three images one by one. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Why:** These images will be reused in Kubernetes lectures. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

## Step 8: Cleanup

**Stop and remove all containers:**

```bash
cd /vagrant
docker compose down
```

 [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Remove volumes:**

```bash
docker volume ls
docker volume rm <volume-name-1> <volume-name-2>
```

Or remove all unused volumes:

```bash
docker volume prune
```

 [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Nuclear cleanup (remove everything — containers, images, cache):**

```bash
docker system prune -a
```

Confirm with `yes`. This removes all stopped containers, all images, all build cache, and all unused networks. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

**Stop the VM:**

```bash
exit       # exit from root
exit       # exit from vagrant ssh
vagrant halt
```

 [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Complete Lifecycle (This Lecture)

```
BUILD → RUN → VERIFY → FIX → PUBLISH → CLEAN

docker compose build     → builds 3 custom images
docker compose up -d     → runs 5 containers (3 built + 2 pulled)
browser verification     → test all 5 services
fix container_name       → docker compose down + up -d
docker login + push      → publish to Docker Hub
docker compose down      → stop + remove containers
docker system prune -a   → remove everything
vagrant halt             → stop VM
```

***

## 🔷 Request Flow (Browser → Backend)

```
Browser: http://192.168.56.16:80
  │
  ▼
HOST PORT 80 ──mapping──► CONTAINER PORT 80
  │
  ▼
NGINX (vproweb) ──proxy──► TOMCAT (vproapp:8080)
  │
  ├──► MySQL (vprodb)        ← login credentials
  ├──► Memcache (vprocache01) ← user data caching
  └──► RabbitMQ (vpromq01)    ← message queue

DNS RESOLUTION: container_name = hostname in Docker network
  vproapp resolves to Tomcat container IP
  vprodb resolves to MySQL container IP
  etc.
```

***

## 🔷 Five Containers

```
CONTAINER        IMAGE SOURCE       PORT    ROLE
──────────       ────────────       ────    ────────────────
vproweb          Custom (built)     80      Nginx reverse proxy
vproapp          Custom (built)     8080    Tomcat application
vprodb           Custom (built)     3306    MySQL database
vprocache01      Official (pulled)  11211   Memcache caching
vpromq01         Official (pulled)  5672    RabbitMQ messaging
```

***

## 🔷 Docker Compose Commands

```bash
docker compose build      # build images from Dockerfiles
docker compose up -d      # create + start all containers (detached)
docker compose down       # stop + remove containers (keeps images/volumes)
docker compose up -d      # recreate after config changes

# Images exist? → up skips build
# Images missing? → up triggers build automatically
```

***

## 🔷 Container Naming = Service Discovery

```
application.properties contains:
  db.host = vprodb
  cache.host = vprocache01
  mq.host = vpromq01

Docker Compose network DNS:
  container_name: vprodb     → resolves to MySQL IP
  container_name: vprocache01 → resolves to Memcache IP
  container_name: vpromq01   → resolves to RabbitMQ IP

WRONG container name = DNS resolution fails = app can't connect
FIX: add container_name directive in docker-compose.yml
```

***

## 🔷 Verification Matrix

```
TEST               ACTION                    SUCCESS = PROVES
────               ──────                    ─────────────────
Page loads         Navigate to URL           Nginx → Tomcat working
Login              admin_vp / admin_vp       MySQL connected
RabbitMQ           Click "RabbitMQ"          MQ service initiated
Cache miss         Click user (1st time)     DB → read, Cache → write
Cache hit          Click user (2nd time)     Cache → read (no DB)
```

***

## 🔷 Docker Hub Push Flow

```bash
docker login                              # browser auth + one-time code
docker push <account>/vprofileapp         # push app image
docker push <account>/vprofiledb          # push db image
docker push <account>/vprofileweb         # push web image

IMAGE NAMING: <dockerhub-account>/<image-name>:<tag>
  Account name MUST prefix the image name for push to work
```

***

## 🔷 Cleanup Commands (Escalating)

```bash
docker compose down              # containers only (stop + remove)
docker volume rm <name>          # specific volumes
docker volume prune              # all unused volumes
docker system prune -a           # EVERYTHING (containers, images, cache, networks)
vagrant halt                     # stop VM
vagrant destroy                  # delete VM entirely
```

***

## 🔷 File Placement (Vagrant Shared Directory)

```
HOST (Windows/Mac):                    VM (/vagrant):
  vagrant-folder/                        /vagrant/
    ├── Vagrantfile                        ├── Vagrantfile
    ├── docker-compose.yml                 ├── docker-compose.yml
    └── Docker-files/                      └── Docker-files/
          ├── app/Dockerfile                     ├── app/Dockerfile
          ├── db/Dockerfile                      ├── db/Dockerfile
          └── web/Dockerfile                     └── web/Dockerfile

HOST folder auto-syncs to /vagrant in VM
Place all Docker files in HOST folder → accessible inside VM
```

***

## 🔷 Built vs. Pulled Images

```
BUILT (docker compose build):
  ├── app image  → from Dockerfile (multi-stage, Java build)
  ├── db image   → from Dockerfile (MySQL + schema)
  └── web image  → from Dockerfile (Nginx + config)

PULLED (docker compose up):
  ├── memcache   → official image from Docker Hub
  └── rabbitmq   → official image from Docker Hub

build = custom images with your code/config
pull = official images used as-is
```

***

## 🔷 The "Everything as Code" Principle

```
VAGRANTFILE        → creates VM with Docker Engine
DOCKERFILES (3)    → build application images
DOCKER-COMPOSE.YML → orchestrates multi-container deployment

ALL ARE TEXT FILES IN VERSION CONTROL

CONSEQUENCE:
  Destroy everything → recreate from files alone
  vagrant up → docker compose build → docker compose up -d
  = complete running application from scratch

"We have everything in the code."
```

***

## 🔷 Reusable Engineering Pattern: Declarative Infrastructure Lifecycle

```
PATTERN: Declare → Build → Run → Verify → Publish → Destroy → Recreate

DECLARE:
  Vagrantfile (VM)
  Dockerfiles (images)
  docker-compose.yml (orchestration)
  
  All declarative: describe WHAT, not HOW

BUILD:     docker compose build (images from Dockerfiles)
RUN:       docker compose up -d (containers from images)
VERIFY:    browser + application-level tests
PUBLISH:   docker push (images to registry)
DESTROY:   docker compose down + docker system prune -a + vagrant halt
RECREATE:  vagrant up + docker compose build + docker compose up -d

NOTHING IS PRECIOUS — everything is reproducible from code.

This pattern applies to:
  Docker Compose (this lecture)
  Kubernetes (manifests + Helm charts)
  Terraform (infrastructure as code)
  CI/CD pipelines (pipeline as code)
  
The principle: if you can't destroy and recreate it from files,
               you don't truly have infrastructure as code.
```

This is the lecture's culminating insight: the ability to confidently run `docker system prune -a` and `vagrant destroy` without fear — because the code defines the infrastructure, not the running state. [\[320-build-and-run \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/320-build-and-run.txt)
