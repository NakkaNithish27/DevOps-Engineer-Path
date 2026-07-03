# Docker Volumes — Deep Learning Material

**Source:** [306-docker-volumes.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt?EntityRepresentationId=db7a2bf2-5882-4977-b9c6-a655121892d0) (VTT Caption File) [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Container Volatility — The Core Problem

Containers are fundamentally **volatile** and **disposable**. This is not a flaw — it is a design principle. The correct way to make any change to a container (adding a package, modifying a configuration file, or any serious modification) is **never** to log in and make changes directly. Instead, you update the **image**, delete the old container, and create a new container from the updated image. This is the immutable infrastructure model that containers enforce. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

This design has a direct consequence for data: when a container is deleted, **all data stored inside it is destroyed along with it**. In orchestration systems like Kubernetes, this happens routinely — during rolling upgrades, the system removes old containers and creates new ones. Any data that lived only inside the container is permanently lost. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

For stateless containers (web servers, API gateways), this is perfectly fine — they hold no critical data. But for **stateful containers** like MySQL, the container stores databases, reads from them, and writes to them. If you replace a MySQL container, all your database data disappears. This is the fundamental problem that Docker volumes solve. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

There is a second, less obvious problem: even while a container is running, its data is stored in a **separate directory structure** that is tightly coupled to the container's filesystem. Extracting or moving that data to another location is extremely difficult — practically impossible. The data is locked inside the container's internal filesystem layer. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## 1.2 Two Solutions — Volumes and Bind Mounts

Docker provides **two mechanisms** for persistent data: **volumes** and **bind mounts**. Both solve the same root problem (data survival beyond container lifecycle), but they serve different primary use cases and have different management models. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

### Bind Mounts

A bind mount takes **any directory from the host machine** and maps it directly to a directory inside the container. The instructor draws a direct parallel: *"This is same as Vagrant sync directories."* Whatever changes you make in the host directory are immediately reflected inside the container directory, and vice versa. You have full control over which host directory to use — it can be anywhere on the host filesystem. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

The primary use case for bind mounts is **injecting data from the host into the container** — for example, developers writing code on the host machine while the container runs the application. Code changes on the host are instantly visible inside the container. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

### Volumes

A volume is a **Docker-managed directory** created inside Docker's own storage area at `/var/lib/docker/volumes/` on Linux. When you create a volume, Docker creates a named directory in that location. You then attach that volume to a container directory. All data written by the container to that directory goes into the volume on the host machine. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

Volumes are the **recommended option for data preservation**. Unlike bind mounts where you manage the directory location yourself, Docker manages volumes entirely. You reference them by name rather than by path, which is more convenient and portable. The internal structure of a volume is: `/var/lib/docker/volumes/<volume-name>/_data/` — the actual data lives inside the `_data` subdirectory. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

The key distinction: **bind mounts are for injecting/sharing data with the host; volumes are for preserving container data on the host.** Both survive container deletion — the data remains on the host machine regardless of what happens to the container. A new container can be attached to the same volume or bind mount to recover the data. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

> 🔍 **Deep Dive**
> Both mechanisms work by mapping a container-internal path to a host-external path. The difference is management ownership: with bind mounts, **you** choose and manage the host path; with volumes, **Docker** chooses and manages the host path (under `/var/lib/docker/volumes/`). Volumes are a wrapper — a layer of Docker-managed abstraction over what is fundamentally the same directory-mapping operation. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## 1.3 Docker Inspect — Reading Image and Container Metadata

`docker inspect` is a diagnostic command that returns **comprehensive JSON metadata** about an image or a container. It is the primary tool for discovering critical runtime information that you need before launching or troubleshooting containers. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

### Inspecting an Image

When you run `docker inspect` against an **image**, the JSON output reveals:

* **ExposedPorts** — Which ports the containerized process listens on. For MySQL 5.7, this is `3306` and `33060`. This tells you what port to map with `-p`. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)
* **Volumes** — The container directory where the process stores its data. For MySQL, this is `/var/lib/mysql`. This tells you what path to map with `-v`. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)
* **Cmd** — The command that runs when the container starts (e.g., `mysqld` for MySQL). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)
* **Entrypoint** — A script that runs **before** the CMD. When both exist, the entrypoint has **higher priority** — it runs first, and then the CMD is passed to it as an argument. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)
* **Environment variables** — Default env vars set in the image.

