# 🎓 Deep Learning Material: Docker Build & Publish in GitLab CI/CD Pipeline

**Source:** [199-build-and-publish-docker.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt?EntityRepresentationId=58527607-6828-452d-af5f-6b14bf490a1a) (video caption) + [199.Docker.yml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199.Docker.yml?EntityRepresentationId=51c3ed85-b3b9-480d-b87a-1422a99efc65) (pipeline file) — Video reconstruction covering building a Docker image inside a GitLab CI pipeline using Docker-in-Docker (dind), authenticating to GitLab's built-in Container Registry using predefined CI variables, modifying a Dockerfile for pipeline context, pushing the image, and verifying the result in the registry. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199.Docker.yml)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: From Built Artifact to Deployable Container Image

At this point in the pipeline, earlier stages have already compiled the Java source code (`build-job`), run tests and checkstyle (`test-job`), and performed a filesystem security scan with Trivy (`security-scan`). What exists after those stages is validated source code inside the pipeline's workspace. But validated source code is not a deployable unit. To deploy this application to a container runtime (Docker host, Kubernetes cluster, etc.), you need a **Docker image** — a self-contained, portable package that includes the application artifact, its runtime (Tomcat), and everything needed to run it. This stage exists to transform the pipeline's validated source code into that Docker image and store it somewhere accessible. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## 1.2 GitLab Container Registry: The Integrated Image Store

Every Docker image, once built, must be **pushed** to a container registry — a storage service that holds images and makes them pullable by deployment targets. You could use Docker Hub, Amazon ECR, Google Container Registry, or any third-party registry. But GitLab provides its own **built-in container registry** as part of its ecosystem. It is accessible under **Deploy → Container Registry** in the GitLab project UI. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

The major advantage of using GitLab's own registry is **authentication simplification**. GitLab provides three **predefined CI/CD variables** that are automatically available inside every pipeline job without any manual configuration:

| Variable                | What It Contains                                                       |
| ----------------------- | ---------------------------------------------------------------------- |
| `$CI_REGISTRY`          | The URI of the GitLab container registry (e.g., `registry.gitlab.com`) |
| `$CI_REGISTRY_USER`     | The username for authenticating to the registry                        |
| `$CI_REGISTRY_PASSWORD` | The password/token for authenticating to the registry                  |

Additionally, `$CI_REGISTRY_IMAGE` provides the **full image repository path**, which is structured as: `<registry-endpoint>/<group-name>/<project-name>`. This becomes the image name you tag and push to. You don't need to construct this path manually — GitLab builds it for you from your project's metadata. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

