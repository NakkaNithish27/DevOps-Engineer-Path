# Docker Logs — Understanding Container Output for Troubleshooting

**Source:** Video caption file — *"Docker Logs"* (from a Docker / DevOps course) [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Are Docker Logs, Really?

The term "docker logs" can be misleading if you think of logs in the traditional sense — like application log files written to `/var/log/`. Docker logs are something more fundamental: **the output of the process that runs inside the container**. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

When a container starts, it executes a command (or sequence of commands). That command produces output — just like any command you run in a terminal produces output. When you run a container in the **foreground** (without `-d`), you see this output directly on your screen. When you run a container in the **background** (with `-d`, detached mode), the output still happens — you just don't see it. The `docker logs` command retrieves that captured output so you can read it later. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

The video states this explicitly: "The process that starts, the process output is the log. So if something goes wrong while the process starts, you can check docker logs and you can find out the problem." This is the core mental model: **container logs = stdout/stderr of the container's main process**. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## 1.2 — Where the Command Comes From: Entrypoint and CMD

To understand what output appears in docker logs, you need to understand **what command the container actually runs**. This is defined by two fields in the Docker image: **Entrypoint** and **CMD**. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

When you execute `docker run <image>`, Docker does the following internally:

1. First, it runs the **Entrypoint** — a script or command defined in the image (e.g., `docker-entrypoint.sh` for NGINX).
2. Then, it runs the **CMD** — the primary command (e.g., `nginx -g 'daemon off;'` for NGINX).

Both the Entrypoint script and the CMD command produce output. That combined output is what `docker logs` shows you. The video demonstrates this with NGINX: the logs first show the output from the entrypoint script (initialization messages), then the output from the NGINX command starting up. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

You can see what Entrypoint and CMD an image uses by running `docker inspect <image>`. This returns the image's **metadata in JSON format** — a large amount of information, but the two fields to focus on for understanding logs are `Cmd` and `Entrypoint`. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

🔍 **Deep Dive:**
The relationship between Entrypoint and CMD follows a specific execution model: Entrypoint defines the executable, CMD provides default arguments to it. In the NGINX image, the Entrypoint is a shell script (`docker-entrypoint.sh`) that performs initialization, and then it executes the CMD (`nginx -g 'daemon off;'`). When both are present, the effective command is essentially `<entrypoint> <cmd>`. Understanding this is crucial when you build your own images — if your Entrypoint script fails, the CMD never executes, and the container dies. The logs will show you exactly where in this sequence the failure occurred. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## 1.3 — Foreground vs. Background: Where Output Goes

The difference between foreground and background execution determines whether you see the process output in real-time or need `docker logs` to retrieve it. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Background (detached mode: `docker run -d`):** The container runs in the background. Docker captures all output internally. Your shell is free — you can run other commands. To see the output, you use `docker logs <container>`. This is the normal way to run production containers.

**Foreground (no `-d`):** The container runs in the foreground. All output appears directly on your terminal in real-time. But your shell is taken — you can't run other commands. For a continuously running process like NGINX, the terminal is occupied indefinitely. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

The video demonstrates the consequence of foreground mode: "It's just taken my shell, right? So if I want my shell back, I'm going to do Ctrl+C." But Ctrl+C doesn't just release the shell — **it kills the container's process**, which kills the container itself. After Ctrl+C, `docker ps` shows the container has exited. This is because Ctrl+C sends a SIGINT signal to the foreground process, terminating it, and since that process is the container's main process, the container stops. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

⚠️ **Expert Note:**
This foreground behavior is actually useful during development and debugging — you see output in real-time and can quickly kill the container with Ctrl+C. But it should never be used in production. Always use `-d` for production containers, and use `docker logs` (or a log aggregation system like Loki, ELK, or Fluentd) to access the output. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## 1.4 — The Real Purpose of Docker Logs: Troubleshooting Failed Containers

The video builds up the concepts of logs, entrypoint, CMD, and foreground/background execution for one primary purpose: **troubleshooting containers that fail to start**. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

The instructor states this directly: "When you build your own images and when you run containers from your own custom-built images, you might make some mistake and your container won't start. How do you figure out what is the problem? By looking at the output of the process. And that you can do it through the docker logs command." [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

This is demonstrated with a MySQL 5.7 container. The container is started in the background (`docker run -d mysql:5.7`), but when you check with `docker ps`, it's **not there**. Running `docker ps -a` reveals it — with status **exited**. The container started, tried to run its entrypoint, encountered an error, and died. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

Running `docker logs <container>` reveals the error: "database is uninitialized and password option is not specified. You need to specify one of the following" — followed by a list of required environment variables (`MYSQL_ROOT_PASSWORD`, `MYSQL_ALLOW_EMPTY_PASSWORD`, `MYSQL_RANDOM_ROOT_PASSWORD`). The MySQL image's entrypoint script checks for these variables and refuses to start without one of them. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

The diagnostic flow is: [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

1. Container should be running → check `docker ps` → not there.
2. Check all containers → `docker ps -a` → container exists but exited.
3. Read the logs → `docker logs <container>` → error message tells you exactly what's wrong.
4. Fix the issue → re-run with the required configuration.

This is the **standard debugging pattern** for Docker containers and will be used repeatedly in upcoming lectures when building custom images and containerizing projects. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## 1.5 — Environment Variables in Containers: The `-e` Flag

The MySQL failure demonstrates a container that requires **configuration via environment variables**. Many Docker images are designed to be configured through environment variables rather than configuration files — this makes them flexible and avoids hardcoding values into the image. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

To pass an environment variable into a container, you use the `-e` flag:

```bash
docker run -d -e MYSQL_ROOT_PASSWORD=My mysql:5.7
```

The `-e MYSQL_ROOT_PASSWORD=My` sets an environment variable inside the container. The MySQL entrypoint script reads this variable, uses its value as the root password, and proceeds with initialization. The container now starts successfully. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

The video notes that the details of MySQL configuration (password, volumes, etc.) will be covered in the next lecture on Docker volumes. In this lecture, the environment variable is introduced only to resolve the logs-demonstrated failure and show the diagnostic-to-fix workflow. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## 1.6 — Docker Inspect: Image Metadata

`docker inspect <image>` returns **detailed metadata** about a Docker image in JSON format. The video uses it specifically to show the Entrypoint and CMD fields, but notes: "There's a lot of information about this. We're going to see this in the coming lecture." [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

The key insight for this lecture: `docker inspect` tells you **what commands the container will run** before you even start it. This is valuable for understanding what output to expect in docker logs and for diagnosing why a container might fail — if you know what command runs, you can predict what might go wrong. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## 1.7 — The `-P` Flag: Automatic Port Mapping

The video uses `-P` (capital P) when running the NGINX container. This flag performs **automatic port mapping** — Docker picks a random available port on the host and maps it to the container's exposed port. Unlike lowercase `-p` (e.g., `-p 8080:80` where you specify both host and container ports), uppercase `-P` eliminates the need to choose a host port manually. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

After running with `-P`, `docker ps` shows the automatically assigned port mapping. This is a convenience feature for quick testing when you don't care about the specific host port number. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Learning

We are learning to use `docker logs` for container troubleshooting — understanding what logs actually contain, how to access them, and how to use them to diagnose and fix container failures. The final outcome: the ability to diagnose why any container fails to start by reading its logs, and understanding the relationship between image commands (Entrypoint/CMD) and log output. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Pre-Requisite: Clean Environment

The video starts with a clean Docker environment — no images, no containers. This is the recommended state for following along. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

### Step 1: Pull the NGINX Image

**What we are doing:** Downloading a fresh NGINX image to work with.

```bash
docker pull nginx
```

**Expected output:** Layer download progress, ending with "Status: Downloaded newer image for nginx:latest." [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

### Step 2: Inspect the Image (Understand What It Will Run)

**What we are doing:** Examining the image's metadata to see what commands it will execute when a container starts.

```bash
docker inspect nginx
```

**Expected output:** A large JSON document containing all image metadata. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**What to look for:** Scroll through the output and find two fields:

* **`Entrypoint`** — shows the script that runs first (e.g., `docker-entrypoint.sh`).
* **`Cmd`** — shows the main command (e.g., `nginx -g 'daemon off;'`). [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Connection to flow:** These two commands produce the output that `docker logs` will show. Knowing them helps you interpret the logs.

***

### Step 3: Run NGINX in Background and View Logs

**What we are doing:** Starting an NGINX container in detached mode and retrieving its output via docker logs.

```bash
docker run -d -P nginx
```

**Breakdown:**

* `docker run` — create and start a container.
* `-d` — detached mode (background). Output is captured, not displayed.
* `-P` — automatic port mapping (Docker picks a random host port for NGINX's port 80).
* `nginx` — the image to run. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Verify the container is running:**

```bash
docker ps
```

**Expected output:** The container appears with its name, the port mapping (e.g., `0.0.0.0:32768->80/tcp`), and status "Up." [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**View the logs:**

```bash
docker logs <container-name-or-id>
```

**Expected output:** Two sections of output:

1. Output from the **Entrypoint script** — initialization messages.
2. Output from the **CMD** (`nginx -g 'daemon off;'`) — NGINX startup messages. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**This is the normal, healthy log output** of a successfully started container.

***

### Step 4: Run NGINX in Foreground (Demonstrate Ctrl+C Behavior)

**What we are doing:** Running a second NGINX container without `-d` to see output in real-time and understand the Ctrl+C consequence.

```bash
docker run -P nginx
```

**Expected output:** All the same output appears directly on your terminal. The shell is occupied — you cannot type other commands. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**To get your shell back:**

Press **Ctrl+C**.

**What happens:** Ctrl+C sends SIGINT to the NGINX process → process terminates → container stops. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Verify:**

```bash
docker ps
```

The container is **not listed** (it's stopped).

```bash
docker ps -a
```

The container appears with status "Exited 8 seconds ago." [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Lesson:** Foreground mode ties your shell to the container's lifecycle. Ctrl+C kills the container. Always use `-d` for containers that should keep running.

***

### Step 5: Troubleshooting a Failed Container — MySQL Example

**What we are doing:** Demonstrating the real-world troubleshooting workflow using a MySQL container that fails to start.

#### 5a: Run MySQL Without Required Configuration

```bash
docker run -d mysql:5.7
```

**What happens internally:** Docker pulls the `mysql:5.7` image (if not present), creates a container, starts the entrypoint script. The entrypoint checks for required environment variables, doesn't find them, prints an error, and exits. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Check if the container is running:**

```bash
docker ps
```

**Expected output:** The MySQL container is **NOT listed**. This is the first sign of a problem. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

#### 5b: Find the Dead Container

```bash
docker ps -a
```

**Expected output:** The MySQL container appears with status **Exited**. It started and immediately died. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Key diagnostic insight:** `docker ps` shows only running containers. `docker ps -a` shows ALL containers including stopped/exited ones. When a container you expected to be running is missing from `docker ps`, always check `docker ps -a`.

#### 5c: Read the Logs to Find the Error

```bash
docker logs <container-name-or-id>
```

**Expected output:** Error message from the entrypoint: [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

```
error entrypoint... database is uninitialized and password option is not specified.
You need to specify one of the following:
- MYSQL_ROOT_PASSWORD
- MYSQL_ALLOW_EMPTY_PASSWORD
- MYSQL_RANDOM_ROOT_PASSWORD
```

**Diagnosis:** The MySQL image requires one of these environment variables to be set. Without it, the entrypoint refuses to initialize the database and exits.

#### 5d: Fix and Re-Run

```bash
docker run -d -e MYSQL_ROOT_PASSWORD=My mysql:5.7
```

**Breakdown:**

* `-e MYSQL_ROOT_PASSWORD=My` — sets the environment variable `MYSQL_ROOT_PASSWORD` to the value `My` inside the container. The MySQL entrypoint reads this variable and uses it as the root password during initialization. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

**Verify:**

```bash
docker ps
```

**Expected output:** The MySQL container is now **running** — it appears in `docker ps` with status "Up." [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

#### 5e: View Logs of the Running Container

```bash
docker logs <container-name-or-id>
```

**Expected output:** A large amount of output — MySQL initialization messages, database creation, user setup, startup confirmation. "A lot of things" — this is normal for MySQL's startup process. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

### Step 6: Recommended Practice

The video recommends hands-on exploration before the next lecture: [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

1. **Fetch different images** of your choice.
2. **Run `docker inspect`** on each — see what Entrypoint and CMD they use.
3. **Run `docker logs`** on containers started from those images — see the output of those commands.
4. **Cleanup:** Remove all containers (`docker rm`) and all images (`docker rmi`) before the next lecture. [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Docker Logs
PURPOSE:  Understand container output + troubleshoot failed containers
CONTEXT:  Before custom image building lectures (where failures will happen)
CORE IDEA: Container logs = stdout/stderr of Entrypoint + CMD process
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## What Docker Logs Actually Are

```
docker run <image>
    │
    ▼
Runs ENTRYPOINT script → produces OUTPUT
    │
    ▼
Runs CMD command → produces OUTPUT
    │
    ▼
COMBINED OUTPUT = docker logs

"The process that starts, the process output is the log"
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Entrypoint + CMD → Logs Relationship

```
docker inspect <image> → shows:
  Entrypoint: ["docker-entrypoint.sh"]    ← runs FIRST
  Cmd:        ["nginx", "-g", "daemon off;"]  ← runs SECOND

docker logs <container> → shows:
  [output of entrypoint script]
  [output of CMD command]

INSPECT BEFORE RUN → know what to expect in logs
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Foreground vs. Background

```
docker run -d <image>        BACKGROUND (detached)
  ├── Output captured silently
  ├── Shell is FREE
  ├── View output: docker logs <container>
  └── Container keeps running

docker run <image>           FOREGROUND
  ├── Output shown in real-time on terminal
  ├── Shell is OCCUPIED
  ├── Ctrl+C → kills process → kills container
  └── Container DIES when you exit

RULE: Always use -d for persistent containers
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Troubleshooting Flow (Critical Pattern)

```
EXPECTED: Container should be running
    │
    ▼
docker ps → container NOT listed
    │
    ▼
docker ps -a → container shows "Exited"
    │
    ▼
docker logs <container> → ERROR MESSAGE
    │
    ▼
Read error → understand what's missing/wrong
    │
    ▼
Fix (e.g., add -e variable) → re-run
    │
    ▼
docker ps → container NOW running ✅

THIS PATTERN WILL BE USED REPEATEDLY in custom image lectures
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## MySQL Failure Example (Concrete)

```
docker run -d mysql:5.7
    │
    ▼
docker ps → NOT THERE
docker ps -a → Exited
docker logs → "database is uninitialized, password option not specified"
             "specify one of: MYSQL_ROOT_PASSWORD, MYSQL_ALLOW_EMPTY_PASSWORD,
              MYSQL_RANDOM_ROOT_PASSWORD"
    │
    ▼
FIX: docker run -d -e MYSQL_ROOT_PASSWORD=My mysql:5.7
    │
    ▼
docker ps → RUNNING ✅
docker logs → full MySQL initialization output (healthy)
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Key Commands

```
COMMAND                        PURPOSE
───────                        ───────
docker pull <image>            Download image
docker inspect <image>         View metadata (Entrypoint, CMD, etc.) in JSON
docker run -d -P <image>       Run in background, auto port mapping
docker run -d -e VAR=val <img> Run with environment variable
docker ps                      List RUNNING containers only
docker ps -a                   List ALL containers (including exited)
docker logs <container>        View process output of container
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Port Mapping: `-P` vs `-p`

```
-P (capital)   Automatic: Docker picks random host port → maps to container port
               docker run -d -P nginx → 0.0.0.0:32768->80/tcp

-p (lowercase) Manual: You specify both ports
               docker run -d -p 8080:80 nginx → 0.0.0.0:8080->80/tcp
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Environment Variables in Containers

```
SYNTAX: docker run -e VARIABLE_NAME=value <image>

EXAMPLE: docker run -d -e MYSQL_ROOT_PASSWORD=My mysql:5.7

WHY: Many images require configuration via env vars
     (passwords, modes, settings)
     Image entrypoint reads env vars → configures service accordingly
     Missing required env var → entrypoint fails → container exits
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Docker Inspect → Docker Logs Connection

```
WORKFLOW:
  1. docker inspect <image>     → What WILL it run? (Entrypoint + CMD)
  2. docker run -d <image>      → Run it
  3. docker logs <container>    → What DID it output? (result of Entrypoint + CMD)

inspect = PREDICT
logs    = OBSERVE
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Container Visibility Rules

```
docker ps       → shows ONLY containers with status "Up"
docker ps -a    → shows ALL containers (Up + Exited + Created)

MISSING FROM docker ps?
  → NOT necessarily deleted
  → Check docker ps -a → likely "Exited"
  → Check docker logs → find why it died
```

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## Reusable Engineering Patterns

| Pattern                                             | Manifestation                                                                               |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Process Output as Diagnostic Source**             | Container logs = stdout/stderr of main process — primary troubleshooting tool               |
| **Inspect Before Execute**                          | `docker inspect` reveals what commands will run — predict behavior before starting          |
| **Failed-Silent Detection**                         | Container exits silently in `-d` mode — `docker ps` vs `docker ps -a` reveals the gap       |
| **Error-Driven Configuration**                      | MySQL logs tell you exactly what env vars are missing — error message IS the fix guide      |
| **Environment-Based Configuration**                 | `-e` flag injects runtime config into containers — images designed for env-var-driven setup |
| **Foreground for Debug, Background for Production** | No `-d` = see output live + Ctrl+C kills; `-d` = persistent + use `docker logs`             |
| **Execution Chain Visibility**                      | Entrypoint → CMD = two-stage startup; logs show output of both stages sequentially          |

 [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

## One-Line System Reconstruction

> **Docker logs are the stdout/stderr output of the container's Entrypoint script + CMD command (viewable via `docker inspect` before running), accessed with `docker logs <container>` for background (`-d`) containers — with the primary use case being troubleshooting failed containers by checking `docker ps` (missing) → `docker ps -a` (exited) → `docker logs` (error message reveals the fix, e.g., MySQL requiring `-e MYSQL_ROOT_PASSWORD=value`), establishing the diagnostic pattern used throughout all custom image building and containerization work.** [\[305-docker-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/305-docker-logs.txt)

***

This completes the full reconstruction of the Docker Logs lecture. It establishes the foundational debugging workflow that will be used extensively in upcoming lectures when building custom Docker images and containerizing the vProfile project — where containers will inevitably fail during development, and `docker logs` will be the primary diagnostic tool. Let me know if you'd like any section expanded or adjusted! 🚀