The instructor emphasizes an important warning: **do not assume** that because MySQL normally stores data at `/var/lib/mysql` on a regular Linux system, it will do the same inside a container. It might be a different directory. For official images, the documentation tells you. For unofficial images, `docker inspect` is how you discover the correct volume path. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

### Inspecting a Container

When you run `docker inspect` against a **running container**, you get additional runtime-specific information:

* **Container ID**, creation time, process ID on the host
* **Status** — running state, whether it's currently active
* **Image ID** — which image the container was created from
* **LogPath** — the file where container logs are stored on the host
* **Binds** — shows which volumes/bind mounts are attached and to which container paths
* **Port bindings** — host port ↔ container port mappings
* **Resource quotas** — memory and CPU limits (0 = unlimited)
* **Mounts** — detailed mount information including type (volume/bind), source path, destination path, and read/write mode
* **Environment variables** — all env vars active in the container
* **NetworkSettings / IPAddress** — the container's internal IP address
* **Entrypoint and CMD** — the actual commands being executed

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

> 🔍 **Deep Dive**
> The **Entrypoint + CMD relationship** works as follows: if an image defines both, the entrypoint script runs first, and the CMD value is passed to the entrypoint as an argument. When you run `docker run`, the system executes the entrypoint script and passes the CMD as its argument. This is a common pattern for initialization — the entrypoint handles setup (user creation, permissions, config generation), and the CMD starts the actual service process. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## 1.4 Docker Hub — Official Images and Documentation

When searching for images on Docker Hub, **official images** provide two key advantages: **trust** (they are maintained and verified) and **documentation** (they include usage instructions, environment variable descriptions, and volume/port information). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

For the MySQL image specifically, the documentation reveals:

* The mandatory environment variable `MYSQL_ROOT_PASSWORD` — the container **will not start** without it.
* The data storage path `/var/lib/mysql` — where to mount volumes.
* The `-e` flag syntax for setting environment variables.

The "Caveats" or "Where to Store Data" section of the documentation is where volume information is typically found. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## 1.5 Container Networking — Internal IP

Every container receives an **internal IP address** within the host machine's Docker network. This IP is visible in `docker inspect` output under NetworkSettings. You can **ping** this IP from the host machine, and services running inside the container are reachable via this IP from the host. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

However, this IP is **only accessible from within the host machine** — it is an internal network. External machines cannot use this IP to connect to the container. For external access, you must use port mapping (`-p` flag). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

The lecture demonstrates connecting to the MySQL container using the MySQL client from the host:

```bash
mysql -h <container-ip> -u root -p
```

This confirms the container is running MySQL, is reachable via its internal IP, and the root password works. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## 1.6 Docker Logs — Process Output Retrieval

The `docker logs <container-name>` command retrieves the **output generated by the process running inside the container**. The log file location on the host is visible in `docker inspect` under the `LogPath` field. This is essential for troubleshooting — if a container fails to start or behaves unexpectedly, the logs show the process output (startup messages, errors, warnings). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## 1.7 Resource Awareness — Cleanup Discipline

The instructor emphasizes a practical operational habit: **always clean up** containers and images after exercises. The learning environment uses a **t2.micro** instance with only **8 GB** of disk. Accumulated containers and images will consume disk space and memory, eventually causing resource exhaustion. The cleanup discipline is: stop the container → remove the container → remove the image. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are running a **MySQL 5.7 container** with persistent data storage using both Docker mechanisms — first a **bind mount**, then a **Docker volume**. Along the way, we use `docker inspect` to discover image metadata, `docker logs` to read container output, and the MySQL client to verify database connectivity via the container's internal IP. The final outcome: understanding how to run stateful containers with data that survives container deletion. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 1: Find and Pull the MySQL Image

Search Docker Hub for the official MySQL image.

```bash
docker pull mysql:5.7
```

| Part          | Meaning                                                 |
| ------------- | ------------------------------------------------------- |
| `docker pull` | Downloads an image from Docker Hub to the local machine |
| `mysql`       | The official MySQL image name                           |
| `:5.7`        | The specific tag/version to pull                        |

**Verification:** The image downloads in layers. Once complete, it is available locally. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Why official images matter:** They provide trustworthy, documented images. The MySQL documentation page on Docker Hub tells you the mandatory env var (`MYSQL_ROOT_PASSWORD`), the data directory (`/var/lib/mysql`), and the run command syntax. For unofficial images, you must use `docker inspect` to discover these details. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 2: Inspect the Image to Discover Metadata

```bash
docker inspect mysql:5.7
```