The video emphasizes this as the preferred approach when using GitLab: "When people use GitLab, they use this entire ecosystem — repository, pipelines, container registry, package registry, security, deployment — everything inbuilt." [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## 1.3 Docker-in-Docker (dind): Why You Need Two Containers

This is the most architecturally significant concept in this lecture. When you specify `image: docker:latest` in a GitLab CI job, you get a container that has the **Docker CLI** — the command-line tool that sends instructions like `docker build` and `docker push`. But the CLI alone cannot build images. It needs to talk to a **Docker daemon** — the background service that actually executes build instructions, manages layers, and handles image storage. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

GitLab, for **security reasons**, does not allow the Docker daemon to run directly inside the main job container. Running the daemon in the same container that executes user-provided scripts would give the pipeline elevated privileges over the host, creating a significant security risk. Instead, GitLab requires you to run the Docker daemon as a **sidecar container** using the `services` keyword. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

When you declare:

```yaml
services:
  - docker:dind
```

GitLab launches **two containers** side by side:

1. **Main container** (`docker:latest`) — runs the Docker CLI and your pipeline scripts.
2. **Sidecar container** (`docker:dind`) — runs the Docker daemon service.

The main container connects to the sidecar container's daemon to execute all Docker commands. When you run `docker build` in the script section, the CLI in container 1 sends the build instruction to the daemon in container 2. The daemon does the actual work — pulling base images, executing Dockerfile instructions, assembling layers. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

🔍 **Deep Dive**
`dind` stands for "Docker-in-Docker" — literally running the Docker engine inside a Docker container. The sidecar pattern here means the dind container has its own lifecycle managed by GitLab's runner, starts before the job's script executes, and is available for the duration of the job. In the pipeline logs, you can observe this sequence: GitLab pulls the `docker:latest` image, starts the main container, then pulls the `docker:dind` image, starts the service, and **waits for the service to be up and running** before the CLI attempts any Docker commands. This startup sequencing is handled automatically by the GitLab runner. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## 1.4 TLS Between CLI and Daemon — And Why It's Disabled Here

When the Docker daemon starts inside the `dind` container, by default it generates **TLS certificates** and expects the client (the Docker CLI in the main container) to present those certificates when connecting. This is a security mechanism to ensure only authorized clients can issue commands to the daemon. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

In this pipeline, this TLS handshake is **disabled** by setting:

```yaml
variables:
  DOCKER_TLS_CERTDIR: ""
```

Setting this variable to an empty string tells the `dind` service not to generate TLS certificates and to accept unauthenticated connections. The reasoning given in the video: "Since we are doing all this internally, we don't need to do that. Even if we provide that, it gives a lot of overhead and it's really not required over here." Both containers are ephemeral, exist only during this job, and communicate within GitLab's isolated runner environment — the TLS overhead adds no practical security value in this context. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

⚠️ **Expert Note**
In production or shared runner environments, disabling TLS between the CLI and daemon may not be appropriate. If multiple jobs share infrastructure or if the runner environment is not fully isolated, enabling TLS (by setting `DOCKER_TLS_CERTDIR: "/certs"`) prevents other processes from hijacking the daemon. The trade-off is operational simplicity vs. defense-in-depth. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## 1.5 Image Tagging Strategy: Commit SHA as the Tag

Every Docker image needs a **tag** — a label that distinguishes one version of the image from another. The pipeline uses the **Git commit SHA** as the tag:

```yaml
IMAGE_TAG: $CI_COMMIT_SHA
```

`$CI_COMMIT_SHA` is another predefined GitLab variable that contains the full 40-character hash of the commit that triggered the pipeline. This means every pipeline run produces an image tagged with the exact commit that generated it. The full image reference becomes: `<registry>/<group>/<project>:<commit-sha>`. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199.Docker.yml)

This is a **traceability pattern**: given any running container in production, you can read its image tag, map it back to the exact Git commit, and know precisely what source code is inside it.

***

## 1.6 Docker Login: Secure Authentication via Stdin

The `docker login` command authenticates the CLI to the container registry so that subsequent `docker push` commands are authorized. The authentication approach used here deliberately avoids exposing the password in logs:

```bash
echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin $CI_REGISTRY
```

