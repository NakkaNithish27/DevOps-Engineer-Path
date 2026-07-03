# 🎓 Deep Learning Material: Docker Compose for the vProfile Project — Writing the Compose File

**Source:** [319-docker-compose.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt?EntityRepresentationId=63837107-d648-42c3-87ad-47aba9ddc403) (video caption) + [319.compose.yml.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt?EntityRepresentationId=28ba960f-511d-47d2-8edd-2662ae553792) (compose file) — Video lecture covering the complete process of writing a Docker Compose file for the vProfile multi-container project: requirement gathering from `application.properties`, mapping five services (MySQL, Memcached, RabbitMQ, Tomcat app, Nginx web) with their ports, volumes, environment variables, build contexts, container names, and image naming for Docker Hub upload. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt), [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Five-Container Architecture

The vProfile application requires **five containers** running together, each playing a distinct role. Three containers need custom images built from Dockerfiles (database, application, web server), and two containers use official images directly from Docker Hub (Memcached, RabbitMQ). [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

| Container     | Role                                     | Image Source                   | Needs Dockerfile? |
| ------------- | ---------------------------------------- | ------------------------------ | ----------------- |
| `vprodb`      | MySQL database                           | Custom (build from Dockerfile) | Yes               |
| `vprocache01` | Memcached cache                          | Official Docker Hub image      | No                |
| `vpromq01`    | RabbitMQ message broker                  | Official Docker Hub image      | No                |
| `vproapp`     | Tomcat application server (vProfile WAR) | Custom (build from Dockerfile) | Yes               |
| `vproweb`     | Nginx reverse proxy (frontend)           | Custom (build from Dockerfile) | Yes               |

This mirrors the same architecture used in previous sections (VMs, EC2 instances, cloud services) — but now every component is a container. Docker Compose orchestrates all five together on a shared network. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.2 Requirement Gathering — The Critical Pre-Writing Step

Before writing a single line of the compose file, the instructor systematically gathers **all requirements** for each container. This is explicitly called "requirement gathering" — the same process used in real engineering. The instructor states: "In real-time also, when you're writing a docker-compose file like this, you need to have all the information handy, so then it becomes easy for you to write the docker-compose file." [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

The primary source of truth for container configuration is the **`application.properties` file** in the vProfile source code (`src/main/resources/application.properties`). This file defines how the Java application connects to its backend services — it specifies **hostnames**, **ports**, **usernames**, and **passwords** for the database, cache, and message broker. Every container's configuration must **match** what this file expects. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

For example, the application.properties file says:

* Database host: `vprodb`, port `3306`, user `root`, password `vprodbpass`
* Memcache host: `vprocache01`, port `11211`
* RabbitMQ host: `vpromq01`, port `5672`, user `guest`, password `guest`

These hostnames become the **container names** in the compose file. In Docker Compose's automatic network, containers reach each other by name — so if the application code expects the database at hostname `vprodb`, the database container must be named exactly `vprodb`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

🔍 **Deep Dive**
The service name in the compose file (the key under `services:`) is used as the hostname by default. However, Docker Compose may add prefixes and suffixes to the actual container name (e.g., `project_vprodb_1`). This modified name would break hostname resolution if the app connects by container name. The `container_name:` directive **overrides** this behavior, forcing the exact name. The instructor emphasizes this: "When you run the container with docker-compose, it's going to add some prefix and suffix. So, we need to make sure the container name is absolutely same as mentioned in the application.properties file." [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.3 The `build` Directive with `context`

In the previous Docker Compose lecture, `build: .` was used when the Dockerfile was in the same directory as the compose file. In this project, Dockerfiles are in **subdirectories** — `Docker-files/db/`, `Docker-files/app/`, `Docker-files/web/`. To point to a Dockerfile in a different location, you use the expanded `build` syntax with `context:`: [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

```yaml
build:
  context: ./Docker-files/db
```

The `context` specifies the directory where Docker should look for the Dockerfile. Docker will search for a file literally named `Dockerfile` in that directory and build from it. The context also determines the build context — the set of files available during the build (for `COPY` instructions, etc.). [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.4 The `image` Directive — Dual Purpose

The `image:` directive serves **two different purposes** depending on whether `build:` is also present: [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**Without `build`:** It specifies which image to **pull** from Docker Hub and run. For Memcached: `image: memcached` pulls the official Memcached image. For RabbitMQ: `image: rabbitmq` pulls the official RabbitMQ image.

**With `build`:** It specifies the **name to give** the built image. For the database: `build: ... + image: vprocontainers/vprofiledb` means "build from the Dockerfile AND name the resulting image `vprocontainers/vprofiledb`." This naming follows the Docker Hub convention: `<account>/<image>`. The instructor uses the account name `vprocontainers` — matching a Docker Hub account — so that later, the image can be pushed directly with `docker push vprocontainers/vprofiledb`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

This dual-purpose behavior is a subtle but important aspect of the compose file. When both `build` and `image` are present, Docker Compose builds the image and tags it with the specified name. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.5 Environment Variables from Official Image Documentation

For containers using official images, you often need to set **environment variables** to configure the service. The correct variable names are found in the **Docker Hub documentation** for each image: [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**MySQL:** The variable `MYSQL_ROOT_PASSWORD` is **mandatory**. Without it, the MySQL container will not start. The value must match what the application expects (from `application.properties`): `vprodbpass`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**RabbitMQ:** The variables `RABBITMQ_DEFAULT_USER` and `RABBITMQ_DEFAULT_PASS` set the default credentials. The instructor navigates to the RabbitMQ Docker Hub page, scrolls to "Setting default user and password," and copies the exact variable names. Values: `guest`/`guest` — matching `application.properties`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**Memcached:** No environment variables needed — it runs as-is with default settings. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

⚠️ **Expert Note**
The instructor's workflow for finding environment variables — going to the Docker Hub page, scrolling to the environment variable section — is the standard real-world process. Don't guess variable names. Official images document their supported variables. Using the wrong variable name means the container runs but the setting doesn't apply, leading to silent misconfigurations. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.6 Volumes — Persistent Data for Stateful Containers

Two named volumes are declared at the top level and mapped to containers that need data persistence: [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt), [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

**`vprodbdata`** → mapped to `/var/lib/mysql` in the `vprodb` container. This is where MySQL stores all database files. Without this volume, destroying the container would lose all data.

**`vproappdata`** → mapped to `/usr/local/tomcat/webapps` in the `vproapp` container. The instructor notes this volume "is not a necessity, but just to show you one extra option" — it persists the deployed WAR file.

Both are declared as `{}` (empty object) at the top level, meaning Docker creates a **host volume** — a directory managed by Docker Engine on the host filesystem. The instructor notes: "Since this is just for testing, development purpose, a host volume here is also fine. In Kubernetes, we'll see how we can manage volumes externally." [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.7 The Compose File Naming Convention

The **preferred name** for the compose file is `compose.yml` (or `compose.yaml`). The previous convention was `docker-compose.yml`. The instructor explicitly renames the file: "The current name is compose.yml and this is the preferred one, but you can also use docker-compose.yml, which was the previous one." Both `.yml` and `.yaml` extensions work. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.8 The Container Name Matching Rule

This is the most important operational rule in this lecture: **container names in the compose file must exactly match the hostnames expected in `application.properties`**. The app container connects to `vprodb:3306` — so the database container must be named `vprodb`. The app connects to `vprocache01:11211` — so the Memcache container must be named `vprocache01`. A single character difference means the application cannot find its backend services. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

The `vproweb` container's name is more flexible because "it's a frontend one" — nothing connects to it by name from within the compose network. It receives traffic from external users. The instructor gives it the name `vproweb` by convention, not by requirement. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## 1.9 The Request Flow Within the Compose Network

The nginx web container (`vproweb`) receives external HTTP requests on port 80 and forwards them to the app container (`vproapp`) on port 8080. This routing is configured in the nginx configuration file (part of the web Dockerfile), which references `vproapp:8080`. The app container then connects to the database (`vprodb:3306`), cache (`vprocache01:11211`), and message broker (`vpromq01:5672`) using the hostnames from `application.properties`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing the complete Docker Compose file (`compose.yml`) for the vProfile project — five services, three with custom Dockerfiles, two from Docker Hub images. The final outcome: a single file that, when executed with `docker compose up`, builds all custom images and runs all five containers together on a shared network, fully interconnected and matching the application's expected configuration. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## Step 1: Gather Requirements from `application.properties`

Open the vProfile source code and navigate to:

```
src/main/resources/application.properties
```

Extract every backend connection detail: [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

| Service      | Hostname      | Port  | Username | Password     | Notes                                             |
| ------------ | ------------- | ----- | -------- | ------------ | ------------------------------------------------- |
| MySQL        | `vprodb`      | 3306  | `root`   | `vprodbpass` | Database name: `accounts` (handled in Dockerfile) |
| Memcache     | `vprocache01` | 11211 | —        | —            | No auth needed                                    |
| RabbitMQ     | `vpromq01`    | 5672  | `guest`  | `guest`      |                                                   |
| App (Tomcat) | `vproapp`     | 8080  | —        | —            | Referenced in nginx config                        |

Also check the **nginx config file** in the web Dockerfile directory — it forwards requests to `vproapp:8080`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**Why this matters:** Every value in this table becomes a directive in the compose file. Mismatched values = broken connections.

***

## Step 2: Rename the Compose File

Rename the file to use the current preferred naming convention:

```
docker-compose.yml → compose.yaml
```

Right-click → Rename (in your editor). Remove `docker-` prefix, change extension to `.yaml`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## Step 3: Write the Top-Level Structure

```yaml
services:

volumes:
   vprodbdata: {}
   vproappdata: {}
```

 [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

| Section           | Purpose                                |
| ----------------- | -------------------------------------- |
| `services:`       | All five container definitions go here |
| `volumes:`        | Named volumes for persistent data      |
| `vprodbdata: {}`  | Host volume for MySQL data             |
| `vproappdata: {}` | Host volume for Tomcat webapps         |

The `{}` means Docker Engine manages the volume location on the host. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## Step 4: Write the Database Service (`vprodb`)

```yaml
  vprodb:
    build:
      context: ./Docker-files/db
    image: vprocontainers/vprofiledb
    container_name: vprodb
    ports:
      - "3306:3306"
    volumes:
      - vprodbdata:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=vprodbpass
```

 [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

| Directive         | Value                            | Why                                                                               |
| ----------------- | -------------------------------- | --------------------------------------------------------------------------------- |
| `build: context:` | `./Docker-files/db`              | Dockerfile is in the `db` subdirectory                                            |
| `image:`          | `vprocontainers/vprofiledb`      | Name the built image for Docker Hub push                                          |
| `container_name:` | `vprodb`                         | **Must match** `application.properties` hostname                                  |
| `ports:`          | `"3306:3306"`                    | MySQL port — host and container same                                              |
| `volumes:`        | `vprodbdata:/var/lib/mysql`      | Persist database files                                                            |
| `environment:`    | `MYSQL_ROOT_PASSWORD=vprodbpass` | **Mandatory** — MySQL won't start without it. Value from `application.properties` |

⚠️ No space between the volume name and the container path: `vprodbdata:/var/lib/mysql` — not `vprodbdata: /var/lib/mysql`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## Step 5: Write the Memcache Service (`vprocache01`)

```yaml
  vprocache01:
    image: memcached
    ports:
      - "11211:11211"
```

 [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

Simplest service — official image, one port, no build, no environment, no volumes. Container name defaults to the service key `vprocache01`. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**Note:** The compose file in the resource doesn't explicitly include `container_name: vprocache01` for this service, relying on the service name for DNS resolution on the compose network. [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

***

## Step 6: Write the RabbitMQ Service (`vpromq01`)

```yaml
  vpromq01:
    image: rabbitmq
    ports:
      - "5672:5672"
    environment:
      - RABBITMQ_DEFAULT_USER=guest
      - RABBITMQ_DEFAULT_PASS=guest
```

 [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

| Directive               | Notes                                          |
| ----------------------- | ---------------------------------------------- |
| `image: rabbitmq`       | Official image from Docker Hub                 |
| `environment:`          | Variable names from RabbitMQ Docker Hub docs   |
| `RABBITMQ_DEFAULT_USER` | Not `RABBITMQ_USER` — exact name from docs     |
| `RABBITMQ_DEFAULT_PASS` | Not `RABBITMQ_PASSWORD` — exact name from docs |

**Where to find variable names:** Docker Hub → RabbitMQ → scroll to "Setting default user and password." [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## Step 7: Write the Application Service (`vproapp`)

```yaml
  vproapp:
    build:
      context: ./Docker-files/app
    image: vprocontainers/vprofileapp
    container_name: vproapp
    ports:
      - "8080:8080"
    volumes:
      - vproappdata:/usr/local/tomcat/webapps
```

 [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

| Directive         | Value                                   | Why                                                      |
| ----------------- | --------------------------------------- | -------------------------------------------------------- |
| `build: context:` | `./Docker-files/app`                    | Dockerfile for the app image                             |
| `image:`          | `vprocontainers/vprofileapp`            | Name for Docker Hub push                                 |
| `container_name:` | `vproapp`                               | **Must match** nginx config and `application.properties` |
| `ports:`          | `"8080:8080"`                           | Tomcat port                                              |
| `volumes:`        | `vproappdata:/usr/local/tomcat/webapps` | Optional — persists deployed WAR                         |

No environment variables needed — the application reads its config from `application.properties` bundled in the WAR file. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## Step 8: Write the Web Service (`vproweb`)

```yaml
  vproweb:
    build:
      context: ./Docker-files/web
    image: vprocontainers/vprofileweb
    container_name: vproweb
    ports:
      - "80:80"
```

 [\[319.compose.yml \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319.compose.yml.txt)

| Directive         | Value                | Why                                                  |
| ----------------- | -------------------- | ---------------------------------------------------- |
| `build: context:` | `./Docker-files/web` | Dockerfile for nginx image                           |
| `container_name:` | `vproweb`            | Flexible — nothing connects to it by name internally |
| `ports:`          | `"80:80"`            | Nginx listens on port 80                             |

No volumes, no environment variables. The nginx config is baked into the image via the Dockerfile. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

***

## Step 9: Validate the Compose File

**9a. Check indentation:** All service names (`vprodb:`, `vprocache01:`, etc.) must be at the same indentation level (3 spaces under `services:`). All directives within a service must be at the next level. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**9b. Cross-check against `application.properties`:** Verify every hostname, port, username, and password matches exactly. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**9c. Compare with the reference file:** Download the compose file from the lecture resources and compare it with yours to catch any mistakes. [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**Common mistakes:**

* Forgetting `container_name` → compose adds prefix/suffix → app can't resolve hostname.
* Space between volume name and path → `vprodbdata: /var/lib/mysql` instead of `vprodbdata:/var/lib/mysql`.
* Wrong Dockerfile path in `context`.
* Copy-paste errors — leaving previous service's values (e.g., `db` path in the `app` service). [\[319-docker-compose \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/319-docker-compose.txt)

**Connection to larger flow:** The compose file is now complete. The next lecture runs `docker compose up` to build all images and start all five containers together.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Five-Container Architecture

```
                     ┌──── INTERNET ────┐
                     │                   │
                     ▼                   │
              ┌─────────────┐            │
              │  vproweb    │ :80        │
              │  (nginx)    │            │
              │  BUILD      │            │
              └──────┬──────┘            │
                     │ forwards to vproapp:8080
                     ▼
              ┌─────────────┐
              │  vproapp    │ :8080
              │  (tomcat)   │
              │  BUILD      │
              └──┬───┬───┬──┘
                 │   │   │
      ┌──────────┘   │   └──────────┐
      ▼              ▼              ▼
┌──────────┐  ┌────────────┐  ┌──────────┐
│ vprodb   │  │vprocache01 │  │ vpromq01 │
│ (mysql)  │  │(memcached) │  │(rabbitmq)│
│ :3306    │  │ :11211     │  │ :5672    │
│ BUILD    │  │ IMAGE      │  │ IMAGE    │
└──────────┘  └────────────┘  └──────────┘
```

***

## Service Configuration Matrix

```
Service       │ Source  │ container_name │ Port  │ Volume              │ Env Vars
──────────────┼────────┼────────────────┼───────┼─────────────────────┼──────────────────────
vprodb        │ BUILD  │ vprodb         │ 3306  │ vprodbdata:/var/lib/ │ MYSQL_ROOT_PASSWORD
              │ db/    │                │       │ mysql               │ =vprodbpass
vprocache01   │ IMAGE  │ (service name) │ 11211 │ —                   │ —
vpromq01      │ IMAGE  │ (service name) │ 5672  │ —                   │ RABBITMQ_DEFAULT_USER
              │        │                │       │                     │ RABBITMQ_DEFAULT_PASS
vproapp       │ BUILD  │ vproapp        │ 8080  │ vproappdata:/usr/   │ —
              │ app/   │                │       │ local/tomcat/webapps│
vproweb       │ BUILD  │ vproweb        │ 80    │ —                   │ —
              │ web/   │                │       │                     │
```

***

## BUILD vs IMAGE Decision

```
BUILD (custom Dockerfile):
  vprodb    → Docker-files/db/Dockerfile
  vproapp   → Docker-files/app/Dockerfile
  vproweb   → Docker-files/web/Dockerfile

IMAGE (official from Docker Hub):
  vprocache01 → memcached
  vpromq01    → rabbitmq

Rule: BUILD when you need customization (your app, your config)
      IMAGE when official service is sufficient
```

***

## `build` + `image` Together

```yaml
build:
  context: ./Docker-files/db     ← WHERE to find Dockerfile
image: vprocontainers/vprofiledb ← WHAT to NAME the built image

build alone  → builds, auto-names
image alone  → pulls from registry
both         → builds AND names (for Docker Hub push: account/image)
```

***

## Source of Truth: application.properties

```
application.properties says:
  db.host=vprodb          → container_name: vprodb
  db.port=3306            → ports: "3306:3306"
  db.user=root            → (MySQL default)
  db.password=vprodbpass  → MYSQL_ROOT_PASSWORD=vprodbpass

  mc.host=vprocache01     → container_name/service: vprocache01
  mc.port=11211           → ports: "11211:11211"

  mq.host=vpromq01        → container_name/service: vpromq01
  mq.port=5672            → ports: "5672:5672"
  mq.user=guest           → RABBITMQ_DEFAULT_USER=guest
  mq.pass=guest           → RABBITMQ_DEFAULT_PASS=guest

nginx config says:
  proxy_pass vproapp:8080 → container_name: vproapp

EVERY compose value derives from these source files
```

***

## Container Name Rule

```
container_name: directive → FORCES exact name
Without it → Docker Compose adds prefix/suffix (e.g., project_vprodb_1)

MANDATORY for: vprodb, vproapp (referenced by name in app config / nginx config)
FLEXIBLE for:  vproweb (nothing connects to it by name internally)
```

***

## Environment Variable Sources

```
MySQL:     MYSQL_ROOT_PASSWORD      ← mandatory, container won't start without it
           Source: Docker Hub → MySQL → Environment Variables

RabbitMQ:  RABBITMQ_DEFAULT_USER    ← from Docker Hub → RabbitMQ docs
           RABBITMQ_DEFAULT_PASS    ← NOT RABBITMQ_PASSWORD (wrong name!)

Memcached: none needed
Tomcat:    none needed (config in WAR)
Nginx:     none needed (config in image)
```

***

## Volume Mapping

```
vprodbdata:/var/lib/mysql              ← MySQL data persistence
vproappdata:/usr/local/tomcat/webapps  ← WAR file persistence (optional)

Declared as: volumes: { vprodbdata: {}, vproappdata: {} }
{} = Docker-managed host volume (local directory)
⚠️ No space between name and path: vprodbdata:/var/lib/mysql
```

***

## File Structure

```
project-root/
├── compose.yaml                    ← THIS file (5 services)
├── Docker-files/
│   ├── db/Dockerfile               ← MySQL custom image
│   ├── app/Dockerfile              ← Tomcat + vProfile WAR
│   └── web/Dockerfile              ← Nginx + custom config
└── src/main/resources/
    └── application.properties      ← source of truth for all config
```

***

## Compose File Writing Workflow

```
1. Read application.properties     → extract hostnames, ports, credentials
2. Read nginx config               → extract upstream hostname:port
3. Read Docker Hub docs             → find env variable names (MySQL, RabbitMQ)
4. List all services                → 5 containers with all gathered info
5. Write compose.yaml               → services + volumes
6. Cross-validate                   → every value matches source files
7. Download reference file          → compare with yours for errors
```

***

## Key Engineering Patterns

| Pattern                                  | Manifestation                                                                                        |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Requirement gathering before writing** | Collect ALL config from source files → then write compose file. Never guess values                   |
| **Source-of-truth alignment**            | `application.properties` = master config → compose file must mirror it exactly                       |
| **Name-based service discovery**         | Container names = DNS hostnames on compose network → names must match app expectations               |
| **Build+Image dual purpose**             | `build` creates the image, `image` names it for registry push — single directive, two outcomes       |
| **Official image + env vars**            | Standard services (MySQL, RabbitMQ) use official images, customized only through documented env vars |
| **Copy-paste-then-modify**               | Write one service fully, copy for others, change only what differs — efficient but verify carefully  |

***

## Project Continuity

```
BEFORE: Docker Compose concepts (lecture 309) + three Dockerfiles written (db, app, web)
THIS:   Complete compose.yaml written with all 5 services
NEXT:   docker compose up → build images + run all 5 containers together
```

***

This completes the full reconstruction. **Theory** explains the five-container architecture, the `application.properties` alignment rule, and the `build`+`image` dual behavior. **Practical** walks through writing every service block with the exact directives and values. The **Compression Map** gives you the service matrix, the source-of-truth mapping, and the container name rule for instant recall during compose file work. Let me know if you'd like Anki flashcards or any section expanded! 🚀