| Part             | Meaning                                                    |
| ---------------- | ---------------------------------------------------------- |
| `docker inspect` | Returns detailed JSON metadata about an image or container |
| `mysql:5.7`      | The image to inspect (tag is required if not `latest`)     |

**What to look for in the JSON output:**

| Field        | Value (MySQL 5.7)       | Why It Matters                                     |
| ------------ | ----------------------- | -------------------------------------------------- |
| ExposedPorts | `3306/tcp`, `33060/tcp` | Tells you what port to map with `-p`               |
| Volumes      | `/var/lib/mysql`        | Tells you the container directory to map with `-v` |
| Cmd          | `mysqld`                | The process that starts when the container runs    |
| Entrypoint   | A shell script          | Runs before CMD; passes CMD as argument            |
| Env          | Environment variables   | Shows defaults and required vars                   |

**Key warning:** Do not assume the container stores data at the same path as a bare-metal MySQL installation. Always verify via documentation or `docker inspect`. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 3: Run MySQL Container with Bind Mount

First, create the host directory that will be mapped:

```bash
mkdir /home/ubuntu/vprodbdata
```

Now run the container:

```bash
docker run --name vprodb \
  -e MYSQL_ROOT_PASSWORD=secretpass \
  -p 3030:3306 \
  -v /home/ubuntu/vprodbdata:/var/lib/mysql \
  -d mysql:5.7
```

**Command breakdown:**

| Flag/Part                                   | Meaning                                                                                                                           |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--name vprodb`                             | Names the container `vprodb` for easy reference                                                                                   |
| `-e MYSQL_ROOT_PASSWORD=secretpass`         | Sets the mandatory env var — MySQL will not start without this                                                                    |
| `-p 3030:3306`                              | Maps host port 3030 → container port 3306 (MySQL service port)                                                                    |
| `-v /home/ubuntu/vprodbdata:/var/lib/mysql` | **Bind mount** — maps the host directory (full absolute path) to the container's data directory                                   |
| `-d`                                        | Runs in **detached mode** (background). Without this, the process takes over your shell and you cannot interact with the terminal |
| `mysql:5.7`                                 | The image and tag to create the container from                                                                                    |

**Expected result:** Container starts and runs in the background. The container ID is printed. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Verification — check the host directory:**

```bash
ls /home/ubuntu/vprodbdata
```

You should see MySQL data files (ibdata, ib\_logfile, mysql directory, etc.) — all the data from `/var/lib/mysql` inside the container is now visible in the host directory. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Verification — log into the container and compare:**

```bash
docker exec -it vprodb bash
```

Inside the container:

```bash
ls /var/lib/mysql
```

The data is **identical** to what you see in the host directory — they are the same data, mapped via the bind mount. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Data persistence test — delete the container:**

```bash
docker stop vprodb
docker rm vprodb
```

Check the host directory:

```bash
ls /home/ubuntu/vprodbdata
```

**Result:** Data is still there. The container is gone, but the data persists on the host machine because it was bind-mounted. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 4: Run MySQL Container with Docker Volume

Create a named volume:

```bash
docker volume create mydbdata
```

| Part                   | Meaning                         |
| ---------------------- | ------------------------------- |
| `docker volume create` | Creates a Docker-managed volume |
| `mydbdata`             | The name of the volume          |

**Verify:**

```bash
docker volume ls
```

The volume `mydbdata` should appear in the list. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

Now run the container using the volume instead of a bind mount:

```bash
docker run --name vprodb \
  -e MYSQL_ROOT_PASSWORD=secretpass \
  -p 3030:3306 \
  -v mydbdata:/var/lib/mysql \
  -d mysql:5.7