The `echo` prints the password, but the `|` (pipe) sends it directly as **standard input** to the `docker login` command via the `--password-stdin` flag. The password never appears as a command-line argument (which would be visible in process listings and logs). The video explicitly notes: "It passes it as a standard input, so you will get the password over here without even leaking it in the logs." [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

🔍 **Deep Dive**
After successful login, Docker stores the authentication credentials in a file at `~/.docker/config.json` inside the container. The pipeline logs show this file being created. All subsequent `docker push` commands use this stored credential automatically. Since the container is ephemeral (destroyed after the job), the credential file does not persist beyond the job's lifecycle. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## 1.7 The Dockerfile Modification: From Git Clone to COPY

The project already has a Dockerfile located at `Docker-files/app/multistage/Dockerfile`. However, the **original** version of this Dockerfile was designed to run standalone — it contained instructions to pull (clone) the source code from a GitHub repository. Inside a CI pipeline, this is unnecessary and wrong: the source code is already cloned into the pipeline workspace by GitLab's runner before any job starts. Cloning again from GitHub would mean the Docker image might build from a different version of the code than what the pipeline validated. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

The modification removes the Git clone lines and replaces them with:

```dockerfile
COPY . /app
WORKDIR /app
RUN mvn install
```

* `COPY . /app` — copies **everything** from the current pipeline workspace (which is the cloned repo) into the `/app` directory inside the Maven build container (this is a multistage build — the first stage uses Maven).
* `WORKDIR /app` — sets `/app` as the working directory so subsequent commands execute there.
* `RUN mvn install` — builds the artifact (WAR file) inside the container.

The second stage of the multistage Dockerfile then copies the built artifact from the first stage:

```dockerfile
COPY --from=build /app/target/vprofile-v2.war <tomcat-webapps-path>
```

This copies the WAR file from the build stage into the Tomcat image's default application directory. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

🔍 **Deep Dive**
The **context** in the `docker build` command (the `.` at the end) determines what files are available to `COPY` instructions. The `.` means "current working directory" — which, inside the pipeline container, is the cloned repository root. So `COPY . /app` captures the entire source tree. The `-f` flag points to the Dockerfile at a non-default path (`Docker-files/app/multistage/Dockerfile`), while the context remains the repo root. This separation of Dockerfile location and build context is a standard Docker pattern. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## 1.8 GitLab as a Complete Ecosystem (Overview)

The video closes with a brief tour of GitLab's broader capabilities beyond CI/CD and container registry. This is not deeply taught but is mentioned to encourage exploration:

* **Plan:** Issue tracking, issue boards, milestones — for bug tracking and product enhancement planning. Issues can be linked to commits, merge requests, and pipelines. Wiki for documentation. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)
* **Security:** SAST (Static Application Security Testing), IaC scanning, container scanning, application security testing — built-in security tooling. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)
* **Deploy:** Container Registry (used in this lecture), Package Registry (for non-container artifacts). [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)
* **Operate:** GitLab Agent for connecting to Kubernetes clusters, Terraform integration, Google Cloud integration. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)
* **Monitor:** Alerting integrations with third-party systems, service desk functionality. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

The core message: GitLab is not just a Git host with CI — it is an end-to-end DevOps platform. The instructor encourages spending time exploring these sections before moving to the next lecture. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are adding a `docker-build-publish` stage to an existing GitLab CI pipeline. This stage takes the source code already validated by previous stages (build, test, security scan), builds a Docker image from a multistage Dockerfile, and pushes that image to GitLab's built-in Container Registry. The final outcome: a versioned, deployable Docker image tagged with the Git commit SHA, stored in the project's container registry, ready to be pulled by any container runtime or Kubernetes cluster. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## Step 1: Register the New Stage

Open the pipeline YAML file in VSCode. In the `stages` block at the top, add `docker` after `security`:

```yaml
stages:
  - build
  - test
  - security
  - docker
  - notify
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199.Docker.yml)

This declares the stage's position in the pipeline sequence. The `docker` stage will execute after `security` completes and before `notify`.

**Connection to larger flow:** Stages execute in declared order. The docker stage depends on the security scan completing first (enforced both by stage ordering and by the `needs` keyword in the job definition).

***

## Step 2: Define the Docker Build & Publish Job

Add the following job block after the `security-scan` job:

```yaml
docker-build-publish:
  stage: docker
  image: docker:latest
  services:
    - docker:dind
  needs: [security-scan]
  variables:
    DOCKER_TLS_CERTDIR: ""
    IMAGE_TAG: $CI_COMMIT_SHA
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199.Docker.yml)

**Breakdown:**

| Key                         | Value                                                                        | Purpose |
| --------------------------- | ---------------------------------------------------------------------------- | ------- |
| `stage: docker`             | Assigns this job to the `docker` stage                                       |         |
| `image: docker:latest`      | Main container — provides the Docker CLI                                     |         |
| `services: [docker:dind]`   | Sidecar container — provides the Docker daemon (as explained in Theory §1.3) |         |
| `needs: [security-scan]`    | Explicit dependency — this job starts only after `security-scan` passes      |         |
| `DOCKER_TLS_CERTDIR: ""`    | Disables TLS between CLI and daemon (as explained in Theory §1.4)            |         |
| `IMAGE_TAG: $CI_COMMIT_SHA` | Sets the image tag to the current commit's SHA hash                          |         |

⚠️ `docker:dind` has **no space** — it is `dind`, not `d i n d`. This is the image name for Docker-in-Docker. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**Connection to larger flow:** The two-container architecture (CLI + daemon sidecar) is now established. The variables prepare the tagging strategy and disable unnecessary TLS.

***

## Step 3: Write the Script — Login, Build, Push

