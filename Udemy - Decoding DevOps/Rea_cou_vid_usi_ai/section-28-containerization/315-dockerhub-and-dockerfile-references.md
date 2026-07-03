# Docker Hub Repositories & Dockerfile Reference — Preparing for Custom Image Builds

**Source:** Video caption file — *"Docker Hub and Dockerfile References"* (from a Docker / DevOps course) [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Docker Hub: The Image Registry and Repository Model

Docker Hub is the **central registry** where Docker images are stored, shared, and distributed. Before you can push a custom-built image, you need a **repository** on Docker Hub to host it — just like you need a GitHub repository before you can push code. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The organizational structure on Docker Hub works at two levels:

**Account / Organization name** — This is the namespace prefix for all your images. When you look at your Docker Hub profile, the name you see at the top is your **account name** — this becomes the first part of every image reference you push. In real projects, you typically create an **organization** instead of using a personal account. The organization name then replaces the account name as the namespace. The video clarifies: "When you have organization, then you can create the organization with your name. That will be the account name." [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

**Repository** — Each repository represents **one image**. The repository name becomes the second part of the image reference. So the full image path is `account-name/repository-name` (e.g., `myaccount/vprofileapp`). Each repository can hold multiple versions of the same image via tags (`:latest`, `:v1`, `:v2`). [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The video creates three repositories for the vProfile project — one per service that will be containerized:

* `vprofileapp` — the application image (Tomcat-based)
* `vprofiledb` — the database image (MySQL-based)
* `vprofileweb` — the web server image (NGINX-based) [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### Public vs. Private Repositories

Repositories can be **public** (anyone can pull the image) or **private** (only authorized users can pull). The video makes a practical note: "Private is not free, one is free. But then we need three images." Since the course needs three repositories and only one private repository is free on Docker Hub's free tier, all three are kept public. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

In real projects, images are almost always **private**: "When you're working in projects, these images will be private mostly." Production images contain your application code, configuration, and potentially sensitive data — they should never be publicly accessible. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## 1.2 — The Docker Build and Push Workflow

The overall workflow for custom images follows a clear sequence that the video outlines: [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

1. **Write a Dockerfile** — a file containing a series of instructions that define how to build the image.
2. **Build the image** — run `docker build -t account-name/image-name .` to create the image locally.
3. **Push the image** — send the locally built image to Docker Hub so it can be pulled and used anywhere.

The `-t` flag in the build command stands for **tag** — it assigns a name to the built image. The name format is `account-name/repository-name`, matching the Docker Hub repository you created. Without this tag, the image would only have a random ID and couldn't be pushed to a specific repository. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## 1.3 — What Is a Dockerfile?

A Dockerfile is a **text file containing a series of instructions** that tell Docker how to build an image, step by step. Each instruction in the Dockerfile creates a layer in the resulting image. The file must be named exactly `Dockerfile` with a capital `D` — the video explicitly notes: "Dockerfile, D, capital there." [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The Dockerfile is not a script that runs on your machine — it's a **build specification** that Docker's build engine processes. Each instruction is executed in order, and each one modifies the image being constructed. The result is a complete, self-contained image that can be run as a container anywhere Docker is installed. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## 1.4 — Dockerfile Instructions: The Building Blocks

The video walks through the key Dockerfile instructions from Docker Hub's reference documentation. Each instruction serves a specific purpose in the image construction process. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### `FROM` — The Base Image

Every Dockerfile **must** start with a `FROM` instruction. It specifies the **base image** — the starting point on top of which your customizations are built. You don't build an image from scratch; you build on top of an existing image that already contains an operating system and potentially some software. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The video connects this to the vProfile project: "We already have figured out our base images — Tomcat, MySQL, and Nginx. We just need to figure out the right tag." Each vProfile service starts from a different base image, and the tag (version) determines which specific version of that base image you use. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### `RUN` — Execute Commands During Build

`RUN` executes a command **during the image build process**. This is how you install software, configure settings, create directories, or perform any operation that needs to happen while the image is being constructed. The video clarifies that the examples in the documentation show Windows commands, but: "We have Linux containers. We're gonna build Linux images. So obviously we'll be using Linux commands." [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The key distinction: `RUN` commands execute at **build time** (when the image is being created), not at **runtime** (when a container starts). They modify the image's filesystem and become permanent layers in the image.

### `CMD` — Default Command at Container Start

`CMD` specifies the **default command** that runs when a container starts from this image. It defines the process that keeps the container alive. For example, `CMD ["catalina.sh", "run"]` would start Tomcat when a container launches. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

`CMD` can be **overridden** at runtime — if you pass a command to `docker run`, it replaces the CMD. This makes CMD a default that can be changed per container.

### `ENTRYPOINT` — Fixed Command at Container Start

`ENTRYPOINT` also defines the command that runs when a container starts, but with **higher priority** than CMD. The video explains: "ENTRYPOINT will have higher priority than command, where we can mention a command. And with command we can pass the arguments." [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The relationship: when both ENTRYPOINT and CMD exist, CMD's value becomes the **arguments** to the ENTRYPOINT command. For example, if ENTRYPOINT is `["top", "-b"]` and CMD is `["-c"]`, the container runs `top -b -c`. The CMD portion can be overridden at runtime (e.g., `docker run <image> -h` would run `top -b -h` instead), but the ENTRYPOINT remains fixed. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

🔍 **Deep Dive:**
The ENTRYPOINT + CMD combination creates a **fixed-executable + default-arguments** pattern. ENTRYPOINT defines *what* runs (the binary/script), CMD defines *how* it runs by default (the arguments). Users can customize the arguments without changing the executable. This is why many production images use ENTRYPOINT for the main process and CMD for default flags — it's flexible yet controlled. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### `COPY` and `ADD` — Putting Files into the Image

Both `COPY` and `ADD` transfer files from your local machine (the build context) into the image's filesystem. This is essential for including your application code, configuration files, or artifacts in the image. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The video explains their primary use: "COPY and ADD will be very useful when you want to put your own customized data while building the image. You want to push a configuration file into your container while you're building the image, or you want to push your artifact — that we are going to do." [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The difference: `ADD` has **more capabilities** than `COPY` — specifically, `ADD` can automatically **extract compressed/zip files** and can also fetch files from URLs. `COPY` is simpler and only does straightforward file copying. The general recommendation is to use `COPY` unless you specifically need `ADD`'s extra features. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### `EXPOSE` — Declaring Container Ports

`EXPOSE` declares which port the containerized process will listen on. It doesn't actually publish the port — it's a **documentation mechanism** that tells Docker (and anyone reading the Dockerfile) which ports the container expects to use. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

The video gives a concrete example: "Let's say we're running Tomcat, CATALINA.sh run. So it's gonna run the service, bind the process on port 8080. So we have to then say EXPOSE 8080." The EXPOSE instruction matches the port that the application inside the container actually uses. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### `ENV` — Setting Environment Variables

`ENV` sets **environment variables** inside the image. These variables persist into any container started from the image. The video notes: "We don't need any environment variable, but we'll just set some environment variable" — implying it will be demonstrated for learning even though the vProfile images don't strictly require it. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### `VOLUME` — Declaring Mountable Directories

`VOLUME` declares directories inside the container that should be mountable as volumes — enabling persistent data storage or sharing between the host and container. The Apache example in the video shows three volumes: `/var/www/`, `/var/log/apache2/`, `/etc/apache2/` — the web content, logs, and configuration directories, all of which benefit from being externally accessible. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

### Other Instructions

The video also mentions `LABEL` (key-value metadata pairs, like AWS tags), `USER` (sets which user the container process runs as), `WORKDIR` (sets the working directory inside the container), and `STOPSIGNAL` (defines the signal sent to stop the container). It explicitly notes that `MAINTAINER` is **deprecated**: "If you are already using it, stop using it." [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## 1.5 — The Apache Dockerfile Example: A Complete Learning Pattern

The video highlights a specific Dockerfile example from the documentation as a recommended practice exercise because "this is very popular, very easy, and also you would have already used Apache or httpd." [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

```dockerfile
FROM debian
RUN apt-get update && apt-get install -y apache2
EXPOSE 80 443
VOLUME ["/var/www/", "/var/log/apache2/", "/etc/apache2/"]
ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]
```

This example demonstrates the complete Dockerfile pattern in miniature: start from a base image (`debian`), install software (`apache2`), expose the service ports (`80`, `443`), declare volumes for persistent/accessible data, and set the entrypoint to run the service in the foreground. The `-D FOREGROUND` flag is important — it runs Apache in the foreground instead of as a daemon, which is necessary for Docker containers (the main process must stay in the foreground or the container exits). [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## 1.6 — The Three vProfile Images: What's Being Prepared

The video establishes the setup for upcoming lectures where three custom Docker images will be built for the vProfile project: [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

| Repository    | Base Image | Purpose                                              |
| ------------- | ---------- | ---------------------------------------------------- |
| `vprofileapp` | Tomcat     | Application server — hosts the Java web application  |
| `vprofiledb`  | MySQL      | Database server — hosts the application database     |
| `vprofileweb` | NGINX      | Web server / reverse proxy — serves frontend traffic |

Each will have its own Dockerfile, built separately, pushed to its own Docker Hub repository, and then run together as containers to form the complete vProfile application stack. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Setting Up

We are preparing Docker Hub repositories for three custom images (app, db, web) and reviewing the Dockerfile instruction reference that will be used in the next lectures to write the actual Dockerfiles. The final outcome: three empty Docker Hub repositories ready to receive pushed images, and a clear understanding of every Dockerfile instruction needed for the build process. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Execution Flow Overview

```
Phase 1: Create Docker Hub repositories (3 repos)
Phase 2: Review Dockerfile reference (instructions for building)
Phase 3: Practice recommendation (Apache example)
```

***

### Step 1: Identify Your Docker Hub Account Name

**What we are doing:** Determining the namespace that will prefix all your image names.

1. Log into **hub.docker.com**.
2. Click on **Repositories** in the top navigation.
3. The name shown at the top of the repositories page is your **account name**. This is the value you'll use in the `docker build -t <account-name>/<image-name>` command. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

**In organizations:** If you're working in a team project with a Docker Hub organization, the organization name replaces your account name as the namespace. You create repositories inside the organization, and images are tagged as `org-name/image-name`.

***

### Step 2: Create Three Repositories

**What we are doing:** Creating one Docker Hub repository for each vProfile service image.

#### Repository 1: Application Image

1. Click **Create Repository**.
2. **Name:** `vprofileapp`.
3. **Visibility:** **Public** (for cost reasons during learning; use Private in production).
4. Click **Create**. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

#### Repository 2: Database Image

1. Click **Repositories** → **Create Repository**.
2. **Name:** `vprofiledb`.
3. **Visibility:** Public.
4. Click **Create**. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

#### Repository 3: Web Server Image

1. Click **Repositories** → **Create Repository**.
2. **Name:** `vprofileweb`.
3. **Visibility:** Public.
4. Click **Create**. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

**Expected result:** Three repositories visible in your Docker Hub account:

* `<account-name>/vprofileapp`
* `<account-name>/vprofiledb`
* `<account-name>/vprofileweb` [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

**Connection to flow:** These repositories are the push targets. After building each image locally with `docker build`, you'll push them here with `docker push`.

***

### Step 3: The Build and Push Command Pattern

**What we will use (in upcoming lectures):**

```bash
docker build -t <account-name>/<image-name> .
```

**Breakdown:**

* `docker build` — triggers the image build process.
* `-t <account-name>/<image-name>` — tags the built image with the full repository path (matching the Docker Hub repository).
* `.` — the build context (current directory), which must contain the `Dockerfile`. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

**After building:**

```bash
docker push <account-name>/<image-name>
```

This uploads the locally built image to the corresponding Docker Hub repository.

**Common mistake:** Forgetting the account name prefix — `docker build -t vprofileapp .` creates an image named `vprofileapp` locally, but it won't push to Docker Hub because Docker doesn't know which account/repository it belongs to. Always include the full `account-name/image-name` path. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

### Step 4: Dockerfile Instruction Reference (For Upcoming Builds)

**What we are doing:** Reviewing each instruction that will be used in the vProfile Dockerfiles.

The Docker Hub documentation provides the complete reference with examples. The key instructions and their roles in the build process:

| Instruction                                                                                                                                                                                                   | Build/Run Time      | Purpose                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | -------------------------------------------------------------- |
| `FROM`                                                                                                                                                                                                        | Build               | Set base image (Tomcat, MySQL, NGINX)                          |
| `RUN`                                                                                                                                                                                                         | Build               | Execute commands (install packages, configure)                 |
| `COPY`                                                                                                                                                                                                        | Build               | Copy files from host into image                                |
| `ADD`                                                                                                                                                                                                         | Build               | Copy files + extract archives + fetch URLs                     |
| `ENV`                                                                                                                                                                                                         | Build               | Set environment variables                                      |
| `EXPOSE`                                                                                                                                                                                                      | Build (declaration) | Document which port the service uses                           |
| `VOLUME`                                                                                                                                                                                                      | Build (declaration) | Declare mountable directories                                  |
| `LABEL`                                                                                                                                                                                                       | Build               | Add metadata (key-value tags)                                  |
| `CMD`                                                                                                                                                                                                         | Run                 | Default command when container starts (overridable)            |
| `ENTRYPOINT`                                                                                                                                                                                                  | Run                 | Fixed command when container starts (higher priority than CMD) |
| `WORKDIR`                                                                                                                                                                                                     | Build               | Set working directory for subsequent instructions              |
| `USER`                                                                                                                                                                                                        | Build               | Set which user runs the process                                |
|  [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt) |                     |                                                                |

**⚠️ Deprecated:** `MAINTAINER` — do not use. Use `LABEL maintainer="name"` instead. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

### Step 5: Practice Recommendation — Apache Dockerfile

**What we are doing:** The video recommends building this example Dockerfile as practice if you don't have hands-on Dockerfile experience.

```dockerfile
FROM debian
RUN apt-get update && apt-get install -y apache2
EXPOSE 80 443
VOLUME ["/var/www/", "/var/log/apache2/", "/etc/apache2/"]
ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

**To practice:**

1. Create a directory, create a file named `Dockerfile` (capital D), paste the above content.
2. Run `docker build -t myapache .`
3. Run `docker run -d -P myapache`
4. Verify with `docker ps` — container should be running with port 80 and 443 mapped.
5. Access via browser using the mapped port.

**Why this example:** It uses the most common instructions (FROM, RUN, EXPOSE, VOLUME, ENTRYPOINT), uses a familiar service (Apache/httpd), and is simple enough to understand completely. [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Docker Hub Repositories + Dockerfile Reference
PURPOSE:  Prepare image hosting + understand build instructions before writing Dockerfiles
CONTEXT:  Setup lecture before building 3 custom vProfile images
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Docker Hub Structure

```
Docker Hub
  └── Account (or Organization)
        ├── Repository: vprofileapp    [Public]
        ├── Repository: vprofiledb     [Public]
        └── Repository: vprofileweb    [Public]

IMAGE NAMING:  <account-name>/<repository-name>:<tag>
EXAMPLE:       myaccount/vprofileapp:latest

REAL PROJECTS:
  Account → Organization (team-shared namespace)
  Public  → Private (security)
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Build → Push Workflow

```
1. Write Dockerfile (capital D)
2. docker build -t <account>/<image> .    ← creates image locally
3. docker push <account>/<image>          ← uploads to Docker Hub

PREREQUISITE: Docker Hub repository must exist with matching name
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Three vProfile Images

```
IMAGE           BASE       PURPOSE              DOCKERFILE (upcoming)
─────           ────       ───────              ──────────
vprofileapp     Tomcat     Java app server      Will COPY artifact, EXPOSE 8080
vprofiledb      MySQL      Database             Will RUN init scripts, EXPOSE 3306
vprofileweb     NGINX      Web/reverse proxy    Will COPY config, EXPOSE 80
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Dockerfile Instruction Map

```
BUILD-TIME INSTRUCTIONS (modify image during construction):
  FROM <base>              ← MUST be first — sets starting image
  RUN <command>            ← execute command (install, configure)
  COPY <src> <dest>        ← copy files from host → image
  ADD <src> <dest>         ← like COPY + extract archives + fetch URLs
  ENV KEY=VALUE            ← set environment variable
  WORKDIR /path            ← set working directory
  USER username            ← set process user
  LABEL key=value          ← metadata tags
  EXPOSE port              ← declare service port (documentation only)
  VOLUME ["/path"]         ← declare mountable directories

RUN-TIME INSTRUCTIONS (define container startup behavior):
  CMD ["cmd", "args"]      ← default command (OVERRIDABLE at docker run)
  ENTRYPOINT ["cmd"]       ← fixed command (HIGHER PRIORITY than CMD)

DEPRECATED:
  MAINTAINER ← don't use, use LABEL instead
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## ENTRYPOINT + CMD Relationship (Critical)

```
ENTRYPOINT only:     Container runs: ENTRYPOINT
CMD only:            Container runs: CMD (overridable)
BOTH present:        Container runs: ENTRYPOINT + CMD-as-arguments

EXAMPLE:
  ENTRYPOINT ["top", "-b"]
  CMD ["-c"]
  → Container runs: top -b -c

  docker run <image> -h
  → Container runs: top -b -h     (CMD overridden, ENTRYPOINT stays)

PATTERN:
  ENTRYPOINT = WHAT to run (fixed executable)
  CMD        = HOW to run by default (overridable arguments)
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## COPY vs ADD

```
COPY:
  ├── Copies files from host → image
  └── Simple, straightforward

ADD:
  ├── Everything COPY does
  ├── + Auto-extracts .tar, .zip archives
  └── + Can fetch from URLs

RULE: Use COPY unless you specifically need ADD's extras
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## RUN vs CMD vs ENTRYPOINT

```
INSTRUCTION    WHEN           PURPOSE                    OVERRIDABLE?
───────────    ────           ───────                    ────────────
RUN            Build time     Install/configure image    N/A (baked into image)
CMD            Container start Default startup command   ✅ YES (docker run <img> <cmd>)
ENTRYPOINT     Container start Fixed startup command     ❌ NO (stays fixed)
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Apache Practice Dockerfile (Recommended)

```dockerfile
FROM debian                                    ← base OS
RUN apt-get update && apt-get install -y apache2  ← install service
EXPOSE 80 443                                  ← declare ports
VOLUME ["/var/www/", "/var/log/apache2/", "/etc/apache2/"]  ← mountable dirs
ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]   ← run in foreground

WHY FOREGROUND: Container main process must stay in foreground
                Daemon mode → process backgrounds → container thinks it exited → dies
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Public vs Private Decision

```
LEARNING:    Public  (free, 3 repos needed, no cost)
PRODUCTION:  Private (paid, images contain app code + config + secrets)

FREE TIER: 1 private repo free, unlimited public
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Account vs Organization

```
PERSONAL:      docker build -t myaccount/vprofileapp .
ORGANIZATION:  docker build -t myorg/vprofileapp .

PERSONAL = individual learning/projects
ORGANIZATION = team projects (shared namespace, access control)

"In real time, you will have organization.
 In organization, you're going to create repositories."
```

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## Reusable Engineering Patterns

| Pattern                                  | Manifestation                                                                         |
| ---------------------------------------- | ------------------------------------------------------------------------------------- |
| **Registry-Before-Build**                | Create Docker Hub repos first → then build images → push matches by name              |
| **Layered Image Construction**           | FROM (base) → RUN (install) → COPY (customize) → EXPOSE/CMD (declare behavior)        |
| **Base Image Inheritance**               | Every image starts FROM another image — build on existing work, don't start from zero |
| **Fixed Executable + Default Arguments** | ENTRYPOINT (what runs) + CMD (default args, overridable) = flexible yet controlled    |
| **Foreground Process Requirement**       | Container main process MUST run in foreground — daemon mode kills the container       |
| **Build-Time vs Run-Time Separation**    | RUN/COPY/ADD modify the image during build; CMD/ENTRYPOINT define container startup   |
| **One Image Per Service**                | vprofileapp, vprofiledb, vprofileweb — each service gets its own Dockerfile and image |
| **Namespace Organization**               | account-or-org/image-name — hierarchical naming maps to registry structure            |

 [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

## One-Line System Reconstruction

> **Docker Hub repositories (created per image as `account/repo-name`, public for learning, private for production) receive images built from Dockerfiles — which are ordered instructions starting with `FROM` (base image), using `RUN` (build-time commands), `COPY`/`ADD` (files into image), `EXPOSE` (port declaration), `ENV` (variables), `VOLUME` (mountable dirs), and `CMD`/`ENTRYPOINT` (container startup commands where ENTRYPOINT is fixed and CMD provides overridable default arguments) — with three vProfile repos (`vprofileapp`/Tomcat, `vprofiledb`/MySQL, `vprofileweb`/NGINX) prepared for the custom image builds in upcoming lectures.** [\[315-docker...references \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/315-dockerhub-and-dockerfile-references.txt)

***

This completes the full reconstruction of the Docker Hub and Dockerfile References lecture. It sets up the infrastructure (Docker Hub repositories) and knowledge foundation (Dockerfile instructions) needed for the next lectures, where three custom Dockerfiles will be written, built, pushed, and run as containers to deploy the complete vProfile application stack. Let me know if you'd like any section expanded or adjusted! 🚀
