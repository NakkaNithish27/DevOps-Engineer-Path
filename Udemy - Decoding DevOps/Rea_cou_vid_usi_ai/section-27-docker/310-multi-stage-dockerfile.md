# 🎓 Deep Learning Material: Multi-Stage Dockerfile — Separating Build and Runtime to Minimize Image Size While Automating the Entire Process

**Source:** Video lecture on multi-stage Dockerfiles (from [310-multi-stage-dockerfile.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt?EntityRepresentationId=c5d0aaa6-713d-461c-8c7e-f99346fe29bb) caption file), with Dockerfile reference from [310.MultiStageDockerfile.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt?EntityRepresentationId=58a84717-64db-4ec7-9e7c-901737f1dd24) [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

**Video Context:** This lecture solves a fundamental Docker engineering problem: you need to **build an artifact** (compile Java source code into a `.war` file) and **package it into a runtime image** (Tomcat), but doing both in a single Dockerfile creates a bloated image (1GB+), while doing the build manually outside Docker breaks automation. Multi-stage Dockerfiles solve this by using **two `FROM` instructions** — one image for building (with JDK, Maven, source code, dependencies) and one image for running (with just Tomcat and the artifact). The build image's contents are discarded; only the artifact is copied into the final image. The instructor demonstrates a reduction from 1GB+ to 374MB while fully automating the build.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Build Dependencies Bloat the Runtime Image

The instructor starts with an existing Dockerfile for the vProfile Java application. This Dockerfile uses a Tomcat base image and copies a pre-built `.war` artifact into it. The problem: *"This docker file has one problem. The problem is it's not completely automated. We have to generate the artifact in this step. It copies the artifact. But this artifact needs to be there in this directory. We need to manually build this artifact."* [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

The manual step is: run `mvn install` on the host machine to compile the Java source code into `vprofile-v2.war`, then run `docker build` which copies that file into the image. This breaks automation — you can't just run `docker build` and get a working image; you need a prerequisite manual step.

***

## 1.2 — The Naive Fix and Why It Fails

The obvious fix is to put the build commands directly into the Dockerfile — install JDK, install Maven, clone the source code, run `mvn install`, all inside the same image. The instructor demonstrates this idea but immediately explains why it's problematic: [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

*"The problem with this is this tomcat image will also have the repository that will add to the storage. Then we have MVN install which is going to download lots of dependencies that will be also in the image. We will have target directory that will contain more than just the artifact. So we have many things into this image which is not even required."*

When Maven runs `mvn install`, it downloads hundreds of megabytes of Java library dependencies. The git repository contains all source files, history, and metadata. The `target/` directory contains intermediate compilation files, test reports, and other build outputs. **None of this is needed at runtime** — the running Tomcat application only needs the final `.war` file. But all of it would be baked into the image, making it **over 1GB**. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

The instructor emphasizes the engineering principle: *"we should have as small footprint as possible for the docker image."* Large images are slower to ship (push/pull from registries), consume more storage, and increase the attack surface.

The instructor also explicitly states this approach should never be used in production: *"Production use cases should not have build and the app image in the same docker file. Or should I say you should not have build artifact and the artifact in the same image."* [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## 1.3 — The Dilemma: Automation vs. Image Size

The instructor frames the core tension: [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

* **Option A (manual build):** Small image (just Tomcat + artifact), but requires a manual `mvn install` step before `docker build` — breaks automation.
* **Option B (build in Dockerfile):** Fully automated, but creates a massive image with unnecessary build tools and dependencies.

*"So we cannot do this and we cannot go with the manual step. So what is the solution? Yes, it's multi stage docker file."* [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## 1.4 — Multi-Stage Dockerfile: Two `FROM` Instructions, One Output Image

A multi-stage Dockerfile uses **multiple `FROM` instructions**, each starting a new build stage. Each stage is an independent image build. The key innovation: you can **copy files from one stage to another** using `COPY --from=<stage-name>`, and only the **final stage** becomes the output image. All previous stages are used only during the build process and are **discarded** from the final image. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

The instructor's multi-stage Dockerfile has two stages:

**Stage 1: BUILD\_IMAGE** — Uses `openjdk:8` as the base. Installs Maven, clones the source code, runs `mvn install` to produce the `.war` artifact. This stage contains JDK, Maven, the git repository, all Maven dependencies, and all build outputs. It's named `BUILD_IMAGE` using the `AS` keyword. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

**Stage 2: Final image** — Uses `tomcat:8-jre11` as the base. Removes default Tomcat webapps. Uses `COPY --from=BUILD_IMAGE` to copy **only the artifact** from Stage 1. Exposes port 8080 and starts Tomcat. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

The instructor explains the `COPY --from` mechanism: *"we want to copy our artifact from this build image to this image. For that we use your copy instruction as usual and we say from equal to this build image. So copy from this image, copy the artifact."* [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

The result: the final image is 374MB (just Tomcat + JRE + artifact). The build image is 1GB+ (JDK + Maven + source + dependencies). Since the build image is not the output, its size doesn't matter for shipping. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## 1.5 — The `AS` Keyword: Naming Build Stages

The `FROM openjdk:8 AS BUILD_IMAGE` syntax gives a **name** to the first build stage. This name is referenced later in `COPY --from=BUILD_IMAGE`. Without a name, you'd have to reference stages by index number (0, 1, 2...), which is fragile and unreadable. Naming stages makes the Dockerfile self-documenting. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## 1.6 — Working Directory Behavior in Multi-Stage Builds

The instructor notes an important detail about file paths across stages. When `git clone` runs in the build image, it creates the repository directory relative to the **working directory** of that image. For `openjdk:8`, the default working directory is typically `/` (root). So the cloned repo is at `/vprofile-repo/`, and the artifact is at `/vprofile-repo/target/vprofile-v2.war`. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

When using `COPY --from=BUILD_IMAGE`, the path you specify is **relative to the build image's filesystem**, not the current stage's filesystem. So `COPY --from=BUILD_IMAGE vprofile-repo/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war` means: from the BUILD\_IMAGE's filesystem, take the file at that path and copy it to the final image's Tomcat directory. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

***

## 1.7 — The Size Impact: Concrete Numbers

The instructor shows the actual `docker images` output after building: [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

| Image    | Tag      | Size       | Contains                                  |
| -------- | -------- | ---------- | ----------------------------------------- |
| `appimg` | `v1`     | **374 MB** | Tomcat + JRE + `.war` artifact only       |
| `<none>` | `<none>` | **\~1 GB** | JDK + Maven + git repo + all dependencies |

*"If you do both in the same image, then just add one GB plus 374 MB. So we reduced the footprint of our app image. And we have also automated the entire build process."* [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

The unnamed `<none>` image is the build stage — Docker keeps it in the local cache (for potential reuse/caching), but it's never shipped. Only the named `appimg:v1` is the deliverable. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## 1.8 — When to Use Multi-Stage Dockerfiles

The instructor provides a clear rule: *"Whenever there is a build for any image, app image, front end, back end, wherever there is build, you should have a multistage docker file."* [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

This applies to any compiled language or framework where the build toolchain is heavier than the runtime:

* Java: JDK + Maven/Gradle for build → JRE + Tomcat/app server for runtime
* Go: Go compiler for build → scratch/alpine for runtime
* Node.js: npm + devDependencies for build → node + production modules for runtime
* React/Angular: node + npm + webpack for build → nginx for runtime

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are writing a **multi-stage Dockerfile** that automatically builds the vProfile Java application from source code and packages it into a minimal Tomcat runtime image. The final outcome: running `docker build` produces a fully functional, small (\~374MB) application image without any manual build steps — the entire process from source code to deployable container is automated in one command.

***

## Step 1: Clone the Source Code Repository

```bash
git clone -b docker https://github.com/devopshydclub/vprofile-project.git
cd vprofile-project/Docker-files/app/
```

* `-b docker` — clones the `docker` branch specifically (contains Docker-related files) [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

**Examine the existing Dockerfile:**

```bash
ls
cat Dockerfile
```

This shows the original single-stage Dockerfile that requires a pre-built artifact. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## Step 2: Create the Multi-Stage Dockerfile

**Create a new directory for the multi-stage version:**

```bash
mkdir multistage
cd multistage/
```

**Write the Dockerfile:**

```bash
vim Dockerfile
```

 [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

**Complete multi-stage Dockerfile:**

```dockerfile
## Multistage Dockerfile

# Stage 1: Build
FROM openjdk:8 AS BUILD_IMAGE
RUN apt update && apt install maven -y
RUN git clone -b vp-docker https://github.com/imranvisualpath/vprofile-repo.git
RUN cd vprofile-repo && mvn install

# Stage 2: Runtime
FROM tomcat:8-jre11
RUN rm -rf /usr/local/tomcat/webapps/*
COPY --from=BUILD_IMAGE vprofile-repo/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080
CMD ["catalina.sh", "run"]
```

 [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

### Stage 1 Breakdown (BUILD\_IMAGE):

| Instruction                              | Purpose                                                          |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `FROM openjdk:8 AS BUILD_IMAGE`          | Base image with JDK 8; named `BUILD_IMAGE` for reference         |
| `RUN apt update && apt install maven -y` | Installs Maven build tool (needed for `mvn install`)             |
| `RUN git clone -b vp-docker <repo-url>`  | Clones the source code from the specific branch                  |
| `RUN cd vprofile-repo && mvn install`    | Compiles the source code → produces `.war` artifact in `target/` |

 [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

### Stage 2 Breakdown (Final Image):

| Instruction                                                                                       | Purpose                                                                      |
| ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `FROM tomcat:8-jre11`                                                                             | New base image — Tomcat with JRE 11 (lightweight runtime)                    |
| `RUN rm -rf /usr/local/tomcat/webapps/*`                                                          | Removes Tomcat's default applications                                        |
| `COPY --from=BUILD_IMAGE vprofile-repo/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war` | Copies **only the artifact** from Stage 1 into Tomcat's deployment directory |
| `EXPOSE 8080`                                                                                     | Documents that the container listens on port 8080                            |
| `CMD ["catalina.sh", "run"]`                                                                      | Starts Tomcat when the container runs                                        |

 [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

**Key line — `COPY --from=BUILD_IMAGE`:**

* `--from=BUILD_IMAGE` — specifies which stage to copy from (the named build stage)
* `vprofile-repo/target/vprofile-v2.war` — source path in the BUILD\_IMAGE filesystem (relative to its working directory, which is `/` for openjdk:8)
* `/usr/local/tomcat/webapps/ROOT.war` — destination in the final image (`ROOT.war` means it's the default application served at `/`) [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## Step 3: Build the Image

```bash
docker build -t appimg:v1 .
```

* `docker build` — builds a Docker image from a Dockerfile
* `-t appimg:v1` — tags the image as `appimg` with version `v1`
* `.` — build context is the current directory (where the Dockerfile is) [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

**What happens during build:** [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

1. Docker processes Stage 1 (BUILD\_IMAGE):
   * Pulls `openjdk:8` image
   * Runs `apt update && apt install maven -y`
   * Runs `git clone` — clones the repository
   * Runs `mvn install` — **downloads many dependencies** (this takes significant time on first build)
   * Stage 1 complete — all build outputs exist in the BUILD\_IMAGE layer

2. Docker processes Stage 2 (final image):
   * Pulls `tomcat:8-jre11` image
   * Removes default webapps
   * Copies the `.war` artifact from BUILD\_IMAGE
   * Sets EXPOSE and CMD
   * Stage 2 complete — this becomes the output image tagged as `appimg:v1`

**The Maven download step is the longest part** — it downloads all Java dependencies. The instructor notes: *"it's downloading so many dependencies. All that will be in the build image."* [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

## Step 4: Verify the Results

```bash
docker images
```

 [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt), [\[310.MultiS...Dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310.MultiStageDockerfile.txt)

**Expected output:**

| REPOSITORY | TAG      | SIZE         |
| ---------- | -------- | ------------ |
| `appimg`   | `v1`     | **\~374 MB** |
| `<none>`   | `<none>` | **\~1 GB**   |

 [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

* `appimg:v1` — the final output image (Tomcat + JRE + artifact only) — **this is what you ship**
* `<none>:<none>` — the intermediate build image (JDK + Maven + source + dependencies) — **not shipped, stays local**

**Verification:** The output image is \~374MB. If everything were in one image, it would be \~1.4GB (1GB build + 374MB runtime). The multi-stage approach saved approximately **1GB of image size** while keeping the process fully automated. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept (One-Line Reconstruction)

> **Multi-stage Dockerfile uses multiple `FROM` instructions: one to BUILD the artifact (heavy, discarded), one to RUN it (lightweight, shipped). `COPY --from=<stage>` bridges them.**

***

## 🔷 The Problem Triangle

```
OPTION A: Manual build + COPY artifact
  ✅ Small image
  ❌ Manual step (breaks automation)

OPTION B: Build inside single Dockerfile
  ✅ Fully automated
  ❌ Huge image (1GB+ with JDK, Maven, deps, source)

OPTION C: Multi-stage Dockerfile ← SOLUTION
  ✅ Fully automated
  ✅ Small image (374MB)
  ✅ Only artifact reaches final image
```

***

## 🔷 Multi-Stage Dockerfile Structure

```dockerfile
# STAGE 1: BUILD (heavy, discarded)
FROM openjdk:8 AS BUILD_IMAGE        ← named stage
RUN apt update && apt install maven -y
RUN git clone -b vp-docker <repo>
RUN cd vprofile-repo && mvn install  ← produces .war artifact

# STAGE 2: RUNTIME (lightweight, shipped)
FROM tomcat:8-jre11                  ← new base = new stage
RUN rm -rf /usr/local/tomcat/webapps/*
COPY --from=BUILD_IMAGE              ← copies ONLY artifact from Stage 1
  vprofile-repo/target/vprofile-v2.war
  /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080
CMD ["catalina.sh", "run"]
```

***

## 🔷 What's in Each Image

```
BUILD_IMAGE (~1GB):              FINAL IMAGE (~374MB):
  ├── OpenJDK 8                    ├── Tomcat 8
  ├── Maven                        ├── JRE 11
  ├── Git                          └── vprofile-v2.war (artifact ONLY)
  ├── vprofile-repo/ (full clone)
  ├── ~/.m2/ (Maven dependencies)
  └── target/ (all build outputs)

SHIPPED: Final image only
DISCARDED: Build image (stays in local cache as <none>)
```

***

## 🔷 Key Syntax Elements

```
FROM <image> AS <name>           ← names a build stage
COPY --from=<name> <src> <dst>   ← copies from named stage to current stage

<src> path is relative to the named stage's working directory
<dst> path is in the current (final) stage's filesystem

AS BUILD_IMAGE → COPY --from=BUILD_IMAGE
```

***

## 🔷 Build Command and Output

```bash
docker build -t appimg:v1 .

RESULT:
  appimg:v1     374 MB    ← output image (ship this)
  <none>:<none> ~1 GB     ← build image (local cache only)
```

***

## 🔷 When to Use Multi-Stage

```
RULE: "Wherever there is build, you should have a multi-stage Dockerfile."

LANGUAGE        BUILD STAGE                RUNTIME STAGE
──────────      ────────────────           ────────────────
Java            JDK + Maven/Gradle         JRE + Tomcat/app server
Go              Go compiler                scratch / alpine
Node.js         npm + devDependencies      node + prod modules
React/Angular   node + webpack + npm       nginx
C/C++           gcc/g++ + make             alpine + binary
```

***

## 🔷 Image Size Comparison

```
SINGLE STAGE:  ~1 GB + 374 MB = ~1.4 GB (build + runtime in one)
MULTI STAGE:   374 MB output (build discarded)

SAVINGS: ~1 GB per image
IMPACT:  faster push/pull, less storage, smaller attack surface
```

***

## 🔷 Data Flow Between Stages

```
STAGE 1 (BUILD_IMAGE):
  openjdk:8
    │
    ├── apt install maven
    ├── git clone → /vprofile-repo/
    ├── mvn install → /vprofile-repo/target/vprofile-v2.war
    │
    └── [ENTIRE FILESYSTEM available for COPY --from]

STAGE 2 (FINAL):
  tomcat:8-jre11
    │
    ├── rm default webapps
    ├── COPY --from=BUILD_IMAGE
    │     /vprofile-repo/target/vprofile-v2.war
    │     → /usr/local/tomcat/webapps/ROOT.war
    │
    └── EXPOSE 8080 + CMD catalina.sh run

ONLY the COPY instruction bridges the stages.
Everything else in Stage 1 is INVISIBLE to Stage 2.
```

***

## 🔷 Reusable Engineering Pattern: Build/Runtime Separation

```
PATTERN: Separate Build Environment from Runtime Environment

BUILD ENV (heavy, temporary):
  ├── Compilers, SDKs, build tools
  ├── Source code, dependencies
  └── Intermediate build outputs
  
  PURPOSE: produce the artifact
  LIFECYCLE: used during build, then discarded

RUNTIME ENV (lightweight, permanent):
  ├── Runtime only (JRE, not JDK)
  ├── Application server (Tomcat, nginx)
  └── The artifact (single file)
  
  PURPOSE: run the application
  LIFECYCLE: shipped, deployed, scaled

BRIDGE: COPY --from (Docker)
        cp from build container (manual)
        artifact repository (CI/CD pipeline)

This pattern appears everywhere:
  Docker:    multi-stage Dockerfile
  CI/CD:     build job → artifact → deploy job
  Java:      Maven build → .war/.jar → app server
  Frontend:  npm build → dist/ → nginx
  Go:        go build → binary → scratch container

The principle: build tools ≠ runtime dependencies.
Never ship build tools into production.
```

This is the lecture's foundational insight: the build environment and the runtime environment have **completely different requirements**, and combining them wastes resources and creates risk. Multi-stage Dockerfiles are Docker's native solution to this universal software engineering problem. [\[310-multi-...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/310-multi-stage-dockerfile.txt)