Add the `script` section to the job:

```yaml
  script:
    - echo "🔑 Logging in to GitLab Container Registry..."
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin $CI_REGISTRY
    - echo "🐳 Building Docker image with custom Dockerfile..."
    - docker build -f Docker-files/app/multistage/Dockerfile -t $CI_REGISTRY_IMAGE:$IMAGE_TAG .
    - echo "📦 Pushing Docker image => $CI_REGISTRY_IMAGE:$IMAGE_TAG"
    - docker push $CI_REGISTRY_IMAGE:$IMAGE_TAG
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199.Docker.yml)

### 3a. Login Command

```bash
echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin $CI_REGISTRY
```

| Part                           | Meaning                                                            |
| ------------------------------ | ------------------------------------------------------------------ |
| `echo "$CI_REGISTRY_PASSWORD"` | Prints the registry password (GitLab predefined variable)          |
| `\|`                           | Pipes the output as standard input to the next command             |
| `docker login`                 | Authenticates to a container registry                              |
| `-u "$CI_REGISTRY_USER"`       | Username for authentication (GitLab predefined variable)           |
| `--password-stdin`             | Reads the password from standard input instead of the command line |
| `$CI_REGISTRY`                 | The registry URI (e.g., `registry.gitlab.com`)                     |

**What happens internally:** Docker authenticates against the registry and stores credentials in `~/.docker/config.json`. The password is never exposed in logs because it flows through stdin, not as a visible argument. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**How to verify:** The pipeline log should show the login command executing without printing any password. A successful login produces no error output.

### 3b. Build Command

```bash
docker build -f Docker-files/app/multistage/Dockerfile -t $CI_REGISTRY_IMAGE:$IMAGE_TAG .
```

| Part                                        | Meaning                                                  |
| ------------------------------------------- | -------------------------------------------------------- |
| `docker build`                              | Builds a Docker image from a Dockerfile                  |
| `-f Docker-files/app/multistage/Dockerfile` | Path to the Dockerfile (non-default location)            |
| `-t $CI_REGISTRY_IMAGE:$IMAGE_TAG`          | Tags the image with the full registry path + commit SHA  |
| `.`                                         | Build context — current directory (the cloned repo root) |

**What `$CI_REGISTRY_IMAGE:$IMAGE_TAG` expands to:** Something like `registry.gitlab.com/<group>/<project>:<40-char-commit-sha>`. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**What happens internally:** The Docker daemon (in the dind sidecar) reads the Dockerfile, executes each instruction (COPY source code → set WORKDIR → run `mvn install` → copy WAR to Tomcat image), and produces a tagged image.

### 3c. Push Command

```bash
docker push $CI_REGISTRY_IMAGE:$IMAGE_TAG
```

| Part                            | Meaning                                               |
| ------------------------------- | ----------------------------------------------------- |
| `docker push`                   | Uploads the image to the registry                     |
| `$CI_REGISTRY_IMAGE:$IMAGE_TAG` | The full image reference (same tag used during build) |

**What happens internally:** Docker pushes each layer of the image to the GitLab Container Registry. The image becomes available for pulling from any environment with registry access. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**How to verify:** Navigate to **Deploy → Container Registry** in GitLab. Click on the repository. You should see the image with the commit SHA as its tag. You can copy the full image URI from there. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

***

## Step 4: Modify the Dockerfile for Pipeline Context

Open the Dockerfile at `Docker-files/app/multistage/Dockerfile`.

**4a. Remove the Git clone lines:**

The original Dockerfile contains two lines that clone the source code from a GitHub repository. **Remove both lines.** Inside the pipeline, the source code is already present in the workspace — cloning again is redundant and risks building from a different version. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**4b. Add COPY, WORKDIR, and RUN instructions:**

Replace the removed lines with:

```dockerfile
COPY . /app
WORKDIR /app
RUN mvn install
```

| Instruction       | What It Does                                                                         |
| ----------------- | ------------------------------------------------------------------------------------ |
| `COPY . /app`     | Copies all files from the build context (repo root) into `/app` inside the container |
| `WORKDIR /app`    | Sets `/app` as the working directory for subsequent instructions                     |
| `RUN mvn install` | Builds the project artifact (WAR file) inside the container                          |

 [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**4c. Verify the second stage's COPY instruction:**

The second stage should contain:

```dockerfile
COPY --from=build /app/target/vprofile-v2.war <tomcat-default-app-path>
```

The path `/app/target/vprofile-v2.war` must match where Maven outputs the artifact based on the `WORKDIR` you set. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**Save the Dockerfile.**

**Connection to larger flow:** The Dockerfile is now adapted for CI context — it uses locally available source code instead of fetching from an external repository.

***

## Step 5: Commit, Push, and Observe the Pipeline

**5a. Save all files** (pipeline YAML + modified Dockerfile).

**5b. Commit and push:**

Commit message: `Docker build and publish` (or similar). Push to the branch. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**5c. Observe the pipeline:**

Navigate to **CI/CD → Pipelines** in GitLab. The pipeline triggers automatically.

**What to observe in the Docker job logs (in order):**

1. GitLab prepares the executor (Docker).
2. Pulls the `docker:latest` image → starts the main container.
3. Pulls the `docker:dind` image → starts the sidecar service.
4. **Waits** for the dind service to become available.
5. Executes login command → no password visible in output → credentials stored in `~/.docker/config.json`.
6. Executes `docker build` → Dockerfile instructions run sequentially → image assembled.
7. Executes `docker push` → image layers uploaded to GitLab registry.

 [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**5d. Verify the `notify-on-failure` job:**

The `notify-on-failure` job should show as **skipped**. It has `when: on_failure`, meaning it only runs if a previous job failed. If everything passed, it skips — which is the expected behavior. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199.Docker.yml)

***

## Step 6: Verify the Image in the Container Registry

Navigate to **Deploy → Container Registry** in GitLab.

1. You should see a repository matching your project.
2. Click on it — you should see the image tagged with the commit SHA.
3. Copy the full image URI — it follows the format: `registry.gitlab.com/<group>/<project>:<commit-sha>`.

This URI is what you would use in a `docker pull` command, a Kubernetes deployment manifest, or any container runtime configuration to deploy this application. [\[199-build-...ish-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/199-build-and-publish-docker.txt)

**Connection to larger flow:** The pipeline is now complete end-to-end: build → test → security scan → Docker image build & publish → (notify on failure). The application is containerized, versioned, and stored — ready for deployment.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Pipeline Stage Position

```
build-job → test-job ──→ security-scan → docker-build-publish → notify-on-failure
  (maven)    (maven)       (trivy)         (docker+dind)          (on_failure only)
                              │
                        needs: [build-job]
                                              needs: [security-scan]