```

The **only difference** from Step 3: the `-v` flag now uses **just the volume name** (`mydbdata`) instead of a full host directory path. Docker resolves this name to `/var/lib/docker/volumes/mydbdata/_data/` automatically. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Verify the container is running:**

```bash
docker ps
```

**Verify data is stored in the volume:**

```bash
ls /var/lib/docker/volumes/mydbdata/_data/
```

You should see the MySQL data files inside the `_data` subdirectory. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Common mistake:** If you did not remove the previous container from Step 3, creating a new container with the same name (`vprodb`) or same host port (`3030`) will cause a **conflict error**. Either remove the old container first, or use a different name and port. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

> ⚠️ **Expert Note**
> The data persists in the volume even after container deletion — same as bind mounts. But volumes are the preferred choice for data preservation because Docker manages them, they are referenced by name (portable), and they are stored in a consistent location. Bind mounts are preferred when you need to **inject** host data into a container (e.g., live code development). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 5: Inspect the Running Container

```bash
docker inspect vprodb
```

**Key fields to examine in the JSON output:**

| Field                       | What It Tells You                                            |
| --------------------------- | ------------------------------------------------------------ |
| `Status.Running`            | Whether the container is active (`true`/`false`)             |
| `Config.Image`              | Which image created this container                           |
| `LogPath`                   | Where the container's log file is stored on the host         |
| `HostConfig.Binds`          | Volume/bind mount mappings (e.g., `mydbdata:/var/lib/mysql`) |
| `HostConfig.PortBindings`   | Port mappings (e.g., `3306 → 3030`)                          |
| `HostConfig.Memory`         | Memory quota (`0` = unlimited)                               |
| `Mounts[].Type`             | `volume` or `bind` — confirms the mount type                 |
| `Mounts[].Source`           | Host-side path                                               |
| `Mounts[].Destination`      | Container-side path                                          |
| `Mounts[].RW`               | Read/write mode (`true` = read-write)                        |
| `NetworkSettings.IPAddress` | Container's internal IP address                              |
| `Config.Env`                | All active environment variables                             |
| `Config.Cmd`                | The command being executed                                   |
| `Config.Entrypoint`         | The initialization script                                    |

**Operational use cases for inspect:** When troubleshooting, use `Binds` to verify correct volume mapping, `PortBindings` to verify port mapping, `IPAddress` to connect to the container directly, and `LogPath` to find the log file. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 6: Read Container Logs

```bash
docker logs vprodb
```

| Part          | Meaning                                                            |
| ------------- | ------------------------------------------------------------------ |
| `docker logs` | Retrieves the stdout/stderr output of the container's main process |
| `vprodb`      | The container name                                                 |

**Expected output:** MySQL startup messages — initialization logs, ready-for-connections messages, or error messages if something went wrong. This is the same output you would see if the container ran in the foreground (without `-d`). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**When to use:** Whenever a container fails to start, crashes, or behaves unexpectedly — `docker logs` is the first troubleshooting step. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 7: Connect to MySQL via Container Internal IP

From the `docker inspect` output, note the container's **IPAddress** (e.g., `172.17.0.x`).

```bash
mysql -h <container-ip> -u root -p
```

| Part                | Meaning                                                    |
| ------------------- | ---------------------------------------------------------- |
| `mysql`             | The MySQL client binary (must be installed on the host)    |
| `-h <container-ip>` | Connect to the container's internal IP address             |
| `-u root`           | Username: root                                             |
| `-p`                | Prompt for password (enter the password you set with `-e`) |

Enter the password (`secretpass` in this case). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Expected result:** MySQL prompt appears. Run `show databases;` to verify the server is functional. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Important:** This internal IP is only reachable from **within the host machine**. External machines cannot use it. For external connectivity, use the mapped port (`-p 3030:3306`). [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

**Common mistake:** The instructor initially entered the wrong password and was denied access. Always verify the exact password from `docker inspect` (under `Config.Env`) if you are unsure what value you set. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Step 8: Cleanup

After completing the exercise, clean up all resources to prevent disk and resource exhaustion on the t2.micro instance:

```bash
docker stop vprodb
docker rm vprodb
docker rmi mysql:5.7
```

| Command                | Purpose                                    |
| ---------------------- | ------------------------------------------ |
| `docker stop vprodb`   | Stops the running container                |
| `docker rm vprodb`     | Removes the stopped container              |
| `docker rmi mysql:5.7` | Removes the MySQL image from local storage |

**Why cleanup matters:** The t2.micro instance has only 8 GB of disk. Accumulated images and containers consume storage and memory, potentially causing resource exhaustion and system instability. [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Problem

```
Containers = volatile + disposable
  └── Delete container → all internal data destroyed
  └── Kubernetes rolling upgrades → automatic container replacement → data loss

Stateful containers (MySQL, DBs) → MUST externalize data
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Two Persistence Mechanisms

```
BIND MOUNT                              VOLUME
─────────────                           ──────
Any host directory                      Docker-managed directory
Full path: /home/ubuntu/dir             Name only: mydbdata
You manage location                     Docker manages location
                                        Stored at: /var/lib/docker/volumes/<name>/_data/
Primary use: inject host data           Primary use: preserve container data
             into container                          on host
Example: live code development          Example: database persistence

Both: survive container deletion
Both: -v flag in docker run
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## -v Flag Syntax

```
Bind mount:  -v /full/host/path:/container/path
Volume:      -v volume-name:/container/path
                 │                    │
          name only (no /)     from docker inspect or docs
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Docker Inspect — Two Targets

