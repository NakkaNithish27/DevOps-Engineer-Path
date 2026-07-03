# 🐳 Containerizing a Microservice Project — Dockerfiles, Docker Compose, Multi-Stage Builds, and API Gateway Routing

**Source:** Docker Section — Containerizing Microservice Project (Caption File) [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

This is a **dense, architecturally rich lecture** that walks through the complete containerization of a real microservice e-commerce application (**Emartapp**). The instructor examines the multi-service architecture (NGINX API gateway, Angular client, Node.js API, Java Books API, MongoDB, MySQL), then opens each service's **multi-stage Dockerfile** in VS Code and explains every instruction line by line. He then walks through the **Docker Compose file** that orchestrates all six containers with dependency ordering, port mapping, volumes, and environment variables. The lecture closes with a powerful methodology statement: containerizing = knowing the build process + knowing the hosting method + writing Dockerfiles + Docker Compose. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. The Microservice Architecture — Four Services, Two Databases

The application being containerized is an **e-commerce application (Emartapp)** built with microservice architecture. The instructor walks through the complete architecture: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**NGINX (API Gateway)** — The front door. All user requests arrive here. NGINX listens for requests and **routes** them based on URL paths/headers to the appropriate microservice. It is not an application service — it's the **routing layer** that connects the outside world to the internal microservices. All inter-service communication from external clients flows through this gateway.

The routing rules are: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

* `/` (root path) → **Client** microservice (Angular front-end)
* `/api` → **API** microservice (Node.js back-end)
* `/webapi` → **Books API** microservice (Java back-end)

**Client (Angular)** — The front-end microservice. Written in Angular, it generates HTML pages that load in the user's browser. When a user accesses the root URL, NGINX routes to this service, which serves the website's UI.

**API / Emart API (Node.js)** — The primary back-end microservice. Handles business logic and data operations for the e-commerce functionality. Written in Node.js. Connects to **MongoDB** (NoSQL database) for its data storage.

**Books API / Web API (Java)** — A secondary back-end microservice. Handles the books-related functionality. Written in Java. Connects to **MySQL** (SQL database) for its data storage. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

This architecture demonstrates a key microservice pattern: **each service uses the database technology best suited to its needs** — the Node.js service uses MongoDB (document-oriented, flexible schema), while the Java service uses MySQL (relational, structured schema). They don't share a database.

***

## 2. Mono Repo — All Microservices in One Repository

The source code for all microservices lives in a **single GitHub repository** called `Emartapp`. Inside the repository, each microservice has its own directory: `client/`, `java-api/`, `nginx/`, `node-api/`. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

The instructor introduces the term **"mono repo"** — a repository structure where all microservice source code lives together. He contrasts this with the alternative: **separate repositories** for each microservice, which is beneficial for creating **separate CI/CD pipelines** for each service and promotes **GitOps** practices. The instructor mentions he is creating a separate course for GitOps.

For this lecture, the mono repo approach is used — all Dockerfiles and source code are in one place, making it easy to build and compose everything together. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

## 3. Multi-Stage Dockerfiles — The Build Pattern

Every custom Dockerfile in this project uses **multi-stage builds** — the most important Dockerfile pattern for microservice containerization. The instructor repeats this across three Dockerfiles, making it a core concept. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

A multi-stage Dockerfile has **two (or more) stages**:

**Stage 1: Build Stage** — Uses a build-tool image (Node, Maven/JDK) to compile the source code into an artifact. This stage contains all the build dependencies (compilers, package managers, SDKs) that are needed only during compilation, not at runtime.

**Stage 2: Runtime Stage** — Uses a lightweight runtime image (NGINX, Node, JDK) and copies **only the built artifact** from Stage 1 into it. The final image contains only what's needed to run the application — no build tools, no source code, no compilation dependencies.

The benefit: the final Docker image is **much smaller** because it doesn't contain build tools. The build tools exist only in Stage 1 (which is discarded after the artifact is extracted). [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

The `COPY --from=<stage_name>` instruction is the bridge between stages — it copies files from a named build stage into the current stage.

***

## 4. Client Dockerfile — Angular on NGINX (Multi-Stage)

The Angular client's Dockerfile demonstrates the pattern of **building a front-end app and hosting it on a web server**: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**Stage 1 (Build):** Uses `node:14` image. Copies Angular source code into the container. Runs `npm install` (installs dependencies) and `npm run build --prod` (compiles Angular into static HTML/CSS/JS files). The compiled output (artifact) lands in a `dist/client/` directory.

**Stage 2 (Runtime):** Uses `nginx` image. Copies the compiled static files from Stage 1's `dist/client/` directory into NGINX's HTML serving directory (`/usr/share/nginx/html`). Also copies a custom NGINX configuration file.

The instructor explains **how you know the paths**: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

* The **artifact output path** (`dist/client/`) — comes from the developer / build tool documentation. When you run `npm run build`, the output goes to `dist/`.
* The **NGINX HTML directory** (`/usr/share/nginx/html`) — comes from the **Docker Hub NGINX documentation**. This is where NGINX looks for files to serve.

The custom NGINX config file (inside the client directory) tells NGINX: if someone accesses `/`, serve `index.html` from the configured directory. The `index.html` file is the Angular application's entry point. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

## 5. Node API Dockerfile — Node.js Application (Multi-Stage)

The Node.js API Dockerfile follows the same multi-stage pattern: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**Stage 1 (Build):** Uses `node` image. Copies source code. Runs `npm install` to install dependencies and generate the artifact (the `node_modules` and application files).

**Stage 2 (Runtime):** Uses `node` image again (Node.js is both the build tool and the runtime — unlike Angular, which builds static files for NGINX). Copies the artifact from Stage 1. Exposes port **5000**. Runs `npm start` to start the Node.js application.

The instructor notes: Node.js **"has its own hosting service"** — unlike Angular which needs NGINX to serve static files, Node.js runs its own web server. The artifact and the runtime are both Node-based. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

## 6. Java API Dockerfile — Java/Maven Application (Multi-Stage)

The Java Books API Dockerfile: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**Stage 1 (Build):** Uses `openjdk` image. Installs Maven (`apt update && apt install maven`). Copies source code. Runs `mvn install` to compile Java source code into a JAR artifact. The artifact lands at a path like `book-work-<version>-SNAPSHOT.jar`.

**Stage 2 (Runtime):** Uses `openjdk` image. Copies the JAR artifact from Stage 1 into the working directory with a clean name. Exposes port **9000**. Runs `java -jar <artifact>.jar` to start the Java application.

This mirrors the Vprofile build process from earlier in the course: Maven + JDK compile source code into a deployable artifact. In the VM world, this artifact went into Tomcat. In the container world, it runs directly on JDK using `java -jar`. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

## 7. NGINX API Gateway — No Custom Image, Just Configuration

For the NGINX API gateway (the routing layer), the instructor makes a deliberate architectural decision: **no custom Docker image is built.** Instead, the official NGINX image is used directly, and the custom configuration file is **attached as a volume**. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

The instructor explains the reasoning: **"We don't need to build a separate NGINX image, because all we need is this configuration for the NGINX container to load."** When the only customization is a configuration file, building a custom image is overkill — mounting the config as a volume is simpler and more flexible (you can change the config without rebuilding the image).

The NGINX configuration file (`default.conf`) contains the **three routing rules** that define the API gateway behavior: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

* `/` → routes to the `client` container
* `/api` → routes to the `api` container (Node.js)
* `/webapi` → routes to the `webapi` container (Java)

The container names in the routing rules **must match** the container names defined in Docker Compose — this is how NGINX resolves the upstream services by name via Docker's internal DNS.

***

## 8. Docker Compose — Orchestrating Six Containers

The Docker Compose file defines **six services** (containers) and their relationships: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

| Service         | Image Source                       | Port        | Database Dependency |
| --------------- | ---------------------------------- | ----------- | ------------------- |
| `client`        | Build from `./client` Dockerfile   | 4200:4200   | —                   |
| `api` (Node)    | Build from `./node-api` Dockerfile | 5000:5000   | MongoDB (`emongo`)  |
| `webapi` (Java) | Build from `./java-api` Dockerfile | 9000:9000   | MySQL (`emartdb`)   |
| `nginx`         | Official `nginx` image             | 80:80       | —                   |
| `emongo`        | Official `mongo` image             | 27017:27017 | —                   |
| `emartdb`       | Official `mysql` image             | 3306:3306   | —                   |

### The `depends_on` Chain — Startup Ordering

Docker Compose's `depends_on` controls the **order** in which containers start. The instructor walks through the dependency chain: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

* **`client`** depends on `api` and `webapi` → back-end services start first.
* **`api`** (Node) depends on `nginx` and `emongo` → NGINX gateway and MongoDB start first.
* **`webapi`** (Java) depends on `emartdb` → MySQL starts first.
* **`nginx`** depends on `client` → client container starts first.

This creates a startup order that ensures databases are running before the applications that connect to them, and the gateway starts when services are available.

### The `restart: always` Pattern

The instructor identifies a real-world problem: `depends_on` only controls **startup order**, not **readiness**. Even if the MySQL container starts before the Java API container, MySQL might not be fully initialized (accepting connections) by the time the Java API tries to connect. The solution: **`restart: always`** on the Java API container. If it fails because the database isn't ready, Docker automatically restarts it, and by the next attempt, the database should be accepting connections. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

<details>
<summary>🔍 Deep Dive</summary>

The `depends_on` vs readiness problem is a well-known Docker Compose limitation. `depends_on` ensures container A starts after container B, but it doesn't wait for container B to be "healthy" (accepting connections). Docker Compose v2+ supports `depends_on` with `condition: service_healthy` combined with healthchecks, which is the proper solution. The `restart: always` approach used here is a simpler workaround — the container retries until the dependency is ready. Both approaches work; healthchecks are more elegant.

</details>

### Database Configuration via Environment Variables

Both database containers are configured through environment variables in Docker Compose: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

* **MongoDB (`emongo`):** Sets the database name to `epoc` — this matches the Node.js application's configuration that expects to connect to a database named `epoc`.
* **MySQL (`emartdb`):** Sets `MYSQL_ROOT_PASSWORD=emartdbpass` and database name to `books` — matching the Java application's database connection configuration.

These environment variables come from the Docker Hub documentation for each database image (as covered in the previous base image lecture).

***

## 9. The Containerization Methodology — The Two Things You Need to Know

The instructor closes with the most operationally valuable insight of the entire lecture — the methodology for containerizing **any** application: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**"Two things while writing the Dockerfile: know the build process and the hosting method."**

1. **Build process:** How do you turn source code into a deployable artifact? What commands? What tools? (`npm install`, `npm run build`, `mvn install`, etc.)
2. **Hosting method:** How do you run that artifact? On what runtime? (`nginx` for static HTML, `node` for Node.js apps, `java -jar` for Java apps, `tomcat` for WAR files)

**"Once you know that, your job will be writing Dockerfile and then Docker Compose file to run all of them together."** [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

The instructor repeatedly emphasizes that this information comes from **working with developers**: **"When you work in a project, you need to work with the developer. Understand the build steps and how to host your application."** A DevOps engineer doesn't need to know Angular, Node.js, or Java deeply — they need to know the build commands and hosting patterns. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

## 10. Troubleshooting Expectations

The instructor sets realistic expectations: **"While you're doing this in real time in a project, you may get many errors while you're building and running containers."** Common problems include: [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

* Wrong database username/password
* Wrong database name
* Wrong container name (breaking DNS-based service discovery)
* Configuration errors

The advice: check logs, go through configuration files, be patient, and work with developers. Containerization in real projects is iterative — you write, build, fail, debug, fix, and repeat. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are examining and understanding the complete containerization of a **microservice e-commerce application (Emartapp)** with six containers: Angular client, Node.js API, Java Books API, NGINX API gateway, MongoDB, and MySQL. This lecture walks through all Dockerfiles and the Docker Compose file — the next lecture runs everything together. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**Why it matters:** This is the real-world pattern for containerizing microservices — multiple Dockerfiles, multi-stage builds, Docker Compose orchestration, and API gateway routing. Every production microservice deployment follows this structure.

**Final outcome:** Complete understanding of every Dockerfile instruction and Docker Compose configuration, ready to build and run the full stack in the next lecture.

***

## Step 1: Clone the Source Code and Open in VS Code

**Clone the repository:** [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

```bash
mkdir /f/microsvc
cd /f/microsvc
git clone <repository_URL>
```

If HTTPS cloning fails, use the **SSH URL** instead:

```bash
git clone git@github.com:hkhcoder/emartapp.git
```

**Open in VS Code:**

```bash
cd emartapp
code .
```

* `code .` — Opens VS Code with the current directory as the workspace.

**Expected result:** VS Code opens showing four directories: `client/`, `java-api/`, `nginx/`, `node-api/`. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**Common mistake:** HTTPS clone failing due to authentication — switch to SSH URL (requires SSH key configured with GitHub).

***

## Step 2: Examine the Client Dockerfile (Angular)

**File:** `client/Dockerfile` [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

```dockerfile
# Stage 1: Build
FROM node:14 AS web-build
WORKDIR /usr/src/app
COPY . /client
RUN cd client && npm install && npm run build --prod

# Stage 2: Runtime
FROM nginx
COPY --from=web-build /usr/src/app/client/dist/client /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
```

**Line-by-line breakdown:**

* `FROM node:14 AS web-build` — Stage 1 uses Node.js 14 image. Named `web-build` for reference in Stage 2.
* `WORKDIR /usr/src/app` — Sets the working directory inside the build container.
* `COPY . /client` — Copies all source code from the Docker build context (the `client/` directory) into `/client` inside the container.
* `RUN cd client && npm install && npm run build --prod` — Changes to the client directory, installs Node dependencies, then builds the Angular app in production mode. Output artifact: static HTML/CSS/JS files in `dist/client/`.
* `FROM nginx` — Stage 2 starts fresh with the official NGINX image (no build tools).
* `COPY --from=web-build /usr/src/app/client/dist/client /usr/share/nginx/html` — Copies ONLY the built artifact from Stage 1 into NGINX's serving directory.
* `COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf` — Copies custom NGINX config into the container. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**The custom NGINX config** (inside `client/nginx/default.conf`):

* Tells NGINX: for `/` path → serve files from the HTML directory → load `index.html`.

**Key knowledge sources:**

* Artifact output path (`dist/client/`) → from developer / Angular build docs.
* NGINX HTML directory (`/usr/share/nginx/html`) → from Docker Hub NGINX docs.

***

## Step 3: Examine the Node API Dockerfile

**File:** `node-api/Dockerfile` [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

```dockerfile
# Stage 1: Build
FROM node AS nodeapi-build
WORKDIR /usr/src/app
COPY . /node-api
RUN cd node-api && npm install

# Stage 2: Runtime
FROM node
WORKDIR /usr/src/app
COPY --from=nodeapi-build /usr/src/app/node-api .
RUN ls
EXPOSE 5000
CMD ["npm", "start"]
```

**Key differences from client:**

* Both stages use `node` (Node.js is both build tool and runtime).
* `npm install` generates the artifact (installed dependencies + app code).
* `EXPOSE 5000` — documents that the app listens on port 5000.
* `CMD ["npm", "start"]` — starts the Node.js application. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)
* `RUN ls` — lists files during build (useful for verifying the artifact was copied correctly).

***

## Step 4: Examine the Java API Dockerfile

**File:** `java-api/Dockerfile` [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

```dockerfile
# Stage 1: Build
FROM openjdk:8 AS build
WORKDIR /usr/src/app
RUN apt update && apt install maven -y
COPY . /usr/src/app
RUN mvn install

# Stage 2: Runtime
FROM openjdk:8
WORKDIR /usr/src/app
COPY --from=build /usr/src/app/target/book-work-*-SNAPSHOT.jar ./book-work.jar
EXPOSE 9000
CMD ["java", "-jar", "book-work.jar"]
```

**Key points:**

* Stage 1 installs Maven on top of OpenJDK (Maven isn't in the base OpenJDK image).
* `mvn install` compiles Java source → produces JAR artifact in `target/` directory.
* Stage 2 copies only the JAR file (with a clean name) and runs it with `java -jar`.
* Port **9000** exposed. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

## Step 5: Examine the NGINX API Gateway Configuration

**File:** `nginx/default.conf` [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

```nginx
# Routing rules:
location / {
    proxy_pass http://client:4200;
}
location /api {
    proxy_pass http://api:5000;
}
location /webapi {
    proxy_pass http://webapi:9000;
}
```

**No Dockerfile** for NGINX gateway — uses official image directly. Config mounted as volume in Docker Compose.

**Critical rule:** The hostnames (`client`, `api`, `webapi`) must **exactly match** the container names in Docker Compose. Docker's internal DNS resolves container names to IP addresses. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

***

## Step 6: Examine the Docker Compose File

**File:** `docker-compose.yml` [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**Six services defined:**

### Client (Angular)

```yaml
client:
  build:
    context: ./client
  ports:
    - "4200:4200"
  container_name: client
  depends_on:
    - api
    - webapi
```

### API (Node.js)

```yaml
api:
  build:
    context: ./node-api
  ports:
    - "5000:5000"
  container_name: api
  depends_on:
    - nginx
    - emongo
```

### Web API (Java)

```yaml
webapi:
  build:
    context: ./java-api
  ports:
    - "9000:9000"
  container_name: webapi
  depends_on:
    - emartdb
  restart: always
```

`restart: always` — handles the case where MySQL isn't ready when Java API first starts. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

### NGINX (API Gateway)

```yaml
nginx:
  image: nginx
  container_name: nginx
  ports:
    - "80:80"
  volumes:
    - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
  command: nginx-debug -g 'daemon off;'
  depends_on:
    - client
```

* `volumes` — mounts the local config file into the container (no custom image needed).
* `command` — runs NGINX in debug mode, foreground (daemon off). [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

### MongoDB

```yaml
emongo:
  image: mongo
  container_name: emongo
  environment:
    - MONGO_INITDB_DATABASE=epoc
  ports:
    - "27017:27017"
```

Database name `epoc` matches Node.js app configuration. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

### MySQL

```yaml
emartdb:
  image: mysql
  container_name: emartdb
  environment:
    - MYSQL_ROOT_PASSWORD=emartdbpass
    - MYSQL_DATABASE=books
  ports:
    - "3306:3306"
```

Root password and database name match Java app configuration. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

**Connection to flow:** All Dockerfiles and Docker Compose examined. Next lecture: `docker-compose up` to build and run everything.

<details>
<summary>⚠️ Expert Note</summary>

In production microservice deployments, Docker Compose is replaced by Kubernetes. But the concepts are identical: each service gets a Dockerfile (or Helm chart), orchestration defines dependencies and networking, and configuration is externalized via environment variables or ConfigMaps. Understanding Docker Compose deeply is direct preparation for Kubernetes — the mental model transfers completely.

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   Containerizing a Microservice Application (Emartapp)
CONTEXT: Docker section → microservice containerization → Dockerfiles + Docker Compose
PURPOSE: Understand how to containerize a multi-service application end-to-end
```

***

## Application Architecture

```
USER REQUEST
    ↓
[NGINX API Gateway] (port 80)
    ├── /        → [Client - Angular]    (port 4200)
    ├── /api     → [API - Node.js]       (port 5000) → [MongoDB] (port 27017)
    └── /webapi  → [WebAPI - Java]       (port 9000) → [MySQL]   (port 3306)

6 containers total: 3 custom images + 1 official image (NGINX) + 2 databases
```

***

## Dockerfile Map — Who Gets What

```
CLIENT (Angular):    Multi-stage → node:14 (build) → nginx (serve static HTML)
NODE API:            Multi-stage → node (build) → node (run npm start)
JAVA API:            Multi-stage → openjdk+maven (build) → openjdk (run java -jar)
NGINX GATEWAY:       NO Dockerfile → official nginx image + config volume
MONGODB:             NO Dockerfile → official mongo image + env vars
MYSQL:               NO Dockerfile → official mysql image + env vars
```

***

## Multi-Stage Build Pattern (Universal)

```
STAGE 1 (Build):
  FROM <build-tool-image> AS build-name
  COPY source code
  RUN build commands (npm install, mvn install, etc.)
  → produces ARTIFACT

STAGE 2 (Runtime):
  FROM <lightweight-runtime-image>
  COPY --from=build-name <artifact-path> <destination>
  EXPOSE port
  CMD [run command]

Result: final image has NO build tools, NO source code → small + clean
```

***

## Build Process per Technology

```
Angular:  npm install → npm run build --prod → static HTML in dist/
          Host on: NGINX (/usr/share/nginx/html)

Node.js:  npm install → artifact = node_modules + app code
          Host on: Node itself (npm start) — self-hosting

Java:     mvn install → JAR file in target/
          Host on: JDK (java -jar) or Tomcat
```

***

## Docker Compose Dependency Chain

```
Startup order (depends_on):

emartdb (MySQL)  ←── webapi (Java) ←─┐
emongo (MongoDB) ←── api (Node)    ←─┤── client (Angular) ←── nginx (gateway)
                     nginx ←──────────┘

Databases start FIRST → apps connect → gateway routes

⚠️ depends_on = startup ORDER, not READINESS
   Solution: restart: always on webapi (retry until DB ready)
```

***

## NGINX Gateway Routing Rules

```
/       → proxy_pass http://client:4200     (Angular front-end)
/api    → proxy_pass http://api:5000        (Node.js back-end)
/webapi → proxy_pass http://webapi:9000     (Java Books API)

CRITICAL: hostnames (client, api, webapi) = container_name in Docker Compose
          Docker internal DNS resolves container names → IP addresses
```

***

## Database Config via Environment Variables

```
MongoDB (emongo):
  MONGO_INITDB_DATABASE=epoc        ← must match Node.js app config

MySQL (emartdb):
  MYSQL_ROOT_PASSWORD=emartdbpass   ← must match Java app config
  MYSQL_DATABASE=books              ← must match Java app config
```

***

## Mono Repo vs Multi Repo

```
MONO REPO (this project):
  emartapp/
  ├── client/        (Angular + Dockerfile)
  ├── java-api/      (Java + Dockerfile)
  ├── nginx/         (config only, no Dockerfile)
  └── node-api/      (Node.js + Dockerfile)

MULTI REPO (alternative):
  Each microservice in separate repo
  ✅ separate CI/CD pipelines per service
  ✅ promotes GitOps
```

***

## Custom Image vs Official Image Decision

```
CUSTOM IMAGE (build Dockerfile):
  When you need to inject: source code, artifacts, custom configs baked in
  → Client, Node API, Java API

OFFICIAL IMAGE (use directly):
  When only configuration changes needed (mount as volume)
  → NGINX gateway, MongoDB, MySQL
```

***

## The Containerization Formula

```
CONTAINERIZING = know BUILD PROCESS + know HOSTING METHOD

BUILD PROCESS:  source code → [what commands?] → artifact
                (npm install, mvn install, go build, etc.)
                → get from DEVELOPERS

HOSTING METHOD: artifact → [what runtime?] → running service
                (nginx, node, java -jar, tomcat, python, etc.)
                → get from DEVELOPERS + Docker Hub docs

OUTPUT: Dockerfile (per service) + Docker Compose (orchestration) + configs
```

***

## Key Paths to Know (From Docs + Developers)

```
Angular artifact:     dist/client/              ← build tool output
NGINX HTML dir:       /usr/share/nginx/html     ← Docker Hub NGINX docs
NGINX config:         /etc/nginx/conf.d/        ← Docker Hub NGINX docs
Java artifact:        target/*.jar              ← Maven convention
Node artifact:        node_modules + app files  ← npm convention
```

***

## Common Errors When Containerizing

```
Wrong DB username/password        → app can't authenticate
Wrong database name               → app connects to nonexistent DB
Wrong container name              → NGINX routing fails (DNS resolution fails)
depends_on ≠ readiness            → app starts before DB is ready → crash
Configuration path errors         → wrong volume mount → config not loaded
Build command wrong               → no artifact produced → COPY fails
```

***

## Reusable Engineering Patterns

```
1. MULTI-STAGE BUILD              → Separate build environment from runtime environment
                                     Build tools in Stage 1 (discarded), artifact in Stage 2 (kept)
                                     Result: small, clean, production-ready images

2. API GATEWAY ROUTING            → Single entry point → routes to multiple back-end services
                                     URL path determines which service handles the request
                                     (same pattern: Kubernetes Ingress, AWS ALB, Envoy)

3. VOLUME-OVER-BUILD              → When only config changes needed → mount as volume, don't build image
                                     Faster iteration, simpler pipeline
                                     (same pattern: ConfigMaps in Kubernetes)

4. CONTAINER NAME = DNS NAME      → Docker Compose creates internal DNS
                                     container_name → resolvable hostname
                                     Routing configs reference container names, not IPs

5. RESTART AS RETRY               → restart: always → handles startup race conditions
                                     App fails if DB not ready → restarts → succeeds on retry
                                     (pragmatic workaround for depends_on limitations)

6. KNOW BUILD + KNOW HOST         → DevOps containerization formula
                                     You don't need to know the language deeply
                                     You need: build commands + hosting method + developer collaboration
```

***

## Rapid Recall Triggers

```
"How many containers in Emartapp?"      → 6: client, api, webapi, nginx, emongo, emartdb
"Multi-stage Dockerfile purpose?"       → Build in Stage 1 (heavy), run in Stage 2 (light) → small image
"COPY --from does what?"                → Copies artifact from a named build stage into current stage
"Why no NGINX Dockerfile for gateway?"  → Only need config → mount as volume → simpler
"How does NGINX route to services?"     → proxy_pass to container_name:port → Docker DNS resolves
"depends_on guarantees readiness?"      → NO — only startup order. Use restart:always as workaround
"Database config in Docker Compose?"    → Environment variables (MYSQL_ROOT_PASSWORD, MONGO_INITDB_DATABASE)
"Mono repo?"                            → All microservice code in one repository
"What do you need from developers?"     → Build process (commands) + hosting method (runtime)
"Containerizing formula?"               → Know build + know host → Dockerfile + Docker Compose + configs
"Angular hosted on what?"               → NGINX (static HTML files)
"Node.js hosted on what?"               → Node itself (npm start — self-hosting)
"Java hosted on what?"                  → JDK directly (java -jar) or Tomcat
"Container name matters why?"           → Used as DNS hostname in NGINX routing + inter-service communication
"restart: always solves what?"          → DB not ready when app starts → app fails → auto-restart → succeeds
```

***

This completes the full reconstruction of the Containerizing Microservice Project lecture — the most architecturally complex Docker lecture in the course. **Theory** builds the complete architecture from API gateway through multi-stage builds to the containerization methodology; **Practical** walks through every Dockerfile instruction and Docker Compose configuration line by line; and the **Mental Compression Map** compresses the six-container architecture, dependency chain, routing rules, and the build+host formula into rapid-recall structures. [\[322-contai...ce-project \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/322-containerizing-microservice-project.txt)

Ready for the next lecture (running the full stack with `docker-compose up`), or shall I generate an **AnkiDeck CSV** covering this lecture or the full course series? 🚀