```

***

## Two-Container Architecture (Core Mental Model)

```
┌──────────────────────────────────────────────┐
│  GitLab Runner Environment                   │
│                                              │
│  ┌─────────────────┐   ┌──────────────────┐  │
│  │  docker:latest   │──▶│  docker:dind      │  │
│  │  (CLI)           │   │  (Daemon)         │  │
│  │                  │   │                   │  │
│  │  script:         │   │  docker service   │  │
│  │  - docker login  │   │  (builds images,  │  │
│  │  - docker build  │   │   manages layers) │  │
│  │  - docker push   │   │                   │  │
│  └─────────────────┘   └──────────────────┘  │
│       MAIN                  SIDECAR           │
│                                              │
│  DOCKER_TLS_CERTDIR: "" (TLS disabled)       │
└──────────────────────────────────────────────┘

WHY two containers? → GitLab security policy: daemon cannot run in main container
```

***

## Authentication Flow

```
$CI_REGISTRY_PASSWORD ──(echo)──▶ pipe (|) ──▶ docker login --password-stdin
                                                    │
                                              -u $CI_REGISTRY_USER
                                              $CI_REGISTRY (URI)
                                                    │
                                                    ▼
                                          ~/.docker/config.json (credentials stored)
                                                    │
                                              ▼ docker push (uses stored creds)

