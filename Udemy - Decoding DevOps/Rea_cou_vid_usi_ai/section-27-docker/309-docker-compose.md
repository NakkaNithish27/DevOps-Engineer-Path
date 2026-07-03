# 🎓 Deep Learning Material: Docker Compose — Multi-Container Orchestration Tool

**Source:** [309-docker-compose.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt?EntityRepresentationId=56d5f41a-251c-4bf9-9a10-53e235625cde) — Video lecture covering what Docker Compose is, how it relates to Docker Engine, why it exists for multi-container management, the docker-compose YAML file structure (services, build, image, ports, volumes, environment variables), installation on an EC2 instance, the official Getting Started exercise (Python Flask + Redis), imperative vs declarative benefits, and the relationship between Docker Compose and project containerization. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Docker Compose Is — And What It Is Not

Docker Compose is a **separate utility** from Docker Engine. When you install Docker Engine, you get two things: the Docker Engine (the daemon that runs containers) and the Docker CLI (the command-line tool to interact with the engine). Docker Compose is **not included** — it must be installed separately. It is a binary that you download and make executable. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

Docker Compose is a **tool to run multiple containers together**. It reads a YAML configuration file that describes all the containers (called "services"), their images, ports, volumes, environment variables, and relationships. Instead of running each container individually with `docker run` and its many flags, you write everything into a single file and execute one command: `docker-compose up`. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.2 The Problem Docker Compose Solves

Real-world applications are not single containers. The vProfile project, for example, has multiple components that need to communicate: an application server, a database, a cache, a message broker. In previous sections of the course, these ran as separate VMs, separate EC2 instances, or separate AWS managed services — all within the same network. When containerized, each component becomes a container, and these containers must **talk to each other**. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

Running multiple containers manually with `docker run` is error-prone. Each container needs port mappings (`-p`), environment variables (`-e`), volume mounts, network configuration, and naming. If you have six or seven containers, the chance of making a mistake — a wrong port, a typo in an environment variable, a missing volume — is very high. Docker Compose eliminates this by moving all configuration from imperative commands into a **declarative YAML file**. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.3 The Vagrant Analogy — A Powerful Mental Model

The instructor draws a direct comparison: **Docker Compose is to containers what Vagrant is to VMs**. Vagrant reads a `Vagrantfile` that declares multiple VMs with their configurations (box, memory, network, provisioning) and brings them all up with `vagrant up`. Docker Compose reads a `docker-compose.yml` that declares multiple containers with their configurations and brings them all up with `docker-compose up`. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

This analogy is operationally precise:

| Vagrant           | Docker Compose        |
| ----------------- | --------------------- |
| `Vagrantfile`     | `docker-compose.yml`  |
| `vagrant up`      | `docker-compose up`   |
| `vagrant destroy` | `docker-compose down` |
| VMs               | Containers            |
| VirtualBox/VMware | Docker Engine         |

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.4 Imperative vs Declarative — The Core Benefit

Running `docker run` commands is **imperative** — you tell Docker exactly what to do, step by step, on the command line. Writing a Docker Compose file is **declarative** — you describe the desired state (what containers should exist, with what configuration), and Docker Compose figures out how to achieve it. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

The declarative approach provides three key benefits:

**1. Reduced human error.** All configuration is in a file, not typed on the command line. You write it once, review it, and reuse it. No more mistyped port numbers or forgotten flags. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**2. Version control.** The `docker-compose.yml` file is part of your repository. Every change is tracked. A developer can clone the repo and run the entire application stack with one command. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**3. Infrastructure as Code.** The compose file is a code artifact that describes your container infrastructure. It is shareable, reviewable, and reproducible. Any developer can use it to run containers locally or in any environment. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.5 The Docker Compose YAML File Structure

The compose file has a defined structure. The video demonstrates two examples — a simple two-service example from the Docker documentation and the Getting Started exercise.

### Top-Level Keys