```
docker inspect IMAGE
  └── ExposedPorts  → what to map with -p
  └── Volumes       → what to map with -v
  └── Cmd           → process command
  └── Entrypoint    → init script (runs before Cmd)
  └── Env           → default environment variables

docker inspect CONTAINER
  └── Status.Running → is it alive?
  └── LogPath        → host log file location
  └── Binds          → volume/mount mappings
  └── PortBindings   → host:container port map
  └── Memory/CPU     → resource quotas (0 = unlimited)
  └── Mounts[]       → type, source, destination, RW
  └── IPAddress      → container internal IP (host-only reachable)
  └── Env            → active env vars (verify passwords here)
  └── Entrypoint+Cmd → actual execution chain
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Entrypoint + CMD Relationship

```
If BOTH exist:
  Entrypoint runs FIRST (higher priority)
  CMD passed as ARGUMENT to Entrypoint

  docker run → executes: Entrypoint(CMD)
  
  Example: entrypoint.sh mysqld
           ^^^^^^^^^^^^  ^^^^^^
           init script   passed as arg
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## MySQL Container Run Command (Complete)

```
docker run --name vprodb \
  -e MYSQL_ROOT_PASSWORD=secretpass \    ← MANDATORY (container won't start without)
  -p 3030:3306 \                        ← host:container port mapping
  -v mydbdata:/var/lib/mysql \          ← volume (or full path for bind mount)
  -d mysql:5.7                          ← detached + image:tag
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Discovery Flow (Unknown Image)

```
1. Docker Hub → search → official image → read docs
   └── Find: mandatory env vars, data directory, ports

2. docker pull image:tag

3. docker inspect image:tag
   └── Find: ExposedPorts, Volumes, Cmd, Entrypoint

4. Construct docker run with correct -e, -p, -v, -d flags
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Container Networking

```
Container ← assigned internal IP (172.17.x.x)
  └── Reachable FROM host machine only
  └── NOT reachable from external machines
  └── For external access → use -p port mapping
  └── Find IP: docker inspect → NetworkSettings.IPAddress
  └── Test: ping <ip> | mysql -h <ip> -u root -p
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Troubleshooting Chain

```
Container not starting?
  └── docker logs <name>  → read process output

Wrong volume/port?
  └── docker inspect <name> → check Binds, PortBindings

Forgot password?
  └── docker inspect <name> → Config.Env → MYSQL_ROOT_PASSWORD

Can't find data directory for unknown image?
  └── docker inspect <image:tag> → Volumes

Name/port conflict on docker run?
  └── docker stop + docker rm old container, OR use different name/port
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Cleanup Sequence

```
docker stop <name> → docker rm <name> → docker rmi <image:tag>

WHY: t2.micro = 8GB disk → accumulated containers/images → resource exhaustion
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Volume Data Paths

```
Bind mount data: wherever you specified (/home/ubuntu/vprodbdata/)
Volume data:     /var/lib/docker/volumes/<name>/_data/

Both persist after: docker stop + docker rm
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

## Reusable Engineering Patterns

**Immutable Infrastructure Pattern**

```
Never modify running containers → update image → replace container
  Container = disposable runtime instance
  Image = versioned source of truth
  Consequence: all mutable state MUST be externalized
```

**State Externalization Pattern**

```
Ephemeral compute (containers, serverless, CodeBuild) → externalize:
  Data     → Volumes / Bind mounts / S3 / EBS
  Logs     → docker logs / CloudWatch / LogPath
  Config   → Env vars / mounted config files
  
  Question: "If this compute dies, where does X live?"
```

**Inspect-Before-Run Pattern**

```
Unknown image → inspect FIRST → discover ports, volumes, env, cmd
  THEN construct the run command with correct flags
  Never guess ports or volume paths
```

 [\[306-docker-volumes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/306-docker-volumes.txt)

***

This completes the full reconstruction of the Docker Volumes lecture. **Theory** builds the conceptual foundation of container volatility and persistence mechanisms, **Practical** walks through every command with full operational detail, and the **Compression Map** enables rapid recall of the architecture, relationships, and patterns. Let me know if you'd like any section refined! 🚀