KEY: Password flows through stdin → never appears in logs
```

***

## GitLab Predefined Variables Map

```
$CI_REGISTRY          → Registry URI (e.g., registry.gitlab.com)
$CI_REGISTRY_USER     → Registry username
$CI_REGISTRY_PASSWORD → Registry password/token
$CI_REGISTRY_IMAGE    → <registry>/<group>/<project>  (full repo path)
$CI_COMMIT_SHA        → 40-char commit hash (used as IMAGE_TAG)

Full image ref = $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

***

## Docker Build Command Anatomy

```
docker build -f Docker-files/app/multistage/Dockerfile -t $CI_REGISTRY_IMAGE:$IMAGE_TAG .
             ▲                                          ▲                                 ▲
             Dockerfile path                            Tag (registry/group/project:sha)  Context (repo root)
             (non-default location)                                                       (what COPY can access)
```

***

## Dockerfile Modification (Pipeline Adaptation)

```
BEFORE (standalone):              AFTER (CI pipeline):
  git clone <github-repo>    →      COPY . /app
  cd <repo>                  →      WORKDIR /app
                                    RUN mvn install

WHY: Source code already cloned by GitLab runner → no need to clone again
RISK of keeping old: May build from different code version than pipeline validated
```

***

## Multistage Build Flow

```
Stage 1 (Maven):
  COPY . /app → WORKDIR /app → RUN mvn install
       │
       ▼
  /app/target/vprofile-v2.war  (artifact produced)

Stage 2 (Tomcat):
  COPY --from=build /app/target/vprofile-v2.war → Tomcat webapps dir
       │
       ▼
  Final image: Tomcat + WAR (no Maven, no source code)
```

***

## Pipeline Execution Log Sequence

```
1. Pull docker:latest → start main container
2. Pull docker:dind → start sidecar
3. Wait for dind service ready
4. Run: docker login → creds → config.json created
5. Run: docker build → Dockerfile executed by daemon
6. Run: docker push → layers uploaded to registry
7. Image visible in Deploy → Container Registry
```

***

## Verify Success

```
Pipeline:    All jobs green, notify-on-failure SKIPPED
Registry:    Deploy → Container Registry → repo → image with commit SHA tag
Image URI:   registry.gitlab.com/<group>/<project>:<sha> → usable for pull/deploy
```

***

## Notify-on-Failure Pattern

```yaml
when: on_failure   # Trigger condition
```

```
All jobs pass → notify SKIPPED
Any job fails → notify RUNS → prints error message with $PROJECT_NAME
```

***

## Engineering Patterns

| Pattern                            | Manifestation                                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Sidecar service**                | dind daemon runs alongside CLI container; separation of concerns enforced by platform security               |
| **Credential isolation via stdin** | Password piped through stdin, never as CLI argument → prevents log leakage                                   |
| **Commit-SHA tagging**             | Image tag = commit hash → full traceability from running container back to exact source code                 |
| **Platform-native integration**    | GitLab registry + predefined vars = zero manual credential setup; ecosystem coupling reduces config overhead |
| **Dockerfile context adaptation**  | Same Dockerfile modified for CI: replace external fetch with local COPY → single source of truth             |
| **Multistage build**               | Build tools (Maven) in stage 1, runtime (Tomcat) in stage 2 → final image has no build dependencies          |
| **Conditional notification**       | `when: on_failure` → job exists in pipeline but only activates on failure → silent success, loud failure     |
| **Ephemeral build environment**    | Both containers destroyed after job → credentials, build cache, artifacts don't persist on infrastructure    |

***

## GitLab Ecosystem Map (Breadth Reference)

```
Plan:     Issues, boards, milestones, wiki
Code:     Repository, merge requests
Build:    CI/CD pipelines
Security: SAST, IaC scanning, container scanning, DAST
Deploy:   Container Registry, Package Registry
Operate:  GitLab Agent (K8s), Terraform, Google Cloud
Monitor:  Alerts, Service Desk
```

***

This completes the full reconstruction. **Theory** builds the conceptual model of why two containers are needed and how authentication flows. **Practical** gives you the exact keystrokes and file changes to reproduce the pipeline. **Compression Map** lets you mentally reload the entire Docker-in-Docker pipeline architecture, command anatomy, and variable relationships in under two minutes. Let me know if you'd like Anki flashcards or any section deepened! 🚀