**`version`** — Declares the compose file format version. (Mentioned in the video as present in examples.)

**`services`** — The most important section. Each entry under `services` defines a **container**. The key name (e.g., `web`, `redis`) becomes the container's name and also its **hostname** on the compose network — other containers can reach it by this name. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**`volumes`** — Top-level volume declarations. Named volumes are created here and referenced by services. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

### Service-Level Options

**`image`** — Specifies a pre-built image to use. `image: redis` is equivalent to `docker run redis`. The image is pulled from Docker Hub (or a configured registry). [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**`build`** — Instead of using a pre-built image, build an image from a Dockerfile. `build: .` means "look for a Dockerfile in the current directory, build it, and use the resulting image." You use `image` when a ready-made image exists (like Redis), and `build` when you need a custom image (like your application). [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**`ports`** — Port mapping. `"8000:5000"` maps host port 8000 to container port 5000. Same as `docker run -p 8000:5000`. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**`volumes`** — Volume mounts, specified as a list. Two types are demonstrated:

* **Bind mount:** `./:/code` maps the current host directory to `/code` in the container. Changes on the host are reflected in the container immediately (useful for development — edit code locally, see changes in the container).
* **Named volume:** A volume created in the top-level `volumes` section, referenced by name. This is the same as creating a volume with `docker volume create` and mapping it with `docker run -v`. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**`environment`** — Environment variables set inside the container. The Getting Started exercise sets Flask-specific variables. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

🔍 **Deep Dive**
The compose file's `build: .` instruction expects a Dockerfile in the same directory as the compose file. When `docker-compose up` runs, it first builds the image from the Dockerfile (if not already built), then runs the container from that image. This means the compose file and the Dockerfile are companions — the Dockerfile defines **how to build** the image, and the compose file defines **how to run** the container (ports, volumes, environment, relationships to other containers). [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.6 The Automatic Network

When `docker-compose up` runs, the first thing it does is **create a network**. The instructor observes this in the output: "first it creates a network and then it starts building your container." All services defined in the compose file are placed on this network automatically. This means they can communicate with each other using their service names as hostnames — the `web` container can reach the `redis` container by simply connecting to `redis:6379`. No manual network creation or `--link` flags are needed. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.7 The Dockerfile in the Getting Started Exercise

The exercise uses a Python Flask application. The Dockerfile is walked through briefly:

```dockerfile
FROM python:3.10-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

The base image is `python:3.10-alpine` (Alpine = very lightweight Linux). The work directory is `/code`. Two Flask environment variables are set. An `apk` command installs build dependencies (Alpine uses `apk`, not `apt`). The `requirements.txt` is copied first and dependencies installed (`pip install`) — this is a Docker layer caching optimization (dependencies change less frequently than application code). Then the entire current directory is copied to `/code`. Finally, `flask run` starts the application. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

The instructor notes: "We are not going to build this one. We are going to do everything through docker compose file." The Dockerfile exists, but `docker build` is never called directly — Docker Compose handles the build automatically when it encounters `build: .` in the compose file. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.8 Foreground vs Background Execution

`docker-compose up` runs in the **foreground** by default — all container logs stream to your terminal, and the process blocks your shell. To stop, you press `Ctrl+C`, which stops the containers. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

`docker-compose up -d` runs in **detached mode** (background). The containers start and you get your shell back immediately. The `-d` flag works the same as `docker run -d`. The instructor recommends background mode: "That's why you should not run it in the foreground." [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.9 `docker-compose down` — Stop and Remove

`docker-compose down` does two things: it **stops** all containers and then **removes** them. After running `down`, the containers no longer exist — they are not just stopped, they are deleted. This is important to understand: `down` is destructive. If you just want to stop without removing, you would use `docker-compose stop`. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

`Ctrl+C` (when running in the foreground) only **stops** the containers — it does not remove them. `docker-compose down` does both. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.10 Docker Compose Management Commands

The video demonstrates several management commands:

**`docker-compose ps`** — Lists the containers managed by this compose file. Similar to `docker ps` but scoped to the compose project. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**`docker-compose top`** — Shows the running processes inside each container, including PID, PPID, and the command being run. More detailed than `docker-compose ps`. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## 1.11 Containerizing = Dockerfile + Docker Compose

The instructor closes with a clear definition: "Whenever you hear the word containerizing or dockerizing, that means you have to write Dockerfile and you have to write docker compose file." [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

* **Dockerfile** = how to **build** the image (base image, dependencies, application code, startup command).
* **Docker Compose file** = how to **run** the containers together (which images/builds, ports, volumes, environment, networks).

The Dockerfile is "mandatory most of the time." Docker Compose is the standard way to orchestrate multi-container applications, though the instructor notes "there are options or alternative to Docker Compose as well." The next lecture applies both to the vProfile project. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are installing Docker Compose on an EC2 instance that already has Docker Engine, then following the official Docker Getting Started exercise to build and run a two-container application (Python Flask web app + Redis cache) using a docker-compose file. The final outcome: accessing the EC2 instance on port 8000 in a browser shows a "Hello World" page with a visit counter powered by Redis. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 1: Install Docker Compose

SSH into your EC2 instance where Docker Engine is already running.

**1a. Download the Docker Compose binary:**

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.x.x/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

(Copy the exact `curl` command from the Docker Compose installation documentation — **Install Compose** page, Linux section.) [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

| Part                               | Meaning                                       |
| ---------------------------------- | --------------------------------------------- |
| `curl -L`                          | Download, following redirects                 |
| URL                                | The Docker Compose binary release from GitHub |
| `-o /usr/local/bin/docker-compose` | Save to this location (on the system PATH)    |

**1b. Make it executable:**

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**1c. Verify installation:**

```bash
docker-compose --version
```

Should display the Docker Compose version. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 2: Create the Project Directory

```bash
mkdir composetest
cd composetest
```

This is the project directory. All files (app code, Dockerfile, compose file) go here. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 3: Create the Python Application File

```bash
vim app.py
```

Paste the content from the Getting Started guide. This is a simple Flask application that connects to Redis, increments a counter on each visit, and returns "Hello World! I have been seen X times." [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

The instructor emphasizes: "You really don't need to understand this" — the application is just a vehicle for learning Docker Compose. Save and quit. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 4: Create the Requirements File

```bash
vim requirements.txt
```

Content:

```
flask
redis
```

These are the Python dependencies. During the Docker build, `pip install -r requirements.txt` will install Flask and the Redis client library. Save and quit. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 5: Create the Dockerfile

```bash
vim Dockerfile
```

Paste the content from the Getting Started guide:

```dockerfile
FROM python:3.10-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

Save and quit. **Do not build this manually** — Docker Compose will handle the build.

***

## Step 6: Create the Docker Compose File

```bash
vim docker-compose.yml
```

Initial content (simple version):

```yaml
version: "3"
services:
  web:
    build: .
    ports:
      - "8000:5000"
  redis:
    image: redis
```

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

| Key                  | Meaning                                          |
| -------------------- | ------------------------------------------------ |
| `services:`          | Container definitions                            |
| `web:`               | First service — the Flask app                    |
| `build: .`           | Build image from Dockerfile in current directory |
| `ports: "8000:5000"` | Map host port 8000 to container port 5000        |
| `redis:`             | Second service — the Redis cache                 |
| `image: redis`       | Use the official Redis image from Docker Hub     |

⚠️ **Indentation matters.** The instructor reminds: "You must have learned all that in Ansible YAML file." All keys at the same level must be at the same indentation. Save and quit. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 7: Run Docker Compose (Foreground)

```bash
docker-compose up
```

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**What happens internally:**

1. Docker Compose reads `docker-compose.yml`.
2. Creates a **network** for the project (visible in the output).
3. Builds the `web` image from the Dockerfile (downloads base image, installs dependencies, copies code).
4. Pulls the `redis` image from Docker Hub.
5. Starts both containers on the created network.
6. Streams all logs to your terminal (foreground mode).

**Expected:** Build output followed by Flask startup messages and Redis startup messages, interleaved.

***

## Step 8: Configure Security Group and Test

**8a. Open port 8000** on your EC2 instance's security group. Add an inbound rule: Custom TCP, port 8000, source = your IP. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**8b. Access in browser:**

```
http://<EC2-public-IP>:8000
```

**Expected:** "Hello World! I have been seen 1 times." Refresh → counter increments. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 9: Stop the Foreground Process

Press `Ctrl+C` in the terminal. This **stops** the containers but does not remove them.

Then run:

```bash
docker-compose down
```

This **stops AND removes** the containers. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**Verify:**

```bash
docker images
```

The built image and the Redis image are still present (images persist after `down`; only containers are removed). [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 10: Add Volumes and Environment Variables

Edit the compose file to add volumes and environment variables (from the Getting Started guide's next step):

```bash
vim docker-compose.yml
```

Updated content:

```yaml
version: "3"
services:
  web:
    build: .
    ports:
      - "8000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_DEBUG: "true"
  redis:
    image: redis
```

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

| New Addition                       | Meaning                                                                       |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| `volumes: - .:/code`               | Bind mount: current host directory → `/code` in container (live code changes) |
| `environment: FLASK_DEBUG: "true"` | Enable Flask debug mode (auto-reload on code changes)                         |

Save and quit. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 11: Run in Detached Mode

```bash
docker-compose up -d
```

 [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

| Flag | Meaning                                                     |
| ---- | ----------------------------------------------------------- |
| `-d` | Detached mode — run in background, return shell immediately |

**Verify running containers:**

```bash
docker-compose ps
```

Shows the containers managed by this compose file with their state and port mappings. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**View process details:**

```bash
docker-compose top
```

Shows PID, PPID, and command for each service's processes. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 12: Test Live Code Updates

Edit `app.py` — change the text string. Because of the bind mount (`volumes: .:/code`) and Flask debug mode, the change is reflected in the browser **without rebuilding or restarting** the container. Just refresh the browser. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

***

## Step 13: Clean Up

```bash
docker-compose down
```

Stops and removes all containers. The images remain on disk. [\[309-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/309-docker-compose.txt)

**Connection to larger flow:** The next lecture uses Docker Compose to containerize the entire vProfile project — writing Dockerfiles for each service and a compose file that runs them all together.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
Docker Compose = multi-container orchestration via declarative YAML
Docker Engine  = runs individual containers
Docker CLI     = imperative commands (docker run, docker build)
Docker Compose = declarative file (docker-compose.yml) + one command

Vagrant : VMs  =  Docker Compose : Containers
```

***

## Compose File Structure

```yaml
version: "3"

services:                    # ← containers
  <service-name>:
    image: <image>           # ← use pre-built image
    # OR
    build: <path>            # ← build from Dockerfile at path
    ports:
      - "host:container"     # ← port mapping
    volumes:
      - ./host:/container    # ← bind mount
      - volname:/container   # ← named volume
    environment:
      KEY: "value"           # ← env vars

volumes:                     # ← named volume declarations
  volname:
```

***

## `image` vs `build`

```
image: redis         → pull ready-made image from registry (like docker run redis)
build: .             → build image from Dockerfile in current directory
                       Dockerfile MUST exist at specified path

Use image:  when official/pre-built image exists (Redis, MySQL, Nginx)
Use build:  when you need custom image (your application)
```

***

## Command Reference

```bash
# Lifecycle
docker-compose up           # start all (foreground)
docker-compose up -d         # start all (background/detached)
docker-compose down          # stop + REMOVE containers
docker-compose stop          # stop only (containers preserved)
Ctrl+C                       # stop foreground (containers preserved)

# Inspection
docker-compose ps            # list compose containers
docker-compose top           # processes in each container (PID, PPID, CMD)

# Installation
curl -L <url> -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

***

## What `docker-compose up` Does Internally

```
1. Read docker-compose.yml
2. Create project NETWORK (auto)
3. Build images (for services with build:)
4. Pull images (for services with image:)
5. Start all containers on the shared network
6. Services reachable by name as hostname
```

***

## Volume Types in Compose

```
Bind mount:    .:/code
               host directory → container directory
               Live sync (edit on host → reflected in container)

Named volume:  volname:/data
               Managed by Docker
               Declared in top-level volumes: section
               Persists after container removal
```

***

## Foreground vs Detached

```
docker-compose up        → foreground (logs stream, shell blocked)
docker-compose up -d     → detached (background, shell free)

Foreground: useful for debugging (see all logs live)
Detached: recommended for normal operation
```

***

## `down` vs `stop` vs `Ctrl+C`

```
Ctrl+C           → stops containers      (containers still exist)
docker-compose stop → stops containers   (containers still exist)
docker-compose down → stops + REMOVES    (containers deleted, images remain)
```

***

## Getting Started Exercise File Structure

```
composetest/
├── app.py                  ← Python Flask app (web counter + Redis)
├── requirements.txt        ← flask, redis (Python dependencies)
├── Dockerfile              ← build instructions for web container
└── docker-compose.yml      ← declares web + redis services
```

***

## Dockerfile Layers (Flask App)

```dockerfile
FROM python:3.10-alpine     ← base image (lightweight)
WORKDIR /code               ← working directory in container
ENV FLASK_APP=app.py        ← environment variables
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add ...             ← install OS-level build dependencies
COPY requirements.txt .     ← copy deps file first (layer cache optimization)
RUN pip install -r ...       ← install Python deps
EXPOSE 5000                 ← document the port
COPY . .                    ← copy application code
CMD ["flask", "run"]        ← startup command
```

***

## Imperative vs Declarative

```
IMPERATIVE (docker run):
  docker run -d -p 8000:5000 -v .:/code -e FLASK_DEBUG=true myapp
  docker run -d redis
  → error-prone, not tracked, not reproducible

DECLARATIVE (docker-compose.yml):
  All config in file → docker-compose up
  → version controlled, reproducible, shareable, IaC
```

***

## Containerizing = Two Artifacts

```
Dockerfile          → HOW to BUILD the image
docker-compose.yml  → HOW to RUN containers together

"Whenever you hear containerizing or dockerizing,
 that means Dockerfile + Docker Compose file"
```

***

## Key Engineering Patterns

| Pattern                         | Manifestation                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------ |
| **Declarative over imperative** | YAML file replaces CLI commands — reduces errors, enables version control      |
| **Automatic networking**        | Compose creates a shared network — services reach each other by name           |
| **Build + Run separation**      | Dockerfile = build concern, Compose = run concern — clean separation           |
| **Bind mount for dev workflow** | Mount source code into container → edit locally, see changes live              |
| **Companion file pattern**      | Dockerfile + docker-compose.yml always coexist in project root                 |
| **Vagrant analogy**             | Same mental model: config file → `up` → infrastructure runs → `down` → cleanup |

***

## Project Continuity

```
BEFORE: Docker Engine, Docker CLI, Dockerfile basics, container operations
THIS:   Docker Compose — multi-container orchestration, YAML file, Getting Started exercise
NEXT:   Containerize vProfile project (write Dockerfiles + compose file for all services)
```

***

This completes the full reconstruction. **Theory** explains what Docker Compose is, why it exists, and how the YAML file maps to container operations. **Practical** walks through every file creation, every command, and the verification flow. The **Compression Map** gives you the file structure, command reference, and the `image` vs `build` distinction for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
